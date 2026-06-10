---
schema_id: "EXECUTION_ROLE_SCHEMA"
version: "0.1.0"
status: "active"
---

# Execution Role Schema

Execution-role records bind one AgentJob to the exact role semantics used for
that job. Registered role contracts are stable templates and guidance for the
Director of Research; the execution-role record is the task-local authority
contract that decides how that template, overlay, or provisional role is used.

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

Use `registered_role` only when the registered role fits directly and no
authority delta is needed. Use `task_overlay` when the selected role remains a
registered role but needs task-specific constraints, removed permissions, or a
bounded non-promotional authority adjustment. Use
`one_job_provisional_role` when no registered role fits, or when a
template-derived modification needs a distinct one-job identity.

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

Non-protected bounded expansions may remain one-job scoped when the AgentJob
claim boundary and write-path allowlist keep them non-promotional. Protected
expansion requires a human gate. Protected expansion includes claim promotion,
canonical ontology authority, benchmark-status authority, Gate Chair authority,
or permanent role registration.

## Provisional Role Fields

One-job provisional roles must include:

- `provisional_role_name`
- `justification`
- `non_reusable_until_registered: true`

Provisional roles expire after their owning AgentJob and are not reusable until
registered as a versioned base role.

Provisional roles may either leave `base_role_id` and `base_role_version` blank
for a brand-new one-job role, or cite a registered role as a template lineage.
When cited, the base role id and version must match `AGENT_ROLE_REGISTRY.csv`.
If the same provisional role pattern recurs three times, the project-system
improvement loop must surface a role-registration review signal.

## Registered Role Fields

Registered-role records must include:

- `base_role_id`
- `base_role_version`

They may not silently add permissions. Prospective task-specific adaptation
should use a `task_overlay` or `one_job_provisional_role` record instead.
