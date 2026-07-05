<!-- authority: control -->

# Current Research Frontier

This control snapshot records the active research-control frontier after
`RT-20260705-032` and `handoff-0605`.
It is generated from tracked control state. It is a synchronized reader-facing
snapshot, not independent routing authority and not a physics proof surface.
If this file ever contradicts `research_control/program_state.yaml`, the
handoff named by that file, or `registries/DISTANCE_TO_GR_LEDGER.csv`, those
tracked authority files govern.

## Active Research State

| Field | Value |
| --- | --- |
| Active task ID | `RT-20260705-032` |
| Latest handoff ID | `handoff-0605` |
| Current status | `v16_p14_t03_target_import_validator_integration_completed_no_physics_delta` |
| Current route family | target_import_attack_validator_integration_v16 |
| Target derivation milestone | `matter_coupling` |
| Current burden | none for physics derivation; live control burden is compact current frontier schema v16 |
| Required next authority | P15-T01 compact frontier schema only |
| Next recommended action | Run one bounded P15-T01 compact current-frontier schema packet. |

## Active Boundary

`current_frontier.md` is a generated snapshot under the P1 active-state
authority invariant. The precedence order remains:

1. `research_control/program_state.yaml` is the compact live state pointer.
2. The latest handoff named by `program_state.yaml` is immediate routing
   authority.
3. `registries/DISTANCE_TO_GR_LEDGER.csv` is the persistent burden-state
   ledger.
4. Task records, DDRs, AgentJobs, completions, claim-boundary rows, and
   role-execution rows provide transaction provenance.
5. This file is a generated synchronized snapshot only.

The P1-T04 renderer check fails when this snapshot drifts from tracked
active-state authority. The renderer provides a deterministic repair command:

```zsh
.venv/bin/python scripts/research_control/render_current_frontier.py --write
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_current_frontier.py --json
```

## Current Route Evidence

- Active task path: `research_control/tasks/RT-20260705-032/00_TASK.yaml`.
- Active task objective: Integrate P14-T02 target-import attack fixtures into fail-closed claim-language validation.
- Latest handoff path: `research_control/handoffs/handoff-0605.yaml`.
- Latest handoff summary: RT-20260705-032 completed v16 P14-T03 by integrating target-import attack fixtures into claim-language validation.
- Current route family: target_import_attack_validator_integration_v16.
- Next recommended action: Run one bounded P15-T01 compact current-frontier schema packet.

## Three-Tier Claim Summary Pilot

This pilot separates source-side object status from evidence/precondition status and from still-open physical targets. Evidence/precondition entries are intentionally not rendered as adopted objects unless tracked source authority independently records adoption.

Adopted source-only or source-extension objects:

| Object | Status | Authority | Scope qualifier | Blocked overread | Downstream promotion authorized |
| --- | --- | --- | --- | --- | --- |
| M_src | adopted only as scoped source-only M_src object | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` | not_target_manifold_not_metric_not_gr_derivation | no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | false |
| g_eff | adopted only as scoped source-extension g_eff object | `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex` | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | no_source_law_adoption<br>no_metricdata_e_adoption<br>no_unscoped_geff_adoption<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | false |

Scoped accepted evidence/preconditions:

| Evidence or precondition | Status | Supports target | Does not establish | Authority |
| --- | --- | --- | --- | --- |
| matter_coupling burden evidence/preconditions | accepted only as scoped source-extension evidence/precondition | matter-semantics and matter-coupling continuation only | no_source_law_adoption<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` |

Open or blocked physical targets:

