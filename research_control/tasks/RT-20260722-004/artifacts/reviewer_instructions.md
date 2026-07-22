---
authority: "control"
protocol: "v21_blind_review_packet_v1"
plan_task_id: "P11-T01"
---

# Blind scientific reviewer instructions

Review only the supplied blind packet. Do not infer workflow history, prior
outcomes, author confidence, validator results, or reviewer independence from
its formatting or source hashes.

## Review duties

1. Restate the declared domain and assumptions before evaluating the result.
2. Check definitions for ambiguity, circularity, and hidden dependence on the
   desired conclusion.
3. Check each supplied proof or construction step against the assumptions.
4. Look for a minimal counterexample within the declared domain.
5. Separate defects in the stated mathematical result from objections that
   require changing its declared domain.
6. Respect every supplied claim boundary. A conditional finite or formal
   result is not evidence of ontology adoption, physical gauge, general EqSrc,
   publication, benchmark promotion, or a completed derivation.

## Required response fields

Return a structured critique containing:

- assumptions received and used;
- blocking defects, if any;
- nonblocking ambiguities or missing explanations;
- attempted in-domain counterexample and its outcome;
- scope-overread risks;
- a concise critique summary.

Do not report a workflow verdict or an independence label. The operator records
review context separately, and a later controlled task classifies reviewer
independence and model diversity.
