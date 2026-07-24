---
authority: control
task_id: "RT-20260723-018"
job_id: "AJ-RT-20260723-018-001"
plan_task_id: "P13-T01"
decision: "HOLD_LEGACY_REPAIR_REQUIRED"
cutover_authorized: false
scientific_claims_changed: false
---

# P13-T01 validation-planner cutover decision

## Decision

`HOLD_LEGACY_REPAIR_REQUIRED`.

The bounded local burn-in has zero unexplained hard mismatches and the rollback path passes, but live cutover evidence is incomplete. Legacy execution remains authoritative.

The fixed component corpus and representative planner-selection families contain zero unexplained hard mismatches. That local result is necessary but not sufficient for a live cutover.

## Evidence gaps

- `live_manifest_epoch_remains_shadow_planner`
- `live_manifest_execution_authority_remains_legacy`
- `current_head_is_not_published_on_origin_main`
- `no_hosted_ci_run_for_current_head`
- `no_scheduled_full_run_for_current_head`
- `project_control_planner_jobs_remain_shadow_advisory`
- `three_clean_current_head_shadow_transactions_not_recorded`
- `affected_checkpoint_full_matched_execution_set_not_recorded`
- `uncached_current_head_final_staged_tree_comparison_pending`
- `current_head_safety_budget_receipt_not_recorded`

## Safety failures

- None observed.

## Authority boundary

The live manifest remains `shadow_planner` with `legacy` execution authority and the explicit rollback path retained. This operational audit does not change validation authority, workflow behavior, scientific status, ontology, benchmark status, proof authority, Distance-to-GR status, or publication authority.

## Reopening criteria

Re-run one fresh bounded P13-T01 authority audit only after the exact candidate checkpoint is published with explicit user authority and matched current-head hosted CI plus scheduled-full evidence is available; do not infer publication authority from this relay.
