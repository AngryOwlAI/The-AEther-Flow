<!-- authority: control -->

# Recommendations Implementation Plan Continue Task v19

```yaml
plan_id: "recommendations_implementation_plan_continue_task-v19"
plan_version: "v19"
created_at: "2026-07-12"
status: "draft_control_implementation_plan"
plan_filename: "recommendations_implementation_plan_continue_task-v19.md"
recommended_repo_path: "implementations_plans/recommendations_implementation_plan_continue_task-v19.md"
primary_subject: "verification_validation_testing_overhead_reduction"
implementation_track: "project_system_sidecar"
primary_controlling_skill: "improve-project-system"
final_handoff_skill: "continue-research"
intended_executor: "local AI agents operating through tracked project-control AgentJobs"
execution_mode: "exactly one bounded AgentJob per plan task"
source_audit: "verification_validation_testing_overhead_audit_2026-07-12.md"
audited_commit: "5ad2d856b5b7a689b76035e348734824cf7411f0"
current_research_task_basis: "RT-20260709-006"
current_research_handoff_basis: "handoff-0740"
preserved_ordinary_research_route: "EqSrc_family_closure_repair_or_stress"
project_system_sidecar_supersedes_research_handoff: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
source_law_adoption_authorized: false
benchmark_promotion_authorized: false
gate_chair_verdict_authorized: false
completed_derivation_authorized: false
```

## 0. Executive directive

This plan converts the complete recommendation set from the verification, validation, and testing overhead review into an implementation program that local AI agents can execute one bounded task at a time.

The central architectural directive is:

> Preserve the valuable invariants, but execute each deterministic validation gate at most once for one evidence identity. Replace repeated command chains with one path-aware validation plan, a cheap working-tree precheck, affected generation, and one authoritative final staged-tree acceptance pass.

The plan does not authorize deletion of scientific safeguards merely because they are expensive. It targets repeated setup, repeated full-corpus parsing, nested validator composition, same-state supersets, mis-scoped test execution, unbounded diagnostic output, independent orchestration owners, and local-only health checks that currently leak into universal acceptance paths.

V19 is a project-system sidecar. It must not displace the ordinary scientific continuation established by `research_control/handoffs/handoff-0740.yaml`. Unless a later tracked scientific decision lawfully changes that route, the project must return to one bounded `EqSrc_family_closure_repair_or_stress` packet after the v19 project-system work is complete.

## 1. Purpose

The purposes of v19 are to:

1. Reduce validation wall time, CI critical-path time, duplicate process execution, repeated repository parsing, filesystem copying, and agent-output exposure.
2. Preserve final staged transaction integrity, role and human-gate authority, write-path allowlists, changed-claim controls, source-authority boundaries, generated-surface freshness when applicable, and scientific checker coverage for changed artifacts.
3. Establish one declarative validation manifest and one deterministic planner and executor used by Make, GitHub Actions, checkpointing, and repo-local skills.
4. Introduce explicit validation profiles so ordinary edits no longer pay the full repository acceptance cost.
5. Refactor dominant integration tests without deleting their assertions.
6. Keep full machine-readable evidence available while making concise summaries the default interface for local AI agents.
7. Prove equivalence through adversarial fixtures, shadow execution, exact-tree receipts, and rollback drills before authoritative cutover.
8. Measure the result against frozen safety and performance budgets.
9. Restore the ordinary research route after the project-system sidecar closes.

## 2. Authority and non-authority boundary

This plan is project-control guidance. It is not a physics proof, theorem, countermodel, source-law adoption, ontology adoption, `MetricData(E)` adoption, `g_eff` scope expansion, detector or readout semantics adoption, coupling-law adoption, matter-coupling derivation, stress-energy semantics, Einstein-equation derivation, benchmark promotion, Gate Chair verdict, program-wide adverse verdict, future source-extension impossibility result, or completed derivation.

Validation success means that declared operational invariants were checked for a declared repository state. Repeating the same deterministic implementation against the same tree, scope, environment, and configuration does not create additional independent evidence.

The canonical identity for reusable deterministic evidence is:

```text
evidence_identity =
  gate_id
  + implementation_digest
  + environment_digest
  + configuration_digest
  + dependency_lock_digest
  + scope
  + base_reference
  + exact_tree_or_working_state_fingerprint
```

A result may be reused or may supersede another obligation only when the declared evidence-identity and semantic predicates match. Working-tree evidence never satisfies a different final staged-tree identity.

## 3. Current project-state basis

V19 starts from these tracked facts:

- `research_control/program_state.yaml` names `RT-20260709-006` and `handoff-0740`.
- `handoff-0740` records v18 recommendation coverage complete with no project-improvement signal.
- The next ordinary research action is one bounded `EqSrc_family_closure_repair_or_stress` packet.
- The current Distance-to-GR effect is `no_distance_delta`.
- V19 concerns project-system validation infrastructure and must preserve scientific route continuity.

## 4. Required source basis for every local agent

Before implementing a task, the agent must run the current memory preflight required by repository policy, use retrieval only for navigation, and directly inspect the canonical files relevant to its task.

### 4.1 Project authority and active state

```text
AGENTS.md
research_control/AGENTS.md
research_control/program_state.yaml
research_control/current_frontier.md
research_control/handoffs/handoff-0740.yaml
research_control/handoffs/handoff-0740.md
research_control/tasks/RT-20260709-006/
registries/AGENT_ROLE_REGISTRY.csv
registries/ROLE_EXECUTION_REGISTRY.csv
registries/DIRECTOR_DECISION_REGISTRY.csv
registries/AGENT_JOB_REGISTRY.csv
registries/RESEARCH_TASK_REGISTRY.csv
registries/CLAIM_BOUNDARY_REGISTRY.csv
```

### 4.2 Source audit and prior plan lineage

```text
verification_validation_testing_overhead_audit_2026-07-12.md
implementations_plans/recommendations_implementation_plan_continue_task-v18.md
research_control/design/validation_command_inventory_v16.md
research_control/design/v18_recommendation_backlog.yaml
research_control/design/v18_recommendation_backlog_schema.md
```

### 4.3 Current orchestration and validator sources

```text
Makefile
.github/workflows/project-control-validation.yml
scripts/research_control/run_full_research_control_validation.py
scripts/research_control/checkpoint_research_transaction.py
scripts/research_control/validate_research_control.py
scripts/research_control/continue_research.py
scripts/research_control/continue_research_memory_preflight.py
scripts/project_control/classify_project_changes.py
scripts/project_control/validate_claim_language.py
scripts/project_control/validate_documentation_impact.py
scripts/project_control/collect_project_improvement_signals.py
scripts/project_control/audit_documentation_surfaces.py
.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.codex/skills/project-memory-system/scripts/obsidian_wiki_lib.py
.codex/skills/project-memory-system/scripts/query_memory.py
scripts/validate_publication_process.py
scripts/spec_depth_lint.py
```

### 4.4 Current generated-surface, diagnostic, and test sources

```text
scripts/research_control/render_current_frontier.py
scripts/research_control/render_compact_current_frontier_v16.py
scripts/research_control/render_dependency_graph.py
scripts/research_control/render_task_index.py
scripts/research_control/generate_claim_graph_v1.py
scripts/research_control/validate_claim_graph_v1.py
scripts/research_control/extract_route_history.py
scripts/research_control/extract_route_signatures.py
scripts/research_control/validate_route_orbits.py
scripts/research_control/report_physics_progress_metrics.py
scripts/research_control/render_ai_methodology_metrics_dashboard.py
scripts/research_control/support_formalization/validate_traceability_registry.py
scripts/research_control/support_formalization/validate_traceability_registry_v18.py
tests/
```

### 4.5 Workflow contract sources

```text
.codex/skills/continue-research/SKILL.md
.codex/skills/improve-project-system/SKILL.md
.codex/skills/user-modified-project/SKILL.md
.codex/skills/project-memory-system/SKILL.md
CONTRIBUTING.md
research_control/README.md
scripts/project_control/README.md
scripts/research_control/README.md
tests/README.md
```

## 5. Audit baseline and problem statement

The source audit measured the following indicative baseline on an Apple M3 Ultra checkout:

| Measure | Audited value | Interpretation |
| --- | ---: | --- |
| Full `unittest` suite | 507.215 s | 584 tests passed; the test count itself is not the main problem. |
| Dependency-graph test module | 378.598 s | 74.6 percent of the suite, caused mainly by repeated full graph extraction. |
| Broad research-control module | 64.568 s | Valuable heterogeneous coverage mixed with repeated live full-corpus calls. |
| Memory-system module | 23.880 s | Small fixture tests mixed with live bootstrap and idempotence tests. |
| Remaining 46 modules | about 40.169 s | Most focused tests are already inexpensive. |
| GitHub project-control validation step | 1,025 s | Main CI critical path on the audited commit. |
| Measured gate-output exposure | about 53,203 proxy tokens | Dominated by verbose diagnostics, not by the quiet full test process. |

The audit also found:

- Plain research-control validation is immediately followed by a `--check-diff` mode that reruns the full spine.
- Checkpointing repeats overlapping working and staged command lists; some staged repetition is legitimate, same-scope direct duplication is not.
- The memory bootstrap already validates, then workflows often run validate-only immediately afterward.
- Memory core invokes publication validation internally, while aggregate targets invoke publication validation again.
- `--docs-only` and `--docs-validate-only` currently do not provide the scope their names imply.
- Seven graph tests perform approximately nine full graph constructions.
- Continuation behavior tests repeatedly invoke the full live research-control spine.
- Traceability negative tests copy the entire repository to mutate one field.
- Route-signature and task-index diagnostics can emit tens of thousands of characters.
- The classifier labels changes but does not produce a complete deduplicated gate plan.
- Make, CI, the local runner, skills, and checkpointing each own partially different command plans.
- Local retrieval health is useful but non-authoritative and should not be a universal checkpoint tax.

## 6. Complete v19 recommendation inventory
| ID | Recommendation | Primary implementation phases |
| --- | --- | --- |
| `V19-R01` | Replace independent repeated command chains with one deduplicated, path-aware validation directed acyclic graph. | P0, P1, P5, P6, P12 |
| `V19-R02` | Use a cheap working-tree precheck and one authoritative final staged-tree affected validation plan for governed transactions. | P0, P5, P6, P12 |
| `V19-R03` | Remove plain research-control validation immediately before the same-scope `--check-diff` superset. | P0, P1, P2, P5, P12 |
| `V19-R04` | Remove the standalone changed-claim invocation when the same-scope research-control diff gate already executes equivalent claim-language checks, after an equivalence proof. | P0, P1, P2, P5, P12 |
| `V19-R05` | Split memory synchronization from memory validation so generation and acceptance can be scheduled independently. | P0, P3, P6, P12 |
| `V19-R06` | Remove immediate `--validate-only` execution after a successful memory bootstrap that already performed the same validation. | P0, P3, P12 |
| `V19-R07` | Separate memory-core validation, publication validation, and local-retrieval health into distinct gates with distinct authority. | P0, P3, P12 |
| `V19-R08` | Implement genuinely scoped documentation-only memory modes or retire the misleading modes. | P0, P3, P12 |
| `V19-R09` | Remove nested publication-validator execution from memory-core validation and let the central planner own composition. | P0, P3, P12 |
| `V19-R10` | Move dependency installation and environment provisioning out of validation targets. | P0, P3, P12 |
| `V19-R11` | Replace skill-level full acceptance chains before checkpoint with cheap editing feedback and one checkpoint-owned authoritative acceptance pass. | P0, P2, P3, P6, P12 |
| `V19-R12` | Refactor checkpoint synchronization to run affected generators to stability, stage the result, and validate the final staged tree once per gate identity. | P0, P2, P3, P6, P12 |
| `V19-R13` | Reuse one live dependency-graph extraction across graph assertions. | P0, P7, P12 |
| `V19-R14` | Combine dependency-graph CLI write, fresh-check, mutation, and stale-check behavior into one bounded lifecycle test. | P0, P7, P12 |
| `V19-R15` | Use small synthetic repositories for dependency-graph determinism and retain only one scheduled live double-build test. | P0, P7, P12 |
| `V19-R16` | Add a narrow routing-snapshot validator for frequent Continue Research routing reads. | P0, P8, P12 |
| `V19-R17` | Generate and cache advisory route-orbit and payload-density diagnostics only when their source records change. | P0, P4, P8, P12 |
| `V19-R18` | Replace support-traceability tests that copy the entire repository with dependency injection and minimal fixture roots. | P0, P9, P12 |
| `V19-R19` | Retain the v1 support-traceability validator until explicit v18 coverage, migration, and historical-readability parity is proven. | P0, P9, P12 |
| `V19-R20` | Adopt a common compact validation-result schema with concise default output and complete receipts written to files. | P0, P2, P4, P6, P11, P12 |
| `V19-R21` | Bound task-index, route-signature, route-orbit, research-control, and memory command output by default. | P0, P4, P12 |
| `V19-R22` | Update local-agent workflows to consume summaries first and expand only the relevant failed finding group or receipt section. | P0, P4, P6, P11, P12 |
| `V19-R23` | Keep change classification fast and pure, then add a deterministic planner that maps classification tags to exact gates and test shards. | P0, P5, P12 |
| `V19-R24` | Create one declarative validation-gate manifest as the single source of operational orchestration truth. | P0, P1, P5, P6, P12 |
| `V19-R25` | Provide explicit `fast`, `affected`, `checkpoint`, `full`, and `doctor` validation profiles. | P0, P5, P6, P9, P11, P12 |
| `V19-R26` | Separate protected authority and transaction checks, derived-surface freshness, scientific artifact verification, and operational diagnostics. | P0, P1, P5, P8, P12 |
| `V19-R27` | Compile role and skill validator declarations into deduplicated obligations rather than independently repeated command strings. | P0, P1, P2, P5, P6, P12 |
| `V19-R28` | Add conservative exact-tree validation receipt caching keyed by tree, gate, implementation, environment, configuration, and dependency fingerprints. | P0, P10, P12 |
| `V19-R29` | Load an immutable repository snapshot once per validation process and share parsed registries and control records across gates. | P0, P3, P7, P10, P12 |
| `V19-R30` | Path-trigger documentation, publication, graph, index, PDF, Mermaid, memory, and scientific checkers according to declared inputs. | P0, P3, P5, P6, P7, P11, P12 |
| `V19-R31` | Remove route-signature extraction and route-orbit diagnostics from blocking and default validation paths while preserving them as advisory tools. | P0, P4, P5, P8, P11, P12 |
| `V19-R32` | Move Obsidian sync, lint, status, search smoke, and other local-retrieval checks to the `doctor` profile, affected memory work, or scheduled health checks. | P0, P3, P5, P8, P9, P12 |
| `V19-R33` | Remove the complete repository test suite from ordinary `validate-memory`; use a memory-focused shard and reserve the full suite for `full` validation. | P0, P3, P5, P9, P12 |
| `V19-R34` | Split the broad research-control test module into pure policy, active-state, checkpoint, continuation, metrics, and live-integration shards. | P0, P8, P12 |
| `V19-R35` | Build each immutable metrics report once per test class or validation run and reuse it across assertions. | P0, P8, P12 |
| `V19-R36` | Convert memory-system tests to miniature fixtures while retaining one live validate-only and one live idempotence acceptance test. | P0, P9, P12 |
| `V19-R37` | Convert Obsidian and SQLite tests to miniature fixture repositories while retaining one live acceptance path. | P0, P9, P12 |
| `V19-R38` | Make Make targets, GitHub Actions, repo-local skills, the local runner, and checkpointing thin wrappers around the central planner and executor. | P0, P2, P3, P5, P6, P11, P12 |
| `V19-R39` | Retire or rename the independent local `CI-equivalent` command-plan owner and replace it with a compatibility wrapper over the shared full profile. | P0, P2, P6, P11, P12 |
| `V19-R40` | After deduplication, shard CI by responsibility, apply safe path filters, and reuse memory evidence instead of unconditionally duplicating the job. | P0, P8, P9, P11, P12 |
| `V19-R41` | Run an unfiltered scheduled full validation as the backstop for path-mapping or planner mistakes. | P0, P7, P11, P12 |
| `V19-R42` | Deprecate the memory `--check` compatibility alias after all tracked references migrate to the canonical command. | P0, P3, P11, P12 |
| `V19-R43` | Instrument gate counts, parse counts, subprocess counts, durations, output bytes, cache behavior, and critical-path timing, then enforce performance budgets. | P0, P1, P2, P4, P6, P7, P10, P12 |
| `V19-R44` | Preserve non-negotiable role, human-gate, write-allowlist, changed-claim, staged-residue, whitespace, source-authority, and one-live-acceptance safeguards. | P0, P1, P6, P8, P10, P12 |
| `V19-R45` | Use shadow comparison and explicit rollback controls before switching authoritative orchestration from legacy command chains to the planner. | P0, P1, P2, P10, P11, P12 |
| `V19-R46` | Maintain a tested change-family matrix that maps representative paths to profiles, gates, generators, and test shards, failing closed for unknown governed paths. | P0, P5, P12 |
| `V19-R47` | Retain complete machine-readable evidence on disk while keeping local caches, receipts, generated summaries, and validation PASS results non-authoritative for physics. | P0, P1, P4, P6, P9, P10, P11, P12 |
| `V19-R48` | Meet and verify the proposed runtime, CI, duplicate-invocation, and agent-output reduction targets without weakening failure-mode coverage. | P0, P2, P7, P8, P10, P11, P12 |

## 7. Target architecture

### 7.1 One source of orchestration truth

The target system has one declarative gate manifest and one deterministic planning and execution stack:

```text
changed paths or explicit scope
  -> fast pure classifier
  -> stable change-family tags
  -> role, skill, profile, and checkpoint obligations
  -> declarative gate manifest
  -> deterministic plan expansion
  -> prerequisite and mutator ordering
  -> conditional supersedence and evidence-identity deduplication
  -> optional exact-tree cache lookup
  -> bounded executor
  -> compact aggregate receipt plus full child receipts
```

Make, GitHub Actions, checkpointing, and skills must not independently maintain command ordering after cutover. They become wrappers that request a profile and scope.

### 7.2 Five permanent profiles

| Profile | Intended use | Blocking content | Explicit exclusions |
| --- | --- | --- | --- |
| `fast` | Editing feedback | Classifier, path sanity, syntax/schema checks, changed claim-language, whitespace, affected fast tests | Full history, full suite, generation, local diagnostics |
| `affected` | Precheckpoint confidence | `fast` plus affected blocking validators, affected generated-surface checks, focused integration tests | Unrelated graph, publication, memory, scientific, or local checks |
| `checkpoint` | Authoritative governed transaction closure | Affected generation, stabilization, final staging, staged authority and diff checks, affected final validation, residue, whitespace | Unrelated full-suite and doctor work |
| `full` | Main integration, release, manual full, scheduled backstop | Every blocking gate and all test shards | No path filtering |
| `doctor` | Local operational health | Local retrieval, environment, optional sync, search smoke, route diagnostics, cache inspection | Cannot satisfy checkpoint or physics authority |

A temporary `shadow` modifier may run legacy and planner paths for comparison. It is a migration mechanism, not a sixth permanent profile.

### 7.3 Four epistemic classes

| Class | Examples | Default authority | Scheduling principle |
| --- | --- | --- | --- |
| Protected transaction integrity | Role, human gate, AgentJob allowlist, changed claims, staged residue, whitespace | Blocking | Always when applicable; final staged form remains mandatory |
| Derived-surface freshness | Memory registries, frontiers, graph, task index, publication, PDF, Mermaid | Blocking when inputs or outputs are affected | Path-triggered plus full scheduled backstop |
| Scientific artifact verification | Finite candidate, source cover, EqSrc orbit, detector collapse, target-import, traceability | Blocking for the changed artifact family | Packet-specific and affected |
| Operational diagnostics | Route orbit, payload density, Obsidian, SQLite search, environment health | Advisory or local-only | Doctor, affected maintenance, or scheduled trend review |

### 7.4 Planned repository additions

```text
research_control/design/
  validation_evidence_identity_policy_v1.md
  validation_gate_id_catalog_v1.md
  validation_supersedence_contracts_v1.yaml
  validation_run_receipt_schema_v1.md
  validation_gate_manifest_schema_v1.md
  validation_gate_manifest_v1.yaml
  validation_change_family_taxonomy_v1.md
  validation_obligation_catalog_v1.yaml
  validation_profile_policy_v1.md
  validation_change_matrix_v1.md
  validation_cache_contract_v1.md
  validation_orchestration_migration_and_rollback_policy_v1.md
  ci_validation_shard_policy_v1.md
  validation_deprecation_ledger_v1.md

scripts/validation/
  __init__.py
  models.py
  trace.py
  reporting.py
  snapshot.py
  plan.py
  profiles.py
  obligations.py
  deduplicate.py
  executor.py
  mutators.py
  staged.py
  aggregate.py
  cache.py
  doctor.py
  cli.py
  adapters/

tests/
  test_validation_manifest.py
  test_validation_planner.py
  test_validation_profiles.py
  test_validation_deduplication.py
  test_validation_executor.py
  test_validation_cache.py
  test_validation_change_matrix.py
  test_v19_validation_non_regression.py
  fixtures/validation_*/
```

This is a proposed layout. A task may choose a slightly different module boundary if it preserves one orchestration owner, stable gate IDs, manifest authority, and the acceptance criteria in this plan.

## 8. Global execution rules

### 8.1 One bounded task per AgentJob

Every plan task becomes exactly one bounded AgentJob. A local agent must not combine multiple task IDs merely because the changes appear adjacent. Batching requires a tracked superseding Director or Project-System Director decision that preserves every task's acceptance and rollback obligations.

### 8.2 Controlling workflow

- P0 through P12-T06 are project-system tasks controlled by `improve-project-system`.
- P12-T07 is the final route-restoration handoff and may use `continue-research` under Director of Research authority.
- The project-system sidecar must not edit canonical science TeX, adopt physics claims, or silently supersede the research handoff.
- Every task must create normal task-local control records, completion evidence, documentation impact, and handoff records required by repository policy.

### 8.3 Standard task-local records

Unless a task is explicitly read-only and current policy allows a read-only report, each state-changing task must create or update:

```text
research_control/tasks/<task-id>/00_TASK.yaml
research_control/tasks/<task-id>/DDR-<id>.md
research_control/tasks/<task-id>/jobs/AJ-<id>.yaml
research_control/tasks/<task-id>/roles/<role-ref>.yaml
research_control/tasks/<task-id>/jobs/completions/AJC-<id>.yaml
research_control/tasks/<task-id>/documentation_impact.yaml
research_control/handoffs/handoff-<next>.yaml
research_control/handoffs/handoff-<next>.md
applicable registry rows
applicable source and generated artifacts
```

### 8.4 Project-system completion fields

Every completion must include equivalent fields:

```yaml
implementation_plan_receipt:
  plan_id: "recommendations_implementation_plan_continue_task-v19"
  plan_path: "implementations_plans/recommendations_implementation_plan_continue_task-v19.md"
  plan_task_id: "P<phase>-T<task>"
  recommendation_ids: ["V19-Rnn"]
  migration_epoch: "legacy | legacy_consolidated | shadow_planner | planner_authoritative"

project_system_change_only: true
scientific_claims_changed: false
physics_promotion_authorized: false
proof_authority: false
distance_to_gr_delta:
  effect: "no_distance_delta"
  changed: false
  ledger_row_updated: false
new_mathematical_payload: []

validation_evidence:
  working_tree_fingerprint: string
  staged_tree_hash: string
  selected_gate_ids: [string]
  executed_gate_ids: [string]
  superseded_gate_ids: [string]
  duplicate_evidence_identity_count: integer
  aggregate_receipt_path: string
  aggregate_receipt_hash: string

performance_evidence:
  before_reference: string
  duration_seconds: number
  subprocess_count: integer
  output_bytes: integer
  cache_hits: integer
  cache_misses: integer

recommendation_coverage:
  implementation_status: "completed | blocked | deferred | superseded | conditionally_not_required"
  coverage_effect: "direct | validation | migration | measurement | documentation | audit"
```

### 8.5 Required forbidden-conclusion summary

Every v19 completion must state, directly or by a stable referenced policy:

```text
This v19 task changes project-system validation, testing, orchestration, caching,
diagnostics, or documentation only. It does not authorize canonical ontology
edit, source-law adoption, general EqSrc discharge, RetainH adoption, GenH
adoption, MetricData(E) adoption, g_eff scope expansion, detector or readout
semantics adoption, coupling-law adoption, matter-coupling derivation,
stress-energy semantics, stress-energy tensor, matter action,
Einstein-equation derivation, benchmark promotion, Gate Chair verdict,
external endorsement, future source-extension impossibility, program-wide
no-go conclusion, completed derivation, or any validator, test, cache, receipt,
registry, generated artifact, CI status, checkpoint, commit, or performance
measurement as physics proof.
```

### 8.6 Migration epochs

| Epoch | Authority | Permitted behavior | Exit requirement |
| --- | --- | --- | --- |
| `legacy` | Existing commands | Inventory, baseline, policy, fixtures | Evidence identity and rollback policy complete |
| `legacy_consolidated` | Existing implementations with direct duplicates removed | Same semantic gates, fewer same-state calls | Equivalence audit PASS |
| `shadow_planner` | Legacy result remains authoritative | Planner runs for comparison; compact output and refactors may operate | Zero unexplained hard mismatch across required corpus and scenarios |
| `planner_authoritative` | Manifest planner and executor | Shared profiles, checkpoint, CI, cache as authorized | Final non-regression and performance audits |
| `legacy_retired` | Planner only, compatibility artifacts retained where needed | Old independent command owners removed | Reference migration and deprecation audit PASS |

### 8.7 Validation during implementation

Until planner authority is cut over, implementation tasks must use the current legacy acceptance path plus the narrow focused tests for their change. During shadow mode, tasks must run legacy and planner comparison without treating planner PASS as authoritative. After cutover, tasks use `checkpoint` and `full` profiles as specified.

No task may reduce its own validation burden before the task that authorizes that migration has passed.

## 9. Gate manifest seed model

A manifest gate should support at least:

```yaml
gate:
  gate_id: string
  description: string
  owner_role: string
  adapter: string
  command_compatibility: list[string]
  input_globs: list[string]
  output_globs: list[string]
  scopes:
    - working
    - staged
    - repository
    - local_retrieval
  severity: "blocking | advisory | local_only"
  mutating: boolean
  cost_class: "fast | medium | slow"
  prerequisites: list[string]
  supersedes:
    - gate_id: string
      predicate_id: string
  satisfies_obligations: list[string]
  profiles: list[string]
  path_tags: list[string]
  timeout_seconds: integer
  parallel_group: string
  cache_policy: "ineligible | exact_tree | scheduled_bypass"
  receipt_schema: string
  test_shard: string
```

### 9.1 Seed gate catalog

| Gate ID | Primary purpose | Default profile placement | Cache |
| --- | --- | --- | --- |
| `classify_changes` | Stable path-family tags and policy implications | all state-changing profiles | exact-tree eligible after P10 |
| `git_diff_check` | Whitespace errors | fast, affected, checkpoint, full | not final-cached |
| `claim_language_changed` | Changed claim-bearing surfaces | fast, affected, checkpoint, full | exact-tree eligible |
| `research_control_core` | Complete tracked control spine | full, affected when control inputs change | exact-tree eligible |
| `research_control_diff` | Core plus path, authority, allowlist, changed claims | checkpoint, full | exact-tree eligible only before final residue; final diff may be uncached |
| `memory_sync` | Generate declared memory and registry derivatives | checkpoint when affected | ineligible |
| `memory_core` | Tracked memory and derivative invariants | affected, checkpoint, full | exact-tree eligible |
| `publication_validation` | Publication brief, spec, HTML, GitHub derivative policy | affected publication, full | exact-tree eligible |
| `local_retrieval_health` | Obsidian and SQLite health | doctor, scheduled, affected memory | local-only |
| `documentation_impact` | Update or no-op receipt requirement | affected project-system, checkpoint, full | exact-tree eligible |
| `project_improvement_signals` | Signal and sidecar parity | affected signal paths, checkpoint, full | exact-tree eligible |
| `documentation_surface_audit` | Registered documentation integrity | affected docs, full | exact-tree eligible |
| `spec_depth` | Explainer source depth | affected spec, full | exact-tree eligible |
| `mermaid_sources` | Source and static SVG safety | affected Mermaid, full | exact-tree eligible |
| `current_frontier_freshness` | Current frontier parity | affected state, full | exact-tree eligible |
| `compact_frontier_freshness` | Compact state parity | affected state, full | exact-tree eligible |
| `dependency_graph_freshness` | Graph outputs and referential integrity | affected graph, full | exact-tree eligible |
| `task_index_freshness` | Task index parity and warnings | affected tasks, full | exact-tree eligible |
| `claim_graph_validation` | Claim graph guards | affected claim graph, full | exact-tree eligible |
| `targeted_pdf_build` | Required PDF derivative | checkpoint when TeX requires | ineligible |
| `proof_normal_form` | PNF registry | affected PNF, full | exact-tree eligible |
| `support_traceability_v1` | v1 support mapping | affected v1, full if retained | exact-tree eligible |
| `support_traceability_v18` | v18 and PNF mapping | affected v18, full | exact-tree eligible |
| `scientific_checker:<family>` | Packet-specific scientific support | affected family, full shard | exact-tree eligible |
| `route_signature_diagnostic` | Advisory normalized route history | doctor, scheduled | exact-tree eligible |
| `route_orbit_diagnostic` | Advisory repeated-route warning | doctor, scheduled | exact-tree eligible |
| `test_shard:<name>` | Focused tests | affected or full | exact-tree eligible if deterministic |
| `final_staged_residue` | No unstaged transaction residue | checkpoint | ineligible |
| `final_index_integrity` | Staged tree and rollback integrity | checkpoint | ineligible |

