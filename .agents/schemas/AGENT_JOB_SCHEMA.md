---
schema_id: "AGENT_JOB_SCHEMA"
version: "0.1.0"
status: "active"
---

# AgentJob Schema

AgentJobs are strict YAML executable contracts. They are immutable after
creation.

## Required Fields

- `job_id`
- `task_id`
- `decision_id`
- `role_id`
- `role_version`
- `status`
- `requires_human_gate`
- `allowed_read_paths`
- `allowed_write_paths`
- `allowed_generated_paths`
- `forbidden_paths`
- `allowed_source_classes`
- `forbidden_source_classes`
- `approved_commands`
- `required_validators`
- `expected_outputs`
- `claim_boundary`

If the role is provisional, the job must include `provisional_role_contract`
with `expires_after_job_id` equal to the job ID.
