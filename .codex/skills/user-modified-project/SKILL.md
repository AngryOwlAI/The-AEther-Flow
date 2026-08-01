---
name: user-modified-project
description: Use when the human has manually changed project files and wants Codex to integrate those changes through the existing physics, AI-agent, registry, wiki, validation, and checkpoint gates without bypassing project authority.
---

# User-Modified Project

Use this skill when the user has manually edited repository files and wants the
changes integrated into Flow's controlled project system.

This skill is an integration router. It does not bypass `continue-research`,
`improve-project-system`, claim gates, registry authority, generated-surface
rules, or checkpoint validation.

## Required Human Intent

Before integrating changes, require or recover a brief human intent note:

- what changed;
- why it changed; and
- expected track: `physics`, `ai-agent/project-system`, `docs`, or `mixed`.

If the intent note is missing and the diff is ambiguous, stop and ask for the
brief note. If the diff is unambiguous, state the inferred intent before
proceeding.

## Workflow

1. Read `AGENTS.md`, `research_control/AGENTS.md`, and the relevant source or
   registry rows for changed paths.
2. Inspect current Git state:

   ```zsh
   git status --short
   ```

3. Classify and resolve the change boundary:

   ```zsh
   .venv/bin/python scripts/project_control/classify_project_changes.py --json
   .venv/bin/python scripts/project_control/resolve_project_improvement.py --json
   ```

4. Route by authority:

   - Physics-bearing edits are human-authored proposals. Do not directly adopt
     canonical ontology changes, benchmark-status changes, derivation claims,
     candidate promotion, or Gate Chair conclusions.
   - Research-control continuation belongs to `.codex/skills/continue-research/SKILL.md`.
   - Project-system, skill, role, validator, registry, README, workflow, memory,
     wiki, and generated-document pipeline changes belong to
     `.codex/skills/improve-project-system/SKILL.md`.
   - A newly added project-improvement handoff sidecar without matching signal
     registry rows routes to `/improve-project-system` or Process Integrity
     repair. An edit to an immutable sidecar is blocked and must be superseded
     by a new sidecar. If the diff includes project-system repair files and an
     open sidecar, let `/improve-project-system` decide whether the diff is the
     selected signal's implementation or unrelated work.
   - Documentation-source changes must update the canonical Markdown source
     first, then regenerate derivatives.
   - Generated wiki notes, generated registry sidecars, HTML derivatives, PDFs,
     and `.local/` retrieval surfaces are never independent authority.

5. Execute at most one authorized bounded AgentJob, using the selected
   workflow's role, allowlist, receipts, and stop conditions.
6. After an authorized state-changing transaction, resolve the named
   obligations in
   `research_control/design/validation_obligation_resolution_policy_v1.md`:
   `memory_sync`, `memory_core`, `documentation_impact`,
   `project_improvement_signals` when signals are emitted,
   `research_control_diff`, the task-selected test shard, and
   `git_diff_check`. Under the registered same-scope predicates,
   `research_control_diff` may also satisfy `research_control_core` and
   `claim_language_changed`; working-tree evidence never satisfies a staged
   obligation. The policy owns the single current compatibility recipe per
   gate. Direct precheckpoint commands are editing aids, not independent
   executions implied by each skill or role declaration. Governed checkpoint
   convergence uses write-only `memory_sync()` passes and one blocking
   `memory_core` validation after the final staged Git tree is known; a
   targeted PDF build still requires its second synchronization pass.

7. Checkpoint only when validation passes and the transaction is non-empty.
   The checkpoint owns the `checkpoint_transaction` obligation and final staged
   acceptance. Use `scripts/research_control/checkpoint_research_transaction.py`,
   passing `--job-id` when integrating a project-system AgentJob that is not the
   active physics research task.

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

Human intent recovery, Git inspection, classification, authority routing,
the selected workflow's memory preflight, and canonical source inspection
remain distinct prerequisites; do not count them as profile acceptance.
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

- Human intent is missing and the diff is ambiguous.
- The change would require more than one bounded AgentJob.
- A write path is outside the selected AgentJob allowlist.
- The change would hand-edit generated derivatives instead of canonical sources.
- Physics-bearing edits would be promoted without the required research-control
  or human-gated authority.
- Any required validator fails.

## Reporting

Report the routed track, the controlling workflow, changed authority surfaces,
validation results, checkpoint result, and any remaining blocked paths or
human-gated decisions.
