---
title: "Project Overview Explainer"
purpose: "Provide a first-read human visual overview of the dual physics and AI research-agent missions, source-first authority chain, and open exact-GR derivation boundary."
audience: "New readers, project maintainers, research agents, and reviewers who need a compact map of the repository's purpose and current claim status."
output_path: "html/project-overview-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "markdown/html-explainer-specs/research-control-system-explainer.md"
claim_boundary: "Human-only project overview. It summarizes the existing dual-track project identity and exact-GR benchmark/open-derivation boundary without changing physics claims, control contracts, routing decisions, or registry authority."
human_visual_only: true
explainer_kind: "project_overview"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
required_controls:
  - "section_toc"
  - "expandable_analysis_panels"
  - "source_drilldowns"
  - "claim_boundary_toggle"
source_drilldowns:
  - "README.md"
  - "AGENTS.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
analysis_capsule_schema:
  - "premise"
  - "mechanism"
  - "source_basis"
  - "authority_status"
  - "uncertainty"
  - "validation_or_test"
  - "next_step"
---

# Project Overview Explainer Spec

## Rendering Intent

Create a self-contained HTML explainer for a reader arriving at the repository
front door. The page should show the two linked missions, the exact-GR benchmark
boundary, the open first-principles derivation burden, and the source-first
authority chain.

## Required Visual Structure

- A two-track project map separating the physics research track from the AI
  research-agent development track.
- A front-facing hub with three exploration paths: ontology and GR derivation
  goal, staged-autonomy physics/math research-agent harness, and source
  authority / claim-boundary discipline.
- A status strip distinguishing established repository state, open derivation
  burden, and human-only explanatory material.
- An authority ladder showing canonical `.tex` sources, registries, registered
  Markdown, and generated derivatives.
- A short visual path from README overview to Markdown specs to generated HTML
  explainers.
- Expandable source drilldowns that state why each cited source matters and
  what boundary or claim-status check it supports.
- A claim-boundary notice stating that this page is human-only and
  non-authoritative.
- Deep-first progressive-disclosure controls for expandable analysis capsules,
  source drilldowns, and claim-boundary
  inspection.

## Required Analysis Capsules

### Ontology and GR Derivation Goal

- premise: The project studies whether ordinary GR can be interpreted and
  eventually derived from a deeper `Æther` / `Æther-flow` ontology.
- mechanism: The front page should explain the ontology as a substrate and flow
  framing, then show the open derivation target: recover effective Lorentzian
  geometry, causal structure, clock behavior, matter coupling, and invariance
  without importing the GR metric by hand.
- source_basis: `README.md`, `AGENTS.md`, and
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- authority_status: Explanatory overview only; canonical science authority
  remains in registered `.tex` sources and registries.
- uncertainty: The first-principles derivation from substrate structure remains
  open.
- validation_or_test: A valid research path must pass claim gates and recover
  the exact-GR benchmark without hidden target import.
- next_step: Direct readers to the ontology explainer for the detailed
  derivation burden.

### Staged-Autonomy Research Harness

- premise: The AI track is a staged-autonomy physics/math research-agent
  harness, not a current autonomous proof system.
- mechanism: The project develops the harness by running it against the hard
  GR-derivation problem with human accountability, role routing, validators,
  claim gates, and source-first memory.
- source_basis: `README.md`, `AGENTS.md`, and the research-agent workflow
  explainer spec.
- authority_status: AI-methodology explanation; it does not establish any
  physics claim.
- uncertainty: Autonomy is a long-term technical target, and current operation
  remains human-accountable and validator-gated.
- validation_or_test: The harness improves only when bounded jobs, validation,
  handoffs, and negative-result preservation remain reproducible.
- next_step: Direct readers to the research-agent workflow explainer for the
  operational loop.

## Non-Goals

- Do not introduce new physics claims.
- Do not imply that GR has been derived from the ontology.
- Do not change project-control rules.
- Do not use external images or network-dependent assets.
