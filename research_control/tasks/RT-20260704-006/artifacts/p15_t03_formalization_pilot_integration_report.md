<!-- authority: control -->

# P15-T03 Formalization Pilot Integration Report

Task: `RT-20260704-006`

Decision: `continue_narrow_support_only_lane`

Proof authority: false

Physics promotion authorized: false

## What Was Formalized

P15-T02 formalized one task-local kernel of the fail-closed missing-certificate behavior selected by P15-T01:

- certificate slot states: `valid`, `missing`, `malformed`, and `target_importing`;
- result states: `valid_certificate` and `bottom`;
- missing certificate behavior: no positive identification is derived;
- declared separation behavior: declared `RR_E` separation is preserved when the source record explicitly provides separated objects;
- insufficient-data behavior: the obstruction `OB-P3T02-MISSING-CERT-RRE-SEPARATION-DATA` is recorded;
- support-only receipt behavior: proof authority, support-only status, and physics-promotion authorization are machine-readable.

The formalized unit is useful because it makes the fail-closed branch executable and testable without requiring a new proof-assistant stack or altering canonical science sources.

## What Was Not Formalized

The pilot did not formalize the full source-certificate algebra, operation-law proof system, `EqSrc`, `RetainH`, `GenH`, source-law adoption, `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption, `PositiveMSProfile_v1` adoption, matter semantics, detector semantics, coupling laws, matter coupling, stress-energy semantics, matter action, Einstein equations, benchmark recovery, or completed derivation.

The pilot also did not formalize a general proof kernel for all future tasks. It remained a task-local executable support artifact.

## How It Helps Validators Or Refuters

The pilot helps validators by making a narrow fail-closed invariant runnable:

- a missing certificate cannot silently become a positive identification;
- malformed or target-importing certificate slots return `bottom`;
- declared separation is preserved instead of collapsed;
- insufficient declared object data becomes an explicit obstruction;
- support-only status is visible in the receipt rather than left to prose.

It helps future Refuter packets by providing a compact negative-control fixture pattern. A Refuter can compare a proposed positive route against the executable branches and ask whether the route smuggles target identity, erases declared separation, or treats insufficient source data as a positive result.

## What Scientific Claims It Does Not Establish

The pilot does not establish any of the following:

- source-law adoption;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption;
- unrestricted `RR_E` theorem authority;
- `PositiveMSProfile_v1` adoption;
- `SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- `MetricData(E)` adoption;
- `g_eff` scope change;
- stress-energy semantics;
- stress-energy tensor;
- matter action;
- Einstein equations;
- exact-GR benchmark promotion;
- Gate Chair verdict;
- completed derivation;
- future source-extension impossibility;
- program-wide no-go conclusion.

The support-only executable spec is a validator aid, not a theorem prover for the physics program.

## Continue, Freeze, Or Expand

Recommendation: continue the lane narrowly as `support_only_formalization_pilot`.

Do not freeze the lane. The P15-T02 pilot found a useful, low-risk pattern: small executable kernels can make fail-closed branch behavior concrete and testable.

Do not expand the lane into proof authority or permanent role authority. Expansion would be premature because only one small kernel has been tested. A stronger lane would need multiple successful pilots, a stable artifact schema, and an explicit proof-authority boundary review.

Allowed future use:

- task-local executable specs for small branch invariants;
- local unit tests or validator fixtures;
- support-only receipts with proof authority false;
- Refuter negative controls where the source-side target is narrow and already scoped by tracked control state.

Blocked future use:

- proof authority over physics;
- canonical ontology modification;
- benchmark status promotion;
- route-freeze verdicts;
- source-law adoption;
- downstream matter-coupling or Einstein-equation inference.

## Selected Next Action

Run one bounded v15 P16-T01 red-team scope and packet template.

P16 follows because P15 is now complete: the formalization pilot target was selected, implemented, tested, and integrated as a narrow support-only lane with no physics promotion.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation plan continue task v15* [Implementation plan]. `implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.

The AEther-Flow Research Project. (2026b). *P15-T01 proof-assistant pilot scope selector* [Internal control artifact]. `research_control/tasks/RT-20260704-004/artifacts/p15_t01_proof_assistant_pilot_scope_selector.md`.

The AEther-Flow Research Project. (2026c). *P15-T02 support-only formalization pilot* [Internal control artifact]. `research_control/tasks/RT-20260704-005/artifacts/p15_t02_formalization_pilot_report.md`.
