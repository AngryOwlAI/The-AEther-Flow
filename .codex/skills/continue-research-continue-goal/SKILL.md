---
name: continue-research-continue-goal
description: Execute or recover exactly one generation of a file-backed continue-research goal relay, then terminalize or dispatch at most one fresh successor discussion.
---

# Continue Research Continue Goal

Use this skill only for one explicitly identified frame of a goal relay created
by `continue-research-goal`, or for an explicit human-authorized recovery. A
normal frame claims one generation, consumes at-most-once authorization,
invokes `continue-research` exactly once, verifies canonical evidence, and
creates zero or one successor. A rejected or recovery frame invokes research
zero times.

## Normal Inputs

```yaml
goal_file: <exact absolute path under continue-research-goal/goals>
goal_id: <matching embedded goal id>
expected_generation: <positive integer>
handoff_token: <matching opaque token>
idempotency_key: <goal_id>:<expected_generation>
```

## Required Reading and Authority

Read `AGENTS.md`, `research_control/AGENTS.md`,
`.codex/skills/continue-research-goal/SKILL.md`, the tracked schema reference,
this skill, `.codex/skills/continue-research/SKILL.md`, and the named goal
record before acting.

The goal record is orchestration state, not scientific authority. Tracked
research-control files, registered canonical sources, registries, Git,
validators, and checkpoint evidence decide progress and completion. This skill
cannot preselect an AgentJob, expand a role, weaken a gate, or promote a claim.

## Entry Validation and Handoff Wait

1. Resolve the supplied path without following a goal-file symlink. It must be
   a direct regular child of the configured `goals/` directory and its
   filename must match the embedded goal ID.
2. Run helper `validate --require-lease-parity`; verify schema, exact goal and
   completion-contract hashes, amendments, journal chain, revision,
   repository binding, generation, token, and idempotency key.
3. Verify the immutable saved-project/root/Git-common-dir/branch/local-mode
   binding. The branch must not be `main`.
4. If the predecessor has not recorded `successor_created`, perform read-only
   polling for no more than `handoff_ready_timeout_seconds`. Do not touch
   tracked research state or claim the generation while waiting. On timeout,
   stop without mutation or research and report the idempotency key for
   explicit recovery.
5. Call helper `claim` exactly once with the expected revision and relay
   identity. A stale, duplicate, consumed, mismatched, or concurrently leased
   frame exits before research and appends no step receipt.

## Pre-Execution Gate

After a successful claim, directly reverify:

- the saved local project, worktree root, Git common directory, branch, HEAD,
  and allowed clean or exact authorized transaction state;
- `research_control/program_state.yaml`, the active task/AgentJob, latest
  handoff pair, and relevant registries;
- the current `continue_research.py` boundary;
- pass count, elapsed deadline, repetition state, and all fixed guards;
- matching per-goal and worktree-global leases; and
- absence of a possibly active predecessor or unexplained repository writer.

Map a pre-execution stop through the helper to one terminal state and one
zero-invocation receipt, then release both leases. Do not consume the
generation when any guard fails.

## One Research Invocation

For an execution-eligible frame:

1. call helper `consume` before research; this atomically sets
   `invocation_consumed=true`, records `invocation_state=authorized`, and
   increments `passes_consumed` exactly once;
2. invoke `$continue-research` exactly once and follow its complete current
   contract, including memory preflight, at most one outer AgentJob,
   validation, checkpoint, no-push, role, and human-gate rules;
3. after a directly observed return, record `returned` with direct execution
   evidence; if the call/return boundary is uncertain, record `unknown`,
   quarantine both leases, and stop for recovery; and
4. never rerun a generation whose invocation-consumed marker is true.

The returned assistant text is telemetry. Inspect the canonical repository
state directly after the invocation.

## Canonical Verification

Build the canonical timestamp-free fingerprint specified by the schema,
including worktree identity, branch, HEAD/status, program-state hash and
fields, active task and AgentJob, latest handoff pair and hashes, normalized
continuation boundary/reason, required validators, and checkpoint outcome.

