# Memory, Registries, Wiki, And Retrieval Surfaces

AEther-Flow memory is a source-finding system, not a second source of truth. Its job is to help a maintainer or agent find relevant source objects, registry rows, prior tasks, generated notes, semantic extracts, and local retrieval mirrors quickly enough to work responsibly.

The authority split remains strict. Registered TeX carries physics and derivational claims. Registries carry routing, provenance, generated-output tracking, and memory metadata. Registered Markdown carries guidance, source specs, publication briefs, role and skill contracts, and project-control notes. Generated wiki notes, content-semantic extracts, Obsidian vault mirrors, SQLite indexes, and `.local` caches are downstream retrieval layers.

The practical workflow is therefore two-stage. Use memory preflight to locate the likely source, then inspect the canonical source file and source registry row before routing, editing, citing, or summarizing. Freshness warnings are useful because they reveal retrieval drift; they do not override tracked files.

## Authority And Retrieval Layers

| Item | Function | Boundary |
| --- | --- | --- |
| Canonical science | Registered TeX rows and source files carry physics and derivational claims. | Inspect before physics summaries. |
| Control registries | CSV rows carry routing, provenance, generated-output tracking, and memory metadata. | Inspect before routing or registry-dependent claims. |
| Registered Markdown | README, AGENTS, source specs, briefs, roles, skills, and design notes carry project-control guidance. | Inspect before documentation or workflow claims. |
| Generated derivatives | HTML pages, wiki notes, and generated indexes support humans and agents. | Read as derivatives only. |
| Local retrieval | Obsidian mirrors, semantic extracts, SQLite, and `.local` caches speed lookup. | Never cite as authority. |

## Query Workflow

| Item | Function | Boundary |
| --- | --- | --- |
| Status | Run memory status and record freshness warnings. | Warn does not block source inspection. |
| Lookup or search | Use a targeted query to find object IDs or likely paths. | Do not broaden into an unbounded scan. |
| Canonical inspection | Open the source file and registry row named by the useful hit. | Required when memory affects routing or claims. |
| Receipt | Record status, queries, returned IDs, source paths, registries, and hashes. | Required in new AgentJobs that use memory preflight. |

## Freshness Warnings

| Item | Function | Boundary |
| --- | --- | --- |
| Stale raw mirror | A local mirror lags the tracked source. | Refresh retrieval layers; inspect source directly. |
| Missing vault note | Local Obsidian support is incomplete. | Run approved sync/bootstrap path. |
| Older SQLite index | Search may miss current inputs. | Refresh before relying on search for navigation. |
| Wiki/source disagreement | A generated derivative is stale or wrong. | Correct source or registry, then regenerate. |

## Bootstrap Boundaries

| Item | Function | Boundary |
| --- | --- | --- |
| Bootstrap | Refreshes generated registry, wiki, semantic, and folder-map derivatives. | Use after source or registry changes. |
| Validate-only | Checks current generated state without writing. | Does not refresh stale derivatives. |
| Generated lanes | Wiki, HTML, PDFs, semantic extracts, and local mirrors are support surfaces. | Do not hand-edit as authority. |

## Reader Scope

Reader scope: memory and retrieval orientation only. This page cannot change memory-system behavior, registry schema, validator behavior, routing behavior, role authority, checkpoint behavior, source authority, or physics status.

<!-- explainer-control: authority_footer -->

## Source Binding And Authority

- **Derived from spec:** `markdown/html-explainer-specs/memory-system-explainer.md`
- **Related HTML:** `html/memory-system-explainer.html`
- **Publication brief:** `markdown/publication-briefs/memory-system.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

This page is a generated noncanonical reader surface. It explains existing source-first memory behavior, registry routing and provenance roles, generated wiki notes, content semantics, Obsidian vault mirrors, SQLite lookup, memory preflight receipts, freshness warnings, and bootstrap refresh boundaries without changing memory-system behavior, registry schema, validator behavior, routing behavior, role authority, checkpoint behavior, generated-output authority, source authority, or physics claim status.

## Source Materials

- AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy and generated-output boundary.]
- AEther-Flow Project. (2026). `.codex/skills/project-memory-system/SKILL.md` [Bootstrap, validate-only, docs modes, and cleanup commands.]
- AEther-Flow Project. (2026). `.codex/skills/obsidian-wiki/SKILL.md` [Local vault, semantic extraction, vault sync, lint, and query guidance.]
- AEther-Flow Project. (2026). `registries/MARKDOWN_SOURCE_REGISTRY.csv` [Registered Markdown source rows and generated outputs.]
- AEther-Flow Project. (2026). `registries/TEX_SOURCE_REGISTRY.csv` [Registered TeX rows for physics and derivational source material.]
- AEther-Flow Project. (2026). `registries/HTML_EXPLAINER_REGISTRY.csv` [Generated HTML rows bound to source specs.]
- AEther-Flow Project. (2026). `registries/WIKI_ARTIFACT_REGISTRY.csv` [Generated wiki-note rows and source-object hashes.]
- AEther-Flow Project. (2026). `registries/OBSIDIAN_VAULT_REGISTRY.csv` [Local Obsidian note and raw mirror paths.]
- AEther-Flow Project. (2026). `registries/CONTENT_SEMANTIC_REGISTRY.csv` [Deterministic semantic extraction rows for local search.]
- AEther-Flow Project. (2026). `FOLDER_MAP.md` [Generated folder classification for canonical, generated, local, tooling, and reserved lanes.]

## Safe Operating Summary

Safe summary: Memory lookup routes attention to canonical sources and registry rows; after source inspection it can support routing, documentation, and receipts.

Unsafe summary: A wiki note, Obsidian mirror, semantic extract, SQLite hit, or `.local` cache overrides tracked source authority.
