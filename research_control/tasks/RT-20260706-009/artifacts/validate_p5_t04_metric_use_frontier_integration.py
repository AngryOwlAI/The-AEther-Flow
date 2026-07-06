#!/usr/bin/env python3
"""Validate v17 P5-T04 metric-use frontier integration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_compact_current_frontier_v16 as compact_renderer  # noqa: E402
import render_current_frontier as current_renderer  # noqa: E402
import validate_compact_current_frontier_v16 as compact_validator  # noqa: E402


REPORT_PATH = (
    "research_control/tasks/RT-20260706-009/artifacts/"
    "p5_t04_metric_use_frontier_integration_report.json"
)
RECEIPT_PATH = (
    "research_control/tasks/RT-20260706-009/artifacts/"
    "p5_t04_metric_use_frontier_integration_receipt.md"
)


def int_value(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def build_report(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    current_payload, current_markdown = current_renderer.render_payload(repo_root)
    compact_snapshot = compact_renderer.build_snapshot(repo_root)
    compact_errors = compact_renderer.validate_snapshot(compact_snapshot)
    compact_report = compact_validator.build_report(repo_root)

    current_summary = current_payload.get("metric_use_ledger_summary", {})
    compact_summary = compact_snapshot.get("metric_use_ledger", {})
    if current_payload.get("metric_use_ledger_path") != current_renderer.METRIC_USE_LEDGER_PATH:
        errors.append("current frontier payload missing metric-use ledger path")
    if current_summary.get("ledger_path") != current_renderer.METRIC_USE_LEDGER_PATH:
        errors.append("current frontier metric-use summary path mismatch")
    if int_value(current_summary.get("forbidden_or_import_row_count")) <= 0:
        errors.append("current frontier forbidden/import guard row count must be positive")
    if "## Metric-Use Ledger Warning" not in current_markdown:
        errors.append("current frontier markdown missing metric-use warning section")
    if "Forbidden/import guard rows" not in current_markdown:
        errors.append("current frontier markdown missing forbidden/import row count")

    if compact_summary.get("ledger_path") != compact_renderer.METRIC_USE_LEDGER_PATH:
        errors.append("compact frontier metric-use summary path mismatch")
    if int_value(compact_summary.get("forbidden_or_import_row_count")) <= 0:
        errors.append("compact frontier forbidden/import guard row count must be positive")
    if compact_errors:
        errors.extend(f"compact snapshot schema error: {message}" for message in compact_errors)
    if compact_report.get("status") != "PASS":
        errors.append("compact frontier validator did not pass")
    if compact_report.get("physics_proof_authority") is not False:
        errors.append("compact frontier validator must preserve no proof authority")
    if compact_report.get("no_physics_delta") is not True:
        errors.append("compact frontier validator must preserve no physics delta")

    return {
        "schema_id": "p5_t04_metric_use_frontier_integration_report_v1",
        "task_id": "RT-20260706-009",
        "job_id": "AJ-RT-20260706-009-001",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "current_frontier": {
            "path": current_renderer.DEFAULT_FRONTIER_PATH,
            "metric_use_ledger_path": current_payload.get("metric_use_ledger_path"),
            "total_row_count": current_summary.get("total_row_count"),
            "forbidden_or_import_row_count": current_summary.get("forbidden_or_import_row_count"),
            "blocked_physical_metric_use_row_count": current_summary.get(
                "blocked_physical_metric_use_row_count"
            ),
        },
        "compact_frontier": {
            "yaml_path": compact_renderer.DEFAULT_YAML_PATH,
            "json_path": compact_renderer.DEFAULT_JSON_PATH,
            "markdown_path": compact_renderer.DEFAULT_MARKDOWN_PATH,
            "metric_use_ledger_path": compact_summary.get("ledger_path"),
            "total_row_count": compact_summary.get("total_row_count"),
            "forbidden_or_import_row_count": compact_summary.get("forbidden_or_import_row_count"),
            "blocked_physical_metric_use_row_count": compact_summary.get(
                "blocked_physical_metric_use_row_count"
            ),
            "validator_status": compact_report.get("status"),
            "physics_proof_authority": compact_report.get("physics_proof_authority"),
            "no_physics_delta": compact_report.get("no_physics_delta"),
        },
    }


def receipt_text(report: dict[str, Any]) -> str:
    current = report["current_frontier"]
    compact = report["compact_frontier"]
    return f"""<!-- authority: control -->

# P5-T04 Metric-Use Frontier Integration Receipt

Task `RT-20260706-009` integrates the metric-use ledger into generated frontier
surfaces only. The current frontier now renders a metric-use warning/status
section, and the compact frontier exposes the ledger path plus guarded row
counts.

## Result

- Status: `{report['status']}`
- Current frontier ledger path: `{current['metric_use_ledger_path']}`
- Current frontier forbidden/import guard rows: `{current['forbidden_or_import_row_count']}`
- Compact frontier ledger path: `{compact['metric_use_ledger_path']}`
- Compact frontier forbidden/import guard rows: `{compact['forbidden_or_import_row_count']}`
- Compact frontier validator status: `{compact['validator_status']}`

## Boundary

This receipt is a renderer and validator-control receipt only. It does not
adopt `MetricData(E)`, expand `g_eff`, authorize a physical metric, import
matter dynamics, promote benchmark status, issue a Gate Chair verdict, or prove
any downstream GR claim.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    if args.write_report:
        report_path = repo_root / REPORT_PATH
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (repo_root / RECEIPT_PATH).write_text(receipt_text(report), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
