---
schema_id: "AGENT_JOB_SCHEMA"
version: "0.1.0"
status: "active"
---

# AgentJob Schema

AgentJobs are strict YAML executable contracts. They are immutable after
creation.

## Required Fields

- `job_id`
- `task_id`
- `decision_id`
- `role_id`
- `role_version`
- `status`
- `requires_human_gate`
- `allowed_read_paths`
- `allowed_write_paths`
- `allowed_generated_paths`
- `forbidden_paths`
- `allowed_source_classes`
- `forbidden_source_classes`
- `approved_commands`
- `required_validators`
- `expected_outputs`
- `claim_boundary`

If the role is provisional, the job must include `provisional_role_contract`
with `expires_after_job_id` equal to the job ID.

For every AgentJob created after `2026-06-18T15:33:00Z`, the job must also
include `memory_preflight`. The completion record for that job must preserve a
matching `memory_preflight` receipt.

Required shape:

```yaml
memory_preflight:
  status_command: ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json"
  status_summary:
    vault_exists: true
    memory_index_exists: true
    source_object_count: 0
  queries:
    - command: ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup <object-id-or-path> --json"
      query_type: "lookup"
      query_text: "<object-id-or-path>"
      returned_object_ids:
        - "<canonical-source-object-id>"
  canonical_inspections:
    - object_id: "<canonical-source-object-id>"
      source_registry: "MARKDOWN_SOURCE_REGISTRY.csv"
      registry_path: "registries/MARKDOWN_SOURCE_REGISTRY.csv"
      canonical_path: "<repo-relative-source-path>"
      source_hash: "<sha256>"
  authority_note: "Obsidian, wiki notes, semantic extracts, and .local are retrieval layers only and not authority."
```

Every `returned_object_ids` entry that influences routing, claims, source
selection, or project-control changes must be an inspected canonical source
object ID from `MARKDOWN_SOURCE_REGISTRY.csv`, `TEX_SOURCE_REGISTRY.csv`,
`PDF_DERIVATIVE_REGISTRY.csv`, or `HTML_EXPLAINER_REGISTRY.csv`. Generated
wiki, semantic, Obsidian, relationship, and `.local` IDs are retrieval evidence;
they must not be listed as canonical memory-preflight returns. Each returned
canonical source ID must have a canonical inspection entry. `source_hash` must
match both the named source registry row and the current file bytes at
`canonical_path`.

For physics-facing AgentJobs, use explicit forbidden source classes rather than
empty placeholders. The expected vocabulary includes `canonical_ontology_write`,
`benchmark_promotion`, `physics_claim_promotion`, `source_law_adoption`,
`M_src_adoption`, `candidate_reconstruction`, `gate_chair_verdict`,
`completed_derivation_claim`, and `generated_derivative_authority`, with
additional packet-specific forbidden classes as needed.

## Prospective Physics-Payload Admission

Every AgentJob created after `2026-07-22T16:24:16Z` must include a
`physics_payload_admission` block conforming to
`research_control/design/physics_payload_admission_policy_v1.md`. Historical
AgentJobs without the block remain readable and valid.

The validator derives the expected path independently from the task taxonomy
and selected role. Tasks with scope `scientific`, `scientific_audit`, or
`mixed`, and jobs assigned to a physics role, use `admission_path: physics`.
Other jobs use `admission_path: project_system`. Declaring a different path is
an error.

All records require:

```yaml
physics_payload_admission:
  schema_id: "physics_payload_admission_v1"
  policy_id: "physics_payload_admission_policy_v1"
  admission_path: "physics"
  payload_type: "proof_step"
  candidate_family: "named candidate or source family"
  assumption_delta:
    - "explicit new removed narrowed or unchanged assumption"
  materiality_basis: "why this expected artifact is new payload"
  source_basis:
    - "canonical object ID or source path"
  expected_artifact_paths:
    - "repo-relative output path"
  process_receipts_excluded_from_payload:
    - "validator_pass"
    - "checkpoint_pass"
    - "documentation_receipt"
    - "role_or_route_selection"
  authority_limits:
    theorem_truth_inferred: false
    scientific_status_changed: false
    ontology_or_source_law_adopted: false
    distance_to_gr_changed: false
    physics_promotion_authorized: false
```

