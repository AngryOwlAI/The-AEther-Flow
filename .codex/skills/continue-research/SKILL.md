---
name: continue-research
description: Resolve tracked research-control state and set up or execute one bounded AgentJob per invocation.
---

# Continue Research

Use this skill for research-control continuation in Flow.

## Control Principle

The Director of Research is a first-class phase. Codex acts as Director only to
author the research-path decision; scripts validate boundaries and checkpoint
state. The Director chooses the next bounded step, roles constrain execution,
skills provide procedures, and gates control claim promotion.

## Workflow

1. Read `AGENTS.md` and `research_control/AGENTS.md`.

   Before any Director routing decision, AgentJob creation, or physics
   claim/control conclusion, run the memory preflight refresh:

   ```zsh
   .venv/bin/python scripts/research_control/continue_research_memory_preflight.py --json
   ```

   This command runs the memory status check, refreshes the local Obsidian
   vault notes, raw mirrors, semantic extracts, and SQLite retrieval index when
   `local_retrieval_status` reports local-cache drift, then reports the final
   status summary. The receipt-facing status command remains:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json
   ```

   Then run at least one targeted memory query against the refreshed retrieval
   layer:

   ```zsh
   .venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup <object-id-or-path> --json
   .venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search "<targeted phrase>" --limit 10 --json
   ```

   Use the memory system only as navigation. After any memory hit that
   influences routing, claims, source selection, or project-control changes,
   inspect the canonical source file or the source registry row named by the
   hit. New AgentJobs and completions created after
   `2026-06-18T15:33:00Z` must include a `memory_preflight` receipt with the
   status command, status summary, query commands, returned object IDs,
   canonical source inspections, source registries, canonical paths, and source
   hashes. If the preflight refresh ran, record the refresh command and before
   or after local-retrieval status in the AgentJob or completion evidence.
   Obsidian, wiki notes, semantic extracts, SQLite memory, and `.local/`
   remain retrieval layers only; they are not authority.

2. Resolve tracked state and request the Director context packet:

   ```zsh
   .venv/bin/python scripts/research_control/continue_research.py
   ```

   The script emits JSON by default. Use `--summary` only for a human-readable
   rendering of the same packet.

3. If the packet boundary is `director_decision_required`, enter Director of
   Research mode under `.agents/roles/research_ops/director-of-research.v0.3.0.md`.
   Write or reuse exactly one Director Decision Record and one AgentJob. The
   Director may create a new task only when tracked state proves that the active
   task is completed, blocked, human-gated, or the latest handoff explicitly
   requires a separate task.

4. If an existing pending or active AgentJob matches `program_state.yaml`, the
   latest DDR, the active task, and the job registry, reuse it. If pending jobs
   conflict, stop or supersede through a tracked Director/Process Integrity
   repair decision. Do not rewrite activated DDRs or AgentJobs.

5. Use an execution-role record for the AgentJob. Registered roles, task
   overlays, and one-job provisional roles are represented by
   `execution_role_ref` records under
   `research_control/tasks/<task_id>/roles/` and registered in
   `registries/ROLE_EXECUTION_REGISTRY.csv`. Base role contracts remain stable;
   task-specific adaptation must be explicit. Registered roles are stable
   templates and guidance, not a rigid routing menu. Use `registered_role` for
   direct template use, `task_overlay` for a modified registered role that
   keeps the same identity, and `one_job_provisional_role` for a brand-new
   one-job role or a template-derived role whose modification needs a distinct
   temporary identity. Protected expansion requires a human gate: claim
   promotion, canonical ontology authority, benchmark-status authority, Gate
   Chair authority, or permanent role registration.

   For every new physics research AgentJob created after
   `2026-06-17T04:08:16Z`, the Director must enable
   `role_decomposition.mode: "parent_child_parallel_synthesis"`. Keep exactly
   one outer AgentJob and the same single execution-role record. The parent and
   two children are internal execution units:

   - parent: `physicist_mathematician_philosopher`
   - child A: `physicist_mathematician`
   - child B: `physicist_philosopher`

   The children inherit the selected role authority, claim boundary, forbidden
   source classes, and write-path allowlist. They do not become independent
   AgentJobs and may not expand authority. The parent must write the conflict
   review artifact, preserve unresolved limitations, and produce one fused
   old-style final artifact. The completion must list the child outputs,
   conflict review, and fusion summary under `parent_child_synthesis`. A PASS
   completion may not contain unresolved blocking conflicts.

   For every new physics research AgentJob created after
   `2026-06-17T15:46:25Z`, declare `target_derivation_milestone` and
   `milestone_burden` from `research_control/design/gr_derivation_burden_map.md`.
   If no derivation milestone can be named, route the work as documentation,
   methodology, validation, or project-system maintenance rather than physics
   derivation work.

6. Execute exactly one authorized AgentJob unless a stop condition applies:
   human gate required, validation failure, no role fit, authority expansion,
   write-path conflict, or protected ontology/authority expansion requiring a
   human gate.

   If the active blocker is a missing datum, metric, witness family,
   computation, or experiment and the repository does not contain it, do not
   treat local absence alone as a terminal result when tracked state or
   explicit user instruction authorizes research or construction. The Director
   may create one bounded non-promotional AgentJob for external primary-source
   search, source-acquisition design, bounded theoretical calculation,
   mathematical construction, or experiment design. The output must distinguish
   established external literature from new project construction, cite
   external materials in APA 7 format when used, remain draft/control, and
   preserve all claim-promotion gates.

   For theoretical physics continuation, missing local data or missing
   experiment access is not a generic pause condition. If continuation requires
   selecting among a source-side selector primitive, source-side irrelevance
   theorem, concrete `Resp_lc` witness, distinct scoped no-go question, bounded
   theoretical calculation, or another new mathematical payload, and no single
   execution role is already determined, the Director must create one bounded
   `theoretical-continuation-selector@0.1.0` AgentJob. That job outputs
   `theoretical_decision_output` and preserves all promotion blocks.

   Future pause-like routing is reserved for protected human-gated authority,
   especially canonical ontology edits or ontology adoption. Record that route
   as `human_gated_ontology_change_required` or the applicable human-gated
   route, not as generic `controlled_pause`.

   If the active derivation milestone is blocked because the current ontology
   does not derive a required source-side law, selector, discriminator,
   transition rule, robustness rule, or equivalent primitive, the Director may
   use the named route `ontology-law-research-packet`. The trigger
   classification is `derivation_critical_missing_source_law`. The route is
   not available for `ordinary_gap` work, including missing documentation,
   missing registry rows, generated derivative drift, missing citations,
   computations available under existing ontology, or proof-detail work under
   existing ontology. The route is also not available for
   `workflow_inconvenience`, including tedious casework, slow literature
   review, awkward templates, or strict validation friction.

   Underdetermination language must stay exact. A packet may state "current
   ontology does not derive X." It must not state "therefore X is impossible"
   unless a separate no-go theorem or scoped obstruction supports that claim.
   When conservative source-side extension remains possible, use the status
   pair `blocked_adoption_open_continuation`: current adoption is blocked while
   same-milestone continuation remains open. Candidate-law status labels are
   `draft/control`, `proposal-only`, `source-extension data`,
   `canonical-ontology candidate`, `adopted`, `rejected`, and `human-gated`.
   `canonical-ontology candidate`, `adopted`, ontology-edit, benchmark,
   `M_src`, metric, coupling, Einstein-equation, and Gate Chair authority
   claims remain protected until explicit human-gated authorization.

   When using `ontology-law-research-packet`, keep one outer physics AgentJob
   for the invocation. The route label is not a new permanent role. Bind the
   AgentJob through the normal execution-role record to the narrowest active
   role that fits the immediate payload: Theoretical Continuation Selector for
   packet selection, Ontology Formalizer for source-law definitions and proof
   obligations, Candidate Constructor for bounded finite or local witnesses,
   Smuggling Auditor for hidden target-import audits, or Refuter for collapse,
   nonuniqueness, inverse, cocycle, and finite-variation stress tests. Use a
   `task_overlay` for route-specific constraints; use permanent role
   registration only through the project-system improvement loop.

   The parent-child synthesis rule still applies. The Physicist-Mathematician
   child defines formal objects, domains, maps, and proof obligations. The
   Physicist-Philosopher child separates ontology, mathematical model,
   empirical recovery, and benchmark status. The parent fuses consensus,
   unique contributions, and unresolved conflicts into one output. Children
   inherit the single outer execution-role record and may not add authority,
   claim boundaries, write paths, or child AgentJobs.

   For Refuter stress tests created after the bridge-or-fail loop-control
   policy activation, the completion must classify the result as one of:
   `concrete_witness_path`, `source_side_irrelevance_theorem_path`,
   `bridge_facing_candidate_path`,
   `repeated_unmet_burdens_no_new_payload`, or `scoped_obstruction`.
   If repeated burdens or a scoped obstruction remain, the next route must be
   one of: Candidate Constructor bridge attempt, Ontology Formalizer concrete
   witness construction, Refuter scoped no-go or obstruction, Theoretical
   Continuation Selector decision packet, human-gated ontology-change
   requirement, or a human-gated Gate Chair closure or suspension proposal. Do
   not route back to another generic Ontology Formalizer obligation packet.

   Future physics completions must include `distance_to_gr_status`. After
   `2026-06-17T15:46:25Z`, that matrix must use the expanded burden list from
   `research_control/design/gr_derivation_burden_map.md`, every physics
   completion must include at least one `new_mathematical_payload`, and
   repeated-burden or scoped-obstruction Refuter completions must include
   `freeze_criteria_status`. Future bridge-facing Candidate Constructor
   completions must include `bridge_attempt_status` naming either a candidate
   map or the missing primitive and preserving all downstream promotion blocks.
   Future Theoretical Continuation Selector completions must include
   `theoretical_decision_output`; source-extension packets must classify the
   extension category, and finite toy metric-response packets must state the
   finite source set, response relation, metric-response analogue, and
   invariance checks.

7. After a state-changing AgentJob completion, create the durable response
   transaction: role output artifact if any, completion record, registry updates,
   new handoff pair, and `program_state.yaml` update when state changes.
   The completion or handoff may record `project_improvement_signals`, but
   `/continue-research` must not opportunistically repair project-system
   machinery unless the active AgentJob explicitly authorizes that boundary.
   After the completion record and normal `handoff-####.yaml/md` pair exist,
   inspect `project_improvement_signals` in both sources. If all entries are
   blank placeholders, no bridge is required. If one or more nonblank signals
   exist, keep the normal research handoff as the research-continuation
   authority, ensure every signal has a concrete row in
   `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv`, generate one
   project-improvement handoff sidecar under
   `research_control/project_improvement_handoffs/`, record that sidecar in the
   source `project_improvement_bridge` blocks, run
   `scripts/project_control/collect_project_improvement_signals.py
   --validate-emitted`, and report the research result before the improvement
   sidecar. The sidecar instructs operators to run `/improve-project-system`
   separately for project-system repair.
   If the AgentJob sets `resolves_signal_routing: true`, its completion must
   preserve repo-relative `resolver_snapshots.before` and
   `resolver_snapshots.after` paths to JSON output from
   `resolve_project_improvement.py --json` and include nonblank
   `routing_delta_summary`. Ordinary validator and documentation jobs do not
   need fresh resolver snapshots merely because future project-system work is
   visible.

