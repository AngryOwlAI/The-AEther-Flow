<!-- authority: implementation_plan -->

# Recommendations Implementation Plan for `/continue-research`, v16

**Filename:** `recommendations_implementation_plan_continue_task-v16.md`  
**Intended repository path:** `implementations_plans/recommendations_implementation_plan_continue_task-v16.md`  
**Generated date:** 2026-07-04  
**Plan ID:** `recommendations_implementation_plan_continue_task-v16`  
**Implementation driver:** Continue Research functionality only  
**Primary implementation lane:** `research_control/` bounded transactions  
**Plan status:** implementation guidance, not physics authority  
**Source recommendation set:** external project analysis section **“6. Recommendations”**  
**Baseline assumed by this plan:** post-`RT-20260704-019`, post-`handoff-0565`, v15 complete  
**Baseline current status assumed:** `v15_complete_selected_matter_coupling_dag_next_edge_theorem_route_no_physics_delta`  
**Immediate required next research route:** one bounded `theoretical-continuation-selector@0.1.0` packet for `matter_coupling_dag_next_edge_theorem_route_selection`.

---

## 0. Executive Implementation Intent

This v16 implementation plan converts **all recommendations** in the external project analysis section **“6. Recommendations”** into a sequence of bounded local AI-agent tasks.

The v16 plan is deliberately post-v15. It assumes v15 completed the recommendation-control implementation, strengthened validation, built the matter-coupling dependency DAG, preserved scoped source-side evidence boundaries, and selected the next ordinary route:

```text
matter_coupling_dag_next_edge_theorem_route
```

v16 now turns that route into payload-bearing research. The plan’s central discipline is:

```text
The next research step must be bounded, source-backed, and mathematically payload-bearing.
It must not become another pure control orbit unless a validator failure, documentation-impact requirement,
or protected authority boundary forces a project-system repair.
```

v16 has five major goals:

1. **Execute the selected post-v15 route exactly.**  
   The first live task is not a theorem proof. It is the one bounded matter-coupling DAG next-edge selector selected by `handoff-0565`.

2. **Make the selected theorem route payload-bearing.**  
   The selected route must require new mathematical content: definitions, theorem targets, proof attempts, explicit finite/local witnesses, countermodels, executable specs, or attack fixtures.

3. **Move from abstract certificate grammar toward concrete certificate instances.**  
   v15 built source certificate vocabulary and fail-closed algebra. v16 must create explicit finite/local examples and attack them.

4. **Reduce orbit risk.**  
   v15 added route-orbit diagnostics. v16 must make orbit detection operationally gating for repeated no-payload cycles.

5. **Preserve public-safe claim boundaries.**  
   v16 must continue to say, without embarrassment or fog, that matter coupling, detector semantics, stress-energy/action, Einstein equations, benchmark promotion, and completed GR derivation remain unestablished unless a later protected authority proves otherwise.

This plan is written for local agents. It is not a narrative essay, not a publication, and not a physics proof.

Every phase and task below must be implemented through the repository’s **Continue Research** functionality. No phase is a manual-edit permission slip. No phase bypasses the Director of Research, AgentJob contracts, claim-boundary registries, validators, or handoff discipline.

---

## 1. Non-Authority Warning

This Markdown file is an implementation plan. It is not:

- a physics proof;
- a mathematical proof;
- a canonical ontology edit;
- a source-law adoption;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption;
- unrestricted `RR_E` theorem authority;
- `PositiveMSProfile_v1` adoption;
- `SourceMatterSemanticsAdoptionReadinessLaw_v1` adoption as law;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- universal matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor construction;
- matter-action construction;
- Einstein-equation derivation;
- exact-GR benchmark promotion;
- benchmark closure by protected authority;
- completed-derivation evidence;
- future source-extension impossibility;
- program-wide rejection claim;
- permission to bypass Continue Research;
- permission to bypass human-gated authority;
- permission to treat validator PASS, role identity, generated derivatives, registries, handoffs, approvals, commits, file order, or `.local/` cache state as scientific proof.

All local agents implementing this plan must preserve this hard boundary unless a later tracked protected authority explicitly changes it:

```text
No source-law adoption.
No RR_ETransportCompletenessOrInvarianceLaw_v1 adoption.
No unrestricted RR_E theorem.
No detector-semantics collapse.
No matter-semantics adoption.
No coupling-law adoption.
No matter-coupling derivation or adoption.
No stress-energy semantics.
No stress-energy tensor.
No matter action.
No Einstein equations.
No benchmark promotion.
No completed derivation.
```

---

## 2. Required Starting-State Verification

Before executing any v16 task, the local Director of Research must inspect the current tracked state from at least:

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `research_control/program_state.yaml`
- `research_control/current_frontier.md`
- latest handoff named by `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0565.yaml`
- `research_control/handoffs/handoff-0565.md`
- `research_control/tasks/RT-20260704-019/00_TASK.yaml`
- `research_control/tasks/RT-20260704-019/DDR-20260704-019.md`
- `research_control/tasks/RT-20260704-019/jobs/AJ-RT-20260704-019-001.yaml`
- `research_control/tasks/RT-20260704-019/jobs/completions/AJC-AJ-RT-20260704-019-001.yaml`
- `research_control/tasks/RT-20260704-019/artifacts/v15_ordinary_continuation_selection.md`, if present
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `research_control/design/gr_derivation_burden_map.md`
- `research_control/design/matter_coupling_dependency_dag_v1.md`
- `research_control/design/matter_coupling_dependency_dag_schema_v1.md`
- `research_control/design/source_certificate_algebra_checklist.md`
- `research_control/design/source_certificate_operation_laws_v1.md`, if registered as a design copy or source path
- `research_control/design/source_extension_classification_checklist_v1.md`
- `research_control/design/refuter_obstruction_schema_v1.md`
- `research_control/design/route_signature_schema_v1.md`
- `research_control/design/einstein_equation_route_moratorium_v1.md`
- `research_control/design/validation_command_inventory_v15.md`
- `research_control/design/claim_graph_schema_v1.md`
- `research_control/design/public_status_exists_does_not_exist_source_spec.md`
- `research_control/design/epistemic_category_glossary.md`
- `research_control/design/negative_result_inventory_v15.md`
- `implementations_plans/recommendations_implementation_plan_continue_task-v15.md`
- this v16 plan once added at `implementations_plans/recommendations_implementation_plan_continue_task-v16.md`.

If any exact path has been superseded, renamed, regenerated, or moved, the Director must locate the canonical equivalent through tracked registries, generated source registries, and latest handoff evidence.

Generated wiki notes, PDFs, generated HTML, semantic extracts, Obsidian notes, SQLite indexes, and `.local/` caches are retrieval aids only. They do not replace canonical source inspection.

---

## 3. Assumed Current State for v16

This plan assumes the following active state at generation time:

| Field | Assumed value |
| --- | --- |
| Active task | `RT-20260704-019` |
| Latest handoff | `handoff-0565` |
| Current status | `v15_complete_selected_matter_coupling_dag_next_edge_theorem_route_no_physics_delta` |
| Current route family | `v15_final_ordinary_continuation_handoff` completed |
| Immediate next route | bounded `theoretical-continuation-selector@0.1.0` matter-coupling DAG next-edge selector |
| Selected next route ID | `matter_coupling_dag_next_edge_theorem_route` |
| Active milestone for next selector | `matter_coupling` |
| Immediate selector burden | select the next theorem edge from the matter-coupling dependency DAG under existing hard blocks |
| Physics promotion authorized | false |
| Source-law adoption authorized | false |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption authorized | false |
| `PositiveMSProfile_v1` adoption authorized | false |
| Matter-semantics adoption authorized | false |
| Detector-semantics adoption authorized | false |
| Coupling-law adoption authorized | false |
| Universal matter-coupling derivation status | false |
| Einstein-equation derivation status | false |
| Exact-GR benchmark promotion authorized | false |
| Completed derivation claimed | false |

If any assumption is stale, P0 must adapt by source evidence. Do not replay completed work. Do not skip required synchronization merely because a later physics packet exists. If a later tracked state already completed a v16 task, mark that task `implemented_by_later_tracked_state` with exact source evidence and continue.

---

## 4. Universal Continue Research Protocol

Every task in this plan is one bounded `/continue-research` transaction unless the live tracked state proves that the task has already been implemented by a later transaction.

Before every task-routing decision, run:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "<task-specific targeted phrase>" --limit 10 --json
.venv/bin/python scripts/research_control/continue_research.py --json
```

If memory search returns relevant objects, inspect the canonical source files or registry rows named by the hits. Memory hits may guide retrieval; they are not authority.

For every v16 task:

1. Use the Director of Research as routing authority.
2. Create exactly one Director Decision Record unless a valid active DDR already exists for the exact task.
3. Create exactly one outer AgentJob.
4. Choose the narrowest role that can complete the task.
5. Preserve active claim boundaries.
6. Use `parent_child_parallel_synthesis` for physics AgentJobs governed by the post-2026-06-17 physics contract.
7. For physics tasks, declare `target_derivation_milestone` and `milestone_burden` from the burden map.
8. For physics completions, include at least one `new_mathematical_payload` unless the task is explicitly a selector, validation packet, repair packet, or freeze review.
9. For selectors, include a scoring or comparison matrix and select exactly one route.
10. For project-system tasks, state explicitly that the task changes control, tooling, validation, documentation, or methodology only and does not promote physics claims.
11. Do not route Gate Chair work unless exact tracked human authorization exists and the live handoff or Director DDR identifies the protected question.
12. If a task emits project-improvement signals, preserve the normal research handoff and emit a sidecar only if current project rules require it.
13. Include `physics_progress_status`, `distance_to_gr_delta`, `mathematical_payload_manifest`, and `forbidden_conclusion_summary` whenever the task touches a physics milestone.
14. Include documentation-impact validation or a no-op rationale for state-changing project-system tasks.
15. Run the active research-control validator and changed-claim-language checks before checkpoint.
16. Write a completion YAML and handoff for every task.
17. Do not use generated memory, wiki notes, validator PASS, or file order as scientific premises.

Minimum post-write validation set unless the AgentJob narrowly justifies a different validator list:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/project_control/validate_documentation_impact.py --json
.venv/bin/python scripts/project_control/validate_claim_language.py --changed --json
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
git diff --check
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py --job-id <JOB_ID>
```

Additional validators that should be included whenever relevant:

```zsh
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_dependency_graph.py --check
.venv/bin/python scripts/research_control/validate_claim_graph_v1.py --json
.venv/bin/python scripts/research_control/validate_route_orbits.py --sample recent-matter-rr-e --json --advisory-only
.venv/bin/python scripts/research_control/extract_route_signatures.py --sample recent-matter-coupling --json
```

If a validator path has moved, use the canonical current equivalent.

---

## 5. V16 Recommendation Map

The recommendations from external analysis section **“6. Recommendations”** are mapped here as `V16-R01` through `V16-R15`.

| ID | Recommendation | Main phases | Primary outputs | Physics promotion allowed |
| --- | --- | --- | --- | --- |
| `V16-R01` | Execute the next route exactly, but make it mathematically payload-bearing. | P0, P1, P2, P3, P17 | v16 plan intake, baseline lock, DAG edge selector, selected theorem route | No |
| `V16-R02` | Build a concrete certificate-instance library. | P4, P6, P15 | finite/local certificate instances and attack fixtures | No |
| `V16-R03` | Separate definitional equivalence from theorem content. | P5, P3, P17 | equivalence refactor theorem target and definitions | No |
| `V16-R04` | Formalize certificate algebra incrementally. | P6 | support-only executable/formal specs and tests | No |
| `V16-R05` | Promote route-orbit detection from advisory to selectively gating. | P7, P17 | route-orbit gating policy and validator integration | No |
| `V16-R06` | Add a minimum physics payload gate for post-v15 tasks. | P7, P17 | minimum payload schema and validation fixtures | No |
| `V16-R07` | Make the next DAG edge selector rank edges by burden discharge potential. | P2 | DAG edge scoring rubric and selector artifact | No |
| `V16-R08` | Rename risky status fields in future schemas. | P8 | layered status-field migration and compatibility aliases | No |
| `V16-R09` | Keep `EqSrc`, `RetainH`, and `GenH` on the horizon, not immediate lane. | P9 | trigger list and routing policy | No |
| `V16-R10` | Build a source model zoo. | P10, P4 | finite/local source model zoo and model registry | No |
| `V16-R11` | Make negative results reader-facing but not sensational. | P11 | negative-result reader brief update and wording guard | No |
| `V16-R12` | Split manuscripts exactly as planned. | P12 | physics and AI manuscript continuation packets | No |
| `V16-R13` | Prepare external red-team review around one concrete question. | P13 | one-question red-team packet and review template | No |
| `V16-R14` | Introduce a target-import attack suite. | P14, P6 | attack-suite fixtures and validator integration | No |
| `V16-R15` | Make current frontier more machine-summarizable. | P15, P17 | current frontier compact YAML/JSON summary and render check | No |
| all | Final integration audit and ordinary continuation handoff. | P17 | coverage audit, final validation, next route | No |

---

## 6. Phase Overview

