<!-- authority: control -->

# P5-T03 Metric-Use Linter Receipt

## Summary

RT-20260706-008 completed one bounded v17 P5-T03 validator packet. The packet
extends the existing claim-language linter taxonomy and focused tests so
forbidden `g_eff` physical-metric overreads fail deterministically, while
scoped source-extension context remains an allowed passing form.

## Implemented Coverage

The linter now has explicit hard-fail classes for:

- `g_eff_proper_time_normalization_overread`;
- `g_eff_detector_calibration_overread`;
- `g_eff_stress_energy_semantics_overread`.

The pre-existing `g_eff_overclaim` class continues to catch unreviewed
`MetricData(E)` adoption wording. A synthetic reviewed-context test confirms
that protected authority must be explicit before that wording is downgraded
from hard failure to review warning.

## Files Changed

- `research_control/design/claim_language_linter_taxonomy.yaml`
- `tests/test_validate_claim_language.py`
- `research_control/tasks/RT-20260706-008/artifacts/validate_p5_t03_metric_use_linter.py`
- `research_control/tasks/RT-20260706-008/artifacts/p5_t03_metric_use_linter_report.json`

## Validation

The task-local validator passed:

```text
.venv/bin/python research_control/tasks/RT-20260706-008/artifacts/validate_p5_t03_metric_use_linter.py --write-report
```

The focused claim-language unit tests passed:

```text
.venv/bin/python -m unittest tests.test_validate_claim_language
```

Result: 35 tests ran successfully.

## Boundary

This packet is project-control validator work only. It does not revise physics
sources, update the Distance-to-GR ledger, adopt `MetricData(E)`, expand
`g_eff`, authorize a physical Lorentzian metric, authorize proper-time
normalization, calibrate detectors, import stress-energy semantics, define a
matter action, derive Einstein equations, promote benchmark status, issue a
Gate Chair verdict, or claim completed derivation.

## Next Route

The logical next v17 packet is P5-T04: integrate the metric-use ledger into the
current frontier and compact frontier without changing physics status.
