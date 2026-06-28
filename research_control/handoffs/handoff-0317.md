# Handoff 0317

## Summary

P1-T01 active-state authority invariant completed. The packet selects Path A,
generated snapshot, as the target current-frontier policy.

## Authority Boundary

`research_control/program_state.yaml` is the compact live state pointer. The
latest handoff named by that file is the immediate routing authority.
`registries/DISTANCE_TO_GR_LEDGER.csv` remains the persistent burden-state
ledger. `research_control/current_frontier.md` is a generated or synchronized
control snapshot and is not independent authority.

This packet does not repair `current_frontier.md`, does not add a validator
guard, and does not add `render_current_frontier.py`.

No canonical ontology edit, source-law adoption, `MetricData(E)` adoption,
`g_eff` adoption or scope expansion, coupling-law adoption, matter-coupling
derivation, stress-energy semantics, stress-energy tensor, matter action,
detector semantics, Einstein equations, benchmark promotion, or completed
derivation was promoted.

## Output

- `research_control/tasks/RT-20260614-284/artifacts/active_state_authority_invariant.md`

## Next Action

Run one bounded P1-T02 `process-integrity-auditor@0.1.0` packet to synchronize
`research_control/current_frontier.md` with live `program_state.yaml`, the
latest handoff, and Distance-to-GR ledger context under the invariant.

## References

The AEther-Flow Research Project. (2026, June 28). *Handoff 0316* [Internal
control handoff].

The AEther-Flow Research Project. (2026, June 28). *Recommendations
implementation plan continue task v11* [Internal implementation plan].
