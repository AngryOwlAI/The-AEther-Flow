<!-- authority: implementation_plan -->
# Recommendations Implementation Plan for `/continue-research`, v11

**Filename:** `recommendations_implementation_plan_continue_task-v11.md`  
**Intended repository path:** `implementations_plans/recommendations_implementation_plan_continue_task-v11.md`  
**Generated date:** 2026-06-28  
**Plan ID:** `recommendations_implementation_plan_continue_task-v11`  
**Implementation driver:** Continue Research functionality only  
**Scope:** Integrate recommendations 1 through 7 from the project review into the AEther-Flow project.  
**Explicit exclusions:** Do not implement recommendations 8, 9, or 10 from the review memo.  

---

## 0. Executive Implementation Intent

This plan converts the review recommendations into a sequence of bounded tasks that local AI agents can execute through the repository's Continue Research workflow. Every phase and every task below is designed to be implemented as a tracked `/continue-research` transaction, with one outer AgentJob per invocation unless a task explicitly stops at a human gate or read-only status report.

The plan has seven substantive implementation tracks:

1. Repair and harden active-state authority drift.
2. Execute the next narrow Gate Chair review for the stress-energy-interface candidate only after exact tracked human authorization.
3. Prevent same-shape matter-coupling interface orbit and route the next post-gate work toward a harder Matter-Coupling Bridge Target v1.
4. Generalize finite/local tests into parameterized source-family tests.
5. Mechanize finite/local source-side mathematics as support-only tooling.
6. Add scientific payload-density and route-orbit diagnostics.
7. Generate a dependency graph of accepted, draft/control, human-gated, blocked, and frozen objects.

Recommendations 8 through 10 are intentionally excluded. No task in this plan creates an external-review packet, changes the exact-GR benchmark policy, or creates a separate adoption-hardening program beyond preserving the project's existing claim-boundary rules.

---

## 1. Source Basis and Current Project State Assumptions

Local agents implementing this plan must verify these assumptions from tracked repository files before acting. This plan is not itself physics authority.

### 1.1 Current state sources to inspect

At the beginning of every phase, inspect the current tracked state from:

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/continue-research/SKILL.md`
- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0287.yaml`
- `research_control/handoffs/handoff-0287.md`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/design/gr_derivation_burden_map.md`
- `research_control/design/mathematical_decisiveness_completion_contract.md`
- `research_control/tasks/RT-20260614-254/00_TASK.yaml`
- `research_control/tasks/RT-20260614-254/jobs/completions/AJC-AJ-RT-20260614-254-001.yaml`
- `research_control/tasks/RT-20260614-254/artifacts/283_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_STRESS_ENERGY_INTERFACE_CANDIDATE_POST_STRESS_ROUTE_SELECTOR.yaml`
- `research_control/tasks/RT-20260614-251/artifacts/280_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_STRESS_ENERGY_INTERFACE_CANDIDATE.tex`
- `research_control/tasks/RT-20260614-252/artifacts/281_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_STRESS_ENERGY_INTERFACE_CANDIDATE_SMUGGLING_AUDIT.tex`
- `research_control/tasks/RT-20260614-253/artifacts/282_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_STRESS_ENERGY_INTERFACE_CANDIDATE_REFUTER_STRESS_TEST.tex`
- `research_control/current_frontier.md`
- `scripts/research_control/continue_research.py`
- `scripts/research_control/validate_research_control.py`
- `scripts/research_control/report_physics_progress_metrics.py`

### 1.2 Current state expected by this plan

The plan assumes the active state is the post-`RT-20260614-254` state:

- Active task: `RT-20260614-254`
- Latest handoff: `handoff-0287`
- Current status: `matter_coupling_stress_energy_interface_selector_requires_narrow_gate_no_adoption`
- Active derivation milestone: `matter_coupling`
- Current next action: exact tracked human authorization for one bounded Gate Chair packet deciding only the scoped evidence-status/precondition status of `SEI_src^{cand}(E,F_E^sharp)` and `SEICert^{cand}(E,F_E^sharp)`

The implementation must verify this against tracked state. If tracked state has advanced, local agents must adapt this plan by preserving the same recommendation intent but routing from the latest handoff and `program_state.yaml`.

### 1.3 Known state-drift defect to address

`research_control/current_frontier.md` may be stale relative to `research_control/program_state.yaml`, `registries/DISTANCE_TO_GR_LEDGER.csv`, and `handoff-0287`. This is the first project-system repair priority.

---

## 2. Universal Continue Research Protocol for Every Task

Every task in this plan must be implemented through Continue Research. Do not manually patch files outside a tracked Continue Research transaction unless the active tool/skill explicitly instructs a read-only inspection and no file changes are made.

### 2.1 Required command sequence before every routing decision

Run:

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "<task-specific targeted phrase>" --limit 10 --json
.venv/bin/python scripts/research_control/continue_research.py --json
```

If memory search returns relevant objects, inspect the canonical source files or registry rows named by the hits. Memory, wiki notes, semantic extracts, Obsidian, SQLite, and `.local/` are retrieval aids only.

### 2.2 Required Director behavior

For each task:

1. Enter Director of Research mode only when `continue_research.py` returns `director_decision_required`.
2. Create or reuse exactly one Director Decision Record.
3. Create or reuse exactly one outer AgentJob.
4. Choose the narrowest role that can complete the task.
5. Preserve active claim boundaries.
6. Do not create protected authority, Gate Chair verdicts, canonical ontology edits, or physics promotions unless exact tracked authorization exists.
7. Use `parent_child_parallel_synthesis` for physics AgentJobs.
8. Declare `target_derivation_milestone` and `milestone_burden` for physics AgentJobs.
9. Use project-system roles for tooling, docs, validator, registry, or state-drift repairs.

### 2.3 Required post-execution commands

