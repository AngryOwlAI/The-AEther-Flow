<!-- authority: control -->

# Source Certificate Instance Library Schema v1

## Status

This schema implements v16 P4-T01. It defines the required record shape for
finite/local source-certificate instances used by later P4, P5, P6, P10, P14,
and P15 packets.

The schema is a draft/control design surface. It is not a universal matter
coupling construction. It does not adopt a source law,
`RR_ETransportCompletenessOrInvarianceLaw_v1`, an unrestricted `RR_E` theorem,
matter semantics, detector semantics, a coupling law, matter coupling,
stress-energy semantics, matter action, Einstein equations, benchmark status,
or a completed derivation.

## Scope

A certificate instance is one finite or locally finite record. It may be used
as a fixture, witness, negative example, or support-only validation input. It
does not certify objects outside its declared source domain, codomain, labels,
guards, and witness payload.

The schema consumes the existing source certificate algebra controls:

- `research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex`
- `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`
- `research_control/design/source_certificate_algebra_checklist.md`
- `research_control/tasks/RT-20260704-024/artifacts/post_selected_theorem_route_selector_v16.md`

Generated wiki notes, registries, validator output, role identity, commits,
handoff status, approvals, and local caches are not certificate payload data.

## Instance Kind Vocabulary

Every record must use exactly one `instance_kind` value:

- `valid_transport_certificate`
- `valid_invariance_certificate`
- `valid_factorization_certificate`
- `missing_certificate_negative`
- `malformed_certificate_negative`
- `target_import_rejected_certificate`
- `detector_semantics_rejected_certificate`
- `process_authority_rejected_certificate`

The first three kinds are positive source-side examples. The remaining kinds
are fail-closed examples. No kind authorizes target-side import or downstream
physics promotion.

## Required Record Fields

```yaml
certificate_instance_id:
instance_kind:
source_object_A:
source_object_B:
declared_context:
domain:
codomain:
source_labels:
source_guards:
response_tokens:
certificate_payload:
no_target_import_guard:
status:
expected_equivalence_result:
rr_e_separation_effect:
fail_closed_reason:
target_import_used: false
detector_semantics_used: false
stress_energy_used: false
matter_action_used: false
benchmark_behavior_used: false
process_authority_used: false
source_paths:
forbidden_overreads:
```

## Field Semantics

| Field | Required type | Semantics |
| --- | --- | --- |
| `certificate_instance_id` | stable string | Unique id for this finite/local instance. Recommended form: `SCI-<KIND>-<NNN>`. |
| `instance_kind` | enum | One value from the instance-kind vocabulary. |
| `source_object_A` | record | Declared source object index, labels, local carrier, and source-only status for the domain-side object. |
| `source_object_B` | record or `null` | Declared source object index, labels, local carrier, and source-only status for the codomain-side object. `null` is allowed only for a missing certificate negative where the missing slot itself is the point. |
| `declared_context` | record | Local context id, finite/local support, declared scope, and assumptions. |
| `domain` | record | Source-side domain data, including object indices, labels, guards, and response-token type. |
| `codomain` | record | Source-side codomain data compatible with the intended certificate use. |
| `source_labels` | list | Source labels used by the instance. These are not target atlas labels or detector-event labels. |
| `source_guards` | list | Source-side validity guards that must pass before the instance can be used positively. |
| `response_tokens` | list | Source response/readout tokens named by the finite/local context. Tokens are source records, not measurements of matter semantics. |
| `certificate_payload` | record or `null` | Witness data for positive records; defect description for malformed or rejected records; `null` for a missing certificate negative. |
| `no_target_import_guard` | record | Explicit pass/fail guard covering target metric, target topology, target atlas, proper time, detector semantics, stress-energy, matter action, benchmark behavior, process authority, validators, commits, and generated derivatives. |
| `status` | enum | One of `valid`, `missing`, `malformed`, `rejected_target_import`, `rejected_detector_semantics`, `rejected_process_authority`, or `fail_closed`. |
| `expected_equivalence_result` | enum | One of `declared_equivalence_allowed`, `declared_equivalence_blocked`, or `not_applicable`. |
| `rr_e_separation_effect` | enum | One of `preserves_declared_separation`, `does_not_identify`, `not_applicable`, or `obstruction_recorded`. |
| `fail_closed_reason` | string or `null` | Required for every non-positive record; `null` only when `status: valid`. |
| `target_import_used` | boolean | Must be `false` for positive records. Must be `true` only for the target-import negative example. |
| `detector_semantics_used` | boolean | Must be `false` for positive records. Must be `true` only for the detector-semantics rejected example. |
| `stress_energy_used` | boolean | Must remain `false` in every v16 P4 schema-conforming record. |
| `matter_action_used` | boolean | Must remain `false` in every v16 P4 schema-conforming record. |
| `benchmark_behavior_used` | boolean | Must remain `false` in every v16 P4 schema-conforming record. |
| `process_authority_used` | boolean | Must be `false` for positive records. Must be `true` only for the process-authority rejected example. |
| `source_paths` | list | Canonical source paths used to construct the instance. Generated derivatives may be listed only as non-authority aids if needed. |
| `forbidden_overreads` | list | Explicit statements of claims the instance does not support. |