Physics `payload_type` values are `theorem`, `proof_step`, `countermodel`,
`source_law`, `external_result`, `independent_replication`,
`justified_ledger_delta`, `source_acquisition`, `precise_obstruction`,
`finite_witness`, `source_model`, `candidate_construction`, and
`route_decision`. `source_acquisition` additionally requires
`payload_details.acquisition_target` and `primary_source_requirement: true`.
`precise_obstruction` requires `payload_details.obstruction_scope` and
`global_no_go_claimed: false`. `route_decision` requires a real new decision
identity and evidence that it was not already encoded.

Project-system jobs use `payload_type: not_applicable`,
`candidate_family: not_applicable`, and a nonblank
`project_system_justification`. They do not count as physics progress.

This is an admission-shape gate. It does not evaluate theorem truth, validate a
candidate or source law, change scientific status, or authorize promotion.

## Prospective Family-Freeze Admission

Every physics-facing AgentJob created after `2026-07-22T17:25:51Z` must also
include a `family_freeze_admission` block conforming to the task-local P12-T02
policy and seed under `research_control/tasks/RT-20260722-013/artifacts/`.
Historical jobs remain readable, and project-system jobs remain on the
separate physics-payload `project_system` path.

The validator independently matches exact `family_id`,
`family_identity_sha256`, and `assumption_sha256es` against the five seeded
EqSrc family freezes. A matching candidate construction, audit, stress, or
repair route requires already tracked evidence in exactly one reopening class:
`new_primitive`, `new_theorem`, `new_variation_class`, or
`protected_decision`. Renaming or repackaging is barred. A materially distinct
theorem, primitive, variation-class, source-acquisition, or precise-
obstruction investigation may proceed without reopening when it explicitly
preserves the local freeze and does not reconstruct the frozen candidate.

```yaml
family_freeze_admission:
  schema_id: "family_freeze_route_admission_v1"
  policy_id: "family_freeze_reopening_policy_v1"
  route_id: "stable route identity"
  family_id: "candidate family identity"
  family_identity_sha256: "lowercase sha256"
  assumption_sha256es:
    - "lowercase sha256"
  route_kind: "candidate_construction"
  detected_match_basis:
    - "family_id"
    - "family_identity_sha256"
    - "assumption_sha256"
  reopening:
    requested: true
    class: "new_theorem"
    evidence_id: "stable evidence identity"
    evidence_path: "repo/relative/tracked/path"
    evidence_sha256: "lowercase sha256"
    material_delta: "why the evidence changes this exact route"
    opens_exact_family_id: "candidate family identity"
    automatic_adoption: false
    theorem_truth_inferred: false
    protected_human_authority: false
    theorem_id: "exact theorem identity"
    proposal_neutral: true
  authority_limits:
    local_family_freeze_preserved: true
    global_no_go_claimed: false
    automatic_candidate_adoption: false
    theorem_truth_inferred: false
    ontology_modified: false
    physics_promotion_authorized: false
```

For an unmatched family, `reopening.requested` is false. For a matched
materially distinct investigation, supply `distinct_branch.branch_identity`,
`material_difference_basis`, `reconstructs_frozen_candidate: false`, and
nonempty `expected_artifact_paths`, while keeping `reopening.requested: false`.
Protected decisions additionally require an exact human-gate identity and an
AgentJob that remains human-gated.

This gate validates identity, evidence presence, and exact source hashes. It
does not prove evidence true, adopt a primitive or candidate, infer a global
no-go result, modify ontology, or authorize physics promotion.

## Prospective Dual-Budget Allocation

Every AgentJob created at or after `2026-07-22T18:10:44Z` must include a
`dual_budget_allocation` block conforming to
`research_control/tasks/RT-20260722-014/artifacts/dual_budget_policy_v1.md`.
Historical jobs without the block remain readable. This is a project-control
accounting and acceptance gate, not a scientific claim gate.

The four categories are `physics_bearing`, `system_bearing`, `mixed`, and
`support_only`. Every job names exactly one `primary_budget`, and the two task
count credits must be 0 or 1 and sum to exactly 1. Mixed jobs must declare
nonempty, disjoint output and acceptance sets in both lanes; their secondary
lane does not create a second task-count credit.

