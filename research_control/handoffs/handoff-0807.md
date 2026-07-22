<!-- authority: control -->

---
authority: control
status: ready_for_director
handoff_id: handoff-0807
task_id: RT-20260721-006
job_id: AJ-RT-20260721-006-001
---

# Handoff 0807: P10-T04 attempt history complete; P10-T05 selected

RT-20260721-006 completed only v21 P10-T04 under one bounded
`project-control-maintainer@0.2.0` AgentJob. It created a task-local event
schema, privacy policy, append-only ledger, validator, deterministic report,
compact receipt, and focused tests.

The ledger contains eight finalized events bound to eight exact tracked source
hashes: one attempt start, one validation failure, one audit finding, two
repairs, one supersession, zero abandoned attempts, and two completions. Its
contiguous SHA-256 chain terminates at
`604dfa5cfe197a402c576f226dd2776e1929fca24993ba144e207324b35c3717`.
The unsupported abandoned-event class is an explicit bounded absence with no
inference. Historic compute metadata stays `not_recorded`; only the current
ledger-build runtime is recorded as operational telemetry.

Ten focused tests and the deterministic write/check cycle pass. The privacy
scan records zero findings, every event sets `physics_result: false`, and all
scientific and protected authority flags remain false. This history indexes
canonical sources; it does not replace or reinterpret them. A process failure
is not a physics result, and validator PASS is not scientific proof.

P10-T03 and P10-T04 now satisfy the direct dependencies for P10-T05. The next
lawful plan item is one fresh P10-T05 project-system AgentJob routed to
`project-control-maintainer@0.2.0`. It may compare JSONL, SQLite, and hybrid
storage and specify the canonical event-store, generated-view, transaction,
migration, and rollback architecture. It must stop before cutover. This
handoff does not execute P10-T05 or protected P4-T05 and supplies no scientific
or protected authority.
