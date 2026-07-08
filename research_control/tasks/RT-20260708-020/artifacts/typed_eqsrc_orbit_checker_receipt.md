<!-- authority: control -->

# Typed EqSrc Orbit Checker Receipt

## Control Status

```yaml
task_id: "RT-20260708-020"
plan_task_id: "P7-T02"
checker_id: "typed_eqsrc_orbit_checker"
support_only: true
proof_authority: false
physics_promotion_authorized: false
status: "v18_p7_t02_typed_eqsrc_orbit_checker_implemented_no_proof_authority"
```

## Implemented Outputs

- `scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py`
- `tests/test_typed_eqsrc_orbit_checker.py`
- `tests/fixtures/research_control/typed_eqsrc_orbit/valid_support_only.yaml`
- `tests/fixtures/research_control/typed_eqsrc_orbit/orbit_closure_failure.yaml`
- `tests/fixtures/research_control/typed_eqsrc_orbit/type_mismatch.yaml`
- `tests/fixtures/research_control/typed_eqsrc_orbit/target_import_overread.yaml`
- `research_control/tasks/RT-20260708-020/artifacts/typed_eqsrc_orbit_checker_spec_v1.md`
- `research_control/tasks/RT-20260708-020/artifacts/typed_eqsrc_orbit_checker_report.json`

## Checker Scope

The checker verifies finite records for:

- declared typed source objects;
- explicit identity maps;
- explicit inverse maps;
- explicit composition table rows;
- finite orbit partition and orbit closure;
- source-only invariant preservation flags;
- fail-closed missing-data and authority-overread behavior.

## Verification

Focused checks passed:

```text
.venv/bin/python -m unittest tests/test_typed_eqsrc_orbit_checker.py
.venv/bin/python scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py --fixture tests/fixtures/research_control/typed_eqsrc_orbit/valid_support_only.yaml --json-output research_control/tasks/RT-20260708-020/artifacts/typed_eqsrc_orbit_checker_report.json --json
```

The positive checker report status is `pass_support_only`, with
`support_only=true`, `proof_authority=false`, and
`physics_promotion_authorized=false`.

## New Mathematical Payload

```yaml
new_mathematical_payload:
  - payload_id: "P7T02-PAYLOAD-001"
    payload_type: "support_only_finite_checker"
    object_name: "typed_eqsrc_orbit_checker"
    summary: "Finite typed source objects maps inverse rows composition rows and orbits are checked for explicit closure."
  - payload_id: "P7T02-PAYLOAD-002"
    payload_type: "negative_branch_suite"
    object_name: "typed_eqsrc_orbit_checker_negative_fixtures"
    summary: "Orbit closure type mismatch target import proof-authority and missing-data branches fail closed."
  - payload_id: "P7T02-PAYLOAD-003"
    payload_type: "specification"
    object_name: "typed_eqsrc_orbit_checker_spec_v1"
    summary: "Defines finite-record contract and authority boundary for later support formalization tools."
```

## Forbidden Conclusions

This packet does not prove general `EqSrc`, adopt a source law, import a target
metric, adopt `MetricData(E)`, adopt or expand `g_eff`, derive matter coupling,
derive Einstein equations, promote a benchmark, issue a Gate Chair verdict, or
complete the derivation.

## Next Route

Run one bounded v18 P7-T03 `closure_countermodel_generator_support_only`
packet.
