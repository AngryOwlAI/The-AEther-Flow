#!/usr/bin/env python3
"""Render the AI methodology metrics dashboard.

The dashboard is a support-only AI-system diagnostic. It is not a physics
truth ranking, proof authority, benchmark authority, or Gate Chair verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import report_physics_progress_metrics as metrics_reporter  # noqa: E402
import scientific_quality_metrics  # noqa: E402


SCHEMA_ID = "ai_methodology_metrics_dashboard_v1"
DEFAULT_JSON_PATH = "output/ai_methodology_metrics_dashboard.json"
DEFAULT_MARKDOWN_PATH = "output/ai_methodology_metrics_dashboard.md"
DEFAULT_WIKI_MARKDOWN_PATH = "wiki/indexes/ai_methodology_metrics_dashboard.md"
METRICS_JSON_PATH = "output/physics_progress_metrics.json"
METRICS_MARKDOWN_PATH = "output/physics_progress_metrics.md"
SOURCE_PATHS = [
    "implementations_plans/recommendations_implementation_plan_continue_task-v17.md",
    "implementations_plans/recommendations_implementation_plan_continue_task-v18.md",
    "research_control/design/v17_recommendation_backlog.yaml",
    "research_control/design/v18_recommendation_backlog.yaml",
    "research_control/design/ai_research_agent_metrics_taxonomy_v1.md",
    "research_control/design/physics_payload_ratio_policy_v1.md",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_metric_taxonomy_v1.md",
    "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_calibration_warning_policy_v1.md",
    "research_control/tasks/RT-20260721-006/artifacts/v21_research_attempt_ledger.json",
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_registry.json",
    "research_control/current_frontier.md",
    "research_control/handoffs/handoff-0667.yaml",
    "research_control/handoffs/handoff-0722.yaml",
    "research_control/tasks/RT-20260706-035/artifacts/ai_research_agent_methodology_evaluation_v1.md",
    "research_control/tasks/RT-20260708-028/artifacts/payload_ratio_metrics_report_v1.md",
    "research_control/tasks/RT-20260708-029/artifacts/payload_ratio_validator_pilot_report_v1.md",
    METRICS_JSON_PATH,
    METRICS_MARKDOWN_PATH,
]
REQUIRED_MARKDOWN_PHRASES = [
    "AI-system diagnostic",
    "does not rank physics truth by workflow activity",
    "do not establish physics truth",
    "Payload-Ratio Diagnostics",
    "Route-Orbit Warnings",
    "Durable Scientific-Quality Diagnostics",
    "raw volume is operational context only",
    "support-only",
]
FORBIDDEN_ROW_FIELDS = {
    "truth_rank",
    "physics_truth_rank",
    "physics_truth_score",
    "physics_truth_ranking",
}


class DashboardError(RuntimeError):
    """Raised when dashboard inputs or outputs are invalid."""


def repo_path(repo_root: Path, rel_path: str) -> Path:
    return repo_root / rel_path


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes(repo_root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel_path in SOURCE_PATHS:
        path = repo_path(repo_root, rel_path)
        if path.exists():
            hashes[rel_path] = sha256_path(path)
    return hashes


def load_methodology_report(repo_root: Path) -> dict[str, Any]:
    report = metrics_reporter.build_report(repo_root)
    metrics = report.get("metrics", {})
    if not isinstance(metrics, dict):
        raise DashboardError("metrics report missing metrics object")
    methodology = metrics.get("ai_research_agent_methodology_metrics")
    if not isinstance(methodology, dict):
        raise DashboardError("metrics report missing ai_research_agent_methodology_metrics")
    metric_records = methodology.get("metrics")
    if not isinstance(metric_records, dict):
        raise DashboardError("methodology metrics must be a mapping")
    return report


def value_text(value: Any) -> str:
    if value is None:
        return "not measured"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def markdown_cell(value: Any) -> str:
    text = value_text(value)
    return text.replace("|", "\\|").replace("\n", " ")


def metric_rows(methodology: dict[str, Any]) -> list[dict[str, Any]]:
    records = methodology.get("metrics", {})
    if not isinstance(records, dict):
        raise DashboardError("methodology metrics must be a mapping")

    rows: list[dict[str, Any]] = []
    for metric_id in metrics_reporter.AI_METHODOLOGY_REQUIRED_METRICS:
        record = records.get(metric_id)
        if not isinstance(record, dict):
            raise DashboardError(f"missing methodology metric: {metric_id}")
        row = {
            "metric_id": metric_id,
            "dashboard_label": "AI-system diagnostic",
            "diagnostic_label": "AI-system diagnostic",
            "family": record.get("family", ""),
            "status": record.get("status", ""),
            "value": record.get("value"),
            "numerator_value": (record.get("numerator") or {}).get("value"),
            "denominator_value": (record.get("denominator") or {}).get("value"),
            "diagnostic_interpretation": record.get("diagnostic_interpretation", ""),
            "interpretation_guardrail": record.get("interpretation_guardrail", ""),
            "uncertainty_note": record.get("uncertainty_note", ""),
            "authority_boundary": record.get("authority_boundary", {}),
        }
        if FORBIDDEN_ROW_FIELDS.intersection(row):
            raise DashboardError(f"metric row contains forbidden ranking field: {metric_id}")
        rows.append(row)
    return rows


def warning_rows(methodology: dict[str, Any]) -> list[dict[str, Any]]:
    warnings = methodology.get("calibrated_acceptance_warnings", [])
    if not isinstance(warnings, list):
        raise DashboardError("calibrated_acceptance_warnings must be a list")
    rows: list[dict[str, Any]] = []
    for warning in warnings:
        if not isinstance(warning, dict):
            continue
        rows.append(
            {
                "warning_id": warning.get("warning_id", ""),
                "metric_id": warning.get("metric_id", ""),
                "status": warning.get("status", ""),
                "severity": warning.get("severity", ""),
                "diagnostic_label": "AI-system diagnostic warning",
                "hard_gate": warning.get("hard_gate"),
                "physics_claim_authority": warning.get("physics_claim_authority"),
                "reason": warning.get("reason", ""),
                "recommended_guard_action": warning.get("recommended_guard_action", ""),
            }
        )
    return rows


def load_payload_ratio_diagnostics(report: dict[str, Any]) -> dict[str, Any]:
    diagnostics = report.get("metrics", {}).get("physics_payload_ratio_diagnostics")
    if not isinstance(diagnostics, dict):
        raise DashboardError("metrics report missing physics_payload_ratio_diagnostics")
    metric_records = diagnostics.get("metrics")
    if not isinstance(metric_records, dict):
        raise DashboardError("physics_payload_ratio_diagnostics.metrics must be a mapping")
    boundary = diagnostics.get("authority_boundary")
    if not isinstance(boundary, dict):
        raise DashboardError("physics_payload_ratio_diagnostics missing authority_boundary")
    if boundary.get("does_not_rank_physics_truth") is not True:
        raise DashboardError("payload-ratio diagnostics must not rank physics truth")
    if boundary.get("not_physics_proof") is not True:
        raise DashboardError("payload-ratio diagnostics must be marked not physics proof")
    return diagnostics


PAYLOAD_RATIO_INTERPRETATIONS = {
    "project_system_task_run_length": "Trailing project-system packet run length.",
    "physics_bearing_task_run_length": "Trailing physics-bearing packet run length.",
    "new_mathematical_payload_count": "Total tracked mathematical payload items in route history.",
    "theorem_countermodel_candidate_count": "Tasks carrying theorem, countermodel, or candidate signals.",
    "candidate_construction_count": "Tasks carrying candidate-construction signals.",
    "support_only_task_count_since_last_physics_payload": (
        "Support-only packets since the last recorded physics payload."
    ),
    "route_orbit_warning_status": "Current route-orbit warning bundle.",
    "project_system_task_count": "Tracked project-system task count.",
    "physics_bearing_task_count": "Tracked physics-bearing task count.",
    "support_only_task_count": "Tracked support-only task count.",
    "physics_bearing_to_project_system_task_ratio": (
        "Ratio of physics-bearing tasks to project-system tasks."
    ),
    "new_mathematical_payload_to_support_only_task_ratio": (
        "Ratio of mathematical payload items to support-only tasks."
    ),
    "route_orbit_same_burden_repetition_count": (
        "Repeated-burden route-orbit diagnostic count."
    ),
}


def payload_ratio_metric_rows(diagnostics: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = diagnostics.get("metrics", {})
    if not isinstance(metrics, dict):
        raise DashboardError("payload-ratio metrics must be a mapping")
    boundary = diagnostics.get("authority_boundary", {})
    rows: list[dict[str, Any]] = []
    for metric_id, value in metrics.items():
        row = {
            "metric_id": metric_id,
            "dashboard_label": "AI-system diagnostic",
            "diagnostic_label": "Payload-ratio diagnostic",
            "family": "physics_payload_ratio",
            "status": diagnostics.get("status", "measured"),
            "value": value,
            "diagnostic_interpretation": PAYLOAD_RATIO_INTERPRETATIONS.get(
                metric_id,
                "Support-only route-history diagnostic.",
            ),
            "interpretation_guardrail": (
                "Does not establish physics truth, proof authority, benchmark status, "
                "Gate Chair verdicts, or completed derivations."
            ),
            "authority_boundary": boundary,
        }
        if FORBIDDEN_ROW_FIELDS.intersection(row):
            raise DashboardError(f"payload-ratio row contains forbidden ranking field: {metric_id}")
        rows.append(row)
    return rows


def route_orbit_warning_rows(
    diagnostic_warnings: list[dict[str, Any]],
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    if not isinstance(diagnostic_warnings, list):
        raise DashboardError("diagnostic_warnings must be a list")
    warning_status = diagnostics.get("metrics", {}).get("route_orbit_warning_status", {})
    if not isinstance(warning_status, dict):
        raise DashboardError("route_orbit_warning_status must be a mapping")
    route_warning_ids = {
        str(warning_id)
        for warning_id in warning_status.get("warning_ids", [])
        if warning_id
    }
    rows: list[dict[str, Any]] = []
    for warning in diagnostic_warnings:
        if not isinstance(warning, dict):
            continue
        warning_id = str(warning.get("warning_id", ""))
        if warning_id not in route_warning_ids:
            continue
        evidence_paths = warning.get("evidence_paths", [])
        if not isinstance(evidence_paths, list):
            evidence_paths = []
        rows.append(
            {
                "warning_id": warning_id,
                "metric_key": warning.get("metric_key", ""),
                "severity": warning.get("severity", ""),
                "observed_value": warning.get("observed_value"),
                "threshold": warning.get("threshold"),
                "diagnostic_label": "Route-orbit warning",
                "hard_gate": warning.get("hard_gate"),
                "physics_claim_authority": warning.get("physics_claim_authority"),
                "recommended_guard_action": warning.get("recommended_guard_action", ""),
                "evidence_path_count": len(evidence_paths),
                "first_evidence_path": evidence_paths[0] if evidence_paths else "",
            }
        )
    return rows


def load_durable_quality_diagnostics(report: dict[str, Any]) -> dict[str, Any]:
    diagnostics = report.get("metrics", {}).get(
        "durable_scientific_quality_metrics"
    )
    if not isinstance(diagnostics, dict):
        raise DashboardError(
            "metrics report missing durable_scientific_quality_metrics"
        )
    records = diagnostics.get("metrics")
    if not isinstance(records, dict):
        raise DashboardError(
            "durable_scientific_quality_metrics.metrics must be a mapping"
        )
    if set(records) != set(scientific_quality_metrics.REQUIRED_METRIC_IDS):
        raise DashboardError(
            "durable scientific-quality metric identity set or order is invalid"
        )
    boundary = diagnostics.get("authority_boundary")
    if not isinstance(boundary, dict):
        raise DashboardError(
            "durable scientific-quality diagnostics missing authority_boundary"
        )
    if boundary.get("aggregate_scientific_truth_score_created") is not False:
        raise DashboardError(
            "durable scientific-quality diagnostics cannot create a truth score"
        )
    if diagnostics.get("raw_volume_is_primary_quality") is not False:
        raise DashboardError("raw volume cannot be the primary quality surface")
    return diagnostics


def durable_quality_metric_rows(
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    records = diagnostics["metrics"]
    rows: list[dict[str, Any]] = []
    for metric_id in scientific_quality_metrics.REQUIRED_METRIC_IDS:
        record = records[metric_id]
        numerator = record.get("numerator", {})
        denominator = record.get("denominator", {})
        row = {
            "metric_id": metric_id,
            "dashboard_label": "Primary scientific-quality diagnostic",
            "diagnostic_label": "Durable scientific-quality diagnostic",
            "family": record.get("family", ""),
            "status": record.get("status", ""),
            "value": record.get("value"),
            "numerator_value": numerator.get("value"),
            "denominator_value": denominator.get("value"),
            "eligible_identity_count": len(denominator.get("eligible_ids", [])),
            "qualifying_identity_count": len(
                numerator.get("qualifying_ids", [])
            ),
            "warning_count": len(record.get("warnings", [])),
            "diagnostic_interpretation": record.get("definition", ""),
            "interpretation_guardrail": record.get(
                "interpretation_guardrail",
                "",
            ),
            "authority_boundary": record.get("authority_boundary", {}),
        }
        if FORBIDDEN_ROW_FIELDS.intersection(row):
            raise DashboardError(
                f"durable-quality row contains forbidden ranking field: {metric_id}"
            )
        rows.append(row)
    return rows


def durable_quality_warning_rows(
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for warning in diagnostics.get("warnings", []):
        if not isinstance(warning, dict):
            continue
        rows.append(
            {
                "warning_id": warning.get("warning_id", ""),
                "metric_id": warning.get("metric_id", ""),
                "code": warning.get("code", ""),
                "severity": warning.get("severity", ""),
                "hard_gate": warning.get("hard_gate"),
                "physics_claim_authority": warning.get(
                    "physics_claim_authority"
                ),
                "message": warning.get("message", ""),
            }
        )
    return rows


def build_dashboard(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    repo_root = Path(repo_root)
    report = load_methodology_report(repo_root)
    methodology = report["metrics"]["ai_research_agent_methodology_metrics"]
    payload_diagnostics = load_payload_ratio_diagnostics(report)
    durable_quality = load_durable_quality_diagnostics(report)
    rows = metric_rows(methodology)
    warnings = warning_rows(methodology)
    durable_rows = durable_quality_metric_rows(durable_quality)
    durable_warnings = durable_quality_warning_rows(durable_quality)
    payload_rows = payload_ratio_metric_rows(payload_diagnostics)
    route_warnings = route_orbit_warning_rows(
        report["metrics"].get("diagnostic_warnings", []),
        payload_diagnostics,
    )
    status_counts: dict[str, int] = {}
    for row in rows:
        status = str(row.get("status") or "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    durable_status_counts: dict[str, int] = {}
    for row in durable_rows:
        status = str(row.get("status") or "unknown")
        durable_status_counts[status] = durable_status_counts.get(status, 0) + 1

    return {
        "schema_id": SCHEMA_ID,
        "dashboard_type": "support_only_ai_system_diagnostic",
        "plan_task_id": "P8-T04",
        "plan_task_ids": ["P12-T05", "P12-T04", "P8-T04"],
        "title": "AI Methodology Metrics Dashboard",
        "source_metrics_report": {
            "report_id": report.get("report_id", ""),
            "as_of": report.get("as_of", ""),
            "source_basis": report.get("source_basis", []),
            "metric_separation_guard_status": report["metrics"].get(
                "metric_separation_guard",
                {},
            ).get("status"),
        },
        "generated_from": {
            "source_paths": [path for path in SOURCE_PATHS if repo_path(repo_root, path).exists()],
            "source_hashes": source_hashes(repo_root),
        },
        "dashboard_labels": {
            "primary_label": "AI-system diagnostic",
            "support_only": True,
            "truth_ranking": "none",
            "no_physics_truth_ranking": True,
            "boundary_statement": (
                "This dashboard labels metrics as AI-system diagnostics and "
                "does not rank physics truth by workflow activity. Durable-quality "
                "rows are identity-bound advisory diagnostics; payload-ratio "
                "diagnostics and route-orbit warnings do not establish physics truth."
            ),
        },
        "summary_cards": {
            "metric_count": len(rows),
            "measured_count": status_counts.get("measured", 0),
            "partial_count": status_counts.get("partial", 0),
            "not_measured_count": status_counts.get("not_measured", 0),
            "advisory_warning_count": len(warnings),
            "metric_separation_guard_status": report["metrics"].get(
                "metric_separation_guard",
                {},
            ).get("status"),
            "payload_ratio_metric_count": len(payload_rows),
            "payload_ratio_status": payload_diagnostics.get("status"),
            "payload_ratio_route_orbit_status": payload_diagnostics["metrics"].get(
                "route_orbit_warning_status",
                {},
            ).get("status"),
            "route_orbit_warning_count": len(route_warnings),
            "durable_quality_metric_count": len(durable_rows),
            "durable_quality_measured_count": durable_status_counts.get(
                "measured",
                0,
            ),
            "durable_quality_not_measured_count": durable_status_counts.get(
                "not_measured",
                0,
            ),
            "durable_quality_invalid_count": durable_status_counts.get(
                "invalid",
                0,
            ),
            "durable_quality_warning_count": len(durable_warnings),
        },
        "durable_scientific_quality_metrics": {
            "schema_id": durable_quality.get("schema_id"),
            "status": durable_quality.get("status"),
            "quality_surface": durable_quality.get("quality_surface"),
            "raw_volume_is_primary_quality": durable_quality.get(
                "raw_volume_is_primary_quality"
            ),
            "metric_count": durable_quality.get("metric_count"),
            "status_counts": durable_quality.get("status_counts", {}),
            "aggregate_metric": durable_quality.get("aggregate_metric"),
            "aggregate_metric_reason": durable_quality.get(
                "aggregate_metric_reason",
                "",
            ),
            "source_basis": durable_quality.get("source_basis", []),
            "authority_boundary": durable_quality.get(
                "authority_boundary",
                {},
            ),
        },
        "durable_quality_metric_rows": durable_rows,
        "durable_quality_warning_rows": durable_warnings,
        "metric_rows": rows,
        "advisory_warning_rows": warnings,
        "physics_payload_ratio_diagnostics": payload_diagnostics,
        "payload_ratio_metric_rows": payload_rows,
        "route_orbit_warning_rows": route_warnings,
        "claim_boundary": {
            "physics_claim_authority_created": False,
            "physics_promotion_authorized": False,
            "gate_chair_verdict_created": False,
            "benchmark_promotion_authorized": False,
            "dashboard_not_physics_proof": True,
            "dashboard_not_physics_truth_ranking": True,
            "dashboard_not_physics_truth_establishment": True,
            "durable_quality_is_advisory": True,
            "durable_quality_is_primary_quality_surface": True,
            "raw_volume_is_primary_scientific_quality": False,
            "aggregate_scientific_truth_score_created": False,
            "forbidden_overreads": [
                "methodology metric success as physics proof",
                "methodology dashboard as autonomous scientific authority",
                "methodology dashboard as benchmark promotion",
                "workflow activity as physics truth ranking",
                "candidate survival as canonical ontology adoption",
                "route-orbit reduction as Einstein-equation derivation",
                "human authorization as Gate Chair verdict",
                "proof-to-process balance as completed derivation",
                "durable-quality metric as theorem truth",
                "raw packet or artifact volume as scientific quality",
            ],
        },
    }


def render_markdown(dashboard: dict[str, Any]) -> str:
    labels = dashboard["dashboard_labels"]
    summary = dashboard["summary_cards"]
    lines = [
        "<!-- authority: generated -->",
        "",
        "# AI Methodology Metrics Dashboard",
        "",
        (
            "This is a support-only AI-system diagnostic. It labels metrics as "
            "AI-system diagnostics and does not rank physics truth by workflow activity."
        ),
        (
            "Payload-ratio diagnostics and route-orbit warnings do not establish "
            "physics truth, proof authority, benchmark status, Gate Chair verdicts, "
            "or completed derivations."
        ),
        (
            "Durable scientific-quality rows are the primary quality diagnostics; "
            "raw volume is operational context only."
        ),
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Dashboard label | {markdown_cell(labels['primary_label'])} |",
        f"| Support-only | {markdown_cell(labels['support_only'])} |",
        f"| Truth ranking | {markdown_cell(labels['truth_ranking'])} |",
        f"| Metric count | {markdown_cell(summary['metric_count'])} |",
        f"| Measured | {markdown_cell(summary['measured_count'])} |",
        f"| Partial | {markdown_cell(summary['partial_count'])} |",
        f"| Not measured | {markdown_cell(summary['not_measured_count'])} |",
        f"| Advisory warnings | {markdown_cell(summary['advisory_warning_count'])} |",
        f"| Metric separation guard | {markdown_cell(summary['metric_separation_guard_status'])} |",
        f"| Payload-ratio metrics | {markdown_cell(summary['payload_ratio_metric_count'])} |",
        f"| Payload-ratio status | {markdown_cell(summary['payload_ratio_status'])} |",
        f"| Route-orbit warning status | {markdown_cell(summary['payload_ratio_route_orbit_status'])} |",
        f"| Route-orbit warnings | {markdown_cell(summary['route_orbit_warning_count'])} |",
        f"| Durable-quality metrics | {markdown_cell(summary['durable_quality_metric_count'])} |",
        f"| Durable-quality measured | {markdown_cell(summary['durable_quality_measured_count'])} |",
        f"| Durable-quality not measured | {markdown_cell(summary['durable_quality_not_measured_count'])} |",
        f"| Durable-quality invalid | {markdown_cell(summary['durable_quality_invalid_count'])} |",
        f"| Durable-quality warnings | {markdown_cell(summary['durable_quality_warning_count'])} |",
        "",
        "## Durable Scientific-Quality Diagnostics",
        "",
        (
            "These eight identity-bound rows are the primary scientific-quality "
            "diagnostic surface. They are advisory, use explicit eligible-set "
            "denominators, preserve `not_measured`, and are never aggregated into "
            "a scientific-truth score."
        ),
        "",
        "| Metric | Family | Status | Numerator | Denominator | Value | Warnings | Guardrail |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in dashboard["durable_quality_metric_rows"]:
        lines.append(
            "| `{metric_id}` | {family} | {status} | {numerator} | "
            "{denominator} | {value} | {warnings} | {guardrail} |".format(
                metric_id=markdown_cell(row["metric_id"]),
                family=markdown_cell(row.get("family", "")),
                status=markdown_cell(row.get("status", "")),
                numerator=markdown_cell(row.get("numerator_value")),
                denominator=markdown_cell(row.get("denominator_value")),
                value=markdown_cell(row.get("value")),
                warnings=markdown_cell(row.get("warning_count")),
                guardrail=markdown_cell(
                    row.get("interpretation_guardrail", "")
                ),
            )
        )

    lines.extend(
        [
            "",
            "### Durable-Quality Calibration Warnings",
            "",
            "| Warning | Metric | Code | Severity | Hard gate | Physics authority | Message |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    durable_warnings = dashboard["durable_quality_warning_rows"]
    if durable_warnings:
        for warning in durable_warnings:
            lines.append(
                "| `{warning_id}` | `{metric_id}` | `{code}` | {severity} | "
                "{hard_gate} | {authority} | {message} |".format(
                    warning_id=markdown_cell(warning.get("warning_id", "")),
                    metric_id=markdown_cell(warning.get("metric_id", "")),
                    code=markdown_cell(warning.get("code", "")),
                    severity=markdown_cell(warning.get("severity", "")),
                    hard_gate=markdown_cell(warning.get("hard_gate")),
                    authority=markdown_cell(
                        warning.get("physics_claim_authority")
                    ),
                    message=markdown_cell(warning.get("message", "")),
                )
            )
    else:
        lines.append("| none | none | none | none | false | false | none |")

    lines.extend(
        [
        "",
        "## AI Methodology Metric Rows",
        "",
        "| Metric | Family | Status | Value | Diagnostic interpretation | Guardrail |",
        "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in dashboard["metric_rows"]:
        lines.append(
            "| `{metric_id}` | {family} | {status} | {value} | {interpretation} | {guardrail} |".format(
                metric_id=markdown_cell(row["metric_id"]),
                family=markdown_cell(row.get("family", "")),
                status=markdown_cell(row.get("status", "")),
                value=markdown_cell(row.get("value")),
                interpretation=markdown_cell(row.get("diagnostic_interpretation", "")),
                guardrail=markdown_cell(row.get("interpretation_guardrail", "")),
            )
        )

    lines.extend(
        [
            "",
            "## Payload-Ratio Diagnostics",
            "",
            (
                "These raw counts and ratios are operational context only. They "
                "are not the primary scientific-quality surface."
            ),
            "",
            "| Metric | Status | Value | Diagnostic interpretation | Guardrail |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in dashboard["payload_ratio_metric_rows"]:
        lines.append(
            "| `{metric_id}` | {status} | {value} | {interpretation} | {guardrail} |".format(
                metric_id=markdown_cell(row["metric_id"]),
                status=markdown_cell(row.get("status", "")),
                value=markdown_cell(row.get("value")),
                interpretation=markdown_cell(row.get("diagnostic_interpretation", "")),
                guardrail=markdown_cell(row.get("interpretation_guardrail", "")),
            )
        )

    lines.extend(
        [
            "",
            "## Route-Orbit Warnings",
            "",
            "| Warning | Metric key | Severity | Observed | Threshold | Hard gate | Physics authority | Recommended guard action |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    route_warnings = dashboard["route_orbit_warning_rows"]
    if route_warnings:
        for warning in route_warnings:
            lines.append(
                "| `{warning_id}` | `{metric_key}` | {severity} | {observed} | {threshold} | {hard_gate} | {authority} | {action} |".format(
                    warning_id=markdown_cell(warning.get("warning_id", "")),
                    metric_key=markdown_cell(warning.get("metric_key", "")),
                    severity=markdown_cell(warning.get("severity", "")),
                    observed=markdown_cell(warning.get("observed_value")),
                    threshold=markdown_cell(warning.get("threshold")),
                    hard_gate=markdown_cell(warning.get("hard_gate")),
                    authority=markdown_cell(warning.get("physics_claim_authority")),
                    action=markdown_cell(warning.get("recommended_guard_action", "")),
                )
            )
    else:
        lines.append("| none | none | none | none | none | false | false | none |")

    lines.extend(
        [
            "",
            "## AI Methodology Advisory Warnings",
            "",
            "| Warning | Metric | Status | Hard gate | Physics authority | Recommended guard action |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    warnings = dashboard["advisory_warning_rows"]
    if warnings:
        for warning in warnings:
            lines.append(
                "| `{warning_id}` | `{metric_id}` | {status} | {hard_gate} | {authority} | {action} |".format(
                    warning_id=markdown_cell(warning.get("warning_id", "")),
                    metric_id=markdown_cell(warning.get("metric_id", "")),
                    status=markdown_cell(warning.get("status", "")),
                    hard_gate=markdown_cell(warning.get("hard_gate")),
                    authority=markdown_cell(warning.get("physics_claim_authority")),
                    action=markdown_cell(warning.get("recommended_guard_action", "")),
                )
            )
    else:
        lines.append("| none | none | none | false | false | none |")

    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "- Dashboard authority: support-only AI-system diagnostic.",
            "- Physics claim authority: false.",
            "- Benchmark promotion authority: false.",
            "- Gate Chair verdict authority: false.",
            "- Completed derivation authority: false.",
            "- This dashboard does not rank physics truth by workflow activity.",
            "- These metrics do not establish physics truth.",
            "",
            "## Source Basis",
            "",
            f"- Metrics report as-of: `{markdown_cell(dashboard['source_metrics_report'].get('as_of', ''))}`",
            "- Generated source paths:",
        ]
    )
    for path in dashboard["generated_from"]["source_paths"]:
        lines.append(f"  - `{path}`")
    lines.append("")
    return "\n".join(lines)


def canonical_json(dashboard: dict[str, Any]) -> str:
    return json.dumps(dashboard, indent=2, sort_keys=True) + "\n"


def write_outputs(
    dashboard: dict[str, Any],
    repo_root: Path,
    json_output: str,
    markdown_output: str,
    wiki_markdown_output: str,
) -> None:
    json_path = repo_path(repo_root, json_output)
    markdown_path = repo_path(repo_root, markdown_output)
    wiki_markdown_path = repo_path(repo_root, wiki_markdown_output)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    wiki_markdown_path.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_markdown(dashboard)
    json_path.write_text(canonical_json(dashboard), encoding="utf-8")
    markdown_path.write_text(rendered, encoding="utf-8")
    wiki_markdown_path.write_text(rendered, encoding="utf-8")


def check_outputs(
    dashboard: dict[str, Any],
    repo_root: Path,
    json_output: str,
    markdown_output: str,
    wiki_markdown_output: str,
) -> list[str]:
    errors: list[str] = []
    expected_json = canonical_json(dashboard)
    expected_markdown = render_markdown(dashboard)
    json_path = repo_path(repo_root, json_output)
    markdown_path = repo_path(repo_root, markdown_output)
    wiki_markdown_path = repo_path(repo_root, wiki_markdown_output)
    if not json_path.exists():
        errors.append(f"missing JSON dashboard: {json_output}")
    elif json_path.read_text(encoding="utf-8") != expected_json:
        errors.append(f"stale JSON dashboard: {json_output}")
    if not markdown_path.exists():
        errors.append(f"missing Markdown dashboard: {markdown_output}")
    elif markdown_path.read_text(encoding="utf-8") != expected_markdown:
        errors.append(f"stale Markdown dashboard: {markdown_output}")
    if not wiki_markdown_path.exists():
        errors.append(f"missing wiki Markdown dashboard: {wiki_markdown_output}")
    elif wiki_markdown_path.read_text(encoding="utf-8") != expected_markdown:
        errors.append(f"stale wiki Markdown dashboard: {wiki_markdown_output}")
    for phrase in REQUIRED_MARKDOWN_PHRASES:
        if phrase not in expected_markdown:
            errors.append(f"renderer markdown missing required phrase: {phrase}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--json-output", default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--wiki-markdown-output", default=DEFAULT_WIKI_MARKDOWN_PATH)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    dashboard = build_dashboard(repo_root)
    if args.print_json:
        print(canonical_json(dashboard), end="")
    if args.check:
        errors = check_outputs(
            dashboard,
            repo_root,
            args.json_output,
            args.markdown_output,
            args.wiki_markdown_output,
        )
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("AI methodology dashboard freshness check: PASS")
        return 0
    write_outputs(
        dashboard,
        repo_root,
        args.json_output,
        args.markdown_output,
        args.wiki_markdown_output,
    )
    print(
        json.dumps(
            {
                "status": "written",
                "json_path": args.json_output,
                "markdown_path": args.markdown_output,
                "wiki_markdown_path": args.wiki_markdown_output,
                "schema_id": SCHEMA_ID,
                "metric_count": len(dashboard["metric_rows"]),
                "advisory_warning_count": len(dashboard["advisory_warning_rows"]),
                "payload_ratio_metric_count": len(dashboard["payload_ratio_metric_rows"]),
                "route_orbit_warning_count": len(dashboard["route_orbit_warning_rows"]),
                "durable_quality_metric_count": len(
                    dashboard["durable_quality_metric_rows"]
                ),
                "durable_quality_warning_count": len(
                    dashboard["durable_quality_warning_rows"]
                ),
                "support_only": True,
                "no_physics_truth_ranking": True,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
