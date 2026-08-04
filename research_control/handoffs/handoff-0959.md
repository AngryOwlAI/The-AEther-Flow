---
authority: control
handoff_id: handoff-0959
task_id: RT-20260803-018
plan_task_id: P16-T03
status: blocked_precheckpoint
---

# Handoff 0959 — RT-017 ordered allowlist parity restored

## Result

Generation 250 preserved `AJ-RT-20260803-017-001.yaml` byte-for-byte and
restored its exact ordered 61-path write contract across the expired execution
role, the AgentJob registry row, and the role-execution registry row. The
task-local receipt confirms all four representations are identical, every
protected RT-017 hash matches, and no non-allowlist role or registry field
changed.

The scoped repair is complete, but the cumulative transaction is not ready for
checkpoint. The inherited RT-015, RT-016, and RT-017 documentation-impact
receipts do not yet cover the full current path set, including the original
`FOLDER_MAP.md` generated-derivative omission, the generation-248 blocker, and
the new bounded RT-018 control paths. Generation 250 did not edit those older
receipts and did not invoke or retry any checkpoint.

## Next action

Run one fresh bounded `improve-project-system` recovery using
`recover_generation_250_cumulative_documentation_impact_coverage_v1`. Repair
only the exact cumulative receipt omissions in RT-015, RT-016, and RT-017;
regenerate and revalidate the transaction; then invoke at most one fresh
governed checkpoint.

The next packet must not replay AJ-RT-20260803-017-001, re-run its failed
checkpoint, execute the P16-T04 re-audit, or begin P16-T05.

## Authority boundary

This handoff records project-control identity recovery only. It changes no
canonical science, ontology, source law, Gate decision, benchmark status,
Distance-to-GR entry, external-review status, independent-replication status,
proof, publication, push, outward action, or completed-derivation authority.

## Evidence

- Completion: `research_control/tasks/RT-20260803-018/jobs/completions/AJC-AJ-RT-20260803-018-001.yaml`
- Parity receipt: `research_control/tasks/RT-20260803-018/artifacts/p16_t04_rt017_allowlist_parity_recovery_receipt.json`
- Precheckpoint blocker: `research_control/tasks/RT-20260803-018/artifacts/precheckpoint_blocker_generation_250_documentation_receipt_coverage_v1.yaml`
- Source blocker: `research_control/tasks/RT-20260803-017/artifacts/checkpoint_blocker_generation_248_rt015_folder_map_coverage_v1.yaml`