After a state-changing AgentJob completion, run:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py
git diff --check
```

Then checkpoint only through:

```zsh
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py
```

Do not stage or commit manually if validation fails.

### 2.4 Required completion receipt fields

For physics tasks governed by the mathematical decisiveness contract, completions must include:

- `physics_progress_status`
- `distance_to_gr_delta`
- `mathematical_payload_manifest`
- `forbidden_conclusion_summary`
- `distance_to_gr_status`
- `parent_child_synthesis`
- `freeze_criteria_status` when the task repeats a burden or reports a scoped obstruction
- `route_cycle_control` when part of a repeated constructor/audit/stress/selector cycle
- `candidate_constructor_result` for Candidate Constructor tasks
- `theoretical_decision_output` for Theoretical Continuation Selector tasks
- `obstruction_record` when a precise obstruction or freeze is produced

For project-system tasks, completions must explicitly state that they are control/tooling/documentation work and do not promote physics claims.

### 2.5 Universal forbidden conclusions

Unless an exact Gate Chair or other protected authority packet explicitly says otherwise, every task must preserve:

- no canonical ontology edit
- no source-law adoption
- no `MetricData(E)` adoption
- no `g_eff` scope change
- no coupling-law adoption
- no matter-coupling derivation or adoption
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
- no validator, registry, generated derivative, local cache, handoff, approval, file order, commit state, PDF, HTML, or wiki object as scientific proof

---

## 3. Role and Route Matrix

Use this matrix as guidance. The Director must still select the exact role from registered repository roles and may create a task overlay only when allowed.

| Work type | Preferred role family | Physics milestone? | Notes |
|---|---|---:|---|
| State-authority drift repair | project-system / process-integrity / validator-oriented role | No | Repairs routing control, not physics. |
| Validator invariant or test | project-system / validator / research-ops role | No | Must not alter physics status. |
| `current_frontier.md` synchronization | project-system / documentation curator / process-integrity role | No | Treat as control-snapshot regeneration or repair. |
| Gate Chair evidence-status review | `gate-chair@0.1.0` | Yes, if physics gate | Requires exact tracked human authorization. |
| Post-gate route classification | `theoretical-continuation-selector@0.1.0` | Yes | Must output `theoretical_decision_output`. |
| Bridge target definitions | `ontology-formalizer@0.2.0` or task overlay | Yes | Draft/control only unless protected authority exists. |
| Bridge candidate construction | `candidate-constructor@0.2.0` | Yes | Must output candidate or precise obstruction. |
| Bridge audit | `smuggling-auditor@0.2.0` | Yes | Checks hidden target import and claim laundering. |
| Bridge stress test | `refuter@0.2.0` | Yes | Must classify route outcome and freeze risk. |
| Mechanization tooling | project-system tooling role | No, unless also producing a science draft artifact | Checker is support only. |
| Metrics/reporting extension | project-system tooling role | No | Scientific scoreboard must remain separated from operational validation. |
| Dependency graph generation | project-system tooling / memory-system role | No | Graph is navigational support, not authority. |

---

## 4. Phase Overview

| Phase | Recommendation implemented | Primary objective | Dependency |
|---|---|---|---|
| P0 | Plan intake and baseline | Register and prepare this plan for local execution | None |
| P1 | Recommendation 1 | Fix active-state authority drift and add drift guard | P0 |
| P2 | Recommendation 2 | Run exact narrow Gate Chair review after human authorization | P1 preferred; may stop human-gated |
| P3 | Recommendation 3 | Prevent same-shape interface orbit and launch Matter-Coupling Bridge Target v1 | P2 accepted-as-evidence outcome preferred |
| P4 | Recommendation 4 | Upgrade finite/local tests into parameterized source-family tests | P3 definitions or scoped preconditions |
| P5 | Recommendation 5 | Mechanize finite/local mathematics as support-only tooling | P3/P4 object signatures stable |
| P6 | Recommendation 6 | Add scientific payload-density guard | P1; can run before P3 |
| P7 | Recommendation 7 | Generate dependency graph of research objects and claim states | P1; benefits from P2/P3 |
| P8 | Integration | Validate rollout of P1-P7 and hand off continuation | P1-P7 complete or explicitly deferred |

---

# P0 — Plan Intake, Authority Bootstrap, and Baseline Snapshot

## P0-T01 — Add the v11 implementation plan as a tracked implementation plan

**Recommendation integrated:** prerequisite for recommendations 1-7  
**Task type:** project-system / implementation-plan intake  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system documentation/control role, not physics role  
**Physics milestone:** none  
**Claim boundary:** no physics claim promotion

### Objective

Add `implementations_plans/recommendations_implementation_plan_continue_task-v11.md` to the repository as the local AI-agent implementation plan for recommendations 1 through 7.

### Preconditions

- Confirm whether `implementations_plans/` is tracked, reserved, ignored, or unregistered.
- Confirm whether implementation plans require registry rows or documentation impact receipts.
- Confirm no active AgentJob already implements v11.

### Required reads

- `FOLDER_MAP.md`
- `research_control/tasks/README.md`
- `.codex/skills/continue-research/SKILL.md`
- any existing implementation plan files if present locally
- `scripts/project_control/classify_project_changes.py`
- `scripts/project_control/validate_documentation_impact.py`

### Required output

- Tracked file: `implementations_plans/recommendations_implementation_plan_continue_task-v11.md`
- Completion receipt identifying the file as implementation-plan/control guidance only.
- Documentation impact record if the classifier requires it.

### Forbidden output

- No `research_control/program_state.yaml` physics state change.
- No Distance-to-GR ledger change.
- No new physics task.
- No claim that the plan itself implements recommendations.

### Acceptance criteria

- File exists in intended path.
- File content explicitly excludes recommendations 8-10.
- Validation passes.
- Handoff states the next phase is P1 state-authority drift repair.

---

## P0-T02 — Baseline state snapshot and current-state reconciliation report

**Recommendation integrated:** prerequisite for recommendation 1  
**Task type:** project-system state audit  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** process-integrity / validator-oriented research-ops role  
**Physics milestone:** none

### Objective

Produce a baseline report comparing active state across:

- `research_control/program_state.yaml`
- latest handoff
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `research_control/current_frontier.md`
- active task folder
- registries for tasks, jobs, decisions, roles, and claim boundaries

### Required checks

The report must answer:

1. What is the active task according to `program_state.yaml`?
2. What is the latest handoff according to `program_state.yaml`?
3. Does the latest handoff file exist?
4. Does the active task folder exist?
5. Does `current_frontier.md` match active task, latest handoff, current status, target milestone, burden, and next action?
6. Does the Distance-to-GR ledger agree with the active burden state?
7. Are there pending or active AgentJobs that conflict with active state?
8. Are any human-gate approvals already present for the next Gate Chair packet?

### Required output

- Task-local artifact, for example:
  `research_control/tasks/<new-task-id>/artifacts/state_authority_baseline_snapshot.yaml`
- Completion receipt with:
  - `state_consistency_status`
  - `mismatched_sources`
  - `blocking_drift_detected`
  - `recommended_next_repair`

### Acceptance criteria

- The report identifies whether `current_frontier.md` is stale.
- The report identifies the authoritative next action.
- The report does not change physics state.
- Handoff routes to P1-T01 if drift is found, or P1-T03 if no drift is found.

---

# P1 — Active-State Authority Drift Repair and Guarding

## P1-T01 — Define active-state source-of-truth invariant

**Recommendation integrated:** 1  
**Task type:** project-system design/control  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** process-integrity / validator role  
**Physics milestone:** none

### Objective

Define a repository-local invariant for active-state authority:

1. `research_control/program_state.yaml` is the compact live state pointer.
2. The latest handoff named by `program_state.yaml` is the immediate routing authority.
3. `registries/DISTANCE_TO_GR_LEDGER.csv` is the persistent burden-state ledger.
4. `research_control/current_frontier.md` is a generated or synchronized control snapshot and must not contradict the above.
5. If a human-facing summary contradicts authority files, validators must fail or emit a blocking repair signal.

### Required design decisions

The task must decide one of these implementation paths:

- **Path A: Generated snapshot.** Make `current_frontier.md` generated from state files.
- **Path B: Manually authored but validator-guarded.** Keep it authored, but require validator equivalence checks.
- **Path C: Demote or archive stale snapshot.** Rename or mark it as historical and create a new generated state report.

Preferred path: **Path A** if feasible without excessive rewrite; otherwise **Path B**.

### Required output

- Design/control artifact:
  `research_control/tasks/<task-id>/artifacts/active_state_authority_invariant.md`
- Optional patch plan for validator changes.
- Completion receipt with:
  - `authority_invariant_selected`
  - `current_frontier_policy`
  - `validator_change_required`
  - `generated_snapshot_required`

### Acceptance criteria

- The invariant names concrete files and precedence order.
- It distinguishes control authority from generated derivative.
- It states exact failure conditions for drift.
- It does not change physics state.

---

## P1-T02 — Synchronize `research_control/current_frontier.md` with live state

**Recommendation integrated:** 1  
**Task type:** project-system repair / control snapshot update  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** documentation curator with process-integrity constraints, or validator-oriented repair role  
**Physics milestone:** none

### Objective

Update `research_control/current_frontier.md` so it reflects the current `program_state.yaml`, latest handoff, and Distance-to-GR ledger.

### Required content updates

The synchronized `current_frontier.md` must include:

- Active task ID from `program_state.yaml`
- Latest handoff ID from `program_state.yaml`
- Current status from `program_state.yaml`
- Current route family
- Target derivation milestone
- Current burden
- Required next authority
- Next recommended action
- Claim boundary summary
- Distance-to-GR status table copied or summarized from the ledger
- Exact blocked claims
- Source materials listing the current task artifacts and handoff
- Retrieval warning status if relevant

### Current expected values to verify before writing

- Active task: `RT-20260614-254`
- Latest handoff: `handoff-0287`
- Current status: `matter_coupling_stress_energy_interface_selector_requires_narrow_gate_no_adoption`
- Target derivation milestone: `matter_coupling`
- Next action: exact tracked human authorization for one bounded Gate Chair evidence-status/precondition review of `SEI_src^{cand}` and `SEICert^{cand}`

If these values have changed, use the latest tracked state instead.

### Forbidden content

Do not copy stale `RT-20260614-184` / `handoff-0218` frontier language except as a historical note if needed. Do not imply `g_eff` was unaccepted if the ledger says scoped source-extension `g_eff` has been accepted. Do not imply matter coupling has been derived.

### Required output

- Updated `research_control/current_frontier.md`
- Completion receipt naming all state sources used.
- Documentation impact receipt if required.

### Acceptance criteria

- `current_frontier.md` no longer contradicts `program_state.yaml`.
- It clearly states that matter coupling remains human-gated and unadopted.
- It clearly states the exact next authority required.
- Validation passes.

---

## P1-T03 — Add a validator guard for active-state drift

**Recommendation integrated:** 1  
**Task type:** tooling / validator implementation  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system validator/tooling role  
**Physics milestone:** none

### Objective

Implement a deterministic check that prevents or flags contradictions between active-state authority files and `current_frontier.md`.

### Candidate implementation paths

The Director must select the smallest acceptable path:

- Add a check to `scripts/research_control/validate_research_control.py`.
- Add a dedicated script such as `scripts/research_control/validate_current_frontier_sync.py` and call it from the main validator.
- Add test fixtures if the repository has a test harness.

### Required checks

The validator must compare:

- `active_task_id`
- `latest_handoff_id`
- `current_status`
- target milestone if present
- next recommended action, at least as a required phrase or handoff reference
- Distance-to-GR burden status, at least for the active burden

### Failure mode

If drift is detected, the validator must fail with:

- mismatched field name
- authoritative value
- snapshot value
- source path of the authoritative value
- suggested repair route

### Required output

- Script or validator patch.
- Test fixture or minimal regression if repository supports tests.
- Completion receipt with command results.
- No physics state change.

### Acceptance criteria

- Validator fails on a deliberately stale fixture or simulated stale content.
- Validator passes on synchronized current state.
- `validate_research_control.py` and `validate_research_control.py --check-diff` pass after implementation.

---

## P1-T04 — Add a generated current-state report option

**Recommendation integrated:** 1  
**Task type:** tooling / state report generation  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system tooling role  
**Physics milestone:** none

### Objective

Add a deterministic command that renders the active frontier from authoritative state, reducing the chance of future stale snapshots.

### Candidate command

```zsh
.venv/bin/python scripts/research_control/render_current_frontier.py --write
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_current_frontier.py --json
```

### Required behavior

- Read `program_state.yaml`.
- Resolve latest handoff.
- Read active task `00_TASK.yaml`.
- Read `DISTANCE_TO_GR_LEDGER.csv`.
- Render `research_control/current_frontier.md`.
- In `--check` mode, compare rendered output to tracked file without writing.
- In `--json` mode, emit machine-readable state.

### Required output

- New or modified script.
- Updated validator integration if selected.
- Updated completion receipt.
- Optional README note if documentation impact requires it.

### Acceptance criteria

- Running `--write` produces stable output.
- Running `--check` after `--write` passes.
- Main validators pass.
- Handoff routes to P2 or P6/P7 depending on active gate availability.

---

# P2 — Exact Narrow Gate Chair Review for the Stress-Energy-Interface Candidate

## P2-T01 — Gate readiness verification and authorization packet preparation

**Recommendation integrated:** 2  
**Task type:** human-gate readiness check  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** theoretical-continuation-selector or research-ops gate-readiness role, depending on active state  
**Physics milestone:** `matter_coupling` if physics role is used  
**Human gate:** this task does not consume Gate Chair authority

### Objective

Verify that the next lawful physics move remains exactly one bounded Gate Chair review of `SEI_src^{cand}(E,F_E^sharp)` and `SEICert^{cand}(E,F_E^sharp)` as scoped source-extension stress-energy-interface-candidate evidence/precondition.

### Required reads

- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0287.yaml`
- `research_control/tasks/RT-20260614-254/00_TASK.yaml`
- `research_control/tasks/RT-20260614-254/jobs/completions/AJC-AJ-RT-20260614-254-001.yaml`
- `research_control/tasks/RT-20260614-254/artifacts/283_...POST_STRESS_ROUTE_SELECTOR.yaml`
- Candidate, audit, and stress artifacts from `RT-20260614-251`, `RT-20260614-252`, and `RT-20260614-253`
- `research_control/approvals/README.md`
- Existing approval files to ensure no duplicate approval was already consumed

