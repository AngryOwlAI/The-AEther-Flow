# AGENTS.md

Root project guidance for agents working in `The Æther-Flow Interpretation of Relativity Research Project`.

## Project Identity

This repository has two linked missions:

1. Physics research: maintain `The Æther-Flow Interpretation of Relativity` as
   an exact-GR benchmark while treating first-principles GR derivation from
   `Æther` / `Æther-flow` substrate structure as open until authorized gates
   establish it.
2. AI research-agent development: agentice theoretical physics workflow using routing, 
   refutation, novelty search, claim gates, manuscript memory, negative-result preservation.

## Authority Hierarchy

Use the repository memory system before making project-knowledge changes.

1. Registered `.tex` files are canonical for physics research and derivational claims.
2. Format-specific registries under `registries/` are canonical for routing, provenance, generated-output tracking, and agent-queryable memory.
3. Registered Markdown files are canonical for README/front-door material, agent guidance, and project-control notes.
4. PDFs, generated wiki notes, generated wiki indexes, `FILE_OBJECT_REGISTRY.csv`, `WIKI_ARTIFACT_REGISTRY.csv`, and HTML explainers are derivative artifacts.

Generated artifacts may be read by humans and agents, but they are not independent authority. Edit the canonical source and registry row, then regenerate.

## Required Checks

Before changing repository knowledge, inspect the relevant source file and registry row. After changing source or registry material, regenerate and validate:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
```

For read-only validation, use:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

Run smoke tests when changing memory-system scripts:

```zsh
.venv/bin/python -m unittest discover -s tests
```

## Generated-Output Boundaries

- Do not hand-edit generated wiki notes under `wiki/`.
- Do not hand-edit generated master registries or generated registry metadata sidecars.
- Do not treat PDFs as independent scientific authority; they are human-reading derivatives from registered TeX.
- Do not add tracked HTML under `html/` unless it is generated from a registered Markdown source spec.
- Keep `.local/` for scratch builds, caches, previews, and experiments.
