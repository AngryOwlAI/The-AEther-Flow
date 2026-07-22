#!/usr/bin/env python3
"""Validate the P12-T01 physics-payload admission fixture matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control.physics_payload_admission import (  # noqa: E402
    admission_policy,
    evaluate_agent_job_admission,
)

ARTIFACT_DIR = Path(__file__).resolve().parent
FIXTURE_PATH = ARTIFACT_DIR / "fixtures" / "physics_payload_admission_cases.json"
REPORT_PATH = ARTIFACT_DIR / "physics_payload_admission_report.json"
RECEIPT_PATH = ARTIFACT_DIR / "physics_payload_admission_compact_receipt.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_report() -> dict[str, object]:
    fixture_bytes = FIXTURE_PATH.read_bytes()
    fixture = json.loads(fixture_bytes)
    results = []
    for case in fixture["cases"]:
        result = evaluate_agent_job_admission(
            case["job"],
            case["task"],
            created_at=case["created_at"],
            role_id=case["role_id"],
        )
        expected = case["expected_status"]
        results.append(
            {
                "case_id": case["case_id"],
                "expected_status": expected,
                "observed_status": result["status"],
                "passed": result["status"] == expected,
                "expected_admission_path": result["expected_admission_path"],
                "payload_type": result["payload_type"],
                "error_count": len(result["errors"]),
                "theorem_truth_evaluated": result["theorem_truth_evaluated"],
            }
        )
    passed = sum(1 for item in results if item["passed"])
    report = {
        "schema_id": "physics_payload_admission_report_v1",
        "policy": admission_policy(),
        "fixture_path": str(FIXTURE_PATH.relative_to(REPO_ROOT)),
        "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "case_count": len(results),
        "passed_case_count": passed,
        "failed_case_count": len(results) - passed,
        "results": results,
        "scientific_claims_changed": False,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }
    report["status"] = "PASS" if passed == len(results) else "FAIL"
    return report


def receipt_for(report: dict[str, object]) -> dict[str, object]:
    return {
        "schema_id": "physics_payload_admission_compact_receipt_v1",
        "status": report["status"],
        "case_count": report["case_count"],
        "passed_case_count": report["passed_case_count"],
        "failed_case_count": report["failed_case_count"],
        "fixture_sha256": report["fixture_sha256"],
        "report_sha256": hashlib.sha256(canonical_json(report).encode("utf-8")).hexdigest(),
        "legacy_readability_preserved": True,
        "source_acquisition_preserved": True,
        "precise_obstruction_preserved": True,
        "selector_only_requires_new_unencoded_decision": True,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }


def rendered(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


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
        drift = [str(path.relative_to(REPO_ROOT)) for path, value in expected.items() if not path.exists() or path.read_text(encoding="utf-8") != value]
        if drift:
            report = {**report, "status": "FAIL", "drift_paths": drift}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
