<!-- authority: control -->

# V21 Scientific Status Schema

## 1. Status and boundary

```yaml
schema_id: "v21_scientific_status_schema_v1"
authority: "control"
status: "active"
created_by_task_id: "RT-20260721-003"
created_by_job_id: "AJ-RT-20260721-003-001"
plan_task_id: "P10-T01"
physics_promotion_authorized: false
proof_authority: false
```

This schema replaces ambiguous one-word future status fields with orthogonal,
machine-readable dimensions. It records what kind of evidence exists without
collapsing mathematical, physical, empirical, authority, or control status
into one ordinal label.

The schema is a project-control contract. It does not change any current
scientific status and does not establish object existence, uniqueness,
naturality, covariance, robustness, dynamics, operational meaning, empirical
support, ontology adoption, benchmark promotion, or completed derivation.

## 2. Normative machine contract

The JSON object between the markers is the machine-readable version-1
contract. The task-local P10-T01 validator parses it directly.

<!-- BEGIN V21_SCIENTIFIC_STATUS_SCHEMA_JSON -->
```json
{
  "schema_id": "v21_scientific_status_schema_v1",
  "schema_version": 1,
  "record_type": "multidimensional_scientific_status",
  "required_paths": [
    "schema_id",
    "record_id",
    "subject_id",
    "subject_scope",
    "candidate_ids",
    "theorem_ids",
    "dimensions.existence",
    "dimensions.uniqueness",
    "dimensions.naturality",
    "dimensions.covariance",
    "dimensions.robustness",
    "dimensions.dynamics",
    "dimensions.operational_meaning",
    "dimensions.empirical_status",
    "dimensions.mathematical_status",
    "dimensions.authority",
    "evidence_by_dimension",
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
    "subject_scope": [
      "source",
      "source_extension",
      "target_benchmark",
      "control"
    ],
    "existence": [
      "not_assessed",
      "absent",
      "candidate",
      "constructed",
      "established",
      "refuted"
    ],
    "uniqueness": [
      "not_assessed",
      "multiple",
      "conditional_unique",
      "unique",
      "refuted"
    ],
    "naturality": [
      "not_assessed",
      "assumed",
      "conditional",
      "derived",
      "refuted"
    ],
    "covariance": [
      "not_assessed",
      "coordinate_scoped",
      "covariant",
      "violated",
      "refuted"
    ],
    "robustness": [
      "not_assessed",
      "fragile",
      "conditional",
      "robust",
      "refuted"
    ],
    "dynamics": [
      "not_assessed",
      "absent",
      "proposed",
      "specified",
      "derived",
      "validated",
      "refuted"
    ],
    "operational_meaning": [
      "not_assessed",
      "absent",
      "proposed",
      "specified",
      "derived",
      "validated",
      "refuted"
    ],
    "empirical_status": [
      "not_assessed",
      "untested",
      "compatible",
      "supported",
      "disfavored",
      "refuted"
    ],
    "mathematical_status": [
      "not_assessed",
      "heuristic",
      "computed",
      "proved",
      "refuted"
    ],
    "authority": [
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
    "authority_kind": [
      "none",
      "registered_control",
      "registered_canonical_science",
      "protected_human_gate",
      "external_primary"
    ]
  },
  "legacy_mapping": {
    "accepted": {
      "control_disposition": "historical_accepted",
      "authority": "context_required"
    },
    "draft": {
      "control_disposition": "draft_control",
      "authority": "control_only"
    },
    "evidence": {
      "control_disposition": "evidence_recorded",
      "authority": "context_required"
    },
    "proposal": {
      "control_disposition": "proposal_only",
      "authority": "proposal_only"
    },
    "adopted": {
      "control_disposition": "historical_adopted",
      "authority": "context_required"
    },
    "frozen": {
      "control_disposition": "frozen_negative",
      "authority": "frozen_negative"
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
  "evidence_required_statuses": {
    "existence": ["constructed", "established", "refuted"],
    "uniqueness": ["conditional_unique", "unique", "refuted"],
    "naturality": ["conditional", "derived", "refuted"],
    "covariance": ["covariant", "violated", "refuted"],
    "robustness": ["fragile", "conditional", "robust", "refuted"],
    "dynamics": ["specified", "derived", "validated", "refuted"],
    "operational_meaning": ["specified", "derived", "validated", "refuted"],
    "empirical_status": ["compatible", "supported", "disfavored", "refuted"],
    "mathematical_status": ["computed", "proved", "refuted"],
    "authority": [
      "scoped_evidence",
      "source_extension_data",
      "canonical_ontology_candidate",
      "adopted",
      "rejected",
      "human_gated",
      "frozen_negative"
    ]
  },
  "conditional_rule_ids": [
    "scientific_status_required_paths",
    "scientific_status_known_enums",
    "scientific_status_dimension_evidence_required",
    "scientific_status_existence_consistency",
    "scientific_status_unique_requires_existence",
    "scientific_status_proof_reference_required",
    "scientific_status_empirical_evidence_required",
    "scientific_status_refutation_scope_required",
    "scientific_status_human_gate_required",
    "scientific_status_protected_candidate_required",
    "scientific_status_adoption_authority_required",
    "scientific_status_legacy_mapping_exact",
    "scientific_status_legacy_raw_preserved",
    "scientific_status_authorization_explicit",
    "scientific_status_no_implicit_physics_promotion"
  ]
}
```
<!-- END V21_SCIENTIFIC_STATUS_SCHEMA_JSON -->

