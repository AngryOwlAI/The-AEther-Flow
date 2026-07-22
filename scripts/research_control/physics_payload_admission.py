#!/usr/bin/env python3
"""Prospective AgentJob physics-payload admission policy."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


SCHEMA_ID = "physics_payload_admission_v1"
POLICY_ID = "physics_payload_admission_policy_v1"
ACTIVE_AFTER = "2026-07-22T16:24:16Z"

PHYSICS_ROLE_IDS = frozenset(
    {
        "ontology-formalizer",
        "candidate-constructor",
        "refuter",
        "smuggling-auditor",
        "theoretical-continuation-selector",
    }
)
PHYSICS_TASK_SCOPES = frozenset({"scientific", "scientific_audit", "mixed"})
QUALIFYING_PAYLOAD_TYPES = frozenset(
    {
        "theorem",
        "proof_step",
        "countermodel",
        "source_law",
        "external_result",
        "independent_replication",
        "justified_ledger_delta",
        "source_acquisition",
        "precise_obstruction",
        "finite_witness",
        "source_model",
        "candidate_construction",
        "route_decision",
    }
)
REQUIRED_PROCESS_EXCLUSIONS = frozenset(
    {
        "validator_pass",
        "checkpoint_pass",
        "documentation_receipt",
        "role_or_route_selection",
    }
)
AUTHORITY_LIMIT_FIELDS = (
    "theorem_truth_inferred",
    "scientific_status_changed",
    "ontology_or_source_law_adopted",
    "distance_to_gr_changed",
    "physics_promotion_authorized",
)


def _timestamp(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def policy_active(created_at: str) -> bool:
    created = _timestamp(created_at)
    activated = _timestamp(ACTIVE_AFTER)
    return bool(created and activated and created > activated)


def admission_policy() -> dict[str, object]:
    """Return the Director-facing policy context."""

    return {
        "policy_id": POLICY_ID,
        "schema_id": SCHEMA_ID,
        "active_after": ACTIVE_AFTER,
        "enforcement": "hard_failure",
        "historical_jobs_without_block": "legacy_readable",
        "physics_task_scopes": sorted(PHYSICS_TASK_SCOPES),
        "qualifying_payload_types": sorted(QUALIFYING_PAYLOAD_TYPES),
        "source_acquisition_allowed": True,
        "precise_obstruction_allowed": True,
        "selector_only_requires_new_unencoded_decision": True,
        "project_system_path_separate": True,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }


def expected_admission_path(
    job: dict[str, Any],
    task: dict[str, Any] | None = None,
    *,
    role_id: str = "",
) -> str:
    taxonomy = task.get("task_taxonomy", {}) if isinstance(task, dict) else {}
    scope = str(taxonomy.get("scope", "")).strip() if isinstance(taxonomy, dict) else ""
    selected_role = str(role_id or job.get("role_id", "")).strip()
    if selected_role in PHYSICS_ROLE_IDS or scope in PHYSICS_TASK_SCOPES:
        return "physics"
    return "project_system"


def _nonempty_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


def evaluate_agent_job_admission(
    job: dict[str, Any],
    task: dict[str, Any] | None = None,
    *,
    created_at: str = "",
    role_id: str = "",
) -> dict[str, object]:
    """Evaluate declared packet shape without evaluating scientific truth."""

    effective_created_at = str(created_at or job.get("created_at", "")).strip()
    active = policy_active(effective_created_at)
    block = job.get("physics_payload_admission")
    expected_path = expected_admission_path(job, task, role_id=role_id)
    errors: list[str] = []

    if not isinstance(block, dict):
        if not active:
            return {
                "status": "legacy_readable",
                "required": False,
                "expected_admission_path": expected_path,
                "payload_type": "",
                "errors": [],
                "theorem_truth_evaluated": False,
            }
        return {
            "status": "rejected",
            "required": True,
            "expected_admission_path": expected_path,
            "payload_type": "",
            "errors": ["prospective AgentJob missing physics_payload_admission"],
            "theorem_truth_evaluated": False,
        }

    if str(block.get("schema_id", "")).strip() != SCHEMA_ID:
        errors.append(f"schema_id must be {SCHEMA_ID}")
    if str(block.get("policy_id", "")).strip() != POLICY_ID:
        errors.append(f"policy_id must be {POLICY_ID}")

    declared_path = str(block.get("admission_path", "")).strip()
    if declared_path != expected_path:
        errors.append(
            f"admission_path must be {expected_path} for the task taxonomy and role"
        )

    candidate_family = str(block.get("candidate_family", "")).strip()
    assumption_delta = block.get("assumption_delta")
    materiality_basis = str(block.get("materiality_basis", "")).strip()
    source_basis = block.get("source_basis")
    expected_artifacts = block.get("expected_artifact_paths")
    if not _nonempty_list(assumption_delta):
        errors.append("assumption_delta must be a non-empty list of explicit statements")
    elif all(str(item).strip().lower() in {"none", "n/a", "not_applicable"} for item in assumption_delta):
        errors.append("assumption_delta may not be a bare none or not_applicable declaration")
    if not materiality_basis:
        errors.append("materiality_basis must be nonblank")
    if not _nonempty_list(source_basis):
        errors.append("source_basis must be a non-empty list")
    if not _nonempty_list(expected_artifacts):
        errors.append("expected_artifact_paths must be a non-empty list")

    exclusions = block.get("process_receipts_excluded_from_payload")
    exclusion_set = {
        str(item).strip() for item in exclusions
    } if isinstance(exclusions, list) else set()
    missing_exclusions = sorted(REQUIRED_PROCESS_EXCLUSIONS - exclusion_set)
    if missing_exclusions:
        errors.append(
            "process_receipts_excluded_from_payload missing "
            + ", ".join(missing_exclusions)
        )

    authority = block.get("authority_limits")
    if not isinstance(authority, dict):
        errors.append("authority_limits must be a mapping")
    else:
        for field_name in AUTHORITY_LIMIT_FIELDS:
            if authority.get(field_name) is not False:
                errors.append(f"authority_limits.{field_name} must be false")

    payload_type = str(block.get("payload_type", "")).strip()
    if expected_path == "project_system":
        if payload_type != "not_applicable":
            errors.append("project_system admission requires payload_type not_applicable")
        if candidate_family != "not_applicable":
            errors.append("project_system admission requires candidate_family not_applicable")
        if not str(block.get("project_system_justification", "")).strip():
            errors.append("project_system admission requires project_system_justification")
    else:
        if payload_type not in QUALIFYING_PAYLOAD_TYPES:
            errors.append(
                "physics admission payload_type must be one of "
                + ", ".join(sorted(QUALIFYING_PAYLOAD_TYPES))
            )
        if not candidate_family or candidate_family == "not_applicable":
            errors.append("physics admission requires a named candidate_family")
        details = block.get("payload_details")
        details = details if isinstance(details, dict) else {}
        if payload_type == "source_acquisition":
            if not str(details.get("acquisition_target", "")).strip():
                errors.append("source_acquisition requires payload_details.acquisition_target")
            if details.get("primary_source_requirement") is not True:
                errors.append("source_acquisition requires primary_source_requirement true")
        elif payload_type == "precise_obstruction":
            if not str(details.get("obstruction_scope", "")).strip():
                errors.append("precise_obstruction requires payload_details.obstruction_scope")
            if details.get("global_no_go_claimed") is not False:
                errors.append("precise_obstruction requires global_no_go_claimed false")
        elif payload_type == "route_decision":
            if details.get("resolves_new_route_decision") is not True:
                errors.append("route_decision requires resolves_new_route_decision true")
            if not str(details.get("decision_identity", "")).strip():
                errors.append("route_decision requires payload_details.decision_identity")
            if not str(details.get("not_already_encoded_evidence", "")).strip():
                errors.append("route_decision requires not_already_encoded_evidence")

    return {
        "status": "rejected" if errors else "admitted",
        "required": active,
        "expected_admission_path": expected_path,
        "declared_admission_path": declared_path,
        "payload_type": payload_type,
        "errors": errors,
        "theorem_truth_evaluated": False,
    }
