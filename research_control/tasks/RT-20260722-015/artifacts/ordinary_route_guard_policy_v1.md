<!-- authority: control -->

# Ordinary-route guard policy v1

```yaml
schema_id: "ordinary_route_guard_policy_v1"
policy_id: "ordinary_route_guard_policy_v1"
implements_plan_task_id: "P12-T04"
effective_after: "2026-07-22T19:00:53Z"
threshold: 3
warning_at: 2
enforcement: "prospective_hard_failure"
authority_status: "project_control_only"
historical_missing_record_status: "legacy_readable"
scientific_claims_changed: false
distance_to_gr_delta_changed: false
physics_promotion_authorized: false
proof_authority: false
```

## Purpose

This policy prevents an indefinite run of project-system work from displacing
dependency-ready scientific work. It turns the earlier advisory ratio into a
prospective routing gate without turning system work, route selection, or a
validator result into scientific payload.

The P12-T04 implementation job at the exact activation instant is exempt.
Every later ordinary research handoff and AgentJob is governed. Historical
records remain readable and are not rewritten.

## Normalized consecutive-run counter

The evaluator sorts completed AgentJobs at or before the handoff timestamp and
walks backward through the trailing run. A task counts as project-system only
when its normalized explicit taxonomy scope is `project_system` and its
physics-payload admission is not `physics`. A dual-budget category of
`physics_bearing` or `mixed` terminates the run. System, support, validation,
documentation, checkpoint, and route-selection receipts never count as
physics.

At two consecutive project-system tasks the evaluator emits the advisory
`ordinary_route_guard_threshold_next`. At three or more, the ordinary
handoff must select a dependency-ready science task from the recommendation
plan named by `selected_next_route.plan_id`.

## Dependency-ready science set

The evaluator resolves the registered backlog from the explicit plan ID and
reads the research task registry as of the handoff timestamp. Completed work
items are represented as `(plan_id, plan_task_id)` pairs, because package IDs
are local to each recommendation plan. A V21 completion therefore cannot
satisfy a colliding V22 dependency. Historical V21 records retain their exact
V21 inference rules; newer plans require an explicit plan identity and treat a
`repair_required` task as incomplete until a qualifying superseding task is
recorded. A completed work item also establishes transitive dependencies only
inside the same plan. A science item is ready only when every same-plan
dependency is satisfied and the item is not already completed.

The handoff records the exact ordered ready-science list. The validator derives
that list independently at the handoff timestamp and rejects omissions,
insertions, or reordering.

## Ordinary research handoff contract

A governed handoff contains:

```yaml
ordinary_route_guard:
  schema_id: "ordinary_route_guard_evaluation_v1"
  policy_id: "ordinary_route_guard_policy_v1"
  evaluation_id: "stable identifier"
  ordinary_handoff_id: "handoff-0000"
  threshold: 3
  consecutive_project_system_tasks_before_selection: 3
  selected_plan_id: "recommendations_implementation_plan_continue_task-v22"
  ready_science_plan_task_ids: ["P0-T00"]
  ready_science_plan_task_refs:
    - "recommendations_implementation_plan_continue_task-v22:P0-T00"
  selected_plan_task_id: "P0-T00"
  selected_route_class: "physics_bearing"
  selected_worker_skill: "continue-research"
  outcome: "physics_bearing_route_selected"
  ordinary_research_handoff_authoritative: true
  project_system_sidecar_supersedes: false
  exception_receipt:
    active: false
  authority_limits:
    ordinary_research_handoff_authoritative: true
    project_system_sidecar_supersedes: false
    system_success_counts_as_physics: false
    system_success_counts_as_distance_to_gr: false
    scientific_status_changed: false
    physics_promotion_authorized: false
```

The selected plan ID, plan task, and worker skill must match the backlog
resolved from the handoff's `selected_next_route`. V21 records that predate
plan namespaces default to the registered V21 plan for compatibility. A
human-gated science task is not executable without the protected authority and
cannot be used as a nominal physics route to evade the guard.

## Lawful exception

A project-system selection at or above the threshold is lawful only when an
`ordinary_route_exception_receipt_v1` accounts for every ready science task.
Each route must have exactly one active blocking class:

- `failing_ci`
- `registry_corruption`
- `claim_boundary_hard_failure`
- `human_gate_required`
- `security_or_integrity_repair`

The evidence path must be repository-relative, regular, tracked, outside
`.local/`, and bound to its exact SHA-256. `human_gate_required` is checked
directly against the selected plan's backlog and its exact hash. Other classes require an
active `ordinary_route_control_failure_v1` record matching the same plan task
and failure class. Partial, stale, untracked, malformed, or duplicate evidence
hard-fails.

An exception authorizes only the selected repair route. It does not recast the
repair as physics, discharge a derivation burden, establish theorem truth,
modify ontology, create Gate Chair authority, or promote any claim.

## Admission and authority

Each later AgentJob binds to the tracked regular ordinary handoff at its exact
hash through `ordinary_route_guard_admission_v1`. The job's plan ID and plan
task must be the handoff selection. Project-improvement handoff sidecars remain
separate signal-routing artifacts and cannot supersede the ordinary research
handoff.

One fail-closed atomic checkpoint-recovery branch may consume an immediately
preceding untracked handoff only when the prior transaction was completed but
could not be staged, the handoff, pending completion, and active blocker are
all repository candidates bound to exact identities and hashes, and the repair
job allowlists those prior paths for the same governed checkpoint. That branch
uses `ordinary_route_checkpoint_recovery_v1`; it does not permit a plan or task
mismatch and does not weaken the ordinary tracked-handoff rule for normal
jobs.

The sole mismatch branch is
`protected_human_route_override_admission_v1`. It requires a deterministic
task-local receipt that hash-binds the admitted and protected jobs, the exact
plan task and ordinary source handoff, a one-time consumed repository approval,
the matching Director decision, the consumed human-authorization artifact, and
the immutable recursive-goal route identity. A separately routed checkpoint
recovery must use the immediate next generation through
`improve-project-system`, bind the exact blocker and strategy, and prove that it
does not reuse the protected approval.

Jobs created after `2026-07-24T16:00:00Z` must name the deterministic receipt
path and SHA-256 inside `override_authority`. Final staged validation requires
all bound records in the Git index. Missing, ignored, symlinked, stale,
mismatched, broadened, unconsumed, reused, or non-immediate chains fail. Jobs
without this exact receipt remain under the ordinary handoff-equality rule.

This entire policy is project-control evidence only. A passing route guard
does not imply scientific quality, correctness, ontology adoption, physical
interpretation, Distance-to-GR progress, proof authority, publication, or a
completed derivation.
