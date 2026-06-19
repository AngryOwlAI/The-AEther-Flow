<!-- authority: explanatory -->

# Post-Migration Quality Plan Audit

## Scope

This audit records the planning-only transaction for the Documentation Curator
post-migration quality plan.

## User Requirements Covered

| Requirement | Plan coverage |
| --- | --- |
| Move generated-noncanonical warning paragraphs to the footer. | Covered in "Required Presentation Change" with separate Markdown and HTML placement rules. |
| Make top topic/functionality descriptions more detailed. | Covered in "Expanded Description Standard" and the page-by-page matrix. |
| Decide where diagrams are beneficial. | Covered in "Diagram Standard", phased implementation, and page-by-page diagram decisions. |
| Re-examine each page's topic/functionality before modifying it. | Covered in Phase 0 audit and the per-page function-to-re-check column. |
| Implement in phases because the corpus is large. | Covered in Phases 0-6 grouped by function and authority risk. |

## Boundary Check

No public explainer page was edited in this transaction. The following paths
remain out of scope until explicit future approval:

- `github-facing/*-explainer.md`
- `html/*-explainer.html`
- `markdown/html-explainer-specs/*-explainer.md`
- `markdown/publication-briefs/*.publication-brief.md`

## Diagram Observation

The current migrated corpus does not contain Mermaid blocks in the
GitHub-facing or source-spec files inspected for this task. Diagram work will
therefore require deliberate source-spec and Markdown additions in future
packets, followed by governed HTML rendering.

## Recommended Next Step

Run Phase 0 from
`research_control/design/documentation_curator_post_migration_quality_plan.md`:
build a page-by-page audit artifact before changing contracts, validators,
source specs, GitHub-facing Markdown, or tracked HTML.
