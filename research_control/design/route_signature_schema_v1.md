<!-- authority: control -->

# Route Signature Schema v1

## Purpose

`route_signature_schema_v1` is the v15 control schema for route-cycle
detection. It defines the comparison fields that a route-signature extractor
must preserve when a task advances, repeats, repairs, obstructs, freezes, or
only refreshes process state.

This schema is operational control metadata only. It is not a physics source,
not a derivation, not a Gate Chair verdict, not a freeze verdict by itself,
and not authority to promote ontology, source laws, matter coupling,
stress-energy semantics, Einstein equations, benchmark status, or a completed
derivation.

## Relationship To Earlier Route Signature Work

`research_control/design/route_signature_definition.md` defines the v14
`route_signature_definition_v1` extractor record. This v15 schema preserves
that record as valid prior control work and adds a narrower comparison
contract required by v15 P10-T01.

Future P10-T02 tooling may emit either a direct
`route_signature_schema_v1` record or a compatibility projection from the
existing v14 route-history extractor. The projection must preserve raw source
evidence and must not infer missing physics or authority fields.

## Required Signature Fields

Every v15 route signature record must include these fields:

| Field | Type | Required | Normalization | Comparison purpose |
| --- | --- | --- | --- | --- |
| `target_derivation_milestone` | string | yes | lower-case compact milestone or `none` | Detects repeated work against the same derivation target. |
| `milestone_burden` | string | yes | lower-case compact burden or `none` | Detects repeated work against the same unresolved burden. |
| `object_or_claim_name` | string | yes | exact project object or claim name when known, otherwise `none` | Distinguishes repeated object work from distinct object work. |
| `route_family` | string | yes | lower-case compact family | Groups route shapes such as selector, theorem, refuter, gate, validator, or project-control. |
| `role_family` | string | yes | base role family or `unknown` | Records the executing research-control role family. |
| `mathematical_payload_class` | string | yes | controlled value | Separates new mathematical payload from process-only work. |
| `distance_to_gr_delta` | map | yes | controlled subfields | States whether the packet changes Distance-to-GR status. |
| `source_extension_classification` | string | yes | controlled value or `none` | Separates source-extension candidate, audit, stress, gate, and adoption-status work. |
| `obstruction_id` | string | yes | exact obstruction ID or `none` | Prevents a precise obstruction from being counted as empty repetition. |
| `freeze_criteria_status` | map | yes | controlled subfields | Records whether repeated-route freeze criteria were evaluated or triggered. |
| `next_route_selected` | string | yes | lower-case compact route or `unknown` | Captures the successor route selected by completion or handoff. |

The field names above are normative for v15. Compatibility tooling may map
older fields into them only when the mapping is source-backed.

## Canonical Record Shape

```yaml
signature_schema_id: "route_signature_schema_v1"
source_task_id: "RT-YYYYMMDD-NNN"
source_job_id: "AJ-RT-YYYYMMDD-NNN-001"
source_completion_path: "research_control/tasks/RT-YYYYMMDD-NNN/jobs/completions/AJC-AJ-RT-YYYYMMDD-NNN-001.yaml"
target_derivation_milestone: "matter_coupling"
milestone_burden: "positive_matter_semantics_missing"
object_or_claim_name: "PositiveMSProfile_v1"
route_family: "source_extension_gate"
role_family: "gate-chair"
mathematical_payload_class: "scoped_evidence_status_review"
distance_to_gr_delta:
  effect: "scoped_evidence_status_update"
  changed: false
  burden_id: "matter_coupling"
  milestone: "matter_coupling"
source_extension_classification: "source_extension_human_gate"
obstruction_id: "none"
freeze_criteria_status:
  evaluated: false
  triggered: false
  decision: "not_applicable"
  freeze_scope: "none"
next_route_selected: "boundary_synchronization"
route_signature_key: "matter_coupling|positive_matter_semantics_missing|PositiveMSProfile_v1|source_extension_gate|gate-chair|scoped_evidence_status_review|scoped_evidence_status_update|source_extension_human_gate|none|not_applicable|boundary_synchronization"
source_evidence:
  target_derivation_milestone:
    - "completion.physics_progress_status.target_derivation_milestone"
  milestone_burden:
    - "completion.physics_progress_status.milestone_burden"
```

