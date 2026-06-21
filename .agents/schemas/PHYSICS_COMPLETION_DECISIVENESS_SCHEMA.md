---
schema_id: "PHYSICS_COMPLETION_DECISIVENESS_SCHEMA"
version: "0.1.0"
status: "active"
activation_mode: "prospective_hard_failure_for_opted_in_future_physics_jobs"
active_after: "2026-06-21T02:32:39Z"
---

# Physics Completion Decisiveness Schema

## Purpose

This schema makes the mathematical-decisiveness completion contract
machine-readable for future physics AgentJobs. It separates operational
validation from physics progress and gives validators one authoritative place
to inspect completion fields and allowed values.

This schema does not promote physics claims. It does not authorize canonical
ontology edits, `M_src` adoption, `g_eff` definition, matter coupling,
Einstein-equation derivation, exact-GR benchmark promotion, Gate Chair closure,
completed-derivation language, future source-extension impossibility, or
global theory rejection.

## Activation And Compatibility

Phase 3 activation is prospective and enforceable for future physics AgentJobs
that opt into this schema by naming either:

```yaml
mathematical_decisiveness_contract_active_after: "2026-06-21T02:32:39Z"
mathematical_decisiveness_schema: ".agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md"
```

or by naming the control contract:

```yaml
mathematical_decisiveness_contract:
  contract_path: "research_control/design/mathematical_decisiveness_completion_contract.md"
  schema_path: ".agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md"
  enforcement_mode: "hard_failure"
  active_after: "2026-06-21T02:32:39Z"
```

Historical tasks remain valid. Missing or malformed fields under this schema
become hard validation failures only for opted-in future physics AgentJobs at
or after the active timestamp. Non-physics project-system completions remain
outside this physics-completion contract.

## Registry Convention

The Phase 2 decision is to keep allowed values in this schema rather than add
new registries. Completion YAML remains the source of truth. If later query
needs justify registries, use type registries only for stable enumerations:

- `PHYSICS_PROGRESS_STATUS_TYPE_REGISTRY.csv`
- `OBSTRUCTION_SCOPE_TYPE_REGISTRY.csv`
- `OBSTRUCTION_CONSEQUENCE_TYPE_REGISTRY.csv`
- `CANDIDATE_CONSTRUCTOR_RESULT_TYPE_REGISTRY.csv`

Such registries require a later bounded task and must not rewrite scientific
claim status.

## Required Completion Fields

Opted-in future physics completions should include:

- `physics_progress_status`
- `distance_to_gr_delta`
- `mathematical_payload_manifest`
- `forbidden_conclusion_summary`

Conditionally expected fields:

- `obstruction_record` when `physics_progress_status.status` is
  `precise_obstruction_found` or `route_frozen`.
- `freeze_criteria_status` when a repeated burden or scoped obstruction is
  reported.
- `candidate_constructor_result` for Candidate Constructor physics tasks.
- `route_cycle_control` when the task belongs to a repeated selector,
  constructor, audit, or stress cycle.

## `physics_progress_status`

Allowed `status` values:

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
  milestone_burden: "M_src"
  explanation: "Selector chose a next packet but did not construct or adopt M_src."
  physics_promotion_authorized: false
  promotion_authority_path: ""
```

Rules:

- `status` must be one of the allowed values.
- `target_derivation_milestone` should match the AgentJob milestone.
- `milestone_burden` should match or refine the AgentJob burden.
- `physics_promotion_authorized` defaults to `false`.
- Any `true` value requires an explicit human-gated authority path.

## `distance_to_gr_delta`

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
  explanation: "No Distance-to-GR delta; downstream GR objects remain blocked."
```

Rules:

- `changed: true` should pair with a ledger update or an explicit no-ledger
  rationale.
- `downstream_unlocked` must not include downstream GR objects unless upstream
  gates are satisfied.
- Selector-only and documentation/control-only completions normally use
  `changed: false`.

## `mathematical_payload_manifest`

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

Allowed `burden_effect` values:

- `discharges`
- `narrows`
- `obstructs`
- `selects_next`
- `audits`
- `stress_tests`
- `freezes`
- `requires_human_gate`
- `no_distance_delta`

Required shape:

```yaml
mathematical_payload_manifest:
  - payload_id: "PAYLOAD-001"
    payload_type: "packet_selection"
    object_name: "general source-cover construction packet"
    claim_status: "draft/control"
    source_path: "research_control/tasks/RT-.../artifacts/..."
    burden_effect: "selects_next"
    summary: "Names the next same-milestone packet without adopting M_src."
```

Rules:

- At least one payload should have nonempty `object_name` and `burden_effect`.
- `construction` should name a constructed artifact path.
- `obstruction` should pair with `obstruction_record`.

## `obstruction_record`

Allowed `scope` values:

- `local_finite_example`
- `exact_finite_local_branch`
- `current_ontology_only`
- `source_extension_candidate`
- `general_source_cover`
- `downstream_metric`
- `matter_coupling`
- `einstein_equations`
- `benchmark_promotion`

Allowed `current_ontology_implication` values:

- `does_not_derive`
- `contradicts`
- `not_applicable`

Allowed `source_extension_implication` values:

- `repair_allowed`
- `new_primitive_required`
- `target_import_detected`
- `not_applicable`

Allowed `consequence` values:

- `repair_candidate_allowed`
- `selector_required`
- `route_frozen`
- `human_gate_required`
- `downstream_block_preserved`
- `new_primitive_required`
- `target_import_detected`

Required shape when present:

