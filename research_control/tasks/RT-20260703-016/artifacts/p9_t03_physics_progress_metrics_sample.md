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
| `tasks_registered` | `671` |
| `jobs_registered` | `671` |
| `completions_read` | `671` |
| `physics_completions_read` | `400` |
| `claim_boundary_rows` | `628` |
| `active_claim_boundary_rows` | `628` |
| `completion_validation_status_counts` | `{"PASS": 670, "PASS_WITH_SURFACE_AUDIT_FINDINGS": 1}` |
| `tasks_with_forbidden_conclusion_summary` | `340` |
| `physics_promotion_authorized_true` | `27` |
| `physics_promotion_authorized_false` | `313` |
| `claim_boundary_rows_active` | `628` |
| `selector_tasks` | `83` |
| `candidate_constructor_tasks` | `47` |
| `smuggling_auditor_tasks` | `79` |
| `refuter_tasks` | `77` |
| `gate_chair_tasks` | `31` |
| `average_tasks_per_construct_audit_stress_cycle` | `2.95` |
| `construct_audit_stress_cycle_count` | `37` |
| `selector_cycles_without_construction` | `65` |
| `support_only_checker_report_files_scanned` | `5` |
| `support_only_checker_report_parse_errors` | `0` |
| `support_only_checker_reports_found` | `2` |
| `support_only_checker_status_counts` | `{"pass_support_only": 2}` |
| `support_only_checker_forbidden_overread_reports` | `0` |
| `support_only_checker_physics_obstruction_reports` | `0` |
| `support_only_checker_boundary_mismatch_reports` | `0` |
| `support_only_checker_tooling_error_reports` | `0` |

## Scientific Progress Metrics

| Metric | Value |
| --- | --- |
| `distance_to_gr_delta_true_count` | `183` |
| `distance_to_gr_delta_false_count` | `183` |
| `burden_discharged_count` | `18` |
| `constructed_candidate_count` | `67` |
| `candidate_smuggling_audit_pass_count` | `43` |
| `candidate_refuter_stress_pass_count` | `34` |
| `precise_obstruction_count` | `26` |
| `minimal_countermodel_count` | `1` |
| `route_frozen_count` | `1` |
| `human_gate_required_count` | `23` |
| `obstruction_records_created` | `33` |
| `obstruction_records_referenced_by_later_tasks` | `24` |
| `repeated_obstructions_triggering_freeze_review` | `213` |
| `frozen_routes_reopened_by_human_gate` | `16` |
| `physics_progress_status_counts` | `{"burden_advanced": 2, "burden_discharged": 18, "candidate_audit_passed_pending_stress": 1, "candidate_audited_pending_stress": 43, "candidate_constructed_pending_audit": 40, "candidate_stress_passed_pending_gate": 34, "candidate_stress_survived_pending_selector": 5, "comparison_only_no_distance_delta": 1, "control_checklist_no_distance_delta": 1, "control_note_no_distance_delta": 2, "control_template_no_distance_delta": 1, "control_validation_only": 1, "dependency_audit_no_distance_delta": 1, "documentation_control_no_distance_delta": 16, "documentation_or_control_only_no_physics_delta": 9, "external_review_no_distance_delta": 1, "formalized_precondition_target_no_distance_delta": 1, "human_gate_required": 23, "invalid_under_claim_boundary": 1, "no_distance_delta": 19, "precise_obstruction_found": 16, "precise_obstruction_found_no_distance_delta": 1, "process_control_no_distance_delta": 33, "project_control_no_distance_delta": 2, "project_control_validation_no_distance_delta": 1, "proposal_only_law_target_formalized_pending_audit": 1, "route_frozen": 1, "route_selector_no_distance_delta": 1, "routing_control_no_distance_delta": 1, "selector_only_no_distance_delta": 49, "selector_routes_to_candidate_constructor_bridge_attempt": 1, "source_acquisition_only_no_distance_delta": 1, "source_extension_adopted": 9, "source_extension_evidence_accepted": 7, "support_only_formalization_no_distance_delta": 1, "support_only_schema_no_distance_delta": 1, "support_only_tooling_design_no_distance_delta": 1, "traceability_only_no_distance_delta": 1, "unchanged": 12}` |

## Payload-Density Metrics

