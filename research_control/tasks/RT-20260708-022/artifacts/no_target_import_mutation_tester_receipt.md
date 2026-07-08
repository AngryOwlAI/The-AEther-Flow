<!-- authority: control -->

# P7-T04 No-Target Import Mutation Tester Receipt

## Summary

Implemented `no_target_import_mutation_tester` as support-only validator
tooling for v18 P7-T04. The tester starts from a source-safe control snippet,
applies the seven plan-defined forbidden-premise mutations, and verifies that
the existing claim-language linter fails closed with the expected class IDs.

This receipt does not claim proof authority, source-law adoption, target metric
import, `MetricData(E)` adoption, `g_eff` adoption or scope expansion,
matter-coupling derivation, stress-energy semantics, matter-action semantics,
Einstein-equation derivation, benchmark promotion, Gate Chair verdict, or
completed derivation.

## Implemented Outputs

- `scripts/research_control/support_formalization/no_target_import_mutation_tester.py`
- `tests/test_no_target_import_mutation_tester.py`
- `research_control/tasks/RT-20260708-022/artifacts/no_target_import_mutation_tester_spec_v1.md`
- `research_control/tasks/RT-20260708-022/artifacts/no_target_import_mutation_tester_report.json`
- `research_control/tasks/RT-20260708-022/artifacts/p7_t04_no_target_import_mutation_tester_report.json`

## Mutation Results

| Mutation | Expected result |
| --- | --- |
| `insert_target_metric_premise` | Linter fails closed on target metric as source-certificate input. |
| `insert_proper_time_normalization` | Linter fails closed on detector/proper-time readout as source semantics. |
| `insert_empirical_detector_protocol` | Linter fails closed on detector semantics as source-label substitute. |
| `insert_stress_energy_semantics` | Linter fails closed on stress-energy notation as matter semantics. |
| `insert_matter_action_premise` | Linter fails closed on matter action as coupling-law derivation. |
| `insert_benchmark_behavior_premise` | Linter fails closed on benchmark behavior as source evidence. |
| `insert_validator_as_proof_premise` | Linter fails closed on validator PASS as proof authority. |

## Verification

- `.venv/bin/python -m unittest tests/test_no_target_import_mutation_tester.py`
  passed six focused tests.
- `.venv/bin/python scripts/research_control/support_formalization/no_target_import_mutation_tester.py --mutation all --json-output research_control/tasks/RT-20260708-022/artifacts/no_target_import_mutation_tester_report.json --json`
  produced `status: PASS`, `mutation_count: 7`, and `failed_check_count: 0`.
- `.venv/bin/python research_control/tasks/RT-20260708-022/artifacts/validate_p7_t04_no_target_import_mutation_tester.py --write-report`
  passed with `failed_check_count: 0`.

## Boundary

The tester reuses the existing claim-language linter. It does not change
validator policy, does not make validator output a theorem, and does not alter
physics-source status. Generated reports are control evidence only.

## Next Route

Run one bounded v18 P7-T05 `metric_use_ledger_tex_validator_support_only`
packet.
