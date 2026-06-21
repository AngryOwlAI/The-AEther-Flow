<!-- authority: control -->

# Obstruction And Freeze Control

## Purpose

This control note defines how future opted-in physics completions should record
negative results, repeated-burden cycles, and local freeze decisions. Its aim is
to make obstruction evidence actionable without promoting physics claims.

An obstruction record is a routing object. It states what failed, under which
scope, and what follows. It is not a theorem of global impossibility unless a
separate authorized no-go theorem proves that stronger claim.

A freeze-control record is a route-cycle object. It decides whether the current
route may continue, should narrow, should enter freeze review, should freeze
locally, or should require a human gate. It does not reject the global theory.

## Activation And Compatibility

This note is part of Phase 4 of the mathematical-decisiveness rollout. It
applies prospectively to future physics completions that opt into
`.agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md`.

Historical completions remain valid under the contracts that governed them at
creation. Backfill may cite this note only as metadata overlay and must not
rewrite prior scientific claims.

## Obstruction Scopes

Allowed obstruction scopes are:

- `local_finite_example`
- `exact_finite_local_branch`
- `current_ontology_only`
- `source_extension_candidate`
- `general_source_cover`
- `downstream_metric`
- `matter_coupling`
- `einstein_equations`
- `benchmark_promotion`

Scope discipline:

- `current_ontology_only` means the current ontology does not derive the named
  object. It does not prove future source-extension impossibility.
- `source_extension_candidate` means the obstruction concerns a proposal-only
  source-extension datum or candidate law.
- Downstream scopes such as `downstream_metric`, `matter_coupling`,
  `einstein_equations`, and `benchmark_promotion` preserve upstream blocks
  unless the required gates have already been satisfied.

## Obstruction Consequences

Allowed obstruction consequences are:

- `repair_candidate_allowed`
- `selector_required`
- `route_frozen`
- `human_gate_required`
- `downstream_block_preserved`
- `new_primitive_required`
- `target_import_detected`

Consequence discipline:

- `repair_candidate_allowed` keeps same-milestone continuation open.
- `selector_required` routes to a selector or theoretical-continuation decision
  rather than another vague continuation.
- `route_frozen` freezes only the named local route unless a separate authority
  expands the verdict.
- `human_gate_required` identifies protected authority, such as ontology
  adoption or a gate decision.
- `downstream_block_preserved` states that no downstream GR object was unlocked.
- `new_primitive_required` means the current assumptions lack a named primitive;
  it does not adopt that primitive.
- `target_import_detected` marks an invalid construction path under the
  no-hidden-target-import boundary.

## Required Obstruction Receipt

When `physics_progress_status.status` is `precise_obstruction_found` or
`route_frozen`, the completion must include:

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
  forbidden_overread: "This does not imply global theory rejection or future repair impossibility."
```

The field `forbidden_overread` is mandatory. It is the explicit guard against
turning a scoped obstruction into a global verdict.

## Freeze-Control Policy

A repeated-burden or scoped-obstruction completion must answer:

1. Is this the same burden as a recent prior task?
2. Did the task add a new mathematical object, proof, witness, countermodel, or
   obstruction?
3. Did it merely select another selector route?
4. Has the route already completed a construct-audit-stress cycle?
5. Did the same failure recur?
6. Should the route freeze locally?
7. If not frozen, what exact new work prevents orbit?

Required shape:

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
  decision_reason: "Continuation is non-orbital because the next role must construct or refute a named object."
  next_allowed_route: "candidate_constructor"
  status_update_path: ""
  no_status_update_rationale: "No local freeze was issued."
```

Allowed `freeze_decision` values are:

- `not_frozen`
- `locally_frozen`
- `freeze_review_required`
- `human_gate_required`

Allowed `next_allowed_route` values are:

- `candidate_constructor`
- `smuggling_auditor`
- `refuter`
- `theoretical_selector`
- `gate_chair`
- `freeze_review`
- `none`

If `freeze_decision` is `locally_frozen`, the completion must name a status
update path or explicitly state why no ledger or registry row is updated in that
task. If `next_allowed_route` is `none`, the freeze decision must be
`locally_frozen`, `freeze_review_required`, or `human_gate_required`.

## Route-Cycle Control

Repeated selector, constructor, audit, or stress cycles must include:

```yaml
route_cycle_control:
  cycle_family: "m_src_atlas_glue"
  current_cycle_step: "candidate_constructor"
  prior_related_tasks:
    - "RT-..."
  cycle_risk: "medium"
  orbit_avoidance_reason: "The next role must construct a named source-cover candidate or return a precise obstruction."
  next_role_consequence: "candidate_constructor"
```

The `orbit_avoidance_reason` must explain why the current completion sharpens
state rather than repeating prior work. The `next_role_consequence` must name a
concrete role family or a clear stop condition.

## Route-Cycle Policy

For future physics derivation tasks governed by this note:

```yaml
route_cycle_policy:
  same_burden_selector_limit_before_construction_or_freeze_review: 1
  same_failure_limit_before_freeze_review: 2
  construct_audit_stress_cycle_required_before_adoption_discussion: true
```

These limits are control defaults, not physics facts. A future task may use a
stricter overlay. A looser overlay should cite the reason and preserve the
claim boundary.

## Local Freeze Is Not Global Rejection

`locally_frozen` means the named local route should not continue under the same
burden and assumptions without freeze review, a new construction target, or a
human-gated decision. It does not prove global impossibility, reject future
source extensions, reject the project theory, or authorize downstream GR
promotion.

## Source Materials

The AEther-Flow Research Project. (2026, June 21). *Mathematical decisiveness
completion contract* [Internal control note].
`research_control/design/mathematical_decisiveness_completion_contract.md`

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations
implementation plan* [Internal implementation plan].
`implementations_plans/aether_recommendations_implementation_plan.md`
