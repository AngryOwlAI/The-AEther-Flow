---
name: continue-research-continue-goal
description: Execute or recover exactly one routed generation of a file-backed continue-research goal relay, then terminalize or dispatch at most one fresh successor discussion.
---

# Continue Research Continue Goal

Use this skill only for one explicitly identified frame of a goal relay created
by `continue-research-goal`, or for an explicit human-authorized recovery. A
normal frame claims one generation, consumes at-most-once authorization,
invokes exactly the immutable route's `continue-research` or
`improve-project-system` worker skill, verifies canonical evidence, and creates
zero or one successor. A rejected or helper-only recovery frame invokes both
worker skills zero times.

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
cannot preselect an AgentJob, expand a role, weaken a gate, promote a claim, or
broaden the immutable scope contract. `continue-research` owns research
packets; `improve-project-system` owns project-system repair packets.

## Entry Validation and Handoff Wait

1. Resolve the supplied path without following a goal-file symlink. It must be
   a direct regular child of the configured `goals/` directory and its
   filename must match the embedded goal ID.
2. Run helper `validate --require-lease-parity`; verify schema, exact goal and
   completion-contract and scope-contract hashes, amendments, journal and
   recovery-ledger chains, revision, repository binding, immutable generation
   route, token, and idempotency key. V1/v2 records are validation-only and
   must not be claimed or resumed.
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
6. Read the claimed generation's `worker_skill`, strategy, work-item ID,
   blocker fingerprint, evidence hashes, and dirty-state manifest directly
   from the validated record. Do not accept a worker route from task prose.

## Pre-Execution Gate

After a successful claim, directly reverify:

- the saved local project, worktree root, Git common directory, branch, HEAD,
  and allowed clean state or the route's byte-equal dirty-state manifest;
- `research_control/program_state.yaml`, the active task/AgentJob, latest
  handoff pair, and relevant registries;
- the current `continue_research.py` boundary;
- the pass count against `max_continue_passes` only when that guard is finite,
  the current time against `deadline_at` only when that guard is finite,
  repetition state, and all fixed guards;
- matching per-goal and worktree-global leases; and
- absence of a possibly active predecessor or unexplained repository writer.

When a pre-execution finding has a distinct safe authorized recovery route,
call `record-recovery-required --recovery-plan-json` before consumption. It
records one zero-invocation work result, appends the one-shot strategy to the
recovery ledger, and approves the next immutable route. Use a non-success
terminal only when a finite guard is reached, cancellation is explicit, or
canonical evidence proves no safe authorized route remains; include mandatory
human-intervention JSON and release or quarantine leases as required. Do not
consume the generation when any pre-execution guard fails.

A JSON `null` pass limit or deadline means unlimited only for that scheduling
dimension. Continue incrementing `passes_consumed` for every authorized
research or project-system invocation. Unlimited scheduling does not expand
the per-frame AgentJob
boundary, weaken human gates or no-progress detection, bypass validators,
leases, identity checks, or concurrency limits, or override any other stop.

## One Routed Worker Invocation

When routed to research, invoke `$continue-research` exactly once. Every normal
frame creates zero or one successor.

For an execution-eligible frame:

1. call helper `consume --worker-skill <immutable route value>` before work;
   for a project-system repair route, also pass the directly reobserved exact
   dirty-state manifest; this atomically sets
   `invocation_consumed=true`, records `invocation_state=authorized`, and
   increments `passes_consumed` exactly once;
2. when `worker_skill=continue-research`, invoke `$continue-research` exactly
   once and follow its complete current contract; when
   `worker_skill=improve-project-system`, invoke `$improve-project-system`
   exactly once and follow its complete current contract; either route may
   execute at most one outer AgentJob and may not cross its authority boundary;
3. after a directly observed return, record `returned` with the same worker
   skill, exact repair manifest when applicable, and direct execution evidence;
   if the call/return boundary is uncertain, record `unknown`, mandatory human
   intervention, quarantine both leases, and stop for recovery; and
4. never rerun a generation whose invocation-consumed marker is true.

The returned assistant text is telemetry. Inspect the canonical repository
state directly after the invocation.

## Canonical Verification

Build the canonical timestamp-free fingerprint specified by the schema,
including worktree identity, branch, HEAD/status, program-state hash and
fields, active task and AgentJob, latest handoff pair and hashes, normalized
continuation boundary/reason, required validators, and checkpoint outcome.

Call helper `verify-step` once with the after fingerprint, canonical evidence,
goal evaluation `met`, `unmet`, or `indeterminate`, and the standardized v3
`work_result`: included work-item ID and status, task and AgentJob IDs,
completion path/hash, checkpoint commit, validator results, progress summary,
explicit zero-AgentJob reason when applicable, and out-of-scope remaining
work. The helper records whether the fingerprint is new, unchanged, or repeats
any prior state, including an `A -> B -> A` cycle.

## Base Case and Protected Stops

