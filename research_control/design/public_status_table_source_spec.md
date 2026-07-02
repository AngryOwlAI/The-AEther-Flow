<!-- authority: control -->

# Public Status Table Source Spec

## Scope

This source spec defines the canonical public status table for the v14
status-layer propagation phase. It is a project-control documentation source.
It is not a physics proof surface, not a generated derivative, and not a
claim-promotion authority.

Future README, GitHub-facing Markdown, HTML explainer source specs, and
generated public derivatives may quote, link, or render this table, but they
must not override the tracked sources listed here.

## Authority Order

If a public rendering conflicts with one of these sources, the tracked source
governs in this order:

1. `registries/DISTANCE_TO_GR_LEDGER.csv` for burden-layer status.
2. `research_control/design/distance_to_gr_status_aliases.yaml` for
   reader-facing aliases and object-specific scope wording.
3. The cited task completion or artifact for object-specific evidence status.
4. `research_control/current_frontier.md` as synchronized reader-facing
   snapshot only.
5. This source spec as the public table contract.

Generated wiki notes, HTML, PDFs, local caches, semantic extracts, validator
output, role records, and commits are not independent scientific authority.

## Required Public Columns

Every public status table derived from this source must preserve these columns
or equivalent labels with the same meaning:

| Column | Required meaning |
| --- | --- |
| Burden | The Distance-to-GR burden or high-risk object being summarized. |
| Control status | The workflow, review, gate, or control state. |
| Mathematical status | The formal object, evidence, witness, obstruction, or missing object actually available. |
| Physical status | The physical interpretation that is not established or remains blocked. |
| Promotion status | Whether any downstream GR, benchmark, or completed-derivation promotion is authorized. |
| Exact positive scoped claim | The strongest public-safe positive claim currently allowed. |
| Exact blocked overread | The strongest readings that must not be inferred. |
| Last evidence path | The tracked source path that supports the row. |
| Source authority note | Which tracked source governs the row if a derivative drifts. |
| Public-safe summary | One concise sentence suitable for public documentation. |

## Canonical Public Table

