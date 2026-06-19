# Phase 3C Research-Control System Merge Decision

## Scope

Task `RT-20260618-017` reviewed whether the historical
`research-control-system-explainer` filename still has a distinct reader job
after the Phase 3A and Phase 3B publication packets.

The packet did not create a publication brief, source spec, GitHub-facing
Markdown page, tracked HTML page, screenshot QA artifact, role contract,
schema, validator, routing behavior, or physics claim.

## Evidence Reviewed

| Surface | Coverage |
| --- | --- |
| `research-agent-workflow-explainer` | Lane selection, memory preflight, one bounded AgentJob, generated-output boundaries, stop conditions, and human gates. |
| `director-agentjob-lifecycle-explainer` | Task, DDR, AgentJob, execution-role, completion, handoff, registry, allowlist, and immutable-record operation. |
| `parent-child-synthesis-explainer` | Internal parent-child perspective mode while preserving one outer AgentJob and one completion. |
| `role-routing-explainer` | Registered roles, task overlays, provisional roles, execution-role records, Gate Chair human-gated status, and actual authority inspection order. |
| `research_control/README.md` | Directory-local authority model, one-job rule, memory preflight, validation commands, documentation-impact handling, and signal handling. |

## Decision

`research-control-system-explainer` should remain merged into the active
Phase 3 and Phase 4 coverage plan. It should not be created as a standalone
publication page now.

## Reasoning

The candidate page fails the distinct-reader-job test. Its workflow overview
content is covered by `research-agent-workflow-explainer`; its record-operation
content is covered by `director-agentjob-lifecycle-explainer`; its parent-child
and role-routing content is covered by the Phase 3B pages; and its directory
operation content is already partly served by `research_control/README.md`.

The remaining practical operator needs, especially project-system routing,
documentation-impact receipts, validator command selection, and memory-system
operation, are separate Phase 4 and Phase 5 reader jobs. A standalone
`research-control-system-explainer` would likely become a generic third
overview and weaken the publication-process rule that every page needs a
specific reader problem.

## Boundary Preserved

- No public page was added.
- No legacy explainer filename was revived.
- No generated output was promoted to authority.
- No role, schema, validator, routing, or checkpoint behavior changed.
- No canonical science or physics claim source changed.

## Recommendation

The logical next public-documentation packet is Phase 4A:
`project-system-improvement-explainer`. It has a distinct reader job: explain
how documentation drift, control drift, validator gaps, memory issues, and
routing ambiguity become bounded project-system work.
