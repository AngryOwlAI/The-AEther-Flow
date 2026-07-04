<!-- authority: control -->

# P15-T01 Proof-Assistant Pilot Scope Selector

## Status

Task: `RT-20260704-004`

Selected pilot target: `fail_closed_missing_certificate_lemma`

Status: completed

Proof authority: false

Physics promotion authorized: false

Support-only: true

## Selection Result

P15-T01 selects exactly one pilot target for P15-T02: formalize the fail-closed missing-certificate lemma.

The target kernel is:

> If a required source certificate slot is missing, a positive certificate-mediated identification is not derived; existing declared separation is preserved when available, otherwise the formal branch records the missing-certificate obstruction.

This selection is support-only. It does not prove a project physics claim, adopt a source law, derive matter coupling, derive Einstein equations, promote benchmark status, or complete the derivation.

## Candidate Review

| Candidate target | Judgment | Reason |
| --- | --- | --- |
| certificate algebra identity/composition | deferred | Useful but broader than the smallest fail-closed kernel. |
| fail-closed missing-certificate lemma | selected | Small, already source-backed by P3, directly supports validators and theorem-packet discipline, and naturally encodes a negative branch. |
| finite RR_E separation witness | deferred | Useful but requires more object-specific witness design. |
| no-target certificate sanity checker | deferred | Useful as a linter target, but P15-T02 should first formalize the missing-certificate kernel it would check. |
| source-equivalence relation properties | deferred | Broader than a first pilot. |
| route-signature schema invariants | deferred | Useful operationally, but less connected to V15-R12 certificate algebra and V15-R15 countermodel discipline. |

## P15-T02 Implementation Recommendation

Recommended route: `validator-engineer@0.2.0` unless the operator finds an already-supported proof assistant requiring no broad dependency work.

Recommended implementation choice: Python typed algebraic spec plus unit tests.

Minimum P15-T02 artifact should encode:

- certificate slot status: valid, missing, malformed, target-importing;
- evaluation result: valid certificate or bottom;
- missing-certificate branch: no positive identification;
- existing declared RR_E separation preserved when explicit declared source objects differ;
- obstruction branch when declared object data are insufficient;
- proof authority false and support-only status.

## Non-Conclusions

This selector does not formalize the whole certificate algebra. It does not certify matter semantics, detector semantics, coupling laws, matter coupling, stress-energy semantics, matter action, Einstein equations, benchmark recovery, or completed derivation. It selects one support-only kernel for local formalization discipline.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation plan continue task v15* [Implementation plan]. `implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.

The AEther-Flow Research Project. (2026b). *Source certificate algebra primitives v1* [Internal draft/control TeX artifact]. `research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex`.

The AEther-Flow Research Project. (2026c). *Source certificate operation laws and fail-closed lemma v1* [Internal draft/control TeX artifact]. `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`.

The AEther-Flow Research Project. (2026d). *Source certificate algebra checklist* [Internal control note]. `research_control/design/source_certificate_algebra_checklist.md`.
