---
name: ontology-promotion
description: Front door for ontology promotion packet boundaries.
---

# Ontology Promotion

Use this skill when proposing to promote manuscript material into the canonical
ontology package.

First-pass boundary:

- Promotion notes live under `markdown/ontology-promotions/`.
- A promotion note is required before changing `ontology/tex/`.
- The first implementation records registry states and skill boundaries only.
- A full benchmark-preservation validator is intentionally deferred.

Validate current registry state with:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --check
```
