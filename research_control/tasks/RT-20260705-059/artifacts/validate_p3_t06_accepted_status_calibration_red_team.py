#!/usr/bin/env python3
"""Validate the v17 P3-T06 accepted-status calibration red-team packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.research_control import strict_yaml  # noqa: E402


TASK_ID = "RT-20260705-059"
JOB_ID = "AJ-RT-20260705-059-001"
ARTIFACT = (
    ROOT
    / "research_control/tasks/RT-20260705-059/artifacts/"
    / "accepted_status_calibration_red_team_review_v1.md"
)
REPORT = (
    ROOT
    / "research_control/tasks/RT-20260705-059/artifacts/"
    / "p3_t06_accepted_status_calibration_red_team_report.json"
)
REQUIRED_OBJECTS = {"m_src", "g_eff", "matter_coupling"}
REQUIRED_QUESTION_IDS = {f"P3-T06-Q{index}" for index in range(1, 8)}
ALLOWED_P3_RESULTS = {"pass", "pass_with_advisory", "repair_required"}
FORBIDDEN_TRUE_FIELDS = (
    "physics_promotion_authorized",
    "repair_required",
)


def _list_items(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    return value if isinstance(value, list) else []


def validate() -> dict[str, Any]:
    failures: list[str] = []
    if not ARTIFACT.exists():
        failures.append(f"missing artifact {ARTIFACT.relative_to(ROOT)}")
        data: dict[str, Any] = {}
    else:
        data = strict_yaml.load(ARTIFACT)

    if data.get("task_id") != TASK_ID:
        failures.append("task_id mismatch")
    if data.get("agent_job_id") != JOB_ID:
        failures.append("agent_job_id mismatch")
    if data.get("p3_review_result") not in ALLOWED_P3_RESULTS:
        failures.append("p3_review_result must be pass pass_with_advisory or repair_required")
    if data.get("verdict") != "no_blocking_defect_found_as_written":
        failures.append("global red-team verdict must be no_blocking_defect_found_as_written")
    if data.get("recommended_next_route") != "v17_p4_t01_detector_semantics_replacement_problem_statement":
        failures.append("recommended_next_route must route to v17 P4-T01")
    for field in FORBIDDEN_TRUE_FIELDS:
        if data.get(field) is not False:
            failures.append(f"{field} must be exactly false")

    per_object = _list_items(data, "per_object_findings")
    object_ids = {item.get("object_id") for item in per_object if isinstance(item, dict)}
    missing_objects = REQUIRED_OBJECTS - object_ids
    if missing_objects:
        failures.append(f"missing per-object findings: {sorted(missing_objects)}")
    for item in per_object:
        if not isinstance(item, dict):
            failures.append("per_object_findings entries must be maps")
            continue
        object_id = item.get("object_id")
        if object_id not in REQUIRED_OBJECTS:
            continue
        for flag in (
            "positive_status_identified",
            "exact_scope_identified",
            "allowed_use_identified",
            "blocked_overread_identified",
        ):
            if item.get(flag) is not True:
                failures.append(f"{object_id}: {flag} must be true")
        if item.get("overclaim_found") is not False:
            failures.append(f"{object_id}: overclaim_found must be false")
        if item.get("underclaim_found") is not False:
            failures.append(f"{object_id}: underclaim_found must be false")

    questions = _list_items(data, "review_questions")
    question_ids = {item.get("question_id") for item in questions if isinstance(item, dict)}
    missing_questions = REQUIRED_QUESTION_IDS - question_ids
    if missing_questions:
        failures.append(f"missing review questions: {sorted(missing_questions)}")
    for item in questions:
        if isinstance(item, dict) and item.get("status") not in ALLOWED_P3_RESULTS:
            failures.append(f"{item.get('question_id')}: invalid review question status")

    gate = data.get("gate_chair_routing_assessment")
    if not isinstance(gate, dict) or gate.get("gate_chair_required_now") is not False:
        failures.append("gate_chair_routing_assessment.gate_chair_required_now must be false")

    distance = data.get("distance_to_gr_status")
    if not isinstance(distance, dict):
        failures.append("distance_to_gr_status must be present")
    else:
        if distance.get("ledger_row_updated") is not False:
            failures.append("distance_to_gr_status.ledger_row_updated must be false")
        if distance.get("status_before") != distance.get("status_after"):
            failures.append("distance_to_gr_status must record no status delta")

    return {
        "schema_id": "p3_t06_accepted_status_calibration_red_team_validator_v1",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "artifact_path": ARTIFACT.relative_to(ROOT).as_posix(),
        "review_result": data.get("p3_review_result"),
        "verdict": data.get("verdict"),
        "recommended_next_route": data.get("recommended_next_route"),
        "reviewed_objects": sorted(object_ids),
        "question_count": len(question_ids),
        "physics_promotion_authorized": data.get("physics_promotion_authorized"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
