---
title: "Memory, Registries, Wiki, And Retrieval Surfaces"
purpose: "Explain how AEther-Flow memory, registries, generated wiki notes, semantic extracts, Obsidian mirrors, SQLite lookup, and .local retrieval relate to source authority."
audience: "Maintainers, reviewers, future agents, and external AI readers."
output_path: "html/memory-system-explainer.html"
github_markdown_output_path: "github-facing/memory-system-explainer.md"
wiki_output_path: "wiki/html/html-memory-system-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/memory-system.publication-brief.md"
document_type: "reference_catalog"
visual_strategy: "layered_architecture"
migration_status: "reviewed"
source_materials:
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/obsidian-wiki/SKILL.md"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "registries/WIKI_ARTIFACT_REGISTRY.csv"
  - "registries/OBSIDIAN_VAULT_REGISTRY.csv"
  - "registries/CONTENT_SEMANTIC_REGISTRY.csv"
  - "FOLDER_MAP.md"
claim_boundary: "Human-only publication explainer for Memory, Registries, Wiki, And Retrieval Surfaces. It explains existing source-first memory behavior, registry routing and provenance roles, generated wiki notes, content semantics, Obsidian vault mirrors, SQLite lookup, memory preflight receipts, freshness warnings, and bootstrap refresh boundaries without changing memory-system behavior, registry schema, validator behavior, routing behavior, role authority, checkpoint behavior, generated-output authority, source authority, or physics claim status."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Memory, Registries, Wiki, And Retrieval Surfaces Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/memory-system.publication-brief.md` as the page-specific editorial contract. The page is a
reference catalog under the post-migration Phase 4 quality
packet. It improves reader orientation, footer-authority placement, and
page-specific operational structure without changing executable project
behavior or physics claim status.

## Source Basis

- `AGENTS.md`: Repository authority hierarchy and generated-output boundary.
- `.codex/skills/project-memory-system/SKILL.md`: Bootstrap, validate-only, docs modes, and cleanup commands.
- `.codex/skills/obsidian-wiki/SKILL.md`: Local vault, semantic extraction, vault sync, lint, and query guidance.
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`: Registered Markdown source rows and generated outputs.
- `registries/TEX_SOURCE_REGISTRY.csv`: Registered TeX rows for physics and derivational source material.
- `registries/HTML_EXPLAINER_REGISTRY.csv`: Generated HTML rows bound to source specs.
- `registries/WIKI_ARTIFACT_REGISTRY.csv`: Generated wiki-note rows and source-object hashes.
- `registries/OBSIDIAN_VAULT_REGISTRY.csv`: Local Obsidian note and raw mirror paths.
- `registries/CONTENT_SEMANTIC_REGISTRY.csv`: Deterministic semantic extraction rows for local search.
- `FOLDER_MAP.md`: Generated folder classification for canonical, generated, local, tooling, and reserved lanes.

## Required Reader Outcome

After reading, a maintainer or future agent should understand the existing
Memory, Registries, Wiki, And Retrieval Surfaces function, which source paths ground it, which adjacent systems
it connects to, and which authority boundary prevents overread. The reader
should be able to use the page as orientation, then inspect the named source
files, registries, task records, role or skill contracts, AgentJob allowlists,
completion records, and checks before acting.

## Visual Strategy

Use page-specific operational structure rather than a reusable template. The
main reader sections are `Authority And Retrieval Layers`, `Query Workflow`, `Freshness Warnings`, `Bootstrap Boundaries`. The HTML derivative may render these
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
