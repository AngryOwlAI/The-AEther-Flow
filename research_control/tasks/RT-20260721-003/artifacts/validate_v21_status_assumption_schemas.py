#!/usr/bin/env python3
"""Validate the v21 P10-T01 assumption and scientific-status schemas."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260721-003"
ART = TASK / "artifacts"
ASSUMPTION_DOC = ROOT / "research_control/design/v21_assumption_ledger_schema.md"
STATUS_DOC = ROOT / "research_control/design/v21_scientific_status_schema.md"
FIXTURES_PATH = ART / "v21_status_assumption_schema_fixtures.json"
REPORT_PATH = ART / "v21_status_assumption_schema_validation.json"
RECEIPT_PATH = ART / "v21_status_assumption_schema_compact_receipt.json"

ASSUMPTION_SCHEMA_ID = "v21_assumption_ledger_schema_v1"
STATUS_SCHEMA_ID = "v21_scientific_status_schema_v1"
AUTH_META_FIELDS = {"authority_scope", "authority_source_path", "blocked_downstream_claims"}
DIMENSIONS = {
    "existence",
    "uniqueness",
    "naturality",
    "covariance",
    "robustness",
    "dynamics",
    "operational_meaning",
    "empirical_status",
    "mathematical_status",
    "authority",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_contract(path: Path, marker: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"<!-- BEGIN {re.escape(marker)} -->\s*```json\s*(.*?)\s*```\s*<!-- END {re.escape(marker)} -->",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"missing machine contract marker {marker} in {path}")
    value = json.loads(match.group(1))
    if not isinstance(value, dict):
        raise ValueError(f"machine contract {marker} is not an object")
    return value


def pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def apply_case(base: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    record = copy.deepcopy(base)
    for pointer, value in case.get("set", {}).items():
        parts = pointer_parts(pointer)
        cursor: dict[str, Any] = record
        for part in parts[:-1]:
            child = cursor.get(part)
            if not isinstance(child, dict):
                child = {}
                cursor[part] = child
            cursor = child
        cursor[parts[-1]] = copy.deepcopy(value)
    for pointer in case.get("delete", []):
        parts = pointer_parts(pointer)
        cursor: Any = record
        for part in parts[:-1]:
            if not isinstance(cursor, dict) or part not in cursor:
                cursor = None
                break
            cursor = cursor[part]
        if isinstance(cursor, dict):
            cursor.pop(parts[-1], None)
    return record


def get_path(record: dict[str, Any], dotted: str) -> tuple[bool, Any]:
    cursor: Any = record
    for part in dotted.split("."):
        if not isinstance(cursor, dict) or part not in cursor:
            return False, None
        cursor = cursor[part]
    return True, cursor


def add_error(errors: list[dict[str, str]], rule_id: str, detail: str) -> None:
    errors.append({"rule_id": rule_id, "detail": detail})


def validate_authorization(
    record: dict[str, Any],
    contract: dict[str, Any],
    prefix: str,
    errors: list[dict[str, str]],
) -> None:
    explicit_rule = f"{prefix}_authorization_explicit"
    promotion_rule = f"{prefix}_no_implicit_physics_promotion"
    auth = record.get("authorization_layers")
    boolean_fields = set(contract.get("authorization_boolean_fields", []))
    if not isinstance(auth, dict):
        add_error(errors, explicit_rule, "authorization_layers must be an object")
        return
    expected_keys = boolean_fields | AUTH_META_FIELDS
    if set(auth) != expected_keys:
        add_error(errors, explicit_rule, f"authorization keys differ: {sorted(set(auth) ^ expected_keys)}")
    bad_types = [name for name in boolean_fields if not isinstance(auth.get(name), bool)]
    if bad_types:
        add_error(errors, explicit_rule, f"authorization fields are not booleans: {sorted(bad_types)}")
    true_fields = [name for name in boolean_fields if auth.get(name) is True]
    if true_fields:
        authority = record.get("authority", {})
        protected = (
            authority.get("authority_kind") == "protected_human_gate"
            and bool(authority.get("authority_refs"))
            and bool(authority.get("authority_scope"))
            and bool(authority.get("gate_id"))
            and bool(auth.get("authority_scope"))
            and bool(auth.get("authority_source_path"))
            and bool(auth.get("blocked_downstream_claims"))
        )
        if not protected:
            add_error(
                errors,
                promotion_rule,
                f"true authorization fields lack exact protected authority: {sorted(true_fields)}",
            )


def validate_legacy(
    record: dict[str, Any],
    contract: dict[str, Any],
    prefix: str,
    errors: list[dict[str, str]],
) -> None:
    exact_rule = f"{prefix}_legacy_mapping_exact"
    preserve_rule = f"{prefix}_legacy_raw_preserved"
    legacy = record.get("legacy_compatibility")
    if not isinstance(legacy, dict):
        add_error(errors, exact_rule, "legacy_compatibility must be an object")
        return
    if legacy.get("mapping_authority") != "compatibility_only":
        add_error(errors, exact_rule, "mapping_authority must be compatibility_only")
    if legacy.get("historical_record_rewritten") is not False:
        add_error(errors, preserve_rule, "historical_record_rewritten must be false")
    raw = legacy.get("raw_label")
    source_ref = legacy.get("source_record_ref")
    mapped = legacy.get("mapped_fields")
    if raw is None:
        if source_ref not in (None, "") or mapped != {}:
            add_error(errors, exact_rule, "null raw label requires empty source ref and mapping")
        return
    expected = contract.get("legacy_mapping", {}).get(raw)
    if expected is None:
        add_error(errors, exact_rule, f"unknown legacy label: {raw}")
    elif mapped != expected:
        add_error(errors, exact_rule, f"legacy mapping differs for {raw}")
    if not isinstance(source_ref, str) or not source_ref.strip():
        add_error(errors, preserve_rule, "historical mapping requires its source record reference")


def validate_assumption(record: dict[str, Any], contract: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    missing = [path for path in contract["required_paths"] if not get_path(record, path)[0]]
    if missing:
        add_error(errors, "assumption_required_paths", f"missing paths: {missing}")

    enums = contract["enums"]
    enum_values = {
        "assumption_kind": record.get("assumption_kind"),
        "subject_scope": record.get("subject_scope"),
        "derivation_role": record.get("derivation_role"),
        "disposition": record.get("disposition"),
        "authority_status": record.get("authority_status"),
        "provenance_kind": record.get("provenance", {}).get("provenance_kind"),
        "authority_kind": record.get("authority", {}).get("authority_kind"),
        "continuation_status": record.get("blocking", {}).get("continuation_status"),
    }
    bad_enums = {name: value for name, value in enum_values.items() if value not in enums.get(name, [])}
    if bad_enums:
        add_error(errors, "assumption_known_enums", f"unknown enum values: {bad_enums}")

    role_by_kind = {
        "primitive": "source_premise",
        "derived": "derived_consequence",
        "auxiliary": "auxiliary_device",
        "benchmark": "target_benchmark_only",
    }
    kind = record.get("assumption_kind")
    if kind in role_by_kind and record.get("derivation_role") != role_by_kind[kind]:
        add_error(errors, "assumption_kind_role_alignment", f"{kind} has incompatible derivation role")

    provenance = record.get("provenance", {})
    provenance_kind = provenance.get("provenance_kind")
    source_refs = provenance.get("source_refs")
    source_hashes = provenance.get("source_hashes")
    if provenance_kind == "missing_source":
        if source_refs or source_hashes:
            add_error(errors, "assumption_missing_source_exclusive", "missing_source must not carry source refs or hashes")
        if not isinstance(provenance.get("missing_reason"), str) or not provenance.get("missing_reason", "").strip():
            add_error(errors, "assumption_missing_source_exclusive", "missing_source requires a precise reason")
    elif provenance_kind in enums.get("provenance_kind", []):
        valid_sources = isinstance(source_refs, list) and bool(source_refs)
        valid_hashes = (
            isinstance(source_hashes, dict)
            and isinstance(source_refs, list)
            and set(source_hashes) == set(source_refs)
            and all(isinstance(value, str) and SHA256_RE.fullmatch(value) for value in source_hashes.values())
        )
        if not valid_sources or not valid_hashes:
            add_error(errors, "assumption_provenance_source_required", "non-missing provenance requires keyed source refs and SHA-256 hashes")
        if provenance_kind == "constructed_draft" and not provenance.get("constructed_from"):
            add_error(errors, "assumption_provenance_source_required", "constructed_draft requires constructed_from inputs")

    if kind == "derived":
        derivation = record.get("derivation", {})
        if not derivation.get("dependency_ids") or not derivation.get("certificate_refs"):
            add_error(errors, "assumption_derived_certificate_required", "derived record requires dependencies and certificate refs")
    if kind == "benchmark" and (
        record.get("subject_scope") != "target_benchmark"
        or record.get("derivation_role") != "target_benchmark_only"
    ):
        add_error(errors, "assumption_benchmark_target_only", "benchmark records are target-benchmark-only")

    disposition = record.get("disposition")
    blocking = record.get("blocking", {})
    if disposition == "blocked_adoption_open_continuation" and (
        not blocking.get("burden_ids")
        or blocking.get("continuation_status") != "blocked_adoption_open_continuation"
    ):
        add_error(errors, "assumption_blocked_burden_required", "blocked adoption requires burdens and open-continuation status")

    authority_status = record.get("authority_status")
    refutation = record.get("refutation", {})
    if disposition in {"rejected", "frozen_negative"} or authority_status in {"rejected", "frozen_negative"}:
        if not refutation.get("scope") or not refutation.get("evidence_refs"):
            add_error(errors, "assumption_refutation_scope_required", "negative disposition requires exact refutation scope and evidence")
    if refutation.get("global_no_go_established") is True and not any(
        str(ref).startswith("THEOREM-GLOBAL-") for ref in refutation.get("evidence_refs", [])
    ):
        add_error(errors, "assumption_refutation_scope_required", "global no-go requires an exact global theorem reference")

    authority = record.get("authority", {})
    if disposition == "human_gated" or authority_status == "human_gated":
        if not authority.get("gate_id") or not authority.get("authority_refs"):
            add_error(errors, "assumption_human_gate_required", "human-gated status requires a named gate and control reference")
    if authority_status == "canonical_ontology_candidate" and not (
        authority.get("authority_kind") == "protected_human_gate"
        and authority.get("gate_id")
        and authority.get("authority_refs")
        and authority.get("authority_scope")
    ):
        add_error(errors, "assumption_protected_candidate_required", "canonical-ontology candidate requires protected human-gate authority")
    if disposition == "adopted" or authority_status == "adopted":
        scope = record.get("subject_scope")
        protected = authority.get("authority_kind") == "protected_human_gate" and authority.get("gate_id")
        target_authority = scope == "target_benchmark" and authority.get("authority_kind") == "registered_canonical_science"
        if not (protected or target_authority) or not authority.get("authority_refs") or not authority.get("authority_scope"):
            add_error(errors, "assumption_adoption_authority_required", "adoption requires exact protected or target-benchmark authority")

    display_labels = contract.get("project_status_labels", {})
    if authority_status in display_labels and record.get("project_status_label") != display_labels[authority_status]:
        add_error(errors, "assumption_project_label_exact", "project status display label differs from the exact vocabulary")

    validate_legacy(record, contract, "assumption", errors)
    validate_authorization(record, contract, "assumption", errors)
    if not isinstance(record.get("forbidden_conclusions"), list) or not record.get("forbidden_conclusions"):
        add_error(errors, "assumption_required_paths", "forbidden_conclusions must be nonempty")
    return errors


def validate_scientific_status(record: dict[str, Any], contract: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    missing = [path for path in contract["required_paths"] if not get_path(record, path)[0]]
    if missing:
        add_error(errors, "scientific_status_required_paths", f"missing paths: {missing}")

    enums = contract["enums"]
    dimensions = record.get("dimensions")
    evidence = record.get("evidence_by_dimension")
    bad_enums: dict[str, Any] = {}
    if not isinstance(dimensions, dict) or set(dimensions) != DIMENSIONS:
        bad_enums["dimension_keys"] = sorted(set(dimensions or {}) ^ DIMENSIONS) if isinstance(dimensions, dict) else "not_an_object"
    else:
        for name in DIMENSIONS:
            if dimensions.get(name) not in enums.get(name, []):
                bad_enums[name] = dimensions.get(name)
    if record.get("subject_scope") not in enums.get("subject_scope", []):
        bad_enums["subject_scope"] = record.get("subject_scope")
    if record.get("authority", {}).get("authority_kind") not in enums.get("authority_kind", []):
        bad_enums["authority_kind"] = record.get("authority", {}).get("authority_kind")
    if bad_enums:
        add_error(errors, "scientific_status_known_enums", f"unknown enum values or dimensions: {bad_enums}")

    if not isinstance(evidence, dict) or set(evidence) != DIMENSIONS or any(
        not isinstance(evidence.get(name), list) for name in DIMENSIONS
    ):
        add_error(errors, "scientific_status_dimension_evidence_required", "evidence_by_dimension must contain exactly one list per dimension")
    elif isinstance(dimensions, dict):
        missing_evidence = [
            name
            for name, required_statuses in contract.get("evidence_required_statuses", {}).items()
            if dimensions.get(name) in required_statuses and not evidence.get(name)
        ]
        if missing_evidence:
            add_error(errors, "scientific_status_dimension_evidence_required", f"strong statuses lack dimension evidence: {missing_evidence}")

    dimensions = dimensions if isinstance(dimensions, dict) else {}
    existence = dimensions.get("existence")
    incompatible = []
    if existence in {"absent", "refuted"}:
        for name, values in {
            "uniqueness": {"unique"},
            "naturality": {"derived"},
            "dynamics": {"derived", "validated"},
            "operational_meaning": {"derived", "validated"},
        }.items():
            if dimensions.get(name) in values:
                incompatible.append(f"{name}={dimensions.get(name)}")
    if incompatible:
        add_error(errors, "scientific_status_existence_consistency", f"{existence} conflicts with {incompatible}")
    if dimensions.get("uniqueness") == "unique" and existence != "established":
        add_error(errors, "scientific_status_unique_requires_existence", "unique requires established existence")
    if dimensions.get("mathematical_status") == "proved" and not record.get("theorem_ids"):
        add_error(errors, "scientific_status_proof_reference_required", "proved requires at least one theorem id")
    if dimensions.get("empirical_status") in {"supported", "disfavored", "refuted"} and not (
        isinstance(evidence, dict) and evidence.get("empirical_status")
    ):
        add_error(errors, "scientific_status_empirical_evidence_required", "empirical status requires empirical evidence")

    authority_status = dimensions.get("authority")
    refuted_dimensions = [name for name, value in dimensions.items() if value == "refuted"]
    refutation = record.get("refutation", {})
    if refuted_dimensions or authority_status in {"rejected", "frozen_negative"}:
        if not refutation.get("scope") or not refutation.get("evidence_refs"):
            add_error(errors, "scientific_status_refutation_scope_required", f"negative statuses require exact scope and evidence: {refuted_dimensions}")
    if refutation.get("global_no_go_established") is True and not any(
        str(ref).startswith("THEOREM-GLOBAL-") for ref in refutation.get("evidence_refs", [])
    ):
        add_error(errors, "scientific_status_refutation_scope_required", "global no-go requires an exact global theorem reference")

    authority = record.get("authority", {})
    if authority_status == "human_gated" and (not authority.get("gate_id") or not authority.get("authority_refs")):
        add_error(errors, "scientific_status_human_gate_required", "human-gated authority requires a named gate and control reference")
    if authority_status == "canonical_ontology_candidate" and not (
        authority.get("authority_kind") == "protected_human_gate"
        and authority.get("gate_id")
        and authority.get("authority_refs")
        and authority.get("authority_scope")
    ):
        add_error(errors, "scientific_status_protected_candidate_required", "canonical-ontology candidate requires protected human-gate authority")
    if authority_status == "adopted":
        scope = record.get("subject_scope")
        protected = authority.get("authority_kind") == "protected_human_gate" and authority.get("gate_id")
        target_authority = scope == "target_benchmark" and authority.get("authority_kind") == "registered_canonical_science"
        if not (protected or target_authority) or not authority.get("authority_refs") or not authority.get("authority_scope"):
            add_error(errors, "scientific_status_adoption_authority_required", "adoption requires exact protected or target-benchmark authority")

    validate_legacy(record, contract, "scientific_status", errors)
    validate_authorization(record, contract, "scientific_status", errors)
    if not isinstance(record.get("candidate_ids"), list) or not isinstance(record.get("theorem_ids"), list):
        add_error(errors, "scientific_status_required_paths", "candidate_ids and theorem_ids must be lists")
    if not isinstance(record.get("forbidden_conclusions"), list) or not record.get("forbidden_conclusions"):
        add_error(errors, "scientific_status_required_paths", "forbidden_conclusions must be nonempty")
    return errors


def evaluate_cases(
    base: dict[str, Any],
    cases: list[dict[str, Any]],
    validator: Any,
    contract: dict[str, Any],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for case in cases:
        record = apply_case(base, case)
        errors = validator(record, contract)
        actual_status = "PASS" if not errors else "FAIL"
        actual_ids = sorted({error["rule_id"] for error in errors})
        expected_ids = sorted(case.get("expected_error_ids", []))
        expectation_met = actual_status == case["expected_status"] and set(expected_ids).issubset(actual_ids)
        results.append(
            {
                "fixture_id": case["fixture_id"],
                "expected_status": case["expected_status"],
                "actual_status": actual_status,
                "expected_error_ids": expected_ids,
                "actual_error_ids": actual_ids,
                "expectation_met": expectation_met,
                "errors": errors,
            }
        )
    return results


def build_outputs() -> tuple[dict[str, Any], dict[str, Any]]:
    assumption_contract = extract_contract(ASSUMPTION_DOC, "V21_ASSUMPTION_SCHEMA_JSON")
    status_contract = extract_contract(STATUS_DOC, "V21_SCIENTIFIC_STATUS_SCHEMA_JSON")
    fixtures = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    check("assumption_schema_id", assumption_contract.get("schema_id") == ASSUMPTION_SCHEMA_ID, str(assumption_contract.get("schema_id")))
    check("scientific_status_schema_id", status_contract.get("schema_id") == STATUS_SCHEMA_ID, str(status_contract.get("schema_id")))
    check("scientific_status_axes", set(status_contract.get("evidence_required_statuses", {})) == DIMENSIONS, "all ten orthogonal dimensions are declared")
    expected_legacy = {"accepted", "draft", "evidence", "proposal", "adopted", "frozen"}
    check("assumption_legacy_labels", set(assumption_contract.get("legacy_mapping", {})) == expected_legacy, "six exact legacy labels")
    check("scientific_status_legacy_labels", set(status_contract.get("legacy_mapping", {})) == expected_legacy, "six exact legacy labels")
    check(
        "authorization_layers_aligned",
        assumption_contract.get("authorization_boolean_fields") == status_contract.get("authorization_boolean_fields")
        and len(assumption_contract.get("authorization_boolean_fields", [])) == 15,
        "both schemas use the fifteen v16 authorization booleans",
    )

    assumption_results = evaluate_cases(
        fixtures["base_records"]["assumption"],
        fixtures["assumption_cases"],
        validate_assumption,
        assumption_contract,
    )
    status_results = evaluate_cases(
        fixtures["base_records"]["scientific_status"],
        fixtures["scientific_status_cases"],
        validate_scientific_status,
        status_contract,
    )
    bad_assumption = [row["fixture_id"] for row in assumption_results if not row["expectation_met"]]
    bad_status = [row["fixture_id"] for row in status_results if not row["expectation_met"]]
    check("assumption_fixture_expectations", not bad_assumption, f"unexpected fixtures={bad_assumption}")
    check("scientific_status_fixture_expectations", not bad_status, f"unexpected fixtures={bad_status}")

    legacy_results = []
    for case in fixtures["legacy_mapping_cases"]:
        raw = case["raw_label"]
        assumption_ok = assumption_contract["legacy_mapping"].get(raw) == case["expected_assumption_mapping"]
        status_ok = status_contract["legacy_mapping"].get(raw) == case["expected_scientific_mapping"]
        legacy_results.append({"raw_label": raw, "assumption_mapping_exact": assumption_ok, "scientific_mapping_exact": status_ok})
    check("legacy_compatibility_fixtures", all(row["assumption_mapping_exact"] and row["scientific_mapping_exact"] for row in legacy_results), "all six raw labels map exactly")

    proved_case = next(row for row in status_results if row["fixture_id"] == "S-PASS-PROVED-WITHOUT-PROMOTION")
    check("no_implicit_physics_promotion", proved_case["actual_status"] == "PASS", "proved fixture passes with all promotion flags false")
    check(
        "unknown_enum_fail_closed",
        all(
            next(row for row in results if row["fixture_id"] == fixture_id)["actual_status"] == "FAIL"
            for results, fixture_id in [
                (assumption_results, "A-FAIL-UNKNOWN-KIND"),
                (status_results, "S-FAIL-UNKNOWN-ENUM"),
                (status_results, "S-FAIL-UNKNOWN-DIMENSION"),
            ]
        ),
        "unknown enums and dimensions fail closed",
    )
    check(
        "contradictions_fail_closed",
        all(
            next(row for row in results if row["fixture_id"] == fixture_id)["actual_status"] == "FAIL"
            for results, fixture_id in [
                (assumption_results, "A-FAIL-DERIVED-WITHOUT-CERTIFICATE"),
                (assumption_results, "A-FAIL-BENCHMARK-SMUGGLED-AS-SOURCE"),
                (status_results, "S-FAIL-ABSENT-BUT-UNIQUE"),
                (status_results, "S-FAIL-SOURCE-ADOPTION-WITHOUT-PROTECTED-AUTHORITY"),
            ]
        ),
        "selected structural and authority contradictions fail closed",
    )

    failed_checks = [row for row in checks if row["status"] == "FAIL"]
    failed_fixture_count = sum(not row["expectation_met"] for row in assumption_results + status_results)
    status = "PASS" if not failed_checks and failed_fixture_count == 0 else "FAIL"
    source_hashes = {
        str(ASSUMPTION_DOC.relative_to(ROOT)): sha256(ASSUMPTION_DOC),
        str(STATUS_DOC.relative_to(ROOT)): sha256(STATUS_DOC),
        str(FIXTURES_PATH.relative_to(ROOT)): sha256(FIXTURES_PATH),
        str(Path(__file__).resolve().relative_to(ROOT)): sha256(Path(__file__).resolve()),
    }
    report = {
        "schema_id": "v21_status_assumption_schema_validation_v1",
        "task_id": "RT-20260721-003",
        "job_id": "AJ-RT-20260721-003-001",
        "claim_boundary_id": "CB-V21-P10-T01-STATUS-ASSUMPTION-SCHEMAS-001",
        "status": status,
        "source_hashes": source_hashes,
        "passed_check_count": len(checks) - len(failed_checks),
        "failed_check_count": len(failed_checks),
        "fixture_counts": {
            "assumption_total": len(assumption_results),
            "assumption_positive": sum(row["expected_status"] == "PASS" for row in assumption_results),
            "assumption_negative": sum(row["expected_status"] == "FAIL" for row in assumption_results),
            "scientific_status_total": len(status_results),
            "scientific_status_positive": sum(row["expected_status"] == "PASS" for row in status_results),
            "scientific_status_negative": sum(row["expected_status"] == "FAIL" for row in status_results),
            "legacy_mapping_total": len(legacy_results),
            "unexpected_fixture_results": failed_fixture_count,
        },
        "checks": checks,
        "assumption_fixture_results": assumption_results,
        "scientific_status_fixture_results": status_results,
        "legacy_mapping_results": legacy_results,
        "boundary": "Operational schema validation only; no historical rewrite, scientific proof, ontology adoption, or physics promotion authority.",
    }
    receipt = {
        "schema_id": "v21_status_assumption_schema_compact_receipt_v1",
        "task_id": "RT-20260721-003",
        "job_id": "AJ-RT-20260721-003-001",
        "plan_task_id": "P10-T01",
        "claim_boundary_id": "CB-V21-P10-T01-STATUS-ASSUMPTION-SCHEMAS-001",
        "result_status": status,
        "source_hashes": source_hashes,
        "finding_counts": {
            "schema_contracts": 2,
            "orthogonal_scientific_status_dimensions": 10,
            "authorization_boolean_fields": 15,
            "legacy_labels_mapped": len(legacy_results),
            "positive_fixtures": sum(row["expected_status"] == "PASS" for row in assumption_results + status_results),
            "negative_fixtures": sum(row["expected_status"] == "FAIL" for row in assumption_results + status_results),
            "unexpected_fixture_results": failed_fixture_count,
            "failed_validator_checks": len(failed_checks),
        },
        "validator_ids": assumption_contract["conditional_rule_ids"] + status_contract["conditional_rule_ids"],
        "recommendation_ids": ["V21-R31", "V21-R32", "V21-R33", "V21-R61", "V21-R63"],
        "assumption_delta": {
            "historical_records_rewritten": 0,
            "existing_assumptions_reclassified": 0,
            "assumptions_adopted": 0,
            "new_schema_contracts": 2
        },
        "candidate_or_theorem_identities": {
            "candidate_ids_created": [],
            "theorem_ids_created": [],
            "note": "P10-T01 defines schemas and fixtures only."
        },
        "authority_flags": {
            "scientific_claims_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "historical_record_rewrite_authorized": False
        },
        "forbidden_conclusions": [
            "Schema or validator PASS does not prove any scientific proposition.",
            "Legacy compatibility mappings do not reinterpret historical claims.",
            "No ontology, source law, metric, coupling, Einstein equation, benchmark, or completed derivation is adopted or promoted."
        ],
        "claim_boundary_summary": "P10-T01 implements additive project-control schemas, fixtures, and validation only; all protected scientific authority remains unchanged."
    }
    return report, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        report, receipt = build_outputs()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        failure = {"status": "FAIL", "error": str(exc)}
        print(json.dumps(failure, indent=2) if args.json else f"FAIL: {exc}")
        return 1

    generated = {
        REPORT_PATH: json.dumps(report, indent=2) + "\n",
        RECEIPT_PATH: json.dumps(receipt, indent=2) + "\n",
    }
    stale: list[str] = []
    if args.write:
        for path, content in generated.items():
            path.write_text(content, encoding="utf-8")
    else:
        for path, content in generated.items():
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))

    output = {
        "status": "PASS" if report["status"] == "PASS" and not stale else "FAIL",
        "mode": "write" if args.write else "check",
        "stale_outputs": stale,
        "report": report,
        "receipt": receipt,
    }
    print(json.dumps(output, indent=2) if args.json else output["status"])
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
