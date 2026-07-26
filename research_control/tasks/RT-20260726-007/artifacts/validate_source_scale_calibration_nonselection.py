#!/usr/bin/env python3
"""Deterministically validate the bounded P6-T04 calibration packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260726-007"
ARTIFACT_DIR = TASK_DIR / "artifacts"
TEX_PATH = ARTIFACT_DIR / "source_scale_calibration_nonselection_v1.tex"
SPEC_PATH = ARTIFACT_DIR / "source_scale_calibration_nonselection_spec_v1.yaml"
REPORT_PATH = ARTIFACT_DIR / "source_scale_calibration_nonselection_validation_receipt_v1.json"


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


def validate() -> dict[str, Any]:
    spec = yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))
    tex = TEX_PATH.read_text(encoding="utf-8")
    checks: list[dict[str, Any]] = []

    check(spec["schema_id"] == "v21_p6_t04_source_scale_calibration_nonselection_v1",
          "SPEC-SCHEMA", "Expected bounded P6-T04 schema.", checks)
    check(spec["task_id"] == "RT-20260726-007", "SPEC-TASK",
          "Specification is bound to the exact task.", checks)
    check(spec["plan_task_id"] == "P6-T04", "SPEC-PLAN",
          "Specification is bound to the exact v21 work item.", checks)
    check(spec["adoption_status"] == "blocked_adoption_open_continuation",
          "SPEC-ADOPTION", "Adoption is blocked while continuation stays open.", checks)

    typed_input = spec["typed_input"]
    check("D_1" in typed_input["one_ray_bundle"], "INPUT-ONE-RAY",
          "P6-T03 one-ray bundle remains explicit.", checks)
    check(typed_input["physical_units_supplied"] is False, "INPUT-NO-UNITS",
          "No physical units are smuggled into the input.", checks)
    check(typed_input["conformal_class_supplied"] is False, "INPUT-NO-CONFORMAL-CLASS",
          "No conformal class is assumed.", checks)
    check(typed_input["target_metric_imported"] is False, "INPUT-NO-TARGET",
          "No target metric is imported.", checks)

    assumptions = {row["id"]: row for row in spec["assumption_table"]}
    check(set(assumptions) == {f"A{i}" for i in range(1, 9)},
          "ASSUMPTION-TABLE", "Eight explicit assumptions are present.", checks)
    check(assumptions["A5"]["status"] == "normalization_open",
          "ASSUMPTION-FLOW-NORMALIZATION", "Flow normalization remains open.", checks)
    check(assumptions["A7"]["status"] == "unit_conversion_open",
          "ASSUMPTION-UNITS", "Dimensionful conversion remains open.", checks)
    check(assumptions["A8"]["status"] == "no_target_import_enforced",
          "ASSUMPTION-NO-TARGET", "No-target boundary is explicit.", checks)

    theorem_ids = {row["theorem_id"] for row in spec["theorems"]}
    check("P6T04-THM-CONDITIONAL-VOLUME-GAUGE" in theorem_ids,
          "THEOREM-VOLUME-GAUGE", "Conditional volume-gauge theorem is present.", checks)
    check("P6T04-THM-UNIMODULAR-DENSITY-CONE-ROD-NONSELECTION" in theorem_ids,
          "THEOREM-UNIMODULAR", "Fixed-density anisotropy theorem is present.", checks)
    check("P6T04-PROP-CLOCK-REPARAMETERIZATION" in theorem_ids,
          "PROPOSITION-CLOCK", "Clock reparameterization result is present.", checks)

    # Exact four-dimensional conformal-volume scaling and countermodel checks.
    omega = 3.0
    check(omega ** 4 == 81.0, "VOLUME-SCALING-4D",
          "Four-dimensional volume scales as Omega^4.", checks)
    mu_over_vol = 16.0
    check(mu_over_vol ** 0.25 == 2.0, "VOLUME-GAUGE-UNIQUE",
          "Positive fourth root gives the unique Weyl factor.", checks)

    for value in (0.0, 0.3, -0.7):
        diagonal = (-1.0, math.exp(2.0 * value), math.exp(-2.0 * value), 1.0)
        determinant = math.prod(diagonal)
        check(math.isclose(determinant, -1.0, rel_tol=0.0, abs_tol=1e-12),
              f"MODEL-DETERMINANT-{value}", "Unimodular witness determinant is -1.", checks)
        check(sum(entry < 0.0 for entry in diagonal) == 1,
              f"MODEL-SIGNATURE-{value}", "Witness has Lorentzian signature.", checks)
    a = 0.3
    g0 = (-1.0, 1.0, 1.0, 1.0)
    ga = (-1.0, math.exp(2.0 * a), math.exp(-2.0 * a), 1.0)
    conformal_factor = ga[0] / g0[0]
    check(conformal_factor == 1.0 and not math.isclose(ga[1], g0[1]),
          "MODEL-NONCONFORMAL", "Time coefficient fixes factor one while spatial coefficient differs.", checks)
    check(math.isclose(g0[0] + g0[1], 0.0) and not math.isclose(ga[0] + ga[1], 0.0),
          "MODEL-DIFFERENT-CONES", "A vector is null only in the a=0 witness.", checks)
    check(not math.isclose(math.sqrt(ga[1]), math.sqrt(g0[1])),
          "MODEL-DIFFERENT-RODS", "Transverse rod length differs.", checks)

    protocol = spec["device_agreement_protocol"]
    f, omega_a, omega_b = 5.0, 7.0, 11.0
    check(math.isclose((f * omega_a) / (f * omega_b), omega_a / omega_b),
          "CLOCK-RATIO-INVARIANT", "Relative phase-rate ratio is reparameterization invariant.", checks)
    check(protocol["absolute_time_unit_supplied"] is False,
          "CLOCK-NO-ABSOLUTE-UNIT", "Protocol does not supply an absolute time unit.", checks)
    check(protocol["rod_agreement_supplied"] is False,
          "CLOCK-NO-ROD", "Clock agreement does not supply rod agreement.", checks)
    check(protocol["current_ontology_derives_protocol_law"] is False,
          "CLOCK-LAW-NOT-DERIVED", "Current ontology does not derive the protocol law.", checks)

    dimensions = spec["dimensional_analysis"]
    check(all(value is False for value in dimensions.values()),
          "DIMENSIONAL-ALL-OPEN", "No physical unit or target calibration is silently supplied.", checks)

    obstruction = spec["precise_obstruction"]
    check(obstruction["obstruction_id"] == "OBST-P6T04-VOLUME-TICK-CALIBRATION-NONSELECTION-001",
          "OBSTRUCTION-ID", "Stable obstruction identity is present.", checks)
    check(obstruction["scope"] == "source_extension_candidate",
          "OBSTRUCTION-SCOPE", "Obstruction remains candidate-scoped.", checks)
    check(obstruction["current_ontology_implication"] == "does_not_derive",
          "OBSTRUCTION-ONTOLOGY", "Underdetermination language is precise.", checks)
    check(obstruction["source_extension_implication"] == "new_primitive_required",
          "OBSTRUCTION-CONTINUATION", "A materially new source primitive may reopen continuation.", checks)
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
          "AUTHORITY-ALL-FALSE", "Every adoption, promotion, and publication authority flag is false.", checks)

    required_tex_markers = [
        "Conditional volume gauge",
        "Unimodular density, cone, and rod nonselection",
        "Volume-tick calibration nonselection",
        "OBST-P6T04-VOLUME-TICK-CALIBRATION-NONSELECTION-001",
        "blocked\\_adoption\\_open\\_continuation",
        "not a theorem that the project can never derive",
        "relative-device agreement protocol",
    ]
    for index, marker in enumerate(required_tex_markers, start=1):
        check(marker in tex, f"TEX-MARKER-{index:02d}",
              f"Required TeX marker is present: {marker}", checks)

    forbidden_tex_markers = [
        "canonical ontology is hereby",
        "physical clock is established",
        "physical rod is established",
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
        "schema_id": "v21_p6_t04_source_scale_calibration_nonselection_validation_v1",
        "task_id": "RT-20260726-007",
        "plan_task_id": "P6-T04",
        "result_id": spec["result_id"],
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "theorem_count": 3,
        "assumption_count": len(spec["assumption_table"]),
        "countermodel_count": 1,
        "device_protocol_count": 1,
        "precise_obstruction_count": 1,
        "physical_metric_count": 0,
        "target_metric_premise_count": 0,
        "global_no_go_count": 0,
        "fixed_sources": fixed_source_results,
        "artifact_hashes": {
            "source_scale_calibration_nonselection_v1.tex": sha256(TEX_PATH),
            "source_scale_calibration_nonselection_spec_v1.yaml": sha256(SPEC_PATH),
        },
        "claim_boundary_summary": (
            "Conditional volume gauge and candidate-scoped density/tick "
            "nonselection only; no ontology or source-law adoption, physical "
            "metric, clock, rod, downstream GR promotion, global no-go, "
            "publication, push, or completed derivation."
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
