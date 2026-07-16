#!/usr/bin/env python3
"""Pure conditional validation-plan deduplication for the v19 shadow planner.

The engine consumes already-expanded, already-resolved planned executions.  It
does not execute validators, mutate the repository, activate manifest policy,
or change legacy execution authority.  Missing identity or predicate evidence
is retained fail-closed.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass, field, replace
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control.strict_yaml import StrictYamlError, loads as load_yaml_text


DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
DEFAULT_CONTRACTS = REPO_ROOT / "research_control/design/validation_supersedence_contracts_v1.yaml"
IDENTITY_FIELDS = (
    "gate_id",
    "implementation_digest",
    "environment_digest",
    "config_digest",
    "scope",
    "tree_hash",
)


class DeduplicationError(ValueError):
    """Fail-closed deduplication input or policy error."""


def _nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _canonical_sha256(value: Mapping[str, object]) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class DeduplicationConfig:
    enabled: bool
    prerequisites_expanded: bool
    obligations_resolved: bool
    migration_epoch: str = "shadow_planner"

    def __post_init__(self) -> None:
        if not isinstance(self.enabled, bool):
            raise DeduplicationError("enabled must be boolean")
        if not isinstance(self.prerequisites_expanded, bool):
            raise DeduplicationError("prerequisites_expanded must be boolean")
        if not isinstance(self.obligations_resolved, bool):
            raise DeduplicationError("obligations_resolved must be boolean")
        if self.migration_epoch != "shadow_planner":
            raise DeduplicationError("deduplication is limited to shadow_planner")


@dataclass(frozen=True, slots=True)
class GateExecution:
    execution_id: str
    gate_id: str
    implementation_digest: str | None
    environment_digest: str | None
    config_digest: str | None
    scope: str | None
    tree_hash: str | None
    generation_state: str | None
    predicate_evidence: Mapping[str, object] = field(default_factory=dict)
    replay_bypass_reason: str | None = None

    def __post_init__(self) -> None:
        if not _nonblank(self.execution_id) or not _nonblank(self.gate_id):
            raise DeduplicationError("execution_id and gate_id must be nonblank")
        if not isinstance(self.predicate_evidence, Mapping):
            raise DeduplicationError("predicate_evidence must be a mapping")
        if self.replay_bypass_reason is not None and not _nonblank(
            self.replay_bypass_reason
        ):
            raise DeduplicationError("replay_bypass_reason must be nonblank when set")

    @property
    def identity_components(self) -> dict[str, str] | None:
        values = {
            "gate_id": self.gate_id,
            "implementation_digest": self.implementation_digest,
            "environment_digest": self.environment_digest,
            "config_digest": self.config_digest,
            "scope": self.scope,
            "tree_hash": self.tree_hash,
        }
        if any(not _nonblank(value) for value in values.values()):
            return None
        return {key: str(values[key]) for key in IDENTITY_FIELDS}

    @property
    def evidence_identity(self) -> str | None:
        components = self.identity_components
        if components is None or not _nonblank(self.generation_state):
            return None
        return f"sha256:{_canonical_sha256(components)}"


@dataclass(frozen=True, slots=True)
class DeduplicationDecision:
    execution_id: str
    gate_id: str
    status: str
    reasons: tuple[str, ...]
    evidence_identity: str | None
    satisfying_execution_id: str | None = None
    satisfying_gate_id: str | None = None
    predicate_id: str | None = None
    predicate_evidence: Mapping[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "execution_id": self.execution_id,
            "gate_id": self.gate_id,
            "status": self.status,
            "reasons": list(self.reasons),
            "evidence_identity": self.evidence_identity,
            "satisfying_execution_id": self.satisfying_execution_id,
            "satisfying_gate_id": self.satisfying_gate_id,
            "predicate_id": self.predicate_id,
            "predicate_evidence": dict(self.predicate_evidence),
        }


@dataclass(frozen=True, slots=True)
class DeduplicationResult:
    decisions: tuple[DeduplicationDecision, ...]
    retained_execution_ids: tuple[str, ...]
    retained_gate_ids: tuple[str, ...]
    skipped_duplicate_count: int
    superseded_count: int
    residual_repeated_identity_count: int
    feature_enabled: bool
    supersedence_policy_active: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_id": "validation_deduplication_result_v1",
            "status": "PASS",
            "feature_enabled": self.feature_enabled,
            "supersedence_policy_active": self.supersedence_policy_active,
            "input_execution_count": len(self.decisions),
            "planned_execution_count": len(self.retained_execution_ids),
            "skipped_duplicate_count": self.skipped_duplicate_count,
            "superseded_count": self.superseded_count,
            "residual_repeated_identity_count": self.residual_repeated_identity_count,
            "retained_execution_ids": list(self.retained_execution_ids),
            "retained_gate_ids": list(self.retained_gate_ids),
            "decisions": [decision.to_dict() for decision in self.decisions],
            "execution_authority_changed": False,
            "planner_executes_commands": False,
            "scientific_claims_changed": False,
        }


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, object]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DeduplicationError(f"manifest load failed: {error}") from error
    if not isinstance(value, dict):
        raise DeduplicationError("manifest must be an object")
    return value


def load_contracts(path: Path = DEFAULT_CONTRACTS) -> dict[str, object]:
    try:
        text = Path(path).read_text(encoding="utf-8")
        expanded: list[str] = []
        for line in text.splitlines():
            match = re.fullmatch(r"(\s*)-\s+(\{.*\})", line)
            if match is None:
                expanded.append(line)
                continue
            json_text = re.sub(
                r"(?:(?<=\{)|(?<=,))\s*([A-Za-z_][A-Za-z0-9_]*)\s*:",
                lambda item: f'"{item.group(1)}":',
                match.group(2),
            )
            inline = json.loads(json_text)
            if not isinstance(inline, dict) or not inline:
                raise DeduplicationError("inline contract mapping must be nonempty")
            indent = match.group(1)
            for index, (key, item) in enumerate(inline.items()):
                prefix = f"{indent}- " if index == 0 else f"{indent}  "
                expanded.append(
                    f"{prefix}{key}: {json.dumps(item, ensure_ascii=False)}"
                )
        value = load_yaml_text("\n".join(expanded) + "\n")
    except (OSError, StrictYamlError, json.JSONDecodeError) as error:
        raise DeduplicationError(f"supersedence contract load failed: {error}") from error
    if not isinstance(value, dict):
        raise DeduplicationError("supersedence contracts must be a mapping")
    return value


def _manifest_gate_map(manifest: Mapping[str, object]) -> dict[str, dict[str, object]]:
    gates = manifest.get("gates")
    if not isinstance(gates, list) or not gates:
        raise DeduplicationError("manifest gates must be a nonempty array")
    result: dict[str, dict[str, object]] = {}
    for raw_gate in gates:
        if not isinstance(raw_gate, dict) or not _nonblank(raw_gate.get("gate_id")):
            raise DeduplicationError("manifest contains a malformed gate")
        gate_id = str(raw_gate["gate_id"])
        if gate_id in result:
            raise DeduplicationError(f"duplicate manifest gate: {gate_id}")
        if not isinstance(raw_gate.get("mutating"), bool):
            raise DeduplicationError(f"manifest gate {gate_id} lacks mutating boolean")
        supersedes = raw_gate.get("supersedes")
        if not isinstance(supersedes, list):
            raise DeduplicationError(f"manifest gate {gate_id} supersedes must be an array")
        result[gate_id] = raw_gate
    return result


def _contract_parts(
    contracts: Mapping[str, object],
) -> tuple[dict[str, dict[str, object]], tuple[dict[str, object], ...], bool]:
    raw_predicates = contracts.get("predicate_catalog")
    raw_contracts = contracts.get("supersedence_contracts")
    activation = contracts.get("activation_gate")
    if not isinstance(raw_predicates, list) or not isinstance(raw_contracts, list):
        raise DeduplicationError("supersedence contract catalogs are malformed")
    if not isinstance(activation, dict):
        raise DeduplicationError("supersedence activation gate is malformed")
    predicates: dict[str, dict[str, object]] = {}
    for predicate in raw_predicates:
        if not isinstance(predicate, dict) or not _nonblank(predicate.get("predicate_id")):
            raise DeduplicationError("malformed supersedence predicate")
        predicate_id = str(predicate["predicate_id"])
        if predicate_id in predicates:
            raise DeduplicationError(f"duplicate supersedence predicate: {predicate_id}")
        for field_name in ("required_equal", "required_true"):
            values = predicate.get(field_name)
            if not isinstance(values, list) or any(not _nonblank(item) for item in values):
                raise DeduplicationError(
                    f"predicate {predicate_id} {field_name} must be a string array"
                )
        predicates[predicate_id] = predicate
    normalized_contracts: list[dict[str, object]] = []
    for contract in raw_contracts:
        if not isinstance(contract, dict):
            raise DeduplicationError("malformed supersedence contract")
        required = ("contract_id", "source_gate_id", "target_gate_id", "predicate_id")
        if any(not _nonblank(contract.get(field_name)) for field_name in required):
            raise DeduplicationError("malformed supersedence contract identity")
        if contract["predicate_id"] not in predicates:
            raise DeduplicationError(
                f"contract references unknown predicate {contract['predicate_id']}"
            )
        normalized_contracts.append(contract)
    return (
        predicates,
        tuple(normalized_contracts),
        activation.get("current_status") == "active",
    )


def evaluate_predicate(
    predicate: Mapping[str, object],
    source: GateExecution,
    target: GateExecution,
) -> tuple[bool, dict[str, object]]:
    """Evaluate one same-scope predicate without inferring missing evidence."""

    required_equal = predicate.get("required_equal")
    required_true = predicate.get("required_true")
    if not isinstance(required_equal, list) or not isinstance(required_true, list):
        raise DeduplicationError("predicate is missing required field lists")
    mismatches: list[str] = []
    matched: dict[str, object] = {}
    for field_name in required_equal:
        if not _nonblank(field_name):
            raise DeduplicationError("predicate contains a blank required_equal field")
        source_value = source.predicate_evidence.get(str(field_name))
        target_value = target.predicate_evidence.get(str(field_name))
        if source_value is None or target_value is None or source_value != target_value:
            mismatches.append(str(field_name))
        else:
            matched[str(field_name)] = source_value
    false_fields = [
        str(field_name)
        for field_name in required_true
        if source.predicate_evidence.get(str(field_name)) is not True
    ]
    identity_mismatches: list[str] = []
    for field_name in ("environment_digest", "config_digest", "scope", "tree_hash"):
        source_value = getattr(source, field_name)
        target_value = getattr(target, field_name)
        if not _nonblank(source_value) or source_value != target_value:
            identity_mismatches.append(field_name)
    if (
        not _nonblank(source.generation_state)
        or source.generation_state != target.generation_state
    ):
        identity_mismatches.append("generation_state")
    eligible = not mismatches and not false_fields and not identity_mismatches
    return eligible, {
        "required_equal_matched": matched,
        "required_equal_mismatches": sorted(mismatches),
        "required_true_matched": sorted(
            str(field_name)
            for field_name in required_true
            if source.predicate_evidence.get(str(field_name)) is True
        ),
        "required_true_false_or_missing": sorted(false_fields),
        "identity_mismatches": sorted(identity_mismatches),
    }


def _active_supersedence_edges(
    manifest_gates: Mapping[str, Mapping[str, object]],
    predicates: Mapping[str, Mapping[str, object]],
    contracts: Sequence[Mapping[str, object]],
    *,
    policy_active: bool,
) -> tuple[tuple[str, str, str, Mapping[str, object]], ...]:
    if not policy_active:
        return ()
    active_contracts = {
        (
            str(contract["source_gate_id"]),
            str(contract["target_gate_id"]),
            str(contract["predicate_id"]),
        ): contract
        for contract in contracts
        if contract.get("activation_status") == "active"
    }
    edges: list[tuple[str, str, str, Mapping[str, object]]] = []
    for source_gate_id, gate in manifest_gates.items():
        for edge in gate["supersedes"]:
            if not isinstance(edge, dict):
                raise DeduplicationError(f"{source_gate_id} has malformed supersedence")
            if edge.get("status") != "active":
                continue
            target_gate_id = str(edge.get("gate_id", ""))
            predicate_id = str(edge.get("predicate_id", ""))
            key = (source_gate_id, target_gate_id, predicate_id)
            if key not in active_contracts:
                continue
            predicate = predicates.get(predicate_id)
            if predicate is None or predicate.get("status") != "active":
                continue
            edges.append((source_gate_id, target_gate_id, predicate_id, predicate))
    return tuple(sorted(edges, key=lambda item: item[:3]))


def deduplicate_executions(
    executions: Iterable[GateExecution],
    manifest: Mapping[str, object],
    contracts: Mapping[str, object],
    config: DeduplicationConfig,
) -> DeduplicationResult:
    """Return a deterministic reasoned plan while preserving fail-closed gates."""

    if config.enabled and not config.prerequisites_expanded:
        raise DeduplicationError("deduplication requires expanded prerequisites")
    if config.enabled and not config.obligations_resolved:
        raise DeduplicationError("deduplication requires resolved obligations")
    manifest_gates = _manifest_gate_map(manifest)
    predicates, raw_contracts, policy_active = _contract_parts(contracts)
    items = tuple(executions)
    execution_ids: set[str] = set()
    for execution in items:
        if not isinstance(execution, GateExecution):
            raise DeduplicationError("executions must contain GateExecution values")
        if execution.execution_id in execution_ids:
            raise DeduplicationError(f"duplicate execution_id: {execution.execution_id}")
        if execution.gate_id not in manifest_gates:
            raise DeduplicationError(f"unknown manifest gate: {execution.gate_id}")
        execution_ids.add(execution.execution_id)

    decisions: list[DeduplicationDecision] = []
    retained: list[GateExecution] = []
    retained_by_identity: dict[tuple[str, str], GateExecution] = {}
    for execution in items:
        gate = manifest_gates[execution.gate_id]
        identity = execution.evidence_identity
        if not config.enabled:
            status = "retained_feature_disabled"
            reasons = ("deduplication_feature_disabled",)
        elif execution.replay_bypass_reason is not None:
            status = "retained_replay_bypass"
            reasons = ("explicit_replay_bypass", execution.replay_bypass_reason)
        elif gate["mutating"]:
            status = "retained_mutator"
            reasons = ("mutating_gate_is_never_deduplicated",)
        elif identity is None:
            status = "retained_unresolved_identity"
            reasons = ("missing_identity_component",)
        else:
            key = (identity, str(execution.generation_state))
            satisfying = retained_by_identity.get(key)
            if satisfying is not None:
                decisions.append(
                    DeduplicationDecision(
                        execution.execution_id,
                        execution.gate_id,
                        "skipped_duplicate",
                        ("exact_evidence_identity_match",),
                        identity,
                        satisfying.execution_id,
                        satisfying.gate_id,
                        "exact_evidence_identity_v1",
                        {
                            "identity_components": execution.identity_components or {},
                            "generation_state": execution.generation_state,
                        },
                    )
                )
                continue
            retained_by_identity[key] = execution
            status = "retained"
            reasons = ("first_complete_evidence_identity",)
        retained.append(execution)
        decisions.append(
            DeduplicationDecision(
                execution.execution_id,
                execution.gate_id,
                status,
                reasons,
                identity,
            )
        )

    if config.enabled:
        edges = _active_supersedence_edges(
            manifest_gates,
            predicates,
            raw_contracts,
            policy_active=policy_active,
        )
        retained_by_id = {execution.execution_id: execution for execution in retained}
        decision_by_id = {decision.execution_id: decision for decision in decisions}
        removed: set[str] = set()
        for source_gate_id, target_gate_id, predicate_id, predicate in edges:
            sources = sorted(
                (
                    execution
                    for execution in retained
                    if execution.gate_id == source_gate_id
                    and execution.execution_id not in removed
                ),
                key=lambda execution: execution.execution_id,
            )
            targets = sorted(
                (
                    execution
                    for execution in retained
                    if execution.gate_id == target_gate_id
                    and execution.execution_id not in removed
                ),
                key=lambda execution: execution.execution_id,
            )
            for target in targets:
                if target.replay_bypass_reason is not None:
                    continue
                if manifest_gates[target.gate_id]["mutating"]:
                    continue
                for source in sources:
                    if manifest_gates[source.gate_id]["mutating"]:
                        continue
                    eligible, evidence = evaluate_predicate(predicate, source, target)
                    if not eligible:
                        continue
                    removed.add(target.execution_id)
                    decision_by_id[target.execution_id] = DeduplicationDecision(
                        target.execution_id,
                        target.gate_id,
                        "skipped_superseded",
                        ("active_manifest_contract", "predicate_proved_same_scope"),
                        target.evidence_identity,
                        source.execution_id,
                        source.gate_id,
                        predicate_id,
                        evidence,
                    )
                    break
        retained = [
            retained_by_id[execution.execution_id]
            for execution in retained
            if execution.execution_id not in removed
        ]
        decisions = [decision_by_id[decision.execution_id] for decision in decisions]

    identity_counts: dict[tuple[str, str], int] = {}
    for execution in retained:
        if execution.evidence_identity is None:
            continue
        key = (execution.evidence_identity, str(execution.generation_state))
        identity_counts[key] = identity_counts.get(key, 0) + 1
    residual_count = sum(max(0, count - 1) for count in identity_counts.values())
    return DeduplicationResult(
        tuple(decisions),
        tuple(execution.execution_id for execution in retained),
        tuple(execution.gate_id for execution in retained),
        sum(decision.status == "skipped_duplicate" for decision in decisions),
        sum(decision.status == "skipped_superseded" for decision in decisions),
        residual_count,
        config.enabled,
        policy_active,
    )


def _activate_rc_core_fixture(
    manifest: Mapping[str, object], contracts: Mapping[str, object]
) -> tuple[dict[str, object], dict[str, object]]:
    active_manifest = deepcopy(manifest)
    active_contracts = deepcopy(contracts)
    predicate_id = "rc_diff_satisfies_core_same_scope_v1"
    for gate in active_manifest["gates"]:
        if gate["gate_id"] == "research_control_diff":
            for edge in gate["supersedes"]:
                if edge["gate_id"] == "research_control_core":
                    edge["predicate_id"] = predicate_id
                    edge["status"] = "active"
    active_contracts["activation_gate"]["current_status"] = "active"
    for predicate in active_contracts["predicate_catalog"]:
        if predicate["predicate_id"] == predicate_id:
            predicate["status"] = "active"
    for contract in active_contracts["supersedence_contracts"]:
        if contract["predicate_id"] == predicate_id:
            contract["activation_status"] = "active"
    return active_manifest, active_contracts


def _audit_execution(execution_id: str, gate_id: str, **changes: object) -> GateExecution:
    evidence = {
        "implementation_family_digest": "sha256:family",
        "core_configuration_digest": "sha256:core-config",
        "environment_digest": "sha256:env",
        "tree_hash": "git-tree:tree",
        "tree_state": "index",
        "base_ref": "HEAD",
        "staged_flag": True,
        "core_scope_digest": "sha256:scope",
        "superset_executed_core": True,
        "raw_core_failures_preserved": True,
    }
    values: dict[str, object] = {
        "execution_id": execution_id,
        "gate_id": gate_id,
        "implementation_digest": f"sha256:{gate_id}",
        "environment_digest": "sha256:env",
        "config_digest": "sha256:config",
        "scope": "tree_state=index;base_ref=HEAD",
        "tree_hash": "git-tree:tree",
        "generation_state": "post_generation",
        "predicate_evidence": evidence,
    }
    values.update(changes)
    return GateExecution(**values)  # type: ignore[arg-type]


def audit_repository(
    manifest_path: Path = DEFAULT_MANIFEST,
    contracts_path: Path = DEFAULT_CONTRACTS,
) -> dict[str, object]:
    manifest = load_manifest(manifest_path)
    contracts = load_contracts(contracts_path)
    active_manifest, active_contracts = _activate_rc_core_fixture(manifest, contracts)
    config = DeduplicationConfig(True, True, True)
    exact = _audit_execution("exact-1", "git_diff_check")
    exact_repeat = replace(exact, execution_id="exact-2")
    exact_result = deduplicate_executions(
        (exact, exact_repeat), manifest, contracts, config
    )
    source = _audit_execution("source", "research_control_diff")
    target = _audit_execution("target", "research_control_core")
    positive = deduplicate_executions(
        (target, source), active_manifest, active_contracts, config
    )
    changed_scope = replace(
        target,
        execution_id="target-working",
        scope="tree_state=working;base_ref=HEAD",
        predicate_evidence={**target.predicate_evidence, "tree_state": "working"},
    )
    negative = deduplicate_executions(
        (changed_scope, source), active_manifest, active_contracts, config
    )
    cases = [
        {
            "case_id": "exact_identity_duplicate",
            "status": "PASS" if exact_result.skipped_duplicate_count == 1 else "FAIL",
            "result": exact_result.to_dict(),
        },
        {
            "case_id": "active_same_scope_supersedence",
            "status": "PASS" if positive.superseded_count == 1 else "FAIL",
            "result": positive.to_dict(),
        },
        {
            "case_id": "cross_scope_retained",
            "status": "PASS" if negative.superseded_count == 0 else "FAIL",
            "result": negative.to_dict(),
        },
    ]
    return {
        "schema_id": "validation_deduplication_predicate_report_v1",
        "status": "PASS" if all(case["status"] == "PASS" for case in cases) else "FAIL",
        "plan_task_id": "P5-T06",
        "migration_epoch": manifest.get("migration_epoch"),
        "execution_authority": manifest.get("execution_authority"),
        "manifest_sha256": _canonical_sha256(manifest),
        "contracts_sha256": hashlib.sha256(contracts_path.read_bytes()).hexdigest(),
        "current_policy_active": contracts.get("activation_gate", {}).get("current_status")
        == "active",
        "cases": cases,
        "authority": {
            "legacy_execution_authoritative": True,
            "planner_integration_changed": False,
            "manifest_changed": False,
            "scientific_claims_changed": False,
            "physics_claim_authority": False,
            "proof_authority": False,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    audit = subcommands.add_parser("audit", help="run deterministic policy fixtures")
    audit.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    audit.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS)
    audit.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = audit_repository(args.manifest, args.contracts)
    except (OSError, DeduplicationError) as error:
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
