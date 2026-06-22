#!/usr/bin/env python3
"""Resolve the next bounded project-system improvement boundary."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from classify_project_changes import changed_paths_from_git, classify_paths  # noqa: E402
from collect_project_improvement_signals import collect_signals  # noqa: E402
from project_improvement_handoff_validation import read_project_improvement_handoffs  # noqa: E402
from project_signal_types import signal_type_role_map  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
HIGH_PRIORITY_SEVERITIES = {"critical", "high"}
OPEN_SIDECAR_STATUSES = {"open", "active"}
PROTECTED_WRITE_HINT_PREFIXES = (
    "ontology/",
    "legacy_ontology/",
    "manuscripts/",
    "tex/",
    "html/",
    "wiki/",
    "github-facing/",
    "markdown/html-explainer-specs/",
    "markdown/publication-briefs/",
)


STOP_CONDITIONS = [
    "validation fails",
    "required write path is outside the AgentJob allowlist",
    "change would edit physics claims or generated derivatives by hand",
    "project-system action needs a human policy decision",
    "more than one AgentJob would be required",
]


def selected_signal(open_signals: list[dict[str, str]]) -> dict[str, str] | None:
    if not open_signals:
        return None
    return sorted(
        open_signals,
        key=lambda row: (
            SEVERITY_ORDER.get(row.get("severity", "low"), 9),
            row.get("created_at", ""),
            row.get("signal_id", ""),
        ),
    )[0]


def high_priority_signal(open_signals: list[dict[str, str]]) -> dict[str, str] | None:
    return selected_signal(
        [
            signal
            for signal in open_signals
            if signal.get("severity") in HIGH_PRIORITY_SEVERITIES
        ]
    )


def _text(value: Any) -> str:
    return str(value or "").strip()


def active_role_ids(repo_root: Path = REPO_ROOT) -> set[str]:
    path = repo_root / "registries" / "AGENT_ROLE_REGISTRY.csv"
    if not path.exists():
        return set()
    with path.open(newline="", encoding="utf-8") as handle:
        return {
            row.get("role_id", "")
            for row in csv.DictReader(handle)
            if row.get("role_id") and row.get("status") == "active"
        }


def _safe_write_hint_errors(hints: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(hints, list):
        return ["allowed_write_paths_hint is not a list"]
    for hint in hints:
        hint_text = _text(hint)
        if not hint_text:
            continue
        path_text = hint_text.replace("**", "x").replace("*", "x")
        path = Path(path_text)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            errors.append(f"invalid write-path hint: {hint_text}")
        if hint_text.startswith(PROTECTED_WRITE_HINT_PREFIXES):
            errors.append(f"protected write-path hint: {hint_text}")
    return errors


def _solution_plan_summary(plan: Any, active_roles: set[str]) -> dict[str, object]:
    if not isinstance(plan, dict):
        return {
            "present": False,
            "status": "absent",
            "implementation_role": "",
            "objective": "",
            "routing_status": "absent",
            "routing_blockers": [],
        }
    present = plan.get("present") is True
    status = _text(plan.get("status")) or "absent"
    implementation_role = _text(plan.get("implementation_role"))
    objective = _text(plan.get("objective"))
    blockers: list[str] = []
    routing_status = "absent"
    if present or status != "absent":
        routing_status = "not_ready"
    if status == "ready_to_implement":
        if not implementation_role:
            blockers.append("missing implementation_role")
        elif implementation_role not in active_roles:
            blockers.append(f"implementation_role is not active: {implementation_role}")
        if not objective:
            blockers.append("missing objective")
        blockers.extend(_safe_write_hint_errors(plan.get("allowed_write_paths_hint", [])))
        routing_status = "ready" if not blockers else "blocked"
    return {
        "present": present,
        "status": status,
        "implementation_role": implementation_role,
        "objective": objective,
        "routing_status": routing_status,
        "routing_blockers": blockers,
    }


def _sidecar_signal_ids(data: dict[str, Any]) -> list[str]:
    summary = data.get("signal_summary", {})
    if not isinstance(summary, dict):
        return []
    signal_ids = summary.get("signal_ids", [])
    if not isinstance(signal_ids, list):
        return []
    return [_text(signal_id) for signal_id in signal_ids if _text(signal_id)]


def _sidecar_summary(
    record: dict[str, Any],
    active_roles: set[str],
    repo_root: Path,
) -> dict[str, object]:
    data = record.get("data", {})
    source = data.get("source", {}) if isinstance(data.get("source"), dict) else {}
    summary = data.get("signal_summary", {}) if isinstance(data.get("signal_summary"), dict) else {}
    return {
        "improvement_handoff_id": _text(data.get("improvement_handoff_id")),
        "path": record.get("relative_path", ""),
        "markdown_path": record.get("markdown_path").relative_to(repo_root).as_posix()
        if record.get("markdown_path")
        else "",
        "status": _text(data.get("status")),
        "source_task_id": _text(source.get("task_id")),
        "source_job_id": _text(source.get("job_id")),
        "source_completion_path": _text(source.get("completion_path")),
        "regular_handoff_id": _text(source.get("regular_handoff_id")),
        "regular_handoff_yaml_path": _text(source.get("regular_handoff_yaml_path")),
        "signal_ids": _sidecar_signal_ids(data),
        "selected_signal_id": _text(summary.get("selected_signal_id")),
        "highest_severity": _text(summary.get("highest_severity")),
        "solution_plan": _solution_plan_summary(data.get("solution_plan"), active_roles),
    }


def open_improvement_handoffs(repo_root: Path = REPO_ROOT) -> tuple[list[dict[str, object]], list[str]]:
    active_roles = active_role_ids(repo_root)
    records, errors = read_project_improvement_handoffs(repo_root)
    summaries = [
        _sidecar_summary(record, active_roles, repo_root)
        for record in records
        if _text(record.get("data", {}).get("status")) in OPEN_SIDECAR_STATUSES
    ]
    return sorted(
        summaries,
        key=lambda row: (
            SEVERITY_ORDER.get(str(row.get("highest_severity", "")), 99),
            str(row.get("improvement_handoff_id", "")),
        ),
    ), errors


def sidecar_for_signal(
    signal_id: str,
    sidecars: list[dict[str, object]],
) -> dict[str, object]:
    for sidecar in sidecars:
        if signal_id in sidecar.get("signal_ids", []):
            return sidecar
    return {}


def resolve_project_improvement(paths: list[str] | None = None) -> dict[str, object]:
    if paths is None:
        paths = changed_paths_from_git()
    classification = classify_paths(paths)
    signals = collect_signals()
    open_signals = signals.get("open_signals", [])
    open_sidecars, sidecar_read_errors = open_improvement_handoffs(REPO_ROOT)
    urgent_signal = high_priority_signal(open_signals)
    backlog_signal = selected_signal(open_signals)
    role_map = signal_type_role_map()
    chosen_signal: dict[str, str] | None = None
    selected_sidecar: dict[str, object] = {}
    selected_signal_source = "none"
    solution_plan: dict[str, object] = _solution_plan_summary({}, active_role_ids(REPO_ROOT))

    boundary = "no_action"
    recommended_role = ""
    reason = "no open project-improvement signal and no current Git change requires action"

    if urgent_signal:
        chosen_signal = urgent_signal
        boundary = "project_improvement_signal_ready"
        recommended_role = chosen_signal.get("recommended_role") or role_map.get(
            chosen_signal.get("signal_type", ""), "project-system-director"
        )
        selected_signal_source = "signal_registry"
        reason = (
            f"high-priority open signal {chosen_signal.get('signal_id', '')} "
            "requires one bounded AgentJob"
        )
    elif classification.get("docs_impact_required"):
        recommended_role = str(classification.get("recommended_role", "documentation-curator"))
        if recommended_role == "documentation-curator":
            boundary = "documentation_curator_required"
            reason = "current Git change has explanatory documentation impact"
        else:
            boundary = "project_system_agent_job_required"
            reason = "current Git change has documentation impact for a non-documentation control surface"
        selected_signal_source = "git_change"
    elif classification.get("project_system_improvement_required"):
        boundary = "project_system_agent_job_required"
        recommended_role = classification.get("recommended_role", "validator-engineer")
        reason = "current Git change affects project-system machinery"
        selected_signal_source = "git_change"
    elif backlog_signal:
        chosen_signal = backlog_signal
        boundary = "project_improvement_signal_ready"
        recommended_role = chosen_signal.get("recommended_role") or role_map.get(
            chosen_signal.get("signal_type", ""), "project-system-director"
        )
        selected_signal_source = "signal_registry"
        reason = f"open backlog signal {chosen_signal.get('signal_id', '')} requires one bounded AgentJob"

    if chosen_signal:
        selected_sidecar = sidecar_for_signal(chosen_signal.get("signal_id", ""), open_sidecars)
        if selected_sidecar:
            selected_signal_source = "improvement_handoff"
            solution_plan = selected_sidecar.get("solution_plan", solution_plan)  # type: ignore[assignment]
            if solution_plan.get("routing_status") == "ready":
                recommended_role = str(solution_plan.get("implementation_role") or recommended_role)
                reason = (
                    f"open signal {chosen_signal.get('signal_id', '')} has executable "
                    f"sidecar plan {selected_sidecar.get('improvement_handoff_id', '')}"
                )
            else:
                recommended_role = "project-system-director"
                reason = (
                    f"open signal {chosen_signal.get('signal_id', '')} has sidecar "
                    f"{selected_sidecar.get('improvement_handoff_id', '')} requiring "
                    "Project-System Director conversion or rejection"
                )

    return {
        "status": "ready",
        "boundary": boundary,
        "reason": reason,
        "resolver_is_advisory": True,
        "hard_checkpoint_gate": False,
        "recommended_skill": "improve-project-system" if boundary != "no_action" else "",
        "recommended_role": recommended_role,
        "selected_signal": chosen_signal or {},
        "selected_signal_source": selected_signal_source,
        "selected_improvement_handoff": selected_sidecar,
        "open_improvement_handoffs": open_sidecars,
        "improvement_handoff_read_errors": sidecar_read_errors,
        "solution_plan": solution_plan,
        "open_signals": open_signals,
        "change_classification": classification,
        "required_authority_surfaces": [
            "AGENTS.md",
            "research_control/AGENTS.md",
            "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv",
            "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv",
            "registries/AGENT_ROLE_REGISTRY.csv",
            ".agents/roles/research_ops/documentation-curator.v0.1.0.md",
            ".agents/roles/research_ops/project-control-maintainer.v0.1.0.md",
            ".codex/skills/improve-project-system/SKILL.md",
        ],
        "stop_conditions": STOP_CONDITIONS,
        "checkpoint_required_after_execution": boundary != "no_action",
        "checkpoint_gate_source": "validators",
        "execution_boundary": "one bounded AgentJob per invocation",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON. This is the default.")
    parser.add_argument("--paths", nargs="*", help="Resolve against explicit paths instead of Git state.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    print(json.dumps(resolve_project_improvement(args.paths), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
