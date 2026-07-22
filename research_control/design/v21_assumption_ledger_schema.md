<!-- authority: control -->

# V21 Assumption Ledger Schema

## 1. Status and boundary

```yaml
schema_id: "v21_assumption_ledger_schema_v1"
authority: "control"
status: "active"
created_by_task_id: "RT-20260721-003"
created_by_job_id: "AJ-RT-20260721-003-001"
plan_task_id: "P10-T01"
physics_promotion_authorized: false
proof_authority: false
```

This schema defines an additive, future-facing record for assumption identity,
structural role, provenance, disposition, authority, and downstream use. It does
not revise the P4-T01 source-assumption ledger or any other historical record.
It also does not adopt an ontology, source law, source extension, physical
metric, matter coupling, Einstein equation, benchmark, or completed
derivation.

The fields are deliberately orthogonal. In particular, `primitive` does not
mean `adopted`, `derived` does not mean `unique`, a registered source does not
mean that the source derives the recorded statement, and a validator PASS does
not confer scientific authority.

## 2. Normative machine contract

The JSON object between the markers is the machine-readable schema contract
for version 1. The task-local P10-T01 validator parses this block directly.

<!-- BEGIN V21_ASSUMPTION_SCHEMA_JSON -->
```json
{
  "schema_id": "v21_assumption_ledger_schema_v1",
  "schema_version": 1,
  "record_type": "assumption_provenance",
  "required_paths": [
    "schema_id",
    "record_id",
    "assumption_id",
    "subject_id",
    "statement",
    "assumption_kind",
    "subject_scope",
    "derivation_role",
    "disposition",
    "authority_status",
    "project_status_label",
    "provenance.provenance_kind",
    "provenance.source_refs",
    "provenance.source_hashes",
    "provenance.missing_reason",
    "provenance.constructed_from",
    "derivation.dependency_ids",
    "derivation.certificate_refs",
    "blocking.burden_ids",
    "blocking.continuation_status",
    "refutation.scope",
    "refutation.evidence_refs",
    "refutation.global_no_go_established",
    "authority.authority_kind",
    "authority.authority_refs",
    "authority.authority_scope",
    "authority.gate_id",
    "legacy_compatibility.raw_label",
    "legacy_compatibility.source_record_ref",
    "legacy_compatibility.mapped_fields",
    "legacy_compatibility.mapping_authority",
    "legacy_compatibility.historical_record_rewritten",
    "authorization_layers",
    "forbidden_conclusions"
  ],
  "enums": {
    "assumption_kind": [
      "primitive",
      "derived",
      "auxiliary",
      "benchmark"
    ],
    "subject_scope": [
      "source",
      "source_extension",
      "target_benchmark",
      "control"
    ],
    "derivation_role": [
      "source_premise",
      "derived_consequence",
      "auxiliary_device",
      "target_benchmark_only",
      "prohibited"
    ],
    "disposition": [
      "open",
      "active",
      "blocked_adoption_open_continuation",
      "adopted",
      "rejected",
      "human_gated",
      "frozen_negative"
    ],
    "authority_status": [
      "unassessed",
      "control_only",
      "context_required",
      "scoped_evidence",
      "proposal_only",
      "source_extension_data",
      "canonical_ontology_candidate",
      "adopted",
      "rejected",
      "human_gated",
      "frozen_negative"
    ],
    "provenance_kind": [
      "registered_canonical_science",
      "registered_control",
      "external_primary",
      "constructed_draft",
      "missing_source"
    ],
    "authority_kind": [
      "none",
      "registered_control",
      "registered_canonical_science",
      "protected_human_gate",
      "external_primary"
    ],
    "continuation_status": [
      "open",
      "blocked_adoption_open_continuation",
      "closed_by_scoped_refutation",
      "not_applicable"
    ]
  },
  "project_status_labels": {
    "control_only": "draft/control",
    "proposal_only": "proposal-only",
    "source_extension_data": "source-extension data",
    "canonical_ontology_candidate": "canonical-ontology candidate",
    "adopted": "adopted",
    "rejected": "rejected",
    "human_gated": "human-gated"
  },
  "legacy_mapping": {
    "accepted": {
      "control_disposition": "historical_accepted",
      "authority_status": "context_required"
    },
    "draft": {
      "control_disposition": "draft_control",
      "authority_status": "control_only"
    },
    "evidence": {
      "control_disposition": "evidence_recorded",
      "authority_status": "context_required"
    },
    "proposal": {
      "control_disposition": "proposal_only",
      "authority_status": "proposal_only"
    },
    "adopted": {
      "control_disposition": "historical_adopted",
      "authority_status": "context_required"
    },
    "frozen": {
      "control_disposition": "frozen_negative",
      "authority_status": "frozen_negative"
    }
  },
  "authorization_boolean_fields": [
    "scoped_evidence_status_change_authorized",
    "source_object_status_change_authorized",
    "source_extension_object_status_change_authorized",
    "source_law_adoption_authorized",
    "matter_semantics_adoption_authorized",
    "detector_semantics_adoption_authorized",
    "coupling_law_adoption_authorized",
    "matter_coupling_derivation_authorized",
    "matter_coupling_adoption_authorized",
    "stress_energy_semantics_authorized",
    "matter_action_authorized",
    "einstein_equation_derivation_authorized",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
    "downstream_physics_promotion_authorized"
  ],
  "conditional_rule_ids": [
    "assumption_required_paths",
    "assumption_known_enums",
    "assumption_kind_role_alignment",
    "assumption_provenance_source_required",
    "assumption_missing_source_exclusive",
    "assumption_derived_certificate_required",
    "assumption_benchmark_target_only",
    "assumption_blocked_burden_required",
    "assumption_refutation_scope_required",
    "assumption_human_gate_required",
    "assumption_protected_candidate_required",
    "assumption_adoption_authority_required",
    "assumption_project_label_exact",
    "assumption_legacy_mapping_exact",
    "assumption_legacy_raw_preserved",
    "assumption_authorization_explicit",
    "assumption_no_implicit_physics_promotion"
  ]
}
```
<!-- END V21_ASSUMPTION_SCHEMA_JSON -->

