#!/usr/bin/env python3
"""Validate the v18 P11-T01 integration report shape and claim boundary."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = TASK_DIR / "artifacts" / "v18_integration_report.md"
REPORT_JSON_PATH = TASK_DIR / "artifacts" / "p11_t01_v18_integration_report_validation.json"

REQUIRED_SECTIONS = [
    "Implemented Tasks",
    "Deferred Tasks",
    "Recommendation Coverage Table",
    "EqSrc Typed-Object Status",
    "EqSrc Family Theorem/Countermodel Status",
    "Countermodel Obligation Status",
    "Source Detector/Readout Status",
    "Finite Toy Response V2 Status",
    "Support Formalization Status",
    "Payload-Ratio Policy Status",
    "Active-State Bifurcation Status",
    "Public Status-Card V2 Status",
    "External-Review Packet Status",
    "Distance-To-GR Effect",
    "Remaining Blocked Claims",
    "Candidate Ordinary Route Families",
    "Next Validation Route",
]

RECOMMENDATION_IDS = [f"V18-R{i:02d}" for i in range(1, 11)]

REQUIRED_LITERALS = [
    'implemented_plan_task_id: "P11-T01"',
    "phase_p11_completed: false",
    "v18_completed: false",
    "physics_promotion_authorized: false",
    "distance_to_gr_promotion_claimed: false",
    "ledger_row_updated: false",
    "external_outreach_performed: false",
    "proof_authority: false",
    "benchmark_authority: false",
    "gate_chair_verdict_issued: false",
    "completed_derivation_claimed: false",
    'next_validation_route: "P11-T02"',
    "Next validation route: P11-T02.",
]

FORBIDDEN_PATTERNS = [
    r"physics_promotion_authorized:\s*true",
    r"distance_to_gr_promotion_claimed:\s*true",
    r"ledger_row_updated:\s*true",
    r"external_outreach_performed:\s*true",
    r"proof_authority:\s*true",
    r"benchmark_authority:\s*true",
    r"gate_chair_verdict_issued:\s*true",
    r"completed_derivation_claimed:\s*true",
    r"\bRetainH adoption\b.*\bcomplete\b",
    r"\bGenH adoption\b.*\bcomplete\b",
    r"\bgeneral EqSrc discharge\b.*\bcomplete\b",
    r"\bEinstein-equation derivation\b.*\bcomplete\b",
    r"\bbenchmark promotion\b.*\bcomplete\b",
]


def _check_heading(text: str, heading: str) -> bool:
    return bool(re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE))


def validate() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    if not REPORT_PATH.exists():
        return {
            "status": "FAIL",
            "report_path": str(REPORT_PATH.relative_to(Path.cwd())),
            "checks": [
                {
                    "name": "report_exists",
                    "status": "FAIL",
                    "details": "v18_integration_report.md is missing",
                }
            ],
        }

    text = REPORT_PATH.read_text(encoding="utf-8")

    missing_sections = [section for section in REQUIRED_SECTIONS if not _check_heading(text, section)]
    checks.append(
        {
            "name": "required_sections",
            "status": "PASS" if not missing_sections else "FAIL",
            "missing": missing_sections,
        }
    )

    missing_recommendations = [rec_id for rec_id in RECOMMENDATION_IDS if rec_id not in text]
    checks.append(
        {
            "name": "recommendation_coverage_ids",
            "status": "PASS" if not missing_recommendations else "FAIL",
            "missing": missing_recommendations,
        }
    )

    missing_literals = [literal for literal in REQUIRED_LITERALS if literal not in text]
    checks.append(
        {
            "name": "required_boundary_literals",
            "status": "PASS" if not missing_literals else "FAIL",
            "missing": missing_literals,
        }
    )

    forbidden_hits = []
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            forbidden_hits.append(pattern)
    checks.append(
        {
            "name": "forbidden_promotion_patterns",
            "status": "PASS" if not forbidden_hits else "FAIL",
            "matches": forbidden_hits,
        }
    )

    candidate_route_count = sum(1 for route in [
        "EqSrc_family_closure_repair_or_stress",
        "RetainH_definition_candidate_packet",
        "GenH_definition_candidate_packet",
        "source_detector_readout_candidate_repair",
        "finite_toy_response_v2_repair_or_freeze",
        "support_formalization_expansion_next_checker",
        "external_review_human_gate_request",
        "scoped_obstruction_freeze_review",
    ] if route in text)
    checks.append(
        {
            "name": "candidate_route_families_visible",
            "status": "PASS" if candidate_route_count >= 8 else "FAIL",
            "candidate_route_count": candidate_route_count,
        }
    )

    all_pass = all(check["status"] == "PASS" for check in checks)
    return {
        "status": "PASS" if all_pass else "FAIL",
        "task_id": "RT-20260709-002",
        "plan_task_id": "P11-T01",
        "report_path": str(REPORT_PATH.relative_to(Path.cwd())),
        "checks": checks,
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "distance_to_gr_promotion_claimed": False,
            "ledger_row_updated": False,
            "external_outreach_performed": False,
            "proof_authority": False,
            "benchmark_authority": False,
            "gate_chair_verdict_issued": False,
            "completed_derivation_claimed": False,
        },
        "next_route": "P11-T02",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate()
    if args.write_report:
        REPORT_JSON_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
