<!-- authority: control -->

# Current Research Frontier

This control snapshot records the active research-control frontier after
`RT-20260801-007` and `handoff-0936`.
It is generated from tracked control state. It is a synchronized reader-facing
snapshot, not independent routing authority and not a physics proof surface.
If this file ever contradicts `research_control/program_state.yaml`, the
handoff named by that file, or `registries/DISTANCE_TO_GR_LEDGER.csv`, those
tracked authority files govern.

## Active Research State

| Field | Value |
| --- | --- |
| Active task ID | `RT-20260801-007` |
| Latest handoff ID | `handoff-0936` |
| Current status | `p13_t02_planner_authoritative_cutover_completed_checkpoint_ready` |
| V16 completed | false |
| Current route family | construction or implementation (project system) |
| Target derivation milestone | `source_equivalence_eqsrc` |
| Current burden | `source_equivalence_eqsrc` |
| Required next authority | One governed checkpoint for AJ-RT-20260801-007-001. After that commit, one fresh bounded P13-T07 project-system packet may enforce generated-report provenance and freshness. |
| Next recommended action | Run the one governed checkpoint for AJ-RT-20260801-007-001. After it commits, route one fresh bounded P13-T07 improve-project-system packet to enforce generated-report source provenance and freshness; do not execute P13-T07 in this frame. |

## Active-State Bifurcation

These fields separate ordinary research-continuation authority from any
project-system sidecar status. A sidecar may be evidence for project-system
repair, but it does not supersede the latest research handoff unless a later
tracked validator and handoff explicitly authorize that change.

| Field | Value |
| --- | --- |
| Latest research task ID | `RT-20260801-007` |
| Latest research handoff ID | `handoff-0936` |
| Latest research next action | Run the one governed checkpoint for AJ-RT-20260801-007-001. After it commits, route one fresh bounded P13-T07 improve-project-system packet to enforce generated-report source provenance and freshness; do not execute P13-T07 in this frame. |
| Latest project-system task ID | `none` |
| Latest project-system status | `none` |
| Latest project-system sidecar task ID | `none` |
| Latest project-system sidecar status | `none` |
| Sidecar supersedes research handoff | false |
| Next research route source | `latest_research_handoff` |

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

- Active task path: `research_control/tasks/RT-20260801-007/00_TASK.yaml`.
- Active task objective: Make the validated manifest planner the single orchestration owner for Make, hosted CI, skills, and governed checkpoint acceptance while preserving every hard gate, exact AgentJob allowlists, final staged-tree integrity, scheduled unfiltered full validation, and an explicit tested legacy fallback.
- Latest handoff path: `research_control/handoffs/handoff-0936.yaml`.
- Latest handoff summary: Generation 205 completed the guarded P13-T02 cutover. The manifest planner is the live operational owner for shared local profiles, hosted validation workflows, and governed checkpoint acceptance. All 28 full-profile gates pass; exact mutation allowlists, final staged-tree checks, scheduled unfiltered full orchestration, complete receipts, and explicit legacy rollback remain.
- Current route family: construction or implementation (project system).
- Next recommended action: Run the one governed checkpoint for AJ-RT-20260801-007-001. After it commits, route one fresh bounded P13-T07 improve-project-system packet to enforce generated-report source provenance and freshness; do not execute P13-T07 in this frame.

## Three-Tier Claim Summary Pilot

This pilot separates source-side object status from evidence/precondition status and from still-open physical targets. Evidence/precondition entries are intentionally not rendered as adopted objects unless tracked source authority independently records adoption.

Adopted source-only or source-extension objects:

