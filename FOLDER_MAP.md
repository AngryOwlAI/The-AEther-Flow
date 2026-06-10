# Folder Map

Generated folder map. Not canonical authority. Update source files, registry rows, or folder contents, then regenerate with bootstrap.

## Source Basis

- Live repository directory tree, excluding `.git/`, `.venv/`, and `__pycache__/`.
- Source and generated CSV registries under `registries/`.
- Project authority rules in `AGENTS.md` and the memory-system bootstrap script.

## Category Key

- `canonical source`: authored source material that can carry project meaning.
- `control authority`: tracked governance, routing, validation, registry, or task-control material.
- `generated derivative`: generated human or agent reading surfaces.
- `local retrieval`: ignored local cache, vault, semantic extraction, or search layer.
- `tooling`: scripts, skills, prompts, templates, or tests.
- `reserved lane`: intentional placeholder or support lane without active registered authority.

## Folder Table

| Folder | Category | CSV Relation | Wiki Relation | Research Role |
| --- | --- | --- | --- | --- |
| `.` | `control authority` | CONTENT_SEMANTIC_REGISTRY: 39; FILE_OBJECT_REGISTRY: 156; MARKDOWN_SOURCE_REGISTRY: 4; OBSIDIAN_VAULT_REGISTRY: 39; PDF_DERIVATIVE_REGISTRY: 8; TEX_SOURCE_REGISTRY: 27; WIKI_ARTIFACT_REGISTRY: 39 | 39 generated wiki note(s) point back to sources here. | Repository front door for project identity, instructions, validation, and generated folder classification. |
| `.agents` | `control authority` | No registered object rows. | No direct generated wiki notes. | Defines permitted agent behavior and claim boundaries. |
| `.codex` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.local` | `local retrieval` | CONTENT_SEMANTIC_REGISTRY: 39; FILE_OBJECT_REGISTRY: 78; OBSIDIAN_VAULT_REGISTRY: 39 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `Step-by-step-Comments` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports local retrieval, semantic search, or ignored reference use; not tracked authority. |
| `assets` | `reserved lane` | No registered object rows. | No direct generated wiki notes. | Reserved for future project material; currently not active authority. |
| `html` | `reserved lane` | No registered object rows. | No direct generated wiki notes. | Reserved for future project material; currently not active authority. |
| `manuscripts` | `reserved lane` | No registered object rows. | No direct generated wiki notes. | Reserved for future project material; currently not active authority. |
| `markdown` | `canonical source` | FILE_OBJECT_REGISTRY: 1; MARKDOWN_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Provides authored source material used by the research workflow. |
| `ontology` | `canonical source` | FILE_OBJECT_REGISTRY: 17; MARKDOWN_SOURCE_REGISTRY: 1; PDF_DERIVATIVE_REGISTRY: 8; TEX_SOURCE_REGISTRY: 8 | 17 generated wiki note(s) point back to sources here. | Holds the ontology and benchmark package used as the derivation target and constraint set. |
| `registries` | `control authority` | CSV authority directory. | Registry rows drive generated wiki notes and indexes. | Makes research state machine-checkable through object IDs, hashes, status, and relationships. |
| `research_control` | `control authority` | FILE_OBJECT_REGISTRY: 19; TEX_SOURCE_REGISTRY: 19 | 19 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `scripts` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `tests` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `tex_shared` | `canonical source` | No registered object rows. | No direct generated wiki notes. | Provides authored source material used by the research workflow. |
| `wiki` | `generated derivative` | FILE_OBJECT_REGISTRY: 39; WIKI_ARTIFACT_REGISTRY: 39 | Generated wiki metadata lives here; edit sources and registries instead. | Makes registered objects easier to browse without changing authority. |
| `.agents/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Defines permitted agent behavior and claim boundaries. |
| `.agents/schemas` | `control authority` | No registered object rows. | No direct generated wiki notes. | Defines permitted agent behavior and claim boundaries. |
| `.codex/prompts` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.local/content_semantics` | `local retrieval` | CONTENT_SEMANTIC_REGISTRY: 39; FILE_OBJECT_REGISTRY: 39 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/html_wikis` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/memory_index` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian` | `local retrieval` | FILE_OBJECT_REGISTRY: 39; OBSIDIAN_VAULT_REGISTRY: 39 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `assets/images` | `reserved lane` | No registered object rows. | No direct generated wiki notes. | Reserved for future project material; currently not active authority. |
| `manuscripts/pdfs` | `generated derivative` | No registered object rows. | No direct generated wiki notes. | Provides generated reading surfaces derived from registered sources. |
| `manuscripts/tex` | `reserved lane` | No registered object rows. | No direct generated wiki notes. | Reserved for future project material; currently not active authority. |
| `markdown/html-explainer-specs` | `reserved lane` | No registered object rows. | No direct generated wiki notes. | Reserved for future project material; currently not active authority. |
| `markdown/ontology-promotions` | `reserved lane` | No registered object rows. | No direct generated wiki notes. | Reserved for future project material; currently not active authority. |
| `ontology/pdfs` | `generated derivative` | FILE_OBJECT_REGISTRY: 8; PDF_DERIVATIVE_REGISTRY: 8 | 8 generated wiki note(s) point back to sources here. | Holds the ontology and benchmark package used as the derivation target and constraint set. |
| `ontology/tex` | `canonical source` | FILE_OBJECT_REGISTRY: 8; TEX_SOURCE_REGISTRY: 8 | 8 generated wiki note(s) point back to sources here. | Holds the ontology and benchmark package used as the derivation target and constraint set. |
| `research_control/approvals` | `control authority` | No registered object rows. | No direct generated wiki notes. | Maintains project governance, validation, routing, or registry authority. |
| `research_control/design` | `control authority` | No registered object rows. | No direct generated wiki notes. | Maintains project governance, validation, routing, or registry authority. |
| `research_control/handoffs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Maintains project governance, validation, routing, or registry authority. |
| `research_control/tasks` | `control authority` | FILE_OBJECT_REGISTRY: 19; TEX_SOURCE_REGISTRY: 19 | 19 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/templates` | `control authority` | No registered object rows. | No direct generated wiki notes. | Maintains project governance, validation, routing, or registry authority. |
| `scripts/research_control` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `wiki/html` | `generated derivative` | No registered object rows. | Generated wiki metadata lives here; edit sources and registries instead. | Makes registered objects easier to browse without changing authority. |
| `wiki/indexes` | `generated derivative` | No registered object rows. | Generated wiki metadata lives here; edit sources and registries instead. | Makes registered objects easier to browse without changing authority. |
| `wiki/markdown` | `generated derivative` | FILE_OBJECT_REGISTRY: 4; WIKI_ARTIFACT_REGISTRY: 4 | Generated wiki metadata lives here; edit sources and registries instead. | Makes registered objects easier to browse without changing authority. |
| `wiki/pdf` | `generated derivative` | FILE_OBJECT_REGISTRY: 8; WIKI_ARTIFACT_REGISTRY: 8 | Generated wiki metadata lives here; edit sources and registries instead. | Makes registered objects easier to browse without changing authority. |
| `wiki/tex` | `generated derivative` | FILE_OBJECT_REGISTRY: 27; WIKI_ARTIFACT_REGISTRY: 27 | Generated wiki metadata lives here; edit sources and registries instead. | Makes registered objects easier to browse without changing authority. |
| `.agents/roles/physics` | `control authority` | No registered object rows. | No direct generated wiki notes. | Defines permitted agent behavior and claim boundaries. |
| `.agents/roles/research_ops` | `control authority` | No registered object rows. | No direct generated wiki notes. | Defines permitted agent behavior and claim boundaries. |
| `.codex/skills/continue-research` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/grill-me` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/html-visual-explainer` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/markdown-wiki` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/obsidian-wiki` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/ontology-promotion` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/pdf-derivative-build` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/project-memory-system` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/tex-wiki` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/visual-explainer` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.local/content_semantics/markdown` | `local retrieval` | CONTENT_SEMANTIC_REGISTRY: 4; FILE_OBJECT_REGISTRY: 4 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/content_semantics/pdf` | `local retrieval` | CONTENT_SEMANTIC_REGISTRY: 8; FILE_OBJECT_REGISTRY: 8 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/content_semantics/tex` | `local retrieval` | CONTENT_SEMANTIC_REGISTRY: 27; FILE_OBJECT_REGISTRY: 27 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/html_wikis/visual-explainer` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki` | `local retrieval` | FILE_OBJECT_REGISTRY: 39; OBSIDIAN_VAULT_REGISTRY: 39 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `research_control/tasks/RT-20260608-001` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-002` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-003` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-004` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-005` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-006` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-007` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-008` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-009` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-010` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-011` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-012` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-013` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-014` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-015` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-016` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-017` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-018` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-019` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-020` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `.codex/skills/project-memory-system/obsidian-vault-template` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/project-memory-system/scripts` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/visual-explainer/commands` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/visual-explainer/references` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/visual-explainer/templates` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.local/obsidian/aether-flow-wiki/.obsidian` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/00_control` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/01_raw` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/02_sources` | `local retrieval` | FILE_OBJECT_REGISTRY: 39; OBSIDIAN_VAULT_REGISTRY: 39 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/03_indexes` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/04_relationships` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/05_queries` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/07_logs` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/08_templates` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/09_schema` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `research_control/tasks/RT-20260608-001/artifacts` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-001/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-001/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-002/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-002/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-002/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-003/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-003/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-003/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-004/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-004/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-004/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-005/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-005/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-005/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-006/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-006/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-006/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-007/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-007/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-007/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-008/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-008/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-008/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-009/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-009/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-009/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-010/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-010/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-010/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-011/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-011/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-011/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-012/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-012/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-012/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-013/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-013/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-013/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-014/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-014/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-014/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-015/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-015/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-015/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-016/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-016/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-016/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-017/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-017/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-017/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-018/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-018/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-018/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-019/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-019/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-019/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-020/artifacts` | `control authority` | FILE_OBJECT_REGISTRY: 1; TEX_SOURCE_REGISTRY: 1 | 1 generated wiki note(s) point back to sources here. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-020/jobs` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-020/roles` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `.codex/skills/project-memory-system/obsidian-vault-template/00_control` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/project-memory-system/obsidian-vault-template/08_templates` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.codex/skills/project-memory-system/obsidian-vault-template/09_schema` | `tooling` | No registered object rows. | No direct generated wiki notes. | Operates or tests the research memory/control workflow. |
| `.local/obsidian/aether-flow-wiki/01_raw/html` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/01_raw/markdown` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/01_raw/pdf` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/01_raw/tex` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/02_sources/html` | `local retrieval` | No registered object rows. | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/02_sources/markdown` | `local retrieval` | FILE_OBJECT_REGISTRY: 4; OBSIDIAN_VAULT_REGISTRY: 4 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/02_sources/pdf` | `local retrieval` | FILE_OBJECT_REGISTRY: 8; OBSIDIAN_VAULT_REGISTRY: 8 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `.local/obsidian/aether-flow-wiki/02_sources/tex` | `local retrieval` | FILE_OBJECT_REGISTRY: 27; OBSIDIAN_VAULT_REGISTRY: 27 | No direct generated wiki notes. | Supports retrieval and semantic search for agents; ignored by Git. |
| `research_control/tasks/RT-20260608-001/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-002/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-003/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-004/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-005/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-006/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-007/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-008/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-009/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-010/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-011/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-012/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-013/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-014/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-015/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-016/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-017/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-018/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-019/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
| `research_control/tasks/RT-20260608-020/jobs/completions` | `control authority` | No registered object rows. | No direct generated wiki notes. | Runs bounded proposal, audit, refutation, repair, and handoff transactions. |
