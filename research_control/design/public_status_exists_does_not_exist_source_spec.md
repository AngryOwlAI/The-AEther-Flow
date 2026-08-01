<!-- authority: control -->

# Public Status Exists / Does-Not-Exist Source Spec

## Scope

This source spec defines the simplified public status table introduced by v15
P14-T01 and aligned by v21 P14-T06 with the completed P14-T02 through P14-T05
evidence chain. It is a project-control documentation source for public-facing
surfaces. It is not a physics proof, not a generated derivative, not a Gate
Chair verdict, and not authority to promote any scientific claim.

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
4. Row-specific protected decisions, Gate Chair artifacts, task completions,
   or control artifacts listed in the table, including the P14-T04 congruence
   decision.
5. `research_control/design/epistemic_category_glossary.md` for distinctions
   among ontology, exact closure, formal equivalence, genuine emergence,
   operational meaning, and empirical novelty.
6. `research_control/design/public_status_table_source_spec.md` as the older
   v14 layered public-status table contract.
7. This source spec as the simplified exists / does-not-exist public table
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
| Exact-GR operational closure | adopted target-side GR dynamics in the canonical exact-closure manuscript sequence | first-principles source derivation, benchmark promotion, or empirical novelty | `ontology/tex/aether_flow_foundations.tex`; `ontology/tex/aether_flow_geometry.tex`; `registries/DISTANCE_TO_GR_LEDGER.csv` rows `einstein_equations` and `benchmark_promotion`; `research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex` | Say the exact-closure theory adopts ordinary GR as its target-side operational law. State separately that Gate E found source recovery not ready, denied benchmark promotion, and forbids a completed-derivation claim. |
| Target-side congruence `u^mu` | admissible, generally non-unique interpretive representative inside the adopted GR benchmark | `Phi_src`, a source-selected congruence, an established pure-gauge result, an independent dynamical field, or a source-to-target bridge | `ontology/tex/aether_flow_geometry.tex`; `research_control/tasks/RT-20260731-005/artifacts/p14_t04_congruence_status_decision_v1.tex`; `research_control/tasks/RT-20260731-005/artifacts/p14_t04_downstream_requirement_update_v1.yaml` | Say `u^mu` supplies a target-side interpretive dictionary only. Representative independence applies to a fixed target solution, fixed base observables, and fixed protocols; congruence-explicit or observer-relative quantities can still differ. |
| `M_src` | scoped source-only object | target manifold, metric, GR derivation | `registries/DISTANCE_TO_GR_LEDGER.csv` row `m_src`; `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex`; `research_control/design/scoped_positive_claim_vocabulary.md` object-specific vocabulary | Say `M_src` exists only as a scoped source-side object under its tracked review. Do not present it as a target manifold, metric, or GR derivation. |
| `ScopedMetricStructureRecord_src` (`g_eff^{GSC-cand}` legacy alias) | exact ten-slot scoped source-extension record | unscoped Lorentzian metric, operational geometry, matter coupling, Einstein equations | `registries/DISTANCE_TO_GR_LEDGER.csv` row `g_eff`; `research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml`; `research_control/design/scoped_positive_claim_vocabulary.md` | Use the current record name and identify `g_eff^{GSC-cand}` only as its exact legacy alias. Do not shorten the scoped record to an unscoped physical metric or a lawful P7 geometry input. |
| Protected finite matter package | exact P7 package adopted as canonical physical matter by explicit protected human postulate within its declared finite domains and current source architecture | first-principles source derivation of those meanings, target-side stress-energy, `g_eff`, equivalence-principle recovery, Einstein equations, or benchmark promotion | `research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex`; `research_control/tasks/RT-20260729-001/artifacts/p7_t08_constitutive_postulate_ledger_v1.yaml`; `research_control/program_state.yaml` block `p7_t08_physical_matter_adoption` | State the positive protected postulate-level adoption first and its exact finite scope. State separately that the current ontology does not derive the adopted meanings and that the cross-layer composition gap remains open. |
| Matter-sector derivational evidence | parameterized finite/local witness preconditions supporting the protected package and later work | source-derived physical matter, target-side gravity, or a completed matter-coupling derivation | `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`; `research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex`; `research_control/tasks/RT-20260728-006/artifacts/matter_package_smuggling_audit_v1.tex` | Keep evidence/precondition status distinct from the separate protected postulate. Neither the evidence nor the postulate supplies a first-principles source derivation or downstream gravitational closure. |
| `RR_E` transport/invariance evidence | certificate-indexed scoped evidence/precondition | source-law adoption, unrestricted theorem | `research_control/design/scoped_positive_claim_vocabulary.md`; `research_control/design/distance_to_gr_status_aliases.yaml` object alias `RR_ETransportCompletenessOrInvarianceLaw_v1`; `research_control/tasks/RT-20260701-030/artifacts/rr_e_transport_law_gate_chair_review_v1.tex`; `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling` | Say `RR_E` transport/invariance material is certificate-indexed scoped evidence/precondition only. Do not say it is source-law adoption, object adoption, an unrestricted `RR_E` theorem, detector semantics, or matter coupling. |
| Einstein equations | draft/control Einstein-sector artifacts and a protected Gate D `NOT_READY` decision | source-derived physical field equations | `registries/DISTANCE_TO_GR_LEDGER.csv` row `einstein_equations`; `research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex`; `research_control/program_state.yaml` | Say the protected review found the Einstein-sector derivation requirements unmet. Do not turn finite controls, adopted matter postulates, or target-side exact closure into a source-derived field-equation result. |
| Benchmark promotion | a protected Gate E `NOT_READY` decision with six inconclusive cases and zero passes | exact or controlled-approximate GR recovery, benchmark promotion, independent replication, or completed derivation | `registries/DISTANCE_TO_GR_LEDGER.csv` row `benchmark_promotion`; `research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex`; `research_control/program_state.yaml` | Say benchmark promotion was denied as not ready. Do not turn the target-side exact-GR operational closure, a protected review, or documentation into source recovery or benchmark closure. |
| Completed derivation | an explicit protected decision that it may not be claimed | completed first-principles derivation | `registries/DISTANCE_TO_GR_LEDGER.csv` rows `einstein_equations`, `benchmark_promotion`, and `gate_chair_status`; `research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex`; `research_control/current_frontier.md` | Say the project has no completed GR derivation. Do not imply completion from adopted target-side closure, protected postulates, scoped objects, evidence, validators, generated derivatives, or commits. |

