<!-- authority: control -->

# Recommendations Implementation Plan Continue Task v18

```yaml
plan_id: "recommendations_implementation_plan_continue_task-v18"
plan_version: "v18"
created_at: "2026-07-07"
status: "draft_control_implementation_plan"
intended_executor: "local AI agents through Continue Research functionality"
execution_mode: "one bounded Continue Research AgentJob per phase task"
plan_filename: "recommendations_implementation_plan_continue_task-v18.md"
recommended_repo_path: "implementations_plans/recommendations_implementation_plan_continue_task-v18.md"
basis: "Integrates all recommendations from the prior project review section 7, Recommendations."
current_research_frontier_basis:
  latest_research_task_id: "RT-20260707-002"
  latest_research_handoff_id: "handoff-0672"
  selected_next_route: "upstream_EqSrc_RetainH_GenH_theorem_attempt"
  selected_next_action: "Run one bounded upstream EqSrc RetainH GenH theorem-attempt continuation packet from the validated v17 outputs."
known_project_system_sidecar_basis:
  latest_project_system_task_id: "RT-20260707-003"
  sidecar_status: "ci_registry_path_visibility_repair_completed_no_physics_delta"
physics_promotion_authorized: false
proof_authority: false
benchmark_promotion_authorized: false
completed_derivation_authorized: false
external_outreach_authorized_by_default: false
```

## 0. Purpose

This implementation plan converts the full recommendation set from the prior project review into a sequential, task-addressable v18 program for local AI agents.

The plan is designed to be consumed by the repository's Continue Research functionality. Every phase task below is intended to become exactly one bounded Continue Research AgentJob. No local agent may batch multiple phase tasks into one research-control transaction unless a later Director Decision Record explicitly supersedes this plan.

The plan integrates all ten recommendations from the review:

1. Run the upstream `EqSrc RetainH GenH` theorem-or-countermodel packet next.
2. Formalize the source-equivalence layer as a typed mathematical object.
3. Introduce minimal countermodel obligations for theorem attempts.
4. Promote source detector/readout semantics to a named frontier burden.
5. Build a non-tag-fragile finite toy response model v2.
6. Expand support formalization into proof-adjacent but authority-limited tooling.
7. Enforce a physics-payload ratio to reduce process orbit.
8. Clarify active-state semantics after project-system sidecars.
9. Reduce public cognitive load with positive-first status cards that include the next burden.
10. Prepare one focused external-review packet rather than asking reviewers to inspect the whole repository.

This plan is not a physics proof, not source-law adoption, not canonical ontology adoption, not `MetricData(E)` adoption, not `g_eff` scope expansion, not coupling-law adoption, not matter-coupling derivation, not Einstein-equation derivation, not benchmark promotion, not Gate Chair closure, not external outreach authorization, and not completed derivation.

## 1. Source basis for local agents

Before implementing any v18 task, the local agent must inspect the tracked sources below through direct file reads and the project memory system. Generated wiki notes, `.local/` cache surfaces, generated dashboards, generated indexes, and rendered summaries may assist retrieval only. They must never override the tracked source files.

### 1.1 Active-state and handoff sources

```text
AGENTS.md
research_control/AGENTS.md
.codex/skills/continue-research/SKILL.md
research_control/program_state.yaml
research_control/current_frontier.md
research_control/handoffs/handoff-0672.yaml
research_control/handoffs/handoff-0672.md
research_control/tasks/RT-20260707-002/00_TASK.yaml
research_control/tasks/RT-20260707-002/DDR-20260707-002.md
research_control/tasks/RT-20260707-002/jobs/AJ-RT-20260707-002-001.yaml
research_control/tasks/RT-20260707-002/jobs/completions/AJC-AJ-RT-20260707-002-001.yaml
research_control/tasks/RT-20260707-002/artifacts/v17_ordinary_continuation_handoff_report.json
research_control/tasks/RT-20260707-003/00_TASK.yaml
research_control/tasks/RT-20260707-003/DDR-20260707-003.md
research_control/tasks/TASK_INDEX.csv
research_control/tasks/TASK_INDEX.md
```

### 1.2 Physics-control and derivation-burden sources

```text
research_control/design/gr_derivation_burden_map.md
registries/DISTANCE_TO_GR_LEDGER.csv
registries/METRIC_USE_LEDGER.csv
research_control/design/matter_coupling_dependency_dag_v1.md
research_control/design/matter_coupling_dependency_dag_schema_v1.md
research_control/design/matter_coupling_derivation_moratorium.md
research_control/design/matter_coupling_pre_adoption_checklist.md
research_control/design/no_target_import_guard_map.md
research_control/design/source_certificate_algebra_checklist.md
research_control/design/accepted_status_calibration_policy_v1.md
research_control/design/accepted_status_calibration_schema_v1.md
research_control/design/accepted_status_calibration_v1.yaml
research_control/design/distance_to_gr_status_aliases.yaml
research_control/design/metric_use_ledger_schema_v1.md
research_control/design/proof_normal_form_schema_v1.md
registries/PROOF_NORMAL_FORM_REGISTRY.csv
```

### 1.3 Priority science-draft artifacts

```text
research_control/tasks/RT-20260706-011/artifacts/selected_upstream_equivalence_attempt_v1.tex
research_control/tasks/RT-20260706-012/artifacts/upstream_attempt_audit_stress_selector_v1.md
research_control/tasks/RT-20260705-047/artifacts/source_side_coupling_law_candidate_v1.tex
research_control/tasks/RT-20260706-002/artifacts/detector_semantics_replacement_candidate_v1.tex
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

### 1.4 Agent-system, validator, and rendering sources

```text
Makefile
scripts/research_control/continue_research.py
scripts/research_control/continue_research_memory_preflight.py
scripts/research_control/validate_research_control.py
scripts/research_control/run_full_research_control_validation.py
scripts/project_control/validate_claim_language.py
scripts/project_control/validate_documentation_impact.py
scripts/research_control/render_current_frontier.py
scripts/research_control/render_compact_current_frontier_v16.py
scripts/research_control/render_task_index.py
scripts/research_control/render_dependency_graph.py
scripts/research_control/generate_claim_graph_v1.py
scripts/research_control/validate_claim_graph_v1.py
scripts/research_control/report_physics_progress_metrics.py
scripts/research_control/render_ai_methodology_metrics_dashboard.py
tests/
```

## 2. Global implementation rules

### 2.1 Continue Research invocation rule

Every phase task in this plan must be implemented through Continue Research.

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
  no_batching_without_superseding_DDR: true
```

The local agent must use the active state pointer and latest research handoff before choosing the next task. A project-system sidecar may repair validation or documentation infrastructure, but it must not silently supersede the latest research handoff unless a Director Decision Record explicitly says so.

### 2.2 Claim-boundary rule

Every task must preserve these hard blocks unless a later protected authority explicitly supersedes them:

```yaml
hard_blocks:
  - canonical ontology edit
  - source-law adoption
  - general EqSrc discharge
  - RetainH adoption
  - GenH adoption
  - RR_ETransportCompletenessOrInvarianceLaw_v1 adoption
  - unrestricted RR_E theorem
  - MetricData(E) adoption
  - g_eff adoption or scope expansion
  - physical Lorentzian metric authority
  - proper-time normalization
  - empirical detector protocol import
  - matter-semantics adoption
  - detector-semantics adoption
  - source detector/readout semantics adoption unless explicitly human-gated
  - coupling-law adoption
  - matter-coupling derivation or adoption
  - stress-energy semantics
  - stress-energy tensor
  - matter action
  - Einstein-equation derivation
  - benchmark promotion
  - Gate Chair benchmark closure
  - proof authority from validators or generated artifacts
  - completed derivation
  - future source-extension impossibility
  - program-wide no-go conclusion
  - external outreach without human authorization
```

Every task completion must include a `forbidden_conclusion_summary` or equivalent explicit field preserving these blocks.

### 2.3 Distance-to-GR rule

Physics-bearing tasks must state:

```yaml
target_derivation_milestone: "<one milestone from the burden map>"
milestone_burden: "<exact task-local burden>"
distance_to_gr_delta:
  effect: "no_distance_delta | scoped_candidate_constructed_no_adoption | scoped_obstruction_recorded_no_promotion | theorem_candidate_no_promotion | countermodel_recorded_no_promotion | ledger_delta_requested_after_gate"
  changed: false
  ledger_row_updated: false
```

A task may not set `changed: true` unless it is an authorized Gate Chair or protected ledger-update packet whose scope explicitly permits that update.

### 2.4 Mathematical payload rule

Every physics-bearing task must include at least one new mathematical payload. Acceptable payload families include:

```yaml
allowed_payload_families:
  - typed source-equivalence definition
  - family-level EqSrc theorem candidate
  - finite or locally finite source witness
  - minimal countermodel
  - RetainH primitive requirement theorem
  - GenH primitive requirement theorem
  - source detector/readout candidate
  - source detector/readout obstruction
  - non-tag finite toy model
  - invariance or tag-removal stress result
  - smuggling audit finding
  - Refuter stress counterexample
  - proof-normal-form extraction
  - formal checker specification
  - source-extension classification
  - dependency-map update with proof-relevant consequence
```

Project-system tasks may have `new_mathematical_payload: []`, but they must state:

```yaml
project_system_change_only: true
physics_promotion_authorized: false
scientific_claims_changed: false
```

### 2.5 Recommendation coverage rule

Every completion must include:

```yaml
recommendation_coverage:
  source_plan_id: "recommendations_implementation_plan_continue_task-v18"
  source_recommendation_ids:
    - "V18-R<nn>"
  implements_plan_task_id: "P<phase>-T<task>"
  implementation_status: "completed | deferred | blocked | superseded"
  coverage_effect: "direct | support | validation | review | handoff"
```

The final v18 integration packet must prove coverage for all recommendations `V18-R01` through `V18-R10`.

### 2.6 Validation rule

Every task must run the narrowest appropriate validations and then the full research-control validation before closure.

Minimum validation sequence:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/project_control/validate_claim_language.py --changed --json
.venv/bin/python scripts/project_control/validate_documentation_impact.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/research_control/run_full_research_control_validation.py --json
git diff --check
```

If a task changes scripts or tests, also run:

```zsh
.venv/bin/python -m unittest discover -s tests
```

If a task changes current-frontier, compact-frontier, dependency-graph, claim-graph, task-index, AI-methodology dashboard, or generated reader surfaces, also run the relevant renderer checks:

```zsh
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_compact_current_frontier_v16.py --check
.venv/bin/python scripts/research_control/render_task_index.py --check
.venv/bin/python scripts/research_control/render_dependency_graph.py --check
.venv/bin/python scripts/research_control/generate_claim_graph_v1.py --check
.venv/bin/python scripts/research_control/validate_claim_graph_v1.py --json
.venv/bin/python scripts/research_control/render_ai_methodology_metrics_dashboard.py --check
```

### 2.7 Project-system boundary rule

Project-system tasks may edit control Markdown, schemas, scripts, tests, renderers, generated outputs, and registries only inside their declared scope. They must not edit canonical science TeX unless the task is explicitly a science-draft task and the claim boundary permits it.

### 2.8 External-review rule

V18 may prepare an external-review packet. It must not send the packet, name specific reviewers, create outreach messages, or imply external endorsement unless a later human-gated task explicitly authorizes outreach.

```yaml
external_review_default:
  packet_preparation_allowed: true
  internal_red_team_allowed: true
  external_outreach_allowed: false
  external_outreach_requires_human_gate: true
  external_response_as_authority: false
