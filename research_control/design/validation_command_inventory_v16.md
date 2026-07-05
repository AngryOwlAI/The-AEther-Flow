<!-- authority: control -->

# Validation Command Inventory v16

This inventory tracks v16 validation commands as operational controls. A PASS
result means the named control ran successfully in the local repository state.
No validator PASS is proof authority, physics-claim authority, source-law
adoption, matter-coupling derivation, Einstein-equation derivation, benchmark
promotion, Gate Chair closure, or completed-derivation evidence.

## P15 Compact Frontier Checks

| Check | Command | Purpose | Authority level | When to run |
| --- | --- | --- | --- | --- |
| compact frontier render check | `.venv/bin/python scripts/research_control/render_compact_current_frontier_v16.py --check` | Confirm compact YAML, JSON, and generated Markdown match tracked state. | `required-render-check` | After program state, latest handoff, current-frontier, or Distance-to-GR tracked-state inputs change. |
| compact frontier synchronization validation | `.venv/bin/python scripts/research_control/validate_compact_current_frontier_v16.py --json` | Fail on active-task, latest-handoff, next-route, high-risk-row, blocked-claim, authority-warning, and protected-target overpromotion drift in compact outputs. | `required-gate` | Before checkpoint when compact frontier outputs or their tracked inputs change. |
| integrated research-control validation | `.venv/bin/python scripts/research_control/validate_research_control.py` | Runs the compact synchronization hook as part of the broader research-control spine validation. | `required-gate` | Before checkpoint for research-control state changes. |
| full local validation compact check | `.venv/bin/python scripts/research_control/run_full_research_control_validation.py --json` | Includes `compact_current_frontier_check` in the local CI-equivalent command plan. | `ci-smoke` | For local CI-equivalent runs and v16 final coverage audits. |

## P16 Consolidation Notice

P16-T02 owns the full v16 inventory update for minimum payload validation,
route-orbit hard-gate checks, target-import attack validation, claim graph
validation, dependency graph checks, documentation impact, claim-language
linting, memory bootstrap, and research-control validation. This P15-T03 entry
records the compact frontier check integration first so the new snapshot cannot
drift while later v16 inventory consolidation proceeds.
