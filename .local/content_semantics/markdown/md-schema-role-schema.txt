---
schema_id: "ROLE_SCHEMA"
version: "0.1.0"
status: "active"
---

# Role Schema

Role contracts are Markdown files with strict frontmatter and a short body.
The registry row and frontmatter must agree.

## Required Frontmatter Fields

- `role_id`
- `version`
- `role_name`
- `role_kind`
- `authority_level`
- `status`
- `may_execute_autonomously`
- `may_create_outputs`
- `may_modify_sources`
- `may_promote_claims`
- `requires_human_gate`
- `default_output_format`
- `default_validators`
- `allowed_source_classes`
- `forbidden_source_classes`

## Rules

Registered role versions are identified by the `(role_id, version)` pair and
are immutable in meaning. Multiple versions of the same `role_id` may remain
registered so historical execution records continue to validate while a newer
active version becomes the default template. The actual one-job execution
semantics are fixed by an execution-role record.

Task-specific modification belongs in `EXECUTION_ROLE_SCHEMA`:

- `registered_role` is direct template use.
- `task_overlay` modifies a registered role while preserving its identity.
- `one_job_provisional_role` creates a temporary one-job role, either brand-new
  or derived from a registered role template.

No execution-role path may bypass validators. Protected authority expansion
requires a human gate: claim promotion, canonical ontology authority,
benchmark-status authority, Gate Chair authority, or permanent role
registration.
