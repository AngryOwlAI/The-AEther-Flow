---
title: "Æther-flow Ontology"
purpose: "Explain the project's specific Æther-flow ontology in high-level, operational, and low-level evidence layers while preserving the open exact-GR derivation burden."
audience: "Technical but human-readable: readers who need to understand the project-specific ontology before inspecting canonical TeX or derivation tasks."
output_path: "html/aether-flow-ontology-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "ontology/aether_flow_interpretation-lemen.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
claim_boundary: "Human-only Æther-flow ontology visualization. It explains the project-specific ontology, exact-GR benchmark adoption, and open derivation burden without promoting, rejecting, or modifying any scientific claim."
human_visual_only: true
explainer_kind: "conceptual_model"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "conceptual_model"
layout_intent: "Use a conceptual model with term cards, derivation-burden panels, governed diagrams, and source-backed claim-boundary callouts."
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_materials_section"
required_content_blocks:
  - "subject_summary"
  - "ontology_terms"
  - "exact_gr_benchmark"
  - "derivation_burden"
  - "claim_boundaries"
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
    - "aether-flow-ontology-stack"
    - "derivation-burden-map"
---

# Æther-flow Ontology Spec

## Rendering Intent

Create a self-contained tracked HTML explainer that describes the
project-specific `Æther-flow ontology`. The page should not explain generic
ontology. It should explain what this project currently says:

- `Æther` is the proposed deeper four-dimensional substrate.
- `Æther-flow` is the intrinsic ordered motion or relational organization of
  that substrate.
- observed three-dimensional space is an observer-accessible experiential slice
  rather than the full substrate.
- `S-time` is the experienced order of change arising from matter, light, and
  the `Æther-flow`.
- observed expansion is treated as the three-dimensional appearance of deeper
  ordered motion.
- gravity is interpreted heuristically as matter-shaped reorganization of the
  surrounding `Æther-flow`.
- exact GR is adopted as the current observable benchmark; a first-principles
  derivation remains open.

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
- High-level model: what the `Æther-flow ontology` says about substrate, flow,
  observed space, `S-time`, expansion, and gravity.
- Operational model: how ontology framing connects to exact-GR benchmark
  adoption and the open derivation program.
- Low-level evidence model: source note, TeX registry, claim-boundary registry,
  and the current local response/readout burden.
- A derivation-burden panel for observer normal/readout source construction,
  same-metric matter, nonmetric mode control, `S-time` closure, invariance, and
  anti-smuggling constraints.
- All Source Materials section with source-path evidence; claim-boundary metadata remains in the source spec.

## Required Diagrams

<!-- mermaid-diagram-id: aether-flow-ontology-stack -->
```mermaid
flowchart TD
  Aether["Æther<br/>four-dimensional substrate"] --> Flow["Æther-flow<br/>intrinsic ordered motion"]
  Flow --> Slice["Observed three-dimensional space<br/>local experiential slice"]
  Flow --> STime["S-time<br/>experienced order of change"]
  Flow --> Expansion["Observed expansion<br/>appearance of deeper motion"]
  Matter["Matter and light"] --> STime
  Matter --> Gravity["Gravity as mass-shaped<br/>Æther-flow reorganization"]
  Slice --> Benchmark["Observable benchmark<br/>ordinary exact GR"]
  STime --> Benchmark
  Gravity --> Benchmark
```

<!-- mermaid-diagram-id: derivation-burden-map -->
```mermaid
flowchart TD
  SourceData["Source-defined substrate data"] --> Readout["Observer normal/readout orbit"]
  Readout --> Metric["Effective Lorentzian metric"]
  Metric --> Causal["Causal structure and clocks"]
  Causal --> Matter["Universal same-metric matter coupling"]
  Matter --> Closure["S-time and Einsteinian closure"]
  Closure --> ExactGR["Exact-GR benchmark recovered"]
  SourceData --> AntiSmuggling["Anti-smuggling constraints"]
  AntiSmuggling --> Metric
  AntiSmuggling --> Matter
  AntiSmuggling --> Closure
  ExactGR --> Gate["Promotion requires claim gate"]
```

