<!-- authority: implementation_plan -->

# Recommendations Implementation Plan for `/continue-research`, v13

**Filename:** `recommendations_implementation_plan_continue_task-v13.md`  
**Intended repository path:** `implementations_plans/recommendations_implementation_plan_continue_task-v13.md`  
**Generated date:** 2026-07-01  
**Plan ID:** `recommendations_implementation_plan_continue_task-v13`  
**Implementation driver:** Continue Research functionality only  
**Primary implementation lane:** `research_control/` bounded transactions  
**Plan status:** implementation guidance, not physics authority  
**Scope:** Integrate the recommendations from the external project analysis section titled **"8. Recommendations"** into the AEther-Flow project, using one bounded Continue Research transaction per task.

---

## 0. Executive Implementation Intent

This v13 implementation plan converts the external recommendations into a sequence of bounded local AI-agent tasks. Every phase and task in this plan must be implemented through the repository's **Continue Research** functionality. No phase in this plan is a manual-edit permission slip, no phase is a Gate Chair verdict, and no phase authorizes physics promotion.

The plan has three intertwined goals:

1. **Make real scoped wins louder and cleaner.**  
   The project has genuine scoped milestones, especially source-only `M_src`, scoped source-extension `g_eff`, and matter-coupling-adjacent evidence/precondition results. These should not be linguistically flattened into vague caution.

2. **Keep downstream physical claims locked behind gates.**  
   The project has not derived universal matter coupling, stress-energy semantics, matter action, Einstein equations, exact-GR benchmark recovery, or completed GR derivation.

3. **Improve the agent system so it expresses the distinction reliably.**  
   Local agents must learn to say exactly what was achieved, exactly what remains blocked, and exactly which route is next.

The current assumed repository frontier is post-`RT-20260701-002` and post-`handoff-0411`. The active milestone is `matter_coupling`. The immediate recommended scientific continuation is one bounded Refuter stress test of `SourceMatterSemanticsAdoptionReadinessLaw_v1`, before any selector, Gate Chair, matter-semantics adoption, detector-semantics adoption, coupling-law adoption, matter-coupling derivation, Einstein-equation route, benchmark route, or promotion route.

This plan must be adapted if the local repository has advanced. Local agents must verify `research_control/program_state.yaml`, the latest handoff, `research_control/current_frontier.md`, and `registries/DISTANCE_TO_GR_LEDGER.csv` before routing any task.

---

## 1. Non-Authority Warning

This file is an implementation plan. It is not:

- a physics proof;
- a canonical ontology edit;
- a source-law adoption;
- a Gate Chair verdict;
- a benchmark-promotion authority;
- completed-derivation evidence;
- a substitute for registered `.tex` sources or registries;
- a substitute for the active `program_state.yaml` and latest handoff;
- permission to bypass Continue Research;
- permission to bypass human-gated authority.

The plan may instruct agents to create, update, or validate project-control artifacts, documentation, validators, role contracts, and scientific draft/control artifacts. Those changes become repository state only through bounded Continue Research transactions and the normal checkpoint path.

---

## 2. Source Basis and Required Starting-State Verification

### 2.1 Required sources to inspect before P0

Before executing P0, the local Director of Research must inspect the current tracked state from at least:

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `research_control/program_state.yaml`
- `research_control/current_frontier.md`
- latest handoff named in `research_control/program_state.yaml`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `research_control/design/gr_derivation_burden_map.md`
- `research_control/design/mathematical_decisiveness_completion_contract.md`
- `research_control/tasks/RT-20260614-134/00_TASK.yaml`
- `research_control/tasks/RT-20260614-222/00_TASK.yaml`
- `research_control/tasks/RT-20260630-056/00_TASK.yaml`
- `research_control/tasks/RT-20260630-057/00_TASK.yaml`
- `research_control/tasks/RT-20260701-001/00_TASK.yaml`
- `research_control/tasks/RT-20260701-002/00_TASK.yaml`
- `research_control/tasks/RT-20260701-002/artifacts/source_matter_semantics_adoption_readiness_law_smuggling_audit_v1.tex`
- `research_control/handoffs/handoff-0411.yaml`
- `research_control/handoffs/handoff-0411.md`
- `implementations_plans/recommendations_implementation_plan_continue_task-v12.md`
- shared `previous_conversation.md`, if present in the local working context.

### 2.2 Assumed current state

This plan assumes the following active state at generation time:

| Field | Assumed value |
|---|---|
| Active task | `RT-20260701-002` |
| Latest handoff | `handoff-0411` |
| Current route family | `v12_p7_t03_source_matter_semantics_adoption_readiness_law_audit_routes_to_stress_no_promotion` |
| Active milestone | `matter_coupling` |
| Latest scientific status | `SourceMatterSemanticsAdoptionReadinessLaw_v1` audited source-pure as written pending Refuter stress |
| Immediate next scientific route | bounded `refuter@0.2.0` stress packet |
| Physics promotion authorized | false |
| Gate Chair verdict active for next task | false |
| Universal matter coupling derived | false |
| Einstein equations derived | false |
| Exact-GR benchmark promoted | false |
| Completed derivation claimed | false |

If any of these assumptions are stale, P0 must adapt the plan before executing later phases.

### 2.3 Current scoped claims that must be preserved

The local agents must preserve these exact scoped-positive statements:

#### `M_src`

`M_src` is Gate-Chair adopted as full source-only `M_src` under H1-H13 and fail-closed obstruction discipline. This is a real source-manifold milestone discharge. It is not a target smooth manifold, not a metric structure, and not a GR derivation.

#### `g_eff`

`g_eff^{GSC-cand}(E;G^beta,T_src(E))` is Gate-Chair adopted only as a scoped source-extension `g_eff` object. This is a real Distance-to-GR status change for the effective-metric burden. It is not an unscoped Lorentzian metric, not canonical source law, not `MetricData(E)` adoption, not matter coupling, and not Einstein-equation evidence.

#### `matter_coupling`

`MSStableMatterSemanticsBridge_v1(E;B_current)` is Gate-Chair accepted only as scoped source-extension stable matter-semantics bridge evidence/precondition. The current continuation target is `SourceMatterSemanticsAdoptionReadinessLaw_v1`, a proposal-only readiness-law target audited source-pure as written pending Refuter stress. Universal matter coupling is not derived or adopted.

---

## 3. Source Recommendation Map

The recommendations from the external analysis are mapped here as `R1` through `R14`.

| Recommendation ID | Recommendation | Main phases | Primary output type | Physics promotion allowed |
|---|---|---|---|---|
| `R1` | Stop using bare `accepted`. | P1, P8, P14 | status vocabulary, validators, docs | No |
| `R2` | Make `SourceMatterSemanticsAdoptionReadinessLaw_v1` stress the immediate research priority. | P2 | physics AgentJob, stress artifact | No automatic promotion |
| `R3` | After stress, route a selector, not a leap to matter coupling. | P3 | route rule, selector task | No |
| `R4` | Build positive source-side matter semantics, not only anti-smuggling guards. | P4 | physics law-target/candidate/audit/stress chain | No automatic promotion |
| `R5` | Treat `RR_E` as a mathematical fault line. | P5 | theorem/obstruction route | No automatic promotion |
| `R6` | Add a claim-language linter. | P6 | validator/tooling/tests | No |
| `R7` | Reconcile validation-status drift. | P7 | schema/renderers/handoffs | No |
| `R8` | Keep the status-layer split and make it public-facing. | P8 | public status tables/docs | No |
| `R9` | Add a three-tier claim convention to all summaries. | P9 | templates, completion contracts | No |
| `R10` | Create a compact frontier theorem inventory. | P10 | registered inventory source | No |
| `R11` | Build support-only formalization, without proof authority. | P11 | typed schemas/formal skeletons/tests | No |
| `R12` | Prepare an external red-team packet. | P12 | role contract, review packet, pilot | No |
| `R13` | Freeze repeated route orbits earlier. | P13 | route-cycle validator, freeze taxonomy | No |
| `R14` | Update local AI instructions with exact replacement wording. | P14 | prompts, skill guidance, examples | No |
| `R15` | Add literature comparison and final audit. | P15, P16 | comparison packet, integration audit | No |

`R15` is included because the external analysis recommended external comparison and final integration audit as part of the next-best implementation path.

---

## 4. Universal Continue Research Protocol

Every task in this plan is one bounded `/continue-research` transaction unless the task explicitly says it is a read-only verification packet. Even read-only verification packets must be initiated through Continue Research if they are part of this plan.

### 4.1 Pre-routing commands

Before every task-routing decision, run:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "<task-specific targeted phrase>" --limit 10 --json
.venv/bin/python scripts/research_control/continue_research.py --json
```

If memory search returns relevant objects, inspect the canonical source files or registry rows named by the hits. Memory, wiki notes, semantic extracts, Obsidian notes, SQLite indexes, PDFs, generated HTML, and `.local/` caches are retrieval aids only. They do not override tracked source files or registries.

### 4.2 Director behavior

For every task:

1. Use the Director of Research as the routing authority.
2. Create exactly one Director Decision Record unless a valid active DDR already exists for the exact task.
3. Create exactly one outer AgentJob.
4. Choose the narrowest role that can complete the task.
5. Preserve active claim boundaries.
6. Use `parent_child_parallel_synthesis` for physics AgentJobs governed by the post-2026-06-17 physics contract.
7. For physics tasks, declare `target_derivation_milestone` and `milestone_burden` from the burden map.
8. For physics completions, include a new mathematical payload.
9. For project-system tasks, state explicitly that the task changes control/tooling/documentation only and does not promote physics claims.
10. Do not route Gate Chair work unless exact tracked human authorization exists.
11. If exact Gate Chair authorization is missing, route a non-promotional selector/control packet or human-gated handoff.
12. If a task discovers project-improvement signals, preserve the normal research handoff and create a project-improvement handoff sidecar only as allowed by repository governance.
13. Do not implement multiple plan tasks in a single AgentJob.
14. Do not silently skip a task. If it is already implemented, create a bounded verification/adaptation task or mark it completed by source evidence.

### 4.3 Required post-execution validation commands

After any state-changing task, run the validation suite appropriate to the changed scope. The default suite is:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/project_control/classify_project_changes.py --json
.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py
.venv/bin/python scripts/research_control/render_current_frontier.py --check
git diff --check
```

