---
schema_id: "EXECUTION_ROLE_SCHEMA"
version: "0.1.0"
status: "active"
---

# Execution Role Schema

Execution-role records bind one AgentJob to the exact role semantics used for
that job. They allow the Director of Research to use a registered role,
task-scoped overlay, or one-job provisional role without mutating base role
contracts.

## Required Fields

- `execution_role_ref`
- `role_execution_kind`
- `task_id`
- `agent_job_id`
- `authority_delta_summary`
- `allowed_write_paths`
- `requires_human_gate`
- `expires_after`

## Role Execution Kinds

- `registered_role`
- `task_overlay`
- `one_job_provisional_role`

## Shared Fields

- `execution_role_ref`: Stable reference used by DDRs, AgentJobs, registries,
  and commits.
- `role_execution_kind`: One of the allowed execution kinds.
- `task_id`: Task that owns the execution role.
- `agent_job_id`: AgentJob that may use the execution role.
- `authority_delta_summary`: Human-readable summary of role authority.
- `allowed_write_paths`: Explicit path allowlist inherited by the AgentJob.
- `requires_human_gate`: Lowercase boolean.
- `expires_after`: Job or event after which the execution role is not reusable.

## Overlay Fields

Task overlays must include:

- `base_role_id`
- `base_role_version`
- `added_constraints`
- `removed_permissions`
- `expanded_permissions`

Expanded permissions require `requires_human_gate: true`.

## Provisional Role Fields

One-job provisional roles must include:

- `provisional_role_name`
- `justification`
- `non_reusable_until_registered: true`

Provisional roles expire after their owning AgentJob and are not reusable until
registered as a versioned base role.

## Registered Role Fields

Registered-role records must include:

- `base_role_id`
- `base_role_version`

They may not silently add permissions. Any task-specific adaptation must use a
`task_overlay` record instead.