| Phase | Name | Implementation purpose | Recommendation IDs |
| --- | --- | --- | --- |
| P0 | V16 plan intake and post-v15 baseline lock | Register v16 plan and verify live post-v15 state. | all |
| P1 | V16 trace matrix and route-readiness audit | Convert all recommendations into tracked implementation evidence and verify selector readiness. | all, R01 |
| P2 | Matter-coupling DAG next-edge selector with ranking | Execute the handoff-selected next route exactly and select one theorem edge. | R01, R07 |
| P3 | Payload-bearing selected theorem-route packet | Execute or prepare the theorem route selected by P2, preferably coupling-law target specification. | R01, R03, R07 |
| P4 | Concrete certificate-instance library | Build explicit finite/local transport, invariance, factorization, missing, malformed, and target-import certificate examples. | R02, R10 |
| P5 | Equivalence/theorem-content separation | Refactor definitional equivalence from theorem content and establish nontrivial theorem obligations. | R03 |
| P6 | Incremental formalization and executable certificate checks | Extend support-only formalization of certificate algebra and fixture tests. | R04, R14 |
| P7 | Selectively gating route-orbit and minimum-payload enforcement | Convert advisory orbit/payload signals into bounded gates after repeated no-payload cycles. | R05, R06 |
| P8 | Risky status-field rename and schema-layering | Replace ambiguous status fields with layered, scoped, compatibility-safe names. | R08 |
| P9 | `EqSrc`/`RetainH`/`GenH` trigger-horizon policy | Keep upstream primitives on a precise trigger list, not an immediate default route. | R09 |
| P10 | Source model zoo | Create finite/local source models that exercise certificates, obstructions, and target-import failures. | R10, R02 |
| P11 | Negative-result reader-facing update | Make negative results visible without sensational/global-no-go overread. | R11 |
| P12 | Manuscript split continuation | Continue two manuscript lanes with exact physics/AI separation. | R12 |
| P13 | One-question red-team packet | Prepare review around a concrete, hard, bounded question. | R13 |
| P14 | Target-import attack suite | Build attack fixtures for hidden target/detector/stress-energy/process imports. | R14 |
| P15 | Compact current-frontier machine summary | Add machine-readable active-state and burden summary. | R15 |
| P16 | Project-system integration bridge | Integrate any validator/schema/docs changes and route project-improvement sidecars if needed. | R05, R06, R08, R15 |
| P17 | Final v16 audit, validation, and handoff | Validate all recommendations and select exactly one next route. | all |

---

## 7. Implementation Order Rules

Default implementation order:

```text
P0 → P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8 → P9 → P10 → P11 → P12 → P13 → P14 → P15 → P16 → P17
```

Allowed deviations:

1. If P0 proves a later tracked state already completed a phase, mark it `implemented_by_later_tracked_state` and continue.
2. If P2 selects a different theorem edge than the preferred coupling-law target specification, P3 must adapt to that selected edge while preserving the same payload requirements.
3. If P2 fails because the DAG is stale, route exactly one repair or refresh packet before repeating P2.
4. If P3 produces a hard obstruction, P4 and P5 may be adapted to focus on the obstruction and certificate/model fixtures.
5. If P7 discovers an active route-orbit hard gate, execute a freeze-review or selector task before continuing same-burden theoretical packets.
6. If a validator failure appears in any phase, route exactly one repair task before continuing.
7. If a protected human gate is required, do not simulate approval. Record the human-gated route and select an allowed non-promotional next step.
8. If manuscript or public-documentation tasks require documentation-impact updates, run those through Continue Research as project-system/documentation transactions.
9. If local scripts or schemas have been renamed since v15, use the canonical current equivalents and record the mapping.

---

# P0 — V16 Plan Intake and Post-v15 Baseline Lock

## P0 purpose

P0 introduces this v16 plan as implementation guidance and verifies that the repository is actually in the expected post-v15 state. P0 must not execute new physics. It may register the v16 plan, create a trace matrix, and route the first post-v15 selector task.

---

## P0-T01 — Register v16 implementation plan

**Continue Research transaction:** required  
**Recommended role:** `project-control-maintainer@0.2.0` or narrow task overlay  
**Task type:** `v16_plan_intake_and_registration`  
**Objective:** Add this plan at `implementations_plans/recommendations_implementation_plan_continue_task-v16.md` and register it as implementation guidance, not physics authority.

### Mandatory reads

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `implementations_plans/recommendations_implementation_plan_continue_task-v15.md`
- `research_control/program_state.yaml`
- latest handoff named by program state
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `research_control/current_frontier.md`
- `registries/RESEARCH_TASK_REGISTRY.csv`

### Allowed writes

- `implementations_plans/recommendations_implementation_plan_continue_task-v16.md`
- task-local files under `research_control/tasks/<new_task_id>/`
- registry rows required to register this Markdown source
- generated memory/wiki derivatives if normal bootstrap produces them
- current handoff if the transaction changes active state

### Required output files

- `research_control/tasks/<task_id>/00_TASK.yaml`
- `research_control/tasks/<task_id>/DDR-<decision_id>.md`
- `research_control/tasks/<task_id>/jobs/<job_id>.yaml`
- `research_control/tasks/<task_id>/roles/<role_execution_ref>.yaml`
- `research_control/tasks/<task_id>/jobs/completions/<completion_id>.yaml`
- `research_control/tasks/<task_id>/documentation_impact.yaml`
- updated source registry row if required
- new handoff YAML and Markdown if active state advances

### Claim boundary

```text
This task registers implementation guidance only. It creates no physics proof, no source-law adoption, no matter-semantics adoption, no detector-semantics adoption, no coupling-law adoption, no matter-coupling derivation, no Einstein equations, no benchmark promotion, and no completed derivation.
```

### Done criteria

- v16 plan is present at the intended path.
- Markdown source registry is updated if repository rules require it.
- Documentation-impact receipt exists or a no-update rationale is valid.
- Validators pass.
- Completion states `distance_to_gr_delta: none`.

---

## P0-T02 — Post-v15 baseline reconciliation

**Continue Research transaction:** required  
**Recommended role:** `process-integrity-auditor@0.1.0` or `project-control-maintainer@0.2.0`  
**Task type:** `v16_post_v15_baseline_reconciliation`  
**Objective:** Verify whether the assumed post-v15 baseline remains current. If live state has advanced, adapt v16 by exact tracked evidence rather than replaying stale tasks.

### Mandatory reads

- `research_control/program_state.yaml`
- latest handoff named by program state
- active task path
- active completion path
- `research_control/current_frontier.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `research_control/design/matter_coupling_dependency_dag_v1.md`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`

### Required artifact

`research_control/tasks/<task_id>/artifacts/v16_post_v15_baseline_reconciliation_report.md`

The report must include:

- active task ID;
- latest handoff ID;
- current status;
- latest selected next route;
- whether v15 is complete;
- whether the matter-coupling DAG next-edge selector has already run;
- whether any v16 recommendation is already implemented by later tracked state;
- exact evidence for all baseline conclusions;
- exact next action.

### Allowed verdicts

- `baseline_matches_v16_assumption`
- `baseline_advanced_adapt_v16`
- `baseline_conflict_requires_repair`
- `baseline_inconclusive_requires_manual_source_inspection`

### Claim boundary

No physics promotion. Baseline reconciliation is routing-control evidence only.

### Done criteria

- Report includes a verdict.
- If stale, it maps which phases are already implemented.
- Completion hands off to P1 or to a source-evidenced adapted equivalent.

---

## P0-T03 — V16 recommendation trace matrix

**Continue Research transaction:** required  
**Recommended role:** `project-control-maintainer@0.2.0`  
**Task type:** `v16_recommendation_trace_matrix`  
**Objective:** Create a machine-checkable trace matrix mapping every `V16-Rxx` recommendation to planned phases, tasks, output artifacts, and validators.

### Required artifact

`research_control/tasks/<task_id>/artifacts/v16_recommendation_trace_matrix.csv`

Required columns:

```csv
recommendation_id,recommendation_text,primary_phase,primary_task,secondary_tasks,expected_output_paths,validator_or_receipt,physics_promotion_allowed,status,implementation_evidence_path,next_route_if_partial
```

### Done criteria

- All `V16-R01` through `V16-R15` are present.
- Every row says `physics_promotion_allowed=false`.
- Rows for deferred, superseded, or already-completed recommendations include exact evidence.
- Completion hands off to P1.

---

# P1 — V16 Route-Readiness Audit

## P1 purpose

P1 verifies that the matter-coupling DAG, current frontier, Distance-to-GR ledger, and latest handoff are ready to support the first v16 route selector. It is a preflight gate for `V16-R01` and `V16-R07`.

---

## P1-T01 — Matter-coupling DAG readiness audit

**Continue Research transaction:** required  
**Recommended role:** `process-integrity-auditor@0.1.0`  
**Task type:** `matter_coupling_dag_readiness_audit_v16`  
**Objective:** Verify that `research_control/design/matter_coupling_dependency_dag_v1.md` is fresh, populated, source-backed, and sufficient for a next-edge selector.

### Mandatory checks

The audit must verify:

1. The DAG artifact exists.
2. The DAG schema artifact exists.
3. Each node has a source evidence path.
4. Each edge has a source evidence path.
5. High-risk nodes do not use bare `accepted`.
6. Blocked physical targets list exact missing burdens.
7. Detector semantics remains blocked.
8. Coupling-law target remains blocked.
9. Stress-energy/action targets remain blocked.
10. Universal matter-coupling derivation remains blocked.
11. Einstein-equation dependency remains blocked.
12. Benchmark promotion remains blocked.
13. No node or edge converts scoped evidence/precondition into adoption.
14. The current frontier’s next route agrees with latest handoff.
15. The Distance-to-GR ledger agrees with high-risk DAG statuses.

### Required artifact

`research_control/tasks/<task_id>/artifacts/matter_coupling_dag_readiness_audit_v16.md`

### Allowed verdicts

- `PASS_ready_for_next_edge_selector`
- `PASS_ready_with_advisory_warnings`
- `FAIL_dag_refresh_required`
- `FAIL_claim_boundary_conflict`
- `INCONCLUSIVE_missing_authority_source`

### Done criteria

- Audit verdict exists.
- If the verdict is not ready, P1-T02 is selected as the next route.
- If ready, handoff names P2-T01 as the next route.
- No physics delta.

---

## P1-T02 — DAG/frontier refresh repair

**Continue Research transaction:** required if P1-T01 fails readiness  
**Recommended role:** `project-control-maintainer@0.2.0` or `validator-engineer@0.2.0`  
**Task type:** `matter_coupling_dag_frontier_refresh_repair_v16`  
**Objective:** Refresh the matter-coupling DAG, current frontier, dependency graph, or registries only as needed to make the next-edge selector lawful.

### Allowed repair classes

- re-render current frontier from tracked state;
- re-render dependency graph;
- update generated DAG derivative from tracked source;
- repair missing source registry references;
- add missing overread guards if a registered control source already requires them;
- route to a separate project-system repair if schema conflict is discovered.

### Forbidden repair classes

- adding new physics results;
- treating DAG refresh as derivation;
- changing Distance-to-GR status without source-backed authority;
- adopting matter semantics, detector semantics, coupling law, matter coupling, Einstein equations, or benchmark promotion.

### Required artifact

`research_control/tasks/<task_id>/artifacts/matter_coupling_dag_frontier_refresh_repair_v16.md`

### Done criteria

- Repair receipt lists changed paths.
- Render/check validators pass.
- No physics delta.
- Handoff returns to P2-T01.

---

# P2 — Matter-Coupling DAG Next-Edge Selector with Ranking

## P2 purpose

P2 executes the exact next route selected by `handoff-0565`: one bounded `theoretical-continuation-selector@0.1.0` matter-coupling DAG next-edge theorem route selection packet.

This phase implements:

- `V16-R01`: execute the next route exactly;
- `V16-R07`: rank edges by burden-discharge potential.

P2 is a selector phase. It must not execute the selected theorem edge. It must select exactly one next theorem edge and define the payload requirement for the next packet.

---

## P2-T01 — DAG edge scoring rubric

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0`  
**Task type:** `matter_coupling_dag_next_edge_scoring_rubric_v16`  
**Objective:** Define the scoring rubric used by the next-edge selector.

### Required artifact

`research_control/tasks/<task_id>/artifacts/matter_coupling_dag_next_edge_scoring_rubric_v16.md`

### Required scoring dimensions

Each candidate edge must be scored on:

| Score dimension | Meaning | Score direction |
| --- | --- | --- |
| `burden_discharge_potential` | Ability to reduce a named blocked burden without overread. | higher is better |
| `available_source_inputs` | How many required inputs already exist as tracked source-side material. | higher is better |
| `certificate_instance_feasibility` | Likelihood that explicit finite/local certificates or witnesses can be constructed. | higher is better |
| `target_import_risk` | Risk of importing target metric, detector semantics, stress-energy, benchmark behavior, or process authority. | lower is better |
| `dependency_on_missing_eqsrc_retainh_genh` | Whether broad upstream primitives are required now. | lower is better |
| `refuter_testability` | Whether the result can be attacked by a bounded Refuter task. | higher is better |
| `formalization_feasibility` | Whether support-only tests or typed specs can cover the object. | higher is better |
| `route_orbit_risk` | Risk of repeating no-payload boundary work. | lower is better |
| `public_overread_risk` | Risk that readers will overread the output. | lower is better |
| `distance_to_gr_specificity` | Whether the edge names an exact missing burden in the Distance-to-GR structure. | higher is better |

### Required candidate edge set

At minimum, score these candidate edges from the DAG if present:

1. `mc_source_matter_semantics_equivalence_theorem` → `mc_coupling_law_target`
2. `mc_detector_semantics_target` → `mc_universal_matter_coupling_derivation`
3. `mc_coupling_law_target` → `mc_universal_matter_coupling_derivation`
4. `mc_stress_energy_semantics_target` → `mc_stress_energy_tensor_target`
5. `mc_stress_energy_tensor_target` → `mc_matter_action_target`
6. `mc_matter_action_target` → `mc_einstein_equation_dependency`
7. `mc_universal_matter_coupling_derivation` → `mc_einstein_equation_dependency`
8. `mc_certificate_gap_obstruction` → `mc_source_matter_semantics_equivalence_theorem`
9. `mc_rr_e_certificate_boundary` → `mc_source_matter_semantics_equivalence_theorem`
10. any newly recorded edge found by live DAG inspection.

### Default recommendation

Unless live evidence changes the scoring, this plan recommends that P2 select:

```text
mc_source_matter_semantics_equivalence_theorem → mc_coupling_law_target
```

as a theorem-route edge for:

```text
source_side_coupling_law_target_specification_under_explicit_certificates
```

This default route is narrow, close to v15 certificate machinery, and can produce a finite/local target specification without adopting a coupling law.

### Done criteria

- Scoring rubric exists.
- Every candidate edge has a score.
- The artifact states that scores are route-selection evidence only, not physics proof.
- Handoff proceeds to P2-T02.

---

## P2-T02 — Matter-coupling DAG next-edge selector

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0`  
**Task type:** `matter_coupling_dag_next_edge_theorem_route_selection_v16`  
**Objective:** Select exactly one next theorem edge from the matter-coupling dependency DAG under all existing hard blocks.

