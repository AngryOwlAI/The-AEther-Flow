#!/usr/bin/env python3
"""Validate the P12-T03 dual-budget policy and deterministic fixture matrix."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control.dual_budget_policy import (  # noqa: E402
    CATEGORIES,
    dual_budget_policy,
    evaluate_dual_budget_allocation,
)

ARTIFACT_DIR = Path(__file__).resolve().parent
POLICY_PATH = ARTIFACT_DIR / "dual_budget_policy_v1.md"
DASHBOARD_SCHEMA_PATH = ARTIFACT_DIR / "budget_dashboard_schema_v1.md"
FIXTURE_PATH = ARTIFACT_DIR / "fixtures" / "dual_budget_cases.json"
REPORT_PATH = ARTIFACT_DIR / "dual_budget_validation_report.json"
RECEIPT_PATH = ARTIFACT_DIR / "dual_budget_compact_receipt.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/design/physics_payload_ratio_policy_v1.md": "0bf6b607a8f93b05e6e67c5a6676c0f889cb28f9a6c81db9c6c508e5f486d213",
    "research_control/design/ai_research_agent_metrics_taxonomy_v1.md": "bb373ae346c855695d0002605410b2113e6aa9a703bce90604c549a66222e439",
    "research_control/design/physics_payload_admission_policy_v1.md": "a390d0e2cde7160de25c239f7750b1a752edda61bdfdf1b6866079549e58fd0f",
    "research_control/tasks/RT-20260721-004/jobs/completions/AJC-AJ-RT-20260721-004-001.yaml": "535b8ed27d9551ec9009e1254dc7e15c65d35ca9796b607962180be9f5d284f4",
    "research_control/tasks/RT-20260722-012/jobs/completions/AJC-AJ-RT-20260722-012-001.yaml": "eee6b42ae304e15620c6df4e9216127f86730b8d2c693b21ca05bea97c7931b4",
}


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def rendered(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _fixture_evidence_verifier(path_text: str, expected_sha256: str) -> str:
    if not path_text.startswith("fixtures/"):
        return "fixture evidence path must remain under fixtures/"
    if not SHA256_RE.fullmatch(expected_sha256):
        return "fixture evidence hash must be lowercase SHA-256"
    return ""


def _source_errors() -> list[str]:
    errors: list[str] = []
    for path_text, expected_sha in SOURCE_HASHES.items():
        path = REPO_ROOT / path_text
        if not path.is_file():
            errors.append(f"missing source {path_text}")
            continue
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed != expected_sha:
            errors.append(f"source hash drift {path_text}")
    return errors


def build_report() -> dict[str, object]:
    fixture_bytes = FIXTURE_PATH.read_bytes()
    fixture = json.loads(fixture_bytes)
    source_errors = _source_errors()
    results: list[dict[str, object]] = []
    for case in fixture["cases"]:
        job = _merge(fixture["base_job"], case.get("job_patch", {}))
        observed = evaluate_dual_budget_allocation(
            job,
            created_at=fixture["created_at"],
            evidence_verifier=_fixture_evidence_verifier,
        )
        results.append(
            {
                "case_id": case["case_id"],
                "expected_status": case["expected_status"],
                "observed_status": observed["status"],
                "passed": observed["status"] == case["expected_status"],
                "error_count": len(observed["errors"]),
                "theorem_truth_evaluated": observed["theorem_truth_evaluated"],
            }
        )
    passed = sum(1 for item in results if item["passed"])
    observed_categories = sorted(
        {
            _merge(fixture["base_job"], case.get("job_patch", {}))["dual_budget_allocation"]["category"]
            for case in fixture["cases"]
            if case["expected_status"] == "admitted"
        }
    )
    report: dict[str, object] = {
        "schema_id": "dual_budget_validation_report_v1",
        "task_id": "RT-20260722-014",
        "plan_task_id": "P12-T03",
        "policy": dual_budget_policy(),
        "policy_path": str(POLICY_PATH.relative_to(REPO_ROOT)),
        "policy_sha256": hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest(),
        "dashboard_schema_path": str(DASHBOARD_SCHEMA_PATH.relative_to(REPO_ROOT)),
        "dashboard_schema_sha256": hashlib.sha256(
            DASHBOARD_SCHEMA_PATH.read_bytes()
        ).hexdigest(),
        "fixture_path": str(FIXTURE_PATH.relative_to(REPO_ROOT)),
        "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "source_hashes": SOURCE_HASHES,
        "source_error_count": len(source_errors),
        "source_errors": source_errors,
        "category_coverage": observed_categories,
        "category_coverage_complete": set(observed_categories) == set(CATEGORIES),
        "case_count": len(results),
        "passed_case_count": passed,
        "failed_case_count": len(results) - passed,
        "results": results,
        "single_primary_credit_enforced": True,
        "mixed_output_disjointness_enforced": True,
        "mixed_acceptance_disjointness_enforced": True,
        "blocked_physics_exception_evidence_enforced": True,
        "missing_compute_zero_coercion_blocked": True,
        "p12_t04_route_guard_implemented": False,
        "system_success_counts_as_physics": False,
        "system_success_counts_as_distance_to_gr": False,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }
    report["status"] = (
        "PASS"
        if not source_errors
        and report["category_coverage_complete"]
        and passed == len(results)
        else "FAIL"
    )
    return report


def receipt_for(report: dict[str, object]) -> dict[str, object]:
    return {
        "schema_id": "dual_budget_compact_receipt_v1",
        "task_id": report["task_id"],
        "plan_task_id": report["plan_task_id"],
        "status": report["status"],
        "source_hashes": report["source_hashes"],
        "policy_sha256": report["policy_sha256"],
        "dashboard_schema_sha256": report["dashboard_schema_sha256"],
        "fixture_sha256": report["fixture_sha256"],
        "report_sha256": hashlib.sha256(
            canonical_json(report).encode("utf-8")
        ).hexdigest(),
        "validator_ids": [
            "dual_budget_four_category_v1",
            "dual_budget_single_primary_credit_v1",
            "dual_budget_mixed_disjointness_v1",
            "dual_budget_blocked_physics_evidence_v1",
            "dual_budget_missing_compute_guard_v1",
            "dual_budget_system_science_authority_guard_v1",
        ],
        "category_coverage": report["category_coverage"],
        "case_count": report["case_count"],
        "passed_case_count": report["passed_case_count"],
        "failed_case_count": report["failed_case_count"],
        "claim_boundary_summary": (
            "Physics and project-system planning reporting and acceptance use separate "
            "lanes with exactly one primary task credit; mixed outputs and criteria are "
            "disjoint; system success never creates physics or Distance-to-GR credit."
        ),
        "p12_t04_route_guard_implemented": False,
        "system_success_counts_as_physics": False,
        "system_success_counts_as_distance_to_gr": False,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    receipt = receipt_for(report)
    if args.write:
        REPORT_PATH.write_text(rendered(report), encoding="utf-8")
        RECEIPT_PATH.write_text(rendered(receipt), encoding="utf-8")
    else:
        expected = {REPORT_PATH: rendered(report), RECEIPT_PATH: rendered(receipt)}
        drift = [
            str(path.relative_to(REPO_ROOT))
            for path, value in expected.items()
            if not path.exists() or path.read_text(encoding="utf-8") != value
        ]
        if drift:
            report = {**report, "status": "FAIL", "drift_paths": drift}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
