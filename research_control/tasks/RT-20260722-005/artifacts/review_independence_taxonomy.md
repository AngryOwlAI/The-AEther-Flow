---
authority: "control"
schema_id: "v21_review_independence_taxonomy_v1"
plan_task_id: "P11-T02"
---

# V21 review-independence and model-diversity taxonomy

## Purpose and boundary

This taxonomy classifies the provenance of review and replication evidence. It
does not score scientific correctness, create epistemic independence, execute
a review, certify a reviewer, prove a theorem, or authorize physics promotion.
The classification is categorical rather than ordinal: more separation along
one dimension does not erase shared dependence along another.

Every new record evaluates seven dimensions separately: model family, prompt
context, data access, institution, human authorship, code base, and method.
Their canonical keys are `model_family`, `prompt_context`, `data_access`,
`institution`, `human_authorship`, `code_base`, and `method`.
Each dimension is `same`, `different`, `independent`, `not_applicable`, or
`unknown`. `different` means only that a documented difference exists;
`independent` requires positive evidence that the relevant dependency is not
shared. Missing evidence is `unknown`.

## Normalized classifications

| Token | Minimum evidence | Allowed interpretation | Forbidden overread |
| --- | --- | --- | --- |
| `same_context_role_review` | An executed review whose prompt context is documented as the same context. | Same-context skeptical pressure, including distinct internal role views. | External review, model diversity, or independent replication. |
| `blind_same_model_review` | Executed review; blind packet received; same model family; only the blind packet was available in the review context. | Bounded context separation within one model family. | Statistical independence, different-model review, external human review, or replication. |
| `different_model_review` | Executed review plus exact evidence that the task-facing model family differs. | Model-configuration diversity with every other dimension reported separately. | Provider, training-data, institutional, methodological, or replication independence. |
| `human_expert_review` | Executed human review; positive human provenance; authorship separation; canonical evidence paths. | Human expert critique with recorded conflicts and access limits. | Independent replication unless a distinct replication was actually executed and evidenced. |
| `independent_replication` | Executed replication; known provenance; independent data access, code base, and method; canonical evidence paths. | A separately reconstructed result under the recorded scope. | Proof, universal reproducibility, ontology adoption, or physics promotion. |
| `unknown` | At least one material dimension lacks evidence. | Exact statement that the available record cannot support a stronger class. | Any inferred external, human-expert, or independent-replication claim. |

## Decision rules

1. Classify the evidence that exists, not the role title or intended setup.
2. A blind packet proves only bounded context separation.
3. A different model identifier proves only model-family difference when the
   identifier and configuration are recorded.
4. A human reviewer is not automatically institutionally or methodologically
   independent.
5. Review and replication are distinct activities. Agreement among reviews is
   not a replication result.
6. `independent_replication` requires an executed reconstruction and positive
   evidence for independent data access, code base, and method.
7. Positive `external review completed`, `human expert review completed`, or
   `independent replication completed` wording must match structured claims
   and evidence.
8. Historical artifacts without the additive context block remain
   `legacy_unclassified`; they are not rewritten or strengthened.

## Examples

- Two task children with different role names and the same inherited context:
  `same_context_role_review`.
- A fresh blind packet sent to the same model family:
  `blind_same_model_review`.
- A fresh blind packet sent to a different task-facing model with shared
  provider and training dependence unknown: `different_model_review`.
- A qualified human report with provenance and conflict declaration:
  `human_expert_review`, not replication.
- A separately implemented calculation using independently sourced data, code,
  and method: `independent_replication` under its exact scope.
- A report with no model, context, or authorship evidence: `unknown`.

## Claim boundary

Passing taxonomy validation means only that provenance labels and language are
internally consistent. It does not prove reviewer independence, scientific
correctness, source-law adoption, ontology status, benchmark status, external
endorsement, publication readiness, or a completed derivation.