The final manifest may refine names, but every semantic gate must remain stable enough for receipts, caches, obligations, and migration evidence.

## 10. Supersedence safety rules

The first supported supersedence rules are:

1. `research_control_diff` may satisfy `research_control_core` only on the same implementation, configuration, scope, base ref, and exact tree identity.
2. `research_control_diff` may satisfy `claim_language_changed` only when the integrated and standalone linter use the same path set, taxonomy, reviewed-context policy, and severity mapping.
3. A compatibility memory bootstrap may report that it performed sync and validation, but internal planner operations must represent sync and validation as separate gates. The mutator itself never supersedes validation.
4. A full profile may include an affected profile's gates, but profile names do not by themselves prove gate equivalence.
5. Working-tree results never supersede staged-tree results.
6. Pre-generation results never supersede post-generation results.
7. A cache hit is reuse of the same evidence identity, not independent verification.
8. Human review, final residue, index restoration, and mutators are never deduplicated through ordinary cache rules.
9. Unknown equivalence remains non-deduplicable.

## 11. Checkpoint target algorithm

The planner-based checkpoint must preserve the current index-restoration and allowlist safety model while reducing duplicate validation:

```text
1. Resolve the selected AgentJob and execution role.
2. Snapshot the entry Git index.
3. Inspect working paths and reject unrelated pre-existing changes.
4. Run the cheap working-tree precheck.
5. Stage allowed initial transaction paths.
6. Select affected mutators from the manifest.
7. Run memory and other generators to a bounded fixed point.
8. If a changed registered TeX source requires a PDF, build only that PDF.
9. Rerun affected synchronization needed after the PDF.
10. Restage allowed generated outputs.
11. Compute the exact final staged tree hash.
12. Build the `checkpoint` plan for the staged tree.
13. Execute fast staged blockers first.
14. Execute remaining affected staged blocking gates once per evidence identity.
15. Verify final allowlist, final staged residue, whitespace, and index integrity.
16. Write one aggregate receipt with child receipt hashes.
17. Commit only if every blocking gate passes.
18. Restore the entry index on any helper exception or blocked transaction.
19. Never push unless explicitly requested.
```

## 12. Output and receipt policy

### 12.1 Console budgets

| Result | Default output |
| --- | --- |
| PASS | One line or a compact structured summary, at most 2 KiB |
| FAIL | Summary, counts, first ten actionable findings, receipt path, at most 8 KiB |
| WARN | Grouped warning IDs and counts, representative examples only |
| CACHE_HIT | Gate ID, original receipt hash, exact tree, saved duration estimate |
| Full detail | Written to a requested or automatic receipt file, not injected by default |

### 12.2 Full receipt location

```text
.local/validation-receipts/<tree-or-working-fingerprint>/<run-id>/
```

This directory is ignored, local, non-authoritative, and disposable. A task may promote a compact hashed receipt into its task artifact directory when durable audit evidence is required.

### 12.3 Agent consumption

Agents must:

1. Read the compact summary.
2. On failure, inspect only the relevant finding group or bounded receipt section.
3. Avoid repeated polling that retransmits unchanged output.
4. Record gate IDs, status, counts, receipt path, and hash in completions.
5. Never treat output volume or PASS count as scientific progress.

## 13. Exact-tree cache contract

The initial conservative key is:

```text
sha256(
  gate_id
  + scope
  + exact_tree_hash
  + base_ref
  + implementation_digest
  + manifest_digest
  + configuration_digest
  + Python_version
  + dependency_lock_digest
  + environment_fingerprint
  + receipt_schema_version
)
```

Eligible results are deterministic read-only gates with complete declared inputs. Mutators, human review, final residue, final index integrity, and scheduled nondeterminism tests are ineligible.

A cache mismatch is a miss. A corrupt entry is a blocking cache-configuration finding followed by uncached execution when safe. Cache disablement must never change correctness.

## 14. CI target topology

The target CI topology is:

| Job | Responsibility |
| --- | --- |
| `validation-plan` | Manifest validation, change classification, affected plan, plan artifact |
| `policy-fast` | Pure policy, schemas, claims, classifier, planner, reporting |
| `research-control-integration` | One live full control acceptance and affected integration tests |
| `dependency-graph` | One live graph lifecycle and affected freshness |
| `memory-core` | Memory core and live memory acceptance when affected |
| `publication` | Spec, publication, Mermaid, HTML and documentation checks |
| `scientific-support` | Packet-specific mechanized checkers and traceability |
| `local-retrieval` | Path-triggered or scheduled Obsidian and SQLite health |
| `orchestration-equivalence` | Shadow or migration-only legacy versus planner comparison |
| `scheduled-full` | Unfiltered union, live determinism, doctor health, cache-bypass audit |

Deduplication comes before sharding. Parallel execution must not reproduce the same expensive gate in multiple jobs.

## 15. Decommission and retention policy

| Surface | Target action | Required proof before action |
| --- | --- | --- |
| Plain research-control immediately before same-scope diff | Remove invocation | P1 equivalence corpus |
| Standalone changed claim immediately before integrated diff | Remove invocation | Exact path and taxonomy equivalence |
| Immediate validate-only after successful bootstrap | Remove invocation | Final post-generation validation preserved |
| Publication subprocess inside memory core | Remove nesting | Full profile still selects publication |
| `pip install` inside validation target | Remove | Explicit setup path works |
| Route diagnostics in default blocking path | Remove from default | Doctor and explicit commands retained |
| Obsidian and search smoke in universal validation | Move to doctor or affected memory | Local-only authority preserved |
| Full suite in ordinary `validate-memory` | Remove | Memory-focused and full profiles retained |
| Independent local CI command plan | Convert to wrapper, later retire | Shared full profile parity |
| Misleading docs modes | Implement true scope or retire | Scope proof |
| Memory `--check` alias | Deprecate, later remove | Tracked reference migration |
| Traceability v1 | Retain unless parity audit authorizes retirement | Entry, failure, and historical parity |
| Final staged allowlist, claim, residue, whitespace, index checks | Retain | Non-negotiable |
| One live memory, graph, research-control, and local-retrieval acceptance | Retain | Non-negotiable |
| Scheduled unfiltered full validation | Retain | Non-negotiable |

## 16. Phase order and dependency rule

```yaml
phase_order:
  - P0: "V19 intake, registration, baseline, and success-budget freeze"
  - P1: "Validation semantics, gate identity, equivalence corpus, and rollback foundation"
  - P2: "Immediate direct-superset consolidation"
  - P3: "Memory, publication, local-retrieval, and environment decomposition"
  - P4: "Compact receipts and bounded agent-facing output"
  - P5: "Declarative manifest, classifier tags, planner, profiles, and change matrix"
  - P6: "DAG executor, staged-tree checkpoint integration, and orchestration wrappers"
  - P7: "Dependency-graph implementation and test-suite optimization"
  - P8: "Research-control routing, test decomposition, and advisory-metrics optimization"
  - P9: "Traceability, memory, and Obsidian fixture minimization"
  - P10: "Shared immutable repository snapshot and exact-tree cache"
  - P11: "CI rollout, compatibility retirement, and operator documentation"
  - P12: "Performance validation, failure-mode audit, recommendation coverage, and research-route restoration"
```

Unless a tracked superseding decision says otherwise, phases execute in order. Within a phase, the explicit `depends_on` field controls task order. A task may begin only when all dependencies are completed or formally superseded.

## 17. Standard task implementation protocol

For every task:

1. Read its declared source files and current repository state.
2. Confirm the active role and task-local execution overlay.
3. Confirm the allowed write paths are no broader than the listed planned modifications plus standard task-local records and generated derivatives.
4. Run the current required memory preflight and inspect canonical sources behind relevant memory hits.
5. Execute only the task objective.
6. Add or update focused regression tests before changing orchestration authority.
7. Run task-local validations.
8. During shadow mode, compare legacy and planner normalized results.
9. Capture compact receipts and hash full evidence.
10. Run final checkpoint acceptance appropriate to the migration epoch.
11. Write a completion that records recommendation coverage, performance evidence, no physics delta, and next task.
12. Emit a project-improvement signal only for a concrete unresolved system issue.

## 18. Detailed phased implementation tasks

---

## P0. V19 intake, registration, baseline, and success-budget freeze

### P0 objective

Complete 5 bounded tasks covering `V19-R01`, `V19-R02`, `V19-R03`, `V19-R04`, `V19-R05`, `V19-R06`, `V19-R07`, `V19-R08`, `V19-R09`, `V19-R10`, `V19-R11`, `V19-R12`, `V19-R13`, `V19-R14`, `V19-R15`, `V19-R16`, `V19-R17`, `V19-R18`, `V19-R19`, `V19-R20`, `V19-R21`, `V19-R22`, `V19-R23`, `V19-R24`, `V19-R25`, `V19-R26`, `V19-R27`, `V19-R28`, `V19-R29`, `V19-R30`, `V19-R31`, `V19-R32`, `V19-R33`, `V19-R34`, `V19-R35`, `V19-R36`, `V19-R37`, `V19-R38`, `V19-R39`, `V19-R40`, `V19-R41`, `V19-R42`, `V19-R43`, `V19-R44`, `V19-R45`, `V19-R46`, `V19-R47`, `V19-R48`. This phase creates evidence and policy only and must not prematurely switch orchestration authority.

### P0-T01: Register the v19 validation-overhead implementation plan

```yaml
plan_task_id: "P0-T01"
phase_id: "P0"
task_type: "v19_plan_registration"
title: "Register the v19 validation-overhead implementation plan"
recommendation_ids:
  - "V19-R01"
  - "V19-R02"
  - "V19-R03"
  - "V19-R04"
  - "V19-R05"
  - "V19-R06"
  - "V19-R07"
  - "V19-R08"
  - "V19-R09"
  - "V19-R10"
  - "V19-R11"
  - "V19-R12"
  - "V19-R13"
  - "V19-R14"
  - "V19-R15"
  - "V19-R16"
  - "V19-R17"
  - "V19-R18"
  - "V19-R19"
  - "V19-R20"
  - "V19-R21"
  - "V19-R22"
  - "V19-R23"
  - "V19-R24"
  - "V19-R25"
  - "V19-R26"
  - "V19-R27"
  - "V19-R28"
  - "V19-R29"
  - "V19-R30"
  - "V19-R31"
  - "V19-R32"
  - "V19-R33"
  - "V19-R34"
  - "V19-R35"
  - "V19-R36"
  - "V19-R37"
  - "V19-R38"
  - "V19-R39"
  - "V19-R40"
  - "V19-R41"
  - "V19-R42"
  - "V19-R43"
  - "V19-R44"
  - "V19-R45"
  - "V19-R46"
  - "V19-R47"
  - "V19-R48"
role_family: "project-system-director@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  []
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Add this plan as a tracked project-control implementation plan while explicitly preserving the v18 ordinary research handoff as the scientific continuation authority.

#### Preconditions and dependency evidence

- This is the first plan task and depends only on current project authority and user authorization.
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `AGENTS.md`
- `research_control/AGENTS.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-0740.yaml`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `implementations_plans/recommendations_implementation_plan_continue_task-v18.md`

#### Planned write scope

- `implementations_plans/recommendations_implementation_plan_continue_task-v19.md`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Verify the filename, plan ID, version, authority marker, and recommended repository path.
2. Register a new `MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V19` source row with `role=implementation_plan`, `authority_status=project_control`, and `audience=agents`.
3. Record `MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V18` and the supplied 2026-07-12 audit as source basis without treating either as physics authority.
4. Generate only the normal memory and wiki derivatives authorized for a registered Markdown source.
5. State in the completion and handoff that v19 is a project-system sidecar and does not supersede `handoff-0740` or its `EqSrc_family_closure_repair_or_stress` route.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_plan_registration_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run the current legacy registration and memory checks required before the planner exists.
- Validate the Markdown source row, generated wiki note, documentation impact receipt, and research-control state.
- Run `git diff --check` and confirm no canonical physics source changed.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- The plan is tracked at the requested path and has one registered source row.
- The completion lists all V19-R01 through V19-R48 recommendation IDs.
- The current research route remains `EqSrc_family_closure_repair_or_stress`.
- No Distance-to-GR, physics-claim, proof-authority, benchmark, or Gate Chair status changes.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if registration would require editing canonical science TeX or changing the current research handoff.
- If generated derivatives drift, repair through the existing memory bootstrap before checkpointing.
- Rollback by removing only the new plan row and generated derivatives if registration validation fails.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P0-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P0-T02: Materialize the v19 recommendation backlog and dependency graph

```yaml
plan_task_id: "P0-T02"
phase_id: "P0"
task_type: "v19_backlog_materialization"
title: "Materialize the v19 recommendation backlog and dependency graph"
recommendation_ids:
  - "V19-R01"
  - "V19-R02"
  - "V19-R03"
  - "V19-R04"
  - "V19-R05"
  - "V19-R06"
  - "V19-R07"
  - "V19-R08"
  - "V19-R09"
  - "V19-R10"
  - "V19-R11"
  - "V19-R12"
  - "V19-R13"
  - "V19-R14"
  - "V19-R15"
  - "V19-R16"
  - "V19-R17"
  - "V19-R18"
  - "V19-R19"
  - "V19-R20"
  - "V19-R21"
  - "V19-R22"
  - "V19-R23"
  - "V19-R24"
  - "V19-R25"
  - "V19-R26"
  - "V19-R27"
  - "V19-R28"
  - "V19-R29"
  - "V19-R30"
  - "V19-R31"
  - "V19-R32"
  - "V19-R33"
  - "V19-R34"
  - "V19-R35"
  - "V19-R36"
  - "V19-R37"
  - "V19-R38"
  - "V19-R39"
  - "V19-R40"
  - "V19-R41"
  - "V19-R42"
  - "V19-R43"
  - "V19-R44"
  - "V19-R45"
  - "V19-R46"
  - "V19-R47"
  - "V19-R48"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P0-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Create a machine-readable backlog containing every v19 task, recommendation mapping, dependency, role, file boundary, migration epoch, validator obligation, and next-route rule.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P0-T01`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `implementations_plans/recommendations_implementation_plan_continue_task-v19.md`
- `research_control/design/v18_recommendation_backlog.yaml`
- `research_control/design/v18_recommendation_backlog_schema.md`
- `registries/AGENT_ROLE_REGISTRY.csv`

#### Planned write scope

- `research_control/design/v19_validation_overhead_backlog.yaml`
- `research_control/design/v19_validation_overhead_backlog_schema.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define backlog fields for plan task ID, phase, title, recommendation IDs, dependencies, role family, migration epoch, expected source changes, expected generated changes, required gates, performance evidence, rollback trigger, and next task.
2. Materialize every P0 through P12 task exactly once.
3. Reject duplicate task IDs, dangling dependencies, cycles, empty recommendation mappings, unregistered role references, and tasks that lack rollback criteria.
4. Record conditional tasks explicitly instead of silently omitting them.
5. Generate a deterministic dependency-order summary for local agents.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_backlog_validation_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Add a focused backlog schema validator or fixture test.
- Validate the graph is acyclic and all tasks are reachable from P0-T01.
- Validate every recommendation appears in at least one direct implementation task and P12 coverage audit.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Backlog and schema are tracked and registered if required by project policy.
- The generated dependency graph has no cycle and no orphan task.
- All V19-R01 through V19-R48 IDs have planned coverage.
- Every task declares one primary role and one migration epoch.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a task requires a role or authority not present in the active registry; route a bounded role-overlay decision instead.
- Do not invent implementation completion evidence during backlog creation.
- Rollback only backlog and schema changes if the validator cannot prove parity with the Markdown plan.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P0-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P0-T03: Capture a reproducible v19 baseline benchmark receipt

```yaml
plan_task_id: "P0-T03"
phase_id: "P0"
task_type: "v19_baseline_benchmark"
title: "Capture a reproducible v19 baseline benchmark receipt"
recommendation_ids:
  - "V19-R43"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P0-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Record a clean, reproducible pre-change baseline for runtime, invocation counts, output exposure, CI evidence, and known stale or local-only conditions.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P0-T02`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `verification_validation_testing_overhead_audit_2026-07-12.md`
- `Makefile`
- `.github/workflows/project-control-validation.yml`
- `scripts/research_control/run_full_research_control_validation.py`
- `scripts/research_control/checkpoint_research_transaction.py`
- `tests/`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Record repository commit, dirty status, machine, Python version, dependency-lock hashes, date, timezone, and warm or cold cache state.
2. Preserve the audit figures as historical baseline: 507.215-second full suite, 378.598-second graph module, 64.568-second research-control module, 23.880-second memory module, and 1,025-second CI validation step.
3. Run at least one current clean baseline pass if repository state permits, storing stdout and stderr in `.local/v19-baseline/` rather than model context.
4. Count concrete gate invocations, full research-control spine invocations, dependency-graph builds, registry parses, subprocesses, output bytes, warnings, and token proxy.
5. Classify dependency-graph, task-index, and local-vault failures as pre-existing baseline, repaired baseline, or no longer present.
6. Never repair unrelated baseline drift inside this measurement task.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_baseline_benchmark.json`
- `research_control/tasks/<task-id>/artifacts/v19_baseline_benchmark.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate the benchmark receipt schema and hash every retained raw log.
- Check that no tracked file changed during measurement.
- Repeat any sub-second measurement at least three times and report median; label single expensive runs as indicative.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- A baseline JSON and human-readable summary exist under the task artifact directory.
- Every value states measurement method and uncertainty.
- Known baseline failures are separated from v19 regressions.
- No benchmark result is represented as physics evidence.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if the working tree is dirty in unrelated paths.
- Do not run mutating bootstrap or checkpoint commands merely to obtain timing.
- If current hardware differs materially from the audit hardware, retain both baselines and do not compare them as controlled measurements.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P0-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P0-T04: Build the legacy validation invocation and obligation graph

```yaml
plan_task_id: "P0-T04"
phase_id: "P0"
task_type: "legacy_validation_invocation_graph"
title: "Build the legacy validation invocation and obligation graph"
recommendation_ids:
  - "V19-R01"
  - "V19-R27"
  - "V19-R38"
  - "V19-R39"
  - "V19-R43"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P0-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Map every current validation obligation and every concrete command invocation across Make, CI, skills, roles, the local runner, checkpointing, and direct scripts.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P0-T03`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `Makefile`
- `.github/workflows/project-control-validation.yml`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `scripts/research_control/run_full_research_control_validation.py`
- `scripts/research_control/checkpoint_research_transaction.py`

#### Planned write scope

- `research_control/design/v19_legacy_validation_invocation_graph.md`
- `research_control/design/v19_legacy_validation_invocation_graph.json`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Assign stable provisional gate IDs to every distinct implementation and distinguish obligation labels from executable commands.
2. For each invocation, record owner, scope, tree state, mutating status, implementation, arguments, nested validators, expected cost, and whether another invocation is a same-state superset.
3. Represent role and skill declarations as obligations linked to satisfying gates rather than as independent evidence.
4. Mark direct duplicates, legitimate cross-scope repetitions, advisory diagnostics, local-only health checks, and conditional scientific validators.
5. Record current drift among Make, GitHub Actions, the local runner, and checkpoint command sets.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_legacy_validation_invocation_graph_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate every command in the audit and current repository has an invocation-graph node or an explicit out-of-scope explanation.
- Check no two provisional gate IDs refer to different implementations.
- Generate counts by owner, scope, severity, and duplicate class.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- The graph exposes all direct-superset duplication with evidence.
- Working-tree and staged-tree executions are never collapsed merely because command text matches.
- Nested publication and memory validation relationships are visible.
- The graph is suitable as seed input for the P5 manifest.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if the graph would classify a protected final staged check as redundant without scope evidence.
- Do not modify command behavior in this inventory task.
- If an invocation cannot be resolved, mark it `unresolved` and route a targeted inspection task.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P0-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P0-T05: Freeze v19 safety, runtime, CI, and output budgets

```yaml
plan_task_id: "P0-T05"
phase_id: "P0"
task_type: "v19_budget_freeze"
title: "Freeze v19 safety, runtime, CI, and output budgets"
recommendation_ids:
  - "V19-R43"
  - "V19-R44"
  - "V19-R47"
  - "V19-R48"
role_family: "project-system-director@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P0-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Define measurable v19 acceptance budgets and non-negotiable safeguards before any optimization changes behavior.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P0-T04`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/tasks/<P0-T03-task>/artifacts/v19_baseline_benchmark.json`
- `research_control/design/v19_legacy_validation_invocation_graph.json`
- `AGENTS.md`
- `research_control/AGENTS.md`

#### Planned write scope

- `research_control/design/v19_validation_performance_and_safety_budget.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define target and hard-guard thresholds separately so environment variance does not create false failures.
2. Set target full-suite runtime to 100-160 seconds and a hard guard of 180 seconds on comparable hardware.
3. Set target affected-loop runtime to 5-30 seconds and checkpoint target to 60-90 seconds for representative transactions.
4. Set target CI critical path to a few minutes, with a provisional hard guard of 8 minutes after rollout.
5. Set duplicate gate-identity count to zero per scope and tree unless a test explicitly exercises replay or nondeterminism.
6. Set default PASS output to at most 2 KiB and default FAIL summary to at most 8 KiB with no more than ten actionable findings.
7. List non-negotiable gates: final staged allowlist, role and human-gate authority, changed claims, residue, whitespace, source authority, one live acceptance per subsystem, and scheduled unfiltered full validation.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_budget_review_receipt.yaml`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate every budget has a measurement method, comparable-environment rule, and rollback threshold.
- Cross-check that no budget can be satisfied by deleting a unique invariant.
- Require baseline and post-change receipts for every performance claim.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- The budget document distinguishes target, hard guard, and advisory trend.
- All protected safeguards have explicit pass criteria.
- The document forbids treating timing or PASS counts as physics progress.
- Future tasks can reference stable budget IDs.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if proposed thresholds require suppressing failures, warnings, or source checks rather than reducing duplicate work.
- Do not make the budget blocking until baseline comparability is established.
- Rollback threshold changes through a project-system decision, never silently.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P1-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P1. Validation semantics, gate identity, equivalence corpus, and rollback foundation

### P1 objective

Complete 5 bounded tasks covering `V19-R01`, `V19-R03`, `V19-R04`, `V19-R24`, `V19-R26`, `V19-R27`, `V19-R43`, `V19-R44`, `V19-R45`, `V19-R47`. This phase creates evidence and policy only and must not prematurely switch orchestration authority.

### P1-T01: Define validation evidence identity and epistemic classes

```yaml
plan_task_id: "P1-T01"
phase_id: "P1"
task_type: "validation_evidence_identity_policy"
title: "Define validation evidence identity and epistemic classes"
recommendation_ids:
  - "V19-R01"
  - "V19-R26"
  - "V19-R44"
  - "V19-R47"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P0-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Define when two validation executions are independent evidence, duplicate evidence, or legitimate cross-state confirmation.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P0-T05`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/v19_legacy_validation_invocation_graph.md`
- `AGENTS.md`
- `research_control/AGENTS.md`
- `scripts/research_control/validate_research_control.py`

#### Planned write scope

- `research_control/design/validation_evidence_identity_policy_v1.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define `evidence_identity = gate_id + implementation_digest + environment_digest + config_digest + scope + tree_hash`.
2. State that repeated executions with the same evidence identity add no independent deterministic evidence unless a nondeterminism experiment is declared.
3. Define four classes: protected transaction integrity, derived-surface freshness, scientific artifact verification, and operational diagnostics.
4. Define blocking, advisory, local-only, mutating, human-review, and scheduled-only authority levels.
5. Specify that a working-tree PASS never satisfies a different staged-tree identity.
6. Specify that generated receipts, cache hits, CI statuses, and summaries are operational evidence only.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/validation_evidence_identity_examples.yaml`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Add policy fixture examples for same-state duplicate, post-generation legitimate rerun, independent implementation, environment change, and replay test.
- Review the policy against checkpoint staging and memory generation semantics.
- Run claim-language validation on the policy to prevent validator-as-proof overread.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Every current gate class can be assigned unambiguously.
- The policy explains why direct duplicates can be removed without weakening evidence.
- The policy preserves final staged and human-gated boundaries.
- No scientific authority is created.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if any proposed equivalence relies only on similar names rather than identical implementation and scope.
- Treat unresolved identity as non-deduplicable until proven.
- Rollback by leaving the legacy invocation graph authoritative during ambiguity.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P1-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P1-T02: Define canonical gate IDs and same-scope supersedence contracts

```yaml
plan_task_id: "P1-T02"
phase_id: "P1"
task_type: "gate_id_and_supersedence_contracts"
title: "Define canonical gate IDs and same-scope supersedence contracts"
recommendation_ids:
  - "V19-R03"
  - "V19-R04"
  - "V19-R24"
  - "V19-R27"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P1-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Assign stable gate IDs and machine-checkable supersedence conditions for the first consolidation wave.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P1-T01`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/validate_research_control.py`
- `scripts/project_control/validate_claim_language.py`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `scripts/validate_publication_process.py`
- `research_control/design/v19_legacy_validation_invocation_graph.json`

#### Planned write scope

- `research_control/design/validation_gate_id_catalog_v1.md`
- `research_control/design/validation_supersedence_contracts_v1.yaml`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define separate IDs for research-control core, research-control diff, changed-claim language, memory sync, memory core, publication, local retrieval, documentation impact, and advisory diagnostics.
2. Encode that `research_control_diff` may satisfy `research_control_core` only when implementation version, tree, base ref, staged flag, configuration, and scope match.
3. Encode that it may satisfy `changed_claim_language` only after P1-T03 proves identical path selection, taxonomy, context policy, severity, and configuration.
4. State explicitly that memory sync never supersedes validation and working scope never supersedes staged scope.
5. Assign stable obligation names that roles and skills can cite independently from command spelling.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/gate_id_catalog_validation.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Add schema tests for duplicate gate IDs and malformed supersedence predicates.
- Add negative fixtures showing why cross-scope or different-base-ref deduplication is forbidden.
- Verify every first-wave legacy command maps to exactly one gate ID.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Gate IDs are stable, unique, and implementation-specific.
- Supersedence is conditional and fail-closed.
- Role labels can be satisfied without repeating commands.
- The catalog is ready for the P5 manifest.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if changed-claim equivalence cannot be stated precisely.
- Do not enable deduplication solely from the catalog; activation waits for P1-T03 and P2.
- If an implementation has multiple modes with different semantics, assign different gate IDs.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P1-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P1-T03: Build the legacy-to-consolidated failure-mode equivalence corpus

```yaml
plan_task_id: "P1-T03"
phase_id: "P1"
task_type: "validation_equivalence_corpus"
title: "Build the legacy-to-consolidated failure-mode equivalence corpus"
recommendation_ids:
  - "V19-R03"
  - "V19-R04"
  - "V19-R44"
  - "V19-R45"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P1-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Create adversarial fixtures proving that planned same-scope consolidation preserves all legacy hard failures and warning classifications.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P1-T02`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_research_control.py`
- `tests/test_validate_claim_language.py`
- `tests/test_project_change_classifier.py`
- `scripts/research_control/validate_research_control.py`
- `scripts/project_control/validate_claim_language.py`

#### Planned write scope

- `tests/fixtures/validation_equivalence/`
- `tests/test_validation_equivalence.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Create fixtures for clean PASS, malformed registry, missing active AgentJob, disallowed path, overly broad allowlist, Markdown authority violation, public overclaim, reviewed historical warning, target import, stale sidecar, and unrelated path.
2. Run the legacy plain-plus-diff chain and the proposed single diff gate against each fixture.
3. Compare normalized status, hard finding IDs, warning finding IDs, selected paths, and authority fields rather than unstable prose order.
4. Run standalone changed-claim and integrated changed-claim logic against the same changed path sets.
5. Declare any difference as blocking unless explicitly reviewed as output-only normalization.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/legacy_consolidated_equivalence_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- The equivalence module must pass under the current legacy implementation before orchestration changes.
- Mutation tests must prove every fixture fails for its intended reason.
- Record coverage of all relevant claim-language taxonomy classes and diff boundary classes.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- No fixture produces legacy FAIL and consolidated PASS.
- No hard finding disappears.
- Allowed differences are limited to duplicate-free command count and compact rendering.
- An equivalence report is retained for P2 cutover.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop and keep both gates if any semantic mismatch remains.
- Do not weaken integrated changed-claim behavior to force parity.
- Rollback test fixtures only if they encode an invalid legacy assumption, with written rationale.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P1-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P1-T04: Instrument gate invocations, scopes, tree hashes, and nested calls

```yaml
plan_task_id: "P1-T04"
phase_id: "P1"
task_type: "validation_invocation_tracing"
title: "Instrument gate invocations, scopes, tree hashes, and nested calls"
recommendation_ids:
  - "V19-R01"
  - "V19-R43"
  - "V19-R45"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P1-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Add temporary or permanent instrumentation that makes duplicate work measurable before and after each migration step.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P1-T03`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `Makefile`
- `scripts/research_control/run_full_research_control_validation.py`
- `scripts/research_control/checkpoint_research_transaction.py`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`

