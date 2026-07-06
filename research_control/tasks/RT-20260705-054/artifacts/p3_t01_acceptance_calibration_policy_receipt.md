<!-- authority: control -->

# P3-T01 Acceptance Calibration Policy Receipt

## Result

`RT-20260705-054` created
`research_control/design/accepted_status_calibration_policy_v1.md`.

The policy requires high-risk accepted/scoped-positive rows to render:

1. Positive status first.
2. Exact scope second.
3. Blocked overread third.

It also forbids treating scoped adoption/evidence/precondition status as
"basically nothing."

## Boundary

This packet changes project-control reporting language only. It does not edit
canonical science sources, adopt a source law, adopt detector semantics, adopt
a coupling law, derive matter coupling, define stress-energy, define matter
action, derive Einstein equations, promote a benchmark, issue a Gate Chair
verdict, or complete the derivation.

## Validator

The task-local validator passed:

```text
.venv/bin/python research_control/tasks/RT-20260705-054/artifacts/validate_p3_t01_acceptance_calibration_policy.py
```

Report path:

```text
research_control/tasks/RT-20260705-054/artifacts/p3_t01_acceptance_calibration_policy_report.json
```

## Next Route

The logical next bounded v17 route is P3-T02: implement machine-readable
acceptance-calibration schema and alias fields while preserving all
physics-promotion blocks.