Add task-specific tests when changing scripts, validators, schemas, renderers, role contracts, prompts, or formalization tooling:

```zsh
.venv/bin/python -m unittest discover -s tests
```

If any validation fails, do not checkpoint. Repair through the same bounded AgentJob if inside scope; otherwise route a separate bounded repair task.

### 4.4 Required checkpoint path

Checkpoint only through:

```zsh
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py
```

Do not stage or commit manually when the checkpoint script is the required control path.

### 4.5 Completion fields for physics tasks

Every physics task in this plan must include:

- `physics_progress_status`
- `distance_to_gr_delta`
- `distance_to_gr_status`
- `mathematical_payload_manifest`
- `forbidden_conclusion_summary`
- `parent_child_synthesis`
- `freeze_criteria_status` when a burden repeats or an obstruction is produced
- `route_cycle_control` when the task is part of a constructor/audit/stress/selector cycle
- `candidate_constructor_result` for Candidate Constructor tasks
- `theoretical_decision_output` for Theoretical Continuation Selector tasks
- `obstruction_record` when a precise obstruction or freeze is produced
- `source_extension_category` when source-extension data are introduced, audited, stress-tested, accepted, rejected, minimized, or classified.

### 4.6 Completion fields for project-system tasks

Every non-physics project-system task in this plan must include:

- `project_system_scope`
- `physics_promotion_authorized: false`
- `scientific_claims_changed: false`
- `documentation_impact`
- `changed_files`
- `validation_status`
- `tests_added_or_updated`
- `forbidden_conclusion_summary`
- `rollback_or_repair_notes`
- `next_recommended_action`

---

## 5. Universal Forbidden Conclusions

Unless an exact protected authority packet explicitly grants a narrower conclusion, every task must preserve:

- no canonical ontology edit;
- no source-law adoption;
- no `MetricData(E)` adoption;
- no unscoped `g_eff` adoption;
- no `g_eff` scope expansion;
- no coupling-law adoption;
- no matter-semantics adoption;
- no detector-semantics adoption;
- no matter-coupling derivation;
- no matter-coupling adoption;
- no stress-energy semantics;
- no stress-energy tensor;
- no matter action;
- no Einstein equations;
- no exact-GR benchmark promotion;
- no benchmark Gate Chair closure;
- no completed derivation;
- no future source-extension impossibility;
- no global theory rejection;
- no validator, role, registry, handoff, approval, generated derivative, local cache, file order, or commit status as scientific proof.

---

## 6. Phase Overview

| Phase | Theme | Main recommendation IDs | Task count | Main route type |
|---|---|---:|---:|---|
| P0 | Plan intake and baseline reconciliation | all | 4 | control |
| P1 | Scoped-positive claim vocabulary | R1, R8, R14 | 5 | control/docs |
| P2 | Immediate frontier stress | R2 | 3 | physics |
| P3 | Post-stress selector and no-leap rule | R3, R13 | 4 | physics/control |
| P4 | Positive source-side matter semantics | R4 | 6 | physics |
| P5 | `RR_E` theorem or obstruction program | R5 | 6 | physics |
| P6 | Claim-language linter | R6 | 5 | tooling/control |
| P7 | Validation-status reconciliation | R7 | 5 | tooling/control |
| P8 | Public status-layer propagation | R8 | 5 | docs/control |
| P9 | Three-tier claim convention | R9 | 4 | control/docs |
| P10 | Frontier theorem inventory | R10 | 5 | control/science-facing |
| P11 | Support-only formalization lane | R11 | 6 | tooling/support |
| P12 | External red-team mode | R12 | 5 | review/control |
| P13 | Route-orbit freeze hardening | R13 | 5 | tooling/control |
| P14 | Local AI wording integration | R14 | 5 | prompts/docs/tests |
| P15 | Literature comparison | R15 | 4 | review/literature |
| P16 | Final integration audit and handoff | all | 5 | audit/control |

Total planned tasks: 78.

---

# Phase P0: Plan Intake and Baseline Reconciliation

## P0 Objective

Register this v13 implementation plan as the current recommendations implementation plan, reconcile it against the live tracked repository state, and prevent stale replay of v12 or pre-`RT-20260701-002` instructions.

## P0-T01: Plan intake transaction

**Task ID suggestion:** `post_v13_p0_t01_plan_intake`  
**Task type:** `implementation_plan_intake_control_packet`  
**Role family:** `documentation-curator@0.1.0` or `director-of-research` routed control role  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Add or verify `implementations_plans/recommendations_implementation_plan_continue_task-v13.md` as the tracked v13 implementation plan.

### Required actions

1. Verify whether the file already exists.
2. If missing, add this plan to `implementations_plans/`.
3. Register the Markdown source if repository policy requires a registry row.
4. Create a task-local plan-intake note explaining that v13 is implementation guidance only.
5. Confirm that v13 does not overwrite v12 historical evidence.
6. Create a handoff that points to P0-T02.

### Required outputs

- `implementations_plans/recommendations_implementation_plan_continue_task-v13.md`
- task-local `00_TASK.yaml`
- task-local DDR
- AgentJob contract
- completion receipt
- documentation impact receipt
- updated registry rows, if required
- handoff to P0-T02

### Acceptance criteria

- The v13 plan exists at the intended path.
- It is discoverable by the memory system after bootstrap.
- It is not registered as physics authority.
- It does not claim any scientific result.
- Validations pass.

### Forbidden conclusions

No physics claim changes. No route promotion. No Gate Chair authority.

---

## P0-T02: Live baseline reconciliation

**Task ID suggestion:** `post_v13_p0_t02_live_baseline_reconciliation`  
**Task type:** `active_state_reconciliation_control_packet`  
**Role family:** `theoretical-continuation-selector@0.1.0` for physics-aware state classification, or control role if no physics route is selected  
**Continue Research required:** yes  
**Physics task:** no, unless the Director determines the active handoff requires a physics selector  
**Objective:** Determine the exact live baseline before executing v13 phases.

### Required actions

1. Inspect `research_control/program_state.yaml`.
2. Inspect latest handoff named by `program_state.yaml`.
3. Inspect `research_control/current_frontier.md`.
4. Inspect `registries/DISTANCE_TO_GR_LEDGER.csv`.
5. Inspect the latest active task folder.
6. Compare live state against this plan’s assumed state.
7. Produce a baseline reconciliation artifact with one of these verdicts:

   - `v13_baseline_matches_assumption`
   - `v13_baseline_advanced_adapt_plan`
   - `v13_baseline_conflict_requires_repair`
   - `v13_baseline_human_gate_required`

### Required outputs

- `research_control/tasks/<task_id>/artifacts/v13_baseline_reconciliation.md`
- handoff to P0-T03 or repair/human-gated handoff
- documentation impact receipt

### Acceptance criteria

- The active task and latest handoff are identified.
- The current immediate next action is identified.
- Already completed v12 or v13-equivalent work is not scheduled for replay.
- If the active state advanced past `RT-20260701-002`, later phases are marked for adaptation.

### Forbidden conclusions

No claim that v13 changes physics state. No claim that baseline inspection itself advances `matter_coupling`.

---

## P0-T03: Recommendation trace matrix

