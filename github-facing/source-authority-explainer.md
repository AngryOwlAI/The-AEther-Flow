# Source Authority Spec

## Rendering Intent

Create a tracked HTML drilldown for source authority. The page should explain
which materials carry authority and which materials are generated retrieval or
human-reading derivatives.

The page should make the hierarchy explicit:

1. Registered `.tex` files are canonical for scientific and derivational
   claims.
2. Format-specific registries are canonical for routing, provenance, generated
   outputs, and agent-queryable memory.
3. Registered Markdown files are canonical for front-door material, agent
   guidance, and source-backed HTML explainer specs.
4. PDFs, generated wiki notes, generated indexes, HTML explainers, local
   Obsidian vault files, and `.local/` caches are derivative or scratch
   surfaces.

The page should use an authority/use-case matrix rather than an extension-only
list. Rows should include format or lane, primary use, authority status, who or
what edits it, generated/authored status, validation, and examples. Cover
`.tex`, `.md`, `.csv`, `.yaml`, `.html`, `.pdf`, `.sqlite` or semantic
extracts, `.meta.json`, and `.local/` surfaces.

## Required Visual Structure

- Source-backed coverage rows: render `Source-Backed Coverage` content blocks
  as full-width horizontal rows rather than narrow multi-column cards. Tables
  must use readable auto layout, with any wide overflow scoped inside the
  content block instead of the page body.
- Responsive containment: navigation chips, grids, tables, code paths, source
  drilldowns, and diagram shells must not create body-level horizontal overflow
  on mobile or desktop viewports.
- Adaptive diagram fit: diagram-backed boxes must read the rendered
  SVG viewBox, set the box height from diagram aspect ratio and available
  width within bounded min/max limits, and make Fit recompute that best-fit
  geometry so horizontal diagrams do not collapse to intrinsic SVG width.
- Three-layer readability: stack the high-level, operational, and evidence
  layer sections vertically; cards inside each layer must auto-fit at a
  readable minimum width rather than nesting fixed three-column grids.
- High-level model: authority ladder and why source-first governance exists.
- Operational model: update source -> regenerate derivatives -> validate
  registries and parity.
- Low-level evidence model: registry rows, source hashes, generated-output
  links, source-basis metadata, and validation commands.
- Format matrix: explain what a file means in this project before naming the
  extension.
- Workflow step inspector for derivative generation.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Required Diagrams

<!-- mermaid-diagram-id: source-authority-ladder -->
```mermaid
flowchart TD
  Tex["Registered TeX<br/>scientific authority"] --> Registries["Format registries<br/>routing and provenance authority"]
  Registries --> Markdown["Registered Markdown<br/>front door and specs"]
  Markdown --> Html["Tracked HTML explainers<br/>human-only generated derivatives"]
  Tex --> Pdf["PDF derivatives<br/>human reading"]
  Registries --> Wiki["Generated wiki and indexes<br/>metadata retrieval"]
  Wiki --> Local["Local Obsidian and .local caches<br/>scratch or retrieval"]
  Html --> Local
```

<!-- mermaid-diagram-id: derivative-generation-flow -->
```mermaid
flowchart TD
  Source["Authoritative source edit"] --> Registry["Registry row and source hash"]
  Registry --> Bootstrap["Memory bootstrap"]
  Bootstrap --> Wiki["Generated wiki notes"]
  Bootstrap --> Html["Generated HTML derivative"]
  Bootstrap --> Pdf["Generated PDF derivative"]
  Html --> Metadata["Source-basis metadata"]
  Wiki --> Banner["Non-authority banner"]
  Pdf --> Link["PDF registry row"]
  Metadata --> Validate["Validate source parity"]
  Banner --> Validate
  Link --> Validate
```

## Source-Backed Summary

Summary heading: `Summary of Source Authority`

Summary text:

Source authority is the repository rule for deciding which files can define
project truth and which files are generated aids for reading, retrieval,
validation, or publication. Its functionality is to rank registered TeX,
format-specific registries, registered Markdown, generated HTML, generated
wiki notes, PDFs, local Obsidian surfaces, and .local caches so contributors
update canonical sources first and regenerate dependent artifacts afterward.
This matters because many surfaces are polished, searchable, or easier to read
than the source files, but convenience does not make them independent
authority. The authority model fits the project by preserving scientific claim
discipline, project-control provenance, and reproducible memory refreshes
across a repo that intentionally generates many human-facing derivatives.

Summary source basis:

- `AGENTS.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `registries/FILE_OBJECT_REGISTRY.csv`

## Required Content Blocks

- subject_summary: Summarize source authority, its file-format ladder, why generated surfaces stay non-authoritative, and which declared sources ground the summary.
- authority_ladder: A documentation-grade ladder covering canonical science sources, registry authority, registered Markdown authority, generated derivatives, and `.local/` scratch boundaries.
- format_use_case_matrix: A complete authority/use-case matrix for `.tex`, `.md`, `.csv`, `.yaml`, `.html`, `.pdf`, `.sqlite` or semantic extracts, `.meta.json`, `wiki/`, and `.local/`, including editor, validator, and failure mode.
- generated_derivatives: A source-backed section explaining generated wiki notes, indexes, PDFs, tracked HTML, metadata sidecars, content semantics, and why regeneration does not promote them to authority.
- local_retrieval_surfaces: A completed section on local Obsidian, content semantics, SQLite, query scripts, caches, and scratch builds as operator aids that must point back to canonical rows.
- validation_evidence: A documentation section on source hashes, source-basis metadata, registry rows, Mermaid parity, bootstrap validation, documentation-impact receipts, and checkpoint boundaries.
