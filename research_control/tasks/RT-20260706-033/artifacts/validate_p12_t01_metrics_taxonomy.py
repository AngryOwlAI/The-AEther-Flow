#!/usr/bin/env python3
"""Validate the v17 P12-T01 AI research-agent metrics taxonomy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TAXONOMY_PATH = ROOT / "research_control/design/ai_research_agent_metrics_taxonomy_v1.md"
REPORT_PATH = ROOT / "research_control/tasks/RT-20260706-033/artifacts/p12_t01_metrics_taxonomy_report.json"
RECEIPT_PATH = ROOT / "research_control/tasks/RT-20260706-033/artifacts/p12_t01_metrics_taxonomy_receipt.md"

REQUIRED_METRICS = [
    "overclaim_catch_rate",
    "underclaim_warning_rate",
    "obstruction_precision",
    "route_orbit_rate",
    "candidate_to_audit_conversion",
    "audit_to_stress_survival",
    "stress_survival_rate",
    "human_gate_load",
    "proof_to_process_ratio",
]

REQUIRED_PHRASES = [
    "P12-T02 is responsible",
    "physics_claim_authority_created: false",
    "Physics promotion authorized: false",
    "Distance-to-GR ledger changed: false",
    "Source-law adoption authorized: false",
    "Matter-coupling derivation authorized: false",
    "Einstein-equation derivation authorized: false",
    "Gate Chair verdict created: false",
    "Completed derivation authorized: false",
]

REQUIRED_COLUMNS = [
    "Metric ID",
    "Definition",
    "Numerator",
    "Denominator",
    "Primary evidence sources",
    "Interpretation guardrail",
]


def build_report() -> dict:
    checks: list[dict] = []
    if not TAXONOMY_PATH.exists():
        return {
            "status": "FAIL",
            "taxonomy_path": str(TAXONOMY_PATH.relative_to(ROOT)),
            "checks": [
                {
                    "check_id": "taxonomy_exists",
                    "status": "FAIL",
                    "detail": "Taxonomy file is missing.",
                }
            ],
        }

    text = TAXONOMY_PATH.read_text(encoding="utf-8")
    checks.append(
        {
            "check_id": "authority_marker",
            "status": "PASS" if text.startswith("<!-- authority: control -->") else "FAIL",
            "detail": "Taxonomy must be an explicit project-control artifact.",
        }
    )

    for metric_id in REQUIRED_METRICS:
        checks.append(
            {
                "check_id": f"metric_present:{metric_id}",
                "status": "PASS" if f"`{metric_id}`" in text else "FAIL",
                "detail": "Required v17 P12-T01 metric identifier must be present.",
            }
        )

    for column in REQUIRED_COLUMNS:
        checks.append(
            {
                "check_id": f"definition_table_column:{column}",
                "status": "PASS" if column in text else "FAIL",
                "detail": "Metric definition table must include numerator, denominator, evidence, and guardrail fields.",
            }
        )

    for phrase in REQUIRED_PHRASES:
        checks.append(
            {
                "check_id": f"boundary_phrase:{phrase}",
                "status": "PASS" if phrase in text else "FAIL",
                "detail": "Taxonomy must preserve P12-T02 deferral and no-physics-delta boundaries.",
            }
        )

    status = "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL"
    return {
        "status": status,
        "taxonomy_path": str(TAXONOMY_PATH.relative_to(ROOT)),
        "required_metric_count": len(REQUIRED_METRICS),
        "checks": checks,
        "physics_claim_authority_created": False,
        "physics_promotion_authorized": False,
        "gate_chair_verdict_created": False,
        "p12_t02_implementation_deferred": True,
    }


def write_receipt(report: dict) -> None:
    failed = [check for check in report["checks"] if check["status"] != "PASS"]
    lines = [
        "# P12-T01 Metrics Taxonomy Validation Receipt",
        "",
        f"Status: `{report['status']}`",
        "",
        f"Taxonomy: `{report['taxonomy_path']}`",
        "",
        "## Scope",
        "",
        "This receipt validates the v17 P12-T01 taxonomy surface only. It does not implement P12-T02 reporting and does not change physics claim status.",
        "",
        "## Required Metrics",
        "",
    ]
    lines.extend(f"- `{metric_id}`" for metric_id in REQUIRED_METRICS)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Physics claim authority created: false.",
            "- Physics promotion authorized: false.",
            "- Gate Chair verdict created: false.",
            "- P12-T02 implementation deferred: true.",
            "",
            "## Failed Checks",
            "",
        ]
    )
    if failed:
        lines.extend(f"- `{check['check_id']}`: {check['detail']}" for check in failed)
    else:
        lines.append("- None.")
    lines.append("")
    RECEIPT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_receipt(report)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
