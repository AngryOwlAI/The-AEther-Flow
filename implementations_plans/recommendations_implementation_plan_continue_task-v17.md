<!-- authority: control -->

# Recommendations Implementation Plan Continue Task v17

```yaml
plan_id: "recommendations_implementation_plan_continue_task-v17"
plan_version: "v17"
created_at: "2026-07-05"
status: "draft_control_implementation_plan"
intended_executor: "local AI agents through Continue Research functionality"
execution_mode: "one bounded Continue Research AgentJob per phase task"
current_frontier_basis:
  active_task_id: "RT-20260705-042"
  latest_handoff_id: "handoff-0615"
  current_status: "v16_completed_ordinary_continuation_selected_no_physics_delta"
  selected_next_route: "concrete_coupling_law_candidate_construction_route"
  selected_next_role_family: "candidate-constructor@0.2.0"
  selected_target_derivation_milestone: "matter_coupling"
  selected_milestone_burden: "Construct one bounded source-side coupling-law candidate from the v16 source-side coupling-law target specification and finite/local certificate evidence without adoption or downstream physics promotion."
physics_promotion_authorized: false
proof_authority: false
benchmark_promotion_authorized: false
completed_derivation_authorized: false
```

## 0. Purpose

This plan translates the full recommendation set from the project review into a sequential implementation program for the local AI agents.

The plan is designed to be consumed by the project’s Continue Research functionality. Each phase task below is intended to become exactly one bounded Continue Research AgentJob. The local agent must not batch multiple phase tasks into a single research-control transaction unless a future Director Decision Record explicitly supersedes this plan.

This plan also adds a new recommendation to fix the `accepted` wording dilemma. Earlier project work correctly noticed that bare `accepted` is dangerous in high-risk rows, but local agents have begun overcorrecting by burying real positive status under excessive caveats. The fix is not to relax claim boundaries. The fix is calibrated status language: positive-first, scope-exact, and overread-blocking without fear-based minimization.

This plan is not a physics proof, not source-law adoption, not canonical ontology adoption, not coupling-law adoption, not matter-coupling derivation, not Einstein-equation derivation, not benchmark promotion, not Gate Chair closure, and not completed derivation.

## 1. Source Basis For Local Agents

Before implementing any task from this plan, the local agent must inspect the tracked sources below through the repository memory system and direct file reads. Generated wiki notes and `.local/` cache surfaces may assist retrieval only. They must not override these sources.

### 1.1 Required active-state sources

```text
research_control/program_state.yaml
research_control/handoffs/handoff-0615.yaml
research_control/current_frontier.md
output/compact_current_frontier_v16.yaml
registries/DISTANCE_TO_GR_LEDGER.csv
research_control/tasks/RT-20260705-042/00_TASK.yaml
research_control/tasks/RT-20260705-042/jobs/completions/AJC-AJ-RT-20260705-042-001.yaml
research_control/tasks/RT-20260705-042/artifacts/v16_ordinary_continuation_selection.md
```

### 1.2 Required physics-control sources

```text
research_control/design/gr_derivation_burden_map.md
research_control/design/matter_coupling_dependency_dag_v1.md
research_control/design/matter_coupling_dependency_dag_schema_v1.md
research_control/design/matter_coupling_derivation_moratorium.md
research_control/design/matter_coupling_pre_adoption_checklist.md
research_control/design/no_target_import_guard_map.md
research_control/design/source_certificate_algebra_checklist.md
research_control/tasks/RT-20260704-021/artifacts/source_side_coupling_law_target_specification_v1.tex
research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex
research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex
research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex
research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex
research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex
research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex
research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex
research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex
research_control/tasks/RT-20260614-060/artifacts/101_RESP_LC_SOURCE_EXTENSION_HUMAN_GATE_ADOPTION_DECISION.tex
research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex
```

### 1.3 Required agent-system and validation sources

```text
AGENTS.md
research_control/AGENTS.md
research_control/tasks/README.md
Makefile
scripts/research_control/validate_research_control.py
scripts/research_control/run_full_research_control_validation.py
scripts/project_control/validate_claim_language.py
research_control/design/claim_language_linter_taxonomy.yaml
tests/test_validate_claim_language.py
scripts/research_control/report_physics_progress_metrics.py
scripts/research_control/render_current_frontier.py
scripts/research_control/render_compact_current_frontier_v16.py
scripts/research_control/render_dependency_graph.py
scripts/research_control/generate_claim_graph_v1.py
scripts/research_control/validate_claim_graph_v1.py
```

## 2. Global Implementation Rules

### 2.1 Continue Research invocation rule

Each phase task below must be implemented through Continue Research as one bounded AgentJob.

Required pattern for every task:

```yaml
execution_rule:
  continue_research_required: true
  max_agentjobs_per_invocation: 1
  task_folder_required: true
  director_decision_record_required: true
  agentjob_contract_required: true
  role_execution_record_required: true
  completion_receipt_required: true
  handoff_required: true
  documentation_impact_receipt_required: true
  validation_required: true
```

The local agent must use the repository’s active state pointer and latest handoff before choosing the next task. It must not skip ahead because a later task looks more interesting.

### 2.2 Claim boundary rule

Every task must preserve these hard blocks unless a later protected authority explicitly supersedes them:

```yaml
hard_blocks:
  - canonical ontology edit
  - source-law adoption
  - RR_ETransportCompletenessOrInvarianceLaw_v1 adoption
  - unrestricted RR_E theorem
  - matter-semantics adoption
  - detector-semantics adoption
  - coupling-law adoption
  - matter-coupling derivation or adoption
  - stress-energy semantics
  - stress-energy tensor
  - matter action
  - Einstein-equation derivation
  - benchmark promotion
  - Gate Chair benchmark closure
  - proof authority
  - completed derivation
  - future source-extension impossibility
  - program-wide no-go conclusion
```

Every task completion must include a `forbidden_conclusion_summary` or equivalent explicit field preserving these blocks.

### 2.3 Distance-to-GR rule

Physics tasks must state:

```yaml
target_derivation_milestone: "matter_coupling"
milestone_burden: "<exact task-local burden>"
distance_to_gr_delta:
  effect: "no_distance_delta | scoped_candidate_constructed_no_adoption | scoped_obstruction_recorded_no_promotion | ledger_delta_requested_after_gate"
  changed: false
```

A task may not set `changed: true` unless the task itself is an authorized Gate Chair or protected ledger-update packet whose scope explicitly permits that update.

### 2.4 Mathematical payload rule

Every physics-bearing task must include at least one new mathematical payload. Examples:

```yaml
allowed_payload_families:
  - concrete source-side relation or partial map
  - explicit finite or locally finite witness
  - explicit source certificate bundle
  - source-side detector replacement candidate
  - obstruction label with proof sketch
  - smuggling audit finding
  - Refuter stress counterexample
  - dependency-map update with proof-relevant consequence
  - proof-normal-form extraction
  - finite model or model-checkable witness
```

Project-system tasks may have `new_mathematical_payload: []`, but they must state `project_system_change_only: true` and `physics_promotion_authorized: false`.

### 2.5 Validation rule

Every task must run the narrowest appropriate validations and then the full research-control validation before closure.

Minimum validation sequence:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/project_control/validate_claim_language.py --changed --json
.venv/bin/python scripts/project_control/validate_documentation_impact.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/research_control/run_full_research_control_validation.py --json
```

If a task changes scripts or tests, also run:

```zsh
.venv/bin/python -m unittest discover -s tests
```

If a task changes current-frontier, compact-frontier, dependency-graph, or claim-graph behavior, also run:

```zsh
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_compact_current_frontier_v16.py --check
.venv/bin/python scripts/research_control/render_dependency_graph.py --check
.venv/bin/python scripts/research_control/generate_claim_graph_v1.py --check
.venv/bin/python scripts/research_control/validate_claim_graph_v1.py --json
```

### 2.6 Project-system boundary rule

Several tasks below are project-system tasks. The user has explicitly requested that Continue Research functionality be used to implement each phase and task. Therefore, every project-system task must include in its AgentJob contract:

```yaml
project_system_boundary_authorized_by_plan: true
source_authorization: "recommendations_implementation_plan_continue_task-v17"
physics_claims_changed: false
```

Project-system tasks may edit control Markdown, schemas, scripts, tests, renderers, and generated outputs only inside their declared scope. They must not edit canonical science TeX unless the task is explicitly a science-draft task and the claim boundary permits it.

## 3. Added Recommendation: Fix The `accepted` Dilemma Through Calibrated Acceptance Language

### 3.1 Problem statement

The project correctly identified that bare `accepted` is dangerous in high-risk rows because readers and agents can overread it as physical adoption, source-law adoption, matter-coupling derivation, Einstein equations, or benchmark promotion.

A second problem has now appeared: local AI agents may overcorrect out of fear of overclaiming. They may write status summaries that bury real positive results under caveat walls, treating legitimate scoped adoption as if it were barely meaningful. That underclaims the tracked research state and makes the frontier hard to read.

The correct resolution is calibrated acceptance language.

### 3.2 Recommendation M: Calibrated acceptance status cards

Add a status-card model for every high-risk accepted row and every public or agent-facing summary that references it.

Each status card must contain four fields in this order:

```yaml
status_card:
  object_id: "m_src | g_eff | matter_coupling | ..."
  positive_status: "what is actually established"
  exact_scope: "where the positive status is valid"
  allowed_use: "what later tasks may use it for"
  blocked_overread: "what must not be inferred"