8. Synchronize generated systems before commit by satisfying the named
   `memory_sync` obligation in
   `research_control/design/validation_obligation_resolution_policy_v1.md`.
   Use the policy's single current compatibility recipe; a skill or role that
   names the same obligation does not create another execution requirement.

   If a changed registered TeX source has `pdf_required=true`, build that
   specific PDF derivative, then rerun the bootstrap. HTML is synchronized
   through the HTML registry when HTML exists; generated HTML is created only
   when the AgentJob explicitly authorizes it from a registered Markdown spec.

9. Resolve post-execution obligations by gate ID under the same policy:
   `memory_core`, `documentation_impact`, `project_improvement_signals` when
   signals are emitted, `research_control_diff`, the task-selected test shard,
   and `git_diff_check`. Under the registered same-scope predicates,
   `research_control_diff` may also satisfy `research_control_core` and
   `claim_language_changed`; working-tree evidence never satisfies a staged-tree
   obligation. Direct precheckpoint commands are editing aids, not final
   acceptance, and must not be repeated merely because both this skill and a
   role declaration name an obligation.

10. Checkpoint only after a successful state-changing transaction. The
    checkpoint owns the `checkpoint_transaction` obligation and final staged
    acceptance:

    ```zsh
    .venv/bin/python scripts/research_control/checkpoint_research_transaction.py
    ```

    The checkpoint script captures preflight dirty state, blocks unrelated
    changes, classifies project-system impact, validates documentation impact,
    synchronizes generated systems, validates, stages only allowed transaction
    paths, and commits with a deterministic template. Push is never performed
    unless explicitly requested.

    If the classifier or documentation-impact validator blocks the checkpoint,
    run `/improve-project-system` for one bounded project-system AgentJob.

11. If the invocation is read-only, blocked, human-gated, or produces no file
    changes, report the state and do not create an empty commit.

## Checkpoint Boundaries

The checkpoint script globally allows only standard memory-system generated
registries, generated registry sidecars, and `wiki/indexes/**`. Source-specific
wiki notes, generated PDFs, generated HTML, execution-role records, and
`ROLE_EXECUTION_REGISTRY.csv` must be authorized by the AgentJob boundary.

If synchronization or validation fails, stage nothing, commit nothing, preserve
the working-tree evidence, and report failed commands, changed paths, active
task, active AgentJob, and the likely repair role.

## Reporting

Report the substantive research/control result first, then explain why the next
role follows from validated state. Do not reduce the final response to
orchestration mechanics.

Use APA 7 citations when DDRs, role artifacts, or handoffs cite documents or
materials. Pure registry metadata does not need APA citations.

Tracked `research_control/` state is authority. Local prompts, logs, previews,
or caches do not override tracked control files.
