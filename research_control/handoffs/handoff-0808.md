<!-- authority: control -->

---
authority: control
status: ready_for_director
handoff_id: handoff-0808
task_id: RT-20260721-007
job_id: AJ-RT-20260721-007-001
---

# Handoff 0808: P10-T05 architecture selected; P10-T06 pilot selected

RT-20260721-007 completed only v21 P10-T05 under one bounded
`project-control-maintainer@0.2.0` AgentJob. It compared tracked JSONL,
SQLite-only, and hybrid storage and selected
`hybrid_tracked_jsonl_plus_generated_sqlite` for a future separately
authorized pilot.

The design binds 13 exact tracked sources and defines eight project-control
event domains, full SHA-256 content identities, append-only corrections, ten
deterministic non-authoritative views, one-writer expected-head
compare-and-swap, one-checkpoint transaction visibility, phased migration,
rollback, and text-first historical readability. Its 36 architecture checks
and 10 focused mutation tests pass.

This is an architecture result, not activation. P10-T05 created no event-store
segment, manifest, SQLite index, imported event, dual-write path, replacement
view, reader switch, or cutover. Existing tracked control sources retain their
current authority. Registered TeX and Gate Chair artifacts retain scientific
and protected authority. Generated views and validator PASS are not scientific
proof, and Distance-to-GR is unchanged.

P10-T06 now satisfies its sole dependency and is the selected next plan item.
One fresh `validator-engineer@0.2.0` AgentJob may implement a bounded,
non-authoritative read-compatible pilot over selected recent control events and
candidate lineage, generate shadow task, candidate, handoff, and status views,
and record exact parity losses. It must not cut over authority. P10-T07 remains
dependency-ready but unexecuted, and protected P4-T05 remains human-gated.
