#!/usr/bin/env python3
"""Validate the v18 P3-T06 post-EqSrc family-closure selector packet."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260707-024"
RECEIPT = TASK_ROOT / "artifacts/post_eqsrc_family_closure_selector_receipt.md"
CHILD_MATH = TASK_ROOT / "artifacts/child_phys_math_post_eqsrc_family_closure_selector.yaml"
CHILD_PHIL = TASK_ROOT / "artifacts/child_phys_phil_post_eqsrc_family_closure_selector.yaml"
CONFLICT_REVIEW = TASK_ROOT / "artifacts/parent_conflict_review_post_eqsrc_family_closure_selector.yaml"
FUSION_NOTES = TASK_ROOT / "artifacts/parent_fusion_notes_post_eqsrc_family_closure_selector.md"
COMPLETION = TASK_ROOT / "jobs/completions/AJC-AJ-RT-20260707-024-001.yaml"
OUTPUT = TASK_ROOT / "artifacts/post_eqsrc_family_closure_selector_validation.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    for path in [RECEIPT, CHILD_MATH, CHILD_PHIL, CONFLICT_REVIEW, FUSION_NOTES, COMPLETION]:
        if not path.exists():
            errors.append(f"missing required artifact: {path.relative_to(REPO_ROOT)}")

    receipt = read(RECEIPT) if RECEIPT.exists() else ""
    completion = read(COMPLETION) if COMPLETION.exists() else ""
    combined = "\n".join(read(path) for path in [CHILD_MATH, CHILD_PHIL, CONFLICT_REVIEW, FUSION_NOTES] if path.exists())

    selected_routes = re.findall(r'selected_route:\s+"([^"]+)"', receipt)
    if "P4_T01_countermodel_obligation_system" not in selected_routes:
        errors.append("receipt does not select P4_T01_countermodel_obligation_system")
    conflicting_routes = [route for route in selected_routes if route != "P4_T01_countermodel_obligation_system"]
    if conflicting_routes:
        errors.append(f"receipt records conflicting selected_route values: {conflicting_routes}")
    if "selected_next_plan_task_id: \"P4-T01\"" not in receipt:
        errors.append("receipt does not select P4-T01")
    if "freeze_decision: \"not_frozen\"" not in receipt:
        errors.append("freeze criteria are not evaluated as not_frozen")
    if "repair_mandatory: false" not in receipt:
        errors.append("repair_mandatory=false is missing")
    if "requires_human_gate: false" not in receipt:
        errors.append("selector must not require a human gate")
    if "P4_T01_countermodel_obligation_system" not in combined:
        errors.append("parent-child synthesis does not agree on P4_T01")
    if "unresolved_conflicts: []" not in receipt and "unresolved_conflicts: []" not in combined:
        errors.append("unresolved conflict absence is not recorded")
    forbidden_positive_claim_patterns = [
        r"general EqSrc discharge follows",
        r"RetainH is adopted",
        r"GenH is adopted",
        r"source law is adopted",
        r"matter coupling is derived",
        r"Einstein equations are derived",
        r"benchmark is promoted",
        r"completed derivation (?:is authorized|follows)",
        r"is a completed derivation",
    ]
    for pattern in forbidden_positive_claim_patterns:
        if re.search(pattern, receipt):
            errors.append(f"forbidden promoted wording appears: {pattern}")
    if "theoretical_decision_output:" not in completion:
        errors.append("completion is missing theoretical_decision_output")
    if "completed_v18_tasks_this_packet" not in completion or "P3-T06" not in completion:
        errors.append("completion does not record P3-T06 implementation receipt")

    report = {
        "schema_id": "post_eqsrc_family_closure_selector_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "selected_route": "P4_T01_countermodel_obligation_system" if not errors else "",
        "selected_next_plan_task_id": "P4-T01" if not errors else "",
        "freeze_decision": "not_frozen" if not errors else "",
        "claim_boundary_preserved": not errors,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
