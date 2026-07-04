<!-- authority: control -->

# Parent Fusion Notes: Certificate Instance Schema

## Summary

The child perspectives agree that P4-T01 must define a finite/local
source-certificate instance record, not construct the P4 instances themselves.
The fused design schema therefore fixes the required fields, allowed instance
kinds, status vocabularies, positive and negative requirements, and a
support-only validation contract.

## Fusion Result

The fused output is:

```text
research_control/design/source_certificate_instance_library_schema_v1.md
```

The mathematical child contributed the typed record grammar, enum domains,
positive-instance requirements, and fail-closed negative-instance requirements.
The philosophy-of-physics child contributed the authority-separation guard:
validators, registries, roles, handoffs, approvals, commits, generated
derivatives, and local caches are never certificate payload data.

## Preserved Boundaries

- finite/local examples only
- no universal matter coupling
- no source-law adoption
- no `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption
- no unrestricted `RR_E` theorem
- no matter-semantics or detector-semantics adoption
- no stress-energy semantics or matter action
- no Einstein equations
- no benchmark promotion
- no completed derivation

## Next Packet

Run P4-T02 as one bounded `ontology-formalizer@0.2.0` packet that constructs
one explicit finite/local valid transport certificate instance using the
schema.
