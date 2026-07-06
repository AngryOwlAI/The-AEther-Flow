<!-- authority: control -->

# P10-T03 Task-Index Validator Receipt

## Result

P10-T03 created the task-index validator and focused coverage:

- `scripts/research_control/validate_task_index.py`
- `tests/test_task_index_renderer.py`
- local full validation runner coverage for `task_index_validation`

The validator checks generated task-index output freshness, exact CSV header,
row equality with tracked renderer output, source task directory existence,
completion-path existence, task status compatibility, support-only
`physics_delta=false` preservation, and forbidden positive task-index overread
language.

## Historical Metadata

The current generated index reports historical metadata issues as warnings. In
the P10-T03 validation run, those warnings were:

- `missing_field`: 293
- `missing_source`: 4

These warnings are not treated as task-index validator failures because they
pre-exist this packet and the P10-T03 validator is designed to report rather
than invent or silently repair them.

## Boundary

The validator is project-control evidence only. It does not make the generated
task index authoritative, does not create P10-T04 memory or folder-documentation
integration, and does not alter source-law, `MetricData(E)`, `g_eff`,
matter-coupling, Einstein-equation, benchmark, Gate Chair, ontology, or
completed-derivation status.

## Verification

Task-local verification is recorded in
`research_control/tasks/RT-20260706-027/artifacts/task_index_validator_report.json`.
