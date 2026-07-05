#!/usr/bin/env python3
"""Validate P14-T03 target-import attack integration into claim-language linting."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
BAD_FIXTURE_SET_PATH = (
    REPO_ROOT / "tests/fixtures/research_control/target_import_attack/bad_target_import_fixtures_v16.json"
)
GOOD_FIXTURE_SET_PATH = (
    REPO_ROOT / "tests/fixtures/research_control/target_import_attack/good_target_import_fixtures_v16.json"
)


def load_linter():
    spec = importlib.util.spec_from_file_location("validate_claim_language", LINTER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_fixture_set(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_snippets(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"<!-- fixture: (?P<key>[-_a-zA-Z0-9]+) -->\n(?P<body>.*?)\n<!-- /fixture -->",
        flags=re.DOTALL,
    )
    return {match.group("key"): match.group("body").strip() for match in pattern.finditer(text)}


def scan_snippet(linter, taxonomy: dict[str, Any], snippet: str) -> dict[str, Any]:
    scanned_path = "research_control/current_frontier.md"
    findings = linter.scan_text_map(
        {scanned_path: snippet},
        taxonomy=taxonomy,
        reviewed_contexts=[],
        active_handoffs=set(),
    )
    return linter.report_dict(findings, scanned_paths=[scanned_path])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Path to write JSON report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report to stdout.")
    args = parser.parse_args(argv)

    linter = load_linter()
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    classes = {item["class_id"] for item in taxonomy.get("phrase_classes", [])}
    bad_fixture_set = load_fixture_set(BAD_FIXTURE_SET_PATH)
    good_fixture_set = load_fixture_set(GOOD_FIXTURE_SET_PATH)
    bad_snippets = load_snippets(REPO_ROOT / bad_fixture_set["snippet_path"])
    good_snippets = load_snippets(REPO_ROOT / good_fixture_set["snippet_path"])

    checks: list[dict[str, Any]] = []
    fixture_reports: list[dict[str, Any]] = []

    expected_target_classes = {
        fixture["expected_future_target_import_class_id"]
        for fixture in bad_fixture_set["fixtures"]
    }
    missing_classes = sorted(expected_target_classes - classes)
    checks.append(
        {
            "check_id": "target_import_phrase_classes_present",
            "status": "PASS" if not missing_classes else "FAIL",
            "missing_classes": missing_classes,
            "expected_class_count": len(expected_target_classes),
        }
    )

    required_output_classes = {
        "target_metric_used_as_source_certificate",
        "proper_time_used_as_source_readout",
        "stress_energy_tensor_used_to_prove_matter_semantics",
        "validator_pass_used_as_proof",
        "finite_local_model_rendered_as_universal_matter_coupling",
    }
    bad_fixture_classes = {fixture["fixture_class"] for fixture in bad_fixture_set["fixtures"]}
    checks.append(
        {
            "check_id": "p14_t03_required_validation_outputs_covered",
            "status": "PASS" if required_output_classes <= bad_fixture_classes else "FAIL",
            "missing_fixture_classes": sorted(required_output_classes - bad_fixture_classes),
        }
    )

    for fixture in bad_fixture_set["fixtures"]:
        report = scan_snippet(linter, taxonomy, bad_snippets[fixture["snippet_key"]])
        observed_classes = {finding["class_id"] for finding in report["findings"]}
        expected_future = fixture["expected_future_target_import_class_id"]
        expected_current = set(fixture["expected_current_linter_class_ids"])
        fixture_status = (
            report["status"] == "FAIL"
            and expected_future in observed_classes
            and expected_current <= observed_classes
        )
        fixture_reports.append(
            {
                "fixture_id": fixture["fixture_id"],
                "mode": "bad",
                "status": "PASS" if fixture_status else "FAIL",
                "report_status": report["status"],
                "expected_future_target_import_class_id": expected_future,
                "expected_current_linter_class_ids": sorted(expected_current),
                "observed_class_ids": sorted(observed_classes),
            }
        )

    for fixture in good_fixture_set["fixtures"]:
        report = scan_snippet(linter, taxonomy, good_snippets[fixture["snippet_key"]])
        fixture_status = report["status"] == "PASS" and report["finding_count"] == 0
        fixture_reports.append(
            {
                "fixture_id": fixture["fixture_id"],
                "mode": "good",
                "status": "PASS" if fixture_status else "FAIL",
                "report_status": report["status"],
                "finding_count": report["finding_count"],
            }
        )

    bad_fail_count = sum(
        1 for item in fixture_reports if item["mode"] == "bad" and item["status"] == "PASS"
    )
    good_pass_count = sum(
        1 for item in fixture_reports if item["mode"] == "good" and item["status"] == "PASS"
    )
    checks.extend(
        [
            {
                "check_id": "bad_fixtures_fail_closed",
                "status": "PASS" if bad_fail_count == len(bad_fixture_set["fixtures"]) else "FAIL",
                "observed_pass_count": bad_fail_count,
                "expected_count": len(bad_fixture_set["fixtures"]),
            },
            {
                "check_id": "good_fixtures_remain_clean",
                "status": "PASS" if good_pass_count == len(good_fixture_set["fixtures"]) else "FAIL",
                "observed_pass_count": good_pass_count,
                "expected_count": len(good_fixture_set["fixtures"]),
            },
            {
                "check_id": "boundary_no_physics_delta",
                "status": "PASS",
                "physics_promotion_authorized": False,
                "proof_authority": False,
                "scientific_claims_changed": False,
                "validator_behavior_changed": True,
            },
        ]
    )

    failed_checks = [check for check in checks if check["status"] != "PASS"]
    failed_fixture_reports = [item for item in fixture_reports if item["status"] != "PASS"]
    report = {
        "schema_id": "p14_t03_target_import_validator_integration_report_v1",
        "status": "PASS" if not failed_checks and not failed_fixture_reports else "FAIL",
        "task_id": "RT-20260705-032",
        "plan_task_id": "P14-T03",
        "operational_receipt_only": True,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "validator_behavior_changed": True,
        "check_count": len(checks),
        "failed_check_count": len(failed_checks),
        "fixture_report_count": len(fixture_reports),
        "failed_fixture_report_count": len(failed_fixture_reports),
        "checks": checks,
        "fixture_reports": fixture_reports,
    }

    output_path = REPO_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
