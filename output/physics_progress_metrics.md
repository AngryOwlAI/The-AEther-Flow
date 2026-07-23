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
- `research_control/tasks/RT-20260722-014/artifacts/dual_budget_policy_v1.md`
- `research_control/tasks/RT-20260722-014/artifacts/budget_dashboard_schema_v1.md`
- `research_control/tasks/RT-20260722-015/artifacts/ordinary_route_guard_policy_v1.md`
- `research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_registry.json`
- `research_control/tasks/RT-20260723-004/artifacts/scientific_quality_metric_taxonomy_v1.md`
- `research_control/tasks/RT-20260723-004/artifacts/scientific_quality_calibration_warning_policy_v1.md`
- `research_control/tasks/RT-20260721-006/artifacts/v21_research_attempt_ledger.json`
- `research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_historical_seed.json`

## Operational Validation Metrics

| Metric | Value |
| --- | --- |
| `tasks_registered` | `1070` |
| `jobs_registered` | `1070` |
| `completions_read` | `1070` |
| `physics_completions_read` | `536` |
| `claim_boundary_rows` | `1027` |
| `active_claim_boundary_rows` | `899` |
| `completion_validation_status_counts` | `{"FAIL": 9, "PASS": 1031, "PASS_WITH_SURFACE_AUDIT_FINDINGS": 1, "PENDING": 1, "unknown": 28}` |
| `tasks_with_forbidden_conclusion_summary` | `492` |
| `physics_promotion_authorized_true` | `27` |
| `physics_promotion_authorized_false` | `465` |
| `claim_boundary_rows_active` | `899` |
| `selector_tasks` | `111` |
| `candidate_constructor_tasks` | `57` |
| `smuggling_auditor_tasks` | `99` |
| `refuter_tasks` | `95` |
| `gate_chair_tasks` | `31` |
| `average_tasks_per_construct_audit_stress_cycle` | `2.93` |
| `construct_audit_stress_cycle_count` | `42` |
| `selector_cycles_without_construction` | `92` |
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
| `distance_to_gr_delta_false_count` | `567` |
| `burden_discharged_count` | `25` |
| `constructed_candidate_count` | `91` |
| `candidate_smuggling_audit_pass_count` | `53` |
| `candidate_refuter_stress_pass_count` | `34` |
| `precise_obstruction_count` | `40` |
| `minimal_countermodel_count` | `1` |
| `route_frozen_count` | `2` |
| `human_gate_required_count` | `23` |
| `obstruction_records_created` | `48` |
| `obstruction_records_referenced_by_later_tasks` | `26` |
| `repeated_obstructions_triggering_freeze_review` | `281` |
| `frozen_routes_reopened_by_human_gate` | `16` |
| `physics_progress_status_counts` | `{"burden_advanced": 2, "burden_discharged": 25, "candidate_audit_passed_pending_stress": 1, "candidate_audited_pending_stress": 53, "candidate_constructed_pending_audit": 56, "candidate_cycle_integrated_no_adoption": 1, "candidate_stress_passed_pending_gate": 34, "candidate_stress_survived_pending_selector": 7, "ci_update_no_physics_delta": 1, "comparison_only_no_distance_delta": 1, "control_checklist_no_distance_delta": 1, "control_note_no_distance_delta": 2, "control_template_no_distance_delta": 1, "control_validation_only": 1, "coverage_audit_no_promotion_v18_complete": 1, "dashboard_update_no_physics_delta": 1, "dependency_audit_no_distance_delta": 1, "detector_readout_audited_no_adoption": 1, "detector_readout_burden_design_no_adoption": 1, "detector_readout_candidate_no_adoption": 1, "detector_readout_route_selected_no_adoption": 1, "detector_readout_setup_no_adoption": 1, "detector_readout_stressed_no_adoption": 1, "detector_replacement_audited_source_pure_as_written_pending_stress": 1, "detector_replacement_candidate_constructed_pending_audit": 1, "detector_replacement_stress_survived_pending_selector": 1, "detector_route_selected_no_adoption": 1, "docs_no_physics_delta": 1, "documentation_control_no_distance_delta": 16, "documentation_or_control_only_no_physics_delta": 25, "eqsrc_family_closure_audited_source_pure_as_written_no_promotion": 1, "eqsrc_family_stressed_no_promotion": 1, "external_review_no_distance_delta": 1, "finite_local_negative_fixtures_recorded": 1, "finite_local_witness_recorded": 3, "finite_toy_response_v2_model_constructed_no_promotion": 1, "finite_toy_response_v2_source_spec_no_promotion": 1, "formalization_selector_no_proof_authority": 1, "formalization_support_no_physics_delta": 1, "formalized_precondition_target_no_distance_delta": 1, "frontier_sync_no_promotion": 2, "human_gate_required": 23, "invalid_under_claim_boundary": 1, "ledger_question_setup_no_delta": 1, "memory_integration_no_physics_delta": 1, "methodology_memo_no_physics_delta": 1, "methodology_metrics_no_physics_delta": 1, "metrics_tool_update_no_physics_delta": 1, "no_distance_delta": 40, "ordinary_route_selected_no_promotion": 1, "precise_obstruction_found": 30, "precise_obstruction_found_no_distance_delta": 1, "process_control_no_distance_delta": 42, "project_control_backlog_no_physics_delta": 3, "project_control_bridge_no_distance_delta": 1, "project_control_candidate_lineage_completed_no_physics_delta": 1, "project_control_coverage_audit_no_distance_delta": 1, "project_control_documentation_impact_no_distance_delta": 1, "project_control_final_validation_no_distance_delta": 1, "project_control_frontier_refresh_no_distance_delta": 1, "project_control_no_distance_delta": 3, "project_control_plan_registration_no_physics_delta": 2, "project_control_prelaunch_audit_completed_no_physics_delta": 1, "project_control_renderer_no_distance_delta": 1, "project_control_schema_no_distance_delta": 1, "project_control_taxonomy_completed_no_physics_delta": 1, "project_control_validation_inventory_no_distance_delta": 1, "project_control_validation_no_distance_delta": 1, "project_control_validator_no_distance_delta": 1, "project_system_agent_output_consumption_no_physics_delta": 1, "project_system_baseline_no_physics_delta": 1, "project_system_cache_adversarial_audit_no_physics_delta": 1, "project_system_checkpoint_integration_no_physics_delta": 1, "project_system_checkpoint_memory_dedup_no_physics_delta": 1, "project_system_checkpoint_supersession_no_physics_delta": 1, "project_system_ci_repair_no_physics_delta": 1, "project_system_ci_shard_design_no_physics_delta": 1, "project_system_ci_shard_implementation_no_physics_delta": 1, "project_system_classifier_taxonomy_no_physics_delta": 1, "project_system_compact_reporting_no_physics_delta": 1, "project_system_control_wording_no_physics_delta": 1, "project_system_documentation_memory_scoping_no_physics_delta": 1, "project_system_execution_binding_repair_no_physics_delta": 1, "project_system_executor_cache_integration_no_physics_delta": 1, "project_system_hosted_ci_authority_audit_no_physics_delta": 1, "project_system_inventory_no_physics_delta": 1, "project_system_launch_manifest_completed_no_physics_delta": 1, "project_system_local_retrieval_doctor_no_physics_delta": 1, "project_system_manifest_population_no_physics_delta": 1, "project_system_manifest_schema_no_physics_delta": 1, "project_system_memory_ci_deduplication_no_physics_delta": 1, "project_system_memory_core_extraction_no_physics_delta": 1, "project_system_memory_make_refactor_no_physics_delta": 1, "project_system_memory_sync_extraction_no_physics_delta": 1, "project_system_memory_test_fixture_minimization_no_physics_delta": 1, "project_system_memory_validation_ownership_no_physics_delta": 1, "project_system_obsidian_test_fixture_minimization_no_physics_delta": 1, "project_system_planner_cutover_audit_no_physics_delta": 1, "project_system_policy_no_physics_delta": 4, "project_system_repository_snapshot_no_physics_delta": 1, "project_system_route_diagnostic_reporting_no_physics_delta": 1, "project_system_snapshot_cache_benchmark_no_physics_delta": 1, "project_system_starting_baseline_frozen_no_physics_delta": 1, "project_system_task_index_reporting_no_physics_delta": 1, "project_system_validation_audit_no_physics_delta": 1, "project_system_validation_cache_contract_no_physics_delta": 1, "project_system_validation_cache_implementation_no_physics_delta": 1, "project_system_validation_environment_separation_no_physics_delta": 1, "project_system_validation_no_physics_delta": 6, "project_system_validation_obligation_compiler_no_physics_delta": 1, "project_system_validation_planner_no_physics_delta": 1, "project_system_validation_receipt_schema_no_physics_delta": 1, "project_system_validation_reporting_no_physics_delta": 1, "proposal_only_law_target_formalized_pending_audit": 1, "publication_preparation_payload_complete_checkpoint_blocked_no_distance_delta": 1, "record_local_theorem_candidate_no_distance_delta": 1, "red_team_review_no_physics_delta": 3, "review_packet_created_no_outreach": 1, "review_packet_spec_no_outreach": 1, "review_question_selected_no_outreach": 1, "route_frozen": 2, "route_selector_no_distance_delta": 1, "routing_control_no_distance_delta": 1, "schema_defined": 1, "schema_no_physics_delta": 1, "selector_no_adoption": 1, "selector_no_promotion": 3, "selector_only_no_distance_delta": 55, "selector_routes_to_candidate_constructor_bridge_attempt": 1, "source_acquisition_only_no_distance_delta": 1, "source_extension_adopted": 9, "source_extension_evidence_accepted": 7, "support_only_conditional_theorem_no_distance_delta": 1, "support_only_formalization_no_distance_delta": 4, "support_only_schema_no_distance_delta": 1, "support_only_tooling_design_no_distance_delta": 1, "theoretical_decision_selected": 5, "tooling_update_no_physics_delta": 2, "toy_model_stressed_no_promotion": 1, "toy_model_zoo_integrated_no_promotion": 1, "toy_selector_no_promotion": 1, "traceability_only_no_distance_delta": 1, "typed_eqsrc_object_audited_source_pure_as_written_no_promotion": 1, "typed_eqsrc_object_defined_no_promotion": 1, "typed_eqsrc_problem_statement_no_promotion": 1, "typed_eqsrc_stressed_no_promotion": 1, "unchanged": 12, "v16_completed_ordinary_continuation_selected_no_distance_delta": 1, "v17_completed_ordinary_continuation_selected": 1, "v17_final_validation_no_promotion": 1, "v17_integration_no_promotion": 1, "v17_p0_t03_active_state_preflight_passed_no_physics_delta": 1, "v18_p0_t03_active_state_preflight_passed_no_physics_delta": 1, "v18_p0_t04_recommendation_coverage_seed_completed_no_physics_delta": 1, "v18_p1_t01_active_state_bifurcation_policy_defined_no_physics_delta": 1, "v18_p1_t02_active_state_bifurcation_renderer_completed_no_physics_delta": 1, "v18_p1_t03_active_state_sidecar_validator_completed_no_physics_delta": 1, "v18_p1_t04_active_state_bifurcation_red_team_repair_required_no_physics_delta": 1, "v18_p1_t04_repair_active_state_supersession_guard_completed_no_physics_delta": 1, "validator_fixture_catalog_no_distance_delta": 1, "validator_integration_no_distance_delta": 1, "validator_update_no_physics_delta": 1}` |