### Required artifact

`research_control/tasks/<task_id>/artifacts/matter_coupling_dag_next_edge_selector_v16.md`

### Required sections

1. Active state summary.
2. DAG source inspection.
3. Candidate edge list.
4. Scoring matrix.
5. Selected edge.
6. Selected theorem-route family.
7. Selected next role family.
8. Required mathematical payload for selected next task.
9. Required Refuter stress route after selected task.
10. Required formalization/support-only route if applicable.
11. Forbidden conclusions.
12. Distance-to-GR effect.
13. Exact handoff.

### Selected route constraints

The selected route must:

- be exactly one edge;
- target `matter_coupling`;
- require no direct physics promotion;
- require no canonical ontology edit;
- require no source-law adoption;
- require no matter-semantics adoption;
- require no detector-semantics adoption;
- require no coupling-law adoption;
- require no matter-coupling derivation/adoption;
- require no stress-energy semantics;
- require no matter action;
- require no Einstein equations;
- require no benchmark promotion;
- require no completed derivation.

### Required next-packet burden if default edge selected

If the selected edge is the recommended coupling-law target edge, the next packet must be:

```yaml
route_id: "source_side_coupling_law_target_specification_under_explicit_certificates"
role_family: "ontology-formalizer@0.2.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: >
  Define a source-side coupling-law target specification that states what a
  future coupling law candidate would have to provide under explicit source
  certificates, without adopting a coupling law or deriving matter coupling.
requires_human_gate: false
```

### Done criteria

- Exactly one route selected.
- Completion records `distance_to_gr_delta: none`.
- Handoff points to P3 adapted to the selected edge.
- No theorem execution occurs in this task.

---

# P3 — Payload-Bearing Selected Theorem-Route Packet

## P3 purpose

P3 implements the theorem-route packet selected by P2. If P2 selects the default recommended edge, P3 creates a source-side coupling-law target specification under explicit certificates.

This phase implements `V16-R01`, supports `V16-R03`, and operationalizes `V16-R07`.

If P2 selects a different edge, the Director must adapt P3 by preserving the same structure: exact edge, explicit source objects, theorem target, proof attempt or obstruction, finite/local witness obligation, Refuter stress obligation, and no downstream promotion.

---

## P3-T01 — Selected theorem-route packet setup

**Continue Research transaction:** required  
**Recommended role:** `director-of-research@0.3.0` task overlay  
**Task type:** `selected_matter_coupling_dag_edge_theorem_packet_setup_v16`  
**Objective:** Create the exact bounded AgentJob for the theorem route selected by P2.

### Mandatory reads

- P2 selector artifact;
- `research_control/design/matter_coupling_dependency_dag_v1.md`;
- `research_control/design/source_certificate_algebra_checklist.md`;
- `research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex`;
- `research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex`;
- `research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex`;
- `research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex`;
- `research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex`;
- `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`;
- current frontier and Distance-to-GR ledger.

### Required AgentJob fields

```yaml
target_derivation_milestone: "matter_coupling"
milestone_burden: "<selected edge burden from P2>"
role_decomposition:
  mode: "parent_child_parallel_synthesis"
physics_progress_contract:
  requires_new_mathematical_payload: true
  distance_to_gr_delta_required: true
  mathematical_payload_manifest_required: true
  forbidden_conclusion_summary_required: true
  refuter_followup_required: true
proof_authority: false
support_only: false
physics_promotion_authorized: false
```

### Required artifact

`research_control/tasks/<task_id>/artifacts/selected_matter_coupling_dag_edge_theorem_packet_setup_v16.md`

### Done criteria

- AgentJob is ready.
- It names exact selected edge and target theorem packet.
- It requires new mathematical payload.
- It blocks all downstream promotion.

---

## P3-T02 — Source-side coupling-law target specification, default route

**Continue Research transaction:** required if P2 selects the recommended default edge  
**Recommended role:** `ontology-formalizer@0.2.0`  
**Task type:** `source_side_coupling_law_target_specification_under_explicit_certificates`  
**Objective:** Define a source-side coupling-law target specification that says what a future source-side coupling-law candidate must provide, without adopting such a law.

### Required mathematical payload

A new artifact, preferably TeX, that defines:

```text
SourceCouplingLawTarget_src^cand_v1
SourceCouplingLawCertificateBundle_v1
SourceMatterSemanticsInputScope_v1
DetectorSemanticsReplacementPlaceholder_v1
NoTargetCouplingImportGuard_v1
CouplingLawCandidateValidityPredicate_v1
CouplingLawCandidateFailClosedBranch_v1
FiniteLocalCouplingWitnessObligation_v1
```

The artifact may adapt names to current project terminology. It must include a canonical name map if names differ.

### Required theorem/definition targets

The packet must state, attempt, prove conditionally, or fail precisely:

1. **Target specification definition.**  
   A source-side coupling-law target is a record of declared source objects, certificate bundle requirements, no-target guards, and explicit blocked overreads.

2. **Certificate sufficiency non-theorem.**  
   Existing source-side matter-semantics equivalence and certificate algebra are necessary context but not sufficient for coupling-law adoption.

3. **Future candidate validity predicate.**  
   A future candidate may be tested against explicit source-certificate inputs, detector-semantics boundary, no-target guards, and fail-closed branches.

4. **Finite/local witness obligation.**  
   A future positive packet must provide a finite/local witness or explain why one is impossible within the current route.

5. **Fail-closed obstruction.**  
   Missing detector semantics or source-side replacement, missing coupling relation, target import, process-authority substitution, or scoped evidence-as-adoption causes failure, not promotion.

### Required artifact

`research_control/tasks/<task_id>/artifacts/source_side_coupling_law_target_specification_v1.tex`

### Required sections

- Control status.
- Source evidence basis.
- Definitions.
- Candidate target specification.
- Certificate bundle requirement.
- Detector-semantics boundary.
- No-target import guard.
- Finite/local witness obligation.
- Fail-closed branches.
- Relation to existing `SourceCouplingLawCandidate^cand_v1`.
- Relation to `NarrowMSCertEq_v1`.
- Relation to `RR_E` certificate boundary.
- Distance-to-GR effect.
- Forbidden conclusions.
- Next route.

### Allowed positive status

```text
draft_control_coupling_law_target_specification_only
```

or:

```text
conditional_source_side_coupling_law_target_specification_candidate
```

### Forbidden statuses

- `coupling_law_adopted`
- `matter_coupling_derived`
- `matter_coupling_adopted`
- `detector_semantics_adopted`
- `stress_energy_semantics_available`
- `einstein_equations_derived`
- `benchmark_promoted`
- `completed_derivation`

### Done criteria

- Artifact defines the target specification.
- It does not adopt a coupling law.
- It names exact missing burdens for future candidate construction.
- It includes at least one formal fail-closed branch.
- Completion includes new mathematical payload.
- Handoff selects P3-T03 Refuter stress.

---

## P3-T03 — Selected theorem-route smuggling audit

**Continue Research transaction:** required  
**Recommended role:** `smuggling-auditor@0.2.0`  
**Task type:** `selected_matter_coupling_edge_theorem_smuggling_audit_v16`  
**Objective:** Audit the P3 theorem-route artifact for hidden target imports, detector imports, stress-energy imports, process authority, and status laundering.

### Required audit targets

- target metric;
- target topology;
- target atlas;
- Lorentzian signature;
- detector semantics;
- empirical readout semantics;
- stress-energy semantics;
- stress-energy tensor;
- matter action;
- Einstein equations;
- benchmark behavior;
- validator status;
- Gate Chair status outside exact scoped evidence role;
- generated memory/wiki status;
- source-extension status as derivation.

### Required artifact

`research_control/tasks/<task_id>/artifacts/selected_matter_coupling_edge_smuggling_audit_v16.tex`

### Allowed verdicts

- `source_pure_as_written_pending_refuter_stress`
- `conditional_source_pure_with_repair_required`
- `target_import_detected_fail_closed`
- `detector_semantics_import_detected_fail_closed`
- `stress_energy_import_detected_fail_closed`
- `status_laundering_detected_fail_closed`

### Done criteria

- Verdict is unambiguous.
- Any repair route is exact.
- No physics promotion.

---

## P3-T04 — Selected theorem-route Refuter stress

**Continue Research transaction:** required  
**Recommended role:** `refuter@0.2.0`  
**Task type:** `selected_matter_coupling_edge_theorem_refuter_stress_v16`  
**Objective:** Stress-test the selected theorem-route artifact and produce a minimal countermodel, witness gap, or obstruction.

### Required stress dimensions

If default coupling-law target specification route was selected, stress:

- deletion of source-certificate bundle requirement;
- malformed coupling-law target record;
- detector-semantics collapse attempt;
- target metric import;
- stress-energy shortcut;
- matter-action shortcut;
- `NarrowMSCertEq_v1` as coupling-law adoption overread;
- `SourceCouplingLawCandidate^cand_v1` as law adoption overread;
- scoped evidence/precondition as matter-coupling derivation;
- process-authority proof laundering;
- finite/local target specification as universal coupling overread.

### Required artifact

`research_control/tasks/<task_id>/artifacts/selected_matter_coupling_edge_refuter_stress_v16.tex`

### Required minimal obstruction fields

```yaml
obstruction_id:
target_claim:
failed_premise:
smallest_failed_premise:
minimal_countermodel_available:
finite_local_witness_available:
repair_or_continuation_route:
global_no_go_authorized: false
future_source_extension_impossibility_authorized: false
matter_coupling_derived: false
```

### Done criteria

- Stress verdict is precise.
- The route either survives as a draft/control target specification or fails with a named obstruction.
- Completion routes to P3-T05 selector.

---

## P3-T05 — Post-selected-theorem route selector

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0`  
**Task type:** `post_selected_matter_coupling_edge_theorem_route_selector_v16`  
**Objective:** Select exactly one next route after P3 theorem/audit/stress.

### Candidate routes

- concrete certificate-instance library;
- repair P3 theorem-route artifact;
- build source model zoo first;
- formalize executable support-only checker;
- route to detector-semantics replacement target;
- route to coupling-law candidate construction;
- route to freeze if repeated no-payload obstruction occurred;
- route to project-system repair if validators failed.

### Default route

If P3 produced a valid draft/control coupling-law target specification with stress survival, select:

```text
concrete_certificate_instance_library
```

This default moves from abstract target specification into finite/local examples.

### Done criteria

- Exactly one next route selected.
- Handoff points to P4 or adapted route.
- No physics promotion.

---

# P4 — Concrete Certificate-Instance Library

## P4 purpose

P4 implements `V16-R02` and supports `V16-R10`. v15 created certificate definitions and operation laws. P4 creates explicit finite/local examples.

The library must not be rhetorical. It must contain actual source object tuples, certificate records, domains, codomains, guards, statuses, and fail-closed examples.

---

## P4-T01 — Certificate-instance library schema

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0` with `validator-engineer@0.2.0` consultation  
**Task type:** `source_certificate_instance_library_schema_v16`  
**Objective:** Define a schema for concrete finite/local certificate instances.

### Required artifact

`research_control/design/source_certificate_instance_library_schema_v1.md`

### Required instance fields

```yaml
certificate_instance_id:
instance_kind:
source_object_A:
source_object_B:
declared_context:
domain:
codomain:
source_labels:
source_guards:
response_tokens:
certificate_payload:
no_target_import_guard:
status:
expected_equivalence_result:
rr_e_separation_effect:
fail_closed_reason:
target_import_used: false
detector_semantics_used: false
stress_energy_used: false
matter_action_used: false
benchmark_behavior_used: false
process_authority_used: false
source_paths:
forbidden_overreads:
```

### Required instance kinds

- `valid_transport_certificate`
- `valid_invariance_certificate`
- `valid_factorization_certificate`
- `missing_certificate_negative`
- `malformed_certificate_negative`
- `target_import_rejected_certificate`
- `detector_semantics_rejected_certificate`
- `process_authority_rejected_certificate`

### Done criteria

- Schema is precise enough for fixtures and support-only validation.
- Schema states that concrete instances are finite/local examples, not universal matter coupling.
- No physics delta.

---

## P4-T02 — Valid transport certificate instance

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0`  
**Task type:** `finite_local_valid_transport_certificate_instance_v16`  
**Objective:** Construct one explicit finite/local valid source transport certificate instance.

### Required artifact

`research_control/tasks/<task_id>/artifacts/finite_local_transport_certificate_instance_v1.tex`

### Required content

- finite source context `E_src`;
- source object `A_src`;
- source object `B_src`;
- source labels;
- source guards;
- response-token family;
- explicit transport map;
- domain/codomain match;
- no-target-import certificate;
- equivalence result inside declared scope;
- proof or verification by direct finite check;
- fail-closed statement outside declared scope.

### Done criteria

- The instance is explicit, not schematic only.
- No target metric, detector semantics, stress-energy, matter action, or benchmark premise appears.
- Completion states finite/local only.

---

## P4-T03 — Valid invariance certificate instance

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0`  
**Task type:** `finite_local_valid_invariance_certificate_instance_v16`  
**Objective:** Construct one explicit finite/local valid source invariance certificate instance.