## Positive-Instance Requirements

For `valid_transport_certificate`, `valid_invariance_certificate`, and
`valid_factorization_certificate`, the record must satisfy:

1. `status: valid`.
2. `certificate_payload` is non-null and names a source-side witness.
3. `target_import_used`, `detector_semantics_used`, `stress_energy_used`,
   `matter_action_used`, `benchmark_behavior_used`, and
   `process_authority_used` are all `false`.
4. `no_target_import_guard.result: pass`.
5. `expected_equivalence_result: declared_equivalence_allowed` only inside the
   declared source scope.
6. `rr_e_separation_effect` is either `preserves_declared_separation` or
   `not_applicable`; no positive record identifies unrestricted `RR_E`.
7. `forbidden_overreads` includes all no-adoption and no-promotion boundaries.

## Negative-Instance Requirements

For missing, malformed, target-import, detector-semantics, and
process-authority records, the record must satisfy:

1. `status` names the relevant failure state or `fail_closed`.
2. `expected_equivalence_result: declared_equivalence_blocked`.
3. `rr_e_separation_effect` is `preserves_declared_separation`,
   `does_not_identify`, or `obstruction_recorded`.
4. `fail_closed_reason` is non-null and names the precise defect.
5. No negative record may be interpreted as evidence for impossibility of all
   future source extensions. It records one bounded fail-closed branch.

## Machine-Readable Schema

```yaml
schema_id: "source_certificate_instance_library_schema_v1"
schema_status: "draft/control"
instance_grain: "finite_or_locally_finite_source_certificate_record"
universal_matter_coupling_claim: false
physics_promotion_authorized: false
required_fields:
  - certificate_instance_id
  - instance_kind
  - source_object_A
  - source_object_B
  - declared_context
  - domain
  - codomain
  - source_labels
  - source_guards
  - response_tokens
  - certificate_payload
  - no_target_import_guard
  - status
  - expected_equivalence_result
  - rr_e_separation_effect
  - fail_closed_reason
  - target_import_used
  - detector_semantics_used
  - stress_energy_used
  - matter_action_used
  - benchmark_behavior_used
  - process_authority_used
  - source_paths
  - forbidden_overreads
instance_kinds:
  positive:
    - valid_transport_certificate
    - valid_invariance_certificate
    - valid_factorization_certificate
  negative:
    - missing_certificate_negative
    - malformed_certificate_negative
    - target_import_rejected_certificate
    - detector_semantics_rejected_certificate
    - process_authority_rejected_certificate
status_values:
  - valid
  - missing
  - malformed
  - rejected_target_import
  - rejected_detector_semantics
  - rejected_process_authority
  - fail_closed
expected_equivalence_result_values:
  - declared_equivalence_allowed
  - declared_equivalence_blocked
  - not_applicable
rr_e_separation_effect_values:
  - preserves_declared_separation
  - does_not_identify
  - not_applicable
  - obstruction_recorded
positive_guard:
  requires_source_side_payload: true
  requires_no_target_import_guard_pass: true
  requires_all_forbidden_import_booleans_false: true
negative_guard:
  requires_fail_closed_reason: true
  blocks_declared_equivalence: true
  blocks_unrestricted_rr_e_identification: true
blocked_authority:
  - canonical_ontology_edit
  - source_law_adoption
  - RR_ETransportCompletenessOrInvarianceLaw_v1_adoption
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

Later fixture builders and support-only validators should reject any record
that:

- omits a required field;
- uses an `instance_kind`, `status`, `expected_equivalence_result`, or
  `rr_e_separation_effect` outside the allowed vocabulary;
- marks a positive record as target-importing, detector-semantics importing,
  stress-energy using, matter-action using, benchmark-behavior using, or
  process-authority using;
- treats generated outputs, validator success, registry state, role identity,
  handoff state, approval state, commit state, or local cache state as
  certificate payload data;
- claims universal matter coupling, stress-energy semantics, matter action,
  Einstein equations, benchmark recovery, or completed derivation.

## Done-Criteria Receipt

- The schema is precise enough for fixture construction and support-only
  validation.
- The schema covers transport, invariance, factorization, missing, malformed,
  target-import, detector-semantics, and process-authority cases.
- The schema states finite/local scope and no physics delta.
