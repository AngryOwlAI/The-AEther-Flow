<!-- authority: implementation_plan -->

# Recommendations Implementation Plan for `/continue-research`, v12

**Filename:** `recommendations_implementation_plan_continue_task-v12.md`  
**Intended repository path:** `implementations_plans/recommendations_implementation_plan_continue_task-v12.md`  
**Generated date:** 2026-06-29  
**Plan ID:** `recommendations_implementation_plan_continue_task-v12`  
**Implementation driver:** Continue Research functionality only  
**Primary implementation lane:** `research_control/` bounded transactions  
**Scope:** Integrate the recommendations from the external project analysis section titled **“8. Recommendations”** into the AEther-Flow project.  
**Recommendations in scope:** all ten numbered recommendations from that section, renumbered in this plan as `R1` through `R10`.  
**Project state assumed by this plan:** post-`RT-20260614-290`, post-`handoff-0323`, with v11 implementation-plan work complete and no remaining v11 task.  
**Core invariant:** this plan is implementation guidance only. It is not physics authority, not a Gate Chair verdict, not a canonical ontology edit, not benchmark promotion, and not completed-derivation evidence.

---

## 0. Executive Implementation Intent

This v12 implementation plan converts the recommendations from the recent project review into a sequence of bounded local AI-agent tasks. Every phase and every task must be implemented through the repository's **Continue Research** workflow, not by informal manual edits. The local Director of Research must route one bounded AgentJob per invocation, preserve the repository's authority hierarchy, run the required validators, and checkpoint only through the approved research transaction path.

The plan has eleven implementation phases:

1. **P0 — Plan intake and baseline authority reconciliation.** Track this v12 plan, establish a clean baseline, and prove that continuation is starting from the post-v11 closed state.
2. **P1 — Distance-to-GR ledger status-layer split.** Separate control status, mathematical status, and physical status so that labels such as `accepted` cannot be overread.
3. **P2 — Canonical frontier theorem inventory.** Create a compact source-backed mathematical inventory of current theorem-like objects, decisions, obstructions, assumptions, and missing theorems.
4. **P3 — New tracked objective restart.** Create the first post-v11 tracked research objective and route the next scientific continuation deliberately rather than by plan inertia.
5. **P4 — Source-extension minimization and compression.** Determine whether the current scoped source-extension stack can be compressed into a smaller source-side law package, or identify the irreducible missing primitives.
6. **P5 — Matter-semantics preflight before Einstein-equation work.** Formalize the source-side matter-sector semantics burden before any Einstein-equation or benchmark-promotion route is attempted.
7. **P6 — Support-only formalization and proof-assistant bridge.** Add a support-only formalization lane beginning with the finite toy obstruction and finite/local source-side definitions.
8. **P7 — External red-team review mode.** Add a review mode that ignores workflow success and attacks only definitions, assumptions, theorem statements, circularity, and hidden target imports.
9. **P8 — Route-orbit guard hardening.** Strengthen same-burden and same-shape loop controls after the v11 closure.
10. **P9 — Public-facing current-status clarity.** Make it impossible for README, website, GitHub-facing pages, or generated explainers to imply that GR has already been derived.
11. **P10 — Literature-comparison packet.** Compare the project against neighboring research programs and known reconstruction/no-go constraints without using literature comparison as claim promotion.
12. **P11 — Final integration audit, metrics, and continuation handoff.** Validate the rollout, regenerate derived surfaces, and hand off to ordinary research continuation under the new objective.

The plan deliberately keeps **physics continuation**, **project-system improvement**, **documentation publication**, **validator/tooling work**, and **human-gated Gate Chair authority** separated. When a task has no mathematical payload, it must be routed as project-system work. When a task is scientific, it must declare a target derivation milestone and milestone burden, include a new mathematical payload, and preserve all forbidden-conclusion boundaries.

---

## 1. Recommendation Map

| Plan recommendation ID | Source recommendation from analysis | Main implementation phase(s) | Primary output type | Physics promotion allowed? |
|---|---|---|---|---:|
| `R1` | Split the Distance-to-GR ledger into control, mathematical, and physical statuses. | P1 | CSV/schema/tooling/control docs | No |
| `R2` | Create a canonical frontier theorem inventory. | P2 | Canonical control/science-facing Markdown or TeX inventory plus registry rows | No, unless later Gate Chair authority exists |
| `R3` | Launch a source-extension minimization/compression packet. | P3, P4 | Physics AgentJobs and TeX/YAML artifacts | No automatic promotion |
| `R4` | Do not pursue Einstein equations until matter semantics are source-side. | P5 | Matter-semantics target, candidate, audit, stress, selector | No automatic promotion |
| `R5` | Add proof-assistant or typed-formalization support, starting small. | P6 | Support-only tooling, formal skeletons, tests | No |
| `R6` | Add an external-red-team review mode. | P7 | Role contract/schema/templates/pilot review | No |
| `R7` | Make route-orbit warnings harder after v11 closure. | P8 | Validator and Continue Research warning/guard changes | No |
| `R8` | Make public-facing status impossible to overread. | P9 | README/GitHub-facing/website source updates and generated derivatives | No |
| `R9` | Map the work against neighboring research programs. | P10 | Literature-comparison control packet | No |
| `R10` | Choose the next tracked objective deliberately. | P3 and P11 | New tracked objective and final handoff | No automatic promotion |

---

## 2. Source Basis and Current Project State Assumptions

Local agents must verify all assumptions from tracked repository state before acting. This plan is not independent authority and must be adapted if `research_control/program_state.yaml` or the latest handoff has advanced.

### 2.1 Required starting-state sources to inspect

Before P0 and before any later phase that changes control or science-bearing state, inspect the current tracked state from at least:

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `research_control/program_state.yaml`
- `research_control/current_frontier.md`
- `research_control/handoffs/handoff-0323.yaml`
- `research_control/handoffs/handoff-0323.md`
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
- `scripts/research_control/continue_research.py`
- `scripts/research_control/validate_research_control.py`
- `scripts/research_control/report_physics_progress_metrics.py`
- `scripts/research_control/render_current_frontier.py`
- `scripts/research_control/render_dependency_graph.py`
- `scripts/project_control/classify_project_changes.py`
- `scripts/project_control/validate_documentation_impact.py`
- `FOLDER_MAP.md`

### 2.2 Current state expected by this plan

This plan assumes the active state after v11 closure is:

- Active task: `RT-20260614-290`
- Latest handoff: `handoff-0323`
- Current status: `v11_p0_evidence_closure_completed_all_plan_tasks_proven_no_promotion`
- Current route family: v11 implementation plan complete, no remaining implementation task
- Required next authority: ordinary research-control continuation under a new tracked objective only
- Distance-to-GR changed by latest task: no
- Physics claim promotion in latest task: no

If these assumptions are false because the repository has advanced, local agents must:

1. Stop using this plan as a literal state snapshot.
2. Read the latest `program_state.yaml`, handoff, current-frontier snapshot, and Distance-to-GR ledger.
3. Route one bounded Director decision to adapt the plan intent to the latest tracked state.
4. Preserve the same recommendation objectives without replaying already completed tasks.

### 2.3 Current scientific frontier expected by this plan

The plan assumes the current science state is approximately:

- `source_ontology_primitives`: draft object exists, canonical adoption rules remain blocking.
- `source_equivalence_eqsrc`: draft object exists, general equivalence under variations remains undischarged.
- `RetainH` and `GenH`: blocked by missing primitive.
- `ObsLoc_lc`: constructive witness exists, still bounded by robustness and exact-branch limits.
- `Resp_lc`: accepted only in a scoped source-extension sense.
- `M_src`: accepted as scoped source-only `M_src` under declared H1-H13/fail-closed boundary.
- `g_eff`: accepted only as a scoped source-extension `g_eff` object under declared source-side scope.
- `matter_coupling`: current ledger status is vulnerable to overread; substance is accepted scoped parameterized-witness evidence/precondition only, not matter-coupling derivation.
- `einstein_equations`: not started.
- `benchmark_promotion`: blocked by missing primitive and Gate Chair authority.
- `finite_toy_metric_response`: frozen negative for the explicit-tag-only route.

The plan's purpose is to make these states clearer, more compressed, more externally reviewable, and more difficult to overclaim.

---

## 3. Universal Continue Research Protocol

Every phase and every task below must be executed through Continue Research. Unless a task explicitly says otherwise, each task is **one bounded `/continue-research` transaction** with exactly one outer AgentJob.

### 3.1 Required pre-routing commands

