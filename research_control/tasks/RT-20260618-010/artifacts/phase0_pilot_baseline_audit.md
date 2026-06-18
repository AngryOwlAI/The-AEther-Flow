<!-- authority: control -->

# Phase 0 Pilot Baseline Audit

## Scope

Task `RT-20260618-010` implements Phase 0 of
`research_control/design/documentation_curator_corpus_migration_plan.md`.
Phase 0 is a maintenance baseline, not a migration packet.

## Phase 0 Requirements

| Requirement | Evidence | Status |
| --- | --- | --- |
| Preserve both reviewed pilot pages as the quality bar. | `PB-PROJECT-OVERVIEW` and `PB-SOURCE-AUTHORITY` remain the only rows in `registries/PUBLICATION_BRIEF_REGISTRY.csv`; both have `migration_status=reviewed` and `review_status=pilot_review_pass`. | Pass |
| Do not broaden the pilot into automatic corpus migration. | No new publication brief, GitHub-facing Markdown, or tracked HTML page was created in this transaction. | Pass |
| Keep `approval_required_before_corpus_migration` set to `true`. | Both publication brief registry rows retain `approval_required_before_corpus_migration=true`. | Pass |
| Repair either pilot if drift is detected. | Strict publication validation passed for both pilot pages; no repair was required. | Pass |

## Pilot Baseline Inventory

| Pilot | Brief | Source Spec | GitHub Markdown | HTML | Review Evidence |
| --- | --- | --- | --- | --- | --- |
| Project Overview | `markdown/publication-briefs/project-overview.publication-brief.md` | `markdown/html-explainer-specs/project-overview-explainer.md` | `github-facing/project-overview-explainer.md` | `html/project-overview-explainer.html` | `research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md` |
| Source Authority And Generated Derivatives | `markdown/publication-briefs/source-authority.publication-brief.md` | `markdown/html-explainer-specs/source-authority-explainer.md` | `github-facing/source-authority-explainer.md` | `html/source-authority-explainer.html` | `research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md` |

## Screenshot Evidence

The Phase 0 baseline preserves the existing screenshot QA evidence:

- `research_control/tasks/RT-20260618-007/artifacts/screenshots/project-overview-desktop.png`
- `research_control/tasks/RT-20260618-007/artifacts/screenshots/project-overview-mobile.png`
- `research_control/tasks/RT-20260618-007/artifacts/screenshots/source-authority-desktop.png`
- `research_control/tasks/RT-20260618-007/artifacts/screenshots/source-authority-mobile.png`

## Validation Evidence

The strict publication validator reported:

```text
Publication process validation PASS
- checked_briefs: 2
- checked_html_runtime: 2
- checked_migrated_surfaces: 2
```

## Boundary Statement

This Phase 0 transaction creates a control receipt only. It does not create a
new public page, does not create a publication brief, does not revise the
reviewed pilot pages, does not authorize Phase 1, and does not change physics
claim authority.

## Logical Next Step

The next migration action remains gated: obtain explicit approval for a
bounded packet before creating new publication briefs or public page outputs.
