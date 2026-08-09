<!-- authority: control -->

# V22 Recommendation Backlog Schema

```yaml
schema_id: "v22_recommendation_backlog_schema_v1"
schema_for: "research_control/design/v22_recommendation_backlog.yaml"
authority_status: "project_control"
source_plan: "implementations_plans/recommendations_implementation_plan_continue_task-v22.md"
source_plan_sha256: "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65"
created_at: "2026-08-08T22:37:10Z"
scientific_claims_changed: false
distance_to_gr_delta_changed: false
physics_promotion_authorized: false
proof_authority: false
```

## Purpose and authority

This schema defines the compact machine-readable backlog required by V22
`P0-T03`. It is project-control routing data derived from the registered V22
draft/control plan. It does not launch a work package, satisfy a planned
dependency, adopt a source law or metric, supply protected authority, change a
Gate or benchmark status, or count as physics progress.

The authored plan and its embedded `V22_MACHINE_MANIFEST` remain the source of
the package IDs, recommendation mappings, sequence mappings, cross-cutting
directive mappings, dependencies, and conditional locks. Live tasks,
AgentJobs, handoffs, validators, checkpoints, and protected human decisions
continue to govern execution.

## Top-level contract

The YAML document contains:

```yaml
schema_id: "v22_recommendation_backlog_v1"
authority: "project_control"
status: "draft_control_backlog"
created_at: timestamp-string
source_plan: mapping
source_evidence: mapping
scope: mapping
coverage_rules: mapping
coverage_summary: mapping
conditional_rules: mapping
dependency_graph: mapping
items: list[work_package]
authority_limits: mapping
```

`source_plan` binds the plan ID, registered object ID, repository path, exact
SHA-256, predecessor, and review-basis hash. `source_evidence` binds the V21
terminal baseline manifest, reproduction receipt, freeze policy, P0-T02
completion, and `handoff-0968` at exact hashes.

## Work-package contract

Each of the 40 work packages appears exactly once:

```yaml
plan_task_id: string
phase_id: string
title: string
track: string
owner: string
declared_coverage_ids: list[string]
recommendation_ids: list[string]
sequence_step_ids: list[string]
cross_cutting_directive_ids: list[string]
depends_on: list[plan-task-id]
objective: string
actions: string
outputs: string
acceptance: string
verification: string
stop_conditions: string
implementation_status: string
requires_separate_agentjob: true
max_outer_agentjobs_per_invocation: 1
automatic_execution_authorized: false
scientific_claims_changed: false
distance_to_gr_delta_changed: false
physics_promotion_authorized: false
proof_authority: false
```

The prose fields are whitespace-normalized transcriptions of the authored
work-package sections. Planned actions and outputs are data, not write-path or
execution authority.

Before a package may be selected by the ordinary-route guard, its backlog item
also carries an explicit runtime-routing overlay:

```yaml
work_kind: string
task_class: "science" | "project_system"
role_family: registered-role-ref
controlling_launcher: string
worker_skill: "continue-research" | "improve-project-system"
route_label: string
target_derivation_milestone: string
milestone_burden: string
expected_result_kind: string
requires_human_gate: boolean
dependency_independent_after_other_human_gates: boolean
allow_scope_expansion: false
```

`RT-20260808-004` adds this overlay for the first eligible V22 successor,
`P1-T01`, while repairing plan-qualified route lookup. A future package must
receive and validate its own explicit overlay before selection; missing fields
are not inferred from a colliding local package ID in another plan.

## Coverage and dependency rules

- Recommendation IDs are exactly `V22-R01` through `V22-R19`.
- Sequence IDs are exactly `S1` through `S12`.
- Cross-cutting directive IDs are exactly `V22-X01` through `V22-X10`.
- Work-package IDs are exactly the 40 detailed headings and manifest keys.
- Every mapped package and dependency resolves to one work-package ID.
- The 61 dependency edges form an acyclic graph rooted at `P0-T01`.
- Every package is reachable and maps to at least one recommendation,
  sequence step, or cross-cutting directive.
- P5 stays locked behind a genuinely positive `P4-T05` Gate B verdict.
- P6-T02 stays locked behind a genuinely positive `P5-T03` Gate D verdict.
- At most one source-extension candidate family may be active.

Coverage is traceability, not implementation evidence. P0-T01 through P0-T03
may be marked complete or checkpoint-pending from exact tracked evidence; all
later packages remain pending or conditionally locked until separately routed.

## Deterministic validation

Run:

```zsh
.venv/bin/python research_control/tasks/RT-20260808-003/artifacts/validate_v22_plan_registration.py --write --json
```

The registration validator checks the exact review, plan, predecessor, terminal-baseline,
registry, ignore-rule, package, coverage, graph, conditional-lock, and
non-authority contracts. It writes the backlog, dependency graph, coverage
seed, source-hash receipt, registration report, validation receipt, and compact
receipt deterministically. The plan-namespace repair validator under
`RT-20260808-004` then validates the live P1-T01 routing overlay and the
plan-qualified guard contract without treating the earlier registration writer
as current mutation authority. Generated wiki and memory projections are
refreshed only through the approved project-memory bootstrap.
