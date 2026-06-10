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

Registered role versions are immutable in meaning. A role may narrow its scope
through a one-job AgentJob overlay, but the overlay cannot expand authority,
bypass validators, or promote claims.