| Physical target | Status | Missing burden or authority | Evidence not to overread | Next lawful route or evidence |
| --- | --- | --- | --- | --- |
| matter_coupling | accepted_as_scoped_evidence_precondition | PositiveMSProfile_v1 RR_ETransportCompletenessOrInvarianceLaw_v1 NarrowMSCertEq_v1 SourceCertificateAlgebraPrimitives_v1 and SourceCertificateOperationLaws_v1 are accepted or drafted only as scoped source-extension evidence/preconditions evidence-status draft/control certificate primitives or draft/control operation-law support under declared source-side and fail-closed scope while no source-law adoption no RR_ETransportCompletenessOrInvarianceLaw_v1 adoption no PositiveMSProfile_v1 adoption no SourceMatterSemanticsAdoptionReadinessLaw_v1 law adoption no source-extension data adoption beyond exact scoped gate result no matter-semantics adoption no detector-semantics adoption no coupling-law adoption no matter-coupling derivation no stress-energy semantics no matter action no MetricData(E) adoption no g_eff scope expansion no Einstein-equation premise no benchmark fit and no downstream promotion occurred | no_source_law_adoption<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex |
| einstein_equations | not_started | dynamics action or variation | no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | research_control/program_state.yaml |
| benchmark_promotion | blocked | all upstream derivation burdens | no_benchmark_promotion<br>no_benchmark_gate_chair_closure<br>no_completed_derivation | research_control/program_state.yaml |

Forbidden overreads:

- three-tier summary as physics proof
- accepted evidence/preconditions as adopted objects
- current-frontier rendering as downstream promotion

## Matter-Coupling Boundary

The Distance-to-GR ledger currently records the `matter_coupling` burden row with legacy status `accepted`, control status `accepted_as_scoped_evidence_precondition`, mathematical status `parameterized_finite_local_witness_precondition`, physical status `not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics`, and promotion status `scoped_source_evidence_only`. Its blocking burden is: PositiveMSProfile_v1 RR_ETransportCompletenessOrInvarianceLaw_v1 NarrowMSCertEq_v1 SourceCertificateAlgebraPrimitives_v1 and SourceCertificateOperationLaws_v1 are accepted or drafted only as scoped source-extension evidence/preconditions evidence-status draft/control certificate primitives or draft/control operation-law support under declared source-side and fail-closed scope while no source-law adoption no RR_ETransportCompletenessOrInvarianceLaw_v1 adoption no PositiveMSProfile_v1 adoption no SourceMatterSemanticsAdoptionReadinessLaw_v1 law adoption no source-extension data adoption beyond exact scoped gate result no matter-semantics adoption no detector-semantics adoption no coupling-law adoption no matter-coupling derivation no stress-energy semantics no matter action no MetricData(E) adoption no g_eff scope expansion no Einstein-equation premise no benchmark fit and no downstream promotion occurred. The last evidence path is `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`.

This ledger status must not be read as coupling-law adoption, universal matter-coupling derivation, matter-coupling adoption, stress-energy semantics, stress-energy tensor, matter action, detector semantics, Einstein equations, benchmark promotion, or completed derivation.

Universal matter coupling and downstream GR promotion remain blocked until a
separate tracked route and the required protected authorities establish them.

## Layered Distance-To-GR Boundary Notes

The legacy `current_status` column is retained for continuity. The layered
columns below are the reader-facing anti-overread boundary:

- `control_status` records workflow or gate-review state.
- `mathematical_status` records the source-side mathematical object state.
- `physical_status` records what must not be inferred physically.
- `promotion_status` records whether any downstream promotion is authorized.
- `overread_guard` records exact blocked readings that must remain visible.

High-risk rows:

