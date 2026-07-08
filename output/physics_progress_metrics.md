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
- `research_control/design/ai_research_agent_metrics_taxonomy_v1.md`
- `research_control/design/physics_payload_ratio_policy_v1.md`

## Operational Validation Metrics

| Metric | Value |
| --- | --- |
| `tasks_registered` | `860` |
| `jobs_registered` | `860` |
| `completions_read` | `860` |
| `physics_completions_read` | `469` |
| `claim_boundary_rows` | `817` |
| `active_claim_boundary_rows` | `807` |
| `completion_validation_status_counts` | `{"PASS": 832, "PASS_WITH_SURFACE_AUDIT_FINDINGS": 1, "unknown": 27}` |
| `tasks_with_forbidden_conclusion_summary` | `402` |
| `physics_promotion_authorized_true` | `27` |
| `physics_promotion_authorized_false` | `375` |
| `claim_boundary_rows_active` | `807` |
| `selector_tasks` | `103` |
| `candidate_constructor_tasks` | `54` |
| `smuggling_auditor_tasks` | `86` |
| `refuter_tasks` | `88` |
| `gate_chair_tasks` | `31` |
| `average_tasks_per_construct_audit_stress_cycle` | `2.93` |
| `construct_audit_stress_cycle_count` | `41` |
| `selector_cycles_without_construction` | `84` |
| `support_only_checker_report_files_scanned` | `9` |
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
| `distance_to_gr_delta_false_count` | `361` |
| `burden_discharged_count` | `18` |
| `constructed_candidate_count` | `74` |
| `candidate_smuggling_audit_pass_count` | `45` |
| `candidate_refuter_stress_pass_count` | `34` |
| `precise_obstruction_count` | `26` |
| `minimal_countermodel_count` | `1` |
| `route_frozen_count` | `1` |
| `human_gate_required_count` | `23` |
| `obstruction_records_created` | `33` |
| `obstruction_records_referenced_by_later_tasks` | `24` |
| `repeated_obstructions_triggering_freeze_review` | `229` |
| `frozen_routes_reopened_by_human_gate` | `16` |
| `physics_progress_status_counts` | `{"burden_advanced": 2, "burden_discharged": 18, "candidate_audit_passed_pending_stress": 1, "candidate_audited_pending_stress": 45, "candidate_constructed_pending_audit": 42, "candidate_cycle_integrated_no_adoption": 1, "candidate_stress_passed_pending_gate": 34, "candidate_stress_survived_pending_selector": 7, "ci_update_no_physics_delta": 1, "comparison_only_no_distance_delta": 1, "control_checklist_no_distance_delta": 1, "control_note_no_distance_delta": 2, "control_template_no_distance_delta": 1, "control_validation_only": 1, "dashboard_update_no_physics_delta": 1, "dependency_audit_no_distance_delta": 1, "detector_readout_audited_no_adoption": 1, "detector_readout_burden_design_no_adoption": 1, "detector_readout_candidate_no_adoption": 1, "detector_readout_route_selected_no_adoption": 1, "detector_readout_setup_no_adoption": 1, "detector_readout_stressed_no_adoption": 1, "detector_replacement_audited_source_pure_as_written_pending_stress": 1, "detector_replacement_candidate_constructed_pending_audit": 1, "detector_replacement_stress_survived_pending_selector": 1, "detector_route_selected_no_adoption": 1, "docs_no_physics_delta": 1, "documentation_control_no_distance_delta": 16, "documentation_or_control_only_no_physics_delta": 11, "eqsrc_family_closure_audited_source_pure_as_written_no_promotion": 1, "eqsrc_family_stressed_no_promotion": 1, "external_review_no_distance_delta": 1, "finite_local_negative_fixtures_recorded": 1, "finite_local_witness_recorded": 3, "finite_toy_response_v2_model_constructed_no_promotion": 1, "finite_toy_response_v2_source_spec_no_promotion": 1, "formalization_selector_no_proof_authority": 1, "formalization_support_no_physics_delta": 1, "formalized_precondition_target_no_distance_delta": 1, "frontier_sync_no_promotion": 1, "human_gate_required": 23, "invalid_under_claim_boundary": 1, "ledger_question_setup_no_delta": 1, "memory_integration_no_physics_delta": 1, "methodology_memo_no_physics_delta": 1, "methodology_metrics_no_physics_delta": 1, "metrics_tool_update_no_physics_delta": 1, "no_distance_delta": 22, "precise_obstruction_found": 16, "precise_obstruction_found_no_distance_delta": 1, "process_control_no_distance_delta": 42, "project_control_backlog_no_physics_delta": 2, "project_control_bridge_no_distance_delta": 1, "project_control_coverage_audit_no_distance_delta": 1, "project_control_documentation_impact_no_distance_delta": 1, "project_control_final_validation_no_distance_delta": 1, "project_control_frontier_refresh_no_distance_delta": 1, "project_control_no_distance_delta": 3, "project_control_plan_registration_no_physics_delta": 2, "project_control_renderer_no_distance_delta": 1, "project_control_schema_no_distance_delta": 1, "project_control_validation_inventory_no_distance_delta": 1, "project_control_validation_no_distance_delta": 1, "project_control_validator_no_distance_delta": 1, "project_system_ci_repair_no_physics_delta": 1, "proposal_only_law_target_formalized_pending_audit": 1, "record_local_theorem_candidate_no_distance_delta": 1, "red_team_review_no_physics_delta": 3, "route_frozen": 1, "route_selector_no_distance_delta": 1, "routing_control_no_distance_delta": 1, "schema_defined": 1, "schema_no_physics_delta": 1, "selector_no_adoption": 1, "selector_no_promotion": 3, "selector_only_no_distance_delta": 49, "selector_routes_to_candidate_constructor_bridge_attempt": 1, "source_acquisition_only_no_distance_delta": 1, "source_extension_adopted": 9, "source_extension_evidence_accepted": 7, "support_only_conditional_theorem_no_distance_delta": 1, "support_only_formalization_no_distance_delta": 4, "support_only_schema_no_distance_delta": 1, "support_only_tooling_design_no_distance_delta": 1, "theoretical_decision_selected": 5, "tooling_update_no_physics_delta": 2, "toy_model_stressed_no_promotion": 1, "toy_model_zoo_integrated_no_promotion": 1, "toy_selector_no_promotion": 1, "traceability_only_no_distance_delta": 1, "typed_eqsrc_object_audited_source_pure_as_written_no_promotion": 1, "typed_eqsrc_object_defined_no_promotion": 1, "typed_eqsrc_problem_statement_no_promotion": 1, "typed_eqsrc_stressed_no_promotion": 1, "unchanged": 12, "v16_completed_ordinary_continuation_selected_no_distance_delta": 1, "v17_completed_ordinary_continuation_selected": 1, "v17_final_validation_no_promotion": 1, "v17_integration_no_promotion": 1, "v17_p0_t03_active_state_preflight_passed_no_physics_delta": 1, "v18_p0_t03_active_state_preflight_passed_no_physics_delta": 1, "v18_p0_t04_recommendation_coverage_seed_completed_no_physics_delta": 1, "v18_p1_t01_active_state_bifurcation_policy_defined_no_physics_delta": 1, "v18_p1_t02_active_state_bifurcation_renderer_completed_no_physics_delta": 1, "v18_p1_t03_active_state_sidecar_validator_completed_no_physics_delta": 1, "v18_p1_t04_active_state_bifurcation_red_team_repair_required_no_physics_delta": 1, "v18_p1_t04_repair_active_state_supersession_guard_completed_no_physics_delta": 1, "validator_fixture_catalog_no_distance_delta": 1, "validator_integration_no_distance_delta": 1, "validator_update_no_physics_delta": 1}` |

