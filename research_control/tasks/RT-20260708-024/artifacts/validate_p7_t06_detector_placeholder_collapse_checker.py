#!/usr/bin/env python3
"""Validate the v18 P7-T06 detector-placeholder collapse checker packet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260708-024"
ARTIFACT_DIR = TASK_DIR / "artifacts"
SCRIPT_PATH = (
    ROOT
    / "scripts"
    / "research_control"
    / "support_formalization"
    / "detector_placeholder_collapse_checker.py"
)
TEST_PATH = ROOT / "tests" / "test_detector_placeholder_collapse_checker.py"
SPEC_PATH = ARTIFACT_DIR / "detector_placeholder_collapse_checker_spec_v1.md"
RECEIPT_PATH = ARTIFACT_DIR / "detector_placeholder_collapse_checker_receipt.md"
REPORT_PATH = ARTIFACT_DIR / "detector_placeholder_collapse_checker_report.json"
VALIDATOR_REPORT_PATH = ARTIFACT_DIR / "p7_t06_detector_placeholder_collapse_checker_report.json"

REQUIRED_STATUS_CODES = {
    "explicit_placeholder_block_safe": {"pass_placeholder_block_preserved"},
    "draft_control_source_readout_candidate_safe": {
        "pass_draft_control_candidate_preserved"
    },
    "placeholder_as_adopted_detector_semantics": {
        "fail_placeholder_as_detector_semantics_collapse"
    },
    "source_readout_candidate_as_detector_semantics": {
        "fail_candidate_as_detector_semantics_collapse",
        "fail_matter_coupling_overread",
    },
    "unprotected_adopted_detector_semantics_state": {
        "fail_unprotected_adopted_detector_semantics"
    },
}


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "detector_placeholder_collapse_checker", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def add_check(checks: list[dict[str, Any]], check_id: str, condition: bool, detail: str) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        }
    )


def run_validation() -> dict[str, Any]:
    checker = load_checker()
    checks: list[dict[str, Any]] = []

    required_paths = [
        SCRIPT_PATH,
        TEST_PATH,
        SPEC_PATH,
        RECEIPT_PATH,
        REPORT_PATH,
        TASK_DIR / "00_TASK.yaml",
        TASK_DIR / "DDR-20260708-024.md",
        TASK_DIR / "jobs" / "AJ-RT-20260708-024-001.yaml",
        TASK_DIR / "roles" / "formalization-engineer@0.1.0--RT-20260708-024.yaml",
        ARTIFACT_DIR / "child_phys_math_detector_placeholder_collapse_checker.yaml",
        ARTIFACT_DIR / "child_phys_phil_detector_placeholder_collapse_checker.yaml",
        ARTIFACT_DIR / "parent_conflict_review_detector_placeholder_collapse_checker.yaml",
        ARTIFACT_DIR / "parent_fusion_notes_detector_placeholder_collapse_checker.md",
    ]
    for path in required_paths:
        add_check(
            checks,
            f"exists:{path.relative_to(ROOT)}",
            path.exists(),
            f"{path.relative_to(ROOT)} exists",
        )

    live_report = checker.generate_report()
    stored_report = json.loads(REPORT_PATH.read_text(encoding="utf-8")) if REPORT_PATH.exists() else {}
    add_check(
        checks,
        "live_report_passes",
        live_report.get("status") == "PASS" and live_report.get("failed_case_count") == 0,
        "live checker suite passes expected pass/fail behavior",
    )
    add_check(
        checks,
        "stored_report_matches_live_core",
        stored_report.get("status") == live_report.get("status")
        and stored_report.get("case_count") == live_report.get("case_count")
        and stored_report.get("failed_case_count") == live_report.get("failed_case_count"),
        "stored JSON report matches live status and case counts",
    )
    add_check(
        checks,
        "support_only_boundary",
        live_report.get("support_only") is True
        and live_report.get("proof_authority") is False
        and live_report.get("physics_promotion_authorized") is False
        and live_report.get("validator_behavior_changed") is False,
        "checker report preserves support-only non-promotion flags",
    )
    state_counts = live_report.get("semantic_state_counts", {})
    add_check(
        checks,
        "required_states_distinguished",
        state_counts.get("explicit_placeholder_block", 0) >= 1
        and state_counts.get("draft_control_source_readout_candidate", 0) >= 1
        and state_counts.get("adopted_detector_semantics", 0) >= 1,
        "report distinguishes placeholder block, draft/control candidate, and adopted-detector-semantics states",
    )
    by_id = {
        result["case_id"]: result
        for result in live_report.get("case_results", [])
        if isinstance(result, dict)
    }
    for case_id, expected_codes in REQUIRED_STATUS_CODES.items():
        observed = set(by_id.get(case_id, {}).get("observed_status_codes", []))
        add_check(
            checks,
            f"expected_codes:{case_id}",
            expected_codes.issubset(observed),
            f"{case_id} includes expected status codes {sorted(expected_codes)}",
        )

    unit = subprocess.run(
        [sys.executable, "-m", "unittest", "tests/test_detector_placeholder_collapse_checker.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    add_check(
        checks,
        "focused_unittest_passes",
        unit.returncode == 0 and "Ran 8 tests" in unit.stderr,
        "focused detector-placeholder collapse checker tests pass",
    )

    spec_text = SPEC_PATH.read_text(encoding="utf-8") if SPEC_PATH.exists() else ""
    add_check(
        checks,
        "spec_routes_to_p7_t07",
        "P7-T07" in spec_text and "support_formalization_traceability_integration" in spec_text,
        "spec records P7-T07 as the next route",
    )
    add_check(
        checks,
        "receipt_forbidden_conclusions",
        "does not adopt `Det_src`" in RECEIPT_PATH.read_text(encoding="utf-8")
        and "does not adopt `Readout_src`" in RECEIPT_PATH.read_text(encoding="utf-8"),
        "receipt preserves Det_src and Readout_src non-adoption",
    )

    failed = [check for check in checks if check["status"] != "PASS"]
    return {
        "validator_id": "p7_t06_detector_placeholder_collapse_checker_task_local_validator",
        "status": "PASS" if not failed else "FAIL",
        "failed_check_count": len(failed),
        "checks": checks,
        "live_checker_status": live_report.get("status"),
        "case_count": live_report.get("case_count"),
        "semantic_state_counts": live_report.get("semantic_state_counts"),
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "detector_semantics_adopted": False,
        "matter_coupling_derived": False,
        "next_route": "P7-T07 support_formalization_traceability_integration",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args(argv)

    report = run_validation()
    if args.write_report:
        VALIDATOR_REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
