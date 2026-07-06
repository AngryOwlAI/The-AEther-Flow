<!-- authority: control -->

# P10-T01 Task-Index Schema Receipt

## Summary

`RT-20260706-025` executed one bounded v17 P10-T01 project-control packet. It
created `research_control/design/task_index_schema_v1.md`.

The schema defines the required generated task-index CSV header:

```csv
task_id,parent_task_id,created_at,closed_at,task_type,status,target_derivation_milestone,milestone_burden,role_family,physics_delta,ledger_rows_changed,artifact_count,next_recommended_action,validation_status,completion_path
```

## Result

The schema defines:

- source records for future generation from tracked task, completion, handoff,
  and registry records;
- required row-field meanings and valid value rules;
- generation rules requiring structured parsing and conflict preservation;
- validation rules for future task-index validator work;
- P10 continuation boundaries for P10-T02, P10-T03, and P10-T04.

## Boundary

This receipt records schema creation only. It does not create
`research_control/tasks/TASK_INDEX.csv`, `research_control/tasks/TASK_INDEX.md`,
or `wiki/indexes/research_control_task_index.md`. It does not change
Distance-to-GR status, ledger rows, physics claims, Gate Chair verdicts,
benchmark status, Einstein-equation status, matter-coupling status, or
completed-derivation status.

## Verification

```text
.venv/bin/python research_control/tasks/RT-20260706-025/artifacts/validate_p10_t01_task_index_schema.py --write-report --json
```

Result: `PASS`.

## Next Route

The next lawful v17 continuation is P10-T02:

```text
task-index generator
```
