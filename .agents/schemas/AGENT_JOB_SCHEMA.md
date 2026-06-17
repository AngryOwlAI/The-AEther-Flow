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
- `role_decomposition`

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

## Role Decomposition For Physics Jobs

`role_decomposition` is mandatory for every new physics research AgentJob
created after `2026-06-17T04:08:16Z`. Historical AgentJobs before that
activation timestamp and non-physics project-system AgentJobs without this
block remain valid.

When present, the only supported mode is
`parent_child_parallel_synthesis` with `decomposition_version: "0.1.0"`. This
mode keeps the old external invariant intact:

- one Director decision
- one outer AgentJob
- one execution-role record
- one completion record
- one final old-style fused output artifact

The decomposition creates internal execution units, not independent AgentJobs.
The parent and children inherit the outer execution-role authority, claim
boundary, source restrictions, forbidden paths, validators, and write-path
allowlist. The decomposition may not declare separate role IDs, source classes,
write allowlists, expanded permissions, human-gate settings, or claim
boundaries.

Required shape:

```yaml
role_decomposition:
  mode: "parent_child_parallel_synthesis"
  decomposition_version: "0.1.0"
  parent:
    execution_unit_id: "parent"
    perspective: "physicist_mathematician_philosopher"
    responsibilities:
      - "derive child role definitions from the selected execution role"
      - "enforce shared claim boundary and source restrictions"
      - "review child outputs for conflicts"
      - "request bounded conflict resolution when needed"
      - "fuse child outputs into the final role artifact"
  children:
    - execution_unit_id: "child_phys_math"
      perspective: "physicist_mathematician"
      output_path: "research_control/tasks/<task_id>/artifacts/child_phys_math_<slug>.tex"
      status: "planned"
    - execution_unit_id: "child_phys_phil"
      perspective: "physicist_philosopher"
      output_path: "research_control/tasks/<task_id>/artifacts/child_phys_phil_<slug>.tex"
      status: "planned"
  conflict_policy:
    review_path: "research_control/tasks/<task_id>/artifacts/parent_conflict_review_<slug>.yaml"
    max_resolution_rounds: 2
    require_parallel_child_revision: true
    unresolved_conflict_status: "blocked"
  fusion_policy:
    fusion_notes_path: "research_control/tasks/<task_id>/artifacts/parent_fusion_notes_<slug>.md"
    fused_output_path: "research_control/tasks/<task_id>/artifacts/<old_style_final_slug>.tex"
    preserve_shared_consensus: true
    preserve_unique_contributions: true
    preserve_unresolved_limitations: true
    final_output_replaces_old_single_role_artifact: true
```

All child output paths, conflict review paths, fusion notes paths, and fused
output paths must be repo-relative paths under the outer AgentJob
`allowed_write_paths`. The fused output path must also appear in
`expected_outputs` and in the `AGENT_JOB_REGISTRY.csv` `output_paths` column.

For science-draft roles, the final fused `.tex` remains the authoritative
old-style role artifact for downstream registry, completion, handoff, and
claim-boundary references. Child `.tex` outputs are supporting draft/control
artifacts and should be registered when retained as source artifacts.
