---
authority: "control"
policy_id: "v21_attempt_history_redaction_policy_v1"
task_id: "RT-20260721-006"
plan_task_id: "P10-T04"
status: "draft/control"
---

# V21 attempt-history redaction policy

## Collection boundary

The attempt ledger may collect only stable task and job identifiers, immutable
candidate IDs, source-recorded timestamps, exact tracked source paths and
hashes, bounded process dispositions, lawful compute-metadata availability, and
the event hash chain. Source files remain canonical; the ledger is an index of
their recorded history.

## Data that must not be collected

The ledger must not contain authentication material, access tokens, signing
material, environment dumps, personal data, user messages, model input text,
private reasoning, hidden instructions, raw terminal transcripts, or copied
third-party content. The validator rejects high-risk field names and common
credential patterns anywhere in the JSON tree.

Summaries must paraphrase only the minimum source-backed disposition. They must
not reproduce private material even if a referenced source were to contain it.

## Compute metadata

Model name, reasoning effort, execution environment, and cost may be recorded
only when directly available for the ledger build or explicitly present in the
canonical event source. Historic missing values use `not_recorded`; numeric
cost uses `null`. Values are never reconstructed from dates, task form, or
neighboring records.

Compute metadata is operational telemetry. It cannot establish a scientific
result, candidate merit, ontology status, Distance-to-GR progress, or proof.

## Correction and retention

Finalized events are retained as an immutable prefix. A factual correction is
a new source-linked event that names the earlier event in `related_event_ids`.
Deletion or mutation of the finalized prefix is invalid. If no canonical source
supports an event class, the ledger records a bounded explicit absence without
inference.

## Classification rule

`process` covers task activation, validator outcomes, repairs, supersessions,
and transaction completion. `scientific_review` covers a tracked audit finding
about a scientific candidate, while `physics_result` remains false. Neither
classification grants adoption, rejection, ontology, promotion, proof,
publication, or completed-derivation authority.
