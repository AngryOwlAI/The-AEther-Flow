<!-- authority: explanatory -->

# Role Contracts

This folder contains versioned role contracts for the research-agent system.
The contracts describe what a role may do, what it must not do, which source
classes it may read or write, and which validators normally apply.

## Folder Structure

- `physics/` contains roles that work on physics research packets, such as
  construction, refutation, formalization, auditing, selection, and gate
  review.
- `research_ops/` contains roles that operate the project system, such as
  Director routing, Documentation Curator work, memory maintenance, validation,
  process auditing, and project-control maintenance.

## What Belongs Here

- Versioned role contracts named with the pattern `<role-id>.v<version>.md`.
- Superseded role versions retained for historical execution records.
- Active role versions referenced by `registries/AGENT_ROLE_REGISTRY.csv`.

## What Does Not Belong Here

- Task-specific execution-role records. Those belong under
  `research_control/tasks/<task_id>/roles/`.
- AgentJob YAML files. Those belong under
  `research_control/tasks/<task_id>/jobs/`.
- Scientific derivations, candidate outputs, or ontology sources.

## Authority Boundary

Role contracts are project-control authority for agent behavior, but they do
not promote physics claims by themselves. Changing an active role contract's
mission, permissions, validators, stop conditions, or authority requires a new
version or a bounded project-control transaction. Use `.agents/AGENTS.md` for
the stricter editing rule.