## Durable Scientific-Quality Diagnostics

This is the primary scientific-quality diagnostic surface. Every measured value has an explicit eligible-set denominator and immutable identities. Unknown populations remain `not_measured`; the eight indicators are not combined into a scientific-truth score.

| Metric | Family | Status | Numerator | Denominator | Value | Warning count |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `assumption_reduction_rate` | assumption_reduction | not_measured | None | None | None | 1 |
| `theorem_generality_rate` | theorem_generality | not_measured | None | None | None | 1 |
| `countermodel_novelty_rate` | countermodel_novelty | not_measured | None | None | None | 1 |
| `obstruction_unification_and_reuse_rate` | obstruction_unification_and_reuse | measured | 18 | 35 | 0.514286 | 0 |
| `independent_review_survival_rate` | independent_review_survival | not_measured | None | None | None | 1 |
| `benchmark_breadth_rate` | benchmark_breadth | not_measured | None | None | None | 1 |
| `retraction_repair_visibility_rate` | retraction_repair_visibility | measured | 5 | 5 | 1.0 | 0 |
| `ledger_durability_rate` | ledger_durability | measured | 8 | 8 | 1.0 | 0 |

### Durable-Quality Calibration Warnings

| Warning | Metric | Observed | Threshold | Hard Gate | Physics Authority |
| --- | --- | --- | --- | --- | --- |
| `assumption_reduction_rate:unknown_denominator` | `assumption_reduction_rate` | `` | `` | `False` | `False` |
| `theorem_generality_rate:unknown_denominator` | `theorem_generality_rate` | `` | `` | `False` | `False` |
| `countermodel_novelty_rate:unknown_denominator` | `countermodel_novelty_rate` | `` | `` | `False` | `False` |
| `independent_review_survival_rate:unknown_denominator` | `independent_review_survival_rate` | `` | `` | `False` | `False` |
| `benchmark_breadth_rate:unknown_denominator` | `benchmark_breadth_rate` | `` | `` | `False` | `False` |

