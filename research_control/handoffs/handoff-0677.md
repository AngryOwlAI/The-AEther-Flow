---
handoff_id: "handoff-0677"
task_id: "RT-20260707-008"
job_id: "AJ-RT-20260707-008-001"
status: "completed"
---

# Handoff 0677

RT-20260707-008 completed v18 P1-T01. The active-state bifurcation policy now
defines how ordinary research handoff authority and project-system sidecar
status coexist in active-state surfaces.

The policy source is:

```yaml
artifact_path: "research_control/design/active_state_bifurcation_policy_v1.md"
source_hash: "5ddc84bbffc1902964da0dc916e7a6a56ce77782dc9ef1abe3896090c3f1e86e"
```

## Result

The policy distinguishes:

- latest research task and handoff authority;
- latest project-system sidecar task and status;
- compatibility fields such as `latest_handoff_id`;
- explicit supersession rules;
- renderer fields for P1-T02;
- validation hooks for P1-T03.

This is project-control policy only. It does not implement renderer behavior,
validator fixtures, typed EqSrc schemas, physics source changes, claim
promotion, or Distance-to-GR progress.

## Next Route

Run one bounded v18 P1-T02 active-state bifurcation renderer packet to add
explicit research-handoff and project-system-sidecar fields while preserving
compatibility fields.

```yaml
selected_next_route:
  route_id: "active_state_bifurcation_renderer"
  plan_task_id: "P1-T02"
  role_family: "tooling-engineer@0.1.0"
  active_role_note: "Backlog names tooling-engineer@0.1.0. The next Director decision must check active role availability and may select the closest registered project-control tooling role if that role remains unavailable."
  target_derivation_milestone: "none"
  milestone_burden: "Render explicit active_state_bifurcation fields while preserving compatibility fields."
```

## Claim Boundary

P1-T01 does not authorize:

- renderer implementation;
- validator fixture implementation;
- typed EqSrc implementation;
- source-law adoption;
- general EqSrc discharge;
- RetainH adoption;
- GenH adoption;
- source detector/readout semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- Einstein-equation derivation;
- benchmark promotion;
- external outreach;
- proof authority;
- completed derivation;
- execution of downstream v18 phases.
