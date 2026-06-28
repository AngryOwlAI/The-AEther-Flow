<!-- authority: control -->

# Active-State Authority Invariant

## Purpose

This artifact defines the P1-T01 active-state source-of-truth invariant for the
v11 implementation plan. It is project-control guidance only. It does not
change scientific claim status and does not repair `research_control/current_frontier.md`.

## Invariant

The repository active state is valid only when the following precedence order is
respected:

1. `research_control/program_state.yaml` is the compact live state pointer.
2. The latest handoff named by `program_state.yaml` is the immediate routing
   authority.
3. `registries/DISTANCE_TO_GR_LEDGER.csv` is the persistent burden-state
   ledger for Distance-to-GR status.
4. Task records, Director decisions, AgentJob records, completions, claim
   boundaries, and role-execution rows under `research_control/tasks/` and
   `registries/` provide transaction provenance.
5. `research_control/current_frontier.md` is a generated or synchronized
   reader-facing control snapshot. It is not independent routing authority and
   must not contradict items 1 through 4.
6. Generated wiki notes, generated graph artifacts, PDFs, HTML, local Obsidian
   notes, semantic extracts, SQLite retrieval indexes, `.local/` caches, and
   commit status are retrieval or reader layers only.

## Selected Path

Selected path: **Path A: Generated snapshot**.

Reasoning: a deterministic frontier renderer is feasible because the required
inputs already exist as tracked machine-readable files:

- `research_control/program_state.yaml`
- the latest handoff pair under `research_control/handoffs/`
- active task `00_TASK.yaml`
- completion records under `research_control/tasks/*/jobs/completions/`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- claim-boundary and role-execution registries

The target policy is therefore:

- P1-T02 performs the immediate synchronization of `current_frontier.md` with
  live tracked state.
- P1-T03 installs a deterministic validator guard that rejects or emits a
  blocking repair signal for drift.
- P1-T04 adds a deterministic `render_current_frontier.py` command so future
  updates can be generated and checked rather than hand-maintained.

## Current-Frontier Policy

`research_control/current_frontier.md` must be treated as a synchronized
snapshot of authority, not authority itself. Any contradiction is resolved in
favor of `program_state.yaml`, the handoff named by that file, and the
Distance-to-GR ledger.

After P1-T04, `current_frontier.md` should be rendered from tracked state. Until
that command exists, any manual synchronization must state the source files used
and must pass the future P1-T03 equivalence checks.

## Required Drift Checks

A drift guard must fail or emit a blocking repair signal when any of these
conditions is true:

1. `current_frontier.md` active task ID differs from
   `program_state.yaml.active_task_id`.
2. `current_frontier.md` latest handoff ID differs from
   `program_state.yaml.latest_handoff_id`.
3. `current_frontier.md` current status differs from
   `program_state.yaml.current_status`.
4. `current_frontier.md` next recommended action omits or contradicts
   `program_state.yaml.next_recommended_action` or the latest handoff
   `next_action`.
5. The handoff named by `program_state.yaml.latest_handoff_id` is missing or
   does not identify the active task/job boundary.
6. The active task folder named by `program_state.yaml.active_task_id` is
   missing or lacks `00_TASK.yaml`.
7. `current_frontier.md` target milestone or burden language contradicts the
   relevant Distance-to-GR ledger row.
8. `current_frontier.md` permits a blocked claim that the active handoff,
   current task, claim-boundary registry, or Distance-to-GR ledger blocks.
9. `current_frontier.md` presents generated graph, checker, metrics, registry,
   wiki, PDF, HTML, local cache, or commit state as scientific proof or routing
   authority.
10. `current_frontier.md` references a required human Gate Chair authority that
    is not the authority named by live handoff state.

The validator output should name the mismatched field, the authoritative value,
the snapshot value, the authoritative source path, the snapshot path, and the
repair route.

## Repair Route

The current live defect is:

- authoritative live state: `RT-20260614-283` and `handoff-0316`;
- stale snapshot state: `RT-20260614-184` and `handoff-0218`.

The logical next packet is P1-T02, one bounded synchronization of
`research_control/current_frontier.md` with live tracked state. P1-T03 and
P1-T04 remain required after that synchronization.

## Forbidden Overread

This invariant does not authorize:

- canonical ontology edit;
- source-law adoption;
- `MetricData(E)` adoption;
- `g_eff` adoption or scope expansion;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor;
- matter action;
- detector semantics;
- Einstein equations;
- exact-GR benchmark promotion;
- benchmark Gate Chair closure;
- completed derivation; or
- treating `current_frontier.md`, validators, generated graph artifacts,
  checker output, metrics, generated derivatives, local caches, registries,
  handoffs, approvals, or commits as scientific proof.

## Source Materials

The AEther-Flow Research Project. (2026). *Current research frontier* [Internal
control snapshot].

The AEther-Flow Research Project. (2026, June 28). *Handoff 0316* [Internal
control handoff].

The AEther-Flow Research Project. (2026, June 28). *Recommendations
implementation plan continue task v11* [Internal implementation plan].
