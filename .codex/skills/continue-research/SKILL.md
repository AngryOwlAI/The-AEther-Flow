---
name: continue-research
description: Resolve tracked research-control state and set up or execute one bounded AgentJob per invocation.
---

# Continue Research

Use this skill for research-control continuation in Flow.

## Workflow

1. Read `AGENTS.md` and `research_control/AGENTS.md`.
2. Run:

   ```zsh
   .venv/bin/python scripts/research_control/continue_research.py
   ```

3. Execute at most one bounded AgentJob if the script and DDR authorize it.
4. Validate:

   ```zsh
   .venv/bin/python scripts/research_control/validate_research_control.py
   ```

5. Write completion and handoff after execution.

Tracked `research_control/` state is authority. Local prompts, logs, previews,
or caches do not override tracked control files.
