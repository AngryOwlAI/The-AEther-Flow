<!-- authority: control -->

# P15-T02 Support-Only Formalization Pilot

Task: `RT-20260704-005`

Pilot target: `fail_closed_missing_certificate_lemma`

Implementation choice: Python typed algebraic spec plus unit tests.

Proof authority: false

Support-only: true

Physics promotion authorized: false

## What Was Implemented

The task-local executable spec in `fail_closed_missing_certificate_pilot.py` models one small kernel:

- certificate slot status: `valid`, `missing`, `malformed`, `target_importing`;
- evaluation result: `valid_certificate` or `bottom`;
- missing-certificate branch: positive identification is not derived;
- declared `RR_E` separation branch: existing declared separation is preserved when two declared source objects are explicitly distinct and separated;
- obstruction branch: `OB-P3T02-MISSING-CERT-RRE-SEPARATION-DATA` is recorded when declared object data are insufficient;
- support-only receipt fields: `proof_authority: false`, `support_only: true`, and `physics_promotion_authorized: false`.

## What Was Not Implemented

This pilot does not formalize the full certificate algebra, identity laws, composition laws, source restriction, general EqSrc, RetainH, GenH, matter semantics, detector semantics, coupling laws, matter coupling, stress-energy semantics, matter action, Einstein equations, benchmark recovery, or completed derivation.

## Test Receipt

The focused unit test command is:

```zsh
.venv/bin/python -m unittest discover -s research_control/tasks/RT-20260704-005/artifacts -p 'test_*.py'
```

The command exercises valid, missing, malformed, target-importing, obstruction, separation-preservation, and support-only receipt branches.

## No-Authority Warning

This executable spec is a support tool. It can help validators and future refuter packets check local fail-closed behavior, but it is not proof authority for project physics and does not promote any scientific status.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation plan continue task v15* [Implementation plan]. `implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.

The AEther-Flow Research Project. (2026b). *P15-T01 proof-assistant pilot scope selector* [Internal control artifact]. `research_control/tasks/RT-20260704-004/artifacts/p15_t01_proof_assistant_pilot_scope_selector.md`.

The AEther-Flow Research Project. (2026c). *Source certificate algebra primitives v1* [Internal draft/control TeX artifact]. `research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex`.

The AEther-Flow Research Project. (2026d). *Source certificate operation laws and fail-closed lemma v1* [Internal draft/control TeX artifact]. `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`.