Before every task-routing decision, run:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "<task-specific targeted phrase>" --limit 10 --json
.venv/bin/python scripts/research_control/continue_research.py --json
```

If memory search returns relevant objects, inspect the canonical source files or registry rows named by the hits. Memory, wiki notes, semantic extracts, Obsidian, SQLite, PDFs, generated HTML, and `.local/` caches are retrieval aids only. They do not override tracked source files or registries.

### 3.2 Required Director behavior

For every task:

1. Use the Director of Research only when `continue_research.py` indicates that a Director decision is required or when the active handoff explicitly requests a new objective.
2. Create exactly one Director Decision Record unless a valid active DDR already exists for that exact task.
3. Create exactly one outer AgentJob.
4. Choose the narrowest role that can complete the task.
5. Preserve active claim boundaries.
6. Use `parent_child_parallel_synthesis` for physics AgentJobs created under the post-2026-06-17 physics contract.
7. For physics AgentJobs, declare `target_derivation_milestone` and `milestone_burden` from the burden map.
8. For physics completions, include a new mathematical payload and the mathematical-decisiveness fields.
9. For project-system tasks, explicitly state that the task changes control/tooling/documentation only and does not promote physics claims.
10. Do not route Gate Chair work unless exact tracked human authorization exists.
11. If exact Gate Chair authorization is missing, create a human-gated handoff or route a non-promotional selector/control packet, not an implied verdict.
12. If a task discovers project-improvement signals, preserve the normal research handoff and create a sidecar project-improvement handoff only as allowed by existing governance.

### 3.3 Required post-execution validation commands

After any state-changing AgentJob, run the full validation suite appropriate to its scope. The default suite is:

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

Add task-specific tests when changing scripts, validators, schemas, renderers, or formalization tooling:

```zsh
.venv/bin/python -m unittest discover -s tests
```

If any validation fails, do not checkpoint. Repair through the same bounded AgentJob if within allowed scope; otherwise hand off to a separate bounded repair task.

### 3.4 Required checkpoint command

Checkpoint only through:

```zsh
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py
```

Do not stage or commit manually if the checkpoint script is the required control path. If a task is read-only, record the read-only result and do not create a fake checkpoint.

### 3.5 Required completion fields for physics tasks

Physics tasks governed by the mathematical-decisiveness contract must include:

- `physics_progress_status`
- `distance_to_gr_delta`
- `distance_to_gr_status`
- `mathematical_payload_manifest`
- `forbidden_conclusion_summary`
- `parent_child_synthesis`
- `freeze_criteria_status` when a burden repeats or a scoped obstruction is produced
- `route_cycle_control` when the task is part of a constructor/audit/stress/selector cycle
- `candidate_constructor_result` for Candidate Constructor tasks
- `theoretical_decision_output` for Theoretical Continuation Selector tasks
- `obstruction_record` when a precise obstruction or freeze is produced
- `source_extension_category` when source-extension data are introduced, audited, stress-tested, accepted, rejected, or minimized

### 3.6 Universal forbidden conclusions

Unless an exact protected authority packet explicitly grants a narrower conclusion, every task must preserve:

- no canonical ontology edit
- no source-law adoption
- no `MetricData(E)` adoption
- no unscoped `g_eff` adoption
- no `g_eff` scope expansion
- no coupling-law adoption
- no matter-coupling derivation
- no matter-coupling adoption
- no stress-energy semantics import
- no stress-energy tensor construction
- no matter action import
- no detector semantics import
- no Einstein-equation derivation
- no exact-GR benchmark promotion
- no benchmark Gate Chair closure
- no completed derivation
- no future source-extension impossibility
- no global theory rejection
- no validator, registry, generated derivative, support-only checker, local cache, handoff, approval, file order, commit state, PDF, HTML, wiki object, dependency graph, metrics report, or current-frontier snapshot as scientific proof

---

## 4. Role and Route Matrix

| Work type | Preferred role family | Physics milestone required? | Human gate? | Notes |
|---|---|---:|---:|---|
| Plan intake and implementation-plan tracking | `process-integrity-auditor`, `documentation-curator`, or project-control role | No | No | Control guidance only. No physics status change. |
| Ledger schema/status split | `validator-engineer`, `process-integrity-auditor`, or project-control maintainer | No | No | Changes control representation, not science. |
| Distance-to-GR row migration | `process-integrity-auditor` with validator support | No, unless a row changes science status | No | Must preserve original science meaning exactly. |
| Frontier theorem inventory design | `ontology-formalizer` if science-bearing, otherwise project-control maintainer | Possibly | No | If it states theorem-like claims, use science-draft role and canonical source inspection. |
| Frontier inventory population | `ontology-formalizer`, `process-integrity-auditor`, or documentation/control overlay depending on content | Possibly | No | Must cite canonical artifacts and preserve blocked claims. |
| New objective selector | `theoretical-continuation-selector@0.1.0` | Yes | No | Required to restart ordinary physics continuation deliberately. |
| Source-extension minimization | `ontology-formalizer`, `candidate-constructor`, `smuggling-auditor`, `refuter`, `theoretical-continuation-selector` | Yes | Maybe | Gate Chair only if exact protected adoption or rejection is requested. |
| Matter-semantics preflight | `ontology-formalizer`, `candidate-constructor`, `smuggling-auditor`, `refuter`, `theoretical-continuation-selector` | Yes | Maybe | No Einstein-equation task until matter semantics are source-side. |
| Support-only formalization tooling | `validator-engineer`, `memory-system-maintainer`, project-control maintainer | No, unless writing science definitions | No | Tooling output is not proof authority. |
| Formal theorem skeleton | `ontology-formalizer` plus support-only tooling role | Yes if science-bearing | No | Formalization may support but not promote claims. |
| External red-team review mode | project-control maintainer, validator engineer, then red-team role if added | No for role creation; yes for pilot science review | No | Must not create claim-promotion authority. |
| Public-facing status update | `documentation-curator@2.0.0` | No | No | Update source specs and regenerate derivatives. |
| Literature comparison packet | theoretical selector or documentation/literature-review overlay | Possibly | No | Must distinguish external literature from project construction. |
| Final integration audit | `process-integrity-auditor`, `validator-engineer`, documentation curator | No | No | Cross-phase validation and handoff only. |

---

## 5. Phase Overview and Dependencies

| Phase | Implements | Primary dependency | Primary result | May be deferred? |
|---|---|---|---|---:|
| P0 | plan intake, baseline | latest state after v11 | v12 plan tracked and baseline proved | No |
| P1 | R1 | P0 | layered Distance-to-GR status representation | No |
| P2 | R2 | P1 preferred | canonical frontier theorem inventory | No |
| P3 | R10 | P0-P2 preferred | first new post-v11 tracked objective | No |
| P4 | R3 | P2-P3 | source-extension minimization/compression result | Yes only if P3 selects P5 first |
| P5 | R4 | P2-P3; P4 preferred | source-side matter-semantics preflight result | Yes only if P3 selects P4 first and P4 blocks |
| P6 | R5 | P2; can run in parallel with P4/P5 only under separate tasks | support-only formalization lane | Yes |
| P7 | R6 | P2; P8 preferred before pilot enforcement | red-team review mode and pilot | Yes |
| P8 | R7 | P1-P3; metrics available | route-orbit guard hardening | No, but can be advisory first |
| P9 | R8 | P1-P2 | README/website/status clarification | No |
| P10 | R9 | P2; can inform P4/P5 | literature comparison map | Yes |
| P11 | all | P0-P10 complete or explicitly deferred | integration audit and handoff | No |

---

# P0 — Plan Intake, Authority Bootstrap, and Baseline Snapshot

## P0 purpose

P0 brings this v12 plan into the repository as tracked implementation guidance and proves that the project is starting from the correct post-v11 baseline. It must not change physics state.

## P0-T01 — Track the v12 implementation plan

**Recommendation integrated:** prerequisite for all recommendations  
**Task type:** project-system / implementation-plan intake  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `process-integrity-auditor@0.1.0` or `documentation-curator@2.0.0` if documentation impact dominates  
**Physics milestone:** none  
**Claim boundary:** no physics claim promotion

### Objective

Add `implementations_plans/recommendations_implementation_plan_continue_task-v12.md` as the tracked implementation plan for integrating recommendations `R1` through `R10`.

### Required reads

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `implementations_plans/recommendations_implementation_plan_continue_task-v11.md`
- `.gitignore`
- `FOLDER_MAP.md`
- `research_control/tasks/README.md`
- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0323.yaml`
- `research_control/current_frontier.md`
- `scripts/project_control/classify_project_changes.py`
- `scripts/project_control/validate_documentation_impact.py`

### Required outputs

- Tracked plan file at `implementations_plans/recommendations_implementation_plan_continue_task-v12.md`.
- Task record under `research_control/tasks/<new-task-id>/`.
- Director Decision Record.
- AgentJob contract.
- Completion receipt proving the plan was added as implementation guidance only.
- Documentation impact receipt, either with source updates or a valid no-op rationale.
- Handoff naming the next P0 task.

### Acceptance criteria

- The plan file exists in the intended path and is not ignored by Git.
- The completion receipt states that the plan is not physics authority.
- Validation passes.
- No Distance-to-GR ledger physics status changes occur.
- No canonical ontology TeX is edited.

### Forbidden outputs

- No new physics claim.
- No claim that v12 tasks have already been implemented.
- No registry or validator change unless required for plan tracking.
- No Gate Chair, benchmark, or completed-derivation language.

---

## P0-T02 — Post-v11 baseline authority snapshot

**Recommendation integrated:** prerequisite for `R1`, `R2`, `R10`  
**Task type:** process-control / baseline evidence  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `process-integrity-auditor@0.1.0`  
**Physics milestone:** none  
**Claim boundary:** baseline snapshot only, not scientific proof

### Objective

Create a standalone baseline snapshot proving the active state after v11 closure, including the active task, latest handoff, current status, Distance-to-GR ledger state, current-frontier snapshot hash, and blocked-claims list.

### Required reads

- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0323.yaml`
- `research_control/handoffs/handoff-0323.md`
- `research_control/current_frontier.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/tasks/RT-20260614-290/00_TASK.yaml`
- `research_control/tasks/RT-20260614-290/jobs/completions/AJC-AJ-RT-20260614-290-001.yaml`

### Required outputs

- Artifact: `research_control/tasks/<task-id>/artifacts/v12_p0_baseline_authority_snapshot.yaml`.
- Artifact: `research_control/tasks/<task-id>/artifacts/v12_p0_baseline_summary.md`.
- Completion receipt with:
  - active task ID
  - latest handoff ID
  - status string
  - Distance-to-GR row hashes or ledger hash
  - current-frontier hash
  - explicit forbidden-conclusion summary
  - statement that this is control evidence only

### Acceptance criteria

- The snapshot matches `program_state.yaml`, `handoff-0323`, `current_frontier.md`, and the ledger.
- Any mismatch triggers a repair handoff rather than silent correction.
- Validation passes.
- The handoff routes to P1-T01.

### Stop conditions

Stop and route a separate repair packet if:

- `current_frontier.md` disagrees with tracked authority.
- `program_state.yaml` names a newer handoff than expected.
- The Distance-to-GR ledger has advanced beyond this plan’s assumed state.

---

## P0-T03 — V12 implementation-plan registry and memory bootstrap receipt

**Recommendation integrated:** prerequisite for all recommendations  
**Task type:** memory/control hygiene  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `memory-system-maintainer@0.2.0` or `process-integrity-auditor@0.1.0`  
**Physics milestone:** none  
**Claim boundary:** generated memory is retrieval only

### Objective

Ensure the v12 plan, baseline snapshot, and associated control records are discoverable through source-first memory without treating generated derivatives as authority.

### Required reads

- P0-T01 completion receipt
- P0-T02 baseline snapshot
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/FILE_OBJECT_REGISTRY.csv`
- `registries/CONTENT_SEMANTIC_REGISTRY.csv`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `.codex/skills/project-memory-system/scripts/query_memory.py`

### Required outputs

- Updated registries if required by the memory system.
- Generated memory/wiki derivatives if required by bootstrap.
- Completion receipt recording source objects and generated retrieval objects separately.

### Acceptance criteria

- `bootstrap_memory_system.py` passes.
- `bootstrap_memory_system.py --validate-only` passes.
- A targeted query for `recommendations_implementation_plan_continue_task-v12` returns the canonical plan source row or an unambiguous pointer to it.
- The completion receipt states that memory/wiki/semantic extracts remain retrieval layers only.

---

# P1 — Distance-to-GR Ledger Status-Layer Split

## P1 purpose

P1 implements `R1`: split the Distance-to-GR ledger into statuses that distinguish **control acceptance**, **mathematical content**, and **physical interpretation**. This prevents rows such as `matter_coupling, accepted` from being misread as a physical matter-coupling derivation.

## P1-T01 — Layered status taxonomy design

**Recommendation integrated:** `R1`  
**Task type:** project-control design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `project-control-maintainer@0.2.0` or `process-integrity-auditor@0.1.0`  
**Physics milestone:** none  
**Claim boundary:** status vocabulary design only

### Objective

Design a layered status taxonomy for the Distance-to-GR ledger that separates:

1. `control_status`: the governance state of evidence, gate review, task completion, or ledger entry.
2. `mathematical_status`: the theorem, witness, construction, countermodel, obstruction, or source-extension status actually supplied.
3. `physical_status`: the physical interpretation status, especially whether a GR-relevant physical burden remains blocked.
4. `promotion_status`: whether any protected authority has promoted the claim beyond draft/control or scoped evidence.
5. `overread_guard`: a short machine-checkable phrase describing exactly what must not be concluded.

### Required reads

- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `research_control/current_frontier.md`
- `research_control/design/gr_derivation_burden_map.md`
- `research_control/tasks/RT-20260614-060/artifacts/101_RESP_LC_SOURCE_EXTENSION_HUMAN_GATE_ADOPTION_DECISION.tex`
- `research_control/tasks/RT-20260614-134/artifacts/165_M_SRC_GSC_INTEGRATED_SOURCE_ONLY_ADOPTION_THEOREM_GATE_CHAIR_REVIEW.tex`
- `research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex`
- `research_control/tasks/RT-20260614-269/artifacts/298_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_SOURCE_FAMILY_WITNESS_V1_SOURCE_EXTENSION_EVIDENCE_GATE_CHAIR_REVIEW.tex`
- `research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex`
- `scripts/research_control/validate_research_control.py`
- `scripts/research_control/render_current_frontier.py`

### Required outputs

- Design artifact: `research_control/design/distance_to_gr_status_layers_v1.md`.
- Proposed schema change description for the Distance-to-GR ledger.
- Migration plan describing how existing rows will be mapped without changing scientific status.
- Validator requirements for future row additions or edits.

### Suggested status vocabularies

`control_status` examples:

- `not_started`
- `draft_control_object_exists`
- `construction_recorded`
- `audit_passed`
- `refuter_stress_passed`
- `gate_review_completed`
- `accepted_as_scoped_evidence`
- `accepted_as_scoped_source_object`
- `frozen_negative`
- `human_gated`
- `blocked`

`mathematical_status` examples:

- `no_mathematical_object`
- `definition_only`
- `conditional_theorem_candidate`
- `constructive_witness`
- `finite_local_witness`
- `parameterized_witness_precondition`
- `scoped_source_extension_object`
- `source_only_adopted_object`
- `countermodel`
- `scoped_obstruction`
- `general_theorem_missing`

`physical_status` examples:

- `no_physical_interpretation_authorized`
- `benchmark_compatible_interpretive_boundary_only`
- `not_matter_coupling`
- `not_stress_energy`
- `not_einstein_equations`
- `not_benchmark_promotion`
- `downstream_gr_blocked`
- `human_gate_required_before_physical_reading`

### Acceptance criteria

- The design handles all current ledger rows without changing their scientific meaning.
- `matter_coupling` can no longer be represented in a way that reads as physical matter-coupling derivation.
- `g_eff` can be represented as scoped source-extension `g_eff` object while preserving no downstream GR claims.
- `M_src` can be represented as scoped source-only adopted object while preserving no metric or GR derivation.
- Frozen negative toy route remains frozen locally, not globally.
- Validation passes.

---

## P1-T02 — Ledger schema migration implementation

**Recommendation integrated:** `R1`  
**Task type:** control registry migration  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `process-integrity-auditor@0.1.0` with `validator-engineer@0.2.0` if script changes are needed  
**Physics milestone:** none  
**Claim boundary:** registry representation change only

### Objective

Modify `registries/DISTANCE_TO_GR_LEDGER.csv` to add the layered status columns designed in P1-T01, preserving all existing information and scientific meaning.

### Required reads

- P1-T01 design artifact
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `research_control/current_frontier.md`
- `scripts/research_control/render_current_frontier.py`
- `scripts/research_control/report_physics_progress_metrics.py`
- `scripts/research_control/validate_research_control.py`
- any tests that inspect the ledger schema

### Required outputs

- Updated `registries/DISTANCE_TO_GR_LEDGER.csv` with added columns.
- Migration artifact: `research_control/tasks/<task-id>/artifacts/distance_to_gr_layered_status_migration_report.md`.
- Completion receipt stating no science status was changed.
- If validators require update, corresponding script/test changes.

### Required migration mappings

Minimum required row treatments:

- `source_ontology_primitives`: control status `draft_control_object_exists`; mathematical status `definition_only_or_draft_object`; physical status `no_canonical_ontology_adoption`.
- `source_equivalence_eqsrc`: control status `draft_control_object_exists`; mathematical status `general_equivalence_theorem_missing`; physical status `downstream_gr_blocked`.
- `retain_h`: control status `blocked`; mathematical status `primitive_missing`; physical status `no_retention_law_adoption`.
- `gen_h`: control status `blocked`; mathematical status `primitive_missing`; physical status `no_generator_law_adoption`.
- `obsloc_lc`: control status `constructive_witness_recorded`; mathematical status `constructive_witness`; physical status `local_exact_branch_only`.
- `resp_lc`: control status `accepted_as_source_extension_data`; mathematical status `selector_data_source_extension`; physical status `not_detector_semantics_not_matter_coupling`.
- `m_src`: control status `gate_review_completed`; mathematical status `scoped_source_only_adopted_object`; physical status `not_target_manifold_not_metric_not_gr_derivation`.
- `g_eff`: control status `gate_review_completed`; mathematical status `scoped_source_extension_geff_object`; physical status `not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations`.
- `matter_coupling`: control status `accepted_as_scoped_evidence_precondition`; mathematical status `parameterized_finite_local_witness_precondition`; physical status `not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics`.
- `einstein_equations`: control status `not_started`; mathematical status `dynamics_action_or_variation_missing`; physical status `no_field_equation_derivation`.
- `benchmark_promotion`: control status `blocked`; mathematical status `upstream_burdens_missing`; physical status `no_exact_gr_benchmark_promotion`.
- `gate_chair_status`: control status `human_gated`; mathematical status `protected_verdict_missing`; physical status `no_benchmark_closure`.
- `finite_toy_metric_response`: control status `frozen_negative`; mathematical status `tag_removal_obstruction`; physical status `local_toy_route_frozen_not_global_theory_rejection`.

### Acceptance criteria

- The CSV remains parseable by existing or updated tools.
- All previous data are preserved or mapped into documented new fields.
- `render_current_frontier.py --check` passes after any renderer update.
- `report_physics_progress_metrics.py` passes.
- The migration report includes before/after row meaning for every changed row.
- No task claims that a status-layer change is a new physics result.

### Stop conditions

Stop and route validator repair if:

- Existing scripts cannot parse the modified ledger.
- A row’s physical status is ambiguous.
- The migration would require rewriting historical scientific artifacts.

---

## P1-T03 — Validator guard for layered ledger semantics

**Recommendation integrated:** `R1`, supports `R7`  
**Task type:** validator/tooling  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** validator only, not physics evidence

### Objective

Update validation so every Distance-to-GR ledger row has complete layered statuses and cannot use dangerous physical-overread terms without an explicit negation or authority source.

### Required reads

- P1-T01 design artifact
- P1-T02 migration report
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `scripts/research_control/validate_research_control.py`
- `tests/test_research_control.py`
- `research_control/current_frontier.md`

### Required validator checks

- Required columns exist.
- Each row has nonblank `control_status`, `mathematical_status`, `physical_status`, and `overread_guard`.
- Rows with `matter_coupling` cannot have physical status implying matter-coupling derivation unless a protected Gate Chair artifact is cited.
- Rows with `einstein_equations` cannot imply field-equation derivation unless the ledger cites a valid derivation artifact.
- Rows with `benchmark_promotion` cannot imply benchmark promotion unless protected benchmark Gate Chair closure exists.
- `accepted` may not appear as a standalone status without qualification in new columns.
- `physical_status` for scoped evidence must include explicit `not_*` or `blocked` wording.
- Generated snapshots may not override ledger status layers.

### Required outputs

- Updated validator script(s).
- New or updated tests.
- Completion receipt with command results.

### Acceptance criteria

- Unit tests pass.
- Validation fails on a fixture where `matter_coupling` is overread as actual matter coupling.
- Validation fails on a fixture where `g_eff` is overread as unscoped Lorentzian metric or benchmark evidence.
- Validation passes on the migrated live ledger.
- Metrics report still separates operational and scientific scoreboards.

---

## P1-T04 — Current-frontier renderer update for layered statuses

**Recommendation integrated:** `R1`, supports `R8`  
**Task type:** generated snapshot renderer update  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0` or `documentation-curator@2.0.0` if only rendering text changes  
**Physics milestone:** none  
**Claim boundary:** reader-facing control snapshot only

### Objective

Update `research_control/current_frontier.md` generation so it displays layered Distance-to-GR statuses and makes overread guards visible.

### Required reads

- P1-T02 migrated ledger
- P1-T03 validator updates
- `scripts/research_control/render_current_frontier.py`
- `research_control/current_frontier.md`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`

### Required outputs

- Updated renderer.
- Regenerated `research_control/current_frontier.md`.
- Tests or check-mode updates proving drift detection still works.
- Completion receipt emphasizing current-frontier is a generated snapshot only.

### Acceptance criteria

- The generated table includes control, mathematical, and physical status or a compact equivalent.
- `matter_coupling` display cannot be read as derived matter coupling.
- `g_eff` display cannot be read as unscoped physical metric adoption.
- Blocked Einstein-equation and benchmark-promotion statuses are explicit.
- `render_current_frontier.py --check` passes.

---

## P1-T05 — P1 cross-check and handoff

**Recommendation integrated:** `R1`  
**Task type:** process-integrity audit  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `process-integrity-auditor@0.1.0`  
**Physics milestone:** none  
**Claim boundary:** audit only

### Objective

Audit P1 outputs to confirm the layered status split is implemented, validated, rendered, and non-promotional.

### Required outputs

- Artifact: `p1_layered_status_cross_check.md`.
- Handoff to P2-T01.

### Acceptance criteria

- All P1 tasks are registered and completed.
- Ledger, validator, renderer, and current-frontier snapshot agree.
- No physics status changed except representation clarity.
- Handoff routes to canonical frontier theorem inventory design.

---

# P2 — Canonical Frontier Theorem Inventory

## P2 purpose

P2 implements `R2`: create a compact, canonical, source-backed inventory of the current theorem-like frontier. This inventory must be precise enough for external review and small enough to expose whether the project has a derivational core or a stack of auxiliary extensions.

## P2-T01 — Frontier theorem inventory schema design

**Recommendation integrated:** `R2`  
**Task type:** science/control schema design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `ontology-formalizer@0.2.0` if theorem semantics are included; otherwise `project-control-maintainer@0.2.0`  
**Physics milestone:** if routed as physics, `source_equivalence_eqsrc` or current burden selected by Director  
**Claim boundary:** inventory schema only, no claim promotion

### Objective

Design a schema for a canonical frontier theorem inventory that records each current theorem-like object, accepted scoped object, obstruction, frozen route, and missing theorem in a compact, source-backed form.

### Required fields per inventory item

- `frontier_item_id`
- `object_or_claim_name`
- `status_layer_summary`
- `source_artifact_path`
- `source_authority_type`
- `assumptions`
- `definitions_used`
- `statement_or_decision`
- `mathematical_conclusion`
- `physical_non_conclusions`
- `allowed_reuse`
- `blocked_reuse`
- `dependency_items`
- `missing_theorem_or_primitive`
- `candidate_next_task`
- `overread_guard`
- `external_review_notes`

### Required reads

- `registries/DISTANCE_TO_GR_LEDGER.csv`
- P1 status-layer design and migration report
- `research_control/design/gr_derivation_burden_map.md`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- Current key Gate Chair and Refuter artifacts

### Required outputs

- Schema artifact: `research_control/design/frontier_theorem_inventory_schema_v1.md`.
- Optional CSV or YAML schema fixture if validators will be added later.
- Completion receipt with no-promotion statement.

### Acceptance criteria

