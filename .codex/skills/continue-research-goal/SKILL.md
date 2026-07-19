---
name: continue-research-goal
description: Launch one file-backed recursive relay that pursues an explicit The-AEther-Flow research goal through fresh bounded continue-research discussions; use only in the Codex desktop app with current task tools.
---

# Continue Research Goal

Use this skill only when the user explicitly requests a fresh-discussion
research relay and supplies the required goal:

```yaml
goal: <nonblank exact research objective>
reasoning_effort: <optional current task-tool reasoning value; default max>
scope:
  mode: single_objective | multi_step
  included_work_items: <exact immutable work-item list>
  dependency_source: <null or exact path and SHA-256>
  exclusions: <nonempty list>
  source_hashes: <path-to-SHA-256 map>
max_continue_passes: <optional positive integer; default null means unlimited>
deadline_at: <optional absolute timezone-aware timestamp; default null means unlimited>
max_elapsed_minutes: <optional positive integer compatibility alias for deadline_at>
```

`deadline_at` and `max_elapsed_minutes` are mutually exclusive. Normalize a
finite deadline to canonical UTC `Z` and reject an invalid, naive, or
non-future value. `--deadline-at` is the canonical CLI override;
`--max-elapsed-minutes` remains a supported compatibility alias.

This is a launcher, not a research worker. It creates one durable ignored goal
record, dispatches one fresh `continue-research-continue-goal` discussion, and
ends. It invokes `continue-research` zero times, invokes
`improve-project-system` zero times, and creates no native Codex goal.

`single_objective` is the default for one task-specific goal. `multi_step` is
lawful only when the exact original user goal explicitly includes every work
item and the dependency source. A task-specific goal may never be repurposed
for later work merely because scheduling budget remains.

## Authority and Runtime Sources

Read, in order:

1. `AGENTS.md`;
2. this skill;
3. `references/goal-file-schema.md`;
4. `.codex/skills/continue-research-continue-goal/SKILL.md`; and
5. `.codex/skills/continue-research/SKILL.md`.

The tracked skill and schema files are the complete runtime contract. An
implementation plan, task transcript, generated wiki note, or prior worker
summary is not runtime authority.

The goal record is orchestration state only. It cannot choose an AgentJob,
change tracked research-control state, prove scientific completion, weaken a
human gate, or promote any claim. `continue-research` remains the one-packet
research authority. `improve-project-system` remains the one-packet
project-system repair authority. A v4 generation route chooses between those
two existing skills without expanding either skill's authority.

## Repository Binding Profiles

Resolve exactly one requested profile before writing goal state. The
disposable acceptance profile remains:

```text
project root: /Volumes/P-SSD/AngryOwl/The-AEther-Flow-continue-goal-test
branch: codex/continue-research-goal-test
environment mode: local
execution profile: acceptance_test
```

The production profile is available only after explicit user authorization
for the exact relay goal and effective scheduling guards. It binds to:

```text
project root: /Volumes/P-SSD/AngryOwl/The-AEther-Flow
branch: the current main branch or a current branch whose name begins with codex/
environment mode: local
execution profile: production_profile
```

The production starting HEAD must be a clean validated checkpoint, the exact
root must resolve to one saved local Codex project, and the user must have
requested fresh recursive discussions for the supplied goal. Production
enablement does not authorize the launcher to create or switch branches, edit
tracked files, run research, push, merge, or relax any relay guard.

Derive and persist the resolved root, Git common directory, branch, starting
HEAD, saved-project identity, environment mode, and selected execution profile.
Do not hard-code either repository path in the state helper. For the acceptance
profile, reject a different root or branch and continue to reject `main`. For
the production profile, reject a different root and accept either `main` or a
branch under `codex/*`. Under both profiles reject a managed-per-step worktree,
an ambiguous saved project, or a non-local mode.

## Mandatory Pre-Launch Acceptance Loop

Before capability preflight or any state creation, maintain two in-memory
candidates: the exact understood goal and the selected reasoning effort.
Omission of `reasoning_effort` selects `max`. Then:

1. restate the complete understood goal without silently narrowing or
   broadening it;
2. display the separate exact line `reasoning_effort: "<value>"`;
3. request one combined confirmation of both the goal and reasoning effort;
4. treat only an unambiguous combined acceptance as confirmation;
5. when the user edits only the goal, preserve the previously selected
   reasoning effort; when the user edits only the effort, preserve the goal;
   when the user edits both simultaneously, replace both candidates;
6. after any goal or effort change, restart the loop and display both values
   again; and
7. treat ambiguous approval, partial approval, or silence as no acceptance and
   create no state.

Do not call `initialize`, reserve a successor, create a task, or write a goal
record until this loop has one unambiguous combined acceptance. The accepted
effort is immutable after initialization. A later effort change requires a new
goal launch.

## Required Capability Preflight

Before writing any goal state:

1. discover the current `list_projects`, `create_thread`, and `node_repl`
   contracts;
2. confirm that exactly one saved local project resolves to the selected
   profile root;
3. confirm that a fresh project task can be requested with local environment
   mode, an initial textual prompt, and explicit `thinking`;
