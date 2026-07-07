#!/usr/bin/env python3
"""Validate RT-20260707-012 active-state supersession guard repair."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260707-012"
    / "artifacts"
    / "p1_t04_active_state_supersession_guard_report.json"
)


def run_command(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
    }


def build_report() -> dict[str, object]:
    validator_path = REPO_ROOT / "scripts" / "research_control" / "validate_research_control.py"
    test_path = REPO_ROOT / "tests" / "test_validate_research_control.py"
    fixture_path = (
        REPO_ROOT
        / "tests"
        / "fixtures"
        / "research_control"
        / "active_state_sidecar_valid"
        / "director_decision_authorized_supersession.yaml"
    )
    validator_text = validator_path.read_text(encoding="utf-8")
    test_text = test_path.read_text(encoding="utf-8")
    fixture_text = fixture_path.read_text(encoding="utf-8")

    required_source_needles = [
        "SIDECAR_SUPERSESSION_DECISION_ID_FIELDS",
        "_director_decision_authorizes_sidecar_supersession",
        "flag-only sidecar supersession authorization is insufficient",
        "active_state_supersession_authorized",
        "active_state_supersession_scope",
    ]
    source_missing = [needle for needle in required_source_needles if needle not in validator_text]
    required_test_needles = [
        "test_sidecar_supersession_with_handoff_flag_but_no_tracked_decision_fails",
        "test_sidecar_supersession_with_tracked_director_decision_passes",
    ]
    test_missing = [needle for needle in required_test_needles if needle not in test_text]
    required_fixture_needles = [
        'sidecar_supersession_decision_id: "DDR-SIDE-001"',
        "active_state_supersession_authorized: true",
        "active_state_supersession_scope:",
    ]
    fixture_missing = [needle for needle in required_fixture_needles if needle not in fixture_text]

    commands = [
        run_command([sys.executable, "-m", "py_compile", str(validator_path.relative_to(REPO_ROOT))]),
        run_command([sys.executable, "-m", "unittest", "tests.test_validate_research_control"]),
    ]
    command_failures = [item for item in commands if item["returncode"] != 0]
    hard_failures = source_missing + test_missing + fixture_missing + [str(item["command"]) for item in command_failures]
    status = "PASS" if not hard_failures else "FAIL"
    return {
        "schema_id": "p1_t04_active_state_supersession_guard_report_v1",
        "task_id": "RT-20260707-012",
        "job_id": "AJ-RT-20260707-012-001",
        "plan_task_id": "P1-T04-repair",
        "status": status,
        "hard_failures": hard_failures,
        "validator_guard_present": not source_missing,
        "focused_tests_present": not test_missing,
        "decision_authorization_fixture_present": not fixture_missing,
        "physics_promotion_authorized": False,
        "no_physics_delta": True,
        "next_route_if_pass": "P2-T01",
        "commands": commands,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