### Required artifact

`research_control/tasks/<task_id>/artifacts/finite_local_invariance_certificate_instance_v1.tex`

### Required content

- finite source context;
- declared relabeling or admissible source variation;
- invariant source labels/guards/response-token relations;
- no-target guard;
- proof by finite enumeration or direct argument;
- scope boundary.

### Done criteria

- The instance shows a real invariance relation.
- The instance does not become empirical/detector invariance.
- No physics promotion.

---

## P4-T04 — Valid factorization certificate instance

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0`  
**Task type:** `finite_local_valid_factorization_certificate_instance_v16`  
**Objective:** Construct one explicit finite/local valid source factorization certificate instance.

### Required artifact

`research_control/tasks/<task_id>/artifacts/finite_local_factorization_certificate_instance_v1.tex`

### Required content

- source object `F_src`;
- maps/factors from `A_src` and `B_src` through `F_src`;
- declared `RR_E` boundary behavior;
- no-target guard;
- proof of factorization inside source scope;
- explicit statement that this does not collapse global `RR_E`.

### Done criteria

- Factorization object is explicit.
- `RR_E` handling is bounded.
- No matter-coupling derivation.

---

## P4-T05 — Negative certificate-instance packet

**Continue Research transaction:** required  
**Recommended role:** `refuter@0.2.0`  
**Task type:** `negative_certificate_instance_packet_v16`  
**Objective:** Construct missing, malformed, target-import, detector-import, and process-authority negative certificate examples.

### Required artifact

`research_control/tasks/<task_id>/artifacts/negative_certificate_instance_packet_v1.tex`

### Required examples

1. Missing source transport certificate.
2. Malformed domain/codomain mismatch.
3. Changed factorization object.
4. Target metric import.
5. Detector-semantics import.
6. Stress-energy shortcut.
7. Validator PASS as proof attempt.
8. Scoped evidence-as-adoption attempt.

### Done criteria

- Each negative instance has an expected fail-closed reason.
- Each negative instance names blocked overreads.
- No global no-go claim.

---

## P4-T06 — Certificate-instance index and selector handoff

**Continue Research transaction:** required  
**Recommended role:** `project-control-maintainer@0.2.0` or `theoretical-continuation-selector@0.1.0`  
**Task type:** `source_certificate_instance_library_index_and_handoff_v16`  
**Objective:** Index certificate instances and select exactly one next route.

### Required artifact

`research_control/design/source_certificate_instance_library_index_v1.md`

### Required index fields

- instance ID;
- artifact path;
- instance kind;
- positive/negative status;
- source objects;
- certificate kind;
- expected result;
- allowed reuse;
- blocked overreads;
- formalization availability;
- related model-zoo model.

### Candidate next routes

- equivalence/theorem separation refactor;
- executable formalization of instances;
- source model zoo expansion;
- target-import attack suite;
- coupling-law candidate construction;
- freeze/review if instances fail.

### Done criteria

- Every P4 instance is indexed.
- Handoff selects one next route, defaulting to P5 if no immediate repair is needed.
- No physics delta.

---

# P5 — Separate Definitional Equivalence from Theorem Content

## P5 purpose

P5 implements `V16-R03`. v15’s central theorem was logically clean but close to definition unfolding. P5 separates:

- constructors;
- validity predicates;
- equivalence relation;
- theorem obligations;
- algebraic properties;
- failure/countermodel behavior.

The goal is not to weaken v15. The goal is to make future theorem content nontrivial.

---

## P5-T01 — Equivalence/theorem-content separation audit

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0` with `process-integrity-auditor@0.1.0` child perspective if physics contract requires  
**Task type:** `eqms_definition_theorem_content_separation_audit_v16`  
**Objective:** Audit `NarrowMSCertEq_v1` and certificate algebra to identify which parts are definition unfolding and which parts are theorem content.

### Required artifact

`research_control/tasks/<task_id>/artifacts/eqms_definition_theorem_content_separation_audit_v16.tex`

### Required sections

- source definitions imported from P2/P3;
- theorem statements imported from P2/P3;
- proof steps that are definitional unfoldings;
- proof steps that are nontrivial;
- missing theorem content;
- future theorem obligations;
- finite/local examples from P4 that demonstrate nontriviality;
- forbidden conclusion boundary.

### Required classification values

For each statement, classify:

- `definition_only`
- `constructor_definition`
- `validity_predicate`
- `definition_unfolding_theorem`
- `nontrivial_conditional_theorem`
- `finite_instance_theorem`
- `countermodel_or_obstruction`
- `future_theorem_target`

### Done criteria

- Audit identifies exact theorem-content gaps.
- It does not demote valid scoped evidence-status; it clarifies its scope.
- Handoff proceeds to P5-T02.

---

## P5-T02 — Refactored source-equivalence target specification

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0`  
**Task type:** `refactored_certificate_indexed_source_equivalence_target_spec_v16`  
**Objective:** State a refactored target where certificate constructors and equivalence properties are distinct.

### Required artifact

`research_control/tasks/<task_id>/artifacts/refactored_certificate_indexed_source_equivalence_target_spec_v1.tex`

### Required definitions

- `SourceObjectRecord_v2`
- `SourceCertificateRecord_v2`
- `CertificateValidity_v2`
- `CertificateGeneratedRelation_v2`
- `EqMS_cert_src_v2`
- `EquivalencePropertyTarget_v2`
- `FailClosedEvaluation_v2`

### Required theorem targets

The artifact must state as theorem targets, not necessarily prove all:

1. reflexivity under valid identity certificate;
2. symmetry only if inverse/dual certificate exists or is supplied;
3. transitivity under valid compatible composition;
4. restriction monotonicity under declared source subdomain;
5. missing certificate blocks generated equivalence;
6. malformed certificate blocks generated equivalence;
7. target-importing certificate blocks generated equivalence;
8. scoped evidence-status does not generate a certificate.

### Done criteria

- Definitions and theorem targets are separated.
- Each theorem target names exact inputs.
- Future proof tasks can select one theorem target.
- No matter-coupling derivation.

---

## P5-T03 — One nontrivial equivalence property theorem attempt

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0`  
**Task type:** `certificate_indexed_equivalence_property_theorem_attempt_v16`  
**Objective:** Attempt one nontrivial theorem from P5-T02.

### Default theorem target

Unless P5-T02 identifies a better one, select:

```text
transitivity under valid compatible certificate composition
```

### Required artifact

`research_control/tasks/<task_id>/artifacts/certificate_indexed_equivalence_property_theorem_attempt_v1.tex`

### Required structure

- theorem target;
- precise assumptions;
- proof attempt;
- finite/local example from P4;
- obstruction if proof fails;
- minimal countermodel if false without extra premises;
- no-target import audit section;
- Distance-to-GR effect;
- forbidden conclusions.

### Done criteria

- The theorem is proved conditionally or fails precisely.
- If failed, obstruction is named.
- Completion includes new mathematical payload.
- No physics promotion.

---

## P5-T04 — Post-refactor selector

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0`  
**Task type:** `post_eqms_refactor_route_selector_v16`  
**Objective:** Select the next route after the equivalence/theorem separation work.

### Candidate routes

- formalize P5 theorem in support-only spec;
- expand certificate-instance library;
- build model zoo;
- route to target-import attack suite;
- select coupling-law candidate construction;
- repair theorem target;
- route freeze if repeated no-payload.

### Done criteria

- Exactly one route selected.
- Handoff points to P6 unless a repair/freeze is required.
- No physics delta.

---

# P6 — Incremental Formalization and Executable Certificate Checks

## P6 purpose

P6 implements `V16-R04` and supports `V16-R14`. It extends v15’s support-only formalization pilot into incremental executable checking for certificate algebra and attack fixtures.

This remains support-only. It does not become proof authority.

---

## P6-T01 — Formalization scope selector for v16

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0` or `validator-engineer@0.2.0`  
**Task type:** `v16_support_only_formalization_scope_selector`  
**Objective:** Select one bounded formalization target from certificate algebra, P4 instances, P5 theorem target, or P14 attack fixtures.

### Candidate targets

- certificate record type and validity predicate;
- transport certificate finite check;
- invariance certificate finite check;
- factorization certificate finite check;
- missing/malformed certificate fail-closed evaluator;
- target-import rejection evaluator;
- transitivity under compatible composition;
- route-signature minimum payload gate;
- compact frontier schema validation.

### Required selection criteria

- finite/local;
- executable or proof-checkable within one bounded task;
- no dependency on full GR derivation;
- useful for validators or Refuters;
- support-only;
- no proof authority.

### Required artifact

`research_control/tasks/<task_id>/artifacts/v16_formalization_scope_selector.md`

### Done criteria

- Exactly one target selected.
- The selected toolchain is justified.
- Handoff to P6-T02.

---

## P6-T02 — Support-only executable certificate spec

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0` or one-job provisional proof-assistant engineer if current roles permit  
**Task type:** `support_only_executable_certificate_spec_v16`  
**Objective:** Implement the selected small kernel in a proof assistant or typed executable spec.

### Allowed implementation choices

The Director may select:

- Lean;
- Coq;
- Isabelle;
- Agda;
- Python typed algebraic spec plus unit tests;
- another bounded formal tool already supported locally.

### Required status

```yaml
proof_authority: false
physics_promotion_authorized: false
support_only: true
generated_derivative_or_test_support_only: true
```

### Required behaviors if certificate evaluator selected

The executable spec should model:

- certificate record;
- status field;
- valid/missing/malformed states;
- domain/codomain matching;
- no-target guard;
- target-import rejection;
- process-authority rejection;
- scoped evidence not filling certificate slots;
- expected equivalence result;
- fail-closed result.

### Required outputs

- source file for the pilot;
- test file or proof run receipt;
- Markdown explanation;
- no-authority warning;
- mapping to P4/P5 artifacts.

### Done criteria

- Pilot runs locally or has a clear non-execution receipt.
- Tests cover at least one positive and three negative cases.
- Completion states that the pilot does not prove project physics claims.

---

## P6-T03 — Formalization integration report

**Continue Research transaction:** required  
**Recommended role:** `process-integrity-auditor@0.1.0` or `validator-engineer@0.2.0`  
**Task type:** `v16_formalization_integration_report`  
**Objective:** Determine how the support-only executable spec should be used in future validators, Refuter tasks, or theorem packets.

### Required artifact

`research_control/tasks/<task_id>/artifacts/v16_formalization_integration_report.md`

### Required sections

- what was formalized;
- what was not formalized;
- how it relates to P4 instances;
- how it relates to P5 theorem targets;
- whether to include it in local CI-equivalent validation;
- how it helps detect target imports;
- what scientific claims it does not establish;
- one next route.

### Done criteria

- Integration route selected.
- No proof-authority overread.
- No physics delta.

---

# P7 — Route-Orbit and Minimum-Payload Gating

## P7 purpose

P7 implements `V16-R05` and `V16-R06`.

v15 produced advisory route-orbit diagnostics and payload-density metrics. v16 must make these selectively gating. This does not mean every selector is blocked. It means repeated no-payload cycles on the same burden must route to repair, freeze review, or payload-bearing work.

---

## P7-T01 — Minimum physics payload schema

**Continue Research transaction:** required  
**Recommended role:** `project-control-maintainer@0.2.0` or `validator-engineer@0.2.0`  
**Task type:** `minimum_physics_payload_schema_v16`  
**Objective:** Define a required minimum payload contract for post-v15 physics tasks.

### Required artifact

`research_control/design/minimum_physics_payload_schema_v1.md`

### Required payload classes

```yaml
payload_classes:
  - new_definition
  - theorem_statement
  - proof_attempt
  - proved_conditional_theorem
  - explicit_finite_witness
  - minimal_countermodel
  - obstruction_record
  - source_model
  - certificate_instance
  - executable_support_spec
  - attack_fixture
  - selector_with_scored_route_matrix
  - validation_repair
  - freeze_review
```

### Required rule

A post-v15 physics task must include at least one of:

- `new_definition`;
- `theorem_statement`;
- `proof_attempt`;
- `proved_conditional_theorem`;
- `explicit_finite_witness`;
- `minimal_countermodel`;
- `obstruction_record`;
- `source_model`;
- `certificate_instance`;
- `executable_support_spec`;
- `attack_fixture`.

Exceptions:

- selector tasks may use `selector_with_scored_route_matrix`;
- validation repair tasks may use `validation_repair`;
- freeze tasks may use `freeze_review`;
- documentation/publication tasks must classify as non-physics project tasks.

### Done criteria

- Schema exists.
- It distinguishes payload from process receipts.
- It says payload status is not physics promotion.

---

## P7-T02 — Route-orbit gating policy

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0` or `project-control-maintainer@0.2.0`  
**Task type:** `route_orbit_gating_policy_v16`  
**Objective:** Convert route-orbit diagnostics into selective gates.

### Required artifact

`research_control/design/route_orbit_gating_policy_v16.md`

### Suggested hard-gate rule

A freeze-review or repair selector is required when three consecutive same-burden tasks have:

- same `target_derivation_milestone`;
- same `milestone_burden`;
- no new mathematical payload;
- no new finite/local witness;
- no new countermodel;
- no new source model;
- no new certificate instance;
- no new executable support spec;
- no validator failure requiring repair;
- no protected gate newly required;
- no external red-team finding requiring integration.

### Advisory-warning rule

Emit warning, but do not hard-gate, when:

