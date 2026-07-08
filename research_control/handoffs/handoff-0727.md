---
authority: control
handoff_id: "handoff-0727"
created_at: "2026-07-08T19:57:05Z"
created_by_task_id: "RT-20260708-034"
created_by_job_id: "AJ-RT-20260708-034-001"
supersedes_handoff_id: "handoff-0726"
---

# Handoff 0727

## Summary

RT-20260708-034 completed v18 P9-T03. It calibrated public Markdown pages,
paired source specs, and publication briefs to status-card v2 wording:
positive status, exact scope, blocked overread, and next burden.

The update reduces public cognitive load without changing claim status. It is
documentation-only project-control work. It records no Distance-to-GR ledger
delta and no physics promotion.

## Outputs

- `README.md`
- `github-facing/project-overview-explainer.md`
- `github-facing/proof-state-dashboard-explainer.md`
- `github-facing/source-authority-explainer.md`
- `github-facing/aether-flow-physics-program-explainer.md`
- `github-facing/aether-flow-ontology-explainer.md`
- `github-facing/gr-derivation-roadmap-explainer.md`
- `github-facing/claim-gates-explainer.md`
- `github-facing/negative-results-and-obstructions-explainer.md`
- `markdown/html-explainer-specs/*.md`
- `markdown/publication-briefs/*.md`
- `html/*.html` metadata-only source-basis hash synchronization for affected pages
- `research_control/tasks/RT-20260708-034/artifacts/p9_t03_public_docs_status_cards_report.json`
- `research_control/tasks/RT-20260708-034/artifacts/public_documentation_cognitive_load_calibration_receipt.md`

## Boundary

This documentation update is not proof authority, routing authority, a
Distance-to-GR ledger override, a physics truth ranking, source-law adoption,
detector-semantics adoption, matter-coupling derivation, Einstein-equation
derivation, benchmark promotion, Gate Chair verdict, completed derivation,
future source-extension impossibility, or program-wide no-go conclusion.

Generated HTML prose and layout were not regenerated. The affected generated
HTML files received metadata-only `aether-flow-source-basis-hash`
synchronization because the established explainer validation pipeline requires
derivatives to point at the current registered source-spec hash. A later
bounded publication or renderer packet may fully regenerate those derivatives
if selected by tracked control state.

## Next Action

Run one bounded v18 P9-T04 `status_card_v2_linter_tests` packet.

Expected scope: add linter tests for missing next-burden fields and
caveat-wall public summaries while keeping overclaims as hard failures.

## APA 7 Source Materials

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v18* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`.

The AEther-Flow Research Project. (2026b). *Status card v2 schema* [Internal
project-control schema]. `research_control/design/status_card_v2_schema.md`.

The AEther-Flow Research Project. (2026c). *Accepted status calibration v2*
[Internal project-control calibration data].
`research_control/design/accepted_status_calibration_v2.yaml`.
