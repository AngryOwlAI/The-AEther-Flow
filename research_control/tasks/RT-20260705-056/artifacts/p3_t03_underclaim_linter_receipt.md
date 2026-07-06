<!-- authority: control -->

# P3-T03 Underclaim Linter Receipt

## Summary

`RT-20260705-056` implements v17 P3-T03 as a project-control validator update.
It adds advisory underclaim calibration warnings to the claim-language linter
without weakening existing overclaim hard failures.

## Implemented Advisory Classes

- `accepted_positive_status_missing`
- `accepted_scope_after_blocked_overread`
- `scoped_adoption_minimized`
- `caveat_wall_public_summary`

## Report Separation

The linter report now includes:

- `overclaim_hard_fail_count`
- `underclaim_calibration_warning_count`
- `finding_kind_counts`

Individual findings include `finding_kind`, allowing consumers to distinguish
`overclaim_hard_fail` from `underclaim_calibration_warning`.

## Validation

The task-local validator report is:

```text
research_control/tasks/RT-20260705-056/artifacts/p3_t03_underclaim_linter_report.json
```

Validator status: `PASS`.

Focused unit test command:

```text
.venv/bin/python -m unittest tests.test_validate_claim_language
```

Result: `PASS` with 30 tests.

## Boundary

This packet is a validator-calibration update only. It does not change any
physics source, Distance-to-GR ledger row, source law, detector semantics,
coupling-law status, matter-coupling status, Einstein-equation status,
benchmark status, Gate Chair verdict, or completed-derivation status.
