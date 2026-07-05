<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

## Active State

- Active task: `RT-20260705-042`
- Latest handoff: `handoff-0615`
- Current status: `v16_completed_ordinary_continuation_selected_no_physics_delta`
- V15 completed: `true`
- V16 plan registered: `true`

## Next Route

- Route ID: `concrete_coupling_law_candidate_construction_route`
- Role family: `candidate-constructor@0.2.0`
- Target milestone: `matter_coupling`
- Milestone burden: Construct one bounded source-side coupling-law candidate from the v16 source-side coupling-law target specification and finite/local certificate evidence without adoption or downstream physics promotion.
- Requires human gate: `false`

## High-Risk Rows

| Burden ID | Reader-facing status | Control | Physical | Promotion |
| --- | --- | --- | --- | --- |
| `m_src` | adopted only as scoped source-only M_src object | gate_review_completed | not_target_manifold_not_metric_not_gr_derivation | scoped_source_object_only |
| `g_eff` | adopted only as scoped source-extension g_eff object | gate_review_completed | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | scoped_source_object_only |
| `matter_coupling` | accepted only as scoped source-extension evidence/precondition | accepted_as_scoped_evidence_precondition | not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics | scoped_source_evidence_only |
| `einstein_equations` | not started; no positive derivation status | not_started | no_field_equation_derivation | none |
| `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | blocked | no_exact_gr_benchmark_promotion | none |

## Snapshot Hashes

- YAML SHA-256: `2e67c1ce98e758bb9cdcdd4ed25abc2b3888754589635896a1aef11f1415f89a`
- JSON SHA-256: `003a5466bb3c9b619aaa0e83dcbd0dd421a1888ce3f692630d00a8394455b821`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
