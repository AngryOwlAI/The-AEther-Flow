---
name: improve-project-system
description: Resolve tracked project-system improvement state from a project-system reliability and governance perspective and set up or execute one bounded AgentJob per invocation.
---

# Improve Project System

Use this skill when improving the research system itself: roles, schemas,
validators, control-marked project markdown, memory tooling, trigger logic,
generated-document pipelines, and operational reliability.

Do not use this skill for physics derivation, scientific claim promotion, or
Gate Chair decisions.

## Perspective

improve-project-system is best understood as a project-system reliability and
governance perspective. It is closest to system engineer plus software
engineer plus process auditor.

This perspective definition is descriptive orientation only. It does not
create role authority, change role semantics, expand write permissions, alter
validators or routing, or authorize scientific claim promotion.

## Control Principle

Project-system improvement follows the same bounded transaction discipline as
research continuation. One invocation may resolve state, select one bounded
AgentJob, execute that AgentJob, or report a stop condition. It must not become
an open-ended repository rewrite.

## Workflow

1. Read `AGENTS.md`, `research_control/AGENTS.md`, relevant registries,
   `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`, and
   `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`.

   Before classifying, routing, or creating an AgentJob, run the memory
   preflight:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
   ```

   Then run at least one targeted memory query:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup <object-id-or-path> --json
   .venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "<targeted phrase>" --limit 10 --json
   ```

   Use memory hits only as navigation. After any hit that influences a
   project-system decision, inspect the canonical source file or source
   registry row named by the hit. New AgentJobs and completions created after
   `2026-06-18T15:33:00Z` must include a `memory_preflight` receipt with the
   status command, status summary, query commands, returned object IDs,
   canonical source inspections, source registries, canonical paths, and source
   hashes. Obsidian, wiki notes, semantic extracts, and `.local/` remain
   retrieval layers only; they are not authority.
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
   If resolver output selects an `improve-project-handoff_*.yaml` sidecar, use
   that sidecar as the local implementation context for the selected signal.
   A sidecar with `solution_plan.status: "ready_to_implement"` may route one
   bounded AgentJob to the named implementation role only when the plan fits
   role authority and write-path allowlists. A sidecar without an executable
   solution plan routes one bounded Project-System Director step to convert the
   issue inventory into a concrete AgentJob or to reject the signal with an
   evidence-bearing decision.

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
6. If explanatory documentation drift is detected, create or reuse one
   Documentation Curator AgentJob.
7. If skill contracts, role contracts, schema contracts, control registries, or
   control-marked mixed Markdown drift, create or reuse one Project-Control
   Maintainer AgentJob.
8. If system-design or validation drift is detected, create or reuse one
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
   A project-system AgentJob resolving a sidecar must list all sidecar-resolved
   signal IDs in `resolved_project_improvement_signals`; when more than one
   signal is closed, the completion must include a nonblank
   `coherent_resolution_summary`.
9. Execute at most one bounded AgentJob. Update only paths in the AgentJob
   allowlist.
10. Write `research_control/tasks/<task_id>/documentation_impact.yaml` for any
   state-changing project-system AgentJob. Source-doc-only handling is valid
   only for plain documentation edits outside a project-system AgentJob. The
   record must mechanically cover live source changes, generated derivatives,
   classifier reason codes, and required validators.
11. Regenerate and validate by resolving the named obligations in
    `research_control/design/validation_obligation_resolution_policy_v1.md`:
    `memory_sync`, `memory_core`, `project_improvement_signals`,
    `documentation_impact`, `research_control_diff`, the task-selected test
    shard, and `git_diff_check`. Under the registered same-scope predicates,
    `research_control_diff` may also satisfy `research_control_core` and
    `claim_language_changed`; working-tree evidence never satisfies a staged
    obligation. Use the policy's single current compatibility recipe per gate.
    Direct precheckpoint commands are editing aids and do not become separate
    executions merely because both a skill and a role name the same obligation.
    Governed checkpoint convergence uses write-only `memory_sync()` passes,
    retains the required second sync after a targeted PDF build, and runs one
    blocking `memory_core` validation against the final staged Git tree.

12. Checkpoint only if the transaction is valid and non-empty. The checkpoint
    owns the `checkpoint_transaction` obligation and final staged acceptance.
    Pass `--job-id` when checkpointing a project-system AgentJob that is not the
    active physics research task. Checkpoint blocking is defined by validators, not by
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

## Validation Profile Wrapper

Select validation through the shared profile planner instead of copying gate
command chains into this skill:

```zsh
.venv/bin/python -m scripts.validation.cli run --profile <fast|affected|full> --paths <changed-path>
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py --job-id <agent-job-id>
.venv/bin/python -m scripts.validation.cli plan --profile doctor --scope local_retrieval --explain
```

Use `fast` for the cheapest local edit loop, `affected` for bounded
precheckpoint feedback, `checkpoint` only through the governed final
state-changing transaction, `full` only for explicit exhaustive or scheduled
coverage, and `doctor` only for local or advisory diagnostics. During the
`planner_authoritative` epoch, `run` executes the manifest-selected gates and
emits the authoritative operational receipt. The explicit
`validate-project-control-legacy` Make target and checkpoint
`--legacy-validation` switch remain rollback controls. A plan alone is not
validation evidence, and no profile replaces a human gate, role boundary,
source inspection, or final staged checkpoint.

Memory preflight, targeted memory queries, canonical source inspection,
change classification, signal resolution, and signal validation remain
distinct routing prerequisites; do not count them as profile acceptance.
Resolve selected obligations through the current shared executor or
compatibility surface authorized by the AgentJob, never through a skill-local
reconstructed command chain. Consume results under
`research_control/design/agent_validation_output_consumption_policy_v1.md`:
record the profile, selected gate IDs, status, compact receipt path and hash,
counts, and tree identity; expand only the relevant failed or warning finding
group.

## Validation-Output Consumption

Follow
`research_control/design/agent_validation_output_consumption_policy_v1.md`.
Read the compact summary first. A PASS needs no receipt expansion unless an
audit contract requires it. For a non-PASS result, inspect only the relevant
failed or warning gate group, finding IDs, or a bounded receipt section or
tail; do not ingest or retransmit an entire full receipt by default. Do not
repeatedly poll when that would return unchanged output.

Completion evidence records the gate ID, status, receipt path, content hash,
counts, tree fingerprint when available, and relevant finding IDs. Full
receipts under `.local/validation-receipts` remain untracked and
non-authoritative; they do not become scientific or project-control authority.

## Stop Conditions

- Required action would edit canonical ontology TeX, benchmark sources, science
  drafts, generated HTML, generated wiki notes, PDFs, or generated registry
  sidecars by hand.
- Required write path is outside the AgentJob allowlist.
- A Documentation Curator job would alter a control-marked mixed-document
  section, skill contract, role contract, schema contract, validator requirement,
  workflow command, routing behavior, permission, stop condition, or checkpoint
  gate.
- A Project-Control Maintainer job would alter an explanatory-only section
  without a task overlay that explicitly grants `explanatory_markdown`
  permission.
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
