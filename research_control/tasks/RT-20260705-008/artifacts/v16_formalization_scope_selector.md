# V16 P6-T01 Formalization Scope Selector

## Question

Which single bounded formalization target should P6-T02 implement as a
support-only executable or proof-checkable pilot?

## Inputs

- P3 defined source certificate records, statuses, composition, restriction,
  malformed certificates, missing certificates, target-import invalidity, and
  fail-closed behavior as draft/control source-side controls.
- P4 supplied finite/local positive transport, invariance, and factorization
  instances plus negative missing, malformed, target-import,
  detector-semantics, process-authority, stress-energy, validator-pass, and
  scoped-evidence examples.
- P5 separated definition from theorem content and showed that transitivity
  needs a supplied valid compatible composition certificate.
- P6-T02 requires an executable support-only spec with at least one positive
  and three negative cases and no project-physics proof authority.

## Candidate Target Evaluation

| Candidate target | Decision | Reason |
| --- | --- | --- |
| certificate record type and validity predicate | selected | This is the smallest shared kernel for positive instances, negative fail-closed instances, the P5 missing-composition obstruction, and later P14 attack fixtures. |
| transport certificate finite check | not selected | Useful positive case, but narrower than the common evaluator required by P6-T02. |
| invariance certificate finite check | not selected | Useful positive case, but narrower than the common evaluator required by P6-T02. |
| factorization certificate finite check | not selected | Useful positive case, but narrower than the common evaluator required by P6-T02. |
| missing/malformed certificate fail-closed evaluator | not selected | Required behavior for P6-T02, but selecting only this branch would under-cover positive validity and target/process rejection. |
| target-import rejection evaluator | not selected | Important negative case, but should be one test branch of the common evaluator rather than the whole scope. |
| transitivity under compatible composition | not selected | Mathematically interesting after P5-T03, but heavier than the P6-T02 finite/local record kernel and risks theorem overread. |
| route-signature minimum payload gate | not selected | Belongs to P7 payload/orbit gating, not P6 certificate formalization. |
| compact frontier schema validation | not selected | Belongs to P15 compact current-frontier work, not P6 certificate formalization. |

## Selected Target

```text
certificate record type and validity predicate
```

P6-T02 should model a finite/local certificate record with:

- certificate id and kind;
- declared source domain and codomain;
- status field;
- source-only witness payload;
- no-target guard;
- expected equivalence result;
- fail-closed reason;
- import booleans for target, detector semantics, stress-energy, matter action,
  benchmark behavior, and process authority;
- forbidden-overread metadata.

The validity predicate should return a support-only classification, not a
physics theorem. Required result classes are:

- `declared_equivalence_allowed` for valid finite/local positive records;
- `declared_equivalence_blocked` for missing, malformed, target-import,
  detector-semantics, process-authority, scoped-evidence, stress-energy,
  matter-action, or benchmark-dependent records;
- a fail-closed reason for every blocked record.

## Selected Toolchain

```text
Python typed algebraic spec plus unittest
```

This toolchain is selected because it:

- is already locally supported by repository validation practice;
- adds no new dependency;
- can encode finite/local records with enums or dataclasses;
- can run deterministic positive and negative tests in one bounded packet;
- is easy for later validators and Refuter packets to consume;
- has no proof-authority implication.

Lean, Coq, Isabelle, and Agda are not selected for this packet because the
target is a finite record evaluator rather than a proof of an algebraic
theorem, and adding a proof-assistant dependency would raise process risk
without increasing the support-only value of P6-T02.

## P6-T02 Handoff

Recommended next role:

```text
validator-engineer@0.2.0
```

Recommended next task:

```text
support_only_executable_certificate_spec_v16
```

Minimum P6-T02 behavior:

1. Implement a small typed executable model of the selected record and
   validity predicate.
2. Cover at least one valid positive certificate and at least three negative
   cases.
3. Include missing, malformed, target-import, process-authority, and
   scoped-evidence fail-closed behavior when feasible inside one bounded task.
4. State that the pilot is support-only and proves no project physics claim.
5. Map tests back to P4 positive and negative instances and the P5-T03
   missing-composition obstruction.

## Theoretical Decision Output

- `selected_next_packet_type`:
  `bounded_theoretical_calculation`
- `selected_next_role_family`:
  `validator-engineer@0.2.0`
- `decision_basis`:
  P6-T02 asks for an executable support-only certificate spec. The certificate
  record type and validity predicate are the narrowest reusable target that
  can cover valid and fail-closed cases without theorem overread.
- `theoretical_method`:
  candidate-target exclusion by finite/local scope, executable feasibility,
  validator usefulness, P4/P5 coverage, and overread-risk minimization.
- `preserves_claim_blocks`:
  true
- `requires_human_gate`:
  false
- `human_gate_reason`:
  no human gate is required because the selected target is support-only
  executable validation infrastructure and does not adopt ontology, source
  law, matter semantics, detector semantics, coupling law, matter coupling,
  GR equations, benchmark status, or completed derivation.

## Distance-to-GR Effect

No Distance-to-GR ledger row changes. P6-T01 selects a support-only executable
target and toolchain. It does not discharge matter coupling or any downstream
GR burden.

## Forbidden Conclusions

This selector does not imply source-law adoption,
`RR_ETransportCompletenessOrInvarianceLaw_v1` adoption, unrestricted `RR_E`
theorem status, matter-semantics adoption, detector-semantics adoption,
coupling-law adoption, matter-coupling derivation or adoption, stress-energy
semantics, matter action, Einstein equations, benchmark promotion, Gate Chair
verdict, completed derivation, global no-go status, or proof authority for any
generated derivative or validator result.