## Payload-Density Metrics

| Metric | Value |
| --- | --- |
| `physics_completions_read` | `469` |
| `total_payload_items` | `986` |
| `tasks_since_last_distance_to_gr_delta` | `71` |
| `tasks_since_last_burden_discharged` | `73` |
| `new_payload_items_per_physics_task` | `2.1` |
| `new_payload_items_per_cycle` | `16.33` |
| `selector_cycles_without_new_payload` | `0` |

## Route-Orbit Risk Metrics

| Metric | Value |
| --- | --- |
| `same_burden_repetition_count` | `1` |
| `freeze_reviews_triggered_by_repetition` | `228` |
| `bridge_attempts_since_last_gate` | `7` |
| `obstructions_created` | `19` |
| `obstructions_created_missing_id` | `0` |
| `obstructions_reused` | `24` |
| `candidate_construct_audit_stress_selector_cycles` | `11` |
| `gate_ready_cycles_without_gate_verdict` | `295` |
| `support_only_tooling_reports` | `2` |
| `physics_promotion_authorized_true_count` | `27` |
| `physics_promotion_authorized_false_count` | `270` |

## Physics-Payload Ratio Diagnostics

These metrics are AI-system diagnostics only. They do not rank physics truth, authorize proof, promote a benchmark, create a Gate Chair verdict, or complete a derivation.

