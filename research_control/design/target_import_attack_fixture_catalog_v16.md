---
title: "Target-Import Attack Fixture Catalog v16"
status: "source"
authority: "project-control"
task_id: "RT-20260705-031"
agent_job_id: "AJ-RT-20260705-031-001"
---

# Target-Import Attack Fixture Catalog v16

## Purpose

This catalog makes the P14 target-import attack taxonomy executable as fixture
data. It is a validator-engineering artifact only. It does not modify physics
claims, promote ontology, authorize benchmark recovery, or change the current
claim-language validator.

The fixture payload is split into:

- structured fixture metadata under `tests/fixtures/research_control/target_import_attack/`
- intentional claim-language snippets under `tests/fixtures/claim_language/`
- a task-local validator receipt under `research_control/tasks/RT-20260705-031/artifacts/`

## Catalog Contract

```json
{
  "schema_id": "target_import_attack_fixture_catalog_v16",
  "catalog_id": "target_import_attack_fixture_catalog_v16",
  "task_id": "RT-20260705-031",
  "agent_job_id": "AJ-RT-20260705-031-001",
  "taxonomy_path": "research_control/design/target_import_attack_taxonomy_v16.md",
  "fixture_sets": [
    {
      "set_id": "bad_target_import_fixtures_v16",
      "mode": "bad",
      "path": "tests/fixtures/research_control/target_import_attack/bad_target_import_fixtures_v16.json",
      "snippet_path": "tests/fixtures/claim_language/target_import_attack_bad_v16.md"
    },
    {
      "set_id": "good_target_import_fixtures_v16",
      "mode": "good",
      "path": "tests/fixtures/research_control/target_import_attack/good_target_import_fixtures_v16.json",
      "snippet_path": "tests/fixtures/claim_language/target_import_attack_good_v16.md"
    }
  ],
  "required_bad_fixture_classes": [
    "target_metric_used_as_source_certificate",
    "lorentzian_signature_used_as_certificate_validity",
    "proper_time_used_as_source_readout",
    "detector_calibration_treated_as_source_label",
    "stress_energy_tensor_used_to_prove_matter_semantics",
    "matter_action_used_to_prove_coupling_law",
    "einstein_equations_used_as_upstream_premise",
    "benchmark_fit_used_as_source_evidence",
    "gate_chair_scoped_evidence_used_as_source_law",
    "validator_pass_used_as_proof",
    "generated_wiki_note_used_as_authority",
    "finite_local_model_rendered_as_universal_matter_coupling"
  ],
  "required_good_fixture_classes": [
    "source_transport_certificate_with_no_target_guard",
    "scoped_evidence_precondition_wording",
    "target_import_fail_closed_wording",
    "detector_semantics_blocked_wording",
    "einstein_equations_not_started_wording",
    "benchmark_promotion_protected_wording"
  ],
  "claim_boundary": {
    "proof_authority": false,
    "physics_promotion_authorized": false,
    "source_law_adopted": false,
    "matter_coupling_derived": false,
    "einstein_equations_derived": false,
    "completed_derivation_claimed": false,
    "validator_behavior_changed": false
  }
}
```

## Fixture Semantics

Bad fixtures are expected to be rejected by the current claim-language linter or
by the target-import extension specified for P14-T03. Good fixtures are expected
to remain acceptable corrective language.

The bad fixtures are intentionally non-authoritative examples. Their only role
is to exercise source/target separation, authority routing, and fail-closed
language.

## Validation Receipt

The task-local validator is:

`research_control/tasks/RT-20260705-031/artifacts/validate_p14_t02_target_import_fixture_catalog.py`

The generated report is:

`research_control/tasks/RT-20260705-031/artifacts/p14_t02_target_import_fixture_catalog_report.json`

