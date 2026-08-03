<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

<!-- generated-report-provenance: {"freshness_status":"fresh_at_generation","generated_view_is_authority":false,"generation_time":"2026-08-02T21:10:21Z","maximum_commit_lag":"1","physics_promotion_authorized":false,"policy_id":"p13_t07_live_generated_report_freshness_v1","proof_authority":false,"report_class":"compact_current_frontier","schema_id":"generated_report_provenance_v1","source_commit":"efbf0e490f9994af1a22cc2ebf2ae13d699b5b79","source_hashes":[{"path":"registries/DISTANCE_TO_GR_LEDGER.csv","sha256":"6b81b42bc7ed83f74f8062f2ade26988e8b369aa2d23744fc9e392279e1de5d8"},{"path":"registries/RESEARCH_TASK_REGISTRY.csv","sha256":"f998998dbc50e6eb1c70018b2cc34957db207189f6562bce2c78768f2315876a"},{"path":"research_control/current_frontier.md","sha256":"bd356eea8e4762ce48e2498c04d2b675727cf7b8ee76e51b91d51caae3e851e4"},{"path":"research_control/handoffs/handoff-0943.yaml","sha256":"1ce2e68c38b2939adf6a4a8392c26011fa857cb919cdb8db53c1e666e3a7bbfb"},{"path":"research_control/program_state.yaml","sha256":"219c8044390f5478f407ca55037d6e02de71230f4642a5277bce57ef41e2fa44"},{"path":"research_control/tasks/RT-20260801-011/artifacts/generated_report_freshness_metadata_schema_v1.yaml","sha256":"dc83260a771ac0bed94e150de76f83d8fb163dbe356f1532da11018fce06adc3"},{"path":"scripts/research_control/generated_report_provenance.py","sha256":"af417fa48220fbb4abffd9a4ab2cb93b4f9ea32f2f26e67e65dd6ad6ba4cee6c"},{"path":"scripts/research_control/render_compact_current_frontier_v16.py","sha256":"36fab56791487f690c7fd31ef036a1dba82d03a66beddefac5a21baf77ab10c2"}],"source_manifest_sha256":"8e2aedb2166d6fceb027b9ce5030aab7bbaa01ee88f5a07c5a175b7eedd33c71","source_path_count":"12","task_count":"1197"} -->

## Generated-Report Provenance

| Field | Value |
| --- | --- |
| Provenance schema | `generated_report_provenance_v1` |
| Freshness policy | `p13_t07_live_generated_report_freshness_v1` |
| Report class | `compact_current_frontier` |
| Source commit | `efbf0e490f9994af1a22cc2ebf2ae13d699b5b79` |
| Source-derived generation time | `2026-08-02T21:10:21Z` |
| Tracked task count | 1197 |
| Exact source-path count | 12 |
| Source manifest SHA-256 | `8e2aedb2166d6fceb027b9ce5030aab7bbaa01ee88f5a07c5a175b7eedd33c71` |
| Maximum commit lag | 1 |
| Freshness status at generation | `fresh_at_generation` |
| Generated view is authority | `false` |

Exact primary source hashes:

- `registries/DISTANCE_TO_GR_LEDGER.csv`: `6b81b42bc7ed83f74f8062f2ade26988e8b369aa2d23744fc9e392279e1de5d8`
- `registries/RESEARCH_TASK_REGISTRY.csv`: `f998998dbc50e6eb1c70018b2cc34957db207189f6562bce2c78768f2315876a`
- `research_control/current_frontier.md`: `bd356eea8e4762ce48e2498c04d2b675727cf7b8ee76e51b91d51caae3e851e4`
- `research_control/handoffs/handoff-0943.yaml`: `1ce2e68c38b2939adf6a4a8392c26011fa857cb919cdb8db53c1e666e3a7bbfb`
- `research_control/program_state.yaml`: `219c8044390f5478f407ca55037d6e02de71230f4642a5277bce57ef41e2fa44`
- `research_control/tasks/RT-20260801-011/artifacts/generated_report_freshness_metadata_schema_v1.yaml`: `dc83260a771ac0bed94e150de76f83d8fb163dbe356f1532da11018fce06adc3`
- `scripts/research_control/generated_report_provenance.py`: `af417fa48220fbb4abffd9a4ab2cb93b4f9ea32f2f26e67e65dd6ad6ba4cee6c`
- `scripts/research_control/render_compact_current_frontier_v16.py`: `36fab56791487f690c7fd31ef036a1dba82d03a66beddefac5a21baf77ab10c2`

Live validation recomputes the full source manifest and commit lag.
Freshness PASS is operational evidence only; it is not physics proof
or claim-promotion authority.

## Active State

- Active task: `RT-20260802-010`
- Latest handoff: `handoff-0943`
- Current status: `p15_t07_exact_four_package_no_external_action_decision_complete_precheckpoint`
- V15 completed: `false`
- V16 plan registered: `true`

## Active-State Bifurcation

- Latest research task: `RT-20260802-010`
- Latest research handoff: `handoff-0943`
- Latest research next action: Run one governed checkpoint for AJ-RT-20260802-010-001. After checkpoint, reconcile the terminal file-backed relay without replay and route dependency-ready P16-T01 through continue-research for the complete recommendation-coverage audit.
- Latest project-system task: `none`
- Latest project-system status: `none`
- Latest project-system sidecar task: `none`
- Latest project-system sidecar status: `none`
- Sidecar supersedes research handoff: `false`
- Next research route source: `latest_research_handoff`

