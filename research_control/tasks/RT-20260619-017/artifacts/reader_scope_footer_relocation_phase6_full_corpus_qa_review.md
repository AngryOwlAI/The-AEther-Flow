<!-- authority: control -->

# Reader Scope Footer Relocation Phase 6 Full-Corpus QA Review

## Purpose

This artifact closes Phase 6 of the Reader Scope footer relocation plan. It
records full-corpus QA for the 17 reviewed publication page stacks after Phases
2 through 5 moved every visible `Reader scope` block to the bottom hook directly
above the authority footer.

## Corpus Result

| Check | Result |
| --- | --- |
| Reviewed publication rows | 17 |
| Source specs present | 17 of 17 |
| GitHub-facing Markdown pages present | 17 of 17 |
| Tracked HTML pages present | 17 of 17 |
| Markdown `## Reader Scope` sections | 17 of 17, exactly one per page |
| Markdown authority-footer markers | 17 of 17, exactly one per page |
| HTML `reader_scope` hooks | 17 of 17, exactly one per page |
| HTML `authority_footer` hooks | 17 of 17, exactly one per page |
| Duplicate top-positioned Reader Scope text | 0 found |
| Mermaid source blocks in publication corpus | 0 |
| Inline SVG render step required | No |
| Desktop screenshots captured | 17 of 17 at 1440 px viewport width |
| Mobile screenshots captured | 17 of 17 at 390 px viewport width |

## Placement Finding

The full-corpus placement audit confirms that each GitHub-facing Markdown page
uses `## Reader Scope` immediately before `<!-- explainer-control:
authority_footer -->`, and each tracked HTML page uses a
`data-explainer-control="reader_scope"` section immediately before
`<footer data-explainer-control="authority_footer">`. No duplicate
`Reader scope:` text remains above the bottom section in the audited pages.

## Regeneration Finding

No canonical bulk HTML renderer was required for this packet because the page
content already satisfied the locked relocation pattern. Phase 6 therefore did
not invent a renderer path, run browser-side Mermaid, use a network runtime, or
rewrite public page prose. It refreshed publication evidence paths, screenshot
artifacts, and generated memory/wiki/registry derivatives through the approved
bootstrap path.

## Screenshot Evidence

| Page | Placement verdict | Desktop evidence | Mobile evidence |
| --- | --- | --- | --- |
| `technical-requirements` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/technical-requirements-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/technical-requirements-mobile.png` |
| `roles-and-skills` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/roles-and-skills-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/roles-and-skills-mobile.png` |
| `memory-system` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/memory-system-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/memory-system-mobile.png` |
| `validator-operator-workflow` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/validator-operator-workflow-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/validator-operator-workflow-mobile.png` |
| `documentation-curator-publication-process` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/documentation-curator-publication-process-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/documentation-curator-publication-process-mobile.png` |
| `project-system-improvement` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/project-system-improvement-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/project-system-improvement-mobile.png` |
| `parent-child-synthesis` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/parent-child-synthesis-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/parent-child-synthesis-mobile.png` |
| `role-routing` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/role-routing-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/role-routing-mobile.png` |
| `research-agent-workflow` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/research-agent-workflow-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/research-agent-workflow-mobile.png` |
| `director-agentjob-lifecycle` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/director-agentjob-lifecycle-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/director-agentjob-lifecycle-mobile.png` |
| `claim-gates` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/claim-gates-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/claim-gates-mobile.png` |
| `gr-derivation-roadmap` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/gr-derivation-roadmap-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/gr-derivation-roadmap-mobile.png` |
| `aether-flow-ontology` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/aether-flow-ontology-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/aether-flow-ontology-mobile.png` |
| `exact-gr-benchmark-boundary` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/exact-gr-benchmark-boundary-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/exact-gr-benchmark-boundary-mobile.png` |
| `aether-flow-physics-program` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/aether-flow-physics-program-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/aether-flow-physics-program-mobile.png` |
| `project-overview` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/project-overview-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/project-overview-mobile.png` |
| `source-authority` | PASS | `research_control/tasks/RT-20260619-017/artifacts/screenshots/source-authority-desktop.png` | `research_control/tasks/RT-20260619-017/artifacts/screenshots/source-authority-mobile.png` |

## Readability Sample

Manual visual sampling checked `project-overview` at desktop width and
`technical-requirements` at mobile width. Both samples show the Reader Scope
block above the footer authority paragraph, with no visible overlap or lost
footer flow. The sample is not treated as aesthetic certification; it is a QA
receipt paired with deterministic validation and full screenshot capture.

## Authority Boundary

This QA packet does not make GitHub-facing Markdown, tracked HTML, screenshots,
wiki notes, semantic extracts, Obsidian mirrors, SQLite memory rows, or local
caches authoritative. The registered source specs, publication briefs, and
registries keep their existing authority roles. Validator PASS means the
governed publication and control checks passed; it does not certify physics
truth, ontology promotion, benchmark promotion, role authority, or editorial
perfection.

## Conclusion

Phase 6 completes the Reader Scope footer relocation closure packet for the
reviewed 17-page publication corpus. All publication-brief registry rows now
point to this full-corpus QA artifact and the current Phase 6 screenshot set.

## Source Materials

AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy].

AEther-Flow Project. (2026).
`research_control/design/documentation_curator_reader_scope_footer_relocation_plan.md`
[Reader Scope footer relocation plan].

AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv`
[Publication brief registry].

AEther-Flow Project. (2026). `scripts/validate_publication_process.py`
[Publication-process validator].

AEther-Flow Project. (2026).
`scripts/project_control/audit_documentation_surfaces.py`
[Documentation-surface audit].
