#!/usr/bin/env python3
"""Validate the bounded v21 P10-T03 candidate identity and lineage snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = Path("research_control/tasks/RT-20260721-005")
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
SCHEMA_PATH = ARTIFACT_ROOT / "v21_candidate_lineage_schema.md"
SEED_PATH = ARTIFACT_ROOT / "v21_candidate_lineage_historical_seed.json"
REGISTRY_PATH = ARTIFACT_ROOT / "v21_candidate_lineage_registry.json"
VALIDATION_PATH = ARTIFACT_ROOT / "v21_candidate_lineage_validation.json"
RECEIPT_PATH = ARTIFACT_ROOT / "v21_candidate_lineage_compact_receipt.json"
SOURCE_INVENTORY_PATH = Path(
    "research_control/tasks/RT-20260720-010/artifacts/eqsrc_canonical_choice_family_inventory.json"
)
SOURCE_GRAPH_PATH = Path(
    "research_control/tasks/RT-20260720-010/artifacts/eqsrc_candidate_lineage_graph.json"
)
SNAPSHOT_AS_OF = "2026-07-22T02:21:42Z"


def load_json(relative_path: Path) -> dict[str, Any]:
    value = json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative_path} must contain a JSON object")
    return value


def file_sha256(relative_path: str | Path) -> str:
    return hashlib.sha256((REPO_ROOT / Path(relative_path)).read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_schema_contract() -> dict[str, Any]:
    text = (REPO_ROOT / SCHEMA_PATH).read_text(encoding="utf-8")
    matches = re.findall(r"```json\n(.*?)\n```", text, flags=re.DOTALL)
    if len(matches) != 1:
        raise ValueError("schema must contain exactly one JSON machine contract")
    value = json.loads(matches[0])
    if not isinstance(value, dict):
        raise ValueError("schema machine contract must be a JSON object")
    return value


def id_list(records: list[dict[str, Any]], key: str) -> list[str]:
    return [str(record.get(key, "")) for record in records]


def duplicate_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def acyclic(candidate_ids: set[str], edges: list[dict[str, Any]]) -> bool:
    adjacency: dict[str, list[str]] = {candidate_id: [] for candidate_id in candidate_ids}
    for edge in edges:
        source = str(edge.get("from_candidate_id", ""))
        target = str(edge.get("to_candidate_id", ""))
        if source in adjacency:
            adjacency[source].append(target)

    state: dict[str, int] = {candidate_id: 0 for candidate_id in candidate_ids}

    def visit(node: str) -> bool:
        state[node] = 1
        for target in adjacency[node]:
            if target not in state:
                continue
            if state[target] == 1:
                return False
            if state[target] == 0 and not visit(target):
                return False
        state[node] = 2
        return True

    return all(state[node] != 0 or visit(node) for node in sorted(candidate_ids))


def validate() -> tuple[dict[str, Any], dict[str, Any]]:
    errors: list[str] = []
    checks: dict[str, bool] = {}

    def record(check_id: str, condition: bool, detail: str) -> None:
        checks[check_id] = checks.get(check_id, True) and condition
        if not condition:
            errors.append(f"{check_id}: {detail}")

    contract = load_schema_contract()
    seed = load_json(SEED_PATH)
    registry = load_json(REGISTRY_PATH)
    source_inventory = load_json(SOURCE_INVENTORY_PATH)
    source_graph = load_json(SOURCE_GRAPH_PATH)

    record(
        "schema_identity",
        contract.get("schema_id") == "v21_candidate_identity_lineage_v1",
        "unexpected contract schema_id",
    )
    record(
        "registry_schema_binding",
        registry.get("contract_schema_id") == contract.get("schema_id")
        and seed.get("contract_schema_id") == contract.get("schema_id"),
        "seed or registry contract_schema_id mismatch",
    )
    record(
        "schema_content_hash",
        registry.get("schema_sha256") == file_sha256(SCHEMA_PATH),
        "registry schema hash does not match schema artifact",
    )
    record(
        "historical_seed_content_hash",
        registry.get("historical_seed_sha256") == file_sha256(SEED_PATH),
        "registry seed hash does not match historical seed artifact",
    )

    for source_path, expected_hash in seed.get("source_hashes", {}).items():
        path = REPO_ROOT / source_path
        record(
            "historical_source_hashes",
            path.is_file() and file_sha256(source_path) == expected_hash,
            f"source hash drift for {source_path}",
        )

    families = seed.get("families", [])
    candidates = seed.get("candidates", [])
    edges = seed.get("lineage_edges", [])
    stages = seed.get("stage_records", [])
    family_events = seed.get("family_events", [])
    explicit_absences = seed.get("explicit_absences", [])
    record("seed_collections", all(isinstance(value, list) for value in (families, candidates, edges, stages, family_events, explicit_absences)), "seed collections must be arrays")

    family_ids = id_list(families, "family_id")
    candidate_ids = id_list(candidates, "immutable_candidate_id")
    edge_ids = id_list(edges, "edge_id")
    stage_ids = id_list(stages, "stage_id")
    family_event_ids = id_list(family_events, "event_id")
    absence_ids = id_list(explicit_absences, "absence_id")
    record("unique_family_ids", not duplicate_values(family_ids) and all(family_ids), f"duplicate or blank family IDs: {duplicate_values(family_ids)}")
    record("unique_candidate_ids", not duplicate_values(candidate_ids) and all(candidate_ids), f"duplicate or blank candidate IDs: {duplicate_values(candidate_ids)}")
    record("unique_edge_ids", not duplicate_values(edge_ids) and all(edge_ids), f"duplicate or blank edge IDs: {duplicate_values(edge_ids)}")
    record("unique_stage_ids", not duplicate_values(stage_ids) and all(stage_ids), f"duplicate or blank stage IDs: {duplicate_values(stage_ids)}")
    record("unique_family_event_ids", not duplicate_values(family_event_ids) and all(family_event_ids), f"duplicate or blank family-event IDs: {duplicate_values(family_event_ids)}")
    record("unique_explicit_absence_ids", not duplicate_values(absence_ids) and all(absence_ids), f"duplicate or blank absence IDs: {duplicate_values(absence_ids)}")

    family_by_id = {str(item["family_id"]): item for item in families}
    candidate_by_id = {str(item["immutable_candidate_id"]): item for item in candidates}
    source_family_by_id = {
        str(item["family_id"]): item for item in source_inventory.get("families", [])
    }
    source_candidate_by_id = {
        str(item["immutable_candidate_id"]): item
        for item in source_inventory.get("candidates", [])
    }

    family_identity_fields = contract.get("family_identity_fields", [])
    candidate_identity_fields = contract.get("candidate_identity_fields", [])
    computed_family_index: dict[str, str] = {}
    for family_id, family in family_by_id.items():
        basis = {field: family.get(field) for field in family_identity_fields}
        digest = canonical_sha256(basis)
        computed_family_index[family_id] = digest
        record(
            "family_identity_hash",
            family.get("family_identity_sha256") == digest,
            f"family identity hash mismatch for {family_id}",
        )
        source = source_family_by_id.get(family_id, {})
        record(
            "family_historical_seed_exact",
            all(family.get(field) == source.get(field) for field in family_identity_fields)
            and family.get("source_disposition") == source.get("disposition"),
            f"family seed differs from P1 inventory for {family_id}",
        )

    computed_candidate_index: dict[str, str] = {}
    for candidate_id, candidate in candidate_by_id.items():
        basis = {field: candidate.get(field) for field in candidate_identity_fields}
        digest = canonical_sha256(basis)
        computed_candidate_index[candidate_id] = digest
        record(
            "candidate_identity_hash",
            candidate.get("candidate_identity_sha256") == digest,
            f"candidate identity hash mismatch for {candidate_id}",
        )
        source = source_candidate_by_id.get(candidate_id, {})
        source_projection = {
            "immutable_candidate_id": source.get("immutable_candidate_id"),
            "family_id": source.get("family_id"),
            "version": source.get("version"),
            "artifact_sha256": source.get("artifact_sha256"),
            "statement_sha256": source.get("theorem_statement_sha256"),
            "assumption_sha256": source.get("assumption_sha256"),
            "ontology_anchor_sha256": source.get("ontology_anchor_sha256"),
        }
        record(
            "candidate_historical_seed_exact",
            basis == source_projection
            and candidate.get("artifact_path") == source.get("artifact_path")
            and candidate.get("source_disposition") == source.get("final_disposition"),
            f"candidate seed differs from P1 inventory for {candidate_id}",
        )
        record(
            "candidate_artifact_hash",
            (REPO_ROOT / str(candidate.get("artifact_path", ""))).is_file()
            and file_sha256(str(candidate.get("artifact_path", "")))
            == candidate.get("artifact_sha256"),
            f"candidate artifact hash mismatch for {candidate_id}",
        )
        family_id = str(candidate.get("family_id", ""))
        record(
            "candidate_family_membership",
            family_id in family_by_id
            and candidate_id in family_by_id[family_id].get("member_candidate_ids", []),
            f"candidate {candidate_id} is not a member of {family_id}",
        )
        record(
            "candidate_construction_ordinal",
            candidate.get("construction_ordinal")
            == source_graph.get("node_order", {}).get(candidate_id),
            f"construction ordinal mismatch for {candidate_id}",
        )

    record(
        "family_membership_partition",
        sorted(
            member
            for family in families
            for member in family.get("member_candidate_ids", [])
        )
        == sorted(candidate_ids),
        "family membership must cover every candidate exactly once",
    )
    record(
        "registry_family_identity_index",
        registry.get("family_identity_index") == computed_family_index,
        "registry family identity index mismatch",
    )
    record(
        "registry_candidate_identity_index",
        registry.get("candidate_identity_index") == computed_candidate_index,
        "registry candidate identity index mismatch",
    )

    expected_collection_hashes = {
        "families_sha256": canonical_sha256(families),
        "candidates_sha256": canonical_sha256(candidates),
        "lineage_edges_sha256": canonical_sha256(edges),
        "stage_records_sha256": canonical_sha256(stages),
        "family_events_sha256": canonical_sha256(family_events),
        "explicit_absences_sha256": canonical_sha256(explicit_absences),
    }
    record(
        "registry_collection_hashes",
        registry.get("collection_hashes") == expected_collection_hashes,
        "registry collection hashes do not match seed collections",
    )
    record("registry_edge_index", registry.get("lineage_edge_ids") == edge_ids, "registry edge index mismatch")
    record("registry_stage_index", registry.get("stage_ids") == stage_ids, "registry stage index mismatch")
    record("registry_family_event_index", registry.get("family_event_ids") == family_event_ids, "registry family-event index mismatch")
    record("registry_absence_index", registry.get("explicit_absence_ids") == absence_ids, "registry explicit-absence index mismatch")

    source_edges = {
        str(item["edge_id"]): item for item in source_graph.get("candidate_edges", [])
    }
    edge_projection_fields = (
        "edge_id",
        "from_candidate_id",
        "to_candidate_id",
        "edge_type",
        "change_class",
        "supersedes",
        "evidence_task_id",
    )
    for edge in edges:
        edge_id = str(edge.get("edge_id", ""))
        source = source_edges.get(edge_id, {})
        record(
            "lineage_edge_historical_seed_exact",
            all(edge.get(field) == source.get(field) for field in edge_projection_fields),
            f"edge seed differs from P1 graph for {edge_id}",
        )
        source_id = str(edge.get("from_candidate_id", ""))
        target_id = str(edge.get("to_candidate_id", ""))
        record(
            "lineage_edge_endpoints",
            source_id in candidate_by_id and target_id in candidate_by_id and source_id != target_id,
            f"dangling or self edge {edge_id}",
        )
        if source_id in candidate_by_id and target_id in candidate_by_id:
            record(
                "lineage_edge_identity_binding",
                edge.get("from_candidate_identity_sha256")
                == candidate_by_id[source_id].get("candidate_identity_sha256")
                and edge.get("to_candidate_identity_sha256")
                == candidate_by_id[target_id].get("candidate_identity_sha256"),
                f"endpoint identity hash mismatch for {edge_id}",
            )
            same_family = candidate_by_id[source_id].get("family_id") == candidate_by_id[target_id].get("family_id")
            if edge.get("supersedes") is True:
                record("semantic_supersession_same_family", same_family, f"cross-family semantic supersession in {edge_id}")
            if not same_family:
                record(
                    "cross_family_non_supersession",
                    edge.get("supersedes") is False
                    and edge.get("edge_type")
                    == "distinct_family_route_successor_after_local_freeze",
                    f"cross-family edge {edge_id} must be route succession with supersedes false",
                )
            record(
                "strict_construction_ordinal",
                int(candidate_by_id[source_id].get("construction_ordinal", -1))
                < int(candidate_by_id[target_id].get("construction_ordinal", -1)),
                f"edge {edge_id} does not strictly increase construction ordinal",
            )
    record("lineage_graph_acyclic", acyclic(set(candidate_ids), edges), "lineage graph contains a directed cycle")

    source_stages = {
        str(item["stage_id"]): item for item in source_graph.get("stage_records", [])
    }
    allowed_stage_kinds = set(contract.get("candidate_stage_kinds", []))
    transitions = contract.get("transition_rules", {})
    stages_by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for stage in stages:
        stage_id = str(stage.get("stage_id", ""))
        candidate_id = str(stage.get("candidate_id", ""))
        source = source_stages.get(stage_id, {})
        record(
            "stage_historical_seed_exact",
            stage.get("candidate_id") == source.get("candidate_id")
            and stage.get("source_stage_type") == source.get("stage_type")
            and stage.get("task_id") == source.get("task_id")
            and stage.get("artifact_path") == source.get("artifact_path")
            and stage.get("artifact_sha256") == source.get("artifact_sha256")
            and stage.get("disposition") == source.get("disposition"),
            f"stage seed differs from P1 graph for {stage_id}",
        )
        record("stage_kind_allowed", stage.get("stage_kind") in allowed_stage_kinds, f"unknown stage kind in {stage_id}")
        record("stage_candidate_exists", candidate_id in candidate_by_id, f"unknown candidate in {stage_id}")
        if candidate_id in candidate_by_id:
            candidate = candidate_by_id[candidate_id]
            record(
                "stage_candidate_identity_binding",
                stage.get("candidate_identity_sha256") == candidate.get("candidate_identity_sha256")
                and stage.get("family_id") == candidate.get("family_id"),
                f"candidate or family identity binding mismatch in {stage_id}",
            )
        artifact_path = str(stage.get("artifact_path", ""))
        record(
            "stage_artifact_hash",
            (REPO_ROOT / artifact_path).is_file()
            and file_sha256(artifact_path) == stage.get("artifact_sha256"),
            f"artifact hash mismatch for {stage_id}",
        )
        stages_by_candidate[candidate_id].append(stage)

    for candidate_id, candidate_stages in stages_by_candidate.items():
        ordered = sorted(candidate_stages, key=lambda item: int(item.get("sequence", -1)))
        sequences = [int(item.get("sequence", -1)) for item in ordered]
        record(
            "stage_sequence_strict",
            sequences == list(range(1, len(sequences) + 1)),
            f"stage sequences are not contiguous for {candidate_id}",
        )
        if ordered:
            record(
                "initial_stage_kind",
                ordered[0].get("stage_kind") in {"construction", "repair"},
                f"initial stage for {candidate_id} must be construction or repair",
            )
        for previous, current in zip(ordered, ordered[1:]):
            allowed_next = transitions.get(previous.get("stage_kind"), [])
            record(
                "stage_transition_allowed",
                current.get("stage_kind") in allowed_next,
                f"invalid {previous.get('stage_kind')} -> {current.get('stage_kind')} transition for {candidate_id}",
            )

    family_event_kinds = set(contract.get("family_event_kinds", []))
    for event in family_events:
        event_id = str(event.get("event_id", ""))
        family_id = str(event.get("family_id", ""))
        record("family_event_kind_allowed", event.get("event_kind") in family_event_kinds, f"unknown event kind in {event_id}")
        record("family_event_family_exists", family_id in family_by_id, f"unknown family in {event_id}")
        terminal_ids = event.get("terminal_candidate_ids", [])
        record(
            "family_event_terminal_membership",
            family_id in family_by_id
            and all(item in family_by_id[family_id].get("member_candidate_ids", []) for item in terminal_ids),
            f"terminal candidate is not a member of {family_id}",
        )
        artifact_path = str(event.get("artifact_path", ""))
        record(
            "family_event_artifact_hash",
            (REPO_ROOT / artifact_path).is_file()
            and file_sha256(artifact_path) == event.get("artifact_sha256"),
            f"artifact hash mismatch for {event_id}",
        )
    record(
        "five_family_freeze_seed",
        len(family_events) == len(families)
        and {event.get("family_id") for event in family_events} == set(family_ids)
        and all(event.get("event_kind") == "freeze" for event in family_events),
        "historical seed must include one P1-T03 freeze event per family",
    )

    record(
        "known_missing_history_explicit",
        isinstance(seed.get("known_missing_history"), list),
        "known_missing_history must be an array",
    )
    for absence in explicit_absences:
        sources = absence.get("source_basis", [])
        record(
            "explicit_absence_complete",
            bool(absence.get("candidate_id") or absence.get("family_id"))
            and bool(absence.get("expected_stage_or_edge"))
            and bool(absence.get("reason"))
            and isinstance(sources, list)
            and bool(sources)
            and absence.get("counted_as_observed") is False,
            f"incomplete or inferred absence {absence.get('absence_id')}",
        )
        record(
            "explicit_absence_sources",
            all((REPO_ROOT / str(path)).is_file() for path in sources),
            f"missing source basis for {absence.get('absence_id')}",
        )

    observed_event_kinds = [stage.get("stage_kind") for stage in stages] + [
        event.get("event_kind") for event in family_events
    ]
    authority_flags = seed.get("authority_flags", {})
    protected_false = (
        authority_flags.get("historical_records_mutated") is False
        and authority_flags.get("missing_history_inferred") is False
        and authority_flags.get("candidate_adoption_event_count") == 0
        and authority_flags.get("candidate_rejection_event_count") == 0
        and authority_flags.get("ontology_modified") is False
        and authority_flags.get("scientific_claims_changed") is False
        and authority_flags.get("distance_to_gr_delta_changed") is False
        and authority_flags.get("physics_promotion_authorized") is False
        and authority_flags.get("proof_authority") is False
        and authority_flags.get("publication_authority") is False
        and "adoption" not in observed_event_kinds
        and "rejection" not in observed_event_kinds
    )
    record("protected_authority_unchanged", protected_false, "seed asserted protected or scientific authority")
    registry_boundary = registry.get("authority_boundary", {})
    record(
        "registry_authority_boundary",
        all(
            registry_boundary.get(key) is False
            for key in (
                "historical_records_mutated",
                "missing_history_inferred",
                "scientific_claims_changed",
                "distance_to_gr_delta_changed",
                "candidate_adoption_authorized",
                "candidate_rejection_authorized",
                "ontology_edit_authorized",
                "physics_promotion_authorized",
                "proof_authority",
                "publication_authority",
            )
        ),
        "registry authority boundary must keep every protected flag false",
    )

    counts = {
        "families": len(families),
        "candidates": len(candidates),
        "lineage_edges": len(edges),
        "candidate_stages": len(stages),
        "family_events": len(family_events),
        "explicit_absences": len(explicit_absences),
        "adoption_events": observed_event_kinds.count("adoption"),
        "rejection_events": observed_event_kinds.count("rejection"),
        "semantic_supersession_edges": sum(1 for edge in edges if edge.get("supersedes") is True),
        "cross_family_route_successor_edges": sum(
            1
            for edge in edges
            if edge.get("edge_type") == "distinct_family_route_successor_after_local_freeze"
        ),
    }
    record("registry_record_counts", registry.get("record_counts") == counts, "registry record counts mismatch")

    validation = {
        "schema_id": "v21_candidate_lineage_validation_v1",
        "task_id": "RT-20260721-005",
        "plan_task_id": "P10-T03",
        "as_of": SNAPSHOT_AS_OF,
        "validation_status": "PASS" if not errors else "FAIL",
        "validator_ids": sorted(checks),
        "check_count": len(checks),
        "passed_check_count": sum(1 for value in checks.values() if value),
        "failed_check_count": sum(1 for value in checks.values() if not value),
        "checks": dict(sorted(checks.items())),
        "errors": errors,
        "record_counts": counts,
        "source_hashes": seed.get("source_hashes", {}),
        "identity_hash_basis": {
            "candidate_fields": candidate_identity_fields,
            "family_fields": family_identity_fields,
            "canonical_json": contract.get("canonical_json", {}),
        },
        "authority_boundary": registry_boundary,
    }
    receipt = {
        "schema_id": "v21_candidate_lineage_compact_receipt_v1",
        "task_id": "RT-20260721-005",
        "plan_task_id": "P10-T03",
        "as_of": SNAPSHOT_AS_OF,
        "result_status": validation["validation_status"],
        "schema_path": str(SCHEMA_PATH),
        "schema_sha256": file_sha256(SCHEMA_PATH),
        "historical_seed_path": str(SEED_PATH),
        "historical_seed_sha256": file_sha256(SEED_PATH),
        "registry_path": str(REGISTRY_PATH),
        "registry_sha256": file_sha256(REGISTRY_PATH),
        "source_hashes": seed.get("source_hashes", {}),
        "finding_counts": counts,
        "validator_ids": sorted(checks),
        "failed_check_count": validation["failed_check_count"],
        "claim_boundary_summary": "Immutable project-control identities and lineage only; no history rewrite missing-lineage inference adoption rejection ontology edit scientific-ledger delta physics promotion proof authority publication or P4-T05 execution.",
        "authority_boundary": registry_boundary,
    }
    return validation, receipt


def rendered(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Write validation and compact receipt artifacts.")
    mode.add_argument("--check", action="store_true", help="Check committed artifacts against a live validation.")
    parser.add_argument("--json", action="store_true", help="Emit a compact JSON summary.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    validation, receipt = validate()
    mismatches: list[str] = []
    if args.write:
        (REPO_ROOT / VALIDATION_PATH).write_text(rendered(validation), encoding="utf-8")
        (REPO_ROOT / RECEIPT_PATH).write_text(rendered(receipt), encoding="utf-8")
    else:
        for path, expected in ((VALIDATION_PATH, rendered(validation)), (RECEIPT_PATH, rendered(receipt))):
            absolute = REPO_ROOT / path
            if not absolute.is_file() or absolute.read_text(encoding="utf-8") != expected:
                mismatches.append(str(path))

    summary = {
        "validation_status": validation["validation_status"],
        "check_count": validation["check_count"],
        "failed_check_count": validation["failed_check_count"],
        "artifact_mismatches": mismatches,
        "record_counts": validation["record_counts"],
    }
    if args.json:
        print(json.dumps(summary, sort_keys=True))
    else:
        print(
            f"{summary['validation_status']}: {summary['check_count']} checks; "
            f"{summary['failed_check_count']} failed; {len(mismatches)} artifact mismatches"
        )
    return 0 if validation["validation_status"] == "PASS" and not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