## Payload-Density Metrics

Raw volume is operational context only and is not the primary scientific-quality surface.

| Metric | Value |
| --- | --- |
| `physics_completions_read` | `536` |
| `total_payload_items` | `1244` |
| `tasks_since_last_distance_to_gr_delta` | `138` |
| `tasks_since_last_burden_discharged` | `0` |
| `new_payload_items_per_physics_task` | `2.32` |
| `new_payload_items_per_cycle` | `19.5` |
| `selector_cycles_without_new_payload` | `0` |

## Route-Orbit Risk Metrics

| Metric | Value |
| --- | --- |
| `same_burden_repetition_count` | `2` |
| `freeze_reviews_triggered_by_repetition` | `280` |
| `bridge_attempts_since_last_gate` | `23` |
| `obstructions_created` | `34` |
| `obstructions_created_missing_id` | `0` |
| `obstructions_reused` | `26` |
| `candidate_construct_audit_stress_selector_cycles` | `16` |
| `gate_ready_cycles_without_gate_verdict` | `361` |
| `support_only_tooling_reports` | `2` |
| `physics_promotion_authorized_true_count` | `27` |
| `physics_promotion_authorized_false_count` | `332` |

## Candidate Lineage Metrics

These lifecycle metrics are keyed by immutable candidate IDs and preserve explicit historical absences. They are project-control diagnostics only and do not adopt, reject, or promote a candidate.

