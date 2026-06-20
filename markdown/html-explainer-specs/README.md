<!-- authority: explanatory -->

# HTML Explainer Source Specs

This folder contains Markdown source specs for generated human-only HTML
explainers.

## How This Lane Works

Each retained public spec must be paired with a publication brief under
`markdown/publication-briefs/` and a row in
`registries/PUBLICATION_BRIEF_REGISTRY.csv`. The spec declares the source
materials, claim boundary, output paths, document type, visual strategy, and
runtime boundary for the generated HTML and GitHub-facing Markdown surfaces.

The current retained corpus contains 17 reviewed page stacks. Phase 6 of the
Reader Scope footer relocation work verified that each reviewed GitHub-facing
Markdown page and tracked HTML page keeps Reader Scope material at the bottom
authority hook, immediately before the footer authority language.

## What Belongs Here

- Source specs listed in `registries/PUBLICATION_BRIEF_REGISTRY.csv`.
- Source-backed publication content grounded in the page brief.
- Diagrams, tables, or custom visuals only when the page brief requires them.

## What Does Not Belong Here

- Generated HTML output.
- GitHub-facing Markdown derivatives.
- Physics claim promotion or canonical ontology edits.

## Authority Boundary

Specs can define the source basis for an explainer, but they do not promote
scientific claims beyond their cited sources. Generated HTML and
GitHub-facing Markdown must remain noncanonical derivatives.

## Relevant Checks

```zsh
.venv/bin/python scripts/validate_publication_process.py --root . --strict
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```
