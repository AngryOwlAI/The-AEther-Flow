---
name: continue-research-goal
description: Launch one file-backed recursive relay that pursues an explicit The-AEther-Flow research goal through fresh bounded continue-research discussions; use only in the Codex desktop app with current task tools.
---

# Continue Research Goal

Use this skill only when the user explicitly requests a fresh-discussion
research relay and supplies all required inputs:

```yaml
goal: <nonblank exact research objective>
max_continue_passes: <positive integer>
max_elapsed_minutes: <positive integer>
```

This is a launcher, not a research worker. It creates one durable ignored goal
record, dispatches one fresh `continue-research-continue-goal` discussion, and
ends. It invokes `continue-research` zero times and creates no native Codex
goal.

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
human gate, or promote any claim. `continue-research` remains the only
one-packet research authority.

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
for the exact relay goal and guards. It binds to:

```text
project root: /Volumes/P-SSD/AngryOwl/The-AEther-Flow
branch: the current non-main branch whose name begins with codex/
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
profile, reject a different root or branch. For the production profile, reject
a different root or a branch outside `codex/*`. Under both profiles reject
`main`, a managed-per-step worktree, an ambiguous saved project, or a non-local
mode.

## Required Capability Preflight

Before writing any goal state:

1. discover the current `list_projects` and `create_thread` tool contracts;
2. confirm that exactly one saved local project resolves to the selected
   profile root;
3. confirm that a fresh project task can be requested with local environment
   mode and an initial textual prompt;
4. inspect Git root, common directory, branch, HEAD, and porcelain status;
5. inspect `research_control/program_state.yaml`, the latest tracked handoff,
   relevant registries, and the current `continue_research.py` boundary;
6. build the canonical repository fingerprint defined by the schema;
7. confirm that `goals/goal-*.md`, locks, temporary files, recovery sidecars,
   and the global lease are ignored and untracked; and
8. confirm that no goal record or global relay lease authorizes another active
   conforming relay.

If capability discovery or any repository identity is absent, ambiguous, or
incompatible, stop before goal creation. Do not substitute a fork, follow-up,
handoff, shell prompt injection, controller, hook, plugin, or App Server
client.

## Input and Completion-Contract Gate

Preserve the user-supplied goal exactly after CRLF/CR-to-LF canonicalization;
do not trim, dedent, normalize Unicode, or add a terminal newline. Reject a
goal containing credentials, access tokens, private keys, or other secrets.

Derive a plain-language completion contract naming the canonical repository
evidence and validator/checkpoint conditions that would prove success. Ask for
clarification before writing state only when an operational interpretation
would materially narrow, broaden, or rewrite the goal. The original goal,
original completion contract, guards, and repository binding are immutable.

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
explicit recovery. It has no research, task-management, Git mutation, commit,
or scientific-evaluation authority.

Treat every helper conflict or validation error as fail-closed. Never hand-edit
a goal record or lease. Lease expiry is diagnostic and never authorizes
stealing.

## Launcher Workflow

After all preflight checks pass:

1. call helper `initialize` exactly once with the exact goal, completion
   contract, guards, repository binding, and initial canonical fingerprint;
2. retain the returned absolute `goal_file`, `goal_id`, revision, and launcher
   lease evidence;
3. call helper `reserve-successor` once for generation 1, creating one random
   handoff token and deterministic idempotency key `<goal_id>:1`;
4. call `create_thread` exactly once against the uniquely resolved saved
   project in local mode with the prompt below;
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
generation. Follow $continue-research-continue-goal exactly. It authorizes one
$continue-research invocation and at most one successor discussion.
```

Do not duplicate the goal text in the prompt. The goal file is the continuation
token.

## Dispatch Failure

- On a definitive create failure, record `terminal_failed`, release both
  leases, and stop.
- On an ambiguous create result, record `terminal_handoff_ambiguous`,
  quarantine both leases, write the ignored dispatch-recovery sidecar if a
  returned ID could not be persisted, and stop for explicit recovery.
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
ID, repository root/branch/HEAD, initial fingerprint, helper revision, and
launcher stop reason. Worker prose is telemetry only.

## Forbidden Actions

- Never call native goal operations (`create_goal`, `get_goal`, `update_goal`,
  `/goal`, or `thread/goal/*`).
- Never invoke `continue-research` from the launcher.
- Never execute an AgentJob, author a Director decision, or evaluate a physics
  result from the launcher.
- Never create more than one initial successor or retry an ambiguous task
  creation.
- Never fork, continue, hand off, archive, delete, or steer a successor.
- Never target `main`, push, merge, rebase, open a pull request, install a
  plugin, create a hook/controller, clean up runtime evidence, or remove the
  branch/worktree.
- Never register, checkpoint, promote, or generate wiki artifacts from runtime
  goal files.
