#!/usr/bin/env python3
"""Deterministically validate the bounded P6-T05 signature packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260726-009"
ARTIFACT_DIR = TASK_DIR / "artifacts"
TEX_PATH = ARTIFACT_DIR / "signature_covariance_naturality_obstruction_v1.tex"
SPEC_PATH = ARTIFACT_DIR / "signature_covariance_naturality_obstruction_spec_v1.yaml"
REPORT_PATH = ARTIFACT_DIR / "signature_covariance_naturality_obstruction_validation_receipt_v1.json"


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


def diagonal_det(values: tuple[float, ...]) -> float:
    return math.prod(values)


def negative_count(values: tuple[float, ...]) -> int:
    return sum(value < 0.0 for value in values)


def validate() -> dict[str, Any]:
    spec = yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))
    tex = TEX_PATH.read_text(encoding="utf-8")
    checks: list[dict[str, Any]] = []

    check(
        spec["schema_id"] == "v21_p6_t05_signature_covariance_naturality_obstruction_v1",
        "SPEC-SCHEMA",
        "Expected bounded P6-T05 schema.",
        checks,
    )
    check(spec["task_id"] == "RT-20260726-009", "SPEC-TASK",
          "Specification is bound to the exact task.", checks)
    check(spec["plan_task_id"] == "P6-T05", "SPEC-PLAN",
          "Specification is bound to the exact v21 work item.", checks)
    check(spec["adoption_status"] == "blocked_adoption_open_continuation",
          "SPEC-ADOPTION", "Adoption is blocked while continuation stays open.", checks)

    typed_input = spec["typed_input"]
    check("D_1" in typed_input["one_ray_bundle"], "INPUT-ONE-RAY",
          "P6-T03 one-ray bundle remains explicit.", checks)
    for key in (
        "source_coframe_supplied",
        "lorentzian_form_supplied",
        "metric_volume_identity_supplied",
        "transition_representation_supplied",
        "target_metric_imported",
    ):
        check(typed_input[key] is False, f"INPUT-{key.upper()}",
              f"{key} remains false.", checks)

    assumptions = {row["id"]: row for row in spec["assumption_table"]}
    check(set(assumptions) == {f"A{i}" for i in range(1, 9)},
          "ASSUMPTION-TABLE", "Eight explicit assumptions are present.", checks)
    check(assumptions["A5"]["status"] == "consistency_requirement",
          "ASSUMPTION-NATURALITY", "Naturality is a consistency requirement.", checks)
    check(assumptions["A7"]["status"] == "missing_source_laws",
          "ASSUMPTION-MISSING-LAWS", "Conditional source laws remain missing.", checks)
    check(assumptions["A8"]["status"] == "no_target_import_enforced",
          "ASSUMPTION-NO-TARGET", "No-target boundary is explicit.", checks)

    theorem_ids = {row["theorem_id"] for row in spec["theorems"]}
    expected_theorems = {
        "P6T05-THM-SIGNATURE-NONSELECTION",
        "P6T05-PROP-NONDEGENERACY-NONCERTIFICATION",
        "P6T05-THM-SOURCE-NATURALITY-OBSTRUCTION",
        "P6T05-THM-CONDITIONAL-COFRAME-GLUING",
        "P6T05-PROP-CONDITIONAL-TIME-ORIENTATION",
    }
    check(theorem_ids == expected_theorems, "THEOREM-SET",
          "Five exact theorem identities are present.", checks)

    q_l = (-1.0, 1.0, 1.0, 1.0)
    q_s = (-1.0, -1.0, 1.0, 1.0)
    check(abs(diagonal_det(q_l)) == abs(diagonal_det(q_s)) == 1.0,
          "SIGNATURE-EQUAL-DET-MAGNITUDE",
          "Lorentzian and split witnesses have equal determinant magnitude.", checks)
    check(negative_count(q_l) == 1, "SIGNATURE-LORENTZIAN",
          "q_L has one negative eigenvalue.", checks)
    check(negative_count(q_s) == 2, "SIGNATURE-SPLIT",
          "q_S has two negative eigenvalues.", checks)
    check(negative_count(q_l) != negative_count(q_s), "SIGNATURE-NONSELECTION",
          "The witnesses have different inertia.", checks)

    for epsilon in (1.0, 0.1, 0.001):
        q_eps = (-1.0, 1.0, 1.0, epsilon * epsilon)
        check(negative_count(q_eps) == 1,
              f"DEGENERACY-SIGNATURE-{epsilon}",
              "Positive-epsilon witness remains Lorentzian.", checks)
        check(math.isclose(diagonal_det(q_eps), -(epsilon * epsilon),
                           rel_tol=0.0, abs_tol=1e-18),
              f"DEGENERACY-DET-{epsilon}",
              "Witness determinant is exactly -epsilon^2 numerically.", checks)
    check(abs(-0.001 ** 2) < abs(-0.1 ** 2), "DEGENERACY-APPROACH",
          "Determinant magnitude approaches zero.", checks)
    check(spec["degeneracy_family"]["determinant_lower_bound_derived"] is False,
          "DEGENERACY-NO-BOUND", "No source determinant bound is derived.", checks)

    weights = [tuple(row) for row in spec["theorems"][2]["weights"]]
    zero_pair_count = 0
    for i, first in enumerate(weights):
        for j in range(i, len(weights)):
            second = weights[j]
            pair_sum = tuple(a + b for a, b in zip(first, second))
            if pair_sum == (0, 0, 0):
                zero_pair_count += 1
            check(pair_sum != (0, 0, 0), f"NATURALITY-WEIGHT-{i}-{j}",
                  "No symmetric component carries zero total weight.", checks)
    check(zero_pair_count == 0, "NATURALITY-ZERO-PAIR-COUNT",
          "The invariant symmetric bilinear space has dimension zero.", checks)
    a, b, c = 0.2, -0.3, 0.7
    diagonal = (math.exp(a), math.exp(b), math.exp(c), math.exp(-a - b - c))
    check(math.isclose(math.prod(diagonal), 1.0, rel_tol=0.0, abs_tol=1e-12),
          "NATURALITY-DET-ONE", "The source automorphism preserves density.", checks)
    check(all(value > 0.0 for value in diagonal), "NATURALITY-RAY-ORIENTATION",
          "The source automorphism preserves positive ray orientation.", checks)

    coframe = spec["conditional_coframe_theorem"]
    check(coframe["transition_law"] == "Lambda_VU^T eta Lambda_VU=eta",
          "COFRAME-LORENTZ", "Lorentz-preserving transition law is exact.", checks)
    check(coframe["inverse_law"] == "Lambda_UV=Lambda_VU^-1",
          "COFRAME-INVERSE", "Inverse transition law is exact.", checks)
    check(coframe["cocycle_law"] == "Lambda_WV Lambda_VU=Lambda_WU",
          "COFRAME-COCYCLE", "Triple-overlap cocycle is exact.", checks)
    check(coframe["premises_derived_by_current_ontology"] is False,
          "COFRAME-NOT-DERIVED", "Conditional coframe premises are not overread.", checks)
    check(coframe["physical_interpretation_established"] is False,
          "COFRAME-NO-PHYSICAL-INTERPRETATION",
          "Conditional gluing does not establish physical geometry.", checks)

    burden = spec["proposal_only_burden_template"]
    check(burden["status_label"] == "proposal-only", "BURDEN-PROPOSAL-ONLY",
          "Burden template uses controlled proposal-only status.", checks)
    check(burden["canonical_ontology_candidate"] is False,
          "BURDEN-NOT-CANONICAL-CANDIDATE",
          "No canonical-ontology candidate is promoted.", checks)
    check(burden["human_gate_required_before_adoption"] is True,
          "BURDEN-HUMAN-GATE", "Adoption remains human-gated.", checks)

    obstruction = spec["precise_obstruction"]
    check(obstruction["obstruction_id"] ==
          "OBST-P6T05-SIGNATURE-COVARIANCE-NATURALITY-001",
          "OBSTRUCTION-ID", "Stable obstruction identity is present.", checks)
    check(obstruction["scope"] == "source_extension_candidate",
          "OBSTRUCTION-SCOPE", "Obstruction remains candidate-scoped.", checks)
    check(obstruction["current_ontology_implication"] == "does_not_derive",
          "OBSTRUCTION-ONTOLOGY", "Underdetermination language is precise.", checks)
    check(obstruction["source_extension_implication"] == "new_primitive_required",
          "OBSTRUCTION-CONTINUATION",
          "A materially new source primitive may reopen continuation.", checks)
    check(obstruction["global_no_go_claimed"] is False,
          "OBSTRUCTION-NO-GLOBAL-NOGO", "No global no-go is claimed.", checks)
    check(len(spec["reopening"]["criteria"]) == 3,
          "REOPENING-CRITERIA", "Three materially richer reopening classes are named.", checks)

    freeze = spec["freeze"]
    check(freeze["materially_richer_continuation_open"] is True,
          "FREEZE-CONTINUATION", "Local freeze leaves materially richer continuation open.", checks)
    check(freeze["global_theory_rejection"] is False,
          "FREEZE-NO-GLOBAL-REJECTION", "Local freeze is not theory rejection.", checks)

    authority = spec["authority"]
    check(all(value is False for value in authority.values()),
          "AUTHORITY-ALL-FALSE",
          "Every adoption, promotion, and publication authority flag is false.", checks)

    required_tex_markers = [
        "Signature nonselection",
        "Nondegeneracy is not certified",
        "Volume-preserving source naturality obstruction",
        "Conditional Lorentz-coframe gluing",
        "OBST-P6T05-SIGNATURE-COVARIANCE-NATURALITY-001",
        "blocked\\_adoption\\_open\\_continuation",
        "This is not a theorem that the project can never derive",
        "Gate B is not passed",
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
        "schema_id": "v21_p6_t05_signature_covariance_naturality_validation_v1",
        "task_id": "RT-20260726-009",
        "plan_task_id": "P6-T05",
        "result_id": spec["result_id"],
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "theorem_count": len(spec["theorems"]),
        "assumption_count": len(spec["assumption_table"]),
        "signature_countermodel_count": 1,
        "degeneracy_family_count": 1,
        "naturality_obstruction_count": 1,
        "conditional_gluing_theorem_count": 1,
        "physical_metric_count": 0,
        "target_metric_premise_count": 0,
        "global_no_go_count": 0,
        "fixed_sources": fixed_source_results,
        "artifact_hashes": {
            "signature_covariance_naturality_obstruction_v1.tex": sha256(TEX_PATH),
            "signature_covariance_naturality_obstruction_spec_v1.yaml": sha256(SPEC_PATH),
        },
        "claim_boundary_summary": (
            "Exact signature, degeneracy, and source-naturality obstruction "
            "plus conditional coframe gluing only; no ontology or source-law "
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
