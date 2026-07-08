#!/usr/bin/env python3
"""Validate v18 P7-T05 metric-use ledger TeX validator artifacts."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = ROOT / "scripts" / "research_control" / "validate_metric_use_tex_references.py"
TEST_PATH = ROOT / "tests" / "test_validate_metric_use_tex_references.py"
SPEC_PATH = (
    ROOT
    / "research_control"
    / "tasks"
    / "RT-20260708-023"
    / "artifacts"
    / "metric_use_tex_validator_spec_v1.md"
)
RECEIPT_PATH = (
    ROOT
    / "research_control"
    / "tasks"
    / "RT-20260708-023"
    / "artifacts"
    / "metric_use_tex_validator_receipt.md"
)
REPORT_PATH = (
    ROOT
    / "research_control"
    / "tasks"
    / "RT-20260708-023"
    / "artifacts"
    / "metric_use_tex_validator_report.json"
)
VALIDATOR_REPORT_PATH = (
    ROOT
    / "research_control"
    / "tasks"
    / "RT-20260708-023"
    / "artifacts"
    / "p7_t05_metric_use_tex_validator_report.json"
)

EXPECTED_CLASSES = [
    "g_eff",
    "metricdata_e",
    "proper_time",
    "detector_calibration",
    "stress_energy",
    "matter_action",
]


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_metric_use_tex_references", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_ledger(path: Path, header: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()


def add_check(checks: list[dict[str, Any]], check_id: str, condition: bool, detail: str) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        }
    )


def run_validation() -> dict[str, Any]:
    validator = load_validator()
    checks: list[dict[str, Any]] = []

    required_paths = [SCRIPT_PATH, TEST_PATH, SPEC_PATH, RECEIPT_PATH, REPORT_PATH]
    for path in required_paths:
        add_check(
            checks,
            f"exists:{path.relative_to(ROOT)}",
            path.exists(),
            f"{path.relative_to(ROOT)} exists",
        )

    live_report = validator.build_report(
        repo_root=ROOT,
        ledger_path=ROOT / validator.DEFAULT_LEDGER,
        failure_mode="hard-fail",
    )
    stored_report = json.loads(REPORT_PATH.read_text(encoding="utf-8")) if REPORT_PATH.exists() else {}

    add_check(
        checks,
        "live_report_passes",
        live_report.get("status") == "PASS" and live_report.get("finding_count") == 0,
        "live configured TeX artifacts have ledger coverage or declaration-only non-use",
    )
    add_check(
        checks,
        "stored_report_matches_live_core",
        stored_report.get("status") == live_report.get("status")
        and stored_report.get("finding_count") == live_report.get("finding_count")
        and stored_report.get("configured_path_count") == live_report.get("configured_path_count"),
        "stored JSON report matches live status, finding count, and configured scope count",
    )
    add_check(
        checks,
        "expected_high_risk_classes",
        live_report.get("high_risk_classes") == EXPECTED_CLASSES,
        "validator tracks the six required P7-T05 high-risk classes",
    )
    add_check(
        checks,
        "support_only_boundary",
        live_report.get("support_only") is True
        and live_report.get("proof_authority") is False
        and live_report.get("physics_promotion_authorized") is False
        and live_report.get("source_law_adopted") is False
        and live_report.get("ledger_changed") is False,
        "live report preserves support-only non-promotion flags",
    )
    add_check(
        checks,
        "hard_or_warning_policy_exposed",
        live_report.get("exit_policy") == {"PASS": 0, "WARN": 0, "FAIL": 1},
        "validator exposes warning and hard-fail integration policy",
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        tex_path = temp_root / "fixture.tex"
        tex_path.write_text(
            "g_eff MetricData(E) proper time detector calibration stress-energy matter action\n",
            encoding="utf-8",
        )
        ledger_path = temp_root / "registries" / "METRIC_USE_LEDGER.csv"
        write_ledger(ledger_path, validator.LEDGER_HEADER)

        hard = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--repo-root",
                str(temp_root),
                "--ledger",
                str(ledger_path),
                "--paths",
                str(tex_path),
                "--failure-mode",
                "hard-fail",
                "--json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        warn = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--repo-root",
                str(temp_root),
                "--ledger",
                str(ledger_path),
                "--paths",
                str(tex_path),
                "--failure-mode",
                "warn",
                "--json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    hard_report = json.loads(hard.stdout)
    warn_report = json.loads(warn.stdout)
    add_check(
        checks,
        "synthetic_unledgered_hard_fail",
        hard.returncode == 1
        and hard_report.get("status") == "FAIL"
        and {finding["class_id"] for finding in hard_report.get("findings", [])}
        == set(EXPECTED_CLASSES),
        "hard-fail mode catches all six unledgered classes",
    )
    add_check(
        checks,
        "synthetic_unledgered_warn_mode",
        warn.returncode == 0
        and warn_report.get("status") == "WARN"
        and {finding["class_id"] for finding in warn_report.get("findings", [])}
        == set(EXPECTED_CLASSES),
        "warning mode catches all six classes while exiting zero",
    )

    spec_text = SPEC_PATH.read_text(encoding="utf-8") if SPEC_PATH.exists() else ""
    add_check(
        checks,
        "spec_routes_to_p7_t06",
        "P7-T06" in spec_text and "detector_placeholder_collapse_checker_support_only" in spec_text,
        "spec records P7-T06 as the next route",
    )

    failed = [check for check in checks if check["status"] != "PASS"]
    return {
        "validator_id": "p7_t05_metric_use_tex_validator_task_local_validator",
        "status": "PASS" if not failed else "FAIL",
        "failed_check_count": len(failed),
        "checks": checks,
        "live_validator_status": live_report.get("status"),
        "live_finding_count": live_report.get("finding_count"),
        "configured_path_count": live_report.get("configured_path_count"),
        "high_risk_classes": live_report.get("high_risk_classes"),
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "source_law_adopted": False,
        "ledger_changed": False,
        "next_route": "P7-T06 detector_placeholder_collapse_checker_support_only",
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
