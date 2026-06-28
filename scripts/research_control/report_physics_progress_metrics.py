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
OPERATIONAL_METRIC_KEY_TOKENS = {
    "checker",
    "diagnostic_warning",
    "validator",
    "validation",
    "registry",
    "generated",
    "memory",
    "payload_density",
    "route_orbit",
    "wiki",
    "receipt",
    "role_schema",
    "handoff_continuity",
}
SUPPORT_ONLY_CHECKER_ID = "finite_local_candidate_checker"
SUPPORT_ONLY_CHECKER_REPORT_GLOB = "research_control/tasks/*/artifacts/*checker_report.json"
SUPPORT_ONLY_BOUNDARY_REQUIRED_PHRASES = ("support-only", "not proof authority")


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


def dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def string_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def payload_count(completion: dict[str, Any]) -> int:
    manifest = completion.get("mathematical_payload_manifest")
    if isinstance(manifest, list):
        return len(manifest)
    legacy = completion.get("new_mathematical_payload")
    if isinstance(legacy, list):
        return len(legacy)
    return 0


def first_nonblank(*values: Any) -> str:
    for value in values:
        text = string_value(value)
        if text:
            return text
    return ""


def selected_packet_type(completion: dict[str, Any]) -> str:
    decision = dict_value(completion.get("theoretical_decision_output"))
    return first_nonblank(
        decision.get("selected_next_packet_type"),
        decision.get("selected_packet_type_for_validator"),
        decision.get("selected_next_packet_family"),
        decision.get("packet_type"),
    )


def selected_role_hint(completion: dict[str, Any]) -> str:
    decision = dict_value(completion.get("theoretical_decision_output"))
    return first_nonblank(
        decision.get("selected_next_role"),
        decision.get("next_execution_role_family"),
        decision.get("selected_next_role_family"),
    )


def source_extension_category(completion: dict[str, Any]) -> str:
    return string_value(completion.get("source_extension_category"))


def burden_key(completion: dict[str, Any]) -> tuple[str, str]:
    progress = dict_value(completion.get("physics_progress_status"))
    delta = dict_value(completion.get("distance_to_gr_delta"))
    milestone = first_nonblank(
        progress.get("target_derivation_milestone"),
        delta.get("milestone"),
    )
    burden = first_nonblank(
        progress.get("milestone_burden"),
        delta.get("burden_id"),
    )
    if not milestone and not burden:
        return "", ""
    return milestone, burden


def bridge_attempt_present(completion: dict[str, Any]) -> bool:
    bridge = dict_value(completion.get("bridge_attempt_status"))
    if any(string_value(value) for value in bridge.values()):
        return True
    category = source_extension_category(completion)
    return "candidate" in category or "construction" in category


def completion_record(
    repo_root: Path,
    row: dict[str, str],
    completion: dict[str, Any],
    is_physics: bool,
) -> dict[str, Any]:
    progress = dict_value(completion.get("physics_progress_status"))
    delta = dict_value(completion.get("distance_to_gr_delta"))
    route = dict_value(completion.get("route_cycle_control"))
    freeze = dict_value(completion.get("freeze_criteria_status"))
    candidate = dict_value(completion.get("candidate_constructor_result"))
    obstruction = dict_value(completion.get("obstruction_record"))
    forbidden = dict_value(completion.get("forbidden_conclusion_summary"))
    completion_path = row.get("completion_path", "")

    return {
        "task_id": first_nonblank(completion.get("task_id"), row.get("task_id", "")),
        "job_id": row.get("job_id", ""),
        "role_id": row.get("role_id", ""),
        "completion_path": completion_path,
        "completed_at": row.get("completed_at", ""),
        "is_physics": is_physics,
        "text": completion_text(repo_root, completion_path),
        "progress_status": string_value(progress.get("status")),
        "milestone": first_nonblank(progress.get("target_derivation_milestone"), delta.get("milestone")),
        "burden_id": first_nonblank(progress.get("milestone_burden"), delta.get("burden_id")),
        "burden_key": burden_key(completion),
        "delta_changed": changed_from_delta(completion),
        "payload_count": payload_count(completion),
        "cycle_family": string_value(route.get("cycle_family")),
        "cycle_step": string_value(route.get("current_cycle_step")),
        "cycle_risk": string_value(route.get("cycle_risk")),
        "candidate_result_type": string_value(candidate.get("result_type")),
        "selected_next_packet_type": selected_packet_type(completion),
        "selected_role_hint": selected_role_hint(completion),
        "freeze_repeated_burden": bool_value(freeze.get("repeated_burden")) is True,
        "freeze_evaluation_required": bool_value(freeze.get("freeze_evaluation_required")) is True,
        "freeze_decision": string_value(freeze.get("freeze_decision")),
        "obstruction_present": bool_value(obstruction.get("present")) is True,
        "obstruction_id": string_value(obstruction.get("obstruction_id")),
        "physics_promotion_authorized": bool_value(
            forbidden.get("physics_promotion_authorized")
        ) is True,
        "has_forbidden_conclusion_summary": isinstance(
            completion.get("forbidden_conclusion_summary"),
            dict,
        ),
        "bridge_attempt_present": bridge_attempt_present(completion),
        "source_extension_category": source_extension_category(completion),
    }


