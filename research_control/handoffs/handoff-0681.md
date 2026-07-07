# Handoff 0681: v18 P1-T04 Repair Active-State Supersession Guard

## Status

Completed: `RT-20260707-012` / `AJ-RT-20260707-012-001`

## Summary

The P1-T04 repair is complete. Active-state sidecar supersession validation now
requires a tracked Director decision registry row and DDR front matter that
explicitly authorizes active-state sidecar supersession with a nonblank scope.

Flag-only authorization from a handoff or `active_state_bifurcation` field is
rejected.

## Next Action

Run one bounded v18 P2-T01 source-equivalence typed-object problem-statement
packet.

## Boundaries

This handoff authorizes no physics promotion, source-law adoption, general
`EqSrc` discharge, `RetainH` adoption, `GenH` adoption, matter-coupling
derivation, Einstein-equation derivation, benchmark promotion, external
outreach, Gate Chair verdict, or completed-derivation claim.
