---
receipt_id: "P9-T04-status-card-v2-linter-receipt"
task_id: "RT-20260708-035"
job_id: "AJ-RT-20260708-035-001"
plan_task_id: "P9-T04"
status: "PASS"
authority: "control"
---

# P9-T04 Status-Card v2 Linter Receipt

## Scope

RT-20260708-035 implements the v18 P9-T04 validator-only packet. The work adds
focused claim-language linter coverage for status-card v2 summaries that omit
the required next-burden statement and preserves advisory caveat-wall warnings.

This packet does not edit canonical science sources, alter the Distance-to-GR
ledger, adopt source laws, derive matter coupling, derive Einstein equations,
promote benchmarks, or issue a Gate Chair verdict.

## Evidence

- `tests/fixtures/claim_language/status_card_v2_valid.md` passes without findings.
- `tests/fixtures/claim_language/status_card_v2_missing_next_burden.md` emits
  `status_card_v2_missing_next_burden` as an advisory
  `underclaim_calibration_warning`.
- `tests/fixtures/claim_language/status_card_v2_caveat_wall.md` emits
  `caveat_wall_public_summary` as an advisory warning.
- The explicit `GR derived` status-card v2 overclaim still hard-fails as
  `einstein_equation_overclaim`.

## Validation

- `.venv/bin/python -m unittest tests.test_validate_claim_language` passed.
- `.venv/bin/python research_control/tasks/RT-20260708-035/artifacts/validate_p9_t04_status_card_v2_linter.py --write-report --json` passed.

The JSON evidence report is:

- `research_control/tasks/RT-20260708-035/artifacts/p9_t04_status_card_v2_linter_report.json`

## Claim Boundary

- Physics promotion authorized: false.
- Scientific claims changed: false.
- Source-law adoption: false.
- Detector semantics adoption: false.
- Coupling-law adoption: false.
- Matter coupling derived or adopted: false.
- Stress-energy semantics imported: false.
- Matter action imported: false.
- Einstein equations derived: false.
- Benchmark promoted: false.
- Gate Chair verdict issued: false.
- Completed derivation claimed: false.

## Next Route

The immediate next lawful v18 route is P9-T05, issue-report appendix guidance,
under the live tracked continuation process.
