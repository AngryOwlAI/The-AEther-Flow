---
name: html-visual-explainer
description: Front door for generated human-only HTML explainers.
---

# HTML Visual Explainer

Use this skill when producing or validating tracked HTML explainers.

Rules:

- Tracked HTML under `html/` is generated-only.
- Every tracked HTML explainer must have a registered Markdown source spec.
- HTML is human-only and never scientific, control, or registry authority.

Implementation metadata is validated by:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --check
```