Unknown enum values and missing required paths fail closed for newly created
version-1 records. Historical data do not fail merely because they predate the
schema; they enter only through the compatibility object in Section 6.

## 3. Field semantics

| Field | Meaning | Non-implication |
| --- | --- | --- |
| `assumption_kind` | Whether the statement is primitive, derived, auxiliary, or a target benchmark. | A primitive is not automatically adopted; a derived statement is not automatically proved. |
| `subject_scope` | Source, source extension, target benchmark, or control scope. | A target benchmark cannot serve as a source-side derivation premise. |
| `derivation_role` | The exact permissible role in later derivations. | Registration does not authorize downstream use outside this value. |
| `disposition` | Current control disposition of the record. | A local freeze or scoped rejection is not a global no-go theorem. |
| `authority_status` | Scientific/control authority layer, independent of structure and disposition. | `scoped_evidence`, `proposal_only`, and `source_extension_data` are not adoption. |
| `provenance` | Where the statement came from, with source references and hashes or an explicit missing-source reason. | Provenance establishes traceability, not truth or derivation. |
| `derivation` | Dependencies and certificate references for a derived assumption. | A certificate reference must still be evaluated under its own claim boundary. |
| `authorization_layers` | Explicit booleans from the v16 layered-status model. | No other status field supplies these permissions implicitly. |

Every non-missing provenance source has a source reference and a keyed SHA-256
value. `missing_source` instead requires a precise `missing_reason` and forbids
source references or hashes. `constructed_draft` additionally names the inputs
under `constructed_from`; it remains a project construction, not established
literature or canonical ontology.

## 4. Conditional validation rules

1. The `assumption_kind` and `derivation_role` pairs are exact:
   `primitive/source_premise`, `derived/derived_consequence`,
   `auxiliary/auxiliary_device`, and `benchmark/target_benchmark_only`.
2. A derived record has at least one dependency and one certificate reference.
3. A benchmark record has `subject_scope: target_benchmark` and cannot be used
   as a source premise.
4. `blocked_adoption_open_continuation` has a nonempty burden list and uses the
   same `blocking.continuation_status`; it states that current adoption is
   blocked while same-milestone continuation remains open.
