<!-- authority: control -->

# V20 Recommendation Backlog Schema

```yaml
schema_id: "v20_recommendation_backlog_schema_v1"
schema_for: "research_control/tasks/RT-20260718-011/artifacts/v20_recommendation_backlog.yaml"
authority_status: "project_control"
source_plan: "implementations_plans/recommendations_implementation_plan_continue_task-v20.md"
created_at: "2026-07-18T20:18:11Z"
scientific_claims_changed: false
distance_to_gr_delta_changed: false
physics_promotion_authorized: false
proof_authority: false
```

## Purpose and authority

This schema defines the typed backlog and dependency DAG required by v20
`P0-T02`. The backlog is project-control routing data. It records future task
boundaries but does not execute them, supply human authority, supersede
`handoff-0740`, change `program_state.yaml`, alter scientific claims, or
authorize validation output as physics proof.

## Top-level object

The YAML backlog requires:

```yaml
schema_id: "v20_recommendation_backlog_v1"
authority: "project_control"
status: string
created_at: timestamp-string
source_plan: source_plan
scope: scope
terminal_outcome_vocabulary: terminal_outcome_vocabulary
recommendation_coverage_rules: recommendation_coverage_rules
recommendation_coverage_matrix: map[recommendation-id, coverage-entry]
dependency_graph: dependency_graph
items: list[backlog_item]
```

`source_plan` records the canonical plan path, object ID, and SHA-256 hash.
`scope` fixes one live continuation, one outer AgentJob per generation, no
cross-task relay reuse, and the no-physics-authority boundary.

## Backlog item

Every v20 task appears exactly once. Each item records:

```yaml
plan_task_id: string
phase_id: string
title: string
task_kind: string
recommendation_ids: nonempty-list[string]
expected_role_families: nonempty-list[registered-role-id-at-version]
depends_on: list[plan-task-id]
conditional_task: boolean
requires_human_gate: boolean
state_changing_expected: boolean
target_derivation_milestone: string
milestone_burden: string
relay_boundary:
  controlling_launcher: "continue-research-goal"
  generation_worker: "continue-research-continue-goal"
  research_authority_per_generation: "continue-research"
  execution_profile: string
  goal_text: string
  goal_text_sha256: sha256
  max_continue_passes: positive-integer
  max_elapsed_minutes: positive-integer
  max_live_continuations: 1
  max_outer_agentjobs_per_generation: 1
  cross_task_relay_reuse: false
source_boundaries: nonempty-list[string]
write_boundaries: nonempty-list[string]
required_artifacts: nonempty-list[string]
implementation_actions: nonempty-list[string]
validator_obligations: nonempty-list[string]
completion_criteria: nonempty-list[string]
completion_record_contract: map
terminal_outcome_rules: map
rollback_and_stop_rules: nonempty-list[string]
human_intervention_boundary: map
next_task_rules: nonempty-list[string]
recommendation_coverage_role: "support | direct_implementation | final_coverage_audit"
implementation_status: "completed | pending | blocked | frozen | deferred | superseded | conditionally_not_required"
scientific_claims_changed: false
distance_to_gr_delta_changed: false
physics_promotion_authorized: false
proof_authority: false
```

The goal text and hash define one immutable relay boundary for that task. A
backlog row is not reusable authorization: every v20 task requires a new goal
record and a fresh generation worker discussion.

## Dependency and recommendation rules

- The expected task set is the 104 canonical `P0-T01` through `P16-T05` task
  cards parsed from the v20 plan.
- Every dependency must name a task in that set.
- The graph must be acyclic and every required task must be reachable from
  `P0-T01`.
- The expected recommendation set is exactly `V20-R01` through `V20-R21`.
- Every recommendation must have at least one direct implementation-task row.
- `P16-T03` must provide final-coverage-audit coverage for all 21
  recommendations.
- Every expected role family must be active in
  `registries/AGENT_ROLE_REGISTRY.csv`.

## Human and terminal boundaries

Human or external action remains a precondition; the relay cannot manufacture
that authority. Each row records the task's human/external preconditions,
protected stop rules, completion criteria, permitted terminal vocabulary, and
next-task rule. `terminal_complete` is lawful only after all completion
criteria and required validators pass. Protected, failed, indeterminate,
repeated, dirty, or capability-blocked states retain their deterministic
non-success terminal disposition.

## Deterministic validation

Run:

```zsh
.venv/bin/python research_control/tasks/RT-20260718-011/artifacts/validate_v20_backlog.py --write --json
```

The validator reparses the canonical plan, regenerates the backlog, checks
exact task and relay-field parity, verifies source/write/validator/terminal
contracts, validates role registration, detects duplicate, dangling, cyclic,
or unreachable tasks, and writes the compact dependency and coverage report to
`research_control/tasks/RT-20260718-011/artifacts/v20_backlog_dependency_report.json`.

The deterministic `--write` operation is authorized only within this bounded
`P0-T02` transaction. Later changes require a new plan amendment or a tracked
superseding task; generated backlog data must not be hand-edited.
