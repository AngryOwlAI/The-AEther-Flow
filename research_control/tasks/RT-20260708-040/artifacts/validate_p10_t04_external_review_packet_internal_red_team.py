#!/usr/bin/env python3
"""Validate v18 P10-T04 external-review packet internal red-team outputs."""

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
from scripts.research_control.validate_red_team_review_artifact import (  # noqa: E402
    validate_review_file,
)


TASK_ID = "RT-20260708-040"
JOB_ID = "AJ-RT-20260708-040-001"
ARTIFACT = (
    ROOT
    / "research_control/tasks/RT-20260708-040/artifacts/"
    / "external_review_packet_internal_red_team_v1.md"
)
TARGET_PACKET = ROOT / "external_review_packets/eqsrc_family_closure_review_packet_v1.md"
REPORT = (
    ROOT
    / "research_control/tasks/RT-20260708-040/artifacts/"
    / "p10_t04_external_review_packet_internal_red_team_report.json"
)
ALLOWED_RESULTS = {"pass", "repair_required", "fail_closed"}
REQUIRED_REVIEW_QUESTIONS = {
    "question_sharp_enough",
    "main_obstruction_visible",
    "scoped_objects_not_overclaimed",
    "useful_progress_not_underclaimed",
    "reviewer_can_answer_without_whole_repo",
    "external_endorsement_not_implied",
    "no_outreach_by_default_preserved",
}
REQUIRED_DONE_CRITERIA = {
    "review_result_allowed",
    "result_is_pass",
    "question_sharp_enough",
    "main_obstruction_visible",
    "scoped_objects_not_overclaimed",
    "useful_progress_not_underclaimed",
    "reviewer_can_answer_without_whole_repo",
    "external_endorsement_not_implied",
    "no_outreach_by_default_preserved",
    "pass_routes_to_p10_t05",
}
REQUIRED_TARGET_PACKET_PHRASES = [
    'external_outreach_performed: false',
    'reviewer_named: false',
    'external_review_completed: false',
    'endorsement_claimed: false',
    'next_route: "P10-T04"',
    "Does the conditional source-only `EqSrc_T` family-closure theorem candidate",
    "inverse closure",
    "composition closure",
    "ledger compatibility",
    "H-retention",
    "H-generation",
    "This packet does not ask for a broad repository tour",
]
REQUIRED_FORBIDDEN_CLAIMS = [
    "internal red-team pass as external endorsement",
    "general EqSrc discharge",
    "RetainH adoption",
    "GenH adoption",
    "source-law adoption",
    "matter-coupling derivation",
    "Einstein-equation derivation",
    "benchmark promotion",
    "Gate Chair verdict",
    "completed derivation",
]


def _as_map(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def _as_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    return value if isinstance(value, list) else []


def validate() -> dict[str, Any]:
    failures: list[str] = []
    schema_summary: dict[str, Any] = {}
    data: dict[str, Any] = {}

    if not ARTIFACT.exists():
        failures.append(f"missing artifact {ARTIFACT.relative_to(ROOT)}")
    else:
        try:
            schema_summary = validate_review_file(ARTIFACT)
        except Exception as exc:  # pragma: no cover - reported as data
            failures.append(f"global red-team schema validation failed: {exc}")
        data = strict_yaml.load(ARTIFACT)

    if data.get("task_id") != TASK_ID:
        failures.append("task_id mismatch")
    if data.get("agent_job_id") != JOB_ID:
        failures.append("agent_job_id mismatch")
    if data.get("plan_task_id") != "P10-T04":
        failures.append("plan_task_id must be P10-T04")
    if data.get("reviewed_object_id") != "MD-EXTERNAL-REVIEW-PACKET-EQSRC-FAMILY-CLOSURE-V1":
        failures.append("reviewed_object_id must name the external-review packet object")
    if "external_review_packets/eqsrc_family_closure_review_packet_v1.md" not in _as_list(data, "reviewed_source_paths"):
        failures.append("reviewed_source_paths must include the target packet path")
    if data.get("p10_review_result") not in ALLOWED_RESULTS:
        failures.append("p10_review_result must be pass repair_required or fail_closed")
    if data.get("p10_review_result") != "pass":
        failures.append("P10-T04 expected pass for this packet")
    if data.get("verdict") != "no_blocking_defect_found_as_written":
        failures.append("global red-team verdict must be no_blocking_defect_found_as_written")
    if data.get("recommended_next_route") != "P10-T05":
        failures.append("recommended_next_route must be P10-T05 on pass")
    if data.get("physics_promotion_authorized") is not False:
        failures.append("physics_promotion_authorized must be exactly false")
    if data.get("repair_required") is not False:
        failures.append("repair_required must be exactly false")
    if data.get("fail_closed") is not False:
        failures.append("fail_closed must be exactly false")
    for flag in (
        "external_outreach_performed",
        "reviewer_named",
        "external_review_completed",
        "endorsement_claimed",
    ):
        if data.get(flag) is not False:
            failures.append(f"{flag} must be exactly false")

    done = _as_map(data, "done_criteria_status")
    missing_done = sorted(REQUIRED_DONE_CRITERIA - set(done))
    if missing_done:
        failures.append(f"missing done criteria: {missing_done}")
    for field in REQUIRED_DONE_CRITERIA:
        if done.get(field) is not True:
            failures.append(f"done_criteria_status.{field} must be true")

    seven = _as_map(data, "seven_question_assessment")
    missing_questions = sorted(REQUIRED_REVIEW_QUESTIONS - set(seven))
    if missing_questions:
        failures.append(f"missing seven-question assessments: {missing_questions}")
    for question in REQUIRED_REVIEW_QUESTIONS:
        block = _as_map(seven, question)
        if not block.get("status"):
            failures.append(f"seven_question_assessment.{question}.status missing")
        if not _as_list(block, "evidence"):
            failures.append(f"seven_question_assessment.{question}.evidence missing")

    if not TARGET_PACKET.exists():
        failures.append(f"missing target packet {TARGET_PACKET.relative_to(ROOT)}")
        target_text = ""
    else:
        target_text = TARGET_PACKET.read_text(encoding="utf-8")
    for phrase in REQUIRED_TARGET_PACKET_PHRASES:
        if phrase not in target_text:
            failures.append(f"target packet missing phrase: {phrase}")

    pressure_points = _as_list(data, "external_mathematical_pressure_points")
    if len(pressure_points) < 3:
        failures.append("external_mathematical_pressure_points must contain at least three items")
    if data.get("minimal_countermodel_attempt", {}).get("attempted") is not False:
        failures.append("minimal_countermodel_attempt.attempted must be false for packet-review task")

    claim_boundary = _as_map(data, "claim_boundary")
    forbidden_claims = " ".join(str(item) for item in _as_list(claim_boundary, "forbidden_claims"))
    for phrase in REQUIRED_FORBIDDEN_CLAIMS:
        if phrase not in forbidden_claims:
            failures.append(f"missing forbidden claim phrase: {phrase}")

    return {
        "schema_id": "p10_t04_external_review_packet_internal_red_team_validator_v1",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "artifact_path": ARTIFACT.relative_to(ROOT).as_posix(),
        "target_packet_path": TARGET_PACKET.relative_to(ROOT).as_posix(),
        "global_schema_summary": schema_summary,
        "review_result": data.get("p10_review_result"),
        "verdict": data.get("verdict"),
        "recommended_next_route": data.get("recommended_next_route"),
        "done_criteria_status": done,
        "review_question_count": len(seven),
        "external_mathematical_pressure_point_count": len(pressure_points),
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
