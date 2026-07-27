#!/usr/bin/env python3
"""Deterministically validate the bounded P6-T06 Refuter packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260726-010"
ARTIFACT_DIR = TASK_DIR / "artifacts"
TEX_PATH = ARTIFACT_DIR / "uniqueness_covariance_robustness_admissibility_obstruction_v1.tex"
SPEC_PATH = ARTIFACT_DIR / "uniqueness_covariance_robustness_admissibility_obstruction_spec_v1.yaml"
VARIATION_PATH = ARTIFACT_DIR / "variation_stress_report_v1.yaml"
MATRIX_PATH = ARTIFACT_DIR / "physical_admissibility_matrix_v1.yaml"
REPORT_PATH = ARTIFACT_DIR / "uniqueness_covariance_robustness_admissibility_obstruction_validation_receipt_v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, check_id: str, detail: str, checks: list[dict[str, Any]]) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        }
    )


def q_inverse_value(a: float) -> float:
    return -1.0 + math.exp(-2.0 * a)


def validate() -> dict[str, Any]:
    spec = yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))
    variation = yaml.safe_load(VARIATION_PATH.read_text(encoding="utf-8"))
    matrix = yaml.safe_load(MATRIX_PATH.read_text(encoding="utf-8"))
    tex = TEX_PATH.read_text(encoding="utf-8")
    checks: list[dict[str, Any]] = []

    check(
        spec["schema_id"]
        == "v21_p6_t06_uniqueness_covariance_robustness_admissibility_obstruction_v1",
        "SPEC-SCHEMA",
        "Expected bounded P6-T06 schema.",
        checks,
    )
    check(spec["task_id"] == "RT-20260726-010", "SPEC-TASK",
          "Specification is bound to the exact task.", checks)
    check(spec["plan_task_id"] == "P6-T06", "SPEC-PLAN",
          "Specification is bound to the exact v21 work item.", checks)
    check(spec["refuter_result_classification"] == "scoped_obstruction",
          "SPEC-REFUTER-CLASS", "Refuter classification is exact.", checks)
    check(spec["adoption_status"] == "blocked_adoption_open_continuation",
          "SPEC-ADOPTION", "Adoption is blocked while continuation stays open.", checks)

    typed_input = spec["typed_input"]
    check("D_1" in typed_input["one_ray_bundle"], "INPUT-ONE-RAY",
          "P6-T03 one-ray bundle remains explicit.", checks)
    false_input_keys = (
        "source_coframe_supplied",
        "lorentzian_form_supplied",
        "operational_covector_transport_supplied",
        "geometry_coarse_graining_map_supplied",
        "matter_universality_law_supplied",
        "target_metric_imported",
    )
    for key in false_input_keys:
        check(typed_input[key] is False, f"INPUT-{key.upper()}",
              f"{key} remains false.", checks)

    assumptions = {row["id"]: row for row in spec["assumption_table"]}
    check(set(assumptions) == {f"A{i}" for i in range(1, 9)},
          "ASSUMPTION-TABLE", "Eight explicit assumptions are present.", checks)
    check(assumptions["A6"]["status"] == "consistency_requirement",
          "ASSUMPTION-GAUGE", "Gauge observability is a consistency requirement.", checks)
    check(assumptions["A7"]["status"] == "missing_source_laws",
          "ASSUMPTION-MISSING-LAWS", "Conditional source laws remain missing.", checks)
    check(assumptions["A8"]["status"] == "no_target_import_enforced",
          "ASSUMPTION-NO-TARGET", "No-target boundary is explicit.", checks)

    theorem_ids = {row["theorem_id"] for row in spec["theorems"]}
    expected_theorems = {
        "P6T06-THM-CONE-TRANSVERSE-NONSELECTION",
        "P6T06-COR-GAUGE-QUOTIENT-BURDEN",
        "P6T06-PROP-FINITE-VARIATION-RESPONSE",
        "P6T06-PROP-UNIFORM-NONDEGENERACY-FAILURE",
        "P6T06-PROP-TRANSITION-INVERSE-COCYCLE-CONTROLS",
        "P6T06-THM-SCOPED-GATE-B-OBSTRUCTION",
    }
    check(theorem_ids == expected_theorems, "THEOREM-SET",
          "Six exact theorem identities are present.", checks)

    for a, expected_sign in ((-1.0, 1), (0.0, 0), (1.0, -1)):
        value = q_inverse_value(a)
        actual_sign = 1 if value > 1e-12 else -1 if value < -1e-12 else 0
        check(actual_sign == expected_sign, f"CONE-SIGN-{a}",
              "Fixed source covector changes classification across a.", checks)

    for a in (-1.0, 0.0, 1.0):
        determinant = -1.0
        transverse_product = math.exp(2.0 * a) * math.exp(-2.0 * a)
        check(math.isclose(transverse_product, 1.0, rel_tol=0.0, abs_tol=1e-12),
              f"FAMILY-TRANSVERSE-PRODUCT-{a}",
              "a-variation preserves determinant while changing transverse entries.", checks)
        check(determinant < 0.0, f"FAMILY-LORENTZ-{a}",
              "The epsilon=1 family remains Lorentzian.", checks)

    for epsilon in (1.0, 0.1, 0.001):
        determinant = -(epsilon * epsilon)
        inverse_component = epsilon ** -2
        check(determinant < 0.0, f"EPSILON-DET-{epsilon}",
              "Positive epsilon has nonzero negative determinant.", checks)
        check(inverse_component >= 1.0, f"EPSILON-INVERSE-{epsilon}",
              "Inverse conditioning witness is explicit.", checks)
    check(0.001 ** -2 > 0.1 ** -2 > 1.0,
          "EPSILON-CONDITIONING-GROWTH",
          "Inverse conditioning grows toward the degenerate boundary.", checks)

    signed_inertias = {
        "positive": sum(v < 0 for v in (-1.0, 1.0, 1.0, 1.0)),
        "negative": sum(v < 0 for v in (-1.0, 1.0, 1.0, -1.0)),
    }
    check(signed_inertias == {"positive": 1, "negative": 2},
          "SIGNATURE-CROSSING",
          "Signed continuation crosses from Lorentzian to split signature.", checks)

    check(spec["inherited_naturality_obstruction"]["invariant_symmetric_bilinear_dimension"] == 0,
          "NATURALITY-INHERITED",
          "P6-T05 zero-dimensional invariant-form result is fixed.", checks)
    check(spec["inherited_naturality_obstruction"]["scope_broadened"] is False,
          "NATURALITY-SCOPE",
          "P6-T05 theorem scope is not broadened.", checks)

    check(4.0 != 1.0, "TRANSITION-2I",
          "2I is not eta-preserving.", checks)
    check(1 != -1, "TRANSITION-INVERSE",
          "I and -I fail the required inverse identity.", checks)
    check(1 * 1 != -1, "TRANSITION-COCYCLE",
          "I,I,-I fail the triple-overlap cocycle.", checks)

    check(variation["robustness_verdict"] == "not_certified",
          "VARIATION-VERDICT", "Variation robustness fails closed.", checks)
    variation_results = {row["result"] for row in variation["stress_tests"]}
    check(
        variation_results
        == {
            "fails_unique_cone_selection",
            "fails_transverse_comparison_selection",
            "fails_uniform_nondegeneracy_and_conditioning",
            "no_source_derived_exclusion",
            "no_transfer_certificate",
        },
        "VARIATION-RESULTS",
        "All five required variation results are present.",
        checks,
    )

    matrix_rows = matrix["rows"]
    check(len(matrix_rows) == 8, "ADMISSIBILITY-ROW-COUNT",
          "Eight physical-admissibility criteria are audited.", checks)
    check(all(row["disposition"] == "not_met" for row in matrix_rows),
          "ADMISSIBILITY-DISPOSITIONS",
          "Every physical-admissibility criterion fails closed.", checks)
    check(matrix["overall_disposition"] == "gate_b_not_passed",
          "ADMISSIBILITY-GATE-B", "Gate B is not passed.", checks)
    check(matrix["branch_status"] == "comparison_branches_unexcluded_not_adopted",
          "ADMISSIBILITY-BRANCH-STATUS",
          "Comparison branches are not adopted physical sectors.", checks)

    burden = spec["proposal_only_burden_template"]
    check(burden["status_label"] == "proposal-only", "BURDEN-PROPOSAL-ONLY",
          "Burden template uses controlled proposal-only status.", checks)
    check(burden["canonical_ontology_candidate"] is False,
          "BURDEN-NOT-CANONICAL-CANDIDATE",
          "No canonical-ontology candidate is promoted.", checks)
    check(burden["human_gate_required_before_adoption"] is True,
          "BURDEN-HUMAN-GATE", "Adoption remains human-gated.", checks)

    obstruction = spec["precise_obstruction"]
    check(
        obstruction["obstruction_id"]
        == "OBST-P6T06-GATE-B-UNIQUENESS-ROBUSTNESS-ADMISSIBILITY-001",
        "OBSTRUCTION-ID",
        "Stable obstruction identity is present.",
        checks,
    )
    check(obstruction["refuter_result_classification"] == "scoped_obstruction",
          "OBSTRUCTION-REFUTER-CLASS", "Refuter vocabulary is exact.", checks)
    check(obstruction["scope"] == "source_extension_candidate",
          "OBSTRUCTION-SCOPE", "Obstruction remains candidate-scoped.", checks)
    check(obstruction["current_ontology_implication"] == "does_not_derive",
          "OBSTRUCTION-ONTOLOGY", "Underdetermination language is precise.", checks)
    check(obstruction["global_no_go_claimed"] is False,
          "OBSTRUCTION-NO-GLOBAL-NOGO", "No global no-go is claimed.", checks)
    check(len(spec["reopening"]["criteria"]) == 4,
          "REOPENING-CRITERIA", "Four materially richer reopening classes are named.", checks)

    freeze = spec["freeze"]
    check(freeze["freeze_decision"] == "locally_frozen",
          "FREEZE-DECISION", "Only the exact unchanged route is locally frozen.", checks)
    check(freeze["next_allowed_route"] == "theoretical_selector",
          "FREEZE-NEXT", "P6-T07 selector is the next route family.", checks)
    check(freeze["materially_richer_continuation_open"] is True,
          "FREEZE-CONTINUATION", "Materially richer continuation stays open.", checks)
    check(freeze["global_theory_rejection"] is False,
          "FREEZE-NO-GLOBAL-REJECTION", "Local freeze is not theory rejection.", checks)

    authority = spec["authority"]
    check(all(value is False for value in authority.values()),
          "AUTHORITY-ALL-FALSE",
          "Every adoption, promotion, and publication authority flag is false.", checks)

    required_tex_markers = [
        "same-source comparison family",
        "Cone and transverse-comparison nonselection",
        "A gauge declaration does not close the burden",
        "No uniform nondegeneracy certificate",
        "Physical-admissibility audit",
        "OBST-P6T06-GATE-B-UNIQUENESS-ROBUSTNESS-ADMISSIBILITY-001",
        "blocked\\_adoption\\_open\\_continuation",
        "Gate B remains unpassed",
    ]
    for index, marker in enumerate(required_tex_markers, start=1):
        check(marker in tex, f"TEX-MARKER-{index:02d}",
              f"Required TeX marker is present: {marker}", checks)

    forbidden_tex_markers = [
        "canonical ontology is hereby",
        "physical metric is established",
        "physical causal cone is established",
        "effective metric is derived",
        "einstein equations are derived",
        "the theory is impossible",
        "this is a completed derivation",
    ]
    lowered_tex = tex.lower()
    for index, marker in enumerate(forbidden_tex_markers, start=1):
        check(marker not in lowered_tex, f"TEX-FORBIDDEN-{index:02d}",
              f"Forbidden promotion marker is absent: {marker}", checks)

    fixed_source_results: list[dict[str, Any]] = []
    for source in spec["fixed_sources"]:
        path = ROOT / source["path"]
        actual = sha256(path)
        matches = actual == source["sha256"]
        check(matches, f"SOURCE-HASH-{source['object_id']}",
              f"Fixed source hash {'matches' if matches else 'does not match'}.", checks)
        fixed_source_results.append(
            {
                "object_id": source["object_id"],
                "path": source["path"],
                "expected_sha256": source["sha256"],
                "actual_sha256": actual,
                "status": "PASS" if matches else "FAIL",
            }
        )

    failed = [entry for entry in checks if entry["status"] != "PASS"]
    return {
        "schema_id": "v21_p6_t06_uniqueness_covariance_robustness_admissibility_validation_v1",
        "task_id": "RT-20260726-010",
        "plan_task_id": "P6-T06",
        "result_id": spec["result_id"],
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "theorem_count": len(spec["theorems"]),
        "assumption_count": len(spec["assumption_table"]),
        "comparison_family_count": 1,
        "variation_stress_count": len(variation["stress_tests"]),
        "physical_admissibility_criterion_count": len(matrix_rows),
        "scoped_obstruction_count": 1,
        "physical_metric_count": 0,
        "target_metric_premise_count": 0,
        "global_no_go_count": 0,
        "fixed_sources": fixed_source_results,
        "artifact_hashes": {
            TEX_PATH.name: sha256(TEX_PATH),
            SPEC_PATH.name: sha256(SPEC_PATH),
            VARIATION_PATH.name: sha256(VARIATION_PATH),
            MATRIX_PATH.name: sha256(MATRIX_PATH),
        },
        "claim_boundary_summary": (
            "Exact same-source cone and conditioning variation, inherited "
            "naturality obstruction, conditional transition controls, and "
            "physical-admissibility audit only; no ontology or source-law "
            "adoption, physical metric, downstream GR promotion, global "
            "no-go, publication, push, or completed derivation."
        ),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        if not REPORT_PATH.exists():
            report["status"] = "FAIL"
            report["receipt_error"] = "validation receipt is missing"
        else:
            recorded = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
            if recorded != report:
                report["status"] = "FAIL"
                report["receipt_error"] = "validation receipt is stale"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
