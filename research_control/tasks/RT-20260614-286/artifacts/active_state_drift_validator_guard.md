<!-- authority: control -->

# Active-State Drift Validator Guard

## Analysis

P1-T03 required a deterministic validator guard for contradictions between
`research_control/current_frontier.md` and active-state authority. The
authority order remains:

1. `research_control/program_state.yaml`
2. the latest handoff named by program state
3. the active task folder
4. `registries/DISTANCE_TO_GR_LEDGER.csv`
5. `current_frontier.md` as synchronized snapshot only

## Implementation

The guard is implemented in `scripts/research_control/validate_research_control.py`.
It parses the `Active Research State` and `Distance-To-GR Table` sections of
`current_frontier.md` and validates:

- active task ID;
- latest handoff ID;
- current status;
- next recommended action as a required handoff phrase;
- target milestone when the latest handoff names one;
- active Distance-to-GR burden status against the ledger when the handoff names
  a non-`none` burden;
- active task folder consistency.

When drift is found, the error includes the field name, authoritative value,
snapshot value, authoritative source path, and the repair route:
`run one bounded current-frontier synchronization repair packet under continue-research before proceeding`.

## Regression Evidence

Focused tests were added to `tests/test_research_control.py`:

- synchronized fixture passes;
- deliberately stale active-task snapshot fails;
- deliberately stale active Distance-to-GR burden status fails.

The live snapshot was also resynchronized to the post-P1-T03 state so the new
guard validates this transaction.

## Boundary

This is project-control validation work only. It does not change
`registries/DISTANCE_TO_GR_LEDGER.csv`, adopt any source law, promote
`MetricData(E)`, expand `g_eff`, derive matter coupling, import stress-energy
semantics, derive Einstein equations, promote a benchmark, or claim a
completed derivation.
