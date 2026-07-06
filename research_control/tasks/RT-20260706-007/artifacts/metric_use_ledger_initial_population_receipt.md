<!-- authority: control -->

# P5-T02 Metric-Use Ledger Initial Population Receipt

## Summary

`RT-20260706-007` populated `registries/METRIC_USE_LEDGER.csv` for the five
required v17 P5-T02 inspection surfaces. The ledger rows are grouped by
artifact and reference class because the P5-T01 schema records object/use
classes rather than line-number fields.

This receipt is project-control evidence only. It does not expand `g_eff`,
adopt `MetricData(E)`, authorize target Lorentzian metric use, normalize
proper time, calibrate detectors, import stress-energy semantics, define a
matter action, derive Einstein equations, promote a benchmark, or claim a
completed derivation.

## Required Scope Coverage

| Required surface | Ledger rows | Coverage status |
| --- | --- | --- |
| `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex` | `MUL-RT-20260706-007-001` through `MUL-RT-20260706-007-005` | Covered by scoped `g_eff`, source-side relation candidate, target-metric guard, detector-benchmark guard, and stress-energy guard rows. |
| `research_control/tasks/RT-20260704-021/artifacts/source_side_coupling_law_target_specification_v1.tex` | `MUL-RT-20260706-007-006` through `MUL-RT-20260706-007-008` | Covered by target-metric/proper-time, detector, and stress-energy/matter-action/Einstein guard rows. |
| `research_control/tasks/RT-20260705-047/artifacts/source_side_coupling_law_candidate_v1.tex` | `MUL-RT-20260706-007-009` through `MUL-RT-20260706-007-011` | Covered by target-metric import guard, detector-response block, and stress-energy/matter-action/Einstein import-guard rows. |
| `research_control/current_frontier.md` | `MUL-RT-20260706-007-012` through `MUL-RT-20260706-007-015` | Covered by current-frontier scoped `g_eff`, `MetricData(E)` overread guard, matter-coupling finite witness, and finite toy metric-response rows. |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | `MUL-RT-20260706-007-016` through `MUL-RT-20260706-007-019` | Covered by Distance-to-GR `g_eff`, matter-coupling, `m_src` overread guard, and finite toy metric-response rows. |

## Line-Cluster Evidence

- Gate Chair scoped `g_eff` review:
  - `g_eff` scoped-source-extension references: lines 22, 33, 54, 55, 60, 99, and 232.
  - `MetricFormAssign` and metric-form candidate language: lines 89, 121, and 204.
  - target metric, Lorentzian signature, proper time, detector, benchmark, and registry-overread guards: lines 44, 45, 124, 125, 142, and 182.
  - stress-energy semantics guard: line 147.
- Coupling-law target specification:
  - detector and stress-energy guard language: lines 66, 67, 75, 116, 163, 169, 177, 179, 184, 185, 252, 253, 264, 265, 285, 286, 314, 316, 366, 370, 390, 392, 401, and 402.
  - No literal `g_eff` or `MetricData(E)` reference was found in this artifact by targeted search; therefore no-use justification is recorded for those objects here.
- Source-side coupling-law candidate:
  - target metric and topology import guards: lines 42, 44, 69, 70, 238, 260, and 261.
  - detector placeholder or block language: lines 111, 141, 183, 187, 191, 242, 251, 279, and 317.
  - stress-energy, matter-action, Lagrangian, coupling-law, and Einstein-equation overread guards: lines 226, 228, 239, 240, 260, 261, 332, 333, 343, and 344.
  - No literal `g_eff` or `MetricData(E)` reference was found in this artifact by targeted search; therefore no-use justification is recorded for those objects here.
- Current frontier:
  - `g_eff`, `MetricData(E)`, metric, matter-coupling, stress-energy, matter-action, detector, Einstein, benchmark, and finite toy metric-response boundaries appear in high-risk status rows and blocked-claim sections around lines 67, 68, 74, 80, 92, 115, 119, 125, 135, 170, 188, 210, 224, 242, 250, 257, and 290.
- Distance-to-GR ledger:
  - High-risk rows are `m_src`, `g_eff`, `matter_coupling`, and `finite_toy_metric_response`, with overread guards blocking `MetricData(E)`, `g_eff` scope expansion, matter coupling, Einstein equations, benchmark promotion, completed derivation, and global theory rejection as applicable.

## No-Use Justifications

- `source_side_coupling_law_target_specification_v1.tex` contains no literal
  `g_eff` or `MetricData(E)` reference. Its high-risk content is guard
  language for target metric, proper time, detector semantics, stress-energy,
  matter action, Einstein equations, and benchmark overreads.
- `source_side_coupling_law_candidate_v1.tex` contains no literal `g_eff` or
  `MetricData(E)` reference. Its high-risk content is guard language and
  detector-block language that prevents target-metric and matter-physics
  imports.
- `research_control/current_frontier.md` and
  `registries/DISTANCE_TO_GR_LEDGER.csv` use `g_eff` and `MetricData(E)` only
  as scoped status or blocked-overread context. The ledger rows record that
  status without changing it.

## Validator

Task-local validator:

```text
research_control/tasks/RT-20260706-007/artifacts/validate_p5_t02_metric_use_ledger_population.py
```

Report:

```text
research_control/tasks/RT-20260706-007/artifacts/p5_t02_metric_use_ledger_population_report.json
```

Initial result: `PASS`.

## Next Route

The logical next step is P5-T03: add metric-use linter tests that reject
forbidden physical uses of `g_eff` while allowing scoped source-extension
context under the declared boundary.