#### Planned write scope

- `scripts/validation/trace.py`
- `tests/test_validation_trace.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define a lightweight trace event with gate ID, scope, tree hash, parent gate, start, end, status, output bytes, and cache state.
2. Write traces only under `.local/validation-traces/` unless a task explicitly promotes a compact receipt artifact.
3. Instrument nested validator launches so hidden publication and memory calls appear as child events.
4. Provide a context manager and subprocess wrapper usable before the full executor exists.
5. Ensure tracing can be disabled and does not change validator status or stdout by default.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/validation_trace_instrumentation_report.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test deterministic trace serialization with timestamps normalized for comparison.
- Test nested call parentage and duplicate identity detection.
- Measure instrumentation overhead and require it to remain below the v19 budget.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- A legacy full run produces a complete invocation trace.
- Duplicate same-identity executions are reported, not automatically removed.
- Tracing remains local, non-authoritative, and optional.
- P2 can measure exact invocation-count reduction.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if tracing changes exit codes, mutates tracked files, or leaks full validator output.
- Disable tracing through one environment switch if it causes instability.
- Do not use trace absence as evidence that a gate passed.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P1-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P1-T05: Create shadow-comparison and rollback control

```yaml
plan_task_id: "P1-T05"
phase_id: "P1"
task_type: "validation_migration_rollback_policy"
title: "Create shadow-comparison and rollback control"
recommendation_ids:
  - "V19-R45"
  - "V19-R44"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P1-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Define the migration epochs, comparison rules, feature switches, rollback triggers, and evidence required before any new planner path becomes authoritative.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P1-T04`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_evidence_identity_policy_v1.md`
- `research_control/design/validation_supersedence_contracts_v1.yaml`
- `research_control/tasks/<P1-T03-task>/artifacts/legacy_consolidated_equivalence_report.json`

#### Planned write scope

- `research_control/design/validation_orchestration_migration_and_rollback_policy_v1.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define epochs `legacy`, `legacy_consolidated`, `shadow_planner`, `planner_authoritative`, and `legacy_retired`.
2. Require legacy authority during shadow mode and fail closed on legacy FAIL or unexplained status mismatch.
3. Define feature switches for planner use, cache use, compact output, and legacy wrapper fallback.
4. Require at least three representative clean shadow runs and the full adversarial corpus before cutover.
5. Define rollback triggers for missing hard findings, wrong path selection, index restoration failure, cache cross-tree reuse, output loss, or performance regression above the hard guard.
6. Define how to restore legacy Make, CI, skill, and checkpoint behavior without rewriting scientific state.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_rollback_tabletop_report.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run a tabletop rollback exercise against one planned P2 change and one planned cache failure.
- Validate every destructive retirement task cites this policy.
- Ensure rollback artifacts do not become scientific or control authority beyond the migration decision.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Migration epochs and switches are explicit.
- Every future cutover has measurable entry and exit criteria.
- Rollback restores acceptance coverage, not merely old command text.
- No new path is authoritative without comparison evidence.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a change cannot be reversed without altering task history or canonical science.
- Do not delete legacy code before the `legacy_retired` epoch.
- If shadow comparison is too expensive, narrow its duration but never skip the adversarial corpus.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P2-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P2. Immediate direct-superset consolidation

### P2 objective

Complete 5 bounded tasks covering `V19-R03`, `V19-R04`, `V19-R11`, `V19-R12`, `V19-R20`, `V19-R27`, `V19-R38`, `V19-R39`, `V19-R43`, `V19-R45`, `V19-R48`. This phase may simplify direct duplication and interfaces while preserving legacy authority or shadow comparison.

### P2-T01: Consolidate the Makefile research-control core and diff pair

```yaml
plan_task_id: "P2-T01"
phase_id: "P2"
task_type: "make_research_control_superset_consolidation"
title: "Consolidate the Makefile research-control core and diff pair"
recommendation_ids:
  - "V19-R03"
  - "V19-R38"
  - "V19-R43"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P1-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Remove the plain research-control invocation that immediately precedes its same-state `--check-diff` superset in `validate-project-control`.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P1-T05`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `Makefile`
- `scripts/research_control/validate_research_control.py`
- `tests/test_run_full_research_control_validation.py`
- `tests/test_project_change_classifier.py`

#### Planned write scope

- `Makefile`
- `tests/test_validation_orchestration.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Replace the two-command pair with one `research_control_diff` invocation using the same Python, base ref, and working-tree scope.
2. Record in the orchestration receipt that the diff gate satisfies both core and diff obligations.
3. Do not alter final staged validation behavior in checkpointing in this task.
4. Add a command-plan test asserting one full research-control spine per Make invocation.
5. Capture before and after trace counts and wall time.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/make_superset_consolidation_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run the P1 equivalence corpus.
- Run focused Make plan/orchestration tests.
- Run `make validate-project-control` in captured-output mode if the baseline is clean enough.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Make executes one research-control full spine in this sequence.
- Pass/fail behavior matches legacy normalized results.
- The saved time is measured and reported.
- No unrelated gate is removed.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback the Makefile change if any hard finding disappears or the diff gate sees a different path set.
- Stop if the repository baseline is dirty in paths that change diff semantics.
- Do not use this task to path-filter the remaining Make commands.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P2-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P2-T02: Consolidate local-runner and checkpoint same-scope research-control pairs

```yaml
plan_task_id: "P2-T02"
phase_id: "P2"
task_type: "runner_checkpoint_superset_consolidation"
title: "Consolidate local-runner and checkpoint same-scope research-control pairs"
recommendation_ids:
  - "V19-R03"
  - "V19-R12"
  - "V19-R39"
  - "V19-R43"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P2-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Remove immediately repeated plain research-control execution from the local runner and checkpoint post-sync working scope while preserving the independent final staged boundary.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P2-T01`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/run_full_research_control_validation.py`
- `scripts/research_control/checkpoint_research_transaction.py`
- `tests/test_run_full_research_control_validation.py`
- `tests/test_research_control.py`

#### Planned write scope

- `scripts/research_control/run_full_research_control_validation.py`
- `scripts/research_control/checkpoint_research_transaction.py`
- `tests/test_validation_orchestration.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. In the local runner, retain the diff superset and update its coverage map to show core obligation satisfaction.
2. In checkpoint post-sync working-scope validation, remove the plain call only when no mutator or staging operation occurs between the pair.
3. Retain the later staged-only diff gate and final staged memory gate until P6 redesign proves a replacement.
4. Add a test asserting working and staged identities remain distinct.
5. Record command counts in checkpoint result metadata.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/runner_checkpoint_superset_consolidation_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run checkpoint ordering and index-restoration tests.
- Run local-runner plan tests and the equivalence corpus.
- Exercise a no-commit synthetic checkpoint fixture with working and staged scopes.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- No same-scope plain-plus-diff pair remains.
- Final staged allowlist, authority, claim, residue, and memory checks remain.
- Checkpoint rollback behavior is unchanged.
- Local runner reports its non-equivalence to CI until P11 centralization.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if index restoration, staged residue detection, or changed-path selection differs.
- Do not remove a second execution when generation or staging changed the tree.
- Stop if trace identity cannot prove the pair used the same tree.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P2-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P2-T03: Consolidate standalone changed-claim checks where the integrated diff gate is equivalent

```yaml
plan_task_id: "P2-T03"
phase_id: "P2"
task_type: "changed_claim_superset_consolidation"
title: "Consolidate standalone changed-claim checks where the integrated diff gate is equivalent"
recommendation_ids:
  - "V19-R04"
  - "V19-R20"
  - "V19-R27"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P2-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Remove standalone changed-claim invocations from command chains that immediately run an equivalent integrated research-control diff gate on the same path set.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P2-T02`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/project_control/validate_claim_language.py`
- `scripts/research_control/validate_research_control.py`
- `scripts/research_control/checkpoint_research_transaction.py`
- `scripts/research_control/run_full_research_control_validation.py`
- `Makefile`

#### Planned write scope

- `scripts/research_control/checkpoint_research_transaction.py`
- `scripts/research_control/run_full_research_control_validation.py`
- `tests/test_validation_equivalence.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Use the P1 supersedence predicate, not command-name matching.
2. Retain the standalone changed-claim command as a fast editor-facing gate and for profiles that do not run research-control diff.
3. Record the standalone claim obligation as satisfied by the integrated diff result when equivalent.
4. Ensure output summaries still expose claim-language finding counts and IDs.
5. Add negative tests for different base refs, staged flags, taxonomies, or path filters.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/claim_gate_supersedence_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all claim-language taxonomy tests and the equivalence corpus.
- Run checkpoint claim-language orchestration tests.
- Compare normalized claim finding sets on public, control, historical, and safe fixtures.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- No eligible chain runs the same claim-language implementation twice.
- Fast profile retains direct changed-claim feedback.
- No hard claim finding or reviewed warning classification changes.
- Receipts show which gate satisfied the obligation.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if integrated path selection omits a standalone-selected file.
- Do not consolidate across working and staged scopes.
- Stop if taxonomy or reviewed-context configuration differs.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P2-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P2-T04: Update skill and role obligation wording after direct consolidation

```yaml
plan_task_id: "P2-T04"
phase_id: "P2"
task_type: "skill_obligation_wording_update"
title: "Update skill and role obligation wording after direct consolidation"
recommendation_ids:
  - "V19-R11"
  - "V19-R27"
  - "V19-R38"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P2-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Update project-control instructions so obligations remain explicit while commands are not independently repeated merely because multiple roles or skills name them.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P2-T03`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `AGENTS.md`
- `research_control/AGENTS.md`

#### Planned write scope

- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `research_control/design/validation_obligation_resolution_policy_v1.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Replace duplicate command recipes with named gate obligations and one current compatibility command where necessary.
2. State that the checkpoint owns final staged acceptance and precheckpoint commands are editing aids.
3. Preserve memory preflight and direct source inspection requirements that concern knowledge retrieval rather than acceptance duplication.
4. Do not change role permissions, physics authority, human-gate requirements, or one-AgentJob boundaries.
5. Document how `research_control_diff` satisfies core and claim obligations in same-scope conditions.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/skill_obligation_update_review.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run documentation-impact, claim-language, and research-control validators.
- Add tests that parse skill command blocks or obligation IDs to prevent reintroduction of direct duplicate pairs.
- Confirm active role registry semantics remain unchanged.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Skills state the same safety obligations with fewer repeated command strings.
- Final checkpoint acceptance remains mandatory.
- No scientific workflow is rerouted by this documentation task.
- Role default validator labels remain auditable.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if wording would imply optional final staged validation.
- Do not edit explanatory-only sections without the proper role overlay.
- Rollback skill text if documentation-impact or authority-marker tests fail.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P2-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P2-T05: Audit first-wave equivalence and measured savings

```yaml
plan_task_id: "P2-T05"
phase_id: "P2"
task_type: "first_wave_equivalence_audit"
title: "Audit first-wave equivalence and measured savings"
recommendation_ids:
  - "V19-R03"
  - "V19-R04"
  - "V19-R43"
  - "V19-R45"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P2-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Close the first consolidation wave only after proving failure-mode parity, invocation-count reduction, and rollback readiness.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P2-T04`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/tasks/<P1-T03-task>/artifacts/legacy_consolidated_equivalence_report.json`
- `research_control/tasks/<P2-T01-task>/artifacts/make_superset_consolidation_report.json`
- `research_control/tasks/<P2-T02-task>/artifacts/runner_checkpoint_superset_consolidation_report.json`
- `research_control/tasks/<P2-T03-task>/artifacts/claim_gate_supersedence_report.json`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Run clean and adversarial shadow comparisons.
2. Compare gate identities, hard findings, warnings, durations, subprocess counts, and output bytes.
3. Verify no final staged gate was removed.
4. Calculate observed savings against the audit estimates without claiming statistical certainty.
5. Issue PASS, REPAIR_REQUIRED, or ROLLBACK_REQUIRED.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_first_wave_equivalence_audit.md`
- `research_control/tasks/<task-id>/artifacts/v19_first_wave_equivalence_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run the focused orchestration, claim-language, checkpoint, and local-runner tests.
- Run one full suite and one applicable aggregate validation if baseline conditions permit.
- Validate rollback switches and legacy command references remain available.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- PASS requires zero missing hard findings and zero unexplained status mismatches.
- Duplicate gate count decreases as planned.
- Measured savings and environment details are recorded.
- The next migration epoch may proceed to memory decomposition.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Route repair or rollback if any safety mismatch exists.
- Do not accept performance improvement as compensation for coverage loss.
- Preserve raw logs outside agent context.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P3-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P3. Memory, publication, local-retrieval, and environment decomposition

### P3 objective

Complete 7 bounded tasks covering `V19-R05`, `V19-R06`, `V19-R07`, `V19-R08`, `V19-R09`, `V19-R10`, `V19-R11`, `V19-R12`, `V19-R29`, `V19-R30`, `V19-R32`, `V19-R33`, `V19-R38`, `V19-R42`. This phase may simplify direct duplication and interfaces while preserving legacy authority or shadow comparison.

### P3-T01: Extract a write-only memory synchronization operation

```yaml
plan_task_id: "P3-T01"
phase_id: "P3"
task_type: "memory_sync_extraction"
title: "Extract a write-only memory synchronization operation"
recommendation_ids:
  - "V19-R05"
  - "V19-R12"
  - "V19-R29"
role_family: "memory-system-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P2-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Refactor memory bootstrap internals so deterministic synchronization can run without implicitly launching the complete validation stack.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P2-T05`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `.codex/skills/project-memory-system/scripts/obsidian_wiki_lib.py`
- `tests/test_memory_system.py`
- `Makefile`

#### Planned write scope

- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `.codex/skills/project-memory-system/scripts/memory_operations.py`
- `tests/test_memory_operations.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Extract a callable `memory_sync()` that performs directory creation, source discovery, authored-row merge, PDF-row refresh, HTML-row generation, wiki generation, generated-registry writes, stale-file pruning, file-object generation, and folder-map generation.
2. Return a structured mutation receipt listing changed, unchanged, created, and pruned paths without automatically calling core or publication validation.
3. Preserve deterministic output ordering and idempotent write-if-changed behavior.
4. Keep the current bootstrap CLI as a compatibility wrapper during migration.
5. Ensure local retrieval generation is an explicit option rather than an unavoidable tracked-core side effect.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/memory_sync_refactor_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run miniature fixture tests for discovery, generation, pruning, and idempotence.
- Run the existing live bootstrap idempotence acceptance test once.
- Compare generated snapshots before and after refactor on an unchanged tree.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- `memory_sync()` can run independently and returns no validation PASS claim.
- Unchanged state produces no tracked diff.
- Compatibility bootstrap still behaves as documented during the migration epoch.
- All generated artifacts retain non-authoritative status.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if generated bytes, ordering, path ownership, or pruning behavior changes unexpectedly.
- Stop if synchronization requires silently overwriting authored judgment fields.
- Do not make local retrieval state tracked.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P3-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P3-T02: Extract memory-core validation as a pure read-only gate

```yaml
plan_task_id: "P3-T02"
phase_id: "P3"
task_type: "memory_core_validator_extraction"
title: "Extract memory-core validation as a pure read-only gate"
recommendation_ids:
  - "V19-R05"
  - "V19-R07"
  - "V19-R29"
role_family: "memory-system-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P3-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Create a pure memory-core validator that checks tracked source, registry, derivative, and generated-surface invariants without publication or local-retrieval subprocesses.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P3-T01`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `scripts/validate_publication_process.py`
- `.codex/skills/project-memory-system/scripts/obsidian_wiki_lib.py`

#### Planned write scope

- `.codex/skills/project-memory-system/scripts/memory_operations.py`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `tests/test_memory_operations.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Extract `memory_validate_core(snapshot=None)` from the current `validate_all()` core checks.
2. Include registry columns, duplicate IDs, paths, source hashes, TeX vocabulary, PDF registry, HTML source binding required for registry correctness, wiki registry, file-object registry, folder map, and tracked local noise.
3. Exclude publication editorial policy and local retrieval freshness from this gate.
4. Accept a preloaded immutable snapshot so P10 can eliminate repeated CSV parsing.
5. Return stable finding IDs and structured counts.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/memory_core_equivalence_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all existing core memory failure fixtures.
- Compare legacy `validate_all()` core finding sets with the extracted gate on a synthetic corpus.
- Run one live read-only acceptance test.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Core validation is side-effect free.
- Every former core hard failure remains represented.
- Publication and local-cache warnings are absent from this gate by design.
- The gate has a stable `memory_core` ID.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if a tracked-source or generated-surface invariant moves to advisory status.
- Stop if the extraction requires duplicated registry parsing that P10 cannot later share.
- Do not classify publication failures as memory-core failures merely for compatibility.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P3-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P3-T03: Separate publication and local-retrieval validation ownership

```yaml
plan_task_id: "P3-T03"
phase_id: "P3"
task_type: "memory_publication_retrieval_separation"
title: "Separate publication and local-retrieval validation ownership"
recommendation_ids:
  - "V19-R07"
  - "V19-R09"
  - "V19-R32"
role_family: "memory-system-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P3-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Create explicit publication and local-retrieval gates and remove their hidden execution from memory-core validation.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P3-T02`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `scripts/validate_publication_process.py`
- `.codex/skills/project-memory-system/scripts/query_memory.py`
- `.codex/skills/project-memory-system/scripts/lint_obsidian_vault.py`

#### Planned write scope

- `.codex/skills/project-memory-system/scripts/memory_operations.py`
- `scripts/validation/adapters/publication.py`
- `scripts/validation/adapters/local_retrieval.py`
- `tests/test_memory_operations.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define `publication_validation` as the sole gate invoking the active publication-process validator.
2. Define `local_retrieval_health` as local-only or advisory unless a memory-maintenance task explicitly requires it.
3. Remove `validate_publication_docs()` from memory-core execution while preserving a compatibility composition path for the legacy bootstrap wrapper.
4. Separate blocking tracked-core findings from local-cache-only warnings in receipts.
5. Document inputs and outputs for both gates for P5 path planning.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/memory_validation_ownership_report.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run publication fixture tests independently from memory tests.
- Run local-retrieval stale-cache fixtures and assert they cannot make tracked core invalid.
- Run compatibility bootstrap and compare overall legacy status on current state.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Memory core, publication, and local retrieval can be selected independently.
- No hidden validator subprocess remains in memory core.
- Local retrieval cannot promote or block tracked scientific authority.
- Legacy wrapper composition remains available until P11 retirement.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if publication failures disappear from the full compatibility profile.
- Stop if local retrieval health can modify tracked files during validation.
- Do not remove publication checks from publication-affecting transactions.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P3-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P3-T04: Implement true documentation-scoped memory modes or retire them

```yaml
plan_task_id: "P3-T04"
phase_id: "P3"
task_type: "true_docs_modes_or_retirement"
title: "Implement true documentation-scoped memory modes or retire them"
recommendation_ids:
  - "V19-R08"
  - "V19-R30"
  - "V19-R42"
role_family: "memory-system-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P3-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Resolve the mismatch between documentation-only CLI names and their current full-scope implementation.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P3-T03`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `.codex/skills/project-memory-system/SKILL.md`
- `Makefile`
- `CONTRIBUTING.md`
- `tests/test_memory_system.py`

#### Planned write scope

- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `.codex/skills/project-memory-system/SKILL.md`
- `tests/test_memory_cli_modes.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define exact documentation inputs: registered Markdown, publication briefs, HTML specs, GitHub-facing derivatives, HTML registry rows, wiki notes for those sources, and documentation-specific generated indexes.
2. Implement `--docs-only` as documentation synchronization only and `--docs-validate-only` as documentation-core plus publication validation only.
3. Prove the modes do not traverse unrelated TeX, physics PDF, scientific checker, or full control-history inputs.
4. If safe scoping cannot be proven, deprecate and remove both modes instead of preserving misleading names.
5. Add explicit mode summaries that report selected object counts and excluded families.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/docs_mode_scope_proof.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Create fixture repositories containing mixed Markdown, TeX, PDF, and local-retrieval sources.
- Assert documentation modes ignore unrelated corrupted TeX while full memory validation detects it.
- Assert documentation corruption is still detected.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Mode names match actual scope, or the modes are retired with a migration note.
- No hidden full validation occurs.
- The planner can select documentation-only memory work safely.
- All tracked documentation references use the canonical resulting commands.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop and choose retirement if object-family scoping creates false PASS risk.
- Do not leave deprecated modes undocumented.
- Rollback to full compatibility wrapper if a scoped mode misses a declared documentation invariant.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P3-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P3-T05: Remove bootstrap-then-validate duplication from workflows and checkpoint stabilization

```yaml
plan_task_id: "P3-T05"
phase_id: "P3"
task_type: "memory_bootstrap_validation_dedup"
title: "Remove bootstrap-then-validate duplication from workflows and checkpoint stabilization"
recommendation_ids:
  - "V19-R06"
  - "V19-R11"
  - "V19-R12"
role_family: "memory-system-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P3-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Stop immediately revalidating the same memory state after a successful bootstrap and use sync-only operations during bounded checkpoint convergence.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P3-T04`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `Makefile`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `scripts/research_control/checkpoint_research_transaction.py`

#### Planned write scope

- `Makefile`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `scripts/research_control/checkpoint_research_transaction.py`
- `tests/test_validation_orchestration.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Replace checkpoint convergence calls to the compatibility bootstrap with `memory_sync()`.
2. Run memory-core validation once after the generated paths stabilize and the final staged tree is known.
3. Remove skill instructions that call bootstrap and immediate validate-only consecutively.
4. Retain a direct validate-only command for read-only checks and failure diagnosis.
5. Record generator passes and final validator identity in checkpoint receipts.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/memory_workflow_dedup_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run checkpoint multi-pass stabilization, PDF build, rollback, and residue tests.
- Run a fixture where generation changes the tree and prove final validation uses the post-generation staged tree.
- Run a fixture where sync fails and confirm no commit occurs.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- No same-tree bootstrap-plus-validate pair remains in governed workflows.
- Final staged memory-core validation remains blocking when memory inputs changed.
- Sync passes remain bounded and index restoration remains exact.
- Command-count and duration reductions are measured.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if final staged memory drift can pass.
- Stop if synchronization mutates paths outside the job allowlist.
- Do not remove the second sync after a targeted PDF build when the PDF changes registered derivative inputs.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P3-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P3-T06: Refactor `validate-memory` into provisioning, sync, core, doctor, and test-shard targets

```yaml
plan_task_id: "P3-T06"
phase_id: "P3"
task_type: "memory_make_target_refactor"
title: "Refactor `validate-memory` into provisioning, sync, core, doctor, and test-shard targets"
recommendation_ids:
  - "V19-R10"
  - "V19-R32"
  - "V19-R33"
  - "V19-R38"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P3-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Replace the monolithic memory target with purpose-specific targets and remove the full repository suite from ordinary memory validation.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P3-T05`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `Makefile`
- `.codex/skills/project-memory-system/SKILL.md`
- `tests/README.md`
- `CONTRIBUTING.md`

#### Planned write scope

- `Makefile`
- `.codex/skills/project-memory-system/SKILL.md`
- `tests/README.md`
- `CONTRIBUTING.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Add or standardize targets such as `setup-dev`, `memory-sync`, `memory-validate-core`, `memory-doctor`, `test-memory`, and `validate-memory-full`.
2. Make `validate-memory` a documented compatibility alias to the memory-focused affected profile during migration.
3. Remove `pip install`, full test discovery, Obsidian sync/lint, status, and search smoke from the ordinary core target.
4. Keep the full memory acceptance target for memory-tool changes and scheduled CI.
5. Ensure each target prints or writes a compact receipt.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/make_memory_target_matrix.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Add Make-plan tests verifying target command membership and exclusion.
- Run the memory-focused shard and one full compatibility acceptance.
- Verify ordinary core validation does not mutate `.local/` or tracked outputs.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Developers can choose setup, sync, core validation, doctor, and tests independently.
- Ordinary `validate-memory` no longer runs all repository tests.
- Full acceptance remains available and documented.
- No target silently provisions dependencies.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if a documented memory acceptance path disappears.
- Stop if target aliases create recursive Make invocation.
- Do not make doctor failures block core validation.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P3-T07` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P3-T07: Move environment provisioning out of all validation entry points

```yaml
plan_task_id: "P3-T07"
phase_id: "P3"
task_type: "validation_environment_separation"
title: "Move environment provisioning out of all validation entry points"
recommendation_ids:
  - "V19-R10"
  - "V19-R38"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy_consolidated"
depends_on:
  - "P3-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Ensure dependency installation is an explicit setup concern and no validation gate changes the environment it is evaluating.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P3-T06`
- The active implementation epoch must permit `legacy_consolidated` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `Makefile`
- `.github/workflows/project-control-validation.yml`
- `CONTRIBUTING.md`
- `requirements.txt`
- `requirements-dev.txt`

#### Planned write scope

- `Makefile`
- `CONTRIBUTING.md`
- `research_control/design/validation_environment_contract_v1.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define a supported Python and dependency-lock environment fingerprint.
2. Remove `pip install` from validation targets while retaining explicit setup targets and CI setup steps.
3. Make missing environment prerequisites fail quickly with a compact remediation message.
4. Record Python version and dependency hash in validation receipts.
5. Document that validators evaluate an environment and do not provision it.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/environment_provisioning_separation_report.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test missing `.venv` and missing dependency behavior.
- Test setup followed by validation in a clean fixture or CI job.
- Verify validation does not modify installed packages.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- No Make validation target runs package installation.
- CI still provisions before validation.
- Local error messages are actionable and concise.
- Environment fingerprint is available for cache keys.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback only the local target change if setup documentation is incomplete.
- Do not vendor or expose font or unrelated binary assets.
- Stop if requirements drift makes the environment fingerprint nondeterministic.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P4-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P4. Compact receipts and bounded agent-facing output

### P4 objective

Complete 6 bounded tasks covering `V19-R17`, `V19-R20`, `V19-R21`, `V19-R22`, `V19-R31`, `V19-R43`, `V19-R47`. This phase may simplify direct duplication and interfaces while preserving legacy authority or shadow comparison.

### P4-T01: Define common validation-run and gate-result receipt schemas

```yaml
plan_task_id: "P4-T01"
phase_id: "P4"
task_type: "validation_receipt_schema"
title: "Define common validation-run and gate-result receipt schemas"
recommendation_ids:
  - "V19-R20"
  - "V19-R22"
  - "V19-R43"
  - "V19-R47"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "legacy"
depends_on:
  - "P3-T07"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Create stable machine-readable schemas for compact run summaries, per-gate results, full receipts, and artifact references.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P3-T07`
- The active implementation epoch must permit `legacy` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/collect_validation_artifacts.py`
- `tests/test_collect_validation_artifacts.py`
- `research_control/design/validation_evidence_identity_policy_v1.md`

#### Planned write scope

- `research_control/design/validation_run_receipt_schema_v1.md`
- `research_control/design/validation_run_receipt_example_v1.json`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define run fields: schema ID, run ID, profile, scope, base ref, tree hash, planner version, manifest hash, environment fingerprint, selected and executed gate IDs, superseded gates, start/end, duration, status, and authority boundary.
2. Define gate fields: gate ID, severity, status, cache status, input and implementation fingerprints, duration, error and warning counts, shown findings, full receipt path, satisfied obligations, child gates, and mutated paths.
3. Define statuses `PASS`, `FAIL`, `WARN`, `SKIP_NOT_APPLICABLE`, `SKIP_SUPERSEDED`, `CACHE_HIT`, and `BLOCKED_CONFIGURATION`.
4. Prohibit raw unbounded stdout and stderr in top-level summary receipts.
5. Require full receipts to remain non-authoritative and local unless explicitly promoted as task evidence.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/validation_receipt_schema_review.yaml`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate example receipts and malformed fixtures.
- Test stable finding IDs and schema-version handling.
- Run claim-language checks against boundary statements.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Use the current authoritative legacy or legacy-consolidated acceptance path for this epoch.

#### Definition of done

- Schemas support legacy, shadow, and planner modes.
- Full evidence can be traced without entering agent context.
- Authority boundaries are explicit.
- P4 adapters can implement one shared format.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a schema field would falsely imply physics, proof, or promotion authority.
- Do not embed secrets, environment tokens, or full file content.
- Version the schema rather than silently changing required fields.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P4-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P4-T02: Implement the common compact reporter and bounded-output library

```yaml
plan_task_id: "P4-T02"
phase_id: "P4"
task_type: "common_compact_reporting"
title: "Implement the common compact reporter and bounded-output library"
recommendation_ids:
  - "V19-R20"
  - "V19-R21"
  - "V19-R47"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P4-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Provide one reusable library for concise console output, summary JSON, bounded findings, and full receipt files.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P4-T01`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/collect_validation_artifacts.py`
- `scripts/research_control/run_full_research_control_validation.py`
- `scripts/project_control/validate_claim_language.py`

#### Planned write scope

