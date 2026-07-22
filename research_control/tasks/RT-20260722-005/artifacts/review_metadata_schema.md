---
authority: "control"
schema_id: "v21_review_context_v1"
plan_task_id: "P11-T02"
---

# V21 review-context metadata schema

## Contract

New external red-team review artifacts may carry this additive strict-YAML
map. The shared validator treats absence as `legacy_unclassified` so historical
reviews remain readable without mutation.

```yaml
review_context:
  schema_id: "v21_review_context_v1"
  classification: "same_context_role_review | blind_same_model_review | different_model_review | human_expert_review | independent_replication | unknown"
  reviewer_kind: "human | ai | mixed | unknown"
  blind_packet_received: false
  prior_context_access: "same_context | blind_packet_only | fresh_context | partial | unknown | not_applicable"
  review_executed: false
  replication_executed: false
  dimensions:
    model_family: {relationship: "same | different | independent | not_applicable | unknown", evidence: "<nonempty>"}
    prompt_context: {relationship: "same | different | independent | not_applicable | unknown", evidence: "<nonempty>"}
    data_access: {relationship: "same | different | independent | not_applicable | unknown", evidence: "<nonempty>"}
    institution: {relationship: "same | different | independent | not_applicable | unknown", evidence: "<nonempty>"}
    human_authorship: {relationship: "same | different | independent | not_applicable | unknown", evidence: "<nonempty>"}
    code_base: {relationship: "same | different | independent | not_applicable | unknown", evidence: "<nonempty>"}
    method: {relationship: "same | different | independent | not_applicable | unknown", evidence: "<nonempty>"}
  evidence_paths: []
  limitations: []
  claims:
    external_review_completed: false
    human_expert_review_completed: false
    independent_replication_completed: false
```

## Validation semantics

- All seven dimensions are required whenever `review_context` is present.
- Every dimension needs a relationship token and a nonempty evidence
  statement, including `unknown` explanations.
- Evidence paths are canonical repo-relative paths; generated wiki and local
  cache paths are forbidden.
- `same_context_role_review` requires an executed review and same prompt
  context.
- `blind_same_model_review` additionally requires a blind packet, same model
  family, and `blind_packet_only` context access.
- `different_model_review` requires an executed review and positive model
  difference evidence.
- `human_expert_review` requires human provenance, authorship separation, and
  canonical evidence paths.
- `independent_replication` requires an executed replication and independent
  data-access, code-base, and method evidence.
- `unknown` requires at least one explicitly unknown dimension and forbids all
  positive completion claims.

## Compatibility

An artifact without `review_context` remains schema-readable and is reported
as `legacy_unclassified`. The compatibility path does not infer a class from
free text, role names, model names, or old provenance fields. A historical
artifact may be classified only by a fresh authorized record that cites the
original artifact without rewriting it.
