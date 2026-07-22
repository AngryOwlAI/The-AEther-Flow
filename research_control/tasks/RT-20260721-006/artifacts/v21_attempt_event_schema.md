---
authority: "control"
schema_id: "v21_research_attempt_ledger_v1"
task_id: "RT-20260721-006"
plan_task_id: "P10-T04"
status: "draft/control"
---

# V21 research-attempt event schema

## Purpose and authority

This schema defines a project-control history of tracked research attempts and
rework. It exposes source-backed process history that PASS-only summaries can
hide. It does not replace a task, completion, scientific source, candidate
ledger, or Distance-to-GR row. A validator failure is process evidence, not a
physics result.

The ledger is additive. Every finalized event is immutable, and a later
revision must retain the complete finalized event prefix from the Git `HEAD`
version byte-for-byte after canonical JSON parsing. Correction occurs through a
new event with `related_event_ids`; mutation or deletion is invalid.

## Ledger object

The top-level JSON object requires:

- `schema_id`: exactly `v21_research_attempt_ledger_v1`.
- `ledger_id`, `task_id`, `plan_task_id`, `status`, `revision`, and
  `sealed_at`: stable ledger identity and revision metadata.
- `append_only`: exactly `true`.
- `chain_algorithm`: exactly `sha256-canonical-json-v1`.
- `redaction_policy_path`: the controlling task-local privacy policy.
- `candidate_registry_path`: the immutable candidate-identity source used when
  an event carries candidate IDs.
- `build_compute_metadata`: lawful runtime metadata for the ledger build only;
  it is operational telemetry and not scientific authority.
- `explicit_absences`: source-scope statements for event classes not found.
- `authority_boundary`: false-valued scientific, ontology, promotion, proof,
  publication, and completed-derivation authority flags.
- `events`: a sequence-ordered array of finalized event objects.

## Event object

Each event requires exactly these fields:

| Field | Contract |
| --- | --- |
| `event_id` | Unique `AEV-` identifier. |
| `sequence` | Contiguous positive integer starting at one. |
| `event_type` | One of `attempt_started`, `validation_failed`, `audit_finding`, `repair_applied`, `superseded`, `abandoned`, or `completed`. |
| `occurred_at` | Source-recorded UTC timestamp. |
| `task_id`, `job_id` | Source task and job identity. |
| `candidate_ids` | Zero or more IDs present in the pinned candidate registry. |
| `source_refs` | One or more tracked paths with exact SHA-256 digests. |
| `summary` | Bounded source-faithful description without private content. |
| `disposition` | Event-type-compatible process disposition. |
| `evidence_domain` | `process` or `scientific_review`. |
| `physics_result` | Exactly `false`; this ledger contains no physics-result events. |
| `finalized` | Exactly `true`. |
| `related_event_ids` | Earlier events repaired, completed, or otherwise related. |
| `compute_metadata` | Historical availability record; missing telemetry is `not_recorded`, never inferred. |
| `authority` | False-valued scientific and protected-authority flags. |
| `prior_event_hash` | Empty for sequence one; otherwise the preceding event hash. |
| `payload_sha256` | SHA-256 of canonical event JSON excluding all three hash fields. |
| `event_hash` | SHA-256 of canonical `{event_id, sequence, payload_sha256, prior_event_hash}`. |

Canonical JSON uses UTF-8, sorted keys, compact separators, and no ASCII
escaping. All source paths are repository-relative regular tracked files.

## Dispositions

The allowed event/disposition pairs are:

- `attempt_started` / `active`
- `validation_failed` / `blocked`
- `audit_finding` / `finding_recorded`
- `repair_applied` / `completed`
- `superseded` / `superseded`
- `abandoned` / `abandoned`
- `completed` / `completed`

`related_event_ids` may name only earlier events. `repair_applied` requires at
least one related event. Candidate IDs are optional because project-control
attempts need not belong to a scientific candidate family.

## Explicit absence

Every event type absent from `events` requires one `explicit_absences` record
with `inference_performed: false`, a bounded `source_search_scope`, and a plain
reason. An absence record means only that no canonical source was located in
that scope. It is not evidence that an event never occurred.

## Privacy and compute metadata

The companion redaction policy forbids credentials, private prompts, private
reasoning, personal data, and copied terminal or environment payloads. Historic
model, effort, environment, or cost data are recorded only when a governing
source states them. Otherwise every missing value remains `not_recorded` and
numeric cost remains `null`.

## Validation obligations

The validator must reject schema drift, noncontiguous sequence, duplicate IDs,
invalid type/disposition pairs, forward relations, source-hash drift, untracked
sources, unknown candidate IDs, hash-chain mismatch, finalized-prefix mutation
or deletion, forbidden private fields or secret patterns, `physics_result:
true`, or any protected-authority flag set to true. It also checks deterministic
report and receipt surfaces.
