---
authority: "control"
schema_id: "v21_reviewer_agreement_metric_specification_v1"
plan_task_id: "P11-T06"
physics_promotion_authorized: false
proof_authority: false
---

# Reviewer disagreement and agreement metric specification v1

## Purpose and boundary

This specification makes disagreement, agreement, unresolved conflict, and
correlated-review risk measurable without treating consensus as theorem truth.
It applies to review evidence only after each input is linked to a stable
reviewed object and a calibrated P11-T02 review-context class.

The P11-T06 implementation is project-control machinery. Its calibration
fixtures are synthetic and execute no scientific review. A metric value,
validator result, majority, unanimous assessment, human-review label, or
replication label cannot change scientific status, adopt an ontology or source
law, authorize a Gate Chair verdict, promote a benchmark, or establish a
completed derivation.

## Input contract

Every metric input identifies:

- one stable `review_id` and `reviewed_object_id`;
- the repo-relative reviewed source path and exact SHA-256;
- the source review-artifact identity or synthetic calibration identity;
- an opaque blinded configuration ID;
- the P11-T02 review-context classification and all seven provenance
  dimensions;
- one assessment for each required review axis; and
- explicit false authority flags.

Production inputs must be backed by a separately authorized, executed review
artifact. The task-local fixture suite uses
`record_mode: synthetic_calibration`, keeps every review-completion claim
false, and exists only to calibrate the report generator.

## Required review axes

The five axes are independent reporting surfaces:

| Axis | Question measured | Examples of preserved disagreement |
| --- | --- | --- |
| `theorem_validity` | Does the stated conclusion follow under the stated scope? | hidden gap, unsupported step, blocking defect |
| `assumptions` | Are assumptions complete, explicit, and adequate? | omission, ambiguity, evidence gap |
| `countermodels` | Was a countermodel attempted or found in scope? | not assessed, scoped counterexample, blocking counterexample |
| `physical_interpretation` | Does interpretation stay within the mathematical result? | interpretation mismatch, ontology overread |
| `claim_scope` | Does the prose preserve the exact authority and domain? | scope overreach, unsupported generalization |

Each axis records `finding_category`, `severity`, `verdict`, `finding_ids`,
`resolution_status`, and canonical `evidence_refs`. The normalized tokens are:

- categories: `no_finding`, `omission`, `ambiguity`, `unsupported_step`,
  `counterexample`, `scope_overreach`, `interpretation_mismatch`,
  `evidence_gap`, and `not_assessed`;
- severities: `none`, `low`, `medium`, `high`, `critical`, and `unknown`;
- verdicts: `clear`, `concern`, `repair_required`, `blocking`, and
  `not_assessed`; and
- resolution states: `no_finding`, `resolved`, `unresolved`, and
  `not_assessed`.

`not_assessed` is excluded from pairwise denominators but remains visible as a
coverage gap. It is never silently converted to agreement.

## Metrics

For every reviewed object and axis, the report generator forms all eligible
review pairs. An exact assessment agreement requires equality of category,
severity, and verdict. Every nonmatching eligible pair is a disagreement. A
disagreement is an unresolved conflict when either side remains unresolved.

The report contains:

1. exact agreement and disagreement counts and rates;
2. coverage gaps from `not_assessed` inputs;
3. every unresolved conflict with both review lineages intact;
4. within-class and cross-class summaries using the exact P11-T02 context
   labels;
5. an explicit list of unanimous assessments at risk of false consensus; and
6. opaque configuration summaries for blinded comparison.

Agreement is descriptive. The schema intentionally defines no winning
configuration, truth score, proof threshold, promotion threshold, or automatic
scientific disposition.

## False-consensus risk

A unanimous assessed axis is flagged when at least two reviews agree exactly,
no `human_expert_review` or `independent_replication` record is present, and
material provenance dimensions remain shared or unknown. The flag records the
review IDs, context classes, and shared or unknown dependency dimensions.

This flag is a correlation warning, not a finding that the unanimous judgment
is false. Conversely, the absence of the flag does not prove independence or
correctness.

## Blinded configuration comparison

Configuration identifiers are opaque. Reports compare axis coverage, finding
diversity, unresolved findings, high-severity findings, objects covered, and
review-context classes. They expose `ranking_forbidden: true` and
`winner: null`. A configuration cannot be optimized or selected solely because
it produces higher agreement.

## Lineage and source integrity

Every reviewed source path must be repo-relative, non-generated authority, and
byte-equal to its recorded SHA-256. Review IDs remain visible in every pair and
conflict row. `.local/`, generated wiki notes, and missing or changed sources
fail closed.

## Non-conclusions

- Consensus is not proof.
- Disagreement is not refutation.
- Reviewer diversity is not independence unless the structured evidence says
  so.
- A human-expert label is not independent replication.
- A metric generator PASS is operational evidence only.
- This task executes no review, changes no scientific ledger row, and grants
  no ontology, source-law, metric, matter-coupling, Einstein-equation,
  benchmark, proof, publication, or completed-derivation authority.