- `scripts/validation/reporting.py`
- `scripts/validation/models.py`
- `tests/test_validation_reporting.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Implement one-line PASS output and bounded FAIL/WARN rendering.
2. Group warnings by stable finding ID and show counts before details.
3. Show at most ten actionable findings by default with a clear `more_findings` count and receipt path.
4. Write full structured results atomically under `.local/validation-receipts/<tree-hash>/<run-id>/`.
5. Support `--summary`, `--json-summary`, `--full-json`, `--receipt`, and `--quiet` without changing exit semantics.
6. Measure console bytes and include them in the receipt.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/compact_reporter_acceptance.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test output budgets, Unicode handling, deterministic sorting, atomic writes, and error fallback.
- Test 0, 1, 10, 11, and 300-warning cases.
- Test that full receipts contain all findings while console output remains bounded.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- PASS is at most 2 KiB and default FAIL at most 8 KiB.
- Full evidence is preserved.
- Exit codes and finding counts remain unchanged.
- No receipt path is tracked by default.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if compact rendering hides the first actionable failure or corrupts full receipts.
- Stop if receipt writing failure changes a validator PASS into silent success; emit `BLOCKED_CONFIGURATION` instead.
- Do not truncate full receipt files.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P4-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P4-T03: Add compact task-index validation output

```yaml
plan_task_id: "P4-T03"
phase_id: "P4"
task_type: "task_index_compact_output"
title: "Add compact task-index validation output"
recommendation_ids:
  - "V19-R20"
  - "V19-R21"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P4-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Reduce task-index agent output from full historical warning dumps to actionable errors, warning groups, counts, and a receipt path.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P4-T02`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/validate_task_index.py`
- `scripts/research_control/render_task_index.py`
- `tests/test_task_index_renderer.py`

#### Planned write scope

- `scripts/research_control/validate_task_index.py`
- `tests/test_task_index_renderer.py`
- `tests/test_validation_reporting.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Adapt task-index findings to stable codes and the common reporter.
2. Show hard freshness and row-parity errors first.
3. Group historical metadata warnings by issue kind and include representative task IDs only.
4. Keep complete warning rows in the full receipt.
5. Preserve current JSON compatibility behind `--full-json` during migration.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/task_index_compact_output_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run fresh, stale CSV, stale Markdown, header mismatch, support-only physics delta, and 297-warning synthetic cases.
- Compare hard finding sets with the legacy report.
- Measure default output bytes.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- All legacy hard errors remain.
- Default output satisfies the budget.
- Full warning evidence remains retrievable.
- A small number of errors cannot be buried beneath warnings.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if any hard error is reordered after non-actionable warnings.
- Do not suppress warning counts.
- Stop if legacy automation depends on full JSON without an explicit compatibility flag.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P4-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P4-T04: Add compact route-signature and route-orbit diagnostic output

```yaml
plan_task_id: "P4-T04"
phase_id: "P4"
task_type: "route_diagnostic_compact_output"
title: "Add compact route-signature and route-orbit diagnostic output"
recommendation_ids:
  - "V19-R17"
  - "V19-R20"
  - "V19-R21"
  - "V19-R31"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P4-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Make advisory route diagnostics concise by default while retaining complete signatures in file receipts.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P4-T03`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/extract_route_signatures.py`
- `scripts/research_control/validate_route_orbits.py`
- `tests/test_route_signature_extractor.py`
- `tests/test_route_orbit_validator.py`

#### Planned write scope

- `scripts/research_control/extract_route_signatures.py`
- `scripts/research_control/validate_route_orbits.py`
- `tests/test_route_signature_extractor.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Default to counts, warning IDs, affected task IDs, and recommended guard action.
2. Move complete normalized route signatures to a requested output file or full receipt.
3. Preserve advisory-only flags, no route-freeze authority, and no physics promotion.
4. Add `--task-id` and bounded sample summaries without printing every signature.
5. Prepare adapters for P8 cached diagnostics.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/route_diagnostic_output_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run built-in sample and repeated-process-refresh fixtures.
- Verify the default output shrinks from tens of thousands of characters to the budget.
- Compare full receipt content with legacy JSON.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Diagnostic status and warning logic are unchanged.
- Default output is concise.
- Full signature evidence remains available.
- The diagnostic remains nonblocking by default.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if advisory status or warning thresholds change.
- Do not delete the full-report mode.
- Stop if a caller requires signatures in stdout and cannot migrate during compatibility period.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P4-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P4-T05: Adapt research-control, memory, and project-control gates to compact receipts

```yaml
plan_task_id: "P4-T05"
phase_id: "P4"
task_type: "core_validator_compact_receipts"
title: "Adapt research-control, memory, and project-control gates to compact receipts"
recommendation_ids:
  - "V19-R20"
  - "V19-R21"
  - "V19-R43"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P4-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Use the common reporter across high-frequency blocking validators without changing their semantic results.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P4-T04`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/validate_research_control.py`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `scripts/project_control/classify_project_changes.py`
- `scripts/project_control/validate_documentation_impact.py`
- `scripts/project_control/collect_project_improvement_signals.py`

#### Planned write scope

- `scripts/research_control/validate_research_control.py`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `scripts/project_control/classify_project_changes.py`
- `scripts/project_control/validate_documentation_impact.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Add stable gate and finding IDs without rewriting existing validation logic unnecessarily.
2. Return compact PASS and bounded FAIL summaries.
3. Write full receipts only when requested or through the central executor.
4. Preserve legacy human-readable modes behind explicit compatibility switches.
5. Record duration, output bytes, selected paths, and warning counts.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/core_validator_reporting_migration.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all focused validator tests and representative CLI tests.
- Compare exit codes and normalized finding sets with legacy output.
- Measure agent-facing bytes for clean and failed cases.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Blocking semantics remain identical.
- Successful outputs satisfy the v19 budget.
- Full evidence remains available.
- No validator PASS claims scientific authority.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback an adapter independently if it changes a finding set.
- Do not force one validator's warning taxonomy onto another.
- Stop if output compatibility breaks an active tracked workflow without migration support.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P4-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P4-T06: Update local-agent summary-first consumption and receipt-expansion rules

```yaml
plan_task_id: "P4-T06"
phase_id: "P4"
task_type: "agent_summary_first_policy"
title: "Update local-agent summary-first consumption and receipt-expansion rules"
recommendation_ids:
  - "V19-R22"
  - "V19-R47"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P4-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Teach local agents to ingest compact summaries, inspect only failed finding groups, and leave complete receipts on disk unless audit evidence is required.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P4-T05`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `AGENTS.md`
- `CONTRIBUTING.md`

#### Planned write scope

- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `research_control/design/agent_validation_output_consumption_policy_v1.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define summary-first command usage and bounded failure expansion.
2. Require agents to open only the relevant receipt section or bounded tail for diagnosis.
3. Prohibit repeated polling that retransmits unchanged output.
4. Require task completions to record receipt path, hash, status, counts, and relevant finding IDs rather than embedding full logs.
5. State that `.local/validation-receipts` is non-authoritative and untracked.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/agent_output_consumption_review.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run documentation-impact and claim-language validators.
- Add static tests for required summary-first wording and forbidden unbounded JSON examples.
- Review one sample completion receipt for compact evidence sufficiency.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Skills no longer instruct agents to ingest full PASS JSON.
- Failure diagnosis remains possible and auditable.
- Full logs are retained without consuming routine model context.
- No authority semantics change.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a compact completion cannot identify the failing gate and receipt.
- Do not delete historical full receipts.
- Rollback wording if it conflicts with current task receipt schemas before their migration.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P5-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P5. Declarative manifest, classifier tags, planner, profiles, and change matrix

### P5 objective

Complete 8 bounded tasks covering `V19-R01`, `V19-R02`, `V19-R03`, `V19-R04`, `V19-R23`, `V19-R24`, `V19-R25`, `V19-R26`, `V19-R27`, `V19-R30`, `V19-R31`, `V19-R32`, `V19-R33`, `V19-R38`, `V19-R46`. This phase operates in shadow mode until the explicit cutover task authorizes planner authority.

### P5-T01: Define the declarative validation-gate manifest schema

```yaml
plan_task_id: "P5-T01"
phase_id: "P5"
task_type: "validation_manifest_schema"
title: "Define the declarative validation-gate manifest schema"
recommendation_ids:
  - "V19-R24"
  - "V19-R26"
  - "V19-R27"
  - "V19-R30"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P4-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Create the schema that will become the single operational source for gate selection, ordering, authority, inputs, outputs, profiles, supersedence, caching, and tests.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P4-T06`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_gate_id_catalog_v1.md`
- `research_control/design/validation_evidence_identity_policy_v1.md`
- `research_control/design/validation_run_receipt_schema_v1.md`
- `research_control/design/v19_legacy_validation_invocation_graph.json`

#### Planned write scope

- `research_control/design/validation_gate_manifest_schema_v1.md`
- `research_control/design/validation_gate_manifest_v1.yaml`
- `tests/test_validation_manifest.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define required gate fields: ID, description, owner role, implementation adapter, input globs, output globs, scopes, severity, mutating flag, cost class, prerequisites, supersedes, satisfies obligations, profiles, path tags, timeout, parallel group, cache policy, receipt schema, and test shard.
2. Define explicit conditions for conditional PDF, Mermaid, publication, graph, task-index, traceability, and scientific checker selection.
3. Define profile membership independently from severity.
4. Require every blocking gate to name at least one regression test or full-profile acceptance path.
5. Reject broad globs such as `**` unless justified by an audited global invariant.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/validation_manifest_schema_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate good and malformed manifest fixtures.
- Test duplicate IDs, cycles, unknown prerequisites, invalid supersedence, unsupported scope, and missing test shard.
- Validate deterministic canonical serialization and manifest hashing.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- The schema can represent every node in the legacy invocation graph.
- Unknown or malformed gates fail closed.
- Gate authority and diagnostic status are explicit.
- The manifest can be hashed for receipts and cache keys.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if the schema encodes shell order only and cannot express semantic dependencies.
- Do not activate the manifest as authoritative in this task.
- Version incompatible schema changes explicitly.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P5-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P5-T02: Populate the initial canonical validation-gate manifest

```yaml
plan_task_id: "P5-T02"
phase_id: "P5"
task_type: "validation_manifest_population"
title: "Populate the initial canonical validation-gate manifest"
recommendation_ids:
  - "V19-R24"
  - "V19-R26"
  - "V19-R30"
  - "V19-R31"
  - "V19-R32"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P5-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Translate the current gate inventory into a complete first manifest without changing execution authority.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P5-T01`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/v19_legacy_validation_invocation_graph.json`
- `research_control/design/validation_gate_manifest_schema_v1.md`
- `Makefile`
- `.github/workflows/project-control-validation.yml`

#### Planned write scope

- `research_control/design/validation_gate_manifest_v1.yaml`
- `tests/fixtures/validation_manifest/`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Create entries for classifier, whitespace, changed claims, research-control core and diff, memory sync and core, documentation impact, signals, documentation audit, spec depth, publication, Mermaid, frontiers, dependency graph, task index, claim graph, proof-normal-form, metric-use TeX, traceability, scientific checkers, test shards, local retrieval, route diagnostics, and targeted PDF build.
2. Mark route diagnostics and local retrieval as advisory or local-only.
3. Mark final staged allowlist, authority, changed claims, residue, whitespace, and relevant memory freshness as blocking.
4. Declare current cost classes and provisional duration estimates from the audit.
5. Include legacy command adapters so shadow mode can execute current implementations.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/initial_manifest_coverage_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run manifest schema validation.
- Compare manifest gate coverage with every legacy invocation-graph node.
- Assert every current blocking command has a gate entry or a documented compatibility wrapper.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Manifest coverage is complete.
- No advisory diagnostic is accidentally blocking.
- No blocking invariant is absent.
- No actual execution path changes yet.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a current gate cannot be classified safely.
- Use `classification_pending` with blocking treatment rather than omitting it.
- Do not set cache eligibility before P10 rules exist.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P5-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P5-T03: Extend change classification with stable path-family tags

```yaml
plan_task_id: "P5-T03"
phase_id: "P5"
task_type: "classifier_path_family_tags"
title: "Extend change classification with stable path-family tags"
recommendation_ids:
  - "V19-R23"
  - "V19-R30"
  - "V19-R46"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P5-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Keep classification fast and pure while adding the stable tags needed by the planner to select affected gates and test shards.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P5-T02`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/project_control/classify_project_changes.py`
- `tests/test_project_change_classifier.py`
- `research_control/design/validation_gate_manifest_v1.yaml`

#### Planned write scope

- `scripts/project_control/classify_project_changes.py`
- `research_control/design/validation_change_family_taxonomy_v1.md`
- `tests/test_project_change_classifier.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define tags for control state, role or schema contract, validator code, memory code, registered Markdown, registered TeX, required PDF, publication spec, HTML, Mermaid, dependency graph input, task-index input, claim graph input, traceability, scientific checker, local retrieval, CI or orchestration, and unknown governed path.
2. Return tags, reasons, canonical paths, generated derivatives, and affected source object IDs.
3. Do not make the classifier launch validators or generators.
4. Keep current documentation-impact and recommended-role outputs for compatibility.
5. Fail closed or select `full` for an unknown governed path rather than returning no action.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/change_family_taxonomy_coverage.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Expand classifier tests for every taxonomy tag and mixed changes.
- Test renames, deletions, untracked files, staged-only mode, and generated-only edits.
- Test that `.local/` remains local-only and generated direct edits remain blocked.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Every representative change family receives deterministic tags.
- Classification remains sub-second on the audited repository.
- No validator subprocess is launched.
- Unknown governed paths cannot silently skip validation.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if current reason codes or documentation-impact behavior regress.
- Stop if path tagging requires reading every large artifact body.
- Do not use filename substrings alone when registry metadata is available.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P5-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P5-T04: Implement the deterministic affected-plan builder

```yaml
plan_task_id: "P5-T04"
phase_id: "P5"
task_type: "deterministic_validation_planner"
title: "Implement the deterministic affected-plan builder"
recommendation_ids:
  - "V19-R01"
  - "V19-R23"
  - "V19-R24"
  - "V19-R30"
  - "V19-R46"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P5-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Build a pure planner that converts classifier tags, requested profile, scope, role obligations, and manifest data into an ordered, deduplicated validation plan.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P5-T03`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_gate_manifest_v1.yaml`
- `scripts/project_control/classify_project_changes.py`
- `research_control/design/validation_change_family_taxonomy_v1.md`

#### Planned write scope

- `scripts/validation/plan.py`
- `scripts/validation/cli.py`
- `tests/test_validation_planner.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Accept explicit changed paths or Git-derived working/staged paths.
2. Select gates by profile, path tags, manifest inputs, and mandatory profile invariants.
3. Expand prerequisites, preserve mutator-before-validator ordering, and detect cycles.
4. Emit selected, superseded, skipped-not-applicable, and unknown-path entries with reasons.
5. Never execute commands in the planner.
6. Produce deterministic JSON and human-readable plan summaries.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/planner_scenario_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test every representative change scenario in the lean change matrix.
- Test mixed documentation and validator changes, generated-only edits, and unknown top-level paths.
- Test deterministic plan output independent of input path order.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- The planner selects the narrowest safe gate set.
- Every selected gate has a reason.
- No command executes during planning.
- Unknown governed paths select a fail-closed or full fallback.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if planner output depends on mutable global state beyond declared inputs.
- Do not allow a profile to remove mandatory final staged invariants.
- Rollback to legacy selection if plan comparison misses any legacy blocking gate.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P5-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P5-T05: Compile role and skill declarations into validation obligations

```yaml
plan_task_id: "P5-T05"
phase_id: "P5"
task_type: "role_skill_obligation_compiler"
title: "Compile role and skill declarations into validation obligations"
recommendation_ids:
  - "V19-R27"
  - "V19-R38"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P5-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Resolve role and skill validator labels into manifest obligations that the planner can satisfy once per evidence identity.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P5-T04`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `registries/AGENT_ROLE_REGISTRY.csv`
- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `research_control/design/validation_gate_manifest_v1.yaml`

#### Planned write scope

- `research_control/design/validation_obligation_catalog_v1.yaml`
- `scripts/validation/obligations.py`
- `tests/test_validation_obligations.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Assign stable obligation IDs to `validate_research_control`, `check_diff`, `claim_boundary_phrase_scan`, `bootstrap_memory_system`, `validate_documentation_impact`, publication validation, and test obligations.
2. Map each obligation to one or more acceptable satisfying gate IDs and conditions.
3. Resolve the strictest applicable obligation across the selected role, skill, task overlay, profile, and changed paths.
4. Record satisfied obligations in gate receipts.
5. Reject an obligation with no manifest mapping.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/obligation_resolution_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test all active role registry rows and the three main workflow skills.
- Test multiple declarations resolving to one gate.
- Test that a stronger staged diff obligation cannot be satisfied by a working-tree core gate.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Every active declaration resolves.
- Repeated labels do not create repeated executions.
- Receipts preserve auditability of who required each gate.
- Role authority remains unchanged.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if obligation compilation expands write permissions or role authority.
- Do not rewrite historical role records.
- Treat unmapped obligations as blocking configuration errors.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P5-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P5-T06: Implement conditional supersedence and evidence-identity deduplication

```yaml
plan_task_id: "P5-T06"
phase_id: "P5"
task_type: "validation_deduplication_engine"
title: "Implement conditional supersedence and evidence-identity deduplication"
recommendation_ids:
  - "V19-R01"
  - "V19-R03"
  - "V19-R04"
  - "V19-R27"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P5-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Apply manifest supersedence only when evidence identity and declared semantic conditions prove that one selected gate contains another.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P5-T05`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_supersedence_contracts_v1.yaml`
- `scripts/validation/plan.py`
- `scripts/validation/obligations.py`

#### Planned write scope

- `scripts/validation/deduplicate.py`
- `tests/test_validation_deduplication.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Canonicalize gate identity before deduplication.
2. Apply supersedence after prerequisite expansion and obligation resolution.
3. Record each skipped duplicate with the satisfying gate and predicate evidence.
4. Refuse cross-tree, cross-scope, cross-base-ref, cross-config, or cross-implementation deduplication.
5. Expose duplicate counts and residual repeated identities in plan output.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/deduplication_predicate_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run positive and negative supersedence fixtures from P1.
- Test working versus staged, pre-generation versus post-generation, and changed taxonomy cases.
- Test that a replay-test gate can deliberately bypass deduplication with an explicit reason.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Same-identity duplicate count is zero in planned normal runs.
- Legitimate cross-state repetitions remain.
- Every skipped gate has machine-readable justification.
- Equivalence corpus remains green.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop and retain both gates on any unresolved predicate.
- Do not deduplicate mutators.
- Rollback dedup activation independently through the migration feature switch.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P5-T07` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P5-T07: Define and implement the five validation profiles

```yaml
plan_task_id: "P5-T07"
phase_id: "P5"
task_type: "validation_profiles"
title: "Define and implement the five validation profiles"
recommendation_ids:
  - "V19-R02"
  - "V19-R25"
  - "V19-R26"
  - "V19-R31"
  - "V19-R32"
  - "V19-R33"
role_family: "project-system-director@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P5-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Create explicit profiles with clear authority, scope, cost, and default use rather than one universal validation chain.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P5-T06`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_gate_manifest_v1.yaml`
- `research_control/design/v19_validation_performance_and_safety_budget.md`
- `scripts/validation/plan.py`

#### Planned write scope

- `research_control/design/validation_profile_policy_v1.md`
- `scripts/validation/profiles.py`
- `tests/test_validation_profiles.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define `fast` for classifier, syntax, changed claims, whitespace, and affected unit tests.
2. Define `affected` for fast plus affected blocking validators and focused integration tests.
3. Define `checkpoint` for affected generation, final staging, staged authority checks, residue, and final affected acceptance.
4. Define `full` for every blocking gate and all test shards.
5. Define `doctor` for local retrieval, route diagnostics, environment health, and other non-authoritative operational diagnostics.
6. Prevent `doctor` from satisfying checkpoint obligations.
7. Define a temporary `shadow` modifier rather than a sixth permanent profile.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/profile_membership_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test profile membership and forbidden cross-profile satisfaction.
- Test representative path scenarios and empty-diff behavior.
- Verify `full` remains unfiltered and `checkpoint` retains mandatory staged safeguards.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Each profile has one documented purpose and command.
- Default local development is not full.
- Full and scheduled coverage remain.
- Operational diagnostics cannot block physics or repository authority unless an explicit maintenance task opts in.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if `affected` can omit an unknown governed path.
- Do not let profile selection override a human gate.
- Rollback defaults without deleting profile definitions if rollout fails.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P5-T08` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P5-T08: Create the lean change matrix, plan explanation, and fail-closed path tests

```yaml
plan_task_id: "P5-T08"
phase_id: "P5"
task_type: "validation_change_matrix"
title: "Create the lean change matrix, plan explanation, and fail-closed path tests"
recommendation_ids:
  - "V19-R30"
  - "V19-R46"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P5-T07"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Codify representative changes and the exact generators, gates, test shards, profiles, and explanations they must select.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P5-T07`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_change_family_taxonomy_v1.md`
- `research_control/design/validation_profile_policy_v1.md`
- `scripts/validation/plan.py`

#### Planned write scope

- `research_control/design/validation_change_matrix_v1.md`
- `tests/fixtures/validation_plans/`
- `tests/test_validation_change_matrix.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Cover pure Python validator, research-control YAML, registered Markdown, TeX with and without required PDF, HTML spec with Mermaid, memory code, dependency graph input or renderer, task-index input, scientific checker, local retrieval only, CI orchestration, deletion, rename, mixed change, and unknown governed path.
2. For each case, state selected profile, tags, generators, gates, test shards, expected skips, and reason strings.
3. Add `validation plan --explain` output that traces each gate to paths and obligations.
4. Test no silent `no_action` on governed unknown paths.
5. Require explicit no-gate classification for truly irrelevant files.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/change_matrix_validation_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run golden plan fixtures and deterministic serialization checks.
- Mutation-test the path map by removing one mapping and confirming fail-closed behavior.
- Compare planner-selected blocking gates with legacy shadow results.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Every matrix row is executable and tested.
- Unknown governed paths fail closed or select full.
- Plan explanations are concise enough for agents.
- The matrix becomes the acceptance basis for P11 path-filtered CI.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if path tags rely on stale generated registries without source fallback.
- Do not accept path filters that cannot be tested.
- Rollback a mapping independently if it creates false negatives.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P6-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P6. DAG executor, staged-tree checkpoint integration, and orchestration wrappers

### P6 objective

Complete 8 bounded tasks covering `V19-R01`, `V19-R02`, `V19-R05`, `V19-R11`, `V19-R12`, `V19-R20`, `V19-R22`, `V19-R24`, `V19-R25`, `V19-R27`, `V19-R30`, `V19-R38`, `V19-R39`, `V19-R43`, `V19-R44`, `V19-R47`. This phase operates in shadow mode until the explicit cutover task authorizes planner authority.

### P6-T01: Implement the read-only validation DAG executor

```yaml
plan_task_id: "P6-T01"
phase_id: "P6"
task_type: "read_only_validation_executor"
title: "Implement the read-only validation DAG executor"
recommendation_ids:
  - "V19-R01"
  - "V19-R20"
  - "V19-R24"
  - "V19-R38"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P5-T08"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Execute planned read-only gates with deterministic ordering, bounded concurrency, compact receipts, and exact status propagation.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P5-T08`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/validation/plan.py`
- `scripts/validation/reporting.py`
- `research_control/design/validation_gate_manifest_v1.yaml`

#### Planned write scope

- `scripts/validation/run.py`
- `scripts/validation/executor.py`
- `tests/test_validation_executor.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Load a validated plan and refuse unknown or mutated manifest entries.
2. Execute blocking fast gates before expensive gates so obvious failures prevent unnecessary work.
3. Run only read-only gates in safe parallel groups; preserve deterministic receipt ordering.
4. Capture stdout and stderr to full receipts rather than streaming unbounded output.
5. Propagate status, severity, duration, output bytes, child gates, and satisfied obligations.
6. Support cancellation while writing a valid partial receipt.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/read_only_executor_acceptance.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test success, hard failure, advisory failure, timeout, cancellation, child-process crash, and receipt-write failure.
- Test deterministic result ordering under parallel execution.
- Compare shadow execution with legacy gates on the equivalence corpus.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Executor status matches legacy normalized status.
- No read-only gate mutates tracked files.
- Console output remains bounded.
- Every gate result is attributable to a plan reason.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if concurrency changes file visibility or result semantics.
- Disable parallelism for a gate without proven independence.
- Rollback to serial shadow mode before disabling the planner entirely.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P6-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P6-T02: Implement mutator barriers and bounded synchronization stabilization

```yaml
plan_task_id: "P6-T02"
phase_id: "P6"
task_type: "mutator_barrier_executor"
title: "Implement mutator barriers and bounded synchronization stabilization"
recommendation_ids:
  - "V19-R02"
  - "V19-R05"
  - "V19-R12"
  - "V19-R30"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P6-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Extend execution planning so affected generators run before read-only validation and the generated path set converges under explicit barriers.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P6-T01`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/checkpoint_research_transaction.py`
- `.codex/skills/project-memory-system/scripts/memory_operations.py`
- `scripts/validation/executor.py`

#### Planned write scope

- `scripts/validation/mutators.py`
- `scripts/validation/executor.py`
- `tests/test_validation_mutator_barriers.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Classify memory sync, frontier rendering, graph and index generation, targeted PDF build, and other writers as mutators.
2. Run mutators serially or in proven non-overlapping groups before read-only gates.
3. Record before and after path sets and content hashes.
4. Bound stabilization passes and fail with a convergence finding rather than looping.
5. Replan after mutators only if declared outputs introduce new affected tags.
6. Never cache mutators.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/mutator_barrier_acceptance.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test one-pass, two-pass, non-converging, targeted PDF, and disallowed-output fixtures.
- Test that no read-only gate begins before the final mutator barrier.
- Test rollback metadata for a failed mutator.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Generated outputs converge within the configured bound.
- Mutated paths remain inside declared outputs and job allowlists.
- Read-only gates see the final generated state.
- No hidden nested generation remains.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop and restore the index if convergence fails.
- Do not broaden output allowlists to make an unexpected generator path pass.
- Rollback mutator integration independently through the legacy checkpoint switch.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P6-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P6-T03: Implement the cheap working-tree precheck

```yaml
plan_task_id: "P6-T03"
phase_id: "P6"
task_type: "working_tree_precheck"
title: "Implement the cheap working-tree precheck"
recommendation_ids:
  - "V19-R02"
  - "V19-R11"
  - "V19-R25"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P6-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Provide fast editing feedback before checkpoint without duplicating the final acceptance chain.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P6-T02`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/validation/profiles.py`
- `scripts/validation/run.py`
- `scripts/project_control/classify_project_changes.py`

#### Planned write scope

- `scripts/validation/precheck.py`
- `tests/test_validation_precheck.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Run classification, path-policy sanity, syntax or schema checks, changed claim-language checks, whitespace, and affected fast tests.
2. Do not run full research-control history, complete memory validation, full test suite, or local diagnostics unless directly affected.
3. Return an explicit statement that precheck is not checkpoint acceptance.
4. Allow agents to rerun only the failed fast gate after an edit.
5. Record the working-tree hash and prevent later staged acceptance from reusing it as a staged PASS.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/working_precheck_scenario_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test representative change matrix cases and empty diff.
- Test that a working precheck PASS cannot satisfy checkpoint final gates.
- Measure runtime against the affected-loop budget.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Common edits receive feedback in the target range.
- Precheck catches path, syntax, claim, and whitespace failures early.
- No final authority is implied.
- Full acceptance remains checkpoint-owned.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if precheck adds mutating generation.
- Do not make precheck mandatory for read-only user questions.
- Rollback default use while retaining the command if path mapping is incomplete.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P6-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P6-T04: Implement final staged-tree planning and acceptance

```yaml
plan_task_id: "P6-T04"
phase_id: "P6"
task_type: "final_staged_validation"
title: "Implement final staged-tree planning and acceptance"
recommendation_ids:
  - "V19-R02"
  - "V19-R12"
  - "V19-R44"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P6-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Compute the final staged tree identity after synchronization and execute one authoritative affected checkpoint plan against that exact tree.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P6-T03`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/checkpoint_research_transaction.py`
- `scripts/validation/plan.py`
- `scripts/validation/executor.py`

#### Planned write scope

- `scripts/validation/staged.py`
- `tests/test_staged_validation.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Snapshot and address the Git index through the existing rollback-safe mechanisms.
2. Compute the staged tree hash only after all allowed generated paths are staged.
3. Plan with `scope=staged`, `base_ref=HEAD`, and the active AgentJob allowlist.
4. Execute required staged authority, diff, memory, derivative, focused test, residue, and whitespace gates once per identity.
5. Record working and staged plans separately.
6. Refuse acceptance if unstaged transaction residue remains.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/staged_acceptance_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test staged-only additions, deletions, renames, mixed staged and unstaged changes, generated outputs, and unrelated residue.
- Test that stale working-tree cache entries cannot satisfy staged gates.
- Compare with legacy checkpoint outcomes on the equivalence corpus.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Acceptance binds to one exact staged tree hash.
- All final non-negotiable gates remain blocking.
- No same-identity staged gate repeats.
- Failed acceptance commits nothing.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if index restoration or staged path detection changes.
- Stop if final staged tree cannot be reproduced after a gate failure.
- Do not accept a plan with unresolved unknown paths.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P6-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P6-T05: Integrate the planner and executor into checkpointing