```

The positive status must come first. The exact scope must be precise rather than apologetic. The blocked-overread field must be complete enough for safety but concise enough not to swallow the positive content.

### 3.3 Required wording pattern

Use this pattern:

```text
Positive status: <object> is <accepted/adopted> as <exact scoped category>.
Scope: This status is valid only under <declared source-side scope>.
Allowed use: Later bounded packets may use it for <specific next-route support>.
Blocked overread: This does not establish <short blocked list>.
```

Do not use this fear-based pattern:

```text
Bad example: <object> is accepted, but only as a heavily qualified thing, but not really physical, but not a derivation, but not many other things, so do not read too much into it.
```

The first pattern is exact. The second pattern trains agents to underclaim.

### 3.4 Examples for high-risk rows

#### `M_src`

Preferred:

```text
Positive status: M_src is adopted as a scoped source-only M_src object.
Scope: The adoption applies to the audited and stressed GSC candidate under its declared source-only H1-H13 and fail-closed boundary.
Allowed use: Later bounded packets may use it as source-side prerequisite context for effective-metric and matter-sector continuation.
Blocked overread: It is not a target manifold, metric, matter-coupling result, Einstein-equation result, benchmark promotion, or completed derivation.
```

Avoid:

```text
Bad example: M_src is only sort of accepted and should not be taken seriously as anything because it is not GR.
```

#### `g_eff`

Preferred:

```text
Positive status: g_eff is adopted as a scoped source-extension g_eff object.
Scope: The adoption applies only to the declared GSC source-extension candidate and not to arbitrary source packages or target Lorentzian geometry.
Allowed use: Later bounded packets may use it as scoped source-extension context for matter-coupling precondition work.
Blocked overread: It is not an unscoped Lorentzian metric, MetricData(E) adoption, matter coupling, Einstein equations, benchmark promotion, or completed derivation.
```

Avoid:

```text
Bad example: g_eff is accepted, but it is basically not useful because it is not a real metric.
```

#### `matter_coupling`

Preferred:

```text
Positive status: matter_coupling has accepted scoped evidence/precondition only for continuation.
Scope: The support is certificate-indexed and finite/local, covering source-side evidence and operation-law discipline only.
Allowed use: Later bounded packets may use it to construct, audit, or stress one source-side coupling-law candidate.
Blocked overread: It is not source-law adoption, matter-semantics adoption, detector-semantics adoption, coupling-law adoption, matter-coupling derivation, stress-energy semantics, matter action, Einstein equations, benchmark promotion, or completed derivation.
```

Avoid:

```text
Bad example: matter_coupling is accepted, but nothing has happened.
```

### 3.5 Machine-readable acceptance schema

Add or extend a machine-readable status layer with these fields:

```yaml
acceptance_calibration_v1:
  object_id: string
  status_family: scoped_source_object | scoped_source_extension_object | scoped_evidence_precondition | draft_control | blocked | frozen_negative | not_started
  positive_status_sentence: string
  exact_scope_sentence: string
  allowed_use_sentence: string
  blocked_overread_sentence: string
  underclaim_guard: string
  overclaim_guard: string
  public_summary_max_blocked_items: integer
  full_control_blocked_items: list[string]
```

The `underclaim_guard` should prevent language that minimizes real positive status. The `overclaim_guard` should preserve existing hard boundaries.

### 3.6 Linter policy

Existing claim-language linting catches overclaim. Add an advisory underclaim calibration linter. It should not initially hard-fail tasks. It should warn when high-risk rows:

1. use bare `accepted` without a scoped category;
2. omit the positive status sentence;
3. list blocked overreads before stating the positive status;
4. use minimization language such as `only sort of`, `not really`, `basically nothing`, `merely administrative`, or equivalent phrasing for scoped adopted objects;
5. repeat the same blocked list so often that the positive content disappears in reader-facing summaries.

After at least one full v17 validation cycle, the Director may promote selected advisory underclaim checks to hard checks for public-facing and current-frontier surfaces.

### 3.7 Local AI agent behavior rule

When summarizing a high-risk row, the local AI agent must answer three questions in order:

```text
1. What is positively established?
2. Under what exact scope is it established?
3. What must not be inferred from it?
```

The local agent must not answer only the third question.

## 4. Recommendation Integration Matrix

| Recommendation ID | Recommendation | Implementation phase(s) | Primary route type | Physics delta expected |
| --- | --- | --- | --- | --- |
| A | Execute the selected concrete coupling-law candidate route | P1, P2 | physics candidate construction, audit, stress | candidate only, no adoption |
| B | Treat the first candidate as audit-eligible only | P1, P2 | claim-boundary enforcement | no distance delta |
| C | Make detector semantics central | P4 | physics selector and candidate work | candidate or obstruction only |
| D | Add metric-use ledger for g_eff in matter work | P5 | project-system plus physics-control support | no distance delta |
| E | Revisit EqSrc, RetainH, GenH after first candidate cycle | P6 | theoretical selector | no direct promotion |
| F | Add proof-normal-form layer | P7 | project-system formalization support | no distance delta |
| G | Mechanize low-level formal fragments | P8 | support-only formalization | no physics proof authority |
| H | Publish proof-state dashboard | P9 | documentation/control renderer | no distance delta |
| I | Replace dangerous bare accepted renderings | P3 | accepted calibration | no distance delta |
| J | Add generated task index | P10 | project-system tooling | no distance delta |
| K | Strengthen CI and reproducibility | P11 | project-system tooling | no distance delta |
| L | Evaluate AI research-agent system as scientific instrument | P12 | methodology metrics | no physics promotion |
| M | Fix accepted dilemma with calibrated acceptance language | P3, P9 | status semantics and linter calibration | no distance delta |

## 5. Phase P0: V17 Intake, Registration, And Active-State Synchronization

### P0 objective

Register this v17 plan as a tracked implementation-control source, synchronize the active frontier, and create a v17 execution backlog without changing any physics claim.

### P0-T01: Register the v17 implementation plan

```yaml
plan_task_id: "P0-T01"
task_type: "v17_plan_registration"
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Register v17 implementation plan as control source with no physics delta."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "project_control_plan_registration_no_physics_delta"
```

#### Objective

Add `implementations_plans/recommendations_implementation_plan_continue_task-v17.md` to the repository and register it in the appropriate source registry.

#### Required inputs

```text
implementations_plans/recommendations_implementation_plan_continue_task-v17.md
registries/MARKDOWN_SOURCE_REGISTRY.csv
AGENTS.md
research_control/AGENTS.md
```

#### Required outputs

```text
research_control/tasks/<new-task-id>/00_TASK.yaml
research_control/tasks/<new-task-id>/DDR-<id>.md
research_control/tasks/<new-task-id>/jobs/AJ-<id>.yaml
research_control/tasks/<new-task-id>/roles/director-of-research@0.3.0--<task-id>.yaml
research_control/tasks/<new-task-id>/jobs/completions/AJC-<id>.yaml
research_control/tasks/<new-task-id>/documentation_impact.yaml
research_control/handoffs/handoff-<next>.yaml
research_control/handoffs/handoff-<next>.md
registries/MARKDOWN_SOURCE_REGISTRY.csv
wiki/markdown/<generated-plan-wiki-note>.md
```

#### Done criteria

- The v17 plan is tracked under `implementations_plans/`.
- The plan is registered as canonical/control Markdown.
- Memory bootstrap and research-control validation pass.
- The completion says `distance_to_gr_delta.changed: false`.
- The next route is P0-T02.

#### Forbidden conclusions

- The v17 plan does not prove any physics result.
- The v17 plan does not supersede the active `handoff-0615` scientific next route until a tracked v17 handoff sequences it.

### P0-T02: Build the v17 execution backlog

```yaml
plan_task_id: "P0-T02"
task_type: "v17_execution_backlog_materialization"
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Create a task-addressable v17 backlog from the implementation plan."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "project_control_backlog_no_physics_delta"
```

#### Objective

Create a machine-readable v17 backlog that maps each phase task to route type, role family, dependencies, outputs, validation commands, and handoff behavior.

#### Required output

```text
research_control/design/v17_recommendation_backlog.yaml
research_control/design/v17_recommendation_backlog_schema.md
```

#### Backlog fields

```yaml
backlog_item:
  plan_task_id: string
  phase_id: string
  title: string
  depends_on: list[string]
  role_family: string
  task_type: string
  target_derivation_milestone: string
  milestone_burden: string
  expected_outputs: list[string]
  required_validators: list[string]
  physics_delta_allowed: boolean
  promotion_allowed: boolean
  next_route_on_success: string
  next_route_on_failure: string
