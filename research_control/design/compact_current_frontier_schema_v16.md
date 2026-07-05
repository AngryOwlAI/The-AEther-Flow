<!-- authority: control -->

# Compact Current Frontier Schema v16

## Purpose

`compact_current_frontier_v16` defines a small machine-readable snapshot of the
current research-control frontier. It is designed for agents and validators
that need active state, next route, high-risk claim boundaries, and
Distance-to-GR context without parsing the full reader-facing
`research_control/current_frontier.md`.

This schema is project-control only. It is not routing authority by itself, not
physics proof, not source-law adoption, not matter-coupling derivation, not an
Einstein-equation derivation, not benchmark promotion, and not completed
derivation evidence.

## Authority Rule

The compact frontier output is always a synchronized snapshot. If compact
frontier YAML or JSON disagrees with any tracked source below, the tracked
source governs:

1. `research_control/program_state.yaml`;
2. the latest handoff named by `program_state.yaml`;
3. `registries/DISTANCE_TO_GR_LEDGER.csv`;
4. `research_control/current_frontier.md`;
5. task records, DDRs, AgentJobs, completions, claim-boundary rows, and
   role-execution rows.

Generated wiki notes, Obsidian notes, semantic extracts, SQLite retrieval
indexes, `.local/` cache state, dependency graphs, validator PASS status, and
commit metadata must not be used as authority for this schema.

## Required Shape

Renderers must produce this top-level shape in YAML and JSON:

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

Additional fields may be added later only by a tracked project-control task.
Renderers should preserve these required fields exactly.

## Field Requirements

| Field | Meaning | Required source |
| --- | --- | --- |
| `schema_id` | Constant schema identifier. | This schema. |
| `generated_from` | Exact tracked authority sources read by the renderer. | This schema and renderer code. |
| `active_state.active_task_id` | Current active task pointer. | `research_control/program_state.yaml`. |
| `active_state.latest_handoff_id` | Current handoff pointer. | `research_control/program_state.yaml`. |
| `active_state.current_status` | Compact status string. | `research_control/program_state.yaml`. |
| `active_state.v15_completed` | Whether v15 is complete in tracked state. | Latest handoff/current frontier evidence. |
| `active_state.v16_plan_registered` | Whether the v16 implementation plan is registered. | `registries/MARKDOWN_SOURCE_REGISTRY.csv`. |
| `next_route.route_id` | Immediate next route. | Latest handoff selected route. |
| `next_route.role_family` | Recommended role family for the next packet. | Latest handoff selected route. |
| `next_route.target_derivation_milestone` | Active milestone name. | Latest handoff selected route or Distance-to-GR context. |
| `next_route.milestone_burden` | Exact next bounded burden. | Latest handoff selected route. |
| `next_route.requires_human_gate` | Whether the next route requires protected authority. | Latest handoff selected route. |
| `claim_boundary.physics_claim_authority` | Whether the compact output has physics-claim authority. | Must be `false`. |
| `claim_boundary.proof_authority` | Whether the compact output has proof authority. | Must be `false`. |
| `claim_boundary.blocked_claims` | High-risk claims blocked by current state. | Current frontier, latest handoff, claim-boundary rows. |
| `scoped_positive_objects` | Objects accepted only in scoped source-side or source-extension senses. | Distance-to-GR ledger and current frontier. |
| `scoped_evidence_preconditions` | Accepted evidence/preconditions that must not render as adopted objects. | Distance-to-GR ledger and current frontier. |
| `blocked_physical_targets` | Downstream targets still blocked. | Distance-to-GR ledger and current frontier. |
| `distance_to_gr.delta` | Whether the latest packet changed Distance-to-GR status. | Latest completion and handoff. |
| `distance_to_gr.high_risk_rows` | Layered status for high-risk ledger rows. | `registries/DISTANCE_TO_GR_LEDGER.csv`. |
| `validation.latest_required_status` | Latest required validation status if available. | Latest completion and handoff. |
| `validation.pending_layers` | Validation layers that are pending with reason. | Latest completion and handoff. |
| `authority_warning.snapshot_only_not_authority` | Snapshot warning flag. | Must be `true`. |

## Required High-Risk Rows

