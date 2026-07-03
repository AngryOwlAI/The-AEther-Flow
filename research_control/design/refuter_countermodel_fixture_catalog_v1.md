<!-- authority: control -->

# Refuter Countermodel Fixture Catalog v1

## Purpose

This control catalog completes P7-T02 of
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.
It defines a small library of negative-control fixtures for future Refuter
outputs and claim-language linter checks.

The catalog is support-only project-control evidence. It is not proof
authority, not a Refuter result on a live candidate, not source-law adoption,
not source-extension data adoption, not matter-semantics adoption, not
detector-semantics adoption, not matter-coupling derivation or adoption, not
`MetricData(E)` adoption, not `g_eff` scope expansion, not Einstein-equation
evidence, not benchmark promotion, not a Gate Chair verdict, not completed
derivation, not a program-wide no-go conclusion, and not future
source-extension impossibility.

## Fixture Contract

Each fixture is a JSON negative control under
`tests/fixtures/research_control/refuter_countermodel/`. Every fixture exposes
three reusable layers:

- `refuter_obstruction_record`: a record shaped by
  `research_control/design/refuter_obstruction_schema_v1.md`;
- `minimal_witness`: a finite or local description of the obstruction trigger;
- `claim_language_linter`: one or more negative example snippets and expected
  linter class IDs.

Future Refuter packets may cite these fixtures when they need a standard
minimal countermodel shape or a linter-facing overread example. Future claim
language work may reuse the snippets as negative controls. A fixture pass or
catalog validation pass remains tooling evidence only.

## Catalog Index JSON

```json
{
  "catalog_schema": "refuter_countermodel_fixture_catalog_v1",
  "catalog_id": "P7-T02-refuter-countermodel-fixture-catalog",
  "plan_task_id": "P7-T02",
  "source_task_id": "RT-20260703-010",
  "fixture_root": "tests/fixtures/research_control/refuter_countermodel",
  "required_fixture_classes": [
    "finite_rr_e_separation_witness",
    "missing_certificate_witness",
    "malformed_certificate_witness",
    "detector_semantics_import_witness",
    "target_metric_import_witness",
    "finite_local_globalization_failure",
    "source_extension_as_derivation_overread",
    "scoped_evidence_as_adoption_overread"
  ],
  "fixtures": [
    {
      "fixture_id": "finite_rr_e_separation_witness",
      "fixture_class": "finite_rr_e_separation_witness",
      "path": "tests/fixtures/research_control/refuter_countermodel/finite_rr_e_separation_witness.json",
      "expected_linter_class_ids": [
        "unrestricted_rr_e_irrelevance_overclaim"
      ]
    },
    {
      "fixture_id": "missing_certificate_witness",
      "fixture_class": "missing_certificate_witness",
      "path": "tests/fixtures/research_control/refuter_countermodel/missing_certificate_witness.json",
      "expected_linter_class_ids": [
        "source_certificate_overread"
      ]
    },
    {
      "fixture_id": "malformed_certificate_witness",
      "fixture_class": "malformed_certificate_witness",
      "path": "tests/fixtures/research_control/refuter_countermodel/malformed_certificate_witness.json",
      "expected_linter_class_ids": [
        "source_certificate_overread"
      ]
    },
    {
      "fixture_id": "detector_semantics_import_witness",
      "fixture_class": "detector_semantics_import_witness",
      "path": "tests/fixtures/research_control/refuter_countermodel/detector_semantics_import_witness.json",
      "expected_linter_class_ids": [
        "source_certificate_overread",
        "source_matter_semantics_adoption_readiness_law_overclaim"
      ]
    },
    {
      "fixture_id": "target_metric_import_witness",
      "fixture_class": "target_metric_import_witness",
      "path": "tests/fixtures/research_control/refuter_countermodel/target_metric_import_witness.json",
      "expected_linter_class_ids": [
        "source_certificate_overread",
        "semantic_layer_collapse_overclaim"
      ]
    },
    {
      "fixture_id": "finite_local_globalization_failure",
      "fixture_class": "finite_local_globalization_failure",
      "path": "tests/fixtures/research_control/refuter_countermodel/finite_local_globalization_failure.json",
      "expected_linter_class_ids": [
        "global_no_go_or_rejection_overclaim",
        "unrestricted_rr_e_irrelevance_overclaim"
      ]
    },
    {
      "fixture_id": "source_extension_as_derivation_overread",
      "fixture_class": "source_extension_as_derivation_overread",
      "path": "tests/fixtures/research_control/refuter_countermodel/source_extension_as_derivation_overread.json",
      "expected_linter_class_ids": [
        "scoped_evidence_or_precondition_as_adoption",
        "einstein_equation_overclaim"
      ]
    },
    {
      "fixture_id": "scoped_evidence_as_adoption_overread",
      "fixture_class": "scoped_evidence_as_adoption_overread",
      "path": "tests/fixtures/research_control/refuter_countermodel/scoped_evidence_as_adoption_overread.json",
      "expected_linter_class_ids": [
        "scoped_evidence_or_precondition_as_adoption",
        "bare_high_risk_accepted"
      ]
    }
  ]
}
```

