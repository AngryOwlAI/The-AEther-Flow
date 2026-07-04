<!-- authority: control -->

# Public Status Exists / Does-Not-Exist Source Spec

## Scope

This source spec defines the simplified public status table required by v15
P14-T01. It is a project-control documentation source for future public-facing
surfaces. It is not a physics proof, not a generated derivative, not a
Gate Chair verdict, and not authority to promote any scientific claim.

The table answers two public questions:

1. What exists in the tracked project record?
2. What does not exist or must not be inferred from that record?

## Authority Order

If a public rendering conflicts with one of these sources, the tracked source
governs in this order:

1. `registries/DISTANCE_TO_GR_LEDGER.csv` for Distance-to-GR burden status.
2. `research_control/design/scoped_positive_claim_vocabulary.md` for safe
   high-risk claim wording.
3. `research_control/design/distance_to_gr_status_aliases.yaml` for
   reader-facing aliases and object-specific blocked-overread language.
4. Row-specific Gate Chair, task, or control artifacts listed in the table.
5. `research_control/design/public_status_table_source_spec.md` as the older
   v14 layered public-status table contract.
6. This source spec as the simplified exists / does-not-exist public table
   contract.

Generated wiki notes, HTML, PDFs, Obsidian notes, semantic extracts, `.local`
caches, validator output, commits, and role records are not independent
scientific authority.

## Required Public Table

Every public table derived from this source must preserve these rows and the
same meaning, although headings may be adapted for layout.

| Object or target | What exists | What does not exist | Source basis | Public-safe wording rule |
| --- | --- | --- | --- | --- |
| AEther-flow ontology | proposed research ontology / explanatory frame | established physical ontology | `AGENTS.md`; `registries/DISTANCE_TO_GR_LEDGER.csv` row `source_ontology_primitives`; `research_control/design/distance_to_gr_status_aliases.yaml` row alias `source_ontology_primitives` | Say the ontology is a proposed research frame with controlled draft primitives. Do not say it is an established physical ontology or completed foundation for deriving GR. |
| `M_src` | scoped source-only object | target manifold, metric, GR derivation | `registries/DISTANCE_TO_GR_LEDGER.csv` row `m_src`; `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex`; `research_control/design/scoped_positive_claim_vocabulary.md` object-specific vocabulary | Say `M_src` exists only as a scoped source-side object under its tracked review. Do not present it as a target manifold, metric, or GR derivation. |
| `g_eff` | scoped source-extension object | unscoped Lorentzian metric, matter coupling, Einstein equations | `registries/DISTANCE_TO_GR_LEDGER.csv` row `g_eff`; `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex`; `research_control/design/scoped_positive_claim_vocabulary.md` object-specific vocabulary | Say `g_eff` exists only inside its declared source-extension scope. Do not present it as an unscoped Lorentzian metric, matter-coupling result, or Einstein-equation premise. |
| Matter-sector evidence | scoped evidence/preconditions | matter semantics, detector semantics, coupling law, matter coupling | `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`; `research_control/design/scoped_positive_claim_vocabulary.md`; `research_control/design/distance_to_gr_status_aliases.yaml` row alias `matter_coupling`; `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` | Say current matter-sector material is scoped evidence/precondition support. Do not say matter semantics, detector semantics, a coupling law, or matter coupling has been adopted or derived. |
| `RR_E` transport/invariance evidence | certificate-indexed scoped evidence/precondition | source-law adoption, unrestricted theorem | `research_control/design/scoped_positive_claim_vocabulary.md`; `research_control/design/distance_to_gr_status_aliases.yaml` object alias `RR_ETransportCompletenessOrInvarianceLaw_v1`; `research_control/tasks/RT-20260701-030/artifacts/rr_e_transport_law_gate_chair_review_v1.tex`; `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling` | Say `RR_E` transport/invariance material is certificate-indexed scoped evidence/precondition only. Do not say it is source-law adoption, object adoption, an unrestricted `RR_E` theorem, detector semantics, or matter coupling. |
| Einstein equations | not started | field-equation derivation | `registries/DISTANCE_TO_GR_LEDGER.csv` row `einstein_equations`; `research_control/design/einstein_equation_route_moratorium_v1.md`; `research_control/program_state.yaml` | Say Einstein equations are not derived and direct EFE routing is blocked until prerequisites are established or lawfully routed. Do not describe scoped evidence/preconditions as a field-equation derivation. |
| Benchmark promotion | blocked | exact-GR derivation or closure | `registries/DISTANCE_TO_GR_LEDGER.csv` row `benchmark_promotion`; `research_control/design/distance_to_gr_status_aliases.yaml` row alias `benchmark_promotion`; `research_control/design/public_status_table_source_spec.md` | Say exact-GR benchmark promotion remains blocked by upstream derivation burdens and protected authority. Do not claim benchmark closure, benchmark fit, exact-GR derivation, or completed derivation. |
| Completed derivation | no | no completed derivation | `registries/DISTANCE_TO_GR_LEDGER.csv` rows `einstein_equations`, `benchmark_promotion`, and `gate_chair_status`; `research_control/current_frontier.md`; `implementations_plans/recommendations_implementation_plan_continue_task-v15.md` P14-T01 | Say the project has no completed GR derivation. Do not imply completion from scoped objects, scoped evidence/preconditions, validators, generated derivatives, or commits. |

## Rendering Rules

Public renderings of this table must:

1. Keep the exists and does-not-exist columns visible.
2. State that GR has not been derived.
3. State that AEther-flow is a proposed research ontology or explanatory
   frame, not an established physical ontology.
4. Preserve scoped wording for `M_src`, `g_eff`, matter-sector evidence, and
   `RR_E` transport/invariance evidence.
5. Preserve blocked wording for matter semantics, detector semantics, coupling
   law, matter coupling, stress-energy semantics, matter action, variation
   principle, Einstein equations, benchmark promotion, Gate Chair closure, and
   completed derivation.
6. Cite or link the source basis for each rendered row.
7. Treat this table as a public documentation contract, not as authority to
   edit the ledger, ontology, theorem inventory, Gate Chair artifacts, or
   canonical science sources.

## Relation To The v14 Public Status Spec

`research_control/design/public_status_table_source_spec.md` remains the
more detailed status-layer contract. This P14-T01 spec does not replace that
source. It provides a shorter public table for surfaces where the reader needs
the basic distinction between existing scoped project objects and non-existing
downstream physical or derivational claims.

## Deferred Public Updates

README, GitHub-facing pages, Markdown HTML-explainer source specs, publication
briefs, and generated HTML updates are deferred to P14-T03 if the
documentation-impact classifier or tracked handoff routes that work. This
packet creates the source spec only.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *Distance-to-GR ledger*
[Internal control registry]. `registries/DISTANCE_TO_GR_LEDGER.csv`

The AEther-Flow Research Project. (2026, July 1). *Scoped positive claim
vocabulary* [Internal control note].
`research_control/design/scoped_positive_claim_vocabulary.md`

The AEther-Flow Research Project. (2026, July 1). *Distance-to-GR status
aliases* [Internal control data].
`research_control/design/distance_to_gr_status_aliases.yaml`

The AEther-Flow Research Project. (2026, July 2). *Public status table source
spec* [Internal control note].
`research_control/design/public_status_table_source_spec.md`

The AEther-Flow Research Project. (2026, July 3). *Recommendations
implementation plan for `/continue-research`, v15* [Internal implementation
plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`
