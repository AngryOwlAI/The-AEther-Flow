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

1. Read `AGENTS.md`, `research_control/AGENTS.md`, relevant registries,
   `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`, and
   `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`.
2. Classify current Git changes:

   ```zsh
   .venv/bin/python scripts/project_control/classify_project_changes.py --json
   ```

3. Resolve the next project-system boundary:

   ```zsh
   .venv/bin/python scripts/project_control/resolve_project_improvement.py --json
   ```

   Resolver output is advisory routing state. It must not block checkpointing
   by itself; hard checkpoint gates are validator failures and concrete
   authority-boundary violations.

4. Validate emitted project-improvement signals against the canonical type and
   instance registries:

   ```zsh
   .venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
   ```

   Project-improvement signal detection is structural: completion and handoff
   YAML files are parsed for nonblank `project_improvement_signals` entries.
   Signal types must come from
   `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`; concrete emitted
   signals must be represented in
   `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`. Do not rely on
   free-text signal terms.
   The type registry owns allowed signal kinds and default routing metadata.
   Severity remains on the concrete signal instance so transaction context can
   distinguish low-risk drift from a hard invariant conflict.

5. If no action is needed, write or report a no-op rationale.
6. If documentation drift is detected, create or reuse one
   Documentation Curator AgentJob.
7. If system-design or validation drift is detected, create or reuse one
   Project-System Director, Validator Engineer, or Memory-System Maintainer
   AgentJob.
   Recurring provisional-role patterns are project-system signals, not silent
   drift. When the same `one_job_provisional_role` pattern appears three times
   by provisional role name plus base-role lineage, route one bounded
   Project-System Director review for possible human-authorized registration as
   a permanent role. Permanent registration must update the registered role
   contract and `AGENT_ROLE_REGISTRY.csv`; do not promote a provisional role by
   convention alone.
   Registered high/critical signals take priority over current Git-change
   routing; registered low/medium signals remain backlog unless no current
   project-system action is pending.
   Terminal signal statuses (`resolved`, `completed`, `closed`, or `rejected`)
   must include `resolved_by_job_id`, `resolution_evidence_path`, and
   `resolved_at` in `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`.
   For `resolved`, `completed`, and `closed`, the evidence path must be a
   completion YAML with `validation_status: "PASS"` and a matching `job_id`.
   For `rejected`, the evidence path may instead be a Director decision record
   that names the signal and explains the rejection.
   Do not duplicate validator command strings in signal rows; completion YAML
   owns command evidence through `command_results`.
   One bounded AgentJob may close multiple project-improvement signals only
   when its `objective` names every closed signal ID and its completion record
   lists the same IDs in `resolved_project_improvement_signals` with a
   nonblank `coherent_resolution_summary`. For shared closures, every signal
   row must use the resolving job's canonical `completion_path` from
   `registries/AGENT_JOB_REGISTRY.csv` as `resolution_evidence_path`.
8. Execute at most one bounded AgentJob. Update only paths in the AgentJob
   allowlist.
9. Write `research_control/tasks/<task_id>/documentation_impact.yaml` for any
   state-changing project-system AgentJob. Source-doc-only handling is valid
   only for plain documentation edits outside a project-system AgentJob. The
   record must mechanically cover live source changes, generated derivatives,
   classifier reason codes, and required validators.
10. Regenerate and validate:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
   .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
   .venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
   .venv/bin/python scripts/project_control/validate_documentation_impact.py
   .venv/bin/python scripts/research_control/validate_research_control.py
   .venv/bin/python scripts/research_control/validate_research_control.py --check-diff
   ```

11. Checkpoint only if the transaction is valid and non-empty. Pass `--job-id`
    when checkpointing a project-system AgentJob that is not the active physics
    research task. Checkpoint blocking is defined by validators, not by
    `resolve_project_improvement.py` reporting future work. Completion records
    do not need a fresh resolver snapshot merely because high or critical
    signals remain open; resolver snapshots are optional handoff context unless
    the AgentJob sets `resolves_signal_routing: true`. Routing-resolution
    completions must preserve repo-relative `resolver_snapshots.before` and
    `resolver_snapshots.after` paths to JSON output from
    `resolve_project_improvement.py --json` and include nonblank
    `routing_delta_summary`. The hard validator checks only summary presence
    and minimal resolver-shape fields: the advisory flags, checkpoint gate
    source, selected signal, open signals, and change classification. Ordinary
    validator and documentation jobs do not inherit that burden.

## Stop Conditions

- Required action would edit canonical ontology TeX, benchmark sources, science
  drafts, generated HTML, generated wiki notes, PDFs, or generated registry
  sidecars by hand.
- Required write path is outside the AgentJob allowlist.
- A completion or handoff emits a project-improvement signal whose type is not
  registered in `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv` or
  whose concrete signal row is absent from
  `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`.
- A project-improvement signal is marked `resolved`, `completed`, `closed`, or
  `rejected` without explicit resolution evidence.
- A `resolved`, `completed`, or `closed` signal lacks a matching PASS
  completion record, or a `rejected` signal lacks either a PASS completion
  record or explanatory Director decision record.
- Documentation impact is required but neither source documentation nor a
  no-op rationale exists.
- The change requires a human policy decision.
- Validation fails.