5. `rejected` or `frozen_negative` has a precise refutation scope and evidence.
   `global_no_go_established: true` is allowed only when an explicitly cited
   no-go theorem actually has that scope.
6. `human_gated` names the unresolved protected gate. A
   `canonical_ontology_candidate` requires a protected human-gate reference;
   it is not created by validator output.
7. `adopted` requires exact authority scope and references. Source-ontology or
   source-extension adoption requires protected human-gate authority. A
   target-benchmark adoption may instead cite registered canonical science,
   but remains target-side only.
8. The exact project display labels are `draft/control`, `proposal-only`,
   `source-extension data`, `canonical-ontology candidate`, `adopted`,
   `rejected`, and `human-gated` for their corresponding normalized values.
9. All authorization booleans are present. A true value requires a nonempty
   exact authority scope, authority source path, and blocked-downstream list.
   Status, provenance, proof, validation, completion, or checkpoint state never
   turns an authorization boolean on.

## 5. Minimal future record shape

```yaml
schema_id: "v21_assumption_ledger_schema_v1"
record_id: "ASSUMPTION-..."
assumption_id: "..."
subject_id: "..."
statement: "..."
assumption_kind: "primitive"
subject_scope: "source"
derivation_role: "source_premise"
disposition: "active"
authority_status: "proposal_only"
project_status_label: "proposal-only"
provenance:
  provenance_kind: "registered_canonical_science"
  source_refs: ["TEX-..."]
  source_hashes: {"TEX-...": "<sha256>"}
  missing_reason: ""
  constructed_from: []
derivation:
  dependency_ids: []
  certificate_refs: []
blocking:
  burden_ids: []
  continuation_status: "not_applicable"
refutation:
  scope: ""
  evidence_refs: []
  global_no_go_established: false
authority:
  authority_kind: "registered_control"
  authority_refs: ["research_control/...yaml"]
  authority_scope: "proposal-only source assumption"
  gate_id: ""
legacy_compatibility:
  raw_label: null
  source_record_ref: ""
  mapped_fields: {}
  mapping_authority: "compatibility_only"
  historical_record_rewritten: false
authorization_layers: {"...": false}
forbidden_conclusions:
  - "No ontology adoption or downstream physics promotion follows."
```

The abbreviated authorization map in this illustration must be expanded to all
fields listed in the machine contract in an actual record.

## 6. Historical compatibility

Migration is additive. A compatibility adapter copies the exact raw label into
`legacy_compatibility.raw_label`, records the historical source path, and adds
only the mapping declared in the normative block. The adapter sets
`mapping_authority: compatibility_only` and
`historical_record_rewritten: false`.

The six legacy labels have these bounded readings:

| Raw label | Additive mapping | Forbidden overread |
| --- | --- | --- |
| `accepted` | Historical control acceptance; context required. | Not adoption, proof, or promotion without exact local authority. |
| `draft` | `draft_control` and `control_only`. | Not scientific evidence or a canonical source. |
| `evidence` | Evidence was recorded; context required. | Not general empirical support or adoption. |
| `proposal` | `proposal_only`. | Not a canonical-ontology candidate or adoption. |
| `adopted` | Historical adoption label; context required. | Its domain and authority must be recovered before normalized reuse. |
| `frozen` | `frozen_negative`. | A local family/route freeze is not global theory rejection. |

The compatibility layer does not update, relabel, or reinterpret the source
record. Later migration work may populate additive normalized views only after
it records the exact claim boundary and authority context.

## 7. Acceptance and authority statement

P10-T01 accepts this schema only as a project-control data contract. Positive
and negative fixtures test its operational rules. They establish neither the
truth of any assumption nor authority to promote any scientific status.

## References

The AEther-Flow Research Project. (2026a). `research_control/tasks/RT-20260720-030/artifacts/comprehensive_source_assumption_ledger_v1.tex` [Registered internal research artifact].

The AEther-Flow Research Project. (2026b). `research_control/design/layered_status_field_schema_v16.md` [Internal project-control schema].

The AEther-Flow Research Project. (2026c). `implementations_plans/recommendations_implementation_plan_continue_task-v21.md` [Internal implementation plan].
