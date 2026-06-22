#!/usr/bin/env python3
"""Generate deterministic project-improvement handoff sidecars."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from project_signal_types import signal_type_names  # noqa: E402
from resolve_project_improvement import SEVERITY_ORDER  # noqa: E402
from strict_yaml import StrictYamlError, load as load_yaml, loads as load_yaml_text  # noqa: E402


OUTPUT_DIR = Path("research_control/project_improvement_handoffs")
SIGNAL_REGISTRY = Path("registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv")
OPEN_STATUSES = {"open", "pending", "active"}
SUCCESS_TERMINAL_STATUSES = {"resolved", "completed", "closed"}
ALLOWED_SIGNAL_SEVERITIES = set(SEVERITY_ORDER)
PROTECTED_PATH_PREFIXES = (
    "ontology/",
    "legacy_ontology/",
    "manuscripts/",
    "tex/",
    "html/",
    "wiki/",
)
SIDE_CAR_FIELD_ORDER = [
    "improvement_handoff_id",
    "created_at",
    "status",
    "source",
    "normal_research_continuation",
    "project_boundary",
    "signal_summary",
    "issues",
    "solution_plan",
    "resolution",
    "notes",
]
PROJECT_IMPROVEMENT_BRIDGE_FIELD = "project_improvement_bridge"
SOURCE_BRIDGE_STATUSES = {"not_required", "required_pending_generation", "generated", "blocked"}
TOP_LEVEL_KEY_RE = re.compile(r"^[A-Za-z0-9_]+:")


@dataclass(frozen=True)
class SourceRecord:
    path: Path
    relative_path: str
    data: dict[str, Any]
    source_type: str


def _text(value: Any) -> str:
    return str(value or "").strip()


def _repo_path(repo_root: Path, path_text: str) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        path = repo_root / path
    try:
        path.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"{path_text}: path is outside repository root") from exc
    return path


def _relative(repo_root: Path, path: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def read_signal_registry(repo_root: Path) -> dict[str, dict[str, str]]:
    path = repo_root / SIGNAL_REGISTRY
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {
            row.get("signal_id", ""): {key: value or "" for key, value in row.items()}
            for row in csv.DictReader(handle)
            if row.get("signal_id")
        }


def _is_blank_signal(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    signal_fields = (
        "signal_id",
        "signal_type",
        "severity",
        "evidence",
        "evidence_path",
        "recommended_skill",
        "recommended_role",
        "notes",
    )
    return not any(_text(value.get(field)) for field in signal_fields)


def _source_record(
    repo_root: Path,
    path_text: str | None,
    source_type: str,
) -> SourceRecord | None:
    if not path_text:
        return None
    path = _repo_path(repo_root, path_text)
    data = load_yaml(path)
    return SourceRecord(
        path=path,
        relative_path=_relative(repo_root, path),
        data=data,
        source_type=source_type,
    )


def _source_timestamp(*sources: SourceRecord | None) -> str:
    for source in sources:
        if not source:
            continue
        for field_name in ("completed_at", "created_at", "updated_at"):
            value = _text(source.data.get(field_name))
            if value:
                return value
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _source_task_id(completion: SourceRecord | None, handoff: SourceRecord | None) -> str:
    for source in (completion, handoff):
        if source:
            task_id = _text(source.data.get("task_id"))
            if task_id:
                return task_id
    return ""


def _default_handoff_id(task_id: str, created_at: str) -> str:
    if task_id.startswith("RT-"):
        parts = task_id.split("-")
        if len(parts) >= 3 and parts[1].isdigit() and parts[2].isdigit():
            return f"improve-project-handoff_{parts[1]}_{int(parts[2]):03d}"
    date_part = created_at[:10].replace("-", "")
    return f"improve-project-handoff_{date_part}_001"


def _extract_signals(source: SourceRecord | None, errors: list[str]) -> list[dict[str, Any]]:
    if not source:
        return []
    signals = source.data.get("project_improvement_signals", [])
    if signals in ("", None):
        return []
    if not isinstance(signals, list):
        errors.append(f"{source.relative_path}: project_improvement_signals must be a list")
        return []
    records: list[dict[str, Any]] = []
    for index, signal in enumerate(signals, start=1):
        if _is_blank_signal(signal):
            continue
        if not isinstance(signal, dict):
            errors.append(
                f"{source.relative_path}: project_improvement_signals[{index}] must be a map"
            )
            continue
        signal_id = _text(signal.get("signal_id"))
        if not signal_id:
            errors.append(
                f"{source.relative_path}: project_improvement_signals[{index}] missing signal_id"
            )
            continue
        records.append(
            {
                "source_path": source.relative_path,
                "source_type": source.source_type,
                "index": index,
                "signal": signal,
            }
        )
    return records


def _dedupe_signals(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for record in records:
        signal_id = _text(record["signal"].get("signal_id"))
        if signal_id not in by_id:
            by_id[signal_id] = {
                "signal_id": signal_id,
                "signal": record["signal"],
                "source_paths": [record["source_path"]],
            }
            continue
        if record["source_path"] not in by_id[signal_id]["source_paths"]:
            by_id[signal_id]["source_paths"].append(record["source_path"])
        existing = by_id[signal_id]["signal"]
        for field_name, value in record["signal"].items():
            if _text(value) and not _text(existing.get(field_name)):
                existing[field_name] = value
    return list(by_id.values())


def _validate_and_enrich_signals(
    repo_root: Path,
    records: list[dict[str, Any]],
    errors: list[str],
) -> list[dict[str, Any]]:
    registry_rows = read_signal_registry(repo_root)
    active_types = signal_type_names(repo_root)
    enriched: list[dict[str, Any]] = []
    for record in records:
        signal_id = record["signal_id"]
        signal = record["signal"]
        registry_row = registry_rows.get(signal_id)
        if not registry_row:
            errors.append(f"{signal_id}: missing {SIGNAL_REGISTRY.as_posix()} row")
            continue
        signal_type = _text(signal.get("signal_type")) or registry_row.get("signal_type", "")
        severity = _text(signal.get("severity")) or registry_row.get("severity", "")
        recommended_skill = _text(signal.get("recommended_skill")) or registry_row.get(
            "recommended_skill", ""
        )
        recommended_role = _text(signal.get("recommended_role")) or registry_row.get(
            "recommended_role", ""
        )
        if signal_type not in active_types:
            errors.append(f"{signal_id}: signal_type {signal_type!r} is not active")
        if severity not in ALLOWED_SIGNAL_SEVERITIES:
            errors.append(f"{signal_id}: severity {severity!r} is not supported")
        if not recommended_skill:
            errors.append(f"{signal_id}: recommended_skill is required")
        if not recommended_role:
            errors.append(f"{signal_id}: recommended_role is required")
        evidence_path = _text(signal.get("evidence_path")) or registry_row.get("evidence_path", "")
        evidence = _text(signal.get("evidence")) or registry_row.get("notes", "")
        enriched.append(
            {
                "signal_id": signal_id,
                "signal_type": signal_type,
                "severity": severity,
                "recommended_skill": recommended_skill,
                "recommended_role": recommended_role,
                "evidence_path": evidence_path,
                "evidence": evidence,
                "registry_row": registry_row,
                "source_paths": record["source_paths"],
            }
        )
    return sorted(
        enriched,
        key=lambda item: (
            SEVERITY_ORDER.get(item["severity"], 99),
            item["registry_row"].get("created_at", ""),
            item["signal_id"],
        ),
    )


def _aggregate_status(signals: list[dict[str, Any]]) -> str:
    statuses = {_text(signal["registry_row"].get("status")) for signal in signals}
    if not statuses:
        return "open"
    if statuses & OPEN_STATUSES:
        return "open"
    if statuses <= SUCCESS_TERMINAL_STATUSES:
        return "resolved"
    if statuses == {"rejected"}:
        return "rejected"
    return "closed"


def _default_solution_plan() -> dict[str, Any]:
    return {
        "present": False,
        "status": "absent",
        "plan_owner_role": "project-system-director",
        "implementation_role": "",
        "objective": "",
        "allowed_write_paths_hint": [""],
        "required_validators": [
            "collect_project_improvement_signals --validate-emitted",
            "validate_documentation_impact",
            "validate_research_control",
        ],
        "plan_steps": [
            {
                "step_id": "PLAN-001",
                "action": (
                    "Project-System Director converts the issue inventory into one bounded "
                    "AgentJob when no executable plan is present."
                ),
                "expected_output": "One AgentJob with allowlisted paths and validators.",
                "stop_condition": "No role fits without authority expansion.",
            }
        ],
    }


def _load_solution_plan(
    repo_root: Path,
    solution_plan_path: str | None,
    errors: list[str],
) -> dict[str, Any]:
    if not solution_plan_path:
        return _default_solution_plan()
    path = _repo_path(repo_root, solution_plan_path)
    data = load_yaml(path)
    plan = data.get("solution_plan", data)
    if not isinstance(plan, dict):
        errors.append(f"{_relative(repo_root, path)}: solution plan must be a map")
        return _default_solution_plan()
    if plan.get("present") is True or _text(plan.get("status")) == "ready_to_implement":
        for field_name in ("implementation_role", "objective"):
            if not _text(plan.get(field_name)):
                errors.append(f"{_relative(repo_root, path)}: solution_plan.{field_name} is required")
        if not isinstance(plan.get("plan_steps"), list) or not plan.get("plan_steps"):
            errors.append(f"{_relative(repo_root, path)}: solution_plan.plan_steps is required")
        if not isinstance(plan.get("required_validators"), list) or not plan.get(
            "required_validators"
        ):
            errors.append(
                f"{_relative(repo_root, path)}: solution_plan.required_validators is required"
            )
    write_hints = plan.get("allowed_write_paths_hint", [])
    if isinstance(write_hints, list):
        for hint in write_hints:
            hint_text = _text(hint)
            if any(hint_text.startswith(prefix) for prefix in PROTECTED_PATH_PREFIXES):
                errors.append(f"{_relative(repo_root, path)}: protected write-path hint {hint_text}")
    return plan


def _source_kind(
    completion: SourceRecord | None,
    handoff: SourceRecord | None,
    allow_backfill: bool,
) -> str:
    if allow_backfill:
        return "backfilled_from_immutable_source"
    if completion and handoff:
        return "research_completion_and_handoff"
    if completion:
        return "completion_only"
    if handoff:
        return "handoff_only"
    return "unknown"


def _source_block(
    repo_root: Path,
    completion: SourceRecord | None,
    handoff: SourceRecord | None,
    allow_backfill: bool,
) -> dict[str, Any]:
    primary = completion or handoff
    handoff_markdown = handoff.path.with_suffix(".md") if handoff else None
    return {
        "source_kind": _source_kind(completion, handoff, allow_backfill),
        "task_id": _text(primary.data.get("task_id")) if primary else "",
        "decision_id": _text(primary.data.get("decision_id")) if primary else "",
        "job_id": _text(primary.data.get("job_id")) if primary else "",
        "completion_path": completion.relative_path if completion else "",
        "regular_handoff_id": _text(handoff.data.get("handoff_id")) if handoff else "",
        "regular_handoff_yaml_path": handoff.relative_path if handoff else "",
        "regular_handoff_markdown_path": (
            _relative(repo_root, handoff_markdown) if handoff_markdown and handoff_markdown.exists() else ""
        ),
    }


def _normal_research_block(handoff: SourceRecord | None) -> dict[str, Any]:
    return {
        "regular_handoff_created": bool(handoff),
        "continue_research_next_action": _text(handoff.data.get("next_action")) if handoff else "",
        "sidecar_does_not_replace_regular_handoff": True,
    }


def _issue_from_signal(index: int, signal: dict[str, Any]) -> dict[str, Any]:
    signal_type_title = signal["signal_type"].replace("_", " ").title()
    evidence_path = signal["evidence_path"] or (signal["source_paths"][0] if signal["source_paths"] else "")
    evidence_summary = signal["evidence"] or "Structured project-improvement signal emitted."
    return {
        "issue_id": f"IPH-ISSUE-{index:03d}",
        "signal_id": signal["signal_id"],
        "signal_type": signal["signal_type"],
        "severity": signal["severity"],
        "title": f"{signal_type_title}: {signal['signal_id']}",
        "description": evidence_summary,
        "evidence": [
            {
                "evidence_path": evidence_path,
                "evidence_summary": evidence_summary,
            }
        ],
        "impact": "Project-system follow-up is required under the improvement workflow.",
        "recommended_skill": signal["recommended_skill"],
        "recommended_role": signal["recommended_role"],
        "recommended_next_step": (
            "Run /improve-project-system to process this signal as one bounded project-system "
            "AgentJob."
        ),
    }


def build_sidecar(
    *,
    repo_root: Path,
    completion: SourceRecord | None,
    handoff: SourceRecord | None,
    signals: list[dict[str, Any]],
    solution_plan: dict[str, Any],
    created_at: str,
    improvement_handoff_id: str,
    allow_backfill: bool,
) -> dict[str, Any]:
    selected = signals[0]
    status = _aggregate_status(signals)
    resolution = {
        "resolved_by_job_id": "",
        "resolution_evidence_path": "",
        "resolved_at": "",
    }
    if status != "open":
        selected_row = selected["registry_row"]
        resolution = {
            "resolved_by_job_id": selected_row.get("resolved_by_job_id", ""),
            "resolution_evidence_path": selected_row.get("resolution_evidence_path", ""),
            "resolved_at": selected_row.get("resolved_at", ""),
        }
    return {
        "improvement_handoff_id": improvement_handoff_id,
        "created_at": created_at,
        "status": status,
        "source": _source_block(repo_root, completion, handoff, allow_backfill),
        "normal_research_continuation": _normal_research_block(handoff),
        "project_boundary": {
            "recommended_skill": "improve-project-system",
            "project_system_only": True,
            "physics_claim_promotion_authorized": False,
            "canonical_science_source_edits_authorized": False,
            "generated_derivative_hand_edits_authorized": False,
            "requires_human_gate": False,
        },
        "signal_summary": {
            "signal_ids": [signal["signal_id"] for signal in signals],
            "signal_count": len(signals),
            "highest_severity": selected["severity"],
            "selected_signal_id": selected["signal_id"],
            "routing_basis": "highest_severity_then_created_at_then_signal_id",
        },
        "issues": [_issue_from_signal(index, signal) for index, signal in enumerate(signals, start=1)],
        "solution_plan": solution_plan,
        "resolution": resolution,
        "notes": "",
    }


def _quote_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(str(value), ensure_ascii=True)


def dump_yaml(data: dict[str, Any], field_order: list[str] | None = None) -> str:
    ordered_keys = list(field_order or [])
    ordered_keys.extend(key for key in data if key not in ordered_keys)
    lines: list[str] = []

    def emit_key_value(key: str, value: Any, indent: int) -> None:
        prefix = " " * indent
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            for child_key, child_value in value.items():
                emit_key_value(child_key, child_value, indent + 2)
        elif isinstance(value, list):
            if not value:
                lines.append(f"{prefix}{key}: []")
                return
            lines.append(f"{prefix}{key}:")
            for item in value:
                emit_list_item(item, indent + 2)
        else:
            lines.append(f"{prefix}{key}: {_quote_scalar(value)}")

    def emit_list_item(item: Any, indent: int) -> None:
        prefix = " " * indent
        if isinstance(item, dict):
            if not item:
                lines.append(f"{prefix}- \"\"")
                return
            first_key, first_value = next(iter(item.items()))
            if isinstance(first_value, (dict, list)):
                lines.append(f"{prefix}- {first_key}:")
                emit_nested_value(first_value, indent + 4)
            else:
                lines.append(f"{prefix}- {first_key}: {_quote_scalar(first_value)}")
            for child_key, child_value in list(item.items())[1:]:
                emit_key_value(child_key, child_value, indent + 2)
        else:
            lines.append(f"{prefix}- {_quote_scalar(item)}")

    def emit_nested_value(value: Any, indent: int) -> None:
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                emit_key_value(child_key, child_value, indent)
        elif isinstance(value, list):
            for item in value:
                emit_list_item(item, indent)
        else:
            lines.append(f"{' ' * indent}{_quote_scalar(value)}")

    for key in ordered_keys:
        if key in data:
            emit_key_value(key, data[key], 0)
    return "\n".join(lines) + "\n"


def _source_signal_ids(source: SourceRecord | None) -> list[str]:
    if not source:
        return []
    signals = source.data.get("project_improvement_signals", [])
    if not isinstance(signals, list):
        return []
    signal_ids = {
        _text(signal.get("signal_id"))
        for signal in signals
        if isinstance(signal, dict) and not _is_blank_signal(signal) and _text(signal.get("signal_id"))
    }
    return sorted(signal_ids)


def _source_bridge_reference(sidecar_path: str, signal_ids: list[str]) -> dict[str, Any]:
    return {
        "required": True,
        "improvement_handoff_path": sidecar_path,
        "signal_ids": signal_ids,
        "bridge_status": "generated",
        "notes": "Generated by scripts/project_control/generate_project_improvement_handoff.py.",
    }


def _replace_or_append_top_level_block(text: str, key: str, block_text: str) -> str:
    lines = text.rstrip("\n").splitlines()
    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.startswith(f"{key}:"):
            start_index = index
            break
    block_lines = block_text.rstrip("\n").splitlines()
    if start_index is None:
        if lines:
            return "\n".join(lines + block_lines) + "\n"
        return block_text

    end_index = start_index + 1
    while end_index < len(lines):
        line = lines[end_index]
        if line and not line.startswith((" ", "\t")) and TOP_LEVEL_KEY_RE.match(line):
            break
        end_index += 1
    return "\n".join(lines[:start_index] + block_lines + lines[end_index:]).rstrip("\n") + "\n"


def _write_source_bridge(
    source: SourceRecord,
    sidecar_path: str,
    *,
    write: bool,
) -> dict[str, Any] | None:
    signal_ids = _source_signal_ids(source)
    if not signal_ids:
        return None
    bridge = _source_bridge_reference(sidecar_path, signal_ids)
    if bridge["bridge_status"] not in SOURCE_BRIDGE_STATUSES:
        raise ValueError(f"{source.relative_path}: unsupported bridge_status")
    bridge_text = dump_yaml({PROJECT_IMPROVEMENT_BRIDGE_FIELD: bridge})
    current = source.path.read_text(encoding="utf-8")
    updated = _replace_or_append_top_level_block(current, PROJECT_IMPROVEMENT_BRIDGE_FIELD, bridge_text)
    if write:
        source.path.write_text(updated, encoding="utf-8")
    return {
        "source_path": source.relative_path,
        "signal_ids": signal_ids,
        "bridge_status": bridge["bridge_status"],
        "write_status": "written" if write else "dry_run",
    }


def render_markdown(sidecar: dict[str, Any]) -> str:
    signal_summary = sidecar["signal_summary"]
    source = sidecar["source"]
    lines = [
        "<!-- authority: control -->",
        "",
        f"# Project-Improvement Handoff: {sidecar['improvement_handoff_id']}",
        "",
        "## Source",
        "",
        f"- Source task: `{source['task_id']}`",
        f"- Source decision: `{source['decision_id']}`",
        f"- Source job: `{source['job_id']}`",
        f"- Source completion: `{source['completion_path']}`",
        f"- Regular research handoff: `{source['regular_handoff_id']}`",
        "",
        "## Boundary",
        "",
        "This sidecar is a project-system improvement handoff. It does not replace the",
        "normal research handoff, does not become the latest `/continue-research`",
        "handoff, and does not authorize project-system repair from the research lane.",
        "",
        "Authorized consumer: `/improve-project-system`.",
        "",
        "Unauthorized effects:",
        "",
        "- physics claim promotion;",
        "- canonical science source edits;",
        "- generated derivative hand edits;",
        "- replacement of `research_control/handoffs/handoff-####.yaml`.",
        "",
        "## Signal Summary",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Signal IDs | {', '.join(f'`{signal_id}`' for signal_id in signal_summary['signal_ids'])} |",
        f"| Signal count | {signal_summary['signal_count']} |",
        f"| Highest severity | {signal_summary['highest_severity']} |",
        f"| Selected signal | `{signal_summary['selected_signal_id']}` |",
        f"| Routing basis | `{signal_summary['routing_basis']}` |",
        "",
        "## Issues",
        "",
    ]
    for issue in sidecar["issues"]:
        lines.extend(
            [
                f"### {issue['issue_id']}: {issue['title']}",
                "",
                f"Signal: `{issue['signal_id']}`",
                "",
                f"Type: `{issue['signal_type']}`",
                "",
                f"Severity: {issue['severity']}",
                "",
                f"Description: {issue['description']}",
                "",
                "Evidence:",
                "",
            ]
        )
        for evidence in issue["evidence"]:
            lines.append(
                f"- `{evidence['evidence_path']}`: {evidence['evidence_summary']}"
            )
        lines.extend(
            [
                "",
                f"Impact: {issue['impact']}",
                "",
                f"Recommended next step: {issue['recommended_next_step']}",
                "",
            ]
        )
    plan = sidecar["solution_plan"]
    lines.extend(
        [
            "## Solution Plan",
            "",
            f"Status: {plan.get('status', '')}.",
            "",
        ]
    )
    if plan.get("present") is True:
        lines.extend(
            [
                f"Implementation role: `{plan.get('implementation_role', '')}`",
                "",
                f"Objective: {plan.get('objective', '')}",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "If no executable plan is present, Project-System Director should convert this",
                "issue inventory into one bounded AgentJob or reject the signal with explicit",
                "evidence.",
                "",
            ]
        )
    resolution = sidecar["resolution"]
    lines.extend(
        [
            "## Resolution",
            "",
            f"- Resolved by job: {resolution.get('resolved_by_job_id') or 'none'}.",
            f"- Resolution evidence: {resolution.get('resolution_evidence_path') or 'none'}.",
            f"- Resolved at: {resolution.get('resolved_at') or 'none'}.",
            "",
            "## Notes",
            "",
            "This Markdown mirror is operator-facing. The YAML sidecar remains the",
            "machine-readable control artifact.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_project_improvement_handoff(
    *,
    completion_path: str | None,
    source_handoff_path: str | None,
    solution_plan_path: str | None = None,
    created_at: str | None = None,
    improvement_handoff_id: str | None = None,
    allow_backfill: bool = False,
    write: bool = False,
    update_source_bridge: bool = False,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    completion = _source_record(repo_root, completion_path, "completion") if completion_path else None
    handoff = (
        _source_record(repo_root, source_handoff_path, "handoff") if source_handoff_path else None
    )
    if not completion and not handoff:
        errors.append("at least one of --completion or --source-handoff is required")
    if handoff:
        handoff_markdown = handoff.path.with_suffix(".md")
        if not handoff_markdown.exists():
            errors.append(f"{_relative(repo_root, handoff_markdown)}: Markdown mirror is missing")

    emitted = _extract_signals(completion, errors)
    emitted.extend(_extract_signals(handoff, errors))
    deduped = _dedupe_signals(emitted)
    if not deduped:
        return {
            "ok": not errors,
            "mode": "write" if write else "dry-run",
            "bridge_required": False,
            "errors": errors,
            "warnings": warnings,
            "signal_ids": [],
            "output_paths": {},
            "write_status": "not_required",
            "source_bridge_update_requested": update_source_bridge,
            "source_bridge_updates": [],
        }

    signals = _validate_and_enrich_signals(repo_root, deduped, errors)
    if errors:
        return {
            "ok": False,
            "mode": "write" if write else "dry-run",
            "bridge_required": True,
            "errors": errors,
            "warnings": warnings,
            "signal_ids": [record["signal_id"] for record in deduped],
            "output_paths": {},
            "write_status": "blocked",
        }

    timestamp = created_at or _source_timestamp(completion, handoff)
    task_id = _source_task_id(completion, handoff)
    handoff_id = improvement_handoff_id or _default_handoff_id(task_id, timestamp)
    output_dir = repo_root / OUTPUT_DIR
    yaml_path = output_dir / f"{handoff_id}.yaml"
    markdown_path = output_dir / f"{handoff_id}.md"
    if write and (yaml_path.exists() or markdown_path.exists()):
        errors.append(f"{OUTPUT_DIR.as_posix()}/{handoff_id}: sidecar output already exists")

    solution_plan = _load_solution_plan(repo_root, solution_plan_path, errors)
    if errors:
        return {
            "ok": False,
            "mode": "write" if write else "dry-run",
            "bridge_required": True,
            "errors": errors,
            "warnings": warnings,
            "signal_ids": [signal["signal_id"] for signal in signals],
            "output_paths": {
                "yaml": _relative(repo_root, yaml_path),
                "markdown": _relative(repo_root, markdown_path),
            },
            "write_status": "blocked",
        }

    sidecar = build_sidecar(
        repo_root=repo_root,
        completion=completion,
        handoff=handoff,
        signals=signals,
        solution_plan=solution_plan,
        created_at=timestamp,
        improvement_handoff_id=handoff_id,
        allow_backfill=allow_backfill,
    )
    yaml_text = dump_yaml(sidecar, SIDE_CAR_FIELD_ORDER)
    load_yaml_text(yaml_text)
    markdown_text = render_markdown(sidecar)
    output_paths = {
        "yaml": _relative(repo_root, yaml_path),
        "markdown": _relative(repo_root, markdown_path),
    }
    write_status = "dry_run"
    source_bridge_updates: list[dict[str, Any]] = []
    if write:
        output_dir.mkdir(parents=True, exist_ok=True)
        yaml_path.write_text(yaml_text, encoding="utf-8")
        markdown_path.write_text(markdown_text, encoding="utf-8")
        write_status = "written"
    if update_source_bridge:
        for source in (completion, handoff):
            if not source:
                continue
            update = _write_source_bridge(source, output_paths["yaml"], write=write)
            if update:
                source_bridge_updates.append(update)
    return {
        "ok": True,
        "mode": "write" if write else "dry-run",
        "bridge_required": True,
        "errors": [],
        "warnings": warnings,
        "improvement_handoff_id": handoff_id,
        "created_at": timestamp,
        "status": sidecar["status"],
        "signal_ids": sidecar["signal_summary"]["signal_ids"],
        "highest_severity": sidecar["signal_summary"]["highest_severity"],
        "selected_signal_id": sidecar["signal_summary"]["selected_signal_id"],
        "output_paths": output_paths,
        "source_paths": {
            "completion": completion.relative_path if completion else "",
            "source_handoff": handoff.relative_path if handoff else "",
        },
        "write_status": write_status,
        "source_bridge_update_requested": update_source_bridge,
        "source_bridge_updates": source_bridge_updates,
        "sidecar": sidecar,
        "yaml_text": yaml_text,
        "markdown_text": markdown_text,
    }


def _json_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in result.items()
        if key not in {"sidecar", "yaml_text", "markdown_text"}
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Validate and report intended output.")
    mode.add_argument("--write", action="store_true", help="Write the sidecar YAML and Markdown.")
    parser.add_argument("--source-handoff", help="Normal handoff YAML source.")
    parser.add_argument("--completion", help="Completion YAML source.")
    parser.add_argument("--allow-backfill", action="store_true", help="Mark output as a backfill.")
    parser.add_argument("--solution-plan", help="Optional strict-YAML solution_plan snippet.")
    parser.add_argument("--created-at", help="Explicit sidecar creation timestamp.")
    parser.add_argument("--improvement-handoff-id", help="Explicit sidecar ID and filename stem.")
    parser.add_argument(
        "--update-source-bridge",
        action="store_true",
        help="Update source YAML project_improvement_bridge blocks when writing the sidecar.",
    )
    parser.add_argument("--json", action="store_true", help="Emit a JSON summary.")
    return parser.parse_args(argv)


def _print_human(result: dict[str, Any]) -> None:
    if not result["ok"]:
        print("Project-improvement handoff generation failed.", file=sys.stderr)
        for error in result["errors"]:
            print(f"- {error}", file=sys.stderr)
        return
    if not result["bridge_required"]:
        print("No nonblank project_improvement_signals found; no sidecar required.")
        return
    print(f"Project-improvement handoff: {result['improvement_handoff_id']}")
    print(f"Mode: {result['mode']}")
    print(f"Status: {result['status']}")
    print(f"Signals: {', '.join(result['signal_ids'])}")
    print(f"YAML: {result['output_paths']['yaml']}")
    print(f"Markdown: {result['output_paths']['markdown']}")
    print(f"Write status: {result['write_status']}")
    for update in result.get("source_bridge_updates", []):
        print(f"Source bridge: {update['source_path']} ({update['write_status']})")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = generate_project_improvement_handoff(
            completion_path=args.completion,
            source_handoff_path=args.source_handoff,
            solution_plan_path=args.solution_plan,
            created_at=args.created_at,
            improvement_handoff_id=args.improvement_handoff_id,
            allow_backfill=args.allow_backfill,
            write=args.write,
            update_source_bridge=args.update_source_bridge,
        )
    except (StrictYamlError, ValueError, OSError) as exc:
        result = {
            "ok": False,
            "mode": "write" if args.write else "dry-run",
            "bridge_required": False,
            "errors": [str(exc)],
            "warnings": [],
            "signal_ids": [],
            "output_paths": {},
            "write_status": "blocked",
        }
    if args.json:
        print(json.dumps(_json_summary(result), indent=2))
    else:
        _print_human(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