**Task ID suggestion:** `post_v13_p0_t03_recommendation_trace_matrix`  
**Task type:** `recommendation_traceability_control_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Create a trace matrix linking each v13 recommendation to phases, tasks, outputs, validators, and claim boundaries.

### Required actions

1. Create a task-local `v13_recommendation_trace_matrix.csv` or Markdown table.
2. Include columns:

   - recommendation ID;
   - summary;
   - phase;
   - task IDs;
   - task type;
   - required role;
   - expected artifacts;
   - physics milestone affected;
   - promotion allowed;
   - validators;
   - status;
   - dependency.

3. Record that the trace matrix is a control aid only.
4. Hand off to P0-T04.

### Required outputs

- trace matrix artifact
- registry updates if project policy requires them
- updated handoff

### Acceptance criteria

- Every recommendation in Section 3 maps to at least one task.
- Every task maps to at least one recommendation.
- No task is orphaned.
- The matrix can be updated as phases complete.

---

## P0-T04: V13 execution gate

**Task ID suggestion:** `post_v13_p0_t04_execution_gate`  
**Task type:** `plan_execution_gate_control_packet`  
**Role family:** `director-of-research`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Confirm that v13 may proceed to P1 and P2 without bypassing the live active handoff.

### Required actions

1. Read P0-T02 and P0-T03 artifacts.
2. Determine whether P1 and P2 can start in parallel or must be serialized.
3. If active scientific route is unchanged, select P2-T01 as the next physics continuation.
4. If public/status/tooling route is safer first, select P1-T01.
5. Record explicit no-promotion boundary.

### Required outputs

- `v13_execution_gate.yaml`
- handoff to selected next task

### Acceptance criteria

- Exactly one next task is selected.
- No phase is treated as globally authorized all at once.
- Continue Research remains the implementation driver.

---

# Phase P1: Scoped-Positive Claim Vocabulary

## P1 Objective

Stop local agents and public docs from using bare `accepted` in high-risk contexts. Introduce status phrases that say the positive scoped result first and the blocked downstream claims second.

---

## P1-T01: Scoped-positive claim vocabulary control note

**Task ID suggestion:** `post_v13_p1_t01_scoped_positive_claim_vocabulary`  
**Task type:** `claim_language_control_note`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Create a canonical control note defining allowed high-risk status language for `M_src`, `g_eff`, `matter_coupling`, `SourceMatterSemanticsAdoptionReadinessLaw_v1`, and future scoped evidence/precondition results.

### Required content

The note must define:

- `adopted_as_source_only_object`
- `adopted_as_scoped_source_extension_object`
- `accepted_as_scoped_evidence_precondition`
- `proposal_only_law_target`
- `source_pure_pending_stress`
- `stress_survived_pending_selector`
- `human_gated_evidence_review_required`
- `blocked_adoption_open_continuation`
- `frozen_negative_no_global_rejection`

### Required exact phrase entries

For `M_src`:

```text
M_src is Gate-Chair adopted as full source-only M_src under H1-H13 and fail-closed obstruction discipline. This is a real source-manifold milestone discharge. It is not a target smooth manifold, not a metric structure, and not a GR derivation.
```

For `g_eff`:

```text
g_eff^{GSC-cand}(E;G^beta,T_src(E)) is Gate-Chair adopted only as a scoped source-extension g_eff object. This is a real Distance-to-GR status change for the effective-metric burden. It is not an unscoped Lorentzian metric, not canonical source law, not MetricData(E) adoption, not matter coupling, and not Einstein-equation evidence.
```

For `matter_coupling`:

```text
MSStableMatterSemanticsBridge_v1(E;B_current) is Gate-Chair accepted only as scoped source-extension stable matter-semantics bridge evidence/precondition. The current continuation target is SourceMatterSemanticsAdoptionReadinessLaw_v1, a proposal-only readiness-law target audited source-pure as written pending Refuter stress. Universal matter coupling is not derived or adopted.
```

### Required outputs

- `research_control/design/scoped_positive_claim_vocabulary.md`
- registry update if applicable
- documentation impact receipt
- handoff to P1-T02

### Acceptance criteria

- Bare `accepted` is explicitly disallowed for high-risk rows unless immediately qualified.
- The control note distinguishes control status, mathematical status, physical status, and promotion status.
- The control note does not change physics claims.

---

## P1-T02: Status alias map for high-risk burdens

**Task ID suggestion:** `post_v13_p1_t02_status_alias_map_high_risk_burdens`  
**Task type:** `distance_to_gr_status_alias_control_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Add a status alias map for reader-facing rendering of high-risk Distance-to-GR rows.

### Required actions

1. Define reader-facing aliases for ledger rows:

   - `m_src`
   - `g_eff`
   - `matter_coupling`
   - `einstein_equations`
   - `benchmark_promotion`
   - `gate_chair_status`
   - `finite_toy_metric_response`

2. If a new registry or YAML config is preferred, create it.
3. If existing renderers can consume the aliases, integrate them.
4. If renderer integration is deferred, create a bounded handoff to P8.

### Required outputs

- alias map artifact, likely `research_control/design/distance_to_gr_status_aliases.yaml`
- renderer integration notes or handoff
- documentation impact receipt

### Acceptance criteria

- High-risk rows have exact scoped-positive wording.
- Aliases do not override ledger authority.
- Aliases are not treated as physics proof.

---

## P1-T03: Current-frontier wording pilot

**Task ID suggestion:** `post_v13_p1_t03_current_frontier_wording_pilot`  
**Task type:** `current_frontier_wording_update_control_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Update `research_control/current_frontier.md` rendering or source data so it uses scoped-positive language for high-risk statuses.

### Required actions

1. Inspect `scripts/research_control/render_current_frontier.py`.
2. Determine whether wording is hardcoded, rendered from ledger fields, or rendered from handoff fields.
3. Update the appropriate source, not generated output by hand.
4. Regenerate current frontier.
5. Validate renderer check.

### Required outputs

- updated renderer or source data
- regenerated `research_control/current_frontier.md`
- tests if renderer logic changes
- documentation impact receipt

### Acceptance criteria

- `M_src`, `g_eff`, and `matter_coupling` are distinguishable at a glance.
- The frontier does not imply `matter_coupling` is solved.
- The frontier does not underclaim `M_src` or scoped `g_eff`.

---

## P1-T04: Claim-language examples pack

**Task ID suggestion:** `post_v13_p1_t04_claim_language_examples_pack`  
**Task type:** `agent_guidance_examples_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Create examples that train local agents to produce two-part status statements.

### Required examples

Each example must show:

1. Bad wording.
2. Why it is wrong.
3. Correct wording.
4. Required source paths to inspect.
5. Forbidden overread.

Example categories:

- `M_src` underclaiming.
- `g_eff` underclaiming.
- `matter_coupling` overclaiming.
- `accepted` ambiguity.
- `audit_ready` ambiguity.
- validator PASS as proof.
- registry row as proof.
- Gate Chair scoped evidence vs adoption.

### Required outputs

- `research_control/design/scoped_claim_language_examples.md`
- handoff to P1-T05

---

## P1-T05: P1 integration validation

**Task ID suggestion:** `post_v13_p1_t05_scoped_claim_language_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Validate that P1 artifacts are coherent, registered, and non-promotional.

### Required actions

1. Run full validation.
2. Search for unqualified high-risk `accepted` in updated docs.
3. Create a P1 completion summary.
4. Select next task, likely P2-T01 or P6-T01 depending on active state.

---

# Phase P2: Immediate Frontier Stress

## P2 Objective

Execute the currently recommended scientific continuation: a bounded Refuter stress test of `SourceMatterSemanticsAdoptionReadinessLaw_v1`.

---

## P2-T01: Refuter stress of `SourceMatterSemanticsAdoptionReadinessLaw_v1`

**Task ID suggestion:** `post_v13_p2_t01_source_matter_semantics_adoption_readiness_law_refuter_stress`  
**Task type:** `ontology_law_research_packet_refuter_stress`  
**Role family:** `refuter@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Target derivation milestone:** `matter_coupling`  
**Milestone burden:** Stress the proposal-only `SourceMatterSemanticsAdoptionReadinessLaw_v1` after source-purity audit, before any selector, Gate Chair, matter-semantics, detector-semantics, coupling-law, matter-coupling, Einstein-equation, benchmark, or promotion route.

### Required source inputs

- `research_control/tasks/RT-20260701-001/artifacts/source_matter_semantics_adoption_readiness_law_target_v1.tex`
- `research_control/tasks/RT-20260701-002/artifacts/source_matter_semantics_adoption_readiness_law_smuggling_audit_v1.tex`
- `research_control/tasks/RT-20260630-056/artifacts/ms_stable_matter_semantics_bridge_source_extension_evidence_gate_chair_review_v1.tex`
- `research_control/design/gr_derivation_burden_map.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- latest handoff

### Required stress targets

1. Readiness-label stability: `audit_ready` must remain routing status only.
2. Relabeling naturality: readiness must commute with admissible source relabelings without target interpretation.
3. Finite-variation behavior: variations must preserve readiness, bottom out, or obstruct by source-side rules only.
4. Certificate deletion: missing no-target, no-detector, no-stress-energy, or no-action certificates must fail closed.
5. `RR_E` separation: distinct `RR_E` records must not be collapsed to manufacture readiness.
6. Scoped-evidence pressure: accepted bridge evidence must not become source-law adoption or matter-semantics adoption.
7. Process-authority pressure: registry, validator, handoff, approval, role, generated derivative, commit, file order, and cache perturbations must remain proof-irrelevant.
8. No-target certificate pressure: negative certificates must not become positive matter theory.
9. `g_eff` pressure: scoped `g_eff` status must not be imported as matter semantics.
10. Benchmark pressure: exact-GR benchmark status must not become evidence for readiness.

### Possible verdicts

- `stress_survived_pending_selector_no_adoption`
- `stress_survived_with_repair_required`
- `scoped_obstruction_found`
- `route_freeze_recommended`
- `human_gate_required`
- `invalid_due_to_target_import`
- `invalid_due_to_process_authority_laundering`
- `invalid_due_to_RR_E_collapse`
- `invalid_due_to_audit_ready_adoption_overread`

### Required mathematical payload

At least one of:

- stress theorem;
- countermodel;
- finite variation case table;
- relabeling naturality lemma or failure;
- `RR_E` pressure-pair counterexample;
- obstruction label family;
- fail-closed theorem;
- route-freeze criterion.

### Required outputs

- task-local TeX stress artifact
- child physics/math artifact
- child physics/philosophy artifact
- parent conflict review
- parent fusion notes
- completion receipt
- handoff to P2-T02

### Acceptance criteria

- Stress result is mathematically substantive.
- No adoption or downstream promotion occurs.
- If stress survives, the next route is selector, not matter coupling.
- If stress fails, obstruction or repair route is precise.

---

## P2-T02: Post-stress route selector

**Task ID suggestion:** `post_v13_p2_t02_post_smsar_stress_route_selector`  
**Task type:** `theoretical_continuation_selector_packet`  
**Role family:** `theoretical-continuation-selector@0.1.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Target derivation milestone:** `matter_coupling`  
**Milestone burden:** Classify the post-stress route for `SourceMatterSemanticsAdoptionReadinessLaw_v1` without adoption or promotion.

