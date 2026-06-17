# Theoretical Continuation Pause-Gate Policy Implementation Audit

Task: `RT-20260617-002`

AgentJob: `AJ-RT-20260617-002-001`

## Objective

Implement the user-directed rule that future research-control pause is reserved
for human-gated ontology authority, while ordinary theoretical uncertainty
routes to a bounded decision role.

## Implemented Policy

Future physics routing after `2026-06-17T04:29:31Z` must not treat missing
local data, absent experiment access, missing source-side primitives, or
unresolved theoretical payload selection as sufficient reason for generic
controlled pause.

The future loop-exit route set now includes:

- `theoretical_decision_role_selection`
- `human_gated_ontology_change_required`

Legacy `controlled_pause` remains valid only for records before the new
activation timestamp.

## New Role

Registered `theoretical-continuation-selector@0.1.0` as a science-draft
routing role. It must output `theoretical_decision_output` selecting one of:

- source-side selector primitive;
- source-side irrelevance theorem;
- concrete `Resp_lc` witness;
- distinct scoped no-go question;
- bounded theoretical calculation; or
- human-gated ontology-change requirement.

The last option is allowed only when continuation requires canonical ontology
authority or another protected human gate.

## Enforcement Points

- `scripts/research_control/validate_research_control.py` rejects future
  `controlled_pause` loop exits and validates the new selector completion
  field.
- `tests/test_research_control.py` covers the new rejection and acceptance
  cases.
- `scripts/research_control/continue_research.py` exposes
  `theoretical_continuation_policy` in the Director context packet.
- `.agents/roles/research_ops/director-of-research.v0.2.0.md` states the
  theoretical-continuation-versus-pause rule.
- `.codex/skills/continue-research/SKILL.md`,
  `.agents/schemas/AGENT_JOB_SCHEMA.md`, and completion/director templates
  state the new contract.
- `AGENTS.md`, `research_control/AGENTS.md`, `README.md`, and
  `research_control/README.md` document the operating rule.

## Authority Boundary

This transaction changes project-system behavior only. It does not execute
physics research, edit canonical ontology, promote benchmark status, request
Gate Chair review, reconstruct a candidate, or make a completed-derivation
claim.