- Schema distinguishes theorem, definition, witness, obstruction, gate decision, and source-extension evidence.
- Schema can represent `Resp_lc`, `M_src`, `g_eff`, matter-coupling precondition evidence, finite toy frozen negative, and open Einstein-equation burden.
- Schema includes explicit non-conclusions for physical claims.
- Schema does not make generated current-frontier snapshot independent authority.

---

## P2-T02 — Canonical inventory source-location decision

**Recommendation integrated:** `R2`  
**Task type:** project-control routing  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `process-integrity-auditor@0.1.0` or `project-control-maintainer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** source-location decision only

### Objective

Decide where the canonical frontier theorem inventory should live and how it should be registered. The plan recommends one of two options:

- Option A: `research_control/design/frontier_theorem_inventory.md` as a control/science bridge document.
- Option B: `ontology/tex/frontier_theorem_inventory.tex` if the inventory will contain science-bearing theorem statements with canonical physics authority.

### Decision criteria

Use Option A if the inventory summarizes existing artifacts without creating new theorem statements. Use Option B if it states new canonical theorem propositions, definitions, or mathematical claims.

### Required outputs

- Director Decision Record explaining Option A or Option B.
- If Option A, registered Markdown source path.
- If Option B, registered TeX source path and any PDF derivative rules.
- Completion receipt explaining authority implications.

### Acceptance criteria

- Chosen location respects the authority hierarchy.
- Generated wiki or HTML derivatives are not treated as canonical inventory.
- If TeX is chosen, PDF derivative handling is documented.

---

## P2-T03 — Populate inventory with current accepted and frozen frontier items

**Recommendation integrated:** `R2`  
**Task type:** science/control synthesis  
**Continue Research requirement:** one bounded `/continue-research` transaction; if too large, split into P2-T03A and P2-T03B through explicit handoff  
**Suggested role:** `ontology-formalizer@0.2.0` with `parent_child_parallel_synthesis` if physics-bearing  
**Physics milestone:** likely `source_equivalence_eqsrc`, `effective_metric_g_eff`, or `matter_coupling`; Director must choose exact burden  
**Claim boundary:** inventory records existing claims only

### Objective

Populate the canonical frontier theorem inventory with all current high-value accepted, scoped, blocked, and frozen items.

### Minimum required inventory items

1. `source_ontology_primitives` draft status.
2. `source_equivalence_eqsrc` draft/undischarged status.
3. `RetainH` blocked by missing primitive.
4. `GenH` blocked by missing primitive.
5. `ObsLoc_lc` constructive witness status.
6. `Resp_lc` source-extension selector data adoption.
7. `M_src^{GSC}` scoped source-only adoption.
8. `g_eff^{GSC-cand}` scoped source-extension object adoption.
9. `MatterCouplingBridgeTarget_v1` draft/control formalization chain.
10. `ParamFiniteLocalWitness_v1`, `BridgeSlot_n`, `NoTargetImport_n` scoped evidence/precondition status.
11. Finite toy metric-response route frozen under tag-removal/equivariant-totalization obstruction.
12. `finite_variation_robustness` current Refuter-stress-passed/proposal-only status.
13. `Einstein equations` not-started status.
14. `benchmark_promotion` blocked status.
15. Gate Chair benchmark closure human-gated status.

### Required reads

- All cited source artifacts for the above items.
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/current_frontier.md`

### Required outputs

- Populated canonical inventory source file.
- Registry row updates if required.
- Completion receipt with list of source artifacts inspected.
- `distance_to_gr_delta.changed: false` unless the task is explicitly routed as a new scientific dependency-map update.

### Acceptance criteria

- Every inventory item cites a canonical source artifact or registry row.
- Every item includes assumptions, conclusion, non-conclusions, and missing theorem/primitive.
- The matter-coupling item explicitly says it is not matter-coupling derivation or adoption.
- The `g_eff` item explicitly says it is not unscoped Lorentzian metric adoption or benchmark recovery.
- The finite toy negative item explicitly says it is local, not global theory rejection.
- Validation passes.

### Stop conditions

Stop and route a narrower task if:

- Too many items require new mathematical interpretation.
- A source artifact is missing or unregistered.
- The inventory would require changing a claim boundary.

---

## P2-T04 — Inventory validator or lint check

**Recommendation integrated:** `R2`, supports `R7`, `R8`  
**Task type:** validator/tooling  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** validator only

### Objective

Add a validator or lint check ensuring every frontier inventory item includes required fields and blocked physical non-conclusions.

### Required checks

- Inventory source exists and is registered.
- Each item has a source path.
- Each item has assumptions and conclusion.
- Each item has non-conclusions.
- Each item has missing theorem or primitive.
- Items with `matter`, `coupling`, `stress-energy`, `Einstein`, `benchmark`, or `g_eff` terms include explicit overread guards.
- No generated derivative is cited as source authority unless paired with canonical source path.

### Required outputs

- Validator script or extension to existing validator.
- Fixture tests for missing non-conclusions and bad source paths.
- Completion receipt.

### Acceptance criteria

- The live inventory passes.
- Broken fixtures fail.
- Existing validation suite passes.

---

## P2-T05 — Render inventory summary for reader surfaces without authority drift

**Recommendation integrated:** `R2`, supports `R8`  
**Task type:** documentation/generated derivative  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `documentation-curator@2.0.0`  
**Physics milestone:** none  
**Claim boundary:** generated reader summary only

### Objective

Create or update a reader-facing summary of the frontier theorem inventory, making clear that the canonical inventory source governs and generated pages are noncanonical.

### Potential outputs

- GitHub-facing Markdown explainer update.
- HTML explainer spec update.
- Publication brief update.
- Generated HTML derivative.
- Wiki/index update from bootstrap.

### Acceptance criteria

- Reader surface clearly states GR has not been derived.
- Reader surface clearly distinguishes scoped source-extension evidence from physical adoption.
- Publication process validation passes.
- Documentation impact receipt is valid.

---

# P3 — New Tracked Objective Restart

## P3 purpose

P3 implements `R10`: choose the next tracked objective deliberately after v11 closure. The current state says no v11 implementation-plan task remains, so the project must restart ordinary research continuation under a new objective rather than drifting into the next packet by inertia.

## P3-T01 — Post-v11 theoretical continuation selector

**Recommendation integrated:** `R10`, routes `R3` and `R4`  
**Task type:** physics routing  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `theoretical-continuation-selector@0.1.0`  
**Physics milestone:** Director must choose, recommended `matter_coupling` or `effective_metric_g_eff` bridge context  
**Claim boundary:** route selection only, no adoption

### Objective

Select the first post-v11 physics objective among the following lawful routes:

1. Source-extension minimization/compression packet.
2. Matter-semantics preflight packet.
3. Formalization/proof-assistant support packet if the scientific route needs mechanized foundations first.
4. External literature/source-acquisition packet if a critical external theorem or no-go constraint must be checked first.
5. Scoped obstruction or freeze review if the current burden cannot advance without repeating the same shape.

### Recommended default decision

Unless latest tracked state has advanced, select **source-extension minimization/compression** first, because it reduces the risk that matter-semantics work builds on an unnecessarily large source-extension stack.

### Required reads

- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0323.yaml`
- `research_control/current_frontier.md`
- P1 layered ledger
- P2 frontier theorem inventory
- `research_control/design/gr_derivation_burden_map.md`
- `scripts/research_control/report_physics_progress_metrics.py` output
- Key `g_eff` and matter-coupling precondition Gate Chair artifacts

### Required completion fields

- `physics_progress_status.status: route_selected`
- `target_derivation_milestone`
- `milestone_burden`
- `mathematical_payload_manifest` containing at least one route-decision payload
- `theoretical_decision_output`
- `distance_to_gr_delta.changed: false`, unless a new dependency-map update is accepted as a science delta
- `forbidden_conclusion_summary`
- `route_cycle_control`
- `freeze_criteria_status` if the selected route repeats a burden

### Required outputs

- Selector YAML or Markdown artifact with selected route and alternatives rejected.
- Handoff to P4-T01, P5-T01, P6-T01, P10-T01, or freeze review depending on decision.

### Acceptance criteria

- The selector explicitly says why the next objective is not generic continuation.
- The selector names the exact derivation milestone and burden.
- The selector does not treat scoped `g_eff` or matter-coupling preconditions as downstream GR evidence.
- The handoff names exactly one next bounded task.

---

## P3-T02 — New objective control-state declaration

**Recommendation integrated:** `R10`  
**Task type:** research-control state update  
**Continue Research requirement:** one bounded `/continue-research` transaction if not already done by P3-T01  
**Suggested role:** `process-integrity-auditor@0.1.0` or Director-selected role  
**Physics milestone:** follows P3-T01  
**Claim boundary:** objective declaration only

### Objective

Ensure the new post-v11 objective is visible in `program_state.yaml`, current-frontier rendering, latest handoff, and task registries.

### Required outputs

- Updated `program_state.yaml` if the active task changes.
- New handoff naming the selected objective.
- Updated `current_frontier.md` generated from tracked state.
- Completion receipt stating no scientific claim was promoted by objective declaration alone.

### Acceptance criteria

- Continue Research reports a coherent next action.
- Current-frontier snapshot matches tracked authority.
- The selected next route is not a v11 implementation-plan residual.

---

# P4 — Source-Extension Minimization and Compression

## P4 purpose

P4 implements `R3`: determine whether the currently accepted scoped source-extension machinery can be compressed into a smaller source-side law package, or whether some source-extension data are irreducible new primitives, conservative definitions, or forbidden target imports.

## P4-T01 — Source-extension dependency extraction

**Recommendation integrated:** `R3`  
**Task type:** physics formalization / dependency analysis  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `ontology-formalizer@0.2.0`  
**Physics milestone:** recommended `source_equivalence_eqsrc` or `matter_coupling`, Director must choose exact burden  
**Claim boundary:** dependency extraction only

### Objective

Extract a formal dependency graph of all source-extension data used by current `Resp_lc`, `M_src`, `g_eff`, and matter-coupling precondition evidence.

### Required dependency categories

For each dependency, classify as one of:

- `derived_from_current_source_ontology`
- `conditional_theorem_input`
- `conservative_source_extension`
- `new_source_law_candidate`
- `new_ontology_primitive_candidate`
- `support_only_tooling_artifact`
- `forbidden_target_import_if_used_physically`
- `unknown_or_unclassified`

### Required reads

- P2 frontier theorem inventory
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `research_control/tasks/RT-20260614-060/...Resp_lc...tex`
- `research_control/tasks/RT-20260614-134/...M_SRC...tex`
- `research_control/tasks/RT-20260614-222/...GEFF...tex`
- `research_control/tasks/RT-20260614-269/...PARAMETERIZED...tex`
- Relevant precursor artifacts cited by those gate reviews
- `research_control/design/gr_derivation_burden_map.md`

### Required outputs

- TeX or Markdown artifact: `source_extension_dependency_extraction_v1`.
- Machine-readable dependency table if feasible: YAML/CSV/JSON.
- Completion receipt with mathematical payload manifest.

### Acceptance criteria

- Every currently used extension datum is listed.
- Each datum has at least one source artifact path.
- The artifact identifies which data are essential for `g_eff` and which are essential for matter-coupling precondition evidence.
- The artifact does not claim compression, adoption, or rejection yet.

---

## P4-T02 — Minimal source-law candidate or irreducible-extension target formalization

**Recommendation integrated:** `R3`  
**Task type:** physics formalization  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `ontology-formalizer@0.2.0`  
**Physics milestone:** same as P4-T01 unless Director selects a narrower burden  
**Claim boundary:** target formalization only

### Objective

Formalize the minimization target: what it would mean to reduce the current extension stack to a smaller source-side law package.

### Required target definitions

Define at least:

- `SourceExtensionStack_v1`
- `ExtensionDatum(E)`
- `DerivableDatum(E)`
- `ConservativeExtension(E)`
- `IrreduciblePrimitiveCandidate(E)`
- `TargetImportRisk(E)`
- `CompressionMap_v1`
- `MinimalSourceLawPackage_v1`
- `NoTargetImportPreservingCompression_v1`
- `CompressionFailureObstruction_v1`

### Required outputs

- Science artifact formalizing the minimization target.
- Explicit allowed/non-allowed conclusions.
- Handoff to Candidate Constructor for construction or obstruction.

### Acceptance criteria

- Target is source-side and does not require target metric, Lorentzian signature, stress-energy, matter action, detector semantics, or Einstein equations.
- Target includes failure conditions.
- Target distinguishes “cannot compress under current ontology” from “global source extension impossible.”

---

## P4-T03 — Candidate Constructor: compression candidate or precise obstruction

**Recommendation integrated:** `R3`  
**Task type:** physics construction  
**Continue Research requirement:** one bounded `/continue-research` transaction with `parent_child_parallel_synthesis`  
**Suggested role:** `candidate-constructor@0.2.0`  
**Physics milestone:** selected in P4-T02  
**Claim boundary:** candidate or obstruction only, no adoption

### Objective

Attempt to construct a `MinimalSourceLawPackage_v1` or produce a precise obstruction showing which extension datum cannot be derived, compressed, or removed under current source ontology.

### Required result types

The Candidate Constructor must end with exactly one:

- `constructed_candidate`
- `precise_obstruction`
- `minimal_countermodel`
- `human_gate_required`
- `route_frozen_recommended`

### Required outputs

- TeX artifact with definitions, construction or obstruction proof sketch, and dependency table.
- `candidate_constructor_result` in completion receipt.
- `obstruction_record` if obstruction is present.
- `distance_to_gr_delta` stating whether the dependency map changed.

### Acceptance criteria for constructed candidate

- Candidate explicitly maps each extension datum to one of: derived, retained as conservative extension, eliminated, or irreducible primitive candidate.
- Candidate preserves no-target-import boundaries.
- Candidate does not treat eliminated notation as eliminated mathematics unless proof is supplied.
- Candidate does not adopt new source laws.

### Acceptance criteria for obstruction

- Obstruction names the exact missing primitive or theorem.
- Obstruction gives a scoped counterexample, dependency failure, or underdetermination argument.
- Obstruction explicitly states whether same-milestone continuation remains open.

---

## P4-T04 — Smuggling audit of compression candidate or obstruction

**Recommendation integrated:** `R3`  
**Task type:** physics adversarial audit  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `smuggling-auditor@0.2.0`  
**Physics milestone:** same as P4-T03  
**Claim boundary:** audit only

### Objective

Audit the compression candidate or obstruction for hidden target imports, ontology-edit laundering, source-law adoption laundering, process-authority laundering, and notation-collapse errors.

### Required audit checks

- No target topology import.
- No target atlas import.
- No target transition map import.
- No target metric import.
- No Lorentzian signature import.
- No proper-time normalization import.
- No detector semantics import.
- No stress-energy tensor import.
- No matter action import.
- No Einstein-equation premise import.
- No benchmark-fit-as-proof import.
- No generated derivative, validator, registry, role, handoff, or approval as mathematical premise.
- No conversion of conservative source-extension data into adopted ontology.
- No silent promotion of `g_eff` scope.
- No silent matter-coupling derivation.

### Required outputs

- Smuggling audit TeX artifact.
- Completion receipt with audit verdict.

### Acceptance criteria

- Audit verdict is one of `source_pure_as_written_pending_stress`, `target_import_detected`, `process_authority_laundering_detected`, `requires_repair_before_stress`, or `freeze_recommended`.
- If defects are found, handoff routes repair or freeze, not stress.

---

## P4-T05 — Refuter stress test of compression candidate or obstruction

**Recommendation integrated:** `R3`, supports `R7`  
**Task type:** physics adversarial stress  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `refuter@0.2.0`  
**Physics milestone:** same as P4-T03  
**Claim boundary:** stress test only

### Objective

Stress-test the audited compression candidate or obstruction under finite variation, tag removal, dependency deletion, symmetry/relabeling, bottom/fail-closed behavior, and known no-target-import constraints.

### Required stress modes

- Remove one extension datum at a time and test whether claimed output survives.
- Relabel source-side tokens and test equivariance/invariance claims.
- Collapse or forget tags and test whether response/metric/coupling-like outputs remain determined.
- Replace generated or registry references with canonical source references only.
- Test whether the package still works when support-only checker outputs are ignored.
- Test whether claimed compression hides a new source law.
- Test whether irreducible primitive claims are narrower than global impossibility.

### Required outputs

- Refuter stress TeX artifact.
- Freeze criteria evaluation.
- Obstruction record if a new obstruction is found.
- Handoff to P4-T06 selector.

### Acceptance criteria

- Stress result is one of `stress_survived_pending_selector`, `scoped_obstruction`, `minimal_countermodel`, `repair_required`, `route_frozen_recommended`, or `human_gate_required`.
- The artifact clearly distinguishes local obstruction from global theory rejection.

---

## P4-T06 — Post-compression selector and ledger update route

**Recommendation integrated:** `R3`, `R10`  
**Task type:** physics route selection  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `theoretical-continuation-selector@0.1.0`  
**Physics milestone:** same as P4 cycle  
**Claim boundary:** route selection only

### Objective

Select the next lawful route after compression construction/audit/stress.

### Allowed next routes

- Narrow Gate Chair evidence-status review, if exact human authorization exists or is requested.
- Matter-semantics preflight P5, if compression produces stable enough source-side package.
- Repair packet, if a fix is local and non-promotional.
- Scoped obstruction or freeze review, if compression fails in a repeated way.
- Formalization/proof-assistant support P6, if the next bottleneck is mechanized precision.
- Literature comparison P10, if an external theorem or no-go result is now decisive.

### Acceptance criteria

- Selector names exactly one next task.
- No automatic adoption or promotion occurs.
- If ledger update is needed, it is a separate bounded process-control task unless the current AgentJob explicitly allowed it.

---

# P5 — Matter-Semantics Preflight Before Einstein-Equation Work

## P5 purpose

P5 implements `R4`: prevent premature Einstein-equation work by formalizing source-side matter semantics, detector semantics, stress-energy-like bookkeeping, matter-action alternatives, conservation-like constraints, and universal-coupling preconditions before field-equation derivation is attempted.

## P5-T01 — Matter-semantics burden selector

**Recommendation integrated:** `R4`  
**Task type:** physics route selection  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `theoretical-continuation-selector@0.1.0`  
**Physics milestone:** `matter_coupling`  
**Milestone burden:** source-side matter-sector semantics before coupling-law or Einstein-equation work  
**Claim boundary:** selector only

### Objective

Select the exact first matter-semantics preflight packet. The selector must decide whether to begin with:

1. Source-side matter-sector syntax.
2. Detector/readout semantics without target detector import.
3. Stress-energy-like bookkeeping target without stress-energy tensor import.
4. Matter-action alternative target without importing an action.
5. Conservation/continuity analogue target.
6. Universal coupling precondition target.
7. Precise obstruction showing current source ontology lacks a matter-sector discriminator.

### Recommended default decision

If P4 produced a stable compression candidate, start with **source-side matter-sector syntax plus detector/readout non-import boundary**. If P4 found an irreducible missing primitive, start with a precise matter-sector primitive obstruction or ontology-law packet.

### Required outputs

- Selector artifact with selected matter-semantics packet.
- `theoretical_decision_output` completion fields.
- Handoff to P5-T02.

### Acceptance criteria

- Selector explicitly blocks Einstein-equation work.
- Selector explicitly blocks stress-energy tensor, matter action, detector semantics, and coupling-law adoption.
- Selector names one next bounded task.

---

## P5-T02 — Matter-semantics target formalization

**Recommendation integrated:** `R4`  
**Task type:** physics formalization  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `ontology-formalizer@0.2.0`  
**Physics milestone:** `matter_coupling`  
**Milestone burden:** selected by P5-T01  
**Claim boundary:** draft/control target only

### Objective

Formalize a target for source-side matter semantics that can later support or obstruct universal matter coupling without importing target stress-energy, matter actions, empirical detector protocols, or Einstein-equation premises.

### Required definitions

Depending on P5-T01 selection, define a subset of:

- `SourceMatterSector_v1(E)`
- `SourceProbeToken_v1(E)`
- `SourceDetectorReadout_v1(E)`
- `MatterResponseToken_v1(E)`
- `SourceStressBookkeeping_v1(E)`
- `SourceActionAnalogue_v1(E)`
- `SourceConservationConstraint_v1(E)`
- `UniversalCouplingPrecondition_v1(E)`
- `NoStressEnergyImport_v1(E)`
- `NoMatterActionImport_v1(E)`
- `NoDetectorImport_v1(E)`
- `MatterSemanticsFailureObstruction_v1(E)`

### Required outputs

- TeX artifact formalizing the target.
- Explicit non-conclusions.
- Handoff to Candidate Constructor.

### Acceptance criteria

- Formalization is source-side.
- Target includes no-target-import obligations.
- Target includes failure conditions.
- Target does not define stress-energy tensor, matter action, detector semantics, or coupling law as adopted physical objects.

---

## P5-T03 — Candidate Constructor: matter-semantics candidate or obstruction

**Recommendation integrated:** `R4`  
**Task type:** physics construction  
**Continue Research requirement:** one bounded `/continue-research` transaction with `parent_child_parallel_synthesis`  
**Suggested role:** `candidate-constructor@0.2.0`  
**Physics milestone:** `matter_coupling`  
**Claim boundary:** candidate or obstruction only

### Objective

Attempt to construct a source-side matter-semantics candidate satisfying P5-T02, or produce a precise obstruction.

### Required result types

- `constructed_candidate`
- `precise_obstruction`
- `minimal_countermodel`
- `human_gate_required`
- `route_frozen_recommended`

### Required outputs

- TeX construction or obstruction artifact.
- `candidate_constructor_result` completion field.
- `obstruction_record` if applicable.
- `mathematical_payload_manifest` with new definitions/theorem/countermodel.

### Candidate acceptance criteria

A candidate must:

- Use only source-side objects and accepted scoped preconditions.
- State whether it depends on the compressed source-extension package from P4.
- Provide no-target-import certificates.
- Define what is reproducible by finite/local support tooling, if anything.
- Avoid identifying source bookkeeping with physical stress-energy.
- Avoid identifying source readout with empirical detector semantics.
- Avoid deriving coupling law or Einstein equations.

### Obstruction acceptance criteria

An obstruction must:

- Name the smallest missing primitive or theorem.
- State whether same-milestone continuation remains open.
- Avoid global impossibility unless proven.

---

## P5-T04 — Smuggling audit of matter-semantics candidate

**Recommendation integrated:** `R4`  
**Task type:** physics adversarial audit  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `smuggling-auditor@0.2.0`  
**Physics milestone:** `matter_coupling`  
**Claim boundary:** audit only

### Objective

Audit the matter-semantics candidate or obstruction for hidden imports of target matter semantics, empirical detector protocols, stress-energy tensors, matter actions, conservation laws, variational principles, or Einstein-equation premises.

### Required audit checks

- No target stress-energy tensor import.
- No matter action import.
- No physical detector protocol import.
- No empirical calibration import.
- No target metric dependence.
- No proper-time normalization import.
- No conservation law imported from GR/QFT by name only.
- No coupling law adoption laundering.
- No benchmark behavior import.
- No use of support-only checker result as proof authority.

### Required outputs

- Smuggling audit artifact.
- Completion receipt with verdict and exact next route.

---

## P5-T05 — Refuter stress test of matter-semantics candidate

**Recommendation integrated:** `R4`  
**Task type:** physics adversarial stress  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `refuter@0.2.0`  
**Physics milestone:** `matter_coupling`  
**Claim boundary:** stress only

### Objective

Stress-test the audited matter-semantics candidate under source relabeling, finite variation, tag removal, sector deletion, degeneracy, fail-closed behavior, and known underdetermination modes.

### Required stress questions

- Does the candidate still determine matter-like distinctions after tag removal?
- Does source relabeling preserve the claimed semantics?
- Does finite variation break universal coupling preconditions?
- Does the candidate secretly require target `g_eff` scope expansion?
- Does it collapse into explicit labels with no source-side law?
- Does it require a new ontology primitive?
- Can it be reproduced as support-only finite/local data without becoming proof authority?

### Required outputs

- Refuter stress artifact.
- Freeze criteria status.
- Handoff to P5-T06 selector.

---

## P5-T06 — Post-matter-semantics selector

**Recommendation integrated:** `R4`, `R10`  
**Task type:** physics route selection  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `theoretical-continuation-selector@0.1.0`  
**Physics milestone:** `matter_coupling`  
**Claim boundary:** selector only

### Objective

Select the next lawful route after matter-semantics construction/audit/stress.

### Allowed next routes

- Narrow Gate Chair evidence-status review if exact tracked human authorization exists.
- Repair packet.
- Source-extension minimization revisit.
- Formalization/proof-assistant support.
- Scoped obstruction or freeze.
- Next matter-coupling precondition packet.
- Only if source-side matter semantics are sufficiently stable: a future coupling-law target formalization. This still must not derive Einstein equations.

### Acceptance criteria

- Einstein-equation route remains blocked unless source-side matter semantics and coupling-law prerequisites are explicitly established by protected authority.
- Selector names exactly one next task.
- If Gate Chair is needed, the selector requests human gate rather than issuing verdict.

---

# P6 — Support-Only Formalization and Proof-Assistant Bridge

## P6 purpose

P6 implements `R5`: introduce support-only mechanized formalization, starting with small, well-scoped results. The first targets should be finite and negative/structural, not the full GR derivation.

## P6-T01 — Formalization tooling route decision

**Recommendation integrated:** `R5`  
**Task type:** project-system / formalization route design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0` or `project-control-maintainer@0.2.0`  
**Physics milestone:** none unless new theorem statements are created  
**Claim boundary:** support-only tooling