- `m_src`: reader-facing `adopted only as scoped source-only M_src object`; control `gate_review_completed`; mathematical `scoped_source_only_adopted_object`; physical `not_target_manifold_not_metric_not_gr_derivation`; promotion `scoped_source_object_only`; guards: no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation.
- `g_eff`: reader-facing `adopted only as scoped source-extension g_eff object`; control `gate_review_completed`; mathematical `scoped_source_extension_geff_object`; physical `not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations`; promotion `scoped_source_object_only`; guards: no_source_law_adoption<br>no_metricdata_e_adoption<br>no_unscoped_geff_adoption<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation.
- `matter_coupling`: reader-facing `accepted only as scoped source-extension evidence/precondition`; control `accepted_as_scoped_evidence_precondition`; mathematical `parameterized_finite_local_witness_precondition`; physical `not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics`; promotion `scoped_source_evidence_only`; guards: no_source_law_adoption<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection.
- `einstein_equations`: reader-facing `not started; no positive derivation status`; control `not_started`; mathematical `dynamics_action_or_variation_missing`; physical `no_field_equation_derivation`; promotion `none`; guards: no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation.
- `benchmark_promotion`: reader-facing `no benchmark promotion from scoped evidence/precondition alone`; control `blocked`; mathematical `upstream_burdens_missing`; physical `no_exact_gr_benchmark_promotion`; promotion `none`; guards: no_benchmark_promotion<br>no_benchmark_gate_chair_closure<br>no_completed_derivation.

## Exact Blocked Claims

- [ ] canonical ontology edit
- [ ] source-law adoption
- [ ] `MetricData(E)` adoption
- [ ] `g_eff` adoption or scope expansion
- [ ] coupling-law adoption
- [ ] matter-coupling derivation
- [ ] matter-coupling adoption
- [ ] stress-energy semantics
- [ ] stress-energy tensor
- [ ] matter action
- [ ] detector semantics
- [ ] Einstein equations
- [ ] exact-GR benchmark promotion
- [ ] benchmark closure without protected authority
- [ ] completed derivation
- [ ] future source-extension impossibility
- [ ] program-wide no-go conclusion
- [ ] this snapshot as independent authority
- [ ] generated graph, checker, registry, validator, local cache, role, handoff, approval, or commit status as scientific proof

## Scoped-Positive Alias Pilot

The renderer consumes the subordinate status alias map at `research_control/design/distance_to_gr_status_aliases.yaml` for reader-facing wording only. The ledger continues to govern if an alias and ledger row ever conflict. Aliases are not physics proof, routing authority, benchmark authority, or claim-promotion authority.

- High-risk rows must not render bare `accepted`: true.
- Aliases override the ledger: false.
- Aliases are physics proof: false.

High-risk burden aliases:

| Object | Reader-facing status | Required qualifier | Required blocked phrase |
| --- | --- | --- | --- |
| `m_src` | adopted only as scoped source-only M_src object | M_src is not a target manifold, not a metric, and not a GR derivation. | No MetricData(E), g_eff scope expansion, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows from this row. |
| `g_eff` | adopted only as scoped source-extension g_eff object | The object is not an unscoped Lorentzian metric and does not supply matter coupling or Einstein equations. | No MetricData(E), unscoped g_eff, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows from this row. |
| `matter_coupling` | accepted only as scoped source-extension evidence/precondition | PositiveMSProfile_v1 and RR_ETransportCompletenessOrInvarianceLaw_v1 are scoped evidence/preconditions only; matter coupling remains not derived and not adopted. | No source-law adoption, RR_ETransportCompletenessOrInvarianceLaw_v1 adoption, PositiveMSProfile_v1 adoption, SourceMatterSemanticsAdoptionReadinessLaw_v1 law adoption, matter semantics, detector semantics, coupling law, matter coupling, stress-energy, matter action, MetricData(E), g_eff scope expansion, Einstein equations, benchmark promotion, or completed derivation follows from this row. |
| `einstein_equations` | not started; no positive derivation status | No Einstein-equation premise, derivation, benchmark closure, or completed derivation has been established. | Einstein equations remain blocked by missing dynamics, action, variation, matter coupling, and protected benchmark authority. |
| `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | Exact-GR benchmark promotion remains blocked by upstream derivation burdens and protected authority. | No benchmark promotion, closure, fit claim, or completed exact-GR derivation claim follows from scoped evidence/preconditions. |
| `finite_toy_metric_response` | frozen negative local toy route only | Tag-removal stress freezes this local toy route; it is not global theory rejection. | No g_eff scope expansion, matter coupling, Einstein equations, benchmark promotion, completed derivation, future source-extension impossibility, or global theory rejection follows from this frozen-negative toy route. |

`matter_coupling` object aliases:

| Object | Reader-facing status | Required qualifier |
| --- | --- | --- |
| `MSStableMatterSemanticsBridge_v1` | draft/control bridge target only | Not adopted matter semantics and not detector semantics. |
| `SourceMatterSemanticsAdoptionReadinessLaw_v1` | proposal-only law target unless a later gate changes status | Not law adoption, not matter semantics, not detector semantics, and not coupling law. |
| `PositiveMSProfile_v1` | accepted only as scoped positive source-semantics evidence/precondition | Not adopted matter semantics, detector semantics, stress-energy, or matter action. |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` | accepted only as certificate-indexed RR_E transport-completeness or invariance evidence/precondition | Not source-law adoption, not object adoption, not unrestricted RR_E theorem, not detector semantics, and not matter coupling. |
| `RR_E_underdetermination_obstruction` | scoped obstruction under current ontology only | Not global impossibility and not global theory rejection. |

