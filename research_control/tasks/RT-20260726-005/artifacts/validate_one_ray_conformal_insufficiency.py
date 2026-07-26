#!/usr/bin/env python3
"""Deterministically validate the bounded P6-T03 one-ray obstruction packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260726-005"
ARTIFACT_DIR = TASK_DIR / "artifacts"
TEX_PATH = ARTIFACT_DIR / "one_ray_conformal_insufficiency_v1.tex"
SPEC_PATH = ARTIFACT_DIR / "one_ray_conformal_insufficiency_spec_v1.yaml"
REPORT_PATH = ARTIFACT_DIR / "one_ray_conformal_insufficiency_validation_receipt_v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant_diagonal(entries: list[float]) -> float:
    value = 1.0
    for entry in entries:
        value *= entry
    return value


def check(condition: bool, check_id: str, detail: str, checks: list[dict[str, Any]]) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        }
    )


def validate() -> dict[str, Any]:
    spec = yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))
    tex = TEX_PATH.read_text(encoding="utf-8")
    checks: list[dict[str, Any]] = []

    check(spec["schema_id"] == "v21_p6_t03_one_ray_conformal_insufficiency_v1",
          "SPEC-SCHEMA", "Expected bounded P6-T03 specification schema.", checks)
    check(spec["task_id"] == "RT-20260726-005", "SPEC-TASK",
          "Specification is bound to the exact task.", checks)
    check(spec["plan_task_id"] == "P6-T03", "SPEC-PLAN",
          "Specification is bound to the exact v21 work item.", checks)
    check(spec["adoption_status"] == "blocked_adoption_open_continuation",
          "SPEC-ADOPTION", "Adoption remains blocked while continuation stays open.", checks)

    typed_input = spec["typed_input"]
    check(typed_input["principal_polynomial"] == "P_x(xi)=xi(V_x)",
          "INPUT-PRINCIPAL-POLYNOMIAL", "The P6-T02 principal polynomial is exact.", checks)
    check("Ann(V_x)" in typed_input["characteristic_covectors"],
          "INPUT-CHARACTERISTIC", "The characteristic annihilator is retained.", checks)
    check("r V_x" in typed_input["dual_propagation_ray"],
          "INPUT-RAY", "The one-ray propagation datum is retained.", checks)

    assumptions = {row["id"]: row for row in spec["assumption_table"]}
    check(set(assumptions) == {f"A{i}" for i in range(1, 8)},
          "ASSUMPTION-TABLE", "Seven explicit assumptions are present.", checks)
    check(assumptions["A5"]["status"] == "deferred_to_later_burden",
          "ASSUMPTION-SCALE", "Overall scale is explicitly deferred.", checks)
    check(assumptions["A7"]["status"] == "enforced",
          "ASSUMPTION-NO-TARGET", "No-target-import boundary is explicit.", checks)

    theorem_ids = {row["theorem_id"] for row in spec["theorems"]}
    check("P6T03-THM-CHARACTERISTIC-HYPERPLANE-MISMATCH" in theorem_ids,
          "THEOREM-HYPERPLANE", "Hyperplane/null-cone mismatch theorem is present.", checks)
    check("P6T03-THM-ONE-RAY-CONFORMAL-NONSELECTION" in theorem_ids,
          "THEOREM-NONSELECTION", "One-ray conformal nonselection theorem is present.", checks)

    # Exact finite-dimensional countermodel checks.
    g0 = [-1.0, 1.0, 1.0, 1.0]
    g1 = [-1.0, 2.0, 1.0, 1.0]
    check(determinant_diagonal(g0) < 0 and determinant_diagonal(g1) < 0,
          "MODEL-NONDEGENERATE", "Both diagonal witnesses are nondegenerate Lorentzian.", checks)
    check(sum(value < 0 for value in g0) == 1 and sum(value < 0 for value in g1) == 1,
          "MODEL-SIGNATURE", "Each witness has exactly one negative direction.", checks)
    conformal_factor = g1[0] / g0[0]
    check(conformal_factor == 1.0 and g1[1] != conformal_factor * g0[1],
          "MODEL-NONCONFORMAL", "Time coefficient fixes factor one while first spatial coefficient differs.", checks)
    v_norms = (g0[0], g1[0])
    check(v_norms == (-1.0, -1.0), "MODEL-SHARED-TIMELIKE-RAY",
          "V is unit timelike for both witnesses.", checks)
    null_test = (g0[0] + g0[1], g1[0] + g1[1])
    check(null_test == (0.0, 1.0), "MODEL-DIFFERENT-NULL-CONES",
          "partial_s+partial_y1 is null only for the first witness.", checks)

    examples = spec["examples"]
    check(examples["uniqueness_failure"]["conformally_related"] is False,
          "EXAMPLE-UNIQUENESS", "Explicit conformal uniqueness failure is recorded.", checks)
    check(examples["null_ray_failure"]["conformally_unique"] is False,
          "EXAMPLE-NULL-RAY", "Chosen-null-ray insufficiency is recorded.", checks)
    check("identically zero" in examples["zero_field_degeneracy"]["result"],
          "EXAMPLE-ZERO-FIELD", "Zero-field degeneracy is fail-closed.", checks)
    check("independent" in examples["disconnected_control"]["result"],
          "EXAMPLE-DISCONNECTED", "Disconnected-component nonselection is explicit.", checks)
    check("no full smooth quadratic cone" in examples["multiple_sector_control"]["result"],
          "EXAMPLE-MULTI-SECTOR", "Finite-ray control blocks overread.", checks)

    obstruction = spec["precise_obstruction"]
    check(obstruction["obstruction_id"] == "OBST-P6T03-ONE-RAY-CONFORMAL-NONSELECTION-001",
          "OBSTRUCTION-ID", "Stable obstruction identity is present.", checks)
    check(obstruction["scope"] == "source_extension_candidate",
          "OBSTRUCTION-SCOPE", "Obstruction remains candidate-scoped.", checks)
    check(obstruction["current_ontology_implication"] == "does_not_derive",
          "OBSTRUCTION-ONTOLOGY", "Underdetermination language is precise.", checks)
    check(obstruction["source_extension_implication"] == "new_primitive_required",
          "OBSTRUCTION-CONTINUATION", "A materially new source primitive can reopen continuation.", checks)
    check(obstruction["global_no_go_claimed"] is False,
          "OBSTRUCTION-NO-GLOBAL-NOGO", "No global no-go is claimed.", checks)
    check(len(spec["reopening"]["criteria"]) == 3,
          "REOPENING-CRITERIA", "Three materially new reopening classes are named.", checks)

    authority = spec["authority"]
    check(all(value is False for value in authority.values()),
          "AUTHORITY-ALL-FALSE", "Every promotion, adoption, and publication authority flag is false.", checks)

    required_tex_markers = [
        "Hyperplane/null-cone mismatch",
        "One-ray conformal nonselection",
        "g_H=-ds^2+H_{ij}",
        "blocked\\_adoption\\_open\\_continuation",
        "not a theorem that the project can never derive",
        "No Lorentzian scale is fixed",
    ]
    for index, marker in enumerate(required_tex_markers, start=1):
        check(marker in tex, f"TEX-MARKER-{index:02d}",
              f"Required TeX marker is present: {marker}", checks)

    forbidden_tex_markers = [
        "canonical ontology is hereby",
        "physical causality is established",
        "effective metric is derived",
        "Einstein equations are derived",
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
        "schema_id": "v21_p6_t03_one_ray_conformal_insufficiency_validation_v1",
        "task_id": "RT-20260726-005",
        "plan_task_id": "P6-T03",
        "result_id": spec["result_id"],
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "theorem_count": len(spec["theorems"]),
        "assumption_count": len(spec["assumption_table"]),
        "uniqueness_example_count": 2,
        "degeneracy_control_count": 3,
        "precise_obstruction_count": 1,
        "physical_conformal_class_count": 0,
        "target_metric_premise_count": 0,
        "global_no_go_count": 0,
        "fixed_sources": fixed_source_results,
        "artifact_hashes": {
            "one_ray_conformal_insufficiency_v1.tex": sha256(TEX_PATH),
            "one_ray_conformal_insufficiency_spec_v1.yaml": sha256(SPEC_PATH),
        },
        "claim_boundary_summary": (
            "Candidate-scoped one-ray conformal nonselection only; no ontology or "
            "source-law adoption, physical causality, metric scale, downstream GR "
            "promotion, global no-go, publication, push, or completed derivation."
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
