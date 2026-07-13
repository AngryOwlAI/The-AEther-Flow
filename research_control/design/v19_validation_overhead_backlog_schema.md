<!-- authority: control -->

# V19 Validation-Overhead Backlog Schema

```yaml
schema_id: "v19_validation_overhead_backlog_schema_v1"
schema_for: "research_control/design/v19_validation_overhead_backlog.yaml"
authority_status: "project_control"
source_plan: "implementations_plans/recommendations_implementation_plan_continue_task-v19.md"
created_at: "2026-07-12T21:03:24Z"
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
```

## Purpose

This schema defines the machine-readable backlog and dependency graph required
by v19 P0-T02. The backlog is project-control routing data. It does not execute
any downstream task, modify scientific claims, change Distance-to-GR status,
supersede `handoff-0740`, or authorize validation output as physics proof.

## Top-level object

The YAML document requires these keys:

```yaml
schema_id: "v19_validation_overhead_backlog_v1"
authority: "project_control"
status: string
created_at: timestamp-string
source_plan: source_plan
scope: scope
recommendation_coverage_rules: recommendation_coverage_rules
dependency_graph: dependency_graph
items: list[backlog_item]
```

`source_plan` records the plan ID, repo-relative path, registered object ID,
and SHA-256 source hash. `scope` fixes one bounded AgentJob per plan task and
records the no-physics-authority and ordinary-research-route boundaries.

## Backlog item

Every P0 through P12 task appears exactly once and requires:

```yaml
plan_task_id: string
phase_id: string
task_type: string
title: string
recommendation_ids: nonempty-list[string]
role_family: registered-role-id-at-version
controlling_skill: "improve-project-system | continue-research"
migration_epoch: "legacy | legacy_consolidated | shadow_planner | planner_authoritative | legacy_retired"
depends_on: list[plan-task-id]
max_agentjobs_per_invocation: 1
requires_human_gate: boolean
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
expected_source_changes: nonempty-list[string]
expected_generated_changes: nonempty-list[string]
required_gates: nonempty-list[string]
validation_obligations: nonempty-list[string]
performance_evidence:
  before_reference: repo-relative-path
  required_metrics: nonempty-list[string]
  task_specific_requirements: list[string]
rollback_triggers: nonempty-list[string]
next_route_on_success: string
next_route_on_repair: string
next_route_on_blocked: string
recommendation_coverage_role: "support | direct_implementation | final_coverage_audit"
implementation_status: "completed | pending | blocked | superseded | conditionally_not_required"
```

The expected-change lists are plan boundaries, not authorization to perform the
changes early. `policy_required_registry_memory_wiki_derivatives` means only
the derivatives required by repository policy for the task's actual source
changes.

## Dependency graph

`dependency_graph` contains the root task, node and edge counts, explicit
directed edges, and a deterministic topological order. Validation must reject
duplicate IDs, dangling dependencies, cycles, an orphan not reachable from
`P0-T01`, or a stored order inconsistent with the item dependencies.

## Recommendation and role rules

- The expected recommendation set is exactly `V19-R01` through `V19-R48`.
- Every recommendation must occur in at least one `direct_implementation` task.
- `P12-T06` must contain every recommendation as `final_coverage_audit`.
- Every `role_family` must name an active row in
  `registries/AGENT_ROLE_REGISTRY.csv`.
- Conditional tasks remain explicit with a status or later tracked
  supersession; they are not silently removed.

## Deterministic validation

Run:

```zsh
.venv/bin/python research_control/tasks/RT-20260712-002/artifacts/validate_v19_backlog.py
```

The validator reparses the canonical v19 task blocks, checks exact plan-field
parity, validates graph reachability and acyclicity, checks recommendation and
role coverage, enforces the no-physics-authority fields, and writes the compact
report to
`research_control/tasks/RT-20260712-002/artifacts/v19_backlog_validation_report.json`.

The backlog may be regenerated deterministically only during this P0-T02 packet
with `--write`. Later changes require a bounded plan amendment or a tracked
superseding decision.
