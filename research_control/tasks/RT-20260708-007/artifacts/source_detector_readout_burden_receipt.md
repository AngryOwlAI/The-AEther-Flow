<!-- authority: control -->

# P5-T01 Source Detector/Readout Burden Receipt

## Result

P5-T01 is complete. The packet defines
`source_detector_readout_semantics` as a named matter-coupling frontier burden
with status `proposal_burden_only`.

Primary output:

```text
research_control/design/source_detector_readout_semantics_burden_v1.md
```

## Burden Model

```yaml
burden_id: "source_detector_readout_semantics"
milestone: "matter_coupling"
required_object: "Det_src or Readout_src"
current_status: "proposal_burden_only"
```

## Done Criteria

- The note defines the burden.
- The note does not update the Distance-to-GR ledger.
- The note states that source detector/readout semantics are not adopted.
- The next route is P5-T02.

## Claim Boundary

Allowed claims:

- v18 P5-T01 source detector/readout burden design note exists.
- `source_detector_readout_semantics` is a proposal-only matter-coupling
  frontier burden.
- The next bounded route is P5-T02.

Forbidden claims:

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
  implements_plan_task_id: "P5-T01"
  implementation_status: "completed"
  coverage_effect: "direct"
```