```

#### Done criteria

- Every task in this plan appears exactly once in the backlog.
- Dependencies are acyclic.
- The backlog marks P1-T01 as the first physics-bearing task after P0.
- Project-system tasks include `project_system_boundary_authorized_by_plan: true`.
- The completion routes to P0-T03.

### P0-T03: Active-state and source-basis preflight

```yaml
plan_task_id: "P0-T03"
task_type: "v17_active_state_preflight"
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Verify active-state sources before executing v17 physics or project-system tasks."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "preflight_no_physics_delta"
```

#### Objective

Confirm that the active state still matches the v16 frontier and that no intervening task has changed the next lawful route.

#### Required checks

- `program_state.yaml` points to the latest handoff.
- The latest handoff still selects concrete coupling-law candidate construction, unless a newer tracked handoff supersedes it.
- `current_frontier.md` and `compact_current_frontier_v16.yaml` are synchronized.
- The Distance-to-GR ledger still blocks matter-coupling adoption, Einstein equations, and benchmark promotion.

#### Done criteria

- Preflight report exists.
- Drift is either absent or routed to a deterministic repair task.
- The next route is P1-T01 unless drift requires a repair task.

#### Required output

```text
research_control/tasks/<task-id>/artifacts/v17_active_state_preflight_report.json
```

## 6. Phase P1: Construct One Concrete Source-Side Coupling-Law Candidate

### P1 objective

Implement the active next route selected by v16: construct exactly one bounded source-side coupling-law candidate from the v16 target specification and finite/local certificate evidence, without adoption or downstream promotion.

### P1-T01: Candidate-constructor packet setup

```yaml
plan_task_id: "P1-T01"
task_type: "concrete_coupling_law_candidate_construction_setup"
role_family: "candidate-constructor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Set up one bounded source-side coupling-law candidate construction packet using the v16 target specification."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "candidate_setup_no_adoption"
```

#### Objective

Define the exact candidate-construction envelope for one source-side relation or partial map `K_E`.

#### Required inputs

```text
research_control/tasks/RT-20260704-021/artifacts/source_side_coupling_law_target_specification_v1.tex
research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex
research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex
research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex
research_control/design/no_target_import_guard_map.md
research_control/design/matter_coupling_dependency_dag_v1.md
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/coupling_law_candidate_construction_setup_v1.md
```

#### Setup must define

```yaml
candidate_setup:
  candidate_name: "SourceCouplingLawCandidate_<short-id>_v1"
  source_event_or_scope_symbol: "E_*"
  source_input_scope: "SMScope(E_*)"
  candidate_relation_symbol: "K_{E_*}"
  certificate_bundle_symbol: "SCLBundle(E_*)"
  detector_placeholder_symbol: "DetPlaceholder(E_*)"
  finite_local_witness_obligation: true
  no_target_import_guard_required: true
  max_candidate_count: 1
  adoption_requested: false
```

#### Done criteria

- The setup names exactly one candidate target.
- The setup names the required fields from the v16 validity predicate.
- The setup says the next task must construct or fail with one precise obstruction.
- No adoption or matter-coupling derivation is claimed.

### P1-T02: Construct the concrete source-side candidate `K_E`

```yaml
plan_task_id: "P1-T02"
task_type: "concrete_coupling_law_candidate_construction"
role_family: "candidate-constructor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Construct one bounded source-side coupling-law candidate K_E or record one precise construction obstruction."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "candidate_constructed_or_obstruction_no_adoption"
```

#### Objective

Construct a concrete source-side relation or partial map `K_E` that is eligible for later audit and stress, or record a precise obstruction explaining why such a candidate cannot be constructed in this route.

#### Required science artifact

```text
research_control/tasks/<task-id>/artifacts/source_side_coupling_law_candidate_v1.tex
```

#### Required candidate structure

The `.tex` artifact must include these sections:

1. Control Status
2. Imported Source-Side Vocabulary
3. Source Matter-Semantics Input Scope `SMScope(E_*)`
4. Explicit Source Coupling-Law Certificate Bundle `SCLBundle(E_*)`
5. Detector-Semantics Replacement Placeholder Or Blocked Marker
6. Candidate Relation Or Partial Map `K_{E_*}`
7. No-Target Coupling Import Guard
8. Finite/Local Witness Or Precise Obstruction
9. Validity Predicate Evaluation Against `SourceCouplingLawTarget_src^cand_v1`
10. Distance-to-GR Effect
11. Forbidden Conclusions
12. Next Route
13. Source Materials

#### Required mathematical payload

One of the following must exist:

```yaml
positive_payload:
  payload_type: "concrete_relation_or_partial_map"
  object_name: "K_{E_*}"
  evidence: "finite_or_locally_finite_source_scope_plus_explicit_certificates"
  audit_eligible_only: true
```

or:

```yaml
obstruction_payload:
  payload_type: "construction_obstruction"
  obstruction_id: "OB-V17-SCL-CAND-<short-label>"
  obstruction_scope: "current v17 coupling-law candidate construction route only"
  global_no_go_claimed: false
```

#### Candidate validity floor

A positive candidate must state:

```yaml
candidate_validity_floor:
  SMScope_declared: true
  certificate_bundle_explicit: true
  detector_placeholder_or_blocked_marker_present: true
  no_target_guard_present: true
  K_E_source_side_relation_or_partial_map_named: true
  finite_local_witness_or_obstruction_present: true
  eligible_for_audit_stress_only: true
  coupling_law_adopted: false
  matter_coupling_derived: false
```

#### Done criteria

- Exactly one candidate or exactly one obstruction is produced.
- No adoption is requested.
- No source law is adopted.
- The artifact is registered in the TeX registry.
- The next route is P1-T03 for self-check if a candidate exists, or P2-T03 selector if an obstruction exists.

### P1-T03: Candidate self-check against v16 target specification

```yaml
plan_task_id: "P1-T03"
task_type: "coupling_law_candidate_target_self_check"
role_family: "candidate-constructor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Check the constructed candidate against the v16 target specification before audit."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "candidate_self_check_no_adoption"
```

#### Objective

Produce a structured self-check showing whether the candidate satisfies the minimum target-specification floor for audit eligibility.

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/source_side_coupling_law_candidate_self_check_v1.yaml
```

#### Required fields

```yaml
candidate_self_check_v1:
  candidate_artifact_path: string
  candidate_name: string
  SMScope_declared: pass | fail
  explicit_certificate_bundle: pass | fail
  detector_placeholder_or_blocked_marker: pass | fail
  no_target_guard: pass | fail
  source_side_relation_or_partial_map: pass | fail
  finite_local_witness_or_obstruction: pass | fail
  primary_fail_closed_branch: string | none
  eligible_for_smuggling_audit: true | false
  eligible_for_refuter_stress: true | false
  adoption_language_detected: true | false
  downstream_gr_language_detected: true | false
```

#### Done criteria

- If self-check passes, route to P2-T01 smuggling audit.
- If self-check fails, route to P2-T03 selector for repair, obstruction, or freeze classification.
- The completion does not claim audit success or stress success.

### P1-T04: Candidate handoff to audit lane

```yaml
plan_task_id: "P1-T04"
task_type: "coupling_law_candidate_audit_handoff"
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Route the constructed candidate to smuggling audit or route an obstruction to selector review."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "candidate_handoff_no_adoption"
```

#### Objective

Create a handoff that chooses exactly one next packet after candidate construction.

#### Candidate dispositions

```yaml
candidate_disposition_options:
  - route_to_smuggling_audit
  - route_to_repair_candidate_constructor
  - route_to_refuter_for_obstruction_stress
  - route_to_theoretical_selector
  - route_to_freeze_review
```

#### Done criteria

- Exactly one disposition is selected.
- Candidate status remains `draft/control` or `audit_eligible_only`.
- No Gate Chair route is selected unless a later audit and stress chain supports a protected question.

## 7. Phase P2: Audit, Stress, And Candidate Route Decision

### P2 objective

Ensure any constructed candidate is treated as audit-eligible only. Audit it for target imports, stress it for collapse modes, and route a bounded next action.

### P2-T01: Smuggling audit of source-side coupling-law candidate

```yaml
plan_task_id: "P2-T01"
task_type: "coupling_law_candidate_smuggling_audit"
role_family: "smuggling-auditor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Audit the coupling-law candidate for target import, detector import, stress-energy import, matter-action import, benchmark import, and process-authority laundering."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "candidate_audited_no_adoption"
```

#### Audit targets

The audit must test for:

```yaml
audit_targets:
  - target topology import
  - target smooth atlas import
  - target Lorentzian metric import
  - proper-time normalization import
  - detector protocol import
  - empirical calibration import
  - stress-energy semantics import
  - stress-energy tensor import
  - matter action import
  - Einstein-equation premise import
  - benchmark behavior import
  - generated derivative as premise
  - registry metadata as premise
  - validator status as premise
  - role identity as premise
  - handoff or approval status as premise
  - local cache state as premise
  - file order or commit state as premise
  - scoped evidence treated as adoption
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/source_side_coupling_law_candidate_smuggling_audit_v1.tex
```

