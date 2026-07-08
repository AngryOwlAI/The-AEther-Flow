---
title: "AEther-Flow Ontology"
purpose: "Explain the AEther-Flow ontology vocabulary and its limits without promoting ontology or claiming a completed GR derivation."
audience: "Technical readers, maintainers, reviewers, research agents, and external AI readers."
output_path: "html/aether-flow-ontology-explainer.html"
github_markdown_output_path: "github-facing/aether-flow-ontology-explainer.md"
wiki_output_path: "wiki/html/html-aether-flow-ontology-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/aether-flow-ontology.publication-brief.md"
document_type: "concept_explainer"
visual_strategy: "layered_architecture"
migration_status: "reviewed"
source_materials:
  - "ontology/aether-and-aether-flow.md"
  - "ontology/aether_flow_interpretation-lemen.md"
  - "ontology/README.md"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "AGENTS.md"
claim_boundary: "Human-only publication explainer for AEther-Flow ontology vocabulary. It orients readers to AEther, AEther-flow, observed space, S-time, observed expansion, live versus legacy ontology sources, and the missing observer normal/readout source construction without promoting ontology, completing a derivation, changing benchmark status, or treating generated outputs as authority."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# AEther-Flow Ontology Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/aether-flow-ontology.publication-brief.md`
as the page-specific editorial contract. The page is a concept explainer for
ontology vocabulary and limits, not a canonical ontology extension and not a
derivation note.

## Source Basis

- `ontology/aether-and-aether-flow.md` gives the current front-facing
  ontology vocabulary and explicitly leaves the first-principles substrate
  derivation open.
- `ontology/aether_flow_interpretation-lemen.md` provides authored source
  material for the interpretive story, exact-closure posture, and contrast
  with older static three-dimensional aether theories.
- `ontology/README.md` defines the live ontology folder, live-versus-legacy
  boundary, and TeX authority boundary.
- `registries/TEX_SOURCE_REGISTRY.csv` identifies registered TeX sources as
  scientific authority and marks current ontology TeX as canonical while
  preserving that the broader first-principles GR derivation is not solved.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv` records active claim boundaries
  against ontology promotion, benchmark promotion, completed-derivation
  claims, and generated-output authority.
- `research_control/design/status_card_v2_schema.md` and
  `research_control/design/accepted_status_calibration_v2.yaml` define the
  concise public order for status summaries that mention downstream burdens
  such as `M_src`, `g_eff`, matter coupling, Einstein equations, and benchmark
  promotion.
- `AGENTS.md` defines the repository-wide source authority hierarchy and
  generated-output boundaries.

## Required Reader Outcome

After reading, a reader should be able to use the project vocabulary without
overclaiming: AEther is the deeper four-dimensional substrate, AEther-flow is
its intrinsic ordered motion, observed three-dimensional space is an
observer-level slice, S-time is experienced order of change, and observed
expansion is a three-dimensional appearance of deeper ordered motion. The
reader should also know that this vocabulary does not by itself derive GR.
The opening should teach vocabulary, source authority, mathematical burden,
and empirical-prediction separation before authority metadata, while the full
generated-noncanonical authority paragraph belongs in the footer authority
section.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: ontology orientation only. It can help readers use the
vocabulary, but it does not promote ontology, certify exact-GR recovery,
complete the derivation, change a claim boundary, or supersede registered TeX
sources.

## Visual Strategy

Use layered architecture. The visual should separate ontology vocabulary,
source authority, open mathematics, and public derivative explanation. Include
a live-versus-legacy comparison and a model/mathematics/prediction separation
panel. Do not use a generic workflow diagram or browser-side Mermaid.

## Acceptance Criteria

- Explains AEther, AEther-flow, observed three-dimensional space, S-time, and
  observed expansion as ontology vocabulary.
- Labels gravity-as-reorganization language as heuristic unless a registered
  TeX source states a stronger claim.
- Distinguishes live `ontology/` from archival `legacy_ontology/`.
- Names the missing observer normal/readout source construction as open work.
- States ontology status in status-card v2 order: positive vocabulary status,
  exact ontology-lane scope, blocked overread, and next mathematical burden.
- Avoids older three-dimensional aether, wind, river, or ordinary fluid
  overreadings.
- Names source paths visibly in GitHub Markdown and HTML.
- Uses the bottom Reader Scope hook immediately above the marked authority
  footer in GitHub Markdown and tracked HTML.
- Places the full generated-noncanonical authority paragraph only in the
  GitHub Markdown and HTML authority footer.
- Preserves generated noncanonical status.