## Next Route

- Route ID: `v21_p16_t01_complete_recommendation_coverage_audit`
- Role family: `process-integrity-auditor@0.1.0`
- Target milestone: `benchmark_promotion`
- Milestone burden: Prove plan coverage without treating coverage as scientific success.
- Requires human gate: `false`

## High-Risk Rows

| Burden ID | Reader-facing status | Control | Physical | Promotion |
| --- | --- | --- | --- | --- |
| `m_src` | adopted only as scoped source-only M_src object | gate_review_completed | not_target_manifold_not_metric_not_gr_derivation | scoped_source_object_only |
| `g_eff` | ScopedMetricStructureRecord_src adopted as the scoped source-extension record; g_eff^{GSC-cand} retained as exact legacy alias | gate_review_completed | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | scoped_source_object_only |
| `matter_coupling` | accepted only as scoped source-extension evidence/precondition | accepted_as_scoped_evidence_precondition | not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics | scoped_source_evidence_only |
| `einstein_equations` | not started; no positive derivation status | not_started | no_field_equation_derivation | none |
| `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | blocked | no_exact_gr_benchmark_promotion | none |

## Positive-First Status Cards

These cards render high-risk rows in the required order: positive status, exact scope, allowed use, and blocked overread. They are operational calibration only and do not create physics proof authority.

| Object | Positive status | Scope | Allowed use | Blocked overread | Next burden |
| --- | --- | --- | --- | --- | --- |
| `m_src` | M_src is adopted only as a scoped source-only M_src object. | The adoption applies only under the declared source-only GSC candidate scope and fail-closed boundary. | Later bounded packets may use it as source-side prerequisite context. | not a target manifold<br>not a metric<br>not MetricData(E) scope expansion<br>not g_eff scope expansion<br>not matter coupling<br>not Einstein equations<br>not benchmark promotion<br>not completed derivation | Use scoped M_src only as source-side prerequisite context while deriving any later metric or coupling bridge without target-manifold or target-metric import. |
| `g_eff` | ScopedMetricStructureRecord_src is the primary name for the adopted scoped source-extension record; g_eff^{GSC-cand} is its exact legacy alias. | The adoption applies only to the exact declared source-extension candidate scope reviewed in RT-20260614-222. | Later bounded packets may use ScopedMetricStructureRecord_src as scoped source-extension context and may use g_eff^{GSC-cand} only as its explicit exact legacy alias. | bare g_eff remains an unresolved burden<br>not an unscoped Lorentzian metric<br>not MetricData(E) adoption<br>not unscoped g_eff<br>not matter coupling<br>not Einstein equations<br>not benchmark promotion<br>not completed derivation | Independently review the full Gate B package while using ScopedMetricStructureRecord_src as the scoped record and keeping bare g_eff unresolved. |
| `matter_coupling` | matter_coupling has accepted scoped evidence/precondition only for continuation. | The support is certificate-indexed, source-side, and finite/local only. | Later bounded packets may use it to construct, audit, or stress one source-side coupling-law candidate. | not source-law adoption<br>not detector semantics<br>not coupling-law adoption<br>not matter-coupling derivation<br>not stress-energy semantics<br>not matter action<br>not Einstein equations<br>not benchmark promotion<br>not completed derivation | Construct, audit, or stress one source-side coupling-law candidate from the scoped evidence/preconditions before any matter-coupling derivation or adoption claim. |
| `einstein_equations` | einstein_equations remains blocked with open continuation and no positive derivation status. | No Einstein-equation premise, derivation, benchmark closure, or completed derivation has been established. | Later bounded packets may use this row only as a visible downstream burden and claim-boundary guard. | not field equations derived<br>not dynamics or action established<br>not matter coupling established<br>not benchmark closure<br>not completed derivation | Derive lawful dynamics/action/variation and matter coupling under protected gates before any Einstein-equation derivation claim. |
| `benchmark_promotion` | benchmark_promotion remains blocked by upstream derivation burdens and protected authority. | No exact-GR benchmark promotion, benchmark closure, fit claim, Gate Chair verdict, or completed derivation follows from scoped evidence/preconditions. | Later bounded packets may use this row only as a protected downstream authority boundary. | not benchmark promoted<br>not exact-GR derivation complete<br>not benchmark fit accepted<br>not Gate Chair verdict<br>not completed derivation | Complete upstream derivation burdens and protected Gate Chair benchmark review before any benchmark promotion or completed-derivation claim. |

## Metric-Use Ledger

- Ledger path: `registries/METRIC_USE_LEDGER.csv`
- Total rows: `25`
- Forbidden/import guard rows: `25`
- Blocked physical metric-use rows: `13`
- Authority: project-control guard ledger only; no physics proof authority.

## Snapshot Hashes

- YAML SHA-256: `d32eb18b5149db01bf9453c32b0856bb54e9bca0abf09eb018fd5089650f52d3`
- JSON SHA-256: `75e68728fc2196f7744b5046f018793c2642761ba597847100336e777ceee467`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