### Required route options

The selector must consider exactly these route families:

1. repair packet;
2. scoped obstruction packet;
3. route freeze;
4. narrow Gate Chair evidence/precondition review;
5. source-side irrelevance theorem route;
6. positive source-matter-semantics target formalization;
7. coupling-law target formalization;
8. bounded recovery-criteria packet;
9. no-go theorem packet, only if a precise no-go question is stated;
10. literature comparison, only if the theoretical decision depends on external primary literature;
11. project-system task, only if no scientific payload is being selected.

### Required selector output fields

- `theoretical_decision_output`
- `selected_next_packet_type`
- `selected_next_role_family`
- `decision_basis`
- `route_options_considered`
- `preserves_claim_blocks`
- `physics_progress_status`
- `distance_to_gr_delta`
- `new_mathematical_payload`
- `freeze_criteria_status`
- `route_cycle_control`
- `forbidden_conclusions`

### Acceptance criteria

- Exactly one next route is selected.
- Direct matter-coupling derivation is rejected unless all preconditions are explicitly established by source authority.
- Any Gate Chair route requires exact protected authority.
- If the same burden repeats, freeze criteria are evaluated.

---

## P2-T03: P2 scientific boundary update

**Task ID suggestion:** `post_v13_p2_t03_scientific_boundary_update_after_smsar_stress`  
**Task type:** `distance_to_gr_boundary_update_packet`  
**Role family:** `documentation-curator@0.1.0` or control role  
**Continue Research required:** yes  
**Physics task:** no, unless ledger change is scientific  
**Objective:** Update reader-facing current frontier and ledger notes after the stress and selector sequence.

### Required actions

1. Do not update ledger unless a valid task changed a Distance-to-GR status.
2. If no status delta, update current frontier only through renderer/source.
3. If stress found obstruction, create or update obstruction registry rows if applicable.
4. Preserve the exact blocked downstream claims.

### Acceptance criteria

- Current frontier matches active state.
- No stale “pending stress” remains if stress completed.
- No overread is introduced.

---

# Phase P3: Post-Stress Selector Discipline and No-Leap Control

## P3 Objective

Prevent a successful stress or audit from becoming an unauthorized leap to matter semantics, coupling law, matter coupling, Einstein equations, benchmark status, or completed derivation.

---

## P3-T01: No-leap route rule formalization

**Task ID suggestion:** `post_v13_p3_t01_no_leap_route_rule_formalization`  
**Task type:** `route_rule_control_packet`  
**Role family:** `documentation-curator@0.1.0` or `director-of-research` control role  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Formalize a route rule requiring selector classification after stress-survival of high-risk matter-coupling preconditions.

### Required rule

For any high-risk object in the matter-coupling chain:

- construction pass;
- source-purity audit pass;
- Refuter stress survival;
- Gate Chair scoped evidence/precondition acceptance;

does not authorize matter-semantics adoption, detector-semantics adoption, coupling-law adoption, matter-coupling derivation, Einstein equations, benchmark route, or promotion. It authorizes only the next bounded route named by a selector or a protected Gate Chair decision if exact human authority exists.

### Required outputs

- `research_control/design/no_leap_route_rule.md`
- route examples
- forbidden overread table

---

## P3-T02: Selector checklist update

**Task ID suggestion:** `post_v13_p3_t02_selector_checklist_update`  
**Task type:** `selector_contract_update_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Update selector guidance so all high-risk selectors must explain why stronger downstream routes are blocked or allowed.

### Required checklist items

Every high-risk selector must answer:

1. What exact object was just constructed, audited, stressed, or gated?
2. Is it adopted, accepted as evidence/precondition, proposal-only, or rejected?
3. Which source laws remain missing?
4. Which target imports are forbidden?
5. Which downstream routes are blocked?
6. Why is the selected route the lowest-authority next route?
7. Does freeze evaluation apply?
8. Is human gate authority required?
9. Does this route add a new mathematical payload?
10. Does the route repeat the same burden without new payload?

### Outputs

- updated role guidance or design note
- tests or validation if role schemas change
- documentation impact receipt

---

## P3-T03: Post-stress route template

**Task ID suggestion:** `post_v13_p3_t03_post_stress_route_template`  
**Task type:** `task_template_control_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Create a reusable template for post-stress selector tasks.

### Required template sections

- stress input artifact
- audit input artifact
- construction input artifact
- exact object under classification
- available route options
- rejected route options
- freeze criteria
- Distance-to-GR delta
- forbidden conclusions
- handoff text
- validation checklist

---

## P3-T04: P3 validation and pilot

**Task ID suggestion:** `post_v13_p3_t04_no_leap_pilot_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Validate P3 by applying the no-leap rule to the latest `SourceMatterSemanticsAdoptionReadinessLaw_v1` route state.

### Acceptance criteria

- Pilot produces no physics promotion.
- The next route remains selector-controlled.
- Any detected documentation drift is routed separately.

---

# Phase P4: Positive Source-Side Matter Semantics Program

## P4 Objective

Move from guard-only or anti-smuggling machinery toward positive source-side definitions for matter semantics, without importing detector semantics, stress-energy semantics, matter action, target metric, or benchmark behavior.

---

## P4-T01: Positive source-matter-semantics target formalizer

**Task ID suggestion:** `post_v13_p4_t01_positive_source_matter_semantics_target_formalizer`  
**Task type:** `ontology_law_research_packet_positive_semantics_target`  
**Role family:** `ontology-formalizer@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Target derivation milestone:** `matter_coupling`  
**Milestone burden:** Formalize a positive source-side matter-semantics target after scoped bridge evidence and readiness-law routing, without adopting matter semantics.

### Required target components

The formalizer must specify:

1. source-side matter-semantics domain;
2. admissible source records;
3. excluded target imports;
4. source-side semantic labels or structures;
5. source-side equivalence or separation conditions;
6. relation to `MSStableMatterSemanticsBridge_v1`;
7. relation to `SourceMatterSemanticsAdoptionReadinessLaw_v1`;
8. fail-closed branches;
9. proof obligations;
10. exact downstream routes still blocked.

### Explicitly forbidden target imports

- detector protocols;
- empirical calibration;
- stress-energy tensor;
- stress-energy semantics;
- matter action;
- conservation law by GR/QFT import;
- target metric;
- Lorentzian signature;
- proper time;
- Einstein equations;
- benchmark fit.

### Required output

- TeX artifact defining a proposal-only target
- completion with `candidate_constructor_result` if a candidate target is constructed
- handoff to P4-T02

---

## P4-T02: Positive source-matter-semantics candidate constructor

**Task ID suggestion:** `post_v13_p4_t02_positive_source_matter_semantics_candidate_constructor`  
**Task type:** `candidate_constructor_positive_source_matter_semantics`  
**Role family:** `candidate-constructor@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Target derivation milestone:** `matter_coupling`  
**Milestone burden:** Construct or precisely obstruct a positive source-side matter-semantics candidate under the P4-T01 target.

### Required result types

- `constructed_candidate_pending_audit`
- `precise_obstruction`
- `route_freeze_recommended`
- `target_repair_required`

### Required mathematical payload

At least one of:

- source-side definition;
- finite/local witness;
- source equivalence theorem;
- source separation theorem;
- fail-closed map;
- countermodel;
- obstruction label.

### Acceptance criteria

- Candidate adds positive source-side semantics, not only no-target certificates.
- No detector semantics, stress-energy, matter action, coupling law, or matter coupling is adopted.

---

## P4-T03: Positive source-matter-semantics smuggling audit

**Task ID suggestion:** `post_v13_p4_t03_positive_source_matter_semantics_smuggling_audit`  
**Task type:** `source_extension_smuggling_audit`  
**Role family:** `smuggling-auditor@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Target derivation milestone:** `matter_coupling`  
**Milestone burden:** Audit the P4-T02 candidate for hidden target imports and evidence-as-adoption overread.

### Audit targets

- target geometry;
- detector semantics;
- empirical calibration;
- stress-energy;
- matter action;
- conservation law;
- coupling-law adoption;
- `MetricData(E)`;
- `g_eff` scope expansion;
- process authority;
- benchmark authority;
- evidence-as-adoption;
- `RR_E` collapse.

---

## P4-T04: Positive source-matter-semantics Refuter stress

**Task ID suggestion:** `post_v13_p4_t04_positive_source_matter_semantics_refuter_stress`  
**Task type:** `source_extension_refuter_stress`  
**Role family:** `refuter@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Target derivation milestone:** `matter_coupling`  
**Milestone burden:** Stress the audited positive source-matter-semantics candidate.

### Stress targets

- source relabeling;
- finite variation;
- certificate deletion;
- semantic-label deletion;
- degeneracy;
- `RR_E` pressure;
- process-authority pressure;
- `g_eff` import pressure;
- detector-semantics pressure;
- stress-energy pressure;
- matter-action pressure;
- adoption pressure.

---

## P4-T05: Positive source-matter-semantics post-stress selector

**Task ID suggestion:** `post_v13_p4_t05_positive_source_matter_semantics_post_stress_selector`  
**Task type:** `theoretical_continuation_selector_packet`  
**Role family:** `theoretical-continuation-selector@0.1.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Objective:** Select exactly one next route after P4 stress.

### Allowed next routes

- repair;
- obstruction;
- freeze;
- Gate Chair evidence/precondition review;
- source-law target formalization;
- detector-semantics preflight target;
- coupling-law target formalization;
- route back to `RR_E` theorem;
- no-promotion handoff.

---

## P4-T06: P4 boundary update

