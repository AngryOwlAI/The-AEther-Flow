<!-- authority: control -->

# P5-T02 Source Detector/Readout DAG Ledger Question Receipt

## Result

P5-T02 is complete. The packet creates a protected ledger-delta question and a
proposal-only DAG patch shape for `source_detector_readout_semantics`.

Required outputs:

```text
research_control/tasks/RT-20260708-008/artifacts/source_detector_readout_ledger_delta_question_v1.yaml
research_control/tasks/RT-20260708-008/artifacts/source_detector_readout_dag_patch_proposal_v1.md
```

## Ledger Question

```yaml
ledger_delta_question:
  proposed_burden_id: "source_detector_readout_semantics"
  proposed_status: "proposal_burden_only"
  proposed_control_status: "burden_proposed_not_adopted"
  proposed_mathematical_status: "readout_law_missing"
  proposed_physical_status: "not_detector_semantics_not_matter_coupling"
  promotion_status: "none"
  requires_protected_authority_to_update_ledger: true
  update_performed_in_this_task: false
```

## Done Criteria

- The task creates a question/proposal only.
- No protected ledger update is performed.
- No populated matter-coupling DAG update is performed.
- The next route is P5-T03.

## Claim Boundary

Allowed claims:

- v18 P5-T02 ledger-delta question exists.
- v18 P5-T02 DAG patch proposal exists.
- `source_detector_readout_semantics` remains `proposal_burden_only`.
- The next bounded route is P5-T03.

Forbidden claims:

- Distance-to-GR ledger update.
- populated matter-coupling DAG update.
- `Det_src` adoption.
- `Readout_src` adoption.
- detector-semantics adoption.
- empirical detector protocol authority.
- proper-time normalization.
- target metric authority.
- coupling-law adoption.
- matter-coupling derivation or adoption.
- stress-energy semantics, stress-energy tensor, or matter action.
- Einstein equations.
- benchmark promotion.
- Gate Chair verdict.
- completed derivation.

## Recommendation Coverage

```yaml
recommendation_coverage:
  source_plan_id: "recommendations_implementation_plan_continue_task-v18"
  source_recommendation_ids:
    - "V18-R04"
  implements_plan_task_id: "P5-T02"
  implementation_status: "completed"
  coverage_effect: "support"
```
