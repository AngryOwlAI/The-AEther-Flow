#!/usr/bin/env python3
"""Validate the P11-T02 review-independence taxonomy and write receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control import validate_red_team_review_artifact as validator


ARTIFACT_DIR = Path(__file__).resolve().parent
FIXTURE_DIR = (
    REPO_ROOT / "tests" / "fixtures" / "research_control" / "red_team_review"
)
TAXONOMY_PATH = ARTIFACT_DIR / "review_independence_taxonomy.md"
METADATA_SCHEMA_PATH = ARTIFACT_DIR / "review_metadata_schema.md"
CLAIM_RULES_PATH = ARTIFACT_DIR / "review_claim_language_rules.md"
VALIDATION_PATH = ARTIFACT_DIR / "review_independence_validation.json"
RECEIPT_PATH = ARTIFACT_DIR / "review_independence_compact_receipt.json"
EXECUTION_ROLE_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260722-005"
    / "roles"
    / "project-control-maintainer@0.2.0--RT-20260722-005.yaml"
)
SHARED_SCHEMA_PATH = (
    REPO_ROOT / ".agents" / "schemas" / "EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md"
)
SHARED_TEMPLATE_PATH = (
    REPO_ROOT / "research_control" / "templates" / "RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml"
)
CENTRAL_VALIDATOR_PATH = (
    REPO_ROOT / "scripts" / "research_control" / "validate_red_team_review_artifact.py"
)
FOCUSED_TEST_PATH = REPO_ROOT / "tests" / "test_red_team_review_artifact_validator.py"
HISTORICAL_REVIEW_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260720-021"
    / "artifacts"
    / "eqsrc_selector_theorem_external_red_team_review_v1.yaml"
)

CLASSIFICATION_FIXTURES = {
    "same_context_role_review": FIXTURE_DIR / "valid_same_context_review.yaml",
    "blind_same_model_review": FIXTURE_DIR / "valid_review_context.yaml",
    "different_model_review": FIXTURE_DIR / "valid_different_model_review.yaml",
    "human_expert_review": FIXTURE_DIR / "valid_human_expert_review.yaml",
    "independent_replication": FIXTURE_DIR / "valid_independent_replication.yaml",
    "unknown": FIXTURE_DIR / "unknown_review_context.yaml",
}
INVALID_FIXTURES = {
    "external_wording_guard": (
        FIXTURE_DIR / "false_external_wording.yaml",
        "review_context.claims.external_review_completed",
    ),
    "replication_wording_guard": (
        FIXTURE_DIR / "false_independent_replication.yaml",
        "review_context.claims.independent_replication_completed",
    ),
}


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_taxonomy() -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )

    expected_classes = tuple(CLASSIFICATION_FIXTURES)
    expected_dimensions = (
        "model_family",
        "prompt_context",
        "data_access",
        "institution",
        "human_authorship",
        "code_base",
        "method",
    )
    check(
        "central_classification_token_exactness",
        validator.REVIEW_CONTEXT_CLASSIFICATIONS == expected_classes,
        "central validator exposes exactly the six P11-T02 classification tokens",
    )
    check(
        "central_dimension_exactness",
        validator.INDEPENDENCE_DIMENSIONS == expected_dimensions,
        "central validator exposes exactly seven independence dimensions",
    )

    taxonomy_text = TAXONOMY_PATH.read_text(encoding="utf-8")
    metadata_text = METADATA_SCHEMA_PATH.read_text(encoding="utf-8")
    claim_text = CLAIM_RULES_PATH.read_text(encoding="utf-8")
    role_text = EXECUTION_ROLE_PATH.read_text(encoding="utf-8")
    schema_text = SHARED_SCHEMA_PATH.read_text(encoding="utf-8")
    template_text = SHARED_TEMPLATE_PATH.read_text(encoding="utf-8")

    for name, text in {
        "taxonomy": taxonomy_text,
        "metadata_schema": metadata_text,
        "execution_role": role_text,
        "shared_schema": schema_text,
        "shared_template": template_text,
    }.items():
        check(
            f"{name}_classification_coverage",
            all(token in text for token in expected_classes),
            f"{name} contains all normalized classifications",
        )
        check(
            f"{name}_dimension_coverage",
            all(token in text for token in expected_dimensions),
            f"{name} contains all seven independence dimensions",
        )

    check(
        "unknown_fail_closed_documented",
        "Missing evidence is `unknown`" in taxonomy_text
        and "`unknown` requires at least one explicitly unknown dimension"
        in metadata_text,
        "missing evidence is explicitly classified as unknown",
    )
    check(
        "legacy_compatibility_documented",
        "legacy_unclassified" in taxonomy_text
        and "legacy_unclassified" in metadata_text
        and "legacy_unclassified" in schema_text,
        "historical artifacts remain readable without retroactive strengthening",
    )
    check(
        "claim_language_rules_complete",
        all(field in claim_text for field in validator.REVIEW_CLAIM_FIELDS)
        and "A blind packet is not independent review." in claim_text
        and "Human review is not independent replication" in claim_text,
        "claim-language rules separate review, external provenance, and replication",
    )

    observed_classes: dict[str, str] = {}
    for expected, path in CLASSIFICATION_FIXTURES.items():
        try:
            receipt = validator.validate_review_file(path)
            observed = receipt["review_context_classification"]
            passed = observed == expected and receipt["review_context_present"] is True
            detail = f"expected={expected} observed={observed}"
            observed_classes[repo_relative(path)] = observed
        except Exception as exc:  # fail-closed receipt, exercised by the script
            passed = False
            detail = str(exc)
        check(f"fixture_{expected}", passed, detail)

    legacy_paths = [FIXTURE_DIR / "valid_minimal.yaml", HISTORICAL_REVIEW_PATH]
    legacy_observations: dict[str, str] = {}
    legacy_passed = True
    legacy_detail_parts: list[str] = []
    for path in legacy_paths:
        try:
            receipt = validator.validate_review_file(path)
            observed = receipt["review_context_classification"]
            present = receipt["review_context_present"]
            passed = observed == "legacy_unclassified" and present is False
            legacy_passed = legacy_passed and passed
            legacy_observations[repo_relative(path)] = observed
            legacy_detail_parts.append(f"{repo_relative(path)}={observed}")
        except Exception as exc:  # fail-closed receipt, exercised by the script
            legacy_passed = False
            legacy_detail_parts.append(f"{repo_relative(path)}={exc}")
    check(
        "legacy_review_readability",
        legacy_passed,
        "; ".join(legacy_detail_parts),
    )

    rejected_fixtures: dict[str, list[str]] = {}
    for check_id, (path, expected_field) in INVALID_FIXTURES.items():
        issue_fields: list[str] = []
        try:
            validator.validate_review_file(path)
            passed = False
            detail = "invalid fixture was accepted"
        except validator.RedTeamReviewValidationError as exc:
            issue_fields = [issue.field for issue in exc.issues]
            passed = expected_field in issue_fields
            detail = f"expected_field={expected_field} issue_fields={issue_fields}"
        except Exception as exc:  # fail-closed receipt, exercised by the script
            passed = False
            detail = str(exc)
        rejected_fixtures[repo_relative(path)] = issue_fields
        check(check_id, passed, detail)

    failed = [item for item in checks if item["status"] == "FAIL"]
    source_paths = [
        TAXONOMY_PATH,
        METADATA_SCHEMA_PATH,
        CLAIM_RULES_PATH,
        EXECUTION_ROLE_PATH,
        SHARED_SCHEMA_PATH,
        SHARED_TEMPLATE_PATH,
        CENTRAL_VALIDATOR_PATH,
        FOCUSED_TEST_PATH,
        Path(__file__),
        *CLASSIFICATION_FIXTURES.values(),
        *(item[0] for item in INVALID_FIXTURES.values()),
    ]
    return {
        "schema_id": "v21_review_independence_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "plan_task_id": "P11-T02",
        "recommendation_ids": ["V21-R37", "V21-R38", "V21-R43", "V21-R68"],
        "classification_count": len(expected_classes),
        "independence_dimension_count": len(expected_dimensions),
        "passing_fixture_count": len(CLASSIFICATION_FIXTURES),
        "rejected_fixture_count": len(INVALID_FIXTURES),
        "legacy_artifact_count": len(legacy_paths),
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
        "observed_classifications": dict(sorted(observed_classes.items())),
        "legacy_observations": dict(sorted(legacy_observations.items())),
        "rejected_fixture_issue_fields": dict(sorted(rejected_fixtures.items())),
        "artifact_hashes": {
            repo_relative(path): sha256_file(path) for path in sorted(set(source_paths))
        },
        "review_executed": False,
        "reviewer_independence_proven": False,
        "external_review_completed_by_task": False,
        "independent_replication_completed_by_task": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def build_receipt(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "v21_review_independence_compact_receipt_v1",
        "status": report["status"],
        "plan_task_id": report["plan_task_id"],
        "recommendation_ids": report["recommendation_ids"],
        "classification_count": report["classification_count"],
        "independence_dimension_count": report["independence_dimension_count"],
        "passing_fixture_count": report["passing_fixture_count"],
        "rejected_fixture_count": report["rejected_fixture_count"],
        "legacy_artifact_count": report["legacy_artifact_count"],
        "check_count": report["check_count"],
        "failed_check_count": report["failed_check_count"],
        "validator_ids": [item["check_id"] for item in report["checks"]],
        "artifact_hashes": report["artifact_hashes"],
        "claim_boundary_summary": (
            "Classification and wording consistency only; no review execution, "
            "reviewer-independence proof, external endorsement, replication result, "
            "scientific proof, ontology, benchmark, publication, or completed-derivation authority."
        ),
        "review_executed": False,
        "reviewer_independence_proven": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        report = validate_taxonomy()
        receipt = build_receipt(report)
        if args.write:
            VALIDATION_PATH.write_bytes(canonical_bytes(report))
            RECEIPT_PATH.write_bytes(canonical_bytes(receipt))
        else:
            if not VALIDATION_PATH.is_file() or load_json(VALIDATION_PATH) != report:
                raise ValueError("validation report drift")
            if not RECEIPT_PATH.is_file() or load_json(RECEIPT_PATH) != receipt:
                raise ValueError("compact receipt drift")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"status": "FAIL", "error": str(exc)}
        print(json.dumps(result, sort_keys=True) if args.json else f"FAIL: {exc}")
        return 1

    result = {
        "status": report["status"],
        "classification_count": report["classification_count"],
        "independence_dimension_count": report["independence_dimension_count"],
        "check_count": report["check_count"],
        "failed_check_count": report["failed_check_count"],
        "passing_fixture_count": report["passing_fixture_count"],
        "rejected_fixture_count": report["rejected_fixture_count"],
        "legacy_artifact_count": report["legacy_artifact_count"],
    }
    print(json.dumps(result, sort_keys=True) if args.json else report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