Unknown enum values, unrecognized dimensions, missing required paths, and
contradictory strong statuses fail closed for newly created version-1 records.
Historical records are not rewritten or retroactively failed.

## 3. Orthogonal dimensions

| Dimension | Question answered | Important boundary |
| --- | --- | --- |
| `existence` | Does the named mathematical or physical object exist in the stated scope? | `candidate` or `constructed` is not `established`. |
| `uniqueness` | Is the object unique, conditionally unique, or one of several? | Uniqueness does not imply naturality or physical selection. |
| `naturality` | Is a construction assumed, conditional, or derived without arbitrary choices? | A natural construction does not imply empirical meaning. |
| `covariance` | Is the result coordinate-scoped, covariant, or violated? | Covariance does not establish dynamics or physical adoption. |
| `robustness` | Does the result persist under the stated perturbations or choices? | A finite or local robustness result is not a continuum theorem. |
| `dynamics` | Are dynamics absent, proposed, specified, derived, validated, or refuted? | Specified equations are not necessarily derived from the source ontology. |
| `operational_meaning` | Are detector/measurement semantics absent, proposed, specified, derived, validated, or refuted? | Formal variables are not automatically observables. |
| `empirical_status` | Is the object untested, compatible, supported, disfavored, or refuted by empirical evidence? | Exact-GR benchmark agreement is not evidence for the substrate interpretation by itself. |
| `mathematical_status` | Is the support heuristic, computed, proved, or refuted? | A proof has the exact assumptions and scope recorded by its theorem reference. |
| `authority` | Is the record control-only, scoped evidence, proposal-only, adopted, rejected, or human-gated? | Authority is never inferred from the other nine dimensions. |

These dimensions are not an ordinal ladder. Renderers and analytics may compare
only values whose semantics explicitly permit comparison. For example,
`covariant` and `empirically supported` answer different questions and cannot
be combined into a scalar “confidence.”

## 4. Evidence and consistency rules

`evidence_by_dimension` is a map from every dimension name to a list of exact
artifact, theorem, computation, primary-source, control, or protected-authority
references. Each strong value listed under `evidence_required_statuses` in the
machine contract has at least one reference for its own dimension.

Additional fail-closed rules are:

1. `existence: absent` or `existence: refuted` cannot coexist with
   `uniqueness: unique`, `naturality: derived`, `dynamics: derived|validated`,
   or `operational_meaning: derived|validated`.
2. `uniqueness: unique` requires `existence: established` and dimension-local
   evidence. `conditional_unique` does not upgrade existence.
3. `mathematical_status: proved` requires at least one `theorem_id` and
   mathematical-status evidence. It grants no adoption or promotion authority.
4. `empirical_status: supported|disfavored|refuted` requires exact empirical
   evidence. `compatible` means no conflict in the stated test scope; it is not
   general support.
5. Any `refuted` dimension, `authority: rejected`, or
   `authority: frozen_negative` requires exact refutation scope and evidence.
   A global no-go flag requires an explicitly cited global no-go theorem.
6. `authority: scoped_evidence` records exact evidence scope.
   `source_extension_data` remains source-extension data only.
