schema_id: "external_red_team_review_artifact_schema_v1"
schema_path: ".agents/schemas/EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md"
review_id: "ERT-REVIEW-20260707-011"
task_id: "RT-20260707-011"
agent_job_id: "AJ-RT-20260707-011-001"
role_execution_ref: "external-red-team-reviewer@0.1.0--RT-20260707-011"
reviewed_object_id: "v18_p1_active_state_bifurcation"
reviewed_source_paths:
  - "implementations_plans/recommendations_implementation_plan_continue_task-v18.md"
  - "research_control/design/active_state_bifurcation_policy_v1.md"
  - "research_control/program_state.yaml"
  - "research_control/current_frontier.md"
  - "output/compact_current_frontier_v16.yaml"
  - "output/compact_current_frontier_v16.json"
  - "scripts/research_control/validate_research_control.py"
  - "tests/test_validate_research_control.py"
  - "research_control/handoffs/handoff-0679.yaml"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
claim_under_review: "The active-state bifurcation lets local agents distinguish research handoff authority from project-system sidecar status without laundering sidecars or generated frontier wording into scientific authority."
workflow_success_disregarded_as_evidence: true
validator_success_disregarded_as_evidence: true
registry_status_disregarded_as_proof: true
assumptions_read:
  - "The v18 plan requires P1-T04 to answer whether agents can identify research handoff authority, sidecar status, sidecar authority risk, generated-frontier proof overread, and next-route continuity."
  - "The active-state bifurcation policy requires explicit tracked Director-decision authorization before a project-system sidecar may supersede ordinary research handoff authority."
  - "Current rendered frontier surfaces are generated snapshots and not independent scientific authority."
  - "A validation PASS is not proof that the reviewed authority model is sufficient."
  - "This packet may route a repair but may not perform source repair or promote physics claims."
definitions_read:
  - "research handoff"
  - "project-system sidecar"
  - "compatibility pointer"
  - "sidecar supersedes research handoff"
  - "next research route source"
  - "tracked Director decision"
  - "generated frontier surface"
  - "proof authority"
  - "authority laundering"
proof_steps_checked:
  - "program_state.yaml points to active_task_id RT-20260707-010 and latest_handoff_id handoff-0679 before this review."
  - "handoff-0679 selects P1-T04 and includes active_state_bifurcation.latest_research_handoff_id handoff-0679."
  - "current_frontier.md renders an Active-State Bifurcation table with latest research handoff, sidecar fields, sidecar_supersedes_research_handoff false, and next_research_route_source latest_research_handoff."
  - "output/compact_current_frontier_v16.yaml and .json render the same bifurcation fields."
  - "validate_research_control.py compares current-frontier and compact-frontier bifurcation fields against the latest handoff."
  - "validate_research_control.py rejects sidecar supersession when no authorization flag is present."
  - "validate_research_control.py accepts explicit_sidecar_supersession_authorization from a handoff or bifurcation object without separately checking a tracked Director decision."
  - "tests/test_validate_research_control.py covers missing authorization, sidecar physics-promotion flags, ordinary later research handoff supersession, and compact-frontier drift, but not Director-decision provenance for supersession authorization."
circularity_findings:
  - "Repair-required authority circularity risk found. A handoff-level supersession flag can be treated as the evidence that authorizes sidecar supersession even though the policy requires a tracked Director decision external to the flag."
hidden_import_findings:
  - "No hidden target-metric, matter-coupling, stress-energy, Einstein-equation, benchmark, or Gate Chair premise is imported by the active-state bifurcation text."
  - "The authority defect is project-control provenance, not a hidden physics import."
notation_overload_findings:
  - "The rendered term latest_handoff_id remains a compatibility pointer and is safe when read with the Active-State Bifurcation table."
  - "The phrase explicitly authorize is under-specified in current validation behavior because it does not force Director-decision provenance."
unproven_equivalence_findings:
  - "The current validator effectively treats handoff-level explicit_sidecar_supersession_authorization as equivalent to tracked Director-decision authorization. That equivalence is not proven by the policy or by the tests."
  - "No inspected surface equates generated current-frontier output with proof authority."
minimal_countermodel_attempt:
  attempted: true
  result: "not_enough_assumptions"
  summary: "A synthetic handoff or bifurcation object could set explicit_sidecar_supersession_authorization true and next_research_route_source project_system_sidecar. The current authorization helper would accept the flag, but the inspected sources do not show a required check that a tracked Director decision row explicitly authorized the supersession. This is not a physics countermodel; it is an authority-provenance insufficiency."
  artifact_path: ""
external_mathematical_pressure_points:
  - "Strengthen _sidecar_supersession_authorized to require a Director-decision identifier or source path and verify that the DDR or registry row explicitly grants active-state sidecar supersession."
  - "Add a negative fixture where a handoff-level authorization flag exists but no Director decision authorizes supersession."
  - "Add a positive fixture where a tracked DDR explicitly authorizes bounded sidecar supersession and the sidecar preserves the latest research handoff as historical context."
  - "Render the Director-decision authorization source when sidecar_supersedes_research_handoff is true."
  - "Keep generated frontier wording explicit that it reports tracked state and is not proof authority."