| Object | Status | Authority | Scope qualifier | Blocked overread | Downstream promotion authorized |
| --- | --- | --- | --- | --- | --- |
| M_src | adopted only as scoped source-only M_src object | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` | not_target_manifold_not_metric_not_gr_derivation | no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | false |
| g_eff | ScopedMetricStructureRecord_src adopted as the scoped source-extension record; g_eff^{GSC-cand} retained as exact legacy alias | `research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml` | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | no_source_law_adoption<br>no_metricdata_e_adoption<br>no_unscoped_geff_adoption<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility | false |

Scoped accepted evidence/preconditions:

| Evidence or precondition | Status | Supports target | Does not establish | Authority |
| --- | --- | --- | --- | --- |
| matter_coupling burden evidence/preconditions | accepted only as scoped source-extension evidence/precondition | matter-semantics and matter-coupling continuation only | no_source_law_adoption<br>no_canonical_ontology_edit<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | `research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex` |

Open or blocked physical targets:

| Physical target | Status | Missing burden or authority | Evidence not to overread | Next lawful route or evidence |
| --- | --- | --- | --- | --- |
| matter_coupling | accepted_as_scoped_evidence_precondition | The exact protected verdict is ADOPTED_AS_CANONICAL_PHYSICAL_MATTER_BY_EXPLICIT_HUMAN_POSTULATE for the unchanged P7-T01 through P7-T06 package within its declared finite domains and the current continuum-first source architecture. This discharges the protected constitutive decision burden but does not supply a first-principles derivation: OBST-P7T07-CROSS-LAYER-COMPOSITION-GAP-001 remains open_derivational_gap_after_constitutive_adoption, current ontology still does not derive the adopted meanings, and P6 Gate B supplies no effective-geometry input. | no_source_law_adoption<br>no_canonical_ontology_edit<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex |
| einstein_equations | not_started | physical gravitational interpretation target field equations and Einstein-leading recovery | no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility | research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex |
| benchmark_promotion | blocked | all upstream derivation burdens | no_benchmark_promotion<br>no_benchmark_gate_chair_closure<br>no_completed_derivation<br>no_einstein_equations<br>no_matter_coupling_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex |

Forbidden overreads:

- three-tier summary as physics proof
- accepted evidence/preconditions as adopted objects
- current-frontier rendering as downstream promotion

## Matter-Coupling Boundary

The Distance-to-GR ledger currently records the `matter_coupling` burden row with legacy status `accepted`, control status `accepted_as_scoped_evidence_precondition`, mathematical status `parameterized_finite_local_witness_precondition`, physical status `not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics`, and promotion status `scoped_source_evidence_only`. Its blocking burden is: The exact protected verdict is ADOPTED_AS_CANONICAL_PHYSICAL_MATTER_BY_EXPLICIT_HUMAN_POSTULATE for the unchanged P7-T01 through P7-T06 package within its declared finite domains and the current continuum-first source architecture. This discharges the protected constitutive decision burden but does not supply a first-principles derivation: OBST-P7T07-CROSS-LAYER-COMPOSITION-GAP-001 remains open_derivational_gap_after_constitutive_adoption, current ontology still does not derive the adopted meanings, and P6 Gate B supplies no effective-geometry input.. The last evidence path is `research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex`.

This ledger status must not be read as coupling-law adoption, universal matter-coupling derivation, matter-coupling adoption, stress-energy semantics, stress-energy tensor, matter action, detector semantics, Einstein equations, benchmark promotion, or completed derivation.

Universal matter coupling and downstream GR promotion remain blocked until a
separate tracked route and the required protected authorities establish them.

## Metric-Use Ledger Warning

`registries/METRIC_USE_LEDGER.csv` is a project-control guard ledger for
metric-adjacent wording. It records allowed scope and blocked interpretations
only. It does not adopt `MetricData(E)`, expand `g_eff`, authorize a physical
metric, import matter dynamics, promote benchmark status, or prove any
downstream GR claim.

| Field | Value |
| --- | --- |
| Ledger path | `registries/METRIC_USE_LEDGER.csv` |
| Total rows | 25 |
| Forbidden/import guard rows | 25 |
| Blocked physical metric-use rows | 13 |
| Audited-clean rows | 11 |
| Blocked-by-scope rows | 14 |
| Use categories | `blocked_physical_metric_use`: 13; `finite_local_witness_context`: 7; `scoped_source_extension_context`: 4; `source_side_relation_input_candidate`: 1 |
| Audit statuses | `audited_clean`: 11; `blocked_by_scope`: 14 |

## Positive-First Status Cards

Every high-risk accepted or blocked row below is rendered with positive status
first, then exact scope, allowed use, and blocked overread. These cards are
reader-facing calibration only. They do not override the Distance-to-GR ledger
and do not create physics proof, Gate Chair authority, benchmark authority, or
completed-derivation authority.

### `m_src`

**Positive status:** M_src is adopted only as a scoped source-only M_src object.

**Scope:** The adoption applies only under the declared source-only GSC candidate scope and fail-closed boundary.

**Allowed use:** Later bounded packets may use it as source-side prerequisite context.

**Blocked overread:** No MetricData(E), g_eff scope expansion, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows from this row.

**Next burden:** Use scoped M_src only as source-side prerequisite context while deriving any later metric or coupling bridge without target-manifold or target-metric import.

### `g_eff`

**Positive status:** ScopedMetricStructureRecord_src is the primary name for the adopted scoped source-extension record; g_eff^{GSC-cand} is its exact legacy alias.

**Scope:** The adoption applies only to the exact declared source-extension candidate scope reviewed in RT-20260614-222.

**Allowed use:** Later bounded packets may use ScopedMetricStructureRecord_src as scoped source-extension context and may use g_eff^{GSC-cand} only as its explicit exact legacy alias.

**Blocked overread:** No MetricData(E), unscoped g_eff, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows from this row.

**Next burden:** Independently review the full Gate B package while using ScopedMetricStructureRecord_src as the scoped record and keeping bare g_eff unresolved.

### `matter_coupling`

**Positive status:** matter_coupling has accepted scoped evidence/precondition only for continuation.

**Scope:** The support is certificate-indexed, source-side, and finite/local only.

**Allowed use:** Later bounded packets may use it to construct, audit, or stress one source-side coupling-law candidate.

**Blocked overread:** No source-law adoption, RR_ETransportCompletenessOrInvarianceLaw_v1 adoption, PositiveMSProfile_v1 adoption, SourceMatterSemanticsAdoptionReadinessLaw_v1 law adoption, matter semantics, detector semantics, coupling law, matter coupling, stress-energy, matter action, MetricData(E), g_eff scope expansion, Einstein equations, benchmark promotion, or completed derivation follows from this row.

**Next burden:** Construct, audit, or stress one source-side coupling-law candidate from the scoped evidence/preconditions before any matter-coupling derivation or adoption claim.

### `einstein_equations`

**Positive status:** einstein_equations remains blocked with open continuation and no positive derivation status.

**Scope:** No Einstein-equation premise, derivation, benchmark closure, or completed derivation has been established.

**Allowed use:** Later bounded packets may use this row only as a visible downstream burden and claim-boundary guard.

**Blocked overread:** Einstein equations remain blocked by missing dynamics, action, variation, matter coupling, and protected benchmark authority.

**Next burden:** Derive lawful dynamics/action/variation and matter coupling under protected gates before any Einstein-equation derivation claim.

### `benchmark_promotion`

**Positive status:** benchmark_promotion remains blocked by upstream derivation burdens and protected authority.

**Scope:** No exact-GR benchmark promotion, benchmark closure, fit claim, Gate Chair verdict, or completed derivation follows from scoped evidence/preconditions.

**Allowed use:** Later bounded packets may use this row only as a protected downstream authority boundary.

**Blocked overread:** No benchmark promotion, closure, fit claim, or completed exact-GR derivation claim follows from scoped evidence/preconditions.

**Next burden:** Complete upstream derivation burdens and protected Gate Chair benchmark review before any benchmark promotion or completed-derivation claim.

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
- `g_eff`: reader-facing `ScopedMetricStructureRecord_src adopted as the scoped source-extension record; g_eff^{GSC-cand} retained as exact legacy alias`; control `gate_review_completed`; mathematical `scoped_source_extension_geff_object`; physical `not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations`; promotion `scoped_source_object_only`; guards: no_source_law_adoption<br>no_metricdata_e_adoption<br>no_unscoped_geff_adoption<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility.
- `matter_coupling`: reader-facing `accepted only as scoped source-extension evidence/precondition`; control `accepted_as_scoped_evidence_precondition`; mathematical `parameterized_finite_local_witness_precondition`; physical `not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics`; promotion `scoped_source_evidence_only`; guards: no_source_law_adoption<br>no_canonical_ontology_edit<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection.
- `einstein_equations`: reader-facing `not started; no positive derivation status`; control `not_started`; mathematical `dynamics_action_or_variation_missing`; physical `no_field_equation_derivation`; promotion `none`; guards: no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility.
- `benchmark_promotion`: reader-facing `no benchmark promotion from scoped evidence/precondition alone`; control `blocked`; mathematical `upstream_burdens_missing`; physical `no_exact_gr_benchmark_promotion`; promotion `none`; guards: no_benchmark_promotion<br>no_benchmark_gate_chair_closure<br>no_completed_derivation<br>no_einstein_equations<br>no_matter_coupling_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection.

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
| `g_eff` | ScopedMetricStructureRecord_src adopted as the scoped source-extension record; g_eff^{GSC-cand} retained as exact legacy alias | Bare g_eff remains an unresolved burden; the scoped record is not an unscoped Lorentzian metric and does not supply matter coupling or Einstein equations. | No MetricData(E), unscoped g_eff, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows from this row. |
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
| `source_ontology_primitives` | `source_ontology` | draft source-ontology primitives only | accepted | accepted_as_source_extension_data | scoped_obstruction | no_physical_interpretation_authorized | scoped_source_object_only | no_source_law_adoption<br>no_canonical_ontology_edit<br>no_metricdata_e_adoption<br>no_matter_coupling_adoption<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility | `research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex` |
| `source_equivalence_eqsrc` | `source_equivalence_eqsrc` | draft source-equivalence object only | draft object exists | draft_control_object_exists | general_equivalence_theorem_missing | downstream_gr_blocked | draft_control_only | no_source_law_adoption<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |
| `retain_h` | `source_equivalence_eqsrc` | blocked by missing primitive | blocked by missing primitive | blocked | primitive_missing | no_retention_law_adoption | none | no_source_law_adoption<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |
| `gen_h` | `source_equivalence_eqsrc` | blocked by missing primitive | blocked by missing primitive | blocked | primitive_missing | no_generator_law_adoption | none | no_source_law_adoption<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |
| `obsloc_lc` | `source_localization_obsloc_lc` | constructive local exact-branch witness only | constructive witness exists | constructive_witness_recorded | constructive_witness | local_exact_branch_only | draft_control_only | no_source_law_adoption<br>no_matter_coupling_derivation<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-037/artifacts/58_LOCALIZATION_SOURCE_BASIS_AXIOM_SELECTOR_DOMAIN_EQSRC_ALTERNATIVE_BRANCH_FAMILY_GUARD_STABILITY_SOURCE_PACKET_SMUGGLING_AUDIT.tex` |
| `resp_lc` | `response_localization_resp_lc` | accepted only as scoped source-extension selector data | accepted | accepted_as_source_extension_data | selector_data_source_extension | not_detector_semantics_not_matter_coupling | scoped_source_object_only | no_canonical_ontology_edit<br>no_matter_coupling_derivation<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-060/artifacts/101_RESP_LC_SOURCE_EXTENSION_HUMAN_GATE_ADOPTION_DECISION.tex` |
| `m_src` | `source_manifold_m_src` | adopted only as scoped source-only M_src object | accepted | gate_review_completed | scoped_source_only_adopted_object | not_target_manifold_not_metric_not_gr_derivation | scoped_source_object_only | no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex` |
| `g_eff` | `effective_metric_g_eff` | ScopedMetricStructureRecord_src adopted as the scoped source-extension record; g_eff^{GSC-cand} retained as exact legacy alias | accepted | gate_review_completed | scoped_source_extension_geff_object | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | scoped_source_object_only | no_source_law_adoption<br>no_metricdata_e_adoption<br>no_unscoped_geff_adoption<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility | `research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml` |
| `matter_coupling` | `matter_coupling` | accepted only as scoped source-extension evidence/precondition | accepted | accepted_as_scoped_evidence_precondition | parameterized_finite_local_witness_precondition | not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics | scoped_source_evidence_only | no_source_law_adoption<br>no_canonical_ontology_edit<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_detector_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | `research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex` |
| `einstein_equations` | `einstein_equations` | not started; no positive derivation status | draft object exists | not_started | dynamics_action_or_variation_missing | no_field_equation_derivation | none | no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility | `research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex` |
| `finite_variation_robustness` | `source_equivalence_eqsrc` | Refuter stress passed | Refuter stress passed | refuter_stress_passed | conditional_theorem_candidate | downstream_gr_blocked | draft_control_only | no_source_law_adoption<br>no_matter_coupling_derivation<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/tasks/RT-20260614-101/artifacts/142_RESP_LC_M_SRC_GSC_FINITE_VARIATION_ROBUSTNESS_LAW_REFUTER_STRESS_TEST.tex` |
| `benchmark_promotion` | `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | blocked by missing primitive | blocked | upstream_burdens_missing | no_exact_gr_benchmark_promotion | none | no_benchmark_promotion<br>no_benchmark_gate_chair_closure<br>no_completed_derivation<br>no_einstein_equations<br>no_matter_coupling_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | `research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex` |
| `gate_chair_status` | `benchmark_promotion` | human-gated verdict authority only | human-gated | human_gated | protected_verdict_missing | no_benchmark_closure | human_gate_required | no_benchmark_gate_chair_closure<br>no_benchmark_promotion<br>no_completed_derivation<br>no_einstein_equations<br>no_matter_coupling_derivation<br>no_future_source_extension_impossibility<br>no_global_theory_rejection | `research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex` |
| `finite_toy_metric_response` | `finite_toy_metric_response` | frozen negative local toy route only | frozen negative | frozen_negative | tag_removal_obstruction | local_toy_route_frozen_not_global_theory_rejection | frozen_negative_no_promotion | no_geff_scope_expansion<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation<br>no_global_theory_rejection<br>no_future_source_extension_impossibility | `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex` |

