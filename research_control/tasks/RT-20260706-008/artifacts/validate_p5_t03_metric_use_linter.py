#!/usr/bin/env python3
"""Validate the v17 P5-T03 metric-use linter packet."""

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
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260706-008/artifacts/p5_t03_metric_use_linter_report.json"
)

REQUIRED_CLASSES = {
    "g_eff_proper_time_normalization_overread",
    "g_eff_detector_calibration_overread",
    "g_eff_stress_energy_semantics_overread",
    "g_eff_overclaim",
}

REQUIRED_BAD_CASES = [
    (
        "g_eff supplies proper time.\n",
        "g_eff_proper_time_normalization_overread",
    ),
    (
        "g_eff calibrates detectors.\n",
        "g_eff_detector_calibration_overread",
    ),
    (
        "g_eff supplies stress-energy semantics.\n",
        "g_eff_stress_energy_semantics_overread",
    ),
    (
        "MetricData(E) adopted.\n",
        "g_eff_overclaim",
    ),
]

SCOPED_PASSING_TEXT = (
    "g_eff is used as scoped source-extension context only; it does not authorize "
    "a physical Lorentzian metric, proper-time normalization, detector calibration, "
    "stress-energy semantics, matter action, Einstein equations, benchmark "
    "promotion, or completed derivation.\n"
)


def load_linter() -> Any:
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


def scan_report(
    linter: Any,
    path: str,
    text: str,
    *,
    reviewed_contexts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    findings = linter.scan_text_map(
        {path: text},
        taxonomy=taxonomy,
        reviewed_contexts=reviewed_contexts or [],
        active_handoffs={"research_control/handoffs/handoff-0640.yaml"},
    )
    return linter.report_dict(findings, scanned_paths=[path])


def build_report() -> dict[str, Any]:
    linter = load_linter()
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    class_ids = {str(item.get("class_id", "")) for item in taxonomy.get("phrase_classes", [])}
    missing_classes = sorted(REQUIRED_CLASSES - class_ids)

    unit_test = run_command([sys.executable, "-m", "unittest", "tests.test_validate_claim_language"])

    bad_case_reports = []
    errors: list[str] = []
    for text, expected_class in REQUIRED_BAD_CASES:
        report = scan_report(linter, "research_control/current_frontier.md", text)
        observed = {finding["class_id"] for finding in report["findings"]}
        bad_case_reports.append(
            {
                "text": text.strip(),
                "expected_class": expected_class,
                "report": report,
            }
        )
        if report["status"] != "FAIL" or expected_class not in observed:
            errors.append(f"bad case did not fail as {expected_class}: {text.strip()}")

    scoped_context_report = scan_report(
        linter,
        "research_control/current_frontier.md",
        SCOPED_PASSING_TEXT,
    )
    if scoped_context_report["status"] != "PASS" or scoped_context_report["finding_count"] != 0:
        errors.append("scoped source-extension context did not pass cleanly")

    protected_context = [
        {
            "entry_id": "P5-T03-PROTECTED-AUTHORITY-SYNTHETIC-CONTEXT",
            "path": "research_control/current_frontier.md",
            "class_ids": ["g_eff_overclaim"],
            "surface_class_override": "current_control_surfaces",
            "severity_override": "warn_review",
            "reviewed_by_task_id": "RT-20260706-008",
            "reviewed_by_role": "gate-chair@0.1.0",
            "scope_rationale": "Synthetic protected-authority context used only to verify fail-unless-reviewed behavior.",
        }
    ]
    protected_metricdata_report = scan_report(
        linter,
        "research_control/current_frontier.md",
        "MetricData(E) adopted.\n",
        reviewed_contexts=protected_context,
    )
    if (
        protected_metricdata_report["status"] != "PASS"
        or protected_metricdata_report["hard_fail_count"] != 0
        or protected_metricdata_report["warning_count"] != 1
    ):
        errors.append("protected-authority synthetic context did not downgrade MetricData(E) adoption")

    if missing_classes:
        errors.append(f"missing required classes: {', '.join(missing_classes)}")
    if unit_test["returncode"] != 0:
        errors.append("focused claim-language unit tests failed")

    required_coverage = taxonomy.get("required_phrase_coverage", {}).get("plan_phrases", [])
    coverage_pairs = {
        (str(item.get("phrase", "")), str(item.get("class_id", ""))) for item in required_coverage
    }
    required_pairs = {
        ("g_eff supplies proper time", "g_eff_proper_time_normalization_overread"),
        ("g_eff calibrates detectors", "g_eff_detector_calibration_overread"),
        ("g_eff supplies stress-energy semantics", "g_eff_stress_energy_semantics_overread"),
    }
    missing_coverage_pairs = sorted(required_pairs - coverage_pairs)
    if missing_coverage_pairs:
        errors.append(f"missing required phrase coverage pairs: {missing_coverage_pairs}")

    return {
        "schema_id": "p5_t03_metric_use_linter_validation_report_v1",
        "task_id": "RT-20260706-008",
        "job_id": "AJ-RT-20260706-008-001",
        "plan_task_id": "P5-T03",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "required_classes": sorted(REQUIRED_CLASSES),
        "missing_classes": missing_classes,
        "unit_test": unit_test,
        "bad_case_reports": bad_case_reports,
        "scoped_context_report": scoped_context_report,
        "protected_metricdata_report": protected_metricdata_report,
        "metricdata_adoption_fails_without_reviewed_authority": (
            bad_case_reports[-1]["report"]["status"] == "FAIL"
        ),
        "scoped_source_extension_context_passes": (
            scoped_context_report["status"] == "PASS"
            and scoped_context_report["finding_count"] == 0
        ),
        "overclaim_hard_gates_preserved": all(
            item["report"]["hard_fail_count"] >= 1 for item in bad_case_reports
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
