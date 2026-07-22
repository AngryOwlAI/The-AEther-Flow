<!-- authority: control -->

---
authority: control
status: ready_for_director
handoff_id: handoff-0811
task_id: RT-20260722-001
job_id: AJ-RT-20260722-001-001
---

# Handoff 0811: P10-T08 transaction recovered; P10-T07 selected

The bounded project-system recovery repaired the exact validator compatibility
defect that prevented the complete P10-T08 transaction from checkpointing. The
registered GR derivation burden map now participates in the established mutable
memory-preflight rule: immutable historical receipts retain their observed hash,
while an active task must still carry the current registered source hash. One
focused regression case directly exercises the burden-map object ID.

The repair did not alter the authored P10-T08 control payload. Its ten stable
burden definitions, all 14 Distance-to-GR ledger burdens, six source bindings,
twelve internal checks, and 11 focused tests remain valid. The stable
definitions, renderer, validator, completion, and blocked handoff remain
byte-for-byte preserved. Only declared generated current-status views may
refresh from the new live program state and handoff.

This is project-system compatibility and freshness evidence only. No scientific
ledger row, ontology, source law, mathematical or physical interpretation,
event-store authority, protected P4-T05 gate, or promotion, proof, publication,
or completed-derivation authority changed.

P10-T07 remains the sole selected successor and becomes execution-ready only
after the governed generation-42 checkpoint succeeds. Its bounded objective is
to define stable artifact paths and content-addressed references without
rewriting historical paths. P10-T09 and the protected P4-T05 decision remain
outside this handoff.
