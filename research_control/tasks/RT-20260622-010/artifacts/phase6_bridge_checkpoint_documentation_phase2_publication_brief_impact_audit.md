<!-- authority: control -->

# Phase 6 Bridge Checkpoint Documentation Phase 2 Publication Brief And Source-Spec Impact Audit

## Analysis

Phase 2 inspected the two primary public explainer stacks selected by the
Phase 0 audit:

- `project-system-improvement`
- `validator-operator-workflow`

The publication briefs and source specs are stale relative to the Phase 6
bridge checkpoint governance result. The missing source basis includes the new
project-improvement sidecar schema, generator, validation helper, checkpoint
script behavior, diff validator behavior, script README boundaries, and the
Phase 6 allowlist-governance artifact.

Strict publication validation exposed an implementation constraint: live
publication brief source-material changes cannot be made alone. The validator
requires parity across the publication brief, publication-brief registry row,
source spec, GitHub-facing Markdown, and tracked HTML stack. Therefore this
phase records impact only and defers live corpus mutation to a synchronized
publication packet.

Conclusion: Phase 2 completed as a task-local impact audit. It did not edit
publication briefs, source specs, the publication-brief registry,
GitHub-facing Markdown, or tracked HTML.

## Brief Impact Matrix

| Brief | Phase 2 decision | Reason |
| --- | --- | --- |
| `project-system-improvement.publication-brief.md` | Impact recorded; no live edit | The reader job, source basis, acceptance criteria, forbidden patterns, and boundary text need the bridge-sidecar and conditional allowlist source basis. |
| `validator-operator-workflow.publication-brief.md` | Impact recorded; no live edit | The operator guide needs to frame checkpoint and `--check-diff` conditional sidecar allowlisting without changing validator behavior. |
| Secondary public briefs | No edit in Phase 2 | Phase 0 marked only the two primary stacks as edit candidates for this phase. Secondary pages can be reconsidered only if the later synchronized packet exposes drift. |

## Source-Spec Impact Matrix

| Source spec | Phase 2 result | Later synchronized action |
| --- | --- | --- |
| `markdown/html-explainer-specs/project-system-improvement-explainer.md` | Selected for later edit; not changed | Add the project-improvement sidecar bridge to the improvement loop map, distinguish signal rows from sidecars, preserve normal handoff authority, and state terminal signal evidence rules. |
| `markdown/html-explainer-specs/validator-operator-workflow-explainer.md` | Selected for later edit; not changed | Add a command/gate row for conditional sidecar allowlisting, name the shared helper behavior at reader level, and preserve validator PASS limits. |
| `research-agent-workflow` | Deferred | Reassess only after the two primary stacks are updated together. |
| `director-agentjob-lifecycle` | Deferred | Reassess only if the synchronized packet needs AgentJob allowlist lifecycle context. |
| `source-authority` | Deferred | Reassess only if the synchronized packet needs a separate authority-boundary note. |
| `memory-system` | No current edit | Phase 6 did not change memory authority or retrieval-sync semantics. |
| `technical-requirements` | No current edit | Phase 6 did not add a new general operator requirement beyond the two selected public stacks. |

## Required Source Basis For Later Synchronized Update

The later publication packet should add or verify the following source basis in
the two selected stacks:

- `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`
- `scripts/project_control/generate_project_improvement_handoff.py`
- `scripts/project_control/project_improvement_handoff_validation.py`
- `scripts/research_control/checkpoint_research_transaction.py`
- `scripts/research_control/validate_research_control.py`
- `scripts/project_control/README.md`
- `scripts/research_control/README.md`
- `research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md`

No live `registries/PUBLICATION_BRIEF_REGISTRY.csv` row changed in this phase.
That registry must remain synchronized with the publication briefs, source
specs, GitHub-facing Markdown, and tracked HTML when the live publication
packet is executed.

## Validator Constraint

`scripts/validate_publication_process.py --root . --strict` requires the
publication stack to move as one synchronized unit. A source-layer-only brief
or source-spec change creates source-material drift against GitHub-facing
Markdown and tracked HTML derivatives.

The implication is operational, not scientific: the repository may still use a
brief-first design process, but committed changes to source-material fields
must either update the full public stack in the same transaction or first
change validator policy explicitly.

## Preserved Boundaries

This phase did not edit:

- publication briefs under `markdown/publication-briefs/`;
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`;
- source specs under `markdown/html-explainer-specs/`;
- GitHub-facing Markdown under `github-facing/`;
- tracked HTML under `html/`;
- generated wiki notes by hand;
- validators, checkpoint scripts, resolver code, schemas, skills, or roles;
- live sidecars under `research_control/project_improvement_handoffs/`;
- canonical science, ontology, benchmark, or Gate Chair authority sources.

The later synchronized packet should continue to forbid these overreads:

- a sidecar replacing the regular research handoff;
- a sidecar proving project-system repair completion;
- global checkpoint allowlisting of the sidecar directory;
- validator PASS proving scientific truth, ontology adoption, benchmark
  promotion, completed derivation, repair completion, or publication quality.

## Phase 2 Exit Criteria

| Criterion | Result |
| --- | --- |
| The two selected publication briefs were inspected for Phase 6 impact. | Satisfied. |
| The two selected source specs were inspected for Phase 6 impact. | Satisfied. |
| Required source basis for the later synchronized update is recorded. | Satisfied. |
| Strict publication validator constraint is recorded. | Satisfied. |
| Publication briefs, source specs, GitHub-facing Markdown, and tracked HTML are untouched. | Satisfied. |
| Publication-brief registry rows are untouched. | Satisfied. |

## Recommendation

Proceed with a validator-safe synchronized publication packet for:

1. `project-system-improvement`
2. `validator-operator-workflow`

That packet should update publication briefs, publication-brief registry rows,
source specs, GitHub-facing Markdown, and tracked HTML together. A different
valid path is to change the strict publication validator explicitly before
allowing transient source-layer-only drift.

The logical source-spec change is not to say "Phase 6 happened." It is to
explain the operational rule, the sidecar boundary, the exact conditional
checkpoint and `--check-diff` acceptance rule, and the failure modes a reader
is likely to misread.

## References

The AEther-Flow Research Project. (2026, June 22). *Phase 6 bridge checkpoint
governance documentation update plan* [Implementation plan].
`implementations_plans/phase6_bridge_checkpoint_documentation_update_plan.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 6 checkpoint allowlist governance* [Project-control artifact].
`research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md`

The AEther-Flow Research Project. (2026). *Project improvement handoff schema*
[Project-control schema]. `.agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`

The AEther-Flow Research Project. (2026). *Publication brief registry*
[Documentation-control registry]. `registries/PUBLICATION_BRIEF_REGISTRY.csv`