#### Done criteria

- Audit result is one of `source_pure_as_written`, `repair_required`, or `fails_closed`.
- Audit result does not adopt the candidate.
- Any failure names one primary obstruction label.
- Success routes to P2-T02 Refuter stress.
- Failure routes to P2-T03 selector.

### P2-T02: Refuter stress of source-side coupling-law candidate

```yaml
plan_task_id: "P2-T02"
task_type: "coupling_law_candidate_refuter_stress"
role_family: "refuter@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Stress the audited candidate against finite/local perturbation, missing-certificate, detector-placeholder, evidence-as-adoption, and metric-use collapse modes."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "candidate_stressed_no_adoption"
```

#### Stress modes

The Refuter must test at least these modes:

```yaml
stress_modes:
  - finite_or_local_scope_perturbation
  - certificate_removal
  - malformed_certificate_replacement
  - target_import_attack
  - detector_placeholder_erasure
  - detector_placeholder_replacement_by_empirical_protocol
  - K_E_domain_collapse
  - K_E_codomains_not_source_side
  - RR_E_unrestricted_theorem_overread
  - evidence_as_adoption_laundering
  - g_eff_as_physical_metric_overread
  - stress_energy_semantics_import
  - matter_action_import
  - benchmark_behavior_import
  - process_authority_import
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/source_side_coupling_law_candidate_refuter_stress_v1.tex
```

#### Done criteria

- Stress result is one of `stress_survives_as_draft_control_candidate`, `repair_required`, `scoped_obstruction`, or `freeze_candidate_route`.
- The result does not adopt the candidate.
- The result does not derive matter coupling.
- The next route is P2-T03 selector.

### P2-T03: Theoretical selector after candidate audit and stress

```yaml
plan_task_id: "P2-T03"
task_type: "post_candidate_audit_stress_selector"
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Select one next route after candidate construction, audit, and stress."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "selector_no_adoption"
```

#### Allowed routes

```yaml
allowed_next_routes:
  - repair_candidate_constructor_packet
  - detector_semantics_replacement_packet
  - metric_use_ledger_integration_packet
  - candidate_refuter_followup_packet
  - scoped_obstruction_freeze_review
  - protected_gate_question_setup_only
  - upstream_EqSrc_RetainH_GenH_selector
```

#### Disallowed routes

```yaml
disallowed_next_routes:
  - coupling_law_adoption
  - matter_coupling_derivation
  - stress_energy_tensor_construction_without_semantics
  - matter_action_construction_without_dynamics_route
  - Einstein_equation_derivation
  - benchmark_promotion
  - completed_derivation_claim
```

#### Done criteria

- Exactly one next route is selected.
- The selector states why alternatives were not selected.
- The selector evaluates freeze criteria if the candidate route repeats a known obstruction.

### P2-T04: Candidate-cycle integration report

```yaml
plan_task_id: "P2-T04"
task_type: "coupling_law_candidate_cycle_integration_report"
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Integrate candidate construction, audit, stress, and selector results into current frontier without promotion."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "candidate_cycle_integrated_no_adoption"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/v17_coupling_law_candidate_cycle_report.md
```

#### Required report sections

1. Candidate status
2. Audit status
3. Stress status
4. Obstruction or repair status
5. Distance-to-GR effect
6. Current blocked claims
7. Next exact route

#### Done criteria

- The current frontier reflects candidate-cycle status without overclaim.
- The Distance-to-GR ledger is unchanged unless a separately authorized ledger packet exists.
- The next route is either P3 or the selector-chosen route.

## 8. Phase P3: Calibrated Accepted-Language System

### P3 objective

Fix the `accepted` dilemma by preserving anti-overclaim protection while preventing local agents from underclaiming real scoped positive results.

### P3-T01: Acceptance calibration design note

```yaml
plan_task_id: "P3-T01"
task_type: "accepted_status_calibration_design_note"
role_family: "documentation-curator@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Define calibrated acceptance language for high-risk rows with no physics delta."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "status_language_design_no_physics_delta"
```

#### Objective

Create a control note that defines calibrated acceptance language and distinguishes overclaim prevention from fear-based underclaiming.

#### Required artifact

```text
research_control/design/accepted_status_calibration_policy_v1.md
```

#### Required sections

1. Problem statement
2. Calibrated acceptance principle
3. Positive-first status-card model
4. High-risk rows covered
5. Preferred wording patterns
6. Forbidden overclaim patterns
7. Forbidden underclaim patterns
8. Public-summary compression rule
9. Full-control non-conclusion rule
10. Renderer and linter implementation requirements
11. Examples for `M_src`, `g_eff`, `matter_coupling`, `Resp_lc`, `NarrowMSCertEq_v1`, and frozen-negative routes

#### Done criteria

- The policy says positive status first, exact scope second, blocked overread third.
- The policy preserves all existing hard blocks.
- The policy explicitly forbids treating scoped adoption as “basically nothing.”
- The policy is registered and validated.

### P3-T02: Acceptance calibration schema and alias update

```yaml
plan_task_id: "P3-T02"
task_type: "accepted_status_calibration_schema_alias_update"
role_family: "schema-maintainer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Add machine-readable acceptance calibration fields for high-risk status rows."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "schema_update_no_physics_delta"
```

#### Required outputs

```text
research_control/design/accepted_status_calibration_schema_v1.md
research_control/design/accepted_status_calibration_v1.yaml
research_control/design/distance_to_gr_status_aliases.yaml
```

#### Required YAML structure

```yaml
accepted_status_calibration_v1:
  high_risk_objects:
    m_src:
      status_family: "scoped_source_object"
      positive_status_sentence: "M_src is adopted as a scoped source-only M_src object."
      exact_scope_sentence: "The adoption applies only under the declared source-only GSC candidate scope and fail-closed boundary."
      allowed_use_sentence: "Later bounded packets may use it as source-side prerequisite context."
      blocked_overread_sentence: "It is not a target manifold, metric, matter coupling, Einstein equations, benchmark promotion, or completed derivation."
      public_summary_max_blocked_items: 6
    g_eff:
      status_family: "scoped_source_extension_object"
      positive_status_sentence: "g_eff is adopted as a scoped source-extension g_eff object."
      exact_scope_sentence: "The adoption applies only to the declared source-extension candidate scope."
      allowed_use_sentence: "Later bounded packets may use it as scoped source-extension context."
      blocked_overread_sentence: "It is not an unscoped Lorentzian metric, MetricData(E) adoption, matter coupling, Einstein equations, benchmark promotion, or completed derivation."
      public_summary_max_blocked_items: 6
    matter_coupling:
      status_family: "scoped_evidence_precondition"
      positive_status_sentence: "matter_coupling has accepted scoped evidence/precondition only for continuation."
      exact_scope_sentence: "The support is certificate-indexed, source-side, and finite/local only."
      allowed_use_sentence: "Later bounded packets may use it to construct, audit, or stress one source-side coupling-law candidate."
      blocked_overread_sentence: "It is not source-law adoption, detector semantics, coupling-law adoption, matter-coupling derivation, stress-energy, matter action, Einstein equations, benchmark promotion, or completed derivation."
      public_summary_max_blocked_items: 9
```

#### Done criteria

- High-risk rows no longer need bare `accepted` in reader-facing output.
- Alias fields provide positive status, scope, allowed use, and blocked overread.
- Existing alias behavior is preserved or superseded deterministically.

### P3-T03: Claim-language linter underclaim calibration

```yaml
plan_task_id: "P3-T03"
task_type: "claim_language_underclaim_calibration_linter"
role_family: "validator-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Add advisory underclaim calibration checks while preserving hard overclaim checks."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "validator_update_no_physics_delta"
```

#### Required modifications

```text
scripts/project_control/validate_claim_language.py
research_control/design/claim_language_linter_taxonomy.yaml
tests/test_validate_claim_language.py
tests/fixtures/claim_language/accepted_underclaim_overcorrection.md
tests/fixtures/claim_language/accepted_calibrated_valid.md
```

#### Advisory finding classes

```yaml
new_advisory_classes:
  accepted_positive_status_missing:
    severity: "warn_current_control"
    description: "High-risk accepted row states caveats without positive scoped status."
  accepted_scope_after_blocked_overread:
    severity: "warn_current_control"
    description: "High-risk accepted row lists blocked overreads before exact positive scope."
  scoped_adoption_minimized:
    severity: "warn_current_control"
    description: "Scoped adopted object is described as basically meaningless or not real."
  caveat_wall_public_summary:
    severity: "warn_public_summary"
    description: "Reader-facing summary repeats blocked claims so heavily that positive status is obscured."
```

#### Tests

Add tests that verify:

- Bare high-risk `accepted` still fails.
- Public overclaims still fail.
- “M_src is adopted as a scoped source-only object” passes.
- “g_eff is adopted as a scoped source-extension object” passes with boundary language.
- “matter_coupling has accepted scoped evidence/precondition only for continuation” passes with blocked-overread language.
- “M_src is not really anything” warns as underclaim.
- A caveat-only summary warns as underclaim.

#### Done criteria

- Overclaim tests still pass.
- Underclaim tests warn but do not hard-fail unless the changed surface is explicitly configured for hard enforcement.
- The linter report distinguishes `overclaim_hard_fail` from `underclaim_calibration_warning`.

### P3-T04: Renderer update for positive-first status cards

```yaml
plan_task_id: "P3-T04"
task_type: "positive_first_status_card_renderer_update"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Update frontier and compact-frontier renderers to use calibrated positive-first status cards."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "renderer_update_no_physics_delta"
```

#### Required modifications

```text
scripts/research_control/render_current_frontier.py
scripts/research_control/render_compact_current_frontier_v16.py
research_control/current_frontier.md
output/compact_current_frontier_v16.yaml
output/compact_current_frontier_v16.json
wiki/indexes/compact_current_frontier_v16.md
```

#### Rendering requirements

Every high-risk row must render as:

```markdown
**Positive status:** ...
**Scope:** ...
**Allowed use:** ...
**Blocked overread:** ...
```

Compact YAML must expose the same model:

```yaml
high_risk_status_card:
  object_id: "g_eff"
  positive_status: "..."
  exact_scope: "..."
  allowed_use: "..."
  blocked_overread:
    - "..."
```

#### Done criteria

- `current_frontier.md` no longer relies on bare `accepted` in high-risk reader-facing rows.
- Compact frontier has machine-readable status cards.
- Render checks pass.
- Claim-language linter reports no hard failures.

### P3-T05: Public-facing documentation calibration pass

```yaml
plan_task_id: "P3-T05"
task_type: "public_documentation_accepted_calibration_pass"
role_family: "documentation-curator@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Update public-facing summaries to use calibrated acceptance language without changing claim status."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "documentation_update_no_physics_delta"
```

#### Candidate files

```text
README.md
github-facing/project-overview-explainer.md
github-facing/aether-flow-physics-program-explainer.md
github-facing/exact-gr-benchmark-boundary-explainer.md
github-facing/gr-derivation-roadmap-explainer.md
github-facing/claim-gates-explainer.md
github-facing/negative-results-and-obstructions-explainer.md
markdown/html-explainer-specs/*.md
markdown/publication-briefs/*.md
```

#### Documentation rules

- Replace fear-based underclaim language with positive-first scope-exact wording.
- Keep public-safe status: GR is not derived, matter coupling is not derived, Einstein equations are not started, benchmark promotion is blocked.
- Do not add any new physics claim.
- Do not hand-edit generated HTML unless the established explainer pipeline requires regeneration from registered source specs.

#### Done criteria

- Public docs remain accurate.
- No public overclaim hard failures.
- Underclaim calibration warnings are resolved or justified.
- Documentation-impact receipt explains every changed surface.

### P3-T06: Acceptance calibration red-team review

```yaml
plan_task_id: "P3-T06"
task_type: "accepted_status_calibration_red_team_review"
role_family: "external-red-team-reviewer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Stress-test calibrated acceptance language for both overclaim and underclaim."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "red_team_review_no_physics_delta"
```

#### Review questions

1. Does the revised language overclaim scoped status as physical derivation?
2. Does the revised language underclaim real scoped adoption as nothing?
3. Can a reader identify what is positively established for `M_src`?
4. Can a reader identify what is positively established for `g_eff`?
5. Can a reader identify what matter-coupling evidence/preconditions support?
6. Are blocked claims concise but complete?
7. Does the local agent have deterministic wording rules?

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/accepted_status_calibration_red_team_review_v1.md
```

#### Done criteria

- Review returns `pass`, `pass_with_advisory`, or `repair_required`.
- Any repair route is routed as exactly one next Continue Research task.
- No physics claim changes.

## 9. Phase P4: Detector-Semantics Replacement Program

### P4 objective

Make detector semantics central by constructing, refuting, or precisely blocking a source-side replacement for detector semantics in the matter-coupling lane.

### P4-T01: Detector-semantics replacement problem statement

```yaml
plan_task_id: "P4-T01"
task_type: "detector_semantics_replacement_problem_statement"
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Define the exact detector-semantics replacement burden for source-side coupling-law candidates."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_problem_statement_no_adoption"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/detector_semantics_replacement_problem_statement_v1.md
```

#### Required content

- What detector semantics would normally contribute.
- Which parts are forbidden as target or empirical imports.
- What a source-side replacement must supply.
- How the replacement interacts with `DetPlaceholder(E)`.
- What counts as a constructive witness.
- What counts as a scoped obstruction.
- What would require an ontology-law research packet.

#### Done criteria

- The next route is one of constructive replacement, obstruction theorem, or ontology-law selector.
- No detector semantics are adopted.

### P4-T02: Construct one source-side detector-replacement candidate or obstruction

```yaml
plan_task_id: "P4-T02"
task_type: "detector_semantics_replacement_candidate_or_obstruction"
role_family: "candidate-constructor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Construct one source-side detector-replacement candidate or record one precise obstruction."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_replacement_candidate_or_obstruction_no_adoption"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/detector_semantics_replacement_candidate_v1.tex
```

#### Positive candidate must include

```yaml
detector_replacement_candidate:
  source_domain: string
  readout_interface: string
  certificate: string
  status: "supplied_source_placeholder"
  no_empirical_protocol_import: true
  no_proper_time_import: true
  no_target_metric_import: true
  finite_local_witness: string
```

#### Obstruction must include

```yaml
detector_replacement_obstruction:
  obstruction_id: "OB-V17-DET-<short-label>"
  exact_missing_burden: string
  scoped_to_current_route: true
  global_no_go_claimed: false
```

#### Done criteria

- Exactly one candidate or one obstruction is produced.
- No detector semantics are adopted.
- Candidate routes to audit and stress.
- Obstruction routes to selector.

### P4-T03: Detector-replacement smuggling audit

```yaml
plan_task_id: "P4-T03"
task_type: "detector_replacement_smuggling_audit"
role_family: "smuggling-auditor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Audit detector-replacement candidate for empirical detector, target metric, proper-time, benchmark, or process-authority imports."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_replacement_audited_no_adoption"
```

#### Done criteria

- Audit classifies candidate as source-pure as written, repair-required, or fail-closed.
- No detector semantics are adopted.
- No matter coupling is derived.

### P4-T04: Detector-replacement Refuter stress

```yaml
plan_task_id: "P4-T04"
task_type: "detector_replacement_refuter_stress"
role_family: "refuter@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Stress detector replacement against placeholder collapse, empirical-protocol substitution, and finite/local perturbations."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_replacement_stressed_no_adoption"
```

#### Stress modes

- Erase readout-interface fields.
- Replace source readout with empirical detector protocol.
- Replace source normalization with proper time.
- Use target metric to define detector response.
- Treat placeholder status as detector adoption.
- Check finite/local witness stability.

#### Done criteria

- Stress result is `survives_as_source_replacement_candidate`, `repair_required`, `scoped_obstruction`, or `freeze_route`.
- No detector semantics are adopted.

### P4-T05: Detector route selector

```yaml
plan_task_id: "P4-T05"
task_type: "detector_replacement_route_selector"
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Select one next route after detector replacement candidate or obstruction."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_route_selected_no_adoption"
```

#### Allowed next routes

- Integrate detector replacement into `K_E` candidate repair.
- Route detector obstruction freeze review.
- Route ontology-law research packet for missing source primitive.
- Route metric-use ledger integration.
- Route source model zoo expansion.

#### Done criteria

- Exactly one route selected.
- Hard blocks preserved.

## 10. Phase P5: Metric-Use Ledger For `g_eff` In Matter Work

### P5 objective

Prevent `g_eff` from being silently used as a physical Lorentzian metric, proper-time standard, detector calibration object, stress-energy premise, or matter-action premise.

### P5-T01: Metric-use ledger schema

```yaml
plan_task_id: "P5-T01"
task_type: "metric_use_ledger_schema"
role_family: "schema-maintainer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Create a metric-use ledger schema for every g_eff reference in matter-coupling tasks."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "schema_no_physics_delta"
```

#### Required outputs

```text
research_control/design/metric_use_ledger_schema_v1.md
registries/METRIC_USE_LEDGER.csv
```

#### Required CSV columns

```csv
use_id,task_id,artifact_path,object_used,use_category,declared_scope,allowed_use,forbidden_interpretations,no_target_guard_path,audit_status,stress_status,created_at,notes
```

#### Allowed use categories

```yaml
allowed_use_categories:
  - scoped_source_extension_context
  - source_side_relation_input_candidate
  - finite_local_witness_context
  - blocked_physical_metric_use
  - forbidden_import_detected
