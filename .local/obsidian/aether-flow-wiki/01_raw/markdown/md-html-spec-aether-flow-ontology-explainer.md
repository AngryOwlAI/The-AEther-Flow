---
title: "Æther-flow Ontology"
purpose: "Explain the project's specific Æther-flow ontology for lay and technical readers while preserving the exact-GR benchmark/open-derivation boundary."
audience: "Mixed lay and technical readers: humans who need the project ontology, physics interpretation, source authority, and open derivation burden explained before reading TeX, registries, or candidate derivation work."
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
claim_boundary: "Human-only Æther-flow ontology documentation. It explains the project-specific ontology, exact-GR benchmark adoption, source-text boundaries, and open derivation burden without promoting, rejecting, or modifying any scientific claim."
human_visual_only: true
explainer_kind: "conceptual_model"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "conceptual_model"
layout_intent: "Use a mixed-audience conceptual model: a plain-language orientation, term cards, source quote panels, adoption-vs-derivation bridge, derivation-burden checklist, governed diagrams, and claim-boundary callouts."
required_controls:
  - "section_toc"
  - "source_materials_section"
required_content_blocks:
  - "subject_summary"
  - "layperson_orientation"
  - "ontology_terms"
  - "exact_gr_benchmark"
  - "derivation_burden"
  - "source_quote_gallery"
  - "claim_boundaries"
  - "reader_paths"
mermaid_diagrams:
  required: true
  ids:
    - "aether-flow-ontology-stack"
    - "derivation-burden-map"
---

# Æther-flow Ontology Spec

## Rendering Intent

Create a standalone, source-backed HTML explainer that helps both lay readers
and technical reviewers understand what the project means by `Æther-flow
ontology`. The page should not explain generic ontology first. It should explain
this project’s vocabulary, why that vocabulary exists, how it connects to exact
general relativity as a benchmark, and why the first-principles substrate
derivation remains open.

The page should have three reading layers:

1. **Plain-language orientation**: what the ontology is trying to picture.
2. **Technical bridge**: how the project maps that picture to exact-GR benchmark
   adoption, observer readout, same-metric matter, and closure constraints.
3. **Source-grounded deep dive**: short source quotations, source chips, and
   claim-boundary notes showing what the current files do and do not authorize.

Do not alter the registered diagrams. Add richer explanation around them.

## Required Visual Structure

- Source-backed content blocks should be full-width documentation panels, not
  narrow placeholder cards.
- Each content block should include a plain answer, project function, source
  basis, and claim boundary.
- Add term cards for `Æther`, `Æther-flow`, observed three-dimensional space,
  `S-time`, observed expansion, gravity, exact closure, adoption, derivation,
  observer readout, and anti-smuggling.
- Add a source quote gallery with short excerpts from the two ontology Markdown
  files.
- Add an adoption-vs-derivation bridge for readers who know GR but not this
  project.
- Add a derivation-burden checklist explaining the missing mathematical work
  without implying the work has been solved.
- Preserve the All Source Materials section with source-path evidence.
- Preserve the human-only generated derivative boundary.

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

The Æther-flow ontology is the project’s conceptual vocabulary for talking about
a proposed deeper four-dimensional substrate, its intrinsic ordered motion, and
the observer-level world that appears to us as space, time-order, expansion, and
gravity. In plain terms, it is the project’s answer to the question: “What kind
of underlying reality might ordinary relativistic geometry be describing?” The
answer is not a new proven replacement for general relativity. The current
project keeps ordinary exact GR as the observable benchmark and treats the
substrate derivation as open work. This distinction matters because the ontology
is useful as a mental model only if it does not smuggle in the GR structures it
is supposed to recover. The page therefore separates vocabulary, interpretation,
mathematical adoption, and derivational burden. Readers should leave knowing
what `Æther`, `Æther-flow`, observed space, `S-time`, observed expansion, and
gravity mean inside this repository, why the picture is attractive, and what
must still be proven before it could count as a first-principles derivation.

Summary source basis:

- `ontology/aether-and-aether-flow.md`
- `ontology/aether_flow_interpretation-lemen.md`
- `README.md`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`

## Required Content Blocks

- subject_summary: Render the source-backed summary above first, with visible source chips for the declared grounding files.
- layperson_orientation: A finished plain-language opening that defines ontology as what the project says exists, distinguishes this conceptual map from a proof, and states the exact-GR benchmark plus open derivation burden before technical vocabulary appears.
- ontology_terms: Source-backed term cards for `Æther`, `Æther-flow`, observed three-dimensional space, `S-time`, observed expansion, gravity, exact closure, adoption, derivation, observer readout, and anti-smuggling, with plain meaning, project function, common misunderstanding, and source basis.
- exact_gr_benchmark: A completed adoption-versus-derivation bridge explaining that current calculations remain ordinary exact GR while a valid substrate derivation would still need to recover Lorentzian geometry, clocks, causal structure, same-metric matter coupling, invariance, and closure without importing them by hand.
- derivation_burden: A source-backed derivation-burden checklist tied to the registered diagram, including source-defined substrate data, observer normal/readout orbit, effective metric, clocks, same-metric matter, nonmetric mode control, `S-time` closure, invariance, anti-smuggling constraints, and claim-gate review.
- source_quote_gallery: Short quote cards from both ontology Markdown sources, each paired with why the quote matters, what it permits, and what it forbids for the generated human-only explainer.
- claim_boundaries: A visible non-claim panel stating what the page may explain and what it may not assert, including no completed GR derivation, no new empirical prediction, no canonical TeX edits, and no generated-HTML authority promotion.
- reader_paths: A where-to-go-next panel routing new readers to term cards and diagrams, technical reviewers to TeX and registries, and project maintainers to source-authority and research-control explainers.
