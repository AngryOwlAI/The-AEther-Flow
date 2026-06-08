---
name: obsidian-wiki
description: Front door for the local generated Obsidian memory vault, content-semantic extraction, relationship graph, and JSON query surface.
---

# Obsidian Wiki

Use this skill when initializing, syncing, validating, or querying the local
Obsidian memory vault.

The live vault is generated under:

```zsh
.local/obsidian/aether-flow-wiki/
```

It is a retrieval and semantic-search layer, not canonical authority. CSV
registries and registered source files remain authoritative.

## Commands

Initialize the local vault:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/init_obsidian_vault.py
```

Extract content semantics and refresh generated registry surfaces:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/extract_content_semantics.py
```

Sync the vault and rebuild the local memory index:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/sync_obsidian_vault.py
```

Validate the local vault:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/lint_obsidian_vault.py --require-index
```

Query the memory system:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup MD-README --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "Lorentzian metric" --formats tex,pdf --limit 10 --json
```
