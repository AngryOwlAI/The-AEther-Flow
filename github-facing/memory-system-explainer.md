# Memory, Registries, Wiki, And Retrieval Surfaces

AEther-Flow memory is source-first. The memory system helps a maintainer or
agent find the right source, but it does not replace the source. A lookup hit,
wiki note, semantic extract, Obsidian mirror, SQLite row, or `.local` cache is
useful only when it points back to a registered source file and the relevant
registry row.

This page is a generated noncanonical reader surface. It explains the existing
memory and retrieval system, but it does not change memory-system behavior,
registry schema, validator behavior, routing behavior, role authority,
checkpoint behavior, generated-output authority, source authority, or physics
claim status.

## Memory Is Source-First

The repository authority ladder remains unchanged:

- Registered TeX files carry physics and derivational claims.
- Registries carry routing, provenance, generated-output tracking, and
  agent-queryable memory metadata.
- Registered Markdown carries front-door guidance, source specs, publication
  briefs, role and skill contracts, and project-control notes.
- GitHub-facing Markdown, tracked HTML, generated wiki notes, semantic
  extracts, Obsidian mirrors, SQLite memory indexes, and `.local` caches are
  downstream aids.

Memory therefore answers "where should I inspect next?" It does not answer
"what is true by itself?"

## What Each Surface Carries

| Surface | What It Carries | How To Use It |
| --- | --- | --- |
| `registries/MARKDOWN_SOURCE_REGISTRY.csv` | Registered Markdown rows, source hashes, owners, generated outputs, and validation status. | Inspect before changing or citing Markdown-backed project guidance. |
| `registries/TEX_SOURCE_REGISTRY.csv` | Registered TeX rows, claim status, research status, PDF links, and equation scope. | Inspect for physics and derivational source authority. |
| `registries/HTML_EXPLAINER_REGISTRY.csv` | Generated HTML rows bound to Markdown source specs. | Verify tracked HTML as generated noncanonical output. |
| `registries/WIKI_ARTIFACT_REGISTRY.csv` | Generated wiki-note rows, source object IDs, source paths, and source-object hashes. | Use as provenance evidence for generated metadata notes. |
| `registries/OBSIDIAN_VAULT_REGISTRY.csv` | Local Obsidian note paths, raw mirror paths, index paths, and sync status. | Use for local retrieval only; do not cite as authority. |
| `registries/CONTENT_SEMANTIC_REGISTRY.csv` | Deterministic extracted text paths, headings, content hashes, and extraction status. | Use for local agent search and navigation only. |
| `FOLDER_MAP.md` | Generated folder classification for canonical, generated, local, tooling, and reserved lanes. | Use as orientation, then inspect source files and registries. |

Generated wiki notes are metadata derivatives. Obsidian notes and raw mirrors
are local generated retrieval surfaces. Semantic extracts are deterministic
search aids. SQLite memory lookup is an index over those registered and
generated surfaces. None of these layers can promote a claim or override a
tracked source.

## Query Workflow

Use memory preflight as a controlled navigation step:

1. Run status:
   `.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json`
2. Run a targeted lookup or search:
   `.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup <object-id-or-path> --json`
3. Record returned object IDs and warning status.
4. Inspect the canonical source file named by the hit.
5. Inspect the source registry row and source hash.
6. Only then route, edit, cite, or summarize.

For new AgentJobs that require a memory preflight receipt, the receipt must
show the status command, status summary, query commands, returned object IDs,
canonical source inspections, source registry names, canonical paths, and
source hashes. Obsidian, generated wiki notes, semantic extracts, SQLite, and
`.local` remain support surfaces in that receipt.

## Freshness Warnings And Bootstrap

Freshness warnings mean a retrieval layer may lag the tracked sources. They do
not mean the stale retrieval layer has authority. A missing Obsidian note,
stale raw mirror, stale semantic extract, or older SQLite index is a repair
signal for retrieval quality, not a replacement for source inspection.

Use bootstrap when sources or registry rows changed and generated derivatives
need to be rebuilt:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
```

Use validate-only for read-only consistency checks:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Validate-only checks the current generated state; it does not refresh stale
generated artifacts. If source files changed, bootstrap is the logical refresh
path.

## Troubleshooting Stale Local Retrieval

| Symptom | Likely Meaning | Correct Response |
| --- | --- | --- |
| `freshness_status` is `WARN` | Some generated retrieval layer is missing, stale, or older than source inputs. | Treat it as a retrieval warning and inspect canonical sources directly. |
| Obsidian vault note is missing | The local vault mirror has not been generated for that object. | Refresh through bootstrap or vault sync; do not hand-edit generated notes. |
| Raw mirror is stale | The `.local/obsidian` raw copy lags the tracked source. | Refresh generated local retrieval surfaces. |
| SQLite index is older than inputs | Search results may not reflect the newest source or registry rows. | Refresh the memory index before relying on search for navigation. |
| Wiki note disagrees with source | The derivative is stale or wrong. | Correct the source or registry row if needed, then regenerate. |

## Operator Boundary

Do not use memory lookup as proof. Do not cite generated wiki notes,
semantic extracts, Obsidian mirrors, SQLite rows, `.local` caches, tracked
HTML, or GitHub-facing Markdown as independent authority. Do not hand-edit
generated wiki notes or generated registry metadata sidecars. Do not use this
page to change memory scripts, registry schemas, validators, routing,
checkpoint gates, role authority, or physics claim status.

## Source Materials

- AEther-Flow Project. (2026). `AGENTS.md` [Repository authority guidance].
- AEther-Flow Project. (2026). `.codex/skills/project-memory-system/SKILL.md` [Project memory system skill].
- AEther-Flow Project. (2026). `.codex/skills/obsidian-wiki/SKILL.md` [Obsidian wiki and memory query skill].
- AEther-Flow Project. (2026). `registries/MARKDOWN_SOURCE_REGISTRY.csv` [Markdown source registry].
- AEther-Flow Project. (2026). `registries/TEX_SOURCE_REGISTRY.csv` [TeX source registry].
- AEther-Flow Project. (2026). `registries/HTML_EXPLAINER_REGISTRY.csv` [HTML explainer registry].
- AEther-Flow Project. (2026). `registries/WIKI_ARTIFACT_REGISTRY.csv` [Wiki artifact registry].
- AEther-Flow Project. (2026). `registries/OBSIDIAN_VAULT_REGISTRY.csv` [Obsidian vault registry].
- AEther-Flow Project. (2026). `registries/CONTENT_SEMANTIC_REGISTRY.csv` [Content semantic registry].
- AEther-Flow Project. (2026). `FOLDER_MAP.md` [Generated folder map].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/memory-system-explainer.md`
- **Related HTML:** `html/memory-system-explainer.html`
- **Publication brief:** `markdown/publication-briefs/memory-system.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

## Safe Summary

Safe summary: use memory to find source paths, inspect the canonical source
and registry row, refresh generated derivatives through bootstrap, treat
freshness warnings as retrieval warnings, and keep generated wiki, semantic,
Obsidian, SQLite, and `.local` layers non-authoritative.

Unsafe summary: memory lookup replaces source inspection, Obsidian is project
authority, `.local` can override tracked control state, wiki notes may be
hand-edited, or generated retrieval layers can promote claims.