### Required output

- Gate-readiness artifact:
  `research_control/tasks/<task-id>/artifacts/stress_energy_interface_candidate_gate_readiness_check.yaml`
- Exact authorization string copied from the latest handoff.
- Status:
  - `authorization_absent_human_gate_required`, or
  - `authorization_present_ready_for_gate_chair`, or
  - `state_advanced_replan_required`

### Exact authorization string to preserve

If still current, the required authorization text is:

```text
I authorize one bounded Gate Chair packet to decide whether the draft/control source-side stress-energy-interface candidate SEI_src^{cand}(E,F_E^sharp) and SEICert^{cand}(E,F_E^sharp) constructed in RT-20260614-251 audited in RT-20260614-252 and stress-survived in RT-20260614-253 may be accepted only as scoped source-extension stress-energy-interface-candidate evidence/precondition under its declared finite/local source-side scope with no canonical ontology edit no source-law adoption no MetricData(E) adoption no g_eff scope change no coupling-law adoption no matter-coupling derivation or adoption no stress-energy semantics no stress-energy tensor no matter action no Einstein equations no benchmark promotion and no completed derivation.
```

### Acceptance criteria

- If no exact authorization exists, the task stops human-gated and does not create a Gate Chair AgentJob.
- If exact authorization exists, the handoff routes to P2-T02.
- No evidence/precondition status is accepted by this task.
- No matter coupling or stress-energy semantics is adopted.

---

## P2-T02 — Execute the narrow Gate Chair evidence-status/precondition review

**Recommendation integrated:** 2  
**Task type:** protected physics Gate Chair review  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Required role:** `gate-chair@0.1.0` or exact registered successor  
**Physics milestone:** `matter_coupling`  
**Human gate:** required and consumed exactly once

### Objective

Decide only whether the draft/control source-side stress-energy-interface candidate data may be accepted as scoped source-extension stress-energy-interface-candidate evidence/precondition under its declared finite/local source-side scope.

### Preconditions

- Exact human authorization exists as a tracked approval file.
- Approval has not already been consumed.
- Candidate construction, audit, stress, and selector artifacts are present and hash-checked if registries provide hashes.
- Claim boundary forbids adoption and downstream promotion.

### Allowed verdicts

The Gate Chair may choose exactly one:

1. `accepted_as_scoped_source_extension_stress_energy_interface_candidate_evidence_only`
2. `rejected`
3. `returned_for_constructor_repair`
4. `returned_for_smuggling_audit`
5. `returned_for_refuter_stress`
6. `requires_broader_ontology_authority`
7. `invalid_under_claim_boundary`

### Required review questions

The Gate Chair must answer:

1. Does the candidate have a complete construction-audit-stress-selector chain?
2. Are the cited evidence paths present and scoped?
3. Is the candidate still finite/local source-side data only?
4. Does the candidate avoid target metric, stress-energy tensor, matter action, detector semantics, and empirical matter import?
5. Does the candidate avoid evidence-as-adoption laundering?
6. Does acceptance, if granted, remain evidence/precondition only?
7. What downstream claims remain blocked even if accepted?
8. What exact next route follows from the verdict?

### Required output

- Gate Chair TeX or YAML artifact:
  `research_control/tasks/<task-id>/artifacts/<number>_...STRESS_ENERGY_INTERFACE_CANDIDATE_SOURCE_EXTENSION_EVIDENCE_GATE_CHAIR_REVIEW.tex`
- Approval consumption record.
- Updated Distance-to-GR ledger row for `matter_coupling` if verdict changes status.
- Updated registries.
- Completion receipt with:
  - `physics_progress_status`
  - `distance_to_gr_delta`
  - `mathematical_payload_manifest`
  - `forbidden_conclusion_summary`
  - `parent_child_synthesis`
  - exact verdict

### Forbidden conclusions

Even if accepted as evidence/precondition, the task must not claim:

- coupling-law adoption
- matter-coupling derivation or adoption
- stress-energy semantics
- stress-energy tensor
- matter action
- Einstein equations
- benchmark promotion
- completed derivation

### Acceptance criteria

- Gate verdict is one of the allowed values.
- Approval file is tracked and consumed exactly once.
- Ledger and handoff match verdict.
- Validators pass.
- Handoff routes according to verdict:
  - accepted -> P2-T03 or P3-T01
  - repair -> constructor/audit/stress repair task
  - rejected -> selector for obstruction/freeze/alternate route
  - broader authority -> human-gated ontology or authority route
  - invalid -> process-integrity repair

---

## P2-T03 — Post-Gate route classification and branch selection

