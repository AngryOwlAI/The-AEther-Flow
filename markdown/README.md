<!-- authority: explanatory -->

# Authored Markdown Sources

This folder contains authored Markdown sources used by the documentation and
project-memory system.

## Folder Structure

- `html-explainer-specs/` contains source specs for reviewed publication-brief
  public pages and their GitHub-facing Markdown derivatives. The current
  reviewed publication corpus contains 17 page stacks.
- `publication-briefs/` contains the page-specific briefs that authorize public
  HTML and GitHub-facing Markdown publication pages. The live corpus status is
  governed by `registries/PUBLICATION_BRIEF_REGISTRY.csv`.
- `ontology-promotions/` is reserved for bounded ontology-promotion packet
  notes.
- `grill-memory-wiki-registry-design-handoff.md` records accepted memory,
  wiki, registry, and file-format design decisions.

## What Belongs Here

- Authored Markdown that is source material for registered documentation
  workflows.
- Non-generated explanatory or project-control notes that need registry and
  wiki visibility.

## What Does Not Belong Here

- Generated wiki notes.
- Generated HTML.
- Task-local completion records.
- Canonical physics TeX sources.

## Authority Boundary

Markdown authority depends on its registry role and authority status. Some
files are project-control design notes, some are publication briefs, and some
are source specs for generated public explainers. Check
`registries/MARKDOWN_SOURCE_REGISTRY.csv` and
`registries/PUBLICATION_BRIEF_REGISTRY.csv` before treating a Markdown file as
publication authority.
