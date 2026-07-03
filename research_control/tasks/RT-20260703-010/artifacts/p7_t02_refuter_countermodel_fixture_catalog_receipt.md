<!-- authority: control -->

# P7-T02 Refuter Countermodel Fixture Catalog Receipt

## Summary

`RT-20260703-010` creates the v15 P7-T02 minimal countermodel fixture library.
The library consists of a registered project-control catalog plus eight JSON
negative-control fixtures under `tests/fixtures/research_control/refuter_countermodel/`.

## Fixture Classes Covered

- `finite_rr_e_separation_witness`
- `missing_certificate_witness`
- `malformed_certificate_witness`
- `detector_semantics_import_witness`
- `target_metric_import_witness`
- `finite_local_globalization_failure`
- `source_extension_as_derivation_overread`
- `scoped_evidence_as_adoption_overread`

## Usability

- Refuter usability: every fixture contains a `refuter_obstruction_record`
  shaped by `research_control/design/refuter_obstruction_schema_v1.md`.
- Claim-language linter usability: every fixture contains negative snippets and
  expected class IDs detected by the current linter.
- Test coverage: `tests/test_refuter_countermodel_fixtures.py` validates the
  catalog, fixture contracts, boundary flags, and linter class detection.
- Task-local validation:
  `research_control/tasks/RT-20260703-010/artifacts/validate_p7_t02_refuter_countermodel_fixture_catalog.py`.

## Claim Boundary

This receipt records project-control fixture work only. It does not authorize
canonical ontology edits, source-law adoption,
`RR_ETransportCompletenessOrInvarianceLaw_v1` adoption, unrestricted `RR_E`
theorem authority, `PositiveMSProfile_v1` adoption,
`SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption,
source-extension data adoption beyond exact scoped evidence/precondition
status, matter-semantics adoption, detector-semantics adoption, coupling-law
adoption, matter-coupling derivation or adoption, `MetricData(E)` adoption,
`g_eff` scope expansion, stress-energy semantics, a stress-energy tensor, a
matter action, Einstein equations, benchmark promotion, a Gate Chair verdict,
completed derivation, a program-wide no-go conclusion, or future
source-extension impossibility.

## Next Route

After validation and checkpoint, the next lawful route is one bounded v15
P7-T03 Refuter role/template update packet.