- two same-burden tasks occur with weak payload;
- selector repeats same route but adds new scoring evidence;
- documentation-only task follows physics task;
- validator or renderer refresh creates no physics payload but is required.

### Done criteria

- Policy distinguishes legitimate multi-packet theorem work from orbit.
- It prevents “selector fog” without blocking actual theorem progress.
- No global no-go implied.

---

## P7-T03 — Payload/orbit validator integration

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0`  
**Task type:** `payload_orbit_validator_integration_v16`  
**Objective:** Integrate minimum payload and route-orbit policy into validators or local CI-equivalent reports.

### Possible outputs

- `scripts/research_control/validate_minimum_physics_payload.py`
- extension to `validate_route_orbits.py`
- fixture files under test directories
- update to `validation_command_inventory_v16.md`
- task-local receipt

### Required bad fixtures

- three same-burden selector tasks with no payload;
- theorem packet with only validator PASS and no theorem/countermodel;
- evidence-status restatement as physics payload;
- generated wiki refresh as physics payload;
- benchmark promotion by route status.

### Required good fixtures

- scored selector matrix;
- explicit certificate instance;
- finite/local source model;
- minimal countermodel;
- executable support spec;
- validation repair task with no physics claim.

### Done criteria

- Validator or report distinguishes PASS, WARN, and HARD_GATE.
- No existing legitimate task is retroactively promoted or refuted.
- No physics delta.

---

# P8 — Risky Status-Field Rename and Schema Layering

## P8 purpose

P8 implements `V16-R08`. v15 did a good job with claim boundaries, but raw fields such as `physics_promotion_authorized: true` for scoped evidence-status gates are risky. v16 adds layered status vocabulary and compatibility aliases.

This phase must be careful. It should not rewrite history destructively. It should add safer future-facing fields and compatibility interpretation.

---

## P8-T01 — Risky field audit

**Continue Research transaction:** required  
**Recommended role:** `process-integrity-auditor@0.1.0`  
**Task type:** `risky_status_field_audit_v16`  
**Objective:** Audit task records, completions, claim-boundary rows, role-execution records, and handoffs for ambiguous field names.

### Required artifact

`research_control/tasks/<task_id>/artifacts/risky_status_field_audit_v16.md`

### Fields to audit

- `physics_promotion_authorized`
- `scientific_claims_changed`
- `accepted`
- `adopted`
- `promotion_authority_path`
- `source_extension_data_adopted`
- `gate_review_completed`
- `Gate Chair accepted`
- `completed`
- any field that can be confused with downstream physics promotion.

### Required classification

For each risky field occurrence, classify:

- `safe_contextual_raw_field`
- `needs_alias_only`
- `needs_schema_update`
- `needs_linter_warning`
- `needs_reader_facing_renderer_fix`
- `unsafe_requires_remediation`

### Done criteria

- Audit distinguishes historical records from future schema changes.
- No physics status is changed.
- Handoff to P8-T02.

---

## P8-T02 — Layered status field schema

**Continue Research transaction:** required  
**Recommended role:** `project-control-maintainer@0.2.0` or `validator-engineer@0.2.0`  
**Task type:** `layered_status_field_schema_v16`  
**Objective:** Define future-facing layered status fields that prevent scoped evidence changes from being read as downstream physics promotion.

### Required artifact

`research_control/design/layered_status_field_schema_v16.md`

### Required field model

```yaml
scoped_evidence_status_change_authorized: false
source_object_status_change_authorized: false
source_extension_object_status_change_authorized: false
source_law_adoption_authorized: false
matter_semantics_adoption_authorized: false
detector_semantics_adoption_authorized: false
coupling_law_adoption_authorized: false
matter_coupling_derivation_authorized: false
matter_coupling_adoption_authorized: false
stress_energy_semantics_authorized: false
matter_action_authorized: false
einstein_equation_derivation_authorized: false
benchmark_promotion_authorized: false
completed_derivation_authorized: false
downstream_physics_promotion_authorized: false
```

### Required compatibility rule

Historical fields must be interpreted through claim-boundary context. Do not rewrite old records unless validators require remediation. Add alias or renderer interpretation first.

### Done criteria

- Schema distinguishes scoped evidence from downstream promotion.
- Schema includes migration guidance.
- No physics delta.

---

## P8-T03 — Status-field compatibility validator

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0`  
**Task type:** `status_field_compatibility_validator_v16`  
**Objective:** Add validation or linter rules for risky status fields in future tasks.

### Required rules

- Any future `physics_promotion_authorized: true` must also specify exact layer and downstream status.
- Scoped evidence-status changes must not set downstream promotion fields.
- Gate Chair scoped evidence acceptance must not imply source-law adoption.
- `accepted` must not render bare for high-risk rows.
- `scientific_claims_changed: true` must state which layer changed.

### Done criteria

- Bad fixtures fail.
- Historical safe contexts produce warnings at most.
- Changed-claim-language validation passes.

---

# P9 — `EqSrc`, `RetainH`, and `GenH` Trigger-Horizon Policy

## P9 purpose

P9 implements `V16-R09`. v15 audited `EqSrc`, `RetainH`, and `GenH`; v16 converts that audit into a future routing trigger list. These upstream primitives remain on the horizon, not the immediate lane, unless a selected theorem edge requires them.

---

## P9-T01 — Upstream primitive trigger list

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0` or `theoretical-continuation-selector@0.1.0`  
**Task type:** `eqsrc_retainh_genh_trigger_list_v16`  
**Objective:** Create a trigger policy for when to route `EqSrc`, `RetainH`, or `GenH` packets.

### Required artifact

`research_control/design/eqsrc_retainh_genh_trigger_list_v16.md`

### Required trigger rules

Route `EqSrc` when a future task:

- removes explicit certificate premises;
- seeks family-wide source equivalence;
- needs equivalence across arbitrary source-family variation;
- claims certificate equivalence independent of certificate records.

Route `RetainH` when a future task:

- preserves certificate structure under `H`;
- preserves source semantics under retention;
- claims stability under an `H`-indexed operation;
- needs retention to sustain matter-sector continuity.

Route `GenH` when a future task:

- constructs an `H`-indexed source family;
- enumerates a generated source family;
- requires generator closure;
- uses generated family structure as theorem input.

Do not route any of these merely because they are philosophically interesting.

### Done criteria

- Trigger list is exact.
- It includes allowed non-trigger cases.
- It includes forbidden overread language.
- No physics delta.

---

## P9-T02 — Selector integration for upstream triggers

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0`  
**Task type:** `upstream_trigger_selector_integration_v16`  
**Objective:** Integrate the trigger list into selector packets and DAG edge ranking.

### Required artifact

`research_control/tasks/<task_id>/artifacts/upstream_trigger_selector_integration_v16.md`

### Required updates or guidance

- P2 scoring rubric uses `dependency_on_missing_eqsrc_retainh_genh`.
- Future theorem setups must state whether selected theorem requires any of the three.
- Future completions must record `upstream_primitive_trigger_status`.

### Required completion fragment

```yaml
upstream_primitive_trigger_status:
  EqSrc:
    triggered: false
    reason: ""
  RetainH:
    triggered: false
    reason: ""
  GenH:
    triggered: false
    reason: ""
```

### Done criteria

- Selector guidance is integrated.
- No immediate upstream primitive route is selected unless triggered by tracked evidence.
- No physics delta.

---

# P10 — Source Model Zoo

## P10 purpose

P10 implements `V16-R10` and supports `V16-R02`. The model zoo makes the source-side theory concrete. It should contain small finite/local source models that exercise certificates, obstructions, and target-import rejection.

The model zoo is a scientific support surface. It is not a physical model of the universe, not GR, and not a benchmark.

---

## P10-T01 — Source model zoo schema

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0` with `validator-engineer@0.2.0` consultation  
**Task type:** `source_model_zoo_schema_v16`  
**Objective:** Define a schema for finite/local source models.

### Required artifact

`research_control/design/source_model_zoo_schema_v1.md`

### Required model fields

```yaml
model_id:
model_kind:
source_domain:
source_objects:
source_labels:
source_guards:
response_tokens:
certificate_instances:
rr_e_records:
target_import_status:
detector_semantics_status:
stress_energy_status:
matter_action_status:
benchmark_status:
expected_valid_relations:
expected_fail_closed_relations:
source_paths:
allowed_reuse:
forbidden_overreads:
```

### Required model kinds

- `trivial_identity_model`
- `transportable_two_object_model`
- `invariant_relabeling_model`
- `factorization_through_source_object_model`
- `certificate_gap_model`
- `rr_e_separated_model`
- `target_import_rejection_model`
- `detector_semantics_collapse_rejection_model`

### Done criteria

- Schema supports P4 certificate instances.
- It makes finite/local scope explicit.
- No physics delta.

---

## P10-T02 — Initial source model zoo

**Continue Research transaction:** required  
**Recommended role:** `ontology-formalizer@0.2.0`  
**Task type:** `initial_source_model_zoo_v16`  
**Objective:** Build the first finite/local source model zoo with at least eight models.

### Required artifact

`research_control/design/source_model_zoo_v1.md`

### Required models

1. Trivial identity model.
2. Transportable two-object model.
3. Invariant relabeling model.
4. Factorization-through-source-object model.
5. Certificate-gap model.
6. `RR_E` separated model.
7. Target-import rejection model.
8. Detector-semantics collapse rejection model.

### For each model

Include:

- model definition;
- finite object table;
- allowed certificates;
- blocked certificates;
- expected theorem result;
- expected fail-closed result;
- relation to P4 certificate instances;
- forbidden overreads.

### Done criteria

- Each model has explicit finite data.
- At least three models map to positive certificate instances.
- At least three models map to negative/refuter instances.
- No model imports target metric, detector semantics, stress-energy, matter action, or benchmark behavior as source data.

---

## P10-T03 — Model zoo validation and selector

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0` or `theoretical-continuation-selector@0.1.0`  
**Task type:** `source_model_zoo_validation_and_selector_v16`  
**Objective:** Validate the model zoo and select its next use.

### Required artifact

`research_control/tasks/<task_id>/artifacts/source_model_zoo_validation_and_selector_v16.md`

### Required checks

- every model has finite/local scope;
- every model has allowed reuse and blocked overreads;
- no model claims matter coupling;
- no model claims detector semantics;
- no model claims Einstein equations;
- no model claims benchmark recovery;
- each model maps to at least one certificate instance or obstruction.

### Candidate next uses

- formalization support;
- target-import attack suite;
- coupling-law target candidate testing;
- red-team packet inclusion;
- negative-result explainer;
- no-op with evidence.

### Done criteria

- One next use selected.
- No physics promotion.

---

# P11 — Negative Results Reader-Facing but Not Sensational

## P11 purpose

P11 implements `V16-R11`. v15 created negative-result inventory and explainers. v16 ensures negative results are reader-facing without sensational overclaim.

---

## P11-T01 — Negative-result reader-language audit

**Continue Research transaction:** required  
**Recommended role:** `documentation-curator@2.0.0` or `process-integrity-auditor@0.1.0`  
**Task type:** `negative_result_reader_language_audit_v16`  
**Objective:** Audit negative-result surfaces for overclaim or underexposure.

### Required reads

- `research_control/design/negative_result_inventory_v15.md`
- negative-result publication brief
- negative-result explainer source spec
- current frontier negative-result rows
- public status docs
- claim-language linter policy

### Required artifact

`research_control/tasks/<task_id>/artifacts/negative_result_reader_language_audit_v16.md`

### Audit questions

- Are frozen local routes visible?
- Are scoped obstructions visible?
- Does any wording imply global program rejection?
- Does any wording imply future source-extension impossibility?
- Does any wording imply benchmark failure or benchmark closure?
- Does any negative result hide what remains open?
- Are negative results tied to exact source artifacts?

### Done criteria

- Audit classifies each surface.
- Any risky wording routes to P11-T02.
- No physics delta.

---

## P11-T02 — Negative-result public-safe wording update

**Continue Research transaction:** required if P11-T01 finds update needed  
**Recommended role:** `documentation-curator@2.0.0`  
**Task type:** `negative_result_public_safe_wording_update_v16`  
**Objective:** Update reader-facing negative-result wording to be clear, scoped, and non-sensational.

### Allowed wording

- “frozen negative local route”
- “scoped obstruction”
- “finite/local witness”
- “blocked under current premises”
- “does not establish global no-go”
- “open continuation remains possible”
- “future source-extension impossibility not proved”
- “program-wide rejection not claimed”

### Forbidden wording without separate proof

- “the theory is refuted”
- “future derivation is impossible”
- “global no-go”
- “benchmark failure proved”
- “GR derivation permanently blocked”
- “all source-extension routes closed”

### Done criteria

- Public-safe wording passes claim-language linter.
- Documentation-impact receipt exists.
- No physics delta.

---

