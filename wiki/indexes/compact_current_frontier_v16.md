<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

## Active State

- Active task: `RT-20260708-003`
- Latest handoff: `handoff-0696`
- Current status: `v18_p4_t03_countermodel_obligation_validator_completed_no_physics_delta`
- V15 completed: `false`
- V16 plan registered: `true`

## Active-State Bifurcation

- Latest research task: `RT-20260708-003`
- Latest research handoff: `handoff-0696`
- Latest research next action: Run one bounded v18 P4-T04 theorem-task template integration packet.
- Latest project-system task: `none`
- Latest project-system status: `none`
- Latest project-system sidecar task: `none`
- Latest project-system sidecar status: `none`
- Sidecar supersedes research handoff: `false`
- Next research route source: `latest_research_handoff`

## Next Route

- Route ID: `countermodel_obligation_task_template_integration`
- Role family: `documentation-curator@2.0.0`
- Target milestone: `none`
- Milestone burden: Update theorem-task templates to require minimal countermodel slots.
- Requires human gate: `false`

## High-Risk Rows

| Burden ID | Reader-facing status | Control | Physical | Promotion |
| --- | --- | --- | --- | --- |
| `m_src` | adopted only as scoped source-only M_src object | gate_review_completed | not_target_manifold_not_metric_not_gr_derivation | scoped_source_object_only |
| `g_eff` | adopted only as scoped source-extension g_eff object | gate_review_completed | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | scoped_source_object_only |
| `matter_coupling` | accepted only as scoped source-extension evidence/precondition | accepted_as_scoped_evidence_precondition | not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics | scoped_source_evidence_only |
| `einstein_equations` | not started; no positive derivation status | not_started | no_field_equation_derivation | none |
| `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | blocked | no_exact_gr_benchmark_promotion | none |

## Positive-First Status Cards

These cards render high-risk rows in the required order: positive status, exact scope, allowed use, and blocked overread. They are operational calibration only and do not create physics proof authority.

| Object | Positive status | Scope | Allowed use | Blocked overread |
| --- | --- | --- | --- | --- |
| `m_src` | M_src is adopted only as a scoped source-only M_src object. | The adoption applies only under the declared source-only GSC candidate scope and fail-closed boundary. | Later bounded packets may use it as source-side prerequisite context. | no_target_manifold<br>no_metric<br>no_metricdata_e_scope_expansion<br>no_geff_scope_expansion<br>no_matter_coupling<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation |
| `g_eff` | g_eff is adopted only as a scoped source-extension g_eff object. | The adoption applies only to the declared source-extension candidate scope. | Later bounded packets may use it as scoped source-extension context. | no_unscoped_lorentzian_metric<br>no_metricdata_e_adoption<br>no_unscoped_geff<br>no_matter_coupling<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation |
| `matter_coupling` | matter_coupling has accepted scoped evidence/precondition only for continuation. | The support is certificate-indexed, source-side, and finite/local only. | Later bounded packets may use it to construct, audit, or stress one source-side coupling-law candidate. | no_source_law_adoption<br>no_rr_e_transport_law_adoption<br>no_positive_ms_profile_adoption<br>no_source_matter_semantics_readiness_law_adoption<br>no_matter_semantics_adoption<br>no_detector_semantics_adoption<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_matter_coupling_adoption<br>no_stress_energy_semantics<br>no_stress_energy_tensor<br>no_matter_action<br>no_metricdata_e_adoption<br>no_geff_scope_expansion<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation |
| `einstein_equations` | not started; no positive derivation status | The status is limited to control status not_started, mathematical status dynamics_action_or_variation_missing, physical status no_field_equation_derivation. | Later bounded packets may use this row only as a blocked-target boundary condition. | No einstein equations follows from this row.<br>No benchmark promotion follows from this row.<br>No completed derivation follows from this row. |
| `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | The status is limited to control status blocked, mathematical status upstream_burdens_missing, physical status no_exact_gr_benchmark_promotion. | Later bounded packets may use this row only as a blocked-target boundary condition. | No benchmark promotion follows from this row.<br>No benchmark gate chair closure follows from this row.<br>No completed derivation follows from this row. |

## Metric-Use Ledger

- Ledger path: `registries/METRIC_USE_LEDGER.csv`
- Total rows: `19`
- Forbidden/import guard rows: `19`
- Blocked physical metric-use rows: `11`
- Authority: project-control guard ledger only; no physics proof authority.

## Snapshot Hashes

- YAML SHA-256: `20ddea4e3ecf6aecc8a89759616a8e7459cc07a33e33ab40c1fab3b910191b62`
- JSON SHA-256: `5ab8851eda4ce33958dafaa8e5d80d8b09360a2f5feeb20b0f2102bdb5b4cf44`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
