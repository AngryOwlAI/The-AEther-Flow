<!-- authority: control -->

# Phase 5B Roles-And-Skills Page Before/After Review

## Page

`roles-and-skills-explainer`

## Before

The role and skill information existed in authoritative surfaces:
`registries/AGENT_ROLE_REGISTRY.csv`, versioned role contracts under
`.agents/roles/`, and skill contracts under `.codex/skills/`. The active
publication-process registry did not contain a reviewed Phase 5B public
reference packet for finding active role responsibilities, superseded role
status, skill entry points, validator defaults, and human-gate cautions.

Earlier historical `roles-and-skills-explainer` surfaces had been removed
from the active publication tree and were not governed by the current
brief-first publication process.

## After

The Phase 5B packet adds:

- `markdown/publication-briefs/roles-and-skills.publication-brief.md`
- `markdown/html-explainer-specs/roles-and-skills-explainer.md`
- `github-facing/roles-and-skills-explainer.md`
- `html/roles-and-skills-explainer.html`
- desktop screenshot evidence
- mobile screenshot evidence
- a reviewed publication-brief registry row

The GitHub-facing page reads as a native reference catalog. The HTML page uses
a static role matrix, superseded-role panel, skill-to-workflow map, validator
family guide, and authority-boundary cautions. Both surfaces state that the
catalog is navigation only and that actual execution authority must be read
from source registries, contracts, execution-role records, AgentJobs, claim
boundaries, completions, and validators.

## Boundary Review

PASS:

- Active versus superseded role status is explicit.
- Physics roles, research-ops roles, and the human-gated Gate Chair are
  separated.
- Skill entry points are mapped to workflow lanes.
- Default validator families are explained without changing validators.
- The source-inspection order is explicit.
- The page states that it is a generated noncanonical navigation catalog.
- No role status, role registration, role authority, skill contract, validator
  behavior, routing behavior, checkpoint behavior, generated-output authority,
  or physics claim status changed.

Remaining risk:

- The page is an operator catalog, not a role-contract substitute. Readers who
  need exact permissions must inspect the active role contract, task-local
  execution-role record, AgentJob allowlist, and completion evidence directly.
