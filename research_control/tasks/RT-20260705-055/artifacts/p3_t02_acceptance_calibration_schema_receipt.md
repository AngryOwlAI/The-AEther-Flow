<!-- authority: control -->

# P3-T02 Acceptance Calibration Schema Receipt

## Summary

`RT-20260705-055` executed one bounded v17 P3-T02 project-control packet. It
created `research_control/design/accepted_status_calibration_schema_v1.md`,
created `research_control/design/accepted_status_calibration_v1.yaml`, and
added matching `acceptance_calibration` metadata to
`research_control/design/distance_to_gr_status_aliases.yaml`.

The packet covers the required high-risk objects:

```text
m_src
g_eff
matter_coupling
```

## Result

The schema and YAML provide machine-readable fields for positive status, exact
scope, allowed use, blocked overread, underclaim guard, overclaim guard, public
summary compression, full control blocked items, evidence source, and
`no_physics_delta`.

Existing reader-facing alias display values remain in place. The new
calibration blocks are metadata for future renderers and linters.

## Boundary

This receipt records no Distance-to-GR ledger update and no physics delta. It
does not authorize source-law adoption, detector semantics, coupling-law
adoption, matter-coupling derivation or adoption, stress-energy semantics,
matter action, Einstein equations, benchmark promotion, Gate Chair verdict, or
completed derivation.

## Verification

```text
.venv/bin/python research_control/tasks/RT-20260705-055/artifacts/validate_p3_t02_acceptance_calibration_schema.py
```

Result: `PASS`.

## Next Route

The next lawful v17 continuation is P3-T03:

```text
claim-language linter underclaim calibration
```
