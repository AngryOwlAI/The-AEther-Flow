---
name: project-memory-system
description: Owns the shared memory, registry, wiki, PDF-derivative, cleanup, and validation scripts for this repository.
---

# Project Memory System

Use this skill when creating, regenerating, or validating the repository memory,
wiki, registry, and derivative-artifact system.

## Authority

- Canonical scientific source lives in registered `.tex` files.
- Authored project documentation lives in registered Markdown files.
- Registered Markdown includes front-door docs, scoped agent guidance, role
  contracts, schema contracts, skill contracts, key research-control design
  notes, and Markdown source specs for generated HTML explainers.
- Generated PDFs, wiki notes, indexes, HTML explainers, and master registries are
  derivative artifacts.
- Generated artifacts must be updated by scripts, not edited by hand.

## Validation Profile Wrapper

Select validation through the shared profile planner instead of copying a
memory-specific acceptance chain into this skill:

```zsh
.venv/bin/python -m scripts.validation.cli run --profile <fast|affected|full> --paths <changed-path>
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py --job-id <agent-job-id>
.venv/bin/python -m scripts.validation.cli plan --profile doctor --scope local_retrieval --explain
```

Use `fast` for the cheapest local edit loop, `affected` for bounded
precheckpoint feedback, `checkpoint` only through the caller's governed final
state-changing transaction, `full` only for explicit exhaustive or scheduled
coverage, and `doctor` only for local retrieval or advisory diagnostics.
During the `planner_authoritative` epoch, `run` executes the manifest-selected
gates and emits the authoritative operational receipt. The explicit
`validate-project-control-legacy` Make target and checkpoint
`--legacy-validation` switch remain rollback controls. A plan alone is not
validation evidence, and no profile replaces source authority, a human gate,
or final staged checkpoint acceptance.

Memory synchronization, memory-core validation, local retrieval refresh, and
canonical source inspection remain distinct operations selected by the plan or
owning AgentJob; do not count them as profile selection evidence. Consume
results under
`research_control/design/agent_validation_output_consumption_policy_v1.md`:
record the profile, selected gate IDs, status, compact receipt path and hash,
counts, and tree identity; expand only the relevant failed or warning finding
group.

Execute the local-retrieval doctor through its explicit Make target:

```zsh
make PYTHON=.venv/bin/python validate-doctor
make PYTHON=.venv/bin/python validate-doctor VALIDATION_DOCTOR_FLAGS=--refresh
```

The default is read-only. `--refresh` explicitly rebuilds only ignored local
retrieval state. Doctor `WARN` findings do not change tracked-memory PASS and
do not satisfy checkpoint acceptance. Full receipts remain under
`.local/validation-receipts/doctor/`; operator output stays compact unless the
receipt is inspected.

## Direct Memory Operations

Use these direct compatibility operations only when the shared plan or owning
AgentJob selects them. Environment provisioning is explicit and no validation
operation depends on it:

```zsh
make PYTHON=.venv/bin/python setup-dev
make PYTHON=.venv/bin/python memory-sync
make PYTHON=.venv/bin/python memory-validate-core
make PYTHON=.venv/bin/python memory-doctor
make PYTHON=.venv/bin/python test-memory
```

`memory-sync` runs the write-only tracked-memory synchronizer and emits its
path-level receipt. `memory-validate-core` runs only the read-only tracked
memory gate. `memory-doctor` remains the mutating compatibility wrapper for
local Obsidian synchronization, linting, status, and search smoke;
`validate-doctor` is the read-only-by-default diagnostic command. Both are
local operational evidence and cannot satisfy checkpoint or physics authority.
`test-memory` runs the focused memory test shard.

The legacy Make aliases `validate-memory` and `validate-memory-full` remain
compatibility entry points until their separately authorized wrapper and
cutover packets. They are migration notes, not skill-owned profile definitions
or permission to recreate their command chains here. Focused tests may exercise
memory operations under fixtures or live-acceptance safeguards.

Bootstrap or refresh generated outputs:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
```

Validate without writing:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

`--check` is accepted as a compatibility alias for `--validate-only`; prefer
`--validate-only` in new documentation.

Documentation publication validation modes:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --docs-only
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --docs-validate-only
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only --strict-docs
```

These modes run the active publication-process validator. They check source
grounding, authority boundaries, no-network public HTML, publication brief
conformance, orphan public explainer files, and known anti-template failures.
They do not promote generated artifacts to authority or replace human-facing
editorial review.

Clean ignored local noise from canonical lanes:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/clean_local_noise.py
```
