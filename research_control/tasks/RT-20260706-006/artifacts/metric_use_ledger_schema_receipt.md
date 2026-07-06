<!-- authority: control -->

# P5-T01 Metric-Use Ledger Schema Receipt

## Summary

`RT-20260706-006` executed one bounded v17 P5-T01 project-control packet. It
created `research_control/design/metric_use_ledger_schema_v1.md` and
`registries/METRIC_USE_LEDGER.csv`.

The registry currently contains only the required header:

```csv
use_id,task_id,artifact_path,object_used,use_category,declared_scope,allowed_use,forbidden_interpretations,no_target_guard_path,audit_status,stress_status,created_at,notes
```

## Result

The schema defines required columns, allowed use categories, forbidden metric
uses, audit fields, stress fields, no-target guard routing, and the P5-T02
population rule.

Allowed use categories:

```text
scoped_source_extension_context
source_side_relation_input_candidate
finite_local_witness_context
blocked_physical_metric_use
forbidden_import_detected
```

Forbidden metric uses:

```text
physical_lorentzian_metric
proper_time_normalization
detector_calibration
stress_energy_semantics
matter_action_premise
Einstein_equation_premise
benchmark_fit_premise
```

## Boundary

This receipt records no ledger population and no physics delta. It does not
authorize `MetricData(E)` adoption, `g_eff` scope expansion, physical
Lorentzian metric use, proper-time normalization, detector calibration,
stress-energy semantics, matter action, Einstein equations, benchmark
promotion, Gate Chair verdict, or completed derivation.

## Verification

```text
.venv/bin/python research_control/tasks/RT-20260706-006/artifacts/validate_p5_t01_metric_use_ledger_schema.py
```

Result: `PASS`.

## Next Route

The next lawful v17 continuation is P5-T02:

```text
metric-use ledger initial population
```
