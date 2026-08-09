<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

<!-- generated-report-provenance: {"freshness_status":"fresh_at_generation","generated_view_is_authority":false,"generation_time":"2026-08-09T08:56:40Z","maximum_commit_lag":"1","physics_promotion_authorized":false,"policy_id":"p13_t07_live_generated_report_freshness_v1","proof_authority":false,"report_class":"compact_current_frontier","schema_id":"generated_report_provenance_v1","source_commit":"488a7f2dd8a18075644d59ed497f3698ead9ee82","source_hashes":[{"path":"registries/DISTANCE_TO_GR_LEDGER.csv","sha256":"8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642"},{"path":"registries/RESEARCH_TASK_REGISTRY.csv","sha256":"0b7793b089f9a70dddfd6c558c2295b6158067880bc0861499af58535ad76a79"},{"path":"research_control/current_frontier.md","sha256":"857e8cd88dd726ce8d1271ab4769cc6f8c2656c98509fba1afd25ed6edc3f4af"},{"path":"research_control/handoffs/handoff-0978.yaml","sha256":"13dca24ba535b09c98dfdfa9eb7886015b1b3b613a7249041802e29ea3db64bf"},{"path":"research_control/program_state.yaml","sha256":"90175fa7881a111e12d6fc75d63712d8edff0bd12c9fda3ef68f1f670a2598ff"},{"path":"research_control/tasks/RT-20260801-011/artifacts/generated_report_freshness_metadata_schema_v1.yaml","sha256":"dc83260a771ac0bed94e150de76f83d8fb163dbe356f1532da11018fce06adc3"},{"path":"scripts/research_control/generated_report_provenance.py","sha256":"af417fa48220fbb4abffd9a4ab2cb93b4f9ea32f2f26e67e65dd6ad6ba4cee6c"},{"path":"scripts/research_control/render_compact_current_frontier_v16.py","sha256":"3700556e8fe203bb8bfb1c2caf15b7fbfc95b25f608169209e1b9930677e3564"}],"source_manifest_sha256":"37b441189efafcb507b7bc54a0d2cbb46749f09c791d35d7b2035b1da540125f","source_path_count":"12","task_count":"1233"} -->

## Generated-Report Provenance

| Field | Value |
| --- | --- |
| Provenance schema | `generated_report_provenance_v1` |
| Freshness policy | `p13_t07_live_generated_report_freshness_v1` |
| Report class | `compact_current_frontier` |
| Source commit | `488a7f2dd8a18075644d59ed497f3698ead9ee82` |
| Source-derived generation time | `2026-08-09T08:56:40Z` |
| Tracked task count | 1233 |
| Exact source-path count | 12 |
| Source manifest SHA-256 | `37b441189efafcb507b7bc54a0d2cbb46749f09c791d35d7b2035b1da540125f` |
| Maximum commit lag | 1 |
| Freshness status at generation | `fresh_at_generation` |
| Generated view is authority | `false` |

Exact primary source hashes:

- `registries/DISTANCE_TO_GR_LEDGER.csv`: `8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642`
- `registries/RESEARCH_TASK_REGISTRY.csv`: `0b7793b089f9a70dddfd6c558c2295b6158067880bc0861499af58535ad76a79`
- `research_control/current_frontier.md`: `857e8cd88dd726ce8d1271ab4769cc6f8c2656c98509fba1afd25ed6edc3f4af`
- `research_control/handoffs/handoff-0978.yaml`: `13dca24ba535b09c98dfdfa9eb7886015b1b3b613a7249041802e29ea3db64bf`
- `research_control/program_state.yaml`: `90175fa7881a111e12d6fc75d63712d8edff0bd12c9fda3ef68f1f670a2598ff`
- `research_control/tasks/RT-20260801-011/artifacts/generated_report_freshness_metadata_schema_v1.yaml`: `dc83260a771ac0bed94e150de76f83d8fb163dbe356f1532da11018fce06adc3`
- `scripts/research_control/generated_report_provenance.py`: `af417fa48220fbb4abffd9a4ab2cb93b4f9ea32f2f26e67e65dd6ad6ba4cee6c`
- `scripts/research_control/render_compact_current_frontier_v16.py`: `3700556e8fe203bb8bfb1c2caf15b7fbfc95b25f608169209e1b9930677e3564`

Live validation recomputes the full source manifest and commit lag.
Freshness PASS is operational evidence only; it is not physics proof
or claim-promotion authority.

## Active State

- Active task: `RT-20260809-008`
- Latest handoff: `handoff-0978`
- Current status: `v22_p2_t03_protocol_complete_p2_t04_selected_checkpoint_pending`
- V15 completed: `false`
- V16 plan registered: `true`

## Active-State Bifurcation

- Latest research task: `RT-20260809-008`
- Latest research handoff: `handoff-0978`
- Latest research next action: After the single governed checkpoint for AJ-RT-20260809-008-001 execute exactly one separately admitted V22 P2-T04 theoretical-continuation-selector AgentJob to compare source-side bridge candidate packets, select one primary and one fallback, leave the third slot unallocated, and preserve every adoption and protected-authority block.
- Latest project-system task: `none`
- Latest project-system status: `none`
- Latest project-system sidecar task: `none`
- Latest project-system sidecar status: `none`
- Sidecar supersedes research handoff: `false`
- Next research route source: `latest_research_handoff`

## Next Route

