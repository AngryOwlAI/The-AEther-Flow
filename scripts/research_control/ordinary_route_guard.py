#!/usr/bin/env python3
"""Prospective ordinary-route guard for consecutive project-system work.

This module is project-control only.  It classifies tracked route history and
v21 backlog readiness; it does not evaluate scientific truth or create
physics, ontology, promotion, proof, or publication authority.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_ID = "ordinary_route_guard_policy_v1"
EVALUATION_SCHEMA_ID = "ordinary_route_guard_evaluation_v1"
ADMISSION_SCHEMA_ID = "ordinary_route_guard_admission_v1"
EXCEPTION_SCHEMA_ID = "ordinary_route_exception_receipt_v1"
CONTROL_FAILURE_SCHEMA_ID = "ordinary_route_control_failure_v1"
REQUIRED_AFTER = "2026-07-22T19:00:53Z"
THRESHOLD = 3
BACKLOG_PATH = "research_control/design/v21_recommendation_backlog.yaml"
TASK_REGISTRY_PATH = "registries/RESEARCH_TASK_REGISTRY.csv"
JOB_REGISTRY_PATH = "registries/AGENT_JOB_REGISTRY.csv"
HANDOFF_PATH_RE = re.compile(r"^research_control/handoffs/handoff-\d{4}\.yaml$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FAILURE_CLASSES = {
    "failing_ci",
    "registry_corruption",
    "claim_boundary_hard_failure",
    "human_gate_required",
    "security_or_integrity_repair",
}
AUTHORITY_LIMITS = {
    "ordinary_research_handoff_authoritative": True,
    "project_system_sidecar_supersedes": False,
    "system_success_counts_as_physics": False,
    "system_success_counts_as_distance_to_gr": False,
    "scientific_status_changed": False,
    "physics_promotion_authorized": False,
}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _int_value(value: Any, default: int = -1) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _read_csv(repo_root: Path, rel_path: str) -> list[dict[str, str]]:
    with (repo_root / rel_path).open(newline="", encoding="utf-8") as handle:
        return [
            {key: value or "" for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_repo_path(repo_root: Path, rel_path: str) -> Path | None:
    if not rel_path or rel_path.startswith("/") or rel_path.startswith(".local/"):
        return None
    parts = Path(rel_path).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        return None
    candidate = (repo_root / rel_path).resolve()
    root = repo_root.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _tracked_paths(repo_root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return set()
    return {
        item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    }


def policy_active(created_at: Any) -> bool:
    """The implementation AgentJob at the exact activation instant is exempt."""

    return bool(_text(created_at) and _text(created_at) > REQUIRED_AFTER)


def ordinary_route_guard_policy() -> dict[str, Any]:
    return {
        "policy_id": POLICY_ID,
        "required_after": REQUIRED_AFTER,
        "threshold": THRESHOLD,
        "enforcement": "prospective_hard_failure",
        "warning_at": THRESHOLD - 1,
        "failure_classes": sorted(FAILURE_CLASSES),
        "historical_missing_record_status": "legacy_readable",
        "authority_limits": dict(AUTHORITY_LIMITS),
    }


def _task_record(repo_root: Path, task_path: str) -> dict[str, Any]:
    path = repo_root / task_path / "00_TASK.yaml"
    if not path.is_file():
        return {}
    try:
        return _load_mapping(path)
    except (OSError, ValueError, yaml.YAMLError):
        return {}


def _job_record(repo_root: Path, job_path: str) -> dict[str, Any]:
    path = repo_root / job_path
    if not path.is_file():
        return {}
    try:
        return _load_mapping(path)
    except (OSError, ValueError, yaml.YAMLError):
        return {}


def completed_plan_task_ids(repo_root: Path, as_of: str) -> set[str]:
    completed: set[str] = set()
    for row in _read_csv(repo_root, TASK_REGISTRY_PATH):
        closed_at = _text(row.get("closed_at"))
        if row.get("status") != "completed" or not closed_at or closed_at > as_of:
            continue
        task = _task_record(repo_root, row.get("task_path", ""))
        plan = _dict(task.get("implementation_plan"))
        plan_task_id = _text(plan.get("plan_task_id") or task.get("plan_task_id"))
        v21_identity = (
            _text(plan.get("plan_id"))
            == "recommendations_implementation_plan_continue_task-v21"
            or _text(task.get("task_type")).startswith("v21_")
            or _text(task.get("claim_boundary_id")).startswith("CB-V21-")
        )
        if plan_task_id and v21_identity:
            completed.add(plan_task_id)
    backlog_by_id = {
        _text(item.get("plan_task_id")): item
        for item in _load_backlog(repo_root)
        if _text(item.get("plan_task_id"))
    }
    pending = list(completed)
    while pending:
        item = backlog_by_id.get(pending.pop(), {})
        for dependency in _list(item.get("depends_on")):
            dependency_id = _text(dependency)
            if dependency_id and dependency_id not in completed:
                completed.add(dependency_id)
                pending.append(dependency_id)
    return completed


def _load_backlog(repo_root: Path) -> list[dict[str, Any]]:
    value = _load_mapping(repo_root / BACKLOG_PATH)
    return [item for item in _list(value.get("items")) if isinstance(item, dict)]


def discover_ready_science_routes(repo_root: Path, as_of: str) -> list[dict[str, Any]]:
    """Return dependency-ready, incomplete v21 science routes as of a handoff."""

    completed = completed_plan_task_ids(repo_root, as_of)
    ready: list[dict[str, Any]] = []
    for item in _load_backlog(repo_root):
        plan_task_id = _text(item.get("plan_task_id"))
        if not plan_task_id or plan_task_id in completed:
            continue
        if _text(item.get("task_class")) != "science":
            continue
        dependencies = [_text(value) for value in _list(item.get("depends_on")) if _text(value)]
        if any(dependency not in completed for dependency in dependencies):
            continue
        ready.append(
            {
                "plan_task_id": plan_task_id,
                "work_kind": _text(item.get("work_kind")),
                "route_label": _text(item.get("route_label")),
                "worker_skill": _text(item.get("worker_skill")),
                "requires_human_gate": item.get("requires_human_gate") is True,
                "dependencies": dependencies,
            }
        )
    return ready


def derive_consecutive_project_system_tasks(repo_root: Path, as_of: str) -> int:
    """Count the trailing run using normalized explicit task scope."""

    task_rows = {
        row.get("task_id", ""): row
        for row in _read_csv(repo_root, TASK_REGISTRY_PATH)
        if row.get("task_id")
    }
    completed_jobs = [
        row
        for row in _read_csv(repo_root, JOB_REGISTRY_PATH)
        if row.get("status") == "completed"
        and row.get("completed_at")
        and row["completed_at"] <= as_of
    ]
    completed_jobs.sort(key=lambda row: (row.get("completed_at", ""), row.get("job_id", "")))
    run_length = 0
    for row in reversed(completed_jobs):
        task_row = task_rows.get(row.get("task_id", ""), {})
        task = _task_record(repo_root, task_row.get("task_path", ""))
        scope = _text(_dict(task.get("task_taxonomy")).get("scope"))
        job = _job_record(repo_root, row.get("job_path", ""))
        admission_path = _text(_dict(job.get("physics_payload_admission")).get("admission_path"))
        category = _text(_dict(job.get("dual_budget_allocation")).get("category"))
        project_system = scope == "project_system" and admission_path != "physics"
        if category in {"physics_bearing", "mixed"}:
            project_system = False
        if not project_system:
            break
        run_length += 1
    return run_length


def _validate_authority_limits(record: dict[str, Any], errors: list[str]) -> None:
    limits = record.get("authority_limits")
    if not isinstance(limits, dict):
        errors.append("authority_limits_missing_or_not_mapping")
        return
    for field_name, expected in AUTHORITY_LIMITS.items():
        if limits.get(field_name) is not expected:
            errors.append(f"authority_limits_{field_name}_must_be_{str(expected).lower()}")


def _validate_evidence(
    blocked_route: dict[str, Any],
    ready_route: dict[str, Any],
    repo_root: Path,
    tracked_paths: set[str],
    errors: list[str],
) -> None:
    plan_task_id = _text(ready_route.get("plan_task_id"))
    prefix = f"blocked_route_{plan_task_id}"
    failure_class = _text(blocked_route.get("failure_class"))
    if failure_class not in FAILURE_CLASSES:
        errors.append(f"{prefix}_failure_class_invalid")
        return
    evidence_path = _text(blocked_route.get("evidence_path"))
    evidence_sha256 = _text(blocked_route.get("evidence_sha256"))
    path = _safe_repo_path(repo_root, evidence_path)
    if path is None or not path.is_file() or path.is_symlink():
        errors.append(f"{prefix}_evidence_path_not_regular")
        return
    if evidence_path not in tracked_paths:
        errors.append(f"{prefix}_evidence_path_not_tracked")
    if not SHA256_RE.fullmatch(evidence_sha256) or _sha256(path) != evidence_sha256:
        errors.append(f"{prefix}_evidence_hash_mismatch")
        return
    if failure_class == "human_gate_required":
        if evidence_path != BACKLOG_PATH or ready_route.get("requires_human_gate") is not True:
            errors.append(f"{prefix}_human_gate_not_authorized_by_backlog")
        return
    try:
        evidence = _load_mapping(path)
    except (OSError, ValueError, yaml.YAMLError):
        errors.append(f"{prefix}_evidence_unreadable")
        return
    if evidence.get("schema_id") != CONTROL_FAILURE_SCHEMA_ID:
        errors.append(f"{prefix}_evidence_schema_invalid")
    if _text(evidence.get("plan_task_id")) != plan_task_id:
        errors.append(f"{prefix}_evidence_plan_task_id_mismatch")
    if _text(evidence.get("failure_class")) != failure_class:
        errors.append(f"{prefix}_evidence_failure_class_mismatch")
    if evidence.get("status") != "active_blocking":
        errors.append(f"{prefix}_evidence_status_not_active_blocking")
    if evidence.get("blocks_scientific_execution") is not True:
        errors.append(f"{prefix}_evidence_does_not_block_scientific_execution")


def _validate_exception(
    receipt: Any,
    ready_routes: list[dict[str, Any]],
    handoff_id: str,
    repo_root: Path,
    tracked_paths: set[str],
    errors: list[str],
) -> None:
    if not isinstance(receipt, dict) or receipt.get("active") is not True:
        errors.append("active_exception_receipt_required")
        return
    if receipt.get("schema_id") != EXCEPTION_SCHEMA_ID:
        errors.append("exception_schema_id_invalid")
    if _text(receipt.get("exception_class")) != "all_ready_science_blocked":
        errors.append("exception_class_invalid")
    if _text(receipt.get("ordinary_handoff_id")) != handoff_id:
        errors.append("exception_ordinary_handoff_id_mismatch")
    expected_ids = [_text(route.get("plan_task_id")) for route in ready_routes]
    declared_ids = [_text(item) for item in _list(receipt.get("ready_science_plan_task_ids"))]
    if declared_ids != expected_ids:
        errors.append("exception_ready_science_ids_mismatch")
    blocked = [item for item in _list(receipt.get("blocked_routes")) if isinstance(item, dict)]
    by_id: dict[str, dict[str, Any]] = {}
    for item in blocked:
        plan_task_id = _text(item.get("plan_task_id"))
        if not plan_task_id or plan_task_id in by_id:
            errors.append("exception_blocked_route_ids_missing_or_duplicate")
            continue
        by_id[plan_task_id] = item
    if set(by_id) != set(expected_ids):
        errors.append("exception_does_not_account_for_all_ready_science")
    for ready_route in ready_routes:
        plan_task_id = _text(ready_route.get("plan_task_id"))
        if plan_task_id in by_id:
            _validate_evidence(
                by_id[plan_task_id],
                ready_route,
                repo_root,
                tracked_paths,
                errors,
            )
    _validate_authority_limits(receipt, errors)


def evaluate_guard_record(
    record: Any,
    *,
    handoff_id: str,
    selected_plan_task_id: str,
    selected_plan_item: dict[str, Any],
    ready_science_routes: list[dict[str, Any]],
    observed_run_length: int,
    repo_root: Path,
    tracked_paths: set[str] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(record, dict):
        return {
            "status": "FAIL",
            "errors": ["ordinary_route_guard_missing_or_not_mapping"],
            "warnings": [],
        }
    if record.get("schema_id") != EVALUATION_SCHEMA_ID:
        errors.append("evaluation_schema_id_invalid")
    if record.get("policy_id") != POLICY_ID:
        errors.append("policy_id_invalid")
    if _text(record.get("ordinary_handoff_id")) != handoff_id:
        errors.append("ordinary_handoff_id_mismatch")
    if _int_value(record.get("threshold")) != THRESHOLD:
        errors.append("threshold_mismatch")
    if (
        _int_value(record.get("consecutive_project_system_tasks_before_selection"))
        != observed_run_length
    ):
        errors.append("consecutive_project_system_task_count_mismatch")
    expected_ready_ids = [_text(route.get("plan_task_id")) for route in ready_science_routes]
    declared_ready_ids = [_text(item) for item in _list(record.get("ready_science_plan_task_ids"))]
    if declared_ready_ids != expected_ready_ids:
        errors.append("ready_science_plan_task_ids_mismatch")
    if _text(record.get("selected_plan_task_id")) != selected_plan_task_id:
        errors.append("selected_plan_task_id_mismatch")
    selected_is_science = _text(selected_plan_item.get("task_class")) == "science"
    selected_requires_gate = selected_plan_item.get("requires_human_gate") is True
    expected_route_class = "physics_bearing" if selected_is_science else "project_system"
    if _text(record.get("selected_route_class")) != expected_route_class:
        errors.append("selected_route_class_mismatch")
    if _text(record.get("selected_worker_skill")) != _text(selected_plan_item.get("worker_skill")):
        errors.append("selected_worker_skill_mismatch")
    if record.get("ordinary_research_handoff_authoritative") is not True:
        errors.append("ordinary_research_handoff_not_authoritative")
    if record.get("project_system_sidecar_supersedes") is not False:
        errors.append("project_system_sidecar_supersedes_must_be_false")
    _validate_authority_limits(record, errors)

    receipt = record.get("exception_receipt")
    if observed_run_length == THRESHOLD - 1:
        warnings.append("ordinary_route_guard_threshold_next")
    if observed_run_length < THRESHOLD:
        expected_outcome = "below_threshold"
        if isinstance(receipt, dict) and receipt.get("active") is True:
            errors.append("exception_not_allowed_below_threshold")
    elif selected_is_science and not selected_requires_gate:
        expected_outcome = "physics_bearing_route_selected"
        if selected_plan_task_id not in expected_ready_ids:
            errors.append("selected_physics_route_not_dependency_ready")
        if isinstance(receipt, dict) and receipt.get("active") is True:
            errors.append("exception_not_allowed_when_physics_route_selected")
    elif selected_is_science and selected_requires_gate:
        expected_outcome = "blocked"
        errors.append("selected_physics_route_requires_unprovided_human_gate")
    else:
        expected_outcome = "all_ready_science_blocked_exception"
        _validate_exception(
            receipt,
            ready_science_routes,
            handoff_id,
            repo_root,
            tracked_paths if tracked_paths is not None else _tracked_paths(repo_root),
            errors,
        )
    if _text(record.get("outcome")) != expected_outcome:
        errors.append("outcome_mismatch")
    return {
        "status": "FAIL" if errors else "WARN" if warnings else "PASS",
        "errors": errors,
        "warnings": warnings,
        "observed_run_length": observed_run_length,
        "ready_science_plan_task_ids": expected_ready_ids,
        "selected_plan_task_id": selected_plan_task_id,
        "expected_outcome": expected_outcome,
    }


def evaluate_research_handoff_guard(
    handoff: Any,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    if not isinstance(handoff, dict):
        return {"status": "FAIL", "errors": ["handoff_not_mapping"], "warnings": []}
    created_at = _text(handoff.get("created_at"))
    if not policy_active(created_at):
        return {
            "status": "LEGACY_READABLE",
            "errors": [],
            "warnings": [],
            "policy_required": False,
        }
    handoff_id = _text(handoff.get("handoff_id"))
    selected = _dict(handoff.get("selected_next_route"))
    selected_plan_task_id = _text(selected.get("plan_task_id"))
    backlog = _load_backlog(repo_root)
    selected_item = next(
        (item for item in backlog if _text(item.get("plan_task_id")) == selected_plan_task_id),
        {},
    )
    if not selected_item:
        return {
            "status": "FAIL",
            "errors": ["selected_plan_task_not_in_v21_backlog"],
            "warnings": [],
            "policy_required": True,
        }
    result = evaluate_guard_record(
        handoff.get("ordinary_route_guard"),
        handoff_id=handoff_id,
        selected_plan_task_id=selected_plan_task_id,
        selected_plan_item=selected_item,
        ready_science_routes=discover_ready_science_routes(repo_root, created_at),
        observed_run_length=derive_consecutive_project_system_tasks(repo_root, created_at),
        repo_root=repo_root,
    )
    result["policy_required"] = True
    return result


def evaluate_agent_job_route_admission(
    job: Any,
    *,
    created_at: str,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    if not policy_active(created_at):
        return {
            "status": "LEGACY_READABLE",
            "errors": [],
            "warnings": [],
            "policy_required": False,
        }
    errors: list[str] = []
    if not isinstance(job, dict):
        return {"status": "FAIL", "errors": ["job_not_mapping"], "warnings": []}
    admission = job.get("ordinary_route_guard_admission")
    if not isinstance(admission, dict):
        return {
            "status": "FAIL",
            "errors": ["ordinary_route_guard_admission_missing_or_not_mapping"],
            "warnings": [],
            "policy_required": True,
        }
    if admission.get("schema_id") != ADMISSION_SCHEMA_ID:
        errors.append("admission_schema_id_invalid")
    if admission.get("policy_id") != POLICY_ID:
        errors.append("admission_policy_id_invalid")
    source_path = _text(admission.get("source_handoff_path"))
    source_sha256 = _text(admission.get("source_handoff_sha256"))
    path = _safe_repo_path(repo_root, source_path)
    if not HANDOFF_PATH_RE.fullmatch(source_path) or path is None or not path.is_file() or path.is_symlink():
        errors.append("source_handoff_path_invalid")
        return {"status": "FAIL", "errors": errors, "warnings": [], "policy_required": True}
    if source_path not in _tracked_paths(repo_root):
        errors.append("source_handoff_not_tracked")
    if not SHA256_RE.fullmatch(source_sha256) or _sha256(path) != source_sha256:
        errors.append("source_handoff_hash_mismatch")
        return {"status": "FAIL", "errors": errors, "warnings": [], "policy_required": True}
    try:
        handoff = _load_mapping(path)
    except (OSError, ValueError, yaml.YAMLError):
        errors.append("source_handoff_unreadable")
        return {"status": "FAIL", "errors": errors, "warnings": [], "policy_required": True}
    handoff_result = evaluate_research_handoff_guard(handoff, repo_root)
    errors.extend(f"source_handoff:{error}" for error in handoff_result.get("errors", []))
    if _text(admission.get("source_handoff_id")) != _text(handoff.get("handoff_id")):
        errors.append("source_handoff_id_mismatch")
    plan_task_id = _text(job.get("plan_task_id"))
    selected_plan_task_id = _text(_dict(handoff.get("selected_next_route")).get("plan_task_id"))
    if not plan_task_id or plan_task_id != selected_plan_task_id:
        errors.append("job_plan_task_id_not_selected_by_handoff")
    if _text(admission.get("selected_plan_task_id")) != selected_plan_task_id:
        errors.append("admission_selected_plan_task_id_mismatch")
    if _text(admission.get("guard_outcome")) != _text(
        _dict(handoff.get("ordinary_route_guard")).get("outcome")
    ):
        errors.append("admission_guard_outcome_mismatch")
    _validate_authority_limits(admission, errors)
    return {
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "warnings": handoff_result.get("warnings", []),
        "policy_required": True,
    }


def canonical_json_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


__all__ = [
    "ADMISSION_SCHEMA_ID",
    "AUTHORITY_LIMITS",
    "BACKLOG_PATH",
    "CONTROL_FAILURE_SCHEMA_ID",
    "EVALUATION_SCHEMA_ID",
    "EXCEPTION_SCHEMA_ID",
    "FAILURE_CLASSES",
    "POLICY_ID",
    "REQUIRED_AFTER",
    "THRESHOLD",
    "canonical_json_hash",
    "completed_plan_task_ids",
    "derive_consecutive_project_system_tasks",
    "discover_ready_science_routes",
    "evaluate_agent_job_route_admission",
    "evaluate_guard_record",
    "evaluate_research_handoff_guard",
    "ordinary_route_guard_policy",
    "policy_active",
]