```yaml
plan_task_id: "P6-T05"
phase_id: "P6"
task_type: "checkpoint_planner_integration"
title: "Integrate the planner and executor into checkpointing"
recommendation_ids:
  - "V19-R02"
  - "V19-R11"
  - "V19-R12"
  - "V19-R38"
  - "V19-R44"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P6-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Replace checkpoint's repeated hardcoded validation lists with planner-owned synchronization and final staged acceptance while preserving exact rollback and commit semantics.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P6-T04`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/checkpoint_research_transaction.py`
- `tests/test_research_control.py`
- `tests/test_validation_executor.py`

#### Planned write scope

- `scripts/research_control/checkpoint_research_transaction.py`
- `tests/test_checkpoint_validation_planner.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Preserve entry and original index snapshots, allowed-path checks, bounded sync passes, targeted PDF logic, no-action behavior, deterministic commit message, and no automatic push.
2. Use cheap preflight only for obvious working-tree blockers.
3. Delegate affected generator selection and staged gate selection to the planner.
4. Write one aggregate transaction receipt and retain command-level child receipts.
5. Keep `--legacy-validation` and `--compare-validation` switches during shadow rollout.
6. Fail closed on old/new status mismatch.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/checkpoint_planner_integration_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all existing checkpoint tests plus planner-specific fixtures.
- Exercise no-action, no-commit, sync failure, PDF failure, disallowed path, residue, commit failure, and helper exception cases.
- Run shadow comparison on at least three representative real or synthetic transactions.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Checkpoint commits exactly the same valid transactions as legacy.
- No invalid legacy-rejected transaction is accepted.
- Index restoration remains byte-for-byte equivalent.
- Duplicate gate identities are eliminated.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Automatic rollback to legacy validation on unexplained mismatch is available before commit.
- Stop if planner receipt generation itself mutates the staged tree.
- Do not remove legacy checkpoint code until P11 cutover.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P6-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P6-T06: Convert repo-local skills to planner profile wrappers

```yaml
plan_task_id: "P6-T06"
phase_id: "P6"
task_type: "skill_profile_wrappers"
title: "Convert repo-local skills to planner profile wrappers"
recommendation_ids:
  - "V19-R11"
  - "V19-R22"
  - "V19-R25"
  - "V19-R38"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P6-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Replace long duplicated validation command recipes in the principal skills with concise profile invocations and receipt handling.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P6-T05`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`

#### Planned write scope

- `.codex/skills/continue-research/SKILL.md`
- `.codex/skills/improve-project-system/SKILL.md`
- `.codex/skills/user-modified-project/SKILL.md`
- `.codex/skills/project-memory-system/SKILL.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Use `fast` or `affected` for editing feedback and `checkpoint` for final state-changing acceptance.
2. Use `doctor` only for local retrieval or advisory diagnostics.
3. Keep memory preflight and canonical source inspection rules distinct from validation profiles.
4. Require agents to cite compact receipt IDs and failed finding groups.
5. Preserve one bounded AgentJob, role authority, human gates, and project-system/research separation.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/skill_profile_wrapper_audit.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run skill contract classification, documentation-impact, and research-control validators.
- Add static tests that no skill recreates the retired full command chain.
- Run plan-only examples for research, project-system, and user-modified flows.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Skills are thin wrappers over shared profiles.
- No command-plan drift remains among skills.
- Final staged checkpoint remains authoritative.
- Research route authority is unchanged.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a wrapper hides a required human gate or source inspection.
- Keep legacy examples in a migration note only until cutover.
- Rollback individual skill changes independently.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P6-T07` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P6-T07: Convert Make and the local full runner to planner wrappers

```yaml
plan_task_id: "P6-T07"
phase_id: "P6"
task_type: "make_and_runner_wrappers"
title: "Convert Make and the local full runner to planner wrappers"
recommendation_ids:
  - "V19-R38"
  - "V19-R39"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P6-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Make familiar local entry points call the same manifest-driven profiles instead of owning independent command lists.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P6-T06`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `Makefile`
- `scripts/research_control/run_full_research_control_validation.py`
- `tests/test_run_full_research_control_validation.py`

#### Planned write scope

- `Makefile`
- `scripts/research_control/run_full_research_control_validation.py`
- `tests/test_validation_wrappers.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Map `validate-project-control` to the appropriate full or affected compatibility profile during rollout.
2. Map new targets `validate-fast`, `validate-affected`, `validate-checkpoint-plan`, `validate-full`, and `validate-doctor` to the shared CLI.
3. Turn `run_full_research_control_validation.py` into a compatibility wrapper that delegates to `--profile full` and reports deprecation status.
4. Remove its independent command-plan and coverage-map ownership after parity.
5. Preserve familiar exit codes and optional output file behavior.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/local_wrapper_parity_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test wrapper arguments, exit propagation, plan selection, and deprecation messages.
- Compare wrapper full plan with manifest full plan.
- Run one full shadow execution through both entry points.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- There is one command-plan owner.
- Make and local runner produce the same full gate set.
- Compatibility remains for existing operators.
- The misleading CI-equivalent label is removed or qualified.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback wrapper defaults if shared CLI is not stable.
- Do not delete the local filename until tracked references migrate.
- Stop if wrappers silently drop legacy output artifacts required by tasks.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P6-T08` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P6-T08: Implement aggregate transaction receipts and obligation coverage reports

```yaml
plan_task_id: "P6-T08"
phase_id: "P6"
task_type: "aggregate_transaction_receipt"
title: "Implement aggregate transaction receipts and obligation coverage reports"
recommendation_ids:
  - "V19-R20"
  - "V19-R27"
  - "V19-R43"
  - "V19-R47"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P6-T07"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Produce one compact transaction receipt that proves selected paths, obligations, gate results, supersedence, performance, and final tree identity.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P6-T07`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_run_receipt_schema_v1.md`
- `scripts/validation/executor.py`
- `scripts/research_control/checkpoint_research_transaction.py`

#### Planned write scope

- `scripts/validation/aggregate.py`
- `tests/test_validation_aggregate_receipt.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Aggregate classifier tags, plan reasons, selected and skipped gates, satisfied obligations, generator changes, staged tree hash, timings, output bytes, cache status, and final residue status.
2. Include an obligation coverage table proving every role, skill, profile, and checkpoint requirement was satisfied.
3. Hash child receipts and raw logs without embedding them.
4. Render a compact console summary and complete JSON.
5. State operational-only and no-physics-authority boundaries.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/aggregate_receipt_acceptance.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test complete, partial, failed, cancelled, cache-hit, and rollback receipts.
- Validate no obligation can be marked satisfied by a skipped-not-applicable gate unless its condition is proven false.
- Test deterministic aggregation independent of execution completion order.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- One receipt explains the full transaction without full log ingestion.
- Every obligation has a satisfying gate or blocking error.
- Final tree and scope are explicit.
- Receipt remains non-authoritative for physics.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if aggregate status can disagree with a blocking child failure.
- Do not omit failed child receipt hashes.
- Rollback aggregation without changing gate execution if schema issues arise.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P7-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P7. Dependency-graph implementation and test-suite optimization

### P7 objective

Complete 6 bounded tasks covering `V19-R13`, `V19-R14`, `V19-R15`, `V19-R29`, `V19-R30`, `V19-R41`, `V19-R43`, `V19-R48`. This phase operates in shadow mode until the explicit cutover task authorizes planner authority.

### P7-T01: Refactor dependency-graph extraction for reusable snapshots

```yaml
plan_task_id: "P7-T01"
phase_id: "P7"
task_type: "dependency_graph_reusable_snapshot"
title: "Refactor dependency-graph extraction for reusable snapshots"
recommendation_ids:
  - "V19-R13"
  - "V19-R29"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P6-T08"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Separate dependency-graph source loading, graph construction, validation, and rendering so one immutable extraction can feed multiple assertions and formats.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P6-T08`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/render_dependency_graph.py`
- `tests/test_render_dependency_graph.py`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/AGENT_JOB_REGISTRY.csv`

#### Planned write scope

- `scripts/research_control/render_dependency_graph.py`
- `scripts/research_control/dependency_graph_model.py`
- `tests/fixtures/dependency_graph/`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Introduce an immutable graph input snapshot containing parsed registries, program state, completions, and handoffs.
2. Make `build_graph()` accept the snapshot and avoid rereading the repository for each render.
3. Keep graph validation pure and separate from file comparison.
4. Expose instrumentation counters for source loads, graph builds, and render calls.
5. Preserve source hashes, node and edge ordering, authority notices, route continuity, and output bytes.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/dependency_graph_refactor_equivalence.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run existing required-node, edge-integrity, authority, and rendering assertions.
- Compare old and new JSON, Markdown, and DOT bytes on the same snapshot.
- Test snapshot immutability and no file reads during repeated rendering.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- One snapshot produces identical graph content and all three formats.
- Source loading occurs once per graph build.
- No authority or frontier node disappears.
- The refactor is ready for shared test setup.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if serialized graph bytes change without a reviewed schema migration.
- Stop if snapshot construction hides unreadable-source warnings.
- Do not cache graph output across a different tree in this phase.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P7-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P7-T02: Reuse one live graph build across property assertions

```yaml
plan_task_id: "P7-T02"
phase_id: "P7"
task_type: "dependency_graph_shared_test_setup"
title: "Reuse one live graph build across property assertions"
recommendation_ids:
  - "V19-R13"
  - "V19-R48"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P7-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Change the live dependency-graph test class to build the repository graph once and reuse it across independent pure assertions.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P7-T01`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_render_dependency_graph.py`
- `scripts/research_control/dependency_graph_model.py`

#### Planned write scope

- `tests/test_render_dependency_graph.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Build one class-level immutable live graph and pre-render JSON, Markdown, and DOT once.
2. Run required frontier item, authority boundary, referential integrity, format-content, and freeze-summary assertions against shared objects.
3. Add counters asserting no property test triggers another live graph extraction.
4. Keep each assertion logically separate even though setup is shared.
5. Ensure failed assertions cannot mutate the shared graph.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/dependency_graph_shared_setup_timing.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run the module repeatedly and verify stable results.
- Run tests in shuffled method order if supported by a small custom harness.
- Compare failure messages for removed node, bad edge, and authority mutation fixtures.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Live graph build count for pure assertions is one.
- Every current property remains covered.
- Tests remain order-independent.
- Module runtime falls materially.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if shared mutable state makes test order affect outcomes.
- Use defensive copies for mutation tests.
- Do not merge distinct assertions merely to reduce test count.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P7-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P7-T03: Combine dependency-graph CLI fresh and stale behavior into one lifecycle test

```yaml
plan_task_id: "P7-T03"
phase_id: "P7"
task_type: "dependency_graph_cli_lifecycle"
title: "Combine dependency-graph CLI fresh and stale behavior into one lifecycle test"
recommendation_ids:
  - "V19-R14"
  - "V19-R48"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P7-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Replace repeated write and check setup with one end-to-end lifecycle that proves all declared formats, fresh acceptance, and stale rejection.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P7-T02`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_render_dependency_graph.py`
- `scripts/research_control/render_dependency_graph.py`

#### Planned write scope

- `tests/test_render_dependency_graph.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Render JSON, Markdown, and DOT once to a temporary directory.
2. Assert declared files exist and contain the authority boundary.
3. Run the check path against the fresh outputs without rebuilding more than the one check-required graph.
4. Mutate one output deterministically and rerun the check to prove stale failure.
5. Assert stale reporting identifies only the mutated output when appropriate.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/dependency_graph_cli_lifecycle_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Instrument graph build count across the lifecycle.
- Test missing output and stale output variants with small helper-level fixtures where possible.
- Preserve CLI exit-code coverage.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- One lifecycle covers write, format content, fresh PASS, and stale FAIL.
- No current CLI failure mode is lost.
- Build count is bounded and documented.
- Runtime reduction is measured.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if combining the lifecycle hides format-specific failure attribution.
- Do not remove missing-file coverage.
- Stop if CLI behavior depends on process isolation that cannot be simulated safely.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P7-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P7-T04: Move dependency-graph determinism to a small synthetic repository

```yaml
plan_task_id: "P7-T04"
phase_id: "P7"
task_type: "dependency_graph_synthetic_determinism"
title: "Move dependency-graph determinism to a small synthetic repository"
recommendation_ids:
  - "V19-R15"
  - "V19-R48"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P7-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Test deterministic construction and serialization on a compact adversarial fixture rather than performing two full live repository scans in the fast suite.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P7-T03`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_render_dependency_graph.py`
- `scripts/research_control/dependency_graph_model.py`

#### Planned write scope

- `tests/fixtures/dependency_graph/synthetic_repo/`
- `tests/test_dependency_graph_determinism.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Build a miniature repository containing representative ledger, task, job, claim-boundary, role, completion, and handoff relationships.
2. Include ordering-sensitive rows, duplicate-source references, blocked claims, scoped acceptance, and a frozen route.
3. Build twice from the same fixture and compare canonical hashes and all rendered formats.
4. Permute source row and file enumeration order and require identical output.
5. Keep one live scheduled double-build task outside the fast suite.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/dependency_graph_synthetic_coverage.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run deterministic, reordered-input, malformed-edge, and missing-source fixture cases.
- Validate the synthetic fixture exercises every graph node and edge class used by the determinism algorithm.
- Compare fixture runtime with the old live double-build.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Fast determinism coverage is stronger and much cheaper.
- Canonical serialization is proven under input reordering.
- Live full-corpus determinism remains scheduled.
- No graph schema field is untested.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if the synthetic fixture omits source-fingerprint or route-continuity behavior.
- Do not replace the live freshness acceptance test.
- Rollback only the test selection if fixture coverage is incomplete.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P7-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P7-T05: Path-trigger graph validation and retain one scheduled live double-build

```yaml
plan_task_id: "P7-T05"
phase_id: "P7"
task_type: "dependency_graph_path_trigger"
title: "Path-trigger graph validation and retain one scheduled live double-build"
recommendation_ids:
  - "V19-R15"
  - "V19-R30"
  - "V19-R41"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P7-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Run the expensive graph gate only when declared inputs or outputs change, while preserving one unfiltered scheduled full determinism run.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P7-T04`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_gate_manifest_v1.yaml`
- `research_control/design/validation_change_matrix_v1.md`
- `.github/workflows/project-control-validation.yml`

#### Planned write scope

- `research_control/design/validation_gate_manifest_v1.yaml`
- `tests/test_validation_change_matrix.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Declare precise graph inputs: relevant control registries, program state, referenced completion and handoff files, graph renderer code, and tracked graph outputs.
2. Select graph freshness for affected changes and full profile.
3. Exclude unrelated documentation or isolated scientific fixture changes unless they enter declared sources.
4. Add one scheduled live double-build determinism gate with no cache reuse.
5. Record graph source fingerprint in receipts.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/dependency_graph_path_selection_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run path-matrix fixtures for relevant and irrelevant changes.
- Mutation-test each declared input family.
- Verify scheduled full always selects the graph gate.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Ordinary unrelated edits do not pay graph cost.
- Relevant edits cannot skip freshness.
- Scheduled full retains live nondeterminism detection.
- Path mapping is explainable.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if graph source discovery is too dynamic to declare safely; use a conservative broader input tag.
- Do not path-filter the scheduled full run.
- Rollback filters if shadow mode shows a legacy graph failure on an unselected path.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P7-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P7-T06: Benchmark and audit dependency-graph failure-mode coverage

```yaml
plan_task_id: "P7-T06"
phase_id: "P7"
task_type: "dependency_graph_coverage_performance_audit"
title: "Benchmark and audit dependency-graph failure-mode coverage"
recommendation_ids:
  - "V19-R13"
  - "V19-R14"
  - "V19-R15"
  - "V19-R43"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P7-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Prove the graph refactor preserves every valuable invariant and delivers the dominant expected runtime saving.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P7-T05`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/tasks/<P0-T03-task>/artifacts/v19_baseline_benchmark.json`
- `tests/test_render_dependency_graph.py`
- `tests/test_dependency_graph_determinism.py`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Measure build counts, source loads, render calls, module runtime, full-suite contribution, and output bytes.
2. Map every legacy graph test assertion to the new test or lifecycle step.
3. Inject missing node, dangling edge, unknown class, stale JSON, stale Markdown, stale DOT, missing file, authority overread, and nondeterministic ordering mutations.
4. Run one live scheduled-style double-build outside the fast path.
5. Report target, observed, and residual cost.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/dependency_graph_final_audit.md`
- `research_control/tasks/<task-id>/artifacts/dependency_graph_final_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run the complete graph shard and one full suite.
- Validate mutation outcomes and no false PASS.
- Compare serialized graph bytes or document reviewed intentional changes.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- All legacy failure modes remain detected.
- Fast graph module runtime is materially below baseline.
- Full-suite target remains plausible.
- No graph output gains authority.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback performance-only changes if any mutation is missed.
- Do not accept fewer assertions as proof of equivalence.
- Route renderer schema changes separately from performance refactoring.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P8-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P8. Research-control routing, test decomposition, and advisory-metrics optimization

### P8 objective

Complete 7 bounded tasks covering `V19-R16`, `V19-R17`, `V19-R26`, `V19-R31`, `V19-R32`, `V19-R34`, `V19-R35`, `V19-R40`, `V19-R44`, `V19-R48`. This phase operates in shadow mode until the explicit cutover task authorizes planner authority.

### P8-T01: Split the broad research-control tests into focused shards

```yaml
plan_task_id: "P8-T01"
phase_id: "P8"
task_type: "research_control_test_sharding"
title: "Split the broad research-control tests into focused shards"
recommendation_ids:
  - "V19-R34"
  - "V19-R40"
  - "V19-R48"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P7-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Separate pure policy, active-state, continuation, checkpoint, metrics, and live-integration tests so frequent feedback does not repeatedly invoke the full live repository validator.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P7-T06`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_research_control.py`
- `tests/test_validate_research_control.py`
- `tests/README.md`

#### Planned write scope

- `tests/test_research_control_policy.py`
- `tests/test_research_control_active_state.py`
- `tests/test_research_control_continuation.py`
- `tests/test_research_control_checkpoint.py`
- `tests/test_research_control_metrics.py`
- `tests/test_research_control_live_integration.py`
- `tests/README.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Move tests by production surface and fixture type without changing assertions.
2. Create shared fixture builders in a non-test utility module under `tests/fixtures` or `tests/support`.
3. Keep historical activation-date fixtures and claim-boundary cases intact.
4. Prevent module import from triggering live validation.
5. Define explicit shard commands for CI and local affected profiles.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/research_control_test_split_map.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run old and new test inventories and compare test identifiers or documented mappings.
- Verify discovered test count and assertion coverage.
- Run each shard independently.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- No test is silently lost.
- Fast shards avoid live full-corpus validation.
- Live integration has a clearly named owner.
- CI can run shards in parallel.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if moving a test changes global patching or module state semantics.
- Retain compatibility import helpers until all tests migrate.
- Rollback individual test groups rather than the whole split.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P8-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P8-T02: Retain exactly one primary live full research-control acceptance test

```yaml
plan_task_id: "P8-T02"
phase_id: "P8"
task_type: "single_live_research_control_acceptance"
title: "Retain exactly one primary live full research-control acceptance test"
recommendation_ids:
  - "V19-R34"
  - "V19-R44"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P8-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Preserve one clear live acceptance test for the complete historical registry and state spine while removing accidental repeated live calls from behavioral tests.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P8-T01`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_research_control_live_integration.py`
- `scripts/research_control/validate_research_control.py`

#### Planned write scope

- `tests/test_research_control_live_integration.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Keep a primary test that calls full `validate_all()` against the live repository and requires no hard errors.
2. Add one explicit full diff integration acceptance if its behavior cannot be covered by the primary staged fixture.
3. Mark live acceptance as slow and include it in `full`, checkpoint when affected, and scheduled CI.
4. Record invocation counts to prevent additional behavioral tests from calling it accidentally.
5. Keep focused live frontier or graph checks only when they protect independent implementations.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/live_research_control_acceptance_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run the live integration shard and full suite.
- Use instrumentation to assert expected full-spine count.
- Test a synthetic corrupted repository separately rather than corrupting live state.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- At least one full live acceptance remains.
- Behavioral test modules do not pay full-spine cost.
- Full profile always includes the live acceptance.
- Failure messages identify the live gate.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a unique live invariant has no replacement.
- Do not mark live acceptance advisory.
- Rollback accidental mocks that bypass actual registry reads.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P8-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P8-T03: Inject validation receipts into continuation behavior tests

```yaml
plan_task_id: "P8-T03"
phase_id: "P8"
task_type: "continuation_validation_receipt_injection"
title: "Inject validation receipts into continuation behavior tests"
recommendation_ids:
  - "V19-R16"
  - "V19-R34"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P8-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Test continuation routing directly by supplying validated fixture state instead of rerunning the entire live research-control spine before every assertion.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P8-T02`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/continue_research.py`
- `tests/test_research_control_continuation.py`

#### Planned write scope

- `scripts/research_control/continue_research.py`
- `tests/test_research_control_continuation.py`
- `tests/fixtures/continuation/`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Refactor `continuation_status()` to accept an optional validation result or routing snapshot for tests and planner integration.
2. Provide PASS, FAIL, human-gate, existing-job, no-action, and warning-only fixtures.
3. Mock or inject route metrics and graph summary separately.
4. Keep one live integration test that exercises default dependency resolution.
5. Assert behavioral tests do not call full `validate_all()`.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/continuation_test_injection_equivalence.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all continuation boundary, graph-summary, route-warning, and Gate Chair availability tests.
- Compare outputs with current live behavior for a snapshot of program state.
- Instrument full-spine call count.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Continuation tests become fast and deterministic.
- Routing logic coverage is unchanged.
- One live default-path test remains.
- Injected PASS cannot be confused with physics authority.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if production accepts untrusted external validation receipts without fingerprint checks.
- Limit injection to internal API or explicit validated receipt objects.
- Rollback if live and injected outputs diverge unexpectedly.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P8-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P8-T04: Build one immutable metrics report per test class and run

```yaml
plan_task_id: "P8-T04"
phase_id: "P8"
task_type: "metrics_snapshot_reuse"
title: "Build one immutable metrics report per test class and run"
recommendation_ids:
  - "V19-R17"
  - "V19-R35"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P8-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Eliminate repeated full completion-history scans in metrics and dashboard assertions.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P8-T03`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/report_physics_progress_metrics.py`
- `scripts/research_control/render_ai_methodology_metrics_dashboard.py`
- `tests/test_research_control_metrics.py`
- `tests/test_report_physics_progress_metrics.py`

#### Planned write scope

- `scripts/research_control/report_physics_progress_metrics.py`
- `tests/test_research_control_metrics.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Expose a pure immutable metrics snapshot and render functions.
2. Build the live snapshot once in class setup or executor context.
3. Pass the same snapshot to separation, payload, route, dashboard, and Markdown assertions.
4. Use small fixtures for parse-error and warning-threshold tests.
5. Instrument completion files read and snapshot builds.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/metrics_snapshot_refactor_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all existing metrics and dashboard assertions.
- Compare report JSON and Markdown bytes before and after refactor.
- Assert one live metrics build per class.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Metric semantics and authority separation remain unchanged.
- Repeated live scans are eliminated.
- Fast metrics tests meet budget.
- P8-T06 can reuse the snapshot for routing diagnostics.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if shared mutable data affects test isolation.
- Do not cache across a changed repository tree.
- Stop if output ordering changes without reviewed normalization.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P8-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P8-T05: Isolate checkpoint tests from live repository validation

```yaml
plan_task_id: "P8-T05"
phase_id: "P8"
task_type: "checkpoint_test_fixture_isolation"
title: "Isolate checkpoint tests from live repository validation"
recommendation_ids:
  - "V19-R34"
  - "V19-R44"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P8-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Keep checkpoint safety tests focused on staging, rollback, allowlists, convergence, and command planning through synthetic repositories and injected gate results.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P8-T04`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_research_control_checkpoint.py`
- `scripts/research_control/checkpoint_research_transaction.py`

#### Planned write scope

- `tests/test_research_control_checkpoint.py`
- `tests/fixtures/checkpoint/`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Use temporary Git repositories or mocked Git command adapters for index and status transitions.
2. Inject planner results for PASS, FAIL, advisory, cache hit, and mismatch cases.
3. Retain actual `git write-tree`, `read-tree`, rename, and residue behavior in representative fixture tests.
4. Remove unnecessary live registry and metrics scans.
5. Keep one live no-commit integration path under the slow shard if safe.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/checkpoint_test_isolation_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all legacy checkpoint failure modes.
- Test exact index restoration by tree hash.
- Test no commit on every blocking result.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Checkpoint safety coverage is at least as strong.
- Tests are faster and less stateful.
- One live integration remains where it adds independent evidence.
- No mutation escapes temporary repositories.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if mocking hides actual Git semantics.
- Do not replace all index tests with pure mocks.
- Rollback fixture abstraction if it changes rename or ignored-file behavior.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P8-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P8-T06: Implement a narrow validated routing snapshot

```yaml
plan_task_id: "P8-T06"
phase_id: "P8"
task_type: "narrow_routing_snapshot"
title: "Implement a narrow validated routing snapshot"
recommendation_ids:
  - "V19-R16"
  - "V19-R26"
  - "V19-R44"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P8-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Provide a frequent routing preflight that validates only active state, current task, decision, job, handoff, execution role, active frontier, allowlist, and protected gate conditions.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P8-T05`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/continue_research.py`
- `scripts/research_control/validate_research_control.py`
- `scripts/research_control/resolve_latest_handoff.py`

#### Planned write scope

- `scripts/research_control/validate_routing_snapshot.py`
- `scripts/research_control/continue_research.py`
- `tests/test_routing_snapshot.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define the exact active-state inputs and exclusions.
2. Validate program state, active task, current decision and job, pending-job uniqueness, latest research handoff, role execution record, active frontier sync, and protected human-gate status.
3. Exclude full historical completion corpus, publication, memory derivatives, advisory metrics, and unrelated registries.
4. Return a fingerprinted routing snapshot with source paths and hashes.
5. Require full research-control validation at checkpoint and full profile.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/routing_snapshot_parity_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Compare narrow and full active-state conclusions across current state and adversarial fixtures.
- Test stale handoff, mismatched job, missing role, conflicting pending jobs, and human gate.
- Measure routing latency.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Frequent routing reads are materially faster.
- Every active-state blocker detected by full validation is detected by the narrow snapshot.
- Historical unrelated drift does not force repeated routing scans but remains caught by full acceptance.
- Snapshot is operational, not scientific authority.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if any active-state blocker appears only in full validation without a narrow equivalent.
- Do not let routing snapshot satisfy checkpoint full obligations.
- Rollback Continue Research default to full validation if parity is incomplete.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P8-T07` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P8-T07: Cache advisory route diagnostics and remove them from default blocking paths

```yaml
plan_task_id: "P8-T07"
phase_id: "P8"
task_type: "cached_advisory_route_diagnostics"
title: "Cache advisory route diagnostics and remove them from default blocking paths"
recommendation_ids:
  - "V19-R17"
  - "V19-R31"
  - "V19-R32"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P8-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Generate route-orbit and payload-density diagnostics only when completion or route-history inputs change, then read a compact support-only artifact during routing.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P8-T06`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/extract_route_history.py`
- `scripts/research_control/extract_route_signatures.py`
- `scripts/research_control/validate_route_orbits.py`
- `scripts/research_control/report_physics_progress_metrics.py`
- `scripts/research_control/continue_research.py`

#### Planned write scope

- `scripts/research_control/render_route_diagnostics.py`
- `research_control/design/route_diagnostic_cache_schema_v1.md`
- `scripts/research_control/continue_research.py`
- `research_control/design/validation_gate_manifest_v1.yaml`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define route-diagnostic source fingerprints from relevant task, job, completion, handoff, and policy files.
2. Generate one compact JSON artifact with warning counts, IDs, source fingerprint, generated time, and authority boundary.
3. Make stale or missing diagnostics an advisory freshness notice during routing.
4. Remove route-signature extraction and route-orbit checks from default blocking and local full command chains unless full diagnostics are explicitly requested.
5. Select regeneration in `doctor`, affected route-policy changes, and scheduled full diagnostics.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/route_diagnostic_cache_parity.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run warning, no-warning, stale-cache, parse-error, and missing-cache fixtures.
- Compare generated diagnostic findings with direct legacy computation.
- Assert no route warning becomes a hard gate.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Routing no longer rescans route history on every invocation.
- Advisory findings remain available and accurate.
- Default validation excludes the expensive or verbose diagnostic commands.
- No route-freeze or physics authority is created.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback to direct advisory computation if cache parity fails.
- Do not cache across source-fingerprint change.
- Stop if a diagnostic is currently relied on as a hard gate contrary to its declared policy.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P9-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P9. Traceability, memory, and Obsidian fixture minimization

### P9 objective

Complete 7 bounded tasks covering `V19-R18`, `V19-R19`, `V19-R25`, `V19-R32`, `V19-R33`, `V19-R36`, `V19-R37`, `V19-R40`, `V19-R47`. This phase operates in shadow mode until the explicit cutover task authorizes planner authority.

### P9-T01: Add dependency injection and minimal-fixture builders to support-traceability validators

