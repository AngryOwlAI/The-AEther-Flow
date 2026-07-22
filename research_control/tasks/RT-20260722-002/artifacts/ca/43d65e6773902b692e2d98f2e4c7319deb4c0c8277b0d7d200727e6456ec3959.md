---
authority: control
task_id: RT-20260721-007
plan_task_id: P10-T05
schema_id: v21_project_control_event_v1
status: design_only
---

# V21 project-control event schema

## Record encoding

A future canonical event segment contains one UTF-8 JSON object per LF-terminated line. Every object uses RFC 8785 JSON Canonicalization Scheme bytes. Binary floating-point payloads are forbidden; quantitative values use decimal strings and declared units. The manifest is canonical JSON and orders immutable segments by their inclusive global sequence range.

This schema is inactive in P10-T05. It defines the input contract for a later bounded pilot and does not authorize event writes or migration.

## Envelope

Each event has these required fields:

| Field | Contract |
| --- | --- |
| `event_schema_id` | Exact supported schema identifier, initially `v21_project_control_event_v1`. |
| `event_id` | `EVT-V21-` plus all 64 lowercase hexadecimal characters of the SHA-256 identity hash. |
| `sequence` | Positive global integer assigned while the single-writer lock is held. It is the replay order. |
| `prior_event_hash` | Prior manifest head hash, or `GENESIS` for sequence 1. |
| `event_hash` | SHA-256 of canonical event content excluding `event_hash`. |
| `event_domain` | One of `task`, `decision`, `agent_job`, `candidate`, `claim`, `validation`, `authority`, or `handoff`. |
| `event_type` | A schema-declared transition for the chosen domain. |
| `subject_id` | Stable identifier of the task, decision, job, candidate, claim boundary, validation, authority record, or handoff. |
| `operation_id` | Producer-supplied stable idempotency key, unique within subject and type. |
| `effective_at` | Source-derived RFC 3339 UTC metadata; it never establishes replay order. |
| `actor_role_ref` | Versioned role or explicit human authority reference responsible for the event. |
| `source_refs` | Nonempty exact references supporting the event. |
| `payload` | Domain-specific project-control content. |
| `authority` | Explicit non-promotion flags and authority classification. |

Optional fields are omitted, not written as `null`. Unknown schemas or event types fail closed until a compatible schema upgrade is explicitly accepted.

## Deterministic identity

The identity basis is canonical JSON containing `event_schema_id`, `event_domain`, `event_type`, `subject_id`, `operation_id`, `source_refs`, and `payload`. Its SHA-256 digest determines `event_id`. Because `operation_id` is stable, retrying the same logical operation yields the same identity. An existing ID with identical canonical content is an idempotent no-op; differing content under the same identity is a hard conflict.

Sequence and prior hash are transaction placement, not logical identity. They are assigned only after the manifest head compare-and-swap succeeds. The event hash binds them into the final chain.

## Source references

Every source reference contains:

- `object_id`: registered object ID, or an explicit control-record ID when no registry object exists;
- `path`: repository-relative tracked source path;
- `sha256`: exact lowercase SHA-256 of the source bytes;
- `authority_status`: the source's actual authority classification.

References are verified at the pinned Git revision. Scientific content is referenced, not copied into a stronger control assertion. A changed hash requires a new source reference and a new event.

## Domains and transitions

| Domain | Representative transitions | Compatibility view |
| --- | --- | --- |
| `task` | created, activated, completed, blocked, corrected | `RESEARCH_TASK_REGISTRY.csv` |
| `decision` | created, activated, completed, superseded, corrected | `DIRECTOR_DECISION_REGISTRY.csv` |
| `agent_job` | created, started, completed, blocked, corrected | `AGENT_JOB_REGISTRY.csv` |
| `candidate` | created, revised, superseded, review recorded, corrected | task-local candidate lineage views |
| `claim` | boundary created, activated, closed, corrected | `CLAIM_BOUNDARY_REGISTRY.csv` |
| `validation` | started, passed, failed, invalidated, corrected | completion and validation receipts |
| `authority` | requested, granted, denied, expired, corrected | tracked human-gate and authority artifacts |
| `handoff` | created, consumed, superseded, corrected | `research_control/handoffs/` |

The candidate domain records lineage and review state, not adoption or rejection authority. The authority domain records that a controlling artifact exists; it does not manufacture authority from an event.

## Append-only corrections

Finalized events are immutable. A correction is a new event with a new stable operation ID and payload that names `superseded_event_ids`, the corrected fields, the reason, and exact source references. Reducers apply the correction prospectively. Old bytes, hashes, sequence numbers, and source records remain readable.

Deletion, in-place repair, backdated sequence, inferred missing history, or a replacement segment with altered finalized events is invalid.

## Privacy and redaction

Event payloads contain minimum necessary project-control evidence. Prompts, hidden reasoning, credentials, tokens, personal data, and unrestricted command output are forbidden. A later redaction cannot mutate history: it adds a restricted correction/tombstone event and preserves a hash-stable audit reference through the repository's approved sensitive-data procedure.

## Explicit authority flags

Every event includes `project_control_only`, `scientific_claims_changed`, `physics_promotion_authorized`, and `proof_authority`. For the P10 design and any read-compatible pilot these must be `true`, `false`, `false`, and `false`, respectively. A future protected action still requires its existing human-gated source artifact and Gate Chair authority where applicable; changing a flag cannot grant that authority.
