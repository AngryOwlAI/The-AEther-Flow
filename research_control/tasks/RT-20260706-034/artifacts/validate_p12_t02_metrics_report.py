#!/usr/bin/env python3
"""Validate the v17 P12-T02 AI methodology metrics report extension."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
JSON_PATH = ROOT / "output" / "physics_progress_metrics.json"
MARKDOWN_PATH = ROOT / "output" / "physics_progress_metrics.md"
REPORT_PATH = ROOT / "research_control" / "tasks" / "RT-20260706-034" / "artifacts" / "p12_t02_metrics_report_validation.json"

REQUIRED_METRICS = {
    "overclaim_catch_rate",
    "underclaim_warning_rate",
    "obstruction_precision",
    "route_orbit_rate",
    "candidate_to_audit_conversion",
    "audit_to_stress_survival",
    "stress_survival_rate",
    "human_gate_load",
    "proof_to_process_ratio",
}


def load_report() -> dict[str, Any]:
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def validate() -> dict[str, Any]:
    errors: list[str] = []
    report = load_report()
    metrics = report.get("metrics", {})
    if not isinstance(metrics, dict):
        errors.append("missing metrics object")
        metrics = {}

    scientific = metrics.get("scientific_progress_metrics", {})
    if not isinstance(scientific, dict):
        errors.append("missing scientific_progress_metrics object")
        scientific = {}

    methodology = metrics.get("ai_research_agent_methodology_metrics", {})
    if not isinstance(methodology, dict):
        errors.append("missing ai_research_agent_methodology_metrics object")
        methodology = {}

    metric_records = methodology.get("metrics", {})
    if not isinstance(metric_records, dict):
        errors.append("methodology metrics record must be a mapping")
        metric_records = {}

    metric_ids = set(metric_records)
    if metric_ids != REQUIRED_METRICS:
        errors.append(f"methodology metrics mismatch: {sorted(metric_ids)}")

    if "ai_research_agent_methodology_metrics" in scientific:
        errors.append("AI methodology metrics are nested under scientific_progress_metrics")

    if metrics.get("metric_separation_guard", {}).get("status") != "pass":
        errors.append("metric_separation_guard is not pass")

    authority = methodology.get("authority_boundary", {})
    for key in (
        "physics_claim_authority_created",
        "physics_promotion_authorized",
        "gate_chair_verdict_created",
        "benchmark_promotion_authorized",
    ):
        if authority.get(key) is not False:
            errors.append(f"methodology authority boundary {key} must be false")

    if methodology.get("status") not in {"measured", "partial"}:
        errors.append("methodology status must be measured or partial")

    warnings = methodology.get("calibrated_acceptance_warnings", [])
    if not isinstance(warnings, list):
        errors.append("calibrated_acceptance_warnings must be a list")
        warnings = []
    for warning in warnings:
        if warning.get("hard_gate") is not False:
            errors.append(f"warning {warning.get('warning_id')} must be advisory, not hard gate")
        if warning.get("physics_claim_authority") is not False:
            errors.append(f"warning {warning.get('warning_id')} must not create physics authority")

    for metric_id, record in metric_records.items():
        if record.get("status") not in {"measured", "partial", "not_measured"}:
            errors.append(f"{metric_id} has invalid status {record.get('status')}")
        boundary = record.get("authority_boundary", {})
        for key in (
            "physics_claim_authority_created",
            "physics_promotion_authorized",
            "gate_chair_verdict_created",
            "benchmark_promotion_authorized",
        ):
            if boundary.get(key) is not False:
                errors.append(f"{metric_id} authority boundary {key} must be false")

    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    for text in (
        "## AI Research-Agent Methodology Metrics",
        "## AI Methodology Acceptance Warnings",
        "`overclaim_catch_rate`",
        "support-only AI-system methodology metrics",
        "do not authorize physics proof",
    ):
        if text not in markdown:
            errors.append(f"markdown missing required text: {text}")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "json_path": str(JSON_PATH.relative_to(ROOT)),
        "markdown_path": str(MARKDOWN_PATH.relative_to(ROOT)),
        "metric_count": len(metric_records),
        "warning_count": len(warnings),
        "scientific_progress_contains_methodology_metrics": "ai_research_agent_methodology_metrics" in scientific,
        "metric_separation_guard_status": metrics.get("metric_separation_guard", {}).get("status"),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