`distance_to_gr.high_risk_rows` must include at least these burden IDs when
present in the ledger:

- `m_src`;
- `g_eff`;
- `matter_coupling`;
- `einstein_equations`;
- `benchmark_promotion`.

The renderer must not emit bare `accepted` for these rows without
reader-facing qualification. The row must include enough layered fields or
guard text to block source-law adoption, matter-semantics adoption,
detector-semantics adoption, coupling-law adoption, matter-coupling derivation
or adoption, stress-energy semantics, matter action, Einstein equations,
benchmark promotion, and completed derivation when those layers remain
unauthorized.

## Required Blocked Claims

`claim_boundary.blocked_claims` must preserve the following claims whenever
the latest tracked state has not explicitly authorized them:

- canonical ontology edit;
- source-law adoption;
- `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption;
- unrestricted `RR_E` theorem status;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor;
- matter action;
- Einstein equations;
- benchmark promotion;
- Gate Chair verdict or closure;
- proof authority;
- completed derivation.

The compact output may include additional blocked claims from the latest
handoff or claim-boundary registry.

## Validation Expectations

A future renderer/check integration should fail when:

1. `active_state.active_task_id` disagrees with
   `research_control/program_state.yaml`;
2. `active_state.latest_handoff_id` disagrees with
   `research_control/program_state.yaml`;
3. `next_route.route_id` disagrees with the latest handoff;
4. required high-risk rows are missing;
5. blocked claims required by this schema are missing;
6. matter coupling renders as derived or adopted without protected authority;
7. Einstein equations render as started or derived without protected authority;
8. benchmark promotion renders as promoted without protected authority;
9. `authority_warning.snapshot_only_not_authority` is absent or false.

## Example Minimal Snapshot

```yaml
schema_id: "compact_current_frontier_v16"
generated_from:
  - "research_control/program_state.yaml"
  - "research_control/handoffs/handoff-0605.yaml"
  - "registries/DISTANCE_TO_GR_LEDGER.csv"
  - "research_control/current_frontier.md"
active_state:
  active_task_id: "RT-20260705-032"
  latest_handoff_id: "handoff-0605"
  current_status: "v16_p14_t03_target_import_validator_integration_completed_no_physics_delta"
  v15_completed: true
  v16_plan_registered: true
next_route:
  route_id: "compact_current_frontier_schema_v16"
  role_family: "project-control-maintainer@0.2.0"
  target_derivation_milestone: "matter_coupling"
  milestone_burden: "Define compact current-frontier schema as snapshot-only project-control summary without physics delta."
  requires_human_gate: false
claim_boundary:
  physics_claim_authority: false
  proof_authority: false
  blocked_claims:
    - "source-law adoption"
    - "matter-coupling derivation or adoption"
    - "Einstein equations"
    - "benchmark promotion"
    - "completed derivation"
scoped_positive_objects:
  - object_id: "m_src"
    reader_facing_status: "adopted only as scoped source-only M_src object"
scoped_evidence_preconditions:
  - object_id: "matter_coupling"
    reader_facing_status: "accepted only as scoped source-extension evidence/precondition"
blocked_physical_targets:
  - target_id: "einstein_equations"
    status: "not_started"
distance_to_gr:
  delta:
    effect: "no_distance_delta"
    changed: false
  high_risk_rows:
    - burden_id: "matter_coupling"
      reader_facing_status: "accepted only as scoped source-extension evidence/precondition"
      promotion_status: "scoped_source_evidence_only"
validation:
  latest_required_status: "PASS"
  pending_layers: []
authority_warning:
  snapshot_only_not_authority: true
```

## Acceptance Check

This schema distinguishes compact snapshot data from authority, names the exact
tracked source paths, preserves blocked claims, and routes renderer and check
implementation to P15-T02 and P15-T03. It creates no physics delta.

## References

The Aether-Flow Research Project. (2026). `implementations_plans/recommendations_implementation_plan_continue_task-v16.md` [Internal project-control plan].

The Aether-Flow Research Project. (2026). `research_control/current_frontier.md` [Internal project-control snapshot].

The Aether-Flow Research Project. (2026). `registries/DISTANCE_TO_GR_LEDGER.csv` [Internal project-control ledger].
