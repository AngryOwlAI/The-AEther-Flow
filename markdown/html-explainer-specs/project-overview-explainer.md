---
title: "Project Overview"
purpose: "Orient a new reader to AEther-Flow's two missions, authority spine, publication atlas, and first reading path without changing project authority."
audience: "New technical readers, maintainers, research agents, reviewers, and external AI readers."
output_path: "html/project-overview-explainer.html"
github_markdown_output_path: "github-facing/project-overview-explainer.md"
wiki_output_path: "wiki/html/html-project-overview-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/project-overview.publication-brief.md"
document_type: "overview_article"
visual_strategy: "source_matrix"
migration_status: "reviewed"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/design/documentation_curator_publication_process.md"
claim_boundary: "Human-only publication explainer for Project Overview. It orients readers to the physics research lane, the research-agent workflow lane, the source-authority spine, and first-reading routes without creating physics claims, role authority, routing behavior, validator authority, write permissions, or generated-output authority."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Project Overview Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/project-overview.publication-brief.md` as the
page-specific editorial contract. The page is an overview article under Phase
5 of `research_control/design/documentation_curator_post_migration_quality_plan.md`.
It improves first-entry orientation, cross-page routing, and footer-authority
placement without changing project behavior or physics claim status.

## Source Basis

- `README.md`: public front-door description, two-track project framing,
  current exact-GR benchmark discipline, open derivation burden, and
  research-agent system overview.
- `AGENTS.md`: source hierarchy, generated-output boundaries, research-control
  continuation rules, project-system improvement rules, and generated-output
  boundaries.
- `research_control/README.md`: Director decisions, AgentJobs, role records,
  memory preflight, one-job rule, and documentation-impact gate.
- `research_control/design/documentation_curator_publication_process.md`:
  publication brief, source spec, GitHub Markdown, tracked HTML, review, and
  validation discipline.

## Required Reader Outcome

After reading, a new reader should understand that AEther-Flow has two linked
missions: a physics program with exact-GR benchmark discipline and an open
substrate derivation burden, and a governed research-agent workflow that makes
theoretical and documentation work auditable. The reader should know that the
overview page is a route map, not authority, and should be able to choose the
next page family or canonical source lane before summarizing claims or changing
files.

## Visual Strategy

Use a compact first-entry route map plus a source matrix. The route map must be
specific to AEther-Flow's two missions, source authority, research control,
and publication pages; it must not become a generic validation or
source-to-output diagram. The HTML derivative may render the route map as local
CSS cards and connectors. The GitHub Markdown derivative should keep the map
as a native Markdown table/list. Do not use browser-side Mermaid, remote
assets, or external runtime packages.

## Acceptance Criteria

- Opens with subject-specific project orientation before the full authority
  paragraph.
- Moves the full generated-noncanonical paragraph to the marked authority
  footer in GitHub Markdown and tracked HTML.
- Points readers to the correct page family and source lane without making the
  overview page itself authoritative.
- Preserves exact-GR benchmark versus open derivation language.
- Preserves generated noncanonical status and source authority boundaries.
- Does not change validators, commands, schemas, role contracts, skill
  contracts, routing behavior, checkpoint behavior, generated-output authority,
  or physics claim status.
- Uses screenshot QA and before/after review evidence for the changed HTML
  derivative.
