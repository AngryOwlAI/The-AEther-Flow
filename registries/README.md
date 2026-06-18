<!-- authority: explanatory -->

# Registries

This folder contains CSV registries and generated metadata sidecars that make
the repository source graph machine-checkable.

## Registry Roles

- Source registries track Markdown, TeX, PDF, and HTML source or derivative
  objects.
- Legacy ontology snapshot rows use distinct `TEX-LEGACY-ONTOLOGY-*`,
  `PDF-LEGACY-ONTOLOGY-*`, and Markdown object IDs so they do not collide with
  live `ontology/` rows.
- Control registries track tasks, Director decisions, AgentJobs, execution
  roles, claim boundaries, role contracts, and project-improvement signals.
- Generated registries track wiki notes, file objects, content semantics,
  Obsidian vault notes, and object relationships.

## What Belongs Here

- CSV registry files required by validators and bootstrap.
- Generated `.meta.json` sidecars produced by bootstrap.

## What Does Not Belong Here

- Free-form notes.
- Generated wiki Markdown.
- Task-local receipts.
- Unregistered scratch data.

## Authority Boundary

Format-specific registries are canonical for routing, provenance,
generated-output tracking, and agent-queryable memory. Generated sidecars are
script-owned derivatives. Update source files and registry rows through the
bounded workflow, then regenerate with bootstrap.

The `legacy_ontology/` lane is archival noncanonical source material. Its rows
exist for retrieval, wiki notes, PDF inventory, and comparison against later
live ontology edits; they do not change physics claim authority.

## Relevant Commands

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```
