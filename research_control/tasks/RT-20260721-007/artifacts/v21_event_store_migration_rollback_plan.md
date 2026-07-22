---
authority: control
task_id: RT-20260721-007
plan_task_id: P10-T05
status: design_only
---

# V21 event-store migration and rollback plan

## Current state

The selected hybrid architecture is inactive. Existing tracked control sources and registries are the current project-control authority. No event-store segment, manifest, SQLite index, backfill, dual-write path, or reader cutover is created by P10-T05.

## Migration phases

| Phase | Purpose | Entry evidence | Exit evidence | Current status |
| --- | --- | --- | --- | --- |
| 0. Design | Fix storage, identity, authority, view, transaction, and rollback contracts. | P10-T03 and P10-T04 finalized. | P10-T05 contract and focused validation pass. | Completed by this packet. |
| 1. Bounded shadow pilot | Model one read-compatible project-control slice without replacing any source. | Fresh P10-T06 AgentJob with exact slice and paths. | Byte-level deterministic replay, source-link checks, and field parity receipt. | Not executed. |
| 2. Historical backfill and dual read | Import legacy records as source-linked events while legacy sources remain authoritative. | Separate authorization naming scope, ordering, identities, and privacy checks. | Complete source coverage and repeatable event head. | Not authorized. |
| 3. Compatibility projection parity | Rebuild selected legacy views and compare all mapped fields. | Stable backfill head and versioned reducers. | Repeated clean-build parity at pinned revisions. | Not authorized. |
| 4. Reader and writer cutover | Make event writes authoritative for explicitly named project-control domains. | Explicit cutover authority naming revision, readers, writers, receipts, and rollback point. | Post-cutover validation and monitored checkpoint. | Not authorized. |
| 5. Legacy retention | Freeze old write paths while retaining historical readability. | Successful cutover and retention decision. | Legacy sources remain available through Git without SQLite. | Not authorized. |

No phase advances because a prior phase merely passed. Each needs its own bounded task and authority record.

## Historical import rules

Backfill never edits a legacy source. It emits new imported events ordered by a declared deterministic key, each with the original object ID or control ID, path, exact source hash, and authority status. Missing history is recorded as an explicit absence; it is not reconstructed from plausibility. Conflicts stop the import and produce a report.

An imported event describes the project-control fact supported by its source. It cannot upgrade candidate, theorem, ontology, benchmark, or derivation status. Original Git history remains the audit fallback.

## Transaction plan

One writer holds a lock in the repository common directory and compares the expected manifest sequence and hash. It stages events, recomputes the chain and manifest, renders views, validates source links and parity, and produces one Git checkpoint containing the complete transaction. Readers pin that checkpoint and manifest hash.

No consumer may observe a new event head with old views or new views with an old receipt. Worktree state, a local SQLite transaction, or a validator success without the Git checkpoint is not authoritative completion.

## Rollback

Before cutover, rollback is immediate: delete or ignore the disposable `.local/` SQLite index and shadow projections, and continue reading the unchanged legacy sources. Committed design and pilot evidence remains historical control evidence.

After a future cutover, a rollback decision pins readers to the recorded last-known-good legacy-authority revision and disables new event writes. The rollback is itself appended and checkpointed; committed events are never deleted, reordered, or rewritten. Resume requires a focused regression test for the failed invariant and a new explicit authority decision.

Triggers include event-chain or manifest failure, unknown schema, non-deterministic projection, field-parity failure, authority-boundary violation, or reader/writer regression.

## Historical readability guarantee

Every historical checkout remains understandable from tracked text and registries available at that revision. SQLite is never required to read old state. Pre-cutover task files, decisions, completions, handoffs, and registries are retained. Segment schema and renderer versions remain pinned by receipts so future tools can replay or diagnose without silently reinterpreting older events.

## Stop conditions

Stop rather than advance on ambiguous event identity, source-hash drift, missing source authority, sensitive-data exposure, sequence conflict, non-byte-identical rebuild, unmapped legacy fields, partial transaction visibility, or any proposed change to registered science or Gate Chair authority.
