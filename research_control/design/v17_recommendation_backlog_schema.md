<!-- authority: control -->

# V17 Recommendation Backlog Schema

```yaml
schema_id: "v17_recommendation_backlog_schema_v1"
schema_for: "research_control/design/v17_recommendation_backlog.yaml"
authority_status: "project_control"
source_plan: "implementations_plans/recommendations_implementation_plan_continue_task-v17.md"
created_at: "2026-07-05T18:14:02Z"
physics_promotion_authorized: false
proof_authority: false
```

## Purpose

This schema defines the machine-readable backlog required by v17 P0-T02. The
backlog converts the v17 implementation plan into task-addressable Continue
Research packets without changing scientific claim status.

The backlog is control infrastructure. It is not a physics proof, source-law
adoption, coupling-law adoption, matter-coupling derivation, Einstein-equation
derivation, benchmark promotion, Gate Chair verdict, or completed derivation.

## Top-Level Object

The backlog file must be a YAML mapping with these required keys:

```yaml
schema_id: string
authority: "project_control"
status: string
created_at: timestamp-string
source_plan: object
scope: object
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
`implementations_plans/recommendations_implementation_plan_continue_task-v17.md`.
The `source_hash` must match the registered source row for that plan at the
time P0-T02 is executed.

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
  completed_derivation_authorized: false
```

`task_count` must equal the number of `### P*-T*` plan task headings in the
registered v17 plan. For the current v17 plan, that count is `57`.

`first_physics_bearing_task_after_p0` must be `P1-T01` unless a future Director
Decision Record explicitly supersedes this plan.

## Backlog Item

Every item in `items` must contain these fields:

```yaml
backlog_item:
  plan_task_id: string
  phase_id: string
  title: string
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
  project_system_boundary_authorized_by_plan: boolean
  implementation_status: string
  next_route_on_success: string
  next_route_on_failure: string
```

The v17 plan explicitly required the following fields. This schema preserves
them exactly and adds `route_type`, `project_system_boundary_authorized_by_plan`,
and `implementation_status` as control fields:

```yaml
required_by_plan:
  - plan_task_id
  - phase_id
  - title
  - depends_on
  - role_family
  - task_type
  - target_derivation_milestone
  - milestone_burden
  - expected_outputs
  - required_validators
  - physics_delta_allowed
  - promotion_allowed
  - next_route_on_success
  - next_route_on_failure
```

## Coverage Rules

1. Every `### P*-T*` heading in the registered v17 plan must appear exactly
   once as an `items[].plan_task_id`.
2. No backlog item may use a `plan_task_id` that is absent from the registered
   v17 plan.
3. `items[].depends_on` must reference only earlier backlog items unless a
   future Director Decision Record explicitly authorizes a non-linear
   dependency.
4. The dependency graph must be acyclic.
5. `P0-T01` must have no dependency.
6. `P0-T02` must depend on `P0-T01`.
7. `P0-T03` must depend on `P0-T02`.
8. `P1-T01` must depend on `P0-T03` and must be the first physics-bearing task
   after P0.

## Authority Rules

`promotion_allowed` must be `false` for every v17 backlog item unless a later
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
Distance-to-GR ledger movement, source-law adoption, coupling-law adoption,
matter-coupling derivation, benchmark promotion, proof authority, or completed
derivation.

## Validation Expectations

A valid P0-T02 completion must record at least these checks:

```yaml
minimum_checks:
  - "backlog YAML parses"
  - "backlog task count equals v17 plan task count"
  - "every v17 plan task appears exactly once"
  - "dependencies reference existing earlier tasks"
  - "dependencies are acyclic"
  - "P1-T01 is first physics-bearing task after P0"
  - "project-system tasks carry project_system_boundary_authorized_by_plan: true"
  - "promotion_allowed is false for every item"
```

The backlog validator may be an inline receipt in P0-T02, a task-local script,
or a future permanent validator. P0-T02 does not require permanent validator
installation.

## Forbidden Interpretations

The backlog must not be cited as evidence for:

- source-law adoption;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption;
- unrestricted `RR_E` theorem authority;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor construction;
- matter action import;
- Einstein-equation derivation;
- benchmark promotion;
- Gate Chair verdict;
- proof authority;
- completed derivation.

## Source Material

The AEther-Flow Research Project. (2026). *Recommendations implementation plan
continue task v17* [Internal implementation plan].
