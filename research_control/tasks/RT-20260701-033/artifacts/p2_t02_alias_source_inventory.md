<!-- authority: control -->

# P2-T02 Alias Source Inventory

## Scope

This inventory supports `RT-20260701-033`, the bounded v14 P2-T02
high-risk status alias-map control packet. It records source inspection only.
It is not a physics proof surface and does not override the Distance-to-GR
ledger.

## Canonical Sources Inspected

| Source | Role in packet | Inspection result |
| --- | --- | --- |
| `implementations_plans/recommendations_implementation_plan_continue_task-v14.md` | Plan source for P2-T02 requirements. | Requires `research_control/design/distance_to_gr_status_aliases.yaml`, required alias rows, required `matter_coupling` object aliases, and a renderer integration note or deferred integration handoff. |
| `research_control/handoffs/handoff-0441.yaml` | Live routing authority. | Selects one bounded P2-T02 high-risk status alias-map packet and blocks public propagation, current-frontier wording pilot, linter, matter-coupling, Einstein-equation, benchmark, and promotion work. |
| `research_control/design/scoped_positive_claim_vocabulary.md` | Vocabulary source. | Defines scoped-positive terms and explicitly disallows bare `accepted` for high-risk rows unless immediately qualified. |
| `registries/DISTANCE_TO_GR_LEDGER.csv` | Ledger authority. | Contains all required P2-T02 alias rows as `burden_id` values and remains authoritative if any alias conflicts with the ledger. |
| `scripts/research_control/render_current_frontier.py` | Future renderer integration target. | Renderer currently reads program state, latest handoff, active task, and ledger rows directly. This packet defers integration to P2-T03 rather than changing renderer behavior. |

## Required Alias Coverage

| Required alias row | Ledger burden ID present | Alias created |
| --- | --- | --- |
| `source_ontology_primitives` | yes | yes |
| `source_equivalence_eqsrc` | yes | yes |
| `obsloc_lc` | yes | yes |
| `resp_lc` | yes | yes |
| `m_src` | yes | yes |
| `g_eff` | yes | yes |
| `matter_coupling` | yes | yes |
| `einstein_equations` | yes | yes |
| `benchmark_promotion` | yes | yes |
| `gate_chair_status` | yes | yes |
| `finite_toy_metric_response` | yes | yes |

## Matter-Coupling Object Alias Coverage

| Required object alias | Alias created | Boundary preserved |
| --- | --- | --- |
| `MSStableMatterSemanticsBridge_v1` | yes | Draft/control bridge target only; not matter semantics or detector semantics. |
| `SourceMatterSemanticsAdoptionReadinessLaw_v1` | yes | Proposal-only law target unless a later protected gate changes status. |
| `PositiveMSProfile_v1` | yes | Scoped positive source-semantics evidence/precondition only. |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` | yes | Certificate-indexed RR_E transport-completeness or invariance evidence/precondition only. |
| `RR_E_underdetermination_obstruction` | yes | Scoped obstruction only; no global no-go or global theory rejection. |

## Conclusion

The alias map has sufficient canonical source support for P2-T02. It is a
control display map only. It does not change ledger authority, scientific
status, ontology, source-law status, matter-coupling status, Einstein-equation
status, benchmark status, or completed-derivation status.

## Source Materials

The AEther-Flow Research Project. (2026, July 1). *Distance-to-GR ledger*
[Internal control registry].

The AEther-Flow Research Project. (2026, July 1). *Scoped positive claim
vocabulary* [Internal control note].

The AEther-Flow Research Project. (2026, July 1). *Handoff 0441*
[Internal research-control handoff].

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v14* [Internal implementation plan].