```yaml
dual_budget_allocation:
  schema_id: "dual_budget_allocation_v1"
  policy_id: "dual_budget_policy_v1"
  category: "mixed"
  primary_budget: "physics"
  task_count_credit:
    physics: 1
    project_system: 0
  expected_durable_outputs:
    physics:
      - "research_control/tasks/<task>/artifacts/scientific-result.tex"
    project_system:
      - "research_control/tasks/<task>/artifacts/checker.py"
  acceptance_criteria:
    physics:
      - "bounded scientific obligation is discharged"
    project_system:
      - "checker fixture matrix passes"
  reporting_dimensions:
    - "task_count"
    - "elapsed_effort"
    - "compute"
    - "durable_outputs"
  resource_measurement:
    physics:
      elapsed_effort: {status: "not_measured", unit: "seconds"}
      compute: {status: "not_measured", unit: ""}
    project_system:
      elapsed_effort: {status: "not_measured", unit: "seconds"}
      compute: {status: "not_measured", unit: ""}
  blocked_physics_exception:
    active: false
    exception_id: ""
    evidence_path: ""
    evidence_sha256: ""
  authority_limits:
    system_success_counts_as_physics: false
    system_success_counts_as_distance_to_gr: false
    validator_pass_counts_as_physics: false
    route_selection_counts_as_physics: false
```

Missing elapsed effort or compute is `not_measured` with the `value` key
omitted (or JSON null in JSON surfaces); it is never represented as numeric
zero. An active blocked-physics exception needs
a stable ID, tracked repository-relative evidence path, and exact SHA-256. It
does not transfer project-system work into the physics budget.

A prospective completion must include `dual_budget_result_v1`, preserve the
admitted category, primary credit, lane-separated observed outputs and
accepted criteria, and the four false authority flags. System and support
success must keep `distance_to_gr_delta.changed: false`.

The P12-T03 accounting evaluator remains the normalized source for budget
classification. P12-T04 activates the separate prospective ordinary-route
hard guard described below.

## Prospective Ordinary-Route Guard Admission

Every AgentJob created after `2026-07-22T19:00:53Z` must include an
`ordinary_route_guard_admission` block conforming to the P12-T04 policy under
`research_control/tasks/RT-20260722-015/artifacts/`. The P12-T04
implementation AgentJob at the exact activation instant and all earlier jobs
remain readable without this block.

The admission binds the job to the immediately preceding ordinary research
handoff. That handoff must contain a passing `ordinary_route_guard` evaluation
whose selected plan ID and plan task match the job's `plan_id` and
`plan_task_id`. Historical V21 records may omit `plan_id` and default only to
the registered V21 plan. The handoff must normally be a tracked regular YAML
file at its exact SHA-256. A project-improvement sidecar cannot replace or
supersede it.

```yaml
ordinary_route_guard_admission:
  schema_id: "ordinary_route_guard_admission_v1"
  policy_id: "ordinary_route_guard_policy_v1"
  source_handoff_id: "handoff-0000"
  source_handoff_path: "research_control/handoffs/handoff-0000.yaml"
  source_handoff_sha256: "lowercase sha256"
  selected_plan_id: "recommendations_implementation_plan_continue_task-v22"
  selected_plan_task_id: "P0-T00"
  selected_plan_task_ref: "recommendations_implementation_plan_continue_task-v22:P0-T00"
  guard_outcome: "physics_bearing_route_selected"
  authority_limits:
    ordinary_research_handoff_authoritative: true
    project_system_sidecar_supersedes: false
    system_success_counts_as_physics: false
    system_success_counts_as_distance_to_gr: false
    scientific_status_changed: false
    physics_promotion_authorized: false
```

When a completed prior transaction cannot be checkpointed because a validator
or checkpoint-planner defect leaves its ordinary handoff untracked, one
separately admitted project-system repair may bind that exact repository
candidate through:

```yaml
checkpoint_recovery:
  schema_id: "ordinary_route_checkpoint_recovery_v1"
  status: "active"
  atomic_checkpoint_required: true
  source_handoff_id: "handoff-0000"
  source_handoff_path: "research_control/handoffs/handoff-0000.yaml"
  source_handoff_sha256: "lowercase sha256"
  prior_job_id: "AJ-RT-YYYYMMDD-NNN-001"
  prior_task_id: "RT-YYYYMMDD-NNN"
  blocker_path: "research_control/tasks/<prior-task>/artifacts/blocker.yaml"
  blocker_sha256: "lowercase sha256"
```

