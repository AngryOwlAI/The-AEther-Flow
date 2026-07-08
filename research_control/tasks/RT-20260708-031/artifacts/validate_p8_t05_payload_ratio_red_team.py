#!/usr/bin/env python3
"""Validate v18 P8-T05 payload-ratio red-team outputs."""

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


TASK_ID = "RT-20260708-031"
JOB_ID = "AJ-RT-20260708-031-001"
ARTIFACT = (
    ROOT
    / "research_control/tasks/RT-20260708-031/artifacts/"
    / "payload_ratio_red_team_review_v1.md"
)
REPORT = (
    ROOT
    / "research_control/tasks/RT-20260708-031/artifacts/"
    / "p8_t05_payload_ratio_red_team_report.json"
)
ALLOWED_RESULTS = {"pass", "repair_required", "fail_closed"}
REQUIRED_DONE_CRITERIA = {
    "review_result_allowed",
    "policy_encourages_theorem_countermodel_work",
    "necessary_repairs_not_suppressed",
    "no_false_pressure_block",
    "no_process_overcorrection_block",
    "no_research_distortion_block",
    "pass_routes_to_p9_t01",
}
FORBIDDEN_TRUE_FIELDS = (
    "physics_promotion_authorized",
    "repair_required",
    "fail_closed",
)
REQUIRED_PHRASES = (
    "theorem",
    "countermodel",
    "necessary repairs",
    "support-only",
    "P9-T01",
)


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
        except Exception as exc:  # pragma: no cover - failure path reported as data
            failures.append(f"global red-team schema validation failed: {exc}")
        data = strict_yaml.load(ARTIFACT)

    if data.get("task_id") != TASK_ID:
        failures.append("task_id mismatch")
    if data.get("agent_job_id") != JOB_ID:
        failures.append("agent_job_id mismatch")
    if data.get("plan_task_id") != "P8-T05":
        failures.append("plan_task_id must be P8-T05")
    if data.get("p8_review_result") not in ALLOWED_RESULTS:
        failures.append("p8_review_result must be pass repair_required or fail_closed")
    if data.get("p8_review_result") != "pass":
        failures.append("P8-T05 expected pass for this packet")
    if data.get("verdict") != "no_blocking_defect_found_as_written":
        failures.append("global red-team verdict must be no_blocking_defect_found_as_written")
    if data.get("recommended_next_route") != "P9-T01":
        failures.append("recommended_next_route must be P9-T01 on pass")
    for field in FORBIDDEN_TRUE_FIELDS:
        if data.get(field) is not False:
            failures.append(f"{field} must be exactly false")

    done = _as_map(data, "done_criteria_status")
    missing_done = sorted(REQUIRED_DONE_CRITERIA - set(done))
    if missing_done:
        failures.append(f"missing done criteria: {missing_done}")
    for field in REQUIRED_DONE_CRITERIA:
        if done.get(field) is not True:
            failures.append(f"done_criteria_status.{field} must be true")

    for section in (
        "false_pressure_assessment",
        "process_overcorrection_assessment",
        "research_distortion_assessment",
    ):
        assessment = _as_map(data, section)
        if assessment.get("blocking_defect_found") is not False:
            failures.append(f"{section}.blocking_defect_found must be false")
        if not assessment.get("summary"):
            failures.append(f"{section}.summary must be nonempty")

    claim_boundary = _as_map(data, "claim_boundary")
    combined_claim_text = " ".join(
        str(item)
        for item in (
            _as_list(claim_boundary, "allowed_claims")
            + _as_list(claim_boundary, "forbidden_claims")
            + _as_list(data, "external_mathematical_pressure_points")
            + [data.get("claim_under_review", "")]
        )
    )
    for phrase in REQUIRED_PHRASES:
        if phrase not in combined_claim_text:
            failures.append(f"missing boundary phrase: {phrase}")

    pressure_points = _as_list(data, "external_mathematical_pressure_points")
    if len(pressure_points) < 3:
        failures.append("external_mathematical_pressure_points must contain at least three items")
    if data.get("minimal_countermodel_attempt", {}).get("attempted") is not False:
        failures.append("minimal_countermodel_attempt.attempted must be false for review-only packet")

    return {
        "schema_id": "p8_t05_payload_ratio_red_team_validator_v1",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "artifact_path": ARTIFACT.relative_to(ROOT).as_posix(),
        "global_schema_summary": schema_summary,
        "review_result": data.get("p8_review_result"),
        "verdict": data.get("verdict"),
        "recommended_next_route": data.get("recommended_next_route"),
        "done_criteria_status": done,
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