| Metric | Value |
| --- | --- |
| `candidate_to_audit_conversion` | `{"denominator_candidate_ids": ["EQSRC-CYCLE-BOUNDARY-V1", "EQSRC-GRADED-ORBIT-ROOT-V1", "EQSRC-IDISC-V1", "EQSRC-IDISC-V2", "EQSRC-IDISC-V3", "EQSRC-ORIENTATION-TORSOR-V1", "EQSRC-ROOTED-PARTITION-V1"], "numerator_candidate_ids": ["EQSRC-CYCLE-BOUNDARY-V1", "EQSRC-GRADED-ORBIT-ROOT-V1", "EQSRC-IDISC-V1", "EQSRC-IDISC-V2", "EQSRC-IDISC-V3", "EQSRC-ORIENTATION-TORSOR-V1", "EQSRC-ROOTED-PARTITION-V1"], "value": 1.0}` |
| `audit_to_stress_survival` | `{"denominator_candidate_ids": ["EQSRC-CYCLE-BOUNDARY-V1", "EQSRC-GRADED-ORBIT-ROOT-V1", "EQSRC-IDISC-V1", "EQSRC-IDISC-V2", "EQSRC-IDISC-V3", "EQSRC-ORIENTATION-TORSOR-V1", "EQSRC-ROOTED-PARTITION-V1"], "numerator_candidate_ids": ["EQSRC-CYCLE-BOUNDARY-V1", "EQSRC-IDISC-V3", "EQSRC-ORIENTATION-TORSOR-V1", "EQSRC-ROOTED-PARTITION-V1"], "value": 0.5714}` |
| `stress_survival_rate` | `{"denominator_candidate_ids": ["EQSRC-CYCLE-BOUNDARY-V1", "EQSRC-IDISC-V3", "EQSRC-ORIENTATION-TORSOR-V1", "EQSRC-ROOTED-PARTITION-V1"], "numerator_candidate_ids": [], "value": 0.0}` |

## Physics-Payload Ratio Diagnostics

These metrics are AI-system diagnostics only. They do not rank physics truth, authorize proof, promote a benchmark, create a Gate Chair verdict, or complete a derivation.

| Metric | Value |
| --- | --- |
| `project_system_task_run_length` | `1` |
| `physics_bearing_task_run_length` | `0` |
| `new_mathematical_payload_count` | `1300` |
| `theorem_countermodel_candidate_count` | `594` |
| `candidate_construction_count` | `206` |
| `support_only_task_count_since_last_physics_payload` | `1` |
| `route_orbit_warning_status` | `{"advisory_only": true, "hard_gate": false, "physics_claim_authority": false, "status": "warning", "warning_ids": ["post_gate_cycle_repeat", "gate_ready_without_gate"]}` |
| `project_system_task_count` | `528` |
| `physics_bearing_task_count` | `449` |
| `support_only_task_count` | `550` |
| `physics_bearing_to_project_system_task_ratio` | `0.8504` |
| `new_mathematical_payload_to_support_only_task_ratio` | `2.3636` |
| `route_orbit_same_burden_repetition_count` | `2` |
| `ordinary_route_guard_status` | `{"current_run_requires_physics_route_or_exception": false, "hard_threshold": 3, "policy_id": "ordinary_route_guard_policy_v1", "policy_source_path": "research_control/tasks/RT-20260722-015/artifacts/ordinary_route_guard_policy_v1.md", "prospective_hard_gate_active": true, "system_work_counts_as_physics": false, "warning_at": 2}` |

