<!-- authority: explanatory -->

# Phase 3A Research-Control Operation Review

## Scope

Phase 3A migrated two public page families from the corpus migration plan:

- `research-agent-workflow-explainer`
- `director-agentjob-lifecycle-explainer`

The packet did not migrate Phase 3B pages, edit role contracts, edit schemas,
change validators, change routing behavior, mutate historical control
records, or alter physics claim status.

## Before

The active publication corpus had Phase 0, Phase 1, and Phase 2 public pages,
but no active brief-first public surface for the high-operational-risk
research-agent workflow pages. Historical semantic memory still contained old
workflow/lifecycle explainer references, but the live source tree no longer
contained those page families after the retired process removal.

## After

Phase 3A now provides two reviewed publication pages:

| Page | Improvement | Boundary preserved |
| --- | --- | --- |
| Research-Agent Workflow | Explains continuation versus project-system improvement, one bounded AgentJob, memory preflight, roles, checks, generated outputs, and stop conditions. | No routing behavior, role authority, validator, claim-boundary, or physics-status change. |
| Director Decisions And AgentJob Lifecycle | Explains task, DDR, AgentJob, execution-role, completion, handoff, registry, allowlist, immutable-record, and supersession discipline. | No schema edit, task-behavior edit, historical-record mutation, or broad-proof claim. |

## Source-Basis Review

| Required source path | Coverage |
| --- | --- |
| `README.md` | Research-agent mission and two-track project context. |
| `AGENTS.md` | Authority hierarchy, continuation boundaries, project-system improvement, generated-output limits. |
| `research_control/README.md` | Director decisions, AgentJobs, execution roles, one-job rule, memory preflight, checks, documentation impact, signals. |
| `research_control/AGENTS.md` | Tracked control authority and immutable-record editing rules. |
| `.codex/skills/continue-research/SKILL.md` | Physics continuation lane and one bounded AgentJob flow. |
| `.codex/skills/improve-project-system/SKILL.md` | Project-system lane and Documentation Curator routing. |
| `.agents/schemas/DIRECTOR_DECISION_SCHEMA.md` | DDR required fields and body sections. |
| `.agents/schemas/AGENT_JOB_SCHEMA.md` | AgentJob fields, memory preflight, allowlists, and role decomposition boundaries. |
| `.agents/schemas/EXECUTION_ROLE_SCHEMA.md` | Registered role, task overlay, and provisional role record semantics. |
| `registries/AGENT_ROLE_REGISTRY.csv` | Role authority levels, human-gate status, and Documentation Curator limits. |
| `registries/DIRECTOR_DECISION_REGISTRY.csv` | DDR provenance. |
| `registries/AGENT_JOB_REGISTRY.csv` | AgentJob provenance, completion paths, allowed writes, and outputs. |
| `registries/ROLE_EXECUTION_REGISTRY.csv` | Exact execution-role contract used for each AgentJob. |

## Acceptance Audit

| Criterion | Result |
| --- | --- |
| Explains two linked missions and agent workflow purpose. | Pass |
| Separates continuation from project-system improvement. | Pass |
| States one bounded AgentJob per invocation. | Pass |
| Explains memory preflight as navigation, not authority. | Pass |
| Explains role contracts and execution-role records without role expansion. | Pass |
| States validators and generated outputs are not scientific verdicts. | Pass |
| Explains task, DDR, AgentJob, execution-role, completion, handoff, and registry relationships. | Pass |
| States activated or created control records are superseded rather than rewritten. | Pass |
| Explains allowlists, claim boundaries, and stop conditions. | Pass |
| Treats completion evidence as transaction evidence only. | Pass |
| Provides page-specific GitHub Markdown, HTML, screenshots, and source binding. | Pass |

## Screenshot QA

Desktop and mobile screenshots are stored under:

- `research_control/tasks/RT-20260618-015/artifacts/screenshots/research-agent-workflow-desktop.png`
- `research_control/tasks/RT-20260618-015/artifacts/screenshots/research-agent-workflow-mobile.png`
- `research_control/tasks/RT-20260618-015/artifacts/screenshots/director-agentjob-lifecycle-desktop.png`
- `research_control/tasks/RT-20260618-015/artifacts/screenshots/director-agentjob-lifecycle-mobile.png`

The screenshots verify the tracked HTML pages render as standalone,
no-network, mobile-safe reader surfaces with visible source grounding and
non-authority language.

## Remaining Risks

- The pages explain operational machinery and may need refresh if future
  project-system work changes role, schema, routing, or validator contracts.
- The pages intentionally do not migrate Phase 3B `parent-child-synthesis` or
  `role-routing` coverage.
- Local retrieval freshness warnings remain nonblocking retrieval-layer
  maintenance, not source authority.

## Verdict

Phase 3A satisfies the publication-process requirements for the two
research-control operation pages and preserves the project's authority
boundaries.
