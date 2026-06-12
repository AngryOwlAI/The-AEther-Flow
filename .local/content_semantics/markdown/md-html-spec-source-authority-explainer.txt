---
title: "Source Authority"
purpose: "Explain the repository authority ladder from canonical TeX and registries through registered Markdown, generated wiki/PDF/HTML derivatives, and local scratch surfaces."
audience: "Technical but human-readable: maintainers, research agents, and reviewers who need to know which files can support claims."
output_path: "html/source-authority-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "registries/WIKI_ARTIFACT_REGISTRY.csv"
  - "registries/PDF_DERIVATIVE_REGISTRY.csv"
  - "registries/FILE_OBJECT_REGISTRY.csv"
  - "research_control/design/html_explainer_flexible_presentation_contract.md"
claim_boundary: "Human-only source-authority visualization. It explains existing authority hierarchy and generated-derivative boundaries without changing registry authority, source status, scientific claims, or control contracts."
human_visual_only: true
explainer_kind: "control_system"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "format_ladder"
layout_intent: "Use an authority/use-case matrix first, with file extensions inside each row, then provide drilldowns for source authority, generated derivatives, local retrieval surfaces, and validation evidence."
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_materials_section"
  - "workflow_step_inspector"
required_content_blocks:
  - "subject_summary"
  - "authority_ladder"
  - "format_use_case_matrix"
  - "generated_derivatives"
  - "local_retrieval_surfaces"
  - "validation_evidence"
analysis_capsule_schema:
  - "premise"
  - "mechanism"
  - "source_basis"
  - "authority_status"
  - "uncertainty"
  - "validation_or_test"
  - "next_step"
mermaid_diagrams:
  required: true
  ids:
    - "source-authority-ladder"
    - "derivative-generation-flow"
---

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
across a repo that intentionally generates many human-facing derivatives. The
summary is grounded in root AGENTS and README authority guidance, the project-
memory-system and HTML explainer skill contracts, and the registries that
track canonical files, source hashes, generated outputs, and derivative
boundaries.

Summary source basis:

- `AGENTS.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `registries/HTML_EXPLAINER_REGISTRY.csv`
- `registries/FILE_OBJECT_REGISTRY.csv`

## Required Content Blocks

- subject_summary: Summarize source authority, its source-first governance function, why it matters for generated and canonical surfaces, and which declared sources ground the summary.
- authority_ladder: Explain canonical science sources, registry authority,
  registered Markdown authority, generated derivatives, and `.local/` scratch
  boundaries.
- format_use_case_matrix: Provide an authority/use-case matrix covering `.tex`,
  `.md`, `.csv`, `.yaml`, `.html`, `.pdf`, `.sqlite` or semantic extracts,
  `.meta.json`, and `.local/`.
- generated_derivatives: Explain generated wiki notes, indexes, PDFs, tracked
  HTML, metadata sidecars, and why they are not independent authority.
- local_retrieval_surfaces: Explain local Obsidian vault, content semantics,
  semantic index, scratch builds, caches, and retrieval outputs as
  noncanonical access layers.
- validation_evidence: Explain source hashes, source-basis metadata, registry
  rows, Mermaid parity, bootstrap validation, and documentation-impact checks.

## Required Analysis Capsules

### Authority Is Source-First

- premise: The repository distinguishes source authority from generated
  retrieval and human-reading surfaces.
- mechanism: Canonical files and registries own claims and provenance; generated
  derivatives expose or visualize that content but do not become independent
  authority.
- source_basis: `AGENTS.md`, `README.md`, and source registries.
- authority_status: Human-only explanation of the existing authority hierarchy.
- uncertainty: Generated derivatives can be useful but stale if source hashes,
  source-basis metadata, or registry rows drift.
- validation_or_test: Run bootstrap validation and check source-basis hashes,
  generated-output rows, and non-authority banners.
- next_step: Edit canonical sources or registered specs first, then regenerate.

### HTML Is A Human Visual Derivative

- premise: Tracked HTML pages help humans understand the project but do not
  carry independent scientific or control authority.
- mechanism: Each HTML file points back to a Markdown source spec and registry
  source basis; diagram source is preserved in the spec and rendered
  into inline SVG for portability.
- source_basis: `.codex/skills/html-visual-explainer/SKILL.md`,
  `registries/HTML_EXPLAINER_REGISTRY.csv`, and
  `registries/MARKDOWN_SOURCE_REGISTRY.csv`.
- authority_status: Explanation of generated HTML boundaries.
- uncertainty: Visual polish can improve comprehension without changing the
  underlying authority chain.
- validation_or_test: Confirm every tracked HTML explainer has a registered
  Markdown spec, source-basis metadata, required controls, source materials,
  and Mermaid parity when diagrams are declared.
- next_step: Use the project hub to navigate the generated pages, then inspect
  the source specs for authoritative explainer content.

## Non-Goals

- Do not change registry semantics.
- Do not edit generated wiki notes or PDFs by hand.
- Do not treat `.local/` caches as tracked authority.
- Do not use external images or network-dependent assets.