Use `terminal_complete` only when every explicit completion criterion is
proved by canonical evidence and all required validators/checkpoint gates
pass. Finalize the generation's one receipt, atomically store the deterministic
completion summary, release both leases, create no successor, call read-only
`summarize`, and render its report beginning `Goal reached.` and ending `That
goal was reached.`

An unchanged/repeated fingerprint, no progress, missing datum, indeterminate
result, validation/checkpoint/generated-derivative failure, or attributable
dirty state requires a materially different safe strategy when one exists:
theoretical selection, source acquisition, bounded calculation, candidate
construction, refutation, ontology-law packet, tracked task-local research
repair, or governed project-system repair. Call
`record-recovery-required`; never rerun the same
`(blocker_fingerprint, strategy_id)` pair.

A human-gated work item in a `multi_step` goal may be recorded as
`deferred_human_gate` while a dependency-independent included work item
remains. Terminalize at a protected gate only when every remaining required
item depends on protected human action.

Create no successor and use the deterministic non-success terminal mapping only
for an explicit cancellation, reached finite guard, corrupt or mismatched
identity/lease state, unresolved duplicate or ambiguous dispatch, protected
authority/credential/publication/scope requirement, uncertain consumed
invocation, or evidence-backed exhaustion of every safe authorized strategy.
Every such terminal stores mandatory human-intervention JSON, and `summarize`
must render a report beginning `Goal not reached — human action required`.

Human-gated ontology adoption, canonical ontology edits, benchmark promotion,
Gate Chair authority, credentials, push/publication, goal expansion, branch or
repository change, corrupt state, lease ambiguity, and uncertain consumed
invocations are never improvised.

## Recursive Case

Ordinary recursion is allowed when the goal remains unmet, the fingerprint is
new, an authoritative in-scope transition exists, the current route's
transaction is at a valid checkpoint, validators and tracked control state
agree, both leases match, task creation remains available, and every guard
permits another pass. For `multi_step`, the next work-item ID must be included
in the immutable scope and all of its declared dependencies must be completed;
`cross_task_relay_reuse: false` forbids repurposing a task-specific goal, not
movement among work items explicitly initialized in one multi-step goal.

Recovery recursion is allowed from `recovery_required` after the helper has
approved one distinct route. A project-system repair must use the exact dirty
manifest; any unexplained HEAD, porcelain, path-hash, owner, or failed-gate
difference requires human intervention.

Then:

1. for ordinary progress, call helper
   `decide-step --decision continuation_required` with the next included
   work-item ID when it changes; for a recovery, use the already-recorded
   `recovery_required` state;
2. call helper `reserve-successor` once for generation `N+1` under the same
   goal; it copies the already-approved route and creates one new token and
   idempotency key;
3. rediscover the exact saved project and current `create_thread` contract;
4. call `create_thread` exactly once in local mode with the same minimal prompt
   shape used by the launcher and the new generation identity;
5. record the returned ID with helper `record-successor`; this atomically
   finalizes generation `N`'s one receipt and transfers both leases;
6. make no further repository, helper, orchestration, or worker call; and
7. end the current turn with the handoff summary and required created-task
   directive.

On definitive failure or timeout, inspect task state once and call
`reconcile-dispatch` only with proof of zero children or exactly one matching
unclaimed child. Never retry an ambiguous create. Duplicate or unresolved
results use the mapped human-required terminal and finalize the same pending
receipt once.

## Recovery Mode

Explicit human recovery is a separate zero-worker invocation and requires:

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

For v3 records, a scheduling-guard amendment may only raise a finite limit or
replace a finite limit with JSON `null`. It may never replace an unlimited
guard with a finite value or append a no-op unlimited value. Finite amended
deadlines are normalized to canonical UTC `Z`. Retained v1/v2 records are
validation-only and cannot be resumed or mutated.

## Reporting

Report substantive research/control progress first, then the terminal or
recursive decision, canonical evidence, goal ID/path/hash, generation,
worker skill and route hash, invocation count (`0`, `1`, or `unknown`),
AgentJob/task/completion/handoff/checkpoint, before/after fingerprint,
validator results, successor ID if any, guard status, and recovery-ledger
strategy when applicable. For terminals, use helper `summarize` and preserve
its unmistakable reader report exactly. Preserve uncertainties exactly.

## Forbidden Actions

- Never call native goal operations (`create_goal`, `get_goal`, `update_goal`,
  `/goal`, or `thread/goal/*`).
- Never invoke either worker skill before a successful claim and consumption,
  more than once, during helper-only recovery, with a route mismatch, or for a
  consumed generation.
- Never execute more than the zero-or-one outer AgentJob authorized by
  `continue-research`.
- Never create more than one successor, reuse this discussion for another
  pass, send a follow-up to itself, fork, hand off, archive, or delete relay
  evidence.
- Never steal an expired lease, hand-edit goal state, accept worker prose as
  proof, bypass a validator/human gate, target `main`, push, merge, rebase,
  open a pull request, install a plugin/controller/hook, or clean up the
  worktree or runtime record.
- Never repeat a recovery strategy for the same blocker, broaden the scope
  contract, cross into an unlisted task, or execute a repair after any
  dirty-manifest field differs.
