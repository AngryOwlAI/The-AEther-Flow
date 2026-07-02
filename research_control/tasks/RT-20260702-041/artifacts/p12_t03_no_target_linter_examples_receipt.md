---
authority: control
task_id: "RT-20260702-041"
job_id: "AJ-RT-20260702-041-001"
created_at: "2026-07-02T12:37:27Z"
---

# P12-T03 No-Target Linter And Examples Receipt

## Result

P12-T03 integrated no-target certificate hygiene into the deterministic
claim-language guardrail layer.

Implemented surfaces:

- `research_control/design/claim_language_linter_taxonomy.yaml`
- `research_control/design/scoped_claim_language_examples.md`
- `tests/test_validate_claim_language.py`
- `tests/fixtures/claim_language/no_target_certificate_overread.md`
- `research_control/tasks/RT-20260702-041/artifacts/validate_p12_t03_no_target_linter_examples.py`
- `research_control/tasks/RT-20260702-041/artifacts/p12_t03_no_target_linter_examples_report.json`

## Acceptance Evidence

- The no-target overread fixture produces five hard failures on a current
  control surface.
- Corrected `source_hygiene_certificate_only` wording produces no no-target
  linter findings.
- The examples pack contains bad and corrected no-target certificate wording.
- The taxonomy stores patterns for positive matter semantics, detector
  semantics, stress-energy semantics, matter action, benchmark recovery, and
  proof-authority overreads.
- The public-surface audit scanned README, GitHub-facing explainers,
  publication briefs, HTML explainer specs, and current frontier with zero
  no-target hard failures.

## Validation Commands

- `.venv/bin/python -m unittest tests.test_validate_claim_language`
- `.venv/bin/python research_control/tasks/RT-20260702-041/artifacts/validate_p12_t03_no_target_linter_examples.py --output research_control/tasks/RT-20260702-041/artifacts/p12_t03_no_target_linter_examples_report.json --json`
- `git diff --check`

## Claim Boundary

This receipt is validator evidence only. It does not establish positive matter
semantics, detector semantics, stress-energy semantics, matter action,
benchmark recovery, proof authority, Einstein equations, benchmark promotion,
or completed derivation.

## Next Route

Run one bounded v14 P12-T04 no-target hygiene phase validation packet.