| Metric | Value |
| --- | --- |
| `physics_completions_read` | `400` |
| `total_payload_items` | `865` |
| `tasks_since_last_distance_to_gr_delta` | `2` |
| `tasks_since_last_burden_discharged` | `4` |
| `new_payload_items_per_physics_task` | `2.16` |
| `new_payload_items_per_cycle` | `16.55` |
| `selector_cycles_without_new_payload` | `0` |

## Route-Orbit Risk Metrics

| Metric | Value |
| --- | --- |
| `same_burden_repetition_count` | `0` |
| `freeze_reviews_triggered_by_repetition` | `213` |
| `bridge_attempts_since_last_gate` | `0` |
| `obstructions_created` | `19` |
| `obstructions_created_missing_id` | `0` |
| `obstructions_reused` | `24` |
| `candidate_construct_audit_stress_selector_cycles` | `10` |
| `gate_ready_cycles_without_gate_verdict` | `227` |
| `support_only_tooling_reports` | `2` |
| `physics_promotion_authorized_true_count` | `27` |
| `physics_promotion_authorized_false_count` | `239` |

## Physics-Progress Integration Metrics

| Metric | Value |
| --- | --- |
| `status` | `pass` |
| `authority_boundary` | `operational_summary_only_not_physics_proof` |
| `not_physics_proof` | `True` |
| `physics_claim_promotion_authorized` | `False` |
| `distance_delta` | `{"changed_false_count": 183, "changed_true_count": 183, "effect_counts": {"missing_effect": 668, "no_distance_delta": 3}, "records_read": 671}` |
| `separate_packet_counts` | `{"candidate_packet_count": 165, "freeze_packet_count": 228, "obstruction_packet_count": 34, "process_only_packet_count": 341, "theorem_packet_count": 108}` |
| `candidate_result_counts` | `{"constructed_candidate": 27, "constructed_target_pending_candidate_constructor": 1, "minimal_countermodel": 1, "precise_obstruction": 10}` |
| `payload_density_summary` | `{"classified_item_count": 1224, "mathematical_payload_item_count": 790, "mathematical_payload_task_count": 330, "payload_class_counts": {"conditional_theorem": 20, "countermodel": 45, "dependency_map_update": 122, "documentation_only": 78, "finite_witness": 183, "new_definition": 43, "new_theorem_statement": 129, "obstruction": 138, "proof_attempt": 0, "proved_theorem": 1, "route_selector_only": 152, "source_extension_classification": 109, "validator_tooling_only": 204}, "payload_density": 0.645425, "process_only_item_count": 434, "process_only_task_count": 341, "task_count": 671, "task_payload_density": 0.491803}` |

## Diagnostic Warnings

| Warning | Metric | Observed | Threshold | Hard Gate | Physics Authority |
| --- | --- | --- | --- | --- | --- |
| `candidate_missing_result` | `candidate_constructor_result_missing_count` | `9` | `0` | `False` | `False` |
| `gate_ready_without_gate` | `gate_ready_cycles_without_gate_verdict` | `227` | `0` | `False` | `False` |

## Separation Guard

| Metric | Value |
| --- | --- |
| `status` | `pass` |
| `operational_metric_key_tokens` | `['checker', 'diagnostic_warning', 'generated', 'handoff_continuity', 'memory', 'payload_density', 'receipt', 'registry', 'role_schema', 'route_orbit', 'validation', 'validator', 'wiki']` |
| `scientific_key_violations` | `[]` |
| `rule` | `Operational checker validation registry generated memory wiki receipt role-schema handoff-continuity payload-density route-orbit and diagnostic-warning metrics stay out of scientific_progress_metrics.` |

## Limitations

- Operational validation metrics are workflow diagnostics and not physics evidence.
- Support-only checker report counts are operational tooling diagnostics; checker syntax or boundary failures are not physics failures.
- Scientific progress metrics are counts of tracked science-claim fields and must still cite source artifacts before any claim is reused.
- Obstruction reuse is measured by completion-level obstruction IDs and later completion references.
- Validator failure history is not a durable event log, so this report does not infer blocked violation counts from past terminal output.

## Conclusion

This report provides separated operational and scientific scoreboards for future evaluation. The metrics show workflow health separately from tracked science-result fields. They do not change the authority of any scientific artifact.

## References

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations implementation plan* [Local implementation plan].

The AEther-Flow Research Project. (2026, June 21). *Agent job registry* [Project-control registry].

The AEther-Flow Research Project. (2026, June 21). *Claim boundary registry* [Project-control registry].