**Recommendation integrated:** 2 and 3  
**Task type:** theoretical route selector  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `theoretical-continuation-selector@0.1.0`  
**Physics milestone:** `matter_coupling`

### Objective

After the Gate Chair verdict, classify the next lawful matter-coupling route. If the candidate was accepted as scoped evidence/precondition only, route toward the harder bridge target rather than same-shape repetition.

### Branch table

| Gate verdict | Required next route |
|---|---|
| accepted as scoped evidence only | P3 Matter-Coupling Bridge Target v1 |
| rejected | precise obstruction, repair, or freeze selector |
| returned for constructor repair | one bounded Candidate Constructor repair with exact defect |
| returned for audit | one bounded Smuggling Auditor packet with exact audit target |
| returned for stress | one bounded Refuter packet with exact stress target |
| requires broader ontology authority | human-gated ontology/authority route |
| invalid under claim boundary | process-integrity repair |

### Required output

- Theoretical decision artifact.
- Updated handoff.
- Freeze criteria if route would repeat construction/audit/stress without new mathematical payload.
- Explicit `route_cycle_control`.

### Acceptance criteria

- Selector does not route to another generic stress-energy-interface criteria packet if the same candidate was accepted.
- Selector names Matter-Coupling Bridge Target v1 as the preferred next bridge-facing route when allowed.
- All downstream claim blocks remain intact.

---

# P3 — Matter-Coupling Bridge Target v1 and Anti-Orbit Control

## P3-T01 — Add route-cycle guard against same-shape interface repetition

**Recommendation integrated:** 3  
**Task type:** project-system + physics-routing control  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** process-integrity / validator role, with physics-routing awareness  
**Physics milestone:** none unless implemented through a physics selector

### Objective

Prevent the system from repeating criteria → candidate → audit → stress → selector cycles for stress-energy-interface records after Gate Chair evidence/precondition acceptance unless the next task introduces a harder mathematical object, a repair, an obstruction, a freeze, or a protected gate.

### Required guard rule

After a stress-energy-interface candidate has completed construction, audit, stress, selector, and Gate Chair evidence/precondition review, a future task must not repeat the same-shape sequence unless one of these is true:

- Gate Chair returned the candidate for a specific repair.
- A Refuter found a precise obstruction requiring reconstruction.
- A Theoretical Continuation Selector chooses a materially new target.
- The task attempts Matter-Coupling Bridge Target v1 or a stricter successor.
- A human-gated authority route authorizes broader review.
- A freeze review is triggered.

### Candidate implementation points

- `scripts/research_control/continue_research.py`
- `scripts/research_control/validate_research_control.py`
- `research_control/design/mathematical_decisiveness_completion_contract.md`
- role overlays for Theoretical Continuation Selector, Candidate Constructor, Smuggling Auditor, and Refuter
- `report_physics_progress_metrics.py` as diagnostic support, not hard gate

### Required output

- Control artifact defining the guard.
- Script or validator update if feasible.
- Completion receipt with `cycle_guard_installed: true` or `cycle_guard_design_only: true`.
- If design-only, handoff to implementation task.

### Acceptance criteria

- Future same-shape cycles require explicit `route_cycle_control`.
- Validator or selector contract emits blocking warning if repetition lacks new payload.
- No existing valid historical task is rewritten.
- No physics claims are promoted.

---

## P3-T02 — Formalize Matter-Coupling Bridge Target v1

**Recommendation integrated:** 3  
**Task type:** physics Ontology Formalizer packet  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `ontology-formalizer@0.2.0` with task overlay if needed  
**Physics milestone:** `matter_coupling`

### Objective

Define the hard bridge target that must follow scoped stress-energy-interface evidence/precondition acceptance.

### Required mathematical object

The artifact must define a draft/control target, provisionally named:

```text
MatterCouplingBridgeTarget_v1(E)
```

or an equivalent source-side name chosen by the Director.

### Required components

The target must specify:

1. **Source domain**
   - accepted scoped source-extension evidence/preconditions available
   - scoped `M_src`
   - scoped `g_eff`
   - stress-energy-interface candidate evidence/precondition if accepted
   - source packages and allowed source variations

2. **Target codomain**
   - pre-tensorial or tensorial matter-interface data over the scoped `M_src, g_eff` setting
   - if tensorial output is not allowed yet, define an explicit pre-tensorial codomain and the missing tensorial promotion burden

3. **Locality condition**
   - source-local dependence only
   - no target metric import beyond previously scoped `g_eff` compatibility
   - no detector, matter action, empirical field, or benchmark premise

4. **Covariance / naturality condition**
   - relabeling invariance
   - source-family morphism compatibility
   - compatibility with finite/local source variations

5. **Sector-uniformity condition**
   - stronger than the current two-sector shared-form rule
   - parameterized across source-sector families or graph-indexed families

6. **Conservation / compatibility obligation**
   - source-side analogue of balance/flux compatibility
   - explicit statement that this is not yet Bianchi identity, stress-energy conservation, or Einstein equations

7. **No-target-import certificate**
   - target topology, target atlas, target metric, stress-energy tensor, matter action, detector semantics, empirical fit, and Einstein equations cannot be premises

8. **Failure labels**
   - missing codomain
   - nonlocality
   - noncovariance
   - sector-nonuniformity
   - conservation-analogue failure
   - target import
   - evidence-as-adoption
   - scoped `g_eff` overread
   - tensorial overread
   - downstream promotion overread

### Required theorem

Include an eligibility theorem:

> If a packet supplies the bridge target obligations, then it becomes eligible only for Candidate Constructor attempt, audit, stress, or protected evidence-status review. It does not derive or adopt matter coupling.

### Required output

- Draft/control TeX artifact.
- Completion receipt with new mathematical payload:
  - `definition`
  - `dependency_map_update`
  - `obstruction label family`
  - `eligibility theorem`
- Handoff to P3-T03.

### Acceptance criteria

- Defines a harder object than `SEI_src^{cand}`.
- Does not simply restate stress-energy-interface criteria.
- Names precise acceptance and failure criteria.
- Preserves all blocked downstream claims.

---

## P3-T03 — Attempt Matter-Coupling Bridge Candidate v1 or return precise obstruction

**Recommendation integrated:** 3  
**Task type:** physics Candidate Constructor packet  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `candidate-constructor@0.2.0`  
**Physics milestone:** `matter_coupling`

### Objective

Attempt to construct a draft/control bridge candidate satisfying Matter-Coupling Bridge Target v1, or return one precise obstruction.

### Candidate object options

The constructor may define one of:

- `MCBridge_src^{cand}(E)`
- `PreT_src^{cand}(E)`
- `SourceMatterInterface_v1(E)`
- another name chosen by the Director, provided it is source-side and draft/control

### Required construction fields

- domain object
- codomain object
- source-local map or relation
- morphism/relabeling behavior
- sector-uniformity rule
- source variation behavior
- balance/flux compatibility
- relationship to scoped `g_eff`
- relationship to accepted stress-energy-interface evidence/precondition
- no-target-import certificate
- fail-closed obstruction labels

### Required obstruction if construction fails

If no candidate is constructed, record exactly one primary obstruction:

- `OB-MC-BRIDGE-CODOMAIN-MISSING`
- `OB-MC-BRIDGE-LOCALITY-FAIL`
- `OB-MC-BRIDGE-COVARIANCE-FAIL`
- `OB-MC-BRIDGE-SECTOR-UNIFORMITY-FAIL`
- `OB-MC-BRIDGE-CONSERVATION-ANALOGUE-FAIL`
- `OB-MC-BRIDGE-GEFF-OVERREAD`
- `OB-MC-BRIDGE-TENSORIAL-OVERREAD`
- `OB-MC-BRIDGE-TARGET-IMPORT`
- `OB-MC-BRIDGE-EVIDENCE-AS-ADOPTION`
- `OB-MC-BRIDGE-DOWNSTREAM-PROMOTION`

### Required output

- Candidate or obstruction TeX/YAML artifact.
- Completion receipt with `candidate_constructor_result`.
- If candidate constructed: handoff to P3-T04.
- If obstruction found: handoff to Refuter obstruction stress or Theoretical Continuation Selector.

### Acceptance criteria

- The candidate is materially stronger than the existing `SEI_src^{cand}`.
- If no candidate exists, the obstruction is precise and reusable.
- No matter coupling is adopted.
- No stress-energy tensor or matter action is imported.

