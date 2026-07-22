<!-- authority: control -->

# Positive-Provenance and Operational-Meaning Gate Policy v1

## 1. Status and authority boundary

```yaml
schema_id: "v21_positive_provenance_operational_meaning_gate_v1"
authority: "control"
status: "active"
created_by_task_id: "RT-20260722-007"
created_by_job_id: "AJ-RT-20260722-007-001"
plan_task_id: "P11-T05"
physics_promotion_authorized: false
proof_authority: false
review_executed_by_this_policy: false
```

This policy makes positive physical evidence a first-class control gate. A
bounded no-target-import check remains necessary, but it is not sufficient.
The same is true of validator, checkpoint, test, or proof-build receipts. None
of those receipts supplies source derivation, naturality, uniqueness or a
defined quotient, dynamics, operational systems, robustness, or appropriately
provenanced review.

The policy evaluates whether an evidence record is complete enough to be sent
to a separately authorized protected Gate Chair review. It never grants the
protected verdict and never authorizes physical promotion. A record may remain
a valid scoped mathematical candidate while failing every physical-readiness
profile.

## 2. Normative machine contract

The JSON object between the markers is normative. Unknown fields and enum
values fail closed for new version-1 records.

<!-- BEGIN V21_POSITIVE_PROVENANCE_GATE_SCHEMA_JSON -->
```json
{
  "schema_id": "v21_positive_provenance_operational_meaning_gate_v1",
  "schema_version": 1,
  "record_type": "positive_provenance_gate_evidence",
  "required_paths": [
    "schema_id",
    "record_id",
    "gate_id",
    "subject_id",
    "subject_scope",
    "review_surface",
    "no_target_purity.status",
    "no_target_purity.evidence_refs",
    "validator_receipts",
    "dimensions.source_derivation.status",
    "dimensions.source_derivation.evidence_refs",
    "dimensions.source_derivation.source_refs",
    "dimensions.source_derivation.source_hashes",
    "dimensions.source_derivation.premise_kinds",
    "dimensions.source_derivation.not_applicable_reason",
    "dimensions.uniqueness_or_quotient.status",
    "dimensions.uniqueness_or_quotient.evidence_refs",
    "dimensions.uniqueness_or_quotient.quotient_scope",
    "dimensions.uniqueness_or_quotient.not_applicable_reason",
    "dimensions.naturality.status",
    "dimensions.naturality.evidence_refs",
    "dimensions.naturality.not_applicable_reason",
    "dimensions.dynamics.status",
    "dimensions.dynamics.evidence_refs",
    "dimensions.dynamics.not_applicable_reason",
    "dimensions.operational_systems.status",
    "dimensions.operational_systems.evidence_refs",
    "dimensions.operational_systems.device_or_protocol_refs",
    "dimensions.operational_systems.not_applicable_reason",
    "dimensions.robustness.status",
    "dimensions.robustness.evidence_refs",
    "dimensions.robustness.perturbation_scope",
    "dimensions.robustness.not_applicable_reason",
    "dimensions.independent_review.status",
    "dimensions.independent_review.evidence_refs",
    "dimensions.independent_review.review_artifact_refs",
    "dimensions.independent_review.not_applicable_reason",
    "review_executed",
    "outcome",
    "authority.status",
    "authority.authority_refs",
    "authority.protected_gate_id",
    "physics_promotion_authorized",
    "forbidden_conclusions"
  ],
  "top_level_fields": [
    "schema_id",
    "record_id",
    "gate_id",
    "subject_id",
    "subject_scope",
    "review_surface",
    "no_target_purity",
    "validator_receipts",
    "dimensions",
    "review_executed",
    "outcome",
    "authority",
    "physics_promotion_authorized",
    "forbidden_conclusions"
  ],
  "required_dimensions": [
    "source_derivation",
    "uniqueness_or_quotient",
    "naturality",
    "dynamics",
    "operational_systems",
    "robustness",
    "independent_review"
  ],
  "enums": {
    "gate_id": ["gate_b", "gate_c"],
    "subject_scope": ["source", "source_extension", "scoped_candidate", "control"],
    "review_surface": ["effective_metric", "detector_semantics", "matter_coupling", "field_equations"],
    "no_target_purity": ["not_assessed", "passed", "failed"],
    "source_derivation": ["missing", "proposed", "source_derived", "refuted", "not_applicable"],
    "uniqueness_or_quotient": ["missing", "multiple_unresolved", "conditional_unique", "unique", "quotient_defined", "refuted", "not_applicable"],
    "naturality": ["missing", "assumed", "conditional", "derived", "refuted", "not_applicable"],
    "dynamics": ["missing", "proposed", "specified", "derived", "validated", "refuted", "not_applicable"],
    "operational_systems": ["missing", "proposed", "specified", "constructed", "validated", "refuted", "not_applicable"],
    "robustness": ["missing", "fragile", "conditional", "robust", "refuted", "not_applicable"],
    "independent_review": ["missing", "same_context_role_review", "blind_same_model_review", "different_model_review", "human_expert_review", "independent_replication", "unknown", "not_applicable"],
    "outcome": ["not_ready", "evidence_complete_for_gate_review", "blocked", "refuted"],
    "authority": ["control_only", "scoped_evidence", "human_gated", "adopted", "rejected"],
    "premise_kind": ["source_ontology", "source_extension", "derived_source_consequence", "external_primary_source"]
  },
  "gate_profiles": {
    "gate_b": {
      "title": "Effective geometry readiness evidence extension",
      "allowed_review_surfaces": ["effective_metric", "detector_semantics"],
      "ready_statuses": {
        "source_derivation": ["source_derived"],
        "uniqueness_or_quotient": ["unique", "quotient_defined"],
        "naturality": ["derived"],
        "dynamics": ["derived", "validated"],
        "operational_systems": ["constructed", "validated"],
        "robustness": ["robust"],
        "independent_review": ["human_expert_review", "independent_replication"]
      },
      "blocked_downstream": ["matter_coupling", "field_equations"]
    },
    "gate_c": {
      "title": "Matter-coupling readiness evidence extension",
      "allowed_review_surfaces": ["matter_coupling", "field_equations"],
      "ready_statuses": {
        "source_derivation": ["source_derived"],
        "uniqueness_or_quotient": ["unique", "quotient_defined"],
        "naturality": ["derived"],
        "dynamics": ["validated"],
        "operational_systems": ["validated"],
        "robustness": ["robust"],
        "independent_review": ["human_expert_review", "independent_replication"]
      },
      "blocked_downstream": ["einstein_equations_derivation", "benchmark_promotion"]
    }
  },
  "review_surface_integration": {
    "effective_metric": ["source_derivation", "uniqueness_or_quotient", "naturality", "dynamics", "operational_systems", "robustness", "independent_review"],
    "detector_semantics": ["source_derivation", "uniqueness_or_quotient", "naturality", "dynamics", "operational_systems", "robustness", "independent_review"],
    "matter_coupling": ["source_derivation", "uniqueness_or_quotient", "naturality", "dynamics", "operational_systems", "robustness", "independent_review"],
    "field_equations": ["source_derivation", "uniqueness_or_quotient", "naturality", "dynamics", "operational_systems", "robustness", "independent_review"]
  },
  "evidence_required_statuses": {
    "source_derivation": ["proposed", "source_derived", "refuted"],
    "uniqueness_or_quotient": ["conditional_unique", "unique", "quotient_defined", "refuted"],
    "naturality": ["conditional", "derived", "refuted"],
    "dynamics": ["specified", "derived", "validated", "refuted"],
    "operational_systems": ["specified", "constructed", "validated", "refuted"],
    "robustness": ["fragile", "conditional", "robust", "refuted"],
    "independent_review": ["same_context_role_review", "blind_same_model_review", "different_model_review", "human_expert_review", "independent_replication"]
  },
  "forbidden_source_premise_kinds": ["target_benchmark", "validator_receipt", "checkpoint_receipt", "test_receipt"],
  "policy_flags": {
    "no_target_purity_required_for_evidence_complete": true,
    "no_target_purity_sufficient_for_evidence_complete": false,
    "validator_pass_sufficient_for_evidence_complete": false,
    "scoped_candidates_remain_representable": true,
    "not_applicable_distinct_from_missing": true,
    "core_dimension_not_applicable_can_complete_gate": false,
    "gate_evidence_completion_is_physical_promotion": false,
    "protected_gate_verdict_required_after_evidence_completion": true
  },
  "conditional_rule_ids": [
    "positive_gate_required_paths",
    "positive_gate_exact_shape",
    "positive_gate_known_enums",
    "positive_gate_gate_surface_alignment",
    "positive_gate_dimension_evidence_required",
    "positive_gate_not_applicable_reason_required",
    "positive_gate_source_hashes_required",
    "positive_gate_source_premises_source_only",
    "positive_gate_quotient_scope_required",
    "positive_gate_operational_refs_required",
    "positive_gate_robustness_scope_required",
    "positive_gate_review_evidence_required",
    "positive_gate_outcome_matches_evidence",
    "positive_gate_no_target_not_sufficient",
    "positive_gate_validator_not_sufficient",
    "positive_gate_no_implicit_physics_promotion"
  ]
}
```
<!-- END V21_POSITIVE_PROVENANCE_GATE_SCHEMA_JSON -->

