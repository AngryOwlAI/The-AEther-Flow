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
        - "<source-object-id>"
  canonical_inspections:
    - object_id: "<source-object-id>"
      source_registry: "MARKDOWN_SOURCE_REGISTRY.csv"
      registry_path: "registries/MARKDOWN_SOURCE_REGISTRY.csv"
      canonical_path: "<repo-relative-source-path>"
      source_hash: "<sha256>"
  authority_note: "Obsidian, wiki notes, semantic extracts, and .local are retrieval layers only and not authority."
```

Every returned object ID that influences routing, claims, source selection, or
project-control changes must have a canonical inspection entry. `source_hash`
must match both the named source registry row and the current file bytes at
`canonical_path`.

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

Phase 2 will define the machine-checkable receipt block for this route. Until
that receipt schema exists, this section defines route vocabulary and claim
boundaries only; it does not add a new validator-enforced field requirement.

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
