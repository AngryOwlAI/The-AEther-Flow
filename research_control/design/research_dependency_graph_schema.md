<!-- authority: control -->

# Research Dependency Graph Schema

## Purpose

This control note completes P7-T01 of
`implementations_plans/recommendations_implementation_plan_continue_task-v11.md`.
It defines the schema for a generated dependency graph of research objects,
claim boundaries, tasks, AgentJobs, artifacts, handoffs, and Distance-to-GR
ledger rows.

The graph is navigational support. It is not physics authority, not a proof
surface, not a claim-promotion mechanism, and not a substitute for registered
TeX, canonical Markdown, tracked completions, Gate Chair records, or control
registries.

## Source Basis

P7-T02 must extract graph data only from tracked authority surfaces:

- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `registries/DIRECTOR_DECISION_REGISTRY.csv`
- `registries/ROLE_EXECUTION_REGISTRY.csv`
- `registries/TEX_SOURCE_REGISTRY.csv`
- `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- `registries/FILE_OBJECT_REGISTRY.csv`
- `research_control/program_state.yaml`
- `research_control/handoffs/handoff-*.yaml`
- `research_control/tasks/*/00_TASK.yaml`
- `research_control/tasks/*/jobs/*.yaml`
- `research_control/tasks/*/jobs/completions/*.yaml`

Generated wiki notes, Obsidian notes, semantic extracts, SQLite memory, and
`.local/` caches may help locate sources, but they must not be graph authority.

## Output Formats

P7-T02 should generate these three output formats from one in-memory graph:

- JSON graph: `output/research_dependency_graph.json`
- Markdown summary table: `wiki/indexes/research_dependency_graph.md`
- DOT graph: `output/research_dependency_graph.dot`

The JSON graph is the machine-readable exchange format. The Markdown summary is
the human scanning surface. The DOT graph is a renderer input only. All three
must state that graph data is navigational support and not independent physics
or control authority.

## JSON Shape

```json
{
  "schema_id": "research_dependency_graph_v1",
  "generated_at": "2026-06-28T00:00:00Z",
  "authority_boundary": {
    "navigational_support_only": true,
    "physics_claim_authority": false,
    "source_authority_required": true
  },
  "sources": [],
  "nodes": [],
  "edges": [],
  "warnings": []
}
```

Each `sources` item should include `path`, `source_kind`, `source_hash` when
available, and `registry_object_id` when the source is a registered artifact.

## Node Schema

Each node must use this shape:

```json
{
  "node_id": "ledger:g_eff",
  "node_class": "accepted_scoped_object",
  "label": "g_eff",
  "state_label": "accepted_scoped",
  "source_path": "registries/DISTANCE_TO_GR_LEDGER.csv",
  "source_registry": "DISTANCE_TO_GR_LEDGER.csv",
  "source_field": "required_object",
  "authority_status": "project_control",
  "summary": "Scoped source-extension g_eff object; downstream claims remain blocked.",
  "metadata": {}
}
```

### Required Node Classes

P7-T02 must support these node classes:

| Node class | Primary source | Required use |
| --- | --- | --- |
| `source_ontology_object` | `TEX_SOURCE_REGISTRY.csv`, ontology paths | Canonical or source-side ontology objects. |
| `source_extension_evidence_precondition` | completion payloads, Gate Chair records, ledger notes | Scoped source-extension evidence or preconditions. |
| `draft_control_candidate` | completion payloads, task artifacts | Draft/control candidates pending audit, stress, or gate. |
| `accepted_scoped_object` | Gate Chair completions, ledger rows | Objects accepted only in a scoped status. |
| `human_gated_object` | approvals, Gate Chair rows, ledger status | Objects whose status requires explicit human authority. |
| `blocked_burden` | `DISTANCE_TO_GR_LEDGER.csv`, completion blocks | Undischarged or blocked derivation burdens. |
| `frozen_negative` | ledger rows, freeze receipts | Frozen negative routes or locally frozen failures. |
| `obstruction` | `obstruction_record`, completion payloads | Named precise obstructions and countermodels. |
| `gate_chair_verdict` | Gate Chair tasks and completions | Human-gated verdict or evidence-status decisions. |
| `task` | `RESEARCH_TASK_REGISTRY.csv`, `00_TASK.yaml` | Research-control tasks. |
| `agent_job` | `AGENT_JOB_REGISTRY.csv`, AgentJob YAML | AgentJobs and their execution roles. |
| `artifact` | source registries, job output paths | Tracked artifacts referenced by jobs and completions. |
| `handoff` | `research_control/handoffs/handoff-*.yaml` | Durable continuation handoffs. |
| `ledger_row` | `DISTANCE_TO_GR_LEDGER.csv` | Distance-to-GR burden rows. |
| `claim_boundary` | `CLAIM_BOUNDARY_REGISTRY.csv` | Claim-boundary records that constrain interpretation. |

`claim_boundary` is an additional required project-control class because the
graph objective includes claim boundaries directly.

### Required State Labels

P7-T02 must support these state labels:

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

State labels are semantic labels, not hardcoded colors. A later renderer may map
labels to colors, but the extractor must emit labels.

## Edge Schema

Each edge must use this shape:

```json
{
  "edge_id": "edge:task:RT-20260614-244:constructs:object:B_E_rec",
  "source_id": "task:RT-20260614-244",
  "target_id": "object:B_E_rec",
  "edge_class": "constructs",
  "source_path": "research_control/tasks/RT-20260614-244/jobs/completions/AJC-AJ-RT-20260614-244-001.yaml",
  "source_field": "mathematical_payload_manifest.object_name",
  "summary": "Task constructs B_E_rec as draft/control candidate data.",
  "metadata": {}
}
```

### Required Edge Classes

P7-T02 must support these edge classes:

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

## Source-To-Graph Mapping

| Source surface | Fields | Nodes | Edges |
| --- | --- | --- | --- |
| `DISTANCE_TO_GR_LEDGER.csv` | `burden_id`, `milestone`, `required_object`, `current_status`, `blocking_burden`, `accept_criteria`, `failure_or_freeze_criteria`, `last_evidence_path`, `notes` | `ledger_row`, burden/object nodes | `requires`, `blocks`, `freezes`, `updates_ledger` |
| `RESEARCH_TASK_REGISTRY.csv` | `task_id`, `task_path`, `parent_task_id`, `current_job_id`, `status`, `closure_status` | `task` | `depends_on`, `handoffs_to` |
| `AGENT_JOB_REGISTRY.csv` | `job_id`, `task_id`, `role_id`, `job_path`, `completion_path`, `output_paths` | `agent_job`, `artifact` | `constructs`, `audits`, `stress_tests`, `depends_on` |
| `CLAIM_BOUNDARY_REGISTRY.csv` | `claim_boundary_id`, `allowed_claims`, `forbidden_claims`, `requires_gate_for`, `authority_source_path` | `claim_boundary`, blocked claim nodes | `forbids_overread`, `blocks`, `requires_human_gate` |
| `DIRECTOR_DECISION_REGISTRY.csv` | `decision_id`, `task_id`, `selected_role_id`, `agent_job_id` | `artifact` or metadata on `task` | `selects_next`, `depends_on` |
| `ROLE_EXECUTION_REGISTRY.csv` | `execution_role_ref`, `base_role_id`, `allowed_write_paths`, `removed_permissions` | metadata on `agent_job` | `forbids_overread` |
| `TEX_SOURCE_REGISTRY.csv` | `object_id`, `path`, `role`, `claim_status`, `research_status`, `ontology_promotion_status` | `source_ontology_object`, `artifact`, candidate nodes | `depends_on`, `constructs` |
| `MARKDOWN_SOURCE_REGISTRY.csv` | `object_id`, `path`, `role`, `authority_status` | `artifact`, control design nodes | `depends_on` |
| completion YAML | `mathematical_payload_manifest`, `new_mathematical_payload`, `obstruction_record`, `candidate_constructor_result`, `theoretical_decision_output`, `freeze_criteria_status`, `route_cycle_control`, `forbidden_conclusion_summary`, `distance_to_gr_delta` | object, obstruction, candidate, verdict, blocked claim nodes | `constructs`, `selects_next`, `blocks`, `freezes`, `forbids_overread`, `updates_ledger` |
| handoff YAML | `handoff_id`, `task_id`, `job_id`, `next_action`, `required_next_packet` | `handoff`, next-route metadata | `handoffs_to`, `selects_next` |

## ID Rules

Node IDs must be stable and deterministic:

- `task:<task_id>`
- `job:<job_id>`
- `handoff:<handoff_id>`
- `ledger:<burden_id>`
- `claim_boundary:<claim_boundary_id>`
- `artifact:<registry_object_id>` when registered, otherwise
  `artifact:<path_slug>`
- `object:<normalized_object_name>`
- `obstruction:<obstruction_id>`
- `gate_verdict:<task_id>`

Normalize object names by lowercasing, replacing spaces and punctuation with
single underscores, and preserving enough symbolic tokens to avoid collisions.
For example, `B_E^{rec}` becomes `object:b_e_rec`.

## Status Mapping

| Source value or pattern | State label |
| --- | --- |
| `authority_status=canonical` or canonical ontology source | `canonical_source` |
| `draft object exists`, `constructive witness exists`, or science draft rows | `science_draft` |
| `draft/control` completion payloads | `draft_control` |
| `proposal-only` completion payloads | `proposal_only` |
| scoped source-extension evidence or precondition wording | `source_extension_evidence` |
| `accepted` with scoped/no-downstream notes | `accepted_scoped` |
| `human-gated`, Gate Chair authority, or approval requirement | `human_gated` |
| `blocked by missing primitive`, forbidden downstream claims, or `current_status=not started` for an active downstream burden | `blocked` |
| `frozen negative`, `route_frozen`, or local freeze receipt | `frozen_negative` |
| explicit rejection verdicts | `rejected` |
| support-only checker/tooling artifacts | `support_only` |

When a source row has both an accepted local status and blocked downstream
notes, emit both the accepted object node and the blocked downstream burden
nodes. Do not collapse them into one state.

## Required Frontier Representation

The schema must be expressive enough for P7-T02 to represent the current
frontier:

| Object or burden | Expected node class | Expected state label | Required edges |
| --- | --- | --- | --- |
| `Resp_lc` | `accepted_scoped_object` | `accepted_scoped` | `requires` source-extension selector data; `blocks` downstream overread. |
| `M_src` | `accepted_scoped_object` | `accepted_scoped` | `requires` response/localization bridge; `blocks` `g_eff` overread unless scoped gate evidence exists. |
| `g_eff` | `accepted_scoped_object` | `accepted_scoped` | `blocks` matter coupling, Einstein equations, benchmark promotion, and completed derivation. |
| `B_E^{rec}` | `source_extension_evidence_precondition` | `source_extension_evidence` | `constructs`, `audits`, `stress_tests`, `accepts_as_evidence`, and `forbids_overread`. |
| `BridgeCert` | `source_extension_evidence_precondition` | `source_extension_evidence` | same recovery-bridge evidence path as `B_E^{rec}`. |
| `SEI-MC` criteria | `draft_control_candidate` | `draft_control` | `requires` recovery-bridge evidence and scoped `g_eff`; `blocks` stress-energy overread. |
| `SEI_src^{cand}` | `draft_control_candidate` | `draft_control` | `constructs`, `selects_next` to audit, and `forbids_overread`. |
| matter-coupling burden | `ledger_row` plus `blocked_burden` where downstream derivation remains unproved | `accepted_scoped` for evidence/precondition and `blocked` for derivation overread | `requires` SEI/audit/stress/gate chain; `blocks` coupling-law adoption and matter-coupling derivation until gates close. |
| Einstein-equations burden | `ledger_row` or `blocked_burden` | `blocked` | `requires` matter coupling and dynamics/action/variation; `blocks` benchmark promotion. |
| benchmark-promotion burden | `ledger_row` or `human_gated_object` | `human_gated` | `requires_human_gate`; `requires` all prior burdens. |
| finite toy metric response | `frozen_negative` | `frozen_negative` | `freezes` explicit-tag-only finite toy route; `blocks` reuse without redesign. |

## Markdown Summary Contract

The Markdown output should include:

- an authority notice;
- a source count table;
- a node summary grouped by `node_class` and `state_label`;
- a frontier table for `Resp_lc`, `M_src`, `g_eff`, matter coupling, Einstein
  equations, benchmark promotion, and finite toy metric response;
- a blocked downstream claims section;
- a route-continuity section showing the latest handoff and next packet.

## DOT Contract

The DOT output should be deterministic:

- sort nodes by `node_id`;
- sort edges by `(source_id, edge_class, target_id, edge_id)`;
- use `state_label` and `node_class` attributes;
- do not encode authority through colors alone;
- include a graph-level label stating `navigational_support_only`.

## Validation Expectations For P7-T02

The extractor should fail or warn when:

- an edge references a missing node;
- a node lacks `source_path`;
- an edge lacks `source_path` or `source_field`;
- a required state label is unknown;
- a required node or edge class is unknown;
- generated output omits the authority notice;
- the graph treats validation status, registry presence, handoff text, local
  cache content, generated wiki notes, or commit status as proof authority.

## References

The AEther-Flow Research Project. (2026, June 17). *GR derivation burden map*
[Internal control design note].

The AEther-Flow Research Project. (2026, June 28). *Handoff 0311* [Internal
control handoff].

The AEther-Flow Research Project. (2026, June 28). *Recommendations
implementation plan continue task v11* [Internal implementation plan].
