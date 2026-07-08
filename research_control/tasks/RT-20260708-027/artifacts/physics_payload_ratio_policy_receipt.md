<!-- authority: control -->

# P8-T01 Physics-Payload Ratio Policy Receipt

## Summary

RT-20260708-027 completed the v18 P8-T01 project-control packet by creating
`research_control/design/physics_payload_ratio_policy_v1.md`.

The policy defines an advisory three-project-system-task threshold after which
the Director should prefer a physics-bearing packet unless a tracked exception
applies. It defines process orbit, route orbit, helpful support work, and
avoidance behavior. It lists the allowed physics-bearing next-task classes,
the allowed exceptions, and the advisory evaluation record expected by P8-T02
and P8-T03.

## Done Criteria

- Process orbit is defined.
- Route orbit is defined and related to existing route-orbit policies.
- Helpful support work is distinguished from avoidance behavior.
- `after_project_system_tasks: 3` is recorded.
- Required next-task classes are listed.
- Exceptions are listed.
- Initial enforcement is `advisory`.
- The next route is P8-T02.

## Boundary

This packet creates no physics delta. The policy is not proof authority, not
validator enforcement, not a standing global gate, not source-law adoption,
not detector-semantics adoption, not matter-coupling derivation, not
Einstein-equation derivation, not benchmark promotion, not a Gate Chair
verdict, and not completed derivation.

## Relationship To Prior Control Sources

The new policy complements:

- `research_control/design/minimum_physics_payload_schema_v1.md`, which
  defines payload classes.
- `research_control/design/route_orbit_gating_policy_v16.md`, which evaluates
  repeated route behavior.
- `research_control/design/route_orbit_freeze_threshold_policy_v1.md`, which
  defines freeze-review thresholds.

P8-T01 does not modify those sources. It adds the project-system run-length
handoff rule that returns support work toward physics-bearing continuation.

## Next Route

The next bounded continuation packet is P8-T02
`route_history_payload_ratio_metrics`, which should extend route-history
metrics to compute project-system run length and physics-payload ratio.
