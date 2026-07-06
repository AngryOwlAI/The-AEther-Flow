<!-- authority: control -->

# P10-T02 Task-Index Generator Receipt

## Result

P10-T02 created `scripts/research_control/render_task_index.py` and generated
the required task-index outputs:

- `research_control/tasks/TASK_INDEX.csv`
- `research_control/tasks/TASK_INDEX.md`
- `wiki/indexes/research_control_task_index.md`

The renderer reads tracked task directories plus the research task, AgentJob,
and Director decision registries. It uses structured YAML and CSV readers where
structured sources exist. It reports missing or malformed task metadata in the
generated Markdown outputs and in the task-local smoke report.

## Boundary

The generated task index is navigation and audit support only. It is not task
authority, proof authority, physics authority, benchmark authority, Gate Chair
authority, or completed-derivation evidence.

P10-T03 remains required for hard task-index validation. P10-T04 remains
required for memory and folder-map integration.

## Verification

Task-local verification is recorded in
`research_control/tasks/RT-20260706-026/artifacts/p10_t02_task_index_generator_report.json`.
