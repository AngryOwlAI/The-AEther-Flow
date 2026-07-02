<!-- authority: control -->

# Source Certificate Algebra Checklist

## Status

This checklist implements v15 P3-T03. It is a project-control validation
surface for certificate-bearing research packets. It does not prove a physics
claim, adopt a source law, authorize matter semantics, authorize detector
semantics, authorize matter coupling, authorize stress-energy semantics,
authorize matter action, derive Einstein equations, promote benchmark status,
or complete a derivation.

## Scope

Use this checklist when a theorem, audit, stress test, selector output, or
handoff relies on source certificates from the P3 certificate algebra.

The checklist is subordinate to the registered science/control sources:

- `source_certificate_algebra_primitives_v1.tex`
- `source_certificate_operation_laws_v1.tex`
- the active claim-boundary registry rows
- the active continue-research handoff

Generated wiki notes, semantic extracts, validators, registries, roles,
approvals, commits, and local caches are not mathematical certificate data.

## Required Certificate Record

Every positive source certificate claim must identify:

- certificate kind: source transport, source invariance, or source
  factorization;
- declared source object indices;
- declared source domain;
- declared source codomain;
- source witness payload;
- source validity guard;
- declared source scope;
- fail-closed branch if the record is missing, malformed, or target-importing.

If any required field is absent, the certificate slot is missing or malformed.
The attempted positive use fails closed.

## Pass/Fail Checklist

| Check | Pass condition | Fail-closed result |
| --- | --- | --- |
| Missing certificate | An explicit certificate record is present for the declared use. | No declared-object equivalence, no `RR_E` identification, and record the relevant certificate-gap obstruction. |
| Malformed certificate | All required source fields are present, compatible, and source-side. | Evaluation returns bottom and no positive theorem or downstream claim follows. |
| Detector-semantics certificate | Detector semantics are not used as certificate fields or proof premises. | The attempted certificate is invalid and cannot supply source certificate validity. |
| Target-metric certificate | Target metric, target topology, target atlas, and proper time are not used as certificate fields or proof premises. | The attempted certificate is invalid and cannot supply source certificate validity. |
| Benchmark-behavior certificate | Benchmark behavior, benchmark recovery, or Gate Chair closure is not used as certificate data. | The attempted certificate is invalid and cannot supply source certificate validity. |
| Source transport certificate | Transport witness maps declared source indices, labels, guards, and record positions only inside the declared source scope. | Missing or incompatible fields fail closed. |
| Source invariance certificate | Invariance witness states source relabeling, variation, or local comparison only inside the declared source scope. | Missing or incompatible fields fail closed. |
| Source factorization certificate | Factorization witness names an explicit declared source factorization object. | Missing, changed, or target-supplied factorization object fails closed. |

## Linter Fixture Contract

The claim-language linter must catch certificate overreads on current control
or public surfaces. The required bad fixture phrases are:

- forbidden phrase: missing certificate proves declared-object equivalence;
- forbidden phrase: missing certificate identifies RR_E;
- forbidden phrase: malformed certificate proves declared-object equivalence;
- forbidden phrase: malformed certificate proves matter semantics;
- forbidden phrase: detector-semantics certificate supplies source certificate validity;
- forbidden phrase: target-metric certificate supplies source certificate validity;
- forbidden phrase: benchmark-behavior certificate supplies source certificate validity.

Correct source-side wording must pass:

- a valid source transport certificate maps declared source indices only
  inside declared source scope;
- a valid source invariance certificate preserves declared source data only
  inside declared source scope;
- a valid source factorization certificate factors through an explicit
  declared source object only inside declared source scope.

## Template Hook

Certificate-bearing theorem packets must include a checklist receipt naming
which rows above passed, which rows failed closed, and which obstruction IDs
were recorded. A missing checklist receipt prevents the packet from being
used as support for stronger downstream routing.

## Non-Conclusions

Passing this checklist is workflow evidence only. It is not proof authority.
It does not adopt `RR_ETransportCompletenessOrInvarianceLaw_v1`,
`PositiveMSProfile_v1`, `SourceMatterSemanticsAdoptionReadinessLaw_v1`,
matter semantics, detector semantics, a coupling law, matter coupling,
stress-energy semantics, stress-energy tensor, matter action, Einstein
equations, benchmark status, or completed derivation.

## Machine-Readable Checklist

```yaml
source_certificate_algebra_checklist:
  schema_id: "source_certificate_algebra_checklist_v1"
  status: "draft/control"
  certificate_record_required: true
  missing_certificate_fails_closed: true
  malformed_certificate_fails_closed: true
  detector_semantics_certificate_invalid: true
  target_metric_certificate_invalid: true
  benchmark_behavior_certificate_invalid: true
  valid_source_transport_allowed: true
  valid_source_invariance_allowed: true
  valid_source_factorization_allowed: true
  linter_fixture_required: true
  template_receipt_required: true
  physics_promotion_authorized: false
  proof_authority: false
```
