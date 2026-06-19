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

Use `markdown/publication-briefs/memory-system.publication-brief.md` as the
page-specific editorial contract. The page is a reference catalog for the
memory and retrieval system. It is not a memory-system implementation packet,
registry schema change, validator change, routing change, role change, or
physics continuation.

## Source Basis

- `AGENTS.md` defines the repository authority hierarchy and the rule that
  generated artifacts may be read but are not independent authority.
- `.codex/skills/project-memory-system/SKILL.md` defines the bootstrap,
  validate-only, docs-only, docs-validate-only, strict-docs, and cleanup
  commands for generated memory, wiki, registry, and derivative artifacts.
- `.codex/skills/obsidian-wiki/SKILL.md` defines the Obsidian vault,
  content-semantic extraction, vault sync, lint, and query commands while
  stating that local vault and memory-index surfaces are retrieval layers.
- `registries/MARKDOWN_SOURCE_REGISTRY.csv` gives registered Markdown source
  rows for front-door documentation, source specs, publication briefs, roles,
  skills, and project-control notes.
- `registries/TEX_SOURCE_REGISTRY.csv` gives registered TeX rows for physics
  and derivational source material.
- `registries/HTML_EXPLAINER_REGISTRY.csv` gives generated HTML rows and
  binds each tracked HTML page back to its Markdown source spec.
- `registries/WIKI_ARTIFACT_REGISTRY.csv` gives generated wiki-note rows and
  their source-object hashes.
- `registries/OBSIDIAN_VAULT_REGISTRY.csv` gives local generated Obsidian
  note and raw mirror paths.
- `registries/CONTENT_SEMANTIC_REGISTRY.csv` gives deterministic semantic
  extraction rows used for local agent retrieval.
- `FOLDER_MAP.md` classifies `wiki/` as generated derivative and `.local/` as
  local retrieval.

## Required Reader Outcome

After reading, an operator should know that memory lookup is a navigation
step. A memory hit must lead to inspection of the canonical source path and
the relevant registry row before routing, editing, citing, or summarizing
project knowledge.

## Visual Strategy

Use a layered architecture showing canonical sources, control registries,
generated derivatives, and local retrieval layers. Add a source matrix that
states what each surface can be used for. Add a query workflow panel and a
stale-local-retrieval troubleshooting section.

## Acceptance Criteria

- Explains the source-first memory principle.
- Explains registry rows as canonical routing, provenance, generated-output,
  and memory metadata.
- Explains generated wiki notes as derivative metadata.
- Explains Obsidian, semantic extracts, SQLite, and `.local` retrieval as
  local non-authority layers.
- Explains memory preflight requirements for future AgentJobs.
- Explains freshness warnings as retrieval warnings rather than source
  authority.
- Explains bootstrap regeneration boundaries and validate-only limits.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.
