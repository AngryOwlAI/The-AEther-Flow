#!/usr/bin/env python3
"""Validate the v18 P11-T04 ordinary continuation handoff receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
REPORT = ROOT / "research_control/tasks/RT-20260709-005/artifacts/v18_ordinary_continuation_handoff_report.json"
HANDOFF = ROOT / "research_control/handoffs/handoff-0739.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
DISTANCE_LEDGER = ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"
METRIC_LEDGER = ROOT / "registries/METRIC_USE_LEDGER.csv"

EXPECTED_ROUTE = "EqSrc_family_closure_repair_or_stress"
EXPECTED_NEXT_PLAN_TASK = "P11-T05"
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
    completion = report.get("v18_completion", {})
    immediate = report.get("immediate_next_plan_packet", {})
    distance_delta = report.get("distance_to_gr_delta", {})
    dispositions = [
        row for row in report.get("route_family_disposition", [])
        if row.get("disposition") == "selected"
    ]

    if report.get("schema_id") != "v18_ordinary_continuation_handoff_report_v1":
        errors.append("wrong report schema_id")
    if report.get("task_id") != "RT-20260709-005":
        errors.append("wrong report task_id")
    if report.get("plan_task_id") != "P11-T04":
        errors.append("wrong report plan_task_id")
    if report.get("aggregate_status") != "PASS":
        errors.append("report aggregate_status is not PASS")
    if completion.get("completed_plan_tasks_this_packet") != ["P11-T04"]:
        errors.append("completed plan tasks this packet must be P11-T04 only")
    if completion.get("deferred_v18_plan_tasks_after_completion") != ["P11-T05", "P11-T06 if project-system signals exist"]:
        errors.append("deferred v18 plan tasks after completion mismatch")
    if completion.get("phase_p11_completed") is not False:
        errors.append("phase_p11_completed must remain false until coverage audit and optional bridge resolution")
    if completion.get("v18_completed") is not False:
        errors.append("v18_completed must remain false after P11-T04")
    if completion.get("ordinary_continuation_route_selected") is not True:
        errors.append("ordinary route selected flag must be true")
    if completion.get("final_handoff_selects_exactly_one_next_ordinary_route") is not True:
        errors.append("exact ordinary route flag must be true")
    if selected.get("route_id") != EXPECTED_ROUTE:
        errors.append("selected route_id mismatch")
    if selected.get("allowed_route_family") != EXPECTED_ROUTE:
        errors.append("selected allowed_route_family mismatch")
    if len(dispositions) != 1:
        errors.append("route_family_disposition does not have exactly one selected row")
    elif dispositions[0].get("route_family") != EXPECTED_ROUTE:
        errors.append("selected disposition row is not the expected route")
    if immediate.get("plan_task_id") != EXPECTED_NEXT_PLAN_TASK:
        errors.append("immediate next plan task must be P11-T05")
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
    handoff_route = handoff.get("selected_ordinary_continuation_route", {})
    selected_next = handoff.get("selected_next_route", {})
    if handoff.get("handoff_id") != "handoff-0739":
        errors.append("handoff id mismatch")
    if handoff.get("task_id") != "RT-20260709-005":
        errors.append("handoff task_id mismatch")
    if receipt.get("completed_plan_task_id") != "P11-T04":
        errors.append("handoff completed_plan_task_id mismatch")
    if receipt.get("selected_next_plan_task_id") != EXPECTED_NEXT_PLAN_TASK:
        errors.append("handoff selected_next_plan_task_id mismatch")
    if receipt.get("v18_completed") is not False:
        errors.append("handoff v18_completed must be false")
    if receipt.get("deferred_v18_plan_tasks_after_completion") != ["P11-T05", "P11-T06 if project-system signals exist"]:
        errors.append("handoff deferred task list mismatch")
    if handoff_route.get("route_id") != EXPECTED_ROUTE:
        errors.append("handoff selected ordinary route mismatch")
    if selected_next.get("plan_task_id") != EXPECTED_NEXT_PLAN_TASK:
        errors.append("handoff selected_next_route must point to P11-T05")

    if program_state.get("active_task_id") != "RT-20260709-005":
        errors.append("program_state active_task_id mismatch")
    if program_state.get("latest_handoff_id") != "handoff-0739":
        errors.append("program_state latest_handoff_id mismatch")
    if EXPECTED_NEXT_PLAN_TASK not in program_state.get("next_recommended_action", ""):
        errors.append("program_state next_recommended_action does not name P11-T05")

    result = {
        "schema_id": "v18_p11_t04_ordinary_handoff_validation_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "selected_route": selected.get("route_id"),
        "selected_route_count": len(dispositions),
        "next_plan_task_id": immediate.get("plan_task_id"),
        "v18_completed": bool(completion.get("v18_completed")),
        "ledger_hashes": {
            "distance_to_gr": sha256(DISTANCE_LEDGER),
            "metric_use": sha256(METRIC_LEDGER),
        },
        "checked_failure_modes": [
            "wrong_schema_or_task",
            "p11_t04_not_complete",
            "premature_v18_completion",
            "not_exactly_one_route_selected",
            "selected_route_not_allowed",
            "wrong_next_plan_task",
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
