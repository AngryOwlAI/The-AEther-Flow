---
authority: "control"
schema_id: "dual_budget_policy_v1"
task_id: "RT-20260722-014"
plan_task_id: "P12-T03"
status: "draft/control"
---

# Dual-Budget Policy v1

## Purpose and boundary

This prospective policy separates physics-bearing work from the research
operating system in planning, reporting, and acceptance. It is project-control
governance. It does not evaluate theorem truth, create scientific evidence,
change a Distance-to-GR burden, adopt ontology, or authorize promotion.

P12-T03 retains the existing three-consecutive-project-system-task threshold
as an advisory diagnostic. P12-T04 owns the future ordinary-route hard guard.
The hard failures introduced here concern accounting integrity and authority
separation, not route frequency.

## Categories

| Category | Definition | Required primary budget |
| --- | --- | --- |
| `physics_bearing` | Expected durable output and acceptance directly concern a scientific burden. | `physics` |
| `system_bearing` | Expected durable output and acceptance concern research-control or agent machinery. | `project_system` |
| `mixed` | One bounded task has genuinely separate outputs and acceptance criteria in both lanes. | exactly one declared lane |
| `support_only` | Tooling, fixtures, documentation, or process evidence with no scientific acceptance claim. | `project_system` |

A mixed task is not two tasks. Its two lane-specific output sets and two
lane-specific acceptance sets must be nonempty and disjoint, and exactly one
lane receives task-count credit.

## Prospective AgentJob allocation

AgentJobs created at or after `2026-07-22T18:10:44Z` declare
`dual_budget_allocation` with:

- one of the four categories and one primary budget;
- `task_count_credit.physics` and `task_count_credit.project_system`, each 0
  or 1 and summing to exactly 1;
- separate expected durable-output lists and acceptance-criterion lists;
- all four reporting dimensions: task count, elapsed effort, compute, and
  durable outputs;
- explicit measurement state for elapsed effort and compute; and
- a blocked-physics exception record.

Each budget lane carries separate elapsed-effort and compute measurements. An
unmeasured resource is represented by `status: not_measured` with `value`
omitted in strict YAML (or JSON null). It is never coerced to zero. A measured value must be
nonnegative and name its unit.

## Blocked-physics exception

A system task may name an exception when a failing control gate demonstrably
blocks an authorized physics packet. The exception requires a stable ID, a
tracked repository-relative evidence path, and the exact SHA-256 of that
evidence. The exception explains sequencing; it does not transfer the system
task into the physics budget or create a Distance-to-GR delta.

## Hard failures

Validation fails when:

1. category, primary budget, or task credit is absent or inconsistent;
2. total task credit differs from exactly one;
3. a pure physics task claims system-lane outputs or acceptance, or a pure
   system/support task claims physics-lane outputs or acceptance;
4. a mixed task omits either lane or reuses an output path or acceptance
   criterion across lanes;
5. a blocked-physics exception lacks exact tracked evidence;
6. missing compute or elapsed effort is reported as numeric zero rather than
   `not_measured`;
7. completion evidence differs from the admitted allocation; or
8. system success, validator success, or route selection is represented as
   physics success or a Distance-to-GR change.

## Acceptance and authority

Completion records must separately enumerate observed durable outputs and
accepted criteria in each lane. The metrics dashboard may aggregate these
records, but remains a support-only project-control view. No dashboard count,
ratio, checker pass, receipt, or system acceptance is physics proof.