## 3. Evidence semantics

| Dimension | Positive question | Fail-closed boundary |
| --- | --- | --- |
| `source_derivation` | Is the claim derived from named source-side premises with exact source hashes? | A target benchmark, validator receipt, or observed GR match is not a source premise. |
| `uniqueness_or_quotient` | Is the object unique, or is the residual equivalence relation and quotient explicitly defined? | `conditional_unique` and unresolved multiplicity do not complete either gate. |
| `naturality` | Is the construction derived without an unrecorded arbitrary choice? | Assumed or conditional naturality remains incomplete. |
| `dynamics` | Are the relevant dynamics source-derived and, where Gate C applies, validated in scope? | Merely specifying equations is not a derivation. |
| `operational_systems` | Are source-defined devices or protocols constructed and tied to the claimed measurement semantics? | Naming clocks, rods, detectors, or observables without a protocol is insufficient. |
| `robustness` | Does the result persist over a declared perturbation or model-choice scope? | A single example or validator fixture is not robustness. |
| `independent_review` | Does an executed review have exact provenance at a sufficiently strong calibrated class? | Role diversity, blindness, or a different model alone is not independent review. |

Every `not_applicable` value requires a reason and remains distinct from
`missing`. Because all seven dimensions are core for Gate B and Gate C, neither
value can complete a gate. This preserves honest partial records without
manufacturing readiness.

