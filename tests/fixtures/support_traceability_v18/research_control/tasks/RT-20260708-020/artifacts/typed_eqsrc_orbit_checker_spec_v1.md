<!-- authority: control -->

# Typed EqSrc Orbit Checker Spec V1

## Control Status

This specification defines the P7-T02 support-only finite typed EqSrc orbit
checker contract. It is project-control tooling, not proof authority and not a
general EqSrc theorem.

```yaml
task_id: "RT-20260708-020"
plan_task_id: "P7-T02"
checker_id: "typed_eqsrc_orbit_checker"
checker_version: "0.1.0"
support_only: true
proof_authority: false
physics_promotion_authorized: false
```

## Record Contract

The checker accepts YAML or JSON finite records with these sections:

- `metadata`: fixture id, support-only flags, exact boundary statement, and
  source artifact paths.
- `typed_objects`: finite source-only objects with `id`, `type`, and
  `source_only: true`.
- `identity_maps`: explicit total identity maps for every declared type.
- `maps`: explicit finite maps with source type, target type, and arrows.
- `inverse_maps`: explicit inverse rows whose compositions recover declared
  identities.
- `composition_table`: explicit composition rows checked against finite arrows.
- `orbits`: finite typed orbits that partition exactly the declared objects.
- `eqsrc_pairs`: finite pair rows that remain type-local and orbit-local.
- `invariant_flags`: source-only invariant preservation and fail-closed flags.
- `forbidden_authority`: explicit false flags for target import and downstream
  promotion.

## Checked Predicates

The checker validates:

- required finite-record sections are present;
- support-only authority flags are exact;
- forbidden target and downstream authority flags are false;
- typed objects are finite, unique, typed, and source-only;
- identity maps are explicit, total, and self maps;
- declared maps are total on their finite source types;
- inverse maps compose to declared identities;
- composition table entries match computed finite-arrow composition;
- orbits partition typed objects;
- all explicit maps preserve declared orbit closure;
- EqSrc pairs are type-local and orbit-local;
- source-only invariant flags are preserved;
- missing-data controls fail closed.

## Failure Statuses

The report status is one of:

- `pass_support_only`
- `fail_malformed_record`
- `fail_authority_overread`
- `fail_target_import`
- `fail_type_mismatch`
- `fail_identity_map`
- `fail_inverse_map`
- `fail_composition_table`
- `fail_orbit_partition`
- `fail_orbit_closure`
- `fail_invariant_preservation`
- `tooling_error`

## Authority Boundary

The checker can only say whether one finite record satisfies the explicit
record contract. A passing report does not prove general `EqSrc`, adopt a
source law, import a target metric, adopt `MetricData(E)`, adopt or expand
`g_eff`, derive matter coupling, derive Einstein equations, promote a
benchmark, issue a Gate Chair verdict, or complete the derivation.

## Implementation Surface

- Script: `scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py`
- Tests: `tests/test_typed_eqsrc_orbit_checker.py`
- Fixtures: `tests/fixtures/research_control/typed_eqsrc_orbit/`
- Positive report: `research_control/tasks/RT-20260708-020/artifacts/typed_eqsrc_orbit_checker_report.json`

## Next Route

The next bounded route is P7-T03:
`closure_countermodel_generator_support_only`.