| Burden | Control status | Mathematical status | Physical status | Promotion status | Exact positive scoped claim | Exact blocked overread | Last evidence path | Source authority note | Public-safe summary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `source_ontology_primitives` | `draft_control_object_exists` | `definition_only_or_draft_object` | `no_canonical_ontology_adoption` | `draft_control_only` | Draft source-ontology primitives exist as control-side definitions. | No canonical ontology edit, benchmark promotion, or completed derivation follows from this row. | `AGENTS.md` | Governed by the Distance-to-GR ledger and root project authority guidance. | The source ontology is still a controlled draft surface, not a completed foundation for deriving GR. |
| `M_src` | `gate_review_completed` | `scoped_source_only_adopted_object` | `not_target_manifold_not_metric_not_gr_derivation` | `scoped_source_object_only` | `M_src` has scoped source-only status under the tracked Gate Chair review. | No `MetricData(E)`, `g_eff` scope expansion, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows from this row. | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` | Governed by the Distance-to-GR ledger row plus the cited Gate Chair artifact. | `M_src` is a real scoped source-side object, but it is not a target manifold, metric, or GR derivation. |
| `g_eff` | `gate_review_completed` | `scoped_source_extension_geff_object` | `not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations` | `scoped_source_object_only` | `g_eff` has scoped source-extension object status under its declared source-side scope. | No source-law adoption, `MetricData(E)` adoption, unscoped `g_eff`, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows from this row. | `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex` | Governed by the Distance-to-GR ledger row plus the cited Gate Chair artifact. | `g_eff` is a scoped source-extension object, not an unscoped Lorentzian metric and not a downstream GR result. |
| `matter_coupling` | `accepted_as_scoped_evidence_precondition` | `parameterized_finite_local_witness_precondition` | `not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics` | `scoped_source_evidence_only` | Current matter-coupling evidence is accepted only as scoped source-extension evidence/precondition. | No source-law adoption, `MetricData(E)` adoption, `g_eff` scope expansion, coupling-law adoption, matter-coupling derivation or adoption, stress-energy semantics, stress-energy tensor, matter action, detector semantics, Einstein equations, benchmark promotion, completed derivation, future source-extension impossibility, or program-wide no-go conclusion follows from this row. | `research_control/tasks/RT-20260701-033/artifacts/p2_t02_alias_map_acceptance_receipt.md` | Governed by the Distance-to-GR ledger and high-risk alias map. | Matter coupling remains not derived and not adopted; only scoped evidence/preconditions are available. |
| `SourceMatterSemanticsAdoptionReadinessLaw_v1` | scoped evidence/precondition review completed | proposal-only law target with scoped readiness evidence | not matter semantics, not detector semantics, not coupling law, and not matter coupling | scoped evidence/precondition only | The object may be cited only as scoped source-extension matter-semantics adoption-readiness evidence/precondition. | No source-law adoption, law adoption for this object, matter-semantics adoption, detector-semantics adoption, coupling-law adoption, matter-coupling derivation, Einstein equations, benchmark promotion, or completed derivation follows. | `research_control/tasks/RT-20260701-009/artifacts/source_matter_semantics_adoption_readiness_law_evidence_gate_chair_review_v1.tex` | Governed by the cited Gate Chair artifact, the matter-coupling ledger row, and the alias map object entry. | This object is public-safe only as scoped readiness evidence/precondition, not as an adopted law. |
| `PositiveMSProfile_v1` | scoped evidence/precondition review completed | scoped positive source-semantics profile evidence/precondition | not matter semantics, not detector semantics, not stress-energy, and not matter action | scoped evidence/precondition only | The profile may be cited only as scoped positive source-semantics evidence/precondition. | No source-law adoption, object adoption beyond the exact scoped evidence result, matter-semantics adoption, detector-semantics adoption, stress-energy semantics, matter action, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows. | `research_control/tasks/RT-20260701-020/artifacts/positive_source_matter_semantics_profile_gate_chair_review_v1.tex` | Governed by the cited Gate Chair artifact, the matter-coupling ledger row, and the alias map object entry. | This profile is positive scoped evidence, not adopted matter semantics or physical matter theory. |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` | scoped evidence/precondition review completed | certificate-indexed transport-completeness or invariance evidence/precondition | not source-law adoption, not unrestricted `RR_E` theorem, not detector semantics, and not matter coupling | scoped evidence/precondition only | The object may be cited only as certificate-indexed `RR_E` transport-completeness or invariance evidence/precondition. | No source-law adoption, object adoption, unrestricted `RR_E` irrelevance theorem, detector-semantics collapse, matter semantics, coupling law, matter coupling, `MetricData(E)`, `g_eff`, Einstein equations, benchmark promotion, or completed derivation follows. | `research_control/tasks/RT-20260701-030/artifacts/rr_e_transport_law_gate_chair_review_v1.tex` | Governed by the cited Gate Chair artifact, the matter-coupling ledger row, and the alias map object entry. | `RR_E` transport material is scoped certificate-indexed evidence/precondition only, not a source law or matter-sector bridge. |
| `einstein_equations` | `not_started` | `dynamics_action_or_variation_missing` | `no_field_equation_derivation` | `none` | No positive Einstein-equation derivation status exists. | No Einstein equations, benchmark promotion, or completed derivation follows from current scoped evidence/preconditions. | `research_control/program_state.yaml` | Governed by the Distance-to-GR ledger and live program state. | Einstein equations remain blocked by missing dynamics, action or variation, matter coupling, and protected benchmark authority. |
| `benchmark_promotion` | `blocked` | `upstream_burdens_missing` | `no_exact_gr_benchmark_promotion` | `none` | No benchmark promotion follows from scoped evidence/precondition status alone. | No benchmark promotion, benchmark Gate Chair closure, benchmark fit claim, exact-GR derivation claim, or completed derivation follows. | `research_control/program_state.yaml` | Governed by the Distance-to-GR ledger and live program state. | Exact-GR benchmark promotion remains blocked by upstream derivation burdens and protected authority. |
| `finite_toy_metric_response` | `frozen_negative` | `tag_removal_obstruction` | `local_toy_route_frozen_not_global_theory_rejection` | `frozen_negative_no_promotion` | The explicit-tag finite toy metric-response route is frozen as a local negative route. | No `g_eff` scope expansion, matter coupling, Einstein equations, benchmark promotion, completed derivation, global theory rejection, or future source-extension impossibility follows from this frozen-negative toy route. | `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex` | Governed by the Distance-to-GR ledger and cited Refuter stress artifact. | The local toy route is frozen; that is not a global rejection of the program. |

## Rendering Rules

Public surfaces that render this table must:

1. Keep the four status layers visible for high-risk rows.
2. Avoid unqualified acceptance wording for `M_src`, `g_eff`,
   `matter_coupling`, or object rows unless the row immediately states the
   scope and blocked overread.
3. Preserve exact blocked-overread language for `matter_coupling`,
   `SourceMatterSemanticsAdoptionReadinessLaw_v1`, `PositiveMSProfile_v1`, and
   `RR_ETransportCompletenessOrInvarianceLaw_v1`.
4. State explicitly that GR is not derived.
5. State explicitly that matter coupling, stress-energy semantics, matter
   action, Einstein equations, benchmark promotion, and completed derivation
   remain blocked.
6. Link to or cite this source spec plus the row-specific evidence path.
7. Treat this table as a public documentation contract, not as an authority to
   edit the ledger, ontology, theorem inventory, or Gate Chair verdicts.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *Distance-to-GR ledger*
[Internal control registry].

The AEther-Flow Research Project. (2026, July 1). *Scoped positive claim
vocabulary* [Internal control note].

The AEther-Flow Research Project. (2026, July 1). *Distance-to-GR status
aliases* [Internal control data].

The AEther-Flow Research Project. (2026, July 2). *Current research frontier*
[Internal control snapshot].

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v14* [Internal implementation plan].
