---
authority: control
handoff_id: "handoff-0589"
task_id: "RT-20260705-016"
job_id: "AJ-RT-20260705-016-001"
status: "completed"
created_at: "2026-07-05T05:27:00Z"
---

# Handoff 0589

RT-20260705-016 completed v16 P8-T03 by adding
`scripts/research_control/validate_status_field_compatibility.py`, a focused
fixture suite, focused unit tests, and a task-local fixture report.

The validator hard-gates unsafe future records that set broad promotion fields
without layered authority, conflate scoped evidence with downstream promotion,
use Gate Chair scoped evidence acceptance as source-law adoption, render bare
`accepted` for high-risk future rows, or set `scientific_claims_changed` without
naming the changed layer. The historical scoped broad-field fixture warns at
most.

No historical record was rewritten. No physics status changed.

The logical next step is one bounded P9-T01 packet to define the `EqSrc`,
`RetainH`, and `GenH` trigger-horizon policy.
