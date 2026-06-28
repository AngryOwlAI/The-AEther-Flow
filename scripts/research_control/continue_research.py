#!/usr/bin/env python3
"""Deterministic entry point for research-control continuation setup.

This bootstrap version validates state and reports the next executable boundary.
It does not perform open-ended research reasoning; Codex/Director reasoning must
author DDRs and execute AgentJobs under the tracked contracts.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

try:
    from report_physics_progress_metrics import build_report as build_physics_progress_report
    from resolve_latest_handoff import resolve_latest
    from strict_yaml import StrictYamlError, load as load_yaml
    from validate_research_control import (
        gr_derivation_roadmap_policy,
        loop_control_policy,
        parent_child_decomposition_policy,
        theoretical_continuation_policy,
        validate_all,
    )
except ImportError:  # pragma: no cover
    from scripts.research_control.report_physics_progress_metrics import (
        build_report as build_physics_progress_report,
    )
    from scripts.research_control.resolve_latest_handoff import resolve_latest
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml
    from scripts.research_control.validate_research_control import (
        gr_derivation_roadmap_policy,
        loop_control_policy,
        parent_child_decomposition_policy,
        theoretical_continuation_policy,
        validate_all,
    )


REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM_STATE_PATH = REPO_ROOT / "research_control" / "program_state.yaml"
REGISTRY_DIR = REPO_ROOT / "registries"


STOP_CONDITIONS = [
    "requires_human_gate=true",
    "validation fails",
    "no role fits",
    "selected role needs authority expansion",
    "job would touch paths outside its allowlist",
    "canonical ontology change or other protected authority requires human gate",
]


TASK_BOUNDARY_POLICY = (
    "The Director normally operates inside the active task. A new task may be "
    "created only when the current task is completed, blocked, human-gated, or "
    "the latest tracked handoff states that the next step is a separate task."
)

WARNING_DEFAULT_ACTION = (
    "No payload-density or route-orbit guard action is triggered by the current "
    "diagnostic report."
)
DIAGNOSTIC_WARNING_IDS_BY_FIELD = {
    "payload_density_warning": {
        "low_payload_density",
        "selector_cycles_without_new_payload",
        "distance_delta_without_payload",
    },
    "same_burden_repetition_warning": {
        "same_burden_repetition",
        "same_burden_without_payload",
    },
    "gate_ready_without_gate_warning": {"gate_ready_without_gate"},
}
PAYLOAD_DENSITY_METRIC_KEYS = {
    "tasks_since_last_distance_to_gr_delta",
    "tasks_since_last_burden_discharged",
    "new_payload_items_per_physics_task",
    "new_payload_items_per_cycle",
    "selector_cycles_without_new_payload",
}


def read_csv_registry(name: str) -> list[dict[str, str]]:
    path = REGISTRY_DIR / name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def by_id(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def active_roles() -> list[dict[str, str]]:
    rows = read_csv_registry("AGENT_ROLE_REGISTRY.csv")
    return [
        {
            "role_id": row.get("role_id", ""),
            "version": row.get("version", ""),
            "role_kind": row.get("role_kind", ""),
            "authority_level": row.get("authority_level", ""),
            "requires_human_gate": row.get("requires_human_gate", ""),
            "contract_path": row.get("role_contract_path", ""),
        }
        for row in rows
        if row.get("status") == "active" or row.get("role_id") == "gate-chair"
    ]


def pending_or_active_jobs() -> list[dict[str, str]]:
    rows = read_csv_registry("AGENT_JOB_REGISTRY.csv")
    return [
        {
            "job_id": row.get("job_id", ""),
            "task_id": row.get("task_id", ""),
            "decision_id": row.get("decision_id", ""),
            "role_id": row.get("role_id", ""),
            "role_version": row.get("role_version", ""),
            "job_path": row.get("job_path", ""),
            "requires_human_gate": row.get("requires_human_gate", ""),
            "status": row.get("status", ""),
        }
        for row in rows
        if row.get("status") in {"pending", "active"}
    ]


def authority_surfaces(
    active_task_id: str,
    latest: dict[str, object],
    task_row: dict[str, str] | None,
    job_row: dict[str, str] | None,
) -> list[str]:
    surfaces = [
        "AGENTS.md",
        "research_control/AGENTS.md",
        "research_control/program_state.yaml",
        "registries/AGENT_ROLE_REGISTRY.csv",
        "registries/ROLE_EXECUTION_REGISTRY.csv",
        "registries/DIRECTOR_DECISION_REGISTRY.csv",
        "registries/AGENT_JOB_REGISTRY.csv",
        "registries/RESEARCH_TASK_REGISTRY.csv",
    ]
    if latest.get("yaml_path"):
        surfaces.append(str(latest["yaml_path"]))
    if latest.get("markdown_path"):
        surfaces.append(str(latest["markdown_path"]))
    if active_task_id:
        surfaces.append(f"research_control/tasks/{active_task_id}/00_TASK.yaml")
    if task_row and task_row.get("current_decision_id"):
        decision = by_id(
            read_csv_registry("DIRECTOR_DECISION_REGISTRY.csv"), "decision_id"
        ).get(task_row["current_decision_id"])
        if decision and decision.get("decision_path"):
            surfaces.append(decision["decision_path"])
    if job_row and job_row.get("job_path"):
        surfaces.append(job_row["job_path"])
    return surfaces


def warning_record(
    *,
    triggered: bool,
    warning_ids: list[str],
    recommended_guard_action: str,
    evidence: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "triggered": triggered,
        "severity": "warning" if triggered else "none",
        "warning_ids": warning_ids,
        "recommended_guard_action": recommended_guard_action,
        "hard_gate": False,
        "physics_claim_authority": False,
        "advisory_only": True,
        "evidence": evidence or {},
    }


def triggered_warnings(
    warnings: list[dict[str, object]],
    *,
    warning_ids: set[str],
    metric_keys: set[str] | None = None,
) -> list[dict[str, object]]:
    metric_keys = metric_keys or set()
    matched: list[dict[str, object]] = []
    for warning in warnings:
        warning_id = str(warning.get("warning_id", ""))
        metric_key = str(warning.get("metric_key", ""))
        if warning_id in warning_ids or metric_key in metric_keys:
            matched.append(warning)
    return matched


def compact_guard_action(warnings: list[dict[str, object]]) -> str:
    actions = [
        f"{warning.get('warning_id', 'warning')}: {warning.get('recommended_guard_action', '')}"
        for warning in warnings
        if warning.get("recommended_guard_action")
    ]
    return "; ".join(actions[:3]) if actions else WARNING_DEFAULT_ACTION


def compact_warning_ids(warnings: list[dict[str, object]]) -> list[str]:
    return [str(warning.get("warning_id", "")) for warning in warnings if warning.get("warning_id")]


def route_orbit_diagnostic_context(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    base_record = warning_record(
        triggered=False,
        warning_ids=[],
        recommended_guard_action=WARNING_DEFAULT_ACTION,
    )
    context: dict[str, object] = {
        "status": "pass",
        "source": "scripts/research_control/report_physics_progress_metrics.py",
        "warnings_are_advisory_only": True,
        "warning_hard_gates_created": False,
        "physics_claim_authority_created": False,
        "payload_density_warning": dict(base_record),
        "route_orbit_warning": dict(base_record),
        "same_burden_repetition_warning": dict(base_record),
        "gate_ready_without_gate_warning": dict(base_record),
        "recommended_guard_action": WARNING_DEFAULT_ACTION,
        "diagnostic_warning_count": 0,
        "diagnostic_warning_ids": [],
        "payload_density_metrics": {},
        "route_orbit_risk_metrics": {},
    }
    try:
        report = build_physics_progress_report(repo_root)
    except Exception as exc:  # pragma: no cover - defensive context packet fallback
        context["status"] = "unavailable"
        context["error"] = str(exc)
        context["recommended_guard_action"] = (
            "Metrics diagnostics were unavailable; run "
            "scripts/research_control/report_physics_progress_metrics.py before routing."
        )
        return context

    metrics = report.get("metrics", {}) if isinstance(report, dict) else {}
    payload_density_metrics = metrics.get("payload_density_metrics", {})
    route_orbit_metrics = metrics.get("route_orbit_risk_metrics", {})
    warnings_value = metrics.get("diagnostic_warnings", [])
    warnings = [
        warning
        for warning in warnings_value
        if isinstance(warning, dict)
    ] if isinstance(warnings_value, list) else []
    warning_ids = compact_warning_ids(warnings)
    guard_action = compact_guard_action(warnings)

    payload_warnings = triggered_warnings(
        warnings,
        warning_ids=DIAGNOSTIC_WARNING_IDS_BY_FIELD["payload_density_warning"],
        metric_keys=PAYLOAD_DENSITY_METRIC_KEYS,
    )
    same_burden_warnings = triggered_warnings(
        warnings,
        warning_ids=DIAGNOSTIC_WARNING_IDS_BY_FIELD["same_burden_repetition_warning"],
    )
    gate_ready_warnings = triggered_warnings(
        warnings,
        warning_ids=DIAGNOSTIC_WARNING_IDS_BY_FIELD["gate_ready_without_gate_warning"],
    )

    same_burden_count = (
        route_orbit_metrics.get("same_burden_repetition_count", 0)
        if isinstance(route_orbit_metrics, dict)
        else 0
    )
    if isinstance(same_burden_count, int) and same_burden_count > 4 and not same_burden_warnings:
        same_burden_warnings = [
            {
                "warning_id": "same_burden_repetition",
                "recommended_guard_action": (
                    "Require the next physics packet to name new mathematical payload "
                    "or justify repetition against the active burden."
                ),
            }
        ]

    route_warning_triggered = bool(warnings or same_burden_warnings or gate_ready_warnings)
    context.update(
        {
            "warning_hard_gates_created": any(bool(warning.get("hard_gate")) for warning in warnings),
            "physics_claim_authority_created": any(
                bool(warning.get("physics_claim_authority")) for warning in warnings
            ),
            "recommended_guard_action": guard_action,
            "diagnostic_warning_count": len(warnings),
            "diagnostic_warning_ids": warning_ids,
            "payload_density_metrics": payload_density_metrics if isinstance(payload_density_metrics, dict) else {},
            "route_orbit_risk_metrics": route_orbit_metrics if isinstance(route_orbit_metrics, dict) else {},
            "payload_density_warning": warning_record(
                triggered=bool(payload_warnings),
                warning_ids=compact_warning_ids(payload_warnings),
                recommended_guard_action=compact_guard_action(payload_warnings),
            ),
            "route_orbit_warning": warning_record(
                triggered=route_warning_triggered,
                warning_ids=warning_ids,
                recommended_guard_action=guard_action,
                evidence={
                    "diagnostic_warning_count": len(warnings),
                    "same_burden_repetition_count": same_burden_count,
                },
            ),
            "same_burden_repetition_warning": warning_record(
                triggered=bool(same_burden_warnings),
                warning_ids=compact_warning_ids(same_burden_warnings),
                recommended_guard_action=compact_guard_action(same_burden_warnings),
                evidence={"same_burden_repetition_count": same_burden_count},
            ),
            "gate_ready_without_gate_warning": warning_record(
                triggered=bool(gate_ready_warnings),
                warning_ids=compact_warning_ids(gate_ready_warnings),
                recommended_guard_action=compact_guard_action(gate_ready_warnings),
                evidence={
                    "gate_ready_cycles_without_gate_verdict": (
                        route_orbit_metrics.get("gate_ready_cycles_without_gate_verdict", 0)
                        if isinstance(route_orbit_metrics, dict)
                        else 0
                    ),
                },
            ),
        }
    )
    return context


def continuation_status() -> dict[str, object]:
    report = validate_all()
    if not report.ok():
        return {
            "status": "blocked",
            "boundary": "blocked",
            "reason": "research-control validation failed",
            "validation_errors": report.errors,
            "checkpoint_required_after_execution": False,
        }
    try:
        program_state = load_yaml(PROGRAM_STATE_PATH)
    except StrictYamlError as exc:
        return {
            "status": "blocked",
            "boundary": "blocked",
            "reason": f"program_state parse failed: {exc}",
            "validation_errors": [str(exc)],
            "checkpoint_required_after_execution": False,
        }
    latest = resolve_latest()
    task_rows = by_id(read_csv_registry("RESEARCH_TASK_REGISTRY.csv"), "task_id")
    job_rows = by_id(read_csv_registry("AGENT_JOB_REGISTRY.csv"), "job_id")
    decision_rows = by_id(read_csv_registry("DIRECTOR_DECISION_REGISTRY.csv"), "decision_id")
    active_task_id = str(program_state.get("active_task_id", ""))
    active_task = task_rows.get(active_task_id, {})
    current_decision_id = active_task.get("current_decision_id", "")
    current_job_id = active_task.get("current_job_id", "")
    current_job = job_rows.get(current_job_id, {})
    current_decision = decision_rows.get(current_decision_id, {})
    jobs_waiting = pending_or_active_jobs()
    route_orbit_diagnostics = route_orbit_diagnostic_context(REPO_ROOT)

    boundary = "director_decision_required"
    if active_task.get("requires_human_gate") == "true" or current_decision.get(
        "requires_human_gate"
    ) == "true":
        boundary = "human_gate_required"
    elif jobs_waiting:
        matching = [
            job
            for job in jobs_waiting
            if job["task_id"] == active_task_id
            and job["decision_id"] == current_decision_id
            and (not current_job_id or job["job_id"] == current_job_id)
        ]
        boundary = "existing_agent_job_ready" if len(matching) == 1 else "blocked"
    elif not latest.get("next_action") and str(program_state.get("next_recommended_action", "")).upper() == "NONE":
        boundary = "no_action"

    return {
        "status": "ready",
        "boundary": boundary,
        "active_task_id": program_state.get("active_task_id", ""),
        "latest_handoff_id": latest.get("handoff_id", ""),
        "latest_handoff_path": latest.get("yaml_path", ""),
        "current_decision_id": current_decision_id,
        "current_job_id": current_job_id,
        "current_status": program_state.get("current_status", ""),
        "latest_handoff": latest,
        "next_action": latest.get("next_action", ""),
        "next_recommended_action": program_state.get("next_recommended_action", latest.get("next_action", "")),
        "task_boundary_policy": TASK_BOUNDARY_POLICY,
        "available_roles": active_roles(),
        "pending_or_active_jobs": jobs_waiting,
        "payload_density_warning": route_orbit_diagnostics["payload_density_warning"],
        "route_orbit_warning": route_orbit_diagnostics["route_orbit_warning"],
        "same_burden_repetition_warning": route_orbit_diagnostics[
            "same_burden_repetition_warning"
        ],
        "gate_ready_without_gate_warning": route_orbit_diagnostics[
            "gate_ready_without_gate_warning"
        ],
        "recommended_guard_action": route_orbit_diagnostics["recommended_guard_action"],
        "route_orbit_diagnostics": route_orbit_diagnostics,
        "bridge_or_fail_policy": loop_control_policy(),
        "theoretical_continuation_policy": theoretical_continuation_policy(),
        "parent_child_decomposition_policy": parent_child_decomposition_policy(),
        "gr_derivation_roadmap_policy": gr_derivation_roadmap_policy(),
        "required_authority_surfaces": authority_surfaces(
            active_task_id,
            latest,
            active_task,
            current_job,
        ),
        "stop_conditions": STOP_CONDITIONS,
        "validation_errors": [],
        "checkpoint_required_after_execution": boundary in {
            "director_decision_required",
            "existing_agent_job_ready",
        },
        "execution_boundary": "one bounded AgentJob per invocation",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output. This is the default.")
    parser.add_argument("--summary", action="store_true", help="Emit a human-readable summary.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    status = continuation_status()
    if args.summary:
        print(f"Status: {status['status']}")
        print(f"Boundary: {status.get('boundary', '')}")
        print(f"Active task: {status.get('active_task_id', '')}")
        print(f"Latest handoff: {status.get('latest_handoff_path', '')}")
        print(f"Next recommended action: {status.get('next_recommended_action', '')}")
        if status["status"] == "blocked":
            for error in status.get("validation_errors", []):
                print(f"- {error}")
    else:
        print(json.dumps(status, indent=2))
    return 0 if status["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