- Route ID: `v22_p2_t04_primary_and_fallback_candidate_selection`
- Role family: `theoretical-continuation-selector@0.1.0`
- Target milestone: `effective_metric_g_eff`
- Milestone burden: Metric law; choose the smallest source extension with a plausible path to a principal polynomial and operational geometry while keeping only one primary active and one fallback preregistered.
- Requires human gate: `false`

## High-Risk Rows

| Burden ID | Reader-facing status | Control | Physical | Promotion |
| --- | --- | --- | --- | --- |
| `m_src` | adopted only as scoped source-only M_src object | gate_review_completed | not_target_manifold_not_metric_not_gr_derivation | scoped_source_object_only |
| `g_eff` | ScopedMetricStructureRecord_src adopted as the scoped source-extension record; g_eff^{GSC-cand} retained as exact legacy alias | gate_review_completed | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | scoped_source_object_only |
| `matter_coupling` | open target matter-coupling derivation after protected source-side postulate adoption | accepted_as_scoped_evidence_precondition | not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics | scoped_source_evidence_only |
| `einstein_equations` | not started; no positive derivation status | not_started | no_field_equation_derivation | none |
| `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | blocked | no_exact_gr_benchmark_promotion | none |

## Positive-First Status Cards

These cards render high-risk rows in the required order: positive status, exact scope, allowed use, and blocked overread. They are operational calibration only and do not create physics proof authority.

| Object | Positive status | Scope | Allowed use | Blocked overread | Next burden |
| --- | --- | --- | --- | --- | --- |
| `m_src` | M_src is adopted only as a scoped source-only M_src object. | The adoption applies only under the declared source-only GSC candidate scope and fail-closed boundary. | Later bounded packets may use it as source-side prerequisite context. | not a target manifold<br>not a metric<br>not MetricData(E) scope expansion<br>not g_eff scope expansion<br>not matter coupling<br>not Einstein equations<br>not benchmark promotion<br>not completed derivation | Use scoped M_src only as source-side prerequisite context while deriving any later metric or coupling bridge without target-manifold or target-metric import. |
| `g_eff` | ScopedMetricStructureRecord_src is the primary name for the adopted scoped source-extension record; g_eff^{GSC-cand} is its exact legacy alias. | The adoption applies only to the exact declared source-extension candidate scope reviewed in RT-20260614-222. | Later bounded packets may use ScopedMetricStructureRecord_src as scoped source-extension context and may use g_eff^{GSC-cand} only as its explicit exact legacy alias. | bare g_eff remains an unresolved burden<br>not an unscoped Lorentzian metric<br>not MetricData(E) adoption<br>not unscoped g_eff<br>not matter coupling<br>not Einstein equations<br>not benchmark promotion<br>not completed derivation | Independently review the full Gate B package while using ScopedMetricStructureRecord_src as the scoped record and keeping bare g_eff unresolved. |
| `matter_coupling` | The unchanged finite P7SourceMatterPackage_v1 is adopted as canonical physical source matter by explicit protected human postulate. | The adoption is limited to the exact P7-T01 through P7-T06 source-side package, its declared finite domains, and the current continuum-first source architecture. | Later bounded packets may use the exact adopted source-matter meanings as scoped P8 input while independently constructing or obstructing g_eff-dependent target coupling. | not source-law adoption<br>not target matter semantics<br>not target detector semantics<br>not unscoped or target coupling-law adoption<br>not matter-coupling derivation<br>not target matter-coupling adoption<br>not target stress-energy semantics or tensor<br>not target matter action<br>not coupling through a derived g_eff<br>not Einstein equations<br>not benchmark promotion<br>not completed derivation | Derive or precisely obstruct the g_eff-dependent source-to-target coupling bridge without treating the protected source-side postulate as a derivation. |
| `einstein_equations` | einstein_equations remains blocked with open continuation and no positive derivation status. | No Einstein-equation premise, derivation, benchmark closure, or completed derivation has been established. | Later bounded packets may use this row only as a visible downstream burden and claim-boundary guard. | not field equations derived<br>not dynamics or action established<br>not matter coupling established<br>not benchmark closure<br>not completed derivation | Derive lawful dynamics/action/variation and matter coupling under protected gates before any Einstein-equation derivation claim. |
| `benchmark_promotion` | benchmark_promotion remains blocked by upstream derivation burdens and protected authority. | No exact-GR benchmark promotion, benchmark closure, fit claim, Gate Chair verdict, or completed derivation follows from scoped evidence/preconditions. | Later bounded packets may use this row only as a protected downstream authority boundary. | not benchmark promoted<br>not exact-GR derivation complete<br>not benchmark fit accepted<br>not Gate Chair verdict<br>not completed derivation | Complete upstream derivation burdens and protected Gate Chair benchmark review before any benchmark promotion or completed-derivation claim. |

## Metric-Use Ledger

- Ledger path: `registries/METRIC_USE_LEDGER.csv`
- Total rows: `25`
- Forbidden/import guard rows: `25`
- Blocked physical metric-use rows: `13`
- Authority: project-control guard ledger only; no physics proof authority.

## Snapshot Hashes

- YAML SHA-256: `e0c60df04e1b366ee609c2de1f94d5502067ef81079c426c9c5aeb5d48d1b37c`
- JSON SHA-256: `83a1916e463b4540a177d37d246c1d09d7ae3bcd224ccf2397e9391715a81e3c`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