`route_signature_key` is derived from the comparison fields and must not be
edited by hand. A later extractor may also emit a hash of the key. The key
excludes volatile file paths, timestamps, registry order, and human-readable
summaries.

## Controlled Values

### `route_family`

Allowed values:

- `selector`
- `theorem`
- `definition`
- `refuter`
- `countermodel`
- `obstruction`
- `source_extension_candidate`
- `source_extension_audit`
- `source_extension_stress`
- `source_extension_gate`
- `boundary_synchronization`
- `freeze_evaluation`
- `validator`
- `project_control`
- `documentation_control`
- `metrics_control`
- `unknown`

### `role_family`

Use the base role ID when available. Examples include:

- `director-of-research`
- `theoretical-continuation-selector`
- `ontology-formalizer`
- `refuter`
- `gate-chair`
- `validator-engineer`
- `project-control-maintainer`
- `process-integrity-auditor`
- `documentation-curator`
- `unknown`

### `mathematical_payload_class`

New mathematical payload classes:

- `new_definition`
- `new_theorem_statement`
- `proved_theorem`
- `conditional_theorem`
- `proof_attempt`
- `countermodel`
- `finite_witness`
- `construction`
- `obstruction`
- `source_extension_candidate`
- `source_extension_audit_result`
- `source_extension_refuter_result`
- `scoped_evidence_status_review`

Process-refresh classes:

- `route_selector_only`
- `validator_tooling_only`
- `metrics_only`
- `documentation_only`
- `registry_only`
- `handoff_only`
- `boundary_synchronization_only`
- `unknown_process`

`mathematical_payload_class` must be classified from task, completion,
artifact, and registry evidence. If evidence is absent, use `unknown_process`
instead of guessing new mathematics.

### `distance_to_gr_delta`

The required subfields are:

| Subfield | Type | Required | Controlled values or rule |
| --- | --- | --- | --- |
| `effect` | string | yes | Use the Distance-to-GR effect vocabulary enforced by research-control validation. Use `no_distance_delta` for pure process work. |
| `changed` | boolean | yes | `true` only when tracked Distance-to-GR status changes. |
| `burden_id` | string | yes | Ledger burden ID or empty string. |
| `milestone` | string | yes | Derivation milestone or empty string. |

`distance_to_gr_delta.changed: false` does not by itself imply failure. It
only says this packet did not move a tracked Distance-to-GR state.

### `source_extension_classification`

Allowed values:

- `none`
- `source_extension_candidate`
- `source_extension_smuggling_audit`
- `source_extension_refuter_stress`
- `source_extension_human_gate`
- `source_extension_adopted_or_rejected`
- `source_extension_boundary_sync`
- `source_extension_obstruction`

### `freeze_criteria_status`

The required subfields are:

| Subfield | Type | Required | Controlled values or rule |
| --- | --- | --- | --- |
| `evaluated` | boolean | yes | Whether freeze criteria were evaluated. |
| `triggered` | boolean | yes | Whether a freeze was triggered. |
| `decision` | string | yes | `not_applicable`, `evaluated_no_freeze`, `freeze_candidate`, `frozen`, `blocked_adoption_open_continuation`, or `unknown`. |
| `freeze_scope` | string | yes | Exact scope label or `none`. |

Freeze fields are comparison evidence only. A signature does not freeze a
route unless a separate tracked freeze policy or completion authorizes that
result.

## New Mathematics Versus Process Refresh

A signature is a `new_mathematics_signature` when at least one of these
source-backed conditions holds:

- `mathematical_payload_class` is one of the new mathematical payload classes;
- `distance_to_gr_delta.changed` is `true`;
- `obstruction_id` is not `none`;
- `freeze_criteria_status.evaluated` is `true`; or
- `source_extension_classification` is not `none` and the packet produced a
  candidate, audit result, refuter result, scoped evidence-status result, or
  obstruction.

A signature is a `process_refresh_signature` only when all of these conditions
hold:

- `mathematical_payload_class` is one of the process-refresh classes;
- `distance_to_gr_delta.effect` is `no_distance_delta`;
- `distance_to_gr_delta.changed` is `false`;
- `source_extension_classification` is `none`;
- `obstruction_id` is `none`;
- `freeze_criteria_status.evaluated` is `false`;
- `freeze_criteria_status.triggered` is `false`; and
- `next_route_selected` does not claim a new derivation milestone unlock.

This distinction is the main v15 addition. It prevents a validator refresh,
registry refresh, handoff rewrite, or metrics report from being counted as
new mathematics while also preventing a precise obstruction or freeze review
from being misread as empty repetition.

## Route-Cycle Detection Support

A later P10-T02 extractor should build the deterministic
`route_signature_key` from this ordered tuple:

1. `target_derivation_milestone`
2. `milestone_burden`
3. `object_or_claim_name`
4. `route_family`
5. `role_family`
6. `mathematical_payload_class`
7. `distance_to_gr_delta.effect`
8. `source_extension_classification`
9. `obstruction_id`
10. `freeze_criteria_status.decision`
11. `next_route_selected`

A later route-orbit validator may classify a hard orbit candidate when the
same normalized key, or the same key after removing benign process-only
fields, repeats in recent history with:

- `process_refresh_signature: true`;
- no new source evidence;
- no precise obstruction;
- no repair attempt;
- no freeze evaluation; and
- no boundary synchronization.

A later validator should warn rather than hard-fail when the same milestone
and burden repeat with new mathematical payload but the completion lacks a
`route_cycle_control` explanation. Legitimate multi-step theorem work is not
a route orbit merely because it repeats a milestone; it must be evaluated by
payload class, object name, obstruction, freeze, source-extension, and
Distance-to-GR delta fields.

## Compatibility Projection From v14

When projecting a `route_signature_definition_v1` record into this v15 schema,
use this mapping:

| v15 field | v14 source field |
| --- | --- |
| `target_derivation_milestone` | `target_derivation_milestone` |
| `milestone_burden` | `milestone_burden` |
| `object_or_claim_name` | `object_name` |
| `route_family` | `selected_route` when known, otherwise `task_type` |
| `role_family` | `role_id` |
| `mathematical_payload_class` | `payload_type` plus `new_mathematical_payload_exists` |
| `distance_to_gr_delta` | completion `distance_to_gr_delta` if present, otherwise `no_distance_delta` with `changed: false` |
| `source_extension_classification` | `source_extension_category` |
| `obstruction_id` | `obstruction_label` |
| `freeze_criteria_status` | `freeze_candidate` and `freeze_criteria_evaluated` |
| `next_route_selected` | `selected_route` or latest handoff `required_next_packet.task_type` |

Projection must preserve `source_evidence` for every non-default field. It
must emit `unknown` or `none` when evidence is missing.

## Done Criteria

This schema satisfies v15 P10-T01 by:

- declaring the required route signature fields;
- defining how the schema distinguishes new mathematics from process refresh;
- providing a deterministic comparison tuple and key for route-cycle
  detection; and
- preserving the operational authority boundary against physics promotion.

## References

The AEther-Flow Research Project. (2026a). *Route signature definition v1*
[Project-control schema]. `research_control/design/route_signature_definition.md`.

The AEther-Flow Research Project. (2026b). *Recommendations implementation
plan continue task v15* [Implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.