```

#### Forbidden categories

```yaml
forbidden_metric_uses:
  - physical_lorentzian_metric
  - proper_time_normalization
  - detector_calibration
  - stress_energy_semantics
  - matter_action_premise
  - Einstein_equation_premise
  - benchmark_fit_premise
```

### P5-T02: Populate ledger for existing high-risk matter-route artifacts

```yaml
plan_task_id: "P5-T02"
task_type: "metric_use_ledger_initial_population"
role_family: "research-ops-curator@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Populate metric-use ledger for existing matter-coupling and g_eff-adjacent artifacts."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "ledger_population_no_physics_delta"
```

#### Required scope

Inspect at least:

```text
research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex
research_control/tasks/RT-20260704-021/artifacts/source_side_coupling_law_target_specification_v1.tex
research_control/tasks/<P1-candidate-task>/artifacts/source_side_coupling_law_candidate_v1.tex
research_control/current_frontier.md
registries/DISTANCE_TO_GR_LEDGER.csv
```

#### Done criteria

- Every high-risk `g_eff`, `MetricData(E)`, proper time, metric, or Lorentzian reference in inspected artifacts has a ledger row or explicit no-use justification.
- No ledger row promotes `g_eff` scope.

### P5-T03: Metric-use linter and tests

```yaml
plan_task_id: "P5-T03"
task_type: "metric_use_linter_tests"
role_family: "validator-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Add linter tests that catch forbidden g_eff physical metric use in matter-coupling artifacts."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "validator_update_no_physics_delta"
```

#### Required tests

- `g_eff supplies proper time` fails.
- `g_eff calibrates detectors` fails.
- `g_eff supplies stress-energy semantics` fails.
- `g_eff is used as scoped source-extension context` passes with boundary.
- Bad example: `MetricData(E) adopted` fails unless protected authority exists.

### P5-T04: Integrate metric-use ledger into current frontier and compact frontier

```yaml
plan_task_id: "P5-T04"
task_type: "metric_use_frontier_integration"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Render metric-use ledger summary in current frontier without changing physics status."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "renderer_update_no_physics_delta"
```

#### Done criteria

- Current frontier shows a concise metric-use warning or status card.
- Compact frontier exposes ledger path and count of forbidden/import rows.
- Render checks pass.

## 11. Phase P6: Upstream EqSrc, RetainH, And GenH Route Reassessment

### P6 objective

After the first candidate cycle, decide whether matter-coupling work should continue or return to unresolved upstream equivalence burdens.

### P6-T01: Upstream-burden selector

```yaml
plan_task_id: "P6-T01"
task_type: "upstream_equivalence_burden_selector"
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select whether to attack EqSrc, RetainH, GenH, or continue matter-coupling candidate repair."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "selector_no_promotion"
```

#### Required decision inputs

- Candidate-cycle result from P2.
- Detector route status from P4.
- Metric-use ledger status from P5.
- Current `EqSrc`, `RetainH`, and `GenH` ledger statuses.

#### Allowed selections

```yaml
allowed_selections:
  - EqSrc_theorem_attempt
  - RetainH_primitive_attempt
  - GenH_primitive_attempt
  - matter_coupling_candidate_repair
  - finite_local_model_zoo_expansion
  - scoped_obstruction_freeze_review
```

### P6-T02: Execute selected upstream theorem or primitive attempt

```yaml
plan_task_id: "P6-T02"
task_type: "selected_upstream_equivalence_attempt"
role_family: "ontology-formalizer@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Execute the upstream theorem or primitive attempt selected by P6-T01."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "upstream_attempt_no_downstream_promotion"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/selected_upstream_equivalence_attempt_v1.tex
```

#### Done criteria

- Produces theorem candidate, primitive candidate, finite witness, or scoped obstruction.
- Does not promote matter coupling, Einstein equations, or benchmark status.
- Routes to audit or selector.

### P6-T03: Upstream attempt audit or stress selector

```yaml
plan_task_id: "P6-T03"
task_type: "upstream_attempt_audit_stress_selector"
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select audit, stress, repair, freeze, or return-to-matter route after upstream attempt."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "selector_no_promotion"
```

#### Done criteria

- Exactly one next route selected.
- Upstream result is not overread as downstream GR recovery.

## 12. Phase P7: Proof-Normal-Form Layer

### P7 objective

Create a proof-normal-form representation for definitions, lemmas, theorem candidates, obstructions, and Gate Chair decisions without replacing TeX authority.

### P7-T01: Proof-normal-form schema

```yaml
plan_task_id: "P7-T01"
task_type: "proof_normal_form_schema"
role_family: "schema-maintainer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Create proof-normal-form schema for source-side mathematical artifacts."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "schema_no_physics_delta"
```

#### Required output

```text
research_control/formalization/proof_normal_form_schema_v1.md
registries/PROOF_NORMAL_FORM_REGISTRY.csv
```

#### Required fields

```yaml
proof_normal_form_v1:
  object_id: string
  source_artifact_path: string
  claim_type: definition | lemma | theorem | proposition | obstruction | decision | boundary | nonconclusion
  authority_status: science_draft | scientific_gate | control | support_only
  status: draft_control | scoped_evidence | scoped_adopted | blocked | frozen_negative | not_started
  premises: list[string]
  forbidden_premises: list[string]
  conclusion: string
  scope: string
  allowed_uses: list[string]
  non_conclusions: list[string]
  depends_on: list[string]
  eligible_next_routes: list[string]
  machine_checkable_fragment: true | false
```

### P7-T02: Extract proof-normal-form rows for high-priority artifacts

```yaml
plan_task_id: "P7-T02"
task_type: "proof_normal_form_initial_extraction"
role_family: "ontology-formalizer@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Extract proof-normal-form rows for M_src, g_eff, matter-coupling certificate laws, target specification, and candidate artifacts."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "formalization_support_no_physics_delta"
```

#### Priority artifacts

```text
M_src Gate Chair review
g_eff Gate Chair review
source certificate operation laws v1
source-side coupling-law target specification v1
source-side coupling-law candidate v1, if P1 produced one
finite toy metric-response stress test
Resp_lc source-extension adoption decision
```

#### Done criteria

- Each priority artifact has at least one proof-normal-form row.
- Rows preserve non-conclusions.
- Rows do not replace TeX authority.

### P7-T03: Proof-normal-form validator

```yaml
plan_task_id: "P7-T03"
task_type: "proof_normal_form_validator"
role_family: "validator-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Validate proof-normal-form rows for schema compliance and non-conclusion preservation."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "validator_update_no_physics_delta"
```

#### Validator checks

- Every row has source artifact path.
- Every high-risk row has non-conclusions.
- Forbidden premises do not appear in premises.
- `scientific_gate` decisions do not expand beyond their declared scope.
- Support-only rows do not claim proof authority.

### P7-T04: Proof-normal-form reader surface

```yaml
plan_task_id: "P7-T04"
task_type: "proof_normal_form_reader_surface"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Render proof-normal-form summaries for agent retrieval without changing authority."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "renderer_update_no_physics_delta"
```

#### Required output

```text
wiki/indexes/proof_normal_form_index.md
output/proof_normal_form_index.json
```

## 13. Phase P8: Support-Only Formal Mechanization

### P8 objective

Mechanize low-level formal fragments where feasible, while preserving the boundary that mechanization is support-only and not physics proof authority.

### P8-T01: Formalization target selector

```yaml
plan_task_id: "P8-T01"
task_type: "support_only_formalization_target_selector"
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Select one low-level formal fragment for support-only mechanization."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "formalization_selector_no_physics_delta"
```

#### Candidate targets

```yaml
candidate_formalization_targets:
  - source_certificate_identity_composition_restriction
  - fail_closed_certificate_evaluation
  - finite_toy_tag_removal_obstruction
  - no_target_import_guard_taxonomy
  - claim_graph_non_promotion_constraints
```

#### Done criteria

- Exactly one target selected.
- Tool choice is justified: Python model checker, Lean, Coq, Agda, TLA+, Alloy, or custom finite checker.
- Support-only boundary is explicit.

### P8-T02: Mechanize selected fragment

```yaml
plan_task_id: "P8-T02"
task_type: "support_only_formalization_fragment"
role_family: "formalization-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Implement support-only mechanization for the selected low-level fragment."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "support_only_formalization_no_physics_delta"
```

#### Required outputs

```text
research_control/formalization/<selected-fragment>/README.md
research_control/formalization/<selected-fragment>/<model-or-proof-file>
research_control/formalization/<selected-fragment>/validation_report.json
```

#### Done criteria

- The fragment runs locally.
- Tests or checker report exist.
- The report states `support_only: true` and `proof_authority: false`.
- No scientific Gate Chair claim follows.

### P8-T03: Formalization traceability registry update

```yaml
plan_task_id: "P8-T03"
task_type: "support_only_formalization_traceability_update"
role_family: "research-ops-curator@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Connect formalized fragment to source artifacts and proof-normal-form rows."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "traceability_update_no_physics_delta"
```

#### Required fields

```yaml
traceability_row:
  formalization_id: string
  source_artifact_path: string
  proof_normal_form_row_id: string
  support_only: true
  proof_authority: false
  physics_promotion_authorized: false
