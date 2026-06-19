---
title: "Project Overview"
purpose: "Orient a new reader to AEther-Flow's two missions, authority spine, and first reading path without changing project authority."
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
claim_boundary: "Human-only publication explainer for Project Overview. It orients readers without creating physics claims, role authority, routing behavior, validator authority, write permissions, or generated-output authority."
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
page-specific editorial contract. The page is an overview article, not an atlas
template.

## Source Basis

- `README.md` establishes the public front-door project description.
- `AGENTS.md` defines source authority, generated-output boundaries, and
  controlled continuation discipline.
- `research_control/README.md` grounds the research-control lane.
- `research_control/design/documentation_curator_publication_process.md`
  defines the new publication process.

## Required Reader Outcome

After reading, a new reader should know that AEther-Flow has a physics research
mission and an AI research-agent workflow mission, and that both are governed
by a source-first authority spine. The page should help the reader choose
their first source path without implying the explainer itself is authority.

## Visual Strategy

Use a source matrix and reading-path layout. Do not use a generic system map or
a diagram that could apply to any documentation page.

## Acceptance Criteria

- Opens with subject framing before metadata.
- Uses a page-specific article structure.
- Makes source authority and derivative status visible.
- HTML is standalone, no-network, and mobile-safe.
- GitHub Markdown is readable without opening the HTML page.
