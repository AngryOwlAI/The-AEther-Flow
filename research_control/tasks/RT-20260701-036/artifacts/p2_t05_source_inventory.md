<!-- authority: control -->

# P2-T05 Source Inventory

## Scope

This receipt records the canonical sources inspected for the v14 P2 vocabulary
validation packet. It is project-control evidence only. It does not change
physics claim status.

## Canonical Sources Inspected

| Surface | Path | Status |
| --- | --- | --- |
| v14 implementation plan | `implementations_plans/recommendations_implementation_plan_continue_task-v14.md` | Contains P2-T05 acceptance criteria and next P3-T01 route. |
| active program state | `research_control/program_state.yaml` | Points to `RT-20260701-035` and `handoff-0444` before this packet. |
| latest handoff | `research_control/handoffs/handoff-0444.yaml` | Requires bounded P2-T05 vocabulary validation. |
| current frontier | `research_control/current_frontier.md` | Renders high-risk rows with scoped-positive reader-facing status. |
| scoped-positive vocabulary | `research_control/design/scoped_positive_claim_vocabulary.md` | Defines required P2-T01 vocabulary. |
| status alias map | `research_control/design/distance_to_gr_status_aliases.yaml` | Defines high-risk row and matter-coupling object aliases. |
| examples pack | `research_control/design/scoped_claim_language_examples.md` | Contains all required P2-T04 example categories. |
| Markdown registry | `registries/MARKDOWN_SOURCE_REGISTRY.csv` | Registers the Markdown P2 sources where applicable. |
| file registry | `registries/FILE_OBJECT_REGISTRY.csv` | Generated registry includes current frontier vocabulary and examples rows. |
| claim boundary registry | `registries/CLAIM_BOUNDARY_REGISTRY.csv` | Contains P2 claim-boundary rows through P2-T04. |
| Distance-to-GR ledger | `registries/DISTANCE_TO_GR_LEDGER.csv` | Remains authoritative for burden status. |

## Registry Coverage

- `MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V14` is registered as implementation-plan control guidance.
- `MD-RESEARCH-CONTROL-CURRENT-FRONTIER` is registered as a generated control snapshot.
- `MD-RESEARCH-CONTROL-DESIGN-SCOPED-POSITIVE-CLAIM-VOCABULARY` is registered as a control-language note.
- `MD-RESEARCH-CONTROL-DESIGN-SCOPED-CLAIM-LANGUAGE-EXAMPLES` is registered as control guidance.
- `research_control/design/distance_to_gr_status_aliases.yaml` is a tracked control map and is consumed by the current-frontier renderer; it is subordinate to the ledger.

## Verdict

The P2 vocabulary, alias, wording-pilot, and examples artifacts exist and are
coherent enough to support P3-T01 claim-language linter taxonomy. No artifact
is physics proof or promotion authority.