The prior AgentJob must be registered completed, its completion must retain a
pending checkpoint, and the exact source handoff, completion, and blocker must
be non-ignored repository candidates covered by the repair job's write
allowlist. This branch authorizes only one atomic recovery checkpoint. It does
not permit a plan/task mismatch, make an untracked handoff normal routing
authority, reuse a protected approval, or create scientific authority.

An exact protected human-route override is the only admission branch that may
permit a job's `plan_task_id` to differ from the source handoff selection. It
is fail-closed and applies only when a deterministic task-local
`protected_human_route_override_admission_v1.yaml` receipt binds all of the
following:

- the admitted job, protected job, exact plan task, and source ordinary
  handoff;
- one repository approval at its exact SHA-256, with `one_time_use: true`,
  `status: consumed`, and `consumed_by` plus `expires_at` equal to the
  protected job;
- the matching Director decision and consumed human-authorization artifact at
  exact hashes;
- the protected recursive-goal route receipt, including goal identity,
  generation, worker skill, plan task, route SHA-256, and idempotency key;
- for a separately routed checkpoint recovery, the immediate next recursive
  generation, `improve-project-system` worker identity, exact blocker hash,
  matching recovery strategy, and no approval reuse;
- the ordinary-route authority limits with every scientific, physics,
  Distance-to-GR, sidecar-supersedence, and promotion inference disabled.

The receipt path is deterministic:
`research_control/tasks/<task_id>/artifacts/protected_human_route_override_admission_v1.yaml`.
Jobs created after `2026-07-24T16:00:00Z` must also bind that receipt through
`ordinary_route_guard_admission.override_authority.receipt_path` and
`receipt_sha256`. The final staged checkpoint validation must see every bound
record in the Git index. A missing, ignored, symlinked, stale, mismatched,
broadened, unconsumed, reused, or non-immediate recovery chain fails.

```yaml
ordinary_route_guard_admission:
  schema_id: "ordinary_route_guard_admission_v1"
  policy_id: "ordinary_route_guard_policy_v1"
  source_handoff_id: "handoff-0000"
  source_handoff_path: "research_control/handoffs/handoff-0000.yaml"
  source_handoff_sha256: "lowercase sha256"
  selected_plan_task_id: "the source handoff selection"
  guard_outcome: "the source handoff guard outcome"
  override_authority:
    present: true
    schema_id: "protected_human_route_override_admission_v1"
    exact_plan_task_id: "the admitted protected plan task"
    receipt_path: "research_control/tasks/<task_id>/artifacts/protected_human_route_override_admission_v1.yaml"
    receipt_sha256: "lowercase sha256"
    validator_support_status: "protected_human_route_override_admission_v1"
  authority_limits:
    ordinary_research_handoff_authoritative: true
    project_system_sidecar_supersedes: false
    system_success_counts_as_physics: false
    system_success_counts_as_distance_to_gr: false
    scientific_status_changed: false
    physics_promotion_authorized: false
```

After three consecutive completed project-system tasks, the ordinary handoff
must select a dependency-ready physics-bearing task in its selected plan. A project-system task
may instead be selected only with an `ordinary_route_exception_receipt_v1`
that accounts for every dependency-ready science task and binds each active
blocking control failure to a tracked exact hash. `human_gate_required` is
verified directly against the registered selected-plan backlog. Other allowed failure
classes require an `ordinary_route_control_failure_v1` evidence record.

The guard emits an advisory warning at two consecutive project-system tasks
and hard-fails at three. It is project-control routing evidence only: neither a
passing guard, an exception, nor a selected physics route is scientific proof,
physics progress, Distance-to-GR progress, ontology authority, or promotion.

For every future physics research AgentJob created after
`2026-06-17T15:46:25Z`, the job must also include:

- `target_derivation_milestone`
- `milestone_burden`

`target_derivation_milestone` must be one of the milestones in
`research_control/design/gr_derivation_burden_map.md`. `milestone_burden`
must state the specific burden the job attempts to discharge. A task that
cannot name a derivation milestone should be routed as documentation,
methodology, validation, or project-system work rather than physics
derivation work.

