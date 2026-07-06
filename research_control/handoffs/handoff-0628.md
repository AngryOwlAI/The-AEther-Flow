<!-- authority: control -->

# Handoff 0628

## Summary

`RT-20260705-055` completed one bounded v17 P3-T02 accepted-status calibration
schema and alias-update packet.

It created:

```text
research_control/design/accepted_status_calibration_schema_v1.md
research_control/design/accepted_status_calibration_v1.yaml
```

It also added matching `acceptance_calibration` metadata to:

```text
research_control/design/distance_to_gr_status_aliases.yaml
```

The packet covers `m_src`, `g_eff`, and `matter_coupling`. Existing
reader-facing alias behavior remains intact. The new fields are structured
metadata for future renderers and linters.

This is a project-control schema result. It is not canonical ontology
adoption, source-law adoption, detector semantics, coupling-law adoption,
matter coupling, stress-energy semantics, matter action, Einstein equations,
benchmark promotion, Gate Chair verdict, or completed derivation.

## Next Action

Run one bounded v17 P3-T03 claim-language linter underclaim calibration
packet. The packet should add advisory warnings for high-risk rows that bury
positive scoped status or use "basically nothing" language while preserving the
existing overclaim hard gates.

## Boundary

The next packet may implement linter warning behavior from the P3-T02
calibration fields. It must not weaken existing hard overclaim checks, alter
the Distance-to-GR ledger, or promote any physics claim.
