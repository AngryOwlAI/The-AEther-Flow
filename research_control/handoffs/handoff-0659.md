<!-- authority: control -->

# Handoff 0659

## Status

`RT-20260706-027` completed one bounded v17 `P10-T03` task-index validator
packet.

## Result

Created the task-index validator and focused test coverage:

- `scripts/research_control/validate_task_index.py`
- `tests/test_task_index_renderer.py`
- `task_index_validation` coverage in the local full validation runner

The validator checks freshness, header equality, renderer-row equality, source
task directories, completion paths, status compatibility, support-only
`physics_delta=false`, and forbidden positive overread language. Historical
missing task metadata remains reported as warnings rather than silently repaired
or promoted to unrelated hard failures.

## Boundary

No P10-T04 memory or folder-documentation integration was created. No
Distance-to-GR ledger row changed. No source law, `MetricData(E)`, `g_eff`,
matter coupling, Einstein equations, benchmark status, Gate Chair verdict,
ontology authority, or completed derivation was promoted.

## Next Action

Run one bounded v17 `P10-T04` task-index memory and folder-documentation
integration packet through an active memory/documentation curator-compatible
role overlay.
