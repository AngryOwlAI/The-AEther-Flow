<!-- authority: control -->

# Minimum Physics Payload Schema v1

## Purpose

`minimum_physics_payload_schema_v1` defines the v16 minimum payload contract
for post-v15 physics tasks. Its purpose is to distinguish payload-bearing
physics work from process receipts, routing metadata, validation status, and
generated derivatives.

This is a project-control schema. It is not a physics proof, not a canonical
ontology edit, not a source-law adoption, not matter-coupling adoption, not an
Einstein-equation derivation, not benchmark promotion, and not completed
derivation evidence.

## Payload Classes

Every payload record must use one of these controlled classes:

```yaml
payload_classes:
  - new_definition
  - theorem_statement
  - proof_attempt
  - proved_conditional_theorem
  - explicit_finite_witness
  - minimal_countermodel
  - obstruction_record
  - source_model
  - certificate_instance
  - executable_support_spec
  - attack_fixture
  - selector_with_scored_route_matrix
  - validation_repair
  - freeze_review
```

## Required Rule

A post-v15 physics task must include at least one of these payload classes:

- `new_definition`;
- `theorem_statement`;
- `proof_attempt`;
- `proved_conditional_theorem`;
- `explicit_finite_witness`;
- `minimal_countermodel`;
- `obstruction_record`;
- `source_model`;
- `certificate_instance`;
- `executable_support_spec`;
- `attack_fixture`.

Exceptions:

- selector tasks may use `selector_with_scored_route_matrix`;
- validation repair tasks may use `validation_repair`;
- freeze tasks may use `freeze_review`;
- documentation and publication tasks must classify as non-physics project
  tasks, not as physics payload tasks.

## Minimal Record Shape

Future validators or route-orbit tools may project completion receipts into
this shape:

```yaml
minimum_payload_schema_id: "minimum_physics_payload_schema_v1"
source_task_id: "RT-YYYYMMDD-NNN"
source_job_id: "AJ-RT-YYYYMMDD-NNN-001"
source_completion_path: "research_control/tasks/RT-YYYYMMDD-NNN/jobs/completions/AJC-AJ-RT-YYYYMMDD-NNN-001.yaml"
target_derivation_milestone: "matter_coupling"
milestone_burden: "example burden"
payload_class: "theorem_statement"
payload_status: "draft/control"
payload_artifact_path: "research_control/tasks/RT-YYYYMMDD-NNN/artifacts/example.tex"
payload_summary: "One sentence source-backed summary."
payload_source_basis:
  - "canonical or task-local source path inspected"
process_receipts_excluded:
  - "validator_status"
  - "registry_row"
  - "handoff_status"
  - "approval_status"
  - "generated_derivative"
physics_promotion_authorized: false
proof_authority: false
```

Fields may be embedded in an existing completion receipt or emitted as a
derived validation record. A derived record is navigational support only unless
a later validator packet explicitly makes it a required gate.

## Payload Class Definitions

| Payload class | Meaning | Not enough by itself |
| --- | --- | --- |
| `new_definition` | Introduces a defined source-side object, predicate, relation, record, or controlled category with stated domain and assumptions. | A name-only row or informal phrase. |
| `theorem_statement` | States a testable theorem target with premises, conclusion, valid regime, and failure branch. | A route label or desired result. |
| `proof_attempt` | Supplies a structured derivation attempt, including missing steps or failure point when incomplete. | A claim that something should follow. |
| `proved_conditional_theorem` | Proves a conditional statement under explicit premises without claiming stronger unrestricted status. | A proof that silently imports target data or process authority. |
| `explicit_finite_witness` | Provides finite or locally finite source-side objects, tables, maps, guards, or records. | A reference to future examples. |
| `minimal_countermodel` | Gives a smallest known model showing a stronger claim fails under stated assumptions. | A generic concern or verbal objection. |
| `obstruction_record` | Names a precise obstruction with source-backed missing datum, failed premise, or blocked derivation step. | A vague statement that progress is hard. |
| `source_model` | Constructs a source-side model or model fragment with declared fields and boundaries. | A target metric, detector semantics, or benchmark behavior. |
| `certificate_instance` | Supplies an explicit certificate record or family with status, domain, codomain, guard, witness payload, and fail-closed branch. | Scoped evidence or validator PASS used as a certificate slot. |
| `executable_support_spec` | Implements deterministic support-only checks, examples, or fixtures tied to source-side payload. | A proof checker claim or production gate without a separate validator packet. |
| `attack_fixture` | Encodes an adversarial case for Refuter, smuggling audit, target-import detection, or validator regression. | A rhetorical objection without executable or inspectable structure. |
| `selector_with_scored_route_matrix` | Selects one route using a scored comparison matrix and source-backed criteria. | Selector prose without alternatives and criteria. |
| `validation_repair` | Repairs validator, schema, registry, or control machinery required before honest physics continuation. | A refresh that merely re-runs existing checks. |
| `freeze_review` | Evaluates whether repeated no-payload cycles require freeze, repair, or human gate. | A generic pause without criteria. |

