<!-- authority: control -->

# Reader Scope Footer Relocation Phase 2 Pilot Review

## Analysis

Phase 2 migrated the pilot pair named by the relocation plan:

- `project-overview`
- `source-authority`

The migration applies the Phase 1 hook exactly. GitHub-facing Markdown now
declares one `## Reader Scope` section immediately before
`<!-- explainer-control: authority_footer -->`. Tracked HTML now declares one
`section[data-explainer-control="reader_scope"]` immediately above
`footer[data-explainer-control="authority_footer"]`, with only `</main>`
between the two.

## Changes Made

- `markdown/html-explainer-specs/project-overview-explainer.md` now records
  the exact footer-bound Reader scope text.
- `markdown/html-explainer-specs/source-authority-explainer.md` now records
  the exact footer-bound Reader scope text.
- `github-facing/project-overview-explainer.md` now includes bottom
  `## Reader Scope` text immediately above the authority footer marker.
- `github-facing/source-authority-explainer.md` now includes bottom
  `## Reader Scope` text immediately above the authority footer marker.
- `html/project-overview-explainer.html` removes the top hero scope block and
  adds the bottom `reader_scope` section immediately above the authority
  footer.
- `html/source-authority-explainer.html` removes the top hero scope block and
  adds the bottom `reader_scope` section immediately above the authority
  footer.
- `registries/PUBLICATION_BRIEF_REGISTRY.csv` points the two pilot rows to the
  Phase 2 screenshot and review evidence.

## Screenshot QA

Full-page Playwright screenshots were captured with the established QA
viewport widths:

| Page | Desktop | Mobile |
| --- | --- | --- |
| `project-overview` | `research_control/tasks/RT-20260619-013/artifacts/screenshots/project-overview-desktop.png` | `research_control/tasks/RT-20260619-013/artifacts/screenshots/project-overview-mobile.png` |
| `source-authority` | `research_control/tasks/RT-20260619-013/artifacts/screenshots/source-authority-desktop.png` | `research_control/tasks/RT-20260619-013/artifacts/screenshots/source-authority-mobile.png` |

Dimension checks passed:

- `project-overview-desktop.png`: 1440 x 3015
- `project-overview-mobile.png`: 390 x 6029
- `source-authority-desktop.png`: 1440 x 3166
- `source-authority-mobile.png`: 390 x 6444

Manual visual samples checked:

- `project-overview-desktop.png`
- `source-authority-mobile.png`

Both samples show the bottom Reader Scope block immediately above the authority
footer, without visible overlap or horizontal overflow in the sampled render.

## Validation Notes

Publication-process strict validation passed after the hook migration.

The documentation-surface audit was also run before bootstrap. It failed only
on expected stale source and derivative hashes for the two edited source specs,
two GitHub-facing derivatives, and two HTML derivatives. No Reader Scope
placement error was reported. The stale hashes are expected until
`bootstrap_memory_system.py` refreshes the generated registries.

## Boundaries Preserved

This packet does not change publication briefs, validators, role contracts,
schema contracts, skill contracts, routing behavior, checkpoint behavior,
canonical science sources, ontology status, benchmark status, derivation
status, Gate Chair authority, or generated-output authority.

## Logical Next Step

After explicit approval, Phase 3 should migrate the physics status and
claim-boundary page stacks while preserving high-risk qualifiers exactly.

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

AEther-Flow Project. (2026). `markdown/html-explainer-specs/project-overview-explainer.md`
[Project Overview source spec].

AEther-Flow Project. (2026). `markdown/html-explainer-specs/source-authority-explainer.md`
[Source Authority source spec].
