<!-- authority: control -->

# V21 Orthogonal Task Taxonomy Policy

```yaml
schema_id: "v21_task_taxonomy_policy_v1"
implements_plan_task_id: "P10-T02"
source_plan: "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
effective_at: "2026-07-22T01:19:45Z"
authority_status: "project_control"
historical_migration_mode: "classify_without_mutation"
scientific_claims_changed: false
physics_promotion_authorized: false
proof_authority: false
```

## Purpose and authority

This policy replaces free-form task-type analytics with six orthogonal machine
fields while retaining the raw task record. It governs routing and operational
reporting only. It cannot establish or strengthen a scientific claim, adopt an
ontology or source law, discharge a Distance-to-GR burden, supply Gate Chair
authority, promote a benchmark, authorize publication, or prove a derivation.

The top-level `title` and `task_type` values remain readable raw provenance.
Normalized values are additive and must never overwrite either field. The
adapter may use exact v21 plan metadata, registered role authority, and
conservative legacy signals to classify old tasks, but ambiguous fields remain
`unknown`.

## Machine contract

The JSON object between the named markers is the machine-readable contract
consumed by `scripts/research_control/task_taxonomy.py`.

<!-- v21-task-taxonomy-contract:start -->
```json
{
  "schema_id": "v21_task_taxonomy_v1",
  "effective_at": "2026-07-22T01:19:45Z",
  "required_top_level_fields": [
    "title",
    "task_type",
    "task_taxonomy"
  ],
  "required_taxonomy_fields": [
    "work_kind",
    "milestone",
    "candidate_family",
    "result_kind",
    "authority",
    "scope"
  ],
  "vocabularies": {
    "work_kind": [
      "audit_or_review",
      "benchmark_or_recovery",
      "construction_or_implementation",
      "formalization_or_theorem",
      "integration_or_selection",
      "protected_gate_review",
      "publication_preparation",
      "unknown"
    ],
    "milestone": [
      "source_ontology",
      "source_equivalence_eqsrc",
      "effective_metric_g_eff",
      "matter_coupling",
      "einstein_equations",
      "benchmark_promotion",
      "not_applicable",
      "unknown"
    ],
    "result_kind": [
      "audit_verdict_or_precise_repair",
      "candidate_or_precise_obstruction",
      "completed_or_precisely_blocked",
      "implemented_and_validated_or_precisely_blocked",
      "protected_verdict_or_deferred_human_gate",
      "theorem_or_precise_obstruction",
      "not_applicable",
      "unknown"
    ],
    "authority": [
      "human_gated",
      "process_control",
      "project_control",
      "routing_control",
      "science_draft",
      "unknown"
    ],
    "scope": [
      "human_gate",
      "project_system",
      "routing",
      "scientific",
      "scientific_audit",
      "mixed",
      "unknown"
    ]
  },
  "candidate_family_contract": {
    "pattern": "^[a-z0-9][a-z0-9_]{0,95}$",
    "reserved_values": [
      "not_applicable",
      "unknown"
    ]
  },
  "confidence_values": [
    "high",
    "medium",
    "low",
    "unknown"
  ],
  "source_values": [
    "explicit",
    "plan_metadata",
    "legacy_compatibility",
    "unknown"
  ],
  "authority_boundaries": {
    "classification_is_scientific_status": false,
    "classification_can_strengthen_science": false,
    "classification_can_promote_claims": false,
    "classification_can_adopt_ontology_or_law": false,
    "classification_can_supply_human_authority": false,
    "raw_historical_records_may_be_mutated": false,
    "unknown_must_be_retained_on_ambiguity": true
  }
}
```
<!-- v21-task-taxonomy-contract:end -->

## Field meanings

| Field | Meaning | Non-meaning |
| --- | --- | --- |
| `work_kind` | Operational shape of the bounded packet. | Not a result or scientific rank. |
| `milestone` | Distance-to-GR milestone the packet is about. | Not evidence that the milestone advanced. |
| `candidate_family` | Stable family slug when an exact family is known. | Not candidate identity or adoption. |
| `result_kind` | Expected disposition vocabulary for the packet. | Not the packet's achieved result. |
| `authority` | Registered authority class of the executing role or explicit task boundary. | Not a grant of stronger authority. |
| `scope` | Operational surface affected by the packet. | Not a scientific truth classification. |

`candidate_family` uses a bounded lowercase slug. `not_applicable` is valid
only when no candidate family belongs to the task. `unknown` is required when
the record does not establish a family exactly.

## New-record rule

Every task whose `created_at` is on or after `2026-07-22T01:19:45Z` must carry
a top-level readable `title`, the raw `task_type`, and a `task_taxonomy` mapping
with `schema_id: v21_task_taxonomy_v1` plus all six fields. Explicit `unknown`
is valid and preferable to an invented value. Missing, extra, malformed, or
out-of-vocabulary normalized fields fail the task-index validation gate.

## Compatibility and migration rules

Classification priority is:

1. exact explicit `task_taxonomy` fields;
2. exact `implementation_plan.plan_task_id` metadata from the registered v21
   backlog plus registered role authority;
3. conservative compatibility parsing of legacy `task_type`, route, milestone,
   and registered role metadata;
4. `unknown`.

Plan and compatibility classifications are derived views only. The adapter
records their source and confidence, exposes unknown fields, preserves the raw
title and `task_type`, and never writes back to activated task records. A
registered `science_draft` role may classify the authority field as
`science_draft`; this does not strengthen any scientific status because the
taxonomy contains no adoption, acceptance, proof, promotion, or truth field.

## Reporting rule

Task-index and analytics reports prefer normalized fields when present. Legacy
heuristics remain compatibility fallbacks only. Reports must expose
`taxonomy_source` and `taxonomy_confidence`, keep raw fields visible, and remain
non-authoritative derivatives.

## Validation and stop conditions

The repository validator must report explicit-field compliance for new tasks,
historical parse coverage, unknown counts, low-confidence counts, raw-field
preservation, historical source mutation count, and stronger-science inference
count. A nonzero required-field error, historical mutation count, or
stronger-science inference count is blocking. Validator PASS remains
operational evidence only.