| Metric | Value |
| --- | --- |
| `project_system_task_run_length` | `4` |
| `physics_bearing_task_run_length` | `0` |
| `new_mathematical_payload_count` | `1039` |
| `theorem_countermodel_candidate_count` | `626` |
| `candidate_construction_count` | `177` |
| `support_only_task_count_since_last_physics_payload` | `4` |
| `route_orbit_warning_status` | `{"advisory_only": true, "hard_gate": false, "physics_claim_authority": false, "status": "warning", "warning_ids": ["post_gate_cycle_repeat", "gate_ready_without_gate"]}` |
| `project_system_task_count` | `439` |
| `physics_bearing_task_count` | `386` |
| `support_only_task_count` | `455` |
| `physics_bearing_to_project_system_task_ratio` | `0.8793` |
| `new_mathematical_payload_to_support_only_task_ratio` | `2.2835` |
| `route_orbit_same_burden_repetition_count` | `1` |

## Physics-Progress Integration Metrics

| Metric | Value |
| --- | --- |
| `status` | `pass` |
| `authority_boundary` | `operational_summary_only_not_physics_proof` |
| `not_physics_proof` | `True` |
| `physics_claim_promotion_authorized` | `False` |
| `distance_delta` | `{"changed_false_count": 361, "changed_true_count": 183, "effect_counts": {"missing_effect": 685, "no_distance_delta": 175}, "records_read": 860}` |
| `separate_packet_counts` | `{"candidate_packet_count": 177, "freeze_packet_count": 257, "obstruction_packet_count": 34, "process_only_packet_count": 462, "theorem_packet_count": 119}` |
| `candidate_result_counts` | `{"constructed_candidate": 32, "constructed_target_pending_candidate_constructor": 1, "minimal_countermodel": 1, "precise_obstruction": 10}` |
| `payload_density_summary` | `{"classified_item_count": 1475, "mathematical_payload_item_count": 904, "mathematical_payload_task_count": 398, "payload_class_counts": {"conditional_theorem": 21, "countermodel": 56, "dependency_map_update": 142, "documentation_only": 101, "finite_witness": 225, "new_definition": 49, "new_theorem_statement": 144, "obstruction": 149, "proof_attempt": 0, "proved_theorem": 1, "route_selector_only": 167, "source_extension_classification": 117, "validator_tooling_only": 303}, "payload_density": 0.612881, "process_only_item_count": 571, "process_only_task_count": 462, "task_count": 860, "task_payload_density": 0.462791}` |

## AI Research-Agent Methodology Metrics

These diagnostics are support-only AI-system methodology metrics. They are separated from scientific progress metrics and do not authorize physics proof, source-law adoption, benchmark promotion, Gate Chair verdicts, or completed-derivation claims.

