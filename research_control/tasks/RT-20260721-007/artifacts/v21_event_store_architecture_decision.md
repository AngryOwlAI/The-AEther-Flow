---
authority: control
task_id: RT-20260721-007
plan_task_id: P10-T05
status: design_selected_not_activated
---

# V21 project-control event-store architecture decision

## Decision

Select `hybrid_tracked_jsonl_plus_generated_sqlite` as the architecture to test in a future, separately authorized pilot. After an explicit future cutover, canonical **project-control events** would be stored as append-only, canonicalized JSON Lines in tracked, hash-addressed segments. SQLite would remain a reproducible, untracked `.local/` query index. CSV, JSON, and Markdown surfaces would remain deterministic generated views.

This packet is design-only. It does not create an event-store directory, migrate a record, begin dual writing, run the P10-T06 pilot, or change any current authority. Existing tracked task files, handoffs, decisions, completions, and registries remain authoritative for project control unless a later cutover decision says otherwise.

## Alternatives considered

| Option | Review and history | Query behavior | Transaction behavior | Decision |
| --- | --- | --- | --- | --- |
| Tracked JSONL only | Strong Git diffs and portable history | Replay or rebuild for joins | Requires an explicit multi-file protocol | Not selected alone because repeated operational joins need a query index. |
| SQLite only | Binary history and merges are difficult to review | Strong indexed queries | Strong local database transactions | Rejected as the canonical tracked format because historical readability, merges, and authority inspection are weak. |
| Tracked JSONL plus generated SQLite | Reviewable append-only history | Fast disposable queries plus flat compatibility views | Single-writer JSONL transaction with deterministic rebuild | Selected for a future pilot because it preserves inspectability while isolating query acceleration from authority. |

## Selection rationale

The hybrid makes the authority boundary visible in the storage boundary. A tracked JSONL record can be reviewed, hashed, pinned to a Git revision, and replayed without a database runtime. A SQLite index can be removed and rebuilt without loss. Existing CSV and Markdown consumers can migrate one view at a time and demonstrate field-level parity before any read cutover.

The cost is stricter machinery: canonical serialization, deterministic identity, one-writer compare-and-swap, chain and manifest validation, and a receipt binding every view to the same committed event head. Those obligations are included in the schema and generated-view contracts rather than deferred as implementation details.

## Authority boundary

The proposed store is limited to project-control facts: task, decision, agent-job, candidate-history, claim-boundary, validation, authority, and handoff events. An event may point to a registered scientific object by exact object ID, path, hash, and authority status. It cannot replace that source or strengthen its meaning.

Registered TeX remains canonical for scientific and derivational claims. Gate Chair artifacts retain protected adoption, rejection, ontology, benchmark, and promotion authority. Generated CSV, Markdown, JSON, dashboards, theorem inventories, and SQLite indexes are never independent authority. Validator success is not scientific proof.

## Transaction and concurrency decision

A future write transaction must hold one repository-common-directory lock, compare the expected manifest head, append a deterministic segment, rebuild all affected views, pass parity and authority checks, and create one Git checkpoint containing events, manifest, views, and receipts. Readers pin one Git revision and manifest hash. A failed worktree is not an authoritative transaction.

Competing branches may propose logical events, but integration assigns sequence and chain identity under the single writer. Raw segment merges are forbidden. A stale lock cannot be broken because it is old; recovery needs recorded owner evidence and a compare-and-swap against the committed head.

## Migration posture

P10-T06 is dependency-ready to pilot one read-compatible slice under a fresh AgentJob. Historical backfill, dual-read parity, writer activation, reader cutover, or retirement of legacy write paths each require later explicit authorization and receipts. The current P10-T05 packet performs none of them.

## Decision result

The target architecture is selected, specified, and testable. Activation remains false, the existing registries remain current project-control authority, registered science authority is unchanged, and no Distance-to-GR burden is discharged.