```

## 3. Recommendation integration matrix

| Recommendation ID | Recommendation | Main phases | Primary route type | Physics delta expected |
| --- | --- | --- | --- | --- |
| `V18-R01` | Run upstream `EqSrc RetainH GenH` theorem-or-countermodel next | P2, P3 | physics theorem/countermodel | theorem or obstruction only, no promotion |
| `V18-R02` | Formalize source-equivalence as a typed mathematical object | P2 | science-draft definition plus audit/stress | definition/theorem support only |
| `V18-R03` | Introduce minimal countermodel obligations | P3, P4 | theorem-packet standard plus validators | obstruction/countermodel support only |
| `V18-R04` | Promote source detector/readout semantics to a named frontier burden | P5 | burden design, candidate/obstruction route | no adoption without gate |
| `V18-R05` | Build non-tag-fragile finite toy response model v2 | P6 | finite model construction and stress | toy model only, no `g_eff` or GR |
| `V18-R06` | Expand support formalization as authority-limited tooling | P7 | support-only executable specs | support only, no proof authority |
| `V18-R07` | Enforce physics-payload ratio | P8 | process-control validator and metrics | no physics delta |
| `V18-R08` | Clarify active-state semantics after sidecars | P1 | active-state schema/rendering | no physics delta |
| `V18-R09` | Reduce public cognitive load with status cards and next burden | P9 | documentation/rendering/linter | no physics delta |
| `V18-R10` | Prepare one focused external-review packet | P10 | review packet preparation | no outreach by default |

## 4. Phase order

V18 must be executed in this order unless a later Director Decision Record supersedes it:

```yaml
phase_order:
  - P0: "V18 intake, registration, and active-state preflight"
  - P1: "Active-state bifurcation after project-system sidecars"
  - P2: "Typed source-equivalence object formalization"
  - P3: "EqSrc family-closure theorem-or-countermodel packet"
  - P4: "Minimal countermodel obligation system"
  - P5: "Source detector/readout semantics frontier burden"
  - P6: "Non-tag-fragile finite toy response model v2"
  - P7: "Authority-limited support formalization expansion"
  - P8: "Physics-payload ratio and route-orbit control"
  - P9: "Public cognitive-load reduction and status-card v2"
  - P10: "Focused external-review packet preparation"
  - P11: "V18 integration, final validation, frontier sync, and ordinary handoff"
```

---

## 5. Phase P0: V18 intake, registration, and active-state preflight

### P0 objective

Register this v18 implementation plan as a tracked control source, materialize a task-addressable backlog, and verify that the live research continuation still starts from the v17 ordinary continuation handoff.

### P0-T01: Register the v18 implementation plan

```yaml
plan_task_id: "P0-T01"
task_type: "v18_plan_registration"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "none"
milestone_burden: "Register v18 implementation plan as control source with no physics delta."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "project_control_plan_registration_no_physics_delta"
```

#### Objective

Add `implementations_plans/recommendations_implementation_plan_continue_task-v18.md` to the repository and register it as a tracked control Markdown source.

#### Required inputs

```text
implementations_plans/recommendations_implementation_plan_continue_task-v18.md
registries/MARKDOWN_SOURCE_REGISTRY.csv
AGENTS.md
research_control/AGENTS.md
research_control/program_state.yaml
research_control/handoffs/handoff-0672.yaml
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

- The v18 plan is tracked under `implementations_plans/`.
- The plan is registered as a control Markdown source.
- The completion records all ten recommendation IDs.
- Memory bootstrap and research-control validation pass.
- `distance_to_gr_delta.changed` is `false`.
- The next route is `P0-T02`.

#### Forbidden conclusions

- The v18 plan does not prove any physics result.
- The v18 plan does not supersede `handoff-0672` except through tracked v18 sequencing.
- Registration does not authorize source-law adoption, matter coupling, Einstein equations, benchmark promotion, or completed derivation.

### P0-T02: Build the v18 execution backlog

```yaml
plan_task_id: "P0-T02"
task_type: "v18_execution_backlog_materialization"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "project-control-maintainer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Create a task-addressable v18 backlog from the implementation plan."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "project_control_backlog_no_physics_delta"
```

#### Objective

Create a machine-readable v18 backlog mapping each phase task to recommendation IDs, route type, role family, dependencies, outputs, validators, and handoff behavior.

#### Required outputs

```text
research_control/design/v18_recommendation_backlog.yaml
research_control/design/v18_recommendation_backlog_schema.md
```

#### Required backlog fields

```yaml
backlog_item:
  plan_task_id: string
  phase_id: string
  title: string
  recommendation_ids: list[string]
  depends_on: list[string]
  role_family: string
  task_type: string
  target_derivation_milestone: string
  milestone_burden: string
  expected_outputs: list[string]
  required_validators: list[string]
  physics_delta_allowed: boolean
  promotion_allowed: boolean
  human_gate_required: boolean
  next_route_on_success: string
  next_route_on_failure: string
```

#### Done criteria

- Every task in this plan appears exactly once in the backlog.
- Dependencies are acyclic.
- Every recommendation ID appears in at least one direct implementation task and one final coverage audit.
- Project-system tasks include `project_system_boundary_authorized_by_plan: true`.
- The next route is `P0-T03`.

### P0-T03: Active-state and source-basis preflight

```yaml
plan_task_id: "P0-T03"
task_type: "v18_active_state_preflight"
recommendation_ids: ["V18-R01", "V18-R08"]
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Verify the latest research handoff and sidecar state before v18 physics or project-system tasks."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "preflight_no_physics_delta"
```

#### Objective

Confirm that the lawful research continuation still points to upstream `EqSrc RetainH GenH` theorem-attempt continuation, and classify any later project-system task as a sidecar unless authority says otherwise.

#### Required checks

- `program_state.yaml` points to the latest active task and handoff.
- `handoff-0672` remains the latest research-continuation handoff unless superseded.
- `RT-20260707-003`, if present, is classified as project-system repair with no physics delta.
- `current_frontier.md`, compact frontier outputs, task index, and dependency graph are synchronized.
- The Distance-to-GR ledger still blocks general `EqSrc` discharge, `RetainH`, `GenH`, matter-coupling derivation, Einstein equations, and benchmark promotion.
- The next physics route remains upstream theorem/countermodel work unless a validator failure forces a deterministic repair.

#### Required output

```text
research_control/tasks/<task-id>/artifacts/v18_active_state_preflight_report.json
```

#### Done criteria

- Preflight report exists.
- Drift is absent or routed to a deterministic repair task.
- The report distinguishes latest research authority from latest project-system sidecar.
- The next route is `P1-T01`.

### P0-T04: V18 recommendation coverage seed report

```yaml
plan_task_id: "P0-T04"
task_type: "v18_recommendation_coverage_seed"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "process-integrity-auditor@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Create a baseline recommendation coverage matrix before executing v18."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "coverage_seed_no_physics_delta"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/v18_recommendation_coverage_seed.yaml
```

#### Done criteria

- Every recommendation has planned implementation tasks.
- Every planned implementation task has at least one validator layer.
- Any protected-action recommendation, especially external outreach or protected ledger updates, is marked human-gated or setup-only.
- The next route is `P1-T01`.

---

## 6. Phase P1: Active-state bifurcation after project-system sidecars

### P1 objective

Implement recommendation `V18-R08`: clarify active-state semantics after project-system sidecars so local agents can distinguish the latest research handoff from later project-system repair tasks.

### P1-T01: Active-state bifurcation design note

```yaml
plan_task_id: "P1-T01"
task_type: "active_state_bifurcation_design_note"
recommendation_ids: ["V18-R08"]
role_family: "project-control-maintainer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Define how research handoffs and project-system sidecars coexist in active-state surfaces."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "active_state_design_no_physics_delta"
```

#### Objective

Create a design note that distinguishes:

```yaml
active_state_roles:
  latest_research_task_id: "task that selected or executed the current scientific route"
  latest_research_handoff_id: "handoff governing ordinary research continuation"
  latest_project_system_task_id: "latest validation or tooling repair sidecar"
  latest_project_system_status: "sidecar status that does not supersede research"
  active_task_id: "compact pointer used by existing scripts"
  latest_handoff_id: "compact pointer used by existing scripts"
```

#### Required output

```text
research_control/design/active_state_bifurcation_policy_v1.md
```

#### Required sections

1. Problem statement.
2. Definitions.
3. Authority precedence.
4. How to render project-system sidecars.
5. How Continue Research chooses the next physics route.
6. Validator requirements.
7. Forbidden overreads.
8. Examples using `RT-20260707-002` and `RT-20260707-003`.

#### Done criteria

- The policy says sidecars can repair validation infrastructure without becoming scientific next-route authority.
- The policy preserves `program_state.yaml` as compact live pointer while allowing richer rendered fields.
- The policy does not change Distance-to-GR status.
- The next route is `P1-T02`.

### P1-T02: Active-state schema and renderer update

```yaml
plan_task_id: "P1-T02"
task_type: "active_state_bifurcation_schema_renderer"
recommendation_ids: ["V18-R08"]
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Expose latest research handoff and latest project-system sidecar in generated frontier surfaces."
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

Render a compact table:

```yaml
active_state_bifurcation:
  latest_research_task_id: string
  latest_research_handoff_id: string
  latest_research_next_action: string
  latest_project_system_task_id: string | none
  latest_project_system_status: string | none
  sidecar_supersedes_research_handoff: false
  next_research_route_source: "latest_research_handoff"
