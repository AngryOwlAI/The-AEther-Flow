# Mandatory Parent-Child Continue-Research Policy Implementation Audit

Task: `RT-20260617-001`

AgentJob: `AJ-RT-20260617-001-001`

## Objective

Implement the user-directed rule that every future physics
`/continue-research` AgentJob must use internal parent-child
perspective synthesis.

## Implemented Policy

Future physics AgentJobs created after `2026-06-17T04:08:16Z` must
declare:

```yaml
role_decomposition:
  mode: "parent_child_parallel_synthesis"
```

The validator preserves historical AgentJobs before the activation
timestamp and project-system AgentJobs where physics-role
decomposition is not applicable.

## Enforcement Points

- `scripts/research_control/validate_research_control.py` now fails
  future physics AgentJobs missing `role_decomposition`.
- `tests/test_research_control.py` covers the future failure case and
  the historical compatibility case.
- `.codex/skills/continue-research/SKILL.md` states the rule in the
  continuation procedure.
- `.agents/schemas/AGENT_JOB_SCHEMA.md` and
  `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` state the schema and role
  inheritance rule.
- `.agents/roles/research_ops/director-of-research.v0.2.0.md` states
  the Director obligation.
- `research_control/templates/DIRECTOR_DECISION_TEMPLATE.md` changes
  the section from optional to required role decomposition for future
  physics jobs.
- `README.md` and `research_control/README.md` explain the future
  operating rule.

## Authority Boundary

This transaction changes project-system behavior only. It does not
execute physics research, edit canonical ontology, promote benchmark
status, request Gate Chair review, reconstruct a candidate, or make a
completed-derivation claim.
