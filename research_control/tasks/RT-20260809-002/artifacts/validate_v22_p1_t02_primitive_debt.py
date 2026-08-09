#!/usr/bin/env python3
"""Validate the bounded V22 P1-T02 primitive-debt audit artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260809-002"
ART = TASK / "artifacts"
OUTPUT = ART / "v22_p1_t02_primitive_debt_validation.json"

EXACT_OBJECTIVE = (
    "Derive a physical Lorentzian conformal and metric structure, universal "
    "matter coupling, and Einstein-leading dynamics from source fields and laws "
    "defined on a primitive smooth four-dimensional source manifold, without "
    "assuming the target metric or its observational predictions."
)

REQUIRED_DIMENSIONS = {
    "manifold",
    "dimension",
    "topology",
    "smoothness",
    "charts",
    "differentiability",
    "locality",
    "measure",
    "derivative",
    "connection",
    "matter",
    "dynamics",
    "symmetry",
    "scale",
    "operational",
    "metric_equivalent",
}

DEBT_STATUSES = {
    "canonical_primitive",
    "protected_postulate",
    "proposal_only_extension",
    "derived",
    "unresolved",
    "forbidden_target_import",
}

COST_CLASSES = {
    "primitive_debt",
    "bounded_postulate",
    "proposal_debt",
    "zero_derived",
    "unresolved_blocker",
    "forbidden_import",
}

REQUIRED_COST_FIELDS = {
    "entry_id",
    "subject",
    "source_type",
    "debt_status",
    "cost_class",
    "rationale",
    "downstream_use",
    "removal_or_derivation_criterion",
    "source_ref",
    "forbidden_overread",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def classify_debt(facts: dict[str, Any]) -> str:
    if facts.get("target_import"):
        return "forbidden_target_import"
    if facts.get("protected_human_postulate"):
        return "protected_postulate"
    if facts.get("canonical_architecture"):
        return "canonical_primitive"
    if facts.get("proposal_only"):
        return "proposal_only_extension"
    if facts.get("derivation_certificate"):
        return "derived"
    return "unresolved"


def classify_metric(facts: dict[str, Any]) -> str:
    if facts.get("target_matched"):
        return "forbidden_target_import"
    kind = str(facts.get("object_kind", ""))
    derived = bool(facts.get("source_derived"))
    if kind in {
        "coframe_plus_fixed_lorentzian_internal_form",
        "nondegenerate_lorentzian_quadratic_form",
        "volume_plus_lorentzian_conformal_class",
    }:
        return (
            "metric_completing_derivation_eligible"
            if derived
            else "metric_completing_postulation"
        )
    if kind in {"single_cone_principal_polynomial", "nonbirefringent_constitutive_tensor"}:
        return (
            "metric_bearing_derivation_eligible"
            if derived
            else "metric_bearing_reconstruction"
        )
    if kind == "bare_coframe_without_internal_form":
        return "metric_adjacent_unresolved"
    if kind in {"multicone_unreduced_principal_polynomial", "generic_constitutive_tensor"}:
        return "ambiguous_fail_closed"
    if kind == "volume_structure_alone":
        return "not_metric_equivalent"
    return "ambiguous_fail_closed"


def classify_scope(facts: dict[str, Any]) -> str:
    pair = (str(facts.get("object_kind", "")), str(facts.get("claimed_as", "")))
    mapping = {
        ("P7_finite_detector_tokens", "target_clocks_and_rods"): "reject_scope_laundering",
        ("Phi_src_semiflow_candidate", "canonical_physical_time"): "reject_proposal_and_clock_laundering",
        ("validator_pass", "metric_derivation"): "reject_process_as_science",
    }
    return mapping.get(pair, "reject_unclassified_scope_claim")


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    paths = {
        "planning": ROOT / "research_control/design/v22_scientific_objective_and_primitive_debt_v1.md",
        "ledger": ART / "v22_p1_t02_primitive_debt_ledger_v1.yaml",
        "cost_schema": ART / "v22_p1_t02_assumption_cost_schema_v1.yaml",
        "cost_baseline": ART / "v22_p1_t02_assumption_cost_baseline_v1.csv",
        "metric": ART / "v22_p1_t02_metric_equivalence_checklist_v1.yaml",
        "smuggling": ART / "v22_p1_t02_smuggling_audit_v1.yaml",
        "fixtures": ART / "fixtures/v22_p1_t02_metric_equivalence_cases.yaml",
        "math_child": ART / "child_phys_math_p1_t02_primitive_debt.yaml",
        "phil_child": ART / "child_phys_phil_p1_t02_smuggling_audit.yaml",
        "conflict": ART / "parent_conflict_review_p1_t02_primitive_debt.yaml",
        "fusion": ART / "parent_fusion_notes_p1_t02_primitive_debt.md",
        "tex": ART / "v22_p1_t02_scientific_objective_primitive_debt_audit_v1.tex",
    }
    for name, path in paths.items():
        check(f"PATH-{name.upper()}", path.is_file(), str(path.relative_to(ROOT)))

    ledger = load_yaml(paths["ledger"])
    cost_schema = load_yaml(paths["cost_schema"])
    metric = load_yaml(paths["metric"])
    smuggling = load_yaml(paths["smuggling"])
    fixtures = load_yaml(paths["fixtures"])
    math_child = load_yaml(paths["math_child"])
    phil_child = load_yaml(paths["phil_child"])
    conflict = load_yaml(paths["conflict"])

    planning_text = paths["planning"].read_text(encoding="utf-8")
    tex_text = paths["tex"].read_text(encoding="utf-8")
    check("OBJECTIVE-LEDGER", ledger.get("exact_objective") == EXACT_OBJECTIVE, "ledger exact objective")
    planning_plain = re.sub(r"(?m)^>\s?", "", planning_text)
    check("OBJECTIVE-PLANNING", EXACT_OBJECTIVE in normalized(planning_plain), "planning source exact objective")
    check("OBJECTIVE-TEX", EXACT_OBJECTIVE in normalized(tex_text), "fused TeX exact objective")

    snapshots = ledger.get("source_snapshots", [])
    snapshot_failures: list[str] = []
    for item in snapshots:
        source_path = ROOT / str(item.get("path", ""))
        expected = str(item.get("sha256", ""))
        if not source_path.is_file() or sha256(source_path) != expected:
            snapshot_failures.append(str(item.get("object_id", source_path)))
    check("SOURCE-HASHES", not snapshot_failures, f"snapshot_count={len(snapshots)} failures={snapshot_failures}")

    dimensions = ledger.get("assumption_dimensions", [])
    dimension_ids = {str(item.get("dimension_id", "")) for item in dimensions}
    check("DIMENSION-COVERAGE", dimension_ids == REQUIRED_DIMENSIONS, f"actual={len(dimension_ids)}")
    check("DIMENSION-COUNT", len(dimensions) == 16, f"actual={len(dimensions)}")
    invalid_dimension_status = [
        str(item.get("dimension_id"))
        for item in dimensions
        if item.get("debt_status") not in DEBT_STATUSES
    ]
    check("DIMENSION-STATUS", not invalid_dimension_status, f"invalid={invalid_dimension_status}")
    required_dimension_fields = {
        "dimension_id",
        "subject",
        "source_type",
        "debt_status",
        "cost_class",
        "rationale",
        "downstream_use",
        "removal_or_derivation_criterion",
        "forbidden_overread",
        "source_refs",
    }
    incomplete_dimensions = [
        str(item.get("dimension_id"))
        for item in dimensions
        if any(not item.get(field) for field in required_dimension_fields)
    ]
    check("DIMENSION-FIELDS", not incomplete_dimensions, f"incomplete={incomplete_dimensions}")

    symbols = ledger.get("symbol_inventory", [])
    incomplete_symbols = [
        str(item.get("symbol"))
        for item in symbols
        if not all(item.get(field) for field in ("symbol", "source_type", "debt_status", "provenance", "downstream_use"))
        or item.get("debt_status") not in DEBT_STATUSES
    ]
    check("SYMBOL-INVENTORY", len(symbols) >= 16 and not incomplete_symbols, f"count={len(symbols)} incomplete={incomplete_symbols}")
    check("PHI-CANONICAL-OPEN", any(item.get("symbol") == "Phi_src" and item.get("debt_status") == "unresolved" for item in symbols), "Phi_src remains unresolved")
    check("PHI-PROPOSAL-SEPARATE", any(item.get("symbol") == "Phi_src_semiflow_candidate" and item.get("debt_status") == "proposal_only_extension" for item in symbols), "semiflow remains proposal-only")
    check("P7-PROTECTED", any(item.get("symbol") == "P7SourceMatterPackage_v1" and item.get("debt_status") == "protected_postulate" for item in symbols), "P7 scope classification")

    check("COST-SCHEMA-FIELDS", set(cost_schema.get("required_fields", [])) == REQUIRED_COST_FIELDS, "required cost fields")
    check("COST-SCHEMA-STATUS", set(cost_schema.get("allowed_debt_status", [])) == DEBT_STATUSES, "allowed debt status")
    check("COST-SCHEMA-CLASSES", set(cost_schema.get("allowed_cost_class", [])) == COST_CLASSES, "allowed cost classes")
    check("COST-NONSCALAR", cost_schema.get("scalar_total_authorized") is False and cost_schema.get("noncompensatory_typed_costs") is True, "noncompensatory typed costs")

    with paths["cost_baseline"].open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    check("COST-BASELINE-HEADER", set(rows[0].keys()) == REQUIRED_COST_FIELDS if rows else False, "baseline header")
    invalid_rows = [
        row.get("entry_id", "")
        for row in rows
        if any(not row.get(field, "").strip() for field in REQUIRED_COST_FIELDS)
        or row.get("debt_status") not in DEBT_STATUSES
        or row.get("cost_class") not in COST_CLASSES
    ]
    check("COST-BASELINE-ROWS", len(rows) >= 24 and not invalid_rows, f"count={len(rows)} invalid={invalid_rows}")
    check("COST-BASELINE-UNIQUE", len({row["entry_id"] for row in rows}) == len(rows), "unique entry IDs")

    metric_cases = {str(item.get("case_id")): item for item in metric.get("cases", [])}
    check("METRIC-CASES", set(metric_cases) == {"coframe", "constitutive_tensor", "quadratic_form", "principal_polynomial", "volume_structure"}, f"cases={sorted(metric_cases)}")
    expected_metric_classes = {
        "coframe": "metric_completing",
        "constitutive_tensor": "metric_bearing",
        "quadratic_form": "metric_completing",
        "principal_polynomial": "metric_bearing",
        "volume_structure": "not_metric_equivalent",
    }
    check("METRIC-CLASSIFICATION", all(metric_cases[key].get("classification") == value for key, value in expected_metric_classes.items()), "five required classifications")
    check("METRIC-PROVENANCE-RULE", "postulation or reconstruction" in metric.get("definitions", {}).get("provenance_rule", ""), "assumed recoverable data lose emergence credit")
    theorem_ids = {item.get("theorem_id") for item in metric.get("theorems", [])}
    check("METRIC-THEOREMS", theorem_ids == {"V22-P1-T02-METRIC-RECOVERABILITY-CLASSIFICATION-THEOREM-V1", "V22-P1-T02-VOLUME-CONFORMAL-SCALE-COMPLETION-V1"}, "theorem identities")
    check("VOLUME-COUNTERMODEL-RECORDED", len(metric.get("countermodels", [])) == 1 and metric["countermodels"][0].get("determinant") == "-1", "same-volume family")

    determinant_failures = []
    for s in (-2.0, -1.0, 0.0, 1.0, 2.0):
        determinant = (-math.exp(2 * s)) * math.exp(-2 * s)
        if not math.isclose(determinant, -1.0, rel_tol=1e-12, abs_tol=1e-12):
            determinant_failures.append(s)
    check("VOLUME-DETERMINANT", not determinant_failures, f"tested=5 failures={determinant_failures}")
    nonconformal_failures = []
    for s, r in ((-2.0, -1.0), (-1.0, 0.0), (0.0, 1.0), (1.0, 2.0)):
        omega_sq = 1.0  # forced by the unchanged third diagonal coefficient
        if math.isclose(math.exp(2 * s), omega_sq * math.exp(2 * r), rel_tol=1e-12):
            nonconformal_failures.append((s, r))
    check("VOLUME-NONCONFORMAL", not nonconformal_failures, f"pairs=4 failures={nonconformal_failures}")

    fixture_cases = fixtures.get("cases", [])
    fixture_failures = []
    category_counts: dict[str, int] = {}
    for item in fixture_cases:
        category = str(item.get("category", ""))
        category_counts[category] = category_counts.get(category, 0) + 1
        facts = item.get("facts", {})
        if category == "debt_status":
            actual = classify_debt(facts)
        elif category == "metric_equivalence":
            actual = classify_metric(facts)
        elif category == "scope_guard":
            actual = classify_scope(facts)
        else:
            actual = "unknown_category"
        if actual != item.get("expected"):
            fixture_failures.append({"case_id": item.get("case_id"), "expected": item.get("expected"), "actual": actual})
    expected_counts = fixtures.get("expected_counts", {})
    check("FIXTURE-TOTAL", len(fixture_cases) == expected_counts.get("total") == 21, f"actual={len(fixture_cases)}")
    check("FIXTURE-CATEGORIES", all(category_counts.get(key) == value for key, value in expected_counts.items() if key != "total"), f"counts={category_counts}")
    check("FIXTURE-VERDICTS", not fixture_failures, f"failures={fixture_failures}")

    audit_checks = smuggling.get("checks", [])
    check("SMUGGLING-CHECKS", len(audit_checks) == 10 and all(item.get("status") == "PASS" for item in audit_checks), f"count={len(audit_checks)}")
    check("SMUGGLING-RESULT", smuggling.get("result", {}).get("status") == "PASS_SOURCE_TARGET_BOUNDARY_EXPLICIT_NO_IMPORT_AS_WRITTEN", "bounded audit status")
    check("REVIEW-PROVENANCE", smuggling.get("external_review_claimed") is False and smuggling.get("independent_replication_claimed") is False, "internal same-context only")

    math_payload_types = {item.get("payload_type") for item in math_child.get("new_mathematical_payload", [])}
    check("MATH-CHILD", math_child.get("status") == "completed" and math_payload_types == {"theorem_with_hypotheses_and_proof", "countermodel_or_obstruction"}, f"payload_types={sorted(math_payload_types)}")
    check("PHIL-CHILD", phil_child.get("status") == "completed" and phil_child.get("review_provenance", {}).get("class") == "same_context_internal_ai_review_only", "bounded internal audit")
    check("PARENT-CONFLICT", conflict.get("status") == "resolved" and conflict.get("unresolved_conflicts") == [] and conflict.get("blocking_conflict_count") == 0, "no unresolved blocking conflict")
    check("PARENT-FUSION", paths["fusion"].is_file() and "No blocking conflict remains." in paths["fusion"].read_text(encoding="utf-8"), "fusion preserves resolution")

    required_tex_phrases = [
        "Same-volume nonconformal counterfamily",
        "Volume completes conformal scale",
        "Expanded Distance-to-GR matrix",
        "same-context internal AI review",
        "physical Distance-to-GR delta is zero",
        "P1-T03 may separately",
    ]
    missing_tex_phrases = [phrase for phrase in required_tex_phrases if phrase not in tex_text]
    check("TEX-CONTENT", not missing_tex_phrases, f"missing={missing_tex_phrases}")
    check("NO-ONTOLOGY-ADOPTION", ledger.get("adoption_status") == "no_ontology_or_source_law_adoption" and ledger.get("audit_counts", {}).get("ontology_adoption_count") == 0, "zero adoption")
    check("ZERO-DISTANCE-DELTA", ledger.get("audit_counts", {}).get("distance_to_gr_delta_count") == 0 and smuggling.get("result", {}).get("distance_to_gr_delta_changed") is False, "zero physical delta")

    failures = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v22_p1_t02_primitive_debt_validation_v1",
        "task_id": "RT-20260809-002",
        "job_id": "AJ-RT-20260809-002-001",
        "generated_at": "2026-08-09T02:08:07Z",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failures),
        "failed_check_count": len(failures),
        "fixture_count": len(fixture_cases),
        "source_snapshot_count": len(snapshots),
        "assumption_dimension_count": len(dimensions),
        "symbol_count": len(symbols),
        "assumption_cost_entry_count": len(rows),
        "metric_equivalence_case_count": len(metric_cases),
        "smuggling_check_count": len(audit_checks),
        "new_mathematical_payload_count": len(math_child.get("new_mathematical_payload", [])),
        "ontology_adoption_count": 0,
        "distance_to_gr_delta_changed": False,
        "external_review_completed": False,
        "independent_replication_completed": False,
        "checks": checks,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.write:
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
