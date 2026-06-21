<!-- authority: control -->

# Mathematical Decisiveness Phase 9 Metrics Report

## Analysis

This report is generated from tracked research-control registries and completion YAML files. It evaluates the AI research-agent system as an operational system. It does not promote a physics claim, adopt a source law, construct `M_src`, or treat validator success as physics evidence.

## Source Basis

- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/tasks/*/jobs/completions/*.yaml`

## Input Counts

| Metric | Value |
| --- | --- |
| `tasks_registered` | `234` |
| `jobs_registered` | `234` |
| `completions_read` | `234` |
| `physics_completions_read` | `125` |
| `claim_boundary_rows` | `235` |
| `active_claim_boundary_rows` | `235` |

## Claim Hygiene Metrics

| Metric | Value |
| --- | --- |
| `tasks_with_forbidden_conclusion_summary` | `1` |
| `physics_promotion_authorized_true` | `0` |
| `physics_promotion_authorized_false` | `1` |
| `claim_boundary_rows_active` | `235` |

## Physics Progress Metrics

| Metric | Value |
| --- | --- |
| `tasks_with_distance_to_gr_delta_true` | `1` |
| `tasks_with_distance_to_gr_delta_false` | `0` |
| `burden_discharged_count` | `0` |
| `candidate_constructed_count` | `2` |
| `precise_obstruction_count` | `0` |
| `route_frozen_count` | `0` |
| `human_gate_required_count` | `0` |
| `physics_progress_status_counts` | `{"candidate_constructed_pending_audit": 1}` |

## Obstruction Reuse Metrics

| Metric | Value |
| --- | --- |
| `obstruction_records_created` | `0` |
| `obstruction_records_referenced_by_later_tasks` | `0` |
| `repeated_obstructions_triggering_freeze_review` | `0` |
| `frozen_routes_reopened_by_human_gate` | `2` |

## Agent Workflow Metrics

| Metric | Value |
| --- | --- |
| `selector_tasks` | `8` |
| `candidate_constructor_tasks` | `10` |
| `smuggling_auditor_tasks` | `33` |
| `refuter_tasks` | `31` |
| `gate_chair_tasks` | `1` |
| `average_tasks_per_construct_audit_stress_cycle` | `2.71` |
| `construct_audit_stress_cycle_count` | `7` |
| `selector_cycles_without_construction` | `6` |

## Limitations

- Counts are descriptive operational diagnostics, not physics evidence.
- Obstruction reuse is measured by completion-level obstruction IDs and later completion references.
- Validator failure history is not a durable event log, so this report does not infer blocked violation counts from past terminal output.

## Conclusion

Phase 9 provides an operational metrics layer for future evaluation. The metrics show whether tracked work is producing candidates, obstructions, freeze reviews, human-gate requirements, or repeated selector cycles. They do not change the authority of any scientific artifact.

## References

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations implementation plan* [Local implementation plan].

The AEther-Flow Research Project. (2026, June 21). *Agent job registry* [Project-control registry].

The AEther-Flow Research Project. (2026, June 21). *Claim boundary registry* [Project-control registry].
