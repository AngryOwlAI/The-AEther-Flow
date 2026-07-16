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

## Commands

Use the Make targets when selecting a local memory operation or acceptance
profile. Environment provisioning is explicit and no validation target depends
on it:

```zsh
make PYTHON=.venv/bin/python setup-dev
make PYTHON=.venv/bin/python memory-sync
make PYTHON=.venv/bin/python memory-validate-core
make PYTHON=.venv/bin/python memory-doctor
make PYTHON=.venv/bin/python test-memory
make PYTHON=.venv/bin/python validate-memory
make PYTHON=.venv/bin/python validate-memory-full
```

`memory-sync` runs the write-only tracked-memory synchronizer and emits its
path-level receipt. `memory-validate-core` runs only the read-only tracked
memory gate. `memory-doctor` owns local Obsidian synchronization and linting,
memory status, and search smoke; it is local operational evidence and cannot
satisfy checkpoint or physics authority. `test-memory` runs the focused memory
test shard.

During the legacy-consolidated migration epoch, `validate-memory` is the
compatibility alias for the memory-focused affected profile: memory-core
validation plus `test-memory`. It does not schedule `memory-sync`, provision
dependencies, run the doctor profile, or discover the full repository test
suite. Focused tests may exercise memory operations under their own fixtures or
live-acceptance safeguards.
`validate-memory-full` retains the full memory acceptance path for memory-tool
changes and scheduled integration: tracked synchronization, doctor checks, the
legacy composite validation gate, and the complete repository test suite. It
also never provisions dependencies.

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
