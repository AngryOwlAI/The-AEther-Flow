<!-- generated: true; authority: derivative -->

# V18 Support Formalization Traceability

This generated index is reader support only. It is not proof authority, not a source artifact, not a Gate Chair verdict, and not physics-promotion authority.

## Summary

| Field | Value |
| --- | --- |
| Registry | `research_control/design/support_formalization_traceability_registry_v18.yaml` |
| Entry count | 5 |
| Proof authority | false |
| Physics promotion authorized | false |

## Tools

| Plan task | Tool | Source artifacts | Test evidence | PNF row | Boundary |
| --- | --- | --- | --- | --- | --- |
| `P7-T02` | `typed_eqsrc_orbit_checker` | `research_control/design/source_equivalence_typed_object_schema_v1.md`<br>`research_control/tasks/RT-20260708-020/artifacts/typed_eqsrc_orbit_checker_spec_v1.md` | `.venv/bin/python -m unittest tests/test_typed_eqsrc_orbit_checker.py`<br>`.venv/bin/python scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py --fixture tests/fixtures/research_control/typed_eqsrc_orbit/valid_support_only.yaml --json-output research_control/tasks/RT-20260708-020/artifacts/typed_eqsrc_orbit_checker_report.json --json` | `PNF-RT-20260708-025-001` | Support-only finite-record checker; not proof authority and not general EqSrc theorem authority. |
| `P7-T03` | `closure_countermodel_generator` | `research_control/tasks/RT-20260708-020/artifacts/typed_eqsrc_orbit_checker_spec_v1.md`<br>`research_control/tasks/RT-20260708-021/artifacts/closure_countermodel_generator_spec_v1.md` | `.venv/bin/python -m unittest tests/test_closure_countermodel_generator.py`<br>`.venv/bin/python scripts/research_control/support_formalization/closure_countermodel_generator.py --mode all --json-output research_control/tasks/RT-20260708-021/artifacts/closure_countermodel_generator_report.json --json` | `PNF-RT-20260708-025-002` | Support-only finite countermodel generator; not proof authority and not RetainH or GenH adoption. |
| `P7-T04` | `no_target_import_mutation_tester` | `research_control/design/no_target_import_guard_map.md`<br>`research_control/tasks/RT-20260708-022/artifacts/no_target_import_mutation_tester_spec_v1.md` | `.venv/bin/python -m unittest tests/test_no_target_import_mutation_tester.py`<br>`.venv/bin/python scripts/research_control/support_formalization/no_target_import_mutation_tester.py --mutation all --json-output research_control/tasks/RT-20260708-022/artifacts/no_target_import_mutation_tester_report.json --json` | `PNF-RT-20260708-025-003` | Support-only mutation tester; not validator-policy proof authority and not target-import evidence. |
| `P7-T05` | `metric_use_tex_reference_validator` | `research_control/design/metric_use_ledger_schema_v1.md`<br>`registries/METRIC_USE_LEDGER.csv`<br>`research_control/tasks/RT-20260708-023/artifacts/metric_use_tex_validator_spec_v1.md` | `.venv/bin/python -m unittest tests/test_validate_metric_use_tex_references.py`<br>`.venv/bin/python scripts/research_control/validate_metric_use_tex_references.py --json-output research_control/tasks/RT-20260708-023/artifacts/metric_use_tex_validator_report.json --json` | `PNF-RT-20260708-025-004` | Support-only TeX validator; not ledger mutation authority, proof authority, or physical metric authority. |
| `P7-T06` | `detector_placeholder_collapse_checker` | `research_control/design/source_detector_readout_semantics_burden_v1.md`<br>`research_control/tasks/RT-20260708-010/artifacts/source_detector_readout_candidate_v1.tex`<br>`research_control/tasks/RT-20260708-024/artifacts/detector_placeholder_collapse_checker_spec_v1.md` | `.venv/bin/python -m unittest tests/test_detector_placeholder_collapse_checker.py`<br>`.venv/bin/python scripts/research_control/support_formalization/detector_placeholder_collapse_checker.py --case all --json-output research_control/tasks/RT-20260708-024/artifacts/detector_placeholder_collapse_checker_report.json --json` | `PNF-RT-20260708-025-005` | Support-only detector/readout semantic-state checker; not Det_src adoption, Readout_src adoption, detector semantics adoption, or matter coupling derivation. |

## Forbidden Overreads

- Einstein equations
- Gate Chair verdict
- MetricData(E) adoption
- benchmark promotion
- canonical ontology edit
- completed derivation
- executable spec as proof authority
- g_eff adoption or scope expansion
- matter action
- matter-coupling derivation or adoption
- source-law adoption
- stress-energy semantics
- stress-energy tensor
- support tool as proof authority
- target metric import
- validator PASS as theorem
