<!-- authority: control -->

# AGENTS.md

Scoped guidance for `research_control/`.

## Authority

Tracked research-control files define task state, Director decisions, AgentJobs,
completion records, approvals, and handoffs. `.local/` files are optional
caches and never override tracked control state.

## Continuation Rule

Use `.codex/skills/continue-research/SKILL.md` for continuation. Execute at
most one bounded AgentJob per invocation.

If the active blocker is a missing datum or metric and the datum is not present
in tracked repository sources, do not infer that the research line must stop
solely from local absence. When tracked state or explicit user instruction
authorizes it, the Director may create one bounded non-promotional task for
external primary-source search, source-acquisition design, theoretical
calculation, mathematical construction, or experiment design. The output must
remain draft/control until the normal audit, refutation, and gate sequence is
complete.

Future research-control pause is reserved for protected human-gated authority,
especially canonical ontology edits or ontology adoption. If the next step is
only a theoretical choice among source-side selector primitives, source-side
irrelevance theorems, concrete witnesses, scoped no-go questions, or bounded
calculations, route one bounded `theoretical-continuation-selector@0.1.0`
AgentJob instead of stopping at generic controlled pause.

## Editing Rules

- Keep DDRs, AgentJobs, completions, approvals, and handoffs immutable after
  activation or creation. Supersede rather than rewrite.
- Science-bearing role outputs must be tracked task artifacts and registered in
  the TeX registry when they are `.tex`.
- Do not edit generated wiki notes here.
- Run ` .venv/bin/python scripts/research_control/validate_research_control.py`
  after control changes.
