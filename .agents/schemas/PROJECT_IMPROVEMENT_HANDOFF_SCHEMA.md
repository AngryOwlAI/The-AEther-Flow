---
schema_id: "PROJECT_IMPROVEMENT_HANDOFF_SCHEMA"
version: "0.1.0"
status: "active"
activation_mode: "prospective_hard_failure_for_future_nonblank_project_improvement_signals"
active_after: "2026-06-22T04:00:00Z"
---

# Project Improvement Handoff Schema

## Purpose

This schema defines the project-improvement handoff sidecar contract for
`research_control/project_improvement_handoffs/improve-project-handoff_*.yaml`.
The sidecar is a bridge from research-discovered project-system issues to the
`/improve-project-system` lane. It is not a research-continuation handoff and
does not authorize repair from `/continue-research`.

## Activation And Compatibility

The contract is prospective. Historical completions and handoffs with
nonblank `project_improvement_signals` before `2026-06-22T04:00:00Z` remain
valid without retroactive sidecar edits. At or after that timestamp, any
completion or regular handoff that emits a nonblank project-improvement signal
must name a generated sidecar in `project_improvement_bridge`.

The regular research handoff remains authoritative for `/continue-research`.
The sidecar is consumed only by project-system improvement workflows and
validators.

## Required Sidecar Fields

Required top-level fields:

- `improvement_handoff_id`
- `created_at`
- `status`
- `source`
- `normal_research_continuation`
- `project_boundary`
- `signal_summary`
- `issues`
- `solution_plan`
- `resolution`
- `notes`

Allowed `status` values:

- `open`
- `active`
- `resolved`
- `closed`
- `rejected`
- `superseded`

Allowed `source.source_kind` values:

- `research_completion_and_handoff`
- `completion_only`
- `handoff_only`
- `backfilled_from_immutable_source`

## Boundary Rules

The sidecar must preserve these project-boundary values:

```yaml
project_boundary:
  recommended_skill: "improve-project-system"
  project_system_only: true
  physics_claim_promotion_authorized: false
  canonical_science_source_edits_authorized: false
  generated_derivative_hand_edits_authorized: false
  requires_human_gate: false
```

The normal research-continuation block must state:

```yaml
normal_research_continuation:
  sidecar_does_not_replace_regular_handoff: true
```

The sidecar must not be placed under `research_control/handoffs/`, must not
match the normal `handoff-####.yaml` filename pattern, and must not become the
latest research handoff.

## Signal Parity Rules

Each sidecar issue must include:

- `signal_id`
- `signal_type`
- `severity`
- `title`
- `description`
- `impact`
- `recommended_skill`
- `recommended_role`
- at least one evidence item with `evidence_path` and `evidence_summary`

The sidecar is valid only when:

- every issue `signal_id` exists in
  `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`;
- every `signal_type` is active in
  `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv`;
- `signal_summary.signal_ids` exactly matches the issue signal IDs;
- `signal_summary.signal_count` equals the number of signal IDs;
- `signal_summary.selected_signal_id` follows
  `highest_severity_then_created_at_then_signal_id`;
- sidecar issue type, severity, recommended skill, and recommended role match
  the corresponding signal registry row when those registry fields are
  present.

At or after the activation timestamp, each source completion or handoff with
nonblank project-improvement signals must contain:

```yaml
project_improvement_bridge:
  required: true
  improvement_handoff_path: "research_control/project_improvement_handoffs/improve-project-handoff_YYYYMMDD_NNN.yaml"
  signal_ids:
    - "PIS-RT-YYYYMMDD-NNN-001"
  bridge_status: "generated"
  notes: ""
```

The `signal_ids` in that source bridge block must match the nonblank emitted
signals and must be present in the sidecar.

## Solution Plan Rules

When `solution_plan.present` is `true` or `solution_plan.status` is
`ready_to_implement`, the sidecar must include nonblank `implementation_role`
and `objective`, plus at least one `required_validators` entry and one
`plan_steps` entry.

For `ready_to_implement`, `allowed_write_paths_hint` must not name protected
science or generated-derivative paths such as `ontology/`, `legacy_ontology/`,
`manuscripts/`, `tex/`, `html/`, `wiki/`, `github-facing/`, or registered
publication-output trees.

## Resolution Rules

Terminal sidecar states must be backed by compatible terminal signal rows.
`resolved` and `closed` sidecars require success-terminal signal rows.
`rejected` sidecars require rejected signal rows. Terminal sidecars must
include nonblank `resolution.resolved_by_job_id`,
`resolution.resolution_evidence_path`, and `resolution.resolved_at`.

## Markdown Mirror Rules

Each sidecar YAML must have a Markdown mirror with the same filename stem. The
Markdown mirror must include the `improvement_handoff_id`, each signal ID, and
each issue title. The YAML remains the machine-readable authority; the Markdown
mirror is operator-facing parity evidence.