def collect_support_only_checker_metrics(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Count support-only checker reports as operational tooling evidence."""
    repo_root = Path(repo_root)
    status_counts: Counter[str] = Counter()
    report_files_scanned = 0
    reports_found = 0
    parse_errors = 0
    forbidden_overread_reports = 0
    physics_obstruction_reports = 0
    boundary_mismatch_reports = 0
    tooling_error_reports = 0

    for path in sorted(repo_root.glob(SUPPORT_ONLY_CHECKER_REPORT_GLOB)):
        report_files_scanned += 1
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            parse_errors += 1
            continue

        if report.get("checker_id") != SUPPORT_ONLY_CHECKER_ID:
            continue

        reports_found += 1
        status = str(report.get("status", "")).strip() or "unknown"
        status_counts[status] += 1

        if list_value(report.get("forbidden_overread_flags")):
            forbidden_overread_reports += 1
        if str(report.get("physics_obstruction", "")).strip():
            physics_obstruction_reports += 1

        boundary = str(report.get("boundary_statement", ""))
        if any(phrase not in boundary for phrase in SUPPORT_ONLY_BOUNDARY_REQUIRED_PHRASES):
            boundary_mismatch_reports += 1

        if bool_value(report.get("tooling_error")) is True:
            tooling_error_reports += 1

    return {
        "support_only_checker_report_files_scanned": report_files_scanned,
        "support_only_checker_report_parse_errors": parse_errors,
        "support_only_checker_reports_found": reports_found,
        "support_only_checker_status_counts": dict(sorted(status_counts.items())),
        "support_only_checker_forbidden_overread_reports": forbidden_overread_reports,
        "support_only_checker_physics_obstruction_reports": physics_obstruction_reports,
        "support_only_checker_boundary_mismatch_reports": boundary_mismatch_reports,
        "support_only_checker_tooling_error_reports": tooling_error_reports,
    }


def scientific_metric_key_violations(metrics: dict[str, Any]) -> list[str]:
    """Return scientific scoreboard keys that look operational-only."""
    violations: list[str] = []
    for key in metrics:
        normalized = key.lower()
        if any(token in normalized for token in OPERATIONAL_METRIC_KEY_TOKENS):
            violations.append(key)
    return violations


def cycle_step_bucket(record: dict[str, Any]) -> str:
    step = record.get("cycle_step", "").lower()
    role_id = record.get("role_id", "")
    if "candidate" in step or "constructor" in step or role_id == "candidate-constructor":
        return "construct"
    if "audit" in step or "smuggling" in step or role_id == "smuggling-auditor":
        return "audit"
    if "stress" in step or "refuter" in step or role_id == "refuter":
        return "stress"
    if "selector" in step or role_id == "theoretical-continuation-selector":
        return "selector"
    return ""


def complete_legacy_cycle_count(records: list[dict[str, Any]]) -> tuple[int, list[list[dict[str, Any]]]]:
    cycles: list[list[dict[str, Any]]] = []
    expected = [
        "candidate-constructor",
        "smuggling-auditor",
        "refuter",
        "theoretical-continuation-selector",
    ]
    index = 0
    while index <= len(records) - len(expected):
        window = records[index : index + len(expected)]
        if [record["role_id"] for record in window] == expected:
            cycles.append(window)
            index += len(expected)
            continue
        index += 1
    return len(cycles), cycles


def explicit_cycle_summary(records: list[dict[str, Any]]) -> tuple[int, int, set[str]]:
    families: dict[str, dict[str, Any]] = {}
    for record in records:
        family = record.get("cycle_family", "")
        if not family:
            continue
        entry = families.setdefault(family, {"steps": set(), "payload": 0})
        bucket = cycle_step_bucket(record)
        if bucket:
            entry["steps"].add(bucket)
        entry["payload"] += int(record.get("payload_count", 0))

    cycle_count = 0
    payload_total = 0
    complete_families: set[str] = set()
    for family, entry in families.items():
        steps = entry["steps"]
        if len(steps) >= 2:
            cycle_count += 1
            payload_total += int(entry["payload"])
        if {"construct", "audit", "stress", "selector"}.issubset(steps):
            complete_families.add(family)
    return cycle_count, payload_total, complete_families


def selector_has_constructive_consequence(
    record: dict[str, Any],
    next_record: dict[str, Any] | None,
) -> bool:
    selected = " ".join(
        [
            record.get("selected_next_packet_type", ""),
            record.get("selected_role_hint", ""),
            record.get("text", ""),
        ]
    ).lower()
    constructive_tokens = (
        "candidate-constructor",
        "candidate constructor",
        "refuter",
        "obstruction",
        "no-go",
        "no_go",
        "gate-chair",
        "gate chair",
        "human_gate",
        "freeze",
    )
    if any(token in selected for token in constructive_tokens):
        return True
    return bool(
        next_record
        and next_record.get("role_id") in {"candidate-constructor", "refuter", "gate-chair"}
    )


def warning_record(
    warning_id: str,
    metric_key: str,
    observed_value: Any,
    threshold: Any,
    evidence_paths: list[str],
    recommended_guard_action: str,
) -> dict[str, Any]:
    return {
        "warning_id": warning_id,
        "severity": "warning",
        "metric_key": metric_key,
        "observed_value": observed_value,
        "threshold": threshold,
        "evidence_paths": sorted(set(path for path in evidence_paths if path)),
        "recommended_guard_action": recommended_guard_action,
        "hard_gate": False,
        "physics_claim_authority": False,
    }


def collect_payload_density_metrics(
    records: list[dict[str, Any]],
    support_metrics: dict[str, Any],
    referenced_obstructions: int,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    if not records:
        return (
            {
                "physics_completions_read": 0,
                "total_payload_items": 0,
                "tasks_since_last_distance_to_gr_delta": 0,
                "tasks_since_last_burden_discharged": 0,
                "new_payload_items_per_physics_task": 0,
                "new_payload_items_per_cycle": 0,
                "selector_cycles_without_new_payload": 0,
            },
            {
                "same_burden_repetition_count": 0,
                "freeze_reviews_triggered_by_repetition": 0,
                "bridge_attempts_since_last_gate": 0,
                "obstructions_created": 0,
                "obstructions_created_missing_id": 0,
                "obstructions_reused": 0,
                "candidate_construct_audit_stress_selector_cycles": 0,
                "gate_ready_cycles_without_gate_verdict": 0,
                "support_only_tooling_reports": support_metrics.get(
                    "support_only_checker_reports_found",
                    0,
                ),
                "physics_promotion_authorized_true_count": 0,
                "physics_promotion_authorized_false_count": 0,
            },
            [],
        )

    total_payload = sum(int(record.get("payload_count", 0)) for record in records)

    since_delta = 0
    for record in records:
        if record.get("delta_changed") is True:
            since_delta = 0
        else:
            since_delta += 1

    since_burden = 0
    for record in records:
        if record.get("progress_status") == "burden_discharged":
            since_burden = 0
        else:
            since_burden += 1

    explicit_cycle_count, explicit_cycle_payload, complete_families = explicit_cycle_summary(records)
    legacy_cycle_count, legacy_cycles = complete_legacy_cycle_count(
        [record for record in records if not record.get("cycle_family")]
    )
    legacy_cycle_payload = sum(
        int(record.get("payload_count", 0))
        for cycle in legacy_cycles
        for record in cycle
    )
    cycle_count = explicit_cycle_count + legacy_cycle_count
    cycle_payload = explicit_cycle_payload + legacy_cycle_payload

    selector_without_payload = 0
    selector_without_payload_paths: list[str] = []
    for index, record in enumerate(records):
        if record.get("role_id") != "theoretical-continuation-selector":
            continue
        if int(record.get("payload_count", 0)) > 0:
            continue
        next_record = records[index + 1] if index + 1 < len(records) else None
        if not selector_has_constructive_consequence(record, next_record):
            selector_without_payload += 1
            selector_without_payload_paths.append(record.get("completion_path", ""))

    same_burden_max = 0
    same_burden_streak = 0
    current_burden_key = ("", "")
    same_burden_paths: list[str] = []
    current_streak_paths: list[str] = []
    for record in records:
        key = record.get("burden_key", ("", ""))
        has_progress = int(record.get("payload_count", 0)) > 0 or record.get("delta_changed") is True
        if not key or key == ("", ""):
            same_burden_streak = 0
            current_burden_key = ("", "")
            current_streak_paths = []
            continue
        if has_progress:
            same_burden_streak = 0
            current_burden_key = key
            current_streak_paths = []
            continue
        if key != current_burden_key:
            current_burden_key = key
            same_burden_streak = 1
            current_streak_paths = [record.get("completion_path", "")]
        else:
            same_burden_streak += 1
            current_streak_paths.append(record.get("completion_path", ""))
        if same_burden_streak > same_burden_max:
            same_burden_max = same_burden_streak
            same_burden_paths = list(current_streak_paths)

    freeze_reviews = sum(
        1
        for record in records
        if record.get("freeze_repeated_burden") or record.get("freeze_evaluation_required")
    )

    gate_indices = [index for index, record in enumerate(records) if record.get("role_id") == "gate-chair"]
    start_index = gate_indices[-1] + 1 if gate_indices else 0
    bridge_attempts = sum(
        1
        for record in records[start_index:]
        if (
            record.get("role_id") == "candidate-constructor"
            and record.get("candidate_result_type") == "constructed_candidate"
        )
        or record.get("bridge_attempt_present")
    )

    obstruction_ids = {
        record.get("obstruction_id")
        for record in records
        if record.get("obstruction_present") and record.get("obstruction_id")
    }
    missing_obstruction_paths = [
        record.get("completion_path", "")
        for record in records
        if record.get("obstruction_present") and not record.get("obstruction_id")
    ]

    complete_route_cycles = len(complete_families) + legacy_cycle_count
    latest_gate_index = gate_indices[-1] if gate_indices else -1
    post_gate_complete_cycles = 0
    if latest_gate_index >= 0:
        post_gate_records = records[latest_gate_index + 1 :]
        post_gate_complete_cycles = explicit_cycle_summary(post_gate_records)[2].__len__()
        post_gate_complete_cycles += complete_legacy_cycle_count(
            [record for record in post_gate_records if not record.get("cycle_family")]
        )[0]

    gate_ready_without_gate = 0
    gate_ready_paths: list[str] = []
    for index, record in enumerate(records):
        selected = record.get("selected_next_packet_type", "").lower()
        text = record.get("text", "").lower()
        gate_ready = (
            record.get("progress_status") == "candidate_stress_passed_pending_gate"
            or "human_gate" in selected
            or "gate chair" in selected
            or "gate chair" in text and "next" in text
        )
        if not gate_ready:
            continue
        verdict_seen = False
        for next_record in records[index + 1 :]:
            if next_record.get("role_id") == "gate-chair":
                verdict_seen = True
                break
            if next_record.get("role_id") == "candidate-constructor":
                break
        if not verdict_seen:
            gate_ready_without_gate += 1
            gate_ready_paths.append(record.get("completion_path", ""))

    missing_candidate_paths = [
        record.get("completion_path", "")
        for record in records
        if record.get("role_id") == "candidate-constructor"
        and not record.get("candidate_result_type")
    ]

    bridge_no_delta_records = [
        record
        for record in records
        if "bridge" in record.get("text", "").lower()
        and record.get("delta_changed") is False
        and int(record.get("payload_count", 0)) == 0
    ]

    promotion_true = sum(1 for record in records if record.get("physics_promotion_authorized"))
    promotion_false = sum(
        1
        for record in records
        if record.get("has_forbidden_conclusion_summary")
        and not record.get("physics_promotion_authorized")
    )

    payload_density_metrics = {
        "physics_completions_read": len(records),
        "total_payload_items": total_payload,
        "tasks_since_last_distance_to_gr_delta": since_delta,
        "tasks_since_last_burden_discharged": since_burden,
        "new_payload_items_per_physics_task": round(total_payload / len(records), 2),
        "new_payload_items_per_cycle": round(cycle_payload / cycle_count, 2) if cycle_count else 0,
        "selector_cycles_without_new_payload": selector_without_payload,
    }
    route_orbit_risk_metrics = {
        "same_burden_repetition_count": same_burden_max,
        "freeze_reviews_triggered_by_repetition": freeze_reviews,
        "bridge_attempts_since_last_gate": bridge_attempts,
        "obstructions_created": len(obstruction_ids),
        "obstructions_created_missing_id": len(missing_obstruction_paths),
        "obstructions_reused": referenced_obstructions,
        "candidate_construct_audit_stress_selector_cycles": complete_route_cycles,
        "gate_ready_cycles_without_gate_verdict": gate_ready_without_gate,
        "support_only_tooling_reports": support_metrics.get("support_only_checker_reports_found", 0),
        "physics_promotion_authorized_true_count": promotion_true,
        "physics_promotion_authorized_false_count": promotion_false,
    }

    warnings: list[dict[str, Any]] = []
    if same_burden_max > 4:
        warnings.append(
            warning_record(
                "same_burden_repetition",
                "same_burden_repetition_count",
                same_burden_max,
                4,
                same_burden_paths,
                "Require construction, obstruction, gate, freeze review, or a sharper target before another same-burden selector/control-only packet.",
            )
        )
    if selector_without_payload > 2:
        warnings.append(
            warning_record(
                "selector_without_payload_or_consequence",
                "selector_cycles_without_new_payload",
                selector_without_payload,
                2,
                selector_without_payload_paths,
                "Prefer Candidate Constructor, Refuter obstruction/no-go, Gate Chair, or freeze review over another selector-only packet.",
            )
        )
    if post_gate_complete_cycles > 0:
        warnings.append(
            warning_record(
                "post_gate_cycle_repeat",
                "candidate_construct_audit_stress_selector_cycles",
                post_gate_complete_cycles,
                0,
                [record.get("completion_path", "") for record in records[latest_gate_index + 1 :]],
                "Require a harder target, broader finite family, explicit bridge attempt, or freeze-review rationale.",
            )
        )
    if len(bridge_no_delta_records) > 2:
        warnings.append(
            warning_record(
                "claimed_bridge_no_delta",
                "tasks_since_last_distance_to_gr_delta",
                len(bridge_no_delta_records),
                2,
                [record.get("completion_path", "") for record in bridge_no_delta_records],
                "Require payload or narrow the claim language to control-only routing.",
            )
        )
    if missing_candidate_paths:
        warnings.append(
            warning_record(
                "candidate_missing_result",
                "candidate_constructor_result_missing_count",
                len(missing_candidate_paths),
                0,
                missing_candidate_paths,
                "Require a completion receipt repair or a future validator task to make the field mandatory.",
            )
        )
    if gate_ready_without_gate > 0:
        warnings.append(
            warning_record(
                "gate_ready_without_gate",
                "gate_ready_cycles_without_gate_verdict",
                gate_ready_without_gate,
                0,
                gate_ready_paths,
                "Route the next packet to Gate Chair, explain why Gate Chair is not yet lawful, or withdraw gate-ready wording.",
            )
        )
    if missing_obstruction_paths:
        warnings.append(
            warning_record(
                "obstruction_without_id",
                "obstructions_created_missing_id",
                len(missing_obstruction_paths),
                0,
                missing_obstruction_paths,
                "Repair future receipt templates; do not rewrite historical artifacts in this task.",
            )
        )

    support_overread_count = sum(
        int(support_metrics.get(key, 0))
        for key in (
            "support_only_checker_forbidden_overread_reports",
            "support_only_checker_physics_obstruction_reports",
            "support_only_checker_boundary_mismatch_reports",
        )
    )
    if support_overread_count:
        warnings.append(
            warning_record(
                "support_tooling_overread",
                "support_only_tooling_reports",
                support_overread_count,
                0,
                [],
                "Treat as tooling or fixture-quality issue unless a later physics packet lawfully interprets it.",
            )
        )

    return payload_density_metrics, route_orbit_risk_metrics, warnings


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
            completion_record(repo_root, row, completion, is_physics)
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

    input_counts = {
        "tasks_registered": len(task_rows),
        "jobs_registered": len(job_rows),
        "completions_read": len(completion_records),
        "physics_completions_read": sum(1 for row in completion_records if row["is_physics"]),
        "claim_boundary_rows": len(claim_rows),
        "active_claim_boundary_rows": sum(1 for row in claim_rows if row.get("status") == "active"),
    }
    claim_hygiene_metrics = {
        "tasks_with_forbidden_conclusion_summary": forbidden_summary_count,
        "physics_promotion_authorized_true": promotion_authorized_count,
        "physics_promotion_authorized_false": max(0, forbidden_summary_count - promotion_authorized_count),
        "claim_boundary_rows_active": sum(1 for row in claim_rows if row.get("status") == "active"),
    }
    agent_workflow_metrics = {
        **role_metrics,
        "average_tasks_per_construct_audit_stress_cycle": average_cycle,
        "construct_audit_stress_cycle_count": len(cycle_lengths),
        "selector_cycles_without_construction": selector_without_construction,
    }
    support_metrics = collect_support_only_checker_metrics(repo_root)
    operational_validation_metrics = {
        **input_counts,
        "completion_validation_status_counts": dict(sorted(completion_status_counts.items())),
        **claim_hygiene_metrics,
        **agent_workflow_metrics,
        **support_metrics,
    }
    scientific_progress_metrics = {
        "distance_to_gr_delta_true_count": distance_true,
        "distance_to_gr_delta_false_count": distance_false,
        "burden_discharged_count": physics_progress_counts.get("burden_discharged", 0),
        "constructed_candidate_count": (
            physics_progress_counts.get("candidate_constructed_pending_audit", 0)
            + candidate_result_counts.get("constructed_candidate", 0)
        ),
        "candidate_smuggling_audit_pass_count": physics_progress_counts.get(
            "candidate_audited_pending_stress",
            0,
        ),
        "candidate_refuter_stress_pass_count": physics_progress_counts.get(
            "candidate_stress_passed_pending_gate",
            0,
        ),
        "precise_obstruction_count": (
            physics_progress_counts.get("precise_obstruction_found", 0)
            + candidate_result_counts.get("precise_obstruction", 0)
        ),
        "minimal_countermodel_count": candidate_result_counts.get("minimal_countermodel", 0),
        "route_frozen_count": physics_progress_counts.get("route_frozen", 0),
        "human_gate_required_count": physics_progress_counts.get("human_gate_required", 0),
        "obstruction_records_created": len(obstruction_records),
        "obstruction_records_referenced_by_later_tasks": referenced_obstructions,
        "repeated_obstructions_triggering_freeze_review": freeze_review_count,
        "frozen_routes_reopened_by_human_gate": human_gate_freeze_count,
        "physics_progress_status_counts": dict(sorted(physics_progress_counts.items())),
    }
    physics_records = [row for row in completion_records if row["is_physics"]]
    (
        payload_density_metrics,
        route_orbit_risk_metrics,
        diagnostic_warnings,
    ) = collect_payload_density_metrics(
        physics_records,
        support_metrics,
        referenced_obstructions,
    )
    separation_violations = scientific_metric_key_violations(scientific_progress_metrics)
    metrics = {
        "operational_validation_metrics": operational_validation_metrics,
        "scientific_progress_metrics": scientific_progress_metrics,
        "payload_density_metrics": payload_density_metrics,
        "route_orbit_risk_metrics": route_orbit_risk_metrics,
        "diagnostic_warnings": diagnostic_warnings,
        "metric_separation_guard": {
            "status": "pass" if not separation_violations else "fail",
            "operational_metric_key_tokens": sorted(OPERATIONAL_METRIC_KEY_TOKENS),
            "scientific_key_violations": separation_violations,
            "rule": "Operational checker validation registry generated memory wiki receipt role-schema handoff-continuity payload-density route-orbit and diagnostic-warning metrics stay out of scientific_progress_metrics.",
        },
        "input_counts": input_counts,
        "claim_hygiene_metrics": claim_hygiene_metrics,
        "physics_progress_metrics": scientific_progress_metrics,
        "obstruction_reuse_metrics": {
            "obstruction_records_created": len(obstruction_records),
            "obstruction_records_referenced_by_later_tasks": referenced_obstructions,
            "repeated_obstructions_triggering_freeze_review": freeze_review_count,
            "frozen_routes_reopened_by_human_gate": human_gate_freeze_count,
        },
        "agent_workflow_metrics": agent_workflow_metrics,
    }

    return {
        "report_id": "research_control_metrics_separation",
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
            "scoreboards_are_separated": True,
            "physics_claim_promotion_authorized": False,
            "validation_status_is_not_physics_evidence": True,
        },
        "metrics": metrics,
        "limitations": [
            "Operational validation metrics are workflow diagnostics and not physics evidence.",
            "Support-only checker report counts are operational tooling diagnostics; checker syntax or boundary failures are not physics failures.",
            "Scientific progress metrics are counts of tracked science-claim fields and must still cite source artifacts before any claim is reused.",
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


def render_warning_table(warnings: list[dict[str, Any]]) -> list[str]:
    if not warnings:
        return ["No diagnostic warnings were emitted."]
    lines = [
        "| Warning | Metric | Observed | Threshold | Hard Gate | Physics Authority |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for warning in warnings:
        lines.append(
            "| `{warning_id}` | `{metric_key}` | `{observed}` | `{threshold}` | `{hard_gate}` | `{authority}` |".format(
                warning_id=warning.get("warning_id", ""),
                metric_key=warning.get("metric_key", ""),
                observed=warning.get("observed_value", ""),
                threshold=warning.get("threshold", ""),
                hard_gate=warning.get("hard_gate", False),
                authority=warning.get("physics_claim_authority", False),
            )
        )
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    lines: list[str] = [
        "<!-- authority: control -->",
        "",
        "# Research-Control Metrics Separation Report",
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
            "## Operational Validation Metrics",
            "",
            *render_table(metrics["operational_validation_metrics"]),
            "",
            "## Scientific Progress Metrics",
            "",
            *render_table(metrics["scientific_progress_metrics"]),
            "",
            "## Payload-Density Metrics",
            "",
            *render_table(metrics["payload_density_metrics"]),
            "",
            "## Route-Orbit Risk Metrics",
            "",
            *render_table(metrics["route_orbit_risk_metrics"]),
            "",
            "## Diagnostic Warnings",
            "",
            *render_warning_table(metrics["diagnostic_warnings"]),
            "",
            "## Separation Guard",
            "",
            *render_table(metrics["metric_separation_guard"]),
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
            "This report provides separated operational and scientific scoreboards for future evaluation. The metrics show workflow health separately from tracked science-result fields. They do not change the authority of any scientific artifact.",
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
