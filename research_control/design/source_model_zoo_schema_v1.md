<!-- authority: control -->

# Source Model Zoo Schema v1

## Status

This schema implements v16 P10-T01. It defines the required record shape for
finite/local source models used by later model-zoo construction, support-only
validation, target-import attack fixtures, red-team packets, and compact
frontier summaries.

The schema is a draft/control design surface. It is not a source law, not an
unrestricted `RR_E` theorem, not detector semantics, not matter semantics, not
stress-energy semantics, not a matter action, not matter coupling, not
Einstein equations, not benchmark promotion, and not a completed derivation.

## Scope

A source model is one finite or locally finite source-side fixture. It may
assemble source objects, labels, guards, response tokens, certificate-instance
links, and expected relation outcomes for controlled tests. It must not import
target metric data, target atlas structure, target topology, detector-event
semantics, stress-energy data, matter-action data, benchmark behavior,
validator status, registry status, role identity, handoff state, approval
state, commit state, generated derivatives, or local cache state as model data.

The schema consumes the P4 certificate-instance library and the P9 trigger
integration guidance:

- `research_control/design/source_certificate_instance_library_schema_v1.md`
- `research_control/design/source_certificate_instance_library_index_v1.md`
- `research_control/tasks/RT-20260704-024/artifacts/post_selected_theorem_route_selector_v16.md`
- `research_control/tasks/RT-20260705-018/artifacts/upstream_trigger_selector_integration_v16.md`

## Model Kind Vocabulary

Every model record must use exactly one `model_kind` value:

- `trivial_identity_model`
- `transportable_two_object_model`
- `invariant_relabeling_model`
- `factorization_through_source_object_model`
- `certificate_gap_model`
- `rr_e_separated_model`
- `target_import_rejection_model`
- `detector_semantics_collapse_rejection_model`

The first four kinds support positive or neutral source-side fixtures. The
last four kinds support fail-closed, obstruction, or rejection fixtures. No
kind authorizes target import, detector semantics, matter coupling, benchmark
recovery, or proof authority.

## Required Record Fields

```yaml
model_id:
model_kind:
source_domain:
source_objects:
source_labels:
source_guards:
response_tokens:
certificate_instances:
rr_e_records:
target_import_status:
detector_semantics_status:
stress_energy_status:
matter_action_status:
benchmark_status:
expected_valid_relations:
expected_fail_closed_relations:
source_paths:
allowed_reuse:
forbidden_overreads:
```

## Field Semantics

| Field | Required type | Semantics |
| --- | --- | --- |
| `model_id` | stable string | Unique id for the model. Recommended form: `SMZ-<KIND>-<NNN>`. |
| `model_kind` | enum | One value from the model-kind vocabulary. |
| `source_domain` | record | Declared finite or locally finite source domain, including support set and locality statement. |
| `source_objects` | list of records | Source-only objects with object ids, local carriers, labels, guards, and declared roles. |
| `source_labels` | list | Source labels used inside the model. These are not target atlas labels or detector-event labels. |
| `source_guards` | list | Source-side validity guards that must pass before positive reuse is allowed. |
| `response_tokens` | list | Source response/readout tokens inside the finite/local model. These are source records, not matter measurements. |
| `certificate_instances` | list | P4 certificate instance ids or `none`, with path and intended use. |
| `rr_e_records` | list | Local relation records. A model may record declared equivalence, blocked equivalence, separation, or obstruction only inside its stated scope. |
| `target_import_status` | enum | One of `not_used`, `rejected`, or `attempted_rejected`. Positive models must use `not_used`. Rejection models may use `rejected` or `attempted_rejected`. |
| `detector_semantics_status` | enum | One of `not_used`, `rejected`, or `attempted_rejected`. Positive models must use `not_used`. |
| `stress_energy_status` | enum | One of `not_used`, `rejected`, or `attempted_rejected`. No model may use stress-energy as accepted source data. |
| `matter_action_status` | enum | One of `not_used`, `rejected`, or `attempted_rejected`. No model may use matter action as accepted source data. |
| `benchmark_status` | enum | One of `not_applicable`, `not_claimed`, or `blocked`. No model may claim benchmark recovery. |
| `expected_valid_relations` | list | Relations expected to pass under declared source guards and explicit certificates. Empty is allowed for rejection models. |
| `expected_fail_closed_relations` | list | Relations expected to fail closed, with precise defect or blocked overread. |
| `source_paths` | list | Canonical source paths used to define the model. Generated derivatives may be listed only as non-authority aids if needed. |
| `allowed_reuse` | list | Permitted support-only uses, scoped to finite/local source testing. |
| `forbidden_overreads` | list | Explicit claims the model cannot support. |

