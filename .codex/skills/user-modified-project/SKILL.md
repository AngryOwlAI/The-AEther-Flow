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
   - Documentation-source changes must update the canonical Markdown source
     first, then regenerate derivatives.
   - Generated wiki notes, generated registry sidecars, HTML derivatives, PDFs,
     and `.local/` retrieval surfaces are never independent authority.

5. Execute at most one authorized bounded AgentJob, using the selected
   workflow's role, allowlist, receipts, and stop conditions.
6. Refresh and validate generated systems after an authorized state-changing
   transaction:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
   .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
   .venv/bin/python scripts/project_control/validate_documentation_impact.py
   .venv/bin/python scripts/research_control/validate_research_control.py
   .venv/bin/python scripts/research_control/validate_research_control.py --check-diff
   ```

7. Checkpoint only when validation passes and the transaction is non-empty.
   Use `scripts/research_control/checkpoint_research_transaction.py`, passing
   `--job-id` when integrating a project-system AgentJob that is not the active
   physics research task.

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