---

## P3-T04 — Smuggling audit for Matter-Coupling Bridge Candidate v1

**Recommendation integrated:** 3  
**Task type:** physics Smuggling Auditor packet  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `smuggling-auditor@0.2.0`  
**Physics milestone:** `matter_coupling`

### Objective

Audit the bridge candidate for hidden target import, tensor laundering, matter-action laundering, conservation-law laundering, scoped `g_eff` overread, evidence-as-adoption laundering, and downstream promotion pressure.

### Required audit dimensions

- target topology import
- target atlas import
- target metric import beyond scoped compatibility
- Lorentzian signature import
- proper-time import
- stress-energy tensor semantics import
- matter action or Lagrangian import
- detector or empirical matter field semantics import
- Bianchi identity or conservation law import
- coupling-law adoption laundering
- `MetricData(E)` adoption laundering
- `g_eff` scope expansion laundering
- process-authority laundering
- validator/registry/generated derivative as proof
- benchmark fit import
- Einstein-equation premise import

### Required output

- Audit artifact.
- Verdict:
  - `source_pure_as_written_pending_refuter_stress`
  - `audit_failed_precise_obstruction`
  - `returned_for_constructor_repair`
  - `invalid_under_claim_boundary`

### Acceptance criteria

- Audit pass does not equal adoption.
- Audit failure gives exact obstruction.
- If passed, handoff routes to P3-T05.
- If failed, handoff routes to repair or obstruction selector.

---

## P3-T05 — Refuter stress test for Matter-Coupling Bridge Candidate v1

**Recommendation integrated:** 3  
**Task type:** physics Refuter packet  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `refuter@0.2.0`  
**Physics milestone:** `matter_coupling`

### Objective

Stress the audited bridge candidate under hard mathematical pressures that matter for eventual universal coupling.

### Required stress targets

- nonempty output
- bottom completeness
- source-locality
- relabeling/naturality
- finite variation stability
- sector-uniformity beyond the original two-sector case
- compatibility with scoped `M_src`
- compatibility with scoped `g_eff`
- balance/flux conservation-analogue coherence
- tensorial-overread pressure
- target-import pressure
- downstream-promotion pressure
- evidence-as-adoption pressure
- stress-energy semantics pressure
- matter-action pressure
- Einstein-equation pressure

### Required outcomes

One of:

- `bridge_candidate_stress_survived_pending_selector`
- `precise_obstruction_found`
- `route_frozen`
- `returned_for_constructor_repair`
- `invalid_under_claim_boundary`

### Required output

- Refuter TeX artifact.
- `obstruction_record` if applicable.
- `freeze_criteria_status` if repeated burden or scoped obstruction.
- Handoff to P3-T06.

### Acceptance criteria

- If stress survives, it survives only as draft/control bridge candidate data.
- If stress fails, the failure is precise and future-routable.
- No matter coupling, stress-energy tensor, matter action, or Einstein equations are adopted.

---

## P3-T06 — Post-bridge stress selector

**Recommendation integrated:** 3  
**Task type:** physics Theoretical Continuation Selector  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `theoretical-continuation-selector@0.1.0`  
**Physics milestone:** `matter_coupling`

### Objective

Classify the post-stress route for the bridge candidate.

### Route options

- narrow Gate Chair evidence-status/precondition review
- constructor repair
- smuggling audit repeat with exact target
- Refuter stress repeat with exact new stress target
- precise obstruction route
- local freeze
- broader ontology authority human gate
- invalid-under-claim-boundary repair

### Anti-orbit requirement

If the bridge candidate merely repeats the stress-energy-interface candidate shape, the selector must trigger freeze review or repair rather than route to another same-shape cycle.

### Required output

- Theoretical decision artifact.
- Handoff naming exact next route.
- `route_cycle_control`.
- `freeze_criteria_status` if repetition detected.

### Acceptance criteria

- Selector chooses the lowest-authority route that adds decision information.
- It does not promote matter coupling.
- It does not route into repetitive orbit.

---

# P4 — Parameterized Finite/Local Source-Family Upgrade

## P4-T01 — Formalize parameterized finite/local source-family target

**Recommendation integrated:** 4  
**Task type:** physics Ontology Formalizer packet  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `ontology-formalizer@0.2.0`  
**Physics milestone:** depends on route, likely `matter_coupling` or `finite_variation_robustness`

### Objective

Replace the single two-sector finite/local family style with a parameterized family target that can test scalability.

### Candidate target forms

The Director must choose one:

1. `F_n` indexed by finite cardinality `n`.
2. `G`-indexed finite graph/DAG source families.
3. Category-like finite source packages with morphisms.
4. A hybrid family using graph-indexed sectors and finite variations.

### Required definitions

- objects/sectors
- morphisms or relabelings
- source tokens
- source states
- allowed variations
- family restriction maps
- sector-uniformity rule
- finite/locality rule
- bottom/fail-closed branches
- no-target-import certificate
- invariance tests

### Required output

- Draft/control TeX artifact defining the target.
- Failure labels for:
  - nonuniform sector behavior
  - relabeling failure
  - variation instability
  - missing morphism behavior
  - target import
  - evidence-as-adoption
- Handoff to P4-T02.

### Acceptance criteria

- The target is strictly more general than `F_E^sharp={S0,S1}`.
- It does not require target geometry.
- It provides tests that a Candidate Constructor can attempt.

---

## P4-T02 — Construct parameterized family witness or obstruction

**Recommendation integrated:** 4  
**Task type:** physics Candidate Constructor packet  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `candidate-constructor@0.2.0`  
**Physics milestone:** `matter_coupling` or `finite_variation_robustness`

### Objective

Construct a parameterized finite/local source-family witness compatible with the current bridge path, or return a precise obstruction.

### Required witness components

- parameter set
- sectors/objects
- morphisms/relabelings
- source-token assignment
- source-state assignment
- allowed variation rules
- invariance rules
- compatibility with `SEI_src^{cand}` or bridge target if applicable
- no-target-import certificate

### Required output

- Candidate artifact or obstruction artifact.
- Candidate constructor result.
- Handoff to audit or obstruction selector.

### Acceptance criteria

- The construction is not merely the two-sector case renamed.
- It supports at least one nontrivial relabeling or morphism.
- It supports finite/local variation tests.
- If it fails, the failure is precise.

---

## P4-T03 — Smuggling audit for parameterized family

**Recommendation integrated:** 4  
**Task type:** physics Smuggling Auditor packet  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `smuggling-auditor@0.2.0`  
**Physics milestone:** same as P4-T02

### Objective

Audit the parameterized family for target import, hidden universality import, benchmark import, source-law adoption laundering, and process-authority laundering.

### Required output

- Audit artifact.
- Source-purity verdict or precise obstruction.
- Handoff to P4-T04 if passed.

### Acceptance criteria

- The audit confirms parameterization is source-defined.
- No target geometry or empirical matter behavior is used.
- Pass routes to Refuter stress only.

---

## P4-T04 — Refuter stress for parameterized family

**Recommendation integrated:** 4  
**Task type:** physics Refuter packet  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `refuter@0.2.0`  
**Physics milestone:** same as P4-T02

### Objective

Stress the parameterized family under scalability and invariance pressures.

### Required stress targets

- nonempty witnesses across parameters
- bottom completeness
- relabeling invariance
- morphism compatibility
- variation stability
- no sector hand-tailoring
- no target repair
- no hidden universal matter-coupling import
- no process-authority import
- no downstream promotion

### Required output

- Refuter artifact.
- Stress verdict.
- Obstruction or freeze record if applicable.
- Handoff to P4-T05.

### Acceptance criteria

- Stress survival is scoped and finite/local or parameterized finite/local only.
- Failure produces a reusable obstruction.
- No global theorem is claimed unless separately authorized and proved.

---

## P4-T05 — Selector for parameterized-family route integration

**Recommendation integrated:** 4  
**Task type:** physics Theoretical Continuation Selector  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** `theoretical-continuation-selector@0.1.0`

### Objective

Decide how the parameterized-family result changes the next matter-coupling bridge route.

### Possible outcomes

- use parameterized family as support for Matter-Coupling Bridge Target v1
- route to bridge candidate repair
- record scoped obstruction
- freeze the parameterized route
- require broader ontology authority
- route to mechanization support in P5

