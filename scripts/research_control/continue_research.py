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
    from resolve_latest_handoff import resolve_latest
    from strict_yaml import StrictYamlError, load as load_yaml
    from validate_research_control import validate_all
except ImportError:  # pragma: no cover
    from scripts.research_control.resolve_latest_handoff import resolve_latest
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml
    from scripts.research_control.validate_research_control import validate_all


REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM_STATE_PATH = REPO_ROOT / "research_control" / "program_state.yaml"
REGISTRY_DIR = REPO_ROOT / "registries"


STOP_CONDITIONS = [
    "requires_human_gate=true",
    "validation fails",
    "no role fits",
    "selected role needs authority expansion",
    "job would touch paths outside its allowlist",
    "Director creates a planning-only or control-only decision with no execution",
]


TASK_BOUNDARY_POLICY = (
    "The Director normally operates inside the active task. A new task may be "
    "created only when the current task is completed, blocked, human-gated, or "
    "the latest tracked handoff states that the next step is a separate task."
)


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
