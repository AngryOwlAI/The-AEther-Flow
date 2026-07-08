#!/usr/bin/env python3
"""Validate the v18 P10-T01 external-review question selector packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-037"
RECEIPT = TASK / "artifacts/external_review_question_selector_receipt.md"
REPORT = TASK / "artifacts/p10_t01_external_review_question_selector_report.json"


REQUIRED_PRESENT = [
    'selected_question_family: "EqSrc_family_closure"',
    'review_question_count: 1',
    'external_outreach_performed: false',
    'selected_next_plan_task_id: "P10-T02"',
    'selected_next_plan_route_type: "external_review_packet_source_spec"',
    'selected_next_role_family: "documentation-curator@2.0.0"',
    'changed: false',
    'ledger_row_updated: false',
    'payload_id: "P10T01-PAYLOAD-001"',
]

QUESTION_NEEDLES = [
    "record-local EqSrc witnesses",
    "family-level closure",
    "H1-H7 closure and ledger structure",
    "RetainH for H-retention",
    "GenH for H-generated families",
]

FORBIDDEN_PRESENT = [
    "external_outreach_performed: true",
    "source_law_adopted: true",
    "RetainH_adopted: true",
    "GenH_adopted: true",
    "matter_coupling_derived: true",
    "einstein_equations_derived: true",
    "benchmark_promoted: true",
    "completed_derivation_claimed: true",
    "global_no_go_claim_authorized: true",
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

    for needle in QUESTION_NEEDLES:
        if needle not in text:
            failures.append(f"selected question missing required focus: {needle}")

    for needle in FORBIDDEN_PRESENT:
        if needle in text:
            failures.append(f"forbidden promotion or outreach text present: {needle}")

    expected_files = [
        TASK / "artifacts/child_phys_math_external_review_question_selector.yaml",
        TASK / "artifacts/child_phys_phil_external_review_question_selector.yaml",
        TASK / "artifacts/parent_conflict_review_external_review_question_selector.yaml",
        TASK / "artifacts/parent_fusion_notes_external_review_question_selector.md",
        TASK / "jobs/AJ-RT-20260708-037-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260708-037-001.yaml",
        TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260708-037.yaml",
        ROOT / "research_control/handoffs/handoff-0730.yaml",
    ]
    for path in expected_files:
        if not path.exists():
            failures.append(f"missing expected file: {path.relative_to(ROOT)}")

    return {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "selected_question_family": "EqSrc_family_closure",
        "review_question_count": 1,
        "selected_next_plan_task_id": "P10-T02",
        "external_outreach_performed": False,
        "adoption_requested": False,
        "ledger_delta_requested": False,
        "physics_promotion_requested": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
