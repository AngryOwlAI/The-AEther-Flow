---
name: improve-project-system
description: Resolve tracked project-system improvement state and set up or execute one bounded AgentJob per invocation.
---

# Improve Project System

Use this skill when improving the research system itself: roles, schemas,
validators, project-control docs, memory tooling, trigger logic,
generated-document pipelines, and operational reliability.

Do not use this skill for physics derivation, scientific claim promotion, or
Gate Chair decisions.

## Control Principle

Project-system improvement follows the same bounded transaction discipline as
research continuation. One invocation may resolve state, select one bounded
AgentJob, execute that AgentJob, or report a stop condition. It must not become
an open-ended repository rewrite.

## Workflow

1. Read `AGENTS.md`, `research_control/AGENTS.md`, relevant registries, and
   `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`.
2. Classify current Git changes:

   ```zsh
   .venv/bin/python scripts/project_control/classify_project_changes.py --json
   ```

3. Resolve the next project-system boundary:

   ```zsh
   .venv/bin/python scripts/project_control/resolve_project_improvement.py --json
   ```

4. If no action is needed, write or report a no-op rationale.
5. If documentation drift is detected, create or reuse one
   Documentation Curator AgentJob.
6. If system-design or validation drift is detected, create or reuse one
   Project-System Director, Validator Engineer, or Memory-System Maintainer
   AgentJob.
7. Execute at most one bounded AgentJob. Update only paths in the AgentJob
   allowlist.
8. Write `research_control/tasks/<task_id>/documentation_impact.yaml` for any
   state-changing project-system AgentJob.
9. Regenerate and validate:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
   .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
   .venv/bin/python scripts/project_control/validate_documentation_impact.py
   .venv/bin/python scripts/research_control/validate_research_control.py
   .venv/bin/python scripts/research_control/validate_research_control.py --check-diff
   ```

10. Checkpoint only if the transaction is valid and non-empty. Pass `--job-id`
    when checkpointing a project-system AgentJob that is not the active physics
    research task.

## Stop Conditions

- Required action would edit canonical ontology TeX, benchmark sources, science
  drafts, generated HTML, generated wiki notes, PDFs, or generated registry
  sidecars by hand.
- Required write path is outside the AgentJob allowlist.
- Documentation impact is required but neither source documentation nor a
  no-op rationale exists.
- The change requires a human policy decision.
- Validation fails.
