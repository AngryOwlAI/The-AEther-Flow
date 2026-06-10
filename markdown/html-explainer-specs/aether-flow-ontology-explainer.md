---
title: "Æther Flow Ontology Explainer"
purpose: "Explain the project's current ontology framing, exact-GR benchmark status, and open derivation burden in a human-only visual form."
audience: "Readers who need a disciplined conceptual overview of the Æther / Æther-flow ontology without mistaking it for an accepted derivation."
output_path: "html/aether-flow-ontology-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
claim_boundary: "Human-only ontology visualization. It explains the current ontology framing and open derivation burden without promoting, rejecting, or modifying any scientific claim."
human_visual_only: true
explainer_kind: "conceptual_model"
interaction_model: "progressive_disclosure"
analysis_depth: "simple_and_deep"
required_controls:
  - "simple_deep_toggle"
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_drilldowns"
  - "claim_boundary_toggle"
source_drilldowns:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/TEX_SOURCE_REGISTRY.csv"
analysis_capsule_schema:
  - "premise"
  - "mechanism"
  - "source_basis"
  - "authority_status"
  - "uncertainty"
  - "validation_or_test"
  - "next_step"
---

# Æther Flow Ontology Explainer Spec

## Rendering Intent

Create a self-contained HTML explainer that presents the ontology lane with
research-level caution. The page should make the distinction between ontology,
mathematical model, benchmark behavior, and empirical derivation burden visually
obvious.

## Required Visual Structure

- A four-layer ontology-to-benchmark stack: substrate idea, source-defined
  structures, effective relativistic behavior, and exact-GR benchmark.
- A boundary panel stating that the benchmark preserves ordinary GR while the
  first-principles substrate derivation remains open.
- A derivation-burden checklist covering Lorentzian metric generation, causal
  structure, clock behavior, matter coupling, invariance, and anti-smuggling
  constraints.
- A detailed analysis layer explaining what an ontology is, how it differs from
  an accepted mathematical derivation, and why deriving GR from the ontology is
  the central open problem.
- A source-authority panel pointing readers back to registered TeX and registry
  rows for scientific authority.
- Expandable source drilldowns that state why each cited source matters and
  what ontology, benchmark, or authority boundary it checks.
- A claim-boundary notice stating that this page is human-only and
  non-authoritative.
- Progressive-disclosure controls for first-read and deep analysis modes,
  expandable analysis capsules, source drilldowns, and claim-boundary
  inspection.

## Required Analysis Capsules

### Ontology Versus Derivation

- premise: An ontology states what kind of underlying structure the project is
  proposing; it is not by itself a completed derivation.
- mechanism: The page should distinguish substrate vocabulary, mathematical
  model, benchmark behavior, and empirical prediction so readers do not confuse
  conceptual framing with proven physics.
- source_basis: `README.md`, `ontology/aether-and-aether-flow.md`, and
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- authority_status: Human-only conceptual explanation; scientific authority
  remains with registered source files and claim-boundary rows.
- uncertainty: The ontology has not yet produced a first-principles derivation
  of the exact-GR benchmark.
- validation_or_test: A successful derivation must recover Lorentzian metric
  behavior, causal structure, clocks, matter coupling, and invariance without
  target-metric smuggling.
- next_step: Inspect the derivation-burden checklist before treating any
  candidate mechanism as progress.

### Exact-GR Benchmark Boundary

- premise: The project preserves ordinary GR as the observable benchmark while
  keeping the substrate derivation burden open.
- mechanism: The explainer should show the benchmark as a constraint on the
  research program rather than as evidence that the ontology has already
  succeeded.
- source_basis: `AGENTS.md`, `README.md`, and `registries/TEX_SOURCE_REGISTRY.csv`.
- authority_status: Explanatory summary of registered claim boundaries.
- uncertainty: Which source-defined substrate laws, if any, can recover the
  benchmark remains unresolved.
- validation_or_test: Candidate structures must be checked for dimensional
  consistency, invariance, anti-smuggling, and recovery of known limiting
  behavior.
- next_step: Route derivation candidates through bounded research-control jobs
  rather than expanding the explainer into scientific authority.

## Non-Goals

- Do not assert that the ontology derives GR.
- Do not add new equations, proof claims, or empirical predictions.
- Do not alter canonical ontology TeX or registry status.
- Do not use external images or network-dependent assets.
