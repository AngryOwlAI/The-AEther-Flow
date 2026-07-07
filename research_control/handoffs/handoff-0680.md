# Handoff 0680: v18 P1-T04 Active-State Bifurcation Red-Team Review

## Status

Completed: `RT-20260707-011` / `AJ-RT-20260707-011-001`

## Summary

P1-T04 reviewed the active-state bifurcation for route confusion and authority
laundering. Current rendered surfaces identify the latest research handoff and
sidecar fields, and generated frontier wording remains non-authoritative as
written.

Repair is required because the validator can accept sidecar supersession
authorization from a handoff-level or bifurcation-level flag without verifying
the explicit tracked Director decision required by
`research_control/design/active_state_bifurcation_policy_v1.md`.

## Next Action

Run one bounded v18 P1-T04 repair task to require tracked Director-decision
authorization before any project-system sidecar may supersede ordinary
research handoff authority.

## Boundaries

This handoff authorizes no physics promotion, source-law adoption, general
`EqSrc` discharge, `RetainH` adoption, `GenH` adoption, matter-coupling
derivation, Einstein-equation derivation, benchmark promotion, external
outreach, Gate Chair verdict, or completed-derivation claim.

P2-T01 remains pending until the repair route passes.
