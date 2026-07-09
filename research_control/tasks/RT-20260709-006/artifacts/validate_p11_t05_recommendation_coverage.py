#!/usr/bin/env python3
"""Validate the v18 P11-T05 recommendation coverage audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260709-006"
ARTIFACT_DIR = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACT_DIR / "v18_recommendation_coverage_audit_report.json"
AUDIT_PATH = ARTIFACT_DIR / "v18_recommendation_coverage_audit.md"
VALIDATION_REPORT_PATH = ARTIFACT_DIR / "p11_t05_recommendation_coverage_audit_validation.json"
EXPECTED = [f"V18-R{i:02d}" for i in range(1, 11)]


def validate() -> dict[str, object]:
    errors: list[str] = []
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    audit_text = AUDIT_PATH.read_text(encoding="utf-8")

    if report.get("plan_task_id") != "P11-T05":
        errors.append("report plan_task_id is not P11-T05")
    if report.get("physics_promotion_authorized") is not False:
        errors.append("physics_promotion_authorized must be false")
    if report.get("proof_authority") is not False:
        errors.append("proof_authority must be false")
    if report.get("expected_recommendation_ids") != EXPECTED:
        errors.append("expected recommendation id list mismatch")

    rows = report.get("coverage_rows", [])
    row_ids = [row.get("recommendation_id") for row in rows]
    if row_ids != EXPECTED:
        errors.append(f"coverage row ids mismatch: {row_ids}")

    for row in rows:
        rec = row.get("recommendation_id", "")
        if row.get("final_coverage_status") != "covered":
            errors.append(f"{rec} final status is not covered")
        if row.get("direct_backlog_task_count", 0) <= 0:
            errors.append(f"{rec} has no direct backlog task")
        if row.get("completed_direct_task_count") != row.get("direct_backlog_task_count"):
            errors.append(f"{rec} completed direct count does not match direct backlog count")
        if row.get("missing_direct_tasks"):
            errors.append(f"{rec} has missing direct tasks")
        if row.get("project_improvement_signal_required") is not False:
            errors.append(f"{rec} incorrectly requires a project-improvement signal")
        if row.get("physics_promotion_authorized") is not False:
            errors.append(f"{rec} authorizes physics promotion")
        if rec not in audit_text:
            errors.append(f"{rec} missing from audit markdown")

    completion = report.get("v18_completion", {})
    if completion.get("project_improvement_bridge_required") is not False:
        errors.append("project improvement bridge should not be required")
    if completion.get("conditional_plan_tasks_not_required_after_packet") != ["P11-T06"]:
        errors.append("P11-T06 must be recorded as conditional and not required")
    if completion.get("all_applicable_plan_tasks_proven") is not True:
        errors.append("all applicable v18 plan tasks must be proven")
    if completion.get("v18_success_criteria_met") is not True:
        errors.append("v18 success criteria must be met")

    if report.get("missing_or_partial_recommendation_count") != 0:
        errors.append("missing_or_partial_recommendation_count must be zero")
    if report.get("project_improvement_signals") != []:
        errors.append("project_improvement_signals must be empty")
    if report.get("selected_next_route", {}).get("route_id") != "EqSrc_family_closure_repair_or_stress":
        errors.append("selected next route must remain EqSrc_family_closure_repair_or_stress")
    if report.get("distance_to_gr_delta", {}).get("changed") is not False:
        errors.append("Distance-to-GR delta must be unchanged")

    for phrase in [
        "does not authorize physics promotion",
        "P11-T06 is not required",
        "EqSrc_family_closure_repair_or_stress",
    ]:
        if phrase not in audit_text:
            errors.append(f"audit markdown missing required phrase: {phrase}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "row_count": len(rows),
        "covered_count": sum(1 for row in rows if row.get("final_coverage_status") == "covered"),
        "project_improvement_bridge_required": completion.get("project_improvement_bridge_required"),
        "selected_next_route": report.get("selected_next_route", {}).get("route_id", ""),
        "audit_path": str(AUDIT_PATH.relative_to(ROOT)),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON validation report.")
    parser.add_argument("--write-report", action="store_true", help="Write validation report JSON beside artifacts.")
    args = parser.parse_args()
    result = validate()
    if args.write_report:
        VALIDATION_REPORT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