```

#### Done criteria

- Frontier surfaces show the latest research handoff separately from latest sidecar.
- Existing compact frontier checks pass.
- No generated surface is treated as scientific proof.
- The next route is `P1-T03`.

### P1-T03: Active-state sidecar validator and tests

```yaml
plan_task_id: "P1-T03"
task_type: "active_state_sidecar_validator"
recommendation_ids: ["V18-R08"]
role_family: "validator-engineer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Add validation that prevents project-system sidecars from silently overriding research handoffs."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "validator_update_no_physics_delta"
```

#### Required modifications

```text
scripts/research_control/validate_research_control.py
scripts/research_control/run_full_research_control_validation.py
tests/test_validate_research_control.py
tests/fixtures/research_control/active_state_sidecar_valid/
tests/fixtures/research_control/active_state_sidecar_invalid/
```

#### Tests

Add tests verifying:

- A later project-system sidecar does not supersede latest research handoff unless explicitly authorized.
- A sidecar that claims physics promotion without ledger authority fails.
- A research task that selects a new ordinary route may supersede the prior research handoff.
- Rendered bifurcation fields remain synchronized with tracked tasks and handoffs.

#### Done criteria

- Focused tests pass.
- Full validation passes.
- The next route is `P1-T04`.

### P1-T04: Active-state bifurcation red-team review

```yaml
plan_task_id: "P1-T04"
task_type: "active_state_bifurcation_red_team_review"
recommendation_ids: ["V18-R08"]
role_family: "external-red-team-reviewer@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Stress the active-state bifurcation for route confusion and authority laundering."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "red_team_review_no_physics_delta"
```

#### Review questions

1. Can a local agent identify the latest research handoff?
2. Can a local agent identify the latest project-system sidecar?
3. Can a sidecar accidentally become scientific authority?
4. Can generated current-frontier wording be mistaken for proof?
5. Does the next route remain upstream theorem/countermodel work unless explicitly superseded?

#### Required output

```text
research_control/tasks/<task-id>/artifacts/active_state_bifurcation_red_team_review_v1.md
```

#### Done criteria

- Review result is `pass`, `repair_required`, or `fail_closed`.
- If repair is required, the next route is a repair task.
- If pass, the next route is `P2-T01`.

---

## 7. Phase P2: Typed source-equivalence object formalization

### P2 objective

Implement recommendation `V18-R02` and prepare recommendation `V18-R01` by formalizing the source-equivalence layer as a typed mathematical object before attempting family-level closure.

### P2-T01: Source-equivalence typed-object problem statement

```yaml
plan_task_id: "P2-T01"
task_type: "source_equivalence_typed_object_problem_statement"
recommendation_ids: ["V18-R01", "V18-R02"]
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Define the exact typed-object burden for EqSrc, RetainH, and GenH continuation."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "typed_eqsrc_problem_statement_no_promotion"
```

#### Objective

Write a problem statement that translates the prior record-local `EqSrc` theorem candidate into a typed source-equivalence object target.

#### Required output

```text
research_control/tasks/<task-id>/artifacts/source_equivalence_typed_object_problem_statement_v1.md
```

#### Required content

- The prior record-local theorem target.
- The named obstruction `OB-P6T02-GENERAL-EQSRC-FAMILY-CLOSURE-MISSING`.
- The distinction between record-local orbit and source family.
- Candidate structure using objects, morphisms/relabelings, invariant ledgers, comparison rules, identities, inverses, and composition.
- Where `RetainH` and `GenH` enter.
- What counts as theorem success.
- What counts as countermodel success.
- What counts as primitive requirement.
- What counts as freeze.
- Forbidden conclusions.

#### Done criteria

- The next route is `P2-T02`.
- No general `EqSrc` discharge is claimed.
- No `RetainH` or `GenH` adoption is claimed.

### P2-T02: Typed source-equivalence schema and registry

```yaml
plan_task_id: "P2-T02"
task_type: "source_equivalence_typed_schema"
recommendation_ids: ["V18-R02"]
role_family: "schema-maintainer@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Create a machine-readable schema for typed source-equivalence objects."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "schema_update_no_physics_delta"
```

#### Required outputs

```text
research_control/design/source_equivalence_typed_object_schema_v1.md
registries/SOURCE_EQUIVALENCE_OBJECT_REGISTRY.csv
```

#### Required CSV columns

```csv
object_id,artifact_path,task_id,source_family_symbol,object_set_status,morphism_status,invariant_ledger_status,comparison_rule_status,identity_closure_status,inverse_closure_status,composition_closure_status,retainh_status,genh_status,no_target_guard_status,proof_state,blocked_overread,created_at,notes
```

#### Required schema model

```yaml
source_equivalence_typed_object_v1:
  source_family:
    symbol: string
    domain_status: declared | missing | partial | countermodel
    finite_or_family_scope: finite | locally_finite | family_level | unspecified
  objects:
    status: explicit | implicit | missing
    source_only: true
  morphisms:
    status: explicit | generated | missing | countermodel
    admissibility_rule: string
    target_import_guard: true
  invariant_ledger:
    status: explicit | partial | missing
    family_validity: proven | assumed | refuted | unknown
  comparison_rule:
    status: explicit | partial | missing
    source_only: true
  closure:
    identity: supplied | derived | missing | countermodel
    inverse: supplied | derived | missing | countermodel
    composition: supplied | derived | missing | countermodel
  retainh:
    status: not_required | required | candidate | missing | adopted_by_gate
  genh:
    status: not_required | required | candidate | missing | adopted_by_gate
  no_target_guard:
    target_topology_imported: false
    target_metric_imported: false
    detector_protocol_imported: false
    stress_energy_imported: false
    matter_action_imported: false
    benchmark_behavior_imported: false
```

#### Done criteria

- Schema and registry exist.
- Registry contains header only unless P2-T03 populates rows.
- The schema marks adoption fields as gate-protected.
- The next route is `P2-T03`.

### P2-T03: Source-equivalence typed object science draft

```yaml
plan_task_id: "P2-T03"
task_type: "source_equivalence_typed_object_science_draft"
recommendation_ids: ["V18-R01", "V18-R02"]
role_family: "ontology-formalizer@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Define the typed source-equivalence object that will support the family-closure theorem-or-countermodel attempt."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "typed_eqsrc_object_defined_no_promotion"
```

#### Required science artifact

```text
research_control/tasks/<task-id>/artifacts/source_equivalence_typed_object_v1.tex
```

#### Required sections

1. Control Status.
2. Prior Record-Local Theorem.
3. Typed Source Family.
4. Source Objects.
5. Admissible Source Morphisms or Relabelings.
6. Invariant Ledger.
7. Source-Only Comparison Rule.
8. Identity Closure.
9. Inverse Closure.
10. Composition Closure.
11. `RetainH` Boundary.
12. `GenH` Boundary.
13. No-Target Guard.
14. Family-Level Burden.
15. Countermodel Slots.
16. Distance-to-GR Effect.
17. Forbidden Conclusions.
18. Source Materials.

#### Required mathematical payload

```yaml
new_mathematical_payload:
  - payload_type: "typed_source_equivalence_definition"
    object_name: "SourceEquivalenceTypedObject_v1"
    scope: "source_equivalence_eqsrc"
    claim_status: "science_draft_definition_only"
    proof_authority: false
```

#### Done criteria

- The typed object is defined without importing target topology, target metric, detector protocol, stress-energy, matter action, benchmark behavior, validator status, role status, or handoff status.
- The artifact states whether identity/inverse/composition are supplied, derived, missing, or countermodel-open.
- No general `EqSrc` discharge is claimed.
- The next route is `P2-T04`.

### P2-T04: Smuggling audit of typed source-equivalence object

```yaml
plan_task_id: "P2-T04"
task_type: "source_equivalence_typed_object_smuggling_audit"
recommendation_ids: ["V18-R02"]
role_family: "smuggling-auditor@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Audit the typed source-equivalence object for target imports and process-authority imports."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "typed_eqsrc_audited_no_promotion"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/source_equivalence_typed_object_smuggling_audit_v1.tex
```

#### Audit targets

```yaml
audit_targets:
  - target topology import
  - target smooth atlas import
  - target Lorentzian metric import
  - proper-time normalization import
  - detector protocol import
  - empirical calibration import
  - stress-energy semantics import
  - matter-action import
  - Einstein-equation premise import
  - benchmark behavior import
  - validation status as premise
  - registry metadata as theorem premise
  - role identity as theorem premise
  - handoff state as theorem premise
  - commit state as theorem premise
  - generated derivative as theorem premise
```

#### Done criteria

- Audit result is `source_pure_as_written`, `repair_required`, or `fails_closed`.
- Any failure names one primary obstruction.
- Success routes to P2-T05.
- Failure routes to a repair task or selector.

### P2-T05: Refuter stress of typed source-equivalence object

```yaml
plan_task_id: "P2-T05"
task_type: "source_equivalence_typed_object_refuter_stress"
recommendation_ids: ["V18-R02", "V18-R03"]
role_family: "refuter@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Stress the typed source-equivalence object for missing closure, weak invariants, and hidden primitive dependence."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "typed_eqsrc_stressed_no_promotion"
```

#### Stress modes

```yaml
stress_modes:
  - remove_identity_maps
  - remove_inverse_maps
  - remove_composition_table
  - weaken_family_invariant_ledger
  - introduce_morphism_outside_declared_family
  - alter_forbidden_channel_orientation
  - introduce_proxy_edge_without_mapping
  - replace_source_comparison_rule_with_target_success_proxy
  - require_RetainH_without_declaring_RetainH
  - require_GenH_without_declaring_GenH
  - treat_validation_pass_as_theorem_premise
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/source_equivalence_typed_object_refuter_stress_v1.tex
```

#### Done criteria

- Stress result is one of `survives_as_draft_control_definition`, `repair_required`, `scoped_obstruction`, or `freeze_candidate_route`.
- The result identifies which closure obligations remain live.
- The next route is `P2-T06`.

### P2-T06: Typed-object continuation selector

```yaml
plan_task_id: "P2-T06"
task_type: "source_equivalence_typed_object_continuation_selector"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03"]
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select one next route after typed-object definition, audit, and stress."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "selector_no_promotion"
```

#### Allowed next routes

```yaml
allowed_next_routes:
  - P3_T01_family_closure_theorem_or_countermodel_setup
  - repair_typed_source_equivalence_definition
  - minimal_countermodel_obligation_system_first
  - RetainH_primitive_requirement_packet
  - GenH_primitive_requirement_packet
  - scoped_obstruction_freeze_review
```

#### Done criteria

- Exactly one next route is selected.
- If P2 stress passed or yielded a precise live obstruction, route to `P3-T01`.
- No adoption or downstream promotion is claimed.

---

## 8. Phase P3: EqSrc family-closure theorem-or-countermodel packet

### P3 objective

Implement recommendation `V18-R01` directly and use recommendation `V18-R03` in the task design: run the upstream family-closure theorem/countermodel continuation that the current research handoff selected.

### P3-T01: EqSrc family-closure theorem-or-countermodel setup

```yaml
plan_task_id: "P3-T01"
task_type: "eqsrc_family_closure_theorem_or_countermodel_setup"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03"]
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Set up one bounded EqSrc family-closure theorem-or-countermodel packet after typed-object audit and stress."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "theorem_countermodel_setup_no_promotion"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/eqsrc_family_closure_packet_setup_v1.md
```

#### Setup must define

```yaml
eqsrc_family_closure_packet_setup:
  source_family_symbol: "F_src"
  typed_object_artifact: "research_control/tasks/<P2-T03-task>/artifacts/source_equivalence_typed_object_v1.tex"
  theorem_or_countermodel_artifact: "eqsrc_family_closure_theorem_or_countermodel_v1.tex"
  max_primary_payload_count: 1
  allowed_primary_payloads:
    - family_level_eqsrc_closure_theorem_candidate
    - minimal_family_closure_countermodel
    - RetainH_primitive_required
    - GenH_primitive_required
    - scoped_freeze_obstruction
  countermodel_obligation_required: true
  no_target_import_guard_required: true
  adoption_requested: false
```

#### Done criteria

- The setup names exactly one packet target.
- The setup requires a theorem candidate or a minimal countermodel.
- The setup requires explicit analysis of `RetainH` and `GenH`.
- The next route is `P3-T02`.

### P3-T02: Execute EqSrc family-closure theorem-or-countermodel attempt

```yaml
plan_task_id: "P3-T02"
task_type: "eqsrc_family_closure_theorem_or_countermodel"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03"]
role_family: "ontology-formalizer@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Discharge, refute, or sharpen OB-P6T02-GENERAL-EQSRC-FAMILY-CLOSURE-MISSING."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "theorem_candidate_or_countermodel_no_promotion"
```

#### Required science artifact

```text
research_control/tasks/<task-id>/artifacts/eqsrc_family_closure_theorem_or_countermodel_v1.tex
```

#### Required artifact sections

1. Control Status.
2. Prior Record-Local `EqSrc` Theorem.
3. Typed Source Family.
4. Family Invariant Ledger.
5. Candidate Family-Level `EqSrc` Relation.
6. Identity Closure Attempt.
7. Inverse Closure Attempt.
8. Composition Closure Attempt.
9. `RetainH` Trigger Analysis.
10. `GenH` Trigger Analysis.
11. Minimal Countermodel Search.
12. Theorem Candidate or Obstruction.
13. Distance-to-GR Effect.
14. Forbidden Conclusions.
15. Source Materials.

#### Required decision branch

Exactly one branch must be primary:

```yaml
primary_result_one_of:
  family_closure_theorem_candidate_supplied:
    required_fields:
      - family_domain_declared
      - family_invariant_ledger_validity_claim
      - source_only_comparison_rule
      - identity_closure
      - inverse_closure
      - composition_closure
      - no_target_guard
      - theorem_scope
      - stress_required_before_adoption
  minimal_countermodel_supplied:
    required_fields:
      - countermodel_id
      - missing_closure_component
      - finite_or_locally_finite_witness
      - exact_obstruction_scope
      - global_no_go_claimed_false
  retainh_primitive_required:
    required_fields:
      - RetainH_requirement_statement
      - why_current_source_data_do_not_derive_it
      - minimal_witness_or_countermodel
      - adoption_requested_false
  genh_primitive_required:
    required_fields:
      - GenH_requirement_statement
      - why_current_source_data_do_not_derive_it
      - minimal_witness_or_countermodel
      - adoption_requested_false
  scoped_freeze_obstruction:
    required_fields:
      - obstruction_id
      - freeze_scope
      - repeated_burden_analysis
      - new_payload_exhaustion_argument
      - global_no_go_claimed_false