## Exact Next Route

The immediate next route is:

```text
Run the one governed checkpoint for AJ-RT-20260801-007-001. After it commits, route one fresh bounded P13-T07 improve-project-system packet to enforce generated-report source provenance and freshness; do not execute P13-T07 in this frame.
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

| Status | Count | Meaning |
| --- | --- | --- |
| `PASS` | 5 | receipt complete |
| `PASS_WITH_WARNINGS` | 1 | receipt complete with stated warnings |
| `PENDING` | 1 | open item; evidence must explain why |

Validation layers:

| Validation layer | Status | Meaning | Evidence |
| --- | --- | --- | --- |
| `pre_execution` | PASS | receipt complete | Generation 205 route, repository, branch, head, clean entry, claim, and one immutable worker invocation were validated. |
| `completion_internal` | PASS | receipt complete | The task-local cutover receipt passes 13 of 13 checks. |
| `post_write` | PASS | receipt complete | The authoritative planner full run passes all 28 selected gates; focused final-state validation passes. |
| `post_checkpoint` | PENDING | open item; evidence must explain why | One governed checkpoint remains authorized and uninvoked. |
| `renderer` | PASS | receipt complete | Frontier, task-index, dependency-graph, claim-graph, registry, and wiki derivatives will be regenerated from this tracked completion and handoff before checkpoint. |
| `memory_bootstrap` | PASS_WITH_WARNINGS | receipt complete with stated warnings | Tracked memory checks pass; local cache warnings are non-authoritative. |
| `claim_language_linter` | PASS | receipt complete | Changed claim-language validation has zero hard failures. |

Authorization layers:

| Authorization field | Value | Meaning |
| --- | --- | --- |
| `protected_scoped_gate_review_authorized` | false (not authorized) | scoped review authority only |
| `protected_scoped_gate_review_scope` | project-system validation orchestration only | exact scope of protected review authority |
| `protected_scoped_gate_review_authority_source_path` | none | tracked source for scoped review authority |
| `downstream_physics_promotion_authorized` | false (not authorized) | authorizes downstream physics promotion only when true |
| `downstream_physics_promotion_authority_source_path` | none | tracked source for downstream promotion authority |
| `benchmark_promotion_authorized` | false (not authorized) | authorizes benchmark promotion only when true |
| `benchmark_promotion_authority_source_path` | none | tracked source for benchmark authority |
| `completed_derivation_authorized` | false (not authorized) | authorizes completed-derivation claim only when true |
| `completed_derivation_authority_source_path` | none | tracked source for completed-derivation authority |
| `hosted_workflow_dispatch_authorized` | False | extension authorization field |
| `proof_authority` | False | extension authorization field |
| `publication_authorized` | False | extension authorization field |
| `push_authorized` | False | extension authorization field |

Legacy compatibility records:

- active task: `RT-20260801-007`;
- latest handoff: `handoff-0936`;
- current status: `p13_t02_planner_authoritative_cutover_completed_checkpoint_ready`;
- renderer source: `scripts/research_control/render_current_frontier.py`;
- renderer policy: tracked-state snapshot only, not authority;
- claim boundary: no ontology edit, no source-law adoption, no `MetricData(E)` adoption, no `g_eff` scope expansion, no coupling-law adoption, no matter-coupling derivation or adoption, no stress-energy semantics, no Einstein equations, no benchmark promotion, no completed derivation, and no downstream GR promotion.

## Retrieval Warning Status

This renderer reads only tracked control sources:

- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0936.yaml`
- `research_control/tasks/RT-20260801-007/00_TASK.yaml`
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

The AEther-Flow Research Project. (2026, July 1). *Handoff 0936*
[Internal research-control handoff].

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v14* [Internal implementation plan].
