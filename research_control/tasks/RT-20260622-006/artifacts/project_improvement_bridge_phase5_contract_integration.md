<!-- authority: control -->

# Research-Improvement Bridge Phase 5 Contract Integration

## Analysis

Phase 5 integrates the project-improvement handoff bridge into the workflow
contract layer. Phase 4 made the generator and resolver capable of handling
sidecar context, but future agents still needed explicit skill and role
instructions for when to create sidecars and how to consume them.

## Changes

Updated:

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `registries/AGENT_ROLE_REGISTRY.csv`

Added new active role-contract versions:

- `.agents/roles/research_ops/director-of-research.v0.3.0.md`
- `.agents/roles/research_ops/project-system-director.v0.2.0.md`
- `.agents/roles/research_ops/project-control-maintainer.v0.2.0.md`
- `.agents/roles/research_ops/validator-engineer.v0.2.0.md`
- `.agents/roles/research_ops/memory-system-maintainer.v0.2.0.md`

Marked the prior active role versions as `superseded` in their front matter and
in `registries/AGENT_ROLE_REGISTRY.csv`.

Refreshed stale historical `memory_preflight` source-hash receipts for shared
AGENTS, skill, and role-contract sources whose registered hashes changed in this
phase. This is a receipt repair only; it does not change the earlier jobs'
scientific or workflow claims.

The `continue-research` skill now states that future nonblank
`project_improvement_signals` require concrete signal registry rows, a separate
project-improvement sidecar, source `project_improvement_bridge` references,
and signal validation after the normal completion and research handoff are
written.

The `improve-project-system` skill now states that selected sidecars supply
local implementation context, ready solution plans can route to the named safe
implementation role, and issue inventories without executable plans route one
Project-System Director planning or rejection step.

The `user-modified-project` skill now blocks immutable sidecar edits, routes
sidecars without registry rows to project-system repair, and lets
`/improve-project-system` decide whether repair diffs correspond to an open
sidecar.

## Preserved Boundaries

No live `research_control/project_improvement_handoffs/` sidecar instance was
created in this transaction.

No normal research handoff resolver behavior, checkpoint behavior, validator
behavior, resolver behavior, optional sidecar registry, canonical science
source, ontology source, benchmark source, Gate Chair authority, or physics
claim status changed.

The role updates are new versions of existing roles, not new role identities.

## Verification Targets

The minimum checks for this phase are:

- memory preflight status and targeted lookups;
- project change classification;
- advisory project-improvement resolution;
- project-improvement signal validation;
- latest research handoff resolution;
- control script `py_compile` smoke check;
- memory bootstrap, Obsidian sync, and validate-only;
- documentation-impact validation;
- research-control validation and diff validation;
- `git diff --check`.

## Logical Next Step

Phase 6 should remain deferred unless checkpoint conditional allowlist
governance for sidecar paths is explicitly authorized.

## References

The AEther-Flow Research Project. (2026, June 22). *The AEther-Flow research
to improvement bridge* [Implementation plan].
`implementations_plans/research_improvement_bridge_plan.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 4 activation* [Project-control artifact].
`research_control/tasks/RT-20260622-005/artifacts/project_improvement_bridge_phase4_activation.md`
