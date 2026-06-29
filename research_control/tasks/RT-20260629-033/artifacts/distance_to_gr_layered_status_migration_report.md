<!-- authority: control -->

# Distance-to-GR Layered Status Migration Report

## Purpose

This report records the P1-T02 additive schema migration for
`registries/DISTANCE_TO_GR_LEDGER.csv`.

The migration appended five columns:

- `control_status`
- `mathematical_status`
- `physical_status`
- `promotion_status`
- `overread_guard`

All pre-existing columns and cell values were preserved. The migration changes
registry representation only. It does not change scientific status, canonical
ontology, source-law adoption, `MetricData(E)` adoption, `g_eff` scope,
coupling-law status, matter-coupling status, stress-energy semantics,
Einstein-equation status, exact-GR benchmark promotion, Gate Chair status, or
completed-derivation status.

## Migration Method

The existing `current_status` field remains as the legacy summary field. The
new fields separate governance state, mathematical object state, physical
interpretation boundary, protected promotion state, and machine-checkable
overread guards.

The P1-T02 task used `research_control/design/distance_to_gr_status_layers_v1.md`
as the schema design source and the P1-T02 implementation-plan mapping as the
minimum required mapping. Where the P1-T02 plan uses narrower vocabulary than
P1-T01, the P1-T02 values control this migration.

## Row Migration Table

| burden_id | before `current_status` | after control layer | after mathematical layer | after physical layer | after promotion layer | before/after meaning |
| --- | --- | --- | --- | --- | --- | --- |
| `source_ontology_primitives` | `draft object exists` | `draft_control_object_exists` | `definition_only_or_draft_object` | `no_canonical_ontology_adoption` | `draft_control_only` | A draft/control primitive object remains available only as non-promotional source-side material. No canonical ontology adoption or benchmark promotion occurred. |
| `source_equivalence_eqsrc` | `draft object exists` | `draft_control_object_exists` | `general_equivalence_theorem_missing` | `downstream_gr_blocked` | `draft_control_only` | EqSrc remains a draft/control object with the general equivalence theorem still missing. Downstream GR burdens remain blocked. |
| `retain_h` | `blocked by missing primitive` | `blocked` | `primitive_missing` | `no_retention_law_adoption` | `none` | RetainH remains blocked by a missing primitive. No retention law was adopted. |
| `gen_h` | `blocked by missing primitive` | `blocked` | `primitive_missing` | `no_generator_law_adoption` | `none` | GenH remains blocked by a missing primitive. No generator law was adopted. |
| `obsloc_lc` | `constructive witness exists` | `constructive_witness_recorded` | `constructive_witness` | `local_exact_branch_only` | `draft_control_only` | ObsLoc_lc retains a local exact-branch constructive witness only. It is not a general source law, coupling result, benchmark result, or completed derivation. |
| `resp_lc` | `accepted` | `accepted_as_source_extension_data` | `selector_data_source_extension` | `not_detector_semantics_not_matter_coupling` | `scoped_source_object_only` | Resp_lc remains accepted only as admissible source-extension data for selector continuation. It is not detector semantics or matter coupling. |
| `m_src` | `accepted` | `gate_review_completed` | `scoped_source_only_adopted_object` | `not_target_manifold_not_metric_not_gr_derivation` | `scoped_source_object_only` | M_src remains a scoped source-only adopted object under its reviewed boundary. It is not the target manifold, not a metric, and not a GR derivation. |
| `g_eff` | `accepted` | `gate_review_completed` | `scoped_source_extension_geff_object` | `not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations` | `scoped_source_object_only` | g_eff remains a scoped source-extension g_eff object only. It is not an unscoped Lorentzian metric, matter coupling, Einstein equations, benchmark promotion, or completed derivation. |
| `matter_coupling` | `accepted` | `accepted_as_scoped_evidence_precondition` | `parameterized_finite_local_witness_precondition` | `not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics` | `scoped_source_evidence_only` | The accepted objects remain scoped source-extension parameterized-witness evidence/preconditions only. They are not matter-coupling derivation or adoption, stress-energy semantics, stress-energy tensor, matter action, detector semantics, Einstein equations, benchmark promotion, or completed derivation. |
| `einstein_equations` | `not started` | `not_started` | `dynamics_action_or_variation_missing` | `no_field_equation_derivation` | `none` | Einstein-equation derivation remains absent. No field-equation derivation was supplied. |
| `finite_variation_robustness` | `Refuter stress passed` | `refuter_stress_passed` | `conditional_theorem_candidate` | `downstream_gr_blocked` | `draft_control_only` | The fail-closed proposal-only finite-variation robustness interface remains a stressed conditional candidate. Arbitrary robustness adoption and downstream GR claims remain blocked. |
| `benchmark_promotion` | `blocked by missing primitive` | `blocked` | `upstream_burdens_missing` | `no_exact_gr_benchmark_promotion` | `none` | Exact-GR benchmark promotion remains blocked by upstream burdens. No benchmark promotion occurred. |
| `gate_chair_status` | `human-gated` | `human_gated` | `protected_verdict_missing` | `no_benchmark_closure` | `human_gate_required` | Gate Chair status remains protected and unresolved. No benchmark closure verdict occurred. |
| `finite_toy_metric_response` | `frozen negative` | `frozen_negative` | `tag_removal_obstruction` | `local_toy_route_frozen_not_global_theory_rejection` | `frozen_negative_no_promotion` | The explicit-tag-only finite toy route remains locally frozen after tag-removal obstruction. This is not a global theory rejection or proof of future source-extension impossibility. |

## Validator Update

`scripts/research_control/validate_research_control.py` now requires the new
columns, checks nonblank layer fields, validates controlled vocabulary, and
checks required overread-guard tokens for high-risk rows including `g_eff`,
`matter_coupling`, `einstein_equations`, `benchmark_promotion`,
`gate_chair_status`, and `finite_toy_metric_response`.

The focused regression test
`tests/test_research_control.py::ResearchControlTests::test_distance_to_gr_ledger_requires_layered_overread_guards`
verifies that removing a required `matter_coupling` overread guard causes a
validator error.

## Completion Receipt

P1-T02 is complete when the ledger parses under the updated schema, the focused
test passes, the current-frontier renderer still checks cleanly, and the normal
Continue Research validators pass.

Completion boundary:

- no science status changed;
- no historical scientific artifact was rewritten;
- no canonical ontology edit occurred;
- no source law was adopted;
- no `MetricData(E)` adoption occurred;
- no `g_eff` scope expansion occurred;
- no coupling law was adopted;
- no matter-coupling derivation or adoption occurred;
- no stress-energy semantics, stress-energy tensor, matter action, or detector
  semantics were imported;
- no Einstein equations were derived;
- no exact-GR benchmark promotion occurred;
- no benchmark Gate Chair closure occurred;
- no completed derivation was claimed.

## APA 7 Source Materials

The AEther-Flow Research Project. (2026, June 29). *Distance-to-GR status
layers v1* [Internal control design note].

The AEther-Flow Research Project. (2026, June 29). *Recommendations
implementation plan continue task v12* [Internal implementation plan].

The AEther-Flow Research Project. (2026, June 29). *Handoff 0327* [Internal
research-control handoff].