## Fixture Class Notes

| Fixture class | Refuter use | Linter use |
| --- | --- | --- |
| `finite_rr_e_separation_witness` | Shows that two finite source-side records with the same local support must remain separate without a declared source certificate. | Catches overreads that collapse `RR_E` without certificate authority. |
| `missing_certificate_witness` | Shows fail-closed behavior when a required declared-object source certificate is absent. | Catches missing-certificate overreads. |
| `malformed_certificate_witness` | Shows fail-closed behavior when a certificate is present but malformed. | Catches malformed-certificate overreads. |
| `detector_semantics_import_witness` | Shows that detector semantics cannot supply source-certificate validity. | Catches detector-semantics import or adoption overreads. |
| `target_metric_import_witness` | Shows that target metric material cannot supply source-certificate validity. | Catches target-metric and semantic-layer import overreads. |
| `finite_local_globalization_failure` | Shows that a finite/local obstruction is local to its fixture scope. | Catches attempts to convert a local fixture into a program-wide no-go. |
| `source_extension_as_derivation_overread` | Shows that scoped source-extension evidence does not create a derivation. | Catches source-extension evidence as source law or GR derivation overreads. |
| `scoped_evidence_as_adoption_overread` | Shows that scoped evidence/precondition status is not adoption. | Catches scoped-evidence-as-adoption and bare high-risk status overreads. |

## Required Boundary For Consumers

Consumers of this catalog must preserve these defaults:

```yaml
proof_authority: false
physics_promotion_authorized: false
source_law_adopted: false
source_extension_data_adopted: false
matter_semantics_adopted: false
detector_semantics_adopted: false
coupling_law_adopted: false
matter_coupling_derived: false
matter_coupling_adopted: false
MetricData_E_adopted: false
g_eff_scope_expanded: false
einstein_equations_derived: false
benchmark_promoted: false
gate_chair_verdict_issued: false
completed_derivation_claimed: false
global_no_go_claim_authorized: false
future_source_extension_impossibility_authorized: false
```

## Validation Expectations

The task-local validator and focused unit test must confirm:

- every P7-T02 required fixture class is present exactly once;
- every catalog path exists and points to a fixture with matching
  `fixture_id` and `fixture_class`;
- every fixture includes a `refuter_obstruction_record` with all fields from
  `refuter_obstruction_schema_v1.md`;
- every fixture keeps protected authorization flags false;
- every fixture lists nonempty `forbidden_conclusions`;
- every fixture includes at least one negative linter snippet and expected
  class ID; and
- the current claim-language linter can identify the expected class IDs from
  the supplied snippets.

## Source Materials

The AEther-Flow Research Project. (2026, July 2). *Recommendations
implementation plan continue task v15* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`

The AEther-Flow Research Project. (2026, July 3). *Refuter obstruction schema
v1* [Internal project-control schema].
`research_control/design/refuter_obstruction_schema_v1.md`

The AEther-Flow Research Project. (2026, July 3). *Claim language linter
taxonomy* [Internal project-control taxonomy].
`research_control/design/claim_language_linter_taxonomy.yaml`
