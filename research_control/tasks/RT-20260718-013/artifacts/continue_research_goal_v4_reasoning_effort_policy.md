---
authority: control
object_id: "MD-CONTINUE-RESEARCH-GOAL-V4-REASONING-EFFORT-POLICY"
task_id: "RT-20260718-013"
schema_version: "continue-research-goal-v4-reasoning-effort-policy.v1"
status: "active"
owner_skill: "continue-research-goal"
scientific_claims_changed: false
distance_to_gr_delta_changed: false
---

# Confirmed and pinned relay reasoning-effort policy

## Authority and boundary

This policy records the bounded project-control change from
`continue-research-goal.v3` to `continue-research-goal.v4`. It adds
pre-launch goal-and-reasoning acceptance, current-task metadata verification,
an immutable discussion contract, and explicit reasoning-effort pinning for
every relay task.

The completed v3 transaction `RT-20260718-012`, its policy and validation
artifacts, retained v1-v3 goal records, ordinary research state, physics
sources, and scientific authority remain unchanged. This policy does not
launch a relay, resume a historical goal, modify Codex configuration, or
authorize push, publication, deployment, or any external mutation.

The executable contract remains split across:

- the `continue-research-goal` launcher skill;
- the `continue-research-continue-goal` recursive worker skill;
- the goal-record schema reference;
- the `goal_state.py` state helper; and
- focused goal-state and static contract tests.

## Combined pre-launch acceptance

The launcher keeps the understood goal and selected reasoning effort as
in-memory candidates. Omission of `reasoning_effort` selects `max`. Before any
goal state or task exists, the launcher:

1. restates the complete understood goal;
2. displays `reasoning_effort: "<value>"`;
3. requests one combined acceptance of both values; and
4. creates no state for ambiguous, partial, or absent approval.

A goal-only edit preserves the selected effort. An effort-only edit preserves
the goal. A simultaneous edit replaces both candidates. Every edit restarts
the combined acceptance loop. Once initialization occurs, the accepted effort
is immutable; changing it requires a new goal launch.

## Current-task verification

After combined acceptance and before initialization, the launcher rediscovers
the live task-tool contracts and reads the current task's actual `model` and
`reasoning_effort` metadata. It verifies all of the following:

- the selected value is in the current `create_thread.thinking` enum;
- the active model supports that value;
- the current task's reasoning metadata exactly matches the accepted value;
  and
- `create_thread` supports an explicit `thinking` argument.

Missing metadata, unsupported effort, absent `thinking` support, or mismatch
stops before initialization. The user must change the Codex UI reasoning
setting and reconfirm. The launcher never changes global Codex configuration,
self-messages, silently downgrades, or substitutes another model.

## Immutable discussion contract

Every new v4 record contains exactly:

```yaml
accepted_goal_sha256: "<goal_sha256>"
reasoning_effort: "<accepted task-tool value>"
confirmation_marker: "combined_goal_and_reasoning_effort_confirmed"
```

Canonical JSON hashing produces `discussion_contract_sha256`. Validation
requires the accepted goal hash to match `goal_sha256`, the effort to remain
in the task-tool enum, and the confirmation marker to be exact. Initialization
journal evidence and the generation-1 route both bind the contract hash.
Read-only summaries expose the contract, its hash, and the accepted effort.
There is no amendment path for the contract.

The helper CLI requires `initialize --reasoning-effort`; the launcher owns the
default-to-`max` behavior and active-model/current-task checks.

## Recursive task pinning

Before a v4 recursive worker claims a generation, it validates the record,
reads the persisted effort only from the discussion contract, rediscovers
current metadata and model support, and proves an exact match. Failure stops
before claim, worker execution, or helper mutation.

After one verified generation determines that a successor is required, the
worker rediscovers `create_thread` and rechecks metadata before successor
reservation. The launcher and every successor call:

`create_thread(..., thinking=<persisted discussion_contract reasoning_effort>)`

The `model` argument remains omitted. Default reasoning inheritance, silent
downgrade, model substitution, and global configuration mutation are
prohibited.

## Compatibility and failure behavior

The helper validates and summarizes `continue-research-goal.v1`, v2, and v3
records under their existing semantics. It does not migrate, rewrite, mutate,
claim, or automatically resume them. Only v4 records may enter mutation paths.

Unsupported reasoning values fail before file creation. A malformed,
goal-mismatched, rehashed, or journal-unbound discussion contract fails
validation. Missing task metadata or runtime tool support fails in the skill
workflow before state initialization, claim, worker execution, or successor
reservation.

## Acceptance evidence

This transaction is complete only when:

- focused tests cover the default and alternate efforts, required CLI input,
  serialization, summary output, retained v1-v3 compatibility, and tamper
  rejection;
- static tests cover goal-only, effort-only, and simultaneous edits,
  ambiguous approval, metadata mismatch, explicit `thinking`, model omission,
  and worker ordering;
- the task-local validator proves the v4 source contract and the unchanged
  `RT-20260718-012` task tree;
- repository unit, affected-profile, documentation-impact, research-control,
  memory, and diff gates pass; and
- the governed checkpoint commits this transaction without launching a relay
  or pushing the branch.

This is project-control evidence only and changes no physics claim or
Distance-to-GR status.