```

### P8-T04: Formalization Refuter review

```yaml
plan_task_id: "P8-T04"
task_type: "support_only_formalization_refuter_review"
role_family: "refuter@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Stress support-only formalization for overread as physics proof."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "formalization_refuter_review_no_physics_delta"
```

#### Done criteria

- Review verifies support-only boundary.
- Any overread risk routes to repair.

## 14. Phase P9: Public Proof-State Dashboard

### P9 objective

Create a concise public proof-state dashboard that lets readers see what is positively established, what remains blocked, and what the next lawful route is.

### P9-T01: Dashboard source specification

```yaml
plan_task_id: "P9-T01"
task_type: "public_proof_state_dashboard_source_spec"
role_family: "documentation-curator@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Define source-backed public proof-state dashboard spec using calibrated status cards."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "documentation_spec_no_physics_delta"
```

#### Required output

```text
markdown/html-explainer-specs/proof-state-dashboard-explainer.spec.md
markdown/publication-briefs/proof-state-dashboard.publication-brief.md
```

#### Required dashboard rows

- `Resp_lc`
- `M_src`
- `g_eff`
- `matter_coupling`
- `Einstein equations`
- `benchmark promotion`
- `finite toy metric response`

#### Required dashboard columns

| Column | Purpose |
| --- | --- |
| Object | The burden or object. |
| Positive status | What exists. |
| Exact scope | Where it is valid. |
| Allowed use | What next tasks may use it for. |
| Blocked overread | What it does not establish. |
| Next lawful route | What Continue Research may do next. |

### P9-T02: Dashboard renderer and generated outputs

```yaml
plan_task_id: "P9-T02"
task_type: "public_proof_state_dashboard_renderer"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Render dashboard from tracked control sources and calibrated status cards."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "renderer_update_no_physics_delta"
```

#### Required outputs

```text
github-facing/proof-state-dashboard-explainer.md
html/proof-state-dashboard-explainer.html
wiki/html/<generated-note>.md
wiki/markdown/<generated-note>.md
registries/PUBLICATION_BRIEF_REGISTRY.csv
registries/HTML_EXPLAINER_REGISTRY.csv
registries/MARKDOWN_SOURCE_REGISTRY.csv
```

#### Done criteria

- Dashboard derives from registered sources.
- Dashboard says GR is not derived.
- Dashboard uses calibrated positive-first status cards.
- Generated surfaces are registered.

### P9-T03: README and front-door integration

```yaml
plan_task_id: "P9-T03"
task_type: "proof_state_dashboard_front_door_integration"
role_family: "documentation-curator@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Link proof-state dashboard from front-door docs without changing claim status."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "documentation_update_no_physics_delta"
```

#### Done criteria

- README links dashboard as reader-facing, non-authoritative derivative.
- README preserves public status boundary.
- Documentation-impact validation passes.

### P9-T04: Public dashboard red-team review

```yaml
plan_task_id: "P9-T04"
task_type: "proof_state_dashboard_red_team_review"
role_family: "external-red-team-reviewer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Review proof-state dashboard for overclaim, underclaim, and reader comprehension."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "red_team_review_no_physics_delta"
```

#### Done criteria

- Red-team review returns pass or repair route.
- No physics claim changes.

## 15. Phase P10: Generated Task Index

### P10 objective

Make `research_control/tasks` easier to navigate for humans and agents by generating an authoritative-reader index from tracked task records.

### P10-T01: Task-index schema

```yaml
plan_task_id: "P10-T01"
task_type: "research_control_task_index_schema"
role_family: "schema-maintainer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Define generated task-index schema from tracked task records."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "schema_no_physics_delta"
```

#### Required output

```text
research_control/design/task_index_schema_v1.md
```

#### Required columns

```csv
task_id,parent_task_id,created_at,closed_at,task_type,status,target_derivation_milestone,milestone_burden,role_family,physics_delta,ledger_rows_changed,artifact_count,next_recommended_action,validation_status,completion_path
```

### P10-T02: Task-index generator

```yaml
plan_task_id: "P10-T02"
task_type: "research_control_task_index_generator"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Generate TASK_INDEX.csv and TASK_INDEX.md from tracked task folders."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "tooling_update_no_physics_delta"
```

#### Required outputs

```text
scripts/research_control/render_task_index.py
research_control/tasks/TASK_INDEX.csv
research_control/tasks/TASK_INDEX.md
wiki/indexes/research_control_task_index.md
```

#### Done criteria

- Index derives only from tracked task records.
- Index is generated, not hand-authored.
- Missing or malformed task records are reported.

### P10-T03: Task-index validator

```yaml
plan_task_id: "P10-T03"
task_type: "research_control_task_index_validator"
role_family: "validator-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Validate generated task index against tracked tasks and completions."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "validator_update_no_physics_delta"
```

#### Required output

```text
scripts/research_control/validate_task_index.py
tests/test_task_index_renderer.py
```

### P10-T04: Task-index integration into memory and folder docs

```yaml
plan_task_id: "P10-T04"
task_type: "research_control_task_index_memory_integration"
role_family: "research-ops-curator@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Integrate generated task index into memory and folder map surfaces."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "memory_integration_no_physics_delta"
```

#### Done criteria

- Bootstrap includes task index outputs.
- `research_control/tasks/README.md` points to the generated index.
- Generated output boundary is explicit.

## 16. Phase P11: CI And Reproducibility

### P11 objective

Make validation reproducible outside the local agent by adding CI checks, environment metadata, and validation artifact publication.

### P11-T01: GitHub Actions validation workflow

```yaml
plan_task_id: "P11-T01"
task_type: "github_actions_validation_workflow"
role_family: "software-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Add CI workflow for project-control validation without changing physics claims."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "ci_update_no_physics_delta"
```

#### Required output

```text
.github/workflows/project-control-validation.yml
```

#### Required jobs

```yaml
jobs:
  validate_project_control:
    commands:
      - python -m pip install -r requirements.txt
      - make validate-project-control
  validate_memory_read_only:
    commands:
      - python -m pip install -r requirements.txt
      - .venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
```

#### Notes

The local agent must adapt commands to CI environment paths. `.venv/bin/python` may need a CI wrapper or Makefile variable override.

### P11-T02: Python environment and reproducibility documentation

```yaml
plan_task_id: "P11-T02"
task_type: "python_environment_reproducibility_docs"
role_family: "software-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Document Python version, environment setup, and validation commands."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "docs_no_physics_delta"
```

#### Required outputs

```text
CONTRIBUTING.md
requirements-dev.txt or pyproject.toml
```

#### Required content

- Supported Python version.
- Virtual environment setup.
- Validation commands.
- Generated-output policy.
- How to interpret validator success as operational only.

### P11-T03: Full validation artifact collector

```yaml
plan_task_id: "P11-T03"
task_type: "validation_artifact_collector"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Collect validation reports into output artifacts for CI and local review."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "tooling_update_no_physics_delta"
```

#### Required output

```text
scripts/research_control/collect_validation_artifacts.py
output/validation_summary.json
output/validation_summary.md
```

### P11-T04: CI boundary red-team review

```yaml
plan_task_id: "P11-T04"
task_type: "ci_validation_boundary_review"
role_family: "external-red-team-reviewer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Review CI and validator language for validator-as-proof overread."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "red_team_review_no_physics_delta"
```

#### Done criteria

- CI docs say validation is not physics proof.
- Validation artifacts do not claim proof authority.

## 17. Phase P12: AI Research-Agent Methodology Metrics

### P12 objective

Evaluate the research-agent system as a scientific instrument: not by whether it proves GR, but by whether it improves controlled theoretical research behavior.

### P12-T01: Metrics taxonomy extension

```yaml
plan_task_id: "P12-T01"
task_type: "ai_research_agent_metrics_taxonomy"
role_family: "research-methodologist@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Define AI research-agent methodology metrics for overclaim, obstruction precision, route orbit, and candidate survival."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "methodology_metrics_no_physics_delta"
```

#### Required metrics

```yaml
metrics:
  overclaim_catch_rate: "fraction of seeded or real overclaim surfaces caught"
  underclaim_warning_rate: "fraction of high-risk summaries missing positive status"
  obstruction_precision: "fraction of obstructions scoped with non-global boundary"
  route_orbit_rate: "frequency of repeated-burden cycles without new payload"
  candidate_to_audit_conversion: "candidate constructor outputs eligible for audit"
  audit_to_stress_survival: "audited candidates that reach stress"
  stress_survival_rate: "stressed candidates that survive as draft/control"
  human_gate_load: "number of protected authority requests per phase"
  proof_to_process_ratio: "mathematical payload artifacts compared with process receipts"