```yaml
plan_task_id: "P9-T01"
phase_id: "P9"
task_type: "traceability_dependency_injection"
title: "Add dependency injection and minimal-fixture builders to support-traceability validators"
recommendation_ids:
  - "V19-R18"
  - "V19-R19"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P8-T07"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Refactor traceability validators so negative tests can supply parsed registries, path resolvers, and compact fixture roots without copying the complete repository.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P8-T07`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/support_formalization/validate_traceability_registry.py`
- `scripts/research_control/support_formalization/validate_traceability_registry_v18.py`
- `tests/test_support_formalization_traceability_registry.py`
- `tests/test_support_formalization_traceability_registry_v18.py`

#### Planned write scope

- `scripts/research_control/support_formalization/traceability_io.py`
- `tests/support/traceability_fixture_builder.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Introduce explicit repository root, registry object, file-loader, hash-provider, and proof-normal-form row dependencies.
2. Keep default production behavior reading the live repository.
3. Build a fixture helper that materializes only files referenced by selected entries.
4. Make authority-path and hash validation operate identically through injected dependencies.
5. Avoid API designs that let tests bypass validation logic.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/traceability_injection_equivalence.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run current live registry tests.
- Run injected missing file, hash mismatch, generated authority path, proof authority, and PNF row cases.
- Compare exception classes and normalized finding messages.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Production defaults remain unchanged.
- Tests can exercise one entry without full repository copy.
- All authority and hash checks remain fail-closed.
- Shared helper supports both v1 and v18.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if injection can return prevalidated results rather than raw inputs.
- Do not weaken path-prefix or source-hash checks.
- Rollback production signatures while retaining internal helper refactor if compatibility breaks.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P9-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P9-T02: Replace v1 support-traceability full-repository copies with minimal fixtures

```yaml
plan_task_id: "P9-T02"
phase_id: "P9"
task_type: "v1_traceability_minimal_fixtures"
title: "Replace v1 support-traceability full-repository copies with minimal fixtures"
recommendation_ids:
  - "V19-R18"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P9-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Rebuild v1 negative tests around minimal fixture roots while retaining one live current-registry acceptance and deterministic CLI test.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P9-T01`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_support_formalization_traceability_registry.py`
- `research_control/design/support_formalization_traceability_registry_v1.yaml`

#### Planned write scope

- `tests/test_support_formalization_traceability_registry.py`
- `tests/fixtures/support_traceability_v1/`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Create one minimal valid entry fixture with canonical source, support dependency, checker report, and traceability YAML.
2. Mutate proof authority and generated authority path in place without copying unrelated files.
3. Retain one live registry validation test and one CLI serialization test.
4. Record filesystem bytes and files created for old and new tests.
5. Preserve required boundary phrase and blocked-overread coverage.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v1_traceability_fixture_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all v1 tests and mutation cases.
- Compare normalized exceptions with legacy tests.
- Measure module runtime.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- All five legacy v1 behaviors remain covered.
- No test copies the entire repository.
- Module runtime falls to the low-second or sub-second range.
- Live acceptance remains.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if fixture simplification omits source-link or formal-object mapping checks.
- Do not remove the live current-registry test.
- Stop if test fixture paths accidentally become authoritative repository paths.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P9-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P9-T03: Replace v18 support-traceability full-repository copies with minimal fixtures

```yaml
plan_task_id: "P9-T03"
phase_id: "P9"
task_type: "v18_traceability_minimal_fixtures"
title: "Replace v18 support-traceability full-repository copies with minimal fixtures"
recommendation_ids:
  - "V19-R18"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P9-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Rebuild v18 negative tests around a minimal source, tool, report, test-evidence, and proof-normal-form fixture.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P9-T02`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_support_formalization_traceability_registry_v18.py`
- `research_control/design/support_formalization_traceability_registry_v18.yaml`
- `registries/PROOF_NORMAL_FORM_REGISTRY.csv`

#### Planned write scope

- `tests/test_support_formalization_traceability_registry_v18.py`
- `tests/fixtures/support_traceability_v18/`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Create a minimal valid v18 registry with one or more representative plan task entries.
2. Include a minimal PNF registry row and referenced source and tool artifacts.
3. Mutate proof authority, missing PNF row, report hash, and source hash independently.
4. Retain one live all-entry acceptance and one CLI Markdown/JSON test.
5. Preserve plan-task ordering and support-only boundary tests.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v18_traceability_fixture_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all v18 tests and new hash mutations.
- Compare normalized failures with legacy.
- Measure module runtime and filesystem work.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- All four legacy behaviors and added hash cases remain covered.
- No full repository copy occurs.
- Live registry parity remains.
- Runtime reduction is recorded.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback if minimal fixtures cannot exercise plan-task ordering.
- Do not remove PNF cross-registry validation.
- Stop if injected rows diverge from current schema semantics.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P9-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P9-T04: Perform v1-to-v18 traceability retirement parity assessment

```yaml
plan_task_id: "P9-T04"
phase_id: "P9"
task_type: "support_traceability_retirement_assessment"
title: "Perform v1-to-v18 traceability retirement parity assessment"
recommendation_ids:
  - "V19-R19"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P9-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Determine whether the v1 traceability validator can be retired, must remain active, or can become historical read-only support.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P9-T03`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/support_formalization/validate_traceability_registry.py`
- `scripts/research_control/support_formalization/validate_traceability_registry_v18.py`
- `research_control/design/support_formalization_traceability_registry_v1.yaml`
- `research_control/design/support_formalization_traceability_registry_v18.yaml`

#### Planned write scope

- `research_control/design/support_traceability_v1_v18_parity_assessment.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Map every v1 active entry to a v18 entry or document why it remains distinct.
2. Map every v1 hard failure to a v18 equivalent or stronger failure.
3. Assess historical artifact readability and referenced task evidence.
4. Run a mutation matrix through both validators.
5. Recommend `retain_active`, `retain_historical`, or `retire_after_migration` with evidence.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/support_traceability_parity_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate row and failure-mode coverage counts.
- Run both live validators.
- Require no v1-only hard failure before retirement.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- No validator is removed from version numbering alone.
- Retirement recommendation is evidence-based.
- Historical records remain readable.
- Any later deletion task cites this assessment.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Default to retain if parity is incomplete.
- Do not rewrite historical receipts to fit v18.
- Stop if active automation still references v1.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P9-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P9-T05: Convert memory-system unit coverage to miniature repositories and isolate live acceptance

```yaml
plan_task_id: "P9-T05"
phase_id: "P9"
task_type: "memory_test_fixture_minimization"
title: "Convert memory-system unit coverage to miniature repositories and isolate live acceptance"
recommendation_ids:
  - "V19-R33"
  - "V19-R36"
  - "V19-R40"
role_family: "memory-system-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P9-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Move discovery, registry, HTML, Mermaid, folder-map, and pruning tests to small fixture repositories while preserving one live validate-only and one live idempotence test.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P9-T04`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_memory_system.py`
- `.codex/skills/project-memory-system/scripts/memory_operations.py`
- `tests/README.md`

#### Planned write scope

- `tests/test_memory_system_unit.py`
- `tests/test_memory_system_live.py`
- `tests/fixtures/memory_system/`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Classify existing tests as pure fixture, compact integration, or live acceptance.
2. Build fixture roots with only the directories and registry rows needed by each behavior.
3. Move live validate-only and bootstrap idempotence to a named slow module.
4. Replace live folder-map and registry scans in unrelated assertions with fixture snapshots.
5. Keep Mermaid and publication tests owned by their focused modules where possible.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/memory_test_migration_map.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Map all legacy test names to new modules.
- Run unit, live, and full suites independently.
- Compare generated snapshot hashes and failure-mode mutations.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- No behavior is lost.
- Fast memory tests avoid live full-corpus scans.
- One live validate-only and one live idempotence acceptance remain.
- Memory-focused shard is explicit.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a fixture test cannot reproduce discovery behavior honestly.
- Do not mock away filesystem or hashing logic that the test claims to verify.
- Rollback individual migrations when fixture coverage is weaker.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P9-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P9-T06: Convert Obsidian and SQLite tests to miniature repositories and isolate live acceptance

```yaml
plan_task_id: "P9-T06"
phase_id: "P9"
task_type: "obsidian_test_fixture_minimization"
title: "Convert Obsidian and SQLite tests to miniature repositories and isolate live acceptance"
recommendation_ids:
  - "V19-R32"
  - "V19-R37"
  - "V19-R40"
role_family: "memory-system-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P9-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Eliminate repeated live source-corpus extraction from Obsidian tests while retaining one end-to-end local retrieval acceptance.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P9-T05`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `tests/test_obsidian_wiki.py`
- `.codex/skills/project-memory-system/scripts/obsidian_wiki_lib.py`

#### Planned write scope

- `tests/test_obsidian_wiki_unit.py`
- `tests/test_obsidian_wiki_live.py`
- `tests/fixtures/obsidian_wiki/`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Create minimal Markdown, TeX, HTML, optional PDF, registry, vault, semantic text, relationship, and SQLite fixtures.
2. Test extraction, indexing, lookup, FTS fallback, stale warnings, manual-note preservation, and index paths in compact roots.
3. Move one full source-object generation and search path to a slow live module.
4. Avoid writing into the repository `.local/` during unit tests.
5. Preserve local-only warning classification.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/obsidian_test_migration_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run unit and live shards.
- Compare current result fields and warning categories.
- Measure source files scanned and runtime.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Fast Obsidian tests use only temporary miniature roots.
- One live acceptance remains.
- Local retrieval warnings remain nonblocking for tracked core.
- Runtime reduction is recorded.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if fixture paths no longer match real relative-path semantics.
- Do not remove PDF extraction coverage; keep it conditional or use a tiny fixture PDF.
- Rollback any test that depends on accidental live state.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P9-T07` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P9-T07: Implement the local-retrieval doctor profile and checkpoint separation

```yaml
plan_task_id: "P9-T07"
phase_id: "P9"
task_type: "local_retrieval_doctor"
title: "Implement the local-retrieval doctor profile and checkpoint separation"
recommendation_ids:
  - "V19-R25"
  - "V19-R32"
  - "V19-R47"
role_family: "memory-system-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P9-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Provide one explicit health command for Obsidian, SQLite, semantic extracts, search smoke, environment, and advisory diagnostics without making it a universal checkpoint gate.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P9-T06`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/validation/profiles.py`
- `.codex/skills/project-memory-system/scripts/query_memory.py`
- `.codex/skills/project-memory-system/scripts/lint_obsidian_vault.py`
- `Makefile`

#### Planned write scope

- `scripts/validation/doctor.py`
- `Makefile`
- `.codex/skills/project-memory-system/SKILL.md`
- `tests/test_validation_doctor.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Select local retrieval status, optional sync, lint, index existence, search smoke, route diagnostics, and environment checks.
2. Separate read-only diagnosis from optional repair or sync actions.
3. Return WARN for stale local-only surfaces and FAIL only when the doctor command itself cannot perform its requested maintenance contract.
4. Ensure checkpoint profiles do not inherit doctor gates.
5. Store full local health receipts under `.local/`.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/doctor_profile_acceptance.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run fresh, stale, missing index, malformed index, optional refresh, and search failure fixtures.
- Assert core validation remains PASS for local-only staleness.
- Test compact output.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- `validate-doctor` or equivalent is documented and useful.
- Local retrieval is no longer a universal acceptance tax.
- Doctor results remain non-authoritative.
- Memory-maintenance tasks can still opt into blocking repair completion.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if doctor repair mutates tracked files.
- Do not convert local warnings into scientific or checkpoint failures.
- Rollback optional auto-refresh if it is not reliably bounded.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P10-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P10. Shared immutable repository snapshot and exact-tree cache

### P10 objective

Complete 6 bounded tasks covering `V19-R28`, `V19-R29`, `V19-R43`, `V19-R44`, `V19-R45`, `V19-R47`, `V19-R48`. This phase operates in shadow mode until the explicit cutover task authorizes planner authority.

### P10-T01: Implement the shared immutable repository snapshot

```yaml
plan_task_id: "P10-T01"
phase_id: "P10"
task_type: "shared_repository_snapshot"
title: "Implement the shared immutable repository snapshot"
recommendation_ids:
  - "V19-R29"
  - "V19-R43"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P9-T07"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Parse commonly used registries, control YAML, Git path state, and source metadata once per validation run and share immutable views across compatible gates.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P9-T07`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/research_control/validate_research_control.py`
- `.codex/skills/project-memory-system/scripts/memory_operations.py`
- `scripts/research_control/render_dependency_graph.py`
- `scripts/research_control/report_physics_progress_metrics.py`

#### Planned write scope

- `scripts/validation/snapshot.py`
- `tests/test_repository_snapshot.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define snapshot components and lazy loading for CSV registries, strict YAML, program state, handoffs, job completions, Git changed paths, and source hashes.
2. Bind the snapshot to repository root, scope, base ref, staged tree hash or working fingerprint, and configuration.
3. Expose immutable mappings and deterministic iteration.
4. Count parses, file reads, and hash operations.
5. Allow gates to request only declared components.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/repository_snapshot_equivalence.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test immutability, lazy loading, stale-tree rejection, parse errors, and deterministic ordering.
- Compare gate findings with and without a shared snapshot.
- Measure parse-count reduction in research-control, graph, and metrics runs.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Compatible gates share parsed state.
- Snapshot cannot outlive or silently cross its tree identity.
- Findings remain unchanged.
- Instrumentation shows fewer repeated reads.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if a gate observes files changed after snapshot creation without invalidation.
- Do not share mutable generator outputs across a mutator barrier.
- Rollback gate adapters individually if snapshot integration changes semantics.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P10-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P10-T02: Define the conservative exact-tree cache contract

```yaml
plan_task_id: "P10-T02"
phase_id: "P10"
task_type: "validation_cache_contract"
title: "Define the conservative exact-tree cache contract"
recommendation_ids:
  - "V19-R28"
  - "V19-R44"
  - "V19-R47"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P10-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Specify cache keys, eligible gates, invalidation, storage, authority, and cross-scope prohibitions before implementation.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P10-T01`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_evidence_identity_policy_v1.md`
- `research_control/design/validation_gate_manifest_v1.yaml`
- `research_control/design/validation_run_receipt_schema_v1.md`

#### Planned write scope

- `research_control/design/validation_cache_contract_v1.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define key components: gate ID, scope, exact tree hash, base ref where applicable, implementation digest, manifest/config digest, environment fingerprint, dependency-lock hash, and receipt schema version.
2. Allow only deterministic read-only gates with complete declared inputs.
3. Forbid caching mutators, human visual review, human gates, final residue and index-integrity checks, and nondeterminism experiments.
4. Store cache under `.local/validation-cache/` and mark it non-authoritative.
5. Require full result hash, creation time, tool version, and source fingerprints.
6. Define size, eviction, corruption, and manual disable behavior.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/cache_contract_review.yaml`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Review every manifest gate for provisional eligibility.
- Create positive and negative key examples.
- Run threat analysis for working-to-staged reuse, environment drift, implementation change, and corrupt receipt.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Cache eligibility is explicit and conservative.
- Cross-tree and cross-scope reuse is impossible by contract.
- Cache hit cannot imply physics authority.
- Final safeguards remain uncached.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Default uncertain gates to ineligible.
- Do not make cache availability required for correctness.
- Rollback by deleting `.local/validation-cache` and disabling one feature switch.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P10-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P10-T03: Implement cache storage, lookup, integrity, and eviction

```yaml
plan_task_id: "P10-T03"
phase_id: "P10"
task_type: "validation_cache_implementation"
title: "Implement cache storage, lookup, integrity, and eviction"
recommendation_ids:
  - "V19-R28"
  - "V19-R47"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P10-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Build a local cache that can safely reuse complete read-only gate receipts for the same evidence identity.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P10-T02`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_cache_contract_v1.md`
- `scripts/validation/models.py`
- `scripts/validation/reporting.py`

#### Planned write scope

- `scripts/validation/cache.py`
- `tests/test_validation_cache.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Use atomic writes and content-addressed directories.
2. Validate key, receipt hash, schema version, environment, manifest, and implementation fingerprints on lookup.
3. Return miss reasons such as absent, expired, corrupt, wrong tree, wrong scope, wrong implementation, or ineligible.
4. Implement bounded size and least-recently-used or age-based eviction without touching tracked files.
5. Provide `--no-cache`, `--clear-cache`, and read-only cache inspection.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/cache_implementation_acceptance.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test every invalidation dimension and corrupted partial writes.
- Test concurrent readers and writers.
- Test eviction and manual clear.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- A hit returns exactly the stored validated result and receipt hash.
- A mismatch is a miss, never a soft hit.
- Cache failures cannot make validation pass.
- Storage remains under `.local/`.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Disable cache on integrity failure.
- Do not repair corrupt entries by guessing.
- Rollback implementation without changing planner or gate semantics.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P10-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P10-T04: Integrate exact-tree cache lookup with the executor

```yaml
plan_task_id: "P10-T04"
phase_id: "P10"
task_type: "executor_cache_integration"
title: "Integrate exact-tree cache lookup with the executor"
recommendation_ids:
  - "V19-R28"
  - "V19-R43"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P10-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Use eligible cache hits to avoid repeated same-tree gate execution across skills, wrappers, and checkpoint phases while recording transparent evidence.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P10-T03`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/validation/executor.py`
- `scripts/validation/cache.py`
- `research_control/design/validation_gate_manifest_v1.yaml`

#### Planned write scope

- `scripts/validation/executor.py`
- `tests/test_executor_cache_integration.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Perform lookup only after evidence identity is fully known.
2. Return `CACHE_HIT` with original status, receipt hash, duration saved, and obligation coverage.
3. Write misses and hit reasons to the aggregate receipt.
4. Never use a working-tree hit for staged acceptance.
5. Bypass cache for final residue, whitespace where working files may change outside tree identity, human review, mutators, and scheduled nondeterminism tests.
6. Allow full profile to choose normal cache use or `--no-cache` audit mode.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/executor_cache_integration_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test repeated same-tree affected runs, working then staged, manifest edit, validator edit, dependency edit, and environment edit.
- Run shadow comparison with cache disabled and enabled.
- Assert child finding sets are identical.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Repeated exact-tree eligible gates are reused safely.
- Every hit is visible and attributable.
- No ineligible final safeguard is cached.
- Correctness is unchanged when cache is disabled.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Disable cache globally on any false hit.
- Stop if tree identity does not include all staged content.
- Do not count cache-hit duration as gate execution duration in performance reports.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P10-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P10-T05: Run cache invalidation, isolation, and adversarial safety tests

```yaml
plan_task_id: "P10-T05"
phase_id: "P10"
task_type: "cache_adversarial_safety_audit"
title: "Run cache invalidation, isolation, and adversarial safety tests"
recommendation_ids:
  - "V19-R28"
  - "V19-R44"
  - "V19-R45"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P10-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Attempt to make the cache return an unsound result and prove every relevant state change causes a miss.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P10-T04`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/validation/cache.py`
- `tests/test_validation_cache.py`
- `tests/test_executor_cache_integration.py`

#### Planned write scope

- `tests/test_validation_cache_adversarial.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Mutate one input file while preserving timestamps.
2. Change validator source, manifest, environment fingerprint, dependency lock, base ref, profile, scope, and receipt schema.
3. Corrupt result status, finding counts, and receipt hash.
4. Attempt working-to-staged, repository-to-temporary-root, and branch-to-branch reuse.
5. Test concurrent writes and interrupted atomic rename.
6. Verify final staged residue and allowlist checks always execute.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/cache_adversarial_audit.md`
- `research_control/tasks/<task-id>/artifacts/cache_adversarial_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run all adversarial cases with cache enabled.
- Run one rollback drill by clearing cache and rerunning uncached.
- Compare uncached and cached normalized results.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Every mutation produces a miss or blocking corruption result.
- No false PASS occurs.
- Rollback is immediate and complete.
- Safety audit authorizes shadow use only.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Any false hit forces `ROLLBACK_REQUIRED` and cache disablement.
- Do not weaken keys to recover hit rate.
- Retain adversarial tests permanently.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P10-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P10-T06: Benchmark shared snapshots and cold and warm cache behavior

```yaml
plan_task_id: "P10-T06"
phase_id: "P10"
task_type: "snapshot_cache_benchmark"
title: "Benchmark shared snapshots and cold and warm cache behavior"
recommendation_ids:
  - "V19-R29"
  - "V19-R43"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P10-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Measure parse reduction, cold execution, warm exact-tree reuse, cache overhead, and storage cost without mixing incompatible environments.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P10-T05`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/tasks/<P0-T03-task>/artifacts/v19_baseline_benchmark.json`
- `scripts/validation/snapshot.py`
- `scripts/validation/cache.py`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Measure affected and full plans with cache disabled, cold cache, and warm cache.
2. Count registry parses, file reads, hashes, subprocesses, cache hits, misses, bytes read and written, and wall time.
3. Run at least three warm repetitions for short plans and report median and range.
4. Measure cache lookup overhead for no-hit cases.
5. Report storage growth and eviction behavior.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/snapshot_cache_benchmark.md`
- `research_control/tasks/<task-id>/artifacts/snapshot_cache_benchmark.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate benchmark receipts and comparable environment fingerprints.
- Run a correctness comparison after each benchmark mode.
- Confirm no tracked diff.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Shared snapshot reduces repeated parsing.
- Warm cache produces meaningful savings without false hits.
- Cold overhead remains within budget.
- Evidence supports or rejects planner-authoritative cache activation.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Keep cache disabled by default if cold overhead or complexity outweighs benefit.
- Do not cherry-pick only favorable runs.
- Stop if benchmark instrumentation changes plan selection.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P11-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P11. CI rollout, compatibility retirement, and operator documentation

### P11 objective

Complete 6 bounded tasks covering `V19-R20`, `V19-R22`, `V19-R25`, `V19-R30`, `V19-R31`, `V19-R38`, `V19-R39`, `V19-R40`, `V19-R41`, `V19-R42`, `V19-R45`, `V19-R47`, `V19-R48`. This phase performs CI rollout, cutover, compatibility retirement, and documentation under the migration policy.

### P11-T01: Design the manifest-driven CI job and shard matrix

```yaml
plan_task_id: "P11-T01"
phase_id: "P11"
task_type: "ci_shard_design"
title: "Design the manifest-driven CI job and shard matrix"
recommendation_ids:
  - "V19-R38"
  - "V19-R40"
  - "V19-R41"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P10-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Define CI around one plan-producing job and responsibility-based shards rather than one serial all-purpose job plus duplicate memory setup.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P10-T06`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.github/workflows/project-control-validation.yml`
- `research_control/design/validation_profile_policy_v1.md`
- `research_control/design/validation_change_matrix_v1.md`

#### Planned write scope

- `research_control/design/ci_validation_shard_policy_v1.md`
- `.github/workflows/project-control-validation.yml`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Define a planning job that checks out code, provisions the environment, computes changed paths, validates the manifest, and emits a plan artifact.
2. Define shards for policy-fast, research-control integration, dependency graph, memory core, publication, scientific support, local retrieval, and orchestration or planner equivalence.
3. Assign each gate and test shard to exactly one primary CI owner while allowing full scheduled composition.
4. Define required versus optional checks and how an inapplicable shard reports success without executing work.
5. Preserve concurrency cancellation and timeouts.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/ci_shard_coverage_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate workflow syntax and generated plan artifact schema.
- Compare shard union with full profile gate and test coverage.
- Test representative path scenarios in a workflow simulation or plan-only fixture.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- CI shard ownership is complete and non-overlapping where possible.
- Full-profile union is preserved.
- No shard relies on hidden legacy command lists.
- Local retrieval is noncritical except when affected or scheduled.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if path-filtered required checks can disappear from branch protection unexpectedly.
- Do not parallelize before deduplication is complete.
- Keep the legacy CI job during shadow rollout.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P11-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P11-T02: Implement CI shards, path filters, and receipt artifacts

```yaml
plan_task_id: "P11-T02"
phase_id: "P11"
task_type: "ci_shard_implementation"
title: "Implement CI shards, path filters, and receipt artifacts"
recommendation_ids:
  - "V19-R30"
  - "V19-R40"
  - "V19-R47"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P11-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Implement the new CI matrix with safe path selection, compact logs, and uploaded full receipts.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P11-T01`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.github/workflows/project-control-validation.yml`
- `scripts/validation/cli.py`
- `research_control/design/ci_validation_shard_policy_v1.md`

#### Planned write scope

- `.github/workflows/project-control-validation.yml`
- `.github/workflows/scheduled-full-validation.yml`
- `tests/test_ci_validation_plan.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Use planner output to select shards rather than duplicating path globs independently in YAML where possible.
2. Upload aggregate and child receipts as artifacts while printing compact summaries.
3. Use pip caching and a shared setup pattern, but do not pretend separate runners share a mutable virtual environment.
4. Run relevant shards in parallel after the planning job.
5. Set timeouts based on measured cost and cancel stale runs.
6. Keep scheduled full workflow unfiltered and cache-audit capable.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/ci_shadow_run_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run workflow syntax checks and plan fixtures.
- Execute branch or dispatch shadow runs for representative path families.
- Compare shard union and statuses with the legacy job.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Affected PRs run only required shards plus mandatory policy checks.
- Full scheduled run executes every blocking shard.
- Full receipts are retained without verbose logs.
- No required invariant is path-filtered away.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback to legacy required job on any unexplained mismatch.
- Do not make the new job sole authority until P11-T04 cutover criteria pass.
- Stop if artifact upload failure hides validation status.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P11-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P11-T03: Deduplicate the parallel memory CI signal and add unfiltered scheduled full validation

```yaml
plan_task_id: "P11-T03"
phase_id: "P11"
task_type: "memory_ci_dedup_and_scheduled_full"
title: "Deduplicate the parallel memory CI signal and add unfiltered scheduled full validation"
recommendation_ids:
  - "V19-R40"
  - "V19-R41"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "shadow_planner"
depends_on:
  - "P11-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Preserve memory visibility without unconditionally repeating the same read-only gate and establish the scheduled backstop for planner mistakes.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P11-T02`
- The active implementation epoch must permit `shadow_planner` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.github/workflows/project-control-validation.yml`
- `.github/workflows/scheduled-full-validation.yml`
- `research_control/design/validation_gate_manifest_v1.yaml`

#### Planned write scope

- `.github/workflows/project-control-validation.yml`
- `.github/workflows/scheduled-full-validation.yml`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Run the memory shard only when memory inputs change, when full profile is requested, or on schedule.
2. If the main affected plan already executes memory core in the same job and tree, reuse its receipt instead of rerunning.
3. Keep an independently visible memory check name if operationally valuable, backed by receipt verification rather than duplicate execution.
4. Schedule an unfiltered full validation at a documented cadence and allow manual dispatch.
5. Run scheduled live graph determinism and local-retrieval health there.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/memory_ci_dedup_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Test memory-affecting, unrelated, full, and scheduled plan cases.
- Verify receipt reuse checks tree, implementation, environment, and manifest fingerprints.
- Run at least one scheduled workflow dispatch.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run legacy and planner shadow comparison for every affected blocking gate and fail closed on unexplained mismatch.

#### Definition of done

- Unrelated changes do not provision and run a duplicate memory job.
- Memory-affecting changes retain a clear signal.
- Scheduled full ignores path filters.
- Runner and critical-path costs are measured.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Keep the separate job if receipt reuse is not trustworthy, but path-filter it.
- Do not use a receipt from a different runner environment unless the gate contract permits it.
- Rollback schedule changes if they create uncontrolled resource consumption.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P11-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P11-T04: Run authoritative shadow comparison and cut over to planner orchestration

```yaml
plan_task_id: "P11-T04"
phase_id: "P11"
task_type: "planner_authoritative_cutover"
title: "Run authoritative shadow comparison and cut over to planner orchestration"
recommendation_ids:
  - "V19-R38"
  - "V19-R40"
  - "V19-R45"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P11-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Compare legacy and planner results across local, checkpoint, and CI scenarios, then authorize planner authority only if all safety and budget criteria pass.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P11-T03`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_orchestration_migration_and_rollback_policy_v1.md`
- `research_control/tasks/<P2-T05-task>/artifacts/v19_first_wave_equivalence_audit.json`
- `research_control/tasks/<P11-T02-task>/artifacts/ci_shadow_run_report.json`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Run at least three clean representative shadow transactions and the complete adversarial equivalence corpus.
2. Run legacy and planner full profiles on the same commit and environment.
3. Compare status, hard findings, warnings, selected paths, final tree, generated changes, and receipts.
4. Compare runtime, output bytes, and invocation counts against budgets.
5. Issue `CUTOVER_AUTHORIZED`, `REPAIR_REQUIRED`, or `ROLLBACK_REQUIRED`.
6. If authorized, switch Make, skills, checkpoint, and CI defaults to planner profiles while retaining explicit legacy fallback.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/planner_cutover_decision.md`
- `research_control/tasks/<task-id>/artifacts/planner_cutover_evidence.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run full test suite, full validation, checkpoint no-commit scenarios, and CI shadow runs.
- Verify rollback switches after cutover.
- Confirm the scheduled full workflow is operational.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- Zero legacy FAIL to planner PASS mismatches.
- All non-negotiable safeguards pass.
- Performance and output hard guards pass.
- Planner becomes authoritative only through a tracked decision.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback immediately on any safety mismatch.
- Do not accept majority agreement; every unexplained hard-status mismatch blocks cutover.
- Keep cache disabled if cache audit is incomplete even when planner cutover proceeds.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P11-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P11-T05: Retire duplicate command owners, default diagnostics, misleading modes, and compatibility aliases

