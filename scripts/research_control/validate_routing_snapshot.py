#!/usr/bin/env python3
"""Validate only the authority surfaces needed for frequent routing.

This validator is intentionally narrower than validate_research_control.py.
It is an operational preflight, not a replacement for full acceptance or
checkpoint validation and not a scientific authority surface.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from .strict_yaml import StrictYamlError, load as load_yaml, load_frontmatter
    from .validate_research_control import ValidationReport
except ImportError:  # pragma: no cover - direct script import path
    from strict_yaml import (
        StrictYamlError,
        load as load_yaml,
        load_frontmatter,
    )
    from validate_research_control import ValidationReport


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = "registries"
CONTROL_DIR = "research_control"
ACTIVE_JOB_STATUSES = {"pending", "active"}
HANDOFF_RE = re.compile(r"handoff-(\d{4})\.yaml$")
ROUTING_GATE_IDS = (
    "program_state",
    "active_task",
    "current_decision",
    "current_job",
    "pending_job_uniqueness",
    "latest_handoff",
    "execution_role",
    "active_frontier",
    "allowlist",
    "protected_human_gate",
)
ACTIVE_FRONTIER_FIELDS = {
    "Active task ID": "active_task_id",
    "Latest handoff ID": "latest_handoff_id",
    "Current status": "current_status",
    "Next recommended action": "next_recommended_action",
}
BIFURCATION_FIELDS = {
    "Latest research task ID": "latest_research_task_id",
    "Latest research handoff ID": "latest_research_handoff_id",
    "Latest research next action": "latest_research_next_action",
    "Latest project-system task ID": "latest_project_system_task_id",
    "Latest project-system status": "latest_project_system_status",
    "Latest project-system sidecar task ID": "latest_project_system_sidecar_task_id",
    "Latest project-system sidecar status": "latest_project_system_sidecar_status",
    "Sidecar supersedes research handoff": "sidecar_supersedes_research_handoff",
    "Next research route source": "next_research_route_source",
}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _bool_text(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value or "").strip().lower()


def _list_text(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [item for item in value.split(";") if item]
    return []


def _normalize(value: object) -> str:
    text = "" if value is None else str(value).strip()
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def _contains_required_phrase(snapshot_value: object, authoritative_value: object) -> bool:
    snapshot_text = _normalize(snapshot_value).rstrip(".")
    authoritative_text = _normalize(authoritative_value).rstrip(".")
    return bool(authoritative_text and authoritative_text in snapshot_text)


@dataclass
class SourceManifest:
    repo_root: Path
    entries: dict[str, str] = field(default_factory=dict)

    def add(self, path: Path) -> None:
        if not path.is_file():
            return
        relative = path.relative_to(self.repo_root).as_posix()
        self.entries[relative] = _sha256_file(path)

    def payload(self) -> list[dict[str, str]]:
        return [
            {"path": path, "sha256": digest}
            for path, digest in sorted(self.entries.items())
        ]


@dataclass
class RoutingEvaluation:
    report: ValidationReport
    payload: dict[str, object]


class GateRecorder:
    def __init__(self, report: ValidationReport) -> None:
        self.report = report
        self.statuses = {gate_id: "PASS" for gate_id in ROUTING_GATE_IDS}
        self.counts = {gate_id: 0 for gate_id in ROUTING_GATE_IDS}

    def fail(self, gate_id: str, message: str) -> None:
        self.statuses[gate_id] = "FAIL"
        self.counts[gate_id] += 1
        self.report.error(f"[{gate_id}] {message}")
        self.report.findings.append(
            {
                "gate_id": gate_id,
                "severity": "blocking",
                "finding_kind": "active_routing_drift",
                "message": message,
            }
        )

    def payload(self) -> list[dict[str, object]]:
        return [
            {
                "gate_id": gate_id,
                "status": self.statuses[gate_id],
                "finding_count": self.counts[gate_id],
            }
            for gate_id in ROUTING_GATE_IDS
        ]


def _read_rows(
    repo_root: Path,
    name: str,
    manifest: SourceManifest,
    gates: GateRecorder,
) -> list[dict[str, str]]:
    path = repo_root / REGISTRY_DIR / name
    if not path.is_file():
        gates.fail("program_state", f"missing registry {REGISTRY_DIR}/{name}")
        return []
    manifest.add(path)
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    except (OSError, csv.Error) as exc:
        gates.fail("program_state", f"cannot read {REGISTRY_DIR}/{name}: {exc}")
        return []


def _rows_by_id(
    rows: list[dict[str, str]],
    key: str,
    *,
    gate_id: str,
    label: str,
    gates: GateRecorder,
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        row_id = row.get(key, "")
        if not row_id:
            gates.fail(gate_id, f"{label} contains a blank {key}")
            continue
        if row_id in result:
            gates.fail(gate_id, f"{label} contains duplicate {key}={row_id}")
            continue
        result[row_id] = row
    return result


def _load_yaml_record(
    repo_root: Path,
    relative_path: str,
    manifest: SourceManifest,
    gates: GateRecorder,
    gate_id: str,
) -> dict[str, Any]:
    path = repo_root / relative_path
    if not path.is_file():
        gates.fail(gate_id, f"missing {relative_path}")
        return {}
    manifest.add(path)
    try:
        value = load_yaml(path)
    except StrictYamlError as exc:
        gates.fail(gate_id, f"{relative_path}: {exc}")
        return {}
    if not isinstance(value, dict):
        gates.fail(gate_id, f"{relative_path} must contain a YAML map")
        return {}
    return value


def _load_frontmatter_record(
    repo_root: Path,
    relative_path: str,
    manifest: SourceManifest,
    gates: GateRecorder,
    gate_id: str,
) -> dict[str, Any]:
    path = repo_root / relative_path
    if not path.is_file():
        gates.fail(gate_id, f"missing {relative_path}")
        return {}
    manifest.add(path)
    try:
        value, _ = load_frontmatter(path)
    except StrictYamlError as exc:
        gates.fail(gate_id, f"{relative_path}: {exc}")
        return {}
    return value if isinstance(value, dict) else {}


def _compare_fields(
    *,
    gate_id: str,
    label: str,
    record: dict[str, Any],
    row: dict[str, str],
    fields: tuple[str, ...],
    gates: GateRecorder,
) -> None:
    for field_name in fields:
        observed = (
            _bool_text(record.get(field_name))
            if field_name == "requires_human_gate"
            else str(record.get(field_name, ""))
        )
        if observed != row.get(field_name, ""):
            gates.fail(
                gate_id,
                f"{label} {field_name} mismatch: record={observed!r} registry={row.get(field_name, '')!r}",
            )


def _frontier_table(text: str, heading: str) -> dict[str, str]:
    lines = text.splitlines()
    try:
        start = next(
            index
            for index, line in enumerate(lines)
            if line.strip() == f"## {heading}"
        )
    except StopIteration:
        return {}
    result: dict[str, str] = {}
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped.startswith("|"):
            continue
        cells = [_normalize(cell) for cell in stripped.strip("|").split("|")]
        if len(cells) >= 2 and cells[0] != "Field" and set(cells[0]) != {"-"}:
            result[cells[0]] = cells[1]
    return result


def _advisory_diagnostics_placeholder() -> dict[str, object]:
    warning = {
        "triggered": False,
        "severity": "none",
        "warning_ids": [],
        "recommended_guard_action": (
            "Advisory route diagnostics are excluded from the narrow blocking preflight."
        ),
        "hard_gate": False,
        "physics_claim_authority": False,
        "advisory_only": True,
        "evidence": {},
    }
    return {
        "status": "excluded_from_narrow_snapshot",
        "source": "deferred advisory diagnostics",
        "warnings_are_advisory_only": True,
        "warning_hard_gates_created": False,
        "physics_claim_authority_created": False,
        "payload_density_warning": dict(warning),
        "route_orbit_warning": dict(warning),
        "same_burden_repetition_warning": dict(warning),
        "gate_ready_without_gate_warning": dict(warning),
        "recommended_guard_action": warning["recommended_guard_action"],
        "diagnostic_warning_count": 0,
        "diagnostic_warning_ids": [],
        "payload_density_metrics": {},
        "route_orbit_risk_metrics": {},
    }


def _dependency_graph_placeholder(
    program_state: dict[str, Any],
    latest: dict[str, object],
    handoff: dict[str, Any],
) -> dict[str, object]:
    distance = handoff.get("distance_to_gr", {})
    if not isinstance(distance, dict):
        distance = {}
    required_next = handoff.get("required_next_packet", {})
    if not isinstance(required_next, dict):
        required_next = {}
    graph_path = "output/research_dependency_graph.json"
    return {
        "status": "excluded_from_narrow_snapshot",
        "authority_note": (
            "Generated dependency graph data is navigational support only and is "
            "not read by the narrow blocking preflight."
        ),
        "source_inspection_required": True,
        "freshness_check_command": (
            ".venv/bin/python scripts/research_control/render_dependency_graph.py --check"
        ),
        "freshness_status": "not_checked_by_narrow_routing_snapshot",
        "active_task": str(program_state.get("active_task_id", "")),
        "latest_handoff": str(latest.get("handoff_id", "")),
        "active_burden": {
            "milestone": str(distance.get("milestone", "none")),
            "burden_id": str(distance.get("burden_id", "none")),
            "status": str(distance.get("status", "unknown")),
        },
        "immediate_upstream_objects": [],
        "accepted_scoped_objects": [],
        "draft_control_objects": [],
        "human_gated_objects": [],
        "blocked_downstream_objects": [],
        "frozen_negative_routes": [],
        "next_recommended_route": str(
            required_next.get("route_label")
            or required_next.get("task_type")
            or latest.get("next_action", "")
        ),
        "graph_path": graph_path,
        "graph_hash": "",
        "graph_path_or_hash": f"{graph_path}#not-read",
    }


def _validate_task(
    task_id: str,
    tasks: dict[str, dict[str, str]],
    repo_root: Path,
    manifest: SourceManifest,
    gates: GateRecorder,
) -> tuple[dict[str, str], dict[str, Any]]:
    row = tasks.get(task_id, {})
    if not row:
        gates.fail("active_task", f"task {task_id!r} is not registered")
        return {}, {}
    record = _load_yaml_record(
        repo_root,
        f"{row.get('task_path', '')}/00_TASK.yaml",
        manifest,
        gates,
        "active_task",
    )
    _compare_fields(
        gate_id="active_task",
        label=f"task {task_id}",
        record=record,
        row=row,
        fields=(
            "task_id",
            "status",
            "current_decision_id",
            "current_job_id",
            "requires_human_gate",
        ),
        gates=gates,
    )
    return row, record


def _validate_decision(
    decision_id: str,
    decisions: dict[str, dict[str, str]],
    repo_root: Path,
    manifest: SourceManifest,
    gates: GateRecorder,
) -> tuple[dict[str, str], dict[str, Any]]:
    row = decisions.get(decision_id, {})
    if not row:
        gates.fail("current_decision", f"decision {decision_id!r} is not registered")
        return {}, {}
    record = _load_frontmatter_record(
        repo_root,
        row.get("decision_path", ""),
        manifest,
        gates,
        "current_decision",
    )
    _compare_fields(
        gate_id="current_decision",
        label=f"decision {decision_id}",
        record=record,
        row=row,
        fields=(
            "decision_id",
            "task_id",
            "selected_role_id",
            "selected_role_version",
            "agent_job_id",
            "status",
            "requires_human_gate",
        ),
        gates=gates,
    )
    return row, record


def _validate_job(
    job_id: str,
    jobs: dict[str, dict[str, str]],
    repo_root: Path,
    manifest: SourceManifest,
    gates: GateRecorder,
) -> tuple[dict[str, str], dict[str, Any]]:
    row = jobs.get(job_id, {})
    if not row:
        gates.fail("current_job", f"job {job_id!r} is not registered")
        return {}, {}
    record = _load_yaml_record(
        repo_root,
        row.get("job_path", ""),
        manifest,
        gates,
        "current_job",
    )
    _compare_fields(
        gate_id="current_job",
        label=f"job {job_id}",
        record=record,
        row=row,
        fields=(
            "job_id",
            "task_id",
            "decision_id",
            "role_id",
            "role_version",
            "status",
            "requires_human_gate",
        ),
        gates=gates,
    )
    if _list_text(record.get("allowed_write_paths")) != _list_text(
        row.get("allowed_write_paths", "")
    ):
        gates.fail("allowlist", f"job {job_id} write allowlist differs from its registry row")
    completion_path = row.get("completion_path", "")
    if completion_path:
        completion = repo_root / completion_path
        if not completion.is_file():
            gates.fail("current_job", f"job {job_id} completion is missing: {completion_path}")
        else:
            manifest.add(completion)
    return row, record


def evaluate(repo_root: Path = REPO_ROOT) -> RoutingEvaluation:
    repo_root = repo_root.resolve()
    report = ValidationReport()
    gates = GateRecorder(report)
    manifest = SourceManifest(repo_root)

    state_path = repo_root / CONTROL_DIR / "program_state.yaml"
    program_state = _load_yaml_record(
        repo_root,
        f"{CONTROL_DIR}/program_state.yaml",
        manifest,
        gates,
        "program_state",
    )
    if "gr_derived" in program_state:
        gates.fail("program_state", "program_state.yaml must not define gr_derived")

    task_rows = _read_rows(
        repo_root, "RESEARCH_TASK_REGISTRY.csv", manifest, gates
    )
    decision_rows = _read_rows(
        repo_root, "DIRECTOR_DECISION_REGISTRY.csv", manifest, gates
    )
    job_rows = _read_rows(repo_root, "AGENT_JOB_REGISTRY.csv", manifest, gates)
    execution_rows = _read_rows(
        repo_root, "ROLE_EXECUTION_REGISTRY.csv", manifest, gates
    )
    role_rows = _read_rows(repo_root, "AGENT_ROLE_REGISTRY.csv", manifest, gates)
    tasks = _rows_by_id(
        task_rows,
        "task_id",
        gate_id="active_task",
        label="RESEARCH_TASK_REGISTRY.csv",
        gates=gates,
    )
    decisions = _rows_by_id(
        decision_rows,
        "decision_id",
        gate_id="current_decision",
        label="DIRECTOR_DECISION_REGISTRY.csv",
        gates=gates,
    )
    jobs = _rows_by_id(
        job_rows,
        "job_id",
        gate_id="current_job",
        label="AGENT_JOB_REGISTRY.csv",
        gates=gates,
    )
    roles = {
        f"{row.get('role_id', '')}@{row.get('version', '')}": row
        for row in role_rows
        if row.get("role_id") and row.get("version")
    }

    active_task_id = str(program_state.get("active_task_id", ""))
    active_task_row, active_task_record = _validate_task(
        active_task_id, tasks, repo_root, manifest, gates
    )
    current_decision_id = active_task_row.get("current_decision_id", "")
    current_job_id = active_task_row.get("current_job_id", "")
    current_decision_row, current_decision_record = _validate_decision(
        current_decision_id, decisions, repo_root, manifest, gates
    )
    current_job_row, current_job_record = _validate_job(
        current_job_id, jobs, repo_root, manifest, gates
    )
    if current_decision_row and current_decision_row.get("task_id") != active_task_id:
        gates.fail(
            "current_decision",
            f"current decision {current_decision_id} does not belong to {active_task_id}",
        )
    if current_job_row and current_job_row.get("task_id") != active_task_id:
        gates.fail(
            "current_job",
            f"current job {current_job_id} does not belong to {active_task_id}",
        )
    if current_job_row and current_job_row.get("decision_id") != current_decision_id:
        gates.fail(
            "current_job",
            f"current job {current_job_id} does not belong to {current_decision_id}",
        )

    waiting_rows = [
        row for row in job_rows if row.get("status") in ACTIVE_JOB_STATUSES
    ]
    if len(waiting_rows) > 1:
        gates.fail(
            "pending_job_uniqueness",
            "multiple pending or active AgentJobs: "
            + ", ".join(sorted(row.get("job_id", "") for row in waiting_rows)),
        )

    selected_tasks: dict[str, dict[str, str]] = {}
    selected_decisions: dict[str, dict[str, str]] = {}
    selected_jobs: dict[str, dict[str, str]] = {}
    selected_task_records: dict[str, dict[str, Any]] = {}
    selected_decision_records: dict[str, dict[str, Any]] = {}
    selected_job_records: dict[str, dict[str, Any]] = {}
    for row in [current_job_row, *waiting_rows]:
        job_id = row.get("job_id", "")
        if not job_id or job_id in selected_jobs:
            continue
        job_row, job_record = _validate_job(
            job_id, jobs, repo_root, manifest, gates
        )
        selected_jobs[job_id] = job_row
        selected_job_records[job_id] = job_record
        task_id = job_row.get("task_id", "")
        decision_id = job_row.get("decision_id", "")
        if task_id and task_id not in selected_tasks:
            task_row, task_record = _validate_task(
                task_id, tasks, repo_root, manifest, gates
            )
            selected_tasks[task_id] = task_row
            selected_task_records[task_id] = task_record
        if decision_id and decision_id not in selected_decisions:
            decision_row, decision_record = _validate_decision(
                decision_id, decisions, repo_root, manifest, gates
            )
            selected_decisions[decision_id] = decision_row
            selected_decision_records[decision_id] = decision_record
        if job_row and selected_tasks.get(task_id, {}).get("current_job_id") != job_id:
            gates.fail(
                "current_job",
                f"job {job_id} is pending or active but task {task_id} does not name it as current_job_id",
            )
        if job_row and selected_decisions.get(decision_id, {}).get("agent_job_id") != job_id:
            gates.fail(
                "current_decision",
                f"job {job_id} is pending or active but decision {decision_id} does not name it",
            )

    selected_tasks.setdefault(active_task_id, active_task_row)
    selected_task_records.setdefault(active_task_id, active_task_record)
    selected_decisions.setdefault(current_decision_id, current_decision_row)
    selected_decision_records.setdefault(current_decision_id, current_decision_record)
    selected_jobs.setdefault(current_job_id, current_job_row)
    selected_job_records.setdefault(current_job_id, current_job_record)

    execution_by_job: dict[str, list[dict[str, str]]] = {}
    for row in execution_rows:
        execution_by_job.setdefault(row.get("agent_job_id", ""), []).append(row)
    protected_sources: list[str] = []
    for job_id, job_row in selected_jobs.items():
        matches = execution_by_job.get(job_id, [])
        if len(matches) != 1:
            gates.fail(
                "execution_role",
                f"job {job_id} requires exactly one execution-role row; found {len(matches)}",
            )
            continue
        execution_row = matches[0]
        execution_record = _load_yaml_record(
            repo_root,
            execution_row.get("record_path", ""),
            manifest,
            gates,
            "execution_role",
        )
        _compare_fields(
            gate_id="execution_role",
            label=f"execution role for {job_id}",
            record=execution_record,
            row=execution_row,
            fields=(
                "execution_role_ref",
                "task_id",
                "agent_job_id",
                "base_role_id",
                "base_role_version",
                "requires_human_gate",
            ),
            gates=gates,
        )
        if str(selected_job_records.get(job_id, {}).get("execution_role_ref", "")) != execution_row.get(
            "execution_role_ref", ""
        ):
            gates.fail(
                "execution_role",
                f"job {job_id} execution_role_ref differs from ROLE_EXECUTION_REGISTRY.csv",
            )
        role_key = (
            f"{execution_row.get('base_role_id', '')}@"
            f"{execution_row.get('base_role_version', '')}"
        )
        role_row = roles.get(role_key, {})
        if not role_row:
            gates.fail("execution_role", f"base role {role_key!r} is not registered")
        else:
            contract = _load_frontmatter_record(
                repo_root,
                role_row.get("role_contract_path", ""),
                manifest,
                gates,
                "execution_role",
            )
            for field_name in ("role_id", "version", "requires_human_gate"):
                observed = (
                    _bool_text(contract.get(field_name))
                    if field_name == "requires_human_gate"
                    else str(contract.get(field_name, ""))
                )
                if observed != role_row.get(field_name, ""):
                    gates.fail(
                        "execution_role",
                        f"base role {role_key} {field_name} differs from its registry row",
                    )
        job_allowlist = _list_text(
            selected_job_records.get(job_id, {}).get("allowed_write_paths")
        )
        execution_allowlist = _list_text(execution_record.get("allowed_write_paths"))
        if execution_allowlist != _list_text(
            execution_row.get("allowed_write_paths", "")
        ):
            gates.fail(
                "allowlist",
                f"execution role for {job_id} differs from its registry allowlist",
            )
        if job_allowlist != execution_allowlist:
            gates.fail(
                "allowlist",
                f"job {job_id} and its execution role have different write allowlists",
            )
        gate_values = {
            "task": _bool_text(
                selected_task_records.get(job_row.get("task_id", ""), {}).get(
                    "requires_human_gate"
                )
            ),
            "decision": _bool_text(
                selected_decision_records.get(job_row.get("decision_id", ""), {}).get(
                    "requires_human_gate"
                )
            ),
            "job": _bool_text(
                selected_job_records.get(job_id, {}).get("requires_human_gate")
            ),
            "execution_role": _bool_text(
                execution_record.get("requires_human_gate")
            ),
            "base_role": role_row.get("requires_human_gate", "false"),
        }
        protected_sources.extend(
            f"{job_id}:{name}" for name, value in gate_values.items() if value == "true"
        )

    handoff_dir = repo_root / CONTROL_DIR / "handoffs"
    candidates: list[tuple[int, Path]] = []
    if not handoff_dir.is_dir():
        gates.fail("latest_handoff", f"missing {CONTROL_DIR}/handoffs")
    else:
        for path in handoff_dir.glob("handoff-*.yaml"):
            match = HANDOFF_RE.fullmatch(path.name)
            if match:
                candidates.append((int(match.group(1)), path))
    latest_handoff_id = str(program_state.get("latest_handoff_id", ""))
    latest_number = -1
    latest_path = handoff_dir / f"{latest_handoff_id}.yaml"
    if not candidates:
        gates.fail("latest_handoff", "no numbered handoff YAML files found")
    else:
        latest_number, observed_latest_path = max(candidates)
        if observed_latest_path.stem != latest_handoff_id:
            gates.fail(
                "latest_handoff",
                f"program state names {latest_handoff_id!r} but latest tracked handoff is {observed_latest_path.stem!r}",
            )
        latest_path = observed_latest_path
    latest_relative = (
        latest_path.relative_to(repo_root).as_posix()
        if latest_path.is_absolute()
        else latest_path.as_posix()
    )
    handoff = _load_yaml_record(
        repo_root, latest_relative, manifest, gates, "latest_handoff"
    )
    markdown_path = latest_path.with_suffix(".md")
    if not markdown_path.is_file():
        gates.fail("latest_handoff", f"missing Markdown mirror for {latest_path.name}")
    else:
        manifest.add(markdown_path)
        if latest_handoff_id not in markdown_path.read_text(encoding="utf-8"):
            gates.fail(
                "latest_handoff",
                f"{markdown_path.relative_to(repo_root).as_posix()} does not identify {latest_handoff_id}",
            )
    if str(handoff.get("handoff_id", "")) != latest_handoff_id:
        gates.fail("latest_handoff", "handoff_id differs from program state")
    if str(handoff.get("task_id", "")) not in tasks:
        gates.fail("latest_handoff", "latest handoff task is not registered")
    if str(handoff.get("job_id", "")) not in jobs:
        gates.fail("latest_handoff", "latest handoff job is not registered")
    if _normalize(handoff.get("next_action")) != _normalize(
        program_state.get("next_recommended_action")
    ):
        gates.fail(
            "latest_handoff",
            "latest handoff next_action differs from program_state next_recommended_action",
        )

    frontier_path = repo_root / CONTROL_DIR / "current_frontier.md"
    if not frontier_path.is_file():
        gates.fail("active_frontier", f"missing {CONTROL_DIR}/current_frontier.md")
    else:
        manifest.add(frontier_path)
        frontier_text = frontier_path.read_text(encoding="utf-8")
        active_frontier = _frontier_table(frontier_text, "Active Research State")
        if not active_frontier:
            gates.fail("active_frontier", "missing Active Research State table")
        for label, field_name in ACTIVE_FRONTIER_FIELDS.items():
            observed = _normalize(active_frontier.get(label, ""))
            expected = _normalize(program_state.get(field_name, ""))
            matches = (
                _contains_required_phrase(observed, expected)
                if field_name == "next_recommended_action"
                else observed == expected
            )
            if not matches:
                gates.fail(
                    "active_frontier",
                    f"{field_name} drift: frontier={observed!r} authority={expected!r}",
                )
        bifurcation = handoff.get("active_state_bifurcation")
        if isinstance(bifurcation, dict):
            frontier_bifurcation = _frontier_table(
                frontier_text, "Active-State Bifurcation"
            )
            if not frontier_bifurcation:
                gates.fail(
                    "active_frontier", "missing Active-State Bifurcation table"
                )
            for label, field_name in BIFURCATION_FIELDS.items():
                observed = _normalize(frontier_bifurcation.get(label, ""))
                expected = _normalize(bifurcation.get(field_name, ""))
                if observed.lower() != expected.lower():
                    gates.fail(
                        "active_frontier",
                        f"{field_name} drift: frontier={observed!r} handoff={expected!r}",
                    )

    latest = {
        "handoff_number": latest_number,
        "handoff_id": latest_handoff_id,
        "yaml_path": latest_relative,
        "markdown_path": (
            markdown_path.relative_to(repo_root).as_posix()
            if markdown_path.is_absolute()
            else markdown_path.as_posix()
        ),
        "task_id": str(handoff.get("task_id", "")),
        "job_id": str(handoff.get("job_id", "")),
        "next_action": str(handoff.get("next_action", "")),
    }
    available_roles = [
        {
            "role_id": row.get("role_id", ""),
            "version": row.get("version", ""),
            "role_kind": row.get("role_kind", ""),
            "authority_level": row.get("authority_level", ""),
            "requires_human_gate": row.get("requires_human_gate", ""),
            "contract_path": row.get("role_contract_path", ""),
        }
        for row in role_rows
        if row.get("status") == "active" or row.get("role_id") == "gate-chair"
    ]
    jobs_waiting = [
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
        for row in waiting_rows
    ]
    manifest_payload = manifest.payload()
    source_fingerprint = _sha256_bytes(
        _canonical_json(manifest_payload).encode("utf-8")
    )
    payload: dict[str, object] = {
        "program_state": program_state,
        "latest": latest,
        "task_rows": selected_tasks,
        "job_rows": selected_jobs,
        "decision_rows": selected_decisions,
        "jobs_waiting": jobs_waiting,
        "available_roles": available_roles,
        "route_orbit_diagnostics": _advisory_diagnostics_placeholder(),
        "dependency_graph_summary": _dependency_graph_placeholder(
            program_state, latest, handoff
        ),
        "required_authority_surfaces": [
            entry["path"] for entry in manifest_payload
        ],
        "source_manifest": manifest_payload,
        "source_fingerprint": source_fingerprint,
        "gate_results": gates.payload(),
        "protected_gate": {
            "requires_human_gate": bool(protected_sources),
            "sources": sorted(protected_sources),
            "physics_claim_authority": False,
        },
        "exclusions": [
            "full historical completion corpus",
            "publication surfaces",
            "memory derivatives",
            "advisory physics-progress metrics",
            "unrelated registries",
            "generated dependency graph payload",
        ],
        "full_acceptance_validator_required": True,
        "full_acceptance_command": (
            ".venv/bin/python scripts/research_control/validate_research_control.py"
        ),
        "authority_boundary": {
            "project_control_only": True,
            "physics_claim_authority": False,
            "checkpoint_authority": False,
        },
    }
    payload["routing_snapshot_fingerprint"] = _sha256_bytes(
        _canonical_json(payload).encode("utf-8")
    )
    _ = state_path
    return RoutingEvaluation(report=report, payload=payload)


def validate_all(*, repo_root: Path = REPO_ROOT) -> ValidationReport:
    """Return the narrow report using the full validator's report type."""

    return evaluate(repo_root).report


def build_routing_snapshot(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    """Build the validated routing payload for the in-process continuation seal."""

    evaluation = evaluate(repo_root)
    if evaluation.report.errors:
        raise ValueError(
            "routing snapshot validation failed: "
            + "; ".join(evaluation.report.errors)
        )
    return evaluation.payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _ = parse_args(argv or sys.argv[1:])
    evaluation = evaluate()
    result = {
        "status": "PASS" if evaluation.report.ok() else "FAIL",
        "errors": evaluation.report.errors,
        "warnings": evaluation.report.warnings,
        "gate_results": evaluation.payload.get("gate_results", []),
        "source_fingerprint": evaluation.payload.get("source_fingerprint", ""),
        "routing_snapshot_fingerprint": evaluation.payload.get(
            "routing_snapshot_fingerprint", ""
        ),
        "source_manifest": evaluation.payload.get("source_manifest", []),
        "authority_boundary": evaluation.payload.get("authority_boundary", {}),
    }
    print(json.dumps(result, indent=2))
    return 0 if evaluation.report.ok() else 1


if __name__ == "__main__":
    raise SystemExit(main())
