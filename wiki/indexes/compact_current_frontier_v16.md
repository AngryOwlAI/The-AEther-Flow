<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

## Active State

- Active task: `RT-20260705-041`
- Latest handoff: `handoff-0614`
- Current status: `v16_p17_t03_final_validation_packet_completed_no_physics_delta`
- V15 completed: `true`
- V16 plan registered: `true`

## Next Route

- Route ID: `v16_final_ordinary_continuation_handoff`
- Role family: `director-of-research@0.3.0`
- Target milestone: `matter_coupling`
- Milestone burden: Select exactly one ordinary continuation route from final v16 outputs without physics delta.
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

- YAML SHA-256: `d477bff3f6d7a7bcaa55de94789e4a611d0e8d4a316eb2781dcf05494616dcb5`
- JSON SHA-256: `6addfcc13a642a14d67293a5ac26273725c5a321097b3c0d7057e1d5013f4e14`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
