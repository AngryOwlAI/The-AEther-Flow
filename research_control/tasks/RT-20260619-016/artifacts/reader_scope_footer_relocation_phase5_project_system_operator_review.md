<!-- authority: control -->

# Reader Scope Footer Relocation Phase 5 Project-System Operator Review

## Analysis

Phase 5 migrated the project-system, memory, operator, role, and requirement
pages named by the relocation plan:

- `project-system-improvement`
- `documentation-curator-publication-process`
- `memory-system`
- `validator-operator-workflow`
- `roles-and-skills`
- `technical-requirements`

The migration applies the locked Phase 1 hook. GitHub-facing Markdown now
declares one `## Reader Scope` section immediately before
`<!-- explainer-control: authority_footer -->`. Tracked HTML now declares one
`section[data-explainer-control="reader_scope"]` immediately above
`footer[data-explainer-control="authority_footer"]`, with only `</main>`
between the two.

## Changes Made

- The six source specs now record explicit Reader Scope Footer Binding
  sections and acceptance criteria.
- The six GitHub-facing Markdown derivatives moved their top Reader scope
  paragraphs to bottom `## Reader Scope` sections.
- The six tracked HTML derivatives removed top `scope` blocks and inserted
  bottom `reader_scope` sections above the authority footers.
- `registries/PUBLICATION_BRIEF_REGISTRY.csv` points the six Phase 5 rows to
  this packet's screenshot and review evidence.

## Boundary Preservation

The changed pages preserve the operational limits already present in the page
family: project-system signal closure evidence, brief-first publication
workflow, memory as retrieval support rather than authority, validator PASS
limits, task-local role and skill authority, and local tool/dependency
boundaries.

No page now implies signal creation or closure authority, validator behavior
change, schema change, routing change, checkpoint change, memory-system
behavior change, role registration, skill-contract change, dependency change,
generated-output authority, physics claim promotion, ontology promotion,
benchmark promotion, or Gate Chair approval.

## Screenshot QA

Full-page Playwright screenshots were captured with the established QA
viewport widths:

| Page | Desktop | Mobile |
| --- | --- | --- |
| `project-system-improvement` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/project-system-improvement-desktop.png` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/project-system-improvement-mobile.png` |
| `documentation-curator-publication-process` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/documentation-curator-publication-process-desktop.png` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/documentation-curator-publication-process-mobile.png` |
| `memory-system` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/memory-system-desktop.png` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/memory-system-mobile.png` |
| `validator-operator-workflow` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/validator-operator-workflow-desktop.png` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/validator-operator-workflow-mobile.png` |
| `roles-and-skills` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/roles-and-skills-desktop.png` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/roles-and-skills-mobile.png` |
| `technical-requirements` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/technical-requirements-desktop.png` | `research_control/tasks/RT-20260619-016/artifacts/screenshots/technical-requirements-mobile.png` |

Dimension checks passed:

- `documentation-curator-publication-process-desktop.png`: 1440 x 3652
- `documentation-curator-publication-process-mobile.png`: 390 x 6706
- `memory-system-desktop.png`: 1440 x 3728
- `memory-system-mobile.png`: 390 x 7386
- `project-system-improvement-desktop.png`: 1440 x 3669
- `project-system-improvement-mobile.png`: 390 x 7239
- `roles-and-skills-desktop.png`: 1440 x 3464
- `roles-and-skills-mobile.png`: 390 x 6975
- `technical-requirements-desktop.png`: 1440 x 3936
- `technical-requirements-mobile.png`: 390 x 7898
- `validator-operator-workflow-desktop.png`: 1440 x 3743
- `validator-operator-workflow-mobile.png`: 390 x 7409

Manual visual samples checked:

- `project-system-improvement-desktop.png`
- `technical-requirements-mobile.png`

Both samples show the bottom Reader Scope block immediately above the authority
footer, without visible overlap or horizontal overflow in the sampled render.

## Validation Notes

Publication-process strict validation passed after the hook migration and
before registry refresh. The documentation-surface audit reported only
expected stale source-hash and HTML-hash receipts before bootstrap refresh.

## Boundaries Preserved

This packet does not change publication briefs, validators, role contracts,
schema contracts, skill contracts, memory-system behavior, routing behavior,
checkpoint behavior, dependency behavior, canonical science sources, ontology
status, benchmark status, derivation status, Gate Chair authority, or
generated-output authority.

## Logical Next Step

After explicit approval, Phase 6 should run the full-corpus Reader Scope QA and
registry refresh for all 17 migrated page stacks.

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
`research_control/tasks/RT-20260619-015/artifacts/reader_scope_footer_relocation_phase4_research_control_operation_review.md`
[Phase 4 evidence pattern].