**Task ID suggestion:** `post_v13_p4_t06_positive_source_matter_semantics_boundary_update`  
**Task type:** `frontier_boundary_update_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no unless ledger status changes  
**Objective:** Update current frontier wording after P4 without overclaiming matter semantics.

---

# Phase P5: `RR_E` Theorem or Obstruction Program

## P5 Objective

Treat `RR_E` separation as a central mathematical fault line. Either prove a source-side irrelevance/equivalence theorem under precise assumptions, or record a scoped obstruction/freeze.

---

## P5-T01: `RR_E` theorem target formalizer

**Task ID suggestion:** `post_v13_p5_t01_rr_e_theorem_target_formalizer`  
**Task type:** `ontology_law_research_packet_rr_e_theorem_target`  
**Role family:** `ontology-formalizer@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Target derivation milestone:** `matter_coupling`  
**Milestone burden:** Formalize the theorem target for when distinct `RR_E` records can or cannot be identified without target detector semantics.

### Required theorem-target questions

1. What is an `RR_E` record in the current source-side framework?
2. What does it mean to preserve `RR_E` separation?
3. What would source-side irrelevance mean?
4. Which assumptions are allowed?
5. Which assumptions would smuggle detector semantics?
6. Which finite/local examples distinguish separation from irrelevance?
7. What obstruction label applies if irrelevance is underdetermined?

### Required outputs

- TeX theorem-target artifact
- fail-closed obstruction family
- handoff to P5-T02

---

## P5-T02: `RR_E` irrelevance theorem attempt or obstruction

**Task ID suggestion:** `post_v13_p5_t02_rr_e_irrelevance_theorem_attempt_or_obstruction`  
**Task type:** `candidate_constructor_rr_e_theorem_or_obstruction`  
**Role family:** `candidate-constructor@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Target derivation milestone:** `matter_coupling`  
**Milestone burden:** Attempt to construct a source-only theorem or precise obstruction for `RR_E` irrelevance/separation.

### Required result types

- `rr_e_irrelevance_theorem_candidate`
- `rr_e_separation_theorem_candidate`
- `rr_e_underdetermination_obstruction`
- `rr_e_target_repair_required`
- `rr_e_route_freeze_recommended`

### Required mathematical payload

At least one of:

- theorem statement;
- proof sketch;
- finite countermodel;
- source-side witness;
- obstruction record;
- exact missing primitive.

---

## P5-T03: `RR_E` smuggling audit

**Task ID suggestion:** `post_v13_p5_t03_rr_e_theorem_smuggling_audit`  
**Task type:** `source_extension_smuggling_audit`  
**Role family:** `smuggling-auditor@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Objective:** Audit the theorem attempt for detector semantics, empirical calibration, target metric, process authority, and evidence-as-adoption smuggling.

---

## P5-T04: `RR_E` Refuter stress

**Task ID suggestion:** `post_v13_p5_t04_rr_e_theorem_refuter_stress`  
**Task type:** `source_extension_refuter_stress`  
**Role family:** `refuter@0.2.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Objective:** Stress the audited `RR_E` theorem or obstruction.

### Stress cases

- pair of records with same source support and different `RR_E`;
- pair of records with transported source relabeling;
- finite variation changing `RR_E`;
- deletion of source certificates;
- pressure to interpret `RR_E` as detector response;
- pressure to identify `RR_E` through `g_eff`;
- pressure to use benchmark behavior;
- process-authority perturbation.

---

## P5-T05: `RR_E` post-stress selector or freeze

**Task ID suggestion:** `post_v13_p5_t05_rr_e_post_stress_selector_or_freeze`  
**Task type:** `theoretical_continuation_selector_packet`  
**Role family:** `theoretical-continuation-selector@0.1.0`  
**Continue Research required:** yes  
**Physics task:** yes  
**Objective:** Select continuation, obstruction, or freeze based on P5 stress.

### Freeze trigger

If the project again cannot state when `RR_E` distinctions are irrelevant without importing detector semantics, record a scoped obstruction or freeze candidate rather than repeating the same route.

---

## P5-T06: `RR_E` boundary update

**Task ID suggestion:** `post_v13_p5_t06_rr_e_boundary_update`  
**Task type:** `frontier_boundary_update_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Update current frontier and theorem inventory with the `RR_E` result.

---

# Phase P6: Claim-Language Linter

## P6 Objective

Create deterministic checks that prevent dangerous wording in documentation, generated surfaces, registries, current-frontier summaries, and possibly task artifacts.

---

## P6-T01: Forbidden phrase taxonomy

**Task ID suggestion:** `post_v13_p6_t01_forbidden_claim_phrase_taxonomy`  
**Task type:** `claim_linter_taxonomy_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Define the phrase taxonomy for a claim-language linter.

### Required phrase classes

1. Bare high-risk `accepted`.
2. Matter-coupling overclaim.
3. `g_eff` overclaim.
4. `M_src` underclaim.
5. Einstein-equation overclaim.
6. Benchmark overclaim.
7. Validator-as-proof.
8. Registry-as-proof.
9. Gate-authority laundering.
10. Generated-derivative authority.
11. `audit_ready` as adoption.
12. no-target certificate as positive semantics.

### Example forbidden or warning phrases

- `matter coupling accepted`
- `matter coupling solved`
- `matter coupling derived`
- `universal coupling established`
- `g_eff metric derived`
- `Lorentzian metric constructed`
- `GR derived`
- `Einstein equations next by implication`
- `benchmark recovered`
- `validated proof`
- `registry proves`
- `Gate Chair pending means accepted`
- `audit_ready means adoptable`
- `no-target certificate supplies matter semantics`
- bare `accepted` near `matter_coupling`, `g_eff`, `M_src`, `MetricData(E)`, or `Einstein equations`

### Required outputs

- `research_control/design/claim_language_linter_taxonomy.yaml`
- examples and severity levels
- handoff to P6-T02

---

## P6-T02: Claim-language linter implementation

**Task ID suggestion:** `post_v13_p6_t02_claim_language_linter_implementation`  
**Task type:** `validator_tooling_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Implement a deterministic linter that scans selected text surfaces for dangerous claim language.

### Candidate implementation

Create or update:

- `scripts/project_control/validate_claim_language.py`
- tests under `tests/`
- configuration from P6-T01 taxonomy

### Required scan surfaces

At minimum:

- `README.md`
- `github-facing/*.md`
- `research_control/current_frontier.md`
- `research_control/design/*.md`
- `implementations_plans/*.md`
- `markdown/publication-briefs/*.md`
- `markdown/html-explainer-specs/*.md`

Optional warning-only scan:

- `research_control/tasks/**/*.md`
- `research_control/tasks/**/*.tex`
- `registries/*.csv`

### Linter behavior

- hard fail on public-facing overclaims;
- warning on historical task artifacts unless current generated summaries repeat the phrase;
- allow exact quoted historical statuses only if followed by scoped interpretation;
- require whitelist entries to be explicit and reviewed.

---

## P6-T03: Integrate linter into validation workflow

**Task ID suggestion:** `post_v13_p6_t03_claim_language_linter_validation_integration`  
**Task type:** `validator_integration_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Add the linter to appropriate validation scripts or documentation-impact workflow.

### Required actions

1. Decide whether linter runs in `validate_research_control.py`, documentation-impact validation, or separate CI-style command.
2. Update docs with command.
3. Add unit tests.
4. Add failure examples.

---

## P6-T04: Remediate linter findings

**Task ID suggestion:** `post_v13_p6_t04_claim_language_linter_remediation`  
**Task type:** `documentation_remediation_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Fix any linter findings in current public-facing and current-control surfaces.

### Rule

Do not edit historical task artifacts merely to satisfy the linter unless they are generated current summaries or the repository policy allows correction.

---

## P6-T05: P6 validation and handoff

**Task ID suggestion:** `post_v13_p6_t05_claim_linter_phase_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Validate linter behavior and hand off to P7 or P8.

---

# Phase P7: Validation-Status Reconciliation

## P7 Objective

Fix ambiguity between `PENDING`, `PASS`, pre-execution checks, task-completion checks, post-checkpoint checks, render checks, and memory bootstrap checks.

---

## P7-T01: Validation-field inventory

**Task ID suggestion:** `post_v13_p7_t01_validation_field_inventory`  
**Task type:** `validation_status_inventory_packet`  
**Role family:** project-system auditor role through Continue Research  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Inventory all validation fields used in handoffs, completions, current frontier, scripts, and registries.

### Required output

- `research_control/design/validation_status_field_inventory.md`

### Required categories

- `pre_execution_checks`
- `task_completion_checks`
- `post_checkpoint_checks`
- `memory_bootstrap_checks`
- `research_control_validation`
- `documentation_impact_validation`
- `graph_freshness_checks`
- `render_freshness_checks`
- `git_diff_checks`
- `tests`

---

## P7-T02: Validation-status schema split

**Task ID suggestion:** `post_v13_p7_t02_validation_status_schema_split`  
**Task type:** `validation_schema_update_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Define and implement a schema split so `PENDING` and `PASS` are not visually contradictory.

### Required schema

Each task or handoff may include:

```yaml
validation_layers:
  pre_execution:
    status: ""
    evidence: []
  completion_internal:
    status: ""
    evidence: []
  post_write:
    status: ""
    evidence: []
  post_checkpoint:
    status: ""
    evidence: []
  renderer:
    status: ""
    evidence: []
  memory_bootstrap:
    status: ""
    evidence: []
```

### Acceptance criteria

- Old fields remain backward compatible or are migrated safely.
- Renderers display layer names.
- No reader sees unexplained `PENDING` beside `PASS`.

