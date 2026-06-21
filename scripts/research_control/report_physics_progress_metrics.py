#!/usr/bin/env python3
"""Report operational physics-progress metrics from tracked control records."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


PHYSICS_AUTHORITY_LEVELS = {"science_draft", "human_gated"}
PHYSICS_ROLE_KIND_PREFIX = "scientific_"
ROLE_METRIC_KEYS = {
    "theoretical-continuation-selector": "selector_tasks",
    "candidate-constructor": "candidate_constructor_tasks",
    "smuggling-auditor": "smuggling_auditor_tasks",
    "refuter": "refuter_tasks",
    "gate-chair": "gate_chair_tasks",
}


def read_csv_rows(repo_root: Path, registry_name: str) -> list[dict[str, str]]:
    path = repo_root / "registries" / registry_name
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str):
        return [value] if value else []
    return []


def bool_value(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return None


def role_key(role_id: str, version: str) -> tuple[str, str]:
    return role_id, version


def is_physics_role(role: dict[str, str] | None) -> bool:
    if not role:
        return False
    return (
        role.get("authority_level", "") in PHYSICS_AUTHORITY_LEVELS
        or role.get("role_kind", "").startswith(PHYSICS_ROLE_KIND_PREFIX)
    )


def completion_text(repo_root: Path, path_text: str) -> str:
    path = repo_root / path_text
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_completion(repo_root: Path, path_text: str) -> dict[str, Any]:
    if not path_text:
        return {}
    path = repo_root / path_text
    if not path.exists():
        return {}
    try:
        return load_yaml(path)
    except StrictYamlError:
        return {}


def status_from_progress(completion: dict[str, Any]) -> str:
    progress = completion.get("physics_progress_status")
    if isinstance(progress, dict):
        return str(progress.get("status", "")).strip()
    return ""


def changed_from_delta(completion: dict[str, Any]) -> bool | None:
    delta = completion.get("distance_to_gr_delta")
    if isinstance(delta, dict):
        return bool_value(delta.get("changed"))
    return None


def obstruction_id(completion: dict[str, Any]) -> str:
    record = completion.get("obstruction_record")
    if not isinstance(record, dict) or bool_value(record.get("present")) is not True:
        return ""
    return str(record.get("obstruction_id", "")).strip()


def freeze_decision(completion: dict[str, Any]) -> str:
    record = completion.get("freeze_criteria_status")
    if not isinstance(record, dict):
        return ""
    return str(record.get("freeze_decision", "")).strip()


def build_report(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    repo_root = Path(repo_root)
    task_rows = read_csv_rows(repo_root, "RESEARCH_TASK_REGISTRY.csv")
    job_rows = read_csv_rows(repo_root, "AGENT_JOB_REGISTRY.csv")
    role_rows = read_csv_rows(repo_root, "AGENT_ROLE_REGISTRY.csv")
    claim_rows = read_csv_rows(repo_root, "CLAIM_BOUNDARY_REGISTRY.csv")

    roles = {
        role_key(row.get("role_id", ""), row.get("version", "")): row
        for row in role_rows
    }

    completion_records: list[dict[str, Any]] = []
    completion_status_counts: Counter[str] = Counter()
    physics_progress_counts: Counter[str] = Counter()
    candidate_result_counts: Counter[str] = Counter()
    physics_role_counts: Counter[str] = Counter()

    distance_true = 0
    distance_false = 0
    forbidden_summary_count = 0
    promotion_authorized_count = 0
    obstruction_records: list[dict[str, str]] = []
    freeze_review_count = 0
    human_gate_freeze_count = 0

    sorted_jobs = sorted(
        job_rows,
        key=lambda row: (row.get("created_at", ""), row.get("job_id", "")),
    )

    for row in sorted_jobs:
        completion_path = row.get("completion_path", "")
        completion = load_completion(repo_root, completion_path)
        if not completion:
            continue

        role = roles.get(role_key(row.get("role_id", ""), row.get("role_version", "")))
        is_physics = is_physics_role(role)
        role_id = row.get("role_id", "")
        if is_physics:
            physics_role_counts[role_id] += 1

        completion_status_counts[str(completion.get("validation_status", "")).strip() or "unknown"] += 1
        progress_status = status_from_progress(completion)
        if progress_status:
            physics_progress_counts[progress_status] += 1

        delta_changed = changed_from_delta(completion)
        if delta_changed is True:
            distance_true += 1
        elif delta_changed is False:
            distance_false += 1

        forbidden = completion.get("forbidden_conclusion_summary")
        if isinstance(forbidden, dict):
            forbidden_summary_count += 1
            if bool_value(forbidden.get("physics_promotion_authorized")) is True:
                promotion_authorized_count += 1

        candidate = completion.get("candidate_constructor_result")
        if isinstance(candidate, dict):
            result_type = str(candidate.get("result_type", "")).strip()
            if result_type:
                candidate_result_counts[result_type] += 1

        oid = obstruction_id(completion)
        if oid:
            obstruction_records.append(
                {
                    "obstruction_id": oid,
                    "completion_path": completion_path,
                    "completed_at": row.get("completed_at", ""),
                }
            )

        freeze = completion.get("freeze_criteria_status")
        if isinstance(freeze, dict):
            repeated = bool_value(freeze.get("repeated_burden")) is True
            required = bool_value(freeze.get("freeze_evaluation_required")) is True
            if repeated or required:
                freeze_review_count += 1
            if freeze_decision(completion) == "human_gate_required":
                human_gate_freeze_count += 1

        completion_records.append(
            {
                "job_id": row.get("job_id", ""),
                "role_id": role_id,
                "completion_path": completion_path,
                "completed_at": row.get("completed_at", ""),
                "is_physics": is_physics,
            }
        )

    referenced_obstructions = 0
    for record in obstruction_records:
        oid = record["obstruction_id"]
        source_path = record["completion_path"]
        source_time = record["completed_at"]
        for later in completion_records:
            if later["completion_path"] == source_path:
                continue
            if source_time and later["completed_at"] and later["completed_at"] <= source_time:
                continue
            if oid and oid in completion_text(repo_root, later["completion_path"]):
                referenced_obstructions += 1
                break

    physics_sequence = [
        row["role_id"]
        for row in completion_records
        if row["is_physics"] and row["role_id"]
    ]
    cycle_lengths: list[int] = []
    selector_without_construction = 0
    index = 0
    while index < len(physics_sequence):
        role_id = physics_sequence[index]
        if role_id == "candidate-constructor":
            length = 1
            if index + length < len(physics_sequence) and physics_sequence[index + length] == "smuggling-auditor":
                length += 1
            if index + length < len(physics_sequence) and physics_sequence[index + length] == "refuter":
                length += 1
            if length > 1:
                cycle_lengths.append(length)
            index += length
            continue
        if role_id == "theoretical-continuation-selector":
            next_role = physics_sequence[index + 1] if index + 1 < len(physics_sequence) else ""
            if next_role != "candidate-constructor":
                selector_without_construction += 1
        index += 1

    average_cycle = round(sum(cycle_lengths) / len(cycle_lengths), 2) if cycle_lengths else 0
    role_metrics = {key: 0 for key in ROLE_METRIC_KEYS.values()}
    for role_id, metric_key in ROLE_METRIC_KEYS.items():
        role_metrics[metric_key] = physics_role_counts.get(role_id, 0)

    metrics = {
        "input_counts": {
            "tasks_registered": len(task_rows),
            "jobs_registered": len(job_rows),
            "completions_read": len(completion_records),
            "physics_completions_read": sum(1 for row in completion_records if row["is_physics"]),
            "claim_boundary_rows": len(claim_rows),
            "active_claim_boundary_rows": sum(1 for row in claim_rows if row.get("status") == "active"),
        },
        "claim_hygiene_metrics": {
            "tasks_with_forbidden_conclusion_summary": forbidden_summary_count,
            "physics_promotion_authorized_true": promotion_authorized_count,
            "physics_promotion_authorized_false": max(0, forbidden_summary_count - promotion_authorized_count),
            "claim_boundary_rows_active": sum(1 for row in claim_rows if row.get("status") == "active"),
        },
        "physics_progress_metrics": {
            "tasks_with_distance_to_gr_delta_true": distance_true,
            "tasks_with_distance_to_gr_delta_false": distance_false,
            "burden_discharged_count": physics_progress_counts.get("burden_discharged", 0),
            "candidate_constructed_count": (
                physics_progress_counts.get("candidate_constructed_pending_audit", 0)
                + candidate_result_counts.get("constructed_candidate", 0)
            ),
            "precise_obstruction_count": (
                physics_progress_counts.get("precise_obstruction_found", 0)
                + candidate_result_counts.get("precise_obstruction", 0)
            ),
            "route_frozen_count": physics_progress_counts.get("route_frozen", 0),
            "human_gate_required_count": physics_progress_counts.get("human_gate_required", 0),
            "physics_progress_status_counts": dict(sorted(physics_progress_counts.items())),
        },
        "obstruction_reuse_metrics": {
            "obstruction_records_created": len(obstruction_records),
            "obstruction_records_referenced_by_later_tasks": referenced_obstructions,
            "repeated_obstructions_triggering_freeze_review": freeze_review_count,
            "frozen_routes_reopened_by_human_gate": human_gate_freeze_count,
        },
        "agent_workflow_metrics": {
            **role_metrics,
            "average_tasks_per_construct_audit_stress_cycle": average_cycle,
            "construct_audit_stress_cycle_count": len(cycle_lengths),
            "selector_cycles_without_construction": selector_without_construction,
        },
    }

    return {
        "report_id": "mathematical_decisiveness_phase9_metrics",
        "as_of": max(
            [row.get("updated_at", "") for row in task_rows]
            + [row.get("completed_at", "") for row in job_rows]
            + [""]
        ),
        "source_basis": [
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "registries/AGENT_JOB_REGISTRY.csv",
            "registries/AGENT_ROLE_REGISTRY.csv",
            "registries/CLAIM_BOUNDARY_REGISTRY.csv",
            "research_control/tasks/*/jobs/completions/*.yaml",
        ],
        "authority_boundary": {
            "metrics_are_operational": True,
            "physics_claim_promotion_authorized": False,
            "validation_status_is_not_physics_evidence": True,
        },
        "metrics": metrics,
        "limitations": [
            "Counts are descriptive operational diagnostics, not physics evidence.",
            "Obstruction reuse is measured by completion-level obstruction IDs and later completion references.",
            "Validator failure history is not a durable event log, so this report does not infer blocked violation counts from past terminal output.",
        ],
    }


def render_table(mapping: dict[str, Any]) -> list[str]:
    lines = ["| Metric | Value |", "| --- | --- |"]
    for key, value in mapping.items():
        rendered = json.dumps(value, sort_keys=True) if isinstance(value, dict) else str(value)
        lines.append(f"| `{key}` | `{rendered}` |")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    lines: list[str] = [
        "<!-- authority: control -->",
        "",
        "# Mathematical Decisiveness Phase 9 Metrics Report",
        "",
        "## Analysis",
        "",
        "This report is generated from tracked research-control registries and completion YAML files. It evaluates the AI research-agent system as an operational system. It does not promote a physics claim, adopt a source law, construct `M_src`, or treat validator success as physics evidence.",
        "",
        "## Source Basis",
        "",
    ]
    lines.extend(f"- `{path}`" for path in report["source_basis"])
    lines.extend(
        [
            "",
            "## Input Counts",
            "",
            *render_table(metrics["input_counts"]),
            "",
            "## Claim Hygiene Metrics",
            "",
            *render_table(metrics["claim_hygiene_metrics"]),
            "",
            "## Physics Progress Metrics",
            "",
            *render_table(metrics["physics_progress_metrics"]),
            "",
            "## Obstruction Reuse Metrics",
            "",
            *render_table(metrics["obstruction_reuse_metrics"]),
            "",
            "## Agent Workflow Metrics",
            "",
            *render_table(metrics["agent_workflow_metrics"]),
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in report["limitations"])
    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "Phase 9 provides an operational metrics layer for future evaluation. The metrics show whether tracked work is producing candidates, obstructions, freeze reviews, human-gate requirements, or repeated selector cycles. They do not change the authority of any scientific artifact.",
            "",
            "## References",
            "",
            "The AEther-Flow Research Project. (2026, June 21). *AEther recommendations implementation plan* [Local implementation plan].",
            "",
            "The AEther-Flow Research Project. (2026, June 21). *Agent job registry* [Project-control registry].",
            "",
            "The AEther-Flow Research Project. (2026, June 21). *Claim boundary registry* [Project-control registry].",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    parser.add_argument("--output", help="Write output to a repository-relative path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report(REPO_ROOT)
    if args.format == "markdown":
        output = render_markdown(report)
    else:
        output = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.output:
        output_path = REPO_ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
