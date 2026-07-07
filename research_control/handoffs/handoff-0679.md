---
handoff_id: "handoff-0679"
task_id: "RT-20260707-010"
job_id: "AJ-RT-20260707-010-001"
status: "completed"
---

# Handoff 0679

RT-20260707-010 completed v18 P1-T03. Research-control validation now checks
active-state sidecar boundaries so project-system sidecars cannot silently
replace ordinary research handoff authority or claim protected physics
authority.

## Result

The validator now checks:

- sidecar supersession without explicit tracked authorization fails;
- sidecar physics-promotion or proof-authority flags fail;
- ordinary later research handoffs remain valid route authority;
- Markdown and compact-frontier active-state bifurcation fields stay synchronized.

This is project-system validation work only. It does not implement the P1-T04
red-team review, typed EqSrc schemas, physics source changes, claim promotion,
or Distance-to-GR progress.

## Next Route

Run one bounded v18 P1-T04 active-state bifurcation red-team review packet to
stress the bifurcation for route confusion and authority laundering.

```yaml
selected_next_route:
  route_id: "active_state_bifurcation_red_team_review"
  plan_task_id: "P1-T04"
  role_family: "external-red-team-reviewer@0.1.0"
  target_derivation_milestone: "none"
  milestone_burden: "Stress the active-state bifurcation for route confusion and authority laundering."
```

## Claim Boundary

P1-T03 does not authorize:

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