## Distance-To-GR Table

This table summarizes the layered fields in
`registries/DISTANCE_TO_GR_LEDGER.csv`; the ledger remains the authoritative
source if this summary drifts. The `Reader-facing status` column is rendered
from `research_control/design/distance_to_gr_status_aliases.yaml` when a row alias exists. The `Legacy status` column
preserves the raw ledger `current_status` field for continuity.

| Burden ID | Milestone | Reader-facing status | Legacy status | Control status | Mathematical status | Physical status | Promotion status | Overread guard | Last evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `source_ontology_primitives` | `source_ontology` | draft source-ontology primitives only | draft object exists | draft_control_object_exists | definition_only_or_draft_object | no_canonical_ontology_adoption | draft_control_only | no_canonical_ontology_edit<br>no_benchmark_promotion<br>no_completed_derivation | `AGENTS.md` |
| `source_equivalence_eqsrc` | `source_equivalence_eqsrc` | draft source-equivalence object only | draft object exists | draft_control_object_exists | general_equivalence_theorem_missing | downstream_gr_blocked | draft_control_only | no_source_law_adoption<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |
| `retain_h` | `source_equivalence_eqsrc` | blocked by missing primitive | blocked by missing primitive | blocked | primitive_missing | no_retention_law_adoption | none | no_source_law_adoption<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |
| `gen_h` | `source_equivalence_eqsrc` | blocked by missing primitive | blocked by missing primitive | blocked | primitive_missing | no_generator_law_adoption | none | no_source_law_adoption<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |
| `obsloc_lc` | `source_localization_obsloc_lc` | constructive local exact-branch witness only | constructive witness exists | constructive_witness_recorded | constructive_witness | local_exact_branch_only | draft_control_only | no_source_law_adoption<br>no_matter_coupling_derivation<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-037/artifacts/58_LOCALIZATION_SOURCE_BASIS_AXIOM_SELECTOR_DOMAIN_EQSRC_ALTERNATIVE_BRANCH_FAMILY_GUARD_STABILITY_SOURCE_PACKET_SMUGGLING_AUDIT.tex` |
| `resp_lc` | `response_localization_resp_lc` | accepted only as scoped source-extension selector data | accepted | accepted_as_source_extension_data | selector_data_source_extension | not_detector_semantics_not_matter_coupling | scoped_source_object_only | no_canonical_ontology_edit<br>no_matter_coupling_derivation<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-060/artifacts/101_RESP_LC_SOURCE_EXTENSION_HUMAN_GATE_ADOPTION_DECISION.tex` |
| `m_src` | `source_manifold_m_src` | adopted only as scoped source-only M_src object | accepted | gate_review_completed | scoped_source_only_adopted_object | not_target_manifold_not_metric_not_gr_derivation | scoped_source_object_only | no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` |
| `g_eff` | `effective_metric_g_eff` | adopted only as scoped source-extension g_eff object | accepted | gate_review_completed | scoped_source_extension_geff_object | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | scoped_source_object_only | no_source_law_adoption<br>no_metricdata_e_adoption<br>no_unscoped_geff_adoption<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex` |
| `matter_coupling` | `matter_coupling` | accepted only as scoped source-extension evidence/precondition | accepted | accepted_as_scoped_evidence_precondition | parameterized_finite_local_witness_precondition | not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics | scoped_source_evidence_only | no_source_law_adoption<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` |
| `einstein_equations` | `einstein_equations` | not started; no positive derivation status | not started | not_started | dynamics_action_or_variation_missing | no_field_equation_derivation | none | no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |
| `finite_variation_robustness` | `source_equivalence_eqsrc` | Refuter stress passed | Refuter stress passed | refuter_stress_passed | conditional_theorem_candidate | downstream_gr_blocked | draft_control_only | no_source_law_adoption<br>no_matter_coupling_derivation<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-101/artifacts/142_RESP_LC_M_SRC_GSC_FINITE_VARIATION_ROBUSTNESS_LAW_REFUTER_STRESS_TEST.tex` |
| `benchmark_promotion` | `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | blocked by missing primitive | blocked | upstream_burdens_missing | no_exact_gr_benchmark_promotion | none | no_benchmark_promotion<br>no_benchmark_gate_chair_closure<br>no_completed_derivation | `research_control/program_state.yaml` |
| `gate_chair_status` | `benchmark_promotion` | human-gated verdict authority only | human-gated | human_gated | protected_verdict_missing | no_benchmark_closure | human_gate_required | no_benchmark_gate_chair_closure<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/approvals/README.md` |
| `finite_toy_metric_response` | `finite_toy_metric_response` | frozen negative local toy route only | frozen negative | frozen_negative | tag_removal_obstruction | local_toy_route_frozen_not_global_theory_rejection | frozen_negative_no_promotion | no_geff_scope_expansion<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility | `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex` |

