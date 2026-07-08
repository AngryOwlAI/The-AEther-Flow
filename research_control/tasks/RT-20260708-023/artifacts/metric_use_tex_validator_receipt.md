<!-- authority: control -->

# P7-T05 Metric-Use Ledger TeX Validator Receipt

## Summary

Implemented `validate_metric_use_tex_references.py` as support-only validator
tooling for v18 P7-T05. The validator scans configured TeX artifacts from
`METRIC_USE_LEDGER.csv`, detects high-risk metric-adjacent references, and
requires either same-artifact ledger coverage or an explicit no-use
justification comment.

This receipt does not claim proof authority, source-law adoption, target metric
import, `MetricData(E)` adoption, `g_eff` adoption or scope expansion,
matter-coupling derivation, stress-energy semantics, matter-action semantics,
Einstein-equation derivation, benchmark promotion, Gate Chair verdict, or
completed derivation.

## Implemented Outputs

- `scripts/research_control/validate_metric_use_tex_references.py`
- `tests/test_validate_metric_use_tex_references.py`
- `research_control/tasks/RT-20260708-023/artifacts/metric_use_tex_validator_spec_v1.md`
- `research_control/tasks/RT-20260708-023/artifacts/metric_use_tex_validator_report.json`
- `research_control/tasks/RT-20260708-023/artifacts/p7_t05_metric_use_tex_validator_report.json`

## Required Classes

| Class | Coverage behavior |
| --- | --- |
| `g_eff` | Body references require matching ledger evidence or no-use justification. |
| `metricdata_e` | `MetricData(E)` and metric-form assignment references require coverage. |
| `proper_time` | Proper-time references require coverage. |
| `detector_calibration` | Detector or calibration references require coverage. |
| `stress_energy` | Stress-energy and stress-tensor references require coverage. |
| `matter_action` | Matter-action and matter-Lagrangian references require coverage. |

## Verification

- `.venv/bin/python -m unittest tests/test_validate_metric_use_tex_references.py`
  passed six focused tests.
- `.venv/bin/python scripts/research_control/validate_metric_use_tex_references.py --json-output research_control/tasks/RT-20260708-023/artifacts/metric_use_tex_validator_report.json --json`
  produced `status: PASS`, `configured_path_count: 3`, and `finding_count: 0`.
- `.venv/bin/python research_control/tasks/RT-20260708-023/artifacts/validate_p7_t05_metric_use_tex_validator.py --write-report`
  passed with `failed_check_count: 0`.

## Boundary

The validator reads ledger rows and TeX artifacts; it does not mutate the
ledger, change validator policy, create a proof, or alter physics-source
status. TeX macro declarations are ignored as declaration surface unless a
body-level reference exists.

## Next Route

Run one bounded v18 P7-T06
`detector_placeholder_collapse_checker_support_only` packet.
