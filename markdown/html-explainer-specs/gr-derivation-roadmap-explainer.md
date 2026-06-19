---
title: "GR Derivation Roadmap"
purpose: "Explain the tracked GR derivation burden chain and current status vocabulary without changing physics status or promoting draft/control work."
audience: "Technical readers, maintainers, reviewers, research agents, and external AI readers."
output_path: "html/gr-derivation-roadmap-explainer.html"
github_markdown_output_path: "github-facing/gr-derivation-roadmap-explainer.md"
wiki_output_path: "wiki/html/html-gr-derivation-roadmap-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/gr-derivation-roadmap.publication-brief.md"
document_type: "decision_or_lifecycle_guide"
visual_strategy: "process_timeline"
migration_status: "reviewed"
source_materials:
  - "research_control/design/gr_derivation_burden_map.md"
  - "registries/DISTANCE_TO_GR_LEDGER.csv"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "registries/AGENT_JOB_REGISTRY.csv"
  - "research_control/README.md"
  - "AGENTS.md"
claim_boundary: "Human-only publication explainer for the GR derivation roadmap. It orients readers to milestone burdens, Distance-to-GR ledger categories, future AgentJob fields, mathematical payload requirements, source-extension and finite toy categories, and current-frontier cautions without updating physics status, adopting M_src, deriving g_eff, matter coupling, or Einstein equations, promoting the benchmark, issuing a Gate Chair verdict, or treating generated outputs as authority."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# GR Derivation Roadmap Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/gr-derivation-roadmap.publication-brief.md`
as the page-specific editorial contract. The page is a
decision-or-lifecycle guide for the tracked derivation-control surface. It is
not a physics proof, not a ledger update, and not a claim-promotion record.

## Source Basis

- `research_control/design/gr_derivation_burden_map.md` defines the milestone
  chain, allowed status vocabulary, future AgentJob fields, mathematical
  payload rule, constructive preference, freeze criteria, source-extension
  category, and finite toy model target.
- `registries/DISTANCE_TO_GR_LEDGER.csv` records live burden rows and current
  statuses including accepted `Resp_lc`, draft/control `M_src`, not-started
  downstream metric/coupling/equation burdens, human-gated benchmark
  promotion, and locally frozen finite toy route status.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv` supplies active boundaries against
  ontology edits, benchmark promotion, completed derivation language,
  generated-output authority, source-authority laundering, and global
  no-go inflation.
- `registries/AGENT_JOB_REGISTRY.csv` shows that physics jobs are bounded
  transactions and that documentation packets are separate from physics
  derivation jobs.
- `research_control/README.md` explains the one-job rule, future physics
  AgentJob milestone fields, the Distance-to-GR ledger, memory preflight, and
  documentation-impact discipline.
- `AGENTS.md` defines the repository authority hierarchy and generated-output
  boundaries.

## Required Reader Outcome

After reading, a reader should understand that the project is tracking a
chain from source ontology to benchmark promotion. They should know why
`source_ontology`, `EqSrc`, `ObsLoc_lc`, `Resp_lc`, `M_src`, `g_eff`,
`matter_coupling`, `einstein_equations`, `finite_toy_metric_response`, and
`benchmark_promotion` are separate burdens. They should also know that a
validator pass, generated public page, screenshot, or bootstrap refresh is
not physics evidence. The opening should teach the roadmap as burden control,
not progress celebration, while the full generated-noncanonical authority
paragraph belongs in the footer authority section.

## Visual Strategy

Use a process timeline. The visual should help the reader see ordered
milestones, current status categories, and which burdens are still blocked,
draft/control, frozen, not started, or human-gated. Pair the timeline with a
burden-versus-evidence matrix and a current-frontier caution panel. Do not use
a generic source-to-output diagram or browser-side Mermaid.

## Acceptance Criteria

- Explains each roadmap milestone and visible status category.
- Names `target_derivation_milestone`, `milestone_burden`, and
  `new_mathematical_payload`.
- Preserves `draft/control`, `source-only`, `source-extension data`, `local`,
  `exact-branch`, and `human-gated` qualifiers.
- Explains source-extension and finite toy categories without treating them as
  GR recovery shortcuts.
- Explains freeze labels as scoped route-control labels, not global theory
  rejection.
- Names source paths visibly in GitHub Markdown and HTML.
- Places the full generated-noncanonical authority paragraph only in the
  GitHub Markdown and HTML authority footer.
- Preserves generated noncanonical status.
