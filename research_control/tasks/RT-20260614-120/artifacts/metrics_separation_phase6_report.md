<!-- authority: control -->

# Research-Control Metrics Separation Report

## Analysis

This report is generated from tracked research-control registries and completion YAML files. It evaluates the AI research-agent system as an operational system. It does not promote a physics claim, adopt a source law, construct `M_src`, or treat validator success as physics evidence.

## Source Basis

- `registries/RESEARCH_TASK_REGISTRY.csv`
- `registries/AGENT_JOB_REGISTRY.csv`
- `registries/AGENT_ROLE_REGISTRY.csv`
- `registries/CLAIM_BOUNDARY_REGISTRY.csv`
- `research_control/tasks/*/jobs/completions/*.yaml`

## Operational Validation Metrics

| Metric | Value |
| --- | --- |
| `tasks_registered` | `284` |
| `jobs_registered` | `284` |
| `completions_read` | `284` |
| `physics_completions_read` | `154` |
| `claim_boundary_rows` | `285` |
| `active_claim_boundary_rows` | `285` |
| `completion_validation_status_counts` | `{"PASS": 283, "PASS_WITH_SURFACE_AUDIT_FINDINGS": 1}` |
| `tasks_with_forbidden_conclusion_summary` | `36` |
| `physics_promotion_authorized_true` | `2` |
| `physics_promotion_authorized_false` | `34` |
| `claim_boundary_rows_active` | `285` |
| `selector_tasks` | `13` |
| `candidate_constructor_tasks` | `13` |
| `smuggling_auditor_tasks` | `41` |
| `refuter_tasks` | `39` |
| `gate_chair_tasks` | `3` |
| `average_tasks_per_construct_audit_stress_cycle` | `2.82` |
| `construct_audit_stress_cycle_count` | `11` |
| `selector_cycles_without_construction` | `11` |

## Scientific Progress Metrics

| Metric | Value |
| --- | --- |
| `distance_to_gr_delta_true_count` | `25` |
| `distance_to_gr_delta_false_count` | `5` |
| `burden_discharged_count` | `0` |
| `constructed_candidate_count` | `11` |
| `candidate_smuggling_audit_pass_count` | `8` |
| `candidate_refuter_stress_pass_count` | `7` |
| `precise_obstruction_count` | `1` |
| `minimal_countermodel_count` | `0` |
| `route_frozen_count` | `0` |
| `human_gate_required_count` | `0` |
| `obstruction_records_created` | `1` |
| `obstruction_records_referenced_by_later_tasks` | `0` |
| `repeated_obstructions_triggering_freeze_review` | `24` |
| `frozen_routes_reopened_by_human_gate` | `2` |
| `physics_progress_status_counts` | `{"candidate_audited_pending_stress": 8, "candidate_constructed_pending_audit": 7, "candidate_stress_passed_pending_gate": 7, "precise_obstruction_found": 1, "selector_only_no_distance_delta": 5, "source_extension_adopted": 1}` |

## Separation Guard

| Metric | Value |
| --- | --- |
| `status` | `pass` |
| `operational_metric_key_tokens` | `['generated', 'handoff_continuity', 'memory', 'receipt', 'registry', 'role_schema', 'validation', 'validator', 'wiki']` |
| `scientific_key_violations` | `[]` |
| `rule` | `Operational validation registry generated memory wiki receipt role-schema and handoff-continuity metrics stay out of scientific_progress_metrics.` |

## Limitations

- Operational validation metrics are workflow diagnostics and not physics evidence.
- Scientific progress metrics are counts of tracked science-claim fields and must still cite source artifacts before any claim is reused.
- Obstruction reuse is measured by completion-level obstruction IDs and later completion references.
- Validator failure history is not a durable event log, so this report does not infer blocked violation counts from past terminal output.

## Conclusion

This report provides separated operational and scientific scoreboards for future evaluation. The metrics show workflow health separately from tracked science-result fields. They do not change the authority of any scientific artifact.

## References

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations implementation plan* [Local implementation plan].

The AEther-Flow Research Project. (2026, June 21). *Agent job registry* [Project-control registry].

The AEther-Flow Research Project. (2026, June 21). *Claim boundary registry* [Project-control registry].
