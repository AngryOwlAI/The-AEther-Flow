#!/usr/bin/env python3
"""Validate v15 P6-T03 source-extension classification validator integration."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
VALIDATOR_PATH = REPO_ROOT / "scripts/research_control/validate_research_control.py"
TEST_PATH = REPO_ROOT / "tests/test_research_control.py"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

REQUIRED_VALIDATOR_TOKENS = [
    "SOURCE_EXTENSION_CLASSIFICATION_REQUIRED_AFTER",
    "SOURCE_EXTENSION_CLASSIFICATION_CHECKLIST_ID",
    "SOURCE_EXTENSION_CLASSIFICATION_VALUES",
    "SOURCE_EXTENSION_ONTOLOGY_RELATION_VALUES",
    "source_extension_classification_required",
    "validate_source_extension_classification_receipt",
    "source-extension completion missing source_extension_classification receipt",
    "requires claim_boundary",
    "requires blocked_overreads",
    "downstream_promotion_authorized must be false",
    "physics_promotion_authorized must be false",
]

REQUIRED_TEST_TOKENS = [
    "test_source_extension_completion_requires_classification_receipt",
    "test_source_extension_classification_receipt_requires_required_fields",
    "test_source_extension_classification_receipt_accepts_valid_record",
    "test_roadmap_selector_accepts_source_extension_category",
]


def load_validator() -> Any:
    spec = importlib.util.spec_from_file_location(
        "validate_research_control_for_p6_t03",
        VALIDATOR_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def make_check(check_id: str, passed: bool, detail: str) -> dict[str, object]:
    return {"id": check_id, "passed": passed, "detail": detail}


def synthetic_job_row() -> dict[str, str]:
    return {
        "role_id": "theoretical-continuation-selector",
        "created_at": "2026-07-03T06:45:01Z",
        "started_at": "2026-07-03T06:45:01Z",
        "completed_at": "2026-07-03T06:45:01Z",
    }


def synthetic_job_contract() -> dict[str, object]:
    return {
        "route_label": "source_extension_candidate",
        "plan_task_id": "source_extension_candidate_fixture",
    }


def receipt_record() -> dict[str, object]:
    return {
        "item_id": "SyntheticSourceExtension",
        "item_source_path": "research_control/tasks/RT-TEST/artifacts/synthetic.md",
        "classification": "conservative_definitional_extension",
        "claim_boundary_id": "CB-TEST-SOURCE-EXTENSION",
        "blocked_overreads": [
            "source-law adoption",
            "matter-coupling derivation",
        ],
        "relation_to_current_ontology": "conservative",
        "protected_authority_required": False,
        "downstream_promotion_authorized": False,
        "physics_promotion_authorized": False,
    }


def run_receipt_checks(validator: Any) -> tuple[bool, bool, bool, dict[str, list[str]]]:
    job_row = synthetic_job_row()
    job_contract = synthetic_job_contract()

    missing_report = validator.ValidationReport()
    validator.validate_source_extension_classification_receipt(
        missing_report,
        job_row,
        job_contract,
        {"completed_at": "2026-07-03T06:45:01Z"},
        "fixture-missing.yaml",
    )

    malformed_report = validator.ValidationReport()
    validator.validate_source_extension_classification_receipt(
        malformed_report,
        job_row,
        job_contract,
        {
            "completed_at": "2026-07-03T06:45:01Z",
            "source_extension_classification": {
                "checklist_id": "source_extension_classification_checklist_v1",
                "records": [{"item_id": "SyntheticSourceExtension"}],
            },
        },
        "fixture-malformed.yaml",
    )

    valid_report = validator.ValidationReport()
    validator.validate_source_extension_classification_receipt(
        valid_report,
        job_row,
        job_contract,
        {
            "completed_at": "2026-07-03T06:45:01Z",
            "source_extension_classification": {
                "checklist_id": "source_extension_classification_checklist_v1",
                "records": [receipt_record()],
            },
        },
        "fixture-valid.yaml",
    )

    missing_passed = any(
        "missing source_extension_classification receipt" in error
        for error in missing_report.errors
    )
    malformed_text = "\n".join(malformed_report.errors)
    malformed_passed = all(
        token in malformed_text
        for token in [
            ".classification is not allowed",
            "requires claim_boundary",
            "requires blocked_overreads",
            ".relation_to_current_ontology is not allowed",
            ".protected_authority_required is required",
            ".downstream_promotion_authorized is required",
        ]
    )
    valid_passed = valid_report.errors == []
    return (
        missing_passed,
        malformed_passed,
        valid_passed,
        {
            "missing_errors": missing_report.errors,
            "malformed_errors": malformed_report.errors,
            "valid_errors": valid_report.errors,
        },
    )


def build_report() -> dict[str, object]:
    validator_text = VALIDATOR_PATH.read_text(encoding="utf-8")
    test_text = TEST_PATH.read_text(encoding="utf-8")
    validator = load_validator()
    missing_passed, malformed_passed, valid_passed, receipt_details = run_receipt_checks(validator)

    checks = [
        make_check(
            "validator_contains_required_tokens",
            all(token in validator_text for token in REQUIRED_VALIDATOR_TOKENS),
            "Validator code contains the source-extension classification policy constants, dispatch, and field errors.",
        ),
        make_check(
            "unit_tests_contain_required_cases",
            all(token in test_text for token in REQUIRED_TEST_TOKENS),
            "Research-control tests contain missing, malformed, valid, and compatibility fixture coverage.",
        ),
        make_check(
            "synthetic_missing_receipt_fails",
            missing_passed,
            "Synthetic post-policy source-extension completion fails when the receipt is omitted.",
        ),
        make_check(
            "synthetic_malformed_receipt_fails_required_fields",
            malformed_passed,
            "Synthetic malformed receipt fails required classification, claim boundary, blocked overread, ontology relation, protected authority, and downstream status checks.",
        ),
        make_check(
            "synthetic_valid_receipt_passes",
            valid_passed,
            "Synthetic valid receipt passes the P6-T03 validator with no errors.",
        ),
        make_check(
            "compatibility_policy_is_time_bounded",
            "2026-07-03T06:45:00Z" in validator_text
            and "timestamp_at_or_after" in validator_text,
            "The new requirement is activation-bounded so existing valid pre-P6-T03 completions remain compatible.",
        ),
    ]
    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "task_id": "RT-20260703-008",
        "check_count": len(checks),
        "failed_check_count": sum(1 for check in checks if not check["passed"]),
        "checks": checks,
        "receipt_details": receipt_details,
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "matter_coupling_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Optional JSON report output path.")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args()

    report = build_report()
    if args.output:
        output_path = REPO_ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
