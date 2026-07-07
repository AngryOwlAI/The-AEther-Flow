"""Validate the v18 P1-T04 active-state bifurcation red-team review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control import strict_yaml
from scripts.research_control.validate_red_team_review_artifact import validate_review_file


TASK_DIR = Path("research_control/tasks/RT-20260707-011")
ARTIFACT = TASK_DIR / "artifacts/active_state_bifurcation_red_team_review_v1.md"
REPORT = TASK_DIR / "artifacts/p1_t04_active_state_bifurcation_red_team_report.json"
EXPECTED_REPAIR_ROUTE = "v18_p1_t04_repair_active_state_supersession_director_decision_guard"


def build_report() -> dict[str, object]:
    global_result = validate_review_file(ARTIFACT)
    data = strict_yaml.load(ARTIFACT)
    issues: list[str] = []

    allowed_results = {"pass", "repair_required", "fail_closed"}
    result = data.get("p1_review_result")
    if result not in allowed_results:
        issues.append(f"p1_review_result must be one of {sorted(allowed_results)}")
    if data.get("verdict") != "repair_required":
        issues.append("verdict must be repair_required for the recorded P1-T04 result")
    if data.get("repair_required") is not True:
        issues.append("repair_required must be true")
    if data.get("repair_route") != EXPECTED_REPAIR_ROUTE:
        issues.append("repair_route must route to the Director-decision supersession guard repair")
    if data.get("recommended_next_route") != EXPECTED_REPAIR_ROUTE:
        issues.append("recommended_next_route must match the repair route")
    if data.get("physics_promotion_authorized") is not False:
        issues.append("physics_promotion_authorized must be false")

    required_sources = {
        "implementations_plans/recommendations_implementation_plan_continue_task-v18.md",
        "research_control/design/active_state_bifurcation_policy_v1.md",
        "research_control/current_frontier.md",
        "output/compact_current_frontier_v16.yaml",
        "scripts/research_control/validate_research_control.py",
        "tests/test_validate_research_control.py",
        "research_control/handoffs/handoff-0679.yaml",
    }
    reviewed_sources = set(data.get("reviewed_source_paths", []))
    missing_sources = sorted(required_sources - reviewed_sources)
    if missing_sources:
        issues.append(f"missing required reviewed sources: {missing_sources}")

    question_status_by_id = {
        item.get("question_id"): item.get("status")
        for item in data.get("review_questions", [])
        if isinstance(item, dict)
    }
    expected_questions = {f"P1-T04-Q{index}" for index in range(1, 6)}
    missing_questions = sorted(expected_questions - set(question_status_by_id))
    if missing_questions:
        issues.append(f"missing review questions: {missing_questions}")
    if question_status_by_id.get("P1-T04-Q3") != "repair_required":
        issues.append("P1-T04-Q3 must be repair_required")
    if question_status_by_id.get("P1-T04-Q5") != "repair_required":
        issues.append("P1-T04-Q5 must be repair_required")
    if question_status_by_id.get("P1-T04-Q1") != "pass":
        issues.append("P1-T04-Q1 must pass")
    if question_status_by_id.get("P1-T04-Q2") != "pass":
        issues.append("P1-T04-Q2 must pass")

    done = data.get("done_criteria_status", {})
    if not isinstance(done, dict):
        issues.append("done_criteria_status must be a map")
    else:
        if done.get("review_result_is_allowed") is not True:
            issues.append("done_criteria_status.review_result_is_allowed must be true")
        if done.get("repair_route_selected_when_required") is not True:
            issues.append("done_criteria_status.repair_route_selected_when_required must be true")
        if done.get("pass_route_to_p2_t01_blocked_until_repair") is not True:
            issues.append("done_criteria_status.pass_route_to_p2_t01_blocked_until_repair must be true")

    status = "PASS" if not issues else "FAIL"
    return {
        "task_id": "RT-20260707-011",
        "plan_task_id": "P1-T04",
        "status": status,
        "artifact_path": ARTIFACT.as_posix(),
        "global_red_team_validator": global_result,
        "issues": issues,
        "review_result": result,
        "repair_required": data.get("repair_required"),
        "repair_route": data.get("repair_route"),
        "recommended_next_route": data.get("recommended_next_route"),
        "physics_promotion_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
