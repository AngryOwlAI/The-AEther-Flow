<!-- authority: control -->

# Handoff handoff-0911 — P9-T01 immutable AgentJob status parity recovery

Status: `blocked_validation`.

`handoff-0911` records the bounded generation-170 Process Integrity Auditor
recovery.

## Result

Exactly one token changes in
`AJ-RT-20260729-012-001.yaml`: its first top-level lifecycle status changes
from `active` to `completed`. Reversing that substitution reproduces the exact
sealed predecessor hash
`0de2bcf0b70cffde72dd4a823ee0b56a18d92b0c1ee33504769c3bb821191bd0`.
The AgentJob now agrees with its completed registry row and completion.

The protected P9-T01 completion, protocol, `handoff-0908`, `handoff-0909`,
checkpoint `14a82f7`, and all scientific status remain unchanged. P9-T01 was
not replayed and P9-T02 remains unexecuted.

Integrated precheckpoint validation then found a distinct routing-accounting
conflict. The two uncheckpointed recovery task records name P9-T02 as their
implementation identity even though both explicitly recover P9-T01. The
ordinary-route guard therefore counts P9-T02 as completed and admits P9-T03.
P9-T02 was not executed, so that derived route cannot be followed. Correcting
the two additional task identities is outside generation 170's exact
one-field predecessor authority. No checkpoint was invoked.

## Scientific boundary

This is project-system lifecycle parity only. All six benchmark cases remain
`NOT_RUN`, Gate D remains `NOT_READY`, and Gate E remains
`NOT_READY_NO_BENCHMARK_CASE_EXECUTED`.

The repair adds no scientific evidence, ontology, source law, effective
geometry, Einstein equation, exact-GR recovery, benchmark result,
Distance-to-GR movement, promotion, proof, publication, push, or
completed-derivation authority.

## Next action

Run one fresh bounded `improve-project-system` recovery for
`repair_p9_recovery_task_plan_identity_and_ordinary_guard_parity_v1`. It must
reconcile only the implementation plan identities of `RT-20260730-002` and
`RT-20260730-003`, preserve the successful one-token status repair and all
P9-T01 science, restore an honest P9-T02 route, and run one future governed
checkpoint only after full validation passes.
