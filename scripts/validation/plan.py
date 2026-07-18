"""Pure deterministic validation-plan construction for the v19 planner.

This module selects and orders declared manifest gates.  It never imports an
adapter, executes a command, mutates the repository, or changes validation
authority.  The manifest's tracked authority determines whether a serialized
plan authorizes a separate executor to run commands.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable, Mapping, Sequence


PROFILES = {"fast", "affected", "checkpoint", "full", "doctor"}
SCOPES = {"working", "staged", "commit", "repository", "local_retrieval"}
TOP_LEVEL_FIELDS = {
    "schema_id",
    "schema_version",
    "manifest_id",
    "migration_epoch",
    "population_status",
    "execution_authority",
    "authority",
    "gates",
}
AUTHORITY_FIELDS = {
    "benchmark_authority",
    "gate_chair_authority",
    "ontology_authority",
    "operational_validation_only",
    "physics_claim_authority",
    "proof_authority",
    "source_authoritative",
}
GATE_FIELDS = {
    "gate_id",
    "description",
    "owner_role",
    "adapter",
    "command_compatibility",
    "input_globs",
    "output_globs",
    "global_invariant_justification",
    "scopes",
    "severity",
    "mutating",
    "cost_class",
    "prerequisites",
    "supersedes",
    "satisfies_obligations",
    "profiles",
    "path_tags",
    "selection",
    "timeout_seconds",
    "parallel_group",
    "cache_policy",
    "receipt_schema",
    "test_shard",
}
MIGRATION_EPOCHS = {
    "legacy",
    "legacy_consolidated",
    "shadow_planner",
    "planner_authoritative",
    "legacy_retired",
}
SEVERITIES = {"blocking", "advisory", "local_only"}
COST_CLASSES = {"fast", "medium", "slow"}
CACHE_POLICIES = {"ineligible", "exact_tree", "scheduled_bypass"}
CONDITION_KINDS = {
    "always",
    "profile_selected",
    "path_tag_any",
    "path_tag_all",
    "explicit_scope",
    "changed_registered_tex_pdf_required",
    "registered_mermaid_changed",
    "publication_surface_changed",
    "graph_inputs_changed",
    "task_index_inputs_changed",
    "traceability_inputs_changed",
    "scientific_checker_family",
}
ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[_:.-][a-z0-9]+)*$")
SPECIAL_CONDITION_TAGS = {
    "changed_registered_tex_pdf_required": frozenset({"required_pdf"}),
    "registered_mermaid_changed": frozenset({"mermaid"}),
    "publication_surface_changed": frozenset({"publication_spec", "html"}),
    "graph_inputs_changed": frozenset({"dependency_graph_input"}),
    "task_index_inputs_changed": frozenset({"task_index_input"}),
    "traceability_inputs_changed": frozenset({"traceability"}),
    "scientific_checker_family": frozenset({"scientific_checker"}),
}


class PlannerError(ValueError):
    """Fail-closed planner configuration error."""


def _reject_nonfinite(value: str) -> None:
    raise PlannerError(f"manifest contains non-finite number: {value}")


def _exact_object(value: object, expected: set[str], context: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise PlannerError(f"{context} must be an object")
    keys = set(value)
    if keys != expected:
        raise PlannerError(
            f"{context} fields differ: missing={sorted(expected - keys)} "
            f"unknown={sorted(keys - expected)}"
        )
    return value


def _nonblank(value: object, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PlannerError(f"{context} must be a nonblank string")
    return value


def _normalized_glob(value: str, context: str) -> None:
    if not value or value.startswith("/") or "\\" in value or "\x00" in value:
        raise PlannerError(f"{context} is not a normalized repository-relative glob")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise PlannerError(f"{context} contains an invalid path segment")


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PlannerError(f"duplicate manifest key: {key}")
        result[key] = value
    return result


def load_manifest(path: Path) -> dict[str, object]:
    """Load the JSON-as-YAML manifest without repairing malformed data."""

    try:
        value = json.loads(
            Path(path).read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite,
        )
    except (OSError, json.JSONDecodeError) as error:
        raise PlannerError(f"manifest load failed: {error}") from error
    if not isinstance(value, dict):
        raise PlannerError("manifest must be an object")
    return value


def canonical_manifest_sha256(manifest: Mapping[str, object]) -> str:
    payload = json.dumps(
        manifest,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _string_set(value: object, context: str) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise PlannerError(f"{context} must be a string array")
    if len(value) != len(set(value)):
        raise PlannerError(f"{context} contains duplicates")
    return set(value)


def _manifest_gates(manifest: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    document = _exact_object(manifest, TOP_LEVEL_FIELDS, "manifest")
    if manifest.get("schema_id") != "validation_gate_manifest_v1":
        raise PlannerError("unsupported manifest schema_id")
    if manifest.get("schema_version") != 1 or isinstance(
        manifest.get("schema_version"), bool
    ):
        raise PlannerError("unsupported manifest schema_version")
    if manifest.get("manifest_id") != "validation-gate-manifest-v1":
        raise PlannerError("unsupported manifest_id")
    migration_epoch = manifest.get("migration_epoch")
    if migration_epoch not in MIGRATION_EPOCHS:
        raise PlannerError("unsupported migration_epoch")
    if manifest.get("population_status") != "populated":
        raise PlannerError("manifest is not populated")
    execution_authority = manifest.get("execution_authority")
    if execution_authority not in {"legacy", "manifest_planner"}:
        raise PlannerError("unsupported execution_authority")
    if (
        execution_authority == "manifest_planner"
        and migration_epoch not in {"planner_authoritative", "legacy_retired"}
    ):
        raise PlannerError(
            "manifest_planner authority requires planner_authoritative or legacy_retired epoch"
        )
    if migration_epoch == "legacy_retired" and execution_authority != "manifest_planner":
        raise PlannerError("legacy_retired epoch requires manifest_planner authority")
    authority = _exact_object(document["authority"], AUTHORITY_FIELDS, "authority")
    expected_authority = {field: False for field in AUTHORITY_FIELDS}
    expected_authority["operational_validation_only"] = True
    if authority != expected_authority:
        raise PlannerError("manifest authority changes the non-promotion boundary")
    raw_gates = manifest.get("gates")
    if not isinstance(raw_gates, list) or not raw_gates:
        raise PlannerError("manifest gates must be a nonempty array")
    gates: list[dict[str, object]] = []
    ids: set[str] = set()
    for index, raw_gate in enumerate(raw_gates):
        if not isinstance(raw_gate, dict):
            raise PlannerError(f"gates[{index}] must be an object")
        raw_gate = _exact_object(raw_gate, GATE_FIELDS, f"gates[{index}]")
        gate_id = raw_gate.get("gate_id")
        if not isinstance(gate_id, str) or not gate_id:
            raise PlannerError(f"gates[{index}].gate_id must be nonblank")
        if not ID_RE.fullmatch(gate_id):
            raise PlannerError(f"gates[{index}].gate_id is not a stable lowercase ID")
        if gate_id in ids:
            raise PlannerError(f"duplicate gate_id: {gate_id}")
        ids.add(gate_id)
        for field in (
            "description",
            "owner_role",
            "adapter",
            "parallel_group",
            "test_shard",
        ):
            _nonblank(raw_gate.get(field), f"{gate_id}.{field}")
        commands = _string_set(
            raw_gate.get("command_compatibility"),
            f"{gate_id}.command_compatibility",
        )
        if not commands or any(not command.strip() for command in commands):
            raise PlannerError(f"{gate_id}.command_compatibility must be nonempty")
        broad_glob = False
        for field in ("input_globs", "output_globs"):
            globs = _string_set(raw_gate.get(field), f"{gate_id}.{field}")
            for glob in globs:
                _normalized_glob(glob, f"{gate_id}.{field}")
                broad_glob = broad_glob or glob == "**" or glob.startswith("**/")
        justification = raw_gate.get("global_invariant_justification")
        if justification is not None and not isinstance(justification, str):
            raise PlannerError(
                f"{gate_id}.global_invariant_justification must be string or null"
            )
        if broad_glob and (not isinstance(justification, str) or not justification.strip()):
            raise PlannerError(f"{gate_id} has an unjustified global glob")
        gate_scopes = _string_set(raw_gate.get("scopes"), f"{gate_id}.scopes")
        if not gate_scopes or not gate_scopes <= SCOPES:
            raise PlannerError(f"{gate_id}.scopes contains unsupported values")
        if raw_gate.get("severity") not in SEVERITIES:
            raise PlannerError(f"{gate_id}.severity is unsupported")
        if raw_gate.get("cost_class") not in COST_CLASSES:
            raise PlannerError(f"{gate_id}.cost_class is unsupported")
        profiles = _string_set(raw_gate.get("profiles"), f"{gate_id}.profiles")
        if not profiles or not profiles <= PROFILES:
            raise PlannerError(f"{gate_id}.profiles contains unsupported values")
        _string_set(raw_gate.get("path_tags"), f"{gate_id}.path_tags")
        _string_set(raw_gate.get("prerequisites"), f"{gate_id}.prerequisites")
        _string_set(
            raw_gate.get("satisfies_obligations"),
            f"{gate_id}.satisfies_obligations",
        )
        if not raw_gate["satisfies_obligations"]:
            raise PlannerError(f"{gate_id}.satisfies_obligations must be nonempty")
        if not isinstance(raw_gate.get("mutating"), bool):
            raise PlannerError(f"{gate_id}.mutating must be boolean")
        selection = _exact_object(
            raw_gate.get("selection"), {"operator", "conditions"}, f"{gate_id}.selection"
        )
        if selection.get("operator") not in {"all", "any"}:
            raise PlannerError(f"{gate_id}.selection is invalid")
        conditions = selection.get("conditions")
        if not isinstance(conditions, list) or not conditions:
            raise PlannerError(f"{gate_id}.selection.conditions must be nonempty")
        condition_ids: set[str] = set()
        for condition_index, condition in enumerate(conditions):
            if not isinstance(condition, dict):
                raise PlannerError(f"{gate_id}.selection condition must be an object")
            condition = _exact_object(
                condition,
                {"condition_id", "kind", "values"},
                f"{gate_id}.selection.conditions[{condition_index}]",
            )
            condition_id = _nonblank(
                condition.get("condition_id"), f"{gate_id}.condition_id"
            )
            if not ID_RE.fullmatch(condition_id):
                raise PlannerError(f"{gate_id}.condition_id is invalid")
            if condition_id in condition_ids:
                raise PlannerError(f"{gate_id} has duplicate condition_id {condition_id}")
            condition_ids.add(condition_id)
            kind = condition.get("kind")
            if kind not in CONDITION_KINDS:
                raise PlannerError(f"{gate_id}.selection condition kind is invalid")
            values = _string_set(condition.get("values"), f"{gate_id}.selection.values")
            if (kind == "always" and values) or (kind != "always" and not values):
                raise PlannerError(f"{gate_id}.selection condition values are invalid")
        timeout = raw_gate.get("timeout_seconds")
        if (
            not isinstance(timeout, int)
            or isinstance(timeout, bool)
            or not 1 <= timeout <= 86400
        ):
            raise PlannerError(f"{gate_id}.timeout_seconds is invalid")
        if raw_gate.get("cache_policy") not in CACHE_POLICIES:
            raise PlannerError(f"{gate_id}.cache_policy is unsupported")
        if raw_gate.get("receipt_schema") != "validation_gate_result_v1":
            raise PlannerError(f"{gate_id}.receipt_schema is unsupported")
        supersedences = raw_gate.get("supersedes")
        if not isinstance(supersedences, list):
            raise PlannerError(f"{gate_id}.supersedes must be an array")
        gates.append(raw_gate)
    for gate in gates:
        unknown = _string_set(gate["prerequisites"], "prerequisites") - ids
        if unknown:
            raise PlannerError(
                f"{gate['gate_id']} has unknown prerequisites: {sorted(unknown)}"
            )
        superseded_targets: set[str] = set()
        supersedences = gate["supersedes"]
        assert isinstance(supersedences, list)
        for index, item in enumerate(supersedences):
            item = _exact_object(
                item,
                {"gate_id", "predicate_id", "status"},
                f"{gate['gate_id']}.supersedes[{index}]",
            )
            target = _nonblank(item.get("gate_id"), "supersedence.gate_id")
            predicate = _nonblank(item.get("predicate_id"), "supersedence.predicate_id")
            if not ID_RE.fullmatch(predicate):
                raise PlannerError(f"{gate['gate_id']} has invalid supersedence predicate")
            if target not in ids or target == gate["gate_id"] or target in superseded_targets:
                raise PlannerError(f"{gate['gate_id']} has invalid supersedence target {target}")
            superseded_targets.add(target)
            if item.get("status") not in {"policy_only_inactive", "active"}:
                raise PlannerError(f"{gate['gate_id']} has invalid supersedence status")
            if item.get("status") == "active":
                raise PlannerError("active supersedence lacks an authorized evidence contract")
    _topological_order(gates, ids)
    return tuple(gates)


def _condition_result(
    condition: Mapping[str, object],
    *,
    profile: str,
    scopes: set[str],
    path_tags: set[str],
) -> bool:
    kind = str(condition.get("kind", ""))
    values = _string_set(condition.get("values"), f"condition {kind} values")
    if kind == "always":
        return not values
    if kind == "profile_selected":
        return profile in values
    if kind == "path_tag_any":
        return bool(path_tags & values)
    if kind == "path_tag_all":
        return values <= path_tags
    if kind == "explicit_scope":
        return bool(scopes & values)
    required_tags = SPECIAL_CONDITION_TAGS.get(kind)
    if required_tags is not None:
        return bool(path_tags & required_tags)
    raise PlannerError(f"unsupported selection condition kind: {kind}")


def _selection_reasons(
    gate: Mapping[str, object],
    *,
    profile: str,
    scopes: set[str],
    path_tags: set[str],
) -> tuple[bool, tuple[str, ...]]:
    selection = gate["selection"]
    assert isinstance(selection, dict)
    conditions = selection["conditions"]
    assert isinstance(conditions, list)
    evaluations: list[tuple[str, bool]] = []
    for condition in conditions:
        assert isinstance(condition, dict)
        condition_id = str(condition.get("condition_id", condition.get("kind", "condition")))
        evaluations.append(
            (
                condition_id,
                _condition_result(
                    condition,
                    profile=profile,
                    scopes=scopes,
                    path_tags=path_tags,
                ),
            )
        )
    selected = all(result for _, result in evaluations)
    if selection["operator"] == "any":
        selected = any(result for _, result in evaluations)
    reasons = tuple(sorted(f"condition:{name}" for name, result in evaluations if result))
    return selected, reasons


def _topological_order(
    gates: Sequence[Mapping[str, object]], selected: set[str]
) -> tuple[str, ...]:
    by_id = {str(gate["gate_id"]): gate for gate in gates}
    positions = {str(gate["gate_id"]): index for index, gate in enumerate(gates)}
    indegree = {gate_id: 0 for gate_id in selected}
    dependents = {gate_id: set() for gate_id in selected}
    for gate_id in selected:
        gate = by_id[gate_id]
        for prerequisite in _string_set(gate["prerequisites"], "prerequisites"):
            if prerequisite not in selected:
                continue
            indegree[gate_id] += 1
            dependents[prerequisite].add(gate_id)
    ready = [gate_id for gate_id, degree in indegree.items() if degree == 0]
    ordered: list[str] = []
    while ready:
        ready.sort(
            key=lambda gate_id: (
                0 if bool(by_id[gate_id]["mutating"]) else 1,
                positions[gate_id],
                gate_id,
            )
        )
        gate_id = ready.pop(0)
        ordered.append(gate_id)
        for dependent in sorted(dependents[gate_id]):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
    if len(ordered) != len(selected):
        cycle = sorted(gate_id for gate_id, degree in indegree.items() if degree)
        raise PlannerError(f"prerequisite graph contains a cycle: {cycle}")
    return tuple(ordered)


def _expand_prerequisites(
    gates: Sequence[Mapping[str, object]],
    selected: set[str],
    reasons: dict[str, set[str]],
) -> None:
    by_id = {str(gate["gate_id"]): gate for gate in gates}
    pending = list(sorted(selected))
    while pending:
        gate_id = pending.pop()
        for prerequisite in _string_set(by_id[gate_id]["prerequisites"], "prerequisites"):
            reasons.setdefault(prerequisite, set()).add(f"prerequisite_for:{gate_id}")
            if prerequisite not in selected:
                selected.add(prerequisite)
                pending.append(prerequisite)


def _unknown_paths(classification: Mapping[str, object]) -> tuple[str, ...]:
    details = classification.get("path_family_details", [])
    if not isinstance(details, list):
        raise PlannerError("classification.path_family_details must be an array")
    unknown: list[str] = []
    for detail in details:
        if not isinstance(detail, dict):
            raise PlannerError("classification path detail must be an object")
        tags = _string_set(detail.get("tags", []), "classification detail tags")
        if "unknown_governed_path" in tags:
            path = detail.get("path")
            if isinstance(path, str) and path:
                unknown.append(path)
    if "unknown_governed_path" in _string_set(
        classification.get("path_family_tags", []), "classification.path_family_tags"
    ) and not unknown:
        changed = classification.get("changed_paths", [])
        if isinstance(changed, list):
            unknown.extend(str(path) for path in changed)
    return tuple(sorted(set(unknown)))


@dataclass(frozen=True, slots=True)
class ValidationPlan:
    manifest_id: str
    manifest_hash: str
    requested_profile: str
    effective_profile: str
    scopes: tuple[str, ...]
    changed_paths: tuple[str, ...]
    blocked_paths: tuple[str, ...]
    path_tags: tuple[str, ...]
    role_obligations: tuple[str, ...]
    ordered_gate_ids: tuple[str, ...]
    selected_gate_ids: tuple[str, ...]
    superseded_gate_ids: tuple[str, ...]
    skipped_gate_ids: tuple[str, ...]
    unknown_paths: tuple[str, ...]
    entries: tuple[dict[str, object], ...]
    execution_authority: str
    status: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_id": "validation_plan_v1",
            "manifest_id": self.manifest_id,
            "manifest_hash": self.manifest_hash,
            "requested_profile": self.requested_profile,
            "effective_profile": self.effective_profile,
            "scopes": list(self.scopes),
            "changed_paths": list(self.changed_paths),
            "blocked_paths": list(self.blocked_paths),
            "path_tags": list(self.path_tags),
            "role_obligations": list(self.role_obligations),
            "ordered_gate_ids": list(self.ordered_gate_ids),
            "selected_gate_ids": list(self.selected_gate_ids),
            "superseded_gate_ids": list(self.superseded_gate_ids),
            "skipped_gate_ids": list(self.skipped_gate_ids),
            "unknown_paths": list(self.unknown_paths),
            "entries": list(self.entries),
            "execution_authority": self.execution_authority,
            "status": self.status,
            "planner_executes_commands": self.execution_authority == "manifest_planner",
            "authority": {
                "operational_validation_only": True,
                "legacy_result_authoritative": self.execution_authority == "legacy",
                "physics_claim_authority": False,
                "ontology_authority": False,
                "benchmark_authority": False,
                "gate_chair_authority": False,
            },
        }

    def canonical_json(self) -> str:
        return json.dumps(
            self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )


def build_plan(
    manifest: Mapping[str, object],
    classification: Mapping[str, object],
    *,
    profile: str,
    scopes: Iterable[str] = (),
    role_obligations: Iterable[str] = (),
) -> ValidationPlan:
    """Build one deterministic plan from fully declared in-memory inputs."""

    if profile not in PROFILES:
        raise PlannerError(f"unsupported profile: {profile}")
    scope_set = set(scopes)
    if not scope_set <= SCOPES:
        raise PlannerError(f"unsupported scopes: {sorted(scope_set - SCOPES)}")
    obligations = set(role_obligations)
    if any(not isinstance(value, str) or not value for value in obligations):
        raise PlannerError("role obligations must be nonblank strings")
    path_tags = _string_set(
        classification.get("path_family_tags", []), "classification.path_family_tags"
    )
    changed_paths = _string_set(
        classification.get("changed_paths", []), "classification.changed_paths"
    )
    blocked_paths = _string_set(
        classification.get("blocked_paths", []), "classification.blocked_paths"
    )
    unknown_paths = _unknown_paths(classification)
    effective_profile = "full" if unknown_paths or blocked_paths else profile
    gates = _manifest_gates(manifest)
    selected: set[str] = set()
    reasons: dict[str, set[str]] = {}
    for gate in gates:
        gate_id = str(gate["gate_id"])
        matches, condition_reasons = _selection_reasons(
            gate,
            profile=effective_profile,
            scopes=scope_set,
            path_tags=path_tags,
        )
        satisfied = _string_set(gate["satisfies_obligations"], "satisfies_obligations")
        matched_obligations = obligations & satisfied
        if matches or matched_obligations:
            selected.add(gate_id)
            reasons.setdefault(gate_id, set()).update(condition_reasons)
            reasons[gate_id].update(
                f"role_obligation:{obligation}" for obligation in matched_obligations
            )
    _expand_prerequisites(gates, selected, reasons)
    ordered = _topological_order(gates, selected)
    by_id = {str(gate["gate_id"]): gate for gate in gates}
    entries: list[dict[str, object]] = []
    for gate in gates:
        gate_id = str(gate["gate_id"])
        if gate_id in selected:
            entry_status = "selected"
            entry_reasons = sorted(reasons.get(gate_id, {"manifest_selection"}))
        else:
            entry_status = "skipped_not_applicable"
            entry_reasons = ["selection_predicate_not_satisfied"]
        entries.append(
            {
                "gate_id": gate_id,
                "status": entry_status,
                "reasons": entry_reasons,
                "mutating": bool(gate["mutating"]),
                "severity": gate.get("severity"),
                "satisfies_obligations": sorted(
                    _string_set(gate["satisfies_obligations"], "satisfies_obligations")
                ),
            }
        )
    for path in unknown_paths:
        entries.append(
            {
                "gate_id": None,
                "status": "unknown_path_full_fallback",
                "path": path,
                "reasons": ["unknown_governed_path", "effective_profile:full"],
                "mutating": False,
                "severity": "blocking",
                "satisfies_obligations": [],
            }
        )
    for path in sorted(blocked_paths):
        entries.append(
            {
                "gate_id": None,
                "status": "blocked_path",
                "path": path,
                "reasons": ["classifier_blocked_path", "effective_profile:full"],
                "mutating": False,
                "severity": "blocking",
                "satisfies_obligations": [],
            }
        )
    selected_ids = tuple(gate_id for gate_id in by_id if gate_id in selected)
    skipped_ids = tuple(gate_id for gate_id in by_id if gate_id not in selected)
    return ValidationPlan(
        manifest_id=str(manifest.get("manifest_id", "")),
        manifest_hash=canonical_manifest_sha256(manifest),
        requested_profile=profile,
        effective_profile=effective_profile,
        scopes=tuple(sorted(scope_set)),
        changed_paths=tuple(sorted(changed_paths)),
        blocked_paths=tuple(sorted(blocked_paths)),
        path_tags=tuple(sorted(path_tags)),
        role_obligations=tuple(sorted(obligations)),
        ordered_gate_ids=ordered,
        selected_gate_ids=selected_ids,
        superseded_gate_ids=(),
        skipped_gate_ids=skipped_ids,
        unknown_paths=unknown_paths,
        entries=tuple(entries),
        execution_authority=str(manifest.get("execution_authority", "")),
        status="BLOCKED_CONFIGURATION" if blocked_paths else "READY",
    )


def render_explanation(plan: ValidationPlan) -> str:
    """Render a concise deterministic human-readable plan explanation."""

    lines = [
        (
            f"validation plan requested={plan.requested_profile} "
            f"effective={plan.effective_profile} status={plan.status} "
            f"authority={plan.execution_authority}"
        ),
        f"changed_paths={len(plan.changed_paths)} selected_gates={len(plan.selected_gate_ids)}",
    ]
    for entry in plan.entries:
        gate_id = entry.get("gate_id") or entry.get("path")
        reasons = ",".join(str(value) for value in entry["reasons"])
        obligations = ",".join(str(value) for value in entry["satisfies_obligations"])
        lines.append(
            f"{entry['status']} {gate_id} reasons={reasons} obligations={obligations or '-'}"
        )
    return "\n".join(lines) + "\n"
