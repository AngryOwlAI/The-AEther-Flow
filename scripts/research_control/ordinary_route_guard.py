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
PROTECTED_HUMAN_OVERRIDE_SCHEMA_ID = (
    "protected_human_route_override_admission_v1"
)
PROTECTED_HUMAN_OVERRIDE_HASH_REQUIRED_AFTER = "2026-07-24T16:00:00Z"
EXCEPTION_SCHEMA_ID = "ordinary_route_exception_receipt_v1"
CONTROL_FAILURE_SCHEMA_ID = "ordinary_route_control_failure_v1"
REQUIRED_AFTER = "2026-07-22T19:00:53Z"
THRESHOLD = 3
BACKLOG_PATH = "research_control/design/v21_recommendation_backlog.yaml"
TASK_REGISTRY_PATH = "registries/RESEARCH_TASK_REGISTRY.csv"
JOB_REGISTRY_PATH = "registries/AGENT_JOB_REGISTRY.csv"
HANDOFF_PATH_RE = re.compile(r"^research_control/handoffs/handoff-\d{4}\.yaml$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
TASK_ID_RE = re.compile(r"^RT-\d{8}-\d{3}$")
JOB_ID_RE = re.compile(r"^AJ-(RT-\d{8}-\d{3})-\d{3}$")
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


def _load_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} must begin with YAML frontmatter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError(f"{path} has unterminated YAML frontmatter") from exc
    value = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(value, dict):
        raise ValueError(f"{path} frontmatter must contain a mapping")
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


def _repository_candidate_paths(repo_root: Path) -> set[str]:
    """Return tracked files plus non-ignored files pending in this transaction."""

    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
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


def _validate_bound_mapping(
    *,
    repo_root: Path,
    path_text: str,
    expected_sha256: str,
    candidate_paths: set[str],
    error_prefix: str,
    errors: list[str],
    frontmatter: bool = False,
) -> dict[str, Any]:
    path = _safe_repo_path(repo_root, path_text)
    if path is None or not path.is_file() or path.is_symlink():
        errors.append(f"{error_prefix}_path_not_regular")
        return {}
    if path_text not in candidate_paths:
        errors.append(f"{error_prefix}_path_not_repository_candidate")
    if not SHA256_RE.fullmatch(expected_sha256) or _sha256(path) != expected_sha256:
        errors.append(f"{error_prefix}_hash_mismatch")
        return {}
    try:
        return _load_frontmatter(path) if frontmatter else _load_mapping(path)
    except (OSError, ValueError, yaml.YAMLError):
        errors.append(f"{error_prefix}_unreadable")
        return {}


def _normalized_goal_route(record: dict[str, Any]) -> dict[str, Any]:
    goal = _dict(record.get("goal_receipt"))
    return {
        "goal_id": _text(goal.get("goal_id")),
        "generation": _int_value(goal.get("generation")),
        "plan_task_id": _text(
            goal.get("route_work_item_id")
            or goal.get("route_plan_task_id")
            or goal.get("plan_task_id")
        ),
        "worker_skill": _text(
            goal.get("route_worker_skill") or goal.get("worker_skill")
        ),
        "route_sha256": _text(
            goal.get("route_sha256")
            or goal.get("immutable_route_hash")
            or goal.get("immutable_route_sha256")
        ),
        "idempotency_key": _text(goal.get("idempotency_key")),
    }


def _validate_declared_goal_route(
    declared: dict[str, Any],
    observed: dict[str, Any],
    *,
    prefix: str,
    errors: list[str],
) -> None:
    for field_name in (
        "goal_id",
        "generation",
        "plan_task_id",
        "worker_skill",
        "route_sha256",
        "idempotency_key",
    ):
        if declared.get(field_name) != observed.get(field_name):
            errors.append(f"{prefix}_{field_name}_mismatch")
    goal_id = _text(declared.get("goal_id"))
    generation = _int_value(declared.get("generation"))
    if not goal_id or generation < 0:
        errors.append(f"{prefix}_identity_invalid")
    if not SHA256_RE.fullmatch(_text(declared.get("route_sha256"))):
        errors.append(f"{prefix}_route_sha256_invalid")
    if _text(declared.get("idempotency_key")) != f"{goal_id}:{generation}":
        errors.append(f"{prefix}_idempotency_key_invalid")


