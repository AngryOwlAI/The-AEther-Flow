#!/usr/bin/env python3
"""Validate the v17 P12-T04 AI methodology dashboard integration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_ai_methodology_metrics_dashboard as dashboard_renderer  # noqa: E402


JSON_PATH = ROOT / "output" / "ai_methodology_metrics_dashboard.json"
MARKDOWN_PATH = ROOT / "wiki" / "indexes" / "ai_methodology_metrics_dashboard.md"
REPORT_PATH = (
    ROOT
    / "research_control"
    / "tasks"
    / "RT-20260706-036"
    / "artifacts"
    / "p12_t04_methodology_dashboard_validation.json"
)
REQUIRED_METRICS = set(dashboard_renderer.metrics_reporter.AI_METHODOLOGY_REQUIRED_METRICS)
FORBIDDEN_RANKING_FIELDS = {
    "truth_rank",
    "physics_truth_rank",
    "physics_truth_score",
    "physics_truth_ranking",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> dict[str, Any]:
    errors: list[str] = []
    freshness_errors = dashboard_renderer.check_outputs(
        dashboard_renderer.build_dashboard(ROOT),
        ROOT,
        str(JSON_PATH.relative_to(ROOT)),
        str(MARKDOWN_PATH.relative_to(ROOT)),
    )
    errors.extend(freshness_errors)

    if not JSON_PATH.exists():
        errors.append("missing dashboard JSON output")
        payload: dict[str, Any] = {}
    else:
        payload = load_json(JSON_PATH)
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8") if MARKDOWN_PATH.exists() else ""

    if payload.get("schema_id") != dashboard_renderer.SCHEMA_ID:
        errors.append("dashboard JSON has wrong schema_id")
    if payload.get("dashboard_type") != "support_only_ai_system_diagnostic":
        errors.append("dashboard_type must be support_only_ai_system_diagnostic")

    labels = payload.get("dashboard_labels", {})
    if not isinstance(labels, dict):
        errors.append("dashboard_labels must be a mapping")
        labels = {}
    if labels.get("primary_label") != "AI-system diagnostic":
        errors.append("dashboard primary label must be AI-system diagnostic")
    if labels.get("support_only") is not True:
        errors.append("dashboard support_only flag must be true")
    if labels.get("truth_ranking") != "none":
        errors.append("dashboard truth_ranking must be none")
    if labels.get("no_physics_truth_ranking") is not True:
        errors.append("dashboard no_physics_truth_ranking flag must be true")

    rows = payload.get("metric_rows", [])
    if not isinstance(rows, list):
        errors.append("metric_rows must be a list")
        rows = []
    metric_ids = {row.get("metric_id") for row in rows if isinstance(row, dict)}
    if metric_ids != REQUIRED_METRICS:
        errors.append(f"metric_rows mismatch: {sorted(str(item) for item in metric_ids)}")

    for row in rows:
        if not isinstance(row, dict):
            errors.append("metric row must be a mapping")
            continue
        metric_id = row.get("metric_id", "")
        if row.get("diagnostic_label") != "AI-system diagnostic":
            errors.append(f"{metric_id} missing AI-system diagnostic label")
        forbidden_present = sorted(FORBIDDEN_RANKING_FIELDS.intersection(row))
        if forbidden_present:
            errors.append(f"{metric_id} contains forbidden ranking fields: {forbidden_present}")
        boundary = row.get("authority_boundary", {})
        if not isinstance(boundary, dict):
            errors.append(f"{metric_id} authority_boundary must be a mapping")
            continue
        for key in (
            "physics_claim_authority_created",
            "physics_promotion_authorized",
            "gate_chair_verdict_created",
            "benchmark_promotion_authorized",
        ):
            if boundary.get(key) is not False:
                errors.append(f"{metric_id} authority boundary {key} must be false")

    claim_boundary = payload.get("claim_boundary", {})
    if not isinstance(claim_boundary, dict):
        errors.append("claim_boundary must be a mapping")
        claim_boundary = {}
    for key in (
        "physics_claim_authority_created",
        "physics_promotion_authorized",
        "gate_chair_verdict_created",
        "benchmark_promotion_authorized",
    ):
        if claim_boundary.get(key) is not False:
            errors.append(f"claim_boundary {key} must be false")
    if claim_boundary.get("dashboard_not_physics_proof") is not True:
        errors.append("dashboard_not_physics_proof must be true")
    if claim_boundary.get("dashboard_not_physics_truth_ranking") is not True:
        errors.append("dashboard_not_physics_truth_ranking must be true")

    for phrase in dashboard_renderer.REQUIRED_MARKDOWN_PHRASES:
        if phrase not in markdown:
            errors.append(f"dashboard markdown missing required phrase: {phrase}")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "json_path": str(JSON_PATH.relative_to(ROOT)),
        "markdown_path": str(MARKDOWN_PATH.relative_to(ROOT)),
        "metric_count": len(rows),
        "warning_count": len(payload.get("advisory_warning_rows", []))
        if isinstance(payload.get("advisory_warning_rows"), list)
        else 0,
        "dashboard_label": labels.get("primary_label"),
        "support_only": labels.get("support_only"),
        "truth_ranking": labels.get("truth_ranking"),
        "no_physics_truth_ranking": labels.get("no_physics_truth_ranking"),
        "physics_claim_authority_created": claim_boundary.get("physics_claim_authority_created"),
        "physics_promotion_authorized": claim_boundary.get("physics_promotion_authorized"),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate()
    if args.write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