---

## P7-T03: Renderer and handoff update

**Task ID suggestion:** `post_v13_p7_t03_validation_renderer_handoff_update`  
**Task type:** `renderer_update_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Update `render_current_frontier.py` and handoff templates to show validation layers.

---

## P7-T04: Backfill latest active state

**Task ID suggestion:** `post_v13_p7_t04_validation_status_latest_state_backfill`  
**Task type:** `latest_state_backfill_packet`  
**Role family:** project-system auditor role through Continue Research  
**Continue Research required:** yes  
**Objective:** Backfill or annotate the latest active handoff/current-frontier validation status using the new layered scheme.

### Guard

Do not rewrite historical scientific conclusions. This is validation metadata clarity only.

---

## P7-T05: P7 validation

**Task ID suggestion:** `post_v13_p7_t05_validation_status_phase_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Run tests and validation, then hand off to P8.

---

# Phase P8: Public Status-Layer Propagation

## P8 Objective

Make the status-layer split visible in public and reader-facing surfaces, so `accepted` cannot be misread.

---

## P8-T01: Public status table source spec

**Task ID suggestion:** `post_v13_p8_t01_public_status_table_source_spec`  
**Task type:** `public_status_source_spec_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Create a canonical public status table source spec.

### Required table columns

- burden;
- control status;
- mathematical status;
- physical status;
- promotion status;
- exact positive scoped claim;
- exact blocked overread;
- last evidence path.

### Required high-risk rows

- `M_src`
- `g_eff`
- `matter_coupling`
- `einstein_equations`
- `benchmark_promotion`

---

## P8-T02: README and GitHub-facing status update

**Task ID suggestion:** `post_v13_p8_t02_readme_github_facing_status_update`  
**Task type:** `public_documentation_update_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Update public-facing docs to include the status-layer table or link to it.

### Candidate files

- `README.md`
- `github-facing/project-overview-explainer.md`
- `github-facing/aether-flow-physics-program-explainer.md`
- `github-facing/exact-gr-benchmark-boundary-explainer.md`
- `github-facing/gr-derivation-roadmap-explainer.md`
- `github-facing/claim-gates-explainer.md`

### Acceptance criteria

- Public surfaces state that GR is not derived.
- Public surfaces do not underclaim scoped `M_src` and `g_eff`.
- Public surfaces do not imply matter coupling is solved.

---

## P8-T03: HTML explainer source-spec update

**Task ID suggestion:** `post_v13_p8_t03_html_explainer_source_spec_update`  
**Task type:** `html_explainer_source_spec_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Update Markdown source specs for generated HTML explainers if they need current status corrections.

### Rule

Do not hand-edit generated HTML. Modify source specs and regenerate through approved tooling.

---

## P8-T04: Public status regeneration

**Task ID suggestion:** `post_v13_p8_t04_public_status_regeneration`  
**Task type:** `generated_derivative_regeneration_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Regenerate affected public derivatives and validate registries.

---

## P8-T05: Public status claim-language validation

**Task ID suggestion:** `post_v13_p8_t05_public_status_claim_language_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Run claim-language linter and documentation validators over public surfaces.

---

# Phase P9: Three-Tier Claim Convention

## P9 Objective

Make every summary distinguish adopted objects, accepted evidence/preconditions, and open or blocked physical targets.

---

## P9-T01: Three-tier claim convention policy

**Task ID suggestion:** `post_v13_p9_t01_three_tier_claim_convention_policy`  
**Task type:** `claim_convention_policy_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Create a policy requiring three-tier summaries.

### Required tiers

1. **Adopted objects**
   - Example: source-only `M_src`, scoped source-extension `g_eff`.

2. **Accepted evidence/preconditions**
   - Example: `MCPA`, source coupling-law candidate evidence, stable partition precondition, stable matter-semantics bridge evidence/precondition.

3. **Open or blocked physical targets**
   - Example: matter semantics, detector semantics, universal coupling, stress-energy, matter action, Einstein equations, benchmark promotion.

---

## P9-T02: Completion template update

**Task ID suggestion:** `post_v13_p9_t02_completion_template_three_tier_update`  
**Task type:** `completion_contract_update_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Update completion templates and role guidance to include three-tier summaries.

### Required fields

```yaml
three_tier_claim_summary:
  adopted_objects: []
  accepted_evidence_preconditions: []
  open_or_blocked_physical_targets: []
  forbidden_overread: []
```

---

## P9-T03: Current frontier three-tier pilot

**Task ID suggestion:** `post_v13_p9_t03_current_frontier_three_tier_pilot`  
**Task type:** `current_frontier_renderer_update_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Add or pilot the three-tier summary in `current_frontier.md`.

---

## P9-T04: P9 validation

**Task ID suggestion:** `post_v13_p9_t04_three_tier_phase_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Validate three-tier summary behavior.

---

# Phase P10: Frontier Theorem Inventory

## P10 Objective

Create a compact, source-backed, current frontier theorem/object inventory that tells agents and humans what exists, what status it has, what assumptions it needs, what fail-closed branches it uses, and what theorem is needed next.

---

## P10-T01: Inventory schema

**Task ID suggestion:** `post_v13_p10_t01_frontier_theorem_inventory_schema`  
**Task type:** `frontier_theorem_inventory_schema_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Define the schema for a frontier theorem inventory.

### Required fields

- object ID;
- object name;
- milestone;
- object type;
- status;
- source path;
- authority level;
- assumptions;
- definitions introduced;
- theorem-like claims;
- audits passed;
- stress results;
- Gate Chair results;
- fail-closed branches;
- known obstructions;
- forbidden overread;
- next theorem needed;
- downstream blocked targets.

---

## P10-T02: Populate core inventory

**Task ID suggestion:** `post_v13_p10_t02_populate_core_frontier_theorem_inventory`  
**Task type:** `frontier_theorem_inventory_population_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Physics task:** no, unless Director requires physics review  
**Objective:** Populate the inventory for core objects.

### Required objects

- `M_src^{GSC}(E)`
- `g_eff^{GSC-cand}(E;G^beta,T_src(E))`
- `MCPA^cand_v1(E)`
- `SourceCouplingLawCandidate^cand_v1(E)`
- `MSStablePartitionPrecondition_v1`
- `MSStableMatterSemanticsBridge_v1(E;B_current)`
- `SourceMatterSemanticsAdoptionReadinessLaw_v1`
- `finite_toy_metric_response` frozen negative route
- `Resp_lc`
- `ObsLoc_lc`
- `EqSrc`
- `RetainH`
- `GenH`

---

## P10-T03: Inventory registry integration

**Task ID suggestion:** `post_v13_p10_t03_frontier_theorem_inventory_registry_integration`  
**Task type:** `registry_integration_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Register or crosslink the inventory according to repository policy.

---

## P10-T04: Inventory renderer

**Task ID suggestion:** `post_v13_p10_t04_frontier_theorem_inventory_renderer`  
**Task type:** `renderer_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** If useful, render a compact inventory table for human readers from the canonical inventory.

---

## P10-T05: P10 validation

**Task ID suggestion:** `post_v13_p10_t05_frontier_theorem_inventory_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Validate inventory freshness and claim boundaries.

---

# Phase P11: Support-Only Formalization Lane

## P11 Objective

Add small formal or typed support artifacts that help agents reason about statuses, fail-closed maps, readiness labels, and route rules, without treating the formalization as proof authority.

---

## P11-T01: Formalization lane design

**Task ID suggestion:** `post_v13_p11_t01_support_only_formalization_lane_design`  
**Task type:** `support_formalization_design_packet`  
**Role family:** project-system tooling or formalization-support role through Continue Research  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Choose the initial support-only formalization substrate.

### Acceptable substrates

- JSON Schema;
- Python dataclasses plus tests;
- typed YAML schemas;
- Lean skeletons with no proof-authority claim;
- another repo-approved support-only formalism.

### Required design decision

The design must state:

- what the formalization can check;
- what it cannot check;
- why it is not physics proof authority;
- how it relates to validators;
- how it avoids target imports.

---

## P11-T02: Status enum formalization

**Task ID suggestion:** `post_v13_p11_t02_status_enum_formalization`  
**Task type:** `support_formalization_packet`  
**Role family:** formalization-support role through Continue Research  
**Continue Research required:** yes  
**Objective:** Formalize status enums and allowed transitions.

### Required enums

- `draft_control`
- `proposal_only`
- `source_extension_candidate`
- `source_extension_smuggling_audit`
- `source_extension_refuter_stress`
- `accepted_as_scoped_evidence_precondition`
- `adopted_as_scoped_source_extension_object`
- `adopted_as_source_only_object`
- `rejected`
- `frozen_negative`
- `human_gated`

### Required forbidden transitions

- audit pass to adoption;
- stress survival to adoption;
- evidence/precondition to matter coupling;
- scoped `g_eff` object to unscoped Lorentzian metric;
- source-only `M_src` to target manifold;
- validator PASS to proof.

---

## P11-T03: Fail-closed map formalization

**Task ID suggestion:** `post_v13_p11_t03_fail_closed_map_formalization`  
**Task type:** `support_formalization_packet`  
**Role family:** formalization-support role through Continue Research  
**Continue Research required:** yes  
**Objective:** Formalize fail-closed maps and obstruction labels used in matter-semantics routes.

---

## P11-T04: Readiness map skeleton

**Task ID suggestion:** `post_v13_p11_t04_readiness_map_skeleton`  
**Task type:** `support_formalization_packet`  
**Role family:** formalization-support role through Continue Research  
**Continue Research required:** yes  
**Objective:** Encode the skeleton:

```text
Ready_E^src: B_E^smb -> {bottom, audit_ready, obstruction}
```

with no proof-authority claim.

---

## P11-T05: Formalization tests

**Task ID suggestion:** `post_v13_p11_t05_support_formalization_tests`  
**Task type:** `support_formalization_tests_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Add tests that ensure invalid status transitions fail.

---

## P11-T06: Support-only boundary docs

**Task ID suggestion:** `post_v13_p11_t06_support_only_boundary_docs`  
**Task type:** `support_boundary_documentation_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Document that formalization artifacts are support-only, not independent physics authority.

---

# Phase P12: External Red-Team Mode

## P12 Objective

Create a review mode that ignores workflow success and attacks definitions, assumptions, theorem statements, circularity, hidden target imports, and route orbiting.

---

## P12-T01: External red-team role contract

**Task ID suggestion:** `post_v13_p12_t01_external_red_team_role_contract`  
**Task type:** `role_contract_packet`  
**Role family:** project-system role governance through Continue Research  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Add or update an `external-red-team-reviewer` role contract.

### Role boundaries

The role may:

- critique definitions;
- identify circularity;
- test target imports;
- compare with external literature when authorized;
- challenge theorem statements;
- recommend obstruction or freeze.

The role may not:

- adopt or reject physics objects;
- issue Gate Chair verdicts;
- promote benchmark status;
- claim global no-go theorem without a precise theorem artifact;
- override canonical sources.

---

## P12-T02: Red-team review template

**Task ID suggestion:** `post_v13_p12_t02_external_red_team_review_template`  
**Task type:** `review_template_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Create a template for red-team review packets.

### Required review sections

- object under attack;
- source files reviewed;
- definitions attacked;
- hidden target imports;
- circularity checks;
- process-authority checks;
- overclaim checks;
- finite counterexamples;
- comparison to known constraints;
- recommended repair, obstruction, freeze, or continuation.

---

## P12-T03: Red-team pilot on `M_src`, `g_eff`, and matter bridge

**Task ID suggestion:** `post_v13_p12_t03_external_red_team_pilot_core_objects`  
**Task type:** `external_red_team_review_packet`  
**Role family:** `external-red-team-reviewer@0.1.0` if available, otherwise provisional bounded role through Continue Research  
**Continue Research required:** yes  
**Physics task:** yes if reviewing scientific objects  
**Target derivation milestone:** use the milestone of the reviewed object  
**Objective:** Pilot external red-team review on core objects.

### Objects to review

- source-only `M_src`
- scoped source-extension `g_eff`
- `MSStableMatterSemanticsBridge_v1`
- `SourceMatterSemanticsAdoptionReadinessLaw_v1`

### Required verdicts

- no blocking issue found;
- repair required;
- scoped obstruction candidate;
- freeze candidate;
- external literature review required.

---

## P12-T04: Red-team findings selector

**Task ID suggestion:** `post_v13_p12_t04_external_red_team_findings_selector`  
**Task type:** `theoretical_continuation_selector_packet`  
**Role family:** `theoretical-continuation-selector@0.1.0`  
**Continue Research required:** yes  
**Objective:** Decide how to route red-team findings without promotion.

---

## P12-T05: P12 validation

**Task ID suggestion:** `post_v13_p12_t05_external_red_team_phase_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** project-system auditor through Continue Research  
**Continue Research required:** yes  
**Objective:** Validate role boundaries and output integration.

---

# Phase P13: Route-Orbit Freeze Hardening

## P13 Objective

Detect repeated same-burden, same-shape route cycles earlier and require repair, obstruction, freeze, or materially new payload.

---

## P13-T01: Route signature definition

**Task ID suggestion:** `post_v13_p13_t01_route_signature_definition`  
**Task type:** `route_cycle_control_design_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Define a route signature for detecting orbiting.

### Route signature fields

- target milestone;
- burden;
- object family;
- task type;
- role;
- source-extension category;
- selected route;
- missing primitive;
- payload type;
- obstruction label;
- freeze candidate;
- previous task IDs.

---

## P13-T02: Route history extractor

**Task ID suggestion:** `post_v13_p13_t02_route_history_extractor`  
**Task type:** `route_history_tooling_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Implement or update a script that extracts route signatures from task records.

---

## P13-T03: Route-orbit validator

**Task ID suggestion:** `post_v13_p13_t03_route_orbit_validator`  
**Task type:** `validator_tooling_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Add warnings or hard-fail conditions for route orbits.

### Hard-fail candidate

Hard fail when:

- same milestone;
- same burden;
- same missing primitive;
- same route type;
- no new mathematical payload;
- no repair;
- no obstruction;
- no freeze evaluation.

### Warning candidate

Warn when:

- same burden repeats with new payload but no route-cycle-control field.

---

## P13-T04: Matter-semantics route orbit pilot

**Task ID suggestion:** `post_v13_p13_t04_matter_semantics_route_orbit_pilot`  
**Task type:** `route_orbit_pilot_packet`  
**Role family:** project-system auditor through Continue Research  
**Continue Research required:** yes  
**Objective:** Run the route-orbit detector on the P5/P7/P13 matter-semantics chain.

---

## P13-T05: P13 validation

**Task ID suggestion:** `post_v13_p13_t05_route_orbit_phase_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Validate route-orbit hardening.

---

# Phase P14: Local AI Wording Integration

## P14 Objective

Update local AI instructions, prompts, role guidance, and examples so local agents use the exact scoped-positive status language.

---

## P14-T01: Continue Research prompt wording update

**Task ID suggestion:** `post_v13_p14_t01_continue_research_prompt_wording_update`  
**Task type:** `agent_prompt_update_packet`  
**Role family:** `documentation-curator@0.1.0` or prompt/tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Update Continue Research guidance so agents use scoped-positive language.

### Required wording blocks

Include the exact `M_src`, `g_eff`, and `matter_coupling` wording from Section 2.3.

---

## P14-T02: Role-specific wording examples

**Task ID suggestion:** `post_v13_p14_t02_role_specific_wording_examples`  
**Task type:** `role_guidance_examples_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Add role-specific examples for:

- Director;
- Theoretical Continuation Selector;
- Candidate Constructor;
- Smuggling Auditor;
- Refuter;
- Gate Chair;
- Documentation Curator;
- external red-team reviewer.

---

## P14-T03: Negative examples and correction tests

**Task ID suggestion:** `post_v13_p14_t03_negative_wording_examples_tests`  
**Task type:** `prompt_test_packet`  
**Role family:** project-system tooling role through Continue Research  
**Continue Research required:** yes  
**Objective:** Add tests or sample fixtures showing bad phrasing and corrected phrasing.

---

## P14-T04: Generated summaries audit

**Task ID suggestion:** `post_v13_p14_t04_generated_summaries_wording_audit`  
**Task type:** `generated_summary_audit_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Audit generated summaries, current frontier, graph notes, and indexes for underclaiming or overclaiming.

---

## P14-T05: P14 validation

**Task ID suggestion:** `post_v13_p14_t05_local_ai_wording_phase_validation`  
**Task type:** `phase_validation_packet`  
**Role family:** project-system auditor through Continue Research  
**Continue Research required:** yes  
**Objective:** Validate that local AI wording guidance is integrated.

---

# Phase P15: Literature Comparison

## P15 Objective

Compare the project against neighboring reconstruction, emergent-gravity, causal-structure, and no-go constraints without using resemblance to literature as claim promotion.

---

## P15-T01: Literature comparison scope selector

**Task ID suggestion:** `post_v13_p15_t01_literature_comparison_scope_selector`  
**Task type:** `literature_comparison_scope_selector`  
**Role family:** `theoretical-continuation-selector@0.1.0` or literature-review role through Continue Research  
**Continue Research required:** yes  
**Physics task:** yes if comparison affects physics routing  
**Target derivation milestone:** likely `matter_coupling` or `effective_metric_g_eff`, selected by Director  
**Objective:** Select a bounded literature comparison scope.

### Candidate comparison areas

- causal set theory;
- emergent gravity;
- analogue gravity;
- metric reconstruction;
- operational spacetime reconstruction;
- relational dynamics;
- effective field theory constraints;
- equivalence principle reconstruction;
- universal coupling no-go and reconstruction constraints;
- stress-energy derivation routes;
- action/variation derivation requirements.

### Source rules

Use primary literature where possible. Cite external materials. Distinguish established literature from project construction.

---

## P15-T02: Literature comparison packet

**Task ID suggestion:** `post_v13_p15_t02_literature_comparison_packet`  
**Task type:** `literature_comparison_packet`  
**Role family:** literature-review role through Continue Research  
**Continue Research required:** yes  
**Objective:** Produce a source-backed comparison artifact.

### Required sections

- literature source list;
- neighboring program summary;
- relevant reconstruction constraints;
- no-go constraints;
- similarities to AEther-Flow;
- differences from AEther-Flow;
- risks to `M_src`;
- risks to scoped `g_eff`;
- risks to matter semantics;
- implications for `RR_E`;
- implications for stress-energy/action route;
- no claim-promotion statement.

---

## P15-T03: Literature findings route selector

**Task ID suggestion:** `post_v13_p15_t03_literature_findings_route_selector`  
**Task type:** `theoretical_continuation_selector_packet`  
**Role family:** `theoretical-continuation-selector@0.1.0`  
**Continue Research required:** yes  
**Objective:** Route literature findings to repair, red-team, theorem target, obstruction, or no action.

---

## P15-T04: Literature comparison public boundary

