#!/usr/bin/env python3
"""Validate the v18 P5-T07 source detector/readout selector packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-013"
RECEIPT = TASK / "artifacts/source_detector_readout_route_selector_integration_receipt.md"
REPORT = TASK / "artifacts/p5_t07_source_detector_readout_route_selector_integration_report.json"


REQUIRED_PRESENT = [
    'selected_route: "proceed_to_finite_toy_response_v2"',
    'selected_next_plan_task_id: "P6-T01"',
    'selected_next_packet_type: "finite_toy_metric_response_model"',
    'repair_mandatory: false',
    'freeze_mandatory: false',
    'freeze_decision: "not_frozen"',
    'changed: false',
    'ledger_row_updated: false',
    'payload_id: "P5T07-PAYLOAD-001"',
]

FORBIDDEN_PRESENT = [
    'Det_src_adopted: true',
    'Readout_src_adopted: true',
    'detector_semantics_adopted: true',
    'source_detector_readout_semantics_adopted: true',
    'source_law_adopted: true',
    'coupling_law_adopted: true',
    'matter_coupling_derived: true',
    'benchmark_promoted: true',
    'completed_derivation_claimed: true',
]


def validate() -> dict:
    failures: list[str] = []
    if not RECEIPT.exists():
        failures.append(f"missing receipt: {RECEIPT}")
        text = ""
    else:
        text = RECEIPT.read_text(encoding="utf-8")

    for needle in REQUIRED_PRESENT:
        if needle not in text:
            failures.append(f"missing required text: {needle}")

    for needle in FORBIDDEN_PRESENT:
        if needle in text:
            failures.append(f"forbidden promotion text present: {needle}")

    expected_files = [
        TASK / "artifacts/child_phys_math_source_detector_readout_route_selector_integration.yaml",
        TASK / "artifacts/child_phys_phil_source_detector_readout_route_selector_integration.yaml",
        TASK / "artifacts/parent_conflict_review_source_detector_readout_route_selector_integration.yaml",
        TASK / "artifacts/parent_fusion_notes_source_detector_readout_route_selector_integration.md",
        TASK / "jobs/AJ-RT-20260708-013-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260708-013-001.yaml",
        TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260708-013.yaml",
        ROOT / "research_control/handoffs/handoff-0706.yaml",
    ]
    for path in expected_files:
        if not path.exists():
            failures.append(f"missing expected file: {path.relative_to(ROOT)}")

    return {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "selected_route": "proceed_to_finite_toy_response_v2",
        "selected_next_plan_task_id": "P6-T01",
        "repair_mandatory": False,
        "freeze_decision": "not_frozen",
        "adoption_requested": False,
        "ledger_delta_requested": False,
        "physics_promotion_requested": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
