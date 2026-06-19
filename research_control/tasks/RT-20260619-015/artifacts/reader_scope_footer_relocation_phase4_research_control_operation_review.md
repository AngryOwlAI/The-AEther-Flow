<!-- authority: control -->

# Reader Scope Footer Relocation Phase 4 Research-Control Operation Review

## Analysis

Phase 4 migrated the research-control operation pages named by the relocation
plan:

- `research-agent-workflow`
- `director-agentjob-lifecycle`
- `parent-child-synthesis`
- `role-routing`

The migration applies the locked Phase 1 hook. GitHub-facing Markdown now
declares one `## Reader Scope` section immediately before
`<!-- explainer-control: authority_footer -->`. Tracked HTML now declares one
`section[data-explainer-control="reader_scope"]` immediately above
`footer[data-explainer-control="authority_footer"]`, with only `</main>`
between the two.

## Changes Made

- The four source specs now record explicit Reader Scope Footer Binding
  sections and acceptance criteria.
- The four GitHub-facing Markdown derivatives moved their top Reader scope
  paragraphs to bottom `## Reader Scope` sections.
- The four tracked HTML derivatives removed top `scope` blocks and inserted
  bottom `reader_scope` sections above the authority footers.
- `registries/PUBLICATION_BRIEF_REGISTRY.csv` points the four Phase 4 rows to
  this packet's screenshot and review evidence.

## Boundary Preservation

The changed pages preserve the operational limits already present in the page
family: one bounded AgentJob, memory as navigation only, immutable
control-record supersession, execution-role authority, task-local allowlists,
schema boundaries, validator limits, parent-child `draft/control` support, and
human-gated protected authority.

No page now implies role registration, schema change, routing change,
checkpoint change, reusable allowlist authority, generated-output authority,
validator-as-physics evidence, child AgentJob creation, child execution-role
creation, Gate Chair approval, ontology promotion, benchmark promotion, or
physics claim promotion.

## Screenshot QA

Full-page Playwright screenshots were captured with the established QA
viewport widths:

| Page | Desktop | Mobile |
| --- | --- | --- |
| `research-agent-workflow` | `research_control/tasks/RT-20260619-015/artifacts/screenshots/research-agent-workflow-desktop.png` | `research_control/tasks/RT-20260619-015/artifacts/screenshots/research-agent-workflow-mobile.png` |
| `director-agentjob-lifecycle` | `research_control/tasks/RT-20260619-015/artifacts/screenshots/director-agentjob-lifecycle-desktop.png` | `research_control/tasks/RT-20260619-015/artifacts/screenshots/director-agentjob-lifecycle-mobile.png` |
| `parent-child-synthesis` | `research_control/tasks/RT-20260619-015/artifacts/screenshots/parent-child-synthesis-desktop.png` | `research_control/tasks/RT-20260619-015/artifacts/screenshots/parent-child-synthesis-mobile.png` |
| `role-routing` | `research_control/tasks/RT-20260619-015/artifacts/screenshots/role-routing-desktop.png` | `research_control/tasks/RT-20260619-015/artifacts/screenshots/role-routing-mobile.png` |

Dimension checks passed:

- `director-agentjob-lifecycle-desktop.png`: 1440 x 2974
- `director-agentjob-lifecycle-mobile.png`: 390 x 6094
- `parent-child-synthesis-desktop.png`: 1440 x 2934
- `parent-child-synthesis-mobile.png`: 390 x 5630
- `research-agent-workflow-desktop.png`: 1440 x 2857
- `research-agent-workflow-mobile.png`: 390 x 5668
- `role-routing-desktop.png`: 1440 x 2736
- `role-routing-mobile.png`: 390 x 5323

Manual visual samples checked:

- `research-agent-workflow-desktop.png`
- `role-routing-mobile.png`

Both samples show the bottom Reader Scope block immediately above the authority
footer, without visible overlap or horizontal overflow in the sampled render.

## Validation Notes

Publication-process strict validation passed after the hook migration and
before registry refresh.

## Boundaries Preserved

This packet does not change publication briefs, validators, role contracts,
schema contracts, skill contracts, routing behavior, checkpoint behavior,
canonical science sources, ontology status, benchmark status, derivation
status, Gate Chair authority, or generated-output authority.

## Logical Next Step

After explicit approval, Phase 5 should migrate the project-system, memory,
operator, role, and requirement page stacks while preserving tool, validator,
retrieval, role-catalog, and dependency boundaries.

## Source Materials

AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy and
generated-output boundaries].

AEther-Flow Project. (2026). `research_control/AGENTS.md` [Research-control
editing rules].

AEther-Flow Project. (2026).
`research_control/design/documentation_curator_reader_scope_footer_relocation_plan.md`
[Reader Scope footer relocation plan].

AEther-Flow Project. (2026).
`research_control/tasks/RT-20260619-012/artifacts/reader_scope_footer_relocation_phase1_guardrail.md`
[Phase 1 hook pattern and validator guardrail].

AEther-Flow Project. (2026).
`research_control/tasks/RT-20260619-014/artifacts/reader_scope_footer_relocation_phase3_physics_claim_boundary_review.md`
[Phase 3 evidence pattern].
