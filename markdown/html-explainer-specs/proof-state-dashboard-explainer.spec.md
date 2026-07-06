---
title: "Proof-State Dashboard"
purpose: "Define a source-backed public proof-state dashboard that shows positive scoped status, exact scope, allowed use, blocked overread, and next lawful route without promoting physics claims."
audience: "External technical readers, maintainers, reviewers, research agents, and summarizing AI readers."
output_path: "html/proof-state-dashboard-explainer.html"
github_markdown_output_path: "github-facing/proof-state-dashboard-explainer.md"
wiki_output_path: "wiki/html/html-proof-state-dashboard-explainer.md"
renderer_skill: "visual-explainer@0.7.1-project-aether-flow"
publication_brief: "markdown/publication-briefs/proof-state-dashboard.publication-brief.md"
document_type: "visual_brief"
visual_strategy: "annotated_table"
migration_status: "publication_pilot"
source_materials:
  - "research_control/current_frontier.md"
  - "output/compact_current_frontier_v16.yaml"
  - "registries/DISTANCE_TO_GR_LEDGER.csv"
  - "registries/METRIC_USE_LEDGER.csv"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "research_control/design/distance_to_gr_status_aliases.yaml"
  - "research_control/design/accepted_status_calibration_v1.yaml"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/handoffs/handoff-0652.yaml"
claim_boundary: "Human-only dashboard source spec. It may define a public reader-facing table from tracked status cards, but it does not create proof authority, source-law adoption, detector semantics, coupling-law adoption, matter-coupling derivation, Einstein-equation derivation, benchmark promotion, Gate Chair verdict, completed derivation, global rejection, or generated-output authority."
human_visual_only: true
standalone_html: true
no_external_runtime: true
required_controls:
  - "section_toc"
  - "source_materials_section"
---

# Proof-State Dashboard Source Spec

## Publication Brief Binding

Use `markdown/publication-briefs/proof-state-dashboard.publication-brief.md`
as the page-specific editorial contract. The page is a visual brief and status
dashboard, not a proof, claim gate, source-law adoption record, or benchmark
promotion surface.

## Source Basis

- `research_control/current_frontier.md` supplies the active state, next route,
  high-risk status cards, and non-authoritative snapshot boundary.
- `output/compact_current_frontier_v16.yaml` supplies compact machine-readable
  status cards for `m_src`, `g_eff`, `matter_coupling`,
  `einstein_equations`, and `benchmark_promotion`.
- `registries/DISTANCE_TO_GR_LEDGER.csv` supplies persistent burden rows,
  legacy statuses, layered statuses, and evidence paths.
- `registries/METRIC_USE_LEDGER.csv` supplies metric-use overread guards,
  including finite toy metric-response and `g_eff` physical-metric blocks.
- `registries/CLAIM_BOUNDARY_REGISTRY.csv` supplies blocked public-overread
  claims for proof authority, source-law adoption, metric promotion, matter
  coupling, Einstein equations, benchmark promotion, and completed derivation.
- `research_control/design/distance_to_gr_status_aliases.yaml` supplies
  reader-facing aliases and required blocked-overread phrases.
- `research_control/design/accepted_status_calibration_v1.yaml` supplies
  positive-first status cards for high-risk accepted or blocked rows.
- `research_control/design/public_status_exists_does_not_exist_source_spec.md`
  supplies the public exists / does-not-exist table contract.
- `research_control/handoffs/handoff-0652.yaml` supplies the P9-T01 route and
  source-dashboard boundary.

## Required Reader Outcome

After reading the generated dashboard, a reader should be able to say:

- `Resp_lc`, `M_src`, `g_eff`, and matter-sector material have scoped positive
  statuses, each with strict limits.
- Einstein equations are not derived.
- Benchmark promotion remains blocked.
- The finite toy metric-response route is locally frozen, not a global
  impossibility result.
- GR has not been derived from the substrate.
- The public dashboard is a noncanonical derivative that cannot change claim
  status.

## Dashboard Table Contract

Render one table with these columns, in this order:

| Column | Purpose |
| --- | --- |
| Object | The burden, object, or route being summarized. |
| Positive status | What exists or what scoped positive status is present. |
| Exact scope | Where that status is valid. |
| Allowed use | What future bounded packets may use it for. |
| Blocked overread | What the status does not establish. |
| Next lawful route | What Continue Research may do next or why the row remains blocked. |

