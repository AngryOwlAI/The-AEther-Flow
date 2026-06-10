---
schema_id: "DIRECTOR_DECISION_SCHEMA"
version: "0.1.0"
status: "active"
---

# Director Decision Schema

Director Decision Records are Markdown files with strict frontmatter. The
frontmatter carries machine-checkable fields; the body records reasoning.

## Required Frontmatter Fields

- `decision_id`
- `task_id`
- `director_version`
- `decision_type`
- `selected_role_id`
- `selected_role_version`
- `agent_job_id`
- `status`
- `supersedes_decision_id`
- `requires_human_gate`
- `role_fit_candidates`

## Required Body Sections

- `## Current Objective`
- `## Authority Surfaces Read`
- `## Role-Fit Matrix`
- `## Selected Role`
- `## Claim Boundary`
- `## Validation`

Use a new DDR to supersede an activated DDR. Do not rewrite activated decisions.
