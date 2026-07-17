#!/usr/bin/env python3
"""Support-only checker for finite typed EqSrc orbit closure records.

This checker validates explicit finite records only. It is not proof authority,
not a general EqSrc theorem, not source-law adoption, not target metric import,
not MetricData(E) adoption, not g_eff adoption or scope expansion, not matter
coupling, not Einstein equations, not benchmark promotion, and not completed
derivation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
RESEARCH_CONTROL_SCRIPT_DIR = SCRIPT_DIR.parent
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

import strict_yaml  # noqa: E402


CHECKER_ID = "typed_eqsrc_orbit_checker"
CHECKER_VERSION = "0.1.0"
SUPPORT_ONLY = True
PROOF_AUTHORITY = False
PHYSICS_PROMOTION_AUTHORIZED = False
BOUNDARY_STATEMENT = (
    "This typed EqSrc orbit checker is support-only finite-record tooling. "
    "It has proof_authority=false and does not prove general EqSrc, adopt a "
    "source law, import a target metric, adopt MetricData(E), adopt or expand "
    "g_eff, derive matter coupling, derive Einstein equations, promote a "
    "benchmark, issue a Gate Chair verdict, or complete the derivation."
)

REQUIRED_SECTIONS = (
    "metadata",
    "typed_objects",
    "identity_maps",
    "maps",
    "inverse_maps",
    "composition_table",
    "orbits",
    "eqsrc_pairs",
    "invariant_flags",
    "forbidden_authority",
)

REQUIRED_FALSE_AUTHORITY_FLAGS = (
    "proof_authority",
    "physics_promotion_authorized",
    "source_law_adopted",
    "eqsrc_theorem_adopted",
    "target_metric_imported",
    "target_atlas_imported",
    "physical_metric_constructed",
    "metricdata_e_adopted",
    "g_eff_adopted",
    "g_eff_scope_expanded",
    "matter_coupling_derived",
    "matter_coupling_adopted",
    "stress_energy_semantics_imported",
    "stress_energy_tensor_constructed",
    "matter_action_imported",
    "einstein_equations_derived",
    "benchmark_promoted",
    "gate_chair_verdict_issued",
    "completed_derivation_claimed",
)

FORBIDDEN_KEY_FRAGMENTS = (
    "target_metric",
    "target_atlas",
    "physical_metric",
    "metricdata",
    "metric_data",
    "g_eff",
    "geff",
    "matter_coupling",
    "stress_energy",
    "matter_action",
    "einstein",
    "benchmark",
    "gate_chair",
    "completed_derivation",
)

STATUS_PRIORITY = (
    "tooling_error",
    "fail_malformed_record",
    "fail_authority_overread",
    "fail_target_import",
    "fail_type_mismatch",
    "fail_identity_map",
    "fail_inverse_map",
    "fail_composition_table",
    "fail_orbit_partition",
    "fail_orbit_closure",
    "fail_invariant_preservation",
)


class CheckerInputError(ValueError):
    """Raised when a fixture cannot be parsed into the required record shape."""


@dataclass(frozen=True)
class PredicateResult:
    predicate: str
    status: str
    message: str
    path: str = ""
    status_code: str = ""
    overread_flag: str = ""

    def to_dict(self) -> dict[str, str]:
        output = {
            "message": self.message,
            "predicate": self.predicate,
            "status": self.status,
        }
        if self.path:
            output["path"] = self.path
        if self.status_code:
            output["status_code"] = self.status_code
        if self.overread_flag:
            output["overread_flag"] = self.overread_flag
        return output


@dataclass(frozen=True)
class ExplicitMap:
    map_id: str
    source_type: str
    target_type: str
    arrows: tuple[tuple[str, str], ...]
    kind: str = "map"

    def as_dict(self) -> dict[str, Any]:
        return {
            "arrows": [{"from": left, "to": right} for left, right in self.arrows],
            "kind": self.kind,
            "map_id": self.map_id,
            "source_type": self.source_type,
            "target_type": self.target_type,
        }


@dataclass
class CheckerReport:
    checker_id: str
    checker_version: str
    fixture_id: str
    fixture_hash: str
    status: str
    predicate_results: list[PredicateResult] = field(default_factory=list)
    checked_counts: dict[str, int] = field(default_factory=dict)
    forbidden_overread_flags: list[str] = field(default_factory=list)
    boundary_statement: str = BOUNDARY_STATEMENT
    support_only: bool = SUPPORT_ONLY
    proof_authority: bool = PROOF_AUTHORITY
    physics_promotion_authorized: bool = PHYSICS_PROMOTION_AUTHORIZED
    source_artifact_refs: list[str] = field(default_factory=list)
    tooling_error: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_statement": self.boundary_statement,
            "checked_counts": self.checked_counts,
            "checker_id": self.checker_id,
            "checker_version": self.checker_version,
            "fixture_hash": self.fixture_hash,
            "fixture_id": self.fixture_id,
            "forbidden_overread_flags": self.forbidden_overread_flags,
            "physics_promotion_authorized": self.physics_promotion_authorized,
            "predicate_results": [
                predicate.to_dict() for predicate in self.predicate_results
            ],
            "proof_authority": self.proof_authority,
            "source_artifact_refs": self.source_artifact_refs,
            "status": self.status,
            "support_only": self.support_only,
            "tooling_error": self.tooling_error,
        }


def _as_map(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any) -> str:
    return str(value).strip()


def _pass(predicate: str, message: str, path: str = "") -> PredicateResult:
    return PredicateResult(predicate=predicate, status="pass", message=message, path=path)


def _fail(
    predicate: str,
    status_code: str,
    message: str,
    path: str = "",
    overread_flag: str = "",
) -> PredicateResult:
    return PredicateResult(
        predicate=predicate,
        status="fail",
        message=message,
        path=path,
        status_code=status_code,
        overread_flag=overread_flag,
    )


def _dedupe_sorted(values: Sequence[str]) -> list[str]:
    return sorted({value for value in values if value})


def _walk(value: Any, path: str = "") -> list[tuple[str, Any]]:
    rows = [(path, value)]
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            rows.extend(_walk(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(_walk(child, f"{path}[{index}]"))
    return rows


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fixture(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if path.suffix == ".json" or stripped.startswith("{"):
        parsed = json.loads(text)
    else:
        parsed = strict_yaml.loads(text)
    if not isinstance(parsed, dict):
        raise CheckerInputError("top-level fixture must be a map")
    return parsed


def typed_objects(data: Mapping[str, Any]) -> dict[str, str]:
    objects: dict[str, str] = {}
    for item in _as_list(data.get("typed_objects")):
        if not isinstance(item, dict):
            continue
        object_id = _text(item.get("id", ""))
        type_id = _text(item.get("type", ""))
        if object_id and type_id:
            objects[object_id] = type_id
    return objects


def objects_by_type(data: Mapping[str, Any]) -> dict[str, set[str]]:
    by_type: dict[str, set[str]] = {}
    for object_id, type_id in typed_objects(data).items():
        by_type.setdefault(type_id, set()).add(object_id)
    return by_type


def parse_map_record(record: Mapping[str, Any], *, kind: str) -> ExplicitMap:
    if kind == "identity":
        type_id = _text(record.get("type", ""))
        source_type = type_id
        target_type = type_id
    else:
        source_type = _text(record.get("source_type", ""))
        target_type = _text(record.get("target_type", ""))
    arrows: list[tuple[str, str]] = []
    for arrow in _as_list(record.get("arrows")):
        if isinstance(arrow, dict):
            arrows.append((_text(arrow.get("from", "")), _text(arrow.get("to", ""))))
    return ExplicitMap(
        map_id=_text(record.get("id", "")),
        source_type=source_type,
        target_type=target_type,
        arrows=tuple(arrows),
        kind=kind,
    )


def all_explicit_maps(data: Mapping[str, Any]) -> dict[str, ExplicitMap]:
    maps: dict[str, ExplicitMap] = {}
    for record in _as_list(data.get("identity_maps")):
        if isinstance(record, dict):
            parsed = parse_map_record(record, kind="identity")
            if parsed.map_id:
                maps[parsed.map_id] = parsed
    for record in _as_list(data.get("maps")):
        if isinstance(record, dict):
            parsed = parse_map_record(record, kind="map")
            if parsed.map_id:
                maps[parsed.map_id] = parsed
    return maps


def orbit_by_member(data: Mapping[str, Any]) -> dict[str, str]:
    by_member: dict[str, str] = {}
    for orbit in _as_list(data.get("orbits")):
        if not isinstance(orbit, dict):
            continue
        orbit_id = _text(orbit.get("id", ""))
        for member in _as_list(orbit.get("members")):
            member_id = _text(member)
            if member_id:
                by_member[member_id] = orbit_id
    return by_member


def map_arrows_by_from(explicit_map: ExplicitMap) -> dict[str, str]:
    return {left: right for left, right in explicit_map.arrows}


def compose_maps(left: ExplicitMap, right: ExplicitMap) -> tuple[tuple[str, str], ...] | None:
    if right.target_type != left.source_type:
        return None
    left_arrows = map_arrows_by_from(left)
    composed: list[tuple[str, str]] = []
    for source, middle in right.arrows:
        if middle not in left_arrows:
            return None
        composed.append((source, left_arrows[middle]))
    return tuple(sorted(composed))


def predicate_required_sections_present(data: Mapping[str, Any]) -> PredicateResult:
    for section in REQUIRED_SECTIONS:
        if section not in data:
            return _fail(
                "required_sections_present",
                "fail_malformed_record",
                f"missing required section {section!r}",
                section,
            )
    for path, value in _walk(data):
        if value is None:
            return _fail(
                "required_sections_present",
                "fail_malformed_record",
                "null values are not allowed in finite explicit records",
                path,
            )
    return _pass("required_sections_present", "all required finite-record sections are present")


def predicate_support_only_authority_flags(data: Mapping[str, Any]) -> PredicateResult:
    metadata = _as_map(data.get("metadata"))
    required_values = {
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "eqsrc_theorem_authority": False,
    }
    for key, expected in required_values.items():
        if metadata.get(key) is not expected:
            return _fail(
                "support_only_authority_flags",
                "fail_authority_overread",
                f"metadata.{key} must be {str(expected).lower()}",
                f"metadata.{key}",
                key,
            )
    if metadata.get("boundary_statement") != BOUNDARY_STATEMENT:
        return _fail(
            "support_only_authority_flags",
            "fail_authority_overread",
            "metadata boundary statement must match the checker boundary exactly",
            "metadata.boundary_statement",
            "boundary_statement_drift",
        )
    return _pass("support_only_authority_flags", "support-only authority flags are exact")


def predicate_no_forbidden_authority(data: Mapping[str, Any]) -> PredicateResult:
    forbidden = _as_map(data.get("forbidden_authority"))
    for key in REQUIRED_FALSE_AUTHORITY_FLAGS:
        if forbidden.get(key) is not False:
            status = "fail_target_import" if key.startswith("target_") else "fail_authority_overread"
            return _fail(
                "no_forbidden_authority",
                status,
                f"forbidden_authority.{key} must be false",
                f"forbidden_authority.{key}",
                key,
            )

    allowed_forbidden_paths = {"forbidden_authority"}
    for key in REQUIRED_FALSE_AUTHORITY_FLAGS:
        allowed_forbidden_paths.add(f"forbidden_authority.{key}")
    for path, _value in _walk(data):
        if not path or path in allowed_forbidden_paths or path.startswith("metadata.boundary_statement"):
            continue
        key = path.rsplit(".", 1)[-1].split("[", 1)[0].lower()
        if any(fragment in key for fragment in FORBIDDEN_KEY_FRAGMENTS):
            return _fail(
                "no_forbidden_authority",
                "fail_target_import",
                f"forbidden target or downstream authority key {key!r} appears outside forbidden_authority",
                path,
                key,
            )
    return _pass("no_forbidden_authority", "forbidden authority flags are explicitly false")


def predicate_typed_objects_well_formed(data: Mapping[str, Any]) -> PredicateResult:
    seen: set[str] = set()
    objects = _as_list(data.get("typed_objects"))
    if not objects:
        return _fail(
            "typed_objects_well_formed",
            "fail_malformed_record",
            "typed_objects must be a nonempty finite list",
            "typed_objects",
        )
    for index, item in enumerate(objects):
        if not isinstance(item, dict):
            return _fail(
                "typed_objects_well_formed",
                "fail_malformed_record",
                "typed object entries must be maps",
                f"typed_objects[{index}]",
            )
        object_id = _text(item.get("id", ""))
        type_id = _text(item.get("type", ""))
        if not object_id or not type_id:
            return _fail(
                "typed_objects_well_formed",
                "fail_malformed_record",
                "typed objects must name id and type",
                f"typed_objects[{index}]",
            )
        if object_id in seen:
            return _fail(
                "typed_objects_well_formed",
                "fail_malformed_record",
                f"duplicate typed object id {object_id!r}",
                "typed_objects",
            )
        if item.get("source_only") is not True:
            return _fail(
                "typed_objects_well_formed",
                "fail_authority_overread",
                f"typed object {object_id!r} must set source_only true",
                f"typed_objects[{index}].source_only",
                "source_only_false",
            )
        seen.add(object_id)
    return _pass("typed_objects_well_formed", "typed source-only objects are finite and unique")


def validate_map_totality(
    explicit_map: ExplicitMap,
    data: Mapping[str, Any],
    *,
    predicate: str,
    status_code: str,
) -> PredicateResult | None:
    object_types = typed_objects(data)
    by_type = objects_by_type(data)
    if not explicit_map.map_id or not explicit_map.source_type or not explicit_map.target_type:
        return _fail(
            predicate,
            status_code,
            "map records must name id source type and target type",
            "maps",
        )
    if explicit_map.source_type not in by_type or explicit_map.target_type not in by_type:
        return _fail(
            predicate,
            "fail_type_mismatch",
            f"map {explicit_map.map_id!r} references unknown source or target type",
            explicit_map.map_id,
        )
    seen_from: set[str] = set()
    for left, right in explicit_map.arrows:
        if left in seen_from:
            return _fail(
                predicate,
                status_code,
                f"map {explicit_map.map_id!r} has duplicate source arrow {left!r}",
                explicit_map.map_id,
            )
        seen_from.add(left)
        if left not in object_types or right not in object_types:
            return _fail(
                predicate,
                "fail_type_mismatch",
                f"map {explicit_map.map_id!r} references undeclared object",
                explicit_map.map_id,
            )
        if object_types[left] != explicit_map.source_type:
            return _fail(
                predicate,
                "fail_type_mismatch",
                f"map {explicit_map.map_id!r} source object {left!r} has wrong type",
                explicit_map.map_id,
            )
        if object_types[right] != explicit_map.target_type:
            return _fail(
                predicate,
                "fail_type_mismatch",
                f"map {explicit_map.map_id!r} target object {right!r} has wrong type",
                explicit_map.map_id,
            )
    expected_sources = by_type[explicit_map.source_type]
    if seen_from != expected_sources:
        return _fail(
            predicate,
            status_code,
            f"map {explicit_map.map_id!r} is not total on source type {explicit_map.source_type!r}",
            explicit_map.map_id,
        )
    return None


def predicate_identity_maps_explicit_and_total(data: Mapping[str, Any]) -> PredicateResult:
    by_type = objects_by_type(data)
    identities = [
        parse_map_record(record, kind="identity")
        for record in _as_list(data.get("identity_maps"))
        if isinstance(record, dict)
    ]
    identity_types = {_text(identity.source_type) for identity in identities}
    if identity_types != set(by_type):
        return _fail(
            "identity_maps_explicit_and_total",
            "fail_identity_map",
            "identity maps must provide exactly one declared identity type per object type",
            "identity_maps",
        )
    seen_ids: set[str] = set()
    for identity in identities:
        if identity.map_id in seen_ids:
            return _fail(
                "identity_maps_explicit_and_total",
                "fail_identity_map",
                f"duplicate identity map id {identity.map_id!r}",
                "identity_maps",
            )
        seen_ids.add(identity.map_id)
        totality_result = validate_map_totality(
            identity,
            data,
            predicate="identity_maps_explicit_and_total",
            status_code="fail_identity_map",
        )
        if totality_result:
            return totality_result
        for left, right in identity.arrows:
            if left != right:
                return _fail(
                    "identity_maps_explicit_and_total",
                    "fail_identity_map",
                    f"identity map {identity.map_id!r} must map every object to itself",
                    identity.map_id,
                )
    return _pass("identity_maps_explicit_and_total", "identity maps are explicit and total")


def predicate_maps_are_total_and_typed(data: Mapping[str, Any]) -> PredicateResult:
    map_records = [
        parse_map_record(record, kind="map")
        for record in _as_list(data.get("maps"))
        if isinstance(record, dict)
    ]
    if not map_records:
        return _fail(
            "maps_are_total_and_typed",
            "fail_malformed_record",
            "at least one non-identity map must be declared",
            "maps",
        )
    seen_ids: set[str] = set()
    for explicit_map in map_records:
        if explicit_map.map_id in seen_ids:
            return _fail(
                "maps_are_total_and_typed",
                "fail_malformed_record",
                f"duplicate map id {explicit_map.map_id!r}",
                "maps",
            )
        seen_ids.add(explicit_map.map_id)
        totality_result = validate_map_totality(
            explicit_map,
            data,
            predicate="maps_are_total_and_typed",
            status_code="fail_malformed_record",
        )
        if totality_result:
            return totality_result
    return _pass("maps_are_total_and_typed", "declared maps are total on their finite source types")


def predicate_inverse_maps_declared_and_verified(data: Mapping[str, Any]) -> PredicateResult:
    maps = all_explicit_maps(data)
    if not _as_list(data.get("inverse_maps")):
        return _fail(
            "inverse_maps_declared_and_verified",
            "fail_inverse_map",
            "inverse_maps must be a nonempty explicit list",
            "inverse_maps",
        )
    for row in _as_list(data.get("inverse_maps")):
        if not isinstance(row, dict):
            return _fail(
                "inverse_maps_declared_and_verified",
                "fail_inverse_map",
                "inverse map entries must be maps",
                "inverse_maps",
            )
        map_id = _text(row.get("map", ""))
        inverse_id = _text(row.get("inverse", ""))
        if map_id not in maps or inverse_id not in maps:
            return _fail(
                "inverse_maps_declared_and_verified",
                "fail_inverse_map",
                f"inverse row references unknown maps {map_id!r}, {inverse_id!r}",
                "inverse_maps",
            )
        left = maps[map_id]
        right = maps[inverse_id]
        if left.source_type != right.target_type or left.target_type != right.source_type:
            return _fail(
                "inverse_maps_declared_and_verified",
                "fail_inverse_map",
                f"inverse row {map_id!r}/{inverse_id!r} has incompatible types",
                "inverse_maps",
            )
        left_right = compose_maps(left, right)
        right_left = compose_maps(right, left)
        source_identity = next(
            (item for item in maps.values() if item.kind == "identity" and item.source_type == left.source_type),
            None,
        )
        target_identity = next(
            (item for item in maps.values() if item.kind == "identity" and item.source_type == left.target_type),
            None,
        )
        if source_identity is None or target_identity is None:
            return _fail(
                "inverse_maps_declared_and_verified",
                "fail_inverse_map",
                "inverse verification requires identity maps for both types",
                "identity_maps",
            )
        if left_right != tuple(sorted(target_identity.arrows)):
            return _fail(
                "inverse_maps_declared_and_verified",
                "fail_inverse_map",
                f"{map_id!r} after {inverse_id!r} does not equal target identity",
                "inverse_maps",
            )
        if right_left != tuple(sorted(source_identity.arrows)):
            return _fail(
                "inverse_maps_declared_and_verified",
                "fail_inverse_map",
                f"{inverse_id!r} after {map_id!r} does not equal source identity",
                "inverse_maps",
            )
    return _pass("inverse_maps_declared_and_verified", "inverse maps compose to declared identities")


def predicate_composition_table_explicit_and_correct(data: Mapping[str, Any]) -> PredicateResult:
    maps = all_explicit_maps(data)
    rows = _as_list(data.get("composition_table"))
    if not rows:
        return _fail(
            "composition_table_explicit_and_correct",
            "fail_composition_table",
            "composition_table must be nonempty",
            "composition_table",
        )
    for row in rows:
        if not isinstance(row, dict):
            return _fail(
                "composition_table_explicit_and_correct",
                "fail_composition_table",
                "composition entries must be maps",
                "composition_table",
            )
        left_id = _text(row.get("left", ""))
        right_id = _text(row.get("right", ""))
        result_id = _text(row.get("result", ""))
        if left_id not in maps or right_id not in maps or result_id not in maps:
            return _fail(
                "composition_table_explicit_and_correct",
                "fail_composition_table",
                f"composition row references unknown map {left_id!r}, {right_id!r}, or {result_id!r}",
                "composition_table",
            )
        composed = compose_maps(maps[left_id], maps[right_id])
        if composed is None:
            return _fail(
                "composition_table_explicit_and_correct",
                "fail_composition_table",
                f"composition {left_id!r} after {right_id!r} is type-incompatible",
                "composition_table",
            )
        expected = tuple(sorted(maps[result_id].arrows))
        if composed != expected:
            return _fail(
                "composition_table_explicit_and_correct",
                "fail_composition_table",
                f"composition {left_id!r} after {right_id!r} does not equal {result_id!r}",
                "composition_table",
            )
    return _pass("composition_table_explicit_and_correct", "explicit composition rows match finite arrows")


def predicate_orbits_partition_typed_objects(data: Mapping[str, Any]) -> PredicateResult:
    object_types = typed_objects(data)
    seen_members: dict[str, str] = {}
    for orbit in _as_list(data.get("orbits")):
        if not isinstance(orbit, dict):
            return _fail(
                "orbits_partition_typed_objects",
                "fail_orbit_partition",
                "orbit entries must be maps",
                "orbits",
            )
        orbit_id = _text(orbit.get("id", ""))
        type_id = _text(orbit.get("type", ""))
        members = [_text(member) for member in _as_list(orbit.get("members"))]
        if not orbit_id or not type_id or not members:
            return _fail(
                "orbits_partition_typed_objects",
                "fail_orbit_partition",
                "each orbit must name id type and at least one member",
                "orbits",
            )
        for member in members:
            if member not in object_types:
                return _fail(
                    "orbits_partition_typed_objects",
                    "fail_orbit_partition",
                    f"orbit {orbit_id!r} references undeclared object {member!r}",
                    "orbits.members",
                )
            if object_types[member] != type_id:
                return _fail(
                    "orbits_partition_typed_objects",
                    "fail_type_mismatch",
                    f"orbit {orbit_id!r} member {member!r} has wrong type",
                    "orbits.members",
                )
            if member in seen_members:
                return _fail(
                    "orbits_partition_typed_objects",
                    "fail_orbit_partition",
                    f"object {member!r} appears in multiple orbits",
                    "orbits.members",
                )
            seen_members[member] = orbit_id
    if set(seen_members) != set(object_types):
        return _fail(
            "orbits_partition_typed_objects",
            "fail_orbit_partition",
            "orbits must partition exactly the declared typed objects",
            "orbits",
        )
    return _pass("orbits_partition_typed_objects", "orbits partition declared typed objects")


def predicate_maps_preserve_orbit_closure(data: Mapping[str, Any]) -> PredicateResult:
    member_orbits = orbit_by_member(data)
    for explicit_map in all_explicit_maps(data).values():
        for left, right in explicit_map.arrows:
            left_orbit = member_orbits.get(left)
            right_orbit = member_orbits.get(right)
            if not left_orbit or not right_orbit:
                return _fail(
                    "maps_preserve_orbit_closure",
                    "fail_orbit_closure",
                    f"map {explicit_map.map_id!r} references object outside declared orbits",
                    explicit_map.map_id,
                )
            if left_orbit != right_orbit:
                return _fail(
                    "maps_preserve_orbit_closure",
                    "fail_orbit_closure",
                    f"map {explicit_map.map_id!r} sends {left!r} outside its EqSrc orbit",
                    explicit_map.map_id,
                )
    return _pass("maps_preserve_orbit_closure", "all explicit maps preserve declared orbit closure")


def predicate_eqsrc_pairs_are_orbit_local(data: Mapping[str, Any]) -> PredicateResult:
    object_types = typed_objects(data)
    member_orbits = orbit_by_member(data)
    pairs = _as_list(data.get("eqsrc_pairs"))
    if not pairs:
        return _fail(
            "eqsrc_pairs_are_orbit_local",
            "fail_malformed_record",
            "eqsrc_pairs must be nonempty",
            "eqsrc_pairs",
        )
    for pair in pairs:
        if not isinstance(pair, dict):
            return _fail(
                "eqsrc_pairs_are_orbit_local",
                "fail_malformed_record",
                "eqsrc pair entries must be maps",
                "eqsrc_pairs",
            )
        left = _text(pair.get("left", ""))
        right = _text(pair.get("right", ""))
        orbit = _text(pair.get("orbit", ""))
        if left not in object_types or right not in object_types:
            return _fail(
                "eqsrc_pairs_are_orbit_local",
                "fail_malformed_record",
                f"EqSrc pair references undeclared object {left!r} or {right!r}",
                "eqsrc_pairs",
            )
        if object_types[left] != object_types[right]:
            return _fail(
                "eqsrc_pairs_are_orbit_local",
                "fail_type_mismatch",
                f"EqSrc pair {left!r}, {right!r} crosses types",
                "eqsrc_pairs",
            )
        if member_orbits.get(left) != orbit or member_orbits.get(right) != orbit:
            return _fail(
                "eqsrc_pairs_are_orbit_local",
                "fail_orbit_closure",
                f"EqSrc pair {left!r}, {right!r} is not local to declared orbit {orbit!r}",
                "eqsrc_pairs",
            )
    return _pass("eqsrc_pairs_are_orbit_local", "EqSrc pairs are type-local and orbit-local")


def predicate_source_only_invariant_flags_preserved(data: Mapping[str, Any]) -> PredicateResult:
    flags = _as_map(data.get("invariant_flags"))
    required = {
        "source_only_invariants_preserved": True,
        "target_import_used": False,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "fail_closed_for_missing_data": True,
    }
    for key, expected in required.items():
        if flags.get(key) is not expected:
            return _fail(
                "source_only_invariant_flags_preserved",
                "fail_invariant_preservation",
                f"invariant_flags.{key} must be {str(expected).lower()}",
                f"invariant_flags.{key}",
                key if expected is False else "",
            )
    for orbit in _as_list(data.get("orbits")):
        if not isinstance(orbit, dict):
            continue
        orbit_flags = _as_map(orbit.get("invariant_flags"))
        if orbit_flags.get("source_only_invariants_preserved") is not True:
            return _fail(
                "source_only_invariant_flags_preserved",
                "fail_invariant_preservation",
                f"orbit {orbit.get('id', '')!r} must preserve source-only invariant flags",
                "orbits.invariant_flags",
            )
        if orbit_flags.get("target_import_used") is not False:
            return _fail(
                "source_only_invariant_flags_preserved",
                "fail_target_import",
                f"orbit {orbit.get('id', '')!r} must not use target import",
                "orbits.invariant_flags.target_import_used",
                "target_import_used",
            )
        if orbit_flags.get("proof_authority") is not False:
            return _fail(
                "source_only_invariant_flags_preserved",
                "fail_authority_overread",
                f"orbit {orbit.get('id', '')!r} must not claim proof authority",
                "orbits.invariant_flags.proof_authority",
                "proof_authority",
            )
    return _pass("source_only_invariant_flags_preserved", "source-only invariant flags are preserved")


def predicate_fail_closed_missing_data_controls_present(data: Mapping[str, Any]) -> PredicateResult:
    controls = _as_map(data.get("invariant_flags"))
    if controls.get("fail_closed_for_missing_data") is not True:
        return _fail(
            "fail_closed_missing_data_controls_present",
            "fail_malformed_record",
            "record must declare fail_closed_for_missing_data true",
            "invariant_flags.fail_closed_for_missing_data",
        )
    if not _as_list(data.get("composition_table")):
        return _fail(
            "fail_closed_missing_data_controls_present",
            "fail_malformed_record",
            "missing composition table data fails closed",
            "composition_table",
        )
    return _pass("fail_closed_missing_data_controls_present", "missing-data controls are explicit and fail closed")


PREDICATES = (
    predicate_required_sections_present,
    predicate_support_only_authority_flags,
    predicate_no_forbidden_authority,
    predicate_typed_objects_well_formed,
    predicate_identity_maps_explicit_and_total,
    predicate_maps_are_total_and_typed,
    predicate_inverse_maps_declared_and_verified,
    predicate_composition_table_explicit_and_correct,
    predicate_orbits_partition_typed_objects,
    predicate_maps_preserve_orbit_closure,
    predicate_eqsrc_pairs_are_orbit_local,
    predicate_source_only_invariant_flags_preserved,
    predicate_fail_closed_missing_data_controls_present,
)


def select_status(results: Sequence[PredicateResult]) -> str:
    codes = {result.status_code for result in results if result.status == "fail"}
    if not codes:
        return "pass_support_only"
    for code in STATUS_PRIORITY:
        if code in codes:
            return code
    return "fail_malformed_record"


def checked_counts(data: Mapping[str, Any]) -> dict[str, int]:
    return {
        "composition_rows": len(_as_list(data.get("composition_table"))),
        "eqsrc_pairs": len(_as_list(data.get("eqsrc_pairs"))),
        "identity_maps": len(_as_list(data.get("identity_maps"))),
        "inverse_rows": len(_as_list(data.get("inverse_maps"))),
        "maps": len(_as_list(data.get("maps"))),
        "orbits": len(_as_list(data.get("orbits"))),
        "typed_objects": len(_as_list(data.get("typed_objects"))),
    }


def check_fixture(data: Mapping[str, Any], *, fixture_hash: str = "") -> CheckerReport:
    metadata = _as_map(data.get("metadata"))
    predicate_results = [predicate(data) for predicate in PREDICATES]
    overread_flags = [
        result.overread_flag for result in predicate_results if result.overread_flag
    ]
    return CheckerReport(
        checker_id=CHECKER_ID,
        checker_version=CHECKER_VERSION,
        fixture_id=_text(metadata.get("fixture_id", "")) or "unknown_fixture",
        fixture_hash=fixture_hash,
        status=select_status(predicate_results),
        predicate_results=predicate_results,
        checked_counts=checked_counts(data),
        forbidden_overread_flags=_dedupe_sorted(overread_flags),
        source_artifact_refs=sorted(
            _text(path)
            for path in _as_list(metadata.get("source_artifact_paths"))
            if _text(path)
        ),
    )


def malformed_report(
    fixture_path: Path,
    message: str,
    *,
    status: str = "fail_malformed_record",
) -> CheckerReport:
    return CheckerReport(
        checker_id=CHECKER_ID,
        checker_version=CHECKER_VERSION,
        fixture_id=fixture_path.stem,
        fixture_hash=sha256_file(fixture_path) if fixture_path.exists() else "",
        status=status,
        predicate_results=[
            _fail(
                "required_sections_present",
                status,
                message,
                str(fixture_path),
            )
        ],
        checked_counts={},
        forbidden_overread_flags=[],
        source_artifact_refs=[],
        tooling_error=status == "tooling_error",
    )


def check_path(path: Path) -> CheckerReport:
    data = load_fixture(path)
    return check_fixture(data, fixture_hash=sha256_file(path))


def json_text(report: CheckerReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"


def markdown_text(report: CheckerReport) -> str:
    lines = [
        "# Typed EqSrc Orbit Checker Report",
        "",
        BOUNDARY_STATEMENT,
        "",
        f"- Checker: `{report.checker_id}`",
        f"- Version: `{report.checker_version}`",
        f"- Fixture: `{report.fixture_id}`",
        f"- Status: `{report.status}`",
        f"- Fixture hash: `{report.fixture_hash}`",
        f"- Support only: `{str(report.support_only).lower()}`",
        f"- Proof authority: `{str(report.proof_authority).lower()}`",
        "",
        "## Predicate Results",
        "",
    ]
    for result in report.predicate_results:
        lines.append(
            f"- `{result.predicate}`: `{result.status}`"
            + (f" ({result.status_code})" if result.status_code else "")
            + f" - {result.message}"
        )
    lines.extend(
        [
            "",
            "## Authority",
            "",
            "This report is finite-record support only. It does not promote any physics state.",
            "",
        ]
    )
    return "\n".join(lines)


def write_if_requested(path: Path | None, text: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, type=Path, help="Typed EqSrc YAML or JSON fixture")
    parser.add_argument("--json", action="store_true", help="Emit JSON report on stdout")
    parser.add_argument("--json-output", type=Path, help="Write JSON report to a file")
    parser.add_argument("--markdown", type=Path, help="Write a Markdown report to a file")
    args = parser.parse_args(argv)

    try:
        report = check_path(args.fixture)
    except (CheckerInputError, strict_yaml.StrictYamlError, json.JSONDecodeError, OSError) as exc:
        report = malformed_report(args.fixture, str(exc))

    output = json_text(report)
    write_if_requested(args.json_output, output)
    write_if_requested(args.markdown, markdown_text(report))
    if args.json or not args.markdown:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