```

#### Required minimal countermodel slots

Even if the primary branch is theorem candidate, the artifact must include at least one attempted countermodel slot:

```yaml
countermodel_slots:
  - missing_inverse_countermodel
  - missing_composition_countermodel
  - invariant_ledger_not_family_stable_countermodel
  - target_import_needed_countermodel
  - RetainH_needed_countermodel
  - GenH_needed_countermodel
```

#### Done criteria

- Exactly one primary result is produced.
- No adoption is requested.
- No general `EqSrc` discharge is claimed unless the theorem candidate explicitly proves all family closure obligations and still routes to audit/stress before any ledger change.
- The next route is `P3-T03`.

### P3-T03: RetainH and GenH primitive-boundary extraction

```yaml
plan_task_id: "P3-T03"
task_type: "retainh_genh_primitive_boundary_extraction"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03"]
role_family: "ontology-formalizer@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Extract exact RetainH and GenH primitive-boundary consequences from the P3-T02 theorem-or-countermodel result."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "primitive_boundary_extracted_no_adoption"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/retainh_genh_primitive_boundary_v1.tex
```

#### Required sections

1. Control Status.
2. Inputs from P3-T02.
3. `RetainH` Boundary.
4. `GenH` Boundary.
5. Primitive Needed, Primitive Avoided, or Primitive Deferred Classification.
6. Minimal Witness or Countermodel.
7. No-Target Import Guard.
8. Distance-to-GR Effect.
9. Forbidden Conclusions.

#### Done criteria

- `RetainH` and `GenH` are each classified as `not_required_here`, `required_but_missing`, `candidate_definition_needed`, `countermodel_blocks_current_route`, or `deferred`.
- Neither primitive is adopted.
- The next route is `P3-T04`.

### P3-T04: Smuggling audit of family-closure attempt

```yaml
plan_task_id: "P3-T04"
task_type: "eqsrc_family_closure_smuggling_audit"
recommendation_ids: ["V18-R01", "V18-R03"]
role_family: "smuggling-auditor@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Audit the family-closure theorem-or-countermodel attempt for target imports and authority laundering."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "eqsrc_family_audited_no_promotion"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/eqsrc_family_closure_smuggling_audit_v1.tex
```

#### Done criteria

- Audit result is `source_pure_as_written`, `repair_required`, or `fails_closed`.
- If theorem branch was primary, audit checks whether family closure was derived or merely supplied.
- If countermodel branch was primary, audit checks whether the countermodel is genuinely source-side.
- The next route is `P3-T05`.

### P3-T05: Refuter stress of family-closure attempt

```yaml
plan_task_id: "P3-T05"
task_type: "eqsrc_family_closure_refuter_stress"
recommendation_ids: ["V18-R01", "V18-R03"]
role_family: "refuter@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Stress the P3 family-closure result against closure removal, invariant weakening, primitive-dependence, and target-import attacks."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "eqsrc_family_stressed_no_promotion"
```

#### Stress modes

```yaml
stress_modes:
  - remove_family_identity_closure
  - remove_inverse_closure
  - remove_composition_closure
  - weaken_invariant_ledger
  - expand_source_family_without_GenH
  - apply_H_retention_without_RetainH
  - replace_source_invariant_with_target_success
  - allow_missing_negative_controls
  - import_metric_or_detector_protocol
  - treat_theorem_candidate_as_adopted_EqSrc
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/eqsrc_family_closure_refuter_stress_v1.tex
```

#### Done criteria

- Stress result is `survives_as_theorem_candidate`, `minimal_countermodel_survives`, `repair_required`, `scoped_obstruction`, or `freeze_route`.
- The result does not adopt general `EqSrc`, `RetainH`, or `GenH`.
- The next route is `P3-T06`.

### P3-T06: Post-family-closure selector

```yaml
plan_task_id: "P3-T06"
task_type: "post_eqsrc_family_closure_selector"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03"]
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select one next route after family-closure theorem/countermodel, audit, and stress."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "selector_no_promotion"
```

#### Allowed routes

```yaml
allowed_next_routes:
  - P4_T01_countermodel_obligation_system
  - RetainH_definition_candidate_packet
  - GenH_definition_candidate_packet
  - repair_family_closure_theorem_packet
  - scoped_obstruction_freeze_review
  - source_detector_readout_semantics_frontier_burden
  - external_review_packet_preparation_after_internal_integration
```

#### Done criteria

- Exactly one route is selected.
- Freeze criteria are evaluated if repeated-burden behavior is detected.
- The default next route is `P4-T01` unless repair or freeze is mandatory.

---

## 9. Phase P4: Minimal countermodel obligation system

### P4 objective

Implement recommendation `V18-R03` as a standing theorem-packet discipline so future theorem attempts include minimal countermodel obligations instead of proving only under supplied closure assumptions.

### P4-T01: Countermodel obligation policy

```yaml
plan_task_id: "P4-T01"
task_type: "countermodel_obligation_policy"
recommendation_ids: ["V18-R03"]
role_family: "project-control-maintainer@0.2.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Define minimal countermodel obligations for future theorem attempts."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "countermodel_policy_no_physics_delta"
```

#### Required output

```text
research_control/design/minimal_countermodel_obligation_policy_v1.md
```

#### Required sections

1. Why theorem attempts require countermodel slots.
2. Difference between countermodel, obstruction, freeze, and global no-go.
3. Required countermodel slots by theorem family.
4. EqSrc-specific slots.
5. Matter-coupling-specific slots.
6. Detector/readout-specific slots.
7. Toy-model-specific slots.
8. Completion receipt requirements.
9. Validator requirements.
10. Forbidden conclusions.

#### Done criteria

- The policy makes countermodel slots mandatory for theorem attempts unless waived by an explicit Director Decision Record.
- The policy forbids reading a local countermodel as program-wide no-go.
- The next route is `P4-T02`.

### P4-T02: Countermodel obligation schema and registry extension

```yaml
plan_task_id: "P4-T02"
task_type: "countermodel_obligation_schema_registry"
recommendation_ids: ["V18-R03"]
role_family: "schema-maintainer@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Add machine-readable countermodel obligation fields to theorem/control registries."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "schema_update_no_physics_delta"
```

#### Required outputs

```text
research_control/design/minimal_countermodel_obligation_schema_v1.md
registries/COUNTERMODEL_OBLIGATION_REGISTRY.csv
```

#### Required columns

```csv
obligation_id,task_id,artifact_path,theorem_family,countermodel_slot,status,result_artifact,obstruction_id,scope,global_no_go_claimed,created_at,notes
```

#### Done criteria

- Schema exists.
- Registry has header and initial rows for P3 outputs if available.
- The next route is `P4-T03`.

### P4-T03: Countermodel obligation validator and tests

```yaml
plan_task_id: "P4-T03"
task_type: "countermodel_obligation_validator"
recommendation_ids: ["V18-R03"]
role_family: "validator-engineer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Add advisory validation that theorem attempts include countermodel slots."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "validator_update_no_physics_delta"
```

#### Required modifications

```text
scripts/research_control/validate_research_control.py
scripts/project_control/validate_claim_language.py
tests/test_countermodel_obligation_validator.py
tests/fixtures/countermodel_obligations/
```

#### Initial severity

```yaml
initial_severity:
  missing_countermodel_slot: "warn_current_control"
  countermodel_overread_as_global_no_go: "overclaim_hard_fail"
  theorem_without_countermodel_justification: "warn_current_control"
  countermodel_scope_missing: "warn_current_control"
```

#### Done criteria

- Existing validation passes.
- Missing countermodel slots warn but do not hard-fail during the first v18 cycle.
- Global no-go overread hard-fails.
- The next route is `P4-T04`.

### P4-T04: Theorem-task template integration

```yaml
plan_task_id: "P4-T04"
task_type: "countermodel_obligation_task_template_integration"
recommendation_ids: ["V18-R03"]
role_family: "documentation-curator@2.0.0"
target_derivation_milestone: "none"
milestone_burden: "Update theorem-task templates to require minimal countermodel slots."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "template_update_no_physics_delta"
```

#### Candidate files

```text
research_control/tasks/README.md
research_control/design/minimum_physics_payload_schema_v16.md
research_control/design/proof_normal_form_schema_v1.md
.codex/skills/continue-research/SKILL.md
```

#### Done criteria

- The task template requires a theorem candidate to include countermodel slots or an explicit waiver.
- The update does not change physics claims.
- The next route is `P4-T05`.

### P4-T05: Countermodel obligation pilot on P3 outputs

```yaml
plan_task_id: "P4-T05"
task_type: "countermodel_obligation_pilot"
recommendation_ids: ["V18-R03", "V18-R01"]
role_family: "process-integrity-auditor@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Pilot the countermodel obligation registry on the P3 EqSrc family-closure packet."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "countermodel_pilot_no_promotion"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/countermodel_obligation_pilot_report_v1.md
```

#### Done criteria

- P3 theorem/countermodel slots are listed in the registry.
- Missing slots are marked `not_applicable`, `attempted`, `satisfied`, or `deferred_with_reason`.
- No global no-go is claimed.
- The next route is `P4-T06`.

### P4-T06: Countermodel obligation red-team review

```yaml
plan_task_id: "P4-T06"
task_type: "countermodel_obligation_red_team_review"
recommendation_ids: ["V18-R03"]
role_family: "external-red-team-reviewer@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Stress the countermodel obligation system for false blockage, overclaim, and process orbit."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "red_team_review_no_promotion"
```

#### Done criteria

- Review result is `pass`, `repair_required`, or `fail_closed`.
- The review checks that countermodel obligations do not become a substitute for theorem work.
- If pass, the next route is `P5-T01`.

---

## 10. Phase P5: Source detector/readout semantics frontier burden

### P5 objective

Implement recommendation `V18-R04`: promote source detector/readout semantics to a named frontier burden while preserving that no detector semantics, matter coupling, stress-energy, matter action, Einstein equations, or benchmark status are adopted.

### P5-T01: Source detector/readout burden design note

```yaml
plan_task_id: "P5-T01"
task_type: "source_detector_readout_burden_design_note"
recommendation_ids: ["V18-R04"]
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Define source detector/readout semantics as a named matter-coupling frontier burden."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_readout_burden_design_no_adoption"
```

#### Required output

```text
research_control/design/source_detector_readout_semantics_burden_v1.md
```

#### Required burden model

```yaml
burden_id: "source_detector_readout_semantics"
milestone: "matter_coupling"
required_object: "Det_src or Readout_src"
current_status: "proposal_burden_only"
blocking_burden: "source-side readout law without empirical detector, proper-time, target metric, stress-energy, matter-action, or benchmark import"
accept_criteria:
  - source-side readout law
  - no empirical detector protocol import
  - no proper-time import
  - no target metric import
  - finite/local witness
  - compatibility with SourceCouplingLawCandidate_EStar_v1