Future physics AgentJobs may opt into the mathematical-decisiveness
completion schema by including:

```yaml
mathematical_decisiveness_contract_active_after: "2026-06-21T02:32:39Z"
mathematical_decisiveness_schema: ".agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md"
```

or by including:

```yaml
mathematical_decisiveness_contract:
  contract_path: "research_control/design/mathematical_decisiveness_completion_contract.md"
  schema_path: ".agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md"
  enforcement_mode: "hard_failure"
  active_after: "2026-06-21T02:32:39Z"
```

Opt-in support is prospective. Missing or malformed mathematical-decisiveness
fields become validator errors for opted-in future physics jobs at or after the
active timestamp. Historical tasks and non-physics project-system completions
remain outside this hard-enforcement boundary.

## Route Contract Vocabulary

`ontology-law-research-packet` is a named route label for the narrow case where
the current ontology does not derive a derivation-critical source-side law,
selector, discriminator, transition rule, robustness rule, or equivalent
primitive. The trigger classification is
`derivation_critical_missing_source_law`.

The non-trigger classifications are `ordinary_gap` and
`workflow_inconvenience`. Ordinary gaps include missing documentation, missing
registry rows, generated derivative drift, missing citations, computations
available under existing ontology, and proof-detail work under existing
ontology. Workflow inconvenience includes tedious casework, slow literature
review, awkward templates, and strict validation friction.

Use `blocked_adoption_open_continuation` when current adoption is blocked but
same-milestone source-side continuation remains open. Candidate-law status
vocabulary is `draft/control`, `proposal-only`, `source-extension data`,
`canonical-ontology candidate`, `adopted`, `rejected`, and `human-gated`.
`canonical-ontology candidate`, adoption, and ontology-edit effects remain
human-gated.

## Ontology-Law Research Packet Completion Receipt

When a completion selects `ontology_law_research_packet`, or otherwise names
the route label `ontology-law-research-packet`, the completion record must
include a top-level `ontology_law_research_packet` block. This is a
completion-level receipt, not an independent ontology artifact.

Required shape:

```yaml
ontology_law_research_packet:
  route: "ontology-law-research-packet"
  trigger_classification: "derivation_critical_missing_source_law"
  target_derivation_milestone: ""
  milestone_burden: ""
  missing_source_law: ""
  underdetermination_statement: ""
  no_go_theorem_status: "not_proved"
  adoption_status:
    current_adoption: "blocked"
    continuation: "open"
    status_pair: "blocked_adoption_open_continuation"
  packet_payload_mode: "candidate_law_payload"
  candidate_law_payload:
    status_label: "proposal-only"
    source_side_definition: ""
    formal_objects: []
    domains: []
    maps: []
    proof_obligations: []
  candidate_law_comparison:
    candidates: []
    comparison_basis: []
    selection_status: ""
  candidate_law_refutation:
    refuted_candidate: ""
    refutation_basis: ""
    surviving_obligations: []
  human_gate_precondition:
    blocks_payload_definition: false
    reason: ""
  exact_gr_recovery_obligations:
    checklist: []
    distance_to_gr_links: []
  no_target_import_audit_scope:
    forbidden_source_classes:
      - "target_atlas"
      - "target_metric"
      - "benchmark_success"
      - "candidate_reconstruction"
      - "generated_derivative"
      - "registry_metadata_authority"
      - "role_authority"
      - "validation_authority"
  atlas_glue_obligations:
    profile_law: ""
    selector_law: ""
    transition_law: ""
    inverse_checks: ""
    cocycle_checks: ""
    finite_variation_robustness: ""
  failure_branches:
    collapse: ""
    nonuniqueness: ""
    inverse_defect: ""
    cocycle_defect: ""
    variation_fragility: ""
  known_risks: []
  failed_alternatives: []
  human_gate_request:
    required_before_adoption: true
    requested_decision: ""
    exact_requested_ontology_edit: ""
```

Required receipt behavior:

- `route` must be `ontology-law-research-packet`.
- `trigger_classification` must be `derivation_critical_missing_source_law`.
- `target_derivation_milestone` and `milestone_burden` must name the active
  derivation burden rather than opening an unrelated route.
