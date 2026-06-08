# AGENTS.md

Scoped guidance for `research_control/`.

## Authority

Tracked research-control files define task state, Director decisions, AgentJobs,
completion records, approvals, and handoffs. `.local/` files are optional
caches and never override tracked control state.

## Continuation Rule

Use `.codex/skills/continue-research/SKILL.md` for continuation. Execute at
most one bounded AgentJob per invocation.

## Editing Rules

- Keep DDRs, AgentJobs, completions, approvals, and handoffs immutable after
  activation or creation. Supersede rather than rewrite.
- Science-bearing role outputs must be tracked task artifacts and registered in
  the TeX registry when they are `.tex`.
- Do not edit generated wiki notes here.
- Run ` .venv/bin/python scripts/research_control/validate_research_control.py`
  after control changes.
