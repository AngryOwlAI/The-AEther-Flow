<!-- authority: control -->

# Corpus Migration Plan Audit

## Scope

Task `RT-20260618-009` created a phased Documentation Curator corpus migration
plan after the publication-process pilot and retired-process cleanup.

The task added:

- `research_control/design/documentation_curator_corpus_migration_plan.md`
- an index entry in `research_control/design/README.md`
- control registry rows for the bounded transaction
- generated memory/wiki derivative refreshes through bootstrap

## Requirement Coverage

| Requirement | Evidence | Status |
| --- | --- | --- |
| Create a detailed migration plan. | `research_control/design/documentation_curator_corpus_migration_plan.md` | Pass |
| Phase migration by project functionality. | Plan sections Phase 0 through Phase 6 and corpus coverage matrix. | Pass |
| Decide what GitHub-facing Markdown must cover. | Each page dossier includes a GitHub-facing Markdown coverage list. | Pass |
| Decide what tracked HTML must cover. | Each page dossier includes an HTML coverage list and visual strategy. | Pass |
| Preserve publication-brief process. | Plan requires briefs and `registries/PUBLICATION_BRIEF_REGISTRY.csv`. | Pass |
| Avoid corpus-wide migration in this transaction. | Plan stops at recommendation and requires explicit approval for Phase 1A. | Pass |
| Avoid retired process fallback. | Plan retires the old teaching-loop page name and Visual Atlas process page. | Pass |
| Preserve source authority and claim boundaries. | Plan includes surface rules, stop conditions, and page-level acceptance emphasis. | Pass |

## Boundary Statement

This transaction creates planning authority only. It does not create new public
HTML or GitHub-facing Markdown pages, does not add publication briefs, does not
promote physics claims, and does not authorize corpus-wide migration.

## Recommended Next Action

Authorize Phase 1A as a separate bounded packet if the next migration step is
desired:

1. `exact-gr-benchmark-boundary-explainer`
2. `aether-flow-physics-program-explainer`
