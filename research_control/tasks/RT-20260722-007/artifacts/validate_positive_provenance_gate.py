#!/usr/bin/env python3
"""Validate the v21 P11-T05 positive-provenance gate and its fixtures."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260722-007"
ART = TASK / "artifacts"
POLICY_PATH = ART / "positive_provenance_operational_meaning_gate_policy.md"
FIXTURES_PATH = ART / "positive_provenance_gate_fixtures.json"
EXTENSIONS_PATH = ART / "gate_b_c_positive_provenance_extensions.json"
REPORT_PATH = ART / "positive_provenance_gate_validation.json"
RECEIPT_PATH = ART / "positive_provenance_gate_compact_receipt.json"
VALIDATOR_PATH = Path(__file__).resolve()

CONTRACT_ID = "v21_positive_provenance_operational_meaning_gate_v1"
CONTRACT_MARKER = "V21_POSITIVE_PROVENANCE_GATE_SCHEMA_JSON"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def extract_contract(path: Path = POLICY_PATH) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"<!-- BEGIN {re.escape(CONTRACT_MARKER)} -->\s*```json\s*(.*?)\s*```\s*<!-- END {re.escape(CONTRACT_MARKER)} -->",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"missing machine contract marker {CONTRACT_MARKER}")
    contract = json.loads(match.group(1))
    if not isinstance(contract, dict):
        raise ValueError("machine contract must be an object")
    return contract


def load_fixtures(path: Path = FIXTURES_PATH) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("fixture suite must be an object")
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


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def validate_contract(contract: dict[str, Any]) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    required_dimensions = {
        "source_derivation",
        "uniqueness_or_quotient",
        "naturality",
        "dynamics",
        "operational_systems",
        "robustness",
        "independent_review",
    }
    expected_surfaces = {
        "effective_metric",
        "detector_semantics",
        "matter_coupling",
        "field_equations",
    }
    flags = contract.get("policy_flags", {})
    profiles = contract.get("gate_profiles", {})
    integration = contract.get("review_surface_integration", {})
    checks.extend(
        [
            ("contract_id", contract.get("schema_id") == CONTRACT_ID, "schema id is exact"),
            ("contract_version", contract.get("schema_version") == 1, "schema version is one"),
            ("required_dimensions", set(contract.get("required_dimensions", [])) == required_dimensions, "all seven positive-evidence dimensions are present"),
            ("gate_profiles", set(profiles) == {"gate_b", "gate_c"}, "Gate B and Gate C profiles are both present"),
            ("surface_integration", set(integration) == expected_surfaces, "all four review surfaces are integrated"),
            ("surface_dimensions", all(set(value) == required_dimensions for value in integration.values()), "every review surface carries all seven dimensions"),
            ("no_target_required", flags.get("no_target_purity_required_for_evidence_complete") is True, "no-target purity is necessary"),
            ("no_target_not_sufficient", flags.get("no_target_purity_sufficient_for_evidence_complete") is False, "no-target purity is not sufficient"),
            ("validator_not_sufficient", flags.get("validator_pass_sufficient_for_evidence_complete") is False, "validator PASS is not sufficient"),
            ("scoped_candidates", flags.get("scoped_candidates_remain_representable") is True, "scoped candidates remain representable"),
            ("na_distinct", flags.get("not_applicable_distinct_from_missing") is True, "not-applicable differs from missing"),
            ("na_not_ready", flags.get("core_dimension_not_applicable_can_complete_gate") is False, "not-applicable cannot complete a core dimension"),
            ("no_promotion", flags.get("gate_evidence_completion_is_physical_promotion") is False, "evidence completion is not physical promotion"),
            ("protected_gate", flags.get("protected_gate_verdict_required_after_evidence_completion") is True, "a protected verdict remains required"),
            ("forbidden_premises", {"target_benchmark", "validator_receipt", "checkpoint_receipt", "test_receipt"}.issubset(set(contract.get("forbidden_source_premise_kinds", []))), "target and operational receipts are forbidden as source premises"),
            ("gate_b_surfaces", set(profiles.get("gate_b", {}).get("allowed_review_surfaces", [])) == {"effective_metric", "detector_semantics"}, "Gate B surfaces are exact"),
            ("gate_c_surfaces", set(profiles.get("gate_c", {}).get("allowed_review_surfaces", [])) == {"matter_coupling", "field_equations"}, "Gate C surfaces are exact"),
            ("review_thresholds", all(set(profile.get("ready_statuses", {}).get("independent_review", [])) == {"human_expert_review", "independent_replication"} for profile in profiles.values()), "same-context blind and different-model labels cannot complete review evidence"),
        ]
    )
    return [
        {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]


def validate_record(record: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    missing = [path for path in contract["required_paths"] if not get_path(record, path)[0]]
    if missing:
        add_error(errors, "positive_gate_required_paths", f"missing paths: {missing}")

    expected_top = set(contract.get("top_level_fields", []))
    if set(record) != expected_top:
        add_error(errors, "positive_gate_exact_shape", f"top-level field difference: {sorted(set(record) ^ expected_top)}")
    dimensions = record.get("dimensions")
    expected_dimensions = set(contract.get("required_dimensions", []))
    if not isinstance(dimensions, dict) or set(dimensions) != expected_dimensions:
        observed = set(dimensions) if isinstance(dimensions, dict) else set()
        add_error(errors, "positive_gate_exact_shape", f"dimension field difference: {sorted(observed ^ expected_dimensions)}")
        dimensions = dimensions if isinstance(dimensions, dict) else {}

    enums = contract.get("enums", {})
    enum_values = {
        "gate_id": record.get("gate_id"),
        "subject_scope": record.get("subject_scope"),
        "review_surface": record.get("review_surface"),
        "no_target_purity": record.get("no_target_purity", {}).get("status"),
        "source_derivation": dimensions.get("source_derivation", {}).get("status"),
        "uniqueness_or_quotient": dimensions.get("uniqueness_or_quotient", {}).get("status"),
        "naturality": dimensions.get("naturality", {}).get("status"),
        "dynamics": dimensions.get("dynamics", {}).get("status"),
        "operational_systems": dimensions.get("operational_systems", {}).get("status"),
        "robustness": dimensions.get("robustness", {}).get("status"),
        "independent_review": dimensions.get("independent_review", {}).get("status"),
        "outcome": record.get("outcome"),
        "authority": record.get("authority", {}).get("status"),
    }
    bad_enums = {name: value for name, value in enum_values.items() if value not in enums.get(name, [])}
    if bad_enums:
        add_error(errors, "positive_gate_known_enums", f"unknown enum values: {bad_enums}")

    profile = contract.get("gate_profiles", {}).get(record.get("gate_id"))
    if isinstance(profile, dict) and record.get("review_surface") not in profile.get("allowed_review_surfaces", []):
        add_error(errors, "positive_gate_gate_surface_alignment", "review surface does not belong to the selected gate")

    evidence_required = contract.get("evidence_required_statuses", {})
    for dimension_name in expected_dimensions:
        dimension = dimensions.get(dimension_name, {})
        if not isinstance(dimension, dict):
            add_error(errors, "positive_gate_exact_shape", f"{dimension_name} must be an object")
            continue
        status = dimension.get("status")
        if status in evidence_required.get(dimension_name, []) and not nonempty_list(dimension.get("evidence_refs")):
            add_error(errors, "positive_gate_dimension_evidence_required", f"{dimension_name}:{status} requires evidence refs")
        if status == "not_applicable" and not isinstance(dimension.get("not_applicable_reason"), str) or (
            status == "not_applicable" and not dimension.get("not_applicable_reason", "").strip()
        ):
            add_error(errors, "positive_gate_not_applicable_reason_required", f"{dimension_name}:not_applicable requires a reason")

    no_target = record.get("no_target_purity", {})
    if no_target.get("status") in {"passed", "failed"} and not nonempty_list(no_target.get("evidence_refs")):
        add_error(errors, "positive_gate_dimension_evidence_required", "assessed no-target purity requires evidence refs")

    source = dimensions.get("source_derivation", {})
    if source.get("status") in {"proposed", "source_derived"}:
        refs = source.get("source_refs")
        hashes = source.get("source_hashes")
        hashes_valid = (
            nonempty_list(refs)
            and isinstance(hashes, dict)
            and set(hashes) == set(refs)
            and all(isinstance(value, str) and SHA256_RE.fullmatch(value) for value in hashes.values())
        )
        if not hashes_valid:
            add_error(errors, "positive_gate_source_hashes_required", "proposed or source-derived evidence requires keyed source refs and SHA-256 hashes")
        premise_kinds = source.get("premise_kinds")
        if not nonempty_list(premise_kinds) or any(kind not in enums.get("premise_kind", []) for kind in premise_kinds):
            add_error(errors, "positive_gate_source_premises_source_only", "source provenance uses a missing target-side or operational-receipt premise kind")

    uniqueness = dimensions.get("uniqueness_or_quotient", {})
    if uniqueness.get("status") == "quotient_defined" and not isinstance(uniqueness.get("quotient_scope"), str) or (
        uniqueness.get("status") == "quotient_defined" and not uniqueness.get("quotient_scope", "").strip()
    ):
        add_error(errors, "positive_gate_quotient_scope_required", "quotient_defined requires an exact quotient scope")

    operational = dimensions.get("operational_systems", {})
    if operational.get("status") in {"specified", "constructed", "validated"} and not nonempty_list(operational.get("device_or_protocol_refs")):
        add_error(errors, "positive_gate_operational_refs_required", "specified or stronger operational status requires device or protocol refs")

    robustness = dimensions.get("robustness", {})
    if robustness.get("status") in {"fragile", "conditional", "robust"} and (
        not isinstance(robustness.get("perturbation_scope"), str) or not robustness.get("perturbation_scope", "").strip()
    ):
        add_error(errors, "positive_gate_robustness_scope_required", "assessed robustness requires a perturbation scope")

    review = dimensions.get("independent_review", {})
    executed_review_statuses = set(evidence_required.get("independent_review", []))
    if review.get("status") in executed_review_statuses:
        if record.get("review_executed") is not True or not nonempty_list(review.get("evidence_refs")) or not nonempty_list(review.get("review_artifact_refs")):
            add_error(errors, "positive_gate_review_evidence_required", "an executed review class requires execution, provenance, and review artifact refs")
    elif record.get("review_executed") is True:
        add_error(errors, "positive_gate_review_evidence_required", "review_executed cannot be true for a missing unknown or not-applicable review class")

    authority = record.get("authority", {})
    if not nonempty_list(authority.get("authority_refs")) or not isinstance(authority.get("protected_gate_id"), str) or not authority.get("protected_gate_id", "").strip():
        add_error(errors, "positive_gate_required_paths", "authority requires control refs and the protected gate identifier")
    if not nonempty_list(record.get("forbidden_conclusions")):
        add_error(errors, "positive_gate_required_paths", "forbidden conclusions must be explicit")
    if record.get("physics_promotion_authorized") is not False:
        add_error(errors, "positive_gate_no_implicit_physics_promotion", "version-1 gate records cannot authorize physical promotion")

    readiness_blockers: list[str] = []
    if no_target.get("status") != "passed" or not nonempty_list(no_target.get("evidence_refs")):
        readiness_blockers.append("no_target_purity")
    if isinstance(profile, dict):
        ready_statuses = profile.get("ready_statuses", {})
        for dimension_name in contract.get("required_dimensions", []):
            if dimensions.get(dimension_name, {}).get("status") not in ready_statuses.get(dimension_name, []):
                readiness_blockers.append(dimension_name)
    else:
        readiness_blockers.append("gate_profile")
    computed_complete = not readiness_blockers
    declared_complete = record.get("outcome") == "evidence_complete_for_gate_review"
    if computed_complete != declared_complete:
        add_error(
            errors,
            "positive_gate_outcome_matches_evidence",
            f"declared evidence completion={declared_complete} but computed evidence completion={computed_complete}",
        )

    valid = not errors
    if not valid:
        evidence_complete = False
        blocker_ids = ["record_invalid"]
    else:
        evidence_complete = computed_complete
        blocker_ids = readiness_blockers
    return {
        "valid": valid,
        "evidence_complete": evidence_complete,
        "blocker_ids": blocker_ids,
        "errors": errors,
    }


def build_extensions(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "v21_gate_b_c_positive_provenance_extensions_v1",
        "source_contract_id": contract["schema_id"],
        "gate_profiles": contract["gate_profiles"],
        "review_surface_integration": contract["review_surface_integration"],
        "policy_flags": contract["policy_flags"],
        "authority_boundary": {
            "evidence_completion_is_gate_verdict": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "review_executed_by_extension": False,
        },
    }


def run_fixture_suite(contract: dict[str, Any], fixtures: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    unexpected: list[dict[str, Any]] = []
    bases = fixtures.get("base_records", {})
    for case in fixtures.get("cases", []):
        fixture_id = case.get("fixture_id", "")
        base_name = case.get("base")
        base = bases.get(base_name)
        if not isinstance(base, dict):
            unexpected.append({"fixture_id": fixture_id, "detail": f"unknown base record: {base_name}"})
            continue
        record = apply_case(base, case)
        result = validate_record(record, contract)
        observed_rules = sorted({error["rule_id"] for error in result["errors"]})
        expected_rules = sorted(case.get("expected_rule_ids", []))
        expected_blockers = sorted(case.get("expected_blocker_ids", []))
        matches = (
            result["valid"] is case.get("expected_valid")
            and result["evidence_complete"] is case.get("expected_evidence_complete")
            and set(expected_rules).issubset(observed_rules)
            and set(expected_blockers).issubset(result["blocker_ids"])
        )
        row = {
            "fixture_id": fixture_id,
            "base": base_name,
            "expected_valid": case.get("expected_valid"),
            "observed_valid": result["valid"],
            "expected_evidence_complete": case.get("expected_evidence_complete"),
            "observed_evidence_complete": result["evidence_complete"],
            "expected_rule_ids": expected_rules,
            "observed_rule_ids": observed_rules,
            "expected_blocker_ids": expected_blockers,
            "observed_blocker_ids": result["blocker_ids"],
            "matches_expectation": matches,
        }
        rows.append(row)
        if not matches:
            unexpected.append(row)
    return {"rows": rows, "unexpected": unexpected}


def build_report() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract = extract_contract()
    fixtures = load_fixtures()
    contract_checks = validate_contract(contract)
    fixture_result = run_fixture_suite(contract, fixtures)
    extensions = build_extensions(contract)
    failed_contract_checks = [check for check in contract_checks if check["status"] != "PASS"]
    rows = fixture_result["rows"]
    status = "PASS" if not failed_contract_checks and not fixture_result["unexpected"] else "FAIL"
    report = {
        "schema_id": "v21_positive_provenance_gate_validation_v1",
        "status": status,
        "contract_id": contract.get("schema_id"),
        "plan_task_id": "P11-T05",
        "contract_checks": contract_checks,
        "fixture_rows": rows,
        "counts": {
            "contract_check_count": len(contract_checks),
            "failed_contract_check_count": len(failed_contract_checks),
            "fixture_count": len(rows),
            "expected_valid_count": sum(row["expected_valid"] is True for row in rows),
            "expected_invalid_count": sum(row["expected_valid"] is False for row in rows),
            "evidence_complete_count": sum(row["observed_evidence_complete"] is True for row in rows),
            "blocked_or_invalid_count": sum(row["observed_evidence_complete"] is False for row in rows),
            "unexpected_result_count": len(fixture_result["unexpected"]),
        },
        "unexpected_results": fixture_result["unexpected"],
        "validator_ids": contract.get("conditional_rule_ids", []),
        "source_hashes": {
            "policy_sha256": sha256(POLICY_PATH),
            "fixtures_sha256": sha256(FIXTURES_PATH),
            "validator_sha256": sha256(VALIDATOR_PATH),
            "extensions_sha256": sha256_bytes(canonical_bytes(extensions)),
        },
        "claim_boundary": {
            "no_target_purity_is_necessary_not_sufficient": True,
            "validator_pass_is_operational_evidence_only": True,
            "scoped_candidates_remain_representable": True,
            "review_executed_by_task": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }
    receipt = {
        "schema_id": "v21_positive_provenance_gate_compact_receipt_v1",
        "status": status,
        "plan_task_id": "P11-T05",
        "contract_id": contract.get("schema_id"),
        "policy_sha256": report["source_hashes"]["policy_sha256"],
        "fixtures_sha256": report["source_hashes"]["fixtures_sha256"],
        "extensions_sha256": report["source_hashes"]["extensions_sha256"],
        "validator_sha256": report["source_hashes"]["validator_sha256"],
        "validation_sha256": sha256_bytes(canonical_bytes(report)),
        "contract_check_count": report["counts"]["contract_check_count"],
        "fixture_count": report["counts"]["fixture_count"],
        "evidence_complete_count": report["counts"]["evidence_complete_count"],
        "blocked_or_invalid_count": report["counts"]["blocked_or_invalid_count"],
        "unexpected_result_count": report["counts"]["unexpected_result_count"],
        "validator_ids": report["validator_ids"],
        "claim_boundary_summary": "Control evidence completeness only; no-target or validator PASS alone cannot complete a gate, scoped candidates remain representable, and no review verdict physics promotion or proof authority is created.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    return extensions, report, receipt


def generated_outputs() -> dict[Path, bytes]:
    extensions, report, receipt = build_report()
    return {
        EXTENSIONS_PATH: canonical_bytes(extensions),
        REPORT_PATH: canonical_bytes(report),
        RECEIPT_PATH: canonical_bytes(receipt),
    }


def write_outputs() -> dict[str, Any]:
    outputs = generated_outputs()
    for path, payload in outputs.items():
        path.write_bytes(payload)
    report = json.loads(outputs[REPORT_PATH])
    return {
        "status": report["status"],
        "mode": "write",
        "written_paths": [str(path.relative_to(ROOT)) for path in outputs],
        **report["counts"],
    }


def check_outputs() -> dict[str, Any]:
    outputs = generated_outputs()
    drift_paths = [
        str(path.relative_to(ROOT))
        for path, payload in outputs.items()
        if not path.exists() or path.read_bytes() != payload
    ]
    report = json.loads(outputs[REPORT_PATH])
    status = "PASS" if report["status"] == "PASS" and not drift_paths else "FAIL"
    return {
        "status": status,
        "mode": "check",
        "drift_paths": drift_paths,
        **report["counts"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = write_outputs() if args.write else check_outputs()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['status']} {result['mode']}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
