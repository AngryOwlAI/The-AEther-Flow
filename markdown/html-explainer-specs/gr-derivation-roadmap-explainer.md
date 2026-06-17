---
title: "GR Derivation Roadmap"
purpose: "Explain how AEther-Flow tracks the open route from source-side ontology to ordinary GR or an exact-GR benchmark without promoting the derivation."
audience: "Technical readers, research agents, and reviewers who need to understand the derivation milestones, burden ledger, freeze criteria, and controlled source-extension path."
output_path: "html/gr-derivation-roadmap-explainer.html"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/design/gr_derivation_burden_map.md"
  - "registries/DISTANCE_TO_GR_LEDGER.csv"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - ".agents/roles/physics/theoretical-continuation-selector.v0.1.0.md"
claim_boundary: "Human-only derivation-roadmap explainer. It may summarize tracked milestone burdens, ledger semantics, selector routing, source-extension categories, toy-model target, and freeze criteria, but it does not promote ontology, metric, matter-coupling, Einstein-equation, benchmark, or Gate Chair claims."
human_visual_only: true
explainer_kind: "conceptual_model"
interaction_model: "progressive_disclosure"
analysis_depth: "deep"
presentation_profile: "claim_boundary_map"
layout_intent: "Use a milestone roadmap with burden rows, status distinctions, and clear open/blocked/freeze boundaries so readers can see what remains to be derived."
required_controls:
  - "section_toc"
  - "source_materials_section"
required_content_blocks:
  - "subject_summary"
  - "milestone_chain"
  - "distance_ledger"
  - "selector_and_freeze"
  - "source_extension_and_toy"
  - "claim_boundary"
---

# GR Derivation Roadmap Spec

## Rendering Intent

Create a source-backed HTML and GitHub-facing explainer for the project's
Distance-to-GR planning function. The subject is not a completed derivation.
The subject is the control mechanism that keeps each future physics AgentJob
attached to a named derivation milestone, a stated burden, an updated ledger,
and a freeze or continuation decision when the same obstacle recurs.

The page should make the milestone chain readable as an ordered dependency
map:

- source ontology primitives;
- source equivalence and localization objects;
- response localization;
- source manifold and effective metric;
- matter coupling and Einstein equations;
- benchmark promotion and Gate Chair status; and
- finite toy metric-response scaffolding.

The page should emphasize the practical difference between a draft object,
a constructive witness, a blocked primitive, a frozen negative route, and
human-gated benchmark promotion.

## Source-Backed Summary

Summary heading: `Summary of GR Derivation Roadmap`

Summary text:

The GR derivation roadmap is the project's control surface for the open physics burden. It keeps the public target conservative: ordinary GR remains the observable benchmark, while a first-principles derivation from AEther or AEther-flow substrate structure remains unresolved. The roadmap names the physics objects that must exist before benchmark promotion can be considered, records their current status in the Distance-to-GR ledger, and requires future physics AgentJobs to declare the milestone and burden they are trying to advance. This prevents a useful candidate, a workflow completion, or a generated explanation from being mistaken for a completed derivation. It also gives negative results a stable place: repeated selector underdetermination, scoped obstruction, source-extension pressure, or finite toy-model failure can freeze a route without rejecting the entire ontology.

Summary source basis:

- `README.md`
- `research_control/README.md`
- `research_control/design/gr_derivation_burden_map.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`

## Required Content Blocks

- subject_summary: A source-backed summary of GR Derivation Roadmap that directly explains the open physics burden, why milestone tracking exists, how the Distance-to-GR ledger controls future physics jobs, and which source paths ground the explanation: `README.md`, `research_control/README.md`, `research_control/design/gr_derivation_burden_map.md`, `registries/DISTANCE_TO_GR_LEDGER.csv`.
- milestone_chain: A reader-facing block on the milestone dependency chain from source ontology through benchmark promotion, including draft objects, missing primitives, and the finite toy metric-response target; source paths: `research_control/design/gr_derivation_burden_map.md`, `registries/DISTANCE_TO_GR_LEDGER.csv`.
- distance_ledger: A reader-facing block on the persistent ledger function, allowed status vocabulary, required future completion fields, and why ledger updates differ from scientific acceptance; source paths: `research_control/design/gr_derivation_burden_map.md`, `registries/DISTANCE_TO_GR_LEDGER.csv`, `research_control/README.md`.
- selector_and_freeze: A reader-facing block on theoretical-continuation selector routing, repeated-burden handling, candidate freeze labels, and the boundary between local obstruction and global no-go claims; source paths: `research_control/README.md`, `research_control/design/gr_derivation_burden_map.md`, `.agents/roles/physics/theoretical-continuation-selector.v0.1.0.md`, `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- source_extension_and_toy: A reader-facing block on controlled source-extension categories and finite toy metric-response construction as draft scaffolding, including the no-target-import rule; source paths: `research_control/design/gr_derivation_burden_map.md`, `AGENTS.md`.
- claim_boundary: A reader-facing block on what the roadmap can and cannot claim: planning status, burden status, and freeze labels are not ontology adoption, metric derivation, coupling derivation, Einstein-equation derivation, benchmark promotion, or Gate Chair approval; source paths: `AGENTS.md`, `registries/CLAIM_BOUNDARY_REGISTRY.csv`, `research_control/design/gr_derivation_burden_map.md`.
