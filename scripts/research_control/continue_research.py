#!/usr/bin/env python3
"""Deterministic entry point for research-control continuation setup.

This bootstrap version validates state and reports the next executable boundary.
It does not perform open-ended research reasoning; Codex/Director reasoning must
author DDRs and execute AgentJobs under the tracked contracts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from report_physics_progress_metrics import build_report as build_physics_progress_report
    from resolve_latest_handoff import resolve_latest
    from strict_yaml import StrictYamlError, load as load_yaml
    from validate_routing_snapshot import build_routing_snapshot, validate_all
    from validate_research_control import (
        ValidationReport,
        gr_derivation_roadmap_policy,
        loop_control_policy,
        parent_child_decomposition_policy,
        theoretical_continuation_policy,
    )
except ImportError:  # pragma: no cover
    from scripts.research_control.report_physics_progress_metrics import (
        build_report as build_physics_progress_report,
    )
    from scripts.research_control.resolve_latest_handoff import resolve_latest
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml
    from scripts.research_control.validate_routing_snapshot import (
        build_routing_snapshot,
        validate_all,
    )
    from scripts.research_control.validate_research_control import (
        ValidationReport,
        gr_derivation_roadmap_policy,
        loop_control_policy,
        parent_child_decomposition_policy,
        theoretical_continuation_policy,
    )


REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM_STATE_PATH = REPO_ROOT / "research_control" / "program_state.yaml"
REGISTRY_DIR = REPO_ROOT / "registries"
DEPENDENCY_GRAPH_JSON_PATH = REPO_ROOT / "output" / "research_dependency_graph.json"


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
GRAPH_SUMMARY_LIMIT = 8
CONTINUATION_INPUT_SCHEMAS = {
    "validation_receipt": "continuation_validation_receipt.v1",
    "routing_snapshot": "continuation_routing_snapshot.v1",
}
CONTINUATION_INPUT_AUTHORITY = {
    "project_control_only": True,
    "physics_claim_authority": False,
}


@dataclass(frozen=True)
class ValidatedContinuationInput:
    """Fingerprint-checked in-process input; no CLI or serialized input path exists."""

    kind: str
    payload_json: str
    sha256: str


def _canonical_json(value: dict[str, object]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _seal_continuation_input(
    kind: str,
    payload: dict[str, object],
) -> ValidatedContinuationInput:
    if kind not in CONTINUATION_INPUT_SCHEMAS:
        raise ValueError(f"unknown continuation input kind: {kind}")
    sealed_payload = {
        **payload,
        "schema_id": CONTINUATION_INPUT_SCHEMAS[kind],
        "authority_boundary": CONTINUATION_INPUT_AUTHORITY,
    }
    payload_json = _canonical_json(sealed_payload)
    return ValidatedContinuationInput(
        kind=kind,
        payload_json=payload_json,
        sha256=hashlib.sha256(payload_json.encode("utf-8")).hexdigest(),
    )


def _open_continuation_input(
    value: ValidatedContinuationInput,
    expected_kind: str,
) -> dict[str, object]:
    if type(value) is not ValidatedContinuationInput or value.kind != expected_kind:
        raise ValueError(f"expected typed {expected_kind}")
    if not isinstance(value.payload_json, str) or not isinstance(value.sha256, str):
        raise ValueError(f"{expected_kind} envelope fields must be strings")
    observed = hashlib.sha256(value.payload_json.encode("utf-8")).hexdigest()
    if observed != value.sha256:
        raise ValueError(f"{expected_kind} fingerprint mismatch")
    payload = json.loads(value.payload_json)
    if (
        not isinstance(payload, dict)
        or payload.get("schema_id") != CONTINUATION_INPUT_SCHEMAS[expected_kind]
        or payload.get("authority_boundary") != CONTINUATION_INPUT_AUTHORITY
    ):
        raise ValueError(f"{expected_kind} schema or authority boundary mismatch")
    if expected_kind == "validation_receipt":
        if payload.get("status") not in {"PASS", "FAIL"}:
            raise ValueError("validation_receipt status must be PASS or FAIL")
        for field_name in ("errors", "warnings"):
            field_value = payload.get(field_name)
            if (
                not isinstance(field_value, list)
                or any(not isinstance(item, str) for item in field_value)
            ):
                raise ValueError(
                    f"validation_receipt {field_name} must be a list of strings"
                )
    else:
        routing_field_types = {
            "program_state": dict,
            "latest": dict,
            "task_rows": dict,
            "job_rows": dict,
            "decision_rows": dict,
            "jobs_waiting": list,
            "available_roles": list,
            "route_orbit_diagnostics": dict,
            "dependency_graph_summary": dict,
            "required_authority_surfaces": list,
        }
        for field_name, field_type in routing_field_types.items():
            if not isinstance(payload.get(field_name), field_type):
                raise ValueError(
                    f"routing_snapshot {field_name} must be {field_type.__name__}"
                )
        for row_map_name in ("task_rows", "job_rows", "decision_rows"):
            if any(
                not isinstance(row, dict)
                for row in payload[row_map_name].values()
            ):
                raise ValueError(
                    f"routing_snapshot {row_map_name} values must be objects"
                )
        for row in payload["jobs_waiting"]:
            if not isinstance(row, dict) or any(
                not isinstance(row.get(field_name), str)
                for field_name in ("job_id", "task_id", "decision_id")
            ):
                raise ValueError(
                    "routing_snapshot jobs_waiting entries require string "
                    "job_id, task_id, and decision_id"
                )
        diagnostics = payload["route_orbit_diagnostics"]
        for field_name in (
            "payload_density_warning",
            "route_orbit_warning",
            "same_burden_repetition_warning",
            "gate_ready_without_gate_warning",
        ):
            if not isinstance(diagnostics.get(field_name), dict):
                raise ValueError(
                    f"routing_snapshot route_orbit_diagnostics.{field_name} "
                    "must be object"
                )
        if not isinstance(diagnostics.get("recommended_guard_action"), str):
            raise ValueError(
                "routing_snapshot route_orbit_diagnostics."
                "recommended_guard_action must be string"
            )
    return payload


def make_validation_receipt(report: ValidationReport) -> ValidatedContinuationInput:
    if type(report) is not ValidationReport:
        raise ValueError("validation receipt requires ValidationReport")
    errors = [str(error) for error in report.errors]
    warnings = [str(warning) for warning in report.warnings]
    return _seal_continuation_input(
        "validation_receipt",
        {"status": "PASS" if not errors else "FAIL", "errors": errors, "warnings": warnings},
    )


def make_routing_snapshot(payload: dict[str, object]) -> ValidatedContinuationInput:
    return _seal_continuation_input("routing_snapshot", payload)


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


def file_sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_node(node: dict[str, object]) -> dict[str, object]:
    return {
        "node_id": str(node.get("node_id", "")),
        "label": str(node.get("label", "")),
        "node_class": str(node.get("node_class", "")),
        "state_label": str(node.get("state_label", "")),
        "source_path": str(node.get("source_path", "")),
    }


def first_nodes(
    nodes: list[dict[str, object]],
    *,
    state_labels: set[str] | None = None,
    node_classes: set[str] | None = None,
    label_prefix: str | None = None,
    limit: int = GRAPH_SUMMARY_LIMIT,
) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    for node in nodes:
        state_label = str(node.get("state_label", ""))
        node_class = str(node.get("node_class", ""))
        label = str(node.get("label", ""))
        if state_labels is not None and state_label not in state_labels:
            continue
        if node_classes is not None and node_class not in node_classes:
            continue
        if label_prefix is not None and not label.lower().startswith(label_prefix.lower()):
            continue
        selected.append(compact_node(node))
        if len(selected) >= limit:
            break
    return selected


def read_handoff_payload(latest: dict[str, object]) -> dict[str, object]:
    yaml_path = str(latest.get("yaml_path", ""))
    if not yaml_path:
        return {}
    path = REPO_ROOT / yaml_path
    if not path.exists():
        return {}
    try:
        data = load_yaml(path)
    except StrictYamlError:
        return {}
    return data if isinstance(data, dict) else {}


def dependency_graph_summary(
    program_state: dict[str, object],
    latest: dict[str, object],
    *,
    graph_path: Path = DEPENDENCY_GRAPH_JSON_PATH,
) -> dict[str, object]:
    graph_relpath = graph_path.relative_to(REPO_ROOT).as_posix()
    handoff_payload = read_handoff_payload(latest)
    distance_to_gr = handoff_payload.get("distance_to_gr", {})
    if not isinstance(distance_to_gr, dict):
        distance_to_gr = {}
    required_next_packet = handoff_payload.get("required_next_packet", {})
    if not isinstance(required_next_packet, dict):
        required_next_packet = {}
    active_task_id = str(program_state.get("active_task_id", ""))
    latest_handoff_id = str(latest.get("handoff_id", ""))
    base_summary: dict[str, object] = {
        "status": "missing",
        "authority_note": (
            "Generated dependency graph data is navigational support only. "
            "It does not replace canonical source inspection and cannot promote claims."
        ),
        "source_inspection_required": True,
        "freshness_check_command": ".venv/bin/python scripts/research_control/render_dependency_graph.py --check",
        "freshness_status": "not_checked_by_continue_research",
        "active_task": active_task_id,
        "latest_handoff": latest_handoff_id,
        "active_burden": {
            "milestone": str(distance_to_gr.get("milestone", "none")),
            "burden_id": str(distance_to_gr.get("burden_id", "none")),
            "status": str(distance_to_gr.get("status", "unknown")),
        },
        "immediate_upstream_objects": [],
        "accepted_scoped_objects": [],
        "draft_control_objects": [],
        "human_gated_objects": [],
        "blocked_downstream_objects": [],
        "frozen_negative_routes": [],
        "next_recommended_route": str(
            required_next_packet.get("route_label")
            or required_next_packet.get("task_type")
            or latest.get("next_action", "")
        ),
        "graph_path": graph_relpath,
        "graph_hash": file_sha256(graph_path),
        "graph_path_or_hash": f"{graph_relpath}#{file_sha256(graph_path)}",
    }
    if not graph_path.exists():
        return base_summary
    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        base_summary["status"] = "unreadable"
        base_summary["error"] = str(exc)
        return base_summary
    nodes_value = graph.get("nodes", [])
    edges_value = graph.get("edges", [])
    nodes = [node for node in nodes_value if isinstance(node, dict)] if isinstance(nodes_value, list) else []
    edges = [edge for edge in edges_value if isinstance(edge, dict)] if isinstance(edges_value, list) else []
    nodes_by_id = {str(node.get("node_id", "")): node for node in nodes}
    active_task_node = f"task:{active_task_id}"
    upstream_nodes = []
    for edge in edges:
        if str(edge.get("target_id", "")) != active_task_node:
            continue
        source_node = nodes_by_id.get(str(edge.get("source_id", "")))
        if source_node:
            upstream_nodes.append(compact_node(source_node))
        if len(upstream_nodes) >= GRAPH_SUMMARY_LIMIT:
            break
    base_summary.update(
        {
            "status": "available",
            "schema_id": str(graph.get("schema_id", "")),
            "source_fingerprint": str(graph.get("source_fingerprint", "")),
            "generated_at": str(graph.get("generated_at", "")),
            "route_continuity_status": (
                "matches_latest_handoff"
                if isinstance(graph.get("route_continuity"), dict)
                and isinstance(graph["route_continuity"].get("latest_handoff"), dict)
                and graph["route_continuity"]["latest_handoff"].get("handoff_id") == latest_handoff_id
                else "inspect_graph_freshness"
            ),
            "immediate_upstream_objects": upstream_nodes,
            "accepted_scoped_objects": first_nodes(nodes, state_labels={"accepted_scoped"}),
            "draft_control_objects": first_nodes(nodes, state_labels={"draft_control", "proposal_only"}),
            "human_gated_objects": first_nodes(nodes, state_labels={"human_gated"}),
            "blocked_downstream_objects": first_nodes(
                nodes,
                node_classes={"blocked_burden"},
                label_prefix="Blocked",
            ),
            "frozen_negative_routes": first_nodes(nodes, state_labels={"frozen_negative"}),
        }
    )
    return base_summary


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


def live_routing_snapshot() -> ValidatedContinuationInput:
    return make_routing_snapshot(build_routing_snapshot(REPO_ROOT))


def continuation_status(
    *,
    validation_result: ValidatedContinuationInput | None = None,
    routing_snapshot: ValidatedContinuationInput | None = None,
) -> dict[str, object]:
    validation_injected = validation_result is not None
    if validation_result is None:
        validation_result = make_validation_receipt(validate_all())
    try:
        validation_payload = _open_continuation_input(
            validation_result,
            "validation_receipt",
        )
    except (ValueError, json.JSONDecodeError) as exc:
        return {
            "status": "blocked",
            "boundary": "blocked",
            "reason": "validation receipt integrity failed",
            "validation_errors": [str(exc)],
            "checkpoint_required_after_execution": False,
        }
    if validation_payload.get("status") != "PASS":
        return {
            "status": "blocked",
            "boundary": "blocked",
            "reason": "research-control validation failed",
            "validation_errors": validation_payload.get("errors", []),
            "checkpoint_required_after_execution": False,
        }
    routing_injected = routing_snapshot is not None
    try:
        if routing_snapshot is None:
            routing_snapshot = live_routing_snapshot()
        routing_payload = _open_continuation_input(routing_snapshot, "routing_snapshot")
    except (StrictYamlError, ValueError, json.JSONDecodeError) as exc:
        return {
            "status": "blocked",
            "boundary": "blocked",
            "reason": f"routing snapshot integrity failed: {exc}",
            "validation_errors": [str(exc)],
            "checkpoint_required_after_execution": False,
        }
    program_state = routing_payload["program_state"]
    latest = routing_payload["latest"]
    task_rows = routing_payload["task_rows"]
    job_rows = routing_payload["job_rows"]
    decision_rows = routing_payload["decision_rows"]
    active_task_id = str(program_state.get("active_task_id", ""))
    active_task = task_rows.get(active_task_id, {})
    current_decision_id = active_task.get("current_decision_id", "")
    current_job_id = active_task.get("current_job_id", "")
    current_job = job_rows.get(current_job_id, {})
    current_decision = decision_rows.get(current_decision_id, {})
    jobs_waiting = routing_payload["jobs_waiting"]
    route_orbit_diagnostics = routing_payload["route_orbit_diagnostics"]
    graph_summary = routing_payload["dependency_graph_summary"]

    boundary = "director_decision_required"
    protected_gate = routing_payload.get("protected_gate", {})
    protected_gate_required = (
        isinstance(protected_gate, dict)
        and protected_gate.get("requires_human_gate") is True
    )
    if (
        active_task.get("requires_human_gate") == "true"
        or current_decision.get("requires_human_gate") == "true"
        or current_job.get("requires_human_gate") == "true"
        or protected_gate_required
    ):
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
        "available_roles": routing_payload["available_roles"],
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
        "dependency_graph_summary": graph_summary,
        "bridge_or_fail_policy": loop_control_policy(),
        "theoretical_continuation_policy": theoretical_continuation_policy(),
        "parent_child_decomposition_policy": parent_child_decomposition_policy(),
        "gr_derivation_roadmap_policy": gr_derivation_roadmap_policy(),
        "required_authority_surfaces": routing_payload["required_authority_surfaces"],
        "stop_conditions": STOP_CONDITIONS,
        "validation_errors": [],
        "input_receipts": {
            "validation": {
                "injected": validation_injected,
                "status": validation_payload["status"],
                "sha256": validation_result.sha256,
                "physics_claim_authority": False,
            },
            "routing": {
                "injected": routing_injected,
                "sha256": routing_snapshot.sha256,
                "physics_claim_authority": False,
            },
        },
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
        graph_summary = status.get("dependency_graph_summary", {})
        if isinstance(graph_summary, dict):
            print(
                "Dependency graph: "
                f"{graph_summary.get('status', '')}; "
                f"{graph_summary.get('graph_path_or_hash', '')}; "
                "navigational support only"
            )
        if status["status"] == "blocked":
            for error in status.get("validation_errors", []):
                print(f"- {error}")
    else:
        print(json.dumps(status, indent=2))
    return 0 if status["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
