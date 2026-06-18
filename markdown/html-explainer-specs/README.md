<!-- authority: explanatory -->

# HTML Explainer Source Specs

This folder contains Markdown source specs for generated human-only HTML
explainers.

## How This Lane Works

Each spec declares source materials, claim boundaries, output path, renderer
skill, interaction model, presentation profile, required controls, and required
content blocks. The spec is the source; the corresponding `html/*.html` file
is a generated derivative.

## What Belongs Here

- Registered source specs for visual explainers.
- Source-backed explanatory content blocks.
- Mermaid diagrams and source-material references when the explainer requires
  them.

## What Does Not Belong Here

- Generated HTML output.
- GitHub-facing Markdown derivatives.
- Raw Student/Teacher teaching-loop transcripts.
- Physics claim promotion or canonical ontology edits.

## Authority Boundary

Specs can define the source basis for an explainer, but they do not promote
scientific claims beyond their cited sources. Generated HTML and
GitHub-facing Markdown must remain noncanonical derivatives.

## Relevant Checks

```zsh
.venv/bin/python scripts/spec_depth_lint.py --root .
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