failure_or_freeze_criteria:
  - detector_semantics_requires_target_import
  - readout_law_requires_new_source_primitive
  - route_repeats_placeholder_without_new_payload
```

#### Done criteria

- The note defines the burden but does not update the Distance-to-GR ledger unless separately authorized.
- The note states that source detector/readout semantics are not adopted.
- The next route is `P5-T02`.

### P5-T02: Matter-coupling DAG and ledger-delta question setup

```yaml
plan_task_id: "P5-T02"
task_type: "source_detector_readout_dag_ledger_question_setup"
recommendation_ids: ["V18-R04"]
role_family: "project-control-maintainer@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Prepare a protected question for adding source_detector_readout_semantics to DAG or ledger surfaces without performing unauthorized promotion."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "ledger_question_setup_no_delta"
```

#### Required outputs

```text
research_control/tasks/<task-id>/artifacts/source_detector_readout_ledger_delta_question_v1.yaml
research_control/tasks/<task-id>/artifacts/source_detector_readout_dag_patch_proposal_v1.md
```

#### Required fields

```yaml
ledger_delta_question:
  proposed_burden_id: "source_detector_readout_semantics"
  proposed_status: "proposal_burden_only"
  proposed_control_status: "burden_proposed_not_adopted"
  proposed_mathematical_status: "readout_law_missing"
  proposed_physical_status: "not_detector_semantics_not_matter_coupling"
  promotion_status: "none"
  requires_protected_authority_to_update_ledger: true
  update_performed_in_this_task: false
```

#### Done criteria

- The task creates a question/proposal only.
- No protected ledger update is performed unless explicitly authorized by a later human-gated task.
- The next route is `P5-T03`.

### P5-T03: Source detector/readout candidate setup

```yaml
plan_task_id: "P5-T03"
task_type: "source_detector_readout_candidate_setup"
recommendation_ids: ["V18-R04"]
role_family: "candidate-constructor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Set up one bounded source detector/readout candidate or obstruction packet."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_readout_setup_no_adoption"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/source_detector_readout_candidate_setup_v1.md
```

#### Setup must define

```yaml
source_detector_readout_candidate_setup:
  candidate_name: "SourceReadoutCandidate_EStar_v1"
  source_domain: "SMScope(E_*)"
  readout_symbol: "Readout_src(E_*)"
  detector_symbol: "Det_src(E_*)"
  compatibility_target: "SourceCouplingLawCandidate_EStar_v1"
  finite_local_witness_required: true
  empirical_protocol_import_forbidden: true
  proper_time_import_forbidden: true
  target_metric_import_forbidden: true
  adoption_requested: false
```

#### Done criteria

- Exactly one candidate target or obstruction branch is named.
- The next route is `P5-T04`.

### P5-T04: Construct source detector/readout candidate or obstruction

```yaml
plan_task_id: "P5-T04"
task_type: "source_detector_readout_candidate_or_obstruction"
recommendation_ids: ["V18-R04"]
role_family: "candidate-constructor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Construct one source-side detector/readout candidate or record one precise obstruction."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_readout_candidate_or_obstruction_no_adoption"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/source_detector_readout_candidate_v1.tex
```

#### Positive candidate must include

```yaml
source_detector_readout_candidate:
  source_domain: string
  readout_interface: string
  detector_source_record: string
  certificate_bundle: string
  finite_local_witness: string
  compatible_with_K_Estar: true | false
  status: "draft_control_candidate"
  no_empirical_protocol_import: true
  no_proper_time_import: true
  no_target_metric_import: true
  detector_semantics_adopted: false
  matter_coupling_derived: false
```

#### Obstruction must include

```yaml
source_detector_readout_obstruction:
  obstruction_id: "OB-V18-READOUT-<short-label>"
  exact_missing_burden: string
  scoped_to_current_route: true
  global_no_go_claimed: false
```

#### Done criteria

- Exactly one candidate or one obstruction is produced.
- No detector semantics are adopted.
- Candidate routes to audit and stress.
- Obstruction routes to selector.
- The next route is `P5-T05`.

### P5-T05: Source detector/readout smuggling audit

```yaml
plan_task_id: "P5-T05"
task_type: "source_detector_readout_smuggling_audit"
recommendation_ids: ["V18-R04"]
role_family: "smuggling-auditor@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Audit source detector/readout candidate for empirical detector, proper-time, target metric, benchmark, and process-authority imports."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_readout_audited_no_adoption"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/source_detector_readout_smuggling_audit_v1.tex
```

#### Done criteria

- Audit result is `source_pure_as_written`, `repair_required`, or `fails_closed`.
- No detector/readout semantics are adopted.
- The next route is `P5-T06`.

### P5-T06: Source detector/readout Refuter stress

```yaml
plan_task_id: "P5-T06"
task_type: "source_detector_readout_refuter_stress"
recommendation_ids: ["V18-R04"]
role_family: "refuter@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Stress source detector/readout candidate against placeholder collapse, empirical substitution, and finite/local perturbations."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_readout_stressed_no_adoption"
```

#### Stress modes

```yaml
stress_modes:
  - readout_interface_erasure
  - source_record_removal
  - empirical_detector_protocol_substitution
  - proper_time_substitution
  - target_metric_substitution
  - benchmark_behavior_substitution
  - finite_local_witness_perturbation
  - K_Estar_compatibility_failure
  - placeholder_as_adoption_laundering
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/source_detector_readout_refuter_stress_v1.tex
```

#### Done criteria

- Stress result is `survives_as_draft_control_candidate`, `repair_required`, `scoped_obstruction`, or `freeze_route`.
- The next route is `P5-T07`.

### P5-T07: Source detector/readout route selector and integration

```yaml
plan_task_id: "P5-T07"
task_type: "source_detector_readout_route_selector_integration"
recommendation_ids: ["V18-R04"]
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Select one next route after source detector/readout candidate or obstruction."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "detector_readout_route_selected_no_adoption"
```

#### Allowed routes

```yaml
allowed_next_routes:
  - integrate_readout_candidate_into_K_E_repair
  - repair_source_readout_candidate
  - route_readout_obstruction_freeze_review
  - request_protected_ledger_burden_update
  - proceed_to_finite_toy_response_v2
  - return_to_EqSrc_RetainH_GenH
```

#### Done criteria

- Exactly one route is selected.
- If the source detector/readout candidate survived, it remains draft/control only.
- The default next route is `P6-T01` unless repair or freeze is mandatory.

---

## 11. Phase P6: Non-tag-fragile finite toy response model v2

### P6 objective

Implement recommendation `V18-R05`: design and test a finite toy response model that does not depend on explicit tags that fail tag-removal stress.

### P6-T01: Finite toy response v2 source specification

```yaml
plan_task_id: "P6-T01"
task_type: "finite_toy_response_v2_source_spec"
recommendation_ids: ["V18-R05"]
role_family: "ontology-formalizer@0.2.0"
target_derivation_milestone: "finite_toy_metric_response"
milestone_burden: "Specify a non-tag-fragile finite source-to-response toy target."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "toy_response_spec_no_promotion"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/finite_toy_response_v2_source_spec.tex
```

#### Required model fields

```yaml
finite_toy_response_v2:
  finite_source_set: required
  source_relation_family: required
  invariant_orbit_structure: required
  induced_response_relation: required
  explicit_target_tags_forbidden: true
  target_metric_import_forbidden: true
  empirical_detector_import_forbidden: true
  relabeling_invariance_test: required
  tag_removal_stress: required
  detector_readout_status: explicit_candidate_or_placeholder
```

#### Done criteria

- The target explicitly avoids tag-only response structure.
- The target states how it differs from the frozen negative tag route.
- The next route is `P6-T02`.

### P6-T02: Construct finite toy response v2 or obstruction

```yaml
plan_task_id: "P6-T02"
task_type: "finite_toy_response_v2_model_or_obstruction"
recommendation_ids: ["V18-R05"]
role_family: "candidate-constructor@0.2.0"
target_derivation_milestone: "finite_toy_metric_response"
milestone_burden: "Construct a non-tag finite toy response model or record a precise obstruction."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "toy_model_or_obstruction_no_promotion"
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/finite_toy_response_v2_model_or_obstruction.tex
```

#### Positive model must include

```yaml
positive_toy_model:
  finite_source_set: explicit
  source_relations: explicit
  orbit_or_invariant_structure: explicit
  induced_response_relation: explicit
  tag_independence_argument: explicit
  relabeling_invariance_argument: explicit
  no_target_metric_import: true
  not_g_eff: true
  not_matter_coupling: true
```

#### Obstruction must include

```yaml
toy_model_obstruction:
  obstruction_id: "OB-V18-TOY-V2-<short-label>"
  obstruction_scope: "finite toy response v2 route"
  exact_missing_burden: string
  frozen_negative_reuse: false
  global_no_go_claimed: false
```

#### Done criteria

- Exactly one toy model or one obstruction is produced.
- No `g_eff`, matter coupling, Einstein equations, or benchmark claim follows.
- The next route is `P6-T03`.

### P6-T03: Finite toy response v2 invariance and tag-removal stress

```yaml
plan_task_id: "P6-T03"
task_type: "finite_toy_response_v2_invariance_tag_stress"
recommendation_ids: ["V18-R05"]
role_family: "refuter@0.2.0"
target_derivation_milestone: "finite_toy_metric_response"
milestone_burden: "Stress finite toy response v2 against relabeling, tag removal, and target-import collapse."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "toy_model_stressed_no_promotion"
```

#### Stress modes

```yaml
stress_modes:
  - remove_explicit_labels_or_tags
  - relabel_source_tokens
  - perturb_source_relation_edges
  - collapse_invariant_orbit_structure
  - substitute_target_distance
  - substitute_physical_metric
  - substitute_empirical_readout
  - treat_toy_response_as_g_eff
  - treat_toy_response_as_matter_coupling
```

#### Required artifact

```text
research_control/tasks/<task-id>/artifacts/finite_toy_response_v2_refuter_stress.tex
```

#### Done criteria

- Stress result is `survives_as_finite_toy_model`, `repair_required`, `scoped_obstruction`, or `freeze_route`.
- If it fails tag-removal stress, freeze only this v2 route unless broader proof justifies more.
- The next route is `P6-T04`.

### P6-T04: Source-model zoo integration for toy v2

```yaml
plan_task_id: "P6-T04"
task_type: "finite_toy_response_v2_model_zoo_integration"
recommendation_ids: ["V18-R05"]
role_family: "ontology-formalizer@0.2.0"
target_derivation_milestone: "finite_toy_metric_response"
milestone_burden: "Integrate finite toy response v2 model, obstruction, and stress status into the source model zoo."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "toy_model_zoo_integration_no_promotion"
```

#### Required outputs

```text
research_control/design/source_model_zoo_schema_v18_extension.md
registries/SOURCE_MODEL_ZOO_REGISTRY.csv
research_control/tasks/<task-id>/artifacts/finite_toy_response_v2_model_zoo_entry.yaml
```

#### Done criteria

- Model or obstruction is retrievable through the source model zoo.
- Frozen negative status is scoped if applicable.
- The next route is `P6-T05`.

### P6-T05: Finite toy response v2 selector

```yaml
plan_task_id: "P6-T05"
task_type: "finite_toy_response_v2_selector"
recommendation_ids: ["V18-R05"]
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "finite_toy_metric_response"
milestone_burden: "Select repair, freeze, source detector/readout continuation, or upstream return after finite toy response v2."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "toy_selector_no_promotion"
```

#### Allowed routes

```yaml
allowed_next_routes:
  - repair_finite_toy_response_v2
  - freeze_finite_toy_response_v2_route
  - source_detector_readout_repair
  - source_model_zoo_expansion
  - support_formalization_expansion
  - return_to_EqSrc_RetainH_GenH
