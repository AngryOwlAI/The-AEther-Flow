<!-- authority: control -->

# Handoff 0328

## Summary

V12 P1-T02 ledger schema migration is complete.

The transaction updated:

- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `scripts/research_control/validate_research_control.py`
- `tests/test_research_control.py`
- `research_control/tasks/RT-20260629-033/artifacts/distance_to_gr_layered_status_migration_report.md`

The Distance-to-GR ledger now has additive `control_status`,
`mathematical_status`, `physical_status`, `promotion_status`, and
`overread_guard` layers. All legacy `current_status` values and existing
scientific meanings were preserved.

## Next Action

Run P1-T03 as one bounded continue-research transaction to harden validator
guard tests for layered ledger semantics without changing scientific status.

## Boundary

The next packet may harden validators and tests for layered ledger semantics
only. It must preserve all current scientific meaning and must not edit
canonical ontology, adopt a source law, adopt `MetricData(E)`, expand or adopt
`g_eff`, adopt a coupling law, derive or adopt matter coupling, import
stress-energy semantics, construct a stress-energy tensor, import matter action
or detector semantics, derive Einstein equations, promote an exact-GR
benchmark, close a benchmark Gate Chair verdict, or claim completed derivation.

## Evidence

- Completion receipt:
  `research_control/tasks/RT-20260629-033/jobs/completions/AJC-AJ-RT-20260629-033-001.yaml`
- Migration report:
  `research_control/tasks/RT-20260629-033/artifacts/distance_to_gr_layered_status_migration_report.md`
- Ledger:
  `registries/DISTANCE_TO_GR_LEDGER.csv`
- Validator:
  `scripts/research_control/validate_research_control.py`
- Focused regression test:
  `tests/test_research_control.py`
- Implementation plan:
  `implementations_plans/recommendations_implementation_plan_continue_task-v12.md`

## Project-Improvement Signals

None.

## APA 7 Source Note

The AEther-Flow Research Project. (2026, June 29). *Distance-to-GR layered
status migration report* [Internal control migration report].
