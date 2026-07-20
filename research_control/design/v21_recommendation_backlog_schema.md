<!-- authority: control -->

# V21 Recommendation Backlog Schema

```yaml
schema_id: "v21_recommendation_backlog_schema_v1"
schema_for: "research_control/design/v21_recommendation_backlog.yaml"
authority_status: "project_control"
source_plan: "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
source_plan_sha256: "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087"
created_at: "2026-07-20T18:41:34Z"
scientific_claims_changed: false
distance_to_gr_delta_changed: false
physics_promotion_authorized: false
proof_authority: false
```

## Purpose and authority

This schema defines the machine-readable backlog and dependency graph required
by v21 `P0-T02`. The backlog is project-control routing data derived from the
registered immutable v21 plan. It does not execute a downstream task, supply a
human decision, change scientific claims, alter either scientific ledger,
supersede `handoff-0772`, or authorize validation output as physics proof.

The registered plan remains the authored dependency source. The backlog is a
validated machine-readable representation. Runtime skills, tracked
research-control state, current source authority, validators, checkpoints, and
protected human gates continue to govern every future packet.

## Top-level object

The YAML document requires these keys:

```yaml
schema_id: "v21_recommendation_backlog_v1"
authority: "project_control"
status: "draft_control_backlog"
created_at: timestamp-string
source_plan: source_plan
source_evidence: source_evidence
scope: scope
terminal_outcome_vocabulary: terminal_outcome_vocabulary
recommendation_coverage_rules: recommendation_coverage_rules
recommendation_coverage_matrix: recommendation_coverage_matrix
dependency_graph: dependency_graph
human_gate_summary: human_gate_summary
items: list[backlog_item]
```

`source_plan` records the exact registered plan ID, repo-relative path, object
ID, and SHA-256. `source_evidence` records the P0-T01 completion, registration
report, current control handoff, and preserved scientific handoff used by this
materialization. `scope` records the immutable multi-step boundary and the
non-authority fields.

## Backlog item

Every `P0-T01` through `P16-T06` task appears exactly once. Each item contains:

```yaml
plan_task_id: string
phase_id: string
work_kind: string
task_class: string
title: string
recommendation_ids: nonempty-list[string]
role_family: string
controlling_launcher: "continue-research-goal@v4"
worker_skill: "continue-research | improve-project-system | none_until_human_authorization"
route_label: string
target_derivation_milestone: string
milestone_burden: string
expected_result_kind: string
depends_on: list[plan-task-id]
max_worker_invocations_per_generation: 1
max_outer_agentjobs_per_generation: 1
requires_human_gate: boolean
dependency_independent_after_other_human_gates: boolean
allow_scope_expansion: false
physics_promotion_authorized_by_plan: false
proof_authority_created_by_plan: false
exact_objective: string
source_boundaries: nonempty-list[string]
write_boundaries: nonempty-list[string]
implementation_actions: nonempty-list[string]
required_artifacts: nonempty-list[string]
validator_obligations: nonempty-list[string]
completion_criteria: nonempty-list[string]
rollback_and_stop_rules: nonempty-list[string]
next_task_rules: nonempty-list[string]
human_intervention_boundary:
  requires_human_gate: boolean
  protected_or_external_conditions: list[string]
  relay_may_supply_human_authority: false
recommendation_coverage_role: "support | direct_implementation | final_coverage_audit | final_goal_disposition"
implementation_status: "completed | pending | blocked | precise_obstruction | frozen | superseded | conditionally_not_required | deferred_human_gate"
scientific_claims_changed: false
distance_to_gr_delta_changed: false
physics_promotion_authorized: false
proof_authority: false
```

The source, write, action, artifact, validation, completion, stop, and handoff
lists are normalized from the corresponding authored subsections without
creating new authority. A planned write path is data only; it is not an
allowlist for a future AgentJob.

## Dependency graph

`dependency_graph` contains the root task, node and edge counts, explicit
directed edges, and a deterministic topological order. Validation rejects:

- duplicate or missing work-item IDs;
- a dangling dependency;
- a cycle;
- a required item unreachable from `P0-T01`;
- stored counts or order inconsistent with item dependencies; or
- any task-field mismatch against the registered plan.

Human-gated items remain explicit. A `deferred_human_gate` status does not
satisfy a dependent task, while a dependency-independent included item may
continue only when current tracked authority and the immutable goal scope both
permit it.

## Recommendation coverage

- The expected set is exactly `V21-R01` through `V21-R72`.
- Every recommendation must have at least one direct implementation task.
- `P16-T01` must carry all 72 recommendations as the final coverage audit.
- `P16-T06` must carry all 72 recommendations as the final goal disposition.
- Support, direct implementation, final audit, and final disposition mappings
  remain distinct.

Recommendation coverage is traceability evidence. It is not implementation
evidence for a pending task and is not scientific proof.

## Role, worker, and authority rules

- A versioned role must match an active registered role.
- A bare role ID must have an active registered version, except a protected
  human-gated role may use a registered `status_defined` record.
- `worker_skill` must preserve the exact plan value.
- Every task permits at most one worker invocation and one outer AgentJob per
  generation.
- `allow_scope_expansion`, physics promotion, and proof authority remain false.
- A relay never supplies protected human authority.

## Deterministic validation

Run:

```zsh
.venv/bin/python research_control/tasks/RT-20260720-005/artifacts/validate_v21_backlog.py --write --json
```

The validator reparses every canonical v21 task block, materializes the
backlog, checks exact plan-field parity, validates graph reachability and
acyclicity, checks recommendation and role coverage, preserves human-gate and
worker boundaries, and writes the compact report to
`research_control/tasks/RT-20260720-005/artifacts/v21_backlog_dependency_report.json`.

The backlog may be regenerated deterministically only from the exact registered
plan. Later semantic changes require a tracked plan amendment or superseding
decision; generated derivatives must be refreshed through the governed memory
workflow.
