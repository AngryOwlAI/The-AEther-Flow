# Memory System Spec

## Rendering Intent

Create a tracked HTML drilldown for the project memory system. The page should
avoid saying the project has competing wikis. The correct model is one
source-first memory system with multiple retrieval surfaces:

- `registries/*.csv`: canonical memory spine for object identity, provenance,
  routing, hashes, ownership, validation, and generated-output binding.
- `wiki/`: tracked generated wiki notes and indexes for repo-visible
  navigation.
- `.local/obsidian/aether-flow-wiki/`: local generated Obsidian reader vault;
  useful, noncanonical, and machine-local.
- `.local/content_semantics/` and `.local/memory_index/memory.sqlite`:
  agent-queryable semantic/search layer and local query surface.

## Required Visual Structure

- Source-backed coverage rows: render `Source-Backed Coverage` content blocks
  as full-width horizontal rows rather than narrow multi-column cards. Tables
  must use readable auto layout, with any wide overflow scoped inside the
  content block instead of the page body.
- Layered map from canonical CSV spine to generated tracked wiki to local
  Obsidian vault to semantic/query surfaces.
- Regeneration workflow showing source edit -> bootstrap -> wiki/registry rows
  -> content semantics -> vault sync -> SQLite query surface.
- Authority boundary panels distinguishing canonical source/registry rows from
  generated retrieval layers.
- Workflow step inspector for regeneration and validation commands.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Required Diagrams

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

## Source-Backed Summary

Summary heading: `Summary of Memory System`

Summary text:

The memory system is the repository's source-first retrieval and derivative-
generation layer for registered Markdown, TeX, PDFs, HTML explainers, wiki
notes, semantic extracts, file objects, and local query surfaces. Its
functionality is to turn canonical registries and source files into generated
wiki pages, source hashes, object relationships, local Obsidian vault entries,
semantic text extracts, and SQLite-backed lookup surfaces without letting any
generated artifact become an independent source of claims. It matters because
humans and agents need fast ways to find evidence, but retrieval convenience
must not bypass the authority hierarchy. The system fits the project by
connecting source edits to bootstrap regeneration, validation receipts,
content semantics, and local reading aids while preserving clear provenance.

Summary source basis:

- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/obsidian-wiki/SKILL.md`

## Required Content Blocks

- subject_summary: Summarize the memory system, its source-first registry spine, why many retrieval surfaces still form one system, and which declared sources ground the summary.
- csv_memory_spine: A completed explanation of format-specific CSV registries as canonical memory rows for identity, routing, provenance, generated outputs, and agent-queryable relationships.
- tracked_generated_wiki: A source-backed section explaining tracked generated wiki notes and indexes as repo-visible derivatives that summarize registered sources without becoming independent authority.
- local_obsidian_vault: A documentation section for `.local/obsidian/aether-flow-wiki/` as a local reader vault and operator aid that can be regenerated and must not override tracked source state.
- semantic_query_layer: A completed explanation of `.local/content_semantics/`, `.local/memory_index/memory.sqlite`, and query scripts as retrieval surfaces that point back to canonical registry objects.
- authority_boundaries: A visible boundary section explaining source-first authority, generated-output refresh, stale derivative risks, validation checks, and why competing retrieval views remain subordinate to the same canonical spine.