```yaml
obstruction_record:
  present: true
  obstruction_id: "OBST-MSRC-001"
  scope: "general_source_cover"
  failed_object: "selector preorder"
  exact_failure: "The source-only selector is not well-defined under the stated hypotheses."
  minimal_counterexample_path: ""
  current_ontology_implication: "does_not_derive"
  source_extension_implication: "repair_allowed"
  consequence: "repair_candidate_allowed"
  forbidden_overread: "This does not imply global theory rejection."
```

Rules:

- `forbidden_overread` is required for any present obstruction record.
- `target_import_detected` is an obstruction consequence, not an adopted
  source-side definition.
- A scoped obstruction does not authorize global theory rejection unless a
  separate authorized no-go theorem proves that stronger claim.

## `freeze_criteria_status`

Required for repeated-burden tasks and scoped-obstruction tasks.

Allowed `freeze_decision` values:

- `not_frozen`
- `locally_frozen`
- `freeze_review_required`
- `human_gate_required`

Allowed `next_allowed_route` values:

- `candidate_constructor`
- `smuggling_auditor`
- `refuter`
- `theoretical_selector`
- `gate_chair`
- `freeze_review`
- `none`

Required shape when present for mathematical-decisiveness enforcement:

```yaml
freeze_criteria_status:
  repeated_burden: true
  freeze_evaluation_required: true
  active_freeze_label: "MSRC-ATLASGLUE-GENERAL-SOURCE-COVER-FAILURE"
  prior_attempts_considered:
    - "RT-..."
  freeze_if:
    - "Same failed object recurs without new payload."
  do_not_freeze_if:
    - "A concrete repair candidate is constructed and routed to audit."
  freeze_decision: "not_frozen"
  decision_reason: "Continuation is non-orbital because a named construction or obstruction is required."
  next_allowed_route: "candidate_constructor"
```

Rules:

- `not_frozen` must explain why continuation is non-orbital.
- `locally_frozen` must name a status update path or explain why no ledger or
  registry row is updated in that task.
- `next_allowed_route: "none"` requires `locally_frozen`,
  `freeze_review_required`, or `human_gate_required`.

## `route_cycle_control`

Required when a repeated selector, constructor, audit, stress, or obstruction
cycle is being reported.

Required shape:

```yaml
route_cycle_control:
  cycle_family: "m_src_atlas_glue"
  current_cycle_step: "candidate_constructor"
  prior_related_tasks:
    - "RT-..."
  cycle_risk: "medium"
  orbit_avoidance_reason: "The next role must construct or refute a named object."
  next_role_consequence: "candidate_constructor"
```

Rules:

- `orbit_avoidance_reason` must state why the task sharpens state instead of
  repeating prior work.
- `next_role_consequence` must be a concrete role family or stop condition.

## `candidate_constructor_result`

Allowed `result_type` values:

- `constructed_candidate`
- `minimal_countermodel`
- `precise_obstruction`
- `invalid_under_claim_boundary`

Required shape for Candidate Constructor completions:

```yaml
candidate_constructor_result:
  result_type: "constructed_candidate"
  constructed_candidate_path: "research_control/tasks/RT-.../artifacts/..."
  minimal_countermodel_path: ""
  obstruction_id: ""
  formal_objects:
    - "source-cover candidate"
  maps:
    - "source profiles to candidate transition data"
  proof_obligations:
    - "hidden target import audit"
  failed_components:
    - ""
  next_required_role: "smuggling_auditor"
  no_fog_check: true
  no_fog_explanation: "States exactly what was constructed or exactly what failed."
  claim_boundary_preserved: true
  claim_boundary_citation: ""
```

Rules:

- `no_fog_check` must be `true`.
- `no_fog_explanation` must be the primary result explanation. It may not end
  in fog-only language such as "more work required", "candidate remains open",
  "future work should explore", "insufficient time", "controlled pause",
  "selector should decide next", or "generalization not attempted".
- `next_required_role` must name a concrete role family or `none`.
- `constructed_candidate` requires `constructed_candidate_path`,
  `formal_objects`, `maps`, and `proof_obligations`.
- `minimal_countermodel` requires `minimal_countermodel_path` and
  `failed_components`.
- `precise_obstruction` requires `obstruction_id`, `failed_components`, and a
  present `obstruction_record`.
- `invalid_under_claim_boundary` requires `failed_components` and
  `claim_boundary_citation`.
- `claim_boundary_preserved` must be `true`.

## `forbidden_conclusion_summary`

Required shape:

```yaml
forbidden_conclusion_summary:
  physics_promotion_authorized: false
  forbidden_conclusions:
    - "canonical ontology edit"
    - "M_src adoption"
    - "g_eff claim"
    - "matter coupling claim"
    - "Einstein-equation claim"
    - "benchmark promotion"
    - "Gate Chair verdict"
    - "completed derivation"
    - "global theory rejection"
  summary: "Validator PASS and role authority are not physics evidence."
```

## Phase Boundary

Phase 2 provided schema, template, and warning-level inspection. Phase 3
converted the required-field, Candidate Constructor, obstruction/freeze, and
unauthorized-promotion checks into hard validator errors for opted-in future
physics AgentJobs. Phase 4 added obstruction/freeze vocabulary and route-cycle
control requirements. Phase 5 tightens Candidate Constructor no-fog result
fields and role-facing output rules. This enforcement does not promote physics
claims and does not authorize downstream GR objects.

## Source Materials

The AEther-Flow Research Project. (2026, June 21). *Mathematical decisiveness
completion contract* [Internal control note].
`research_control/design/mathematical_decisiveness_completion_contract.md`

The AEther-Flow Research Project. (2026, June 21). *Obstruction and freeze
control* [Internal control note].
`research_control/design/obstruction_and_freeze_control.md`

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations
implementation plan* [Internal implementation plan].
`implementations_plans/aether_recommendations_implementation_plan.md`