```

#### Done criteria

- Exactly one next route is selected.
- The default next route is `P7-T01` unless repair/freeze is mandatory.

---

## 12. Phase P7: Authority-limited support formalization expansion

### P7 objective

Implement recommendation `V18-R06`: expand support formalization into proof-adjacent tooling while preserving that executable checks, validators, and generated artifacts do not become proof authority.

### P7-T01: Support formalization target selector

```yaml
plan_task_id: "P7-T01"
task_type: "support_formalization_target_selector_v18"
recommendation_ids: ["V18-R06"]
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select the first support-only formalization target from the v18 recommendation set."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "formalization_selector_no_proof_authority"
```

#### Allowed targets

```yaml
allowed_formalization_targets:
  - typed_EqSrc_orbit_checker
  - closure_countermodel_generator
  - no_target_import_mutation_tester
  - metric_use_ledger_tex_validator
  - detector_placeholder_collapse_checker
```

#### Done criteria

- Exactly one target is selected for immediate implementation.
- The selector may sequence the remaining targets for later P7 tasks.
- The next route is `P7-T02`.

### P7-T02: Typed EqSrc orbit checker

```yaml
plan_task_id: "P7-T02"
task_type: "typed_eqsrc_orbit_checker_support_only"
recommendation_ids: ["V18-R06", "V18-R02"]
role_family: "formalization-engineer@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Implement a support-only checker for finite typed EqSrc orbit closure records."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "support_formalization_no_proof_authority"
```

#### Required outputs

```text
scripts/research_control/support_formalization/typed_eqsrc_orbit_checker.py
tests/test_typed_eqsrc_orbit_checker.py
research_control/tasks/<task-id>/artifacts/typed_eqsrc_orbit_checker_spec_v1.md
```

#### Checker scope

The checker may verify finite records for:

- Declared objects.
- Explicit identity maps.
- Explicit inverse maps.
- Explicit composition table.
- Source-only invariant preservation flags.
- Fail-closed status for missing data.

It must not claim to prove general `EqSrc`.

#### Done criteria

- Unit tests pass.
- Traceability note states support-only authority.
- The next route is `P7-T03`.

### P7-T03: Closure countermodel generator

```yaml
plan_task_id: "P7-T03"
task_type: "closure_countermodel_generator_support_only"
recommendation_ids: ["V18-R06", "V18-R03"]
role_family: "formalization-engineer@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Implement a support-only generator for minimal missing-closure countermodels."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "support_formalization_no_proof_authority"
```

#### Required outputs

```text
scripts/research_control/support_formalization/closure_countermodel_generator.py
tests/test_closure_countermodel_generator.py
research_control/tasks/<task-id>/artifacts/closure_countermodel_generator_spec_v1.md
```

#### Generator modes

```yaml
countermodel_modes:
  - missing_identity
  - missing_inverse
  - missing_composition
  - non_family_stable_invariant
  - RetainH_required
  - GenH_required
```

#### Done criteria

- Generator creates finite mock records demonstrating each configured missing-closure mode.
- Output is marked support-only.
- The next route is `P7-T04`.

### P7-T04: No-target import mutation tester

```yaml
plan_task_id: "P7-T04"
task_type: "no_target_import_mutation_tester_support_only"
recommendation_ids: ["V18-R06"]
role_family: "validator-engineer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Implement a support-only mutation tester for no-target import guards."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "support_formalization_no_proof_authority"
```

#### Required outputs

```text
scripts/research_control/support_formalization/no_target_import_mutation_tester.py
tests/test_no_target_import_mutation_tester.py
research_control/tasks/<task-id>/artifacts/no_target_import_mutation_tester_spec_v1.md
```

#### Mutations

```yaml
mutations:
  - insert_target_metric_premise
  - insert_proper_time_normalization
  - insert_empirical_detector_protocol
  - insert_stress_energy_semantics
  - insert_matter_action_premise
  - insert_benchmark_behavior_premise
  - insert_validator_as_proof_premise
```

#### Done criteria

- Mutations trigger expected failures in fixtures.
- No source-law or proof authority is claimed.
- The next route is `P7-T05`.

### P7-T05: Metric-use ledger TeX validator

```yaml
plan_task_id: "P7-T05"
task_type: "metric_use_ledger_tex_validator_support_only"
recommendation_ids: ["V18-R06"]
role_family: "validator-engineer@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Implement support-only validation that high-risk metric references in TeX have ledger rows or no-use justification."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "support_formalization_no_proof_authority"
```

#### Required outputs

```text
scripts/research_control/validate_metric_use_tex_references.py
tests/test_validate_metric_use_tex_references.py
research_control/tasks/<task-id>/artifacts/metric_use_tex_validator_spec_v1.md
```

#### Done criteria

- The validator catches unledgered `g_eff`, `MetricData(E)`, proper-time, detector-calibration, stress-energy, and matter-action references in configured TeX artifacts.
- The validator can be integrated into full validation as warning or hard fail according to existing policy.
- The next route is `P7-T06`.

### P7-T06: Detector-placeholder collapse checker

```yaml
plan_task_id: "P7-T06"
task_type: "detector_placeholder_collapse_checker_support_only"
recommendation_ids: ["V18-R06", "V18-R04"]
role_family: "formalization-engineer@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: "Implement support-only checks for placeholder-as-detector-semantics collapse."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "support_formalization_no_proof_authority"
```

#### Required outputs

```text
scripts/research_control/support_formalization/detector_placeholder_collapse_checker.py
tests/test_detector_placeholder_collapse_checker.py
research_control/tasks/<task-id>/artifacts/detector_placeholder_collapse_checker_spec_v1.md
```

#### Done criteria

- The checker flags claims that `DetPlaceholder(E)` or source readout candidates imply adopted detector semantics.
- The checker distinguishes explicit placeholder/block, draft/control source-readout candidate, and adopted detector semantics.
- The next route is `P7-T07`.

### P7-T07: Support formalization traceability integration

```yaml
plan_task_id: "P7-T07"
task_type: "support_formalization_traceability_integration_v18"
recommendation_ids: ["V18-R06"]
role_family: "project-control-maintainer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Integrate v18 support formalization tools into traceability and proof-normal-form registries without proof authority."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "traceability_update_no_proof_authority"
```

#### Required outputs

```text
research_control/design/support_formalization_traceability_registry_v18.yaml
registries/PROOF_NORMAL_FORM_REGISTRY.csv
wiki/indexes/support_formalization_v18.md
```

#### Done criteria

- Every support tool has source artifact, test evidence, authority boundary, and forbidden-overread entry.
- The traceability registry says validators and executable specs are support-only.
- The next route is `P7-T08`.

### P7-T08: Support formalization Refuter review

```yaml
plan_task_id: "P7-T08"
task_type: "support_formalization_refuter_review_v18"
recommendation_ids: ["V18-R06"]
role_family: "refuter@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Stress v18 support formalization for proof-authority overread and false-confidence hazards."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "formalization_red_team_no_proof_authority"
```

#### Review questions

1. Does any checker imply proof authority?
2. Does any checker smuggle source-law adoption?
3. Does any checker hide missing mathematical burden?
4. Does any checker make false positives that block useful research?
5. Does any checker make false negatives that allow target import?

#### Done criteria

- Result is `pass`, `repair_required`, or `fail_closed`.
- If pass, next route is `P8-T01`.

---

## 13. Phase P8: Physics-payload ratio and route-orbit control

### P8 objective

Implement recommendation `V18-R07`: enforce a physics-payload ratio so the project uses its control system to drive hard theorem/countermodel work rather than indefinitely orbiting process tasks.

### P8-T01: Physics-payload ratio policy

```yaml
plan_task_id: "P8-T01"
task_type: "physics_payload_ratio_policy"
recommendation_ids: ["V18-R07"]
role_family: "project-control-maintainer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Define a policy requiring physics-bearing payloads after runs of project-system tasks."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "payload_ratio_policy_no_physics_delta"
```

#### Required output

```text
research_control/design/physics_payload_ratio_policy_v1.md
```

#### Policy seed

```yaml
physics_payload_ratio_policy:
  after_project_system_tasks: 3
  require_next_task_type_one_of:
    - theorem_candidate
    - countermodel
    - finite_witness
    - obstruction_with_proof_sketch
    - source_primitive_requirement
    - candidate_construction
  exceptions:
    - failing_ci
    - registry_corruption
    - claim_boundary_hard_failure
    - human_gate_required
    - security_or_integrity_repair
  initial_enforcement: "advisory"
```

#### Done criteria

- Policy defines process orbit and route orbit.
- Policy distinguishes helpful support work from avoidance behavior.
- The next route is `P8-T02`.

### P8-T02: Route-history and payload-ratio metrics extension

```yaml
plan_task_id: "P8-T02"
task_type: "route_history_payload_ratio_metrics"
recommendation_ids: ["V18-R07"]
role_family: "process-integrity-auditor@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Extend route-history metrics to compute project-system run length and physics-payload ratio."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "metrics_update_no_physics_delta"
```

#### Required outputs

```text
scripts/research_control/report_physics_progress_metrics.py
output/physics_progress_metrics.json
output/physics_progress_metrics.md
research_control/tasks/<task-id>/artifacts/payload_ratio_metrics_report_v1.md
```

#### Metrics

```yaml
new_metrics:
  - project_system_task_run_length
  - physics_bearing_task_run_length
  - new_mathematical_payload_count
  - theorem_countermodel_candidate_count
  - candidate_construction_count
  - support_only_task_count_since_last_physics_payload
  - route_orbit_warning_status
```

#### Done criteria

- Metrics are labeled AI-system diagnostics only.
- Metrics do not rank physics truth.
- The next route is `P8-T03`.

### P8-T03: Payload-ratio validator pilot

```yaml
plan_task_id: "P8-T03"
task_type: "physics_payload_ratio_validator_pilot"
recommendation_ids: ["V18-R07"]
role_family: "validator-engineer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Add advisory validation for payload-ratio policy."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "validator_update_no_physics_delta"
```

#### Required modifications

```text
scripts/research_control/validate_research_control.py
tests/test_physics_payload_ratio_policy.py
tests/fixtures/physics_payload_ratio/
```

#### Initial severity

```yaml
initial_findings:
  project_system_run_exceeds_threshold: "warn_current_control"
  physics_payload_missing_after_threshold: "warn_current_control"
  exception_declared_without_evidence: "warn_current_control"
  process_task_claims_physics_delta: "overclaim_hard_fail"
