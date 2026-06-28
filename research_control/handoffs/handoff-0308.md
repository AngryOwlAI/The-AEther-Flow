<!-- authority: control -->

# Handoff 0308

## Summary

P6-T01 defined payload-density and route-orbit diagnostics in:

- `research_control/tasks/RT-20260614-275/artifacts/p6_t01_payload_density_metrics_design.md`

The design defines all fifteen required metrics from the v11 plan, including
tasks since Distance-to-GR delta, tasks since burden discharge, payload items
per task and cycle, selector cycles without new payload, same-burden
repetition, freeze reviews, bridge attempts, obstruction creation/reuse,
construct-audit-stress-selector cycles, gate-ready cycles without Gate Chair
verdict, support-only tooling reports, and physics-promotion authorization
counts.

It also defines advisory warning thresholds. Warnings are not hard validation
gates and are not physics evidence.

## Boundary

This packet is project-control design only. It does not implement
`report_physics_progress_metrics.py`, does not modify `continue_research.py`,
does not alter Distance-to-GR status, and does not promote any physics claim.

Payload-density and route-orbit diagnostics may read science-result receipt
fields, but they remain operational diagnostics. They are not source-law
adoption, not `MetricData(E)` adoption, not `g_eff` adoption or scope
expansion, not matter coupling, not stress-energy semantics, not Einstein
equations, not benchmark promotion, and not completed derivation.

## Next Action

Run one bounded P6-T02 `validator-engineer@0.2.0` packet.

The next packet should implement the design in
`scripts/research_control/report_physics_progress_metrics.py`, add focused
tests, preserve the separation guard, and keep diagnostic warnings advisory.