- `missing_source_law` must name the missing source-side law, selector,
  discriminator, transition rule, robustness rule, or equivalent primitive.
- `underdetermination_statement` must use the precise form "current ontology
  does not derive X" or an equivalent statement that does not assert
  impossibility without a separate no-go theorem or scoped obstruction.
- `adoption_status.status_pair` must be
  `blocked_adoption_open_continuation` when current adoption is blocked but
  same-milestone continuation remains open.
- `packet_payload_mode` must be one of `candidate_law_payload`,
  `candidate_law_comparison`, `candidate_law_refutation`, or
  `human_gate_precondition`.
- At least one payload branch matching `packet_payload_mode` must be
  substantive: a candidate source law, a bounded candidate comparison, a
  candidate refutation, or a precise explanation that human Gate Chair
  authority is required before such a law can be proposed.
- `candidate_law_payload.status_label` must use the controlled status
  vocabulary: `draft/control`, `proposal-only`, `source-extension data`,
  `canonical-ontology candidate`, `adopted`, `rejected`, or `human-gated`.
- `exact_gr_recovery_obligations.checklist` must name recovery obligations
  that the candidate would have to preserve.
- `no_target_import_audit_scope.forbidden_source_classes` must include the
  target atlas, target metric, benchmark success, candidate reconstruction,
  generated derivatives, registry metadata authority, role authority, and
  validation authority.
- `human_gate_request.required_before_adoption` must be `true` for every
  packet that proposes, compares, refutes, or prepares an ontology-law
  candidate.

This schema defines the machine-checkable receipt contract. Phase 4 validator
enforcement checks the receipt fields, labels, blocked-adoption/open-continuation
boundary, no-target-import scope, exact-GR recovery obligations, and human-gate
boundary. Broader route fixtures remain Phase 5 work.

## Optional Fields

- `objective`
- `resolves_signal_routing`
- `role_decomposition`

`objective` is optional for ordinary one-signal or source-driven jobs. If one
AgentJob resolves more than one project-improvement signal, `objective` must
explicitly name each resolved signal ID. The completion record must then list
the same signal IDs in `resolved_project_improvement_signals` and provide a
nonblank `coherent_resolution_summary`. Each closed signal row must use the
AgentJob's canonical `completion_path` from `AGENT_JOB_REGISTRY.csv` as
`resolution_evidence_path`.

`resolves_signal_routing` is optional and defaults to `false`. Set it to
`true` only when the AgentJob objective explicitly fixes project-improvement
signal routing. A completion for such a job must include
nonblank `routing_delta_summary` plus `resolver_snapshots.before` and
`resolver_snapshots.after` as repo-relative paths to preserved JSON output from
`scripts/project_control/resolve_project_improvement.py --json`.
The research-control validator checks only that the summary is present and
that the snapshots preserve the stable advisory-routing shape: parseable JSON
object, advisory resolver fields, checkpoint gate source, and the
selected-signal, open-signals, and change-classification sections. Ordinary
validator and documentation jobs must not inherit this evidence burden.

## Role Decomposition For Physics Jobs

`role_decomposition` is mandatory for every new physics research AgentJob
created after `2026-06-17T04:08:16Z`. Historical AgentJobs before that
activation timestamp and non-physics project-system AgentJobs without this
block remain valid.

When present, the only supported mode is
`parent_child_parallel_synthesis` with `decomposition_version: "0.1.0"`. This
mode keeps the old external invariant intact:

- one Director decision
- one outer AgentJob
- one execution-role record
- one completion record
- one final old-style fused output artifact

The decomposition creates internal execution units, not independent AgentJobs.
The parent and children inherit the outer execution-role authority, claim
boundary, source restrictions, forbidden paths, validators, and write-path
allowlist. The decomposition may not declare separate role IDs, source classes,
write allowlists, expanded permissions, human-gate settings, or claim
boundaries.

Required shape:

```yaml
role_decomposition:
  mode: "parent_child_parallel_synthesis"
  decomposition_version: "0.1.0"
  parent:
    execution_unit_id: "parent"
    perspective: "physicist_mathematician_philosopher"
    responsibilities:
      - "derive child role definitions from the selected execution role"
      - "enforce shared claim boundary and source restrictions"
      - "review child outputs for conflicts"
      - "request bounded conflict resolution when needed"
      - "fuse child outputs into the final role artifact"
  children:
    - execution_unit_id: "child_phys_math"
      perspective: "physicist_mathematician"
      output_path: "research_control/tasks/<task_id>/artifacts/child_phys_math_<slug>.tex"
      status: "planned"
    - execution_unit_id: "child_phys_phil"
      perspective: "physicist_philosopher"
      output_path: "research_control/tasks/<task_id>/artifacts/child_phys_phil_<slug>.tex"
      status: "planned"
  conflict_policy:
    review_path: "research_control/tasks/<task_id>/artifacts/parent_conflict_review_<slug>.yaml"
    max_resolution_rounds: 2
    require_parallel_child_revision: true
    unresolved_conflict_status: "blocked"
  fusion_policy:
    fusion_notes_path: "research_control/tasks/<task_id>/artifacts/parent_fusion_notes_<slug>.md"
    fused_output_path: "research_control/tasks/<task_id>/artifacts/<old_style_final_slug>.tex"
    preserve_shared_consensus: true
    preserve_unique_contributions: true
    preserve_unresolved_limitations: true
    final_output_replaces_old_single_role_artifact: true
```

All child output paths, conflict review paths, fusion notes paths, and fused
output paths must be repo-relative paths under the outer AgentJob
`allowed_write_paths`. The fused output path must also appear in
`expected_outputs` and in the `AGENT_JOB_REGISTRY.csv` `output_paths` column.

For science-draft roles, the final fused `.tex` remains the authoritative
old-style role artifact for downstream registry, completion, handoff, and
claim-boundary references. Child `.tex` outputs are supporting draft/control
artifacts and should be registered when retained as source artifacts.

## Theoretical Continuation Selector Jobs

When the Director cannot select a single ordinary execution role because the
next step is a theoretical decision among admissible packets, use
`theoretical-continuation-selector@0.1.0`.

The job remains a physics research AgentJob and therefore must use
`role_decomposition` when created after `2026-06-17T04:08:16Z`. Its completion
must include `distance_to_gr_status` and `theoretical_decision_output`.

The selector may choose only one future packet type:

- `source_side_selector_primitive`
- `source_side_irrelevance_theorem`
- `concrete_resp_lc_witness`
- `distinct_scoped_no_go_question`
- `bounded_theoretical_calculation`
- `finite_toy_metric_response_model`
- `ontology_law_research_packet`
- `source_extension_candidate`
- `source_extension_smuggling_audit`
- `source_extension_refuter_stress`
- `source_extension_human_gate`
- `human_gated_ontology_change_required`

The last option is reserved for cases where the next honest continuation needs
canonical ontology authority, ontology adoption, or another protected human
gate. Missing empirical data or absent experiment access is not sufficient.
When `ontology_law_research_packet` is selected, the route label is
`ontology-law-research-packet`, the trigger classification must be
`derivation_critical_missing_source_law`, and current adoption must remain
blocked unless a later explicit human Gate Chair action authorizes otherwise.

After `2026-06-17T15:46:25Z`, `distinct_scoped_no_go_question` must include a
new-payload novelty statement and a decision consequence. Source-extension
packet decisions must classify the source-extension category and state whether
the proposal is a derivation from current ontology, a conservative definitional
extension, a new ontology primitive, or a forbidden target-GR import. Finite
toy model decisions must name the finite source set, response relation, toy
metric-response analogue, and invariance checks.

## Distance-To-GR And Payload Contract

Future physics completions after `2026-06-17T15:46:25Z` must include the
expanded `distance_to_gr_status` burdens from
`research_control/design/gr_derivation_burden_map.md` and at least one
`new_mathematical_payload` item. Accepted payload families are new
definitions, lemmas, theorems, finite models, countermodels, explicit
witnesses, obstructions, dependency-map updates, finite toy targets,
source-extension classifications, packet selections, or established
role-specific payload types.

Repeated-burden or scoped-obstruction Refuter completions after that timestamp
must also include `freeze_criteria_status`, including evaluated criteria,
freeze decision, rationale, and a candidate freeze label when freezing a
route.
