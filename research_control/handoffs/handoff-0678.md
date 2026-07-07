---
handoff_id: "handoff-0678"
task_id: "RT-20260707-009"
job_id: "AJ-RT-20260707-009-001"
status: "completed"
---

# Handoff 0678

RT-20260707-009 completed v18 P1-T02. The current-frontier and compact-frontier
renderers now expose explicit `active_state_bifurcation` fields that separate
research-handoff authority from project-system sidecar status.

## Result

Rendered surfaces now include:

- latest research task and handoff;
- latest research next action;
- latest project-system task and status fields;
- sidecar supersession set to false;
- next research route source set to `latest_research_handoff`;
- existing compatibility active-state fields preserved.

This is project-control renderer work only. It does not implement the P1-T03
sidecar validator, typed EqSrc schemas, physics source changes, claim
promotion, or Distance-to-GR progress.

## Next Route

Run one bounded v18 P1-T03 active-state sidecar validator and tests packet to
prevent project-system sidecars from overriding research handoffs.

```yaml
selected_next_route:
  route_id: "active_state_sidecar_validator"
  plan_task_id: "P1-T03"
  role_family: "validator-engineer@0.2.0"
  target_derivation_milestone: "none"
  milestone_burden: "Add validation that prevents project-system sidecars from silently overriding research handoffs."
```

## Claim Boundary

P1-T02 does not authorize:

- validator enforcement;
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
