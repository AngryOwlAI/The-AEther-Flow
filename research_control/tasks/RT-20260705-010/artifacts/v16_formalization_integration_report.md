<!-- authority: implementation_record -->

# V16 P6-T03 Formalization Integration Report

## Status

This artifact implements v16 P6-T03. It decides how the P6-T02 support-only
executable certificate spec should be used after P6.

Conclusion: keep the executable spec task-local for now. Permit future
Refuter tasks and theorem packets to reuse it as an optional advisory fixture
for certificate-shape and target-import checks. Do not install it as a
standing local CI-equivalent validator until a separate validator packet
defines the minimum payload contract and production validation policy.

This report is process-control integration guidance only. It does not grant
proof authority and it does not change physics status.

## What Was Formalized

P6-T02 formalized a finite/local certificate-record evaluator in Python. The
formalized kernel contains:

- `InstanceKind`;
- `CertificateStatus`;
- `ExpectedEquivalenceResult`;
- `RRESeparationEffect`;
- `NoTargetImportGuard`;
- `CertificateRecord`;
- `EvaluationResult`;
- `evaluate_certificate(record)`.

The evaluator accepts only positive certificate records with valid status,
non-null witness payload, passing no-target guard, no forbidden import flags,
and witness maps whose keys match the declared domain and whose values lie in
the declared codomain. All missing, malformed, target-import,
detector-semantics, process-authority, scoped-evidence, stress-energy,
matter-action, and benchmark branches fail closed.

The executable module also exposes explicit support-only constants:

```python
PROOF_AUTHORITY = False
PHYSICS_PROMOTION_AUTHORIZED = False
SUPPORT_ONLY = True
GENERATED_DERIVATIVE_OR_TEST_SUPPORT_ONLY = True
```

## What Was Not Formalized

P6-T02 did not formalize any of the following:

- existence of certificate records;
- construction of a compatible composition certificate;
- a proof of P5 theorem targets;
- unrestricted equivalence for `EqMS_cert_src_v2`;
- a source law;
- `RR_ETransportCompletenessOrInvarianceLaw_v1`;
- unrestricted `RR_E`;
- matter semantics;
- detector semantics;
- coupling law;
- matter coupling;
- stress-energy semantics;
- matter action;
- Einstein equations;
- exact-GR benchmark promotion;
- Gate Chair verdict;
- completed derivation;
- production validator integration.

The Python evaluator is a finite/local shape checker and fail-closed branch
fixture. It is not a theorem prover and not an ontology source.

## Relation To P4 Instances

P4 supplies the concrete finite/local instance families that motivated the
support-only evaluator:

- P4-T02 supplies `SCI-TRANSPORT-001`, a positive finite/local transport
  certificate instance.
- P4-T03 supplies `SCI-INVARIANCE-001`, a positive finite/local invariance
  certificate instance.
- P4-T04 supplies `SCI-FACTORIZATION-001`, a positive finite/local
  factorization certificate instance.
- P4-T05 supplies negative certificate packets covering missing, malformed,
  target-import, process-authority, scoped-evidence, and related fail-closed
  branches.

P6-T02 directly tested the P4-T02 transport shape and multiple P4-T05
negative shapes. The P4-T03 invariance and P4-T04 factorization instances are
structurally compatible with the positive branch, but P6-T02 did not add
separate positive tests for them. That restraint is correct: P6-T02 was a
pilot and not a complete P4 instance test harness.

## Relation To P5 Theorem Targets

P5-T02 defines certificate-indexed source-equivalence target scaffolding:
source object records, certificate records, validity, generated relations,
theorem targets, and fail-closed evaluation.

P5-T03 proves only a conditional theorem: transitivity holds when a compatible
composition certificate record is explicitly supplied, endpoint compatible,
source-pure, and valid. P5-T03 also records that the stronger claim without
the supplied composition record fails by the
`OB-P5T03-MISSING-COMPATIBLE-COMPOSITION-CERTIFICATE` obstruction.

The P6-T02 evaluator can support future P5-style theorem packets by checking
whether a supplied finite/local certificate record has the expected shape and
forbidden-import flags. It cannot prove that a composition certificate exists,
cannot construct such a certificate, and cannot turn two valid input
certificates into a transitivity proof.

## Local CI-Equivalent Validation Decision

Decision: do not include the P6-T02 executable spec in standing
local CI-equivalent validation yet.

Reasoning:

1. The spec is task-local and intentionally support-only.
2. It has not been promoted through a validator-engineer packet that defines a
   production validation contract.
3. P7-T01 still needs to define the minimum physics payload schema for
   post-v15 physics tasks.
4. P8 still needs route-orbit policy before advisory fixtures become gating
   checks.

Allowed near-term use: future Refuter, theorem, or validator-design packets
may run the P6-T02 tests as optional advisory evidence, provided their
receipts state that the result is not proof authority.

Blocked near-term use: treating the P6-T02 evaluator as a mandatory repository
gate, proof checker, production validator, benchmark gate, or scientific
claim authority.

## How It Helps Detect Target Imports

The evaluator is useful as a small target-import oracle because it makes
forbidden evidence branches explicit:

- `target_import_used`;
- `detector_semantics_used`;
- `stress_energy_used`;
- `matter_action_used`;
- `benchmark_behavior_used`;
- `process_authority_used`;
- `scoped_evidence_used`;
- `NoTargetImportGuard`.

These fields help future packets test whether a proposed certificate record
quietly imports target-side metric, detector, matter-action, benchmark, or
process-authority evidence into a source certificate slot. A future Refuter
task can use the evaluator to generate attack fixtures that should fail
closed.

## Scientific Claims Not Established

This integration report establishes none of the following scientific claims:

- source-law adoption;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption;
- unrestricted `RR_E` theorem status;
- unrestricted `EqMS_cert_src_v2` equivalence;
- source matter semantics;
- detector semantics;
- coupling law;
- matter coupling;
- stress-energy semantics or tensor construction;
- matter action;
- Einstein equations;
- exact-GR benchmark promotion;
- Gate Chair verdict;
- completed derivation;
- impossibility of future source extensions.

Validator PASS, unit-test PASS, role identity, handoff state, registry rows,
approval status, generated derivatives, local cache state, file order, and
commit state remain transaction evidence only.

## Selected Integration Route

Route selected: proceed to P7-T01, `minimum_physics_payload_schema_v16`.

The P6-T02 executable spec should remain task-local until P7 and P8 define the
minimum payload and route-orbit policy that decide when an executable support
spec may become a required validation artifact. After those policies exist, a
separate validator-engineer packet may propose production integration if and
only if it preserves support-only status and explicit no-proof-authority
language.

The logical next step is P7-T01: define the minimum payload schema for
post-v15 physics tasks.