4. inspect Git root, common directory, branch, HEAD, and porcelain status;
5. inspect `research_control/program_state.yaml`, the latest tracked handoff,
   relevant registries, and the current `continue_research.py` boundary;
6. build the canonical repository fingerprint defined by the schema;
7. confirm that `goals/goal-*.md`, locks, temporary files, recovery sidecars,
   and the global lease are ignored and untracked; and
8. confirm that no goal record or global relay lease authorizes another active
   conforming relay.

After combined acceptance and before `initialize`, read
`nodeRepl.requestMeta["x-codex-turn-metadata"]` from the current task. Require
nonblank `model` and `reasoning_effort` metadata. Confirm that:

- the accepted effort is a member of the current `create_thread.thinking`
  enum;
- the discovered `create_thread` contract lists that effort as supported by
  the active metadata model; and
- current-task `reasoning_effort` exactly equals the accepted effort.

Missing metadata, an unsupported effort, absent `thinking` support, or a
current-task mismatch stops before goal initialization. On mismatch, tell the
user to change the Codex UI reasoning setting and then restart the combined
acceptance loop. Never change global Codex configuration, send a message to
the current task itself, silently downgrade the effort, substitute another
model, or infer support from a different model.

If capability discovery or any repository identity is absent, ambiguous, or
incompatible, stop before goal creation. Do not substitute a fork, follow-up,
handoff, shell prompt injection, controller, hook, plugin, or App Server
client.

## Input, Scope, and Completion-Contract Gate

Preserve the user-supplied goal exactly after CRLF/CR-to-LF canonicalization;
do not trim, dedent, normalize Unicode, or add a terminal newline. Reject a
goal containing credentials, access tokens, private keys, or other secrets.

Derive a plain-language completion contract naming the canonical repository
evidence and validator/checkpoint conditions that would prove success. Also
derive one immutable `scope_contract`:

- `mode` is `single_objective` or `multi_step`;
- every included work item has a stable ID, exact objective, and in-scope
  dependency list;
- a structured `multi_step` goal names the exact dependency-source path and
  SHA-256;
- exclusions and every source hash are explicit; and
- `allow_scope_expansion` is exactly `false`.

Ask for clarification before writing state when an operational interpretation
would materially narrow, broaden, or rewrite the goal or when an asserted
multi-step scope is not explicit in the original user request. The original
goal, original completion contract, scope contract, scheduling guards, fixed
guards, and repository binding are immutable.

New records use `continue-research-goal.v4`. Omitted
`max_continue_passes` and `deadline_at` values are persisted independently as
JSON `null`; each `null` disables only its corresponding count or elapsed-time
stop. Continue recording `passes_consumed` even when the pass horizon is
unlimited. The helper retains byte-compatible read and validation behavior for
v1 through v3 records. It never migrates, rewrites, or automatically resumes
them.

Every v4 record contains one immutable, hash-bound `discussion_contract`
containing the accepted goal hash, accepted reasoning effort, and
`combined_goal_and_reasoning_effort_confirmed` confirmation marker. The
contract hash is initialization evidence and summary evidence. It is not
amendable.

Every v4 generation has one immutable route containing the worker skill,
reason and strategy identifiers, source generation, included work-item ID,
canonical blocker fingerprint, evidence hashes, and any exact dirty-state
manifest. The initial route is `continue-research`; later routes are approved
only by verified in-scope continuation or `record-recovery-required`.

“Unlimited” applies only to the scheduling horizon. It does not expand the
single bounded AgentJob permitted in each worker frame, weaken human gates,
bypass validation or checkpoint requirements, relax leases or repository
identity, permit concurrency, broaden the scope contract, repeat a consumed
generation, or repeat the same recovery strategy for the same blocker.

Fixed guards are:

```yaml
max_repeated_state_fingerprints: 1
max_live_continuations: 1
handoff_ready_timeout_seconds: 60
stop_on_human_gate: true
stop_on_validation_failure: true
stop_on_checkpoint_failure: true
stop_on_unexpected_dirty_state: true
stop_on_no_progress: true
stop_on_repeated_state: true
stop_on_capability_loss: true
stop_on_branch_or_repository_mismatch: true
```

For v4, a validation, checkpoint, dirty-state, no-progress, or repeated-state
finding does not itself force terminalization. The generation must first select
a distinct safe authorized recovery strategy when one exists. A non-success
terminal is lawful only when the user cancels, a finite guard is reached, or
canonical evidence proves that no safe authorized AI route remains and names
one exact human action.

## Deterministic State Helper

Use only the repository helper:

```text
.venv/bin/python .codex/skills/continue-research-goal/scripts/goal_state.py
```

Pass `--goals-dir .codex/skills/continue-research-goal/goals` and one explicit
subcommand. The helper provides exclusive initialization, schema/hash/journal
validation, compare-and-swap revisions, per-goal and worktree-global lease
parity, successor reservation, idempotent successor-ID recording, generation
claims, pre-execution consumption, receipt finalization, terminalization, and
explicit recovery. V4 additionally provides:

