---
title: "Exact-GR Benchmark Boundary"
purpose: "Explain the boundary between exact-GR benchmark adoption and open first-principles substrate derivation."
audience: "External technical readers, maintainers, reviewers, research agents, and summarizing AI readers."
output_path: "html/exact-gr-benchmark-boundary-explainer.html"
github_markdown_output_path: "github-facing/exact-gr-benchmark-boundary-explainer.md"
wiki_output_path: "wiki/html/html-exact-gr-benchmark-boundary-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/exact-gr-benchmark-boundary.publication-brief.md"
document_type: "comparison_or_boundary_map"
visual_strategy: "source_matrix"
migration_status: "reviewed"
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "registries/TEX_SOURCE_REGISTRY.csv"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "research_control/design/gr_derivation_burden_map.md"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/design/epistemic_category_glossary.md"
claim_boundary: "Human-only publication explainer for the exact-GR benchmark boundary. It distinguishes adoption, compatibility, derivation, and promotion without creating physics claims, benchmark promotion, Gate Chair approval, routing authority, validator authority, or generated-output authority."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Exact-GR Benchmark Boundary Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/exact-gr-benchmark-boundary.publication-brief.md`
as the page-specific editorial contract. The page is a comparison and boundary
map, not a proof and not a claim gate.

## Source Basis

- `README.md` states the public benchmark boundary: ordinary GR at observable
  scale, one operative metric, universal matter coupling, standard causal
  structure, and open first-principles derivation.
- `AGENTS.md` defines source authority and generated-output boundaries.
- `ontology/aether-and-aether-flow.md` distinguishes operational adoption from
  derivation from explicit substrate structure.
- `registries/TEX_SOURCE_REGISTRY.csv` names the registered TeX sources that
  carry benchmark claims and their claim status.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv` records task-level claim boundaries
  that block benchmark promotion, derivation claims, and generated-derivative
  authority.
- `research_control/design/gr_derivation_burden_map.md` names the open burden
  chain from source ontology through benchmark promotion.
- `research_control/design/public_status_exists_does_not_exist_source_spec.md`
  supplies the simplified public exists / does-not-exist status table,
  including proposed AEther-flow ontology status, open GR derivation, blocked
  benchmark promotion, blocked Einstein equations, scoped `M_src`, scoped
  `g_eff`, and scoped matter-coupling evidence/preconditions.
- `research_control/design/epistemic_category_glossary.md` supplies category
  distinctions for interpretation, model, benchmark compatibility, derivation,
  evidence/precondition, adoption, promotion, validator receipt, publication,
  and authority source.

## Required Reader Outcome

After reading, a reader should be able to say: the project uses an exact-GR
benchmark as a conservative operational boundary; it has not completed a
first-principles substrate derivation; benchmark promotion remains a gated
matter for source authority, not public derivative prose. The opening should
teach adoption, compatibility, derivation, and promotion as separate statuses
before authority metadata, while the full generated-noncanonical authority
paragraph belongs in the footer authority section.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: boundary explanation only. It does not change benchmark status,
certify a derivation, issue a Gate Chair verdict, or make HTML, PDFs, or
GitHub-facing Markdown into scientific authority.

## Visual Strategy

Use a source matrix and comparison table. The visual should teach which layer
owns adoption, derivation, promotion, and public explanation. Do not use a
generic documentation-flow diagram.

## Acceptance Criteria

- Includes an adoption-versus-derivation matrix.
- Includes a benchmark-boundary ladder from canonical TeX to public
  derivatives.
- Includes a failure-mode panel for common overclaims.
- Names `registries/TEX_SOURCE_REGISTRY.csv` and
  `registries/CLAIM_BOUNDARY_REGISTRY.csv` as source paths.
- Names `research_control/design/public_status_exists_does_not_exist_source_spec.md`
  and `research_control/design/epistemic_category_glossary.md` when explaining
  public status, and keeps benchmark promotion blocked by upstream derivation
  burdens and protected authority.
- Uses positive-first status-card wording for high-risk scoped rows:
  positive scoped status, exact scope, allowed use, then blocked overread.
- Uses the bottom Reader Scope hook immediately above the marked authority
  footer in GitHub Markdown and tracked HTML.
- Places the full generated-noncanonical authority paragraph only in the
  GitHub Markdown and HTML authority footer.
- Preserves the noncanonical status of GitHub-facing Markdown and HTML.
