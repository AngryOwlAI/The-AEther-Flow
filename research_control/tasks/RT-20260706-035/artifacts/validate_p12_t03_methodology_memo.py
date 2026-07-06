#!/usr/bin/env python3
"""Validate the v17 P12-T03 AI-methodology evaluation memo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260706-035"
MEMO_PATH = TASK_DIR / "artifacts" / "ai_research_agent_methodology_evaluation_v1.md"
METRICS_PATH = ROOT / "output" / "physics_progress_metrics.json"
REPORT_PATH = TASK_DIR / "artifacts" / "p12_t03_methodology_memo_validation.json"

REQUIRED_SECTIONS = [
    "## Research-Agent Purpose",
    "## Metrics Definitions",
    "## Current Measured Values",
    "## Strengths",
    "## Failure Modes",
    "## Recommendations",
    "## Physics Claim Boundary",
]

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

REQUIRED_BOUNDARY_TEXT = [
    "physics_claim_authority_created: false",
    "physics_promotion_authorized: false",
    "gate_chair_verdict_created: false",
    "benchmark_promotion_authorized: false",
    "completed_derivation_authorized: false",
    "distance_to_gr_delta: \"none\"",
]


def load_metrics() -> dict[str, Any]:
    report = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    metrics = report.get("metrics", {}).get("ai_research_agent_methodology_metrics", {})
    if not isinstance(metrics, dict):
        return {}
    return metrics


def validate() -> dict[str, Any]:
    errors: list[str] = []
    memo = MEMO_PATH.read_text(encoding="utf-8") if MEMO_PATH.exists() else ""
    metrics = load_metrics()

    for section in REQUIRED_SECTIONS:
        if section not in memo:
            errors.append(f"memo missing required section: {section}")

    for metric_id in REQUIRED_METRICS:
        if f"`{metric_id}`" not in memo:
            errors.append(f"memo missing metric id: {metric_id}")

    for text in REQUIRED_BOUNDARY_TEXT:
        if text not in memo:
            errors.append(f"memo missing boundary text: {text}")

    for text in (
        "support-only AI methodology evaluation memo",
        "It does not evaluate the truth of any physics claim.",
        "The current methodology metrics are support-only diagnostics.",
        "analysis to response artifact to handoff loop",
    ):
        if text not in memo:
            errors.append(f"memo missing methodology boundary text: {text}")

    metric_records = metrics.get("metrics", {})
    if set(metric_records) != REQUIRED_METRICS:
        errors.append(f"metrics report ids mismatch: {sorted(metric_records)}")

    if metrics.get("status") != "partial":
        errors.append("P12-T03 expects current methodology metric status to be partial")

    if metrics.get("metric_count") != 9:
        errors.append("methodology metric count must be 9")

    separation_guard = metrics.get("separation_guard", {})
    if separation_guard.get("status") != "pass":
        errors.append("methodology metrics separation guard must pass")

    warnings = metrics.get("calibrated_acceptance_warnings", [])
    if len(warnings) != 3:
        errors.append("expected exactly three P12-T02 advisory warnings")
    for warning in warnings:
        if warning.get("hard_gate") is not False:
            errors.append(f"warning {warning.get('warning_id')} must not be hard gate")
        if warning.get("physics_claim_authority") is not False:
            errors.append(f"warning {warning.get('warning_id')} must not create physics authority")

    boundary = metrics.get("authority_boundary", {})
    for key in (
        "physics_claim_authority_created",
        "physics_promotion_authorized",
        "gate_chair_verdict_created",
        "benchmark_promotion_authorized",
    ):
        if boundary.get(key) is not False:
            errors.append(f"metrics authority boundary {key} must be false")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "memo_path": str(MEMO_PATH.relative_to(ROOT)),
        "metrics_path": str(METRICS_PATH.relative_to(ROOT)),
        "required_section_count": len(REQUIRED_SECTIONS),
        "required_metric_count": len(REQUIRED_METRICS),
        "metrics_report_status": metrics.get("status"),
        "metrics_report_metric_count": metrics.get("metric_count"),
        "warning_count": len(warnings) if isinstance(warnings, list) else 0,
        "physics_claim_authority_created": False,
        "physics_promotion_authorized": False,
        "distance_to_gr_delta": "none",
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
