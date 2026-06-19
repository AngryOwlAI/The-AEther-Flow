---
title: "Documentation Curator Publication Process"
purpose: "Explain how AEther-Flow public pages are planned, briefed, written, reviewed, and validated under the active Documentation Curator publication process."
audience: "Maintainers, reviewers, future agents, and external AI readers."
output_path: "html/documentation-curator-publication-process-explainer.html"
github_markdown_output_path: "github-facing/documentation-curator-publication-process-explainer.md"
wiki_output_path: "wiki/html/html-documentation-curator-publication-process-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/documentation-curator-publication-process.publication-brief.md"
document_type: "workflow_guide"
visual_strategy: "process_timeline"
migration_status: "reviewed"
source_materials:
  - "research_control/design/documentation_curator_publication_process.md"
  - ".agents/roles/research_ops/documentation-curator.v2.0.0.md"
  - "markdown/publication-briefs/README.md"
  - "registries/PUBLICATION_BRIEF_REGISTRY.csv"
  - "scripts/validate_publication_process.py"
  - "research_control/tasks/RT-20260618-007/artifacts/publication_process_requirement_audit.md"
  - "research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md"
claim_boundary: "Human-only publication explainer for the AEther-Flow Documentation Curator publication process. It explains brief-first planning, page-local document types, medium-specific GitHub Markdown and HTML output, visual strategy, pilot discipline, screenshot QA, review evidence, retired-process boundaries, and deterministic publication checks without changing role authority, validator behavior, schemas, routing, checkpoint gates, source authority, generated-output authority, corpus-migration approval, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Documentation Curator Publication Process Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/documentation-curator-publication-process.publication-brief.md`
as the page-specific editorial contract. The page is a workflow guide for
publication-process operation. It does not change validators, role contracts,
schemas, routing behavior, checkpoint gates, generated-output authority, or
physics claim status.

## Source Basis

- `research_control/design/documentation_curator_publication_process.md`
  defines the active publication standard: brief-first public documentation,
  unchanged source authority, page-local document types, medium-specific output
  synchronization, pilot-first migration, deterministic publication checks, and
  rollback discipline.
- `.agents/roles/research_ops/documentation-curator.v2.0.0.md` defines the
  active Documentation Curator role, including publication briefs, document
  types, optional visuals, source authority, and boundaries.
- `markdown/publication-briefs/README.md` states that briefs are the active
  quality surface and lists rejected patterns such as universal headings,
  diagram-for-validator behavior, source metadata first, and identical
  GitHub/HTML heading requirements.
- `registries/PUBLICATION_BRIEF_REGISTRY.csv` is the active control surface
  for reviewed publication pages and their evidence paths.
- `scripts/validate_publication_process.py` supplies mechanical checks for
  brief/spec/output consistency, no-network HTML, source visibility,
  authority-boundary language, screenshot evidence, duplicate skeletons, and
  known retired-process patterns.
- `research_control/tasks/RT-20260618-007/artifacts/publication_process_requirement_audit.md`
  records the implementation evidence for replacing the old process.
- `research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md`
  records the pilot review evidence for Project Overview and Source Authority.

## Required Reader Outcome

After reading, a maintainer or future agent should know that a public page is
not created by filling a universal template. It begins with a publication
brief, binds to a source spec, produces native GitHub Markdown and standalone
HTML derivatives, receives screenshot and before/after review evidence, and is
checked by deterministic validators that protect known boundaries. The reader
should also know that validator PASS is necessary evidence for governed
publication work but not sufficient proof of editorial quality.

## Visual Strategy

Use a publication lifecycle timeline from brief to review evidence. Add a
document-type palette, a retired-path anti-pattern panel, and a source-authority
review checklist. The visual should teach how the process preserves quality
and boundaries; it must not imply that validation alone produces quality.

## Acceptance Criteria

- Explains the publication brief as quality-control surface.
- Explains document types and page-local headings.
- Explains medium-specific divergence between GitHub Markdown and HTML.
- Explains visual strategy as reader-specific and optional.
- Explains pilot-first discipline and explicit approval before new page
  packets.
- Explains screenshot QA and before/after review evidence.
- Explains retirement of Visual Atlas, topic-registry creation path, and active
  teaching-packet fallback.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
