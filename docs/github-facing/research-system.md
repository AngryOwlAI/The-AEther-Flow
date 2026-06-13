<!-- authority: explanatory -->

# Research System

The research system is the governed workflow that turns a question, continuation state, or project-improvement need into bounded agent work with explicit evidence.

Authority boundary: this page explains the workflow at GitHub-reading depth. It does not authorize routing, change validator behavior, or make scientific claims.

## Two Entry Paths

- `continue-research`: physics continuation from tracked research-control state.
- `improve-project-system`: roles, validators, documentation systems, memory tooling, generated-doc pipelines, and operational reliability.

Both paths use the same discipline: inspect tracked state, choose one bounded job, constrain allowed paths, validate the result, and preserve completion evidence.

## Lifecycle

<!-- mermaid-diagram-id: github-facing-research-system -->
```mermaid
flowchart TD
  State["Tracked state and latest handoff"] --> Director["Director decision"]
  Director --> Job["Bounded AgentJob"]
  Job --> Role["Execution role or task overlay"]
  Role --> Outputs["Allowed outputs"]
  Outputs --> Validators["Validators and diff gates"]
  Validators --> Completion["Completion record"]
  Completion --> Handoff["Next handoff or recommendation"]
  Completion --> Registries["Registry updates"]
  Handoff --> State
```

## What an AgentJob Does

An AgentJob defines the executable boundary:

- Objective and selected role.
- Allowed read paths and write paths.
- Forbidden paths and forbidden authority surfaces.
- Expected outputs.
- Required validators.
- Completion record and claim boundary.

The one-job rule matters because the repository combines science, workflow machinery, generated artifacts, and memory systems. A small uncontrolled edit can otherwise blur physics authority, documentation authority, and project-control authority.

## Documentation and Project-System Changes

Documentation-impact handling is a receipt requirement. If project-system machinery changes, the transaction must explain whether source documentation was updated or why no update was required. The validator checks live changed paths, generated derivatives, classifier reason codes, and required validators.

## Source Basis

- [../../markdown/html-explainer-specs/research-agent-workflow-explainer.md](../../markdown/html-explainer-specs/research-agent-workflow-explainer.md)
- [../../markdown/html-explainer-specs/research-control-system-explainer.md](../../markdown/html-explainer-specs/research-control-system-explainer.md)
- [../../research_control/README.md](../../research_control/README.md)
- [../../.codex/skills/continue-research/SKILL.md](../../.codex/skills/continue-research/SKILL.md)
- [../../.codex/skills/improve-project-system/SKILL.md](../../.codex/skills/improve-project-system/SKILL.md)
- [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md)
