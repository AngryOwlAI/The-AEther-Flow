#!/usr/bin/env python3
"""Validate the v17 P13-T04 ordinary continuation handoff receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
REPORT = ROOT / "research_control/tasks/RT-20260707-002/artifacts/v17_ordinary_continuation_handoff_report.json"
HANDOFF = ROOT / "research_control/handoffs/handoff-0672.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
DISTANCE_LEDGER = ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"
METRIC_LEDGER = ROOT / "registries/METRIC_USE_LEDGER.csv"

EXPECTED_ROUTE = "upstream_EqSrc_RetainH_GenH_theorem_attempt"
EXPECTED_DISTANCE_HASH = "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61"
EXPECTED_METRIC_HASH = "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    report = json.loads(REPORT.read_text())
    handoff = yaml.safe_load(HANDOFF.read_text())
    program_state = yaml.safe_load(PROGRAM_STATE.read_text())

    selected = report.get("selected_ordinary_continuation_route", {})
    completion = report.get("v17_completion", {})
    distance_delta = report.get("distance_to_gr_delta", {})
    dispositions = [
        row for row in report.get("route_family_disposition", [])
        if row.get("disposition") == "selected"
    ]

    if report.get("schema_id") != "v17_ordinary_continuation_handoff_report_v1":
        errors.append("wrong report schema_id")
    if report.get("task_id") != "RT-20260707-002":
        errors.append("wrong report task_id")
    if report.get("plan_task_id") != "P13-T04":
        errors.append("wrong report plan_task_id")
    if report.get("aggregate_status") != "PASS":
        errors.append("report aggregate_status is not PASS")
    if completion.get("implemented_v17_plan_tasks_after_completion") != 57:
        errors.append("implemented_v17_plan_tasks_after_completion is not 57")
    if completion.get("deferred_v17_plan_tasks_after_completion") != []:
        errors.append("deferred_v17_plan_tasks_after_completion is not empty")
    if not completion.get("phase_p13_completed"):
        errors.append("phase_p13_completed is not true")
    if not completion.get("all_applicable_plan_tasks_proven"):
        errors.append("all_applicable_plan_tasks_proven is not true")
    if not completion.get("final_handoff_selects_exactly_one_next_ordinary_route"):
        errors.append("final handoff exact-route flag is not true")
    if selected.get("route_id") != EXPECTED_ROUTE:
        errors.append("selected route_id mismatch")
    if selected.get("allowed_route_family") != EXPECTED_ROUTE:
        errors.append("selected allowed_route_family mismatch")
    if len(dispositions) != 1:
        errors.append("route_family_disposition does not have exactly one selected row")
    elif dispositions[0].get("route_family") != EXPECTED_ROUTE:
        errors.append("selected disposition row is not the expected route")
    if distance_delta.get("changed") is not False:
        errors.append("distance_to_gr_delta.changed is not false")
    if distance_delta.get("effect") != "no_distance_delta":
        errors.append("distance_to_gr_delta.effect is not no_distance_delta")
    if report.get("physics_promotion_authorized") is not False:
        errors.append("physics promotion is not false")
    if sha256(DISTANCE_LEDGER) != EXPECTED_DISTANCE_HASH:
        errors.append("Distance-to-GR ledger hash changed")
    if sha256(METRIC_LEDGER) != EXPECTED_METRIC_HASH:
        errors.append("Metric-use ledger hash changed")

    receipt = handoff.get("implementation_plan_receipt", {})
    route = handoff.get("selected_ordinary_continuation_route", {})
    if handoff.get("handoff_id") != "handoff-0672":
        errors.append("handoff id mismatch")
    if handoff.get("task_id") != "RT-20260707-002":
        errors.append("handoff task_id mismatch")
    if receipt.get("completed_plan_task_id") != "P13-T04":
        errors.append("handoff completed_plan_task_id mismatch")
    if receipt.get("implemented_v17_plan_tasks_after_completion") != 57:
        errors.append("handoff implemented task count mismatch")
    if receipt.get("deferred_v17_plan_tasks_after_completion") != []:
        errors.append("handoff deferred tasks are not empty")
    if not receipt.get("all_applicable_plan_tasks_proven"):
        errors.append("handoff all_applicable_plan_tasks_proven is not true")
    if route.get("route_id") != EXPECTED_ROUTE:
        errors.append("handoff selected ordinary route mismatch")

    if program_state.get("active_task_id") != "RT-20260707-002":
        errors.append("program_state active_task_id mismatch")
    if program_state.get("latest_handoff_id") != "handoff-0672":
        errors.append("program_state latest_handoff_id mismatch")
    if "upstream EqSrc RetainH GenH" not in program_state.get("next_recommended_action", ""):
        errors.append("program_state next_recommended_action does not name selected route family")

    result = {
        "schema_id": "v17_p13_t04_ordinary_handoff_validation_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "selected_route": selected.get("route_id"),
        "selected_route_count": len(dispositions),
        "v17_completed": bool(completion.get("all_applicable_plan_tasks_proven")),
        "ledger_hashes": {
            "distance_to_gr": sha256(DISTANCE_LEDGER),
            "metric_use": sha256(METRIC_LEDGER),
        },
        "checked_failure_modes": [
            "wrong_schema_or_task",
            "v17_not_fully_proven",
            "deferred_tasks_remaining",
            "not_exactly_one_route_selected",
            "selected_route_not_allowed",
            "ledger_hash_changed",
            "physics_promotion_authorized",
            "handoff_program_state_mismatch",
        ],
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"status={result['status']}")
        for error in errors:
            print(f"error: {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
