<!-- authority: control -->

# P4-T03 Semantic-Layer Separation Control Note Receipt

## Summary

`RT-20260703-002` implements v15 P4-T03 by creating
`research_control/design/semantic_layer_separation_control_note.md`.

The note separates:

- `SourceMatterSemantics_src`;
- `DetectorSemantics_det`; and
- `StressEnergyAction_sem`.

It lists allowed and blocked reuse for each layer, states that no-target
certificates are hygiene only, and proposes claim-language linter fixtures for
P4-T04.

## Task-Local Validation

Command:

```zsh
.venv/bin/python research_control/tasks/RT-20260703-002/artifacts/validate_p4_t03_semantic_layer_separation_note.py --output research_control/tasks/RT-20260703-002/artifacts/p4_t03_semantic_layer_separation_note_report.json --json
```

Result:

```yaml
status: PASS
check_count: 15
failed_check_count: 0
report_path: research_control/tasks/RT-20260703-002/artifacts/p4_t03_semantic_layer_separation_note_report.json
```

## Claim Boundary

Allowed result:

- P4-T03 semantic-layer separation control note exists.
- Required layers have allowed and blocked reuse lists.
- No-target certificates are recorded as hygiene only.
- Linter fixtures are proposed for later P4-T04 implementation.

Forbidden result:

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
- `g_eff` scope expansion;
- stress-energy semantics;
- stress-energy tensor;
- matter action;
- Einstein equations;
- benchmark promotion; and
- completed derivation.

## Next Route

The next lawful packet is one bounded v15 P4-T04 semantic-layer
claim-language linter fixture implementation packet.
