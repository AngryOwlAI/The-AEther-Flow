<!-- authority: control -->

# P8-T03 Payload-Ratio Validator Pilot Report

## Summary

P8-T03 added an advisory `physics_payload_ratio_policy_v1` validator pilot to
`scripts/research_control/validate_research_control.py`.

The validator consumes explicit `physics_payload_ratio_policy_record` receipts
when present in completions or handoffs. It emits warning records for advisory
process-orbit conditions and reserves hard errors for process/support tasks
that claim a physics delta.

## Initial Finding Classes

| Finding | Severity | Result |
| --- | --- | --- |
| `project_system_run_exceeds_threshold` | `warn_current_control` | Implemented as a warning when the project-system run meets the threshold. |
| `physics_payload_missing_after_threshold` | `warn_current_control` | Implemented as a warning when no exception is active and the selected next task is not physics-bearing. |
| `exception_declared_without_evidence` | `warn_current_control` | Implemented as a warning when an exception is unsupported or lacks evidence. |
| `process_task_claims_physics_delta` | `overclaim_hard_fail` | Implemented as a hard validation error when a process task claims a physics delta. |

## Fixture Coverage

The focused fixture suite under `tests/fixtures/physics_payload_ratio/` covers:

- below-threshold non-applicability;
- project-system threshold warnings;
- exception-without-evidence warnings;
- security/integrity repair exception pass behavior;
- process-task physics-delta overclaim hard failure behavior.

## Claim Boundary

This pilot is project-control validation only. It is not proof authority,
physics truth ranking, physics promotion, source-law adoption,
detector-semantics adoption, matter-coupling derivation, Einstein-equation
derivation, benchmark promotion, a Gate Chair verdict, or completed derivation
evidence.

## Next Route

The next bounded continuation packet is P8-T04
`physics_payload_ratio_dashboard_integration`.
