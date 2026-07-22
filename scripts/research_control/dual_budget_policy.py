#!/usr/bin/env python3
"""Prospective physics and project-system dual-budget policy."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


SCHEMA_ID = "dual_budget_allocation_v1"
RESULT_SCHEMA_ID = "dual_budget_result_v1"
POLICY_ID = "dual_budget_policy_v1"
ACTIVE_AFTER = "2026-07-22T18:10:44Z"
REPO_ROOT = Path(__file__).resolve().parents[2]
CATEGORIES = frozenset(
    {"physics_bearing", "system_bearing", "mixed", "support_only"}
)
BUDGETS = ("physics", "project_system")
REPORTING_DIMENSIONS = frozenset(
    {"task_count", "elapsed_effort", "compute", "durable_outputs"}
)
AUTHORITY_LIMITS = {
    "system_success_counts_as_physics": False,
    "system_success_counts_as_distance_to_gr": False,
    "validator_pass_counts_as_physics": False,
    "route_selection_counts_as_physics": False,
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _timestamp(value: object) -> datetime | None:
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


def policy_active(created_at: object) -> bool:
    created = _timestamp(created_at)
    active = _timestamp(ACTIVE_AFTER)
    return bool(created and active and created >= active)


def dual_budget_policy() -> dict[str, object]:
    """Return the Director-facing policy without creating science authority."""

    return {
        "policy_id": POLICY_ID,
        "schema_id": SCHEMA_ID,
        "result_schema_id": RESULT_SCHEMA_ID,
        "active_after": ACTIVE_AFTER,
        "categories": sorted(CATEGORIES),
        "budgets": list(BUDGETS),
        "reporting_dimensions": sorted(REPORTING_DIMENSIONS),
        "task_count_rule": "exactly_one_primary_budget_credit",
        "mixed_output_rule": "physics_and_project_system_paths_are_disjoint",
        "mixed_acceptance_rule": "physics_and_project_system_criteria_are_disjoint",
        "missing_compute_representation": "not_measured_never_zero",
        "existing_three_task_threshold": "advisory_in_p12_t03",
        "ordinary_route_guard_owner": "P12-T04",
        "system_success_counts_as_physics": False,
        "system_success_counts_as_distance_to_gr": False,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }


def _string_list(value: object) -> list[str] | None:
    if not isinstance(value, list):
        return None
    result = [str(item).strip() for item in value]
    if any(not item for item in result) or len(set(result)) != len(result):
        return None
    return result


def _credit_value(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value in {0, 1}:
        return value
    if isinstance(value, str) and value.strip() in {"0", "1"}:
        return int(value.strip())
    return None


def _numeric_value(value: object) -> int | float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        text = value.strip()
        try:
            return float(text) if "." in text else int(text)
        except ValueError:
            return None
    return None


def _lane_lists(
    value: object,
    field_name: str,
    errors: list[str],
) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        errors.append(f"{field_name} must be a mapping")
        return {budget: [] for budget in BUDGETS}
    result: dict[str, list[str]] = {}
    for budget in BUDGETS:
        items = _string_list(value.get(budget))
        if items is None:
            errors.append(f"{field_name}.{budget} must be a duplicate-free string list")
            items = []
        result[budget] = items
    if set(value) != set(BUDGETS):
        errors.append(f"{field_name} must contain exactly physics and project_system")
    return result


def _validate_measurement(
    value: object,
    field_name: str,
    errors: list[str],
) -> dict[str, object]:
    if not isinstance(value, dict):
        errors.append(f"{field_name} must be a mapping")
        return {"status": "invalid", "value": None, "unit": ""}
    status = str(value.get("status", "")).strip()
    measured_value = value.get("value")
    normalized_value = _numeric_value(measured_value)
    unit = str(value.get("unit", "")).strip()
    if status == "not_measured":
        if measured_value is not None:
            errors.append(
                f"{field_name} not_measured value must be null"
            )
    elif status == "measured":
        if normalized_value is None:
            errors.append(
                f"{field_name} measured value must be numeric"
            )
        elif normalized_value < 0:
            errors.append(
                f"{field_name} measured value must be nonnegative"
            )
        if not unit:
            errors.append(
                f"{field_name} measured unit must be nonblank"
            )
    else:
        errors.append(
            f"{field_name}.status must be measured or not_measured"
        )
    return {
        "status": status,
        "value": normalized_value if status == "measured" else measured_value,
        "unit": unit,
    }


def _validate_resource_measurement(
    value: object,
    errors: list[str],
) -> dict[str, dict[str, dict[str, object]]]:
    if not isinstance(value, dict):
        errors.append("resource_measurement must be a mapping")
        value = {}
    if set(value) != set(BUDGETS):
        errors.append(
            "resource_measurement must contain exactly physics and project_system"
        )
    result: dict[str, dict[str, dict[str, object]]] = {}
    for budget in BUDGETS:
        lane = value.get(budget)
        if not isinstance(lane, dict):
            errors.append(f"resource_measurement.{budget} must be a mapping")
            lane = {}
        if set(lane) != {"elapsed_effort", "compute"}:
            errors.append(
                f"resource_measurement.{budget} must contain exactly elapsed_effort and compute"
            )
        result[budget] = {
            name: _validate_measurement(
                lane.get(name),
                f"resource_measurement.{budget}.{name}",
                errors,
            )
            for name in ("elapsed_effort", "compute")
        }
    return result


def _default_evidence_verifier(path_text: str, expected_sha256: str) -> str:
    path = Path(path_text)
    if not path_text or path.is_absolute() or ".." in path.parts:
        return "blocked_physics_exception.evidence_path must be repository-relative"
    source = REPO_ROOT / path
    if not source.is_file():
        return f"blocked physics evidence path does not exist: {path_text}"
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != expected_sha256:
        return f"blocked physics evidence SHA-256 does not match {path_text}"
    return ""


def evaluate_dual_budget_allocation(
    job: dict[str, Any],
    *,
    created_at: str = "",
    evidence_verifier: Callable[[str, str], str] | None = None,
) -> dict[str, object]:
    """Validate prospective accounting shape without judging scientific truth."""

    effective_created_at = str(created_at or job.get("created_at", "")).strip()
    active = policy_active(effective_created_at)
    block = job.get("dual_budget_allocation")
    if not isinstance(block, dict):
        if not active:
            return {
                "status": "legacy_readable",
                "required": False,
                "errors": [],
                "normalized": {},
                "theorem_truth_evaluated": False,
            }
        return {
            "status": "rejected",
            "required": True,
            "errors": ["prospective AgentJob missing dual_budget_allocation"],
            "normalized": {},
            "theorem_truth_evaluated": False,
        }

    errors: list[str] = []
    if str(block.get("schema_id", "")).strip() != SCHEMA_ID:
        errors.append(f"schema_id must be {SCHEMA_ID}")
    if str(block.get("policy_id", "")).strip() != POLICY_ID:
        errors.append(f"policy_id must be {POLICY_ID}")

    category = str(block.get("category", "")).strip()
    primary = str(block.get("primary_budget", "")).strip()
    if category not in CATEGORIES:
        errors.append("category must be one of " + ", ".join(sorted(CATEGORIES)))
    if primary not in BUDGETS:
        errors.append("primary_budget must be physics or project_system")
    if category == "physics_bearing" and primary != "physics":
        errors.append("physics_bearing category requires primary_budget physics")
    if category in {"system_bearing", "support_only"} and primary != "project_system":
        errors.append(f"{category} category requires primary_budget project_system")

    credits = block.get("task_count_credit")
    if not isinstance(credits, dict) or set(credits) != set(BUDGETS):
        errors.append("task_count_credit must contain exactly physics and project_system")
        normalized_credits = {budget: 0 for budget in BUDGETS}
    else:
        normalized_credits = {
            budget: _credit_value(credits.get(budget)) for budget in BUDGETS
        }
        if any(value is None for value in normalized_credits.values()):
            errors.append("task_count_credit values must be integer 0 or 1")
        if sum(value for value in normalized_credits.values() if value is not None) != 1:
            errors.append("task_count_credit must assign exactly one total credit")
        if primary in BUDGETS and normalized_credits.get(primary) != 1:
            errors.append("primary_budget must receive the single task-count credit")

    outputs = _lane_lists(
        block.get("expected_durable_outputs"), "expected_durable_outputs", errors
    )
    criteria = _lane_lists(
        block.get("acceptance_criteria"), "acceptance_criteria", errors
    )
    shared_outputs = sorted(set(outputs["physics"]) & set(outputs["project_system"]))
    shared_criteria = sorted(set(criteria["physics"]) & set(criteria["project_system"]))
    if shared_outputs:
        errors.append("physics and project_system durable outputs must be disjoint")
    if shared_criteria:
        errors.append("physics and project_system acceptance criteria must be disjoint")

    if category == "physics_bearing":
        if not outputs["physics"] or not criteria["physics"]:
            errors.append("physics_bearing category requires physics outputs and criteria")
        if outputs["project_system"] or criteria["project_system"]:
            errors.append("physics_bearing category may not claim project_system lane credit")
    elif category in {"system_bearing", "support_only"}:
        if not outputs["project_system"] or not criteria["project_system"]:
            errors.append(f"{category} category requires project_system outputs and criteria")
        if outputs["physics"] or criteria["physics"]:
            errors.append(f"{category} category may not claim physics lane credit")
    elif category == "mixed":
        for budget in BUDGETS:
            if not outputs[budget] or not criteria[budget]:
                errors.append(f"mixed category requires nonempty {budget} outputs and criteria")

    dimensions = _string_list(block.get("reporting_dimensions"))
    if dimensions is None or set(dimensions) != set(REPORTING_DIMENSIONS):
        errors.append(
            "reporting_dimensions must contain task_count elapsed_effort compute and durable_outputs"
        )
        dimensions = []

    measurements = _validate_resource_measurement(
        block.get("resource_measurement"), errors
    )

    exception = block.get("blocked_physics_exception")
    if not isinstance(exception, dict):
        errors.append("blocked_physics_exception must be a mapping")
        exception = {}
    exception_active = exception.get("active") is True
    if exception.get("active") not in {True, False}:
        errors.append("blocked_physics_exception.active must be boolean")
    if exception_active:
        evidence_verifier = evidence_verifier or _default_evidence_verifier
        for field_name in ("exception_id", "evidence_path", "evidence_sha256"):
            if not str(exception.get(field_name, "")).strip():
                errors.append(f"blocked_physics_exception.{field_name} must be nonblank")
        evidence_sha = str(exception.get("evidence_sha256", "")).strip()
        if evidence_sha and not SHA256_RE.fullmatch(evidence_sha):
            errors.append(
                "blocked_physics_exception.evidence_sha256 must be lowercase SHA-256"
            )
        path_text = str(exception.get("evidence_path", "")).strip()
        if path_text and SHA256_RE.fullmatch(evidence_sha):
            evidence_error = evidence_verifier(path_text, evidence_sha)
            if evidence_error:
                errors.append(evidence_error)
    else:
        for field_name in ("exception_id", "evidence_path", "evidence_sha256"):
            if str(exception.get(field_name, "")).strip():
                errors.append(
                    f"inactive blocked_physics_exception.{field_name} must be blank"
                )

    authority = block.get("authority_limits")
    if not isinstance(authority, dict):
        errors.append("authority_limits must be a mapping")
    else:
        for field_name, expected in AUTHORITY_LIMITS.items():
            if authority.get(field_name) is not expected:
                errors.append(f"authority_limits.{field_name} must be false")

    return {
        "status": "rejected" if errors else "admitted",
        "required": active,
        "errors": errors,
        "normalized": {
            "category": category,
            "primary_budget": primary,
            "task_count_credit": normalized_credits,
            "expected_durable_outputs": outputs,
            "acceptance_criteria": criteria,
            "reporting_dimensions": dimensions,
            "resource_measurement": measurements,
            "blocked_physics_exception_active": exception_active,
        },
        "theorem_truth_evaluated": False,
    }


def evaluate_dual_budget_completion(
    job: dict[str, Any],
    completion: dict[str, Any],
    *,
    created_at: str = "",
) -> dict[str, object]:
    """Validate completion accounting against the admitted allocation."""

    admission = evaluate_dual_budget_allocation(job, created_at=created_at)
    if admission["status"] == "legacy_readable":
        return {"status": "legacy_readable", "required": False, "errors": []}
    errors = [str(item) for item in admission["errors"]]
    result = completion.get("dual_budget_result")
    if not isinstance(result, dict):
        errors.append("completion missing dual_budget_result")
        return {"status": "rejected", "required": True, "errors": errors}
    if str(result.get("schema_id", "")).strip() != RESULT_SCHEMA_ID:
        errors.append(f"dual_budget_result.schema_id must be {RESULT_SCHEMA_ID}")
    if str(result.get("policy_id", "")).strip() != POLICY_ID:
        errors.append(f"dual_budget_result.policy_id must be {POLICY_ID}")

    normalized = admission.get("normalized", {})
    normalized = normalized if isinstance(normalized, dict) else {}
    for field_name in ("category", "primary_budget"):
        if result.get(field_name) != normalized.get(field_name):
            errors.append(f"dual_budget_result.{field_name} must match AgentJob allocation")
    result_credits_source = result.get("task_count_credit")
    result_credits = (
        {
            budget: _credit_value(result_credits_source.get(budget))
            for budget in BUDGETS
        }
        if isinstance(result_credits_source, dict)
        else {}
    )
    if result_credits != normalized.get("task_count_credit"):
        errors.append("dual_budget_result.task_count_credit must match AgentJob allocation")

    observed_outputs = _lane_lists(
        result.get("observed_durable_outputs"),
        "dual_budget_result.observed_durable_outputs",
        errors,
    )
    accepted_criteria = _lane_lists(
        result.get("accepted_criteria"),
        "dual_budget_result.accepted_criteria",
        errors,
    )
    if set(observed_outputs["physics"]) & set(observed_outputs["project_system"]):
        errors.append("completion durable outputs may not be double counted across budgets")
    if set(accepted_criteria["physics"]) & set(accepted_criteria["project_system"]):
        errors.append("completion criteria may not be double counted across budgets")

    expected_outputs = normalized.get("expected_durable_outputs", {})
    expected_criteria = normalized.get("acceptance_criteria", {})
    if isinstance(expected_outputs, dict):
        for budget in BUDGETS:
            missing = set(expected_outputs.get(budget, [])) - set(observed_outputs[budget])
            if missing:
                errors.append(f"completion missing {budget} durable outputs: {sorted(missing)}")
    if isinstance(expected_criteria, dict):
        for budget in BUDGETS:
            missing = set(expected_criteria.get(budget, [])) - set(accepted_criteria[budget])
            if missing:
                errors.append(f"completion missing {budget} accepted criteria: {sorted(missing)}")

    category = str(normalized.get("category", ""))
    if category in {"system_bearing", "support_only"}:
        if observed_outputs["physics"] or accepted_criteria["physics"]:
            errors.append("system or support completion may not claim physics lane success")
        delta = completion.get("distance_to_gr_delta")
        if not isinstance(delta, dict) or delta.get("changed") is not False:
            errors.append("system or support completion requires distance_to_gr_delta.changed false")

    _validate_resource_measurement(result.get("resource_measurement"), errors)
    authority = result.get("authority_limits")
    if not isinstance(authority, dict):
        errors.append("dual_budget_result.authority_limits must be a mapping")
    else:
        for field_name, expected in AUTHORITY_LIMITS.items():
            if authority.get(field_name) is not expected:
                errors.append(f"dual_budget_result.authority_limits.{field_name} must be false")

    return {
        "status": "rejected" if errors else "accepted",
        "required": True,
        "errors": errors,
    }
