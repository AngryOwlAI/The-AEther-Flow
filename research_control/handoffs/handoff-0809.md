<!-- authority: control -->

---
authority: control
status: ready_for_director
handoff_id: handoff-0809
task_id: RT-20260721-008
job_id: AJ-RT-20260721-008-001
---

# Handoff 0809: P10-T06 shadow pilot passes; P10-T08 selected

RT-20260721-008 completed only v21 P10-T06 under one bounded
`validator-engineer@0.2.0` AgentJob. It read 12 tracked sources from pinned
commit `0cfe0fe53f31ea2e1d3855d397ba30258dd4f444` and produced 20
full-SHA-256, source-linked shadow events across seven project-control domains.
Those events deterministically regenerate four task-local task, candidate,
handoff, and status compatibility views and one ignored disposable SQLite
query index.

Thirteen internal checks and 13 focused tests pass. The bounded views contain
zero mismatches and zero unmapped fields. The receipts explicitly preserve
three legacy-shape findings—handoff field aliases, reverse-chronological task
row order, and YAML decimal normalization—and five migration risks. In
particular, the pilot did not exercise or authorize a production writer,
concurrent correction, protected-authority transition, dual write, reader
switch, registry replacement, or cutover.

This is project-control feasibility and risk evidence, not general migration
readiness or scientific evidence. Existing tracked registries and control
sources retain their authority. Registered TeX and Gate Chair artifacts retain
scientific and protected authority. No historical source, candidate status,
ontology, scientific ledger, Distance-to-GR row, or protected P4-T05 gate
changed.

P10-T08 now has qualifying P10-T05 and P10-T06 completion evidence and is the
selected next plan item under the P10-T06 handoff rule. One fresh
`project-control-maintainer@0.2.0` AgentJob may separate stable burden
definitions from generated current values and render current burden status from
the authoritative Distance-to-GR ledger, program state, and latest handoff. It
must not cut over the event store or execute protected P4-T05. P10-T07 remains
independently dependency-ready but unexecuted.