Call helper `verify-step` once with the after fingerprint, canonical evidence,
and goal evaluation `met`, `unmet`, or `indeterminate`. The helper records
whether the fingerprint is new, unchanged, or repeats any prior state,
including an `A -> B -> A` cycle.

## Base Case and Protected Stops

Use `terminal_complete` only when every explicit completion criterion is
proved by canonical evidence and all required validators/checkpoint gates
pass. Finalize the generation's one receipt, release both leases, and create no
successor.

Create no successor and use the deterministic terminal mapping when any of the
following applies: human-gated authority; indeterminate evaluation; no action
or no authoritative progress; unchanged/repeated fingerprint; exhausted count
or deadline; validation/checkpoint/dirty-state failure; identity or branch
mismatch; corrupt schema/hash/journal/path; missing or conflicting leases;
interruption; task-capability loss; duplicate successor; or ambiguous dispatch.

Human-gated ontology adoption, canonical ontology edits, benchmark promotion,
Gate Chair authority, and equivalent protected decisions always stop the
relay.

## Recursive Case

Recursion is allowed only when the goal remains unmet, the fingerprint is new,
an authoritative transition or valid tracked next route exists, the repository
is clean at a valid checkpoint, validators and tracked control state agree,
`continue_research.py` permits another bounded pass, both leases match, task
creation remains available, and every guard permits another pass.

Then:

1. call helper `decide-step --decision continuation_required`;
2. call helper `reserve-successor` once for generation `N+1` under the same
   goal, creating one new token and idempotency key;
3. rediscover the exact saved project and current `create_thread` contract;
4. call `create_thread` exactly once in local mode with the same minimal prompt
   shape used by the launcher and the new generation identity;
5. record the returned ID with helper `record-successor`; this atomically
   finalizes generation `N`'s one receipt and transfers both leases;
6. make no further repository, helper, orchestration, or research call; and
7. end the current turn with the handoff summary and required created-task
   directive.

On definitive or ambiguous dispatch failure, finalize the same pending receipt
once with the mapped terminal outcome. Never retry an ambiguous create.

## Recovery Mode

Recovery is a separate zero-research invocation and requires:

```yaml
mode: recover
goal_file: <exact absolute path>
goal_id: <matching goal id>
requested_recovery: <adopt | resume | reconcile | amend_contract | amend_guards | cancel>
user_authorization: <exact instruction or approval reference>
```

Use direct task-lifecycle and canonical repository evidence to prove the prior
holder terminal before reconciling any lease. Begin `recovery_pending` only
from a recoverable terminal. An unconsumed abandoned generation receives one
zero-invocation receipt. A consumed generation is never rerun: reconcile it as
`1` only when one returned invocation is directly proven, otherwise as
`unknown`, then finalize exactly one receipt. Keep both leases quarantined
until terminal-holder proof and receipt finalization exist.

Contract and guard amendments are append-only, hash-linked, and preserve exact
authorization. They never rewrite the original goal, original contract,
original guards, repository binding, prior events, or prior receipts. A goal
change requires a new launcher record. Absorbing terminal states
(`terminal_complete`, `terminal_duplicate_detected`,
`terminal_corrupt_state`, and `terminal_cancelled`) cannot resume.

## Reporting

Report substantive research/control progress first, then the terminal or
recursive decision, canonical evidence, goal ID/path/hash, generation,
invocation count (`0`, `1`, or `unknown`), AgentJob/task/handoff/checkpoint,
before/after fingerprint, validator results, successor ID if any, and guard
status. Preserve uncertainties exactly.

## Forbidden Actions

- Never call native goal operations (`create_goal`, `get_goal`, `update_goal`,
  `/goal`, or `thread/goal/*`).
- Never invoke `continue-research` before a successful claim and consumption,
  more than once, during recovery, or for a consumed generation.
- Never execute more than the zero-or-one outer AgentJob authorized by
  `continue-research`.
- Never create more than one successor, reuse this discussion for another
  pass, send a follow-up to itself, fork, hand off, archive, or delete relay
  evidence.
- Never steal an expired lease, hand-edit goal state, accept worker prose as
  proof, bypass a validator/human gate, target `main`, push, merge, rebase,
  open a pull request, install a plugin/controller/hook, or clean up the
  worktree or runtime record.
