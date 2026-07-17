<!-- authority: control -->

# No-Target Import Mutation Tester Spec v1

## Purpose

This artifact specifies the v18 P7-T04
`no_target_import_mutation_tester_support_only` implementation. The tester
creates deterministic negative text fixtures by applying plan-defined forbidden
premise mutations to a source-safe control snippet, then runs the existing
claim-language linter against each mutated fixture.

The tester is support-only validator tooling. It is not proof authority, not a
source-law adoption route, not target metric import, not `MetricData(E)`
adoption, not `g_eff` adoption or scope expansion, not matter-coupling
derivation, not Einstein-equation derivation, not benchmark promotion, not a
Gate Chair verdict, and not a completed derivation.

## Inputs

- `implementations_plans/recommendations_implementation_plan_continue_task-v18.md`
- `research_control/design/no_target_import_guard_map.md`
- `research_control/design/claim_language_linter_taxonomy.yaml`
- `scripts/project_control/validate_claim_language.py`

## Required Mutations

The tester must include exactly these v18 P7-T04 mutation identifiers:

- `insert_target_metric_premise`
- `insert_proper_time_normalization`
- `insert_empirical_detector_protocol`
- `insert_stress_energy_semantics`
- `insert_matter_action_premise`
- `insert_benchmark_behavior_premise`
- `insert_validator_as_proof_premise`

Each mutation must fail closed under the existing claim-language linter and
must expose at least one expected target-import or validator-as-proof class.

## Output Contract

The script at
`scripts/research_control/support_formalization/no_target_import_mutation_tester.py`
must emit a JSON report with:

- `tester_id: no_target_import_mutation_tester`
- `support_only: true`
- `proof_authority: false`
- `physics_promotion_authorized: false`
- `source_law_adopted: false`
- `validator_behavior_changed: false`
- `base_safe_text_status: PASS`
- one `mutation_results` item per required mutation
- `status: PASS` only if every mutation has `observed_status: FAIL` and no
  missing expected linter classes

## Done Criteria

- Focused unit tests pass.
- The task-local validator report passes.
- No source-law or proof authority is claimed.
- The next route is P7-T05
  `metric_use_ledger_tex_validator_support_only`.
