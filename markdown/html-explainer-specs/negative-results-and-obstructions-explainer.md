---
title: "Negative Results And Obstructions"
purpose: "Explain frozen local routes and scoped obstructions as useful source-backed constraints without turning them into global no-go claims."
audience: "Technical readers, maintainers, reviewers, research agents, and external AI readers."
output_path: "html/negative-results-and-obstructions-explainer.html"
github_markdown_output_path: "github-facing/negative-results-and-obstructions-explainer.md"
wiki_output_path: "wiki/html/html-negative-results-and-obstructions-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/negative-results-and-obstructions.publication-brief.md"
document_type: "comparison_or_boundary_map"
visual_strategy: "source_matrix"
migration_status: "deferred"
source_materials:
  - "research_control/design/negative_result_inventory_v15.md"
  - "research_control/design/frontier_theorem_inventory.md"
  - "registries/DISTANCE_TO_GR_LEDGER.csv"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/design/epistemic_category_glossary.md"
  - "AGENTS.md"
claim_boundary: "Human-only publication source spec for a future negative-results explainer. It may frame frozen routes, scoped obstructions, certificate gaps, minimal countermodels, and open continuation boundaries as source-backed constraints. It does not publish the page, create generated public outputs, reject the research program, prove future source-extension impossibility, promote a benchmark, issue a Gate Chair verdict, adopt matter semantics, adopt detector semantics, derive matter coupling, derive Einstein equations, or complete the derivation."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Negative Results And Obstructions Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/negative-results-and-obstructions.publication-brief.md`
as the page-specific editorial contract. The page is a comparison and boundary
map for negative results. It is not a research result, a Gate Chair decision, a
physics adoption record, or a public release action by itself.

This source spec authorizes derivative reader surfaces only when they are
generated through the approved source-spec path. Those derivatives remain
generated noncanonical reader surfaces, not physics authority and not
publication action by themselves.

## Source Basis

- `research_control/design/negative_result_inventory_v15.md` is the primary
  source for current frozen, obstructed, failed, or counterexample-bearing
  routes and for the fields that separate what each result blocks from what it
  does not block.
- `research_control/design/frontier_theorem_inventory.md` supplies theorem and
  stress-test context for the inventory entries without replacing their source
  artifacts.
- `registries/DISTANCE_TO_GR_LEDGER.csv` supplies current burden status for
  high-risk rows such as `Resp_lc`, matter coupling, Einstein equations,
  benchmark promotion, and the finite toy metric-response route.
- `research_control/design/public_status_exists_does_not_exist_source_spec.md`
  supplies the public exists / does-not-exist contract that prevents scoped
  evidence or local obstruction from becoming downstream physics promotion.
- `research_control/design/epistemic_category_glossary.md` supplies the
  category distinctions among interpretation, model, evidence, adoption,
  validation receipt, publication surface, and authority source.
- `research_control/design/status_card_v2_schema.md` and
  `research_control/design/accepted_status_calibration_v2.yaml` supply the
  public order for positive status, exact scope, blocked overread, and next
  burden when negative-result pages mention high-risk burdens.
- `AGENTS.md` defines the authority hierarchy and the rule that generated
  reader surfaces remain derivative.

## Required Reader Outcome

After reading, a reader should understand five boundaries.

1. A frozen route means a specific attempted route is not to be reused as if it
   still supported the target claim. It does not prove that every redesigned
   route or conservative source-extension route is impossible.
2. A scoped obstruction means the current premises or current route fail for a
   named reason and scope. It is not a program-wide rejection claim unless a
   separate source-backed no-go theorem establishes that stronger conclusion.
3. Negative results matter because they preserve constraints, prevent repeated
   overreads, provide adversarial examples for future packets, and improve
   route selection.
4. Current frozen or obstructed routes must be summarized from the inventory
   and ledger, with source paths visible, without replacing those sources.
5. The open continuation set remains visible: redesigned finite toy routes,
   source-side selector laws, certificate-indexed transport or invariance
   routes, and future source-extension candidates remain open unless a tracked
   authority source closes them.

## Source Matrix Strategy

Use a source matrix rather than a generic lifecycle diagram. Each row should
represent one negative-result family from the inventory. Columns should be:

- source artifact;
- route or claim attempted;
- negative-result type;
- what the result blocks;
- what the result does not block;
- lawful reuse.

The matrix should include at minimum:

- finite toy metric-response frozen route;
- `Resp_lc` old-tuple selector obstruction;
- `RR_E` underdetermination obstruction;
- `RR_E` finite separation witness;
- P2 certificate-gap witness for `NarrowMSCertEq_v1`;
- the P10 route-orbit note that no route-orbit freeze was triggered.

The visual purpose is source inspection. A reader should learn where to look,
what scope is closed, and what overread is blocked.

## Required Sections For Future Explainer

Use page-specific headings that serve the reader job. The future page should
cover:

- why the project preserves negative results;
- frozen route versus scoped obstruction;
- current inventory;
- what remains open;
- safe public wording;
- source materials and authority boundary.

Do not use the retired universal heading sequence.

## Reader Scope Footer Binding

GitHub Markdown and tracked HTML derivatives must place the page-specific
Reader Scope boundary at the bottom of the reader content, immediately before
the marked authority footer. Preserve this boundary text exactly unless a
future source inspection authorizes a wording repair:

Reader scope: negative-result explanation only. This page cannot reject the
research program, prove future source-extension impossibility, promote a
benchmark, issue a Gate Chair decision, derive matter coupling, derive
Einstein equations, complete the derivation, or supersede tracked source
artifacts.

## Acceptance Criteria

- Defines frozen route and scoped obstruction in plain technical language.
- Explains why negative results are first-class constraints.
- Summarizes current frozen, obstructed, failed, or counterexample-bearing
  routes from `research_control/design/negative_result_inventory_v15.md`.
- States what remains open after each negative result.
- Uses status-card v2 order for public negative-result summaries: scoped
  status, exact route scope, blocked overread, and next burden.
- States that exact source artifacts and registries remain authority.
- Names source paths visibly in any generated GitHub Markdown and HTML.
- Uses the bottom Reader Scope hook immediately above the marked authority
  footer in generated GitHub Markdown and tracked HTML.
- Preserves generated noncanonical status for any future public surface.
- Does not imply that this source spec itself created public output.

## Forbidden Readings

- Scoped obstruction as program-wide rejection.
- Frozen local route as future source-extension impossibility.
- Minimal countermodel as matter semantics, detector semantics, coupling law,
  matter coupling, stress-energy semantics, matter action, Einstein equations,
  benchmark promotion, or completed derivation.
- Generated page, validator pass, wiki note, screenshot, or source spec as
  physics proof authority.
- Any public page as a replacement for the exact source artifacts and
  registries.