Render exactly these rows unless a later tracked source changes P9:

| Object | Positive status | Exact scope | Allowed use | Blocked overread | Next lawful route |
| --- | --- | --- | --- | --- | --- |
| `Resp_lc` | accepted only as scoped source-extension selector data | `Xi_X^R` is accepted only as admissible source-extension data for `Resp_lc` continuation through `S_X^+`. | May support later source-side continuation under declared selector-data scope. | No detector semantics, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows. | Use only as upstream scoped source-extension context unless a later bounded packet changes the ledger. |
| `M_src` | `M_src` is adopted only as a scoped source-only `M_src` object. | The adoption applies only under the declared source-only GSC candidate scope and fail-closed boundary. | Later bounded packets may use it as source-side prerequisite context. | It is not a target manifold, metric, matter coupling, Einstein-equation result, benchmark promotion, or completed derivation. | Use as source-side prerequisite context for bounded continuation. |
| `g_eff` | `g_eff` is adopted only as a scoped source-extension `g_eff` object. | The adoption applies only to the declared source-extension candidate scope. | Later bounded packets may use it as scoped source-extension context. | It is not an unscoped Lorentzian metric, `MetricData(E)` adoption, matter coupling, Einstein-equation result, benchmark promotion, or completed derivation. | Use only as scoped source-extension context; metric-use overread remains blocked. |
| `matter_coupling` | `matter_coupling` has accepted scoped evidence/precondition only for continuation. | The support is certificate-indexed, source-side, and finite/local only. | Later bounded packets may use it to construct, audit, or stress one source-side coupling-law candidate. | It is not source-law adoption, detector semantics, coupling-law adoption, matter-coupling derivation, stress-energy semantics, matter action, Einstein-equation result, benchmark promotion, or completed derivation. | Continue through bounded matter-coupling packets only under tracked handoff authority. |
| Einstein equations | not started; no positive derivation status | The status is limited to control status `not_started`, mathematical status `dynamics_action_or_variation_missing`, and physical status `no_field_equation_derivation`. | Later bounded packets may use this row only as a blocked-target boundary condition. | No Einstein equations, benchmark promotion, or completed derivation follows. | Blocked until upstream dynamics, action, variation, matter coupling, and protected authority are established or lawfully routed. |
| Benchmark promotion | no benchmark promotion from scoped evidence/precondition alone | The status is limited to control status `blocked`, mathematical status `upstream_burdens_missing`, and physical status `no_exact_gr_benchmark_promotion`. | Later bounded packets may use this row only as a blocked-target boundary condition. | No benchmark promotion, benchmark Gate Chair closure, or completed derivation follows. | Blocked by upstream derivation burdens and protected authority. |
| Finite toy metric response | frozen local route context only | The finite toy route failed tag-removal stress and is frozen locally. | Use only as a local frozen-negative boundary and redesign signal. | It is not `g_eff` scope expansion, matter-coupling derivation, Einstein equations, benchmark promotion, completed derivation, global theory rejection, or future source-extension impossibility. | Route is frozen or must be redesigned before any broader GR use. |

## Reader Scope Footer Binding

Generated GitHub Markdown and tracked HTML derivatives must place a
page-specific Reader Scope boundary at the bottom of reader content,
immediately before the marked authority footer:

Reader scope: proof-state dashboard only. It does not change the
Distance-to-GR ledger, certify a proof, adopt a source law, derive matter
coupling, derive Einstein equations, promote benchmark status, issue a Gate
Chair verdict, complete the derivation, or make generated public outputs into
scientific authority.

## Acceptance Criteria

- Includes every required P9-T01 dashboard row.
- Includes every required P9-T01 dashboard column.
- States that GR has not been derived.
- Preserves positive-first status-card wording for `Resp_lc`, `M_src`,
  `g_eff`, and `matter_coupling`.
- States Einstein equations are not started and benchmark promotion is blocked.
- States finite toy metric response is a local frozen route, not global
  rejection or future impossibility.
- Names tracked source paths visibly.
- Preserves the noncanonical status of generated GitHub Markdown and HTML.
- Includes desktop and mobile screenshot QA evidence before the publication
  brief row can be marked as a publication pilot.
