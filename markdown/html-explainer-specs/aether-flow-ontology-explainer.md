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
- A source-authority panel pointing readers back to registered TeX and registry
  rows for scientific authority.
- A claim-boundary notice stating that this page is human-only and
  non-authoritative.

## Non-Goals

- Do not assert that the ontology derives GR.
- Do not add new equations, proof claims, or empirical predictions.
- Do not alter canonical ontology TeX or registry status.
- Do not use external images or network-dependent assets.
