<!-- authority: control -->

# V18 Recommendation Backlog Schema

```yaml
schema_id: "v18_recommendation_backlog_schema_v1"
schema_for: "research_control/design/v18_recommendation_backlog.yaml"
authority_status: "project_control"
source_plan: "implementations_plans/recommendations_implementation_plan_continue_task-v18.md"
created_at: "2026-07-07T05:42:52Z"
physics_promotion_authorized: false
proof_authority: false
external_outreach_authorized: false
```

## Purpose

This schema defines the machine-readable backlog required by v18 P0-T02. The
backlog converts the v18 implementation plan into task-addressable Continue
Research packets without changing scientific claim status.

The backlog is control infrastructure. It is not a physics proof, source-law
adoption, general EqSrc discharge, RetainH adoption, GenH adoption,
source-detector/readout semantics adoption, coupling-law adoption,
matter-coupling derivation, Einstein-equation derivation, benchmark promotion,
Gate Chair verdict, external outreach, or completed derivation.

## Top-Level Object

The backlog file must be a YAML mapping with these required keys:

```yaml
schema_id: string
authority: "project_control"
status: string
created_at: timestamp-string
source_plan: object
scope: object
recommendation_coverage_rules: object
validator_sets: object
common_failure_route: string
items: list[backlog_item]
```

### `source_plan`

```yaml
source_plan:
  plan_id: string
  plan_path: string
  object_id: string
  source_hash: sha256-string
```

The `plan_path` must point to
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`. The `source_hash` must match the registered source row for that
plan at the time P0-T02 is executed.

### `scope`

```yaml
scope:
  execution_mode: "one_bounded_continue_research_agentjob_per_plan_task"
  dependency_model: string
  acyclic_by_construction: boolean
  task_count: integer
  first_physics_bearing_task_after_p0: string
  physics_promotion_authorized: false
  proof_authority: false
  benchmark_promotion_authorized: false
  external_outreach_authorized: false
  completed_derivation_authorized: false
```

`task_count` must equal the number of `### P*-T*` plan task headings in the
registered v18 plan. For the current v18 plan, that count is `68`.

`first_physics_bearing_task_after_p0` must be `P2-T01` unless a future Director
Decision Record explicitly supersedes this plan. P1 is active-state
project-system work and does not carry a physics delta.

## Backlog Item

Every item in `items` must contain these fields:

```yaml
backlog_item:
  plan_task_id: string
  phase_id: string
  title: string
  recommendation_ids: list[string]
  depends_on: list[string]
  role_family: string
  route_type: string
  task_type: string
  target_derivation_milestone: string
  milestone_burden: string
  expected_outputs: list[string]
  required_validators: list[string]
  physics_delta_allowed: boolean
  promotion_allowed: false
  human_gate_required: boolean
  project_system_boundary_authorized_by_plan: boolean
  implementation_status: string
  recommendation_coverage_role: string
  next_route_on_success: string
  next_route_on_failure: string
```

The v18 plan explicitly required these fields. This schema preserves them
exactly and adds `route_type`, `project_system_boundary_authorized_by_plan`,
`implementation_status`, and `recommendation_coverage_role` as control fields:

```yaml
required_by_plan:
  - plan_task_id
  - phase_id
  - title
  - recommendation_ids
  - depends_on
  - role_family
  - task_type
  - target_derivation_milestone
  - milestone_burden
  - expected_outputs
  - required_validators
  - physics_delta_allowed
  - promotion_allowed
  - human_gate_required
  - next_route_on_success
  - next_route_on_failure
```

## Coverage Rules

1. Every `### P*-T*` heading in the registered v18 plan must appear exactly
   once as an `items[].plan_task_id`.
2. No backlog item may use a `plan_task_id` absent from the registered v18
   plan.
3. `items[].depends_on` must reference only earlier backlog items unless a
   future Director Decision Record explicitly authorizes a non-linear
   dependency.
4. The dependency graph must be acyclic.
5. `P0-T01` must have no dependency.
6. `P0-T02` must depend on `P0-T01`.
7. `P0-T03` must depend on `P0-T02`.
8. `P2-T01` must be the first physics-bearing task after P0.
9. Every `V18-R*` recommendation must appear in at least one backlog item with
   `recommendation_coverage_role: "direct_implementation"`.
10. `P11-T05` must carry all ten `V18-R*` recommendation IDs and use
    `recommendation_coverage_role: "final_coverage_audit"`.

## Authority Rules

`promotion_allowed` must be `false` for every v18 backlog item unless a later
protected authority explicitly supersedes this schema.

Project-system tasks must set:

```yaml
project_system_boundary_authorized_by_plan: true
physics_delta_allowed: false
```

Physics-bearing or science-draft tasks may set:

```yaml
physics_delta_allowed: true
promotion_allowed: false
```

This means draft/control construction, audit, stress, selector, obstruction,
or support-only formalization work may be routed. It does not mean
Distance-to-GR ledger movement, source-law adoption, general EqSrc discharge,
RetainH adoption, GenH adoption, source-detector/readout semantics adoption,
coupling-law adoption, matter-coupling derivation, benchmark promotion, proof
authority, external outreach, or completed derivation.

## Validation Expectations

A valid P0-T02 completion must record at least these checks:

```yaml
minimum_checks:
  - "backlog YAML parses"
  - "backlog task count equals v18 plan task count"
  - "every v18 plan task appears exactly once"
  - "dependencies reference existing earlier tasks"
  - "dependencies are acyclic"
  - "P2-T01 is first physics-bearing task after P0"
  - "project-system tasks carry project_system_boundary_authorized_by_plan: true"
  - "promotion_allowed is false for every item"
  - "every V18 recommendation appears in a direct implementation task"
  - "P11-T05 is the final coverage audit for all ten V18 recommendations"
  - "P0-T02 next route is P0-T03"
```

The backlog validator may be an inline receipt in P0-T02, a task-local script,
or a future permanent validator. P0-T02 does not require permanent validator
installation.

## Forbidden Interpretations

The backlog must not be cited as evidence for:

- canonical ontology edit;
- source-law adoption;
- general EqSrc discharge;
- RetainH adoption;
- GenH adoption;
- `MetricData(E)` adoption;
- `g_eff` scope expansion;
- physical metric authority;
- detector semantics adoption;
- source-detector/readout semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor construction;
- matter action import;
- Einstein-equation derivation;
- benchmark promotion;
- Gate Chair verdict;
- external outreach;
- proof authority;
- completed derivation;
- future source-extension impossibility;
- program-wide no-go conclusion.

## Source Material

The AEther-Flow Research Project. (2026). *Recommendations implementation plan
continue task v18* [Internal implementation plan].
