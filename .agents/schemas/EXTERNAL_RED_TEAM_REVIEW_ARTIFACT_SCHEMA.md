---
schema_id: "EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA"
version: "0.1.0"
status: "active"
---

# External Red-Team Review Artifact Schema

## Purpose

This schema defines the P7 red-team review artifact contract. It is
project-control validation for critique and routing evidence only. It does not
create proof authority, Gate Chair authority, source-law adoption, benchmark
promotion, or completed-derivation status.

## Required Fields

- `reviewed_object_id`: nonempty canonical object identifier or stable local
  review target identifier.
- `reviewed_source_paths`: nonempty list of repo-relative canonical source
  paths inspected by the reviewer. `.local/`, generated wiki notes, absolute
  paths, and parent-directory escapes are invalid here.
- `claim_under_review`: nonempty statement of the claim being externally
  pressured.
- `assumptions_read`: list of assumptions inspected.
- `definitions_read`: list of definitions inspected.
- `proof_steps_checked`: list of theorem or proof-skeleton steps checked.
- `circularity_findings`: list of circularity findings, or `[]`.
- `hidden_import_findings`: list of hidden target-import findings, or `[]`.
- `notation_overload_findings`: list of overloaded-notation findings, or `[]`.
- `unproven_equivalence_findings`: list of unproven-equivalence findings, or
  `[]`.
- `minimal_countermodel_attempt`: map describing whether a countermodel was
  attempted, the result, and a summary.
- `external_mathematical_pressure_points`: list of external skeptic pressure
  points, or `[]`.
- `verdict`: one of the allowed verdict values below.
- `recommended_next_route`: nonempty route recommendation.
- `physics_promotion_authorized`: exactly `false`.

## Required Verdict Vocabulary

- `no_blocking_defect_found_as_written`
- `repair_required`
- `hidden_target_import_detected`
- `circularity_detected`
- `unproven_equivalence_blocks_claim`
- `not_enough_assumptions`
- `minimal_countermodel_found`
- `freeze_recommended`
- `external_expert_review_required`

## Additive review-context contract

New review artifacts include a `review_context` map. Artifacts created before
this additive contract remain valid and are reported by the validator as
`legacy_unclassified`; they are not retroactively relabeled.

The map has these fields:

- `schema_id`: exactly `v21_review_context_v1`.
- `classification`: one of `same_context_role_review`,
  `blind_same_model_review`, `different_model_review`,
  `human_expert_review`, `independent_replication`, or `unknown`.
- `reviewer_kind`: one of `human`, `ai`, `mixed`, or `unknown`.
- `blind_packet_received`: boolean.
- `prior_context_access`: one of `same_context`, `blind_packet_only`,
  `fresh_context`, `partial`, `unknown`, or `not_applicable`.
- `review_executed`: boolean.
- `replication_executed`: boolean.
- `dimensions`: exactly the seven keys `model_family`, `prompt_context`,
  `data_access`, `institution`, `human_authorship`, `code_base`, and `method`.
  Every dimension records `relationship` as `same`, `different`,
  `independent`, `not_applicable`, or `unknown`, plus a nonempty `evidence`
  statement.
- `evidence_paths`: repo-relative canonical evidence paths, or `[]` when the
  class is explicitly `unknown` and no evidence exists.
- `limitations`: explicit limitations, or `[]` when none are known.
- `claims`: booleans `external_review_completed`,
  `human_expert_review_completed`, and
  `independent_replication_completed`.

Different roles or model configurations are not automatically independent.
`human_expert_review` requires human provenance and evidence.
`independent_replication` requires an executed replication plus independent
data-access, code-base, and method evidence. Missing evidence fails closed to
`unknown`. Positive external-review or independent-replication wording is
invalid unless the structured class and evidence support it.

## Minimal Countermodel Attempt

`minimal_countermodel_attempt` must be a map with:

- `attempted`: boolean.
- `result`: one of `not_attempted`, `no_countermodel_found_under_scope`,
  `countermodel_found`, or `not_enough_assumptions`.
- `summary`: nonempty text.
- `artifact_path`: optional repo-relative path or empty string.

## Validator

The deterministic validator is
`scripts/research_control/validate_red_team_review_artifact.py`. It validates
one or more strict-YAML red-team review artifacts and emits a JSON receipt.

## Boundary

Passing this schema means only that the review artifact has the required shape
and preserves `physics_promotion_authorized: false`. It does not imply that the
review is scientifically correct, that a claim is proven, or that a defect is
resolved. Review-context validation records provenance calibration only; it
does not create epistemic independence or scientific authority.
