# P3-T02 Linter Source Inventory

## Sources Inspected

| Source | Role | Finding |
| --- | --- | --- |
| `implementations_plans/recommendations_implementation_plan_continue_task-v14.md` | Route context | P3-T02 requires deterministic claim-language linter implementation, selected scan surfaces, JSON and human-readable output, reviewed whitelisting, and required tests. |
| `research_control/design/claim_language_linter_taxonomy.yaml` | Machine-readable config | Provides eighteen phrase classes, regex or near-term detection contracts, severity levels, surface policies, and required output fields. |
| `research_control/current_frontier.md` | Current status surface | Must remain free of hard-fail claim-language findings after denial and scoped-positive contexts are recognized. |
| `research_control/handoffs/handoff-0446.yaml` | Active routing authority | Requires exactly one bounded P3-T02 linter implementation packet before integration, remediation, or downstream physics work. |
| `.agents/roles/research_ops/validator-engineer.v0.2.0.md` | Role contract | Allows deterministic validator and test changes, while forbidding scientific role verdict or physics-source status changes. |

## Boundary

This packet implements validation tooling only. It does not remediate current public surfaces, wire the linter into checkpoint gates, or promote any physics claim.