| Metric | Family | Status | Value | Interpretation |
| --- | --- | --- | --- | --- |
| `overclaim_catch_rate` | Claim-boundary control | `measured` | `0.9328` | Forbidden-conclusion summaries are counted as eligible overclaim-control surfaces; caught means no physics promotion was authorized. |
| `underclaim_warning_rate` | Claim-boundary control | `not_measured` | `None` | The current registries do not deterministically encode high-risk positive scoped-status omission events. |
| `obstruction_precision` | Obstruction quality | `measured` | `1.0` | This deterministic proxy counts obstruction records with IDs plus milestone, burden, or status context as locally scoped. |
| `route_orbit_rate` | Route dynamics | `measured` | `0.0021` | Repeated-burden streaks are process warnings only and do not change Distance-to-GR status. |
| `candidate_to_audit_conversion` | Candidate life cycle | `measured` | `0.8` | Candidate outputs are counted as audit-eligible only when tracked fields expose candidate result or pending-audit status. |
| `audit_to_stress_survival` | Candidate life cycle | `partial` | `1.0233` | This is an aggregate route-stage proxy; candidate lineage across audit and stress is not yet deterministic. |
| `stress_survival_rate` | Candidate life cycle | `partial` | `0.3864` | Stress survival is counted only as a non-promotional candidate-status outcome. |
| `human_gate_load` | Governance load | `measured` | `None` | Gate-load signals are governance workload diagnostics, not Gate Chair scientific verdicts. |
| `proof_to_process_ratio` | Payload balance | `measured` | `1.5832` | Payload balance compares mathematical payload items to process-only items; it is not proof authority. |

## AI Methodology Acceptance Warnings

| Warning | Metric | Status | Hard Gate | Physics Authority | Reason |
| --- | --- | --- | --- | --- | --- |
| `underclaim_warning_rate_not_measured` | `underclaim_warning_rate` | `not_measured` | `False` | `False` | Needs a future extraction rule for accepted-scoped evidence omitted from summaries. |
| `audit_to_stress_survival_partial` | `audit_to_stress_survival` | `partial` | `False` | `False` | Partial because the current completion records count stage occurrences, not candidate-linked transitions. |
| `stress_survival_rate_partial` | `stress_survival_rate` | `partial` | `False` | `False` | Partial because draft/control survivor lineage is not fully normalized across historical receipts. |

## Diagnostic Warnings

| Warning | Metric | Observed | Threshold | Hard Gate | Physics Authority |
| --- | --- | --- | --- | --- | --- |
| `post_gate_cycle_repeat` | `candidate_construct_audit_stress_selector_cycles` | `1` | `0` | `False` | `False` |
| `candidate_missing_result` | `candidate_constructor_result_missing_count` | `11` | `0` | `False` | `False` |
| `gate_ready_without_gate` | `gate_ready_cycles_without_gate_verdict` | `295` | `0` | `False` | `False` |

## Separation Guard

| Metric | Value |
| --- | --- |
| `status` | `pass` |
| `operational_metric_key_tokens` | `['ai_methodology', 'checker', 'diagnostic_warning', 'generated', 'handoff_continuity', 'memory', 'methodology', 'payload_density', 'payload_ratio', 'proof_to_process', 'receipt', 'registry', 'role_schema', 'route_orbit', 'validation', 'validator', 'wiki']` |
| `scientific_key_violations` | `[]` |
| `rule` | `Operational checker validation registry generated memory wiki receipt role-schema handoff-continuity payload-density route-orbit and diagnostic-warning metrics stay out of scientific_progress_metrics.` |

## Limitations

- Operational validation metrics are workflow diagnostics and not physics evidence.
- Support-only checker report counts are operational tooling diagnostics; checker syntax or boundary failures are not physics failures.
- Scientific progress metrics are counts of tracked science-claim fields and must still cite source artifacts before any claim is reused.
- Obstruction reuse is measured by completion-level obstruction IDs and later completion references.
- AI research-agent methodology metrics are support-only diagnostics and cannot be used as proof, source-law adoption, benchmark promotion, or Gate Chair verdicts.
- Physics-payload ratio diagnostics are AI-system diagnostics only; they do not rank physics truth.
- Validator failure history is not a durable event log, so this report does not infer blocked violation counts from past terminal output.

## Conclusion

This report provides separated operational and scientific scoreboards for future evaluation. The metrics show workflow health separately from tracked science-result fields. They do not change the authority of any scientific artifact.

## References

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations implementation plan* [Local implementation plan].

The AEther-Flow Research Project. (2026, June 21). *Agent job registry* [Project-control registry].

The AEther-Flow Research Project. (2026, June 21). *Claim boundary registry* [Project-control registry].
