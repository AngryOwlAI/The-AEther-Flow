<!-- authority: control -->

# handoff-0850 — P13-T04 payload complete, frontier repair required

Generation 92 implemented the bounded `P13-T04` payload under
`AJ-RT-20260723-020-001`. The repository now has exact Ruff and mypy
development tooling, bounded lint and strict type targets, a typed adapter over
the current validation planner and executor, a shared prospective
P10-T07-compatible path linter, and explicit Linux and macOS CPython 3.12
workflow cells.

The local Darwin CPython 3.12 quality target, all 13 new contract tests, and the
48-test combined focused shard pass. The hosted GitHub Actions cells were not
executed by this frame and are not claimed. No historical path was renamed,
truncated, deleted, or migrated. Required pre-checkpoint research-control
validation nevertheless fails because the generated current and compact
frontier artifacts remain bound to `handoff-0849`.

The direct renderer commands needed to synchronize those generated artifacts
are outside the immutable generation-92 AgentJob. The worker invocation was
not repeated, and no checkpoint, staging, or commit occurred.

## Required next action

Run one fresh bounded Validator Engineer recovery through
`improve-project-system`. It may render the current and compact frontiers from
the finalized tracked `P13-T04` state, repeat required pre-checkpoint
validation, and invoke one governed checkpoint only if every gate passes.

`P13-T05` and `P13-T06` have not been executed and remain blocked until that
recovery checkpoint. `P13-T02` remains blocked by the held `P13-T01` cutover.

## Authority boundary

This handoff creates no scientific, ontology, source-law, Distance-to-GR,
benchmark, proof, Gate Chair, completed-derivation, publication, push, hosted
workflow, or external-system authority. Generated frontiers must not be
hand-edited. The ordinary-route exception remains limited to the fact that
dependency-ready science task `P4-T05` requires explicit human Gate Chair
authority unavailable to this relay.
