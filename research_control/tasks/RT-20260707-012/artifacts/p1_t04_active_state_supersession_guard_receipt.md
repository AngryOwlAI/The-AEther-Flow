# P1-T04 Repair Receipt: Active-State Supersession Guard

## Status

PASS.

## Repair

`scripts/research_control/validate_research_control.py` now requires sidecar
supersession to resolve through a tracked Director decision. A handoff-level or
bifurcation-level truthy flag is not sufficient.

Valid supersession requires:

- a Director decision id;
- a matching `DIRECTOR_DECISION_REGISTRY.csv` row;
- a readable DDR at the registered decision path;
- DDR front matter with `active_state_supersession_authorized: true` or
  `sidecar_supersession_authorized: true`;
- a nonblank supersession scope.

## Focused Evidence

- `tests.test_validate_research_control` ran 7 tests and passed.
- `validate_p1_t04_active_state_supersession_guard.py --write-report --json`
  passed.

## Boundary

This repair changes validator enforcement only. It does not authorize physics
promotion, source-law adoption, general `EqSrc` discharge, `RetainH` adoption,
`GenH` adoption, matter-coupling derivation, Einstein-equation derivation,
benchmark promotion, external outreach, Gate Chair verdict, or completed
derivation.

## Next Route

Because the repair passed, the next v18 route is `P2-T01`.
