<!-- authority: control -->

# P5-T01 Public Status Table Source Spec Receipt

## Scope

This receipt records one bounded v14 P5-T01 source-spec packet. It creates a
canonical public status table source spec and does not update public surfaces
or generated derivatives beyond ordinary memory/wiki synchronization.

## Deliverable

| Deliverable | Path | Result |
| --- | --- | --- |
| Canonical public status table source spec | `research_control/design/public_status_table_source_spec.md` | PASS |

## Required Column Coverage

The source spec defines all required v14 P5-T01 columns:

- burden;
- control status;
- mathematical status;
- physical status;
- promotion status;
- exact positive scoped claim;
- exact blocked overread;
- last evidence path;
- source authority note;
- public-safe summary.

## Required Row Coverage

The source spec covers all required high-risk rows:

- `source_ontology_primitives`;
- `M_src`;
- `g_eff`;
- `matter_coupling`;
- `SourceMatterSemanticsAdoptionReadinessLaw_v1`;
- `PositiveMSProfile_v1`;
- `RR_ETransportCompletenessOrInvarianceLaw_v1`;
- `einstein_equations`;
- `benchmark_promotion`;
- `finite_toy_metric_response`.

## Validation Receipts

| Check | Result | Evidence |
| --- | --- | --- |
| Memory preflight | PASS | `core_validation_status=PASS`, `freshness_status=PASS`, `local_retrieval_status=PASS`, `refresh_performed=false` |
| Targeted memory query | PASS | Returned P4-T05 summary, current frontier, and v14 plan; canonical sources were inspected. |
| Continue-research route | PASS | Resolver selected `v14_p5_t01_public_status_table_source_spec` from `handoff-0455`. |
| Source-spec claim-language gate | PASS | `validate_claim_language.py --json --changed` reported `hard_fail_count=0` after source-spec wording repair. |

## Interpretation Boundary

P5-T01 is a documentation source-spec packet. It does not establish or change
the physics status of any row. It does not authorize ontology edits, source-law
adoption, `MetricData(E)` adoption, `g_eff` scope expansion, matter-coupling
derivation, stress-energy semantics, matter action, Einstein equations,
benchmark promotion, or completed derivation.

## Next Route

The logical next packet is v14 P5-T02 README and GitHub-facing status update.
HTML source-spec updates, generated public derivative regeneration, public
claim-language validation, and downstream physics routes remain blocked until
their own tracked packets authorize them.
