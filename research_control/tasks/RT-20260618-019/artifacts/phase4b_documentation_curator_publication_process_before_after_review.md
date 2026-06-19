<!-- authority: control -->

# Phase 4B Documentation Curator Publication Process Review

## Scope

Task `RT-20260618-019` migrated one public Documentation Curator publication
page:

- `documentation-curator-publication-process-explainer`

The packet did not edit canonical science, ontology, role contracts, schemas,
validators, routing behavior, signal registries, checkpoint behavior, or
physics claim status.

## Before

The active publication-process corpus had Phase 4A project-system improvement
coverage, but no public page explained the publication process itself as a
reader-facing workflow. The underlying process existed in control documents,
role contracts, validator code, and pilot evidence. A maintainer had to read
several control surfaces to understand how a page moves from brief to reviewed
public derivative.

## After

| Page | Improvement | Boundary Preserved |
| --- | --- | --- |
| Documentation Curator Publication Process | Explains brief-first planning, page-local document types, medium-specific GitHub Markdown and HTML outputs, reader-specific visuals, pilot-first approval discipline, screenshot QA, before/after review evidence, retired-process anti-patterns, and validator limits. | Does not change validator behavior, role authority, schemas, routing, checkpoint gates, source authority, generated-output authority, corpus-migration approval, or physics claim status. |

## Review Findings

- The page opens with the subject and reader problem, not source metadata.
- The page states generated noncanonical status early.
- The GitHub-facing Markdown reads as a native workflow guide rather than an
  HTML transcript.
- The HTML derivative uses a publication lifecycle timeline, document-type
  palette, medium-specific output comparison, review checklist, and retired
  anti-pattern panel.
- The page explicitly states that deterministic checks catch mechanical
  failures and retired patterns but do not certify editorial quality by
  themselves.
- Source materials are named visibly in APA 7 style.
- HTML is standalone, no-network, and readable without JavaScript.

## Remaining Risks

- `.local` Obsidian and memory-index freshness warnings may remain after
  bootstrap. These are retrieval-layer warnings and not source authority.
- This page explains existing publication-process behavior; it intentionally
  does not repair future validator or operator command gaps. Phase 4C remains
  the planned validator-operator surface.

## Recommendation

Seek explicit approval before Phase 4C:
`validator-operator-workflow-explainer`.