## Kind-Specific Constraints

| Model kind | Required content | Required boundary |
| --- | --- | --- |
| `trivial_identity_model` | One or more source objects with identity relation records. | Identity is local bookkeeping only; it is not a global source law or proof authority. |
| `transportable_two_object_model` | At least two source objects and a positive or blocked transport certificate reference. | Transport validity is only inside the declared finite/local domain. |
| `invariant_relabeling_model` | A source object family or relabeling orbit and an invariance certificate reference. | Relabeling is source-label invariance only, not detector or empirical invariance. |
| `factorization_through_source_object_model` | A declared middle source object and factorization certificate reference. | Factorization does not imply global `RR_E` collapse or matter coupling. |
| `certificate_gap_model` | A missing, malformed, or incompatible certificate reference or explicit absence. | The gap blocks the local relation and is not a global no-go theorem. |
| `rr_e_separated_model` | At least two objects or records kept separated by local `RR_E` discipline. | Separation is local and does not discharge or refute unrestricted `RR_E`. |
| `target_import_rejection_model` | A rejected target-metric, target-atlas, stress-energy, benchmark, or related import attempt. | The rejection records smuggling risk only; it is not a derivation obstruction for all future source extensions. |
| `detector_semantics_collapse_rejection_model` | A rejected detector-semantics or detector-sameness collapse attempt. | Detector semantics remain outside source data and cannot be used to collapse source distinctions. |

## Certificate-Instance Compatibility

A model that references P4 certificate instances must preserve the source
artifact boundary:

- `SCI-TRANSPORT-001` may support `transportable_two_object_model`.
- `SCI-INVARIANCE-001` may support `invariant_relabeling_model`.
- `SCI-FACTORIZATION-001` may support
  `factorization_through_source_object_model`.
- `SCI-NEG-MISSING-001`, `SCI-NEG-MALFORMED-001`, and
  `SCI-NEG-FACTOR-CHANGE-001` may support `certificate_gap_model`.
- `SCI-NEG-TARGET-METRIC-001`, `SCI-NEG-STRESS-ENERGY-001`, and related
  target-import negatives may support `target_import_rejection_model`.
- `SCI-NEG-DETECTOR-001` may support
  `detector_semantics_collapse_rejection_model`.
- `SCI-NEG-VALIDATOR-PASS-001` and `SCI-NEG-SCOPED-EVIDENCE-001` may support
  process-authority or scope-expansion rejection notes under
  `forbidden_overreads`.

Positive certificate references do not become source-law adoption. Negative
certificate references do not become global impossibility theorems.

## Machine-Readable Schema