## Process Receipts Are Not Payload

The following surfaces are not physics payload classes:

- validator PASS;
- unit-test PASS;
- role identity;
- handoff status;
- Director approval status;
- registry row presence;
- generated wiki note;
- generated PDF;
- generated HTML;
- semantic extract;
- Obsidian note;
- `.local/` cache state;
- commit hash;
- file order.

These surfaces may be transaction evidence. They may help verify that a packet
was executed. They do not satisfy the minimum physics payload rule unless an
associated source artifact contains one of the payload classes above.

## Payload Status Is Not Promotion

Payload status records the epistemic and control status of an artifact. It
does not promote the artifact.

Allowed payload statuses include:

- `draft/control`;
- `proposal-only`;
- `support-only`;
- `scoped evidence`;
- `negative result`;
- `human-gated`;
- `rejected`;
- `adopted`.

Only explicit protected authority may use `adopted` for protected physics
objects. The presence of a payload class, payload status, schema PASS,
validator PASS, or checkpoint commit does not authorize source-law adoption,
matter-semantics adoption, detector-semantics adoption, coupling-law adoption,
matter-coupling derivation or adoption, stress-energy semantics, matter
action, Einstein equations, benchmark promotion, Gate Chair verdict, or
completed derivation.

## Relationship To Route Signature Schema

`route_signature_schema_v1` distinguishes new mathematics from process
refreshes using `mathematical_payload_class`, Distance-to-GR fields,
obstruction IDs, freeze criteria, and source-extension classifications. This
schema narrows the post-v15 requirement: future physics packets should not
advance by process refresh alone unless they are selector, validation repair,
freeze review, documentation/publication, or another explicitly non-physics
project task.

The mapping is intentionally conservative:

| Minimum payload class | Route-signature class family |
| --- | --- |
| `new_definition` | `new_definition` |
| `theorem_statement` | `new_theorem_statement` |
| `proof_attempt` | `proof_attempt` |
| `proved_conditional_theorem` | `conditional_theorem` or `proved_theorem` |
| `explicit_finite_witness` | `finite_witness` |
| `minimal_countermodel` | `countermodel` |
| `obstruction_record` | `obstruction` |
| `source_model` | `construction` or `finite_model` |
| `certificate_instance` | `finite_witness` or `construction` |
| `executable_support_spec` | `validator_tooling_only` plus support-only payload evidence |
| `attack_fixture` | `countermodel`, `obstruction`, or validator fixture evidence |
| `selector_with_scored_route_matrix` | `route_selector_only` with scored criteria |
| `validation_repair` | `validator_tooling_only` or `validation_repair` |
| `freeze_review` | `freeze_evaluation` |

If a mapping is ambiguous, the completion must choose the weaker class and
name the limitation.

## Validation Guidance

A future validator may check these conditions:

1. A physics completion after v15 declares a payload class or an allowed
   exception class.
2. The declared payload class is one of the controlled values.
3. The completion names a payload artifact path or explains why the payload is
   wholly contained in the completion.
4. Process receipts are not counted as payload.
5. `physics_promotion_authorized` remains false unless a protected authority
   path is recorded.
6. Selector, validation repair, and freeze-review exceptions are explicitly
   labeled.
7. Documentation/publication tasks classify as non-physics project tasks.

This guidance is not itself a validator implementation. P7-T01 defines the
schema; later packets may decide whether and how to enforce it.

## Done Criteria

- Schema exists.
- Payload classes are controlled.
- The required post-v15 physics task rule is stated.
- Exceptions are stated.
- Payload is distinguished from process receipts.
- Payload status is explicitly not physics promotion.