def _approval_job_uses(repo_root: Path, approval_id: str) -> list[str]:
    uses: list[str] = []
    jobs_root = repo_root / "research_control" / "tasks"
    for path in jobs_root.glob("RT-*/jobs/AJ-*.yaml"):
        if path.is_symlink() or not path.is_file():
            continue
        try:
            record = _load_mapping(path)
        except (OSError, ValueError, yaml.YAMLError):
            continue
        if _text(record.get("approval_id")) == approval_id:
            uses.append(_text(record.get("job_id")))
    return sorted(value for value in uses if value)


def _validate_protected_human_override(
    *,
    job: dict[str, Any],
    admission: dict[str, Any],
    handoff: dict[str, Any],
    created_at: str,
    repo_root: Path,
    errors: list[str],
) -> bool:
    override = admission.get("override_authority")
    if not isinstance(override, dict) or override.get("present") is not True:
        return False

    job_id = _text(job.get("job_id"))
    task_id = _text(job.get("task_id"))
    decision_id = _text(job.get("decision_id"))
    plan_task_id = _text(job.get("plan_task_id"))
    if not JOB_ID_RE.fullmatch(job_id) or not TASK_ID_RE.fullmatch(task_id):
        errors.append("protected_override_admitted_job_identity_invalid")
        return True
    if _text(override.get("exact_plan_task_id")) != plan_task_id:
        errors.append("protected_override_exact_plan_task_id_mismatch")

    deterministic_receipt_path = (
        f"research_control/tasks/{task_id}/artifacts/"
        "protected_human_route_override_admission_v1.yaml"
    )
    receipt_path_text = _text(override.get("receipt_path")) or deterministic_receipt_path
    if receipt_path_text != deterministic_receipt_path:
        errors.append("protected_override_receipt_path_not_deterministic")
        return True
    receipt_path = _safe_repo_path(repo_root, receipt_path_text)
    candidate_paths = _repository_candidate_paths(repo_root)
    if (
        receipt_path is None
        or not receipt_path.is_file()
        or receipt_path.is_symlink()
    ):
        errors.append("protected_override_receipt_path_not_regular")
        return True
    if receipt_path_text not in candidate_paths:
        errors.append("protected_override_receipt_not_repository_candidate")
    receipt_sha256 = _text(override.get("receipt_sha256"))
    if created_at > PROTECTED_HUMAN_OVERRIDE_HASH_REQUIRED_AFTER:
        if not SHA256_RE.fullmatch(receipt_sha256):
            errors.append("protected_override_receipt_sha256_required")
        elif _sha256(receipt_path) != receipt_sha256:
            errors.append("protected_override_receipt_hash_mismatch")
    elif receipt_sha256 and (
        not SHA256_RE.fullmatch(receipt_sha256)
        or _sha256(receipt_path) != receipt_sha256
    ):
        errors.append("protected_override_receipt_hash_mismatch")
    try:
        receipt = _load_mapping(receipt_path)
    except (OSError, ValueError, yaml.YAMLError):
        errors.append("protected_override_receipt_unreadable")
        return True

    if receipt.get("schema_id") != PROTECTED_HUMAN_OVERRIDE_SCHEMA_ID:
        errors.append("protected_override_schema_id_invalid")
    if receipt.get("policy_id") != POLICY_ID:
        errors.append("protected_override_policy_id_invalid")
    if receipt.get("status") != "active":
        errors.append("protected_override_status_not_active")
    purpose = _text(receipt.get("admission_purpose"))
    if purpose not in {"protected_execution", "checkpoint_recovery"}:
        errors.append("protected_override_purpose_invalid")

    admitted = _dict(receipt.get("admitted_job"))
    admitted_expected = {
        "job_id": job_id,
        "task_id": task_id,
        "decision_id": decision_id,
        "plan_task_id": plan_task_id,
    }
    for field_name, expected in admitted_expected.items():
        if _text(admitted.get(field_name)) != expected:
            errors.append(f"protected_override_admitted_{field_name}_mismatch")

    protected = _dict(receipt.get("protected_job"))
    protected_job_id = _text(protected.get("job_id"))
    protected_task_id = _text(protected.get("task_id"))
    protected_decision_id = _text(protected.get("decision_id"))
    protected_plan_task_id = _text(protected.get("plan_task_id"))
    if (
        not JOB_ID_RE.fullmatch(protected_job_id)
        or not TASK_ID_RE.fullmatch(protected_task_id)
        or protected_plan_task_id != plan_task_id
    ):
        errors.append("protected_override_protected_job_identity_invalid")
        return True
    protected_job_path_text = (
        f"research_control/tasks/{protected_task_id}/jobs/{protected_job_id}.yaml"
    )
    protected_job_path = _safe_repo_path(repo_root, protected_job_path_text)
    if protected_job_id == job_id:
        protected_job = job
    elif (
        protected_job_path is None
        or not protected_job_path.is_file()
        or protected_job_path.is_symlink()
    ):
        errors.append("protected_override_protected_job_path_not_regular")
        return True
    else:
        if protected_job_path_text not in candidate_paths:
            errors.append("protected_override_protected_job_not_repository_candidate")
        try:
            protected_job = _load_mapping(protected_job_path)
        except (OSError, ValueError, yaml.YAMLError):
            errors.append("protected_override_protected_job_unreadable")
            return True
    for field_name, expected in (
        ("job_id", protected_job_id),
        ("task_id", protected_task_id),
        ("decision_id", protected_decision_id),
        ("plan_task_id", protected_plan_task_id),
    ):
        if _text(protected_job.get(field_name)) != expected:
            errors.append(f"protected_override_protected_job_{field_name}_mismatch")

    if purpose == "protected_execution":
        if protected_job_id != job_id:
            errors.append("protected_execution_job_identity_mismatch")
    else:
        if protected_job_id == job_id:
            errors.append("checkpoint_recovery_requires_distinct_admitted_job")
        if _text(job.get("role_id")) != "validator-engineer":
            errors.append("checkpoint_recovery_role_must_be_validator_engineer")
        if _text(_dict(job.get("physics_payload_admission")).get("admission_path")) != "project_system":
            errors.append("checkpoint_recovery_must_be_project_system")
        if _text(job.get("approval_id")) or _text(job.get("human_authorization_id")):
            errors.append("checkpoint_recovery_must_not_reuse_protected_approval")

    source = _dict(receipt.get("source_handoff"))
    actual_selected = _text(_dict(handoff.get("selected_next_route")).get("plan_task_id"))
    for field_name, expected in (
        ("handoff_id", _text(handoff.get("handoff_id"))),
        ("path", _text(admission.get("source_handoff_path"))),
        ("sha256", _text(admission.get("source_handoff_sha256"))),
        ("selected_plan_task_id", actual_selected),
        (
            "guard_outcome",
            _text(_dict(handoff.get("ordinary_route_guard")).get("outcome")),
        ),
    ):
        if _text(source.get(field_name)) != expected:
            errors.append(f"protected_override_source_handoff_{field_name}_mismatch")

    approval_record = _dict(receipt.get("approval"))
    approval_id = _text(approval_record.get("approval_id"))
    approval_path_text = _text(approval_record.get("path"))
    expected_approval_path = f"research_control/approvals/{approval_id}.yaml"
    if approval_path_text != expected_approval_path:
        errors.append("protected_override_approval_path_not_canonical")
    approval = _validate_bound_mapping(
        repo_root=repo_root,
        path_text=approval_path_text,
        expected_sha256=_text(approval_record.get("sha256")),
        candidate_paths=candidate_paths,
        error_prefix="protected_override_approval",
        errors=errors,
    )
    protected_approval_id = _text(protected_job.get("approval_id"))
    protected_human_authorization_id = _text(
        protected_job.get("human_authorization_id")
    )
    if approval_id != protected_approval_id:
        errors.append("protected_override_approval_id_mismatch")
    for field_name, expected in (
        ("approval_id", approval_id),
        ("decision_id", protected_decision_id),
        ("human_authorization_id", protected_human_authorization_id),
        ("status", "consumed"),
        ("consumed_by", protected_job_id),
        ("expires_at", protected_job_id),
    ):
        if _text(approval.get(field_name)) != expected:
            errors.append(f"protected_override_approval_{field_name}_mismatch")
    if approval.get("one_time_use") is not True:
        errors.append("protected_override_approval_not_one_time_use")
    if not _text(approval.get("scope")):
        errors.append("protected_override_approval_scope_missing")
    protected_scope = _dict(approval.get("protected_scope"))
    if not _list(protected_scope.get("must_not_authorize")):
        errors.append("protected_override_approval_non_authorizations_missing")
    if _approval_job_uses(repo_root, approval_id) != [protected_job_id]:
        errors.append("protected_override_approval_reused_or_ambiguous")

    decision_record = _dict(receipt.get("director_decision"))
    decision_path_text = _text(decision_record.get("path"))
    expected_decision_path = (
        f"research_control/tasks/{protected_task_id}/{protected_decision_id}.md"
    )
    if decision_path_text != expected_decision_path:
        errors.append("protected_override_director_decision_path_not_canonical")
    decision = _validate_bound_mapping(
        repo_root=repo_root,
        path_text=decision_path_text,
        expected_sha256=_text(decision_record.get("sha256")),
        candidate_paths=candidate_paths,
        error_prefix="protected_override_director_decision",
        errors=errors,
        frontmatter=True,
    )
    for field_name, expected in (
        ("decision_id", protected_decision_id),
        ("task_id", protected_task_id),
        ("agent_job_id", protected_job_id),
        ("approval_id", approval_id),
        ("human_authorization_id", protected_human_authorization_id),
    ):
        if _text(decision.get(field_name)) != expected:
            errors.append(
                f"protected_override_director_decision_{field_name}_mismatch"
            )

    authorization_record = _dict(receipt.get("human_authorization"))
    authorization_path_text = _text(authorization_record.get("path"))
    authorization = _validate_bound_mapping(
        repo_root=repo_root,
        path_text=authorization_path_text,
        expected_sha256=_text(authorization_record.get("sha256")),
        candidate_paths=candidate_paths,
        error_prefix="protected_override_human_authorization",
        errors=errors,
    )
    decision_code = _text(approval.get("decision_code"))
    for field_name, expected in (
        ("task_id", protected_task_id),
        ("job_id", protected_job_id),
        ("approval_id", approval_id),
        ("human_authorization_id", protected_human_authorization_id),
        ("decision_code", decision_code),
        ("status", "consumed"),
    ):
        if _text(authorization.get(field_name)) != expected:
            errors.append(
                f"protected_override_human_authorization_{field_name}_mismatch"
            )
    if not _list(authorization.get("non_authorizations")):
        errors.append("protected_override_human_authorization_limits_missing")

    protected_route_record = _dict(receipt.get("protected_route"))
    protected_route_path_text = _text(protected_route_record.get("evidence_path"))
    protected_completion = _validate_bound_mapping(
        repo_root=repo_root,
        path_text=protected_route_path_text,
        expected_sha256=_text(protected_route_record.get("evidence_sha256")),
        candidate_paths=candidate_paths,
        error_prefix="protected_override_protected_route_evidence",
        errors=errors,
    )
    for field_name, expected in (
        ("job_id", protected_job_id),
        ("task_id", protected_task_id),
        ("decision_id", protected_decision_id),
    ):
        if _text(protected_completion.get(field_name)) != expected:
            errors.append(
                f"protected_override_protected_route_{field_name}_mismatch"
            )
    observed_protected_route = _normalized_goal_route(protected_completion)
    _validate_declared_goal_route(
        protected_route_record,
        observed_protected_route,
        prefix="protected_override_protected_route",
        errors=errors,
    )
    if observed_protected_route.get("plan_task_id") != protected_plan_task_id:
        errors.append("protected_override_protected_route_plan_task_id_mismatch")

    observed_admitted_route = (
        _normalized_goal_route(job)
        if isinstance(job.get("goal_receipt"), dict)
        else observed_protected_route
    )
    admitted_route_record = _dict(receipt.get("admitted_route"))
    _validate_declared_goal_route(
        admitted_route_record,
        observed_admitted_route,
        prefix="protected_override_admitted_route",
        errors=errors,
    )
    if observed_admitted_route.get("plan_task_id") != plan_task_id:
        errors.append("protected_override_admitted_route_plan_task_id_mismatch")
    if purpose == "protected_execution":
        if observed_admitted_route != observed_protected_route:
            errors.append("protected_execution_route_identity_mismatch")
    else:
        if observed_admitted_route.get("goal_id") != observed_protected_route.get("goal_id"):
            errors.append("checkpoint_recovery_goal_id_mismatch")
        if (
            _int_value(observed_admitted_route.get("generation"))
            != _int_value(observed_protected_route.get("generation")) + 1
        ):
            errors.append("checkpoint_recovery_generation_not_immediate_successor")
        if observed_admitted_route.get("worker_skill") != "improve-project-system":
            errors.append("checkpoint_recovery_worker_skill_mismatch")
        recovery = _dict(receipt.get("recovery"))
        blocker_path_text = _text(recovery.get("blocker_path"))
        blocker = _validate_bound_mapping(
            repo_root=repo_root,
            path_text=blocker_path_text,
            expected_sha256=_text(recovery.get("blocker_sha256")),
            candidate_paths=candidate_paths,
            error_prefix="protected_override_recovery_blocker",
            errors=errors,
        )
        if _text(blocker.get("job_id")) != protected_job_id:
            errors.append("protected_override_recovery_blocker_job_id_mismatch")
        if _text(blocker.get("plan_task_id")) != protected_plan_task_id:
            errors.append(
                "protected_override_recovery_blocker_plan_task_id_mismatch"
            )
        required_recovery = _dict(blocker.get("required_recovery"))
        if (
            _text(recovery.get("strategy_id"))
            != _text(required_recovery.get("strategy_id"))
        ):
            errors.append("protected_override_recovery_strategy_id_mismatch")
        if _text(required_recovery.get("worker_skill")) != "improve-project-system":
            errors.append("protected_override_recovery_blocker_worker_mismatch")

    consumption = _dict(receipt.get("approval_consumption"))
    for field_name, expected in (
        ("one_time_use", True),
        ("consumed", True),
        ("consumed_by", protected_job_id),
        ("reused_for_admitted_job", False),
    ):
        if consumption.get(field_name) != expected:
            errors.append(f"protected_override_consumption_{field_name}_mismatch")
    _validate_authority_limits(receipt, errors)
    return True


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
    override_evaluated = False
    if plan_task_id and plan_task_id != selected_plan_task_id:
        override_evaluated = _validate_protected_human_override(
            job=job,
            admission=admission,
            handoff=handoff,
            created_at=created_at,
            repo_root=repo_root,
            errors=errors,
        )
    if not plan_task_id or (
        plan_task_id != selected_plan_task_id and not override_evaluated
    ):
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
    "PROTECTED_HUMAN_OVERRIDE_HASH_REQUIRED_AFTER",
    "PROTECTED_HUMAN_OVERRIDE_SCHEMA_ID",
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
