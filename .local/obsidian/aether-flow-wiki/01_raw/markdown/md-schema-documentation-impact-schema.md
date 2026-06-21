---
schema_id: "DOCUMENTATION_IMPACT_SCHEMA"
version: "0.1.0"
status: "active"
---

# Documentation Impact Schema

Documentation-impact records are strict YAML records created by state-changing
project-system AgentJobs. They explain whether a project-system change required
documentation updates and how that decision was validated.

## Required Fields

- `documentation_impact_id`
- `task_id`
- `job_id`
- `changed_paths`
- `docs_update_required`
- `reason_codes`
- `source_surfaces_inspected`
- `updated_source_docs`
- `updated_registries`
- `generated_derivatives`
- `no_update_rationale`
- `validators_run`
- `status`

## Rules

- `docs_update_required` must be a lowercase boolean.
- If `docs_update_required` is `false`, `no_update_rationale` must explain why
  no documentation update was needed.
- If `docs_update_required` is `true`, at least one updated source document or
  registry must be listed.
- Generated derivatives may be listed only as outputs of approved generation
  commands, never as independent authority.
- Records live at `research_control/tasks/<task_id>/documentation_impact.yaml`.

## No-Op Receipt Example

Use a no-op receipt when classifier output requires documentation-impact
accounting but the correct conclusion is that no source documentation or
registry documentation update is needed:

```yaml
documentation_impact_id: "DI-RT-YYYYMMDD-NNN-001"
task_id: "RT-YYYYMMDD-NNN"
job_id: "AJ-RT-YYYYMMDD-NNN-001"
changed_paths:
  - "scripts/project_control/example.py"
docs_update_required: false
reason_codes:
  - "project_control_tooling_changed"
source_surfaces_inspected:
  - "scripts/project_control/example.py"
updated_source_docs: []
updated_registries: []
generated_derivatives: []
no_update_rationale: "No source documentation update was needed because the change only clarified an existing validator message and did not alter workflow commands or authority boundaries."
validators_run:
  - ".venv/bin/python scripts/project_control/classify_project_changes.py --json"
  - ".venv/bin/python scripts/project_control/validate_documentation_impact.py"
status: "no_update_required"
```