## P11-T03 — Negative-result integration selector

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0` or `documentation-curator@2.0.0`  
**Task type:** `negative_result_integration_selector_v16`  
**Objective:** Select one next route for negative-result integration.

### Candidate routes

- add negative-result section to physics manuscript outline;
- add negative-result section to AI methodology manuscript outline;
- include selected obstruction in red-team packet;
- add linter fixture;
- no-op with evidence.

### Done criteria

- Exactly one route selected.
- No negative result is promoted to global no-go.

---

# P12 — Manuscript Split Continuation

## P12 purpose

P12 implements `V16-R12`. v15 created two manuscript outlines and a glossary. v16 continues them exactly as planned, without blending physics claims and AI methodology claims.

---

## P12-T01 — Physics manuscript status refresh

**Continue Research transaction:** required  
**Recommended role:** `documentation-curator@2.0.0` with ontology-formalizer consultation if needed  
**Task type:** `physics_manuscript_status_refresh_v16`  
**Objective:** Refresh the physics manuscript outline with v16 post-v15 route state and keep it honest.

### Required artifact

`research_control/tasks/<task_id>/artifacts/physics_manuscript_status_refresh_v16.md`

or, if manuscript lane is active, an update under the approved manuscript path.

### Required sections

- exact-GR benchmark boundary;
- current public-safe ontology status;
- scoped `M_src`;
- scoped `g_eff`;
- scoped matter-sector evidence/preconditions;
- `NarrowMSCertEq_v1` as scoped/conditional source-side theorem evidence;
- certificate algebra;
- concrete certificate-instance library if P4 complete;
- selected matter-coupling DAG edge;
- current missing burdens;
- negative results;
- no completed derivation.

### Done criteria

- Physics manuscript remains a physics-program/open-burden paper, not a GR derivation paper.
- It does not claim matter coupling or Einstein equations.
- No submission/publication action implied.

---

## P12-T02 — AI methodology manuscript status refresh

**Continue Research transaction:** required  
**Recommended role:** `documentation-curator@2.0.0` or `process-integrity-auditor@0.1.0`  
**Task type:** `ai_methodology_manuscript_status_refresh_v16`  
**Objective:** Refresh the AI methodology manuscript outline with v16 control-system developments.

### Required artifact

`research_control/tasks/<task_id>/artifacts/ai_methodology_manuscript_status_refresh_v16.md`

### Required sections

- Director-led Continue Research;
- AgentJob contracts;
- claim-boundary registries;
- Distance-to-GR ledger;
- smuggling audit;
- Refuter stress;
- Gate Chair boundaries;
- route-orbit gating;
- minimum payload gate;
- source-first memory;
- negative-result preservation;
- target-import attack suite;
- compact frontier state;
- limitations and human accountability.

### Done criteria

- AI methodology claims are separated from physics success claims.
- It does not claim autonomous scientific authority.
- No physics delta.

---

## P12-T03 — Manuscript split boundary validator/checklist

**Continue Research transaction:** required  
**Recommended role:** `project-control-maintainer@0.2.0` or `documentation-curator@2.0.0`  
**Task type:** `manuscript_split_boundary_checklist_v16`  
**Objective:** Create a checklist preventing the physics manuscript and AI methodology manuscript from lending authority to each other incorrectly.

### Required artifact

`research_control/design/manuscript_split_boundary_checklist_v16.md`

### Required checks

- physics manuscript cannot cite AI validator PASS as physics proof;
- AI methodology manuscript cannot cite physics theorem as autonomous-system success beyond scoped result;
- neither manuscript may claim GR derivation;
- neither manuscript may convert scoped evidence into adoption;
- public wording must preserve proposed ontology status;
- negative results must remain scoped.

### Done criteria

- Checklist exists.
- Manuscript updates cite checklist or record compatibility.
- No physics delta.

---

# P13 — One-Question External Red-Team Packet

## P13 purpose

P13 implements `V16-R13`. The external red-team packet should be centered on one concrete, high-value question, not a request to review the entire repository labyrinth.

---

## P13-T01 — Red-team question selector

**Continue Research transaction:** required  
**Recommended role:** `theoretical-continuation-selector@0.1.0` or `process-integrity-auditor@0.1.0`  
**Task type:** `one_question_red_team_question_selector_v16`  
**Objective:** Select exactly one concrete red-team question.

### Default question

Unless live evidence indicates a better target, select:

```text
Does NarrowMSCertEq_v1 plus the source certificate algebra supply any nontrivial
source-side mathematical content beyond definitions, and does any hidden target-side
or detector-side import occur?
```

### Alternative questions

- Does the P3 source-side coupling-law target specification smuggle in coupling-law adoption?
- Do the P4 certificate instances genuinely instantiate the certificate schema?
- Does the P5 equivalence/theorem separation produce nontrivial theorem content?
- Does the current matter-coupling DAG hide target imports?
- Does the target-import attack suite cover the main overread risks?

### Required artifact

`research_control/tasks/<task_id>/artifacts/one_question_red_team_question_selector_v16.md`

### Done criteria

- Exactly one question selected.
- It names source artifacts to review.
- It names expected reviewer output.
- No external outreach occurs unless separately authorized.

---

## P13-T02 — One-question red-team packet

**Continue Research transaction:** required  
**Recommended role:** `documentation-curator@2.0.0`, `process-integrity-auditor@0.1.0`, or one-job provisional red-team coordinator  
**Task type:** `one_question_red_team_packet_v16`  
**Objective:** Prepare a red-team packet around the selected question.

### Required artifact

`research_control/design/one_question_red_team_packet_v16.md`

### Required packet sections

- selected question;
- exact source artifacts;
- project claim boundary;
- strongest allowed positive reading;
- strongest forbidden overreads;
- reviewer tasks;
- expected output template;
- reviewer scoring rubric;
- conflict-of-interest note;
- how findings will be integrated;
- non-authority warning.

### Expected reviewer output template

```yaml
reviewer_name_or_anonymous_id:
review_date:
reviewed_artifacts:
selected_question:
strongest_valid_reading:
strongest_overread_risk:
hidden_imports_detected:
smallest_counterexample_or_missing_premise:
recommendation:
  - accept_scoped_status
  - repair_required
  - reject_current_claim
  - request_formalization
  - route_refuter_stress
  - route_smuggling_audit
review_confidence:
notes:
```

### Done criteria

- Packet can be used internally or externally.
- No adoption or promotion occurs.
- Handoff selects internal pilot or hold-for-human outreach.

---

## P13-T03 — Internal one-question red-team pilot

**Continue Research transaction:** required unless external review is immediately human-authorized  
**Recommended role:** `refuter@0.2.0` or one-job provisional red-team reviewer  
**Task type:** `internal_one_question_red_team_pilot_v16`  
**Objective:** Run an internal red-team review using the one-question packet.

### Required artifact

`research_control/tasks/<task_id>/artifacts/internal_one_question_red_team_pilot_v16.md`

### Required findings

- answer to selected question;
- strongest valid reading;
- strongest overread risk;
- hidden imports detected or not detected;
- smallest counterexample or missing premise;
- recommendation;
- integration route.

### Done criteria

- Findings are bounded.
- Exactly one integration route selected.
- No external outreach implied.

---

# P14 — Target-Import Attack Suite

## P14 purpose

P14 implements `V16-R14`. The attack suite actively tries to smuggle forbidden target-side or process-authority premises into source-side proofs and certificates.

The attack suite should be executable or semi-executable when possible, but it remains validator/support evidence, not physics proof.

---

## P14-T01 — Target-import attack taxonomy

**Continue Research transaction:** required  
**Recommended role:** `smuggling-auditor@0.2.0` or `validator-engineer@0.2.0`  
**Task type:** `target_import_attack_taxonomy_v16`  
**Objective:** Define a taxonomy of forbidden imports and attack patterns.

### Required artifact

`research_control/design/target_import_attack_taxonomy_v16.md`

### Required attack classes

- target metric import;
- Lorentzian signature import;
- target topology/atlas import;
- proper-time import;
- detector calibration import;
- empirical readout import;
- stress-energy tensor shortcut;
- matter action shortcut;
- Einstein-equation premise shortcut;
- benchmark fit shortcut;
- Gate Chair/process authority as proof;
- validator PASS as proof;
- generated derivative as proof;
- scoped evidence as adoption;
- finite/local-to-global overread.

### Done criteria

- Taxonomy maps each attack to expected fail-closed response.
- It names source paths or schemas that should reject each attack.
- No physics delta.

---

## P14-T02 — Attack-suite fixture library

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0` with smuggling-auditor input  
**Task type:** `target_import_attack_fixture_library_v16`  
**Objective:** Create fixtures for forbidden target imports and allowed source-safe statements.

### Required outputs

- `research_control/design/target_import_attack_fixture_catalog_v16.md`
- fixture files under current validator fixture path, if allowed
- task-local validation receipt

### Required bad fixtures

1. Target metric used as source certificate.
2. Lorentzian signature used as certificate validity.
3. Proper time used as source readout.
4. Detector calibration treated as source label.
5. Stress-energy tensor used to prove matter semantics.
6. Matter action used to prove coupling law.
7. Einstein equations used as upstream premise.
8. Benchmark fit used as source evidence.
9. Gate Chair scoped evidence used as source law.
10. Validator PASS used as proof.
11. Generated wiki note used as authority.
12. Finite/local model rendered as universal matter coupling.

### Required good fixtures

1. Source transport certificate with no-target guard.
2. Scoped evidence/precondition wording.
3. Target import fail-closed wording.
4. Detector semantics blocked wording.
5. Einstein equations not started wording.
6. Benchmark promotion protected wording.

### Done criteria

- Fixtures are registered or discoverable by validators.
- Bad examples fail under current or new linter.
- Good examples pass.
- No physics delta.

---

## P14-T03 — Attack-suite validator integration

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0`  
**Task type:** `target_import_attack_validator_integration_v16`  
**Objective:** Integrate the attack suite into claim-language, smuggling-audit, or research-control validation.

### Possible implementation paths

- extend `validate_claim_language.py`;
- add a dedicated `validate_target_import_attacks.py`;
- add fixtures consumed by existing linter;
- add local CI-equivalent command;
- add smuggling-audit checklist update.

### Required validation outputs

- PASS on source-safe current wording;
- FAIL on target metric import;
- FAIL on detector collapse;
- FAIL on stress-energy shortcut;
- FAIL on process-authority proof laundering;
- WARN or FAIL on finite/local-to-global overread depending on context.

### Done criteria

- Validator integration is documented.
- No existing allowed source-safe phrasing is broken without remediation path.
- No physics delta.

---

# P15 — Compact Current-Frontier Machine Summary

## P15 purpose

P15 implements `V16-R15`. The current frontier is readable but dense. v16 adds compact machine-readable state, while preserving the rule that `program_state.yaml`, latest handoff, Distance-to-GR ledger, and tracked task records remain authority.

---

## P15-T01 — Compact frontier schema

**Continue Research transaction:** required  
**Recommended role:** `project-control-maintainer@0.2.0` or `validator-engineer@0.2.0`  
**Task type:** `compact_current_frontier_schema_v16`  
**Objective:** Define a compact machine-readable current-frontier summary schema.

### Required artifact

`research_control/design/compact_current_frontier_schema_v16.md`

### Required schema shape

```yaml
schema_id: "compact_current_frontier_v16"
generated_from:
  - "research_control/program_state.yaml"
  - "latest_handoff"
  - "registries/DISTANCE_TO_GR_LEDGER.csv"
  - "research_control/current_frontier.md"
active_state:
  active_task_id:
  latest_handoff_id:
  current_status:
  v15_completed:
  v16_plan_registered:
next_route:
  route_id:
  role_family:
  target_derivation_milestone:
  milestone_burden:
  requires_human_gate:
claim_boundary:
  physics_claim_authority: false
  proof_authority: false
  blocked_claims: []
scoped_positive_objects: []
scoped_evidence_preconditions: []
blocked_physical_targets: []
distance_to_gr:
  delta:
  high_risk_rows: []
validation:
  latest_required_status:
  pending_layers: []
authority_warning:
  snapshot_only_not_authority: true
```

### Done criteria

- Schema distinguishes snapshot from authority.
- It names exact source paths.
- It preserves blocked claims.

---

## P15-T02 — Compact frontier renderer

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0`  
**Task type:** `compact_current_frontier_renderer_v16`  
**Objective:** Implement or specify a renderer that produces compact YAML/JSON from tracked state.

### Preferred outputs

- `output/compact_current_frontier_v16.yaml`
- `output/compact_current_frontier_v16.json`
- optional `wiki/indexes/compact_current_frontier_v16.md`

### Required renderer behavior

- reads only tracked authority files;
- does not use generated wiki, Obsidian, semantic extracts, SQLite memory, or local caches as authority;
- includes hard blocks;
- includes next route;
- includes scoped positives;
- includes blocked physical targets;
- includes Distance-to-GR delta;
- includes snapshot-only warning.

### Done criteria

- Renderer output is generated or an implementation spec is produced if code changes are not allowed.
- Output validates against schema.
- No physics delta.

---

## P15-T03 — Compact frontier check integration

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0`  
**Task type:** `compact_current_frontier_check_integration_v16`  
**Objective:** Add a check that compact current-frontier output stays synchronized with tracked state.

### Required behavior

The check should fail when:

- active task mismatches `program_state.yaml`;
- latest handoff mismatches;
- next route mismatches latest handoff;
- high-risk blocked claims are missing;
- matter coupling renders as derived/adopted without authority;
- Einstein equations render as started/derived without authority;
- benchmark promotion renders as promoted without authority.

### Done criteria

- Check runs locally or has exact implementation receipt.
- Validation inventory updated if required.
- No physics delta.

---

# P16 — Project-System Integration Bridge

## P16 purpose

P16 integrates the project-system changes introduced by v16: validators, schemas, renderers, attack fixtures, route gates, and documentation-impact updates. It prevents system changes from becoming an untracked thicket.

This phase may be skipped only if P0/P17 coverage audit proves no v16 task changed project-system surfaces requiring integration.

---

## P16-T01 — Documentation-impact consolidation

**Continue Research transaction:** required if any v16 task changed design docs, validators, scripts, generated outputs, README, GitHub-facing docs, registries, or public specs  
**Recommended role:** `project-control-maintainer@0.2.0` or `documentation-curator@2.0.0` depending on changed paths  
**Task type:** `v16_documentation_impact_consolidation`  
**Objective:** Consolidate documentation-impact receipts and ensure each project-system change is documented or explicitly no-op.

### Required artifact

`research_control/tasks/<task_id>/artifacts/v16_documentation_impact_consolidation.md`

### Required checks

- every design schema has source registry status if required;
- every validator/script addition has maintainer note or command inventory update;
- every generated derivative is regenerated, not hand-edited;
- every public-facing change has publication brief or source spec when required;
- no documentation change promotes physics claims.

### Done criteria

- `validate_documentation_impact.py --json` passes.
- Changed paths are explained.
- No physics delta.

---

## P16-T02 — Validation inventory v16 update

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0`  
**Task type:** `validation_command_inventory_v16_update`  
**Objective:** Update the validation command inventory to include v16 checks.

