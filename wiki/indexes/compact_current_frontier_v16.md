<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

## Active State

- Active task: `RT-20260705-036`
- Latest handoff: `handoff-0609`
- Current status: `v16_p16_t01_documentation_impact_consolidation_completed_no_physics_delta`
- V15 completed: `true`
- V16 plan registered: `true`

## Next Route

- Route ID: `validation_command_inventory_v16_update`
- Role family: `validator-engineer@0.2.0`
- Target milestone: `matter_coupling`
- Milestone burden: Update v16 validation command inventory to include all v16 checks without physics delta.
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

- YAML SHA-256: `bec78117b9de153dc7d22787b7af874a3c8e1c26ee351bfaf71a600caaceb227`
- JSON SHA-256: `aca8ca8c602f7a81bd98d49b126d0d51d41cdba1d9a12edde4911d5be7ff1057`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
