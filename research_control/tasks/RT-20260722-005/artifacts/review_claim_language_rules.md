---
authority: "control"
rules_id: "v21_review_claim_language_rules_v1"
plan_task_id: "P11-T02"
---

# V21 calibrated review claim-language rules

## Allowed language

- "same-context role review" when `same_context_role_review` validates.
- "blind same-model review" when `blind_same_model_review` validates.
- "different-model review" when `different_model_review` validates.
- "human expert review" when `human_expert_review` and its evidence validate.
- "independent replication" only when `independent_replication`, an executed
  replication, and independent data, code, and method evidence validate.
- "unknown" whenever a material provenance dimension is not evidenced.

## Forbidden substitutions

- An `external-red-team-reviewer` role name is not proof of external review.
- Different role names are not model diversity or epistemic independence.
- A blind packet is not independent review.
- A fresh prompt is not different-model evidence.
- A different model configuration is not external human review or independent
  replication.
- Reviewer agreement is not replication.
- Validator or checkpoint PASS is not scientific correctness or endorsement.
- Human review is not independent replication without a separately executed
  and evidenced reconstruction.

## Structured wording gate

The shared validator rejects positive completion flags unless the structured
context supports them:

- `external_review_completed: true` requires evidenced human provenance and
  authorship separation under `human_expert_review` or
  `independent_replication`.
- `human_expert_review_completed: true` requires an executed human review.
- `independent_replication_completed: true` requires the
  `independent_replication` class and `replication_executed: true`.

Internal and unknown classes require all three flags to be false. Negative
statements such as "not external review" and "independence unknown" remain
permitted and should be used when they preserve the exact evidence boundary.

## Non-authority

Calibrated wording changes only project-control provenance semantics. It does
not create proof, ontology, source-law, benchmark, Gate Chair, publication, or
completed-derivation authority.