## Dual-Budget Dashboard

This dashboard separates physics and project-system task credit, elapsed effort, compute, durable outputs, and acceptance accounting. It is support-only and system success never creates physics or Distance-to-GR credit.

| Metric | Value |
| --- | --- |
| `physics` | `{"acceptance_criteria": {"declared_count": 23, "measured_record_count": 15, "not_measured_record_count": 531, "status": "partially_measured"}, "compute": {"measured_record_count": 0, "not_measured_record_count": 546, "status": "not_measured", "values_by_unit": {}}, "declared_acceptance_criterion_count": 23, "declared_durable_output_count": 20, "durable_outputs": {"declared_count": 20, "measured_record_count": 15, "not_measured_record_count": 531, "status": "partially_measured"}, "elapsed_effort": {"measured_record_count": 531, "not_measured_record_count": 15, "status": "partially_measured", "value_seconds": 34702.0}, "task_count_credit": 537}` |
| `project_system` | `{"acceptance_criteria": {"declared_count": 52, "measured_record_count": 15, "not_measured_record_count": 524, "status": "partially_measured"}, "compute": {"measured_record_count": 0, "not_measured_record_count": 539, "status": "not_measured", "values_by_unit": {}}, "declared_acceptance_criterion_count": 52, "declared_durable_output_count": 47, "durable_outputs": {"declared_count": 47, "measured_record_count": 15, "not_measured_record_count": 524, "status": "partially_measured"}, "elapsed_effort": {"measured_record_count": 527, "not_measured_record_count": 12, "status": "partially_measured", "value_seconds": 158075.0}, "task_count_credit": 533}` |
| `integrity` | `{"missing_compute_zero_coercion_status": "pass", "mixed_acceptance_disjointness_status": "pass", "mixed_output_disjointness_status": "pass", "single_primary_credit_status": "pass", "system_science_authority_separation_status": "pass"}` |
| `category_counts` | `{"mixed": 6, "physics_bearing": 531, "support_only": 107, "system_bearing": 426}` |

## Physics-Progress Integration Metrics

The packet, artifact, and payload counts in this section are retained only as raw operational context. They do not measure scientific quality or create physics progress.

| Metric | Value |
| --- | --- |
| `status` | `pass` |
| `authority_boundary` | `operational_summary_only_not_physics_proof` |
| `not_physics_proof` | `True` |
| `physics_claim_promotion_authorized` | `False` |
| `reporting_role` | `raw_volume_operational_context_only` |
| `primary_scientific_quality_surface` | `False` |
| `distance_delta` | `{"changed_false_count": 567, "changed_true_count": 183, "effect_counts": {"conditional_theorem_candidate": 19, "decision_evidence_only": 1, "evaluation_framework_only": 1, "frozen_negative": 1, "literature_basis_only": 1, "missing_effect": 718, "no_distance_delta": 307, "obstruction_recorded": 14, "review_calibration_only": 1, "scoped_evidence_precondition": 3, "scoped_source_extension_object": 4}, "records_read": 1070}` |
| `separate_packet_counts` | `{"candidate_packet_count": 206, "freeze_packet_count": 312, "obstruction_packet_count": 49, "process_only_packet_count": 608, "theorem_packet_count": 152}` |
| `candidate_result_counts` | `{"constructed_candidate": 35, "constructed_target_pending_candidate_constructor": 1, "minimal_countermodel": 1, "precise_obstruction": 10}` |
| `payload_density_summary` | `{"classified_item_count": 1879, "mathematical_payload_item_count": 1132, "mathematical_payload_task_count": 461, "payload_class_counts": {"conditional_theorem": 32, "countermodel": 90, "dependency_map_update": 162, "documentation_only": 107, "finite_witness": 283, "new_definition": 69, "new_theorem_statement": 180, "obstruction": 170, "proof_attempt": 0, "proved_theorem": 1, "route_selector_only": 197, "source_extension_classification": 145, "validator_tooling_only": 443}, "payload_density": 0.602448, "process_only_item_count": 747, "process_only_task_count": 608, "task_count": 1069, "task_payload_density": 0.431244}` |