## 4. Gate B and Gate C extensions

Gate B integrates the seven dimensions into effective-metric and
detector-semantics review. It supplements the existing causal, conformal,
scale, signature, covariance, operational-calibration, and propagation burden;
it does not authorize matter coupling or field equations.

Gate C integrates the same dimensions into matter-coupling and field-equation
review. It additionally requires validated dynamics and validated operational
systems. Evidence completion does not authorize Einstein equations or
benchmark promotion.

For both gates, `evidence_complete_for_gate_review` means only that the record
passes this control policy and may be presented to a separately authorized
protected review. `physics_promotion_authorized` remains exactly `false` in
every version-1 record.

## 5. Review calibration

The independent-review field reuses the exact P11-T02 labels. Same-context
role review, blind same-model review, and different-model review remain useful
but cannot complete this gate. A human-expert review or independent replication
must have an executed review artifact plus evidence references. Even these
classes do not imply proof, source-law adoption, ontology adoption, or physical
promotion.

## 6. Forbidden conclusions

- No-target purity, a validator PASS, a clean checkpoint, or a formal build is
  not positive physical provenance.
- Exact-GR agreement is target-side benchmark evidence, not source derivation.
- Evidence completion is not a Gate Chair verdict.
- A scoped candidate remains proposal-only or scoped evidence until separate
  authority changes that status.
- This policy executes no review and changes no physics, ontology, scientific
  ledger, benchmark, proof, publication, or completed-derivation authority.
