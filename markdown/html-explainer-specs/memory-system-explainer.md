---
title: "Memory System"
purpose: "Explain the source-first memory system: canonical CSV registries, tracked generated wiki notes, local Obsidian vault, semantic extracts, SQLite index, and query surface."
audience: "Technical but human-readable: maintainers and research agents who need to know where project memory authority lives and how retrieval surfaces are regenerated."
output_path: "html/memory-system-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/PDF_DERIVATIVE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "registries/WIKI_ARTIFACT_REGISTRY.csv"
  - "registries/CONTENT_SEMANTIC_REGISTRY.csv"
  - "registries/FILE_OBJECT_REGISTRY.csv"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/markdown-wiki/SKILL.md"
  - ".codex/skills/tex-wiki/SKILL.md"
  - ".codex/skills/pdf-derivative-build/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/obsidian-wiki/SKILL.md"
claim_boundary: "Human-only memory-system visualization. It explains existing source-first memory, registry, wiki, Obsidian, semantic, and query surfaces without changing registry authority, generated-output boundaries, routing behavior, validators, or scientific claim status."
human_visual_only: true
explainer_kind: "control_system"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "memory_system_map"
layout_intent: "Use a layered memory map: canonical CSV memory spine, tracked generated wiki surface, local Obsidian reader vault, semantic/query layer, and authority-boundary panels."
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_materials_section"
  - "workflow_step_inspector"
required_content_blocks:
  - "subject_summary"
  - "csv_memory_spine"
  - "tracked_generated_wiki"
  - "local_obsidian_vault"
  - "semantic_query_layer"
  - "authority_boundaries"
analysis_capsule_schema:
  - "premise"
  - "mechanism"
  - "source_basis"
  - "authority_status"
  - "uncertainty"
  - "validation_or_test"
  - "next_step"
mermaid_diagrams:
  required: true
  ids:
    - "memory-surface-map"
    - "memory-regeneration-flow"
---

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
This summary is grounded in the Markdown, TeX, PDF, HTML, wiki, content-
semantic, and file-object registries plus the project-memory, markdown-wiki,
tex-wiki, PDF-derivative, HTML-explainer, and Obsidian-wiki skill contracts.

Summary source basis:

- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `.codex/skills/project-memory-system/SKILL.md`
- `.codex/skills/obsidian-wiki/SKILL.md`

## Required Content Blocks

- subject_summary: Summarize the repository memory system, its source-first retrieval and regeneration function, why it matters for evidence lookup, and which declared sources ground the summary.
- csv_memory_spine: Explain format-specific CSV registries as canonical memory
  spine for IDs, provenance, source hashes, routing, ownership, and validation.
- tracked_generated_wiki: Explain `wiki/` as tracked generated repo-visible
  navigation, not independent authority.
- local_obsidian_vault: Explain `.local/obsidian/aether-flow-wiki/` as a
  generated local reader vault and optional operator environment aid.
- semantic_query_layer: Explain `.local/content_semantics/`,
  `.local/memory_index/memory.sqlite`, and `query_memory.py` as local
  agent-queryable retrieval surfaces.
- authority_boundaries: Explain source-first authority, generated-output
  boundaries, regeneration commands, validation, and stale-surface risks.

## Required Analysis Capsules

### CSV Is The Memory Spine

- premise: The repository memory system is source-first and registry-backed.
- mechanism: Format-specific CSV registries bind object identity, source path,
  source hash, generated outputs, owner skill, authority status, and validation
  status; generated surfaces are derived from those rows.
- source_basis: `AGENTS.md`, `README.md`,
  `.codex/skills/project-memory-system/SKILL.md`, and `registries/*.csv`.
- authority_status: Human-only explanation; CSV registries and registered
  sources carry authority.
- uncertainty: Generated surfaces can become stale if bootstrap or local sync
  has not been run after source changes.
- validation_or_test: Run memory bootstrap, validate-only, and `make
  validate-memory` when full local retrieval validation is in scope.
- next_step: Inspect the relevant format-specific registry row before relying
  on a wiki, vault, or semantic search result.

### Retrieval Surfaces Are Derived

- premise: Wiki, Obsidian, semantic extracts, and SQLite exist to make source
  memory easier to inspect and query.
- mechanism: Scripts regenerate tracked wiki notes, local vault files, content
  semantics, relationship graphs, and query indexes from registered sources and
  registries.
- source_basis: `.codex/skills/obsidian-wiki/SKILL.md`,
  `registries/WIKI_ARTIFACT_REGISTRY.csv`, and
  `registries/CONTENT_SEMANTIC_REGISTRY.csv`.
- authority_status: Explanation of generated noncanonical access layers.
- uncertainty: Local `.local/` surfaces may differ by machine and are not
  Git-authoritative.
- validation_or_test: Validate with `lint_obsidian_vault.py --require-index`
  and query smoke checks when local retrieval is needed.
- next_step: Treat retrieval hits as pointers back to registered source rows.

## Non-Goals

- Do not make generated wiki, Obsidian, semantic extracts, SQLite, or `.local/`
  outputs authoritative.
- Do not change memory scripts, registries, or source authority.
- Do not edit generated wiki notes by hand.
- Do not introduce physics claims.