## Exact Next Route

The immediate next route is:

```text
Run one bounded P15-T01 compact current-frontier schema packet.
```

The next route must be executed through tracked continue-research state. This
snapshot does not create physics authority, Gate Chair authority, benchmark
authority, or completed-derivation authority.

## Validation And Authorization Layers

Validation receipts and protected authorization are separate. A layer-level
`PENDING` value must carry evidence explaining what remains pending; it does
not override a separate aggregate compatibility field unless the tracked
completion or handoff says so.

Layer status summary:

No validation-layer status summary is available.

Validation layers:

No validation-layer split is recorded in the latest handoff.

Authorization layers:

No authorization-layer split is recorded in the latest handoff.

Legacy compatibility records:

- active task: `RT-20260705-032`;
- latest handoff: `handoff-0605`;
- current status: `v16_p14_t03_target_import_validator_integration_completed_no_physics_delta`;
- renderer source: `scripts/research_control/render_current_frontier.py`;
- renderer policy: tracked-state snapshot only, not authority;
- claim boundary: no ontology edit, no source-law adoption, no `MetricData(E)` adoption, no `g_eff` scope expansion, no coupling-law adoption, no matter-coupling derivation or adoption, no stress-energy semantics, no Einstein equations, no benchmark promotion, no completed derivation, and no downstream GR promotion.

## Retrieval Warning Status

This renderer reads only tracked control sources:

- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0605.yaml`
- `research_control/tasks/RT-20260705-032/00_TASK.yaml`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `research_control/design/distance_to_gr_status_aliases.yaml` when present

Memory, wiki notes, semantic extracts, Obsidian notes, PDFs, generated HTML,
SQLite indexes, and `.local/` caches remain retrieval or reader layers only.
They are not scientific authority and are not inputs to this rendered state.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *GR derivation burden map*
[Internal control note].

The AEther-Flow Research Project. (2026, July 1). *Current research frontier*
[Generated internal control snapshot].

The AEther-Flow Research Project. (2026, July 1). *Handoff 0605*
[Internal research-control handoff].

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v14* [Internal implementation plan].