7. `canonical_ontology_candidate` requires protected human-gate authority;
   `adopted` requires exact domain, scope, and authority. Source-ontology or
   source-extension adoption requires a protected human gate. Target-benchmark
   adoption may cite registered canonical science but remains target-side.
8. `human_gated` names the unresolved gate. A gate requirement is not a gate
   verdict.
9. All authorization booleans are explicit. A true value requires exact
   authority scope, source path, and blocked downstream conclusions. No
   combination of dimension values turns any authorization on automatically.

## 5. Minimal future record shape

```yaml
schema_id: "v21_scientific_status_schema_v1"
record_id: "STATUS-..."
subject_id: "..."
subject_scope: "source_extension"
candidate_ids: ["CAND-..."]
theorem_ids: []
dimensions:
  existence: "constructed"
  uniqueness: "not_assessed"
  naturality: "not_assessed"
  covariance: "coordinate_scoped"
  robustness: "not_assessed"
  dynamics: "proposed"
  operational_meaning: "absent"
  empirical_status: "untested"
  mathematical_status: "computed"
  authority: "source_extension_data"
evidence_by_dimension:
  existence: ["artifact-ref"]
  uniqueness: []
  naturality: []
  covariance: []
  robustness: []
  dynamics: []
  operational_meaning: []
  empirical_status: []
  mathematical_status: ["computation-ref"]
  authority: ["control-authority-ref"]
refutation:
  scope: ""
  evidence_refs: []
  global_no_go_established: false
authority:
  authority_kind: "registered_control"
  authority_refs: ["control-authority-ref"]
  authority_scope: "source-extension data only"
  gate_id: ""
legacy_compatibility:
  raw_label: null
  source_record_ref: ""
  mapped_fields: {}
  mapping_authority: "compatibility_only"
  historical_record_rewritten: false
authorization_layers: {"...": false}
forbidden_conclusions:
  - "No physical metric, ontology adoption, or benchmark promotion follows."
```

The abbreviated authorization map must be expanded to every boolean listed in
the normative contract in an actual record.

## 6. Historical compatibility

The same six raw labels used by the assumption schema are mapped additively.
The raw value and source record reference remain present, the declared mapping
is exact, `mapping_authority` is `compatibility_only`, and
`historical_record_rewritten` remains false.

| Raw label | Normalized compatibility view | What remains unresolved |
| --- | --- | --- |
| `accepted` | `historical_accepted`, authority `context_required` | Exact accepted object, scope, and accepting authority. |
| `draft` | `draft_control`, authority `control_only` | Any scientific evidence or review. |
| `evidence` | `evidence_recorded`, authority `context_required` | Evidence type, scope, and permitted inference. |
| `proposal` | `proposal_only`, authority `proposal_only` | Protected candidacy or adoption. |
| `adopted` | `historical_adopted`, authority `context_required` | Authority domain and whether adoption was target-side, scoped, or protected. |
| `frozen` | `frozen_negative`, authority `frozen_negative` | Exact frozen family, reopening criteria, and global-no-go status. |

No compatibility mapping populates existence, uniqueness, naturality,
covariance, robustness, dynamics, operational meaning, empirical, or
mathematical status. Those dimensions require their own source-backed evidence.

## 7. Downstream use

Later P10 and P11 tasks may add adapters, append-only events, or generated views
that emit this shape. They must preserve raw historical records, cite the exact
source for every populated dimension, and keep contradictions fail closed.
This P10-T01 packet supplies the schema only; it performs no bulk migration.

## 8. Acceptance and authority statement

P10-T01 accepts this schema only as an operational control contract. Validator
PASS, fixture coverage, memory regeneration, and a checkpoint establish
implementation integrity, not scientific proof, adoption, promotion, or
publication authority.

## References

The AEther-Flow Research Project. (2026a). `research_control/design/distance_to_gr_status_layers_v1.md` [Internal project-control schema].

The AEther-Flow Research Project. (2026b). `research_control/design/accepted_status_calibration_schema_v1.md` [Internal project-control schema].

The AEther-Flow Research Project. (2026c). `research_control/design/layered_status_field_schema_v16.md` [Internal project-control schema].

The AEther-Flow Research Project. (2026d). `implementations_plans/recommendations_implementation_plan_continue_task-v21.md` [Internal implementation plan].
