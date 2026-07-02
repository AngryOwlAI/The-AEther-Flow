<!-- authority: control -->

# Route Signature Definition v1

## Purpose

`route_signature_definition_v1` defines the minimum comparable record used to
detect repeated route orbits in research-control history. It is a control
schema for later extraction and validation packets. It is not a physics source,
not a Gate Chair verdict, and not authority to freeze a route by itself.

The definition exists so that later tooling can compare tasks by burden,
route shape, payload novelty, repair attempt, obstruction, freeze evaluation,
and boundary synchronization before another same-shape continuation is allowed.

## Authority Boundary

Route signatures are operational diagnostics. They may warn, hard-fail a
workflow transition when a validator later implements that rule, or request a
repair/freeze/boundary-sync packet. They must not:

- promote ontology, source laws, matter coupling, Einstein equations, benchmark
  status, or completed-derivation claims;
- treat accepted scoped evidence or preconditions as adopted physics objects;
- treat route repetition as a program-wide rejection or impossibility claim;
- override tracked task, AgentJob, completion, handoff, or Gate Chair records.

## Canonical Record

A route signature is a normalized map with these fields.

| Field | Required | Type | Normalization | Purpose |
| --- | --- | --- | --- | --- |
| `signature_schema_id` | yes | string | literal `route_signature_definition_v1` | Identifies this schema. |
| `signature_id` | yes | string | deterministic stable ID | Names the extracted signature. |
| `source_task_id` | yes | string | task ID or `unknown` | Links the signature to a task. |
| `source_job_id` | yes | string | AgentJob ID or `unknown` | Links the signature to a job. |
| `source_completion_path` | yes | string | repo-relative path or empty string | Links to completion evidence. |
| `implementation_plan_id` | yes | string | lower-case plan ID or `none` | Separates v12/v13/v14 routes. |
| `plan_task_id` | yes | string | plan task ID or `none` | Identifies the intended plan step. |
| `target_derivation_milestone` | yes | string | lower-case canonical milestone or `none` | Compares same milestone continuation. |
| `milestone_burden` | yes | string | compact normalized burden or `none` | Compares repeated burden. |
| `object_family` | yes | string | lower-case family or `none` | Groups related objects. |
| `object_name` | yes | string | exact source object name or `none` | Detects same object replay. |
| `task_type` | yes | string | lower-case task type or `unknown` | Compares route shape. |
| `role_id` | yes | string | base role ID or `unknown` | Records execution role. |
| `execution_role_ref` | yes | string | role ref or empty string | Preserves overlay/provisional identity. |
| `source_extension_category` | yes | string | controlled label or `none` | Separates source-extension packets. |
| `selected_route` | yes | string | controlled route label or `unknown` | Captures selector or handoff route. |
| `missing_primitive` | yes | string | exact primitive or `none` | Detects repeated missing-law loops. |
| `payload_type` | yes | string | controlled payload type or `none` | Records the payload class. |
| `obstruction_label` | yes | string | obstruction ID/label or `none` | Distinguishes obstruction progress from replay. |
| `freeze_candidate` | yes | string | freeze label, `true`, `false`, or `none` | Records freeze consideration. |
| `boundary_synchronization_state` | yes | string | controlled state | Records whether scoped evidence boundaries were synchronized. |
| `gate_chair_state` | yes | string | controlled state | Records human-gated review state. |
| `previous_task_ids` | yes | list[string] | sorted task IDs | Links local predecessor route. |
| `new_mathematical_payload_exists` | yes | boolean | boolean | Distinguishes new payload from orbiting. |
| `exact_repair_attempted` | yes | boolean | boolean | Records repair attempts. |
| `freeze_criteria_evaluated` | yes | boolean | boolean | Records freeze review. |
| `new_source_evidence_exists` | yes | boolean | boolean | Records new cited source evidence. |
| `signature_hash` | yes | string | SHA-256 of canonical comparison map | Supports deterministic comparison. |

## Controlled Values

### `boundary_synchronization_state`

- `not_applicable`
- `pending`
- `synchronized`
- `missing_after_scoped_gate_result`
- `unknown`

Use `missing_after_scoped_gate_result` when a Gate Chair scoped evidence or
precondition result is followed by new physics construction before the
boundary, ledger, current-frontier, or public-status layer has been
synchronized.

### `gate_chair_state`

- `not_applicable`
- `not_requested`
- `pending`
- `scoped_evidence_or_precondition_accepted`
- `adoption_rejected_or_blocked`
- `adoption_authorized`
- `unknown`

`adoption_authorized` is human-gated and may be recorded only from an explicit
Gate Chair or human-authorized source. Ordinary route signatures must not
infer it.

### `source_extension_category`

- `none`
- `source_extension_candidate`
- `source_extension_smuggling_audit`
- `source_extension_refuter_stress`
- `source_extension_human_gate`
- `source_extension_adopted_or_rejected`

### `payload_type`

Allowed values are the payload types already named by the GR derivation
roadmap policy plus `none` and `unknown`. Later extractor tooling may emit a
more specific project-control payload type only if it preserves the raw source
field used to derive it.

## Signature Hash

`signature_hash` is the SHA-256 hash of a canonical JSON object containing the
comparison fields below, sorted by key and serialized without whitespace:

- `implementation_plan_id`
- `plan_task_id`
- `target_derivation_milestone`
- `milestone_burden`
- `object_family`
- `object_name`
- `task_type`
- `role_id`
- `source_extension_category`
- `selected_route`
- `missing_primitive`
- `payload_type`
- `obstruction_label`
- `freeze_candidate`
- `boundary_synchronization_state`
- `gate_chair_state`
- `new_mathematical_payload_exists`
- `exact_repair_attempted`
- `freeze_criteria_evaluated`
- `new_source_evidence_exists`

The hash intentionally excludes volatile file paths, timestamps, registry row
order, and human-readable summaries.

## Orbit Candidate Logic

A later validator may classify a route as a hard orbit candidate when all of
the following are true for two or more recent signatures:

- same `target_derivation_milestone`;
- same `milestone_burden`;
- same `missing_primitive`;
- same `selected_route` or same `task_type`;
- same `object_family` and same `object_name` when those fields are known;
- `new_mathematical_payload_exists` is `false`;
- `exact_repair_attempted` is `false`;
- `obstruction_label` is `none`;
- `freeze_criteria_evaluated` is `false`;
- `boundary_synchronization_state` is neither `synchronized` nor
  `not_applicable`;
- `new_source_evidence_exists` is `false`.

A later validator may warn, rather than hard-fail, when the burden repeats with
new payload but the completion lacks an explicit `route_cycle_control` or
equivalent route-signature explanation.

## Boundary-Sync Guard

When `gate_chair_state` is `scoped_evidence_or_precondition_accepted`, later
physics construction should be preceded by `boundary_synchronization_state:
synchronized` or by a completion explanation that the scoped result is not a
precondition for the new construction. This protects against
evidence-as-adoption laundering.

## Extractor Requirements

The P8-T02 extractor should:

- read task, AgentJob, completion, handoff, and relevant registry rows;
- preserve raw source paths for every non-default field;
- emit `unknown` rather than guessing when evidence is absent;
- keep generated retrieval layers out of the authority chain;
- produce at least one task-local sample covering recent matter-coupling and
  `RR_E` chains;
- avoid changing claim boundaries or scientific status.

## Validation Expectations

P8-T03 validator work may use this definition to add warnings or hard-fail
conditions, but that validator must be separately authorized and tested. This
definition alone does not create a hard gate.