```yaml
plan_task_id: "P11-T05"
phase_id: "P11"
task_type: "validation_compatibility_retirement"
title: "Retire duplicate command owners, default diagnostics, misleading modes, and compatibility aliases"
recommendation_ids:
  - "V19-R31"
  - "V19-R38"
  - "V19-R39"
  - "V19-R42"
role_family: "project-control-maintainer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P11-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

After cutover, remove or deprecate obsolete orchestration surfaces without deleting unique validators or historical evidence.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P11-T04`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `Makefile`
- `scripts/research_control/run_full_research_control_validation.py`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `.codex/skills/*/SKILL.md`
- `research_control/design/support_traceability_v1_v18_parity_assessment.md`

#### Planned write scope

- `Makefile`
- `scripts/research_control/run_full_research_control_validation.py`
- `.codex/skills/project-memory-system/scripts/bootstrap_memory_system.py`
- `research_control/design/validation_deprecation_ledger_v1.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Remove independent command lists from Make, skills, local runner, and checkpoint where wrappers now suffice.
2. Retire the `CI-equivalent` claim or retain the filename only as a deprecated full-profile wrapper.
3. Remove route-signature and route-orbit diagnostics from default and blocking plans while retaining doctor and explicit commands.
4. Remove misleading documentation-only flags only if P3 chose retirement; otherwise keep their true scoped implementations.
5. Deprecate the memory `--check` alias after tracked references migrate.
6. Retire v1 traceability only if P9-T04 authorizes it and all references migrate; otherwise record explicit retention.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/validation_deprecation_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Search tracked sources and registries for deprecated command references.
- Run wrapper, manifest, full, documentation-impact, memory, and research-control tests.
- Run a legacy fallback smoke test during the deprecation window.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- One orchestration owner remains.
- No unique validator implementation is deleted accidentally.
- Every removal has a ledger entry and replacement.
- Historical receipts remain readable.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop any removal lacking cutover evidence or reference migration.
- Default to deprecation before deletion.
- Rollback individual aliases or wrappers if an active operator path breaks.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P11-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P11-T06: Update contributor, operator, test, memory, and project-control documentation

```yaml
plan_task_id: "P11-T06"
phase_id: "P11"
task_type: "validation_operator_documentation"
title: "Update contributor, operator, test, memory, and project-control documentation"
recommendation_ids:
  - "V19-R20"
  - "V19-R22"
  - "V19-R25"
  - "V19-R38"
  - "V19-R47"
role_family: "documentation-curator@2.0.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P11-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Document the new validation model, profiles, receipts, cache, CI shards, doctor mode, rollback, and authority boundaries for humans and agents.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P11-T05`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `research_control/README.md`
- `scripts/README.md`
- `scripts/project_control/README.md`
- `scripts/research_control/README.md`
- `tests/README.md`
- `.codex/skills/project-memory-system/SKILL.md`

#### Planned write scope

- `README.md`
- `CONTRIBUTING.md`
- `research_control/README.md`
- `scripts/project_control/README.md`
- `scripts/research_control/README.md`
- `tests/README.md`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Provide a command table for setup, fast, affected, checkpoint, full, and doctor.
2. Explain that validation PASS is operational evidence, not proof authority.
3. Explain summary-first output and where full receipts live.
4. Explain cache keys, non-authority, disable and clear commands.
5. Explain CI shard selection and scheduled full coverage.
6. Document legacy fallback only for the active deprecation window.
7. Update source documentation, then regenerate derivatives through the approved path.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_documentation_consistency_report.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run documentation-impact, documentation-surface, publication if applicable, memory, and research-control validation.
- Run command examples in plan-only or help mode.
- Check no deprecated command is presented as primary.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- Humans and local agents can choose the correct profile.
- Authority boundaries are prominent and accurate.
- Documentation matches actual commands.
- Generated derivatives remain noncanonical.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if documentation requires hand-editing generated HTML or wiki.
- Do not expand role permissions through explanatory prose.
- Rollback individual docs if command behavior is not yet cut over.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P12-T01` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## P12. Performance validation, failure-mode audit, recommendation coverage, and research-route restoration

### P12 objective

Complete 7 bounded tasks covering `V19-R01`, `V19-R02`, `V19-R03`, `V19-R04`, `V19-R05`, `V19-R06`, `V19-R07`, `V19-R08`, `V19-R09`, `V19-R10`, `V19-R11`, `V19-R12`, `V19-R13`, `V19-R14`, `V19-R15`, `V19-R16`, `V19-R17`, `V19-R18`, `V19-R19`, `V19-R20`, `V19-R21`, `V19-R22`, `V19-R23`, `V19-R24`, `V19-R25`, `V19-R26`, `V19-R27`, `V19-R28`, `V19-R29`, `V19-R30`, `V19-R31`, `V19-R32`, `V19-R33`, `V19-R34`, `V19-R35`, `V19-R36`, `V19-R37`, `V19-R38`, `V19-R39`, `V19-R40`, `V19-R41`, `V19-R42`, `V19-R43`, `V19-R44`, `V19-R45`, `V19-R46`, `V19-R47`, `V19-R48`. This phase measures final behavior, proves non-regression, audits coverage, and restores ordinary research continuity.

### P12-T01: Benchmark the post-v19 full suite and gate profiles

```yaml
plan_task_id: "P12-T01"
phase_id: "P12"
task_type: "v19_final_performance_benchmark"
title: "Benchmark the post-v19 full suite and gate profiles"
recommendation_ids:
  - "V19-R43"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P11-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Measure final full, fast, affected, checkpoint-plan, and doctor profiles against the frozen baseline using comparable methods.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P11-T06`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/tasks/<P0-T03-task>/artifacts/v19_baseline_benchmark.json`
- `research_control/design/v19_validation_performance_and_safety_budget.md`
- `scripts/validation/cli.py`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Run the complete test suite with module and test timing instrumentation.
2. Run fast, representative affected, full, and doctor profiles with cache disabled, cold, and warm where applicable.
3. Record graph module, research-control shards, memory shards, traceability shards, and remaining top costs.
4. Count duplicate evidence identities, full-spine calls, graph builds, parses, subprocesses, and output bytes.
5. Report median and range for short runs and environment caveats for expensive runs.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_final_performance_benchmark.md`
- `research_control/tasks/<task-id>/artifacts/v19_final_performance_benchmark.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate benchmark receipts, log hashes, and no tracked diff.
- Compare hard finding sets with final full acceptance.
- Check target and hard-guard budgets.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- Final performance is measured, not merely estimated.
- Full-suite and profile results identify residual bottlenecks.
- No duplicate same-identity normal gate remains.
- Any missed target has a concrete follow-up, not hidden data.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Do not rerun until a favorable number appears.
- Separate noncomparable hardware results.
- Stop if benchmark instrumentation materially changes runtime without correction.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P12-T02` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P12-T02: Benchmark representative affected edits and governed checkpoints

```yaml
plan_task_id: "P12-T02"
phase_id: "P12"
task_type: "affected_checkpoint_benchmark"
title: "Benchmark representative affected edits and governed checkpoints"
recommendation_ids:
  - "V19-R02"
  - "V19-R30"
  - "V19-R43"
  - "V19-R46"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P12-T01"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Exercise the lean change matrix through realistic synthetic or disposable branches and measure plan selection and checkpoint cost.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P12-T01`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/validation_change_matrix_v1.md`
- `scripts/research_control/checkpoint_research_transaction.py`
- `scripts/validation/cli.py`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Test pure Python, control YAML, registered Markdown, TeX no-PDF, TeX with required PDF, HTML/Mermaid, memory code, graph renderer, task index, scientific checker, local retrieval, mixed, rename, deletion, and unknown path scenarios.
2. For each, record tags, selected gates, generators, tests, skipped gates, working precheck time, staged acceptance time, and output bytes.
3. Use temporary worktrees or fixture repositories and no production commit.
4. Verify unknown governed paths fail closed.
5. Compare selected blocking gates with the matrix golden expectations.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_affected_checkpoint_benchmark.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run plan-only, affected execution, and no-commit checkpoint for each scenario where practical.
- Validate exact index restoration after each fixture.
- Run full profile on a sample to confirm no missed failure.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- Affected scenarios meet target or document justified exceptions.
- Path selection matches the matrix.
- No scenario skips a necessary gate.
- Checkpoint remains atomic and fail-closed.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if any test scenario touches canonical live science sources outside a disposable fixture.
- Rollback path mappings that produce false negatives.
- Do not weaken unknown-path fallback for performance.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P12-T03` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P12-T03: Measure CI critical path, runner compute, and scheduled-full behavior

```yaml
plan_task_id: "P12-T03"
phase_id: "P12"
task_type: "v19_ci_performance_audit"
title: "Measure CI critical path, runner compute, and scheduled-full behavior"
recommendation_ids:
  - "V19-R40"
  - "V19-R41"
  - "V19-R43"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P12-T02"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Evaluate real GitHub Actions behavior after cutover, including critical path, shard balance, path filtering, artifact retention, and scheduled backstop.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P12-T02`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `.github/workflows/project-control-validation.yml`
- `.github/workflows/scheduled-full-validation.yml`
- `research_control/tasks/<P0-T03-task>/artifacts/v19_baseline_benchmark.json`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Collect at least three successful affected CI runs where available and one scheduled or manual full run.
2. Record planning time, setup time, shard durations, critical path, total runner time, cancellations, cache behavior, and receipt artifact sizes.
3. Compare with the audited 1,025-second project-control step while noting runner-hardware variance.
4. Identify imbalanced shards and unnecessary setup duplication.
5. Confirm scheduled full selects every blocking shard and live nondeterminism checks.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_ci_performance_audit.md`
- `research_control/tasks/<task-id>/artifacts/v19_ci_performance_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate workflow run commit hashes and profile receipts.
- Compare shard union with manifest full plan.
- Check no path-filtered PR run masks a scheduled-full failure without a follow-up signal.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- CI critical path and runner cost are reported honestly.
- Required checks are stable.
- Scheduled full functions as mapping backstop.
- Any residual bottleneck has a bounded follow-up recommendation.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Do not claim controlled speedup from unlike hosted runners.
- Rollback required-check changes if branch protection becomes ambiguous.
- Stop if scheduled full cannot upload receipts or report failures.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P12-T04` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P12-T04: Audit agent-output and receipt exposure against token budgets

```yaml
plan_task_id: "P12-T04"
phase_id: "P12"
task_type: "v19_output_exposure_audit"
title: "Audit agent-output and receipt exposure against token budgets"
recommendation_ids:
  - "V19-R20"
  - "V19-R21"
  - "V19-R22"
  - "V19-R43"
  - "V19-R47"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P12-T03"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Measure default output exposure for PASS, small FAIL, warning-heavy FAIL, cache hit, and doctor scenarios while confirming complete receipts remain available.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P12-T03`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `scripts/validation/reporting.py`
- `scripts/research_control/validate_task_index.py`
- `scripts/research_control/extract_route_signatures.py`
- `scripts/research_control/validate_research_control.py`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Measure stdout and stderr characters, lines, findings shown, full receipt bytes, and char-divided-by-four token proxy.
2. Include the historical task-index, route-signature, and research-control cases from the audit.
3. Verify successful commands return summaries rather than raw full JSON.
4. Verify agents can expand one failed finding group without reading unrelated warnings.
5. Check receipts contain all original findings and hashes.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_output_exposure_audit.json`
- `research_control/tasks/<task-id>/artifacts/v19_output_exposure_audit.md`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run reporting unit tests and representative live or fixture commands.
- Validate output budgets and no missing full evidence.
- Check no secrets or environment tokens enter receipts.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- PASS and default FAIL outputs satisfy budgets.
- Token-proxy exposure falls materially from baseline.
- Complete evidence is retained.
- Summary-first skill instructions match actual behavior.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Rollback compact mode for any command that loses actionable failure context.
- Do not delete full report modes.
- Stop if receipt files are tracked or treated as authority by default.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P12-T05` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P12-T05: Run the final failure-mode mutation and non-negotiable safeguard audit

```yaml
plan_task_id: "P12-T05"
phase_id: "P12"
task_type: "v19_non_regression_audit"
title: "Run the final failure-mode mutation and non-negotiable safeguard audit"
recommendation_ids:
  - "V19-R19"
  - "V19-R44"
  - "V19-R45"
  - "V19-R48"
role_family: "validator-engineer@0.2.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P12-T04"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Prove the optimized system still fails closed for every protected authority, transaction, generated-surface, scientific-checker, and cache boundary.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P12-T04`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/design/v19_validation_performance_and_safety_budget.md`
- `tests/fixtures/validation_equivalence/`
- `research_control/design/validation_gate_manifest_v1.yaml`

#### Planned write scope

- `tests/test_v19_validation_non_regression.py`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Mutate role authority, human-gate requirements, AgentJob allowlists, Markdown authority markers, claim language, generated-only edits, stale registries, stale frontiers, graph and index outputs, publication source binding, traceability proof authority, cache keys, staged residue, and whitespace.
2. For each mutation, record the expected gate and stable finding ID.
3. Run the affected plan and full plan.
4. Verify final staged checks execute uncached.
5. Verify v1 traceability remains or is safely retired according to P9-T04.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_non_regression_audit.md`
- `research_control/tasks/<task-id>/artifacts/v19_non_regression_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run the complete mutation suite, full test suite, and full profile.
- Validate zero false PASS and expected warning versus hard-fail distinctions.
- Run rollback mode on one injected planner defect.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- Every non-negotiable safeguard detects its mutation.
- No performance optimization weakens severity.
- Unknown governed paths fail closed.
- Rollback remains functional.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Any false PASS is a release blocker and triggers rollback.
- Do not reclassify a hard failure to warning to pass the audit.
- Preserve the mutation suite permanently.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P12-T06` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P12-T06: Audit final coverage of all v19 recommendations

```yaml
plan_task_id: "P12-T06"
phase_id: "P12"
task_type: "v19_recommendation_coverage_audit"
title: "Audit final coverage of all v19 recommendations"
recommendation_ids:
  - "V19-R01"
  - "V19-R02"
  - "V19-R03"
  - "V19-R04"
  - "V19-R05"
  - "V19-R06"
  - "V19-R07"
  - "V19-R08"
  - "V19-R09"
  - "V19-R10"
  - "V19-R11"
  - "V19-R12"
  - "V19-R13"
  - "V19-R14"
  - "V19-R15"
  - "V19-R16"
  - "V19-R17"
  - "V19-R18"
  - "V19-R19"
  - "V19-R20"
  - "V19-R21"
  - "V19-R22"
  - "V19-R23"
  - "V19-R24"
  - "V19-R25"
  - "V19-R26"
  - "V19-R27"
  - "V19-R28"
  - "V19-R29"
  - "V19-R30"
  - "V19-R31"
  - "V19-R32"
  - "V19-R33"
  - "V19-R34"
  - "V19-R35"
  - "V19-R36"
  - "V19-R37"
  - "V19-R38"
  - "V19-R39"
  - "V19-R40"
  - "V19-R41"
  - "V19-R42"
  - "V19-R43"
  - "V19-R44"
  - "V19-R45"
  - "V19-R46"
  - "V19-R47"
  - "V19-R48"
role_family: "process-integrity-auditor@0.1.0"
controlling_skill: "improve-project-system"
migration_epoch: "planner_authoritative"
depends_on:
  - "P12-T05"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Assign final implemented, retained, deferred, blocked, superseded, or conditionally-not-required status to every v19 recommendation and every plan task.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P12-T05`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `implementations_plans/recommendations_implementation_plan_continue_task-v19.md`
- `research_control/design/v19_validation_overhead_backlog.yaml`
- `research_control/tasks/<all-v19-tasks>/jobs/completions/`

#### Planned write scope

- No production-source write is planned. Only task-local reports, receipts, and normal control records may be created.
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Build a row for V19-R01 through V19-R48 with direct implementation evidence, validation evidence, performance evidence, and remaining caveats.
2. Verify every P0 through P12 task has final status and completion or supersession evidence.
3. Identify any missing or partial recommendation as a concrete project-improvement signal.
4. Separate target misses from safety failures.
5. State explicitly that coverage counts and speedups are not physics progress.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_recommendation_coverage_audit.md`
- `research_control/tasks/<task-id>/artifacts/v19_recommendation_coverage_audit.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Validate evidence paths and hashes.
- Cross-check backlog and Markdown task counts.
- Run the final full profile and non-regression audit receipt validation.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- Every recommendation has final status and evidence.
- No missing recommendation is silently marked covered.
- Any follow-up signal is routed through project-system sidecar machinery.
- The audit determines whether P12-T07 may restore ordinary research continuation.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Stop if evidence paths are missing or completion statuses conflict.
- Do not close a recommendation from intention alone.
- Route unresolved safety items as blockers, not backlog polish.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, select `P12-T07` unless a tracked repair or supersession decision is required.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.

### P12-T07: Publish the v19 integration handoff and restore the ordinary v18 research route

```yaml
plan_task_id: "P12-T07"
phase_id: "P12"
task_type: "v19_integration_handoff"
title: "Publish the v19 integration handoff and restore the ordinary v18 research route"
recommendation_ids:
  - "V19-R01"
  - "V19-R02"
  - "V19-R03"
  - "V19-R04"
  - "V19-R05"
  - "V19-R06"
  - "V19-R07"
  - "V19-R08"
  - "V19-R09"
  - "V19-R10"
  - "V19-R11"
  - "V19-R12"
  - "V19-R13"
  - "V19-R14"
  - "V19-R15"
  - "V19-R16"
  - "V19-R17"
  - "V19-R18"
  - "V19-R19"
  - "V19-R20"
  - "V19-R21"
  - "V19-R22"
  - "V19-R23"
  - "V19-R24"
  - "V19-R25"
  - "V19-R26"
  - "V19-R27"
  - "V19-R28"
  - "V19-R29"
  - "V19-R30"
  - "V19-R31"
  - "V19-R32"
  - "V19-R33"
  - "V19-R34"
  - "V19-R35"
  - "V19-R36"
  - "V19-R37"
  - "V19-R38"
  - "V19-R39"
  - "V19-R40"
  - "V19-R41"
  - "V19-R42"
  - "V19-R43"
  - "V19-R44"
  - "V19-R45"
  - "V19-R46"
  - "V19-R47"
  - "V19-R48"
role_family: "director-of-research@0.3.0"
controlling_skill: "continue-research"
migration_epoch: "planner_authoritative"
depends_on:
  - "P12-T06"
max_agentjobs_per_invocation: 1
requires_human_gate: false
project_system_boundary_authorized_by_plan: true
scientific_claims_changed: false
physics_delta_authorized: false
physics_promotion_authorized: false
proof_authority: false
ordinary_research_handoff_preserved: true
```

#### Objective

Close the project-system sidecar, publish one bounded integration handoff, and return ordinary research continuation to the validated `EqSrc_family_closure_repair_or_stress` route unless a later tracked scientific decision supersedes it.

#### Preconditions and dependency evidence

- Every dependency below must have a PASS completion or a tracked supersession decision:
  - `P12-T06`
- The active implementation epoch must permit `planner_authoritative` behavior.
- The working tree must be inspected for unrelated changes before any write.
- The selected role execution record must not expand physics, proof, benchmark, or canonical-source authority.

#### Required source inspection

- `research_control/handoffs/handoff-0740.yaml`
- `research_control/tasks/<P12-T06-task>/artifacts/v19_recommendation_coverage_audit.md`
- `research_control/tasks/<P12-T01-task>/artifacts/v19_final_performance_benchmark.md`
- `research_control/program_state.yaml`

#### Planned write scope

- `research_control/handoffs/handoff-<next>.yaml`
- `research_control/handoffs/handoff-<next>.md`
- `research_control/program_state.yaml`
- Standard task-local records, applicable registry rows, and generated derivatives are allowed only when required by current project policy.
- Any path outside this scope requires a new tracked decision or a narrower follow-up task.

#### Implementation actions

1. Summarize implemented orchestration, removed duplicate invocations, retained safeguards, performance results, output reductions, cache status, and remaining signals.
2. Distinguish the latest project-system task from the latest research-continuation authority using active-state bifurcation fields.
3. Select exactly one next action: resume `EqSrc_family_closure_repair_or_stress`, execute a bounded v19 repair signal, or request a human decision if a protected issue remains.
4. Do not claim that validation efficiency changes Distance-to-GR status.
5. Record the final manifest, planner, schema, and coverage evidence paths and hashes.

#### Required durable outputs

- `research_control/tasks/<task-id>/artifacts/v19_integration_handoff_report.json`
- A compact validation receipt or audit report containing gate IDs, status, counts, relevant hashes, and no-physics-authority boundary.
- Updated documentation-impact receipt for any state-changing project-system work.

#### Required validation and evidence

- Run final checkpoint profile, full profile, memory core if affected, documentation impact, and `git diff --check`.
- Validate handoff and program-state consistency.
- Confirm no project-system sidecar silently supersedes a scientific route.
- Run `git diff --check` before closure.
- Record full raw output in receipt files rather than embedding unbounded logs in the completion.
- Run the authoritative planner `checkpoint` profile and the task's affected focused tests.

#### Definition of done

- V19 has a final integration handoff.
- All applicable recommendations are covered or explicitly routed.
- The ordinary research route is restored exactly once when safe.
- No physics, proof, source-law, benchmark, Gate Chair, or completed-derivation authority is claimed.
- Completion records `distance_to_gr_delta.changed: false` and `scientific_claims_changed: false`.
- No unrelated tracked change remains.

#### Stop, repair, and rollback conditions

- Do not restore research continuation if a v19 safety blocker remains.
- Do not select more than one next route.
- Rollback only the final handoff and program-state pointer if validation fails before checkpoint.
- A missing hard finding, wrong staged tree, unexplained legacy/planner mismatch, or write outside the allowlist is always blocking.
- Performance improvement never compensates for lost failure-mode coverage.

#### Handoff rule

- On PASS, close the v19 project-system sidecar and route exactly one ordinary scientific next action or one bounded repair as specified by the final handoff.
- On `REPAIR_REQUIRED`, create one bounded repair task that preserves this task ID's recommendation coverage obligation.
- On `BLOCKED`, preserve evidence, commit nothing invalid, and report the narrow blocking authority or invariant.


---

## 31. Final v19 success criteria

V19 is complete only when every applicable condition below is proven by tracked evidence:

```yaml
v19_success_criteria:
  plan_registered: true
  recommendation_backlog_complete_and_acyclic: true
  baseline_and_budgets_frozen: true
  validation_evidence_identity_policy_active: true
  direct_same_scope_research_control_duplication_removed: true
  equivalent_changed_claim_duplication_removed: true
  memory_sync_and_validation_separated: true
  nested_publication_validation_removed: true
  docs_modes_true_or_retired: true
  dependency_installation_removed_from_validation_targets: true
  compact_receipt_schema_active: true
  task_index_and_route_diagnostics_bounded: true
  manifest_is_single_orchestration_source: true
  classifier_is_pure_and_planner_is_deterministic: true
  fast_affected_checkpoint_full_doctor_profiles_active: true
  role_and_skill_obligations_deduplicated: true
  checkpoint_validates_exact_final_staged_tree: true
  final_allowlist_residue_whitespace_and_index_checks_preserved: true
  dependency_graph_fast_tests_reuse_one_live_build: true
  dependency_graph_cli_lifecycle_combined: true
  live_graph_determinism_retained_scheduled: true
  research_control_tests_split: true
  one_live_research_control_acceptance_retained: true
  narrow_routing_snapshot_parity_proven: true
  advisory_route_diagnostics_cached_and_nonblocking: true
  traceability_tests_use_minimal_fixtures: true
  traceability_v1_retained_or_retired_only_by_parity_evidence: true
  memory_and_obsidian_fast_tests_use_miniature_fixtures: true
  one_live_memory_and_local_retrieval_acceptance_retained: true
  immutable_repository_snapshot_active: true
  exact_tree_cache_safety_audit_passed_or_cache_left_disabled: true
  make_ci_skills_runner_checkpoint_are_planner_wrappers: true
  ci_shards_cover_full_manifest_union: true
  scheduled_unfiltered_full_validation_active: true
  legacy_cutover_shadow_comparison_passed: true
  deprecated_surfaces_have_replacement_and_reference_migration: true
  full_failure_mode_mutation_audit_passed: true
  recommendation_coverage_V19_R01_through_V19_R48_complete: true
  distance_to_gr_changed: false
  physics_promotion_authorized: false
  proof_authority: false
  benchmark_promotion_authorized: false
  completed_derivation_authorized: false
  ordinary_research_route_restored_or_explicitly_blocked: true
```

## 32. Performance acceptance matrix

These are targets and hard guards for comparable environments. They are engineering goals, not physics metrics.

| Metric | Baseline | Target | Provisional hard guard | Measurement rule |
| --- | ---: | ---: | ---: | --- |
| Full local suite | 507.215 s | 100-160 s | 180 s | Same Python, dependency state, machine class, captured output |
| Dependency-graph fast module | 378.598 s | 45-90 s | 120 s | One shared live build plus lifecycle and synthetic tests |
| Common affected loop | Often full chain | 5-30 s | 45 s | Representative change matrix, warm environment |
| Governed checkpoint | Repeated full spines | 60-90 s typical | 150 s except justified PDF or graph work | Final staged affected plan |
| CI critical path | 1,025 s validation step | A few minutes | 8 min after rollout | Compare multiple runs and disclose runner variance |
| Same-identity duplicate gates | Multiple | 0 | 0 | Trace by gate, scope, tree, implementation, config |
| Default PASS output | Up to many KiB | <=2 KiB | 4 KiB | stdout plus stderr |
| Default FAIL output | Up to tens of thousands of chars | <=8 KiB | 12 KiB | First ten actionable findings plus receipt path |
| Full evidence retention | Mixed stdout | 100 percent | 100 percent | Full receipt files and hashes |
| False PASS in mutation corpus | Unknown | 0 | 0 | Every protected mutation must fail or warn as specified |

A target miss is not automatically a safety failure. A hard-guard miss requires repair, an explicit exception with evidence, or rollback. Any false PASS or missing hard finding is an immediate safety failure regardless of speed.

## 33. Non-negotiable safeguards

The following must remain after every phase:

1. Final staged write-allowlist enforcement.
2. Role and execution-role authority validation.
3. Human-gate requirements.
4. Changed claim-language protection.
5. Mixed Markdown authority boundaries.
6. Source versus generated authority separation.
7. Final staged residue detection.
8. `git diff --check`.
9. Exact index restoration on blocked or exceptional checkpoint paths.
10. Targeted PDF builds for changed registered TeX with `pdf_required=true`.
11. Relevant generated-surface freshness for affected inputs.
12. Relevant scientific checker and traceability coverage for changed artifacts.
13. One live full research-control acceptance.
14. One live memory validate-only and one live idempotence acceptance.
15. One live dependency-graph freshness path and one scheduled live determinism path.
16. One live local-retrieval acceptance.
17. An unfiltered scheduled full validation.
18. Fail-closed handling for unknown governed paths.
19. Complete receipts for full evidence.
20. No cache reuse across scope, tree, implementation, environment, configuration, or dependency changes.
21. No validation, CI, cache, benchmark, or test result as physics proof.

## 34. Default final route after v19

If all v19 safety requirements pass and no project-system blocker remains, the final handoff must restore the ordinary research continuation recorded in `handoff-0740`:

```yaml
selected_next_route:
  route_id: "EqSrc_family_closure_repair_or_stress"
  packet_count: 1
  requires_human_gate: false
  physics_promotion_authorized: false
  project_system_sidecar_supersedes_research_handoff: false
```

If a v19 safety blocker remains, the final handoff may instead select exactly one bounded project-system repair. It must state why ordinary research cannot yet resume and which invariant blocks it.

## 35. Minimal v19 completion receipt template

```yaml
completion_id: string
job_id: string
task_id: string
completed_at: string
status: "completed | blocked | failed_closed | superseded"

implementation_plan_receipt:
  plan_id: "recommendations_implementation_plan_continue_task-v19"
  plan_path: "implementations_plans/recommendations_implementation_plan_continue_task-v19.md"
  plan_task_id: string
  recommendation_ids: list[string]
  migration_epoch: string

project_system_change_only: true
scientific_claims_changed: false
physics_promotion_authorized: false
proof_authority: false

output_paths: list[string]
changed_paths: list[string]
generated_paths: list[string]

validation:
  profile: string
  scope: string
  working_tree_fingerprint: string
  staged_tree_hash: string
  manifest_hash: string
  environment_fingerprint: string
  selected_gate_ids: list[string]
  executed_gate_ids: list[string]
  superseded_gate_ids: list[string]
  satisfied_obligations: list[string]
  duplicate_evidence_identity_count: integer
  blocking_failure_count: integer
  warning_count: integer
  aggregate_receipt_path: string
  aggregate_receipt_hash: string
  legacy_comparison_status: "not_applicable | match | mismatch"

performance:
  baseline_reference: string
  duration_seconds: number
  subprocess_count: integer
  registry_parse_count: integer
  graph_build_count: integer
  output_bytes: integer
  cache_hits: integer
  cache_misses: integer
  budget_status: "target_met | hard_guard_met | exception_required | not_measured"

distance_to_gr_delta:
  effect: "no_distance_delta"
  changed: false
  ledger_row_updated: false

recommendation_coverage:
  implementation_status: string
  coverage_effect: string
  evidence_paths: list[string]

claim_boundary:
  validator_results_are_physics_proof: false
  cache_results_are_physics_proof: false
  generated_receipts_are_authority: false
  ordinary_research_route_preserved: true

project_improvement_signals: list[object]
next_recommendation: string
```

