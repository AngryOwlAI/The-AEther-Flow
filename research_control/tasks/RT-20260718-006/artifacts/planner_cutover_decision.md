# P11-T04 planner cutover decision

Decision: `REPAIR_REQUIRED`.

## Result

Local equivalence and rollback checks pass, but planner authority cannot be cut over because required execution and current-head hosted-CI evidence is absent while tracked defaults still preserve shadow-planner legacy authority.

## Blocking findings

- `tracked_manifest_epoch_remains_shadow_planner`
- `tracked_manifest_execution_authority_remains_legacy`
- `full_profile_plan_is_selection_only`
- `no_tracked_default_adapter_binding_for_full_planner_execution`
- `no_official_ci_shadow_run_for_current_head`
- `ci_shadow_shards_remain_non_authoritative`
- `ci_default_still_names_shadow_execution`
- `matched_authoritative_planner_full_receipt_absent`

## Safety failures

- None observed in the bounded local audit.

## Authority boundary

Legacy validation remains authoritative unless every cutover criterion is directly proven. This operational decision does not change ordinary research, scientific claims, proof authority, benchmark status, ontology, or Distance-to-GR status.

## Next route

Create one separately bounded P11-T04 Validator Engineer repair that implements an explicit planner-authoritative execution binding and obtains matched current-head local checkpoint full and hosted-CI receipts while retaining the tested legacy fallback; do not execute P11-T05 yet.