### Required artifact

`research_control/design/validation_command_inventory_v16.md`

or update the current inventory according to repository convention.

### Include commands for

- minimum payload validation;
- route-orbit hard-gate check;
- target-import attack validation;
- compact frontier check;
- claim graph validation;
- current frontier render check;
- dependency graph check;
- documentation impact;
- claim-language linter;
- memory bootstrap;
- research-control validation.

### Done criteria

- Inventory distinguishes required-gate, required-render-check, advisory-diagnostic, and support-only tests.
- No validator PASS is described as proof authority.
- No physics delta.

---

## P16-T03 — Project-improvement signal bridge

**Continue Research transaction:** required if v16 emits project-improvement signals or validators identify project-system defects  
**Recommended role:** `project-control-maintainer@0.2.0`  
**Task type:** `v16_project_improvement_signal_bridge`  
**Objective:** Route any project-system improvement sidecars without blocking the scientific handoff unless current rules require it.

### Required artifact

`research_control/tasks/<task_id>/artifacts/v16_project_improvement_signal_bridge.md`

### Required fields

```yaml
project_improvement_signals:
  - signal_id:
    signal_type:
    source_task:
    severity:
    requires_handoff:
    selected_route:
bridge_required:
bridge_completed:
normal_research_handoff_preserved:
```

### Done criteria

- Any nonblank project-improvement signal is accounted for.
- Normal research continuation is not lost.
- No physics delta.

---

# P17 — Final v16 Audit, Validation, and Ordinary Continuation Handoff

## P17 purpose

P17 verifies that v16 integrated all recommendations or explicitly deferred them with tracked evidence. It then creates one ordinary continuation handoff. P17 must not itself execute new physics.

---

## P17-T01 — V16 recommendation coverage audit

**Continue Research transaction:** required  
**Recommended role:** `process-integrity-auditor@0.1.0`  
**Task type:** `v16_recommendation_coverage_audit`  
**Objective:** Audit coverage for all `V16-R01` through `V16-R15`.

### Required artifact

`research_control/tasks/<task_id>/artifacts/v16_recommendation_coverage_audit.md`

### Required table columns

```csv
recommendation_id,implemented,status,evidence_path,phase,task,notes,physics_promotion_authorized,next_route_if_partial
```

### Allowed statuses

- `implemented`
- `implemented_by_later_tracked_state`
- `partially_implemented`
- `deferred_with_reason`
- `blocked_by_human_gate`
- `superseded_by_source_evidence`
- `not_applicable_after_baseline_change`

### Done criteria

- No recommendation row is blank.
- Partial/deferred rows name exact next route.
- Every row has `physics_promotion_authorized=false`.
- No physics delta.

---

## P17-T02 — Current frontier and compact summary final refresh

**Continue Research transaction:** required  
**Recommended role:** `project-control-maintainer@0.2.0` or `validator-engineer@0.2.0` depending on renderer ownership  
**Task type:** `v16_current_frontier_and_compact_summary_final_refresh`  
**Objective:** Refresh current frontier, compact current-frontier summary, dependency graph, claim graph, and public-safe status if v16 changed their inputs.

### Required outputs if applicable

- `research_control/current_frontier.md`
- `output/compact_current_frontier_v16.yaml`
- `output/compact_current_frontier_v16.json`
- updated dependency graph
- updated claim graph
- updated matter-coupling DAG or index
- updated public-safe status table
- documentation-impact receipt

### Required current frontier statements

- latest task and handoff;
- whether v16 completed;
- selected next route;
- active burden;
- scoped positives;
- blocked physical targets;
- hard claim blocks;
- Distance-to-GR effect.

### Done criteria

- Current frontier states no overread.
- Compact summary validates.
- All high-risk rows avoid bare `accepted`.
- No unauthorized physics promotion.

---

## P17-T03 — Final validation packet

**Continue Research transaction:** required  
**Recommended role:** `validator-engineer@0.2.0`  
**Task type:** `v16_final_validation_packet`  
**Objective:** Run full validation after v16 implementation.

### Required validation layers

- memory preflight PASS;
- memory bootstrap PASS;
- research-control validation PASS;
- diff validation PASS;
- claim-language linter PASS;
- documentation-impact validation PASS;
- registry consistency PASS;
- current frontier render check PASS;
- dependency graph check PASS;
- claim graph validation PASS if claim graph exists;
- route-orbit report generated;
- route-orbit hard-gate check PASS or exact pending reason;
- minimum payload validation PASS or exact task-class exception;
- target-import attack suite PASS if implemented;
- compact frontier check PASS if implemented;
- high-risk bare accepted check PASS;
- premature EFE linter PASS;
- support-only formalization tests PASS or non-execution receipt if applicable.

### Required artifact

`research_control/tasks/<task_id>/artifacts/v16_final_validation_report.json`

### Done criteria

- Report includes layer-level statuses, not just aggregate PASS.
- Pending layers include exact reason.
- Report says `operational_receipt_only: true`.
- Report says whether v16 produced any Distance-to-GR delta.
- No validation layer is described as physics proof.

---

## P17-T04 — Ordinary continuation handoff

**Continue Research transaction:** required  
**Recommended role:** `director-of-research@0.3.0`  
**Task type:** `v16_final_ordinary_continuation_handoff`  
**Objective:** Complete v16 and select exactly one ordinary next research route.

### Candidate next routes

The Director must select exactly one, based on actual v16 outputs:

1. coupling-law target repair route;
2. concrete coupling-law candidate construction route;
3. detector-semantics replacement target route;
4. certificate-instance library expansion route;
5. source model zoo expansion route;
6. equivalence/theorem property proof route;
7. support-only formalization expansion route;
8. target-import attack-suite repair route;
9. Refuter/countermodel follow-up route;
10. `EqSrc`, `RetainH`, or `GenH` upstream theorem route if trigger conditions are met;
11. route-orbit freeze review if hard-gate triggered;
12. red-team findings integration route;
13. negative-result publication continuation route;
14. manuscript preparation continuation route;
15. project-system repair route if final validation failed.

### Forbidden next routes unless separately authorized by tracked source

- direct universal matter-coupling derivation;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- stress-energy semantics;
- matter action;
- Einstein-equation derivation;
- benchmark promotion;
- completed derivation.

### Required handoff fields

```yaml
v16_completed: true
source_plan_id: "recommendations_implementation_plan_continue_task-v16"
selected_next_route:
  route_id:
  role_family:
  target_derivation_milestone:
  milestone_burden:
  requires_human_gate:
v16_distance_to_gr_delta:
  effect:
  changed:
  burden_id:
hard_blocks:
  - source-law adoption
  - RR_ETransportCompletenessOrInvarianceLaw_v1 adoption
  - unrestricted RR_E theorem
  - matter-semantics adoption
  - detector-semantics adoption
  - coupling-law adoption
  - matter-coupling derivation or adoption
  - stress-energy semantics
  - matter action
  - Einstein equations
  - benchmark promotion
  - completed derivation
```

### Done criteria

- Exactly one next route selected.
- Handoff is synchronized with `program_state.yaml`.
- Completion states whether v16 produced any Distance-to-GR delta.
- Final claim boundary is public-safe.

---

## 8. Required Completion Language for All v16 Tasks

Every v16 completion must include a short version of this statement, adapted to task scope:

```text
This completion implements a bounded v16 task. It does not authorize source-law adoption,
RR_ETransportCompletenessOrInvarianceLaw_v1 adoption, unrestricted RR_E theorem status,
matter-semantics adoption, detector-semantics adoption, coupling-law adoption,
matter-coupling derivation or adoption, stress-energy semantics, stress-energy tensor
construction, matter action, Einstein equations, benchmark promotion, or completed derivation.
```

Physics tasks must also include:

```yaml
physics_progress_status:
distance_to_gr_delta:
mathematical_payload_manifest:
minimum_payload_class:
route_orbit_signature:
forbidden_conclusion_summary:
freeze_criteria_status:
upstream_primitive_trigger_status:
```

Project-system tasks must include:

```yaml
project_system_change_only: true
physics_promotion_authorized: false
documentation_impact:
validation_status:
```

Selector tasks must include:

```yaml
selector_result:
  selected_route_id:
  candidate_count:
  scoring_matrix_path:
  rejected_routes:
  reason_selected:
  reason_not_promotion:
  next_packet_requires_new_payload:
```

---

## 9. V16 Success Criteria

v16 is complete only when:

1. The v16 implementation plan is registered or otherwise tracked as implementation guidance.
2. Live post-v15 baseline is reconciled.
3. The matter-coupling DAG next-edge selector executes exactly one bounded selection packet.
4. The selector ranks candidate edges by burden-discharge potential.
5. The selected theorem route requires new mathematical payload.
6. The selected theorem route is executed or precisely handed off as the immediate next packet, depending on what P2 selects.
7. A concrete certificate-instance schema exists.
8. At least one valid transport certificate instance exists or is precisely obstructed.
9. At least one valid invariance certificate instance exists or is precisely obstructed.
10. At least one valid factorization certificate instance exists or is precisely obstructed.
11. Negative certificate instances exist for missing, malformed, target-import, detector-import, and process-authority cases.
12. Definitional equivalence and theorem content are separated.
13. At least one nontrivial equivalence property theorem is attempted, proved conditionally, or precisely failed.
14. Certificate algebra formalization is extended support-only.
15. Route-orbit detection has a selectively gating policy.
16. Minimum physics payload gate exists and is integrated.
17. Risky status fields have a layered future-facing schema or compatibility warning.
18. `EqSrc`, `RetainH`, and `GenH` trigger conditions are defined.
19. A source model zoo schema exists.
20. Initial finite/local source models exist.
21. Negative-result public language is audited and remediated if needed.
22. Manuscript split is preserved and refreshed.
23. One concrete red-team question packet exists.
24. Target-import attack suite exists or is precisely specified.
25. Compact current-frontier schema and output exist or are explicitly deferred with reason.
26. Documentation-impact consolidation is complete.
27. V16 validation layers pass or include exact pending reasons.
28. V16 coverage audit maps every `V16-Rxx` recommendation to evidence.
29. Final v16 handoff selects exactly one next route.
30. Final state remains public-safe.

---

## 10. Expected Public-Safe State After v16

Unless a later protected authority changes the scientific state, the public-safe state after v16 should remain:

```text
The AEther-Flow project has not derived GR from the source substrate.
M_src exists only as a scoped source-only object.
g_eff exists only as a scoped source-extension object.
Matter-sector results remain scoped evidence/preconditions only.
Narrow source-side matter-semantics results remain conditional/source-scoped and certificate-indexed.
Certificate instances and source models are finite/local support artifacts, not universal matter coupling.
Matter semantics, detector semantics, coupling law, universal matter coupling,
stress-energy semantics, matter action, Einstein equations, exact-GR benchmark
promotion, and completed derivation remain unestablished.
The next lawful research route is whatever final v16 handoff selects, and that
route must remain bounded, source-backed, and non-promotional unless protected
authority explicitly changes the claim boundary.
```

---

## 11. Appendix A — Recommended Artifact Names

Local agents may adjust exact filenames to match active repository conventions, but should preserve these semantic names.

