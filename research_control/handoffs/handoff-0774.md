---
authority: control
status: ready_for_director
handoff_id: handoff-0774
task_id: RT-20260720-004
job_id: AJ-RT-20260720-004-001
---

# Handoff 0774: Active allowlist parity restored

`RT-20260720-004` completed one bounded
`project-control-maintainer@0.2.0` repair packet.

## Repair outcome

The completed `RT-20260720-003` AgentJob contains one job-only write pattern,
`research_control/tasks/RT-*/jobs/**`. Its execution-role record does not.
Both source records agree with their respective registry rows, so the
canonical resolver correctly rejected the active snapshot.

The predecessor task, decision, AgentJob, role, completion, handoff, and
checkpoint remain unchanged. A new task now carries one exact least-authority
write allowlist across its AgentJob, execution-role record, and both registry
rows. This supersedes only the active routing snapshot; it neither rewrites
history nor broadens the expired predecessor role.

## Scientific authority preserved

`RT-20260718-047` and `handoff-0772` remain the scientific basis for the fresh
Smuggling Auditor review of proposal-only
`EqSrcFlowGeneratedGradedOrbitRootLaw_src^cand,v1`. The repair changes no
science TeX, ontology source, Distance-to-GR row, metric-use row, benchmark
status, Gate Chair authority, proof authority, or completed-derivation status.

## Next bounded action

Run one separately authorized v21 `P0-T02` Project-Control Maintainer packet
to materialize the recommendation backlog and dependency DAG. This repair did
not execute `P0-T02` or `P1-T01`.
