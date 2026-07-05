<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

## Active State

- Active task: `RT-20260705-040`
- Latest handoff: `handoff-0613`
- Current status: `v16_p17_t02_current_frontier_compact_summary_refresh_completed_no_physics_delta`
- V15 completed: `true`
- V16 plan registered: `true`

## Next Route

- Route ID: `v16_final_validation_packet`
- Role family: `validator-engineer@0.2.0`
- Target milestone: `matter_coupling`
- Milestone burden: Run final v16 validation layers and record exact pending reasons if any without physics delta.
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

- YAML SHA-256: `89527f63a92b4ebae6102483c4090bf966df8567c36e1f6ff2877bbc80ba2e39`
- JSON SHA-256: `66e663af2caca1a83c28a68a233b3461812fa02a5d6c18620fe9095cc43c65e6`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
