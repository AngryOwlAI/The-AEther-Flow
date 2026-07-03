<!-- authority: control -->

# P4-T04 Semantic-Layer Linter Fixtures Receipt

## Result

P4-T04 adds deterministic claim-language coverage for semantic-layer collapse
phrases proposed by
`research_control/design/semantic_layer_separation_control_note.md`.

Implemented surfaces:

- `research_control/design/claim_language_linter_taxonomy.yaml`
- `research_control/design/claim_language_linter_reviewed_contexts.yaml`
- `tests/fixtures/claim_language/semantic_layer_collapse.md`
- `tests/fixtures/claim_language/semantic_layer_valid.md`
- `tests/test_validate_claim_language.py`

## Fixture Coverage

The bad fixture hard-fails when scanned as a current control surface for all
ten P4-T04 phrases:

- source matter semantics as detector semantics
- source matter semantics as stress-energy
- no-target certificate as matter theory
- `RR_E` transport evidence as unrestricted theorem
- `PositiveMSProfile_v1` as matter-semantics adoption
- `g_eff` as unscoped Lorentzian metric
- matter-sector evidence as coupling law
- scoped evidence as Einstein-equation premise
- source certificate supplies detector protocol
- stress-energy target supplies matter action

The passing fixture preserves canonical scoped wording:

- source-side matter-semantics evidence remains inside declared source
  certificate scope;
- detector semantics remain blocked unless separately derived or adopted by
  tracked authority;
- stress-energy semantics and matter action remain blocked unless separately
  derived or adopted by tracked authority;
- no-target certificates are hygiene only and do not supply positive matter
  theory; and
- scoped evidence/precondition status supports later work without adopting
  matter semantics or coupling law.

## Boundary

This fixture packet is project-control validation work. It does not create a
physics theorem, source-law adoption, `RR_ETransportCompletenessOrInvarianceLaw_v1`
adoption, unrestricted `RR_E` theorem, `PositiveMSProfile_v1` adoption,
matter-semantics adoption, detector-semantics adoption, stress-energy
semantics, stress-energy tensor, matter action, coupling-law adoption,
matter-coupling derivation or adoption, `MetricData(E)`, `g_eff` scope change,
Einstein equations, benchmark promotion, or completed derivation.

## Validation

Task-local validator:
`research_control/tasks/RT-20260703-003/artifacts/validate_p4_t04_semantic_layer_linter_fixtures.py`

Expected report:
`research_control/tasks/RT-20260703-003/artifacts/p4_t04_semantic_layer_linter_fixtures_report.json`
