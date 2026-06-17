---
decision_id: "DDR-YYYYMMDD-NNN"
task_id: "RT-YYYYMMDD-NNN"
director_version: "director-of-research@0.2.0"
decision_type: "existing_role"
selected_role_id: ""
selected_role_version: ""
agent_job_id: ""
status: "proposed"
supersedes_decision_id: ""
requires_human_gate: false
role_fit_candidates:
  - "role-id|accepted-or-rejected|reason"
---

# Director Decision Record

## Current Objective

## Authority Surfaces Read

## Role-Fit Matrix

## Selected Role

If the next step is a theoretical decision among admissible packets and no
single execution role is already determined, select
`theoretical-continuation-selector@0.1.0`. Do not use generic controlled pause
for missing local data, missing experiment access, or unresolved theoretical
payload selection.

## Required Role Decomposition

For new physics research AgentJobs created after `2026-06-17T04:08:16Z`, use
`role_decomposition.mode: "parent_child_parallel_synthesis"`. Preserve one
outer AgentJob and one execution-role record; do not create child AgentJobs.
For non-physics project-system jobs, state `not_applicable`.

## Target Derivation Milestone

For new physics research AgentJobs created after `2026-06-17T15:46:25Z`, name
the `target_derivation_milestone` from
`research_control/design/gr_derivation_burden_map.md` and the exact
`milestone_burden` the job attempts to discharge. If no milestone can be
named, route the work as documentation, methodology, validation, or
project-system work rather than physics derivation work.

## Claim Boundary

## Validation
