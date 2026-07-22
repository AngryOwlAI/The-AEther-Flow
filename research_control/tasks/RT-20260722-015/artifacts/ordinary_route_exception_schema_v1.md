<!-- authority: control -->

# Ordinary-route exception receipt schema v1

```yaml
schema_id: "ordinary_route_exception_schema_v1"
receipt_schema_id: "ordinary_route_exception_receipt_v1"
control_failure_schema_id: "ordinary_route_control_failure_v1"
policy_id: "ordinary_route_guard_policy_v1"
authority_status: "project_control_only"
```

## Exception receipt

```yaml
active: true
schema_id: "ordinary_route_exception_receipt_v1"
exception_id: "stable identifier"
exception_class: "all_ready_science_blocked"
ordinary_handoff_id: "handoff-0000"
ready_science_plan_task_ids:
  - "P0-T00"
blocked_routes:
  - plan_task_id: "P0-T00"
    failure_class: "claim_boundary_hard_failure"
    evidence_path: "research_control/tasks/RT-YYYYMMDD-NNN/artifacts/blocker.yaml"
    evidence_sha256: "lowercase sha256"
authority_limits:
  ordinary_research_handoff_authoritative: true
  project_system_sidecar_supersedes: false
  system_success_counts_as_physics: false
  system_success_counts_as_distance_to_gr: false
  scientific_status_changed: false
  physics_promotion_authorized: false
```

`ready_science_plan_task_ids` must equal the independently derived complete
ordered ready-science set. `blocked_routes` must contain exactly one matching
entry for each ID and no other entries. An empty ready set may support an
exception, but it does not create physics credit.

## Non-human control-failure evidence

For `failing_ci`, `registry_corruption`, `claim_boundary_hard_failure`, and
`security_or_integrity_repair`, the hash-bound evidence file contains:

```yaml
schema_id: "ordinary_route_control_failure_v1"
failure_id: "stable identifier"
plan_task_id: "P0-T00"
failure_class: "claim_boundary_hard_failure"
status: "active_blocking"
blocks_scientific_execution: true
observed_at: "RFC3339 timestamp"
failure_summary: "exact control failure"
remediation_route: "bounded repair task"
authority_limits:
  scientific_status_changed: false
  physics_promotion_authorized: false
```

The evidence record is a control receipt, not proof that a scientific route
would otherwise succeed. Once the failure is no longer active, a later
handoff cannot reuse it.

## Human-gate evidence

For `human_gate_required`, the evidence path is exactly
`research_control/design/v21_recommendation_backlog.yaml` at its current
tracked SHA-256, and the named ready item must set `requires_human_gate: true`.
The relay cannot fabricate or infer human authorization.

## Rejection rules

Reject a receipt when any ready science task is absent; an ID is duplicated;
the failure class is outside the closed vocabulary; the evidence is missing,
symlinked, untracked, outside the repository, under `.local/`, stale, or
malformed; the task or failure class differs; the failure is not active and
blocking; a nominal human-gated route lacks protected authority; or a
project-system sidecar is presented as ordinary route authority.

A passing exception changes no scientific claim or protected authority and
does not count toward the physics budget or Distance-to-GR.