```yaml
schema_id: "source_model_zoo_schema_v1"
schema_status: "draft/control"
implemented_plan_task: "P10-T01"
model_grain: "finite_or_locally_finite_source_model"
physics_promotion_authorized: false
proof_authority: false
required_fields:
  - model_id
  - model_kind
  - source_domain
  - source_objects
  - source_labels
  - source_guards
  - response_tokens
  - certificate_instances
  - rr_e_records
  - target_import_status
  - detector_semantics_status
  - stress_energy_status
  - matter_action_status
  - benchmark_status
  - expected_valid_relations
  - expected_fail_closed_relations
  - source_paths
  - allowed_reuse
  - forbidden_overreads
model_kinds:
  positive_or_neutral:
    - trivial_identity_model
    - transportable_two_object_model
    - invariant_relabeling_model
    - factorization_through_source_object_model
  fail_closed_or_rejection:
    - certificate_gap_model
    - rr_e_separated_model
    - target_import_rejection_model
    - detector_semantics_collapse_rejection_model
status_values:
  target_import_status:
    - not_used
    - rejected
    - attempted_rejected
  detector_semantics_status:
    - not_used
    - rejected
    - attempted_rejected
  stress_energy_status:
    - not_used
    - rejected
    - attempted_rejected
  matter_action_status:
    - not_used
    - rejected
    - attempted_rejected
  benchmark_status:
    - not_applicable
    - not_claimed
    - blocked
validation_contract:
  requires_finite_or_local_source_domain: true
  requires_declared_source_objects: true
  requires_allowed_reuse: true
  requires_forbidden_overreads: true
  blocks_target_metric_as_source_data: true
  blocks_detector_semantics_as_source_data: true
  blocks_stress_energy_as_source_data: true
  blocks_matter_action_as_source_data: true
  blocks_benchmark_recovery_claim: true
  requires_certificate_or_obstruction_link_for_p10_t02: true
upstream_primitive_trigger_status:
  EqSrc:
    triggered: false
    reason: "P10-T01 defines a schema while retaining explicit certificate and obstruction records; it does not remove certificate premises or claim record-independent equivalence."
  RetainH:
    triggered: false
    reason: "P10-T01 defines model fields only; it does not claim H-indexed retention or matter-sector continuity under H."
  GenH:
    triggered: false
    reason: "P10-T01 defines model fields only; it does not construct an H-indexed generated family or require generator closure as theorem input."
blocked_authority:
  - canonical_ontology_edit
  - source_law_adoption
  - EqSrc_discharge
  - RetainH_adoption
  - GenH_adoption
  - unrestricted_RR_E_theorem
  - matter_semantics_adoption
  - detector_semantics_adoption
  - coupling_law_adoption
  - matter_coupling_derivation_or_adoption
  - stress_energy_semantics
  - matter_action
  - Einstein_equations
  - benchmark_promotion
  - completed_derivation
```

## Validation Contract

Later source model zoo builders and support-only validators should reject any
model that:

- omits a required field;
- uses a `model_kind` or status value outside the allowed vocabulary;
- lacks finite/local source-domain data;
- lacks `allowed_reuse` or `forbidden_overreads`;
- treats target metric data, target atlas data, detector semantics,
  stress-energy data, matter-action data, or benchmark behavior as source
  model data;
- treats generated outputs, validator success, registry state, role identity,
  handoff state, approval state, commit state, or local cache state as model
  payload data;
- claims source-law adoption, unrestricted `RR_E`, matter coupling,
  stress-energy semantics, matter action, Einstein equations, benchmark
  recovery, proof authority, or completed derivation.

## Done-Criteria Receipt

- The schema includes all fields required by v16 P10-T01.
- The schema includes all eight required model kinds.
- The schema supports P4 positive and fail-closed certificate instances.
- The schema makes finite/local scope explicit.
- The schema records `EqSrc`, `RetainH`, and `GenH` as not triggered by schema
  definition alone.
- No physics delta is made.

## References

The Aether-Flow Research Project. (2026). `implementations_plans/recommendations_implementation_plan_continue_task-v16.md` [Internal project-control plan].

The Aether-Flow Research Project. (2026). `research_control/design/source_certificate_instance_library_index_v1.md` [Internal project-control index].

The Aether-Flow Research Project. (2026). `research_control/design/source_certificate_instance_library_schema_v1.md` [Internal project-control schema].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260705-018/artifacts/upstream_trigger_selector_integration_v16.md` [Internal project-control routing artifact].