verdict: "repair_required"
recommended_next_route: "v18_p1_t04_repair_active_state_supersession_director_decision_guard"
physics_promotion_authorized: false
p1_review_result: "repair_required"
repair_required: true
repair_route: "v18_p1_t04_repair_active_state_supersession_director_decision_guard"
review_questions:
  - question_id: "P1-T04-Q1"
    question: "Can a local agent identify the latest research handoff?"
    answer: "Yes. program_state.yaml, current_frontier.md, compact_current_frontier_v16.yaml, and handoff-0679 all identify handoff-0679 as the latest research handoff before this review."
    status: "pass"
  - question_id: "P1-T04-Q2"
    question: "Can a local agent identify the latest project-system sidecar?"
    answer: "Yes. The active_state_bifurcation fields render latest_project_system_task_id, latest_project_system_status, latest_project_system_sidecar_task_id, and latest_project_system_sidecar_status; all are currently none."
    status: "pass"
  - question_id: "P1-T04-Q3"
    question: "Can a sidecar accidentally become scientific authority?"
    answer: "Repair required. Sidecar recency is blocked and sidecar physics-promotion flags are checked, but a supersession authorization flag on the handoff or bifurcation object can satisfy the current helper without proving the explicit tracked Director decision required by policy."
    status: "repair_required"
  - question_id: "P1-T04-Q4"
    question: "Can generated current-frontier wording be mistaken for proof?"
    answer: "No blocking defect found as written. The frontier states it is a generated snapshot, keeps Distance-to-GR and handoff authority separate, and does not claim proof authority."
    status: "pass"
  - question_id: "P1-T04-Q5"
    question: "Does the next route remain upstream theorem/countermodel work unless explicitly superseded?"
    answer: "Repair required before routing to P2-T01. The current state routes to P1-T04 correctly, but the validator should require Director-decision provenance before any future sidecar may supersede the ordinary research next route."
    status: "repair_required"
per_surface_findings:
  - surface_id: "research_control/design/active_state_bifurcation_policy_v1.md"
    result: "pass"
    overclaim_found: false
    proof_authority_claim_found: false
    summary: "The policy states the correct authority model and requires tracked Director-decision authorization for sidecar supersession."
  - surface_id: "research_control/current_frontier.md"
    result: "pass_with_advisory"
    overclaim_found: false
    proof_authority_claim_found: false
    summary: "The rendered surface is clear in the current no-sidecar state. Future supersession rendering should name the authorizing Director decision source."
  - surface_id: "output/compact_current_frontier_v16.yaml"
    result: "pass"
    overclaim_found: false
    proof_authority_claim_found: false
    summary: "The compact frontier exposes separate research and sidecar fields and currently routes from latest_research_handoff."
  - surface_id: "scripts/research_control/validate_research_control.py"
    result: "repair_required"
    overclaim_found: false
    proof_authority_claim_found: false
    summary: "The validator checks drift and missing authorization but needs Director-decision provenance for supersession authorization."
done_criteria_status:
  review_result_is_allowed: true
  allowed_review_result: "repair_required"
  repair_route_selected_when_required: true
  pass_route_to_p2_t01_blocked_until_repair: true
gate_chair_routing_assessment:
  gate_chair_required_now: false
  reason: "The defect is project-control authorization provenance. It does not require source-law adoption, benchmark promotion, Gate Chair verdict, or completed-derivation authority."
distance_to_gr_status:
  target_derivation_milestone: "none"
  milestone_burden: "Stress the active-state bifurcation for route confusion and authority laundering."
  status_before: "no_distance_delta"
  status_after: "no_distance_delta"
  ledger_row_updated: false
  explanation: "P1-T04 reviews project-control authority separation only and creates no Distance-to-GR ledger delta."
control_payload:
  payload_id: "p1_t04_active_state_supersession_authority_provenance_gap"
  payload_type: "authority_boundary_review"
  status: "repair_required"
  artifact_path: "research_control/tasks/RT-20260707-011/artifacts/active_state_bifurcation_red_team_review_v1.md"
  summary: "The review separates correct current rendering from insufficient supersession authorization provenance."
freeze_criteria_status:
  evaluated: false
  repeated_burden_or_scoped_obstruction: false
  freeze_recommended: false
  reason: "P1-T04 is not a physics repeated-burden or scoped-obstruction route."
forbidden_conclusion_summary:
  forbidden_conclusions:
    - "P1-T04 review as proof of completed v18 implementation"
    - "P1-T04 review as physics proof"
    - "P1-T04 review as source-law adoption"
    - "P1-T04 review as general EqSrc discharge"
    - "P1-T04 review as RetainH adoption"
    - "P1-T04 review as GenH adoption"
    - "P1-T04 review as source detector/readout semantics adoption"
    - "P1-T04 review as coupling-law adoption"
    - "P1-T04 review as matter-coupling derivation or adoption"
    - "P1-T04 review as Einstein-equation derivation"
    - "P1-T04 review as benchmark promotion"
    - "P1-T04 review as Gate Chair verdict"
    - "P1-T04 review as external outreach"
    - "P1-T04 review as completed derivation"
  summary: "P1-T04 is a project-control red-team review. It routes a repair and does not promote any physics or benchmark claim."
