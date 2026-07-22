---
authority: control
task_id: RT-20260721-007
plan_task_id: P10-T05
status: design_only
---

# V21 generated-view contract

## Purpose

The proposed event store preserves current readers through deterministic projections. A view is a reproducible representation of a validated, manifest-ordered project-control event prefix. It is not an independent source of project-control or scientific authority.

P10-T05 defines these projections only. Existing files remain authoritative under their current rules; no renderer is changed and no view is cut over here.

## Required projections

| View | Target | Stable order | Authority |
| --- | --- | --- | --- |
| Research task registry | `registries/RESEARCH_TASK_REGISTRY.csv` | `task_id` | generated after future cutover; never science authority |
| Director decision registry | `registries/DIRECTOR_DECISION_REGISTRY.csv` | `decision_id` | generated after future cutover |
| Agent job registry | `registries/AGENT_JOB_REGISTRY.csv` | `job_id` | generated after future cutover |
| Claim-boundary registry | `registries/CLAIM_BOUNDARY_REGISTRY.csv` | `claim_boundary_id` | generated after future cutover |
| Current frontier | `research_control/current_frontier.md` | replay sequence | generated summary |
| Task index | `research_control/tasks/TASK_INDEX.csv` and `.md` | `task_id` | generated index |
| Frontier theorem inventory | `research_control/design/frontier_theorem_inventory.md` | registered science object ID | reference projection only; registered TeX remains authority |
| Operational dashboard | `output/project_control_event_metrics.json` | `metric_id` | operational derivative |
| SQLite query index | `.local/research_control/project_control_events.sqlite3` | replay sequence and indexed keys | disposable untracked cache |

## Replay and reduction

The renderer reads one manifest at one pinned Git revision, verifies every segment hash, event hash, sequence, prior hash, schema, source reference, and authority field, then folds events using a versioned reducer for each domain. Corrections act only through explicit supersession references. Unknown input fails closed.

The same manifest hash and renderer version must yield byte-identical tracked output. Rows use declared column order and stable key ordering. Markdown uses stable headings and list order. JSON uses canonical key order. No wall-clock generation timestamp is written into content; a source-derived effective timestamp may appear where the compatibility schema requires it.

## Receipts

Each build emits or updates a receipt with:

- manifest hash and last sequence;
- renderer path and exact hash;
- reducer/schema versions;
- input event and subject counts;
- output path, row count, and SHA-256;
- unknown, rejected, and unmapped field counts;
- parity result against the still-authoritative legacy surface during migration.

A consumer accepts a view only when the receipt, view, manifest, and Git revision belong to the same checkpoint transaction.

## Read compatibility and parity

Before cutover, a shadow renderer compares generated output with the authoritative legacy surface using an explicit field allowlist. Every legacy field must be mapped, declared intentionally absent, or declared outside the pilot slice. Differences are machine-readable and fail the pilot. Semantic approximation, normalized prose equality, or silent field dropping is insufficient.

P10-T06 may choose one bounded slice under a fresh AgentJob. That pilot may generate shadow outputs under task-local or `.local/` paths, but it cannot replace a current registry or activate an event writer.

## Failure behavior

Sequence gaps, conflicting event IDs, hash drift, missing sources, unknown schema, ambiguous reduction, non-deterministic bytes, receipt mismatch, or authority violations stop publication of replacement views. Existing tracked sources remain readable and authoritative. A partially rendered file is diagnostic worktree state, not a valid view.

## Scientific boundary

The theorem inventory and dashboards may expose identifiers, statuses, burden labels, and exact source references. A generated view is not scientific proof. It may not derive a scientific status, reinterpret a theorem, adopt a candidate, alter Distance-to-GR, or replace the registered TeX and Gate Chair artifacts that control those claims.
