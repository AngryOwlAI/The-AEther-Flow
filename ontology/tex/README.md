<!-- authority: explanatory -->

# Ontology TeX Sources

This folder contains registered TeX source files for ontology and exact-GR
benchmark material. It is the live TeX lane; the copied 2026-06-18 reference
state lives under `legacy_ontology/tex/`.

## What Belongs Here

- Canonical ontology and benchmark TeX files.
- TeX source files registered in `registries/TEX_SOURCE_REGISTRY.csv`.
- Scientific material whose claim status must be tracked by registry metadata.

## What Does Not Belong Here

- Generated PDFs. Those belong under `ontology/pdfs/`.
- Project-control task receipts.
- Scratch derivation attempts not authorized by a bounded task.
- Markdown documentation.

## Authority Boundary

These TeX files can carry scientific authority, but claim status still depends
on the registry row, claim boundary, and project gates. Editing them requires
the appropriate research-control task and validation path.

## Derivative Path

PDF derivatives are generated from these files and recorded in
`registries/PDF_DERIVATIVE_REGISTRY.csv`. Do not treat a PDF as independent
authority when the TeX source is available.

If the live ontology changes, update files here through the governed task and
validation path. The legacy TeX snapshot is for comparison only and should not
be used as the active edit target.
