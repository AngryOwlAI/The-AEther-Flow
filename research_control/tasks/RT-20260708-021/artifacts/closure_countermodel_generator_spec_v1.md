<!-- authority: science_draft -->

# Closure Countermodel Generator Spec v1

## Control Status

```yaml
task_id: "RT-20260708-021"
plan_task_id: "P7-T03"
generator_id: "closure_countermodel_generator"
support_only: true
proof_authority: false
physics_promotion_authorized: false
```

## Purpose

This specification defines the v18 P7-T03 support-only closure countermodel
generator. The generator creates deterministic finite mock records that
exercise missing-closure branches after the P7-T02 typed EqSrc orbit checker.

The generated records are support-only fixtures. They are not proof authority,
not a general EqSrc theorem, not RetainH or GenH adoption, not source-law
adoption, not target metric import, not `MetricData(E)` adoption, not `g_eff`
adoption or scope expansion, not matter-coupling derivation, not Einstein
equations, not benchmark promotion, not a Gate Chair verdict, and not a
completed-derivation claim.

## Generator Modes

```yaml
countermodel_modes:
  - "missing_identity"
  - "missing_inverse"
  - "missing_composition"
  - "non_family_stable_invariant"
  - "RetainH_required"
  - "GenH_required"
```

Each mode mutates the finite P7-T02 typed-record substrate and records the
expected support-checker status. The `RetainH_required` and `GenH_required`
modes mark primitive requirements with `adopted=false`; they do not create
adoption authority.

## Required Outputs

- `scripts/research_control/support_formalization/closure_countermodel_generator.py`
- `tests/test_closure_countermodel_generator.py`
- `research_control/tasks/RT-20260708-021/artifacts/closure_countermodel_generator_report.json`

## Done Criteria Mapping

| P7-T03 criterion | Evidence |
| --- | --- |
| Generator creates finite mock records for each configured mode | `closure_countermodel_generator_report.json` has six cases matching the configured mode list. |
| Output is marked support-only | Generator bundle and each case set `support_only=true`, `proof_authority=false`, and `physics_promotion_authorized=false`. |
| Unit tests pass | `tests/test_closure_countermodel_generator.py` covers mode coverage, support-only authority, deterministic CLI output, fixture writing, primitive-required modes, and typed-checker fail-closed behavior. |
| Next route is P7-T04 | `handoff-0714` routes to `P7-T04` no-target import mutation tester. |

## Next Route

The next bounded route is `P7-T04`: `no_target_import_mutation_tester`.