### Acceptance criteria

- The selector names a concrete next packet.
- It updates Distance-to-GR only if warranted.
- It preserves all downstream blocks.

---

# P5 — Mechanize Finite/Local Mathematics as Support-Only Tooling

## P5-T01 — Mechanization boundary and support-only checker design

**Recommendation integrated:** 5  
**Task type:** project-system tooling design with physics-source awareness  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system tooling role, with physics claim-boundary constraints  
**Physics milestone:** none unless a separate science draft artifact is produced

### Objective

Design a support-only mechanization layer for finite/local source-side objects. The checker must not become proof authority.

### Required design decisions

- language: Python first, unless theorem prover route is explicitly authorized later
- path location:
  - `scripts/research_control/mechanized_checks/` or similar
  - `tests/fixtures/research_control/` for fixtures
- input format:
  - YAML/JSON fixtures extracted from task artifacts
  - hand-authored fixtures
  - no parsing TeX as authority unless explicitly scoped
- output format:
  - JSON report
  - Markdown report if needed
- validator integration:
  - optional support-only checks
  - failure mode must distinguish tooling failure from physics obstruction

### Required boundary statement

Every generated checker report must state:

> This mechanized report is support-only scaffolding. It is not proof authority, not source-law adoption, not `MetricData(E)` adoption, not `g_eff` adoption or scope expansion, not matter coupling, not stress-energy semantics, not a stress-energy tensor, not a matter action, not Einstein equations, not benchmark promotion, and not completed derivation.

### Required output

- Design artifact.
- Handoff to P5-T02.

### Acceptance criteria

- The design names exact predicates to mechanize.
- The design names exact files to read and write.
- The design prevents checker proof-authority overread.

---

## P5-T02 — Implement finite/local checker model

**Recommendation integrated:** 5  
**Task type:** project-system tooling implementation  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system tooling role  
**Physics milestone:** none

### Objective

Implement executable representations of the finite/local source-side objects needed for the current SEI and bridge lines.

### Required model components

- source family
- source sectors
- source tokens
- source states
- balance predicate
- flux ledger
- bottom result
- no-target-import scan
- bridge compatibility marker
- scoped `g_eff` boundary marker
- candidate map
- certificate object
- obstruction labels
- variation/relabeling structure if P4 has completed

### Required commands

Candidate command names:

```zsh
.venv/bin/python scripts/research_control/mechanized_checks/check_finite_local_candidate.py --fixture <fixture> --json
.venv/bin/python scripts/research_control/mechanized_checks/check_finite_local_candidate.py --fixture <fixture> --markdown <report>
```

### Required output

- Script(s)
- Fixture(s)
- Minimal README or in-script help
- Completion receipt with command results

### Acceptance criteria

- Checker runs on at least one fixture.
- Checker produces deterministic JSON.
- Checker fails closed on malformed target-import fixture.
- No physics state is promoted.

---

## P5-T03 — Add property tests for finite/local invariants

**Recommendation integrated:** 5  
**Task type:** project-system tests/tooling  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system testing role  
**Physics milestone:** none

### Objective

Add automated tests for support-only finite/local invariants.

### Required test classes

- bottom completeness
- nonempty output
- no-target-import rejection
- evidence-as-adoption rejection
- scoped `g_eff` overread rejection
- process-authority-as-proof rejection
- relabeling invariance if P4 available
- finite variation stability if P4 available
- malformed fixture failure
- deterministic output

### Required output

- Tests under `tests/` or repository-appropriate location.
- Fixtures under `tests/fixtures/` or support directory.
- Completion receipt.

### Acceptance criteria

- Tests pass.
- Tests are included in a documented command.
- Test failures do not imply physics obstructions unless a separate Refuter task records one.

---

## P5-T04 — Run checker on current SEI candidate as support-only report

**Recommendation integrated:** 5  
**Task type:** support-only tooling run  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system tooling role, not Gate Chair  
**Physics milestone:** none unless Director explicitly routes a physics support artifact

### Objective

Run the mechanized checker on a fixture representing the current stress-energy-interface candidate and produce a support-only report.

### Required reads

- `RT-20260614-251` candidate artifact
- `RT-20260614-252` audit artifact
- `RT-20260614-253` stress artifact
- checker fixture

### Required output

- JSON report
- Optional Markdown report
- Completion receipt stating support-only status

### Acceptance criteria

- Report does not change claim status.
- Report can be cited as tooling support but not proof authority.
- Handoff routes to validator integration or bridge work.

---

## P5-T05 — Integrate checker into validation or metrics as non-authoritative support

**Recommendation integrated:** 5  
**Task type:** project-system validator integration  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system validator/tooling role  
**Physics milestone:** none

### Objective

Optionally integrate mechanized checks into validation or metrics without letting them become scientific proof authority.

### Integration options

- Add a separate support-only command to validation docs.
- Add optional validator check for fixture syntax.
- Add metrics count for checker reports, but keep it operational.
- Add `--support-checks` flag rather than default hard gate if fragile.

### Required output

- Validator or docs patch.
- Completion receipt.
- Validation results.

### Acceptance criteria

- Integration is deterministic.
- Checker output does not affect Distance-to-GR status.
- Validator failure from checker syntax is tooling failure, not physics failure.
- Main validators pass.

---

# P6 — Scientific Payload-Density and Route-Orbit Diagnostics

## P6-T01 — Define payload-density metrics and thresholds

**Recommendation integrated:** 6  
**Task type:** project-system metrics design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system metrics/reporting role  
**Physics milestone:** none

### Objective

Define diagnostics that measure whether research-control cycles are producing substantive scientific payloads rather than validated task churn.

### Required metrics

At minimum define:

1. `tasks_since_last_distance_to_gr_delta`
2. `tasks_since_last_burden_discharged`
3. `new_payload_items_per_physics_task`
4. `new_payload_items_per_cycle`
5. `selector_cycles_without_new_payload`
6. `same_burden_repetition_count`
7. `freeze_reviews_triggered_by_repetition`
8. `bridge_attempts_since_last_gate`
9. `obstructions_created`
10. `obstructions_reused`
11. `candidate_construct_audit_stress_selector_cycles`
12. `gate_ready_cycles_without_gate_verdict`
13. `support_only_tooling_reports`
14. `physics_promotion_authorized_true_count`
15. `physics_promotion_authorized_false_count`

### Threshold policy

Define thresholds as warnings first, not hard failures, unless a later project-system task makes them hard gates. Candidate warnings:

- More than 4 physics tasks on the same burden without new payload.
- More than 2 selector cycles without construction, obstruction, gate, or freeze.
- Construct/audit/stress/selector cycle repeated after a Gate Chair accepted evidence/precondition without a harder target.
- `distance_to_gr_delta.changed` false for multiple physics tasks despite route claiming bridge progress.
- Candidate result missing or empty for Candidate Constructor task.

### Required output

- Metrics design artifact.
- Handoff to P6-T02.

### Acceptance criteria

- Metrics clearly distinguish operational validation from scientific progress.
- Metrics do not create physics claims.
- Metrics are machine-computable from completion receipts and registries.

---

## P6-T02 — Extend `report_physics_progress_metrics.py`

**Recommendation integrated:** 6  
**Task type:** project-system metrics implementation  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system tooling role  
**Physics milestone:** none

### Objective

Implement payload-density and route-orbit diagnostics in `scripts/research_control/report_physics_progress_metrics.py`.

### Required implementation details

- Read existing completion YAMLs.
- Count `mathematical_payload_manifest` items.
- Count `new_mathematical_payload` items for legacy completions.
- Track tasks by burden ID and milestone.
- Track `route_cycle_control`.
- Track `freeze_criteria_status`.
- Track `candidate_constructor_result`.
- Track `theoretical_decision_output`.
- Track Gate Chair verdicts.
- Keep all operational metrics separate from scientific progress metrics.
- Add a `payload_density_metrics` section.
- Add a `route_orbit_risk_metrics` section.
- Add `diagnostic_warnings` without making them physics evidence.

### Required output

- Script patch.
- JSON output example, if repository convention allows.
- Completion receipt with command output.

### Acceptance criteria

- Existing report still runs.
- New metrics appear in JSON and Markdown/table output if present.
- No operational metric keys contaminate scientific progress metrics.
- Validation passes.

---

## P6-T03 — Add route-orbit warning into Continue Research context packet

