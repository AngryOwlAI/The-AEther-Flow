<!-- authority: control -->

# Handoff 0629

## Summary

`RT-20260705-056` completed one bounded v17 P3-T03 claim-language linter
underclaim calibration packet.

It updated:

```text
scripts/project_control/validate_claim_language.py
research_control/design/claim_language_linter_taxonomy.yaml
tests/test_validate_claim_language.py
```

It added:

```text
tests/fixtures/claim_language/accepted_underclaim_overcorrection.md
tests/fixtures/claim_language/accepted_calibrated_valid.md
```

The linter now emits advisory `underclaim_calibration_warning` findings for
high-risk accepted/scoped-positive status summaries that bury positive status
under caveat walls or minimize scoped status as basically nothing.

Existing overclaim checks remain hard failures. The JSON report now separates
`overclaim_hard_fail_count`, `underclaim_calibration_warning_count`, and
`finding_kind_counts`.

This is a project-control validator result. It is not canonical ontology
adoption, source-law adoption, detector semantics, coupling-law adoption,
matter coupling, stress-energy semantics, matter action, Einstein equations,
benchmark promotion, Gate Chair verdict, or completed derivation.

## Next Action

Run one bounded v17 P3-T04 renderer update for positive-first status cards.
The packet should update the frontier and compact-frontier renderers to use the
P3-T02 calibration metadata and P3-T03 warning semantics without weakening
existing claim boundaries.

## Boundary

The next packet may implement renderer behavior for positive-first status
cards. It must not alter the Distance-to-GR ledger, promote any physics claim,
or treat generated renderer output as proof authority.
