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
- Generated PDFs, wiki notes, indexes, HTML explainers, and master registries are
  derivative artifacts.
- Generated artifacts must be updated by scripts, not edited by hand.

## Commands

Bootstrap or refresh generated outputs:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
```

Validate without writing:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Clean ignored local noise from canonical lanes:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/clean_local_noise.py
```