| Artifact | Suggested path |
| --- | --- |
| v16 plan | `implementations_plans/recommendations_implementation_plan_continue_task-v16.md` |
| v16 baseline reconciliation | `research_control/tasks/<task_id>/artifacts/v16_post_v15_baseline_reconciliation_report.md` |
| v16 trace matrix | `research_control/tasks/<task_id>/artifacts/v16_recommendation_trace_matrix.csv` |
| DAG readiness audit | `research_control/tasks/<task_id>/artifacts/matter_coupling_dag_readiness_audit_v16.md` |
| DAG edge scoring rubric | `research_control/tasks/<task_id>/artifacts/matter_coupling_dag_next_edge_scoring_rubric_v16.md` |
| DAG edge selector | `research_control/tasks/<task_id>/artifacts/matter_coupling_dag_next_edge_selector_v16.md` |
| selected theorem setup | `research_control/tasks/<task_id>/artifacts/selected_matter_coupling_dag_edge_theorem_packet_setup_v16.md` |
| coupling-law target spec | `research_control/tasks/<task_id>/artifacts/source_side_coupling_law_target_specification_v1.tex` |
| selected theorem smuggling audit | `research_control/tasks/<task_id>/artifacts/selected_matter_coupling_edge_smuggling_audit_v16.tex` |
| selected theorem Refuter stress | `research_control/tasks/<task_id>/artifacts/selected_matter_coupling_edge_refuter_stress_v16.tex` |
| certificate-instance schema | `research_control/design/source_certificate_instance_library_schema_v1.md` |
| transport instance | `research_control/tasks/<task_id>/artifacts/finite_local_transport_certificate_instance_v1.tex` |
| invariance instance | `research_control/tasks/<task_id>/artifacts/finite_local_invariance_certificate_instance_v1.tex` |
| factorization instance | `research_control/tasks/<task_id>/artifacts/finite_local_factorization_certificate_instance_v1.tex` |
| negative certificate packet | `research_control/tasks/<task_id>/artifacts/negative_certificate_instance_packet_v1.tex` |
| certificate instance index | `research_control/design/source_certificate_instance_library_index_v1.md` |
| equivalence separation audit | `research_control/tasks/<task_id>/artifacts/eqms_definition_theorem_content_separation_audit_v16.tex` |
| refactored equivalence target | `research_control/tasks/<task_id>/artifacts/refactored_certificate_indexed_source_equivalence_target_spec_v1.tex` |
| equivalence property theorem | `research_control/tasks/<task_id>/artifacts/certificate_indexed_equivalence_property_theorem_attempt_v1.tex` |
| formalization scope selector | `research_control/tasks/<task_id>/artifacts/v16_formalization_scope_selector.md` |
| formalization integration report | `research_control/tasks/<task_id>/artifacts/v16_formalization_integration_report.md` |
| minimum payload schema | `research_control/design/minimum_physics_payload_schema_v1.md` |
| route-orbit gating policy | `research_control/design/route_orbit_gating_policy_v16.md` |
| risky field audit | `research_control/tasks/<task_id>/artifacts/risky_status_field_audit_v16.md` |
| layered status schema | `research_control/design/layered_status_field_schema_v16.md` |
| upstream trigger list | `research_control/design/eqsrc_retainh_genh_trigger_list_v16.md` |
| source model zoo schema | `research_control/design/source_model_zoo_schema_v1.md` |
| source model zoo | `research_control/design/source_model_zoo_v1.md` |
| negative-result language audit | `research_control/tasks/<task_id>/artifacts/negative_result_reader_language_audit_v16.md` |
| physics manuscript refresh | `research_control/tasks/<task_id>/artifacts/physics_manuscript_status_refresh_v16.md` |
| AI manuscript refresh | `research_control/tasks/<task_id>/artifacts/ai_methodology_manuscript_status_refresh_v16.md` |
| manuscript split checklist | `research_control/design/manuscript_split_boundary_checklist_v16.md` |
| red-team question selector | `research_control/tasks/<task_id>/artifacts/one_question_red_team_question_selector_v16.md` |
| red-team packet | `research_control/design/one_question_red_team_packet_v16.md` |
| target import taxonomy | `research_control/design/target_import_attack_taxonomy_v16.md` |
| target import fixtures | `research_control/design/target_import_attack_fixture_catalog_v16.md` |
| compact frontier schema | `research_control/design/compact_current_frontier_schema_v16.md` |
| compact frontier YAML | `output/compact_current_frontier_v16.yaml` |
| compact frontier JSON | `output/compact_current_frontier_v16.json` |
| validation inventory | `research_control/design/validation_command_inventory_v16.md` |
| v16 coverage audit | `research_control/tasks/<task_id>/artifacts/v16_recommendation_coverage_audit.md` |
| final validation report | `research_control/tasks/<task_id>/artifacts/v16_final_validation_report.json` |
| final handoff | `research_control/handoffs/handoff-<next>.yaml` and `.md` |

---

## 12. Appendix B — Minimal AgentJob Contract Fragment for v16 Physics Tasks

```yaml
job_contract_fragment:
  plan_id: "recommendations_implementation_plan_continue_task-v16"
  implementation_driver: "continue_research"
  target_derivation_milestone: "<from gr_derivation_burden_map>"
  milestone_burden: "<exact burden attempted>"
  role_decomposition:
    mode: "parent_child_parallel_synthesis"
  claim_boundary:
    proof_authority: false
    ontology_edit_authorized: false
    source_law_adoption_authorized: false
    rr_e_transport_law_adoption_authorized: false
    unrestricted_rr_e_irrelevance_authorized: false
    matter_semantics_adoption_authorized: false
    detector_semantics_adoption_authorized: false
    coupling_law_adoption_authorized: false
    matter_coupling_derivation_authorized: false
    matter_coupling_adoption_authorized: false
    stress_energy_semantics_authorized: false
    matter_action_authorized: false
    downstream_physics_promotion_authorized: false
    benchmark_promotion_authorized: false
    completed_derivation_authorized: false
  completion_contract:
    physics_progress_status_required: true
    distance_to_gr_delta_required: true
    mathematical_payload_manifest_required: true
    minimum_payload_class_required: true
    route_orbit_signature_required: true
    forbidden_conclusion_summary_required: true
    freeze_criteria_status_required_if_obstruction_or_repeated_burden: true
    upstream_primitive_trigger_status_required: true
```

---

## 13. Appendix C — Minimal Selector Completion Fragment

```yaml
selector_completion_fragment:
  plan_id: "recommendations_implementation_plan_continue_task-v16"
  selector_role: "theoretical-continuation-selector@0.1.0"
  selected_route:
    route_id: "<exact route id>"
    source_edge_id: "<dag edge id or not_applicable>"
    role_family: "<role>"
    target_derivation_milestone: "<milestone>"
    milestone_burden: "<burden>"
    requires_human_gate: false
  candidate_routes:
    - route_id:
      disposition: "<selected|not_selected>"
      reason:
      burden_discharge_potential:
      target_import_risk:
      route_orbit_risk:
      payload_requirement:
  next_packet_requires_new_payload: true
  distance_to_gr_delta:
    effect: "no_distance_delta"
    changed: false
  forbidden_conclusion_summary: >
    This selector does not authorize source-law adoption, RR_ETransportCompletenessOrInvarianceLaw_v1 adoption,
    unrestricted RR_E theorem status, matter-semantics adoption, detector-semantics adoption,
    coupling-law adoption, matter-coupling derivation or adoption, stress-energy semantics,
    matter action, Einstein equations, benchmark promotion, or completed derivation.
```

---

## 14. Appendix D — Minimal Completion Fragment for v16 Physics Tasks

```yaml
physics_progress_status:
  status: "<no_distance_delta | scoped_evidence_precondition | scoped_source_only_object | scoped_source_extension_object | conditional_theorem_candidate | obstruction_recorded | frozen_negative | finite_local_witness_recorded | certificate_instance_recorded | source_model_recorded | milestone_discharge | protected_gate_pending>"
  target_derivation_milestone: "<milestone>"
  milestone_burden: "<burden>"
  explanation: "<plain-language actual research delta>"

distance_to_gr_delta:
  changed: <true|false>
  burden_id: "<ledger burden id or blank>"
  milestone: "<milestone or blank>"
  old_status: "<old status or blank>"
  new_status: "<new status or blank>"
  ledger_row_updated: <true|false>
  downstream_unlocked:
    - "<bounded non-promotional route if any>"
  downstream_still_blocked:
    - "source-law adoption"
    - "RR_ETransportCompletenessOrInvarianceLaw_v1 adoption"
    - "unrestricted RR_E theorem"
    - "matter-semantics adoption"
    - "detector-semantics adoption"
    - "coupling-law adoption"
    - "matter-coupling derivation or adoption"
    - "stress-energy semantics"
    - "matter action"
    - "Einstein equations"
    - "benchmark promotion"
    - "completed derivation"

mathematical_payload_manifest:
  new_definitions:
    - "<name or none>"
  new_lemmas:
    - "<name or none>"
  new_theorems_or_theorem_targets:
    - "<name or none>"
  proof_attempts:
    - "<name or none>"
  finite_local_witnesses:
    - "<name or none>"
  certificate_instances:
    - "<name or none>"
  source_models:
    - "<name or none>"
  countermodels_or_obstructions:
    - "<name or none>"
  executable_support_specs:
    - "<name or none>"
  attack_fixtures:
    - "<name or none>"

minimum_payload_class:
  class: "<payload class>"
  exception_applies: false
  exception_reason: ""

route_orbit_signature:
  target_derivation_milestone:
  milestone_burden:
  object_or_claim_name:
  route_family:
  mathematical_payload_class:
  distance_to_gr_delta:
  next_route_selected:

upstream_primitive_trigger_status:
  EqSrc:
    triggered: false
    reason: ""
  RetainH:
    triggered: false
    reason: ""
  GenH:
    triggered: false
    reason: ""

forbidden_conclusion_summary: >
  This task does not authorize source-law adoption, RR_ETransportCompletenessOrInvarianceLaw_v1 adoption,
  unrestricted RR_E theorem status, matter-semantics adoption, detector-semantics adoption,
  coupling-law adoption, matter-coupling derivation or adoption, stress-energy semantics,
  matter action, Einstein equations, benchmark promotion, or completed derivation.
```

---

## 15. Appendix E — Phase-to-Recommendation Coverage Checklist

This checklist must be completed in P17-T01.

| Recommendation | Required evidence before v16 complete |
| --- | --- |
| `V16-R01` | P2 next-edge selector and P3 selected theorem-route packet or exact handoff |
| `V16-R02` | P4 certificate-instance schema and positive/negative instance packets |
| `V16-R03` | P5 equivalence/theorem separation audit and refactored theorem target |
| `V16-R04` | P6 support-only executable/formal certificate spec |
| `V16-R05` | P7 route-orbit gating policy and validator integration |
| `V16-R06` | P7 minimum physics payload schema and validator integration |
| `V16-R07` | P2 scoring rubric and selector matrix |
| `V16-R08` | P8 risky field audit and layered status field schema |
| `V16-R09` | P9 upstream primitive trigger list |
| `V16-R10` | P10 source model zoo schema and initial model zoo |
| `V16-R11` | P11 negative-result language audit and update/no-op receipt |
| `V16-R12` | P12 manuscript split refresh and boundary checklist |
| `V16-R13` | P13 one-question red-team packet and internal pilot or human-outreach handoff |
| `V16-R14` | P14 target-import attack taxonomy, fixtures, and validator integration |
| `V16-R15` | P15 compact frontier schema, renderer/output, and check integration |

---

## 16. Appendix F — Preferred P2 Edge Ranking Seed

The local selector must not blindly copy this seed. It must inspect the live DAG. This seed is included to prevent the selector from starting in the mist.

| Candidate edge | Default ranking | Reason |
| --- | --- | --- |
| `mc_source_matter_semantics_equivalence_theorem → mc_coupling_law_target` | 1 | Narrowest route with available source-certificate machinery, strong payload potential, and manageable target-import risk. |
| `mc_rr_e_certificate_boundary → mc_source_matter_semantics_equivalence_theorem` | 2 | Good for theorem-content strengthening if P5/P4 reveals certificate weaknesses. |
| `mc_certificate_gap_obstruction → mc_source_matter_semantics_equivalence_theorem` | 3 | Good if the immediate burden is repairing unconditional overread or strengthening fail-closed logic. |
| `mc_detector_semantics_target → mc_universal_matter_coupling_derivation` | 4 | Important but conceptually broad; likely requires new semantic target work. |
| `mc_coupling_law_target → mc_universal_matter_coupling_derivation` | 5 | Important but premature until coupling-law target/candidate specification exists. |
| `mc_stress_energy_semantics_target → mc_stress_energy_tensor_target` | 6 | Downstream and high target-import risk. |
| `mc_stress_energy_tensor_target → mc_matter_action_target` | 7 | Downstream and likely premature. |
| `mc_matter_action_target → mc_einstein_equation_dependency` | 8 | Blocked by missing action/dynamics path. |
| `mc_universal_matter_coupling_derivation → mc_einstein_equation_dependency` | 9 | Premature before matter coupling. |
| `mc_einstein_equation_dependency → mc_benchmark_promotion_dependency` | 10 | Protected and far downstream. |

---

## 17. Appendix G — Hard Blocks to Repeat in Every Handoff

```text
No canonical ontology edit.
No source-law adoption.
No RR_ETransportCompletenessOrInvarianceLaw_v1 adoption.
No unrestricted RR_E theorem.
No PositiveMSProfile_v1 adoption.
No SourceMatterSemanticsAdoptionReadinessLaw_v1 adoption as law.
No matter-semantics adoption.
No detector-semantics adoption.
No coupling-law adoption.
No matter-coupling derivation.
No matter-coupling adoption.
No stress-energy semantics.
No stress-energy tensor.
No matter action.
No Einstein equations.
No benchmark promotion.
No benchmark closure.
No completed derivation.
No future source-extension impossibility claim.
No program-wide rejection claim.
No generated derivative as proof authority.
No validator PASS as scientific proof.
No Gate Chair status outside exact scoped authority.
```

---

## 18. Appendix H — Compact Next Action if Local Agent Needs a Single Starting Packet

If the local agent needs one immediate starting task after registering this plan, use:

```yaml
task_type: "matter_coupling_dag_next_edge_theorem_route_selection_v16"
role_family: "theoretical-continuation-selector@0.1.0"
target_derivation_milestone: "matter_coupling"
milestone_burden: >
  Select exactly one next theorem edge from matter_coupling_dependency_dag_v1.
  The selected edge must require new mathematical payload and must not authorize
  matter-coupling derivation or adoption.
preferred_candidate_edge:
  source: "mc_source_matter_semantics_equivalence_theorem"
  target: "mc_coupling_law_target"
preferred_next_theorem_packet:
  route_id: "source_side_coupling_law_target_specification_under_explicit_certificates"
  expected_output_status: "draft_control_coupling_law_target_specification_only"
required_payload:
  - "formal candidate object definition"
  - "required certificate inputs"
  - "blocked target imports"
  - "finite/local witness obligation"
  - "Refuter countermodel obligation"
forbidden_conclusions:
  - "source-law adoption"
  - "matter-semantics adoption"
  - "detector-semantics adoption"
  - "coupling-law adoption"
  - "matter-coupling derivation or adoption"
  - "stress-energy semantics"
  - "matter action"
  - "Einstein equations"
  - "benchmark promotion"
  - "completed derivation"
```

---

## 19. Final Instruction to Local Agents

Do not “implement v16” by editing many files at once.

Use Continue Research. Treat every phase and task as a bounded transaction. Let the Director route. Let the AgentJob constrain. Let Refuters attack. Let validators complain. Let handoffs speak plainly.

The strongest v16 success condition is not that the project sounds closer to GR. The strongest v16 success condition is that the project becomes harder to fool while producing the next mathematically inspectable bridge plank.