## Required Success-Label Separation

Public explanations must keep these six labels visibly distinct:

| Label | Minimum public meaning | Does not establish |
| --- | --- | --- |
| Ontology | What the proposed source interpretation says reality may be about. | Exact target dynamics, source derivation, or empirical truth. |
| Exact closure | Ordinary GR is adopted as the target-side operational law of the exact-closure theory. | First-principles recovery from source variables or benchmark promotion. |
| Formal equivalence | A declared mathematical relation, isomorphism, quotient, or target-side redescription under stated assumptions. | Positive source provenance, physical interpretation, or genuine emergence. |
| Genuine emergence | A source-to-target result supported by provenance, dynamics, uniqueness or quotient status, operational meaning, and robustness. | It is not supplied merely by no-target purity, exact closure, or an interpretive representative. |
| Operational meaning | A tracked link to observers, detectors, protocols, calibration, or physical semantics within exact scope. | Source derivation, representative uniqueness, or empirical novelty. |
| Empirical novelty | A source-backed observable difference or independent prediction with an authorized comparison protocol. | It is not implied by interpretation, formal equivalence, exact closure, or current public documentation. |

## Rendering Rules

Public renderings of this table must:

1. Keep the exists and does-not-exist columns visible.
2. State that GR has not been derived.
3. State that AEther-flow is a proposed research ontology or explanatory
   frame, not an established physical ontology.
4. Preserve scoped wording for `M_src`, the current
   `ScopedMetricStructureRecord_src`, matter-sector evidence, and `RR_E`
   transport/invariance evidence.
5. State the exact P7 protected matter adoption positively while separating
   postulate-level adoption from source derivation and downstream gravity.
6. State the target-side congruence status and the observer-relative exception
   to fixed-protocol representative independence.
7. Preserve blocked wording for source-derived matter coupling, target-side
   stress-energy, Einstein equations, benchmark promotion, Gate Chair closure,
   empirical novelty, and completed derivation.
8. Cite or link the source basis for each rendered row.
9. Treat this table as a public documentation contract, not as authority to
   edit the ledger, ontology, theorem inventory, Gate Chair artifacts, or
   canonical science sources.

## Relation To The v14 Public Status Spec

`research_control/design/public_status_table_source_spec.md` remains the
more detailed status-layer contract. This P14-T01 spec does not replace that
source. It provides a shorter public table for surfaces where the reader needs
the basic distinction between existing scoped project objects and non-existing
downstream physical or derivational claims.

## P14-T06 Propagation Boundary

P14-T06 propagates this contract only to its bounded README and paired
publication surfaces. That synchronization remains project-system work. It
does not revise the ledger, the P14-T04 decision, canonical ontology, physics
TeX, a protected Gate verdict, or any scientific claim status.

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

The AEther-Flow Research Project. (2026, July 20). *Recommendations
implementation plan for `/continue-research`, v21* [Internal implementation
plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v21.md`

The AEther-Flow Research Project. (2026, July 22). *Non-empirical ontology
success criteria* [Draft/control scientific artifact].
`research_control/tasks/RT-20260722-018/artifacts/non_empirical_ontology_success_criteria_v1.tex`

The AEther-Flow Research Project. (2026, July 22). *No-target positive
provenance sufficiency policy* [Draft/control scientific artifact].
`research_control/tasks/RT-20260722-019/artifacts/no_target_positive_provenance_sufficiency_policy_v1.tex`

The AEther-Flow Research Project. (2026, July 31). *Protected congruence status
decision* [Protected task-local scientific gate artifact].
`research_control/tasks/RT-20260731-005/artifacts/p14_t04_congruence_status_decision_v1.tex`

The AEther-Flow Research Project. (2026, July 22). *Negative-result success
pathway* [Draft/control scientific artifact].
`research_control/tasks/RT-20260722-020/artifacts/negative_result_success_pathway_v1.tex`
