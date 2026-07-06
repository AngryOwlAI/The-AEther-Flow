<!-- authority: control -->

# Handoff 0641

## Analysis

`RT-20260706-009` completed the bounded v17 P5-T04 metric-use frontier
integration packet. The generated current frontier now includes a
Metric-Use Ledger Warning section, and the compact frontier exposes the
metric-use ledger path plus guarded row counts.

The packet is renderer and validator control only. It does not change the
Distance-to-GR ledger, physics source material, protected gate verdicts,
benchmark status, or completed-derivation status.

## Completed Work

- Updated `scripts/research_control/render_current_frontier.py` to read
  `registries/METRIC_USE_LEDGER.csv` and render a concise metric-use ledger
  warning/status section.
- Updated `scripts/research_control/render_compact_current_frontier_v16.py`
  to expose `metric_use_ledger` with the ledger path, total row count,
  forbidden/import guard row count, blocked metric-use row count, and status
  counts.
- Updated `scripts/research_control/validate_compact_current_frontier_v16.py`
  to require the compact metric-use ledger summary.
- Added focused renderer and compact-validator test coverage.
- Added task-local validator and receipt for P5-T04.

## Boundary

Blocked readings:

- P5-T04 metric-use ledger summary as physics proof.
- P5-T04 metric-use ledger summary as `MetricData(E)` adoption.
- P5-T04 metric-use ledger summary as `g_eff` scope expansion.
- P5-T04 metric-use ledger summary as physical metric authority.
- P5-T04 metric-use ledger summary as stress-energy semantics, matter action,
  Einstein equations, benchmark promotion, or completed derivation.

## Next Route

Run one bounded v17 P6-T01 upstream-burden selector packet:

```text
Select whether to attack EqSrc, RetainH, GenH, or continue matter-coupling candidate repair.
```

This next packet should use P2 candidate-cycle result, detector route status,
metric-use ledger status, and current EqSrc/RetainH/GenH Distance-to-GR
statuses as selector inputs.
