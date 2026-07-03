<!-- generated: claim_graph_v1; authority: derivative -->

# Claim Graph v1

This index is generated project-control metadata. It is not proof authority, not physics source authority, and not authority to promote any claim.

- Schema: `claim_graph_schema_v1`
- Generated from tracked state as of: `2026-07-03T20:38:51Z`
- Nodes: `10`
- Edges: `15`
- Claim boundary: `no physics delta; no promotion; no proof authority`

## Required Pilot Nodes

| Label | Type | Status | Promotion status | Authority |
| --- | --- | --- | --- | --- |
| `benchmark promotion` | `blocked_physical_target` | `blocked` | `blocked` | `registries/DISTANCE_TO_GR_LEDGER.csv` |
| `Einstein equations` | `blocked_physical_target` | `blocked` | `blocked` | `registries/DISTANCE_TO_GR_LEDGER.csv` |
| `matter_coupling` | `blocked_physical_target` | `blocked` | `blocked` | `registries/DISTANCE_TO_GR_LEDGER.csv` |
| `NarrowMSCertEq_v1` | `conditional_theorem` | `accepted_as_scoped_evidence_status` | `scoped_evidence_precondition` | `research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex` |
| `PositiveMSProfile_v1` | `evidence_precondition` | `accepted_as_scoped_evidence_precondition` | `scoped_evidence_precondition` | `research_control/design/frontier_theorem_inventory.md` |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` | `evidence_precondition` | `accepted_as_scoped_evidence_precondition` | `scoped_evidence_precondition` | `research_control/design/frontier_theorem_inventory.md` |
| `RR_E separation obstruction` | `obstruction` | `obstruction_recorded` | `blocked` | `research_control/design/frontier_theorem_inventory.md` |
| `g_eff` | `source_extension_object` | `gate_review_completed` | `scoped_source_object_only` | `registries/DISTANCE_TO_GR_LEDGER.csv` |
| `Resp_lc` | `source_extension_object` | `accepted_as_source_extension_data` | `scoped_source_object_only` | `registries/DISTANCE_TO_GR_LEDGER.csv` |
| `M_src` | `source_object` | `gate_review_completed` | `scoped_source_object_only` | `registries/DISTANCE_TO_GR_LEDGER.csv` |

## High-Risk Non-Establishment Edges

| Source | Relation | Target | Does not establish |
| --- | --- | --- | --- |
| `benchmark promotion` | `requires_human_gate` | `Einstein equations` | benchmark promotion; completed derivation |
| `Einstein equations` | `does_not_establish` | `benchmark promotion` | benchmark promotion; completed derivation |
| `g_eff` | `does_not_establish` | `matter_coupling` | matter-coupling derivation or adoption; Einstein equations; benchmark promotion; completed derivation |
| `matter_coupling` | `does_not_establish` | `Einstein equations` | Einstein equations; benchmark promotion; completed derivation |
| `NarrowMSCertEq_v1` | `does_not_establish` | `matter_coupling` | matter-coupling derivation or adoption; Einstein equations; benchmark promotion; completed derivation |
| `PositiveMSProfile_v1` | `does_not_establish` | `matter_coupling` | matter-coupling derivation or adoption; Einstein equations; benchmark promotion; completed derivation |
| `RR_E separation obstruction` | `blocks` | `matter_coupling` | future source-extension impossibility; program-wide no-go conclusion |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` | `does_not_establish` | `matter_coupling` | matter-coupling derivation or adoption; Einstein equations; benchmark promotion; completed derivation |

## Source Materials

The AEther-Flow Research Project. (2026a). *Distance-to-GR ledger* [Research-control registry]. `registries/DISTANCE_TO_GR_LEDGER.csv`.

The AEther-Flow Research Project. (2026b). *Frontier theorem inventory* [Internal control inventory]. `research_control/design/frontier_theorem_inventory.md`.

The AEther-Flow Research Project. (2026c). *Claim graph schema v1* [Project-control schema]. `research_control/design/claim_graph_schema_v1.md`.

The AEther-Flow Research Project. (2026d). *Recommendations implementation plan continue task v15* [Implementation plan]. `implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.