## AI Research-Agent Methodology Metrics

These diagnostics are support-only AI-system methodology metrics. They are separated from scientific progress metrics and do not authorize physics proof, source-law adoption, benchmark promotion, Gate Chair verdicts, or completed-derivation claims.

| Metric | Family | Status | Value | Interpretation |
| --- | --- | --- | --- | --- |
| `overclaim_catch_rate` | Claim-boundary control | `measured` | `0.9451` | Forbidden-conclusion summaries are counted as eligible overclaim-control surfaces; caught means no physics promotion was authorized. |
| `underclaim_warning_rate` | Claim-boundary control | `not_measured` | `None` | The current registries do not deterministically encode high-risk positive scoped-status omission events. |
| `obstruction_precision` | Obstruction quality | `measured` | `1.0` | This deterministic proxy counts obstruction records with IDs plus milestone, burden, or status context as locally scoped. |
| `route_orbit_rate` | Route dynamics | `measured` | `0.0037` | Repeated-burden streaks are process warnings only and do not change Distance-to-GR status. |
| `candidate_to_audit_conversion` | Candidate life cycle | `measured` | `1.0` | Exact immutable candidate IDs replace the former aggregate completion-stage proxy; an audit stage is counted only when bound to the same candidate identity hash. |
| `audit_to_stress_survival` | Candidate life cycle | `measured` | `0.5714` | Exact candidate-keyed lineage counts only observed stress stages; the explicit graded-orbit stress absence is not inferred as a pass or failure. |
| `stress_survival_rate` | Candidate life cycle | `measured` | `0.0` | The seeded stressed candidates all carry scoped obstruction dispositions; local freeze remains preserved and is not relabeled as survival adoption rejection or global no-go. |
| `human_gate_load` | Governance load | `measured` | `None` | Gate-load signals are governance workload diagnostics, not Gate Chair scientific verdicts. |
| `proof_to_process_ratio` | Payload balance | `measured` | `1.5154` | Payload balance compares mathematical payload items to process-only items; it is not proof authority. |

## AI Methodology Acceptance Warnings

| Warning | Metric | Status | Hard Gate | Physics Authority | Reason |
| --- | --- | --- | --- | --- | --- |
| `underclaim_warning_rate_not_measured` | `underclaim_warning_rate` | `not_measured` | `False` | `False` | Needs a future extraction rule for accepted-scoped evidence omitted from summaries. |

## Diagnostic Warnings

| Warning | Metric | Observed | Threshold | Hard Gate | Physics Authority |
| --- | --- | --- | --- | --- | --- |
| `post_gate_cycle_repeat` | `candidate_construct_audit_stress_selector_cycles` | `6` | `0` | `False` | `False` |
| `claimed_bridge_no_delta` | `tasks_since_last_distance_to_gr_delta` | `4` | `2` | `False` | `False` |
| `candidate_missing_result` | `candidate_constructor_result_missing_count` | `11` | `0` | `False` | `False` |
| `gate_ready_without_gate` | `gate_ready_cycles_without_gate_verdict` | `361` | `0` | `False` | `False` |

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
- Candidate-lineage metrics are keyed by immutable candidate IDs and preserve explicit historical absences; they remain support-only project-control evidence and do not adopt or reject a candidate.
- Durable scientific-quality diagnostics use explicit eligible sets and immutable identities, leave absent denominators not_measured, and never aggregate scientific truth into one score.
- Raw packet, artifact, task, and payload counts remain operational context only; they are not the primary scientific-quality surface.
- Physics-payload ratio diagnostics are AI-system diagnostics only; they do not rank physics truth.
- Dual-budget dashboard values are operational accounting; system success, missing-resource markers, and lane counts are not physics evidence or Distance-to-GR progress.
- Validator failure history is not a durable event log, so this report does not infer blocked violation counts from past terminal output.

## Conclusion

This report provides separated operational and scientific scoreboards for future evaluation. The metrics show workflow health separately from tracked science-result fields. They do not change the authority of any scientific artifact.

## References

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations implementation plan* [Local implementation plan].

The AEther-Flow Research Project. (2026, June 21). *Agent job registry* [Project-control registry].

The AEther-Flow Research Project. (2026, June 21). *Claim boundary registry* [Project-control registry].
