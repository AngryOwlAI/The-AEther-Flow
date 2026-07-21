#!/usr/bin/env python3
"""Validate the bounded P2-T07 selector-theorem Refuter stress packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
CASES_PATH = ARTIFACT_DIR / "eqsrc_selector_theorem_stress_cases.json"
TEX_PATH = ARTIFACT_DIR / "eqsrc_selector_theorem_refuter_stress_v1.tex"
COMPACT_PATH = ARTIFACT_DIR / "eqsrc_selector_theorem_refuter_stress_compact_receipt.json"
REPORT_PATH = ARTIFACT_DIR / "eqsrc_selector_theorem_refuter_stress_validation.json"
THEOREM_PATH = ROOT / "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex"
AUDIT_PATH = ROOT / "research_control/tasks/RT-20260720-019/artifacts/eqsrc_selector_theorem_smuggling_audit_v1.tex"
EXPECTED_THEOREM_HASH = "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae"
EXPECTED_AUDIT_HASH = "d093d7b0afbe322cf537644de54f17156ea2427fcc0988f4fc8fb305e93a0f76"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixed_locus(action: dict[str, list[int]], carrier: list[int]) -> list[int]:
    return [point for point in carrier if all(perm[point] == point for perm in action.values())]


def add_check(checks: list[dict[str, object]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})


def validate() -> dict[str, object]:
    cases_doc = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    compact = json.loads(COMPACT_PATH.read_text(encoding="utf-8"))
    tex = TEX_PATH.read_text(encoding="utf-8")
    checks: list[dict[str, object]] = []

    add_check(checks, "theorem_hash", sha256(THEOREM_PATH) == EXPECTED_THEOREM_HASH, EXPECTED_THEOREM_HASH)
    add_check(checks, "audit_hash", sha256(AUDIT_PATH) == EXPECTED_AUDIT_HASH, EXPECTED_AUDIT_HASH)
    add_check(checks, "result_classification", cases_doc.get("result_classification") == "scoped_obstruction", "exact Refuter enum")
    stress_cases = cases_doc.get("stress_cases", [])
    add_check(checks, "stress_case_count", len(stress_cases) == 6, "six required stress classes")
    by_class = {case["stress_class"]: case for case in stress_cases}
    required_classes = {
        "nonfaithful_action", "partial_morphism", "multiple_components",
        "stochastic_selector", "added_mark", "altered_variation_class",
    }
    add_check(checks, "stress_class_coverage", set(by_class) == required_classes, "exact P2-T07 class set")

    nonfaithful = by_class["nonfaithful_action"]
    full_fixed = fixed_locus(nonfaithful["action"], nonfaithful["carrier"])
    quotient_fixed = fixed_locus(nonfaithful["faithful_quotient_action"], nonfaithful["carrier"])
    add_check(checks, "nonfaithful_full_fixed", full_fixed == [], "Klein action has empty fixed locus")
    add_check(checks, "nonfaithful_quotient_fixed", quotient_fixed == [], "faithful quotient has same fixed locus")
    add_check(checks, "nonfaithful_kernel_nontrivial", len(nonfaithful["action_kernel"]) == 2, "action kernel has two elements")

    partial = by_class["partial_morphism"]
    add_check(checks, "partial_not_total", set(partial["partial_domain"]) != set(partial["carrier"]), "proper partial domain")
    add_check(checks, "partial_no_groupoid_inverse", partial["has_groupoid_inverse"] is False, "outside certified groupoid")

    multi = by_class["multiple_components"]
    products = []
    for profile in multi["finite_factor_profiles"]:
        product = 1
        for size in profile["fixed_locus_sizes"]:
            product *= size
        products.append(product)
    add_check(checks, "component_product_sizes", products == [0, 2], "empty complement and multiplicity control")
    add_check(checks, "choice_guard", multi["infinite_family_choice_guard_preserved"] is True, "arbitrary product qualification retained")

    stochastic = by_class["stochastic_selector"]
    generator = stochastic["generator"]
    deterministic_fixed = [i for i in stochastic["carrier"] if generator[i] == i]
    weights = [Fraction(value) for value in stochastic["invariant_probability"]]
    permuted_weights = [weights[generator.index(i)] for i in stochastic["carrier"]]
    add_check(checks, "stochastic_no_fixed_point", deterministic_fixed == [], "transitive C3 point action")
    add_check(checks, "stochastic_probability_normalized", sum(weights) == 1, "uniform measure sums to one")
    add_check(checks, "stochastic_probability_invariant", permuted_weights == weights, "uniform measure is rotation-invariant")

    marked = by_class["added_mark"]
    add_check(checks, "unmarked_fixed_empty", marked["unmarked_fixed_locus"] == [], "swap has no fixed point")
    add_check(checks, "marked_fixed_singleton", marked["marked_fixed_locus"] == [marked["marked_value"]], "mark changes domain to singleton")

    varied = by_class["altered_variation_class"]
    add_check(checks, "variation_full_fixed_empty", varied["full_group_fixed_locus"] == [], "full swap group")
    add_check(checks, "variation_subgroup_fixed_all", varied["restricted_identity_subgroup_fixed_locus"] == varied["carrier"], "identity subgroup")
    add_check(checks, "variation_monotonicity", set(varied["full_group_fixed_locus"]).issubset(varied["restricted_identity_subgroup_fixed_locus"]), "D^G subseteq D^H")

    branches = cases_doc.get("ontology_law_failure_branches", {})
    add_check(checks, "failure_branch_coverage", set(branches) == {"collapse", "nonuniqueness", "inverse_defect", "cocycle_defect", "finite_variation_fragility"}, "five required branches")
    authority = cases_doc.get("authority", {})
    protected_false = [
        "canonical_ontology_edit_authorized", "source_law_adoption_authorized",
        "general_EqSrc_discharged", "distance_to_gr_ledger_changed",
        "metric_use_ledger_changed", "proof_authority",
        "physics_promotion_authorized", "global_no_go_claim_authorized",
        "future_source_extension_impossibility_authorized",
    ]
    add_check(checks, "protected_authority_false", all(authority.get(key) is False for key in protected_false), "all protected fields false")
    add_check(checks, "adoption_status", authority.get("adoption_status") == "blocked_adoption_open_continuation", "exact status pair")
    add_check(checks, "tex_result_marker", "\\texttt{scoped\\_obstruction}" in tex, "fused artifact exact classification")
    add_check(checks, "tex_faithful_quotient", "Faithful-quotient fixed-locus invariance" in tex, "new proposition present")
    add_check(checks, "tex_variation_monotonicity", "Variation-subgroup monotonicity" in tex, "new proposition present")
    add_check(checks, "tex_stochastic_countermodel", "Transitive three-point stochastic boundary" in tex, "minimal countermodel present")
    add_check(checks, "compact_parity", compact.get("result_classification") == "scoped_obstruction" and compact.get("stress_case_count") == 6, "compact receipt agrees")
    cases_text = CASES_PATH.read_text(encoding="utf-8")
    add_check(checks, "uncorrected_metric_keys_absent", "relation_image_sizes" not in cases_text and "relation_stabilizer_order" not in cases_text, "P2-T04 metric labels not used")

    failures = [check for check in checks if check["status"] != "PASS"]
    return {
        "schema_id": "eqsrc-selector-theorem-refuter-stress-validation.v1",
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260720-020",
        "plan_task_id": "P2-T07",
        "result_classification": "scoped_obstruction",
        "check_count": len(checks),
        "failed_check_count": len(failures),
        "stress_case_count": len(stress_cases),
        "failure_branch_count": len(branches),
        "distance_to_gr_delta": "scoped_obstruction_no_ledger_change",
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: {report['check_count'] - report['failed_check_count']}/{report['check_count']} checks")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
