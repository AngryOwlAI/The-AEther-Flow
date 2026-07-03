#!/usr/bin/env python3
"""Validate the v15 P11-T02 local CI-equivalent validator packet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
RUNNER_PATH = REPO_ROOT / "scripts/research_control/run_full_research_control_validation.py"
TEST_PATH = REPO_ROOT / "tests/test_run_full_research_control_validation.py"
REPORT_PATH = REPO_ROOT / "research_control/tasks/RT-20260703-021/artifacts/p11_t02_local_ci_equivalent_report.json"

REQUIRED_LABELS = {
    "memory_validate_only",
    "current_frontier_check",
    "dependency_graph_check",
    "claim_language_changed_lint",
    "documentation_impact_validation",
    "project_improvement_signal_validation",
    "research_control_validation",
    "research_control_diff_validation",
    "route_signature_extraction",
    "route_orbit_advisory",
    "whitespace_diff_check",
}

REQUIRED_SCRIPT_PHRASES = [
    "operational receipt evidence only",
    "physics proof authority",
    "no_physics_delta",
    "route_signature_extraction",
]


def load_runner():
    spec = importlib.util.spec_from_file_location("run_full_research_control_validation", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {RUNNER_PATH.relative_to(REPO_ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate() -> dict[str, object]:
    errors: list[str] = []

    if not RUNNER_PATH.exists():
        errors.append(f"missing runner: {RUNNER_PATH.relative_to(REPO_ROOT)}")
        runner_text = ""
        runner = None
    else:
        runner_text = RUNNER_PATH.read_text(encoding="utf-8")
        runner = load_runner()

    if not TEST_PATH.exists():
        errors.append(f"missing focused test: {TEST_PATH.relative_to(REPO_ROOT)}")
        test_text = ""
    else:
        test_text = TEST_PATH.read_text(encoding="utf-8")

    lower_script = runner_text.lower()
    for phrase in REQUIRED_SCRIPT_PHRASES:
        if phrase.lower() not in lower_script:
            errors.append(f"runner missing boundary or coverage phrase: {phrase}")

    plan_labels: set[str] = set()
    coverage: dict[str, bool] = {}
    if runner is not None:
        plan = runner.command_plan()
        plan_labels = {entry["label"] for entry in plan}
        coverage = runner.coverage_map(plan)
        missing_labels = sorted(REQUIRED_LABELS - plan_labels)
        if missing_labels:
            errors.append(f"runner command plan missing labels: {missing_labels}")
        false_coverage = sorted(label for label, value in coverage.items() if not value)
        if false_coverage:
            errors.append(f"runner required coverage contains false entries: {false_coverage}")

    for phrase in ["command_plan", "coverage_map", "operational_receipt_only", "no_physics_delta"]:
        if phrase not in test_text:
            errors.append(f"focused test missing phrase: {phrase}")

    report: dict[str, object] = {}
    if not REPORT_PATH.exists():
        errors.append(f"missing local CI report: {REPORT_PATH.relative_to(REPO_ROOT)}")
    else:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        if report.get("status") != "PASS":
            errors.append("local CI report status is not PASS")
        if report.get("operational_receipt_only") is not True:
            errors.append("local CI report does not preserve operational_receipt_only=true")
        if report.get("no_physics_delta") is not True:
            errors.append("local CI report does not preserve no_physics_delta=true")
        report_coverage = report.get("required_check_coverage", {})
        if not isinstance(report_coverage, dict) or not all(report_coverage.values()):
            errors.append("local CI report required_check_coverage is incomplete")

    return {
        "schema_id": "p11_t02_local_ci_equivalent_validator_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "runner_path": str(RUNNER_PATH.relative_to(REPO_ROOT)),
        "test_path": str(TEST_PATH.relative_to(REPO_ROOT)),
        "report_path": str(REPORT_PATH.relative_to(REPO_ROOT)),
        "required_labels": sorted(REQUIRED_LABELS),
        "plan_labels": sorted(plan_labels),
        "coverage": coverage,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
