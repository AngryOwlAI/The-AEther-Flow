---
title: "P14-T02 Target-Import Attack Fixture Catalog Receipt"
status: "receipt"
task_id: "RT-20260705-031"
agent_job_id: "AJ-RT-20260705-031-001"
validator_id: "p14_t02_target_import_fixture_catalog_validator"
---

# P14-T02 Target-Import Attack Fixture Catalog Receipt

## Result

Status: PASS.

The P14-T02 packet created a discoverable fixture catalog for target-import
attacks and validated it with a task-local receipt.

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| `research_control/design/target_import_attack_fixture_catalog_v16.md` | `6cad549dc392a827eae401da5c85d7514144e43a4c52df26daaa43800ef8a608` |
| `tests/fixtures/research_control/target_import_attack/bad_target_import_fixtures_v16.json` | `bba64e5693d785d9a9f1a85078db03277c30bc5172c4204b9a7ac45e32d9ffca` |
| `tests/fixtures/research_control/target_import_attack/good_target_import_fixtures_v16.json` | `aaa5b2326924d3248b82daf6a6a566c7827eb448e38367cbfcaabaadfe3904f5` |
| `tests/fixtures/claim_language/target_import_attack_bad_v16.md` | `06b4fc35c60f567602cf29273478fa53b24636d269c4fc765ed5988ca5e2d8fc` |
| `tests/fixtures/claim_language/target_import_attack_good_v16.md` | `481819daf9209323626d81d1efb77d7060740fba85a501ffee956ebf479f24f1` |
| `research_control/tasks/RT-20260705-031/artifacts/validate_p14_t02_target_import_fixture_catalog.py` | `fc5ad8d8a934cebf6690f82efdc0b5ed8ec93edec49c7a7fbd52e82a6c6ef39a` |
| `research_control/tasks/RT-20260705-031/artifacts/p14_t02_target_import_fixture_catalog_report.json` | `6884301309804bf071c094b90e0d4c63004642c69b2c1bfe988807ed8aa813f2` |
| `tests/test_target_import_attack_fixtures.py` | `0b75d9602d0be14956f6372a5232560ffc62f50aa9ce26bc525432887771c635` |

## Validation Evidence

Command:

```zsh
.venv/bin/python research_control/tasks/RT-20260705-031/artifacts/validate_p14_t02_target_import_fixture_catalog.py --output research_control/tasks/RT-20260705-031/artifacts/p14_t02_target_import_fixture_catalog_report.json --json
```

Observed report:

- `status`: `PASS`
- `check_count`: `13`
- `failed_check_count`: `0`
- `fixture_report_count`: `18`
- bad fixtures: `12` expected failures observed
- good fixtures: `6` clean passes observed

Focused durable test:

```zsh
.venv/bin/python -m unittest tests/test_target_import_attack_fixtures.py
```

Observed result: `Ran 4 tests ... OK`.

## Boundary

This receipt is a validator-engineering and research-control artifact. It does
not promote ontology, adopt a source law, derive matter coupling, derive the
Einstein equations, claim completed derivation, or change production validator
behavior.

## Next Action

Route P14-T03 to implement fail-closed target-import detection using this
fixture catalog.

