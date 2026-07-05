# V16 P5-T04 Post-Refactor Route Selector

## Question

After P5 separated certificate-indexed equivalence targets from theorem
content, which single next route should the research-control program execute?

## Inputs

- P5-T02 defined `EqMS_cert_src_v2` and its theorem targets as draft/control
  source-side material.
- P5-T03 proved conditional transitivity only when a supplied valid compatible
  composition certificate exists.
- P5-T03 recorded
  `OB-P5T03-MISSING-COMPATIBLE-COMPOSITION-CERTIFICATE` for the stronger
  premise-free reading.
- The P5-T04 done criteria require a handoff to P6 unless a repair or freeze
  route is required.

## Candidate Route Evaluation

| Candidate route | Decision | Reason |
| --- | --- | --- |
| `v16_support_only_formalization_scope_selector` | selected | P5 produced a conditional theorem and explicit obstruction. The next disciplined step is to select one finite/local support-only formalization target before constructing checkers. |
| formalize P5 theorem in support-only spec | not selected | This is a plausible P6 target, but P6-T01 must first choose the exact target and toolchain. |
| expand certificate-instance library | not selected | P4 already supplied the initial finite/local fixtures; additional expansion can follow a scoped P6 or P10 decision. |
| build model zoo | not selected | The source model zoo is scheduled for P10 and should not bypass P6 support-only checking. |
| route to target-import attack suite | not selected | Target-import attacks are scheduled for P14 and should consume clearer checker and status fields. |
| select coupling-law candidate construction | not selected | Premature before support-only checker scope and later route selection. |
| repair theorem target | not selected | P5-T03 returned a conditional theorem plus precise obstruction, not a blocking theorem-target defect. |
| route freeze if repeated no-payload | not selected | P5 produced new payload and no repeated no-payload freeze condition is active. |

## Selected Next Route

```text
v16_support_only_formalization_scope_selector
```

The next bounded AgentJob should be P6-T01:

```text
v16_support_only_formalization_scope_selector
```

Recommended next role:

```text
theoretical-continuation-selector@0.1.0
```

## Theoretical Decision Output

- `selected_next_packet_type`:
  `bounded_theoretical_calculation`
- `selected_next_role_family`:
  `theoretical-continuation-selector@0.1.0`
- `decision_basis`:
  P5 produced a usable support-only theorem boundary and no tracked repair or
  freeze trigger. The v16 plan directs the next handoff to P6 under those
  conditions.
- `theoretical_method`:
  candidate-route exclusion by plan criteria, theorem-status inspection,
  burden continuity, and overread-risk minimization.
- `preserves_claim_blocks`:
  true
- `requires_human_gate`:
  false
- `human_gate_reason`:
  no human gate is required because this packet selects a support-only
  formalization-scope selector and does not adopt ontology, source law,
  coupling law, matter coupling, GR equations, benchmark status, or completed
  derivation.

## Distance-to-GR Effect

No Distance-to-GR ledger row changes. This selector advances control routing
only. It unlocks P6-T01, which must choose one bounded finite/local
formalization target and justify a toolchain without proof authority.

## Forbidden Conclusions

The selector does not imply source-law adoption, detector-semantics adoption,
matter-semantics adoption, coupling-law adoption, matter-coupling derivation,
stress-energy semantics, matter action, Einstein equations, benchmark
promotion, Gate Chair verdict, or completed derivation.
