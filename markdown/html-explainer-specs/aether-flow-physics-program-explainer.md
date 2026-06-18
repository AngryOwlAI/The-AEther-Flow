---
title: "AEther-Flow Physics Program"
purpose: "Orient readers to the physics track as a benchmark-disciplined, claim-gated research program with open derivation burdens."
audience: "New technical readers, maintainers, reviewers, research agents, and external AI readers."
output_path: "html/aether-flow-physics-program-explainer.html"
github_markdown_output_path: "github-facing/aether-flow-physics-program-explainer.md"
wiki_output_path: "wiki/html/html-aether-flow-physics-program-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/aether-flow-physics-program.publication-brief.md"
document_type: "overview_article"
visual_strategy: "layered_architecture"
migration_status: "reviewed"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "research_control/README.md"
  - "research_control/design/gr_derivation_burden_map.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
claim_boundary: "Human-only publication explainer for the AEther-Flow physics program. It orients readers to ontology, benchmark discipline, open derivation burden, negative-result preservation, and gates without promoting ontology, benchmark, derivation, Gate Chair status, or generated-output authority."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# AEther-Flow Physics Program Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/aether-flow-physics-program.publication-brief.md`
as the page-specific editorial contract. The page is an overview article for
physics status, not a derivation note.

## Source Basis

- `README.md` defines the two project tracks and public benchmark language.
- `AGENTS.md` defines claim boundaries, generated-output boundaries, and
  research-control routing discipline.
- `ontology/aether-and-aether-flow.md` gives the front-facing ontology while
  explicitly leaving first-principles substrate derivation open.
- `research_control/README.md` explains the AgentJob, claim-gate, negative
  result, and human-gate workflow.
- `research_control/design/gr_derivation_burden_map.md` names the derivation
  burden chain and current status categories.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv` records concrete claim boundaries
  that prevent local artifacts from becoming broad physics claims.

## Required Reader Outcome

After reading, a reader should be able to summarize the physics program as a
controlled research program: ontology and benchmark discipline are present,
the first-principles derivation remains open, negative results are preserved,
and claim promotion requires source authority and gates.

## Visual Strategy

Use layered architecture: ontology, benchmark, derivation burden, negative
results, and gate status are separate layers. Include safe and unsafe summary
examples. Do not turn the page into a task transcript or role manual.

## Acceptance Criteria

- Separates ontology, exact-GR benchmark, derivation burden, and gate status.
- Explains no-go, obstruction, and freeze records without global no-go
  inflation.
- Preserves qualifiers such as `draft/control`, `source-only`, `local`,
  `exact-branch`, `source-extension data`, and `human-gated`.
- Names source paths visibly in GitHub Markdown and HTML.
- Preserves generated noncanonical status.

