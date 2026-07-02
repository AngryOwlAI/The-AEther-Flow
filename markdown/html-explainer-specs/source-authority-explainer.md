---
title: "Source Authority And Generated Derivatives"
purpose: "Explain which repository surfaces carry authority, which surfaces are derivative or local retrieval aids, and what must be inspected before citing, editing, or routing work."
audience: "Contributors, maintainers, research agents, reviewers, and external AI readers."
output_path: "html/source-authority-explainer.html"
github_markdown_output_path: "github-facing/source-authority-explainer.md"
wiki_output_path: "wiki/html/html-source-authority-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/source-authority.publication-brief.md"
document_type: "comparison_or_boundary_map"
visual_strategy: "source_matrix"
migration_status: "reviewed"
source_materials:
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "registries/WIKI_ARTIFACT_REGISTRY.csv"
  - "registries/FILE_OBJECT_REGISTRY.csv"
claim_boundary: "Human-only publication explainer for Source Authority And Generated Derivatives. It teaches source-authority and derivative-surface boundaries without creating physics claims, control authority, role authority, routing behavior, validator authority, write permissions, or generated-output authority."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Source Authority And Generated Derivatives Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/source-authority.publication-brief.md` as the
page-specific editorial contract. The page is a boundary map and trust
reference under Phase 5 of
`research_control/design/documentation_curator_post_migration_quality_plan.md`.
It improves source-authority clarity, source-to-derivative visualization, and
footer-authority placement without changing the authority hierarchy.

## Source Basis

- `AGENTS.md`: authority hierarchy, generated-output boundaries,
  research-control continuation rules, project-system improvement boundaries,
  and generated-output editing rules.
- `.codex/skills/project-memory-system/SKILL.md`: memory, registry, wiki,
  bootstrap, validate-only, and generated-derivative refresh behavior.
- `.codex/skills/html-visual-explainer/SKILL.md`: tracked HTML publication
  boundaries, source-spec authority, and direct HTML-only edit restrictions.
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`: concrete rows for registered
  Markdown sources, source specs, role and skill contracts, and generated
  GitHub-facing Markdown derivatives.
- `registries/HTML_EXPLAINER_REGISTRY.csv`: generated HTML rows bound to
  source specs and source-basis hashes.
- `research_control/design/public_status_table_source_spec.md`: canonical
  public status table source spec for public status renderings; generated
  HTML and GitHub-facing Markdown may render it but cannot override its
  tracked source basis.
- `registries/WIKI_ARTIFACT_REGISTRY.csv`: generated wiki-note rows and
  source-object hash bindings.
- `registries/FILE_OBJECT_REGISTRY.csv`: generated file object index rows used
  for local discovery and routing support.

## Required Reader Outcome

After reading, a contributor or external AI reader should be able to answer the
trust question: which file or registry row can define the project state for the
claim being made? The reader should know that generated pages, wiki notes,
semantic extracts, Obsidian mirrors, PDFs, and `.local` caches can support
navigation only after they are traced back to registered sources.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: source-authority orientation only. This page cannot change the
hierarchy, replace a registry, promote ontology, certify a benchmark, issue a
Gate Chair verdict, expand roles, or modify routing behavior.

## Visual Strategy

Use a source-authority ladder and source-to-derivative boundary map. The visual
must make the canonical-versus-derivative distinction obvious: TeX, registries,
and registered Markdown define their lanes; GitHub-facing Markdown, tracked
HTML, wiki notes, PDFs, semantic extracts, Obsidian mirrors, and `.local`
caches help readers or agents navigate back to those lanes. Do not use a
generic validation flow, browser-side Mermaid, remote assets, or external
runtime packages.

## Acceptance Criteria

- Opens with the trust-boundary problem before the full authority paragraph.
- Adds a page-specific authority ladder or source-to-derivative visual.
- Names concrete source surfaces, generated surfaces, and local retrieval
  surfaces.
- Explains that public status renderings must trace back to
  `research_control/design/public_status_table_source_spec.md`,
  `registries/DISTANCE_TO_GR_LEDGER.csv`, and row-specific evidence paths
  before citing `M_src`, `g_eff`, matter-coupling evidence, Einstein-equation
  status, or benchmark status.
- Uses the bottom Reader Scope hook immediately above the marked authority
  footer in GitHub Markdown and tracked HTML.
- Moves the full generated-noncanonical paragraph to the marked authority
  footer in GitHub Markdown and tracked HTML.
- Preserves generated noncanonical status and source authority boundaries.
- Does not change validators, commands, schemas, role contracts, skill
  contracts, routing behavior, checkpoint behavior, generated-output authority,
  or physics claim status.
- Uses screenshot QA and before/after review evidence for the changed HTML
  derivative.
