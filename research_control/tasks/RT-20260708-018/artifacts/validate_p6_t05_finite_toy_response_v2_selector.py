#!/usr/bin/env python3
"""Validate the v18 P6-T05 finite toy response v2 selector packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-018"
RECEIPT = TASK / "artifacts/finite_toy_response_v2_selector_receipt.md"
REPORT = TASK / "artifacts/p6_t05_finite_toy_response_v2_selector_report.json"


REQUIRED_PRESENT = [
    'selected_route: "support_formalization_expansion"',
    'selected_next_plan_task_id: "P7-T01"',
    'selected_next_packet_type: "source_side_selector_primitive"',
    'selected_next_plan_route_type: "support_formalization_target_selector_v18"',
    'repair_mandatory: false',
    'freeze_mandatory: false',
    'freeze_decision: "not_frozen"',
    'changed: false',
    'ledger_row_updated: false',
    'payload_id: "P6T05-PAYLOAD-001"',
]

FORBIDDEN_PRESENT = [
    'target_metric_imported: true',
    'g_eff_constructed: true',
    'matter_coupling_derived: true',
    'benchmark_promoted: true',
    'completed_derivation_claimed: true',
    'source_law_adopted: true',
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
        TASK / "artifacts/child_phys_math_finite_toy_response_v2_selector.yaml",
        TASK / "artifacts/child_phys_phil_finite_toy_response_v2_selector.yaml",
        TASK / "artifacts/parent_conflict_review_finite_toy_response_v2_selector.yaml",
        TASK / "artifacts/parent_fusion_notes_finite_toy_response_v2_selector.md",
        TASK / "jobs/AJ-RT-20260708-018-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260708-018-001.yaml",
        TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260708-018.yaml",
        ROOT / "research_control/handoffs/handoff-0711.yaml",
    ]
    for path in expected_files:
        if not path.exists():
            failures.append(f"missing expected file: {path.relative_to(ROOT)}")

    return {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "selected_route": "support_formalization_expansion",
        "selected_next_plan_task_id": "P7-T01",
        "selected_next_packet_type": "source_side_selector_primitive",
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
