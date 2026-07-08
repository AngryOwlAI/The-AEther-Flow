<!-- authority: control -->

# Parent Fusion Notes: Typed EqSrc Orbit Checker

## Consensus

The P7-T02 implementation should be a finite-record checker, not a theorem
prover. The mathematical child focused on explicit typed object, map, inverse,
composition, and orbit-closure checks. The philosophical child focused on
preventing a successful finite check from becoming proof authority.

## Fused Design

The implementation uses a deterministic Python checker at
`scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py`.
It parses strict YAML or JSON records and evaluates a fixed predicate suite.

The accepted finite-record contract requires:

- declared typed source-only objects;
- explicit total identities;
- explicit total maps;
- inverse rows that compose to identities;
- composition rows that match finite-arrow composition;
- orbit partition and orbit closure;
- source-only invariant preservation flags;
- fail-closed missing-data and authority-overread guards.

## Authority Boundary

The fused packet preserves:

```yaml
support_only: true
proof_authority: false
physics_promotion_authorized: false
```

The checker does not prove general `EqSrc`, adopt a source law, import a
target metric, adopt `MetricData(E)`, adopt or expand `g_eff`, derive matter
coupling, derive Einstein equations, promote a benchmark, issue a Gate Chair
verdict, or complete the derivation.

## Result

P7-T02 is complete as support-only implementation work. The next route is
P7-T03, the closure countermodel generator.
