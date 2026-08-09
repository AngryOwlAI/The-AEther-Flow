#!/usr/bin/env python3
"""Validate the V22 P1-T01 track-governance contracts.

This module is project-control only.  It checks assignment, scorecard,
resource, cross-track-reference, publication-lane, and repository-separation
contracts.  A PASS is operational conformance evidence only; it cannot change
science, ontology, a protected Gate, Distance-to-GR, review or replication
status, publication authority, or repository layout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
PLAN_ID = "recommendations_implementation_plan_continue_task-v22"
PLAN_TASK_ID = "P1-T01"
TRACK_IDS = ("track_a", "track_b", "track_c", "shared_control")
RESOURCE_DIMENSIONS = ("task_count", "elapsed_effort", "compute", "financial_cost")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

DESIGN_PATHS = {
    "charter": "research_control/design/v22_three_track_charter_v1.md",
    "authority": "research_control/design/v22_track_authority_matrix_v1.yaml",
    "assignment": "research_control/design/v22_plan_task_track_assignments_v1.yaml",
    "budget": "research_control/design/v22_track_budget_allocation_v1.yaml",
    "cross_track": "research_control/design/v22_cross_track_reference_schema_v1.yaml",
    "repository": "research_control/design/v22_repository_separation_decision_v1.yaml",
    "backlog": "research_control/design/v22_recommendation_backlog.yaml",
}
SCORECARD_PATHS = {
    "track_a": "research_control/design/v22_track_a_scorecard_schema_v1.yaml",
    "track_b": "research_control/design/v22_track_b_scorecard_schema_v1.yaml",
    "track_c": "research_control/design/v22_track_c_scorecard_schema_v1.yaml",
    "shared_control": "research_control/design/v22_shared_control_scorecard_schema_v1.yaml",
}
FIXTURE_PATH = (
    "research_control/tasks/RT-20260809-001/artifacts/fixtures/"
    "v22_cross_track_promotion_cases.yaml"
)


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def _repo_relative_path(value: Any) -> bool:
    text = _text(value)
    if not text or text.startswith("/") or text.startswith(".local/"):
        return False
    parts = Path(text).parts
    return bool(parts) and all(part not in {"", ".", ".."} for part in parts)


def _add(condition: bool, errors: list[str], code: str) -> None:
    if not condition:
        errors.append(code)


def validate_assignment_manifest(
    backlog: dict[str, Any], manifest: dict[str, Any]
) -> list[str]:
    """Require one and only one primary assignment for all backlog packages."""

    errors: list[str] = []
    backlog_items = _list(backlog.get("items"))
    backlog_ids = [_text(_mapping(item).get("plan_task_id")) for item in backlog_items]
    assignments = _list(manifest.get("assignments"))
    assigned_ids = [_text(_mapping(row).get("plan_task_id")) for row in assignments]
    allowed = set(TRACK_IDS)

    _add(manifest.get("schema_id") == "v22_plan_task_track_assignments_v1", errors,
         "assignment_schema_id_invalid")
    _add(manifest.get("plan_id") == PLAN_ID, errors, "assignment_plan_id_invalid")
    _add(manifest.get("plan_task_id") == PLAN_TASK_ID, errors,
         "assignment_plan_task_id_invalid")
    _add(manifest.get("assignment_rule") == "exactly_one_primary_track_or_shared_control",
         errors, "assignment_rule_invalid")
    _add(set(_list(manifest.get("allowed_primary_tracks"))) == allowed, errors,
         "assignment_track_set_invalid")
    _add(len(backlog_ids) == 40 and len(set(backlog_ids)) == 40 and "" not in backlog_ids,
         errors, "backlog_package_identity_invalid")
    _add(len(assigned_ids) == 40 and len(set(assigned_ids)) == 40 and "" not in assigned_ids,
         errors, "assignment_identity_not_exactly_40_unique")
    _add(set(assigned_ids) == set(backlog_ids), errors,
         "assignment_backlog_coverage_mismatch")

    actual_counts: Counter[str] = Counter()
    for row_value in assignments:
        row = _mapping(row_value)
        primary = row.get("primary_track")
        if isinstance(primary, list):
            errors.append(
                f"assignment_multiple_primary_tracks:{_text(row.get('plan_task_id'))}"
            )
            continue
        primary_text = _text(primary)
        if primary_text not in allowed:
            errors.append(
                f"assignment_primary_track_invalid:{_text(row.get('plan_task_id'))}"
            )
            continue
        actual_counts[primary_text] += 1
        participating = [_text(item) for item in _list(row.get("participating_tracks"))]
        if any(item not in allowed or item == primary_text for item in participating):
            errors.append(
                f"assignment_participating_tracks_invalid:{_text(row.get('plan_task_id'))}"
            )

    expected_counts = {
        key: int(value)
        for key, value in _mapping(manifest.get("expected_primary_track_counts")).items()
        if key in allowed and not isinstance(value, bool)
    }
    _add(expected_counts == dict(actual_counts), errors,
         "assignment_declared_counts_mismatch")
    _add(expected_counts == {"track_a": 1, "track_b": 22, "track_c": 3,
                             "shared_control": 14}, errors,
         "assignment_expected_counts_invalid")
    return sorted(set(errors))


def validate_authority_matrix(matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    tracks = _mapping(matrix.get("tracks"))
    _add(matrix.get("schema_id") == "v22_track_authority_matrix_v1", errors,
         "authority_schema_id_invalid")
    _add(set(tracks) == set(TRACK_IDS), errors, "authority_track_set_invalid")
    for track_id in ("track_a", "track_c", "shared_control"):
        track = _mapping(tracks.get(track_id))
        _add(track.get("distance_to_gr_effect") == "none", errors,
             f"authority_{track_id}_distance_to_gr_not_none")
        _add(track.get("may_supply_gate_evidence") is False, errors,
             f"authority_{track_id}_gate_evidence_not_forbidden")
    track_b = _mapping(tracks.get("track_b"))
    required_forbidden = {
        "track_a_interpretive_coherence",
        "target_side_exact_gr_agreement",
        "track_c_methodology_success",
        "workflow_pass",
        "validator_pass",
        "checkpoint_pass",
        "control_traceability",
    }
    _add(required_forbidden.issubset(set(_list(track_b.get("forbidden_gate_evidence_classes")))),
         errors, "authority_track_b_forbidden_gate_evidence_incomplete")
    _add(track_b.get("distance_to_gr_effect") == "conditional_authorized_science_only",
         errors, "authority_track_b_distance_to_gr_policy_invalid")
    protected = _mapping(matrix.get("protected_actions"))
    distance = _mapping(protected.get("distance_to_gr_update"))
    gate = _mapping(protected.get("gate_verdict"))
    split = _mapping(protected.get("repository_split"))
    release = _mapping(protected.get("publication_or_release"))
    _add(distance.get("permitted_primary_track") == "track_b" and
         distance.get("additional_authority_required") is True, errors,
         "authority_distance_to_gr_action_not_protected")
    _add(gate.get("requires_exact_human_gate") is True and
         gate.get("workflow_or_interpretation_substitution_forbidden") is True,
         errors, "authority_gate_action_not_protected")
    _add(split.get("requires_exact_human_authority") is True and
         split.get("current_authorized") is False, errors,
         "authority_repository_split_not_protected")
    _add(release.get("requires_exact_human_authority") is True and
         release.get("current_authorized") is False, errors,
         "authority_publication_release_not_protected")
    _add(set(_mapping(matrix.get("cross_track_link_defaults")).values()) == {"none"},
         errors, "authority_cross_track_defaults_promotional")
    return sorted(set(errors))


def validate_scorecard_schemas(
    schemas: dict[str, dict[str, Any]], matrix: dict[str, Any]
) -> list[str]:
    """Require four distinct schemas, namespaces, dashboards and publication lanes."""

    errors: list[str] = []
    _add(set(schemas) == set(TRACK_IDS), errors, "scorecard_track_set_invalid")
    ids: list[str] = []
    namespaces: list[str] = []
    dashboards: list[str] = []
    lanes: list[str] = []
    matrix_tracks = _mapping(matrix.get("tracks"))
    for track_id in TRACK_IDS:
        schema = _mapping(schemas.get(track_id))
        ids.append(_text(schema.get("schema_id")))
        namespaces.append(_text(schema.get("metric_namespace")))
        dashboards.append(_text(schema.get("dashboard_id")))
        lanes.append(_text(schema.get("publication_lane_id")))
        _add(schema.get("track_id") == track_id, errors,
             f"scorecard_track_id_invalid:{track_id}")
        _add(set(_list(schema.get("resource_fields"))) == set(RESOURCE_DIMENSIONS), errors,
             f"scorecard_resource_fields_invalid:{track_id}")
        matrix_lane = _mapping(matrix_tracks.get(track_id)).get("publication_lane_id")
        _add(schema.get("publication_lane_id") == matrix_lane, errors,
             f"scorecard_publication_lane_authority_mismatch:{track_id}")
        if track_id in {"track_a", "track_c", "shared_control"}:
            _add(schema.get("distance_to_gr_effect_policy") == "forbidden", errors,
                 f"scorecard_distance_policy_invalid:{track_id}")
        else:
            required = {
                "track_a_interpretive_coherence", "target_side_exact_gr_agreement",
                "track_c_methodology_success", "workflow_pass", "validator_pass",
                "checkpoint_pass", "control_traceability",
            }
            _add(required.issubset(set(_list(schema.get("forbidden_gate_evidence_classes")))),
                 errors, "scorecard_track_b_forbidden_gate_evidence_incomplete")
    for label, values in (
        ("schema_id", ids), ("metric_namespace", namespaces),
        ("dashboard_id", dashboards), ("publication_lane", lanes),
    ):
        _add(len(values) == 4 and "" not in values and len(set(values)) == 4,
             errors, f"scorecard_{label}_not_disjoint")
    return sorted(set(errors))


def validate_budget(
    budget: dict[str, Any], manifest: dict[str, Any],
    schemas: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    centers = _mapping(budget.get("cost_centers"))
    assignments = _list(manifest.get("assignments"))
    actual = Counter(_text(_mapping(item).get("primary_track")) for item in assignments)
    _add(budget.get("schema_id") == "v22_track_budget_allocation_v1", errors,
         "budget_schema_id_invalid")
    _add(set(_list(budget.get("resource_dimensions"))) == set(RESOURCE_DIMENSIONS), errors,
         "budget_resource_dimensions_invalid")
    _add(set(centers) == set(TRACK_IDS), errors, "budget_cost_center_set_invalid")
    _add(budget.get("cross_track_reference_reallocates_cost") is False, errors,
         "budget_cross_track_reallocation_not_forbidden")
    _add(budget.get("missing_measurement_representation") == "not_measured_never_zero",
         errors, "budget_missing_measurement_policy_invalid")
    total = 0
    for track_id in TRACK_IDS:
        center = _mapping(centers.get(track_id))
        count = center.get("planned_task_count")
        if isinstance(count, bool) or not isinstance(count, int):
            errors.append(f"budget_planned_task_count_invalid:{track_id}")
        else:
            total += count
            _add(count == actual.get(track_id, 0), errors,
                 f"budget_assignment_count_mismatch:{track_id}")
        for dimension in ("elapsed_effort", "compute", "financial_cost"):
            measurement = _mapping(center.get(dimension))
            _add(measurement.get("status") == "not_measured", errors,
                 f"budget_missing_measurement_not_explicit:{track_id}:{dimension}")
            _add(measurement.get("value") != 0, errors,
                 f"budget_unmeasured_silently_zero:{track_id}:{dimension}")
        _add(center.get("dashboard_id") == _mapping(schemas.get(track_id)).get("dashboard_id"),
             errors, f"budget_dashboard_mismatch:{track_id}")
    _add(total == 40 and budget.get("total_plan_task_count") == 40, errors,
         "budget_total_task_count_not_40")
    return sorted(set(errors))


def validate_cross_track_schema(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _add(schema.get("schema_id") == "v22_cross_track_reference_schema_v1", errors,
         "cross_track_schema_id_invalid")
    _add(set(_list(schema.get("track_ids"))) == set(TRACK_IDS), errors,
         "cross_track_track_set_invalid")
    required_fixed = {
        "authority_effect": "none",
        "evidence_credit": "none",
        "distance_to_gr_effect": "none",
        "gate_effect": "none",
        "resource_reattribution": "none",
    }
    _add(_mapping(schema.get("fixed_values")) == required_fixed, errors,
         "cross_track_fixed_values_promotional")
    _add(set(required_fixed).issubset(set(_list(schema.get("required_fields")))), errors,
         "cross_track_promotion_fields_not_required")
    return sorted(set(errors))


def validate_repository_decision(decision: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    criteria = _mapping(decision.get("criteria"))
    required = {"coupling", "release_cadence", "access", "maintenance_cost",
                "provenance_preservation"}
    _add(decision.get("schema_id") == "v22_repository_separation_decision_v1", errors,
         "repository_decision_schema_id_invalid")
    _add(decision.get("current_decision") == "retain_monorepo", errors,
         "repository_current_decision_not_retain")
    _add(decision.get("automatic_split_authorized") is False, errors,
         "repository_automatic_split_not_forbidden")
    _add(decision.get("appearance_only_split_forbidden") is True, errors,
         "repository_appearance_split_not_forbidden")
    _add(required.issubset(set(criteria)), errors, "repository_split_criteria_incomplete")
    rule = _mapping(decision.get("decision_rule"))
    _add(rule.get("sufficient_for_execution") is False and
         "separate human authorization" in _list(rule.get("execution_requires")),
         errors, "repository_split_human_authority_missing")
    evidence = _mapping(decision.get("current_evidence"))
    _add(evidence.get("split_trigger_satisfied") is False, errors,
         "repository_split_trigger_unjustified")
    return sorted(set(errors))


def validate_cross_track_link(
    link: dict[str, Any], schema: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    for field in _list(schema.get("required_fields")):
        _add(field in link and link.get(field) not in (None, ""), errors,
             f"cross_track_required_field_missing:{field}")
    source = _text(link.get("source_track"))
    target = _text(link.get("target_track"))
    _add(source in TRACK_IDS and target in TRACK_IDS, errors,
         "cross_track_track_invalid")
    _add(source != target, errors, "cross_track_tracks_must_differ")
    _add(link.get("relation_type") in _list(schema.get("allowed_relation_types")), errors,
         "cross_track_relation_type_invalid")
    _add(_repo_relative_path(link.get("source_path")), errors,
         "cross_track_source_path_invalid")
    _add(_repo_relative_path(link.get("consumer_path")), errors,
         "cross_track_consumer_path_invalid")
    _add(bool(SHA256_RE.fullmatch(_text(link.get("source_sha256")))), errors,
         "cross_track_source_sha256_invalid")
    for key, required_value in _mapping(schema.get("fixed_values")).items():
        _add(link.get(key) == required_value, errors,
             f"cross_track_promotion_forbidden:{key}")
    return sorted(set(errors))


def validate_scorecard_record(
    record: dict[str, Any], schemas: dict[str, dict[str, Any]],
    matrix: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    track_id = _text(record.get("track_id"))
    if track_id not in TRACK_IDS:
        return ["scorecard_track_id_invalid"]
    schema = _mapping(schemas.get(track_id))
    track_authority = _mapping(_mapping(matrix.get("tracks")).get(track_id))
    _add(record.get("metric_namespace") == schema.get("metric_namespace"), errors,
         "scorecard_metric_namespace_mismatch")
    _add(record.get("dashboard_id") == schema.get("dashboard_id"), errors,
         "scorecard_dashboard_mismatch")
    _add(record.get("publication_lane_id") == schema.get("publication_lane_id"), errors,
         "scorecard_publication_lane_mismatch")
    resources = _mapping(record.get("resource_accounting"))
    _add(set(resources) == set(RESOURCE_DIMENSIONS), errors,
         "scorecard_resource_accounting_not_separate")
    distance_effect = _text(record.get("distance_to_gr_effect"))
    if track_id in {"track_a", "track_c", "shared_control"}:
        _add(distance_effect == "none", errors,
             f"{track_id}_distance_to_gr_effect_forbidden")
    else:
        _add(distance_effect in {"none", "conditional_authorized_science_only"}, errors,
             "track_b_distance_to_gr_effect_invalid")
    gate_evidence = {_text(item) for item in _list(record.get("gate_evidence_classes"))}
    if track_id != "track_b":
        _add(not gate_evidence, errors, f"{track_id}_gate_evidence_forbidden")
    else:
        forbidden = set(_list(schema.get("forbidden_gate_evidence_classes")))
        for evidence in sorted(gate_evidence & forbidden):
            errors.append(f"track_b_forbidden_gate_evidence:{evidence}")
    forbidden_claims = set(_list(track_authority.get("forbidden_claim_classes")))
    forbidden_claims.update(_list(schema.get("forbidden_promotions")))
    claims = {_text(item) for item in _list(record.get("claim_classes"))}
    for claim in sorted(claims & forbidden_claims):
        errors.append(f"scorecard_forbidden_claim:{track_id}:{claim}")
    _add(record.get("gate_verdict_issued") is not True, errors,
         "scorecard_gate_verdict_forbidden")
    _add(record.get("publication_authorized") is not True, errors,
         "scorecard_publication_authority_forbidden")
    return sorted(set(errors))


def validate_resource_events(events: list[Any]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for value in events:
        event = _mapping(value)
        event_id = _text(event.get("resource_event_id"))
        if not event_id:
            errors.append("resource_event_id_missing")
        elif event_id in seen:
            errors.append(f"resource_event_duplicate:{event_id}")
        else:
            seen.add(event_id)
        centers = _list(event.get("primary_cost_centers"))
        if len(centers) != 1:
            errors.append(f"resource_event_primary_cost_center_not_exactly_one:{event_id}")
        elif centers[0] not in TRACK_IDS:
            errors.append(f"resource_event_cost_center_invalid:{event_id}")
        _add(event.get("dimension") in RESOURCE_DIMENSIONS, errors,
             f"resource_event_dimension_invalid:{event_id}")
    return sorted(set(errors))


def validate_publication_summary(
    summary: dict[str, Any], schemas: dict[str, dict[str, Any]]
) -> list[str]:
    errors: list[str] = []
    entries = _list(summary.get("entries"))
    _add(summary.get("preserves_separate_lanes") is True, errors,
         "publication_summary_separate_lanes_not_preserved")
    _add(summary.get("claim_merge") is False, errors,
         "publication_summary_claim_merge_forbidden")
    seen: set[str] = set()
    for value in entries:
        entry = _mapping(value)
        track_id = _text(entry.get("track_id"))
        if track_id not in TRACK_IDS:
            errors.append("publication_summary_track_invalid")
            continue
        if track_id in seen:
            errors.append(f"publication_summary_duplicate_track:{track_id}")
        seen.add(track_id)
        _add(entry.get("publication_lane_id") ==
             _mapping(schemas.get(track_id)).get("publication_lane_id"), errors,
             f"publication_summary_lane_mismatch:{track_id}")
    _add(not _text(summary.get("blended_publication_lane_id")), errors,
         "publication_summary_blended_lane_forbidden")
    return sorted(set(errors))


def validate_protected_action(action: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if action.get("requested") is not True:
        return errors
    action_id = _text(action.get("action"))
    primary_track = _text(action.get("primary_track"))
    exact_authority = action.get("exact_human_authority_present") is True
    if action_id in {"distance_to_gr_update", "gate_verdict"}:
        _add(primary_track == "track_b", errors,
             f"protected_action_track_forbidden:{action_id}")
        _add(exact_authority, errors, f"protected_action_human_authority_missing:{action_id}")
    elif action_id in {"repository_split", "publication_or_release"}:
        _add(exact_authority, errors, f"protected_action_human_authority_missing:{action_id}")
    else:
        errors.append("protected_action_unknown")
    return sorted(set(errors))


def evaluate_fixture_case(
    case: dict[str, Any], governance: dict[str, Any]
) -> dict[str, Any]:
    """Evaluate one declarative positive or negative governance fixture."""

    kind = _text(case.get("kind"))
    payload = _mapping(case.get("payload"))
    if kind == "assignment":
        primary = _list(payload.get("primary_tracks"))
        errors = []
        _add(len(primary) == 1, errors, "assignment_primary_track_not_exactly_one")
        if len(primary) == 1:
            _add(primary[0] in TRACK_IDS, errors, "assignment_primary_track_invalid")
    elif kind == "scorecard":
        errors = validate_scorecard_record(
            payload, governance["scorecards"], governance["authority"]
        )
    elif kind == "cross_track_reference":
        errors = validate_cross_track_link(payload, governance["cross_track"])
    elif kind == "resource_events":
        errors = validate_resource_events(_list(payload.get("events")))
    elif kind == "publication_summary":
        errors = validate_publication_summary(payload, governance["scorecards"])
    elif kind == "protected_action":
        errors = validate_protected_action(payload)
    else:
        errors = ["fixture_kind_unknown"]
    expected_valid = case.get("expected_valid") is True
    expected_errors = {_text(value) for value in _list(case.get("expected_errors"))}
    actual_errors = set(errors)
    expectation_met = (not errors) == expected_valid and expected_errors.issubset(actual_errors)
    return {
        "case_id": _text(case.get("case_id")),
        "kind": kind,
        "expected_valid": expected_valid,
        "actual_valid": not errors,
        "expected_errors": sorted(expected_errors),
        "errors": sorted(errors),
        "expectation_met": expectation_met,
    }


def load_governance(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    return {
        "charter_path": repo_root / DESIGN_PATHS["charter"],
        "authority": _load_mapping(repo_root / DESIGN_PATHS["authority"]),
        "assignment": _load_mapping(repo_root / DESIGN_PATHS["assignment"]),
        "budget": _load_mapping(repo_root / DESIGN_PATHS["budget"]),
        "cross_track": _load_mapping(repo_root / DESIGN_PATHS["cross_track"]),
        "repository": _load_mapping(repo_root / DESIGN_PATHS["repository"]),
        "backlog": _load_mapping(repo_root / DESIGN_PATHS["backlog"]),
        "scorecards": {
            track_id: _load_mapping(repo_root / rel_path)
            for track_id, rel_path in SCORECARD_PATHS.items()
        },
    }


def validate_governance(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    governance = load_governance(repo_root)
    charter_path = governance["charter_path"]
    charter_text = charter_path.read_text(encoding="utf-8")
    checks: dict[str, list[str]] = {
        "assignment_manifest": validate_assignment_manifest(
            governance["backlog"], governance["assignment"]
        ),
        "authority_matrix": validate_authority_matrix(governance["authority"]),
        "scorecard_separation": validate_scorecard_schemas(
            governance["scorecards"], governance["authority"]
        ),
        "budget_separation": validate_budget(
            governance["budget"], governance["assignment"], governance["scorecards"]
        ),
        "cross_track_schema": validate_cross_track_schema(governance["cross_track"]),
        "repository_separation_decision": validate_repository_decision(
            governance["repository"]
        ),
        "charter_contract": [],
    }
    required_charter_terms = (
        "<!-- authority: control -->", "Track A", "Track B", "Track C",
        "Shared control", "distance_to_gr_effect: none", "not_measured",
        "retain the monorepo", "internal deterministic process checks",
    )
    for term in required_charter_terms:
        _add(term.lower() in charter_text.lower(), checks["charter_contract"],
             f"charter_required_term_missing:{term}")
    errors = sorted({error for values in checks.values() for error in values})
    assignment_counts = Counter(
        _text(_mapping(row).get("primary_track"))
        for row in _list(governance["assignment"].get("assignments"))
    )
    return {
        "schema_id": "v22_track_governance_validation_v1",
        "plan_id": PLAN_ID,
        "plan_task_id": PLAN_TASK_ID,
        "status": "PASS" if not errors else "FAIL",
        "checks": [
            {"check_id": key, "status": "PASS" if not value else "FAIL",
             "errors": value}
            for key, value in checks.items()
        ],
        "errors": errors,
        "assignment_count": sum(assignment_counts.values()),
        "assignment_counts": {key: assignment_counts.get(key, 0) for key in TRACK_IDS},
        "scorecard_schema_count": len(governance["scorecards"]),
        "metric_namespaces": sorted(
            _text(schema.get("metric_namespace"))
            for schema in governance["scorecards"].values()
        ),
        "dashboard_ids": sorted(
            _text(schema.get("dashboard_id"))
            for schema in governance["scorecards"].values()
        ),
        "publication_lanes": sorted(
            _text(schema.get("publication_lane_id"))
            for schema in governance["scorecards"].values()
        ),
        "resource_dimensions": list(RESOURCE_DIMENSIONS),
        "repository_decision": governance["repository"].get("current_decision"),
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "external_review_completed": False,
            "independent_scientific_replication_completed": False,
            "repository_split_authorized": False,
            "publication_authorized": False,
            "external_action_authorized": False,
        },
    }


def validate_fixture_suite(
    repo_root: Path = REPO_ROOT, fixture_path: str = FIXTURE_PATH
) -> dict[str, Any]:
    governance = load_governance(repo_root)
    fixture = _load_mapping(repo_root / fixture_path)
    results = [
        evaluate_fixture_case(_mapping(case), governance)
        for case in _list(fixture.get("cases"))
    ]
    failed = [result["case_id"] for result in results if not result["expectation_met"]]
    return {
        "schema_id": "v22_track_governance_fixture_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "fixture_schema_id": fixture.get("schema_id"),
        "fixture_case_count": len(results),
        "fixture_pass_count": len(results) - len(failed),
        "fixture_failure_count": len(failed),
        "failed_case_ids": failed,
        "results": results,
        "authority_limits": {
            "fixture_pass_is_science_evidence": False,
            "fixture_pass_changes_distance_to_gr": False,
            "fixture_pass_is_external_review": False,
        },
    }


def build_validation_report(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    governance = validate_governance(repo_root)
    fixtures = validate_fixture_suite(repo_root)
    status = "PASS" if governance["status"] == fixtures["status"] == "PASS" else "FAIL"
    return {
        "schema_id": "v22_p1_t01_combined_validation_v1",
        "status": status,
        "governance": governance,
        "fixtures": fixtures,
        "authority_limits": governance["authority_limits"],
    }


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_validation_report(args.repo_root.resolve())
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"status={report['status']}")
        print(f"assignment_count={report['governance']['assignment_count']}")
        print(f"scorecard_schema_count={report['governance']['scorecard_schema_count']}")
        print(f"fixture_case_count={report['fixtures']['fixture_case_count']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