- `initialize --scope-contract-json --reasoning-effort`;
- `record-recovery-required --recovery-plan-json`;
- route-aware `reserve-successor`;
- worker-skill and exact repair-manifest checks in `consume` and `returned`;
- `reconcile-dispatch` for zero-or-one-child proof;
- mandatory `--human-intervention-json` on non-success terminal operations;
  and
- read-only `summarize`, which validates and aggregates finalized receipts and
  renders the terminal report.

It has no research, task-management, Git mutation, commit, or
scientific-evaluation authority.

Treat every helper conflict or validation error as fail-closed. Never hand-edit
a goal record or lease. Lease expiry is diagnostic and never authorizes
stealing. Every state-changing research or project-system worker frame consumes
one pass before invocation. A helper-only routing or dispatch-reconciliation
operation consumes no pass.

## Launcher Workflow

After combined acceptance and all preflight checks pass:

1. call helper `initialize` exactly once with the exact goal, completion
   contract, scope-contract JSON, required `--reasoning-effort`, optional
   scheduling guards, fixed guards, repository binding, and initial canonical
   fingerprint; the helper writes the accepted discussion contract and
   approved generation-1 `continue-research` route;
2. retain the returned absolute `goal_file`, `goal_id`, revision, and launcher
   lease evidence;
3. call helper `reserve-successor` once for generation 1, creating one random
   handoff token and deterministic idempotency key `<goal_id>:1`;
4. call
   `create_thread(..., thinking=<persisted discussion_contract reasoning_effort>)`
   exactly once against the uniquely resolved saved project in local mode with
   the prompt below; omit the `model` argument;
5. if a concrete thread ID returns, call helper `record-successor` only; this
   idempotent operation records the ID, moves to `successor_created`, and
   transfers both cooperative leases to the reserved successor token;
6. after that record succeeds, make no repository call, no additional helper
   call, and no orchestration call; immediately return the handoff summary and
   required created-task directive; and
7. leave both discussions and all ignored relay evidence unarchived.

The successor prompt must begin with and contain only the relay identity and
bounded contract:

```text
Use $continue-research-continue-goal.

This is one authorized frame of a user-requested recursive research relay.
goal_file: <exact absolute goal path>
goal_id: <goal-id>
expected_generation: 1
handoff_token: <unguessable token>
idempotency_key: <goal-id>:1

Wait for the handoff to reach successor_created, then atomically claim this
generation. Read and obey its immutable worker_skill route. Follow
$continue-research-continue-goal exactly. It authorizes one routed worker-skill
invocation and at most one successor discussion.
```

Do not duplicate the goal text in the prompt. The goal file is the continuation
token.

## Dispatch Failure

- On a definitive create failure or timeout, inspect task state once. Call
  `reconcile-dispatch` only when canonical evidence proves either that no child
  exists and task creation capability remains available, or that exactly one
  matching unclaimed child exists. The first case approves one new
  idempotent generation; the second records that one child.
- On duplicate matching children, unavailable capability, uncertain
  invocation, or unresolved ambiguity, record the mapped non-success terminal
  with exact human-intervention JSON. Quarantine leases where the schema
  requires it.
- On an ambiguous create result without zero-or-one-child proof, record
  `terminal_handoff_ambiguous`, quarantine both leases, and write the ignored
  dispatch-recovery sidecar if a returned ID could not be persisted.
- If a concrete thread ID was returned but record persistence fails, retry
  only the idempotent record-only operation for a short bounded count. Never
  call `create_thread` again for the same intent.

Preflight failures and global-lease losers create no goal file and no task.
Once initialization succeeds, terminal dispatch evidence remains retained; do
not delete it to make the attempt appear not to have happened.

## Stop Semantics and Reporting

“Stop” means that after confirmed dispatch is recorded, the launcher performs
no further repository, helper, task-management, or research action and ends
its current turn. A short scheduling overlap is permitted; the successor is
authorized only to poll until the handoff is recorded and its atomic claim
wins.

Report the goal path and ID, immutable goal hash, generation, successor task
ID, discussion-contract hash, accepted reasoning effort, scope-contract hash,
generation route hash, repository root/branch/HEAD, initial fingerprint,
helper revision, and launcher stop reason. Worker prose is telemetry only.

## Forbidden Actions

- Never call native goal operations (`create_goal`, `get_goal`, `update_goal`,
  `/goal`, or `thread/goal/*`).
- Never invoke `continue-research` from the launcher.
- Never invoke `improve-project-system` from the launcher.
- Never execute an AgentJob, author a Director decision, or evaluate a physics
  result from the launcher.
- Never create more than one initial successor or retry an ambiguous task
  creation.
- Never fork, continue, hand off, archive, delete, or steer a successor.
- Never treat a production `main` binding as authority to bypass any other
  relay guard, push, merge, rebase, open a pull request, install a plugin,
  create a hook/controller, clean up runtime evidence, or remove the
  branch/worktree.
- Never register, checkpoint, promote, or generate wiki artifacts from runtime
  goal files.
- Never omit, infer away, or broaden the immutable scope contract.
- Never omit `thinking`, rely on default inheritance, change global Codex
  configuration, self-message, silently downgrade reasoning effort, or pass a
  substitute `model`.
