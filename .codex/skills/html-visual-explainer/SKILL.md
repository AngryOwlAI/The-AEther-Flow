---
name: html-visual-explainer
description: Front door for governed, standalone HTML publication explainers.
---

# HTML Visual Explainer

Use this skill when producing, validating, or reviewing tracked HTML explainers
under `html/`.

## Active Process

Tracked public HTML uses the Documentation Curator Publication Process. Each
migrated or new page must be designed from a page-specific publication brief
under `markdown/publication-briefs/` and a row in
`registries/PUBLICATION_BRIEF_REGISTRY.csv`.

The source spec under `markdown/html-explainer-specs/` remains the Markdown
source for the generated HTML. The publication brief defines the reader job,
document type, narrative structure, visual strategy, acceptance criteria, and
forbidden patterns.

## Required Source-Spec Fields

For migrated publication pages, source specs should declare:

- `title`
- `purpose`
- `audience`
- `output_path`
- `github_markdown_output_path`
- `renderer_skill`
- `publication_brief`
- `document_type`
- `visual_strategy`
- `migration_status`
- `source_materials`
- `claim_boundary`
- `human_visual_only: true`
- `standalone_html: true`
- `no_external_runtime: true`

Do not add `reader_blocks`, `github_markdown_parity`, or a universal
`required_content_blocks` skeleton to new publication pages.

## HTML Requirements

Tracked HTML must be:

- single-file and no-network;
- readable without JavaScript;
- mobile-safe with no horizontal overflow from ordinary prose;
- grounded in visible source paths;
- explicit that it is a generated noncanonical reader surface; and
- synchronized with the related GitHub Markdown on source basis, authority
  boundary, and core claims.

Allowed JavaScript is limited to local reading enhancement for an already
complete document. Do not import runtime packages. Do not execute Mermaid in
the browser. If a brief requires a diagram, render it at build time or use a
local semantic visual that needs no network.

## Visual Strategy

Visuals are optional. Use a visual only when the reader learns something that
prose or a table cannot teach as well. Allowed strategies include no diagram,
bespoke Mermaid diagram, annotated table, process timeline, source matrix, role
matrix, decision tree, state model, layered architecture, and custom HTML
visual.

Every major visual needs a page-specific purpose and source basis. A generic
source-to-validation map fails publication review unless the brief explicitly
requires that exact abstraction.

## GitHub Markdown Pair

The GitHub-facing Markdown derivative must read as native Markdown. It does
not need to mirror the HTML section order. It does need the same source basis,
authority boundary, and core claims.

## Validation

Run:

```zsh
.venv/bin/python scripts/validate_publication_process.py --root .
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

For state-changing project-system work, also run:

```zsh
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
```

Screenshot QA is required for pilot HTML pages. Store controlled evidence under
the current task's `research_control/tasks/<task_id>/artifacts/` directory.

## Boundary

HTML is human-only generated output. Direct HTML-only edits remain blocked for
normal publication work: update the publication brief and source spec first,
then regenerate or replace the HTML derivative in the same bounded
transaction.
