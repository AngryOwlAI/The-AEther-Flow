<!-- authority: control -->

# Handoff handoff-0912 — P9 recovery-task plan identity parity

Status: `blocked_validation`.

`handoff-0912` records the bounded generation-171 Process Integrity Auditor
recovery.

## Result

Exactly two task-control fields change. The `implementation_plan.plan_task_id`
in `RT-20260730-002` and `RT-20260730-003` now reads `P9-T01`, matching each
record's explicit `recovery_for_plan_task_id`. Reversing either substitution
reproduces its exact sealed preimage.

The corrected task identities no longer count P9-T02 as completed.
`handoff-0911` now derives the ready science set `[P9-T02, P14-T04]` and
selects P9-T02. The ordinary-route guard itself, its tests, and its policy are
unchanged.

The successful predecessor lifecycle-status repair, the protected P9-T01
completion and protocol, `handoff-0908`, `handoff-0909`, and checkpoint
`14a82f7` remain unchanged. P9-T01 was not replayed and P9-T02 remains
unexecuted.

## Pre-checkpoint blocker

The complete repository test shard finds one pre-existing explicit taxonomy
error in `RT-20260729-012`. Its
`task_taxonomy.candidate_family` is
`SourceDerivedBenchmarkProtocol_v1`, while the executable contract requires a
bounded lowercase slug. The source task, taxonomy validator, policy, and test
are unchanged from `HEAD`; changing that task is outside generation 171's
immutable write scope.

The exact generation-171 repair passes its task-local checks and the hard
research-control diff. No checkpoint was invoked after the repository-wide
gate failed.

## Scientific boundary

This is project-system identity parity only. All six benchmark cases remain
`NOT_RUN`, Gate D remains `NOT_READY`, and Gate E remains
`NOT_READY_NO_BENCHMARK_CASE_EXECUTED`.

The repair adds no scientific evidence, ontology, source law, effective
geometry, Einstein equation, exact-GR recovery, benchmark result,
Distance-to-GR movement, promotion, proof, publication, push, or
completed-derivation authority.

## Next action

Run one fresh bounded `improve-project-system` recovery for
`repair_p9_t01_benchmark_protocol_task_taxonomy_candidate_family_slug_v1`.
Change only the candidate-family scalar to
`source_derived_benchmark_protocol_v1`, prove every other source-task byte and
all generation-171 repairs remain exact, rerun the complete validation stack,
and invoke one future cumulative checkpoint only after every gate passes.
P9-T02 remains unexecuted until that checkpoint commits.
