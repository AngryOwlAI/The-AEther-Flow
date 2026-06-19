<!-- authority: control -->

# Reader Scope Footer Relocation Phase 3 Physics And Claim-Boundary Review

## Analysis

Phase 3 migrated the physics status and claim-boundary pages named by the
relocation plan:

- `aether-flow-physics-program`
- `exact-gr-benchmark-boundary`
- `aether-flow-ontology`
- `gr-derivation-roadmap`
- `claim-gates`

The migration applies the Phase 1 hook exactly. GitHub-facing Markdown now
declares one `## Reader Scope` section immediately before
`<!-- explainer-control: authority_footer -->`. Tracked HTML now declares one
`section[data-explainer-control="reader_scope"]` immediately above
`footer[data-explainer-control="authority_footer"]`, with only `</main>`
between the two.

## Changes Made

- The five source specs now record explicit Reader Scope Footer Binding
  sections and acceptance criteria.
- The five GitHub-facing Markdown derivatives moved their top Reader scope
  paragraphs to bottom `## Reader Scope` sections.
- The five tracked HTML derivatives removed top `notice` Reader scope blocks
  and inserted bottom `reader_scope` sections above the authority footers.
- `registries/PUBLICATION_BRIEF_REGISTRY.csv` points the five Phase 3 rows to
  this packet's screenshot and review evidence.

## Qualifier Preservation

The changed pages preserve high-risk terms already present in the page family:
`draft/control`, `source-only`, `local`, `exact-branch`, `source-extension data`,
`human-gated`, `Resp_lc`, `M_src`, `AtlasGlue_src^+`, `g_eff`, matter coupling,
Einstein equations, Gate Chair, benchmark promotion, and generated
noncanonical reader surface.

No page now implies completed derivation, ontology promotion, benchmark
promotion, Gate Chair approval, global no-go rejection, validator-as-physics
evidence, generated-output authority, or registered-source supersession.

## Screenshot QA

Full-page Playwright screenshots were captured with the established QA
viewport widths:

| Page | Desktop | Mobile |
| --- | --- | --- |
| `aether-flow-physics-program` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/aether-flow-physics-program-desktop.png` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/aether-flow-physics-program-mobile.png` |
| `exact-gr-benchmark-boundary` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/exact-gr-benchmark-boundary-desktop.png` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/exact-gr-benchmark-boundary-mobile.png` |
| `aether-flow-ontology` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/aether-flow-ontology-desktop.png` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/aether-flow-ontology-mobile.png` |
| `gr-derivation-roadmap` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/gr-derivation-roadmap-desktop.png` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/gr-derivation-roadmap-mobile.png` |
| `claim-gates` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/claim-gates-desktop.png` | `research_control/tasks/RT-20260619-014/artifacts/screenshots/claim-gates-mobile.png` |

Dimension checks passed:

- `aether-flow-ontology-desktop.png`: 1440 x 4144
- `aether-flow-ontology-mobile.png`: 390 x 7217
- `aether-flow-physics-program-desktop.png`: 1440 x 2436
- `aether-flow-physics-program-mobile.png`: 390 x 4754
- `claim-gates-desktop.png`: 1440 x 4789
- `claim-gates-mobile.png`: 390 x 8370
- `exact-gr-benchmark-boundary-desktop.png`: 1440 x 2083
- `exact-gr-benchmark-boundary-mobile.png`: 390 x 4668
- `gr-derivation-roadmap-desktop.png`: 1440 x 4580
- `gr-derivation-roadmap-mobile.png`: 390 x 8660

Manual visual samples checked:

- `aether-flow-physics-program-desktop.png`
- `claim-gates-mobile.png`

Both samples show the bottom Reader Scope block immediately above the authority
footer, without visible overlap or horizontal overflow in the sampled render.

## Validation Notes

Publication-process strict validation passed after the hook migration.

## Boundaries Preserved

This packet does not change publication briefs, validators, role contracts,
schema contracts, skill contracts, routing behavior, checkpoint behavior,
canonical science sources, ontology status, benchmark status, derivation
status, Gate Chair authority, or generated-output authority.

## Logical Next Step

After explicit approval, Phase 4 should migrate the research-control operation
page stacks while preserving one-job, role-authority, task-record, schema, and
allowlist boundaries.

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
`research_control/tasks/RT-20260619-013/artifacts/reader_scope_footer_relocation_phase2_pilot_review.md`
[Phase 2 pilot evidence].
