#!/usr/bin/env python3
"""Validate the v17 P3-T03 underclaim calibration linter packet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
UNDERCLAIM_FIXTURE = REPO_ROOT / "tests/fixtures/claim_language/accepted_underclaim_overcorrection.md"
VALID_FIXTURE = REPO_ROOT / "tests/fixtures/claim_language/accepted_calibrated_valid.md"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260705-056/artifacts/p3_t03_underclaim_linter_report.json"
)

REQUIRED_CLASSES = {
    "accepted_positive_status_missing",
    "accepted_scope_after_blocked_overread",
    "scoped_adoption_minimized",
    "caveat_wall_public_summary",
}


def load_linter():
    spec = importlib.util.spec_from_file_location("validate_claim_language", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
    }


def scan_report(linter: Any, path: str, text: str) -> dict[str, Any]:
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    findings = linter.scan_text_map(
        {path: text},
        taxonomy=taxonomy,
        reviewed_contexts=[],
        active_handoffs={"research_control/handoffs/handoff-0629.yaml"},
    )
    return linter.report_dict(findings, scanned_paths=[path])


def build_report() -> dict[str, Any]:
    linter = load_linter()
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    class_ids = {str(item.get("class_id", "")) for item in taxonomy.get("phrase_classes", [])}
    missing_classes = sorted(REQUIRED_CLASSES - class_ids)

    unit_test = run_command([sys.executable, "-m", "unittest", "tests.test_validate_claim_language"])

    public_overclaim = scan_report(
        linter,
        "README.md",
        "The project has GR derived from the substrate.\n",
    )
    underclaim = scan_report(
        linter,
        "research_control/current_frontier.md",
        UNDERCLAIM_FIXTURE.read_text(encoding="utf-8"),
    )
    calibrated_valid = scan_report(
        linter,
        "research_control/current_frontier.md",
        VALID_FIXTURE.read_text(encoding="utf-8"),
    )

    underclaim_class_ids = {finding["class_id"] for finding in underclaim["findings"]}
    errors: list[str] = []
    if missing_classes:
        errors.append(f"missing required advisory classes: {', '.join(missing_classes)}")
    if unit_test["returncode"] != 0:
        errors.append("focused unit tests failed")
    if public_overclaim["status"] != "FAIL" or public_overclaim["overclaim_hard_fail_count"] < 1:
        errors.append("public overclaim did not remain a hard failure")
    if underclaim["status"] != "PASS" or underclaim["hard_fail_count"] != 0:
        errors.append("underclaim fixture produced a hard failure")
    if underclaim["underclaim_calibration_warning_count"] < 4:
        errors.append("underclaim fixture did not produce all advisory warning classes")
    if REQUIRED_CLASSES - underclaim_class_ids:
        errors.append(
            "underclaim fixture missing warning classes: "
            + ", ".join(sorted(REQUIRED_CLASSES - underclaim_class_ids))
        )
    if calibrated_valid["status"] != "PASS" or calibrated_valid["finding_count"] != 0:
        errors.append("calibrated valid fixture did not pass cleanly")

    return {
        "schema_id": "p3_t03_underclaim_linter_validation_report_v1",
        "task_id": "RT-20260705-056",
        "job_id": "AJ-RT-20260705-056-001",
        "plan_task_id": "P3-T03",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "required_underclaim_classes": sorted(REQUIRED_CLASSES),
        "missing_underclaim_classes": missing_classes,
        "unit_test": unit_test,
        "public_overclaim_report": public_overclaim,
        "underclaim_fixture_report": underclaim,
        "calibrated_valid_fixture_report": calibrated_valid,
        "overclaim_hard_gates_preserved": public_overclaim["overclaim_hard_fail_count"] >= 1,
        "underclaim_warnings_are_advisory_only": (
            underclaim["status"] == "PASS" and underclaim["hard_fail_count"] == 0
        ),
        "report_distinguishes_overclaim_and_underclaim": (
            "overclaim_hard_fail_count" in underclaim
            and "underclaim_calibration_warning_count" in underclaim
            and "finding_kind_counts" in underclaim
        ),
        "no_physics_delta": True,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true", help="Write the JSON report artifact.")
    parser.add_argument("--report", default=REPORT_PATH.as_posix(), help="Report output path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report()
    if args.write_report:
        path = Path(args.report)
        if not path.is_absolute():
            path = REPO_ROOT / path
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
