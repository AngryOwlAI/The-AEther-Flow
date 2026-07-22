---
authority: "control"
schema_id: "dual_budget_dashboard_v1"
task_id: "RT-20260722-014"
plan_task_id: "P12-T03"
status: "draft/control"
---

# Dual-Budget Dashboard Schema v1

The dashboard is derived from registered AgentJobs and their completion
records. It has two lane objects, `physics` and `project_system`, plus category
counts, coverage, integrity checks, and an authority boundary.

Each lane reports:

- `task_count_credit`: the sum of primary credits, never the number of lane
  appearances;
- `elapsed_effort`: measured value and coverage, with absent values retained
  as `not_measured` in that lane;
- `compute`: values grouped by unit and measurement coverage, with no implicit
  zero;
- `declared_durable_output_count`; and
- `declared_acceptance_criterion_count`.

Historical jobs without a prospective allocation remain readable. Their
category and primary task credit may be classified from established route
history, but their durable-output, acceptance, and compute measurements remain
unmeasured unless a tracked record supplies them.

Required integrity fields are `single_primary_credit_status`,
`mixed_output_disjointness_status`, `mixed_acceptance_disjointness_status`,
and `missing_compute_zero_coercion_status`. Every dashboard carries explicit
false flags for physics-proof, promotion, benchmark, Gate Chair, and completed-
derivation authority.
