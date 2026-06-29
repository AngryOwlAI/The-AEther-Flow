<!-- authority: control -->

# Handoff 0329

## Summary

V12 P1-T03 layered ledger validator guard hardening is complete.

The transaction updated:

- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `scripts/research_control/validate_research_control.py`
- `tests/test_research_control.py`

The validator now checks exact protected status layers for high-risk
Distance-to-GR rows, requires accepted scoped rows to remain scoped, rejects
scoped physical layers without explicit not/no/blocked wording, rejects
generated snapshots as layered-status authority, and preserves a machine guard
against reading the finite toy frozen-negative result as future
source-extension impossibility.

## Next Action

Run P1-T04 as one bounded continue-research transaction to update the
current-frontier renderer so layered Distance-to-GR statuses and overread
guards are visible.

## Boundary

The next packet may update the generated current-frontier renderer and tests
only. It must preserve all current scientific meaning and must not edit
canonical ontology, adopt a source law, adopt `MetricData(E)`, expand or adopt
`g_eff`, adopt a coupling law, derive or adopt matter coupling, import
stress-energy semantics, construct a stress-energy tensor, import matter action
or detector semantics, derive Einstein equations, promote an exact-GR
benchmark, close a benchmark Gate Chair verdict, or claim completed
derivation.

## Evidence

- Completion receipt:
  `research_control/tasks/RT-20260629-034/jobs/completions/AJC-AJ-RT-20260629-034-001.yaml`
- Ledger:
  `registries/DISTANCE_TO_GR_LEDGER.csv`
- Validator:
  `scripts/research_control/validate_research_control.py`
- Focused regression tests:
  `tests/test_research_control.py`
- Implementation plan:
  `implementations_plans/recommendations_implementation_plan_continue_task-v12.md`

## Project-Improvement Signals

None.

## APA 7 Source Note

The AEther-Flow Research Project. (2026, June 29). *Distance-to-GR status
layers v1* [Internal control design note].
