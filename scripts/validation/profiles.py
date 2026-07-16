#!/usr/bin/env python3
"""Five validation-profile contracts for the v19 shadow planner.

This module validates profile membership and wraps the pure planner.  It does
not execute validators, mutate the repository, satisfy a human gate, or change
legacy execution authority.  The temporary ``shadow`` modifier requests a
comparison receipt only; it never changes selected gate membership.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import json
from pathlib import Path
import sys
from typing import Iterable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.project_control.classify_project_changes import classify_paths
from scripts.validation.plan import (
    PlannerError,
    ValidationPlan,
    build_plan,
    canonical_manifest_sha256,
    load_manifest,
)


DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
PERMANENT_PROFILES = ("fast", "affected", "checkpoint", "full", "doctor")
SHADOW_MODIFIER = "shadow"
DEFAULT_LOCAL_PROFILE = "fast"
CHECKPOINT_OBLIGATIONS = (
    "checkpoint_transaction",
    "final_staged_allowlist",
    "authority_validation",
    "residue_validation",
    "whitespace_validation",
)
CHECKPOINT_GATE_ID = "checkpoint_transaction"
FULL_SHARD_GATE_IDS = ("test_shard_repository",)
SCHEDULED_FULL_GATE_IDS = ("profile_ci_project_control",)
SPECIAL_CONDITION_TAGS = {
    "changed_registered_tex_pdf_required": ("required_pdf",),
    "registered_mermaid_changed": ("mermaid",),
    "publication_surface_changed": ("publication_spec", "html"),
    "graph_inputs_changed": ("dependency_graph_input",),
    "task_index_inputs_changed": ("task_index_input",),
    "traceability_inputs_changed": ("traceability",),
    "scientific_checker_family": ("scientific_checker",),
}


class ProfileError(ValueError):
    """Fail-closed validation-profile configuration error."""


@dataclass(frozen=True, slots=True)
class ProfileDefinition:
    name: str
    purpose: str
    command: str
    scope: str
    cost: str
    default_use: str
    capabilities: tuple[str, ...]
    repository_acceptance_authority: bool
    operational_diagnostics_only: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "purpose": self.purpose,
            "command": self.command,
            "scope": self.scope,
            "cost": self.cost,
            "default_use": self.default_use,
            "capabilities": list(self.capabilities),
            "repository_acceptance_authority": self.repository_acceptance_authority,
            "operational_diagnostics_only": self.operational_diagnostics_only,
        }


PROFILE_DEFINITIONS = {
    "fast": ProfileDefinition(
        name="fast",
        purpose="Run the lowest-cost local edit loop over changed operational surfaces.",
        command=(
            ".venv/bin/python -m scripts.validation.cli plan --profile fast "
            "--paths <changed-path> --explain"
        ),
        scope="working tree changed paths",
        cost="lowest",
        default_use="default local development loop",
        capabilities=(
            "classify_changes",
            "syntax_compilation",
            "changed_claim_validation",
            "whitespace_validation",
            "affected_unit_tests",
        ),
        repository_acceptance_authority=False,
        operational_diagnostics_only=False,
    ),
    "affected": ProfileDefinition(
        name="affected",
        purpose="Run fast checks plus blocking validators and focused integration tests affected by the classified change.",
        command=(
            ".venv/bin/python -m scripts.validation.cli plan --profile affected "
            "--paths <changed-path> --explain"
        ),
        scope="working tree affected dependency closure",
        cost="bounded",
        default_use="precheckpoint implementation acceptance",
        capabilities=(
            "fast_profile",
            "affected_blocking_validators",
            "focused_integration_tests",
            "unknown_path_full_fallback",
        ),
        repository_acceptance_authority=False,
        operational_diagnostics_only=False,
    ),
    "checkpoint": ProfileDefinition(
        name="checkpoint",
        purpose="Generate governed derivatives and validate the final staged transaction before commit.",
        command=(
            ".venv/bin/python -m scripts.validation.cli plan --profile checkpoint "
            "--paths <staged-path> --explain"
        ),
        scope="generated working state and final staged tree",
        cost="transactional",
        default_use="one governed checkpoint transaction",
        capabilities=(
            "affected_generation",
            "final_staging",
            "final_staged_allowlist",
            "authority_validation",
            "residue_validation",
            "whitespace_validation",
            "final_affected_acceptance",
        ),
        repository_acceptance_authority=True,
        operational_diagnostics_only=False,
    ),
    "full": ProfileDefinition(
        name="full",
        purpose="Run every nontransactional blocking validation gate and every repository test shard without change-family filtering.",
        command=(
            ".venv/bin/python -m scripts.validation.cli plan --profile full "
            "--paths <changed-path> --explain"
        ),
        scope="repository and scheduled exhaustive coverage",
        cost="highest",
        default_use="scheduled full coverage and explicit exhaustive review",
        capabilities=(
            "all_nontransactional_blocking_gates",
            "all_repository_test_shards",
            "scheduled_full_coverage",
            "unfiltered_change_family_coverage",
        ),
        repository_acceptance_authority=False,
        operational_diagnostics_only=False,
    ),
    "doctor": ProfileDefinition(
        name="doctor",
        purpose="Inspect local retrieval, route, environment, and other non-authoritative operational health.",
        command=(
            ".venv/bin/python -m scripts.validation.cli plan --profile doctor "
            "--scope local_retrieval --explain"
        ),
        scope="local-only and advisory operational diagnostics",
        cost="diagnostic",
        default_use="explicit troubleshooting only",
        capabilities=(
            "local_retrieval_diagnostics",
            "route_diagnostics",
            "environment_health",
            "non_authoritative_operational_diagnostics",
        ),
        repository_acceptance_authority=False,
        operational_diagnostics_only=True,
    ),
}


@dataclass(frozen=True, slots=True)
class ProfileResolution:
    requested_profile: str
    effective_profile: str
    definition: ProfileDefinition
    plan: ValidationPlan
    shadow_modifier_active: bool
    comparison_required: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_id": "validation_profile_resolution_v1",
            "requested_profile": self.requested_profile,
            "effective_profile": self.effective_profile,
            "profile_definition": self.definition.to_dict(),
            "shadow_modifier_active": self.shadow_modifier_active,
            "comparison_required": self.comparison_required,
            "profile_executes_commands": False,
            "plan": self.plan.to_dict(),
            "authority": {
                "operational_validation_only": True,
                "repository_acceptance_authority": (
                    self.definition.repository_acceptance_authority
                ),
                "profile_selection_is_evidence": False,
                "human_gate_authority": False,
                "physics_claim_authority": False,
                "proof_authority": False,
                "ontology_authority": False,
                "benchmark_authority": False,
                "gate_chair_authority": False,
            },
        }


def profile_definition(name: str) -> ProfileDefinition:
    """Return one immutable permanent profile definition."""

    try:
        return PROFILE_DEFINITIONS[name]
    except KeyError as error:
        raise ProfileError(f"unsupported permanent profile: {name}") from error


def _manifest_gates(manifest: Mapping[str, object]) -> tuple[Mapping[str, object], ...]:
    gates = manifest.get("gates")
    if not isinstance(gates, list) or not gates or any(
        not isinstance(gate, dict) for gate in gates
    ):
        raise ProfileError("manifest gates must be a nonempty object array")
    return tuple(gates)


def _gate_profiles(gate: Mapping[str, object]) -> set[str]:
    profiles = gate.get("profiles")
    if not isinstance(profiles, list) or any(
        not isinstance(profile, str) for profile in profiles
    ):
        raise ProfileError(f"{gate.get('gate_id')} has invalid profile membership")
    return set(profiles)


def _gate_obligations(gate: Mapping[str, object]) -> set[str]:
    obligations = gate.get("satisfies_obligations")
    if not isinstance(obligations, list) or any(
        not isinstance(obligation, str) for obligation in obligations
    ):
        raise ProfileError(f"{gate.get('gate_id')} has invalid obligations")
    return set(obligations)


def _profile_membership(
    gates: Iterable[Mapping[str, object]], profile: str
) -> tuple[str, ...]:
    return tuple(
        str(gate["gate_id"])
        for gate in gates
        if profile in _gate_profiles(gate)
    )


def _profile_obligations(
    gates: Iterable[Mapping[str, object]], profile: str
) -> tuple[str, ...]:
    obligations: set[str] = set()
    for gate in gates:
        if profile in _gate_profiles(gate):
            obligations.update(_gate_obligations(gate))
    return tuple(sorted(obligations))


def _full_path_tags(
    gates: Iterable[Mapping[str, object]],
) -> tuple[str, ...]:
    tags: set[str] = set()
    for gate in gates:
        if gate.get("severity") != "blocking":
            continue
        if gate.get("gate_id") == CHECKPOINT_GATE_ID:
            continue
        selection = gate.get("selection")
        if not isinstance(selection, dict):
            raise ProfileError(f"{gate.get('gate_id')} has invalid selection")
        conditions = selection.get("conditions")
        if not isinstance(conditions, list):
            raise ProfileError(f"{gate.get('gate_id')} has invalid conditions")
        for condition in conditions:
            if not isinstance(condition, dict):
                raise ProfileError(f"{gate.get('gate_id')} has invalid condition")
            if condition.get("kind") in {"always", "profile_selected", "explicit_scope"}:
                continue
            kind = str(condition.get("kind"))
            if kind in SPECIAL_CONDITION_TAGS:
                tags.update(SPECIAL_CONDITION_TAGS[kind])
                continue
            values = condition.get("values")
            if not isinstance(values, list) or any(
                not isinstance(value, str) for value in values
            ):
                raise ProfileError(f"{gate.get('gate_id')} has invalid condition values")
            tags.update(values)
    return tuple(sorted(tags))


def _classification_with_full_tags(
    classification: Mapping[str, object],
    gates: tuple[Mapping[str, object], ...],
) -> dict[str, object]:
    expanded = dict(classification)
    current = classification.get("path_family_tags", [])
    if not isinstance(current, list) or any(not isinstance(tag, str) for tag in current):
        raise ProfileError("classification.path_family_tags must be a string array")
    expanded["path_family_tags"] = sorted(set(current) | set(_full_path_tags(gates)))
    return expanded


def _without_checkpoint_transaction(plan: ValidationPlan) -> ValidationPlan:
    if CHECKPOINT_GATE_ID not in plan.selected_gate_ids:
        return plan
    entries: list[dict[str, object]] = []
    for entry in plan.entries:
        if entry.get("gate_id") != CHECKPOINT_GATE_ID:
            entries.append(entry)
            continue
        changed = dict(entry)
        changed["status"] = "skipped_cross_profile_transaction"
        changed["reasons"] = ["checkpoint_transaction_requires_checkpoint_profile"]
        entries.append(changed)
    selected = tuple(
        gate_id for gate_id in plan.selected_gate_ids if gate_id != CHECKPOINT_GATE_ID
    )
    skipped = tuple(
        str(entry["gate_id"])
        for entry in entries
        if entry.get("gate_id") is not None
        and entry.get("status") != "selected"
    )
    return replace(
        plan,
        ordered_gate_ids=tuple(
            gate_id for gate_id in plan.ordered_gate_ids if gate_id != CHECKPOINT_GATE_ID
        ),
        selected_gate_ids=selected,
        skipped_gate_ids=skipped,
        entries=tuple(entries),
    )


def _validate_manifest_profile_contract(
    manifest: Mapping[str, object],
) -> tuple[Mapping[str, object], ...]:
    try:
        build_plan(manifest, classify_paths([]), profile=DEFAULT_LOCAL_PROFILE)
    except PlannerError as error:
        raise ProfileError(f"manifest planner validation failed: {error}") from error
    if manifest.get("migration_epoch") != "shadow_planner":
        raise ProfileError("P5-T07 profiles require the shadow_planner epoch")
    if manifest.get("execution_authority") != "legacy":
        raise ProfileError("P5-T07 cannot change legacy execution authority")
    if tuple(PROFILE_DEFINITIONS) != PERMANENT_PROFILES:
        raise ProfileError("profile definitions do not match the permanent profile order")
    if DEFAULT_LOCAL_PROFILE == "full":
        raise ProfileError("default local development cannot use full")

    gates = _manifest_gates(manifest)
    declared = set().union(*(_gate_profiles(gate) for gate in gates))
    if declared != set(PERMANENT_PROFILES):
        raise ProfileError(
            "manifest permanent profiles differ: "
            f"missing={sorted(set(PERMANENT_PROFILES) - declared)} "
            f"unknown={sorted(declared - set(PERMANENT_PROFILES))}"
        )
    if SHADOW_MODIFIER in declared:
        raise ProfileError("shadow must remain a modifier, not a permanent profile")

    full_members = set(_profile_membership(gates, "full"))
    required_full = {
        str(gate["gate_id"])
        for gate in gates
        if gate.get("severity") == "blocking"
        and gate.get("gate_id") != CHECKPOINT_GATE_ID
    }
    missing_full = sorted(required_full - full_members)
    if missing_full:
        raise ProfileError(f"full profile omits blocking gates: {missing_full}")
    missing_shards = sorted(set(FULL_SHARD_GATE_IDS) - full_members)
    if missing_shards:
        raise ProfileError(f"full profile omits repository test shards: {missing_shards}")
    missing_scheduled = sorted(set(SCHEDULED_FULL_GATE_IDS) - full_members)
    if missing_scheduled:
        raise ProfileError(f"full profile omits scheduled coverage: {missing_scheduled}")

    checkpoint_members = set(_profile_membership(gates, "checkpoint"))
    checkpoint_obligations = set(_profile_obligations(gates, "checkpoint"))
    if CHECKPOINT_GATE_ID not in checkpoint_members:
        raise ProfileError("checkpoint profile omits checkpoint_transaction")
    missing_checkpoint = sorted(set(CHECKPOINT_OBLIGATIONS) - checkpoint_obligations)
    if missing_checkpoint:
        raise ProfileError(
            f"checkpoint profile omits staged safeguards: {missing_checkpoint}"
        )

    doctor_gates = [gate for gate in gates if "doctor" in _gate_profiles(gate)]
    doctor_blocking = sorted(
        str(gate["gate_id"])
        for gate in doctor_gates
        if gate.get("severity") == "blocking"
    )
    if doctor_blocking:
        raise ProfileError(
            f"doctor profile contains blocking gates: {doctor_blocking}"
        )
    doctor_obligations = set().union(
        *(_gate_obligations(gate) for gate in doctor_gates)
    )
    overlap = sorted(doctor_obligations & set(CHECKPOINT_OBLIGATIONS))
    if overlap:
        raise ProfileError(
            f"doctor profile can satisfy checkpoint obligations: {overlap}"
        )
    return gates


def _build_resolved_plan(
    manifest: Mapping[str, object],
    classification: Mapping[str, object],
    *,
    requested_profile: str,
    scopes: Iterable[str],
    role_obligations: Iterable[str],
    gates: tuple[Mapping[str, object], ...],
) -> ValidationPlan:
    obligations = set(role_obligations)
    if requested_profile == "checkpoint":
        obligations.update(CHECKPOINT_OBLIGATIONS)
    resolved_classification = (
        _classification_with_full_tags(classification, gates)
        if requested_profile == "full"
        else classification
    )
    plan = build_plan(
        manifest,
        resolved_classification,
        profile=requested_profile,
        scopes=scopes,
        role_obligations=obligations,
    )
    if plan.effective_profile == "full" and requested_profile != "full":
        plan = build_plan(
            manifest,
            _classification_with_full_tags(classification, gates),
            profile=requested_profile,
            scopes=scopes,
            role_obligations=obligations,
        )
    if requested_profile != "checkpoint":
        plan = _without_checkpoint_transaction(plan)
    return plan


def resolve_profile(
    manifest: Mapping[str, object],
    classification: Mapping[str, object],
    *,
    requested_profile: str = DEFAULT_LOCAL_PROFILE,
    scopes: Iterable[str] = (),
    role_obligations: Iterable[str] = (),
    shadow: bool = False,
    human_gate_required: bool = False,
) -> ProfileResolution:
    """Build one fail-closed pure profile resolution around the shadow planner."""

    definition = profile_definition(requested_profile)
    if not isinstance(shadow, bool):
        raise ProfileError("shadow modifier must be boolean")
    if human_gate_required:
        raise ProfileError("profile selection cannot satisfy or override a human gate")
    obligations = tuple(role_obligations)
    if requested_profile == "doctor" and set(obligations) & set(
        CHECKPOINT_OBLIGATIONS
    ):
        raise ProfileError("doctor cannot request or satisfy checkpoint obligations")
    gates = _validate_manifest_profile_contract(manifest)
    try:
        plan = _build_resolved_plan(
            manifest,
            classification,
            requested_profile=requested_profile,
            scopes=scopes,
            role_obligations=obligations,
            gates=gates,
        )
    except PlannerError as error:
        raise ProfileError(f"profile plan failed: {error}") from error
    return ProfileResolution(
        requested_profile=requested_profile,
        effective_profile=plan.effective_profile,
        definition=profile_definition(plan.effective_profile),
        plan=plan,
        shadow_modifier_active=shadow,
        comparison_required=shadow,
    )


def build_membership_audit(
    manifest: Mapping[str, object],
) -> dict[str, object]:
    """Return a deterministic profile-membership and safety audit."""

    gates = _validate_manifest_profile_contract(manifest)
    by_id = {str(gate["gate_id"]): gate for gate in gates}
    memberships = {
        profile: list(_profile_membership(gates, profile))
        for profile in PERMANENT_PROFILES
    }
    obligations = {
        profile: list(_profile_obligations(gates, profile))
        for profile in PERMANENT_PROFILES
    }

    scenarios = {
        "empty_fast": resolve_profile(
            manifest,
            classify_paths([]),
            requested_profile="fast",
        ),
        "validator_affected": resolve_profile(
            manifest,
            classify_paths(["scripts/validation/profiles.py"]),
            requested_profile="affected",
        ),
        "task_checkpoint": resolve_profile(
            manifest,
            classify_paths(["research_control/tasks/RT-TEST/00_TASK.yaml"]),
            requested_profile="checkpoint",
        ),
        "repository_full": resolve_profile(
            manifest,
            classify_paths([]),
            requested_profile="full",
        ),
        "local_doctor": resolve_profile(
            manifest,
            classify_paths([".local/example.db"]),
            requested_profile="doctor",
            scopes=("local_retrieval",),
        ),
        "unknown_affected": resolve_profile(
            manifest,
            classify_paths(["future_governed_surface/example.rule"]),
            requested_profile="affected",
        ),
    }
    scenario_payload = {
        name: {
            "requested_profile": resolution.requested_profile,
            "effective_profile": resolution.effective_profile,
            "status": resolution.plan.status,
            "selected_gate_ids": list(resolution.plan.selected_gate_ids),
            "unknown_paths": list(resolution.plan.unknown_paths),
        }
        for name, resolution in scenarios.items()
    }

    affected = scenarios["validator_affected"].plan
    affected_blocking = [
        gate_id
        for gate_id in affected.selected_gate_ids
        if by_id[gate_id].get("severity") == "blocking"
    ]
    legacy_compatible = [
        gate_id
        for gate_id in affected_blocking
        if isinstance(by_id[gate_id].get("command_compatibility"), list)
        and bool(by_id[gate_id]["command_compatibility"])
        and str(by_id[gate_id].get("adapter", "")).startswith("legacy:")
    ]
    mismatch = sorted(set(affected_blocking) - set(legacy_compatible))
    if mismatch:
        raise ProfileError(
            f"affected blocking legacy/planner comparison mismatch: {mismatch}"
        )

    doctor_gate_ids = memberships["doctor"]
    doctor_blocking = sorted(
        gate_id
        for gate_id in doctor_gate_ids
        if by_id[gate_id].get("severity") == "blocking"
    )
    doctor_overlap = sorted(
        set(obligations["doctor"]) & set(CHECKPOINT_OBLIGATIONS)
    )
    full_selected = set(scenarios["repository_full"].plan.selected_gate_ids)
    required_full = {
        str(gate["gate_id"])
        for gate in gates
        if gate.get("severity") == "blocking"
        and gate.get("gate_id") != CHECKPOINT_GATE_ID
    }
    missing_resolved_full = sorted(required_full - full_selected)
    if missing_resolved_full:
        raise ProfileError(
            f"resolved full profile is filtered: {missing_resolved_full}"
        )

    return {
        "schema_id": "validation_profile_membership_audit_v1",
        "status": "PASS",
        "plan_task_id": "P5-T07",
        "migration_epoch": manifest.get("migration_epoch"),
        "legacy_execution_authority": manifest.get("execution_authority"),
        "manifest_sha256": canonical_manifest_sha256(manifest),
        "permanent_profiles": list(PERMANENT_PROFILES),
        "default_local_profile": DEFAULT_LOCAL_PROFILE,
        "shadow_modifier": {
            "name": SHADOW_MODIFIER,
            "permanent_profile": False,
            "changes_gate_membership": False,
            "comparison_required": True,
        },
        "profile_definitions": {
            name: PROFILE_DEFINITIONS[name].to_dict()
            for name in PERMANENT_PROFILES
        },
        "profile_membership": memberships,
        "profile_obligations": obligations,
        "profile_counts": {
            name: len(memberships[name]) for name in PERMANENT_PROFILES
        },
        "gate_count": len(gates),
        "blocking_gate_count": sum(
            gate.get("severity") == "blocking" for gate in gates
        ),
        "doctor_blocking_gate_ids": doctor_blocking,
        "doctor_checkpoint_obligation_overlap": doctor_overlap,
        "full_nontransactional_blocking_missing_gate_ids": missing_resolved_full,
        "representative_scenarios": scenario_payload,
        "affected_blocking_shadow_comparison": {
            "status": "PASS",
            "scope": "working_tree_validator_change",
            "planner_gate_ids": affected_blocking,
            "legacy_compatible_gate_ids": legacy_compatible,
            "unexplained_mismatch_gate_ids": mismatch,
        },
        "authority": {
            "operational_validation_only": True,
            "profile_selection_is_evidence": False,
            "legacy_execution_authoritative": True,
            "scientific_claims_changed": False,
            "physics_claim_authority": False,
            "proof_authority": False,
            "ontology_authority": False,
            "benchmark_authority": False,
            "gate_chair_authority": False,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    audit = subcommands.add_parser("audit", help="audit profile membership")
    audit.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    audit.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = build_membership_audit(load_manifest(args.manifest))
    except (OSError, PlannerError, ProfileError) as error:
        print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":") if args.json else None,
            indent=None if args.json else 2,
        )
    )
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
