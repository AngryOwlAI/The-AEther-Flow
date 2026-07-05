<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

## Active State

- Active task: `RT-20260705-044`
- Latest handoff: `handoff-0617`
- Current status: `v17_p0_t02_backlog_materialized_no_physics_delta`
- V15 completed: `false`
- V16 plan registered: `true`

## Next Route

- Route ID: `v17_active_state_preflight`
- Role family: `director-of-research@0.3.0`
- Target milestone: `matter_coupling`
- Milestone burden: Verify active-state sources before executing v17 physics or project-system tasks.
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

- YAML SHA-256: `58ada80eeb340090f245616b15cf10e29c1c7b5f32e2d038909d6f1bfa3c2bc8`
- JSON SHA-256: `12baa43dcf1108bef54695e13e14683c73b4d75dffbdc0e445f6b13440f79086`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
