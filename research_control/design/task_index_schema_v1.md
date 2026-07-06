<!-- authority: control -->

# Task Index Schema v1

## Purpose

This project-control schema defines the generated task-index row shape for
tracked `research_control/tasks` records. It implements v17 P10-T01 only.

The task index is a navigation, audit, and validation support surface. It must
be generated from tracked task records and related completion/handoff files. It
does not replace canonical task records, Director decisions, AgentJobs,
completion records, handoffs, registries, or science sources.

## Authority Boundary

Canonical research-control authority remains in the tracked task directories,
Director Decision Records, AgentJobs, completion records, handoffs,
`program_state.yaml`, and registries. The generated task index may summarize
those sources only to help humans and agents find the authoritative record.

Rows may be used to:

- locate task records and completion receipts;
- audit v17 plan progress and next-route continuity;
- detect missing, malformed, or inconsistent task metadata;
- support memory and folder-map navigation after a generated renderer exists.

Rows may not be used to:

- infer completion when the source task, completion, and handoff disagree;
- replace inspection of canonical task records or source artifacts;
- promote `MetricData(E)`, `g_eff`, detector semantics, matter semantics,
  coupling law, matter coupling, stress-energy semantics, matter action,
  Einstein equations, benchmark promotion, Gate Chair verdicts, or completed
  derivation;
- treat generated index freshness as scientific proof authority.

## Generated Surfaces

Future P10 tasks may generate these files from this schema:

```text
research_control/tasks/TASK_INDEX.csv
research_control/tasks/TASK_INDEX.md
wiki/indexes/research_control_task_index.md
```

P10-T01 defines the schema only. It does not create the generated task index.

## Required CSV Header

```csv
task_id,parent_task_id,created_at,closed_at,task_type,status,target_derivation_milestone,milestone_burden,role_family,physics_delta,ledger_rows_changed,artifact_count,next_recommended_action,validation_status,completion_path
```

## Source Records

A generated row must derive from tracked repository files only:

- `research_control/tasks/<task_id>/00_TASK.yaml`
- `research_control/tasks/<task_id>/DDR-*.md`
- `research_control/tasks/<task_id>/jobs/AJ-*.yaml`
- `research_control/tasks/<task_id>/jobs/completions/AJC-*.yaml`
- `research_control/handoffs/handoff-*.yaml`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`

Generated wiki notes, local Obsidian notes, SQLite retrieval indexes, and
`.local/` caches are not source records for the task index.

## Required Row Fields

| Field | Required meaning | Valid value rule |
| --- | --- | --- |
| `task_id` | Stable research-control task id. | Nonblank `RT-YYYYMMDD-NNN` value matching a tracked task directory. |
| `parent_task_id` | Immediate predecessor or parent task. | Existing task id or empty when no parent is declared. |
| `created_at` | Task creation timestamp. | ISO 8601 UTC timestamp from `00_TASK.yaml` or registry. |
| `closed_at` | Task closure timestamp. | ISO 8601 UTC timestamp for completed tasks; empty for pending or active tasks. |
| `task_type` | Machine-readable task family. | Nonblank value from `00_TASK.yaml` or `RESEARCH_TASK_REGISTRY.csv`. |
| `status` | Current task status. | One of `pending`, `active`, `completed`, `blocked`, `human_gated`, or `superseded`. |
| `target_derivation_milestone` | Declared milestone for physics-adjacent tasks. | Nonblank when present in the source task; use `none` for pure project-control support work when the source says none. |
| `milestone_burden` | Local burden stated by the task. | Nonblank summary copied or normalized from tracked task records. |
| `role_family` | Execution role family selected for the AgentJob. | `<role-id>@<version>` when a job exists; empty only for tasks without an AgentJob. |
| `physics_delta` | Whether the task changed Distance-to-GR or physics claim status. | `true` or `false`. Must be `false` for support-only project-control packets. |
| `ledger_rows_changed` | Whether the task changed Distance-to-GR or controlled ledger rows. | `true`, `false`, or a semicolon-separated list of ledger ids when explicitly available. |
| `artifact_count` | Count of tracked task-local artifacts. | Nonnegative integer derived from `research_control/tasks/<task_id>/artifacts`. |
| `next_recommended_action` | Next route named by completion, handoff, or task state. | Empty only when the task is terminal or superseded; otherwise nonblank. |
| `validation_status` | Validation status of the task transaction. | Prefer `PASS`, `FAIL`, `PENDING`, or `not_applicable` as recorded in source state. |
| `completion_path` | Completion record path for the active AgentJob. | Existing repo-relative path for completed jobs; empty for tasks without completion. |

## Generation Rules

1. The renderer must parse structured YAML/CSV sources rather than scrape
   prose where structured fields exist.
2. If structured sources disagree, the generated row must preserve the conflict
   as a validation issue rather than silently choosing a favorable value.
3. The generated CSV and Markdown index must be regenerated outputs, not
   hand-authored authority.
4. Rows must preserve `physics_delta=false` for project-control, schema,
   documentation, validator, memory, or publication-support packets unless a
   tracked completion explicitly records a Distance-to-GR or controlled ledger
   delta.
5. Missing required fields must be reported by the future validator rather than
   filled with invented values.

## Validation Rules

Future P10-T03 validation must check at least:

- required header equality;
- source task directory existence for every row;
- completion path existence for completed AgentJobs;
- task status compatibility between `00_TASK.yaml`,
  `RESEARCH_TASK_REGISTRY.csv`, and completion records;
- `physics_delta=false` preservation for support-only project-control tasks;
- no generated task-index row claims proof authority, benchmark promotion, Gate
  Chair verdict authority, Einstein-equation derivation, or completed
  derivation.

## P10 Continuation Rules

P10-T02 may create the renderer and generated task-index outputs from this
schema. P10-T03 may validate those generated outputs. P10-T04 may integrate
the generated index into memory and folder-map surfaces. None of those steps
may treat the generated index as independent scientific or research-control
authority. No task-index row may assert completed derivation.
