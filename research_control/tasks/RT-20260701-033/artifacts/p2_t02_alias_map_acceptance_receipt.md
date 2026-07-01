<!-- authority: control -->

# P2-T02 Alias Map Acceptance Receipt

## Acceptance Matrix

| Criterion | Result |
| --- | --- |
| Required alias rows are present. | PASS |
| Required object aliases inside `matter_coupling` are present. | PASS |
| High-risk rows have scoped-positive wording. | PASS |
| Bare `accepted` is explicitly prevented for high-risk rows. | PASS |
| Aliases do not override ledger authority. | PASS |
| Aliases are not treated as physics proof. | PASS |
| Renderer integration is noted or deferred. | PASS |
| No physics claim changed. | PASS |

## Alias Authority

`research_control/design/distance_to_gr_status_aliases.yaml` is a control
display map. Its authority is subordinate to
`registries/DISTANCE_TO_GR_LEDGER.csv`, `research_control/program_state.yaml`,
and the latest tracked handoff. If the alias map ever conflicts with those
tracked authority surfaces, the tracked authority surfaces govern.

The map forbids renderer-facing use of bare `accepted` for high-risk rows.
The required replacement is a scoped-positive alias that states the control
status, mathematical status, physical non-conclusion, promotion status, and
overread guard.

## High-Risk Display Result

The `matter_coupling` row now has a control alias:

```text
accepted only as scoped source-extension evidence/precondition
```

The alias requires the following blocked reading:

```text
No source-law adoption, RR_ETransportCompletenessOrInvarianceLaw_v1 adoption,
PositiveMSProfile_v1 adoption, SourceMatterSemanticsAdoptionReadinessLaw_v1
law adoption, matter semantics, detector semantics, coupling law, matter
coupling, stress-energy, matter action, MetricData(E), g_eff scope expansion,
Einstein equations, benchmark promotion, or completed derivation follows from
this row.
```

## Renderer Integration Decision

Renderer integration is deliberately deferred to P2-T03. The current renderer
will be inspected and changed, if appropriate, in the next bounded
current-frontier wording pilot. This packet creates only the canonical alias
data and acceptance evidence.

## Boundary Conclusion

P2-T02 is complete as a status-alias control packet. It creates no ontology
edit, source-law adoption, RR_ETransportCompletenessOrInvarianceLaw_v1
adoption, unrestricted RR_E theorem, detector-semantics collapse, matter
semantics, detector semantics, coupling law, matter coupling, stress-energy
semantics, matter action, MetricData(E), g_eff scope expansion, Einstein
equations, benchmark promotion, completed derivation, future source-extension
impossibility, or global theory rejection.
