---
title: "Source Authority And Generated Derivatives"
purpose: "Explain which repository surfaces carry authority and which are derivative or retrieval aids."
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
claim_boundary: "Human-only publication explainer for Source Authority And Generated Derivatives. It teaches authority boundaries without creating physics claims, control authority, role authority, routing behavior, validator authority, write permissions, or generated-output authority."
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
reference, not a universal atlas page.

## Source Basis

- `AGENTS.md` defines the authority hierarchy and generated-output boundaries.
- `.codex/skills/project-memory-system/SKILL.md` explains memory, registry,
  wiki, and derivative refresh behavior.
- `.codex/skills/html-visual-explainer/SKILL.md` defines tracked HTML
  publication boundaries.
- The Markdown, HTML, wiki, and file-object registries provide concrete
  examples of source and derivative rows.

## Required Reader Outcome

After reading, a contributor or external AI reader should know which surfaces
can be cited as authority, which are reader aids, and what to inspect before
editing or summarizing project knowledge.

## Visual Strategy

Use an authority matrix and failure-mode checklist. Do not use a generic
source-to-validation flow. A diagram is not required.

## Acceptance Criteria

- Opens with the trust-boundary question.
- Makes the authority ladder concrete through source rows and examples.
- Separates generated/readable from canonical/authoritative.
- HTML is standalone, no-network, and mobile-safe.
- GitHub Markdown is readable without opening the HTML page.
