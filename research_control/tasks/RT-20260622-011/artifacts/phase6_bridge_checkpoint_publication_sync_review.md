<!-- authority: control -->

# Phase 6 Bridge Checkpoint Publication Sync Review

Task: `RT-20260622-011`  
Job: `AJ-RT-20260622-011-001`

## Scope

This artifact records the before/after review for the synchronized
publication packet recommended by `RT-20260622-010`.

Included stacks:

- `project-system-improvement`
- `validator-operator-workflow`

Included surfaces:

- Publication briefs.
- `registries/PUBLICATION_BRIEF_REGISTRY.csv` rows.
- Markdown source specs.
- GitHub-facing Markdown derivatives.
- Tracked standalone HTML derivatives.
- Desktop/mobile screenshot evidence.

Excluded surfaces:

- Live project-improvement sidecar instances.
- Validator, resolver, checkpoint, role, skill, schema, and test behavior.
- Canonical physics, ontology, benchmark, or Gate Chair authority sources.

## Before State

The Phase 2 audit found that both selected public stacks still described the
pre-bridge project-system and validator/operator workflows. They did not carry
the Phase 6 source basis for:

- `PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md`.
- `generate_project_improvement_handoff.py`.
- `project_improvement_handoff_validation.py`.
- `checkpoint_research_transaction.py`.
- `validate_research_control.py`.
- The project-control and research-control script README guidance.
- The Phase 6 checkpoint allowlist governance artifact.

The audit also found that strict publication validation requires the public
stack to move together. Source-material edits in only the publication brief or
source spec would create invalid parity until the registry row, GitHub-facing
Markdown, and tracked HTML were updated.

## After State

The synchronized packet updates both public stacks so their source materials
match across all governed surfaces.

`project-system-improvement` now explains:

- Project-system improvement remains separate from physics continuation.
- Project-improvement sidecars are separate improvement-lane inputs.
- Normal research handoffs remain the research-continuation authority.
- `/improve-project-system` may consume one sidecar as one bounded
  project-system packet.
- Checkpoint and `--check-diff` sidecar acceptance is exact-path and
  source-bridge based, not a global sidecar directory allowance.
- Signal closure still requires explicit completion or rejection evidence.

`validator-operator-workflow` now explains:

- Commands are selected by changed authority surface.
- Publication pages need strict publication validation plus screenshot
  evidence.
- Project-system packets need documentation-impact and research-control
  receipts.
- Source-bridged sidecar paths require exact YAML/Markdown pair evidence.
- Positive and negative sidecar controls describe validator evidence but do
  not change validator behavior.
- PASS is bounded deterministic evidence, not scientific truth, sidecar
  adoption, editorial taste, or generated-output authority.

## Parity Check

The same source paths are now present in each stack's:

- Publication brief `source_basis`.
- `registries/PUBLICATION_BRIEF_REGISTRY.csv` `source_materials` field.
- Source spec `source_materials`.
- GitHub-facing Markdown source-materials section.
- Tracked HTML source-materials section.

The HTML files also carry updated source-basis hashes:

- `project-system-improvement`: `efa606cfe8e37da0756962a43ae2ecd3e5e51a2e2554ef20098ea1c97106be5b`
- `validator-operator-workflow`: `e8fd64d8b601632e3e5797d08bf06a21db864343a77561eab519c6c528e68a3b`

## Boundary Finding

The packet documents existing Phase 6 bridge checkpoint governance. It does
not create sidecars, replace normal research handoffs, change validators,
change checkpoint behavior, change schemas, change role or skill contracts,
or promote physics claims.

Conclusion: the synchronized publication update is coherent because source
materials, public derivatives, evidence paths, and authority boundaries now
move together.

## References

The AEther-Flow Research Project. (2026, June 22). *Phase 6 bridge checkpoint
documentation Phase 2 publication brief and source-spec impact audit*
[Project-control artifact].
`research_control/tasks/RT-20260622-010/artifacts/phase6_bridge_checkpoint_documentation_phase2_publication_brief_impact_audit.md`

The AEther-Flow Research Project. (2026, June 22). *Research-improvement
bridge Phase 6 checkpoint allowlist governance* [Project-control artifact].
`research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md`

The AEther-Flow Research Project. (2026). *Publication brief registry*
[Documentation-control registry]. `registries/PUBLICATION_BRIEF_REGISTRY.csv`
