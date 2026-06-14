# Memory System

This page explains the repository memory model: one source-first system with several retrieval surfaces, not competing wikis.

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/memory-system-explainer.md`
- **Related HTML:** `html/memory-system-explainer.html`
- **Authority status:** `generated_noncanonical`

## What This Feature Does

The memory system turns registered sources and registries into generated wiki notes, indexes, content semantics, file-object rows, Obsidian vault entries, SQLite query data, and local search surfaces.

## Why The Project Needs It

Humans and agents need fast retrieval, but retrieval convenience cannot authorize claims. The system preserves provenance so every generated note, semantic extract, and local view points back to canonical sources or registry rows.

## How It Works

Memory lifecycle:

`source edit or registry row` -> `bootstrap_memory_system.py` -> format registries and hashes -> generated wiki notes -> content-semantic extracts -> local Obsidian vault -> SQLite/query surface -> validation.

What memory can retrieve: paths, summaries, generated notes, source hashes, object relationships, content extracts, and local query results. What memory cannot authorize: physics promotion, control decisions, role permissions, or generated-output authority.

## What It Is Not

It is not a second source of truth, not a competing wiki hierarchy, not a replacement for registries, and not a reason to trust stale `.local/` content over tracked files.

## Diagram Reading Guide

The surface map shows registered sources and registries feeding tracked wiki, file registry, local Obsidian, semantic extracts, SQLite, and query tools. The regeneration flow shows the order of refresh; arrows mean derivation and retrieval, not authority transfer.

<!-- mermaid-diagram-id: memory-surface-map -->
```mermaid
flowchart TD
  Sources["Registered sources<br/>TeX and Markdown"] --> Registries["registries/*.csv<br/>canonical memory spine"]
  Registries --> Wiki["wiki/<br/>tracked generated notes and indexes"]
  Registries --> FileRegistry["FILE_OBJECT_REGISTRY.csv<br/>generated query surface"]
  Wiki --> Obsidian[".local/obsidian/aether-flow-wiki/<br/>local reader vault"]
  Sources --> Semantics[".local/content_semantics/<br/>semantic extracts"]
  Registries --> Semantics
  Semantics --> SQLite[".local/memory_index/memory.sqlite<br/>local query index"]
  Obsidian --> Query["query_memory.py<br/>lookup and search"]
  SQLite --> Query
```

<!-- mermaid-diagram-id: memory-regeneration-flow -->
```mermaid
flowchart TD
  Edit["Edit canonical source or registry"] --> Bootstrap["bootstrap_memory_system.py"]
  Bootstrap --> FormatRegistries["Format registries and hashes"]
  FormatRegistries --> WikiNotes["Generated wiki notes"]
  FormatRegistries --> Master["FILE_OBJECT_REGISTRY.csv"]
  WikiNotes --> Semantics["extract_content_semantics.py"]
  Master --> Semantics
  Semantics --> Vault["sync_obsidian_vault.py"]
  Vault --> Index["memory.sqlite"]
  Index --> Query["query_memory.py"]
  Query --> Validate["make validate-memory"]
```

## Source Authority

The memory spine is grounded in Markdown, TeX, PDF, HTML, wiki, content-semantic, and file registries plus the project-memory, wiki, PDF, HTML, and Obsidian skills.

## External AI Navigation Card

You are reading a non-authoritative GitHub-facing explainer.

Safe uses:
- summarize this feature for orientation
- identify source files to inspect next
- explain workflow boundaries

Before modifying project knowledge:
- read `AGENTS.md`
- inspect the relevant registry rows
- inspect the relevant source spec or canonical source file
- route through the correct research-control workflow

Do not:
- do not treat this page as physics authority
- do not claim the Æther-flow derivation is complete
- do not treat generated HTML, wiki, PDF, or `.local/` files as independent authority
- do not bypass claim gates, validators, or AgentJob boundaries

## Where To Go Next

- Run bootstrap after source or registry edits.
- Treat wiki and Obsidian notes as generated reading aids.
- Use source hashes and registry rows to detect stale derivatives.
- Cite source paths, not local retrieval convenience.

## All Source Materials

- `README.md`
- `AGENTS.md`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/PDF_DERIVATIVE_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `registries/WIKI_ARTIFACT_REGISTRY.csv`
- `registries/CONTENT_SEMANTIC_REGISTRY.csv`
- `registries/FILE_OBJECT_REGISTRY.csv`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/markdown-wiki/SKILL.md`
- `.codex/skills/tex-wiki/SKILL.md`
- `.codex/skills/pdf-derivative-build/SKILL.md`
- `.codex/skills/html-visual-explainer/SKILL.md`
- `.codex/skills/obsidian-wiki/SKILL.md`
