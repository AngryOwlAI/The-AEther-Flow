#!/usr/bin/env python3
"""Validate the v18 P7-T02 typed EqSrc orbit checker packet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260708-020"
ARTIFACTS = TASK_DIR / "artifacts"
SCRIPT = ROOT / "scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py"
TEST_FILE = ROOT / "tests/test_typed_eqsrc_orbit_checker.py"
FIXTURE_DIR = ROOT / "tests/fixtures/research_control/typed_eqsrc_orbit"
COMPLETION = TASK_DIR / "jobs/completions/AJC-AJ-RT-20260708-020-001.yaml"
CHECKER_REPORT = ARTIFACTS / "typed_eqsrc_orbit_checker_report.json"
REPORT = ARTIFACTS / "p7_t02_typed_eqsrc_orbit_checker_report.json"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def load_checker():
    spec = importlib.util.spec_from_file_location("typed_eqsrc_orbit_checker", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_unittest() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", str(TEST_FILE.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    required_paths = [
        SCRIPT,
        TEST_FILE,
        FIXTURE_DIR / "valid_support_only.yaml",
        FIXTURE_DIR / "orbit_closure_failure.yaml",
        FIXTURE_DIR / "type_mismatch.yaml",
        FIXTURE_DIR / "target_import_overread.yaml",
        TASK_DIR / "00_TASK.yaml",
        TASK_DIR / "DDR-20260708-020.md",
        TASK_DIR / "roles/formalization-engineer@0.1.0--RT-20260708-020.yaml",
        TASK_DIR / "jobs/AJ-RT-20260708-020-001.yaml",
        COMPLETION,
        ARTIFACTS / "typed_eqsrc_orbit_checker_spec_v1.md",
        ARTIFACTS / "typed_eqsrc_orbit_checker_receipt.md",
        ARTIFACTS / "parent_fusion_notes_typed_eqsrc_orbit_checker.md",
        CHECKER_REPORT,
    ]

    errors: list[str] = []
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(ROOT)}")

    checker = load_checker() if SCRIPT.exists() else None
    status_by_fixture: dict[str, str] = {}
    if checker is not None:
        expected_statuses = {
            "valid_support_only.yaml": "pass_support_only",
            "orbit_closure_failure.yaml": "fail_orbit_closure",
            "type_mismatch.yaml": "fail_type_mismatch",
            "target_import_overread.yaml": "fail_target_import",
        }
        for name, expected in expected_statuses.items():
            report = checker.check_path(FIXTURE_DIR / name)
            status_by_fixture[name] = report.status
            if report.status != expected:
                errors.append(f"{name} status {report.status!r} != {expected!r}")
            if report.proof_authority is not False:
                errors.append(f"{name} proof_authority must be false")
            if report.physics_promotion_authorized is not False:
                errors.append(f"{name} physics_promotion_authorized must be false")

    if CHECKER_REPORT.exists():
        report = json.loads(CHECKER_REPORT.read_text(encoding="utf-8"))
        if report.get("status") != "pass_support_only":
            errors.append("typed_eqsrc_orbit_checker_report.json must pass support-only")
        if report.get("support_only") is not True:
            errors.append("checker report support_only must be true")
        if report.get("proof_authority") is not False:
            errors.append("checker report proof_authority must be false")
        if report.get("physics_promotion_authorized") is not False:
            errors.append("checker report physics_promotion_authorized must be false")

    if COMPLETION.exists():
        completion = load_yaml(COMPLETION)
        claim_boundary = completion.get("claim_boundary", {})
        for key in (
            "proof_authority",
            "physics_promotion_authorized",
            "source_law_adopted",
            "eqsrc_theorem_adopted",
            "target_metric_imported",
            "matter_coupling_derived",
            "einstein_equations_derived",
            "benchmark_promoted",
            "completed_derivation_claimed",
        ):
            if claim_boundary.get(key) is not False:
                errors.append(f"claim_boundary.{key} must be false")
        selected = completion.get("selected_next_route", {})
        if selected.get("plan_task_id") != "P7-T03":
            errors.append("selected_next_route.plan_task_id must be P7-T03")

    spec_text = (
        (ARTIFACTS / "typed_eqsrc_orbit_checker_spec_v1.md").read_text(encoding="utf-8")
        if (ARTIFACTS / "typed_eqsrc_orbit_checker_spec_v1.md").exists()
        else ""
    )
    for phrase in (
        "support_only: true",
        "proof_authority: false",
        "does not prove general `EqSrc`",
        "closure_countermodel_generator_support_only",
    ):
        if phrase not in spec_text:
            errors.append(f"spec missing phrase: {phrase}")

    unittest_ok, unittest_output = run_unittest() if TEST_FILE.exists() else (False, "missing test file")
    if not unittest_ok:
        errors.append("focused unittest command failed")

    validation_report = {
        "schema_id": "p7_t02_typed_eqsrc_orbit_checker_validation_report_v1",
        "task_id": "RT-20260708-020",
        "job_id": "AJ-RT-20260708-020-001",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checker_id": "typed_eqsrc_orbit_checker",
        "status_by_fixture": status_by_fixture,
        "focused_unittest_passed": unittest_ok,
        "focused_unittest_output": unittest_output,
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "selected_next_plan_task_id": "P7-T03",
    }

    if args.write_report:
        REPORT.write_text(json.dumps(validation_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(validation_report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
