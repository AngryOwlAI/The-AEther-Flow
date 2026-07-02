<!-- authority: control -->

# Handoff 0517

## Summary

`RT-20260702-064` completed one bounded v15 P3-T02
`ontology-formalizer@0.2.0` packet. It created the draft/control TeX artifact
`source_certificate_operation_laws_v1.tex`.

## Result

The packet states and resolves the P3-T02 targets:

- identity certificate preservation is proved only inside declared source
  scope;
- compatible certificate composition is proved source-side under valid input
  hypotheses;
- source restriction is proved source-side for declared source subdomains;
- malformed certificates fail closed;
- missing certificates preserve declared `RR_E` separation when the source
  records contain it, otherwise the named obstruction
  `OB-P3T02-MISSING-CERT-RRE-SEPARATION-DATA` applies;
- target-importing certificates are invalid and fail closed.

## Boundary

P3-T02 does not adopt source law,
`RR_ETransportCompletenessOrInvarianceLaw_v1`, `PositiveMSProfile_v1`,
`SourceMatterSemanticsAdoptionReadinessLaw_v1`, matter semantics, detector
semantics, a coupling law, matter coupling, `MetricData(E)`, `g_eff`,
stress-energy semantics, a matter action, Einstein equations, benchmark
status, or completed derivation.

The operation laws do not erase the P2 certificate-gap witness. Missing or
malformed concrete certificates remain fail-closed.

## Next Action

Run one bounded v15 P3-T03 certificate checklist integration packet. The
packet should turn the P3-T01 primitives and P3-T02 operation laws into an
explicit pass/fail checklist before P4 matter-coupling dependency DAG or
semantic-layer split work.

## Validation

Validation receipts are recorded in
`research_control/tasks/RT-20260702-064/jobs/completions/AJC-AJ-RT-20260702-064-001.yaml`.
The handoff YAML is the machine-readable continuation authority.
