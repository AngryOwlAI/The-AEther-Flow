<!-- authority: control -->

# Mathematical Decisiveness Completion Contract

## Purpose

This control note defines the prospective completion contract for future
physics AgentJobs. Its purpose is to separate operational validation from
physics progress and to make each future physics completion terminally
informative.

A completion with `validation_status: "PASS"` proves that the task followed
the project-control rules. It does not prove that a theorem was established,
that a source-side law was adopted, that `M_src` was constructed, or that any
downstream GR object was promoted. Physics progress must be stated in explicit
completion fields.

This contract is a project-system rule. It does not promote any physics claim,
does not edit canonical ontology, and does not authorize adoption of
`MSL-MSRC-ATLASGLUE-LAW`, `AtlasGlue_src^+`, `AtlasGlueDisc_src^+`, `M_src`,
`g_eff`, matter coupling, Einstein equations, benchmark status, Gate Chair
closure, completed derivation, future source-extension impossibility, or global
theory rejection.

## Activation And Compatibility

This contract applies prospectively to physics AgentJobs created after
`2026-06-21T01:56:33Z` once their AgentJob or task overlay names this contract
or once validator enforcement is added in a later bounded project-system task.

Historical tasks remain valid under the schemas that governed them at creation.
Backfill may add metadata overlays for older high-value tasks only through a
separate bounded task. Backfill must not rewrite prior scientific artifacts or
change their claim status.

## Source Of Truth

The first rollout uses completion YAML as the source of truth. No new physics
progress registry is created by this Phase 1 contract. Future validator work may
extract summary rows after the completion fields are stable.

The existing `distance_to_gr_status` matrix and `new_mathematical_payload`
fields remain valid. The fields below refine that older receipt pattern by
stating the actual burden effect, the Distance-to-GR delta, the payload manifest,
and the route consequence in a machine-checkable shape.

## Required Fields For Future Physics Completions

Every future physics completion governed by this contract must include:

- `physics_progress_status`
- `distance_to_gr_delta`
- `mathematical_payload_manifest`
- `forbidden_conclusion_summary`

Conditionally required fields:

- `obstruction_record` when the completion reports a precise obstruction or a
  route freeze.
- `freeze_criteria_status` when the task repeats a burden or reports a scoped
  obstruction.
- `candidate_constructor_result` for Candidate Constructor physics tasks.
- `route_cycle_control` when the task is part of a repeated selector,
  constructor, audit, or stress cycle.

## `physics_progress_status`

Purpose: classify what the task actually accomplished, separately from
validator success.

Allowed statuses:

- `burden_discharged`
- `candidate_constructed_pending_audit`
- `candidate_audited_pending_stress`
- `candidate_stress_passed_pending_gate`
- `precise_obstruction_found`
- `route_frozen`
- `human_gate_required`
- `selector_only_no_distance_delta`
- `documentation_or_control_only_no_physics_delta`
- `invalid_under_claim_boundary`
- `no_distance_delta`

Required shape:

```yaml
physics_progress_status:
  status: "selector_only_no_distance_delta"
  target_derivation_milestone: "source_manifold_m_src"
  milestone_burden: "..."
  explanation: "..."
  physics_promotion_authorized: false
  promotion_authority_path: ""
```

Rules:

- `status` must be one of the allowed values.
- `target_derivation_milestone` must match the AgentJob milestone.
- `milestone_burden` must match or refine the AgentJob burden.
- `physics_promotion_authorized` defaults to `false`.
- If `physics_promotion_authorized` is ever `true`, the completion must cite an
  explicit human-gated authority path.

## `distance_to_gr_delta`

Purpose: state whether the task changed the Distance-to-GR ledger or only
preserved the current burden state.

Required shape:

```yaml
distance_to_gr_delta:
  changed: false
  burden_id: "m_src"
  milestone: "source_manifold_m_src"
  old_status: "Refuter stress passed"
  new_status: "Refuter stress passed"
  ledger_row_updated: false
  ledger_path: "registries/DISTANCE_TO_GR_LEDGER.csv"
  downstream_unlocked:
    - "none"
  downstream_still_blocked:
    - "g_eff"
    - "matter_coupling"
    - "einstein_equations"
    - "benchmark_promotion"
  explanation: "..."
```

Rules:

- `changed: true` requires either a corresponding ledger update or an explicit
  reason why the ledger is not updated.
- `downstream_unlocked` must not include `g_eff`, matter coupling, Einstein
  equations, or benchmark promotion unless all upstream gates are satisfied.
- Selector-only and documentation/control-only tasks normally use
  `changed: false`.

## `mathematical_payload_manifest`

Purpose: make the mathematical or control payload concrete and auditable.

Allowed `payload_type` values:

- `definition`
- `lemma`
- `theorem`
- `finite_model`
- `countermodel`
- `explicit_witness`
- `obstruction`
- `construction`
- `dependency_map_update`
- `packet_selection`
- `source_extension_classification`

Required shape:

```yaml
mathematical_payload_manifest:
  - payload_id: "PAYLOAD-001"
    payload_type: "packet_selection"
    object_name: "..."
    claim_status: "draft/control"
    source_path: "..."
    burden_effect: "selects_next"
    summary: "..."
```

Rules:

- At least one payload must have nonempty `object_name` and `burden_effect`.
- `construction` requires a source path to the constructed artifact.
- `obstruction` requires `obstruction_record`.
- A pure packet selection normally pairs with
  `selector_only_no_distance_delta` unless the selector changes route status.