### Objective

Choose the formalization approach for support-only theorem skeletons.

### Candidate approaches

- Lean project under a support-only folder.
- Coq project under a support-only folder.
- Isabelle/HOL theory files.
- Python typed algebraic specification plus property tests.
- Lightweight custom finite-structure checker with proof comments.

### Decision criteria

- Minimal dependency friction.
- Ability to formalize finite toy obstruction quickly.
- Ability to represent finite source graphs and relabeling symmetries.
- Clear separation from proof authority.
- Easy validation in local environment.
- No claim that mechanization proves physics unless a later protected theorem route grants that status.

### Required outputs

- Design artifact: `research_control/design/support_only_formalization_lane_v1.md`.
- Chosen folder path and validation commands.
- Handoff to P6-T02.

### Acceptance criteria

- Tooling lane is support-only.
- Generated or machine-checked result cannot be used as physics proof without separate Gate Chair or theorem authority.
- If dependencies are unavailable locally, the design includes a minimal fallback.

---

## P6-T02 — Formalize finite toy tag-removal obstruction

**Recommendation integrated:** `R5`  
**Task type:** support-only formalization plus science traceability  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0` for tooling; `ontology-formalizer@0.2.0` if theorem statement changes are needed  
**Physics milestone:** none for tooling; `finite_toy_metric_response` if science-bearing  
**Claim boundary:** support-only formalization of existing frozen negative

### Objective

Formalize the finite toy tag-removal obstruction already recorded by the Refuter route: tag erasure maps tagged toy objects to the untagged object, and the response relation is undefined without explicit tags.

### Required formal objects

- finite toy source object type
- tag record type for orientation, normalization, token semantics
- untagged object
- tag-erasure map
- partial response relation
- proposition: tag erasure makes response undefined
- optional proposition: no equivariant no-new-source-data totalization under sign/token relabeling

### Required outputs

- Support-only formalization files.
- Test or proof command.
- Traceability note mapping formal objects to the canonical TeX artifact.
- Completion receipt stating mechanization is support-only and does not change frozen route status.

### Acceptance criteria

- Formalization command passes.
- Formalization source includes no target metric or GR import.
- Traceability note cites canonical finite toy Refuter artifact.
- Validator recognizes the output as support-only.

---

## P6-T03 — Formalize finite/local source-side witness schema skeleton

**Recommendation integrated:** `R5`  
**Task type:** support-only formalization  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0` or `memory-system-maintainer@0.2.0` depending on tooling  
**Physics milestone:** none unless new mathematical definitions are introduced  
**Claim boundary:** support-only skeleton

### Objective

Formalize the common finite/local witness schema used by parameterized witness and support-only checker tasks, without treating checker results as proof authority.

### Required formal objects

- finite source index graph
- sector assignment
- source token assignment
- relabeling map
- restriction map
- bridge-slot compatibility predicate
- no-target-import certificate predicate
- fail-closed bottom label
- support-only pass/fail report type

### Required outputs

- Support-only formalization files.
- Tests/proofs for basic invariants.
- Traceability note to current checker and parameterized witness artifacts.

### Acceptance criteria

- Does not claim matter coupling.
- Does not claim stress-energy semantics.
- Does not expand `g_eff` scope.
- Formalization validates locally.

---

## P6-T04 — Proof-to-source traceability registry

**Recommendation integrated:** `R5`  
**Task type:** registry/tooling  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `memory-system-maintainer@0.2.0` or `validator-engineer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** traceability only

### Objective

Create a traceability mechanism linking support-only formalization files to canonical TeX/Markdown sources and declaring their authority boundary.

### Required outputs

- Registry or manifest, for example `registries/SUPPORT_FORMALIZATION_REGISTRY.csv` or a controlled YAML manifest under `research_control/design/`.
- Validator check ensuring every formalization file has a source artifact and boundary statement.
- Completion receipt.

### Acceptance criteria

- Formalization artifacts are discoverable.
- Each artifact maps to canonical source paths.
- Each artifact declares `proof_authority: false` unless future protected authority changes it.

---

# P7 — External Red-Team Review Mode

## P7 purpose

P7 implements `R6`: add a review mode that is adversarial in a different way from current internal Refuter/Smuggling Auditor roles. The red-team reviewer should ignore workflow success and evaluate the mathematical object as an external skeptic would.

## P7-T01 — Red-team role contract design

**Recommendation integrated:** `R6`  
**Task type:** project-control role design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `project-control-maintainer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** role contract only

### Objective

Design a new role or task overlay, tentatively `external-red-team-reviewer@0.1.0`, with authority to critique but not promote claims.

### Required role mandate

The role must:

- Ignore task success and validator success as evidence.
- Inspect definitions, assumptions, theorem statements, and proof skeletons.
- Identify circularity.
- Identify hidden target imports.
- Identify overloaded notation.
- Identify unproven equivalences.
- Identify mismatch between mathematical conclusion and physical interpretation.
- Produce a minimal countermodel or “not enough assumptions” theorem when possible.
- Produce a review artifact that can route repair, obstruction, freeze, or external review.
- Never promote physics claims.

### Required outputs

- Role contract draft under `.agents/roles/` if allowed.
- Registry row update if a role is added.
- Schema or template for red-team review artifacts.
- Completion receipt stating no claim-promotion authority.

### Acceptance criteria

- Role has `may_promote_claims: false`.
- Role does not duplicate Gate Chair authority.
- Role does not replace Smuggling Auditor or Refuter; it complements them.
- Validation passes.

---

## P7-T02 — Red-team artifact schema and validator

**Recommendation integrated:** `R6`  
**Task type:** schema/validator  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** validator only

### Objective

Create a schema for red-team review outputs and validate required fields.

### Required fields

- `reviewed_object_id`
- `reviewed_source_paths`
- `claim_under_review`
- `assumptions_read`
- `definitions_read`
- `proof_steps_checked`
- `circularity_findings`
- `hidden_import_findings`
- `notation_overload_findings`
- `unproven_equivalence_findings`
- `minimal_countermodel_attempt`
- `external_mathematical_pressure_points`
- `verdict`
- `recommended_next_route`
- `physics_promotion_authorized: false`

### Required verdict vocabulary

- `no_blocking_defect_found_as_written`
- `repair_required`
- `hidden_target_import_detected`
- `circularity_detected`
- `unproven_equivalence_blocks_claim`
- `not_enough_assumptions`
- `minimal_countermodel_found`
- `freeze_recommended`
- `external_expert_review_required`

### Acceptance criteria

- Validator fails missing field fixtures.
- Validator fails `physics_promotion_authorized: true` for red-team outputs.
- Validator passes a minimal pilot fixture.

---

## P7-T03 — Pilot red-team review of frontier theorem inventory

**Recommendation integrated:** `R6`, supports `R2`, `R3`, `R4`  
**Task type:** adversarial science review  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `external-red-team-reviewer@0.1.0` if created; otherwise a bounded task overlay under existing Refuter with red-team schema  
**Physics milestone:** selected by Director; recommended `effective_metric_g_eff` or `matter_coupling`  
**Claim boundary:** review only

### Objective

Run the first red-team review on the P2 frontier theorem inventory, focusing on the transition from scoped `g_eff` and parameterized matter-coupling precondition evidence to any future matter-semantics or coupling-law route.

### Required review questions

- Are all assumptions explicit?
- Is any source-side name doing target-GR work implicitly?
- Does scoped `g_eff` rely on metric-form assignment that is effectively target metric input?
- Does parameterized matter-coupling evidence rely on matter semantics in disguise?
- Are `accepted` statuses overread anywhere?
- Does any dependency require a canonical ontology edit that has not happened?
- Can a minimal countermodel break the intended next route?

### Required outputs

- Red-team review artifact.
- Completion receipt with no-promotion statement.
- Handoff to repair, freeze, P4, P5, or external review as appropriate.

### Acceptance criteria

- Review cites canonical sources.
- Review distinguishes mathematical defect from documentation ambiguity.
- Review names exact repair or obstruction if found.

---