```

#### Done criteria

- Validator warnings are separate from hard overclaim failures.
- The policy does not block CI/security repair tasks.
- The next route is `P8-T04`.

### P8-T04: Payload-ratio dashboard integration

```yaml
plan_task_id: "P8-T04"
task_type: "physics_payload_ratio_dashboard_integration"
recommendation_ids: ["V18-R07"]
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Render payload-ratio metrics as support-only AI methodology diagnostics."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "dashboard_update_no_physics_delta"
```

#### Required outputs

```text
output/ai_methodology_metrics_dashboard.json
output/ai_methodology_metrics_dashboard.md
wiki/indexes/ai_methodology_metrics_dashboard.md
```

#### Done criteria

- Dashboard includes route-orbit warnings and payload-ratio diagnostics.
- Dashboard states that metrics do not establish physics truth.
- The next route is `P8-T05`.

### P8-T05: Payload-ratio red-team review

```yaml
plan_task_id: "P8-T05"
task_type: "physics_payload_ratio_red_team_review"
recommendation_ids: ["V18-R07"]
role_family: "external-red-team-reviewer@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Stress payload-ratio policy for false pressure, process overcorrection, and research distortion."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "payload_ratio_red_team_no_physics_delta"
```

#### Done criteria

- Review verifies that the policy encourages theorem/countermodel work without suppressing necessary repairs.
- If pass, next route is `P9-T01`.

---

## 14. Phase P9: Public cognitive-load reduction and status-card v2

### P9 objective

Implement recommendation `V18-R09`: reduce public cognitive load by extending positive-first status cards with an explicit next-burden field and by keeping public summaries short, exact, and non-promotional.

### P9-T01: Status-card v2 schema with next burden

```yaml
plan_task_id: "P9-T01"
task_type: "status_card_v2_schema_next_burden"
recommendation_ids: ["V18-R09"]
role_family: "schema-maintainer@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Extend status-card schema with next burden and public compression fields."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "schema_update_no_physics_delta"
```

#### Required outputs

```text
research_control/design/status_card_v2_schema.md
research_control/design/accepted_status_calibration_v2.yaml
research_control/design/distance_to_gr_status_aliases.yaml
```

#### Required status-card v2 fields

```yaml
status_card_v2:
  object_id: string
  positive_status: string
  exact_scope: string
  allowed_use: string
  blocked_overread: list[string]
  next_burden: string
  next_lawful_route: string
  public_summary: string
  full_control_non_conclusions: list[string]
```

#### Done criteria

- `next_burden` is required for high-risk rows.
- Existing positive-first order is preserved.
- The next route is `P9-T02`.

### P9-T02: Current-frontier and compact-frontier status-card v2 renderer

```yaml
plan_task_id: "P9-T02"
task_type: "status_card_v2_frontier_renderer"
recommendation_ids: ["V18-R09"]
role_family: "tooling-engineer@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Render status-card v2 in current frontier and compact frontier."
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

#### Rendering format

```markdown
**Positive status:** ...
**Scope:** ...
**Allowed use:** ...
**Blocked overread:** ...
**Next burden:** ...
```

#### Done criteria

- High-risk rows include next burden.
- Public-facing blocked lists remain concise.
- Full-control non-conclusion lists remain available in control surfaces.
- The next route is `P9-T03`.

### P9-T03: Public documentation cognitive-load calibration

```yaml
plan_task_id: "P9-T03"
task_type: "public_documentation_cognitive_load_calibration"
recommendation_ids: ["V18-R09"]
role_family: "documentation-curator@2.0.0"
target_derivation_milestone: "none"
milestone_burden: "Update public-facing pages to use concise status-card v2 summaries without changing claim status."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "documentation_update_no_physics_delta"
```

#### Candidate files

```text
README.md
github-facing/project-overview-explainer.md
github-facing/proof-state-dashboard-explainer.md
github-facing/source-authority-explainer.md
github-facing/aether-flow-physics-program-explainer.md
github-facing/aether-flow-ontology-explainer.md
github-facing/gr-derivation-roadmap-explainer.md
github-facing/claim-gates-explainer.md
github-facing/negative-results-and-obstructions-explainer.md
markdown/html-explainer-specs/*.md
markdown/publication-briefs/*.md
```

#### Documentation rules

- State positive scoped status first.
- State exact scope second.
- State blocked overread third.
- State next burden fourth.
- Avoid caveat walls that hide real scoped progress.
- Avoid public overclaims.
- Do not hand-edit generated HTML unless the established explainer pipeline requires regeneration.

#### Done criteria

- Public docs remain accurate.
- No public overclaim hard failures.
- Underclaim/caveat-wall warnings are resolved or justified.
- The next route is `P9-T04`.

### P9-T04: Status-card v2 linter tests

```yaml
plan_task_id: "P9-T04"
task_type: "status_card_v2_linter_tests"
recommendation_ids: ["V18-R09"]
role_family: "validator-engineer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Add linter tests for missing next-burden fields and caveat-wall public summaries."
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
tests/fixtures/claim_language/status_card_v2_valid.md
tests/fixtures/claim_language/status_card_v2_missing_next_burden.md
tests/fixtures/claim_language/status_card_v2_caveat_wall.md
```

#### Done criteria

- Missing next burden warns or fails according to configured surface.
- Caveat-wall summaries warn.
- Overclaims still hard-fail.
- The next route is `P9-T05`.

### P9-T05: Public cognitive-load red-team review

```yaml
plan_task_id: "P9-T05"
task_type: "public_cognitive_load_red_team_review"
recommendation_ids: ["V18-R09"]
role_family: "external-red-team-reviewer@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Review public and reader-facing status surfaces for overclaim, underclaim, and cognitive overload."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "reader_surface_red_team_no_physics_delta"
```

#### Review questions

1. Can a reader identify what exists?
2. Can a reader identify the exact scope?
3. Can a reader identify what does not follow?
4. Can a reader identify the next burden?
5. Does the page avoid both hype and caveat fog?
6. Does any generated surface appear authoritative when it is not?

#### Done criteria

- Review result is `pass`, `repair_required`, or `fail_closed`.
- If pass, next route is `P10-T01`.

---

## 15. Phase P10: Focused external-review packet preparation

### P10 objective

Implement recommendation `V18-R10`: prepare one focused external-review packet that asks a narrow question, with internal red-team review and no external outreach unless human-gated.

### P10-T01: External-review question selector

```yaml
plan_task_id: "P10-T01"
task_type: "external_review_question_selector_v18"
recommendation_ids: ["V18-R10", "V18-R01", "V18-R02", "V18-R03"]
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select one focused external-review question from v18 theorem/countermodel results."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "review_question_selected_no_outreach"
```

#### Default question

Unless P3 produced a more urgent result, default to:

```text
Does the proposed record-local EqSrc theorem have a valid path to family-level closure without adding a primitive equivalent to the missing structure?
```

#### Allowed question families

```yaml
allowed_question_families:
  - EqSrc_family_closure
  - RetainH_primitive_requirement
  - GenH_primitive_requirement
  - source_detector_readout_semantics
  - finite_toy_response_v2_tag_independence
```

#### Done criteria

- Exactly one review question is selected.
- No external outreach is performed.
- The next route is `P10-T02`.

### P10-T02: External-review packet source spec

```yaml
plan_task_id: "P10-T02"
task_type: "external_review_packet_source_spec"
recommendation_ids: ["V18-R10"]
role_family: "documentation-curator@2.0.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Write a source spec for one focused external-review packet."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "review_packet_spec_no_outreach"
```

#### Required output

```text
markdown/external-review-specs/eqsrc_family_closure_review_packet_spec_v1.md
```

#### Required sections

1. Review question.
2. What the project is not claiming.
3. Minimal definitions.
4. Record-local theorem summary.
5. Typed source-equivalence object summary.
6. Family-closure obstruction.
7. `RetainH` and `GenH` boundary.
8. What feedback is requested.
9. What feedback is not requested.
10. Source paths.
11. Non-authority and non-endorsement statement.

#### Done criteria

- Source spec is concise enough for external review.
- It does not ask the reviewer to inspect the whole repository.
- The next route is `P10-T03`.

### P10-T03: External-review packet artifact

```yaml
plan_task_id: "P10-T03"
task_type: "external_review_packet_artifact"
recommendation_ids: ["V18-R10"]
role_family: "documentation-curator@2.0.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Generate the focused external-review packet from tracked source spec."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "review_packet_created_no_outreach"
```

#### Required outputs

```text
external_review_packets/eqsrc_family_closure_review_packet_v1.md
registries/EXTERNAL_REVIEW_PACKET_REGISTRY.csv
```

#### Packet constraints

- Target length: 2 to 5 pages in Markdown equivalent.
- No broad repository tour.
- No hype.
- No external-reviewer naming.
- No outreach message.
- No claim that the packet was reviewed externally.
- No claim that external acceptance would prove the physics.

#### Done criteria

- Packet is registered.
- Packet is source-backed.
- The next route is `P10-T04`.

### P10-T04: Internal red-team review of external packet

```yaml
plan_task_id: "P10-T04"
task_type: "external_review_packet_internal_red_team"
recommendation_ids: ["V18-R10"]
role_family: "external-red-team-reviewer@0.1.0"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Internally stress the external-review packet for overclaim, ambiguity, and reviewer burden."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "internal_red_team_no_outreach"
```

#### Review questions

1. Is the question sharp enough?
2. Does the packet hide the main obstruction?
3. Does the packet overclaim scoped objects?
4. Does the packet underclaim useful progress?
5. Could the reviewer answer without reading the whole repo?
6. Does the packet imply external endorsement?
7. Does the packet preserve no-outreach-by-default?

#### Required output

```text
research_control/tasks/<task-id>/artifacts/external_review_packet_internal_red_team_v1.md
```

#### Done criteria

- Result is `pass`, `repair_required`, or `fail_closed`.
- If pass, next route is `P10-T05`.

### P10-T05: External-outreach human-gate setup only

```yaml
plan_task_id: "P10-T05"
task_type: "external_outreach_human_gate_setup_only"
recommendation_ids: ["V18-R10"]
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "none"
milestone_burden: "Prepare a human-gate question for possible future external outreach without sending anything."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "human_gate_setup_no_outreach"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/external_outreach_human_gate_question_v1.yaml
```

#### Required fields

```yaml
external_outreach_human_gate_question:
  packet_path: "external_review_packets/eqsrc_family_closure_review_packet_v1.md"
  proposed_outreach: "not_executed"
  external_outreach_authorized_in_this_task: false
  human_gate_required_for_future_outreach: true
  external_feedback_as_proof_authority: false
```

#### Done criteria

- Human-gate setup exists.
- No external message is sent.
- No reviewer is named unless already human-provided in a later gate.
- The next route is `P10-T06`.

### P10-T06: Review-response intake template

```yaml
plan_task_id: "P10-T06"
task_type: "external_review_response_intake_template"
recommendation_ids: ["V18-R10"]
role_family: "process-integrity-auditor@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Create a template for future external-review responses without treating them as proof authority."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "response_intake_template_no_outreach"
```

#### Required output

```text
research_control/design/external_review_response_intake_template_v1.md
```

#### Template fields

```yaml
external_review_response_intake:
  reviewer_identity_publication_allowed: false
  response_received_at: string
  response_summary: string
  theorem_issue_identified: list[string]
  countermodel_issue_identified: list[string]
  terminology_issue_identified: list[string]
  overclaim_risk_identified: list[string]
  action_recommendation:
    - repair
    - refuter_stress
    - theorem_rewrite
    - freeze_review
    - no_action
  proof_authority: false
  benchmark_authority: false
  endorsement_claim_authorized: false
```

#### Done criteria

- Template exists.
- No outreach is performed.
- If pass, next route is `P11-T01`.

---