**Recommendation integrated:** 6  
**Task type:** project-system routing support  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system tooling / research-control role  
**Physics milestone:** none

### Objective

Surface payload-density and orbit-risk warnings in the Continue Research context packet so the Director sees them before routing.

### Candidate implementation

- Extend `scripts/research_control/continue_research.py` to include:
  - `payload_density_warning`
  - `route_orbit_warning`
  - `same_burden_repetition_warning`
  - `gate_ready_without_gate_warning`
  - `recommended_guard_action`

### Required behavior

Warnings must not automatically block a valid human-gated Gate Chair route. They should inform Director routing and completion requirements.

### Required output

- Script patch.
- Completion receipt.
- Validation output.

### Acceptance criteria

- Director packet includes warnings when applicable.
- No warning changes physics claim status.
- Gate Chair route remains available when exact authorization exists.

---

## P6-T04 — Add completion validator checks for required payload fields

**Recommendation integrated:** 6  
**Task type:** project-system validator hardening  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** validator/tooling role  
**Physics milestone:** none

### Objective

Ensure future physics tasks governed by the mathematical decisiveness contract cannot complete without concrete payload fields.

### Required checks

For future physics completions:

- `physics_progress_status.status` present and allowed.
- `distance_to_gr_delta` present.
- `mathematical_payload_manifest` contains at least one item with nonempty:
  - `payload_id`
  - `payload_type`
  - `object_name`
  - `claim_status`
  - `source_path`
  - `burden_effect`
  - `summary`
- `forbidden_conclusion_summary` present.
- Candidate Constructor tasks include `candidate_constructor_result`.
- Selector tasks include `theoretical_decision_output`.
- Repeated-burden tasks include `freeze_criteria_status`.
- Route-cycle tasks include `route_cycle_control`.

### Required output

- Validator patch.
- Regression fixture.
- Completion receipt.

### Acceptance criteria

- Validator catches missing payload manifest in fixture.
- Validator passes current valid completions or handles historical compatibility.
- No historical task is rewritten unless separately authorized.

---

# P7 — Dependency Graph of Research Objects and Claim States

## P7-T01 — Define dependency graph schema

**Recommendation integrated:** 7  
**Task type:** project-system design  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system memory/registry role  
**Physics milestone:** none

### Objective

Define a generated dependency graph showing the state of research objects, claim boundaries, and task relationships.

### Required node classes

- source ontology object
- source-extension evidence/precondition
- draft/control candidate
- accepted scoped object
- human-gated object
- blocked burden
- frozen negative
- obstruction
- Gate Chair verdict
- task
- AgentJob
- artifact
- handoff
- ledger row

### Required edge classes

- `requires`
- `constructs`
- `audits`
- `stress_tests`
- `selects_next`
- `accepts_as_evidence`
- `adopts_scoped`
- `rejects`
- `blocks`
- `freezes`
- `forbids_overread`
- `depends_on`
- `updates_ledger`
- `handoffs_to`
- `requires_human_gate`

### Required state colors or labels

Use labels, not hardcoded colors, unless a visual renderer later maps labels to colors:

- `canonical_source`
- `science_draft`
- `draft_control`
- `proposal_only`
- `source_extension_evidence`
- `accepted_scoped`
- `human_gated`
- `blocked`
- `frozen_negative`
- `rejected`
- `support_only`

### Required output formats

Design must choose at least two:

- JSON graph
- Markdown summary table
- DOT graph
- Mermaid graph
- CSV node/edge tables

Preferred: JSON + Markdown + DOT or Mermaid.

### Required output

- Graph schema artifact.
- Handoff to P7-T02.

### Acceptance criteria

- Schema maps directly to existing registries and completion fields.
- Schema states graph is navigational support, not physics authority.
- It can represent current `g_eff`, matter-coupling, and frozen finite-toy statuses.

---

## P7-T02 — Implement dependency graph extractor

**Recommendation integrated:** 7  
**Task type:** project-system tooling implementation  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system tooling/memory role  
**Physics milestone:** none

### Objective

Implement a deterministic script that extracts dependency graph data from tracked state.

### Candidate command

```zsh
.venv/bin/python scripts/research_control/render_dependency_graph.py --json output/research_dependency_graph.json
.venv/bin/python scripts/research_control/render_dependency_graph.py --markdown wiki/indexes/research_dependency_graph.md
.venv/bin/python scripts/research_control/render_dependency_graph.py --dot output/research_dependency_graph.dot
```

The Director must choose repository-appropriate output paths and avoid untracked scratch output in the final transaction.

### Required reads

- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- completion YAMLs
- handoff YAMLs
- current state file

### Required extraction behavior

- Create nodes for tasks, jobs, artifacts, ledger burdens, and named physics objects when fields expose them.
- Create edges from parent task/handoff relationships.
- Create edges from completion payload manifests.
- Create edges from Gate Chair verdicts.
- Create edges from blocked claims.
- Mark support-only tooling separately.

### Required output

- Script.
- Generated graph artifact(s).
- Completion receipt.

### Acceptance criteria

- Script runs deterministically.
- Graph includes at minimum:
  - `Resp_lc`
  - `M_src`
  - scoped `g_eff`
  - `B_E^{rec}`
  - `BridgeCert`
  - `SEI-MC` criteria
  - `SEI_src^{cand}`
  - matter-coupling burden
  - Einstein-equations burden
  - benchmark-promotion burden
  - finite toy metric response frozen negative
- Graph clearly labels blocked downstream claims.
- Graph does not become authority.

---

## P7-T03 — Add graph freshness validation

**Recommendation integrated:** 7  
**Task type:** project-system validator integration  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** validator/tooling role  
**Physics milestone:** none

### Objective

Add a check that generated graph artifacts are fresh relative to source registries and completions.

### Candidate behavior

- `render_dependency_graph.py --check`
- integrate with `validate_research_control.py --check-diff`, or keep as a separate validation command documented in completion
- compare generated graph hash or content

### Required output

- Script update or validator patch.
- Completion receipt.
- Validation results.

### Acceptance criteria

- Fresh graph passes.
- Deliberately stale fixture or changed source triggers warning/failure.
- No physics claims are changed.

---

## P7-T04 — Surface graph summary in Continue Research context

**Recommendation integrated:** 7  
**Task type:** project-system routing support  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** project-system tooling/research-control role  
**Physics milestone:** none

### Objective

Add a compact dependency summary to Continue Research context so the Director can see active burden dependencies before routing.

### Required summary fields

- active task
- latest handoff
- active burden
- immediate upstream objects
- accepted scoped objects
- draft/control objects
- human-gated objects
- blocked downstream objects
- frozen negative routes
- next recommended route
- graph path or hash

### Acceptance criteria

- Continue Research context remains readable.
- Summary does not replace canonical source inspection.
- Output explicitly states graph is navigational support only.

---

# P8 — Integrated Rollout, Validation, and Continuation Handoff

P8 is not recommendation 8. It is the integration phase for recommendations 1 through 7 only.

## P8-T01 — Cross-phase consistency audit

**Recommendations integrated:** 1-7  
**Task type:** project-system audit  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** process-integrity / validator role  
**Physics milestone:** none

### Objective

Audit the implementation results of P1 through P7 for consistency.

### Required checks

- `current_frontier.md` synchronized.
- Active-state drift validator installed or intentionally deferred.
- Gate Chair authorization route preserved or consumed properly.
- Same-shape cycle guard installed or design artifact created.
- Matter-Coupling Bridge Target v1 route exists if Gate Chair outcome allowed it.
- Parameterized-family target and/or tasks are queued or completed.
- Mechanized checker is support-only.
- Payload-density metrics are separated from operational validation.
- Dependency graph is generated and support-only.
- No recommendation 8-10 tasks were implemented.

### Required output

- Cross-phase audit artifact.
- List of completed tasks.
- List of deferred tasks with reasons.
- List of blockers.
- Handoff to next active implementation task or research continuation.

### Acceptance criteria

- Audit identifies any plan deviations.
- Audit confirms no forbidden recommendation was implemented.
- Audit confirms no physics overclaim.

---

## P8-T02 — Final validation and checkpoint transaction

**Recommendations integrated:** 1-7  
**Task type:** project-system validation/checkpoint  
**Continue Research requirement:** one bounded `/continue-research` transaction or checkpoint-only flow if repository convention supports it  
**Suggested role:** validator/tooling role  
**Physics milestone:** none

