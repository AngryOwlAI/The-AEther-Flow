# P1-T04 Active-State Bifurcation Red-Team Receipt

Task: `RT-20260707-011`

AgentJob: `AJ-RT-20260707-011-001`

Result: `repair_required`

The review found that current rendered active-state surfaces let a local agent
identify the latest research handoff and inactive sidecar fields, and that
generated frontier wording does not claim proof authority as written.

Repair is required because the supersession authorization predicate in
`scripts/research_control/validate_research_control.py` accepts a handoff-level
or bifurcation-level `explicit_sidecar_supersession_authorization` flag without
verifying the explicit tracked Director decision required by
`research_control/design/active_state_bifurcation_policy_v1.md`.

Next route:

`v18_p1_t04_repair_active_state_supersession_director_decision_guard`

No physics promotion, source-law adoption, benchmark promotion, Gate Chair
verdict, external outreach, or completed-derivation authority is created.
