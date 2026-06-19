---
title: "Documentation Curator Publication Process"
purpose: "Explain how AEther-Flow public pages are planned, briefed, written, reviewed, and checked under the active Documentation Curator publication process."
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
claim_boundary: "Human-only publication explainer for Documentation Curator Publication Process. It explains brief-first planning, page-local document types, medium-specific GitHub Markdown and HTML output, visual strategy, pilot discipline, screenshot QA, review evidence, retired-process boundaries, and deterministic publication checks without changing role authority, validator behavior, schemas, routing, checkpoint gates, source authority, generated-output authority, corpus-migration approval, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Documentation Curator Publication Process Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/documentation-curator-publication-process.publication-brief.md` as the page-specific editorial contract. The page is a
workflow guide under the post-migration Phase 4 quality
packet. It improves reader orientation, footer-authority placement, and
page-specific operational structure without changing executable project
behavior or physics claim status.

## Source Basis

- `research_control/design/documentation_curator_publication_process.md`: Active publication standard and pilot discipline.
- `.agents/roles/research_ops/documentation-curator.v2.0.0.md`: Documentation Curator role mission, document types, and boundaries.
- `markdown/publication-briefs/README.md`: Publication brief quality guidance and rejected patterns.
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`: Reviewed page registry and evidence paths.
- `scripts/validate_publication_process.py`: Mechanical publication checks and known anti-pattern guards.
- `research_control/tasks/RT-20260618-007/artifacts/publication_process_requirement_audit.md`: Evidence for replacing the old process.
- `research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md`: Pilot review evidence for Project Overview and Source Authority.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the existing
Documentation Curator Publication Process function, which source paths ground it, which adjacent systems
it connects to, and which authority boundary prevents overread. The reader
should be able to use the page as orientation, then inspect the named source
files, registries, task records, role or skill contracts, AgentJob allowlists,
completion records, and checks before acting.

## Visual Strategy

Use page-specific operational structure rather than a reusable template. The
main reader sections are `Publication Lifecycle`, `Brief And Medium Split`, `Review Evidence`, `Retired Paths`. The HTML derivative may render these
as local CSS cards and tables; the GitHub Markdown derivative should remain a
native article with compact tables. Do not use browser-side Mermaid, remote
assets, or external runtime packages.

## Acceptance Criteria

- Opens with subject-specific operational explanation before the full authority paragraph.
- Moves the full generated-noncanonical paragraph to the marked authority footer in GitHub Markdown and tracked HTML.
- Includes visible source paths in both public derivatives.
- Preserves generated noncanonical status and source authority boundaries.
- Does not change validators, commands, schemas, role contracts, skill contracts, routing behavior, checkpoint behavior, generated-output authority, or physics claim status.
- Uses screenshot QA and before/after review evidence for the changed HTML derivative.
