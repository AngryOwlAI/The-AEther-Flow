<!-- authority: control -->

---
authority: control
status: blocked_validation
handoff_id: handoff-0810
task_id: RT-20260721-009
job_id: AJ-RT-20260721-009-001
---

# Handoff 0810: P10-T08 payload complete; checkpoint blocked

RT-20260721-009 completed only v21 P10-T08 under one bounded
`project-control-maintainer@0.2.0` AgentJob. It moved ten authored stable
milestone definitions and their dependency graph out of mutable status prose,
removed the legacy inline Current Status column from the canonical burden map,
and preserved the prior map bytes through exact Git commit and SHA-256 markers.

One task-local renderer now reads the authoritative Distance-to-GR ledger,
program state, latest handoff, task registry, authored definitions, and burden
map. Its generated Markdown reader view contains all 14 current ledger burdens
and embeds the exact six source hashes, a full source commit, the handoff
generation time, and the tracked task count. The output is explicitly marked
generated and noncanonical. The ledger, program state, and latest handoff
continue to govern if the view becomes stale.

Twelve internal checks and 11 focused tests pass. The tests deliberately reject
stale source hashes, duplicate or blank burden rows, unmapped milestones,
dependency cycles, mutable status fields inside stable definitions,
program-state/handoff contradictions, and tracked-output drift. This is
operational project-control freshness evidence only. No ledger row, scientific
status, ontology, event-store reader or writer, protected P4-T05 gate, or
promotion, proof, publication, or completed-derivation authority changed.

Required repository validation fails because the registered burden map is
mutable while the validator still requires its current hash in immutable
historical memory-preflight snapshots. The P10-T08 AgentJob does not authorize
shared-validator edits or historical receipt rewrites. No checkpoint ran.

P10-T07 remains the selected plan successor, but it is not execution-ready
while this transaction is dirty and uncheckpointed. The lawful next action is
one governed `improve-project-system` recovery that adds only this registered
map to the established mutable memory-preflight source set, proves historical
snapshot compatibility while preserving active-current and immutable-source
hash checks, reruns required validation, and checkpoints the combined P10-T08
transaction. P10-T07 and P10-T09 must remain unexecuted until that succeeds.
