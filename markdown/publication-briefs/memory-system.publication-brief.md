---
brief_id: "PB-MEMORY-SYSTEM"
subject: "Memory, Registries, Wiki, And Retrieval Surfaces"
reader: "Maintainer, reviewer, or future agent deciding how to use AEther-Flow memory, registries, wiki notes, semantic extracts, Obsidian mirrors, and local retrieval without confusing them with source authority."
reader_job: "Understand which memory-related surfaces carry routing and provenance authority, which are generated retrieval aids, how memory preflight should be used, how bootstrap refreshes derivatives, and why freshness warnings never replace canonical source inspection."
document_type: "reference_catalog"
reading_experience: "A compact source-first reference catalog with an authority layer diagram, surface matrix, query workflow, freshness-warning guidance, troubleshooting notes, and source-boundary reminders."
narrative_structure:
  - "Open with the source-first memory rule."
  - "Separate canonical sources and registry rows from generated wiki, semantic, Obsidian, SQLite, and .local retrieval layers."
  - "Show the practical query workflow: status, lookup or search, then canonical source and registry inspection."
  - "Explain bootstrap and validate-only regeneration boundaries."
  - "Close with stale-local-retrieval troubleshooting and forbidden overreads."
visual_strategy: "layered_architecture"
source_basis:
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
authority_boundaries:
  - "The page may explain existing source-first memory behavior, registry routing and provenance roles, generated wiki notes, content semantics, Obsidian vault mirrors, SQLite lookup, memory preflight receipts, freshness warnings, and bootstrap refresh boundaries."
  - "The page may not change memory-system behavior, registry schema, validator behavior, routing behavior, role authority, checkpoint behavior, generated-output authority, source authority, or physics claim status."
  - "Generated wiki notes, semantic extracts, Obsidian mirrors, SQLite indexes, and .local caches remain retrieval aids only; they are never source authority."
output_surfaces:
  - "github-facing/memory-system-explainer.md"
  - "html/memory-system-explainer.html"
acceptance_criteria:
  - "Explains the source-first memory principle."
  - "Explains registry rows as canonical routing, provenance, generated-output, and memory metadata."
  - "Explains generated wiki notes as derivative metadata."
  - "Explains Obsidian, semantic extracts, SQLite, and .local retrieval as local non-authority layers."
  - "Explains memory preflight requirements for future AgentJobs."
  - "Explains freshness warnings as retrieval warnings rather than source authority."
  - "Explains bootstrap regeneration boundaries and validate-only limits."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Promoting .local, Obsidian, semantic extracts, SQLite memory indexes, wiki notes, PDFs, HTML, or GitHub-facing Markdown to authority."
  - "Treating memory lookup as a replacement for source inspection."
  - "Hand-editing generated wiki notes or generated registry metadata sidecars."
  - "Changing memory-system scripts, registry schemas, validators, routing behavior, role authority, checkpoint gates, or physics claim status."
  - "Migrating Phase 5B, Phase 5C, or the whole corpus without separate explicit approval."
migration_status: "reviewed"
---

# Publication Brief: Memory, Registries, Wiki, And Retrieval Surfaces

This Phase 5A page is a reference catalog for the AEther-Flow memory system.
It explains how registry rows, generated wiki notes, semantic extracts,
Obsidian mirrors, SQLite lookup, and `.local` retrieval fit together without
changing memory tooling or promoting generated surfaces to authority.
