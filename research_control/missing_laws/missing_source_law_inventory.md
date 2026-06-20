<!-- authority: control -->

# Missing Source-Law Inventory

## Analysis

This inventory is a tracked control artifact for known derivation-critical
missing source-side laws. It is navigation evidence for `/continue-research`;
it is not a second router, not a batch queue, and not an adoption mechanism.

The active live state is `RT-20260614-075` with `handoff-0117`. That handoff
maps to `MSL-MSRC-ATLASGLUE-LAW`: current ontology does not derive
discriminator profiles, selector preorder, inverse checks, cocycle checks, or
finite-variation robustness for `AtlasGlueDisc_src^+`, `AtlasGlue_src^+`, or
`M_src`. Adoption is blocked. Same-milestone continuation remains open.

## Selection Policy

- `/continue-research` remains the only selector and executor.
- The inventory may inform one bounded AgentJob selection per invocation.
- If more than one row matches live state, route one
  `theoretical-continuation-selector@0.1.0` job.
- Non-trigger rows and frozen rows are not eligible for ontology-law routing.
- Generated wiki, semantic, Obsidian, and `.local` paths are retrieval only.

## Seed Candidates

| Law ID | Status | Trigger class | Milestone | Evidence summary |
| --- | --- | --- | --- | --- |
| `MSL-MSRC-ATLASGLUE-LAW` | `selected_by_handoff` | `derivation_critical_missing_source_law` | `source_manifold_m_src` | `RT-20260614-075`, `handoff-0117`, Distance ledger `m_src` and `finite_variation_robustness` rows. |
| `MSL-MSRC-ATLASGLUE-DISCRIMINATOR-LAW` | `open` | `derivation_critical_missing_source_law` | `source_manifold_m_src` | `RT-20260614-069` through `RT-20260614-074`; finite witness survives as draft/control data while adoption is human-gated. |
| `MSL-RESP-LC-SELECTOR-LAW` | `deferred` | `derivation_critical_missing_source_law` | `response_localization_resp_lc` | `RT-20260614-041`, `RT-20260614-046`, `RT-20260614-051`, and Distance ledger `resp_lc`. |
| `MSL-OBSLOC-SOLDERING-LAW` | `deferred` | `derivation_critical_missing_source_law` | `source_localization_obsloc_lc` | `RT-20260614-035` through `RT-20260614-040`; exact-branch witness exists, robustness remains limited. |
| `MSL-MSRC-METRIC-RESPONSE-LAW` | `blocked_by_dependency` | `derivation_critical_missing_source_law` | `source_manifold_m_src` | `RT-20260614-038`, `RT-20260614-040`, `RT-20260614-041`, `RT-20260614-061`; metric-response law remains downstream of atlas-glue and response-selector burdens. |
| `MSL-FINITE-VARIATION-ROBUSTNESS-LAW` | `open` | `derivation_critical_missing_source_law` | `source_equivalence_eqsrc` | `RT-20260614-034`, `RT-20260614-072`, `RT-20260614-074`, `RT-20260614-075`, Distance ledger `finite_variation_robustness`. |
| `MSL-FINITE-TOY-RESPONSE-LAW` | `frozen_negative` | `derivation_critical_missing_source_law` | `finite_toy_metric_response` | `RT-20260614-053` and Distance ledger `finite_toy_metric_response`; frozen locally after tag-removal stress. |
| `MSL-EQSRC-GENERALIZATION-LAW` | `deferred` | `derivation_critical_missing_source_law` | `source_equivalence_eqsrc` | `RT-20260614-034` and Distance ledger `source_equivalence_eqsrc`; broad row intentionally needs later narrowing. |

## Active Mapping

The current handoff maps to exactly one top-level inventory row:

```text
handoff-0117 -> MSL-MSRC-ATLASGLUE-LAW
```

Its direct dependency is:

```text
MSL-FINITE-VARIATION-ROBUSTNESS-LAW
```

The logical next research-control move remains a single bounded
`/continue-research` decision. If the Director treats the atlas-glue row as
ambiguous between profile semantics, selector preorder, transition algebra,
inverse/cocycle law, and finite-variation law branches, the safe selector is
`theoretical-continuation-selector@0.1.0`.

## Boundary

Every row preserves `blocked_adoption_open_continuation`. The inventory does
not authorize canonical ontology edits, `AtlasGlue_src^+` adoption,
`AtlasGlueDisc_src^+` adoption, `M_src` adoption, full `M_src` construction,
`g_eff`, matter coupling, Einstein-equation claims, benchmark promotion, Gate
Chair verdicts, completed-derivation language, global theory rejection, or
future source-extension impossibility.

## Can It Be Improved?

An improvement will be to make `/continue-research` report the matched
inventory candidate ID in its context packet after the inventory has been used
manually at least once. That belongs to a later integration phase, not this
Phase 1 artifact creation packet.

## References

The AEther-Flow Research Project. (2026, June 20). *Handoff 0117* [Internal
research-control handoff]. `research_control/handoffs/handoff-0117.yaml`

The AEther-Flow Research Project. (2026, June 20). *Missing source-law
inventory Phase 0 requirement audit* [Internal project-control artifact].
`research_control/tasks/RT-20260620-009/artifacts/missing_source_law_inventory_phase0_requirement_audit.md`

The AEther-Flow Research Project. (2026, June 20). *Resp_lc current-ontology
AtlasGlue derivation attempt* [Internal research-control artifact].
`research_control/tasks/RT-20260614-075/artifacts/116_RESP_LC_CURRENT_ONTOLOGY_ATLAS_GLUE_DERIVATION_ATTEMPT.tex`

The AEther-Flow Research Project. (2026). *Distance to GR ledger* [Control
registry]. `registries/DISTANCE_TO_GR_LEDGER.csv`
