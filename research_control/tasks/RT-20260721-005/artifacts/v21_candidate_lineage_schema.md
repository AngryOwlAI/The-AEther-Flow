<!-- authority: control -->

# V21 Candidate Identity and Lineage Schema

## Purpose

This task-local project-control contract makes candidate lifecycle references exact. It does not decide whether a candidate is physically true, adopt or reject a candidate, modify ontology, change either scientific ledger, authorize promotion, or establish a derivation.

The historical seed is additive: it copies exact identifiers and hashes from tracked P1 evidence without editing or reinterpreting those sources. When history is incomplete, a registry must record an explicit absence; it must not synthesize a stage or edge.

## Machine contract

```json
{
  "schema_id": "v21_candidate_identity_lineage_v1",
  "schema_status": "draft/control",
  "canonical_json": {
    "encoding": "UTF-8",
    "key_order": "lexicographic",
    "separators": [",", ":"],
    "trailing_newline_in_hash_basis": false,
    "hash_algorithm": "sha256"
  },
  "family_identity_fields": [
    "family_id",
    "family_label",
    "member_candidate_ids"
  ],
  "candidate_identity_fields": [
    "immutable_candidate_id",
    "family_id",
    "version",
    "artifact_sha256",
    "statement_sha256",
    "assumption_sha256",
    "ontology_anchor_sha256"
  ],
  "immutable_rules": {
    "candidate_id_reuse_with_changed_identity_hash": "forbidden",
    "family_id_reuse_with_changed_family_hash": "forbidden",
    "changed_identity_content_requires_new_candidate_id": true,
    "display_name_is_identity": false,
    "similar_name_is_identity": false,
    "historical_source_mutation": "forbidden",
    "missing_history_inference": "forbidden"
  },
  "candidate_stage_kinds": [
    "construction",
    "audit",
    "stress",
    "repair",
    "freeze",
    "adoption",
    "rejection",
    "supersession"
  ],
  "family_event_kinds": [
    "freeze",
    "adoption",
    "rejection",
    "supersession"
  ],
  "lineage_edge_types": [
    "repair_supersedes",
    "distinct_family_route_successor_after_local_freeze"
  ],
  "transition_rules": {
    "construction": ["audit", "stress", "freeze", "rejection", "supersession"],
    "audit": ["stress", "repair", "freeze", "rejection", "supersession"],
    "stress": ["repair", "freeze", "adoption", "rejection", "supersession"],
    "repair": ["audit", "stress", "freeze", "rejection", "supersession"],
    "freeze": ["repair", "adoption", "rejection", "supersession"],
    "adoption": [],
    "rejection": [],
    "supersession": []
  },
  "protected_events": {
    "adoption": "human-gated",
    "rejection": "human-gated",
    "ontology_modification": "human-gated",
    "physics_promotion": "human-gated"
  },
  "edge_rules": {
    "acyclic": true,
    "self_edges": "forbidden",
    "dangling_endpoints": "forbidden",
    "semantic_supersession_requires_same_family": true,
    "cross_family_route_successor_supersedes": false,
    "endpoint_identity_hashes_required": true
  },
  "stage_rules": {
    "candidate_identity_hash_required": true,
    "family_id_required": true,
    "artifact_path_required": true,
    "artifact_sha256_required": true,
    "artifact_hash_must_match_tracked_file": true,
    "task_id_required": true,
    "source_stage_type_preserved": true,
    "per_candidate_sequence_strictly_increasing": true
  },
  "missing_history_rules": {
    "known_missing_history_array_required": true,
    "explicit_absence_array_required": true,
    "absence_requires_candidate_or_family_id": true,
    "absence_requires_expected_stage_or_edge": true,
    "absence_requires_source_basis_and_reason": true,
    "absence_may_not_be_counted_as_observed": true
  },
  "authority_boundary": {
    "record_kind": "project_control",
    "scientific_claims_changed": false,
    "distance_to_gr_delta_changed": false,
    "candidate_adoption_authorized": false,
    "candidate_rejection_authorized": false,
    "ontology_edit_authorized": false,
    "physics_promotion_authorized": false,
    "proof_authority": false,
    "publication_authority": false
  }
}
```

## Identity basis

`candidate_identity_sha256` is the SHA-256 digest of canonical JSON containing exactly the seven `candidate_identity_fields`. Paths, display labels, prose findings, stage dispositions, and current status are not identity fields. A corrected statement, assumption set, ontology anchor, artifact content, family assignment, or version therefore requires a new candidate ID.

`family_identity_sha256` is the corresponding digest over the three `family_identity_fields`. Adding a member changes the family identity digest and must be an explicit registry revision; it never silently changes an existing snapshot.

## Lifecycle meaning

Stages are observations tied to exact artifacts. A repair that changes identity content is a new candidate node connected by a `repair_supersedes` edge. A route to a distinct family is not semantic supersession and must use `distinct_family_route_successor_after_local_freeze` with `supersedes: false`.

The enums include adoption and rejection so future records can represent them, but both remain human-gated. Their presence in the schema does not authorize or imply either result. This P10-T03 seed contains zero adoption events and zero rejection events.

## Historical-seed rule

The seed may normalize legacy stage labels while retaining each original value in `source_stage_type`. It must preserve exact candidate IDs, family IDs, source paths, source hashes, dispositions, edge types, and supersession booleans. A stage absent from the source is never backfilled. An explicit absence explains that the stage was not observed and remains excluded from observed-stage metrics.

## Validation rule

The task-local validator must fail closed on source drift, schema or seed hash drift, identity collision, family membership mismatch, invalid stage transition, artifact hash mismatch, dangling or cyclic edges, cross-family semantic supersession, missing endpoint identity hashes, inferred history, or protected authority asserted by the seed.
