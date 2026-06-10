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

## Optional Fields

- `objective`
- `resolves_signal_routing`

`objective` is optional for ordinary one-signal or source-driven jobs. If one
AgentJob resolves more than one project-improvement signal, `objective` must
explicitly name each resolved signal ID. The completion record must then list
the same signal IDs in `resolved_project_improvement_signals` and provide a
nonblank `coherent_resolution_summary`. Each closed signal row must use the
AgentJob's canonical `completion_path` from `AGENT_JOB_REGISTRY.csv` as
`resolution_evidence_path`.

`resolves_signal_routing` is optional and defaults to `false`. Set it to
`true` only when the AgentJob objective explicitly fixes project-improvement
signal routing. A completion for such a job must include
nonblank `routing_delta_summary` plus `resolver_snapshots.before` and
`resolver_snapshots.after` as repo-relative paths to preserved JSON output from
`scripts/project_control/resolve_project_improvement.py --json`.
The research-control validator checks only that the summary is present and
that the snapshots preserve the stable advisory-routing shape: parseable JSON
object, advisory resolver fields, checkpoint gate source, and the
selected-signal, open-signals, and change-classification sections. Ordinary
validator and documentation jobs must not inherit this evidence burden.
