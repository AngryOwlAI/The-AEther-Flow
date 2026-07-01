# P3-T04 Claim-Language Remediation Receipt

## Objective

Remediate current public and current-control claim-language hard failures from
the default linter scan while preserving historical implementation-plan
provenance and all physics claim gates.

## Source Edits

Current public and current-control source wording was remediated in:

- `README.md`
- `github-facing/exact-gr-benchmark-boundary-explainer.md`
- `markdown/publication-briefs/claim-gates.publication-brief.md`
- `markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md`
- `html/gr-derivation-roadmap-explainer.html` source-basis metadata only
- `research_control/design/frontier_theorem_inventory.md`
- `research_control/design/high_risk_selector_checklist.md`
- `research_control/design/support_only_formalization_lane_v1.md`
- `research_control/design/documentation_curator_corpus_migration_plan.md`
- `research_control/design/no_leap_route_rule.md`
- `research_control/design/distance_to_gr_status_layers_v1.md`
- `research_control/design/director_led_agent_architecture_grill_decisions.md`

## Historical Warning Treatment

Older implementation plans were not rewritten for lint satisfaction. The packet
instead records reviewed-context entries in
`research_control/design/claim_language_linter_reviewed_contexts.yaml` for the
historical implementation-plan backlog. These entries classify those surfaces as
historical artifacts and keep their findings at `warn_historical`.

## Linter Result

Command:

```text
.venv/bin/python scripts/project_control/validate_claim_language.py --json
```

Result:

- status: `PASS`
- hard-fail findings: `0`
- warning findings: `2990`
- total findings: `2990`
- scanned paths: `2340`

## Boundary

This packet changes documentation and control wording only. The HTML change is
limited to generated source-basis metadata required by the canonical source
spec hash. It does not adopt a source law, modify ontology, derive matter
coupling, derive Einstein equations, promote benchmark status, or complete a
derivation.

## Next Route

Run one bounded v14 `P3-T05` claim-language phase validation packet.