```

### P12-T02: Extend physics-progress metrics report

```yaml
plan_task_id: "P12-T02"
task_type: "ai_research_agent_metrics_report_extension"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Extend progress metrics report with AI methodology metrics and calibrated acceptance warnings."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "metrics_tool_update_no_physics_delta"
```

#### Required modifications

```text
scripts/research_control/report_physics_progress_metrics.py
output/physics_progress_metrics.json
output/physics_progress_metrics.md
```

#### Done criteria

- Metrics report separates physics metrics from AI-system diagnostics.
- No metric is interpreted as proof of physics progress.

### P12-T03: AI-methodology evaluation memo

```yaml
plan_task_id: "P12-T03"
task_type: "ai_methodology_evaluation_memo"
role_family: "research-methodologist@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Write methodology memo evaluating the research-agent system without physics promotion."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "methodology_memo_no_physics_delta"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/ai_research_agent_methodology_evaluation_v1.md
```

#### Required sections

1. Research-agent purpose
2. Metrics definitions
3. Current measured values
4. Strengths
5. Failure modes
6. Recommendations
7. Physics claim boundary

### P12-T04: Methodology dashboard integration

```yaml
plan_task_id: "P12-T04"
task_type: "ai_methodology_dashboard_integration"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Render methodology metrics dashboard as support-only AI-system diagnostic."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "dashboard_update_no_physics_delta"
```

#### Done criteria

- Dashboard labels metrics as AI-system diagnostics.
- Dashboard does not rank physics truth by workflow activity.

## 18. Phase P13: V17 Integration, Final Validation, And Next Route Selection

### P13 objective

Integrate v17 outputs, run final validation, summarize physics and project-system effects, and select exactly one next route.

### P13-T01: V17 integration report

```yaml
plan_task_id: "P13-T01"
task_type: "v17_integration_report"
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Integrate v17 phase outputs into one control report without physics overclaim."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "v17_integration_no_promotion"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/v17_integration_report.md
```

#### Required sections

- Implemented tasks
- Deferred tasks
- Candidate construction status
- Audit and stress status
- Accepted-language calibration status
- Detector-semantics status
- Metric-use ledger status
- Upstream-burden status
- Proof-normal-form status
- Formalization status
- Dashboard status
- Task-index status
- CI status
- AI-methodology metrics status
- Distance-to-GR effect
- Next route candidates

### P13-T02: V17 final validation packet

```yaml
plan_task_id: "P13-T02"
task_type: "v17_final_validation_packet"
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Run final v17 validation layers and record exact pending reasons if any."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "v17_final_validation_no_promotion"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/v17_final_validation_report.json
```

#### Required validation layers

- memory preflight
- memory bootstrap
- research-control validation
- diff validation
- claim-language linter
- accepted calibration advisory report
- documentation-impact validation
- registry consistency
- current-frontier render check
- compact-frontier render check
- dependency-graph check
- claim-graph validation
- task-index validation
- metric-use ledger validation
- proof-normal-form validation
- support-only formalization validation
- unit tests
- CI workflow syntax check, where available

### P13-T03: Current frontier and ledger synchronization

```yaml
plan_task_id: "P13-T03"
task_type: "v17_current_frontier_synchronization"
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Synchronize current frontier, compact frontier, graphs, and ledgers after v17 final validation."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "frontier_sync_no_promotion"
```

#### Done criteria

- `current_frontier.md` is synchronized.
- Compact frontier is synchronized.
- Claim graph and dependency graph are fresh.
- Distance-to-GR ledger remains accurate.
- Any ledger status change is justified by protected authority. Otherwise no ledger status change.

### P13-T04: V17 ordinary continuation handoff

```yaml
plan_task_id: "P13-T04"
task_type: "v17_ordinary_continuation_handoff"
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Complete v17 and select exactly one ordinary continuation route from validated v17 outputs."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "v17_completed_ordinary_continuation_selected"
```

#### Allowed next route families

```yaml
allowed_next_routes:
  - repair_coupling_law_candidate
  - smuggling_audit_next_candidate
  - refuter_stress_next_candidate
  - detector_semantics_replacement_continuation
  - metric_use_ledger_repair
  - upstream_EqSrc_RetainH_GenH_theorem_attempt
  - proof_normal_form_expansion
  - support_only_formalization_expansion
  - project_system_repair_from_validation_findings
  - scoped_obstruction_freeze_review
```

#### Selection rule

Pick exactly one next route. The route must follow the strongest current blocker:

1. A hard validation failure routes to project-system repair.
2. A candidate construction failure routes to repair or obstruction review.
3. A smuggling audit failure routes to repair or freeze review.
4. A Refuter stress failure routes to repair, obstruction, or freeze review.
5. A detector-semantics obstruction routes to detector continuation or ontology-law selector.
6. No hard failures and an audit/stress-surviving candidate routes to the next bounded non-promotional selector, not adoption.
7. No physics candidate progress but completed project-system improvements routes back to the current physics frontier.

#### Forbidden next routes

- Direct coupling-law adoption.
- Direct matter-coupling derivation.
- Einstein-equation derivation.
- Benchmark promotion.
- Completed derivation.

## 19. Completion Receipts Required Across V17

Every task completion must include the following minimum receipt fields:

```yaml
completion_required_fields:
  completion_id: string
  job_id: string
  task_id: string
  source_role_id: string
  completed_at: string
  status: completed | blocked | failed | superseded
  implementation_plan_receipt:
    plan_id: "recommendations_implementation_plan_continue_task-v17"
    plan_task_id: string
    plan_phase_id: string
    implemented_task_scope: string
  output_paths: list[string]
  command_results: list[string]
  physics_progress_status:
    status: string
    physics_promotion_authorized: false
  distance_to_gr_delta:
    effect: string
    changed: false
  mathematical_payload_manifest: list[object]
  validation_layers: object
  claim_boundary:
    proof_authority: false
    source_law_adoption_authorized: false
    matter_coupling_derivation_authorized: false
    benchmark_promotion_authorized: false
    completed_derivation_authorized: false
  forbidden_conclusions: list[string]
  project_improvement_signals: list[string]
  next_recommended_action: string
```

## 20. V17 Success Criteria

V17 is successful when the project has accomplished the following without overclaiming:

1. The selected v16 next route has been executed: one concrete source-side coupling-law candidate has been constructed, or one precise obstruction has been recorded.
2. Any candidate has been treated as audit-eligible only.
3. Smuggling audit and Refuter stress have been routed or completed for the candidate.
4. The `accepted` dilemma has been fixed with calibrated positive-first status cards.
5. High-risk reader-facing outputs no longer rely on bare `accepted`.
6. Local AI agents have linter and renderer support for avoiding both overclaim and fear-based underclaim.
7. Detector semantics has a dedicated replacement or obstruction route.
8. `g_eff` usage in matter work is tracked through a metric-use ledger.
9. Upstream `EqSrc`, `RetainH`, and `GenH` burdens have a selector decision after the first candidate cycle.
10. Proof-normal-form support exists for priority artifacts.
11. At least one low-level formal fragment has a support-only mechanization plan or implementation.
12. A public proof-state dashboard exists or is explicitly routed.
13. A generated task index exists or is explicitly routed.
14. CI and reproducibility tasks are either implemented or routed with exact blockers.
15. AI research-agent methodology metrics are defined and separated from physics proof claims.
16. Final validation passes or records exact pending layers.
17. The final handoff selects exactly one next ordinary route.

## 21. V17 Non-Success Criteria

V17 must not be considered successful if any of these occur:

1. A task claims matter coupling is derived from candidate construction alone.
2. A task adopts a coupling law without protected authority.
3. A task treats detector-placeholder status as detector semantics.
4. A task uses `g_eff` as physical Lorentzian metric, proper time, or detector calibration without a separately authorized derivation.
5. A task treats a validator pass, registry row, handoff, role identity, commit state, or generated artifact as scientific proof.
6. A public-facing surface says or implies GR has been derived.
7. The `accepted` calibration removes needed blocked-overread guards.
8. The `accepted` calibration keeps positive status hidden behind caveat walls.
9. Multiple phase tasks are bundled into one uncontrolled transaction.
10. Final validation is skipped.

## 22. Recommended First Three Continue Research Invocations

To begin v17 safely, run these in order:

```text
1. P0-T01: Register the v17 implementation plan.
2. P0-T02: Build the v17 execution backlog.
3. P0-T03: Run active-state and source-basis preflight.
```

After those pass, run:

```text
4. P1-T01: Candidate-constructor packet setup.
5. P1-T02: Construct the concrete source-side coupling-law candidate or obstruction.
```

Do not start the accepted-language system tasks before the plan is registered and the active-state preflight has passed, unless a Director Decision Record explicitly routes a project-system repair first.

## 23. Final Boundary Statement

This v17 plan is ambitious, but its ambition is procedural and constructive, not promotional. It tells the local agents how to build the next candidate, how to audit and stress it, how to fix the accepted-language dilemma, how to strengthen tooling, and how to expose the project state to humans without distortion.

It does not establish matter coupling, Einstein equations, benchmark promotion, or a completed derivation of GR from the AEther-flow ontology. Those remain future burdens behind the project’s normal construction, audit, stress, selector, and protected-gate sequence.
