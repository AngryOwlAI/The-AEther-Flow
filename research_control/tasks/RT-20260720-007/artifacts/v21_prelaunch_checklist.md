<!-- authority: control -->

# V21 P0-T04 prelaunch checklist

This checklist is a tracked planning artifact. It does not call the launcher,
reserve a successor, create a goal record, or override an active relay lease.

## Static contract checks completed by P0-T04

- [x] Goal text SHA-256 is `630b81e0f318cf85eb8ceb2ffbaf85f2148f68ee721c121d61f76b0ab393291a`.
- [x] Combined goal and reasoning-effort confirmation marker is present.
- [x] `reasoning_effort` is exactly `max`.
- [x] Scope mode is `multi_step`.
- [x] Included work-item count is 122 and dependency edge count is 183.
- [x] Work-item IDs, objectives, and dependencies equal the materialized backlog.
- [x] Dependency source is the registered v21 plan with SHA-256 `4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087`.
- [x] `allow_scope_expansion` is `false`.
- [x] `max_continue_passes` and `deadline_at` are JSON `null`.
- [x] Every fixed v4 stop guard is retained.
- [x] Production binding requires the exact project root, Git common directory, local mode, and `main` or `codex/*` branch.
- [x] Baseline evidence contains the exact immutable launch hash for all ten scope source paths.
- [x] P0-T03 baseline paths whose bytes differ from the immutable launch hash: `research_control/program_state.yaml`.
- [x] Runtime goal-file inventory was unchanged during artifact generation.

## Human and live-runtime checks required before any future submission

- [ ] Confirm the exact goal text and `reasoning_effort: "max"` together in one unambiguous response.
- [ ] Verify no active conforming goal or worktree-global relay lease exists.
- [ ] Rediscover `list_projects`, `create_thread`, and `node_repl`; verify the active model supports `max` and the current task is running at `max`.
- [ ] Verify exactly one saved local project resolves to `/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.
- [ ] Verify the production checkout is clean, locally bound, and on `main` or `codex/*` at the intended starting HEAD.
- [ ] Recompute every mutable source hash. If goal text, work items, dependencies, exclusions, or source hashes changed, regenerate this manifest instead of editing the contract by hand.
- [ ] Do not submit this packet while goal `crg-20260720T161354Z-96bc2664ce31bfe0` remains active; a duplicate live relay is forbidden.
- [ ] Do not push, merge, publish, promote a benchmark, bypass a human gate, or claim a completed derivation through launcher status.
