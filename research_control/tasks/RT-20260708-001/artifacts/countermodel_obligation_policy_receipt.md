<!-- authority: control -->

# Countermodel Obligation Policy Receipt

## Control Status

```yaml
artifact_id: "countermodel_obligation_policy_receipt"
artifact_type: "project_control_task_receipt"
task_id: "RT-20260708-001"
job_id: "AJ-RT-20260708-001-001"
role_id: "project-control-maintainer"
created_at: "2026-07-08T00:22:57Z"
plan_task_id: "P4-T01"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Define minimal countermodel obligations for future theorem attempts."
```

## Implementation Result

P4-T01 is complete. The packet created:

```text
research_control/design/minimal_countermodel_obligation_policy_v1.md
```

The policy makes countermodel slots mandatory for future theorem attempts
unless waived by an explicit Director Decision Record. It distinguishes
countermodel, obstruction, freeze, and program-wide no-go language. It also
states that a local countermodel must not be read as a program-wide no-go
conclusion.

## Required Sections

| Required section | Status |
| --- | --- |
| Why theorem attempts require countermodel slots | present |
| Difference between countermodel, obstruction, freeze, and program-wide no-go | present |
| Required countermodel slots by theorem family | present |
| EqSrc-specific slots | present |
| Matter-coupling-specific slots | present |
| Detector/readout-specific slots | present |
| Toy-model-specific slots | present |
| Completion receipt requirements | present |
| Validator requirements | present |
| Forbidden conclusions | present |

## Done Criteria

```yaml
done_criteria:
  countermodel_slots_mandatory_unless_ddr_waived: true
  local_countermodel_as_program_wide_no_go_forbidden: true
  next_route: "P4-T02"
  physics_delta_allowed: false
  physics_promotion_authorized: false
```

## Validation

Task-local validation is recorded in:

```text
research_control/tasks/RT-20260708-001/artifacts/p4_t01_countermodel_obligation_policy_report.json
```

## Forbidden Conclusions

This receipt and policy do not authorize canonical ontology edit, general
EqSrc discharge, RetainH adoption, GenH adoption, source-law adoption,
matter-coupling derivation, Einstein-equation derivation, benchmark promotion,
Gate Chair verdict, completed derivation, future source-extension
impossibility, or program-wide no-go conclusion.

## Next Route

Run one bounded v18 P4-T02 countermodel-obligation schema and registry
extension packet.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v18* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *Minimal countermodel obligation
policy v1* [Project-control policy].
