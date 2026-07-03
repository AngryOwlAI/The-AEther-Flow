<!-- authority: control -->

# P11-T02 Local CI-Equivalent Validator Receipt

## Scope

This receipt records v15 P11-T02. The packet created
`scripts/research_control/run_full_research_control_validation.py` as a
repeatable local CI-equivalent validation entry point and added focused unit
tests for the runner plan and report boundary fields.

## Coverage

The local CI-equivalent runner covers:

- memory validate-only drift detection;
- current-frontier freshness;
- dependency-graph freshness;
- changed-file claim-language lint;
- documentation-impact validation;
- project-improvement signal validation;
- research-control registry and task validation;
- research-control diff allowlist validation;
- route-signature extraction diagnostics;
- route-orbit advisory diagnostics;
- whitespace diff checking.

The full repository unittest suite remains opt-in through
`--include-smoke-tests` so the default entry point remains a focused required
gate rather than a long-running smoke layer.

## Boundary

A PASS result from the local CI-equivalent runner is operational receipt
evidence only. It does not establish physics proof authority, authorize route
freeze, adopt source laws, adopt matter or detector semantics, derive or adopt
matter coupling, adopt `MetricData(E)`, expand `g_eff`, introduce
stress-energy semantics, construct a stress-energy tensor, import a matter
action, import a variation principle, derive Einstein equations, promote a
benchmark, issue a Gate Chair verdict, complete the derivation, authorize a
program-wide no-go conclusion, or authorize future source-extension
impossibility.

## Verification

- `.venv/bin/python -m py_compile scripts/research_control/run_full_research_control_validation.py tests/test_run_full_research_control_validation.py research_control/tasks/RT-20260703-021/artifacts/validate_p11_t02_local_ci_equivalent_validator.py`
- `.venv/bin/python -m unittest tests.test_run_full_research_control_validation`
- `.venv/bin/python scripts/research_control/run_full_research_control_validation.py --json --output research_control/tasks/RT-20260703-021/artifacts/p11_t02_local_ci_equivalent_report.json`
- `.venv/bin/python research_control/tasks/RT-20260703-021/artifacts/validate_p11_t02_local_ci_equivalent_validator.py --output research_control/tasks/RT-20260703-021/artifacts/p11_t02_local_ci_equivalent_validator_report.json --json`

## Next Route

Run one bounded v15 P11-T03 CI documentation impact and maintainer guide
packet.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v15* [Implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.

The AEther-Flow Research Project. (2026b). *V15 validation command inventory*
[Control inventory]. `research_control/design/validation_command_inventory_v15.md`.
