<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

## Active State

- Active task: `RT-20260705-055`
- Latest handoff: `handoff-0628`
- Current status: `v17_p3_t02_acceptance_calibration_schema_completed_no_physics_delta`
- V15 completed: `false`
- V16 plan registered: `true`

## Next Route

- Route ID: `v17_p3_t03_claim_language_underclaim_calibration_linter`
- Role family: ``
- Target milestone: `matter_coupling`
- Milestone burden: Add advisory underclaim warnings using accepted-status calibration fields while preserving existing overclaim hard gates.
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

- YAML SHA-256: `d57c3af312d57f8197324d63606135a557127ba9c214225e81b8ab8a4e569f88`
- JSON SHA-256: `9fb153e072aca77905591827c56b63104ac85875b490c929317f7f95cf066936`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