## 16. Phase P11: V18 integration, final validation, frontier sync, and ordinary handoff

### P11 objective

Integrate v18 outputs, verify recommendation coverage, synchronize generated surfaces, and select exactly one ordinary continuation route from validated v18 outputs.

### P11-T01: V18 integration report

```yaml
plan_task_id: "P11-T01"
task_type: "v18_integration_report"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "none"
milestone_burden: "Integrate all v18 phase outputs into one control report without physics promotion."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "v18_integration_no_promotion"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/v18_integration_report.md
```

#### Required sections

1. Implemented tasks.
2. Deferred tasks.
3. Recommendation coverage table.
4. EqSrc typed-object status.
5. EqSrc family theorem/countermodel status.
6. Countermodel obligation status.
7. Source detector/readout status.
8. Finite toy response v2 status.
9. Support formalization status.
10. Payload-ratio policy status.
11. Active-state bifurcation status.
12. Public status-card v2 status.
13. External-review packet status.
14. Distance-to-GR effect.
15. Remaining blocked claims.
16. Candidate ordinary route families.
17. Next validation route.

#### Done criteria

- Every v18 recommendation has implemented, deferred, blocked, or superseded status.
- No Distance-to-GR ledger promotion is claimed unless separately authorized.
- The next route is `P11-T02`.

### P11-T02: V18 final validation packet

```yaml
plan_task_id: "P11-T02"
task_type: "v18_final_validation_packet"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "validator-engineer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Run final v18 validation layers and record exact pending reasons if any."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "v18_final_validation_no_promotion"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/v18_final_validation_report.json
```

#### Required validation layers

```yaml
validation_layers:
  - research_control_validation
  - research_control_diff_validation
  - claim_language_changed
  - documentation_impact
  - memory_bootstrap_validate_only
  - current_frontier_render_check
  - compact_frontier_render_check
  - task_index_render_check
  - dependency_graph_check
  - claim_graph_validation
  - ai_methodology_dashboard_check
  - source_equivalence_object_registry_validation
  - countermodel_obligation_registry_validation
  - metric_use_ledger_tex_validator_if_integrated
  - support_formalization_tests
  - full_research_control_validation
  - git_diff_check
```

#### Done criteria

- Report lists pass/fail for every layer.
- Any pending hard failure routes to repair.
- If all required layers pass, next route is `P11-T03`.

### P11-T03: Current frontier, compact frontier, graphs, and ledger synchronization

```yaml
plan_task_id: "P11-T03"
task_type: "v18_current_frontier_ledger_sync"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "project-control-maintainer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Synchronize current frontier, compact frontier, graphs, and ledgers after v18 final validation."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "frontier_sync_no_promotion"
```

#### Required outputs

```text
research_control/current_frontier.md
output/compact_current_frontier_v16.yaml
output/compact_current_frontier_v16.json
output/claim_graph_v1.json
output/research_dependency_graph.json
wiki/indexes/research_dependency_graph.md
research_control/tasks/<task-id>/artifacts/v18_current_frontier_ledger_sync_report.json
```

#### Required sync checks

- Frontier displays active-state bifurcation.
- Frontier displays status-card v2 next burden.
- Frontier displays latest EqSrc family closure status.
- Frontier displays source detector/readout status as proposal/candidate/obstruction only.
- Frontier displays finite toy response v2 status.
- Frontier displays support formalization as support-only.
- Frontier displays payload-ratio diagnostics as AI methodology only.
- Distance-to-GR ledger hashes are recorded.
- Ledger rows are unchanged unless a protected ledger-update task exists.

#### Done criteria

- All render checks pass.
- No generated surface promotes physics claims.
- The next route is `P11-T04`.

### P11-T04: V18 ordinary continuation handoff

```yaml
plan_task_id: "P11-T04"
task_type: "v18_ordinary_continuation_handoff"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "director-of-research@0.3.0"
target_derivation_milestone: "none"
milestone_burden: "Complete v18 by selecting exactly one ordinary continuation route from validated v18 outputs."
continue_research_required: true
requires_human_gate: false
physics_progress_status: "v18_completed_ordinary_continuation_selected"
```

#### Allowed ordinary continuation route families

```yaml
allowed_ordinary_continuation_routes:
  - EqSrc_family_closure_repair_or_stress
  - RetainH_definition_candidate_packet
  - GenH_definition_candidate_packet
  - source_detector_readout_candidate_repair
  - source_detector_readout_freeze_review
  - finite_toy_response_v2_repair_or_freeze
  - support_formalization_expansion_next_checker
  - external_review_human_gate_request
  - matter_coupling_candidate_repair_with_readout
  - project_system_repair_from_v18_validation
  - scoped_obstruction_freeze_review
```

#### Disallowed routes

```yaml
disallowed_routes:
  - general_EqSrc_adoption_without_gate
  - RetainH_adoption_without_gate
  - GenH_adoption_without_gate
  - detector_semantics_adoption
  - coupling_law_adoption
  - matter_coupling_derivation
  - stress_energy_tensor_construction_without_semantics
  - matter_action_construction_without_dynamics_route
  - Einstein_equation_derivation
  - benchmark_promotion
  - completed_derivation_claim
  - external_outreach_without_human_gate
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/v18_ordinary_continuation_handoff_report.json
research_control/handoffs/handoff-<next>.yaml
research_control/handoffs/handoff-<next>.md
research_control/program_state.yaml
```

#### Done criteria

- Exactly one ordinary continuation route is selected.
- All v18 plan tasks are implemented, deferred with reason, blocked with reason, or superseded by DDR.
- The handoff states no physics promotion unless protected authority exists.
- The next route is concrete and bounded.

### P11-T05: V18 recommendation coverage audit

```yaml
plan_task_id: "P11-T05"
task_type: "v18_recommendation_coverage_audit"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "process-integrity-auditor@0.1.0"
target_derivation_milestone: "none"
milestone_burden: "Audit coverage of all v18 recommendations and identify any project-improvement signals."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "coverage_audit_no_promotion"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/v18_recommendation_coverage_audit.md
```

#### Done criteria

- Every recommendation has final coverage status.
- Missing or partial recommendations become project-improvement signals.
- No coverage count is treated as physics proof.
- The next route is `P11-T06` if project-system signals exist, otherwise the ordinary handoff route selected by `P11-T04`.

### P11-T06: Project-improvement signal bridge if needed

```yaml
plan_task_id: "P11-T06"
task_type: "v18_project_improvement_signal_bridge"
recommendation_ids: ["V18-R01", "V18-R02", "V18-R03", "V18-R04", "V18-R05", "V18-R06", "V18-R07", "V18-R08", "V18-R09", "V18-R10"]
role_family: "project-control-maintainer@0.2.0"
target_derivation_milestone: "none"
milestone_burden: "Account for v18 project-improvement signals without physics promotion."
continue_research_required: true
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
physics_progress_status: "project_improvement_bridge_no_promotion"
```

#### Required output

```text
research_control/tasks/<task-id>/artifacts/v18_project_improvement_signal_bridge.yaml
```

#### Done criteria

- Any validation, documentation, memory, or renderer follow-up is routed as project-system work.
- The bridge does not override the ordinary scientific handoff.
- If no bridge is required, the completion says so.

---

## 17. Final v18 success criteria

V18 is complete only when all of the following hold:

```yaml
v18_success_criteria:
  plan_registered: true
  backlog_materialized: true
  active_state_bifurcation_implemented: true
  typed_source_equivalence_object_defined: true
  EqSrc_family_closure_theorem_or_countermodel_attempted: true
  countermodel_obligation_system_implemented: true
  source_detector_readout_burden_defined: true
  source_detector_readout_candidate_or_obstruction_attempted: true
  finite_toy_response_v2_attempted: true
  support_formalization_expanded: true
  physics_payload_ratio_policy_implemented: true
  status_card_v2_public_cognitive_load_reduction_implemented: true
  external_review_packet_prepared_no_outreach: true
  v18_integration_report_complete: true
  v18_final_validation_passed_or_repair_routed: true
  v18_ordinary_handoff_selected_exactly_one_route: true
  distance_to_gr_promotion_without_gate: false
  external_outreach_without_gate: false
  completed_derivation_claim: false
```

## 18. Default next scientific preference after v18

If v18 completes without a protected ledger promotion and without a freeze condition, the default scientific preference should be selected by `P11-T04` from validated outputs. The preferred route ordering is:

1. Repair or stress the strongest surviving `EqSrc` family-closure theorem/countermodel result.
2. If `RetainH` is required, run a bounded `RetainH` definition-candidate or countermodel packet.
3. If `GenH` is required, run a bounded `GenH` definition-candidate or countermodel packet.
4. If source detector/readout candidate survived audit/stress, integrate it into a repaired `K_E` coupling-law candidate.
5. If finite toy response v2 survived, use it only as toy-model evidence for source-response pattern construction.
6. If external review packet is ready and human authorization exists, route a human-gated external-outreach packet.
7. If repeated burdens persist without new mathematical payload, route a scoped freeze review.

No route may skip to matter-coupling adoption, Einstein equations, benchmark promotion, or completed derivation.

## 19. Canonical forbidden-conclusion summary for all v18 tasks

Every v18 completion should include or reference this summary:

```text
This v18 task does not authorize canonical ontology edit, source-law adoption,
general EqSrc discharge, RetainH adoption, GenH adoption, MetricData(E)
adoption, g_eff scope expansion, physical metric authority, detector semantics
adoption, source detector/readout semantics adoption unless separately
human-gated, coupling-law adoption, matter-coupling derivation or adoption,
stress-energy semantics, stress-energy tensor, matter action, Einstein-equation
derivation, benchmark promotion, Gate Chair verdict, external outreach without
human authorization, completed derivation, future source-extension impossibility,
program-wide no-go conclusion, or generated derivative, validator, registry,
role, handoff, local cache, checkpoint, commit, CI status, or current-frontier
rendering as scientific proof.
```

## 20. Appendix: Minimal task completion receipt fields for v18

Every v18 completion receipt should include:

```yaml
completion_id: string
job_id: string
task_id: string
source_role_id: string
completed_at: string
status: "completed | blocked | failed_closed | superseded"
implementation_plan_receipt:
  plan_id: "recommendations_implementation_plan_continue_task-v18"
  plan_path: "implementations_plans/recommendations_implementation_plan_continue_task-v18.md"
  related_plan_task_id: string
  recommendation_ids: list[string]
  implemented_task_scope: string
output_paths: list[string]
validation_status: "PASS | FAIL | PARTIAL"
validation_layers:
  pre_execution: object
  implementation: object
  task_local_validator: object
  post_write: object
  renderer: object
  memory_bootstrap: object
  claim_language_linter: object
  full_research_control_validation: object
physics_progress_status:
  status: string
  physics_promotion_authorized: false
distance_to_gr_delta:
  effect: string
  changed: false
  ledger_row_updated: false
new_mathematical_payload: list[object]
mathematical_payload_manifest: list[object]
recommendation_coverage:
  source_plan_id: "recommendations_implementation_plan_continue_task-v18"
  source_recommendation_ids: list[string]
  implements_plan_task_id: string
  implementation_status: string
  coverage_effect: string
claim_boundary:
  allowed_claims: list[string]
  forbidden_claims: list[string]
authorization_layers:
  protected_gate_review_authorized: false
  benchmark_promotion_authorized: false
  completed_derivation_authorized: false
  external_outreach_authorized: false
project_improvement_signals: list[object]
coherent_resolution_summary: string
next_recommendation: string
```