### Objective

Run the full validation suite after implemented phases.

### Required commands

```zsh
.venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
.venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/project_control/classify_project_changes.py --json
.venv/bin/python scripts/project_control/collect_project_improvement_signals.py --validate-emitted
.venv/bin/python scripts/project_control/validate_documentation_impact.py
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
.venv/bin/python scripts/research_control/report_physics_progress_metrics.py
git diff --check
.venv/bin/python scripts/research_control/checkpoint_research_transaction.py
```

### Required output

- Validation receipt.
- Checkpoint result or explicit failure report.
- If failure occurs, route one bounded `/improve-project-system` or Continue Research repair task as appropriate.

### Acceptance criteria

- All validators pass.
- Checkpoint succeeds or failure is reported with exact repair path.
- No unrelated files are staged.
- Final handoff names next active research or implementation route.

---

## P8-T03 — Final continuation handoff for research agents

**Recommendations integrated:** 1-7  
**Task type:** handoff/control summary  
**Continue Research requirement:** one bounded `/continue-research` transaction  
**Suggested role:** research-ops handoff/documentation role  
**Physics milestone:** none unless active state requires a physics selector

### Objective

Create the final implementation handoff for local AI agents after recommendations 1 through 7 are integrated or explicitly queued.

### Required handoff content

- active task
- latest handoff
- current burden
- current next action
- implemented recommendation list
- deferred recommendation list
- exact blocker list
- exact human-gate status
- support-only tooling paths
- validator status
- graph path if generated
- metrics status if implemented
- next recommended `/continue-research` invocation

### Acceptance criteria

- Handoff is concise but complete.
- It points to authoritative files, not memory-only artifacts.
- It preserves all physics claim boundaries.
- It does not mention or implement excluded recommendations 8-10.

---

# 5. Branching Rules and Dependency Management

## 5.1 If the Gate Chair authorization is absent

If P2-T01 finds no exact tracked authorization:

1. Stop at human-gated state.
2. Do not create P2-T02.
3. Continue project-system phases P6 and P7 if the Director determines they are lawful and noninterfering.
4. P3 may only proceed if it does not require the missing Gate Chair verdict, or if it is framed as design-only future route planning with no physics state change.
5. Final response must state the exact authorization required.

## 5.2 If the Gate Chair accepts SEI candidate as scoped evidence/precondition

Route:

1. P2-T03 post-gate selector.
2. P3-T01 cycle guard if not already installed.
3. P3-T02 Matter-Coupling Bridge Target v1.
4. P3-T03 bridge candidate or obstruction.
5. P3-T04 audit.
6. P3-T05 stress.
7. P3-T06 selector.

## 5.3 If the Gate Chair rejects the SEI candidate

Route:

1. P2-T03 selector.
2. Record precise rejection basis.
3. Choose repair, obstruction, or freeze.
4. Do not proceed to Matter-Coupling Bridge Target v1 unless the rejection still leaves a narrower bridge route open.

## 5.4 If project-system validators fail during P1, P5, P6, or P7

Route:

1. Preserve working-tree evidence.
2. Do not checkpoint.
3. Create one bounded repair task through Continue Research or `/improve-project-system`, depending on the active blocker.
4. Repair only the validator/tooling/documentation issue.
5. Re-run validation.

## 5.5 If a physics task repeats a burden without new payload

Route:

1. Require `freeze_criteria_status`.
2. Require `route_cycle_control`.
3. Prefer a Candidate Constructor bridge attempt, Refuter obstruction, Selector decision, or human gate.
4. Do not route back to a generic Ontology Formalizer obligation packet.

---

# 6. Plan-Level Acceptance Checklist

The implementation of this plan is complete when all applicable items are true:

## State-authority repair

- [ ] `current_frontier.md` matches `program_state.yaml`, latest handoff, and the ledger.
- [ ] A validator or generation command detects future drift.
- [ ] The active next action is unambiguous.

## Gate Chair route

- [ ] The exact human-gated authorization requirement is preserved.
- [ ] Gate Chair packet is executed only if authorization exists.
- [ ] Gate verdict is one of the allowed narrow outcomes.
- [ ] No matter coupling or downstream GR claim is adopted by the Gate Chair evidence-status review.

## Anti-orbit and bridge target

- [ ] Same-shape post-gate cycles require repair, obstruction, harder target, freeze, or gate.
- [ ] Matter-Coupling Bridge Target v1 is formalized or queued.
- [ ] A bridge candidate or precise obstruction is attempted when lawful.

## Parameterized family

- [ ] A parameterized source-family target is formalized or queued.
- [ ] It is more general than `F_E^sharp={S0,S1}`.
- [ ] It includes relabeling, variation, and sector-uniformity tests.

## Mechanization

- [ ] Finite/local checker design exists.
- [ ] Checker implementation exists or is queued.
- [ ] Checker reports are support-only and never proof authority.
- [ ] Tests cover bottom completeness and no-target-import at minimum.

## Payload-density metrics

- [ ] Payload-density and orbit-risk metrics are defined.
- [ ] Metrics are implemented or queued.
- [ ] Operational validation metrics remain separate from scientific progress metrics.
- [ ] Director sees warnings before repeated low-payload routing.

## Dependency graph

- [ ] Graph schema exists.
- [ ] Extractor exists or is queued.
- [ ] Graph includes accepted, draft/control, blocked, human-gated, and frozen objects.
- [ ] Graph is navigational support only.

## Exclusions

- [ ] No external-review packet was added under this plan.
- [ ] No separate exact-GR benchmark-hard-wall task was added under this plan.
- [ ] No separate adoption-hardening program was added under this plan.
- [ ] Existing claim-boundary rules are preserved, but recommendations 8-10 are not implemented.

---

# 7. Suggested Implementation Order

Recommended order if no human authorization is immediately available:

1. P0-T01
2. P0-T02
3. P1-T01
4. P1-T02
5. P1-T03
6. P1-T04
7. P6-T01
8. P6-T02
9. P6-T03
10. P7-T01
11. P7-T02
12. P7-T03
13. P5-T01
14. P5-T02
15. P5-T03
16. P2-T01, stopping human-gated if authorization is absent
17. P8-T01
18. P8-T02
19. P8-T03

Recommended order if exact human authorization is already present:

1. P0-T01
2. P0-T02
3. P1-T01
4. P1-T02
5. P1-T03
6. P2-T01
7. P2-T02
8. P2-T03
9. P3-T01
10. P3-T02
11. P3-T03
12. P3-T04
13. P3-T05
14. P3-T06
15. P4-T01
16. P4-T02
17. P4-T03
18. P4-T04
19. P4-T05
20. P5-T01
21. P5-T02
22. P5-T03
23. P5-T04
24. P5-T05
25. P6-T01
26. P6-T02
27. P6-T03
28. P6-T04
29. P7-T01
30. P7-T02
31. P7-T03
32. P7-T04
33. P8-T01
34. P8-T02
35. P8-T03

The Director may alter this order only when tracked state, validators, human gates, or latest handoff require it.

---

# 8. Non-Goals

This plan does not:

- derive GR
- derive Einstein equations
- derive or adopt universal matter coupling
- adopt a stress-energy tensor
- import a matter action
- adopt `MetricData(E)`
- change scoped `g_eff`
- promote the exact-GR benchmark
- close the benchmark Gate Chair
- claim completed derivation
- reject the global theory
- prove future source-extension impossibility
- implement excluded recommendations 8, 9, or 10

---

# 9. Final Instruction to Local AI Agents

Use Continue Research for every phase and every task. Treat this file as an implementation plan, not as authority over physics. The authoritative route remains the tracked state emitted by `continue_research.py`, `program_state.yaml`, the latest handoff, the registries, and validated task completions.

For each task:

1. Run memory preflight.
2. Resolve current state.
3. Let the Director create or reuse exactly one AgentJob.
4. Execute only the bounded task.
5. Write only authorized paths.
6. Preserve claim boundaries.
7. Record completion fields.
8. Bootstrap memory.
9. Validate.
10. Checkpoint only through the checkpoint script.
11. Handoff the next lawful route.

If this plan and tracked state conflict, tracked state wins. Record the conflict and route one bounded repair or selector task rather than improvising.
