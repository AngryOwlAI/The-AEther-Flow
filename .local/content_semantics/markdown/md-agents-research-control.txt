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

Future physics AgentJobs after `2026-06-17T15:46:25Z` must name a
`target_derivation_milestone` and `milestone_burden` from
`research_control/design/gr_derivation_burden_map.md`. Completions must update
the expanded Distance-to-GR burden matrix, name a new mathematical payload, and
evaluate freeze criteria for repeated-burden or scoped-obstruction outcomes.
Source-extension and finite toy metric-response packets are controlled
categories, not claim-promotion shortcuts.

## Ontology-Law Research Packet Route

Use route label `ontology-law-research-packet` only when the active derivation
milestone is blocked by `derivation_critical_missing_source_law`: the current
ontology lacks a required source-side law, selector, discriminator, transition
rule, robustness rule, or equivalent primitive.

Non-triggers are `ordinary_gap` and `workflow_inconvenience`. Ordinary gaps
include missing documentation, missing registry rows, generated derivative
drift, missing citations, missing computations that can be done under existing
ontology, and proof-detail work under existing ontology. Workflow
inconvenience includes tedious casework, slow literature review, awkward
templates, and strict validation friction.

A valid underdetermination statement may say "current ontology does not derive
X." It may not conclude "therefore X is impossible" unless a separate no-go
theorem or scoped obstruction proves that stronger claim. If conservative
source-side extension remains possible, record the status pair
`blocked_adoption_open_continuation`: current adoption is blocked while
same-milestone research continuation stays open.

Candidate status vocabulary is `draft/control`, `proposal-only`,
`source-extension data`, `canonical-ontology candidate`, `adopted`,
`rejected`, and `human-gated`. The route does not edit canonical ontology,
promote benchmark status, adopt `M_src` or atlas-glue data, create Gate Chair
authority, or weaken exact-GR recovery obligations.

## Editing Rules

- Keep DDRs, AgentJobs, completions, approvals, and handoffs immutable after
  activation or creation. Supersede rather than rewrite.
- Science-bearing role outputs must be tracked task artifacts and registered in
  the TeX registry when they are `.tex`.
- Do not edit generated wiki notes here.
- Run ` .venv/bin/python scripts/research_control/validate_research_control.py`
  after control changes.
