# V16 P6-T02 Support-Only Executable Certificate Spec

## Status

This artifact implements v16 P6-T02. It creates a task-local Python typed
algebraic spec plus `unittest` coverage for the P6-T01 selected target:
`certificate record type and validity predicate`.

The implementation is support-only. It is not proof authority. It does not
adopt a source law, `RR_ETransportCompletenessOrInvarianceLaw_v1`, an
unrestricted `RR_E` theorem, matter semantics, detector semantics, a coupling
law, matter coupling, stress-energy semantics, matter action, Einstein
equations, benchmark status, Gate Chair verdict, or completed derivation.

## Source Files

- `research_control/tasks/RT-20260705-009/artifacts/support_only_certificate_spec_v16.py`
- `research_control/tasks/RT-20260705-009/artifacts/test_support_only_certificate_spec_v16.py`

## Formalized Kernel

The Python module formalizes the following finite/local support objects:

- `InstanceKind`
- `CertificateStatus`
- `ExpectedEquivalenceResult`
- `RRESeparationEffect`
- `NoTargetImportGuard`
- `CertificateRecord`
- `EvaluationResult`
- `evaluate_certificate(record)`

The evaluator returns `declared_equivalence_allowed` only for positive records
that meet all of these conditions:

1. Positive instance kind.
2. `status: valid`.
3. Non-null witness payload.
4. No-target import guard passes.
5. No target, detector-semantics, stress-energy, matter-action, benchmark, or
   process-authority import flags.
6. Witness-map keys match the declared domain and witness-map values lie in the
   declared codomain.

Every negative branch returns `declared_equivalence_blocked` and a fail-closed
classification.

## Required Behaviors Covered

| Required behavior | Implementation status |
| --- | --- |
| certificate record | `CertificateRecord` dataclass |
| status field | `CertificateStatus` enum |
| valid/missing/malformed states | positive branch, missing branch, malformed/mismatch branches |
| domain/codomain matching | `_witness_map_matches` |
| no-target guard | `NoTargetImportGuard` and guard failure branch |
| target-import rejection | `EvaluationKind.TARGET_IMPORT` |
| process-authority rejection | `EvaluationKind.PROCESS_AUTHORITY` |
| scoped evidence not filling certificate slots | `EvaluationKind.SCOPED_EVIDENCE_NOT_CERTIFICATE` |
| expected equivalence result | `ExpectedEquivalenceResult` in every `EvaluationResult` |
| fail-closed result | negative branches return `fail_closed: True` |

## Test Coverage

The unit test file covers:

- one positive transport certificate record mapped to P4-T02
  `SCI-TRANSPORT-001`;
- missing certificate payload mapped to P4-T05 `SCI-NEG-MISSING-001`;
- malformed domain/codomain mismatch mapped to P4-T05
  `SCI-NEG-MALFORMED-001`;
- target metric import mapped to P4-T05 `SCI-NEG-TARGET-METRIC-001`;
- process-authority import mapped to P4-T05
  `SCI-NEG-VALIDATOR-PASS-001`;
- scoped evidence treated as a certificate slot mapped to P4-T05
  `SCI-NEG-SCOPED-EVIDENCE-001`.

This exceeds the P6-T02 minimum of one positive and three negative tests.

## Mapping to P4/P5

P4-T02, P4-T03, and P4-T04 are positive finite/local examples. The P6-T02
pilot directly tests the transport shape and leaves invariance and
factorization as structurally compatible positive branches for later reuse.

P4-T05 supplies fail-closed negative examples. The P6-T02 tests cover missing,
malformed, target-import, process-authority, and scoped-evidence branches.

P5-T03 records that two valid input certificates do not fill the separate
compatible composition certificate slot. The P6-T02 scoped-evidence and missing
branches preserve that principle: process evidence, scoped evidence, and absent
payloads cannot supply certificate data.

## No-Authority Warning

The module exposes:

```python
PROOF_AUTHORITY = False
PHYSICS_PROMOTION_AUTHORIZED = False
SUPPORT_ONLY = True
GENERATED_DERIVATIVE_OR_TEST_SUPPORT_ONLY = True
```

These constants are receipt-facing guardrails. They do not themselves create
authority. They make explicit that this pilot is executable support
infrastructure only.

## Done Criteria

- The pilot runs locally under `unittest`.
- Tests cover one positive and five negative cases.
- The completion receipt records that the pilot does not prove project physics
  claims.

## Next Route

Run P6-T03 as one bounded formalization integration report. It should decide
whether this pilot should remain task-local, be reused by future Refuter tasks,
or be proposed for a later repository validator under a separate authorized
packet.
