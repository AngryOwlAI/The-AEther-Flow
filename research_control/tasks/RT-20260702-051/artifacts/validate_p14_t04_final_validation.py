#!/usr/bin/env python3
"""Validate v14 P14-T04 final validation command receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260702-051"
OUTPUT_DIR = (
    "research_control/tasks/RT-20260702-051/artifacts/"
    "final_validation_command_outputs"
)

PATHS = {
    "task": "research_control/tasks/RT-20260702-051/00_TASK.yaml",
    "decision": "research_control/tasks/RT-20260702-051/DDR-20260702-051.md",
    "receipt": "research_control/tasks/RT-20260702-051/artifacts/p14_t04_v14_final_validation_receipt.md",
    "completion": "research_control/tasks/RT-20260702-051/jobs/completions/AJC-AJ-RT-20260702-051-001.yaml",
    "handoff": "research_control/handoffs/handoff-0504.yaml",
    "program_state": "research_control/program_state.yaml",
    "current_frontier": "research_control/current_frontier.md",
    "plan": "implementations_plans/recommendations_implementation_plan_continue_task-v14.md",
    "bootstrap": f"{OUTPUT_DIR}/command_01_bootstrap_memory_system.txt",
    "bootstrap_validate_only": f"{OUTPUT_DIR}/command_02_bootstrap_memory_system_validate_only.txt",
    "classifier": f"{OUTPUT_DIR}/command_03_classify_project_changes.json",
    "signals": f"{OUTPUT_DIR}/command_04_collect_project_improvement_signals.txt",
    "documentation_impact": f"{OUTPUT_DIR}/command_05_validate_documentation_impact.txt",
    "claim_language": f"{OUTPUT_DIR}/command_06_validate_claim_language.json",
    "research_control": f"{OUTPUT_DIR}/command_07_validate_research_control.txt",
    "research_control_check_diff": f"{OUTPUT_DIR}/command_08_validate_research_control_check_diff.txt",
    "metrics": f"{OUTPUT_DIR}/command_09_report_physics_progress_metrics.json",
    "frontier_check": f"{OUTPUT_DIR}/command_10_render_current_frontier_check.txt",
    "unit_tests": f"{OUTPUT_DIR}/command_11_unittest_discover.txt",
    "git_diff_check": f"{OUTPUT_DIR}/command_12_git_diff_check.txt",
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict[str, Any]:
    return json.loads(read_text(path))


def digest(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def add_check(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"id": check_id, "passed": bool(passed), "detail": detail})


def contains(path: str, needle: str) -> bool:
    return needle in read_text(path)


def no_fail_text(path: str) -> bool:
    text = read_text(path)
    forbidden = ["Traceback", "FAILED", "FAIL\n", "ERROR", "failed:"]
    return not any(token in text for token in forbidden)


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    plan = read_text(PATHS["plan"])
    completion = read_text(PATHS["completion"])
    handoff = read_text(PATHS["handoff"])
    program_state = read_text(PATHS["program_state"])
    current_frontier = read_text(PATHS["current_frontier"])
    receipt = read_text(PATHS["receipt"])

    add_check(
        checks,
        "plan_contains_p14_t04_required_commands",
        "P14-T04: V14 final validation" in plan
        and "validate_claim_language.py --json" in plan
        and "unittest discover -s tests" in plan,
        "v14 plan contains the P14-T04 command suite.",
    )
    add_check(
        checks,
        "program_state_routes_to_p14_t05",
        "v14_p14_t04_final_validation_passed_next_ordinary_handoff" in program_state
        and "P14-T05 ordinary research continuation handoff" in program_state,
        "program_state routes from P14-T04 to P14-T05.",
    )
    add_check(
        checks,
        "handoff_routes_to_p14_t05",
        "Run one bounded v14 P14-T05 ordinary research continuation handoff packet." in handoff,
        "handoff-0504 routes to P14-T05.",
    )
    add_check(
        checks,
        "completion_records_no_physics_promotion",
        "downstream_physics_promotion_authorized: false" in completion
        and "completed_derivation_authorized: false" in completion,
        "completion preserves no downstream physics promotion or completed derivation.",
    )
    add_check(
        checks,
        "receipt_records_validation_suite",
        "unit test discovery: PASS" in receipt
        and "claim-language validation: PASS" in receipt
        and "research-control validation: PASS" in receipt,
        "receipt records the required validation suite.",
    )
    add_check(
        checks,
        "current_frontier_updated",
        "RT-20260702-051" in current_frontier
        and "P14-T05 ordinary research continuation handoff" in current_frontier,
        "current frontier reflects the P14-T04 state transition.",
    )
    add_check(
        checks,
        "bootstrap_pass",
        contains(PATHS["bootstrap"], "Validation PASS"),
        "bootstrap_memory_system.py output contains Validation PASS.",
    )
    add_check(
        checks,
        "bootstrap_validate_only_pass",
        contains(PATHS["bootstrap_validate_only"], "Validation PASS"),
        "bootstrap_memory_system.py --validate-only output contains Validation PASS.",
    )

    classifier = read_json(PATHS["classifier"])
    add_check(
        checks,
        "classifier_pass",
        bool(classifier.get("docs_impact_required"))
        and not classifier.get("blocked_paths"),
        "classify_project_changes.py returned docs_impact_required=true with no blocked paths.",
    )
    add_check(
        checks,
        "signals_pass",
        contains(PATHS["signals"], "Project-improvement signal validation passed."),
        "collect_project_improvement_signals.py --validate-emitted passed.",
    )
    add_check(
        checks,
        "documentation_impact_pass",
        contains(PATHS["documentation_impact"], "Documentation-impact validation passed."),
        "validate_documentation_impact.py passed.",
    )

    claim_language = read_json(PATHS["claim_language"])
    add_check(
        checks,
        "claim_language_pass",
        claim_language.get("status") == "PASS"
        and int(claim_language.get("hard_fail_count", -1)) == 0,
        "validate_claim_language.py --json returned PASS with hard_fail_count=0.",
    )
    add_check(
        checks,
        "research_control_pass",
        contains(PATHS["research_control"], "Research-control validation passed."),
        "validate_research_control.py passed.",
    )
    add_check(
        checks,
        "research_control_check_diff_pass",
        contains(PATHS["research_control_check_diff"], "Research-control validation passed."),
        "validate_research_control.py --check-diff passed.",
    )

    metrics = read_json(PATHS["metrics"])
    authority_boundary = metrics.get("authority_boundary", {})
    add_check(
        checks,
        "metrics_pass",
        metrics.get("report_id") == "research_control_metrics_separation"
        and authority_boundary.get("metrics_are_operational") is True
        and authority_boundary.get("physics_claim_promotion_authorized") is False,
        "report_physics_progress_metrics.py returned operational diagnostics with no physics promotion authority.",
    )
    add_check(
        checks,
        "frontier_check_pass",
        no_fail_text(PATHS["frontier_check"]),
        "render_current_frontier.py --check returned no failure text.",
    )
    add_check(
        checks,
        "unit_tests_pass",
        contains(PATHS["unit_tests"], "OK")
        and contains(PATHS["unit_tests"], "Ran ")
        and "FAILED (" not in read_text(PATHS["unit_tests"]),
        "python -m unittest discover -s tests passed.",
    )
    add_check(
        checks,
        "git_diff_check_pass",
        read_text(PATHS["git_diff_check"]).strip() == "",
        "git diff --check produced no output.",
    )

    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "validator_id": "validate_p14_t04_final_validation",
        "task_id": TASK_ID,
        "status": status,
        "checks": checks,
        "source_hashes": {name: digest(path) for name, path in PATHS.items()},
        "claim_boundary": {
            "proof_authority": False,
            "source_law_adoption_authorized": False,
            "rr_e_transport_law_adoption_authorized": False,
            "unrestricted_rr_e_irrelevance_authorized": False,
            "matter_semantics_adoption_authorized": False,
            "detector_semantics_adoption_authorized": False,
            "downstream_physics_promotion_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
        },
        "phase_result": {
            "p14_t04_validated": status == "PASS",
            "next_plan_task_id": "P14-T05",
            "next_route": "ordinary research continuation handoff",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    output_path = ROOT / args.output
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