## `obstruction_record`

Purpose: preserve negative results in a form future agents can route from.

Required when `physics_progress_status.status` is `precise_obstruction_found`
or `route_frozen`.

Required shape:

```yaml
obstruction_record:
  present: true
  obstruction_id: "OBST-MSRC-ATLASGLUE-GENERAL-COVER-001"
  scope: "general_source_cover"
  failed_object: "selector preorder"
  exact_failure: "..."
  minimal_counterexample_path: ""
  current_ontology_implication: "does_not_derive"
  source_extension_implication: "repair_allowed"
  consequence: "repair_candidate_allowed"
  forbidden_overread: "..."
```

Rules:

- `scope`, `failed_object`, `exact_failure`, and `consequence` must be
  nonempty.
- `forbidden_overread` must state why the obstruction does not imply a global
  theory rejection unless a separate authorized no-go theorem exists.

## `freeze_criteria_status`

Purpose: prevent repeated-burden orbit.

Required for repeated-burden tasks and scoped-obstruction tasks.

Required shape:

```yaml
freeze_criteria_status:
  repeated_burden: true
  freeze_evaluation_required: true
  active_freeze_label: "MSRC-ATLASGLUE-GENERAL-SOURCE-COVER-FAILURE"
  prior_attempts_considered:
    - "RT-..."
  freeze_if:
    - "..."
  do_not_freeze_if:
    - "..."
  freeze_decision: "not_frozen"
  decision_reason: "..."
  next_allowed_route: "candidate_constructor"
```

Allowed `freeze_decision` values:

- `not_frozen`
- `locally_frozen`
- `freeze_review_required`
- `human_gate_required`

Rules:

- `not_frozen` requires a reason explaining why continuation is non-orbital.
- `locally_frozen` requires a ledger or registry status update, or an explicit
  reason why no row is updated in this task.
- `next_allowed_route: "none"` requires human-gated or freeze-review authority.

## `candidate_constructor_result`

Purpose: prevent Candidate Constructor completions from ending in vague
continuation language.

Required for Candidate Constructor physics tasks.

Allowed `result_type` values:

- `constructed_candidate`
- `minimal_countermodel`
- `precise_obstruction`
- `invalid_under_claim_boundary`

Required shape:

```yaml
candidate_constructor_result:
  result_type: "constructed_candidate"
  constructed_candidate_path: "..."
  minimal_countermodel_path: ""
  obstruction_id: ""
  formal_objects:
    - "..."
  maps:
    - "..."
  proof_obligations:
    - "..."
  failed_components:
    - ""
  next_required_role: "smuggling_auditor"
  no_fog_check: true
  no_fog_explanation: "States exactly what was constructed or exactly what failed."
  claim_boundary_preserved: true
  claim_boundary_citation: ""
```

Rules:

- A constructed candidate must name the constructed candidate path, formal
  objects, maps, proof obligations, and next role.
- A countermodel must name the countermodel path and failed components.
- A precise obstruction must name the obstruction identifier, failed
  components, and a present `obstruction_record`.
- An invalid-under-claim-boundary result must name failed components and cite
  the claim boundary it violates.
- `no_fog_check` must be `true`.
- `no_fog_explanation` must state the decisive result in plain language. It may
  not use fog-only language such as "more work required", "candidate remains
  open", "future work should explore", "insufficient time",
  "controlled pause", "selector should decide next", or "generalization not
  attempted" as the primary result.

## `forbidden_conclusion_summary`

Purpose: force each completion to state what it does not authorize.

Required shape:

```yaml
forbidden_conclusion_summary:
  physics_promotion_authorized: false
  forbidden_conclusions:
    - "canonical ontology edit"
    - "M_src adoption"
    - "g_eff claim"
  summary: "..."
```

Rules:

- The summary must explicitly block downstream GR promotion unless a separate
  human-gated source authorizes it.
- Validator PASS, role authority, registry authority, generated derivatives, and
  prior finite witnesses are not physics evidence by themselves.

## `route_cycle_control`

Purpose: expose repeated selector, constructor, audit, or stress loops.

Required shape when applicable:

```yaml
route_cycle_control:
  cycle_family: "m_src_atlas_glue"
  current_cycle_step: "candidate_constructor"
  prior_related_tasks:
    - "RT-..."
  cycle_risk: "low"
  orbit_avoidance_reason: "..."
  next_role_consequence: "smuggling_auditor"
```

Rules:

- `orbit_avoidance_reason` must explain why the task sharpens state instead of
  repeating prior work.
- `next_role_consequence` must be a concrete next role family or a clear stop
  condition.

## Enforcement Schedule

Phase 1, this task: documentation only. The contract exists and can be cited by
future task overlays.

Phase 2: validator support should warn, not fail, on missing fields for pilot
tasks.

Phase 3: validator support may convert the missing-field checks into hard
failures for future physics tasks after one successful pilot completion.

Required future validator work:

- update `scripts/research_control/validate_research_control.py`;
- update completion YAML template or schema documentation;
- add fixtures for valid selector-only, valid Candidate Constructor,
  obstruction, vague Candidate Constructor failure, and promotion-without-gate
  cases.

## Operating Rule

Future physics tasks should leave the research state sharper than they found it.
The acceptable terminal outcomes are burden discharged, candidate constructed,
candidate audited, candidate stress-passed pending gate, precise obstruction,
route freeze, human gate required, selector-only no-distance-delta,
documentation/control-only no-physics-delta, invalid under claim boundary, or
explicit no-distance-delta.