## 36. Appendix A: Recommendation-to-task coverage
| Recommendation | Direct and supporting tasks |
| --- | --- |
| `V19-R01` | `P0-T01`, `P0-T02`, `P0-T04`, `P1-T01`, `P1-T04`, `P5-T04`, `P5-T06`, `P6-T01`, `P12-T06`, `P12-T07` |
| `V19-R02` | `P0-T01`, `P0-T02`, `P5-T07`, `P6-T02`, `P6-T03`, `P6-T04`, `P6-T05`, `P12-T02`, `P12-T06`, `P12-T07` |
| `V19-R03` | `P0-T01`, `P0-T02`, `P1-T02`, `P1-T03`, `P2-T01`, `P2-T02`, `P2-T05`, `P5-T06`, `P12-T06`, `P12-T07` |
| `V19-R04` | `P0-T01`, `P0-T02`, `P1-T02`, `P1-T03`, `P2-T03`, `P2-T05`, `P5-T06`, `P12-T06`, `P12-T07` |
| `V19-R05` | `P0-T01`, `P0-T02`, `P3-T01`, `P3-T02`, `P6-T02`, `P12-T06`, `P12-T07` |
| `V19-R06` | `P0-T01`, `P0-T02`, `P3-T05`, `P12-T06`, `P12-T07` |
| `V19-R07` | `P0-T01`, `P0-T02`, `P3-T02`, `P3-T03`, `P12-T06`, `P12-T07` |
| `V19-R08` | `P0-T01`, `P0-T02`, `P3-T04`, `P12-T06`, `P12-T07` |
| `V19-R09` | `P0-T01`, `P0-T02`, `P3-T03`, `P12-T06`, `P12-T07` |
| `V19-R10` | `P0-T01`, `P0-T02`, `P3-T06`, `P3-T07`, `P12-T06`, `P12-T07` |
| `V19-R11` | `P0-T01`, `P0-T02`, `P2-T04`, `P3-T05`, `P6-T03`, `P6-T05`, `P6-T06`, `P12-T06`, `P12-T07` |
| `V19-R12` | `P0-T01`, `P0-T02`, `P2-T02`, `P3-T01`, `P3-T05`, `P6-T02`, `P6-T04`, `P6-T05`, `P12-T06`, `P12-T07` |
| `V19-R13` | `P0-T01`, `P0-T02`, `P7-T01`, `P7-T02`, `P7-T06`, `P12-T06`, `P12-T07` |
| `V19-R14` | `P0-T01`, `P0-T02`, `P7-T03`, `P7-T06`, `P12-T06`, `P12-T07` |
| `V19-R15` | `P0-T01`, `P0-T02`, `P7-T04`, `P7-T05`, `P7-T06`, `P12-T06`, `P12-T07` |
| `V19-R16` | `P0-T01`, `P0-T02`, `P8-T03`, `P8-T06`, `P12-T06`, `P12-T07` |
| `V19-R17` | `P0-T01`, `P0-T02`, `P4-T04`, `P8-T04`, `P8-T07`, `P12-T06`, `P12-T07` |
| `V19-R18` | `P0-T01`, `P0-T02`, `P9-T01`, `P9-T02`, `P9-T03`, `P12-T06`, `P12-T07` |
| `V19-R19` | `P0-T01`, `P0-T02`, `P9-T01`, `P9-T04`, `P12-T05`, `P12-T06`, `P12-T07` |
| `V19-R20` | `P0-T01`, `P0-T02`, `P2-T03`, `P4-T01`, `P4-T02`, `P4-T03`, `P4-T04`, `P4-T05`, `P6-T01`, `P6-T08`, `P11-T06`, `P12-T04`, `P12-T06`, `P12-T07` |
| `V19-R21` | `P0-T01`, `P0-T02`, `P4-T02`, `P4-T03`, `P4-T04`, `P4-T05`, `P12-T04`, `P12-T06`, `P12-T07` |
| `V19-R22` | `P0-T01`, `P0-T02`, `P4-T01`, `P4-T06`, `P6-T06`, `P11-T06`, `P12-T04`, `P12-T06`, `P12-T07` |
| `V19-R23` | `P0-T01`, `P0-T02`, `P5-T03`, `P5-T04`, `P12-T06`, `P12-T07` |
| `V19-R24` | `P0-T01`, `P0-T02`, `P1-T02`, `P5-T01`, `P5-T02`, `P5-T04`, `P6-T01`, `P12-T06`, `P12-T07` |
| `V19-R25` | `P0-T01`, `P0-T02`, `P5-T07`, `P6-T03`, `P6-T06`, `P9-T07`, `P11-T06`, `P12-T06`, `P12-T07` |
| `V19-R26` | `P0-T01`, `P0-T02`, `P1-T01`, `P5-T01`, `P5-T02`, `P5-T07`, `P8-T06`, `P12-T06`, `P12-T07` |
| `V19-R27` | `P0-T01`, `P0-T02`, `P0-T04`, `P1-T02`, `P2-T03`, `P2-T04`, `P5-T01`, `P5-T05`, `P5-T06`, `P6-T08`, `P12-T06`, `P12-T07` |
| `V19-R28` | `P0-T01`, `P0-T02`, `P10-T02`, `P10-T03`, `P10-T04`, `P10-T05`, `P12-T06`, `P12-T07` |
| `V19-R29` | `P0-T01`, `P0-T02`, `P3-T01`, `P3-T02`, `P7-T01`, `P10-T01`, `P10-T06`, `P12-T06`, `P12-T07` |
| `V19-R30` | `P0-T01`, `P0-T02`, `P3-T04`, `P5-T01`, `P5-T02`, `P5-T03`, `P5-T04`, `P5-T08`, `P6-T02`, `P7-T05`, `P11-T02`, `P12-T02`, `P12-T06`, `P12-T07` |
| `V19-R31` | `P0-T01`, `P0-T02`, `P4-T04`, `P5-T02`, `P5-T07`, `P8-T07`, `P11-T05`, `P12-T06`, `P12-T07` |
| `V19-R32` | `P0-T01`, `P0-T02`, `P3-T03`, `P3-T06`, `P5-T02`, `P5-T07`, `P8-T07`, `P9-T06`, `P9-T07`, `P12-T06`, `P12-T07` |
| `V19-R33` | `P0-T01`, `P0-T02`, `P3-T06`, `P5-T07`, `P9-T05`, `P12-T06`, `P12-T07` |
| `V19-R34` | `P0-T01`, `P0-T02`, `P8-T01`, `P8-T02`, `P8-T03`, `P8-T05`, `P12-T06`, `P12-T07` |
| `V19-R35` | `P0-T01`, `P0-T02`, `P8-T04`, `P12-T06`, `P12-T07` |
| `V19-R36` | `P0-T01`, `P0-T02`, `P9-T05`, `P12-T06`, `P12-T07` |
| `V19-R37` | `P0-T01`, `P0-T02`, `P9-T06`, `P12-T06`, `P12-T07` |
| `V19-R38` | `P0-T01`, `P0-T02`, `P0-T04`, `P2-T01`, `P2-T04`, `P3-T06`, `P3-T07`, `P5-T05`, `P6-T01`, `P6-T05`, `P6-T06`, `P6-T07`, `P11-T01`, `P11-T04`, `P11-T05`, `P11-T06`, `P12-T06`, `P12-T07` |
| `V19-R39` | `P0-T01`, `P0-T02`, `P0-T04`, `P2-T02`, `P6-T07`, `P11-T05`, `P12-T06`, `P12-T07` |
| `V19-R40` | `P0-T01`, `P0-T02`, `P8-T01`, `P9-T05`, `P9-T06`, `P11-T01`, `P11-T02`, `P11-T03`, `P11-T04`, `P12-T03`, `P12-T06`, `P12-T07` |
| `V19-R41` | `P0-T01`, `P0-T02`, `P7-T05`, `P11-T01`, `P11-T03`, `P12-T03`, `P12-T06`, `P12-T07` |
| `V19-R42` | `P0-T01`, `P0-T02`, `P3-T04`, `P11-T05`, `P12-T06`, `P12-T07` |
| `V19-R43` | `P0-T01`, `P0-T02`, `P0-T03`, `P0-T04`, `P0-T05`, `P1-T04`, `P2-T01`, `P2-T02`, `P2-T05`, `P4-T01`, `P4-T05`, `P6-T08`, `P7-T06`, `P10-T01`, `P10-T04`, `P10-T06`, `P12-T01`, `P12-T02`, `P12-T03`, `P12-T04`, `P12-T06`, `P12-T07` |
| `V19-R44` | `P0-T01`, `P0-T02`, `P0-T05`, `P1-T01`, `P1-T03`, `P1-T05`, `P6-T04`, `P6-T05`, `P8-T02`, `P8-T05`, `P8-T06`, `P10-T02`, `P10-T05`, `P12-T05`, `P12-T06`, `P12-T07` |
| `V19-R45` | `P0-T01`, `P0-T02`, `P1-T03`, `P1-T04`, `P1-T05`, `P2-T05`, `P10-T05`, `P11-T04`, `P12-T05`, `P12-T06`, `P12-T07` |
| `V19-R46` | `P0-T01`, `P0-T02`, `P5-T03`, `P5-T04`, `P5-T08`, `P12-T02`, `P12-T06`, `P12-T07` |
| `V19-R47` | `P0-T01`, `P0-T02`, `P0-T05`, `P1-T01`, `P4-T01`, `P4-T02`, `P4-T06`, `P6-T08`, `P9-T07`, `P10-T02`, `P10-T03`, `P11-T02`, `P11-T06`, `P12-T04`, `P12-T06`, `P12-T07` |
| `V19-R48` | `P0-T01`, `P0-T02`, `P0-T03`, `P0-T05`, `P2-T05`, `P7-T02`, `P7-T03`, `P7-T04`, `P7-T06`, `P8-T01`, `P10-T06`, `P11-T04`, `P12-T01`, `P12-T02`, `P12-T03`, `P12-T04`, `P12-T05`, `P12-T06`, `P12-T07` |

## 37. Appendix B: Task index

| Task | Phase | Title | Role | Migration epoch | Depends on |
| --- | --- | --- | --- | --- | --- |
| `P0-T01` | `P0` | Register the v19 validation-overhead implementation plan | `project-system-director@0.2.0` | `legacy` | none |
| `P0-T02` | `P0` | Materialize the v19 recommendation backlog and dependency graph | `project-control-maintainer@0.2.0` | `legacy` | `P0-T01` |
| `P0-T03` | `P0` | Capture a reproducible v19 baseline benchmark receipt | `process-integrity-auditor@0.1.0` | `legacy` | `P0-T02` |
| `P0-T04` | `P0` | Build the legacy validation invocation and obligation graph | `process-integrity-auditor@0.1.0` | `legacy` | `P0-T03` |
| `P0-T05` | `P0` | Freeze v19 safety, runtime, CI, and output budgets | `project-system-director@0.2.0` | `legacy` | `P0-T04` |
| `P1-T01` | `P1` | Define validation evidence identity and epistemic classes | `project-control-maintainer@0.2.0` | `legacy` | `P0-T05` |
| `P1-T02` | `P1` | Define canonical gate IDs and same-scope supersedence contracts | `validator-engineer@0.2.0` | `legacy` | `P1-T01` |
| `P1-T03` | `P1` | Build the legacy-to-consolidated failure-mode equivalence corpus | `validator-engineer@0.2.0` | `legacy` | `P1-T02` |
| `P1-T04` | `P1` | Instrument gate invocations, scopes, tree hashes, and nested calls | `validator-engineer@0.2.0` | `legacy` | `P1-T03` |
| `P1-T05` | `P1` | Create shadow-comparison and rollback control | `process-integrity-auditor@0.1.0` | `legacy` | `P1-T04` |
| `P2-T01` | `P2` | Consolidate the Makefile research-control core and diff pair | `validator-engineer@0.2.0` | `legacy_consolidated` | `P1-T05` |
| `P2-T02` | `P2` | Consolidate local-runner and checkpoint same-scope research-control pairs | `validator-engineer@0.2.0` | `legacy_consolidated` | `P2-T01` |
| `P2-T03` | `P2` | Consolidate standalone changed-claim checks where the integrated diff gate is equivalent | `validator-engineer@0.2.0` | `legacy_consolidated` | `P2-T02` |
| `P2-T04` | `P2` | Update skill and role obligation wording after direct consolidation | `project-control-maintainer@0.2.0` | `legacy_consolidated` | `P2-T03` |
| `P2-T05` | `P2` | Audit first-wave equivalence and measured savings | `process-integrity-auditor@0.1.0` | `legacy_consolidated` | `P2-T04` |
| `P3-T01` | `P3` | Extract a write-only memory synchronization operation | `memory-system-maintainer@0.2.0` | `legacy_consolidated` | `P2-T05` |
| `P3-T02` | `P3` | Extract memory-core validation as a pure read-only gate | `memory-system-maintainer@0.2.0` | `legacy_consolidated` | `P3-T01` |
| `P3-T03` | `P3` | Separate publication and local-retrieval validation ownership | `memory-system-maintainer@0.2.0` | `legacy_consolidated` | `P3-T02` |
| `P3-T04` | `P3` | Implement true documentation-scoped memory modes or retire them | `memory-system-maintainer@0.2.0` | `legacy_consolidated` | `P3-T03` |
| `P3-T05` | `P3` | Remove bootstrap-then-validate duplication from workflows and checkpoint stabilization | `memory-system-maintainer@0.2.0` | `legacy_consolidated` | `P3-T04` |
| `P3-T06` | `P3` | Refactor `validate-memory` into provisioning, sync, core, doctor, and test-shard targets | `project-control-maintainer@0.2.0` | `legacy_consolidated` | `P3-T05` |
| `P3-T07` | `P3` | Move environment provisioning out of all validation entry points | `project-control-maintainer@0.2.0` | `legacy_consolidated` | `P3-T06` |
| `P4-T01` | `P4` | Define common validation-run and gate-result receipt schemas | `project-control-maintainer@0.2.0` | `legacy` | `P3-T07` |
| `P4-T02` | `P4` | Implement the common compact reporter and bounded-output library | `validator-engineer@0.2.0` | `shadow_planner` | `P4-T01` |
| `P4-T03` | `P4` | Add compact task-index validation output | `validator-engineer@0.2.0` | `shadow_planner` | `P4-T02` |
| `P4-T04` | `P4` | Add compact route-signature and route-orbit diagnostic output | `validator-engineer@0.2.0` | `shadow_planner` | `P4-T03` |
| `P4-T05` | `P4` | Adapt research-control, memory, and project-control gates to compact receipts | `validator-engineer@0.2.0` | `shadow_planner` | `P4-T04` |
| `P4-T06` | `P4` | Update local-agent summary-first consumption and receipt-expansion rules | `project-control-maintainer@0.2.0` | `shadow_planner` | `P4-T05` |
| `P5-T01` | `P5` | Define the declarative validation-gate manifest schema | `project-control-maintainer@0.2.0` | `shadow_planner` | `P4-T06` |
| `P5-T02` | `P5` | Populate the initial canonical validation-gate manifest | `validator-engineer@0.2.0` | `shadow_planner` | `P5-T01` |
| `P5-T03` | `P5` | Extend change classification with stable path-family tags | `validator-engineer@0.2.0` | `shadow_planner` | `P5-T02` |
| `P5-T04` | `P5` | Implement the deterministic affected-plan builder | `validator-engineer@0.2.0` | `shadow_planner` | `P5-T03` |
| `P5-T05` | `P5` | Compile role and skill declarations into validation obligations | `project-control-maintainer@0.2.0` | `shadow_planner` | `P5-T04` |
| `P5-T06` | `P5` | Implement conditional supersedence and evidence-identity deduplication | `validator-engineer@0.2.0` | `shadow_planner` | `P5-T05` |
| `P5-T07` | `P5` | Define and implement the five validation profiles | `project-system-director@0.2.0` | `shadow_planner` | `P5-T06` |
| `P5-T08` | `P5` | Create the lean change matrix, plan explanation, and fail-closed path tests | `process-integrity-auditor@0.1.0` | `shadow_planner` | `P5-T07` |
| `P6-T01` | `P6` | Implement the read-only validation DAG executor | `validator-engineer@0.2.0` | `shadow_planner` | `P5-T08` |
| `P6-T02` | `P6` | Implement mutator barriers and bounded synchronization stabilization | `validator-engineer@0.2.0` | `shadow_planner` | `P6-T01` |
| `P6-T03` | `P6` | Implement the cheap working-tree precheck | `validator-engineer@0.2.0` | `shadow_planner` | `P6-T02` |
| `P6-T04` | `P6` | Implement final staged-tree planning and acceptance | `validator-engineer@0.2.0` | `shadow_planner` | `P6-T03` |
| `P6-T05` | `P6` | Integrate the planner and executor into checkpointing | `validator-engineer@0.2.0` | `shadow_planner` | `P6-T04` |
| `P6-T06` | `P6` | Convert repo-local skills to planner profile wrappers | `project-control-maintainer@0.2.0` | `shadow_planner` | `P6-T05` |
| `P6-T07` | `P6` | Convert Make and the local full runner to planner wrappers | `project-control-maintainer@0.2.0` | `shadow_planner` | `P6-T06` |
| `P6-T08` | `P6` | Implement aggregate transaction receipts and obligation coverage reports | `validator-engineer@0.2.0` | `shadow_planner` | `P6-T07` |
| `P7-T01` | `P7` | Refactor dependency-graph extraction for reusable snapshots | `validator-engineer@0.2.0` | `shadow_planner` | `P6-T08` |
| `P7-T02` | `P7` | Reuse one live graph build across property assertions | `validator-engineer@0.2.0` | `shadow_planner` | `P7-T01` |
| `P7-T03` | `P7` | Combine dependency-graph CLI fresh and stale behavior into one lifecycle test | `validator-engineer@0.2.0` | `shadow_planner` | `P7-T02` |
| `P7-T04` | `P7` | Move dependency-graph determinism to a small synthetic repository | `validator-engineer@0.2.0` | `shadow_planner` | `P7-T03` |
| `P7-T05` | `P7` | Path-trigger graph validation and retain one scheduled live double-build | `validator-engineer@0.2.0` | `shadow_planner` | `P7-T04` |
| `P7-T06` | `P7` | Benchmark and audit dependency-graph failure-mode coverage | `process-integrity-auditor@0.1.0` | `shadow_planner` | `P7-T05` |
| `P8-T01` | `P8` | Split the broad research-control tests into focused shards | `validator-engineer@0.2.0` | `shadow_planner` | `P7-T06` |
| `P8-T02` | `P8` | Retain exactly one primary live full research-control acceptance test | `validator-engineer@0.2.0` | `shadow_planner` | `P8-T01` |
| `P8-T03` | `P8` | Inject validation receipts into continuation behavior tests | `validator-engineer@0.2.0` | `shadow_planner` | `P8-T02` |
| `P8-T04` | `P8` | Build one immutable metrics report per test class and run | `validator-engineer@0.2.0` | `shadow_planner` | `P8-T03` |
| `P8-T05` | `P8` | Isolate checkpoint tests from live repository validation | `validator-engineer@0.2.0` | `shadow_planner` | `P8-T04` |
| `P8-T06` | `P8` | Implement a narrow validated routing snapshot | `validator-engineer@0.2.0` | `shadow_planner` | `P8-T05` |
| `P8-T07` | `P8` | Cache advisory route diagnostics and remove them from default blocking paths | `validator-engineer@0.2.0` | `shadow_planner` | `P8-T06` |
| `P9-T01` | `P9` | Add dependency injection and minimal-fixture builders to support-traceability validators | `validator-engineer@0.2.0` | `shadow_planner` | `P8-T07` |
| `P9-T02` | `P9` | Replace v1 support-traceability full-repository copies with minimal fixtures | `validator-engineer@0.2.0` | `shadow_planner` | `P9-T01` |
| `P9-T03` | `P9` | Replace v18 support-traceability full-repository copies with minimal fixtures | `validator-engineer@0.2.0` | `shadow_planner` | `P9-T02` |
| `P9-T04` | `P9` | Perform v1-to-v18 traceability retirement parity assessment | `process-integrity-auditor@0.1.0` | `shadow_planner` | `P9-T03` |
| `P9-T05` | `P9` | Convert memory-system unit coverage to miniature repositories and isolate live acceptance | `memory-system-maintainer@0.2.0` | `shadow_planner` | `P9-T04` |
| `P9-T06` | `P9` | Convert Obsidian and SQLite tests to miniature repositories and isolate live acceptance | `memory-system-maintainer@0.2.0` | `shadow_planner` | `P9-T05` |
| `P9-T07` | `P9` | Implement the local-retrieval doctor profile and checkpoint separation | `memory-system-maintainer@0.2.0` | `shadow_planner` | `P9-T06` |
| `P10-T01` | `P10` | Implement the shared immutable repository snapshot | `validator-engineer@0.2.0` | `shadow_planner` | `P9-T07` |
| `P10-T02` | `P10` | Define the conservative exact-tree cache contract | `project-control-maintainer@0.2.0` | `shadow_planner` | `P10-T01` |
| `P10-T03` | `P10` | Implement cache storage, lookup, integrity, and eviction | `validator-engineer@0.2.0` | `shadow_planner` | `P10-T02` |
| `P10-T04` | `P10` | Integrate exact-tree cache lookup with the executor | `validator-engineer@0.2.0` | `shadow_planner` | `P10-T03` |
| `P10-T05` | `P10` | Run cache invalidation, isolation, and adversarial safety tests | `process-integrity-auditor@0.1.0` | `shadow_planner` | `P10-T04` |
| `P10-T06` | `P10` | Benchmark shared snapshots and cold and warm cache behavior | `process-integrity-auditor@0.1.0` | `shadow_planner` | `P10-T05` |
| `P11-T01` | `P11` | Design the manifest-driven CI job and shard matrix | `validator-engineer@0.2.0` | `shadow_planner` | `P10-T06` |
| `P11-T02` | `P11` | Implement CI shards, path filters, and receipt artifacts | `validator-engineer@0.2.0` | `shadow_planner` | `P11-T01` |
| `P11-T03` | `P11` | Deduplicate the parallel memory CI signal and add unfiltered scheduled full validation | `validator-engineer@0.2.0` | `shadow_planner` | `P11-T02` |
| `P11-T04` | `P11` | Run authoritative shadow comparison and cut over to planner orchestration | `process-integrity-auditor@0.1.0` | `planner_authoritative` | `P11-T03` |
| `P11-T05` | `P11` | Retire duplicate command owners, default diagnostics, misleading modes, and compatibility aliases | `project-control-maintainer@0.2.0` | `planner_authoritative` | `P11-T04` |
| `P11-T06` | `P11` | Update contributor, operator, test, memory, and project-control documentation | `documentation-curator@2.0.0` | `planner_authoritative` | `P11-T05` |
| `P12-T01` | `P12` | Benchmark the post-v19 full suite and gate profiles | `process-integrity-auditor@0.1.0` | `planner_authoritative` | `P11-T06` |
| `P12-T02` | `P12` | Benchmark representative affected edits and governed checkpoints | `process-integrity-auditor@0.1.0` | `planner_authoritative` | `P12-T01` |
| `P12-T03` | `P12` | Measure CI critical path, runner compute, and scheduled-full behavior | `process-integrity-auditor@0.1.0` | `planner_authoritative` | `P12-T02` |
| `P12-T04` | `P12` | Audit agent-output and receipt exposure against token budgets | `process-integrity-auditor@0.1.0` | `planner_authoritative` | `P12-T03` |
| `P12-T05` | `P12` | Run the final failure-mode mutation and non-negotiable safeguard audit | `validator-engineer@0.2.0` | `planner_authoritative` | `P12-T04` |
| `P12-T06` | `P12` | Audit final coverage of all v19 recommendations | `process-integrity-auditor@0.1.0` | `planner_authoritative` | `P12-T05` |
| `P12-T07` | `P12` | Publish the v19 integration handoff and restore the ordinary v18 research route | `director-of-research@0.3.0` | `planner_authoritative` | `P12-T06` |

## 38. Appendix C: Representative change-family matrix

| Change family | Required fast feedback | Required affected or checkpoint work | Full or scheduled backstop |
| --- | --- | --- | --- |
| Pure Python validator | Classifier, syntax, affected unit tests | Affected adapter and orchestration tests; staged diff if governed | Policy-fast plus relevant integration shard |
| Research-control YAML or registry | Classifier, changed claims, schema | Staged research-control diff, relevant frontier or index | Full research-control integration |
| Registered Markdown | Classifier, documentation impact, changed claims | Memory core, publication or Mermaid only when applicable | Full derivative freshness |
| Registered TeX without required PDF | Claim and metric-use checks as applicable | Memory core and scientific checker | Full scientific support |
| Registered TeX with required PDF | Same as above | Targeted PDF build, restage, memory core | Full scientific support and derivative freshness |
| HTML explainer or spec | Spec depth, publication, Mermaid if present | Memory registration and page-specific visual evidence | Publication shard |
| Memory implementation | Focused memory unit shard | Memory sync, core, live acceptance when affected | Full memory shard and scheduled doctor |
| Dependency graph renderer or input | Graph unit and synthetic tests | One graph freshness lifecycle | Scheduled live double-build |
| Task-index renderer or input | Renderer tests | Compact task-index freshness | Full task-index historical audit |
| Scientific checker or fixture | Direct checker and focused tests | Traceability and staged claim or research-control gates | Scientific-support shard |
| Local retrieval only | Doctor | No checkpoint authority unless maintenance task opts in | Scheduled local-retrieval health |
| CI, Make, skill, or planner | Planner, wrapper, and manifest tests | Shadow equivalence and staged project-control diff | Full orchestration shard |
| Unknown governed path | Classification error or full fallback | Blocking until mapped | Scheduled full detects mapping gaps |

## 39. Appendix D: Test-shard ownership

| Shard | Primary modules and responsibilities |
| --- | --- |
| `policy-fast` | Classifier, claim language, schemas, planner, profiles, reporting, cache unit tests |
| `research-control-integration` | One live full spine, active state, continuation integration, checkpoint integration |
| `dependency-graph` | Shared live graph, CLI lifecycle, synthetic determinism, scheduled live double-build |
| `memory-core` | Miniature memory tests plus live validate-only and idempotence |
| `publication` | Spec depth, publication process, Mermaid, HTML, documentation surfaces |
| `scientific-support` | Finite and typed checkers, target-import, PNF, traceability |
| `local-retrieval` | Obsidian, SQLite, search, local warnings, doctor |
| `orchestration` | Make wrappers, skills, executor, staged planner, receipts, legacy comparison |
| `scheduled-full` | Union of all blocking shards, cache bypass audit, live determinism, doctor health |

## 40. Appendix E: Rollback matrix

| Failure | Immediate response | Authority after rollback |
| --- | --- | --- |
| Legacy FAIL but planner PASS | Disable planner authority and cache; restore legacy wrapper | Legacy commands |
| Missing hard finding | Roll back responsible adapter, mapping, or supersedence rule | Legacy or prior planner version |
| Wrong staged tree or index restoration | Abort checkpoint, restore entry index, disable checkpoint planner | Legacy checkpoint |
| Cache false hit | Disable cache globally, clear local cache, run uncached full audit | Planner without cache or legacy |
| Path-filter false negative | Remove filter or select full for that family | Conservative planner |
| Compact output hides actionable failure | Restore legacy renderer for that gate while keeping full receipts | Same semantic gate |
| CI required-check ambiguity | Restore legacy required job and keep new shards informational | Legacy CI |
| Performance hard-guard miss without safety issue | Retain correctness, route bounded optimization | Current safe authority |
| Safety mutation false PASS | Release blocker, roll back to last passing epoch | Last proven safe epoch |
| Documentation drift | Repair source documentation and regenerate, never hand-edit derivative | Current safe implementation |

## 41. Appendix F: Plan quality checks

Before registering this file, validate:

- The authority marker is `control`.
- The filename and plan ID are v19.
- Every recommendation ID V19-R01 through V19-R48 appears in the inventory and coverage appendix.
- Every task ID is unique.
- Every dependency references an existing earlier or explicitly supersedable task.
- The backlog dependency graph is acyclic.
- Every task has one role, objective, source inspection set, write scope, actions, validations, done criteria, rollback criteria, and handoff.
- The final task preserves or explicitly blocks the ordinary research route.
- No task authorizes physics promotion.
- No em dash or unsupported Unicode control character is required for semantics.
- Markdown code fences are balanced.
- Tables have consistent column counts.
- Generated wiki and registry derivatives are produced only through approved tooling.

## 42. Logical first implementation packet

The first bounded implementation wave after registration should be P1 and P2, with particular priority on:

1. Same-scope research-control core and diff consolidation.
2. Same-scope changed-claim consolidation after equivalence proof.
3. Invocation tracing and rollback policy.
4. Measured before and after evidence.

The dependency-graph test refactor and compact output work should follow immediately because they address the dominant time and token costs while preserving the current invariants.
