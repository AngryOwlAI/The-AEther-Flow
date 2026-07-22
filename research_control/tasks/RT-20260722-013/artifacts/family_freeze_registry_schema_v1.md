<!-- authority: control -->

# P12-T02 Family Freeze Registry Schema

The registry is task-local `draft/control` evidence. It copies identity hashes
from the P10-T03 historical seed and freeze dispositions from P1-T03 without
mutating either source.

```json
{
  "schema_id": "family_freeze_registry_v1",
  "status": "draft/control",
  "source_hashes": {"repo/relative/path": "sha256"},
  "freezes": [
    {
      "freeze_id": "stable freeze identity",
      "family_id": "immutable family identity",
      "family_identity_sha256": "sha256",
      "candidate_ids": ["immutable candidate identity"],
      "candidate_identity_sha256es": ["sha256"],
      "assumption_sha256es": ["sha256"],
      "disposition": "family_locally_frozen_no_adoption_no_global_no_go"
    }
  ],
  "barred_route_kinds": ["rename_or_repackage"],
  "reopening_classes": [
    "new_primitive",
    "new_theorem",
    "new_variation_class",
    "protected_decision"
  ],
  "authority_flags": {
    "historical_records_mutated": false,
    "global_no_go_inferred": false,
    "candidate_adoption_authorized": false,
    "ontology_edit_authorized": false,
    "physics_promotion_authorized": false
  }
}
```

The validator requires unique freeze and family IDs, exact lowercase SHA-256
digests, nonempty candidate and assumption sets, current source hashes, and the
fixed authority flags. A changed source or identity is drift, not an implicit
registry update.
