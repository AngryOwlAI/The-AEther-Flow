<!-- authority: generated -->

# Compact Current Frontier v16

This generated index mirrors `output/compact_current_frontier_v16.yaml` and `output/compact_current_frontier_v16.json`. It is a snapshot-only reader aid. If it differs from tracked control state, tracked control state governs.

<!-- generated-report-provenance: {"freshness_status":"fresh_at_generation","generated_view_is_authority":false,"generation_time":"2026-08-04T05:18:15Z","maximum_commit_lag":"1","physics_promotion_authorized":false,"policy_id":"p13_t07_live_generated_report_freshness_v1","proof_authority":false,"report_class":"compact_current_frontier","schema_id":"generated_report_provenance_v1","source_commit":"2cc682251201d8d034dcd447fde006a49f3db650","source_hashes":[{"path":"registries/DISTANCE_TO_GR_LEDGER.csv","sha256":"8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642"},{"path":"registries/RESEARCH_TASK_REGISTRY.csv","sha256":"26bad5e313611909db7cf54ff305b25f1239445de88ac5f31f044838ae6af48b"},{"path":"research_control/current_frontier.md","sha256":"0722132dff379365dabd9ab6859d8f2d2ed5c5a64805ac4b81b07111b8b94fa3"},{"path":"research_control/handoffs/handoff-0961.yaml","sha256":"462cb60c3553fe5e373b4ce30f4780e6714c2fb740fe622eb229b5d6295e908e"},{"path":"research_control/program_state.yaml","sha256":"d6988171456915ffeab79ab66788892d946ec79d8686895e0e107dc9cfa6831c"},{"path":"research_control/tasks/RT-20260801-011/artifacts/generated_report_freshness_metadata_schema_v1.yaml","sha256":"dc83260a771ac0bed94e150de76f83d8fb163dbe356f1532da11018fce06adc3"},{"path":"scripts/research_control/generated_report_provenance.py","sha256":"af417fa48220fbb4abffd9a4ab2cb93b4f9ea32f2f26e67e65dd6ad6ba4cee6c"},{"path":"scripts/research_control/render_compact_current_frontier_v16.py","sha256":"3700556e8fe203bb8bfb1c2caf15b7fbfc95b25f608169209e1b9930677e3564"}],"source_manifest_sha256":"b0d2a9157db937bf40a70ad56599afc673a2dcbe35295cb352668abb100aafe2","source_path_count":"12","task_count":"1216"} -->

## Generated-Report Provenance

| Field | Value |
| --- | --- |
| Provenance schema | `generated_report_provenance_v1` |
| Freshness policy | `p13_t07_live_generated_report_freshness_v1` |
| Report class | `compact_current_frontier` |
| Source commit | `2cc682251201d8d034dcd447fde006a49f3db650` |
| Source-derived generation time | `2026-08-04T05:18:15Z` |
| Tracked task count | 1216 |
| Exact source-path count | 12 |
| Source manifest SHA-256 | `b0d2a9157db937bf40a70ad56599afc673a2dcbe35295cb352668abb100aafe2` |
| Maximum commit lag | 1 |
| Freshness status at generation | `fresh_at_generation` |
| Generated view is authority | `false` |

Exact primary source hashes:

- `registries/DISTANCE_TO_GR_LEDGER.csv`: `8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642`
- `registries/RESEARCH_TASK_REGISTRY.csv`: `26bad5e313611909db7cf54ff305b25f1239445de88ac5f31f044838ae6af48b`
- `research_control/current_frontier.md`: `0722132dff379365dabd9ab6859d8f2d2ed5c5a64805ac4b81b07111b8b94fa3`
- `research_control/handoffs/handoff-0961.yaml`: `462cb60c3553fe5e373b4ce30f4780e6714c2fb740fe622eb229b5d6295e908e`
- `research_control/program_state.yaml`: `d6988171456915ffeab79ab66788892d946ec79d8686895e0e107dc9cfa6831c`
- `research_control/tasks/RT-20260801-011/artifacts/generated_report_freshness_metadata_schema_v1.yaml`: `dc83260a771ac0bed94e150de76f83d8fb163dbe356f1532da11018fce06adc3`
- `scripts/research_control/generated_report_provenance.py`: `af417fa48220fbb4abffd9a4ab2cb93b4f9ea32f2f26e67e65dd6ad6ba4cee6c`
- `scripts/research_control/render_compact_current_frontier_v16.py`: `3700556e8fe203bb8bfb1c2caf15b7fbfc95b25f608169209e1b9930677e3564`

Live validation recomputes the full source manifest and commit lag.
Freshness PASS is operational evidence only; it is not physics proof
or claim-promotion authority.

## Active State

- Active task: `RT-20260803-020`
- Latest handoff: `handoff-0961`
- Current status: `p16_t04_generation_251_staged_checkpoint_contracts_reconciled_pending_checkpoint`
- V15 completed: `false`
- V16 plan registered: `true`

## Active-State Bifurcation

- Latest research task: `RT-20260803-020`
- Latest research handoff: `handoff-0961`
- Latest research next action: Run the single governed checkpoint for AJ-RT-20260803-020-001. After it commits, run one fresh bounded P16-T04 final claim-boundary re-audit through continue-research; do not execute P16-T05 first.
- Latest project-system task: `none`
- Latest project-system status: `none`
- Latest project-system sidecar task: `none`
- Latest project-system sidecar status: `none`
- Sidecar supersedes research handoff: `false`
- Next research route source: `latest_research_handoff`

## Next Route

- Route ID: `v21_p16_t04_fresh_claim_boundary_reaudit_after_generation_252_checkpoint`
- Role family: `external-red-team-reviewer@0.1.0`
- Target milestone: `benchmark_promotion`
- Milestone burden: Provide the final adversarial claim-boundary check without provenance overread.
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

- YAML SHA-256: `ad778236387828dc16453e2d49a4e09431ba301834b2b5e5ea96e7eff69b0c4e`
- JSON SHA-256: `c1ce73c14c724da192e2f34ae26285d31d36ded31d9ae865ac7656c95976785a`

## Authority Warning

This compact current frontier is not physics authority, proof authority, Gate Chair authority, benchmark authority, or completed-derivation evidence.