## Source-Backed Summary

Summary heading: `Summary of Æther-flow Ontology`

Summary text:

The AEther-flow ontology is the project's conceptual vocabulary for a proposed
deeper four-dimensional substrate, its intrinsic ordered motion, and the
observer-accessible appearance of space, time-order, expansion, and gravity.
Its role is not to replace general relativity or claim a completed derivation;
it frames exact GR as the observable benchmark that any future substrate law
must recover. The ontology matters because it keeps the research program's
intuitive picture disciplined: observed three-dimensional space is treated as
a local experiential slice, S-time as the experienced order of change, and
gravity as a heuristic matter-shaped reorganization of the deeper flow. At the
project level, the explainer helps readers separate ontology, mathematical
model, benchmark adoption, and open derivation burden before reading diagrams
or candidate arguments. The summary is grounded in the ontology notes, README
and AGENTS authority guidance, and the claim-boundary registry that prevents a
human-only explainer from promoting speculative ontology into accepted
physics.

Summary source basis:

- `ontology/aether-and-aether-flow.md`
- `ontology/aether_flow_interpretation-lemen.md`
- `README.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`

## Required Content Blocks

- subject_summary: Summarize the project-specific Æther-flow ontology, its role in the exact-GR benchmark program, why the distinction matters, and which declared sources ground the summary.
- ontology_terms: Explain project-local meanings of `Æther`,
  `Æther-flow`, observed space, `S-time`, expansion, and gravity.
- exact_gr_benchmark: State that exact GR is the observable benchmark and not a
  completed first-principles derivation.
- derivation_burden: Show the source-defined readout, same-metric matter,
  invariance, closure, and anti-smuggling requirements.
- claim_boundaries: Preserve the human-only, no-physics-promotion boundary for
  the ontology explainer.

## Required Analysis Capsules

### Project-Specific Ontology

- premise: The `Æther-flow ontology` is the project-specific claim that reality
  is grounded in a deeper four-dimensional substrate and its intrinsic ordered
  motion.
- mechanism: The explainer should connect substrate, flow, observed space,
  `S-time`, observed expansion, and gravity as parts of one conceptual model,
  while making clear that this model is not yet a completed derivation.
- source_basis: `ontology/aether-and-aether-flow.md`, `README.md`, and
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- authority_status: Human-only conceptual explanation; scientific authority
  remains with registered TeX and claim-boundary rows.
- uncertainty: The ontology has not yet supplied the source theorem that
  uniquely recovers the exact-GR benchmark from substrate data.
- validation_or_test: A candidate derivation must source-construct the observer
  normal/readout orbit and recover Lorentzian geometry, clocks, matter
  coupling, invariance, and closure without importing target GR structures.
- next_step: Inspect the derivation-burden map before treating any candidate
  mechanism as progress.

### Exact-GR Benchmark Adoption

- premise: The public benchmark preserves ordinary GR at observable scale while
  the substrate derivation remains open.
- mechanism: The page should show exact-GR adoption as a constraint and
  comparison target, not as evidence that the ontology has already succeeded.
- source_basis: `README.md`, `AGENTS.md`, and `registries/TEX_SOURCE_REGISTRY.csv`.
- authority_status: Explanatory summary of registered claim boundaries.
- uncertainty: Which source-defined substrate laws, if any, can recover the
  benchmark remains unresolved.
- validation_or_test: Candidate structures must pass dimensional consistency,
  invariance, anti-smuggling, same-metric matter, clock behavior, and recovery
  of known limiting behavior.
- next_step: Route derivation candidates through bounded research-control jobs
  and claim gates.

## Non-Goals

- Do not assert that the `Æther-flow ontology` derives GR.
- Do not add new equations, proof claims, or empirical predictions.
- Do not alter canonical ontology TeX or registry status.
- Do not use external images or network-dependent assets.
