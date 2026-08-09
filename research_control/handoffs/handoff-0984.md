---
authority: control
handoff_id: "handoff-0984"
task_id: "RT-20260809-014"
job_id: "AJ-RT-20260809-014-001"
status: "ready_for_v22_p3_t03_after_allowlist_parity_checkpoint"
validation_status: "PASS_PRECHECKPOINT_STAGING_REQUIRED"
created_at: "2026-08-09T15:23:29Z"
---

# Handoff 0984 — P3-T02 ordered allowlist parity recovery

The successful RT-013 checkpoint committed the P3-T02 staged-acceptance
recovery. Live continuation then found one ordered write-allowlist mismatch:
the immutable AgentJob and its registry row listed handoff-0983 YAML before
Markdown, while the expired execution-role overlay and role-registry row used
the reverse order. All four representations contained the same 17 unique
paths.

This recovery aligns only the expired role and its registry projection to the
AgentJob order. The AgentJob, completion, handoff, recovery evidence, and
P3-T02 manuscript, model, fixtures, ledgers, validation, and compact receipt
remain at their sealed hashes. Validator semantics are unchanged, P3-T02 was
not replayed, and P3-T03 remains selected but unexecuted.

One governed checkpoint for `AJ-RT-20260809-014-001` remains. Only after that
checkpoint commits may a separately admitted P3-T03 Candidate Constructor
packet run with Refuter and Validator Engineer perspectives. P2-T02 remains
externally gated. No ontology adoption, effective metric, Gate result,
publication, push, reviewer contact, or other external action is authorized.
