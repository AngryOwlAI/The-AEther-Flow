<!-- authority: control -->

# P9-T01 Status-Card v2 Schema Receipt

## Summary

RT-20260708-032 implements v18 P9-T01 by adding
`research_control/design/status_card_v2_schema.md`,
`research_control/design/accepted_status_calibration_v2.yaml`, and
`status_card_v2` mirror blocks in
`research_control/design/distance_to_gr_status_aliases.yaml`.

The packet adds required next-burden and public-compression fields for:

- `m_src`
- `g_eff`
- `matter_coupling`
- `einstein_equations`
- `benchmark_promotion`

## Boundary

This receipt records a project-control schema update only. It does not change
Distance-to-GR ledger status, create renderer integration, create linter
enforcement, adopt ontology, adopt a source law, derive matter coupling, derive
Einstein equations, promote a benchmark, issue a Gate Chair verdict, or claim a
completed derivation.

## Done Criteria

- `next_burden` is required for each high-risk row.
- Existing positive-first order is preserved.
- `public_summary` is short compression only.
- `full_control_non_conclusions` remains available for audit surfaces.
- Renderer integration is deferred to P9-T02.
- Claim-language linter tests are deferred to P9-T04.

## Validator

```text
.venv/bin/python research_control/tasks/RT-20260708-032/artifacts/validate_p9_t01_status_card_v2_schema.py --write-report --json
```

The validator report path is:

```text
research_control/tasks/RT-20260708-032/artifacts/p9_t01_status_card_v2_schema_report.json
```

## APA 7 Source Materials

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v18* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`.

The AEther-Flow Research Project. (2026b). *Handoff 0724* [Internal
research-control handoff]. `research_control/handoffs/handoff-0724.yaml`.