# P8 — Route-Orbit Guard Hardening

## P8 purpose

P8 implements `R7`: after v11 closure, make repeated same-burden or same-shape cycles harder to continue without new mathematical payload, construction, obstruction, gate decision, formalization target, or freeze rationale.

## P8-T01 — Route-orbit guard policy design

**Recommendation integrated:** `R7`  
**Task type:** project-control design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `project-control-maintainer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** workflow guard only

### Objective

Design a post-v11 route-orbit guard policy for future physics continuations.

### Required guard rule

A future same-burden or same-shape physics packet may proceed only if it produces or routes toward at least one:

- new theorem with explicit assumptions and conclusion
- new definition with a decision consequence
- constructed candidate
- precise obstruction
- minimal countermodel
- formal mechanization target
- source-extension minimization result
- scoped no-go theorem
- Gate Chair request with exact protected question
- explicit freeze recommendation

### Required outputs

- Policy artifact: `research_control/design/post_v11_route_orbit_guard_policy.md`.
- Proposed changes to metrics/reporting/Continue Research context.
- Completion receipt.

### Acceptance criteria

- Policy is advisory or hard-gated only where validator support is clear.
- Policy does not block lawful Gate Chair requests.
- Policy does not treat metrics as physics evidence.
- Policy includes escape hatches for genuinely new payload.

---

## P8-T02 — Implement route-orbit guard in metrics and Continue Research context

**Recommendation integrated:** `R7`  
**Task type:** validator/tooling  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** tooling only

### Objective

Update `report_physics_progress_metrics.py` and/or `continue_research.py` to surface stronger post-v11 route-orbit warnings or guards.

### Required behavior

- Detect same-burden repetition after v11 closure.
- Detect constructor/audit/stress/selector cycles with insufficient new payload.
- Detect gate-ready wording without Gate Chair routing or explanation.
- Detect bridge language with no Distance-to-GR delta and no new payload.
- Recommend Candidate Constructor, Refuter obstruction, Gate Chair, formalization target, minimization, or freeze review.
- Keep warnings out of scientific progress metrics unless they count tracked science fields.

### Required outputs

- Updated script(s).
- Tests for warning/guard behavior.
- Completion receipt.

### Acceptance criteria

- Existing metrics separation guard passes.
- New warning fixtures emit expected warnings.
- Warnings have `physics_claim_authority: false`.
- If any hard guard is introduced, its bypass conditions are explicit and tested.

---

## P8-T03 — Completion-template hardening for new mathematical payload

**Recommendation integrated:** `R7`  
**Task type:** schema/template validation  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** template only

### Objective

Ensure future physics completions cannot omit concrete mathematical payload details when the mathematical-decisiveness contract applies.

### Required checks

- `mathematical_payload_manifest` must include item type, source path, summary, and decision consequence.
- Candidate Constructor completions must include `candidate_constructor_result`.
- Selector completions must include `theoretical_decision_output`.
- Repeated-burden completions must include `freeze_criteria_status`.
- Obstructions must include an `obstruction_id`.

### Acceptance criteria

- Historical compatibility preserved where required.
- Future-governed completions fail if required fields are missing.
- Tests pass.

---

# P9 — Public-Facing Current-Status Clarity

## P9 purpose

P9 implements `R8`: make README, website, GitHub-facing explainers, and generated public pages impossible to overread as claiming that GR has already been derived.

## P9-T01 — Public status block source spec

**Recommendation integrated:** `R8`  
**Task type:** documentation source design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `documentation-curator@2.0.0`  
**Physics milestone:** none  
**Claim boundary:** public explanation only

### Objective

Draft a canonical public-facing current-status block that can be reused across README, website, and explainers.

### Required status block content

The block must state plainly:

- GR has not been derived.
- The exact-GR benchmark remains the target boundary.
- Scoped `M_src` exists under internal source-only gate boundaries.
- Scoped source-extension `g_eff` exists under declared source-side scope.
- Matter-coupling status is evidence/precondition only, not matter-coupling derivation or adoption.
- Stress-energy semantics, stress-energy tensor, matter action, detector semantics, Einstein equations, benchmark promotion, and completed derivation remain blocked.
- Workflow validators and generated artifacts are not scientific proof.

### Required outputs

- Source spec or canonical Markdown snippet, for example `markdown/public-status/current-physics-status-v1.md` or a controlled equivalent.
- Registry row if required.
- Completion receipt.

### Acceptance criteria

- Text is clear to non-specialist readers.
- Text is faithful to the layered ledger and frontier inventory.
- Text contains no new physics claims.

---

## P9-T02 — README front-door update

**Recommendation integrated:** `R8`  
**Task type:** public documentation  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `documentation-curator@2.0.0`  
**Physics milestone:** none  
**Claim boundary:** explanatory only

### Objective

Update `README.md` to include the public current-status block near the top, before readers encounter ontology or benchmark discussion that could be overread.

### Required reads

- P9-T01 public status block
- `README.md`
- P2 frontier theorem inventory
- P1 layered ledger/current frontier
- `registries/PUBLICATION_BRIEF_REGISTRY.csv` if publication surfaces are affected

### Required outputs

- Updated `README.md`.
- Documentation impact receipt.
- Generated memory/wiki derivatives if required by bootstrap.

### Acceptance criteria

- README explicitly says GR has not been derived.
- README does not imply that scoped evidence equals physical adoption.
- README links or points to reader surfaces only as noncanonical explainers.
- Validation passes.

---

## P9-T03 — GitHub-facing and website explainer synchronization

**Recommendation integrated:** `R8`  
**Task type:** public documentation / generated derivative synchronization  
**Continue Research requirement:** one bounded `/continue-research` transaction; split if HTML generation is large  
**Suggested role:** `documentation-curator@2.0.0`  
**Physics milestone:** none  
**Claim boundary:** explanatory only

### Objective

Synchronize GitHub-facing Markdown explainers, HTML explainer specs, publication briefs, and generated HTML so public surfaces preserve current-status clarity.

### Candidate files to inspect

- `github-facing/project-overview-explainer.md`
- `github-facing/aether-flow-physics-program-explainer.md`
- `github-facing/exact-gr-benchmark-boundary-explainer.md`
- `github-facing/gr-derivation-roadmap-explainer.md`
- `github-facing/claim-gates-explainer.md`
- `markdown/html-explainer-specs/*.md`
- `markdown/publication-briefs/*.md`
- `registries/PUBLICATION_BRIEF_REGISTRY.csv`
- `html/*.html`

### Required outputs

- Updated source specs/briefs as required.
- Regenerated HTML only through approved generation workflow.
- Registry updates if required.
- Completion receipt distinguishing source edits from generated derivatives.

### Acceptance criteria

- Public pages consistently state current blocked claims.
- Generated HTML validates.
- No direct HTML-only edits unless explicitly allowed by project policy.
- Publication-process validation passes.

---

# P10 — Literature-Comparison Packet

## P10 purpose

P10 implements `R9`: compare the AEther-Flow program against neighboring research programs and known reconstruction/no-go constraints. This is not claim promotion. It is an external pressure map to identify constraints the project must eventually face.

## P10-T01 — Literature-comparison route selector and source-acquisition design

**Recommendation integrated:** `R9`  
**Task type:** research route selection / external primary-source acquisition design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `theoretical-continuation-selector@0.1.0` or bounded literature-review overlay if available  
**Physics milestone:** Director chooses; likely `source_equivalence_eqsrc`, `effective_metric_g_eff`, or `matter_coupling`  
**Claim boundary:** comparison design only

### Objective

Design a bounded literature-comparison packet that identifies primary sources and neighboring programs relevant to emergent metric structure, Lorentzian recovery, matter coupling, and Einstein-equation derivation.

### Required comparison domains

At minimum consider whether to include:

- emergent gravity programs
- analogue gravity
- Einstein-aether-like models and Lorentz-violating constraints
- causal set or order-theoretic reconstruction ideas
- relational or shape-dynamics-adjacent approaches
- thermodynamic/entropic gravity claims and criticisms
- spin-network/group-field/quantum-geometry metric emergence, if relevant
- effective field theory constraints on emergent Lorentzian dynamics
- reconstruction theorems for spacetime geometry from causal/order/conformal/projective structures
- no-go theorems or consistency constraints for universal coupling and massless spin-2 dynamics

### Required outputs

- Source-acquisition design artifact.
- List of primary-source search targets.
- Criteria for source inclusion/exclusion.
- Handoff to P10-T02.

### Acceptance criteria

- Packet is bounded.
- It prioritizes primary sources and review papers where appropriate.
- It states that external literature comparison does not prove AEther-Flow claims.

---

## P10-T02 — External primary-source comparison memo

**Recommendation integrated:** `R9`  
**Task type:** literature comparison / source-backed research memo  
**Continue Research requirement:** one bounded `/continue-research` transaction; may require external-source search if authorized by tracked state or user instruction  
**Suggested role:** Director-selected research/literature overlay; if no role exists, project-system task may design role first  
**Physics milestone:** selected by P10-T01  
**Claim boundary:** comparison only

### Objective

Produce a source-backed comparison memo mapping AEther-Flow’s current burdens against neighboring research programs and external constraints.

### Required memo sections

- Scope and non-promotion boundary.
- Source list with bibliographic metadata.
- One-paragraph summary of each neighboring program.
- Relevance to AEther-Flow source-side metric emergence.
- Relevance to source-side matter semantics and universal coupling.
- Relevance to Einstein-equation derivation.
- Relevance to Lorentzian signature and causal structure.
- Known no-go or consistency constraints.
- What AEther-Flow must prove to be competitive or coherent.
- What AEther-Flow must not import by analogy.
- Candidate next tasks generated by the comparison.

### Required outputs

- Markdown or TeX comparison artifact.
- Registry rows if required.
- Completion receipt distinguishing established literature from project construction.

### Acceptance criteria

- Memo cites external sources accurately.
- Memo does not use analogy as proof.
- Memo identifies at least three concrete external pressure points for the project.
- Memo routes any follow-up through bounded tasks.

---

## P10-T03 — Smuggling and overclaim audit of literature comparison

**Recommendation integrated:** `R9`, supports `R6`, `R8`  
**Task type:** audit  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `smuggling-auditor@0.2.0` or red-team role if P7 completed  
**Physics milestone:** same as P10-T02 if science-bearing  
**Claim boundary:** audit only

### Objective

Audit the comparison memo to ensure it does not import external theory authority, GR reconstruction assumptions, or physical conclusions into AEther-Flow as if they were derived.

### Required audit checks

- No “neighboring program proves our claim” move.
- No importing Lorentzian metric through reconstruction theorem without satisfying theorem hypotheses.
- No importing universal coupling or spin-2 dynamics by analogy.
- No treating external no-go theorem as applying unless hypotheses match.
- No benchmark-promotion language.

### Acceptance criteria

- Audit verdict is recorded.
- Defects route repair.
- Clean memo may be used as orientation only.

---

# P11 — Final Integration Audit, Metrics, and Continuation Handoff

## P11 purpose

P11 integrates all v12 work. It proves which recommendations were implemented, which were deferred, what changed, what did not change, and what the next ordinary research-control step should be.

## P11-T01 — Cross-phase consistency audit

**Recommendation integrated:** all  
**Task type:** process-integrity audit  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `process-integrity-auditor@0.1.0`  
**Physics milestone:** none  
**Claim boundary:** audit only

### Objective

Audit P0 through P10 for consistency, traceability, validators, documentation impact, claim boundaries, and Distance-to-GR status integrity.

### Required audit questions

- Was every v12 phase either completed or explicitly deferred?
- Does every completed task have a DDR, AgentJob, completion, role record, and handoff where required?
- Do all physics tasks include target milestone, burden, mathematical payload, and forbidden-conclusion summary?
- Do all project-system tasks state no physics promotion?
- Does the layered ledger agree with current-frontier rendering?
- Does the frontier theorem inventory cite canonical sources?
- Are public surfaces synchronized with current status?
- Are support-only formalization artifacts clearly non-authoritative?
- Are red-team findings routed or recorded?
- Are route-orbit warnings/guards active and non-promotional?
- Are literature comparisons non-promotional?

### Required outputs

- Artifact: `v12_cross_phase_consistency_audit.md`.
- List of completed, deferred, blocked, and failed tasks.
- Handoff to P11-T02.

### Acceptance criteria

- Audit identifies no unresolved authority contradiction.
- Any unresolved defect routes a bounded repair task before final handoff.

---

## P11-T02 — Metrics, current-frontier, dependency graph, and memory refresh

**Recommendation integrated:** all  
**Task type:** validation/generated derivative refresh  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `validator-engineer@0.2.0` or `memory-system-maintainer@0.2.0`  
**Physics milestone:** none  
**Claim boundary:** generated derivatives and metrics are not proof

### Objective

Run and refresh all final generated support surfaces after v12 implementation.

### Required commands

```zsh
.venv/bin/python scripts/research_control/render_current_frontier.py --write
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_current_frontier.py --json
.venv/bin/python scripts/research_control/render_dependency_graph.py --json output/research_dependency_graph.json --markdown wiki/indexes/research_dependency_graph.md --dot output/research_dependency_graph.dot
.venv/bin/python scripts/research_control/render_dependency_graph.py --check
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
git diff --check
```

### Required outputs

- Updated current-frontier snapshot.
- Updated dependency graph outputs.
- Updated memory/wiki/registry derivatives as required.
- Completion receipt with command results.

### Acceptance criteria

- All checks pass.
- Any generated outputs are identified as generated derivatives or snapshots.
- No metrics output is treated as physics evidence.

---

## P11-T03 — Final v12 continuation handoff

**Recommendation integrated:** all  
**Task type:** final handoff  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `documentation-curator@2.0.0` or `process-integrity-auditor@0.1.0` depending on final work type  
**Physics milestone:** none unless the handoff routes a physics task  
**Claim boundary:** handoff only

### Objective

Create the final v12 handoff that summarizes implementation state and names the next ordinary research-control action.

### Required handoff fields

- `summary`
- `completed_recommendations`
- `deferred_recommendations`
- `blocked_recommendations`
- `latest_layered_ledger_status`
- `frontier_inventory_status`
- `new_tracked_objective_status`
- `source_extension_minimization_status`
- `matter_semantics_preflight_status`
- `support_formalization_status`
- `red_team_status`
- `route_orbit_guard_status`
- `public_status_sync_status`
- `literature_comparison_status`
- `distance_to_gr_changed`
- `blocked_claims`
- `next_recommended_action`

### Required next-action logic

The final handoff must route exactly one of:

1. Continue source-extension minimization if P4 is incomplete or produced a repairable candidate.
2. Continue matter-semantics preflight if P4 established a stable enough source-side package.
3. Run Gate Chair only if exact human approval exists and the protected question is precise.
4. Run red-team repair if P7 found a blocking defect.
5. Run route-orbit freeze review if repeated-burden risk remains high.
6. Run support-only formalization if the next bottleneck is mechanized precision.
7. Run literature-source follow-up if P10 identified a critical external theorem or no-go constraint.
8. Stop at human gate if canonical ontology edit, ontology adoption, benchmark promotion, or protected verdict is required.

### Acceptance criteria

- Handoff is the immediate routing authority.
- Handoff does not claim completed derivation.
- Handoff preserves all blocked claims unless protected authority changed them.
- Final validation passes.

---

## P11-T04 — Optional P0-style evidence closure if any v12 task evidence is incomplete

**Recommendation integrated:** all, only if needed  
**Task type:** process-integrity closure  
**Continue Research requirement:** one bounded `/continue-research` transaction only if P11-T01 finds a gap  
**Suggested role:** `process-integrity-auditor@0.1.0`  
**Physics milestone:** none  
**Claim boundary:** evidence closure only

### Objective

If the cross-phase audit finds that one or more v12 implementation-plan tasks were completed in substance but lack standalone evidence receipts, create a closure packet analogous to the v11 P0 evidence closure.

### Acceptance criteria

- Closure distinguishes later audit evidence from original historical proof.
- Closure does not replay completed tasks.
- Closure does not promote physics claims.
- Closure handoff states whether v12 is complete, partially complete, deferred, or blocked.

---

## 6. Definition of Done for v12

The v12 implementation plan is complete only when all of the following are true or explicitly deferred with a valid reason:

1. The v12 plan is tracked and discoverable.
2. A post-v11 baseline snapshot exists.
3. The Distance-to-GR ledger has layered statuses or an explicitly approved equivalent.
4. Validators prevent high-risk status overread.
5. `current_frontier.md` displays or references layered status boundaries.
6. A canonical frontier theorem inventory exists and is registered.
7. The inventory has validator coverage or lint coverage.
8. A new post-v11 tracked objective has been selected and recorded.
9. Source-extension minimization has either produced a candidate, obstruction, freeze, or explicit deferral.
10. Matter-semantics preflight has either produced a candidate, obstruction, freeze, or explicit deferral.
11. Support-only formalization has at least a selected route and preferably a finite toy obstruction formalization.
12. External red-team mode exists or is explicitly deferred with reason.
13. Route-orbit hardening is active at least as warnings and preferably with validated guard behavior.
14. Public-facing README/website/explainer status cannot be overread as claiming GR derivation.
15. Literature comparison has either produced a source-backed memo or a bounded source-acquisition design.
16. Final metrics, current-frontier, dependency graph, documentation impact, memory bootstrap, and research-control validation pass.
17. Final handoff names exactly one next route.
18. No unapproved physics claim has been promoted.

---

## 7. Global Risk Register

| Risk ID | Risk | Where it can occur | Required mitigation |
|---|---|---|---|
| `VR12-RISK-STATUS-OVERREAD` | `accepted` or similar status is read as physical derivation. | P1, P2, P9 | Layered ledger statuses; public status block; validators. |
| `VR12-RISK-EXTENSION-ACCRETION` | Source-extension stack grows without compression. | P4, P5 | Minimization packet; red-team review; route-orbit guard. |
| `VR12-RISK-PREMATURE-EINSTEIN` | Einstein-equation work begins before matter semantics. | P5, P11 | Matter-semantics preflight gate; handoff restrictions. |
| `VR12-RISK-TOOLING-AS-PROOF` | Formalization/checker output is treated as proof authority. | P6 | Support-only registry; boundary statements; validators. |
| `VR12-RISK-INTERNAL-GRAMMAR-BIAS` | Internal roles miss defects because they share project language. | P7 | External red-team role and pilot. |
| `VR12-RISK-PUBLIC-OVERCLAIM` | README/site imply GR is derived. | P9 | Public current-status block and publication validation. |
| `VR12-RISK-LITERATURE-LAUNDERING` | External frameworks are used as proof by analogy. | P10 | Literature smuggling audit. |
| `VR12-RISK-ROUTE-ORBIT` | Same-shape task cycles continue without new payload. | P8, P11 | Guard warnings/hard gates and freeze criteria. |
| `VR12-RISK-AUTHORITY-DRIFT` | Generated snapshots or wiki notes override canonical sources. | all phases | Source-first memory and current-frontier guard. |
| `VR12-RISK-HUMAN-GATE-BYPASS` | Gate Chair or ontology authority is implied without approval. | P4, P5, P11 | Exact tracked approval requirement and stop conditions. |

---

## 8. Required Forbidden-Conclusion Phrase Bank

Local agents may reuse these phrases in completion receipts, artifacts, and handoffs. They should be adapted to the exact task, not copied blindly.

- This task does not edit canonical ontology TeX.
- This task does not adopt a source law.
- This task does not adopt `MetricData(E)`.
- This task does not expand or unscope `g_eff`.
- This task does not adopt a coupling law.
- This task does not derive or adopt matter coupling.
- This task does not import stress-energy semantics.
- This task does not construct a stress-energy tensor.
- This task does not import a matter action.
- This task does not import detector semantics.
- This task does not derive Einstein equations.
- This task does not promote the exact-GR benchmark.
- This task does not issue benchmark Gate Chair closure.
- This task does not claim completed derivation.
- This task does not prove future source-extension impossibility.
- This task does not reject the global theory.
- This task does not treat validator, registry, handoff, approval, metrics, graph, checker, generated derivative, wiki, PDF, HTML, local cache, file order, or commit status as scientific proof.

---

## 9. Suggested Artifact Naming Conventions

Use actual task IDs assigned by Continue Research. Suggested local artifact stems:

- `v12_p0_baseline_authority_snapshot.yaml`
- `v12_p0_baseline_summary.md`
- `distance_to_gr_status_layers_v1.md`
- `distance_to_gr_layered_status_migration_report.md`
- `frontier_theorem_inventory_schema_v1.md`
- `frontier_theorem_inventory.md` or `.tex`
- `frontier_theorem_inventory_validation_report.md`
- `post_v11_theoretical_continuation_selector.yaml`
- `source_extension_dependency_extraction_v1.tex`
- `source_extension_minimization_target_v1.tex`
- `minimal_source_law_package_candidate_or_obstruction_v1.tex`
- `minimal_source_law_package_smuggling_audit_v1.tex`
- `minimal_source_law_package_refuter_stress_v1.tex`
- `matter_semantics_burden_selector_v1.yaml`
- `source_matter_semantics_target_v1.tex`
- `source_matter_semantics_candidate_or_obstruction_v1.tex`
- `source_matter_semantics_smuggling_audit_v1.tex`
- `source_matter_semantics_refuter_stress_v1.tex`
- `support_only_formalization_lane_v1.md`
- `finite_toy_tag_removal_formalization_traceability.md`
- `support_formalization_registry_design.md`
- `external_red_team_reviewer_role_design.md`
- `external_red_team_review_schema_v1.md`
- `frontier_inventory_external_red_team_pilot_v1.md`
- `post_v11_route_orbit_guard_policy.md`
- `public_current_physics_status_block_v1.md`
- `neighboring_programs_literature_comparison_design.md`
- `neighboring_programs_literature_comparison_memo_v1.md`
- `v12_cross_phase_consistency_audit.md`
- `v12_final_continuation_handoff.md`

---

## 10. Final Note to Local Agents

This plan is intentionally strict. Its purpose is not to slow research down; it is to keep the research engine from mistaking a well-oiled route for a theorem. The most valuable post-v11 outcome would be a compact, externally legible statement of exactly what the project has, exactly what it lacks, and exactly which source-side primitive would close or freeze the next gap.

The next scientific triumph is not a louder claim. It is a smaller assumption set.

