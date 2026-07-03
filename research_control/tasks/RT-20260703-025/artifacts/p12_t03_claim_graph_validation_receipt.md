<!-- authority: control -->

# P12-T03 Claim Graph Validation Receipt

## Summary

`RT-20260703-025` completed one bounded v15 P12-T03 claim graph validation
packet. The packet added `scripts/research_control/validate_claim_graph_v1.py`,
focused unit tests, a deliberately bad fixture graph, and a local
CI-equivalent command-plan hook.

## Validation Rules

The validator enforces the P12-T03 rule set:

- every high-risk positive node has blocked-overread edges;
- every accepted evidence-precondition node has downstream
  `does_not_establish` edges;
- every generated derivative node has an `is_derivative_of` edge;
- every Gate Chair node has an exact authority path;
- benchmark-promotion edges are negative/non-establishing or human-gated;
- scoped evidence cannot reach completed derivation without matter-coupling,
  Einstein-equation, and benchmark-promotion intermediates.

## Outputs

| Output | Status |
| --- | --- |
| `scripts/research_control/validate_claim_graph_v1.py` | added |
| `tests/test_validate_claim_graph_v1.py` | added |
| `tests/fixtures/research_control/claim_graph_v1_bad_missing_guards.json` | added |
| `research_control/tasks/RT-20260703-025/artifacts/p12_t03_claim_graph_validation_report.json` | `PASS` |
| `research_control/tasks/RT-20260703-025/artifacts/p12_t03_bad_fixture_validation_report.json` | expected `FAIL` |
| `scripts/research_control/run_full_research_control_validation.py` | local CI hook added |

## Claim Boundary

The validator is project-control tooling only. It is not a physics source, not
proof authority, not a source-law adoption, not matter semantics, not detector
semantics, not a coupling law, not matter coupling, not stress-energy
semantics, not a matter action, not a variation principle, not Einstein
equations, not benchmark promotion, and not completed derivation.

## Verification

- Validator and local CI runner compile: `PASS`.
- Focused validator and local-CI-plan unit tests: `PASS`.
- Current graph validation report: `PASS`.
- Bad fixture validation report: expected `FAIL`.

## Next Route

Phase P12 is complete. The logical next step is one bounded v15 P13-T01
high-risk wording audit packet under `process-integrity-auditor@0.1.0`.

## Source Materials

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v15* [Implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.

The AEther-Flow Research Project. (2026b). *Claim graph schema v1*
[Project-control schema]. `research_control/design/claim_graph_schema_v1.md`.

The AEther-Flow Research Project. (2026c). *Claim graph v1*
[Generated project-control graph]. `output/claim_graph_v1.json`.

The AEther-Flow Research Project. (2026d). *Handoff 0543*
[Research-control handoff]. `research_control/handoffs/handoff-0543.yaml`.