**Task ID suggestion:** `post_v13_p15_t04_literature_comparison_public_boundary`  
**Task type:** `documentation_boundary_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** If public-facing docs mention the comparison, ensure they do not imply external validation or claim promotion.

---

# Phase P16: Final Integration Audit and Continuation Handoff

## P16 Objective

Validate v13 rollout, prove recommendation coverage, refresh current frontier, and hand off to ordinary research continuation.

---

## P16-T01: V13 coverage audit

**Task ID suggestion:** `post_v13_p16_t01_v13_coverage_audit`  
**Task type:** `implementation_plan_coverage_audit`  
**Role family:** project-system auditor through Continue Research  
**Continue Research required:** yes  
**Physics task:** no  
**Objective:** Audit every v13 recommendation and task.

### Required output

- `research_control/tasks/<task_id>/artifacts/v13_coverage_audit.md`

### Required statuses

- completed;
- implemented by existing later state;
- superseded by tracked state;
- blocked by human gate;
- deferred with reason;
- failed with repair task;
- not applicable.

---

## P16-T02: Physics-progress metrics report

**Task ID suggestion:** `post_v13_p16_t02_physics_progress_metrics_report`  
**Task type:** `metrics_report_packet`  
**Role family:** project-system auditor through Continue Research  
**Continue Research required:** yes  
**Objective:** Run and interpret physics progress metrics after v13.

### Required command

```zsh
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py
```

### Guard

Metrics are AI-system diagnostics, not physics promotion.

---

## P16-T03: Current frontier final refresh

**Task ID suggestion:** `post_v13_p16_t03_current_frontier_final_refresh`  
**Task type:** `current_frontier_final_refresh_packet`  
**Role family:** `documentation-curator@0.1.0`  
**Continue Research required:** yes  
**Objective:** Refresh current frontier and ensure it uses v13 claim language.

---

## P16-T04: V13 final validation

**Task ID suggestion:** `post_v13_p16_t04_v13_final_validation`  
**Task type:** `final_validation_packet`  
**Role family:** project-system auditor through Continue Research  
**Continue Research required:** yes  
**Objective:** Run all required validations and tests.

### Required commands

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/project_control/classify_project_changes.py --json
.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python -m unittest discover -s tests
git diff --check
```

---

## P16-T05: Ordinary research continuation handoff

**Task ID suggestion:** `post_v13_p16_t05_ordinary_research_continuation_handoff`  
**Task type:** `final_continuation_handoff_packet`  
**Role family:** `director-of-research`  
**Continue Research required:** yes  
**Objective:** Create the final handoff after v13, selecting the next ordinary research route.

### Handoff must state

- v13 completed or partially completed status;
- active scientific frontier;
- current Distance-to-GR state;
- current positive scoped claims;
- current blocked claims;
- exact next task;
- whether human gate is required;
- whether project-improvement sidecar exists;
- no physics promotion unless separately authorized.

---

## 7. Dependency Order

The preferred execution order is:

```text
P0
  -> P1
  -> P2
  -> P3
  -> P4 or P5 depending on selector output
  -> P6
  -> P7
  -> P8
  -> P9
  -> P10
  -> P11
  -> P12
  -> P13
  -> P14
  -> P15
  -> P16
```

However, the Director may adapt order if the active handoff requires immediate scientific continuation. In particular:

- P2-T01 may run immediately after P0 if the active frontier still requests `SourceMatterSemanticsAdoptionReadinessLaw_v1` stress.
- P6 through P9 may run before P4/P5 if claim-language drift threatens public overread.
- P4 and P5 should be sequenced by selector output, not plan inertia.
- P12 red-team may run before P4/P5 if the Director decides definitions need attack before further construction.
- P15 literature comparison may run earlier if a theoretical selector requires external constraints.

---

## 8. Task Routing Matrix

| Task family | Default role | Milestone | Human gate required | Promotion allowed |
|---|---|---|---|---|
| Plan intake | documentation/control | none | no | no |
| Status vocabulary | documentation/control | none | no | no |
| Readiness law stress | `refuter@0.2.0` | `matter_coupling` | no | no |
| Post-stress selector | `theoretical-continuation-selector@0.1.0` | `matter_coupling` | no | no |
| Gate Chair review | `gate-chair@0.1.0` | selected | yes, exact | only exact scoped verdict |
| Positive source semantics | `ontology-formalizer@0.2.0` or `candidate-constructor@0.2.0` | `matter_coupling` | no unless adoption | no automatic promotion |
| `RR_E` theorem | `ontology-formalizer@0.2.0`, `candidate-constructor@0.2.0`, `refuter@0.2.0` | `matter_coupling` | no unless adoption | no automatic promotion |
| Claim linter | project-system tooling | none | no | no |
| Validation reconciliation | project-system tooling | none | no | no |
| Public docs | `documentation-curator@0.1.0` | none | no | no |
| Formalization support | support/tooling role | none unless theorem attempt | no | no |
| Red-team | red-team role | selected | no | no |
| Literature comparison | literature-review role | selected | no | no |
| Final audit | project-system auditor | none | no | no |

---

## 9. Standard AgentJob Skeleton for v13 Physics Tasks

Use this skeleton unless a task-specific contract supersedes it:

```yaml
job_id: "AJ-<task>-001"
task_id: "<task>"
role_id: "<role>"
role_version: "<version>"
execution_mode: "parent_child_parallel_synthesis"
target_derivation_milestone: "<burden-map milestone>"
milestone_burden: "<exact burden>"
objective: "<bounded objective>"
claim_boundary:
  source_law_adopted: false
  source_extension_data_adopted_beyond_exact_scoped_gate_result: false
  MetricData_E_adopted: false
  scoped_geff_scope_changed: false
  coupling_law_adopted: false
  matter_semantics_adopted: false
  detector_semantics_adopted: false
  matter_coupling_derived: false
  matter_coupling_adopted: false
  stress_energy_semantics_imported: false
  stress_energy_tensor_constructed: false
  matter_action_imported: false
  einstein_equations_derived: false
  benchmark_promoted: false
  completed_derivation_claimed: false
required_inputs:
  - "<canonical source paths>"
expected_outputs:
  - "<task-local artifacts>"
validation_required:
  - "bootstrap_memory_system"
  - "bootstrap_memory_system --validate-only"
  - "validate_research_control"
  - "render_current_frontier --check"
  - "git diff --check"
```

---

## 10. Standard Completion Skeleton for v13 Physics Tasks

```yaml
completion_id: "AJC-<job>"
job_id: "<job>"
task_id: "<task>"
status: "completed"
physics_progress_status:
  status: "<precise scoped status>"
  target_derivation_milestone: "<milestone>"
  milestone_burden: "<burden>"
  explanation: "<positive result plus blocked overread>"
distance_to_gr_delta:
  changed: false
  burden_id: "<burden>"
  milestone: "<milestone>"
  ledger_row_updated: false
  explanation: "<why or why not>"
distance_to_gr_status:
  - burden: "Source ontology primitives"
    status: "<unchanged or exact change>"
  - burden: "M_src"
    status: "<unchanged or exact change>"
  - burden: "g_eff"
    status: "<unchanged or exact change>"
  - burden: "matter coupling"
    status: "<exact scoped result>"
  - burden: "Einstein equations"
    status: "blocked unless exact theorem supplied"
mathematical_payload_manifest:
  - payload_id: "<id>"
    payload_type: "<definition|lemma|theorem|witness|countermodel|obstruction|selector|audit|stress>"
    object_name: "<object>"
    source_path: "<artifact path>"
    burden_effect: "<narrows|constructs|stresses|obstructs|selects>"
forbidden_conclusion_summary:
  - "no source-law adoption"
  - "no matter-coupling derivation"
  - "no Einstein equations"
  - "no benchmark promotion"
  - "no completed derivation"
three_tier_claim_summary:
  adopted_objects: []
  accepted_evidence_preconditions: []
  open_or_blocked_physical_targets: []
  forbidden_overread: []
next_recommendation: "<exact next bounded route>"
```

---

## 11. Definition of Done for v13

V13 is complete only when:

1. Every phase has a completion or valid deferral record.
2. Every recommendation maps to completed tasks, superseded tasks, or explicit deferrals.
3. The active frontier uses scoped-positive language.
4. The claim-language linter exists or has a justified deferral.
5. Validation-status fields are no longer ambiguous.
6. Public-facing docs cannot imply that GR has already been derived.
7. `M_src` is not underclaimed.
8. scoped `g_eff` is not underclaimed.
9. `matter_coupling` is not overclaimed.
10. `SourceMatterSemanticsAdoptionReadinessLaw_v1` stress and post-stress selector state are either completed or explicitly superseded by newer tracked state.
11. `RR_E` has a theorem, obstruction route, or scheduled bounded continuation.
12. Repeated same-burden route orbits trigger freeze evaluation.
13. Support-only formalization has no proof-authority overread.
14. External red-team mode exists or has a scheduled bounded pilot.
15. The final current frontier, Distance-to-GR ledger, registries, generated derivatives, and validation reports agree.
16. The final handoff names exactly one next ordinary research continuation route.

---

## 12. Final Implementation Guardrail

The safest possible v13 implementation posture is:

```text
Claim scoped wins strongly.
Block downstream overread fiercely.
Continue by bounded packets only.
Freeze repeated route orbits.
Do not confuse workflow success with physics proof.
Do not confuse guard certificates with positive matter theory.
Do not confuse scoped evidence/precondition with adoption.
Do not confuse scoped source-extension g_eff with an unscoped Lorentzian metric.
Do not confuse source-only M_src with target GR spacetime.
```

That is the project’s control spine. Every task in this plan exists to keep it from bending.
