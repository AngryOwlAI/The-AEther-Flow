---
authority: control
handoff_id: "handoff-0728"
created_at: "2026-07-08T20:41:56Z"
created_by_task_id: "RT-20260708-035"
created_by_job_id: "AJ-RT-20260708-035-001"
supersedes_handoff_id: "handoff-0727"
---

# Handoff 0728

## Summary

RT-20260708-035 completed v18 P9-T04. It added status-card v2
claim-language linter coverage for missing next-burden statements and
caveat-wall public summaries.

The update is validator-only project-control work. It records no
Distance-to-GR ledger delta and no physics promotion.

## Outputs

- `scripts/project_control/validate_claim_language.py`
- `research_control/design/claim_language_linter_taxonomy.yaml`
- `tests/test_validate_claim_language.py`
- `tests/fixtures/claim_language/status_card_v2_valid.md`
- `tests/fixtures/claim_language/status_card_v2_missing_next_burden.md`
- `tests/fixtures/claim_language/status_card_v2_caveat_wall.md`
- `research_control/tasks/RT-20260708-035/artifacts/validate_p9_t04_status_card_v2_linter.py`
- `research_control/tasks/RT-20260708-035/artifacts/p9_t04_status_card_v2_linter_report.json`
- `research_control/tasks/RT-20260708-035/artifacts/p9_t04_status_card_v2_linter_receipt.md`

## Result

- Valid status-card v2 wording passes without findings.
- Missing next-burden wording warns as
  `status_card_v2_missing_next_burden`.
- Caveat-wall public-summary wording warns as
  `caveat_wall_public_summary`.
- Explicit overclaim wording still hard-fails as
  `einstein_equation_overclaim`.

## Boundary

This validator update is not proof authority, routing authority beyond the
tracked next route, a Distance-to-GR ledger override, physics truth ranking,
source-law adoption, detector-semantics adoption, coupling-law adoption,
matter-coupling derivation, Einstein-equation derivation, benchmark promotion,
Gate Chair verdict, completed derivation, future source-extension
impossibility, or program-wide no-go conclusion.

## Next Action

Run one bounded v18 P9-T05 `public_cognitive_load_red_team_review` packet.

Expected scope: review public and reader-facing status surfaces for overclaim,
underclaim, cognitive overload, and generated-surface authority confusion.

## APA 7 Source Materials

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v18* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v18.md`.

The AEther-Flow Research Project. (2026b). *Status card v2 schema* [Internal
project-control schema]. `research_control/design/status_card_v2_schema.md`.

The AEther-Flow Research Project. (2026c). *Accepted status calibration v2*
[Internal project-control calibration data].
`research_control/design/accepted_status_calibration_v2.yaml`.
