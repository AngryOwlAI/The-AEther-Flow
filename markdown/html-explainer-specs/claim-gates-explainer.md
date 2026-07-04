---
title: "Claim Gates, Negative Results, And Freeze Criteria"
purpose: "Explain the project's claim-control lifecycle and negative-result boundaries without issuing a Gate Chair verdict or changing any claim boundary."
audience: "Technical readers, maintainers, reviewers, research agents, and external AI readers."
output_path: "html/claim-gates-explainer.html"
github_markdown_output_path: "github-facing/claim-gates-explainer.md"
wiki_output_path: "wiki/html/html-claim-gates-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/claim-gates.publication-brief.md"
document_type: "comparison_or_boundary_map"
visual_strategy: "state_model"
migration_status: "reviewed"
source_materials:
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/design/gr_derivation_burden_map.md"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/design/epistemic_category_glossary.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/AGENT_ROLE_REGISTRY.csv"
claim_boundary: "Human-only publication explainer for claim gates, negative results, and freeze criteria. It explains proposal, audit, refutation, stress-test, completion, handoff, freeze, and human-gate concepts without creating a claim boundary, issuing a Gate Chair verdict, promoting benchmark status, rejecting the global ontology, changing role authority, or treating validator pass state or generated public documentation as scientific evidence."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Claim Gates Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/claim-gates.publication-brief.md` as the
page-specific editorial contract. The page is a comparison and boundary map
for the project's claim-control lifecycle. It is not a Gate Chair decision, a
claim-boundary registry update, a physics review, or a global verdict on the
ontology.

## Source Basis

- `AGENTS.md` defines the repository authority hierarchy and generated-output
  boundaries.
- `research_control/README.md` defines Director decisions, AgentJobs,
  execution roles, completions, handoffs, validators, memory preflight, human
  gates, and documentation-impact discipline.
- `research_control/design/gr_derivation_burden_map.md` defines derivation
  burdens, allowed Distance-to-GR status vocabulary, mathematical payload
  expectations, constructive preference, freeze criteria, source-extension
  categories, and finite toy model boundaries.
- `research_control/design/public_status_exists_does_not_exist_source_spec.md`
  supplies the simplified public high-risk status contract and examples where
  scoped acceptance or scoped evidence/precondition status must not be overread
  as downstream physics promotion.
- `research_control/design/epistemic_category_glossary.md` supplies the public
  category distinctions that keep interpretation, model, evidence, adoption,
  validator receipt, publication surface, and authority source separate.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv` supplies active examples of
  allowed claims, forbidden claims, required gates, and authority source
  paths.
- `registries/AGENT_ROLE_REGISTRY.csv` records the Gate Chair as human-gated
  and shows that Documentation Curator cannot promote claims.

## Required Reader Outcome

After reading, a reader should understand that AEther-Flow preserves failed
routes and scoped obstructions because they improve future reasoning. They
should also know that a completion record, validator pass, freeze label, public
explainer, wiki note, or screenshot is not enough to promote a physics claim.
Human-gated roles remain human-gated, and a rejected or frozen draft/control
packet is not a global rejection of the whole theory. The opening should teach
scope discipline before authority metadata, while the full
generated-noncanonical authority paragraph belongs in the footer authority
section.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: claim-control explanation only. It does not create a claim
boundary, issue a Gate Chair verdict, promote a benchmark, reject the global
ontology, change role authority, supersede tracked source files, or treat
validator pass state as scientific evidence.

## Visual Strategy

Use a state model. The visual should show movement from proposal to audit,
refutation or stress test, completion, possible handoff, possible freeze, and
possible human gate. Pair it with a scoped-obstruction versus global-no-go
comparison and an allowed/forbidden claim table. Do not use a generic
source-to-validation diagram or browser-side Mermaid.

## Acceptance Criteria

- Defines proposal, audit, refutation, stress test, completion, handoff,
  freeze, and human gate without changing role authority.
- Explains negative-result preservation as scientific discipline.
- Separates scoped obstruction from global no-go language.
- States that Gate Chair decisions require human-gated authority.
- Includes allowed and forbidden claim examples grounded in
  `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- Includes public-status gate examples grounded in
  `research_control/design/public_status_exists_does_not_exist_source_spec.md`
  and `research_control/design/epistemic_category_glossary.md`, including why
  AEther-flow is proposed research ontology / explanatory frame only and why
  scoped `M_src`, scoped `g_eff`, and scoped matter-coupling
  evidence/preconditions are not source-law, matter-coupling,
  Einstein-equation, benchmark, or completed-derivation claims.
- Names source paths visibly in GitHub Markdown and HTML.
- Uses the bottom Reader Scope hook immediately above the marked authority
  footer in GitHub Markdown and tracked HTML.
- Places the full generated-noncanonical authority paragraph only in the
  GitHub Markdown and HTML authority footer.
- Preserves generated noncanonical status.
