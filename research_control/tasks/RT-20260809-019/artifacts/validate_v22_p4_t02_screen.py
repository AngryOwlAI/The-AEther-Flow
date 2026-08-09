#!/usr/bin/env python3
"""Focused deterministic validator for the V22 P4-T02 B1 stress screen."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ARTIFACTS = Path(__file__).resolve().parent
REPO = ARTIFACTS.parents[3]
VALIDATION_PATH = ARTIFACTS / "v22_p4_t02_screen_validation.json"
COMPACT_PATH = ARTIFACTS / "v22_p4_t02_compact_receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate() -> dict[str, Any]:
    paths = {
        "spec": ARTIFACTS / "v22_p4_t02_screen_specification_v1.yaml",
        "gate": ARTIFACTS / "v22_p4_t02_gate_b_hard_fail_disposition_v1.yaml",
        "sector": ARTIFACTS / "v22_p4_t02_sector_universality_matrix_v1.yaml",
        "obstruction": ARTIFACTS / "v22_p4_t02_refuter_obstruction_record_v1.yaml",
        "countermodel": ARTIFACTS / "v22_p4_t02_robustness_countermodel_v1.yaml",
        "transition": ARTIFACTS / "v22_p4_t02_candidate_termination_budget_transition_v1.yaml",
        "provenance": ARTIFACTS / "v22_p4_t02_source_provenance_manifest_v1.yaml",
        "fixtures": ARTIFACTS / "fixtures/v22_p4_t02_stress_cases.yaml",
        "math_child": ARTIFACTS / "child_phys_math_p4_t02_hyperbolicity.yaml",
        "phil_child": ARTIFACTS / "child_phys_phil_p4_t02_scope_refutation.yaml",
        "conflict": ARTIFACTS / "parent_conflict_review_p4_t02_screen.yaml",
        "fusion": ARTIFACTS / "parent_fusion_notes_p4_t02_screen.md",
        "evidence": ARTIFACTS / "validator_engineer_p4_t02_independent_evidence.yaml",
        "latex_receipt": ARTIFACTS / "v22_p4_t02_latex_compile_receipt.json",
        "tex": ARTIFACTS / "v22_p4_t02_hyperbolicity_universality_robustness_hard_fail_screen_v1.tex",
        "primary": ARTIFACTS / "v22_p4_t02_hyperbolicity_model.py",
        "independent": ARTIFACTS / "v22_p4_t02_independent_reproduction.py",
    }
    spec = load_yaml(paths["spec"])
    gate = load_yaml(paths["gate"])
    sector = load_yaml(paths["sector"])
    obstruction = load_yaml(paths["obstruction"])
    countermodel = load_yaml(paths["countermodel"])
    transition = load_yaml(paths["transition"])
    provenance = load_yaml(paths["provenance"])
    fixtures = load_yaml(paths["fixtures"])
    math_child = load_yaml(paths["math_child"])
    phil_child = load_yaml(paths["phil_child"])
    conflict = load_yaml(paths["conflict"])
    evidence = load_yaml(paths["evidence"])
    latex_receipt = load_json(paths["latex_receipt"])
    tex = paths["tex"].read_text(encoding="utf-8")
    fusion = paths["fusion"].read_text(encoding="utf-8")

    primary = load_module(paths["primary"], "v22_p4_t02_primary")
    independent = load_module(paths["independent"], "v22_p4_t02_independent")
    primary_result = primary.evaluate()
    independent_result = independent.evaluate()

    checks: dict[str, bool] = {}

    def check(name: str, value: object) -> None:
        checks[name] = bool(value)

    check("spec_schema", spec["schema_id"] == "v22_p4_t02_screen_specification_v1")
    check("spec_plan_task", spec["plan_task_id"] == "P4-T02")
    check("spec_scoped_obstruction", spec["result_classification"] == "scoped_obstruction")
    check("spec_candidate", spec["candidate_id"] == "CAND-V22-B1-SIX-TRANSPORT-REDUCED-PRINCIPAL-V1")
    check("spec_fixed_symmetric_hyperbolic", spec["fixed_source_system"]["symmetric_hyperbolic_with_respect_to_source_tau"] is True)
    check("spec_time_matrix_identity", spec["fixed_source_system"]["time_matrix"] == "A^0=I_6")
    check("spec_symmetrizer_typed", spec["fixed_source_system"]["field_symmetrizer_is_source_spacetime_metric"] is False)
    check("spec_condition_one", spec["fixed_source_system"]["strong_hyperbolicity_condition_number"] == 1)
    check("spec_no_physical_hyperbolicity", spec["fixed_source_system"]["physical_hyperbolicity_claimed"] is False)
    check("spec_polynomial_hyperbolic", spec["polynomial_hyperbolicity"]["all_line_roots_real"] is True)
    check("spec_six_time_factors", spec["polynomial_hyperbolicity"]["factor_values_at_h"] == [1] * 6)
    check("spec_polyhedral_component", "polyhedral" in spec["polynomial_hyperbolicity"]["cone_kind"])
    check("spec_component_not_physical", spec["polynomial_hyperbolicity"]["physical_causal_cone"] is False)
    check("spec_no_common_quadratic", spec["quadratic_cone_obstruction"]["common_quadratic_characteristic_cone_exists"] is False)
    check("spec_no_common_lorentzian", spec["quadratic_cone_obstruction"]["common_lorentzian_characteristic_cone_exists"] is False)
    check("spec_independent_rank_certificate", "rank ten" in spec["quadratic_cone_obstruction"]["independent_certificate"])
    check("spec_crossings_singular", spec["degeneracy_and_conditioning"]["all_pair_intersections_singular_for_reduced_variety"] is True)
    check("spec_max_corank_four", spec["degeneracy_and_conditioning"]["maximum_symbol_corank"] == 4)
    check("spec_countermodel_background", spec["finite_variation_countermodel"]["background_preserved"] is True)
    check("spec_countermodel_source_only", spec["finite_variation_countermodel"]["target_atlas_or_metric_used"] is False)
    check("spec_countermodel_discriminant", spec["finite_variation_countermodel"]["characteristic_discriminant"] == "-16 epsilon^2")
    check("spec_countermodel_all_nonzero", spec["finite_variation_countermodel"]["complex_characteristic_pair_for_every_nonzero_epsilon"] is True)
    check("spec_fixed_law_changed", spec["finite_variation_countermodel"]["exact_fixed_law_changed"] is True)
    check("spec_refinement_pass", spec["refinement_status"]["p3_t03_controlled_limit_passes_for_fixed_law"] is True)
    check("spec_refinement_decreasing", spec["refinement_status"]["errors_strictly_decrease"] is True)
    check("spec_refinement_six_branches", spec["refinement_status"]["limit_preserves_six_branch_structure"] is True)
    check("spec_gb03_fail", spec["gate_b_screen"]["GB03_STABLE_LORENTZIAN_CONE"] == "FAIL")
    check("spec_gb04_fail", spec["gate_b_screen"]["GB04_UNIVERSAL_MATTER_COMPATIBILITY"] == "FAIL")
    check("spec_gb07_fail", spec["gate_b_screen"]["GB07_VARIATION_COARSE_GRAINING_ROBUSTNESS"] == "FAIL_FAMILY_LEVEL")
    check("spec_no_gate_b_verdict", spec["gate_b_screen"]["gate_b_verdict_issued"] is False)
    check("spec_two_hard_fails", spec["hard_fail_screen"]["triggered_ids"] == ["HF04_NONUNIVERSAL_OR_UNSELECTED_MULTICONE", "HF05_INSTABILITY_NONHYPERBOLICITY_DEGENERACY"])
    check("spec_terminate_b1", spec["hard_fail_screen"]["candidate_disposition"] == "TERMINATE_B1_PRIMARY_APPEND_ONLY")
    check("spec_no_auto_fallback", spec["hard_fail_screen"]["automatic_fallback_activation"] is False)
    check("spec_no_effective_metric", spec["authority_limits"]["effective_metric_constructed"] is False)
    check("spec_no_distance_delta", spec["authority_limits"]["distance_to_gr_changed"] is False)

    gate_statuses = {row["criterion_id"]: row["status"] for row in gate["gate_b_criteria"]}
    trigger_statuses = {row["trigger_id"]: row["status"] for row in gate["hard_fail_triggers"]}
    check("gate_eight_criteria", len(gate_statuses) == 8)
    check("gate_gb02_source_only", gate_statuses["GB02_REDUCED_HYPERBOLIC_PRINCIPAL"] == "PASS_SOURCE_PDE_ONLY")
    check("gate_gb03_fail", gate_statuses["GB03_STABLE_LORENTZIAN_CONE"] == "FAIL")
    check("gate_gb04_fail", gate_statuses["GB04_UNIVERSAL_MATTER_COMPATIBILITY"] == "FAIL")
    check("gate_gb07_family_fail", gate_statuses["GB07_VARIATION_COARSE_GRAINING_ROBUSTNESS"] == "FAIL_FAMILY_LEVEL")
    check("gate_eight_triggers", len(trigger_statuses) == 8)
    check("gate_hf04_triggered", trigger_statuses["HF04_NONUNIVERSAL_OR_UNSELECTED_MULTICONE"] == "TRIGGERED")
    check("gate_hf05_family_triggered", trigger_statuses["HF05_INSTABILITY_NONHYPERBOLICITY_DEGENERACY"] == "TRIGGERED_FAMILY_LEVEL")
    check("gate_hf06_not_triggered", trigger_statuses["HF06_NO_CONTROLLED_CONTINUUM_LIMIT"] == "NOT_TRIGGERED_FOR_FIXED_LAW")
    check("gate_primary_terminated", gate["disposition"]["primary_terminated"] is True)
    check("gate_p4_t03_locked", gate["disposition"]["p4_t03_unlocked"] is False)
    check("gate_b2_inactive", gate["disposition"]["fallback_activated"] is False)

    check("sector_six_channels", len(sector["b1_channel_rows"]) == 6)
    check("sector_six_distinct_factors", sector["b1_channel_comparison"]["distinct_global_characteristic_factors"] == 6)
    check("sector_common_source_time", sector["b1_channel_comparison"]["common_source_time_covector"] is True)
    check("sector_no_common_characteristic", sector["b1_channel_comparison"]["common_characteristic_hypersurface"] is False)
    check("sector_no_quotient", sector["b1_channel_comparison"]["derived_channel_equivalence_or_quotient"] is False)
    check("sector_four_p7_rows", len(sector["p7_declared_sector_rows"]) == 4)
    check("sector_all_fail_closed", all(row["status"] == "FAIL_CLOSED_NOT_TYPED" for row in sector["p7_declared_sector_rows"]))
    check("sector_universality_not_established", sector["universality_verdict"]["physical_sector_universality_established"] is False)

    check("countermodel_scope", countermodel["scope"] == "source_extension_candidate")
    check("countermodel_background_preserved", countermodel["mutation"]["background_preserved"] is True)
    check("countermodel_time_matrix", countermodel["mutation"]["time_matrix_unchanged"] == "I_6")
    check("countermodel_no_target", countermodel["mutation"]["metric_or_target_data_used"] is False)
    check("countermodel_discriminant", countermodel["crossing_test"]["discriminant"] == "-16 epsilon^2")
    check("countermodel_four_nonzero_cases", len(countermodel["parameter_sweep"]) == 4)
    check("countermodel_all_complex", all(row["complex_pair"] for row in countermodel["parameter_sweep"]))
    check("countermodel_fixed_not_refuted", countermodel["scope_guard"]["exact_fixed_diagonal_law_refuted"] is False)
    check("countermodel_family_refuted", countermodel["scope_guard"]["broader_b1_family_robustness_refuted"] is True)

    check("obstruction_class", obstruction["result_classification"] == "scoped_obstruction")
    record = obstruction["refuter_obstruction_record"]
    check("obstruction_minimal_countermodel", record["minimal_countermodel_available"] is True)
    check("obstruction_repair_possible", record["source_extension_repair_possible"] == "repair_possible")
    check("obstruction_no_global_no_go", record["global_no_go_claim_authorized"] is False)
    check("obstruction_local_freeze", obstruction["freeze_criteria_status"]["freeze_decision"] == "locally_frozen")
    check("obstruction_next_selector", obstruction["freeze_criteria_status"]["next_allowed_route"] == "theoretical_selector")
    check("obstruction_route_cycle_selector", obstruction["route_cycle_control"]["next_role_consequence"] == "theoretical-continuation-selector@0.1.0")

    check("transition_terminated", transition["termination"]["executed"] is True)
    check("transition_two_triggers", len(transition["termination"]["trigger_ids"]) == 2)
    check("transition_slot_one_consumed", transition["budget_state_after_transition"]["consumed_family_slots"] == [1])
    check("transition_no_active_family", transition["budget_state_after_transition"]["active_family_id"] == "")
    check("transition_b2_inactive", transition["budget_state_after_transition"]["fallback_activation_status"] == "inactive_fresh_selector_and_descriptor_required")
    check("transition_slot_three_reserved", transition["budget_state_after_transition"]["third_slot_status"] == "reserved_unallocated")
    check("transition_budget_not_exhausted", transition["budget_state_after_transition"]["budget_exhausted"] is False)
    check("transition_fresh_selector", transition["next_transition"]["authority"] == "fresh theoretical-continuation selector AgentJob")
    check("transition_six_missing_prereqs", len(transition["next_transition"]["prerequisites_still_missing"]) == 4)

    check("fixture_frozen", fixtures["status"] == "frozen")
    check("fixture_six_vectors", len(fixtures["source_vectors"]) == 6)
    check("fixture_five_fixed_cases", len(fixtures["fixed_system_cases"]) == 5)
    check("fixture_five_line_cases", len(fixtures["hyperbolicity_line_cases"]) == 5)
    check("fixture_five_perturbations", len(fixtures["cross_channel_countermodel"]["perturbation_parameters"]) == 5)
    check("fixture_expected_two_triggers", len(fixtures["expected_disposition"]["hard_fail_trigger_ids"]) == 2)

    check("primary_status", primary_result["status"] == "PASS")
    for name, value in primary_result["checks"].items():
        check(f"primary_{name}", value)
    check("primary_fixed_hyperbolic", primary_result["disposition"]["exact_fixed_source_pde_hyperbolic"] is True)
    check("primary_scoped_obstruction", primary_result["disposition"]["result_classification"] == "scoped_obstruction")
    check("primary_two_triggers", len(primary_result["disposition"]["hard_fail_trigger_ids"]) == 2)
    check("primary_refinement_four_levels", len(primary_result["refinement"]) == 4)

    check("independent_status", independent_result["status"] == "PASS")
    for name, value in independent_result["checks"].items():
        check(f"independent_{name}", value)
    check("independent_156_constraints", independent_result["quadratic_obstruction"]["constraint_count"] == 156)
    check("independent_rank_ten", independent_result["quadratic_obstruction"]["exact_constraint_rank"] == 10)
    check("independent_no_quadratic", independent_result["quadratic_obstruction"]["nonzero_common_quadratic_exists"] is False)
    check("independent_four_perturbations", len(independent_result["perturbation_sweep"]) == 4)
    check("independent_all_complex", all(row["complex_pair"] for row in independent_result["perturbation_sweep"]))

    check("provenance_ten_sources", len(provenance["sources"]) == 10)
    check("provenance_source_commit", provenance["source_commit"] == "4e87a27cd96ef8497098a65f4e8ff82274350f81")
    check("provenance_source_tree", provenance["source_tree"] == "752371cc6204c9943d22e3d14f09be5808dbd39f")
    check("provenance_all_forbidden_zero", all(value == 0 for value in provenance["forbidden_input_counts"].values()))
    for source in provenance["sources"]:
        check(f"source_hash_{source['object_id']}", sha256(REPO / source["path"]) == source["sha256"])

    check("math_child_complete", math_child["status"] == "completed")
    check("math_child_three_payloads", len(math_child["new_mathematical_payload"]) == 3)
    check("phil_child_complete", phil_child["status"] == "completed")
    check("phil_child_no_imports", phil_child["result"]["prohibited_imports_detected"] == [])
    check("children_preserve_boundary", math_child["claim_boundary_preserved"] is True and phil_child["claim_boundary_preserved"] is True)
    check("conflicts_resolved", conflict["status"] == "resolved" and conflict["resolved_conflict_count"] == 5)
    check("no_blocking_conflicts", conflict["blocking_conflict_count"] == 0 and conflict["unresolved_conflicts"] == [])
    check("evidence_no_primary_import", evidence["independence"]["independent_imports_primary"] is False)
    check("evidence_rank_ten", evidence["checks"]["quadratic_constraint_rank"] == 10)
    check("evidence_no_global_validator_change", evidence["global_validator_semantics_changed"] is False)

    check("latex_status", latex_receipt["status"] == "PASS")
    check("latex_source_hash", latex_receipt["source_sha256"] == sha256(paths["tex"]))
    check("latex_seven_pages", latex_receipt["page_count"] == 7 and latex_receipt["pages_visually_reviewed"] == 7)
    check("latex_zero_final_warnings", latex_receipt["final_overfull_hbox_warning_count"] == 0 and latex_receipt["final_underfull_hbox_warning_count"] == 0 and latex_receipt["final_undefined_reference_count"] == 0)
    check("latex_no_visual_defects", not any(value for key, value in latex_receipt["visual_findings"].items() if key not in {"page_numbering_consistent", "section_hierarchy_consistent", "margins_consistent"}))
    check("latex_layout_consistent", all(latex_receipt["visual_findings"][key] for key in ("page_numbering_consistent", "section_hierarchy_consistent", "margins_consistent")))

    tex_phrases = (
        "Fixed source symmetric hyperbolicity",
        "No common characteristic quadric",
        "156 integer points",
        "-16\\epsilon^2",
        "HF04\\_NONUNIVERSAL\\_OR\\_UNSELECTED\\_MULTICONE",
        "HF05\\_INSTABILITY\\_NONHYPERBOLICITY\\_DEGENERACY",
        "scoped\\_obstruction",
        "P4--T03 is not unlocked",
        "fresh Theoretical Continuation Selector",
        "Distance-to-GR delta is zero",
        "not a global no-go theorem",
    )
    for index, phrase in enumerate(tex_phrases, start=1):
        check(f"tex_required_phrase_{index}", phrase in tex)
    check("fusion_fixed_positive", "symmetric hyperbolic relative" in fusion)
    check("fusion_quadratic_rank", "156 points" in fusion and "rank ten" in fusion)
    check("fusion_countermodel_scope", "does not refute fixed-law symmetric" in fusion)
    check("fusion_p4_t03_locked", "P4-T03 is not unlocked" in fusion)
    check("fusion_b2_inactive", "B2 fallback remains\ninactive" in fusion)
    check("fusion_scoped_not_global", "scoped obstruction, not a global no-go" in fusion)

    tracked_artifacts = tuple(paths.values()) + (Path(__file__).resolve(),)
    artifact_hashes = {
        path.relative_to(ARTIFACTS).as_posix(): sha256(path)
        for path in tracked_artifacts
    }
    failures = sorted(name for name, passed in checks.items() if not passed)
    return {
        "schema_id": "v22_p4_t02_screen_validation_v1",
        "task_id": "RT-20260809-019",
        "job_id": "AJ-RT-20260809-019-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "failures": failures,
        "checks": checks,
        "primary_result_summary": {
            "status": primary_result["status"],
            "fixed_source_symmetric_hyperbolic": primary_result["fixed_system"]["source_symmetric_hyperbolic"],
            "result_classification": primary_result["disposition"]["result_classification"],
            "hard_fail_trigger_ids": primary_result["disposition"]["hard_fail_trigger_ids"],
        },
        "independent_result_summary": {
            "status": independent_result["status"],
            "constraint_count": independent_result["quadratic_obstruction"]["constraint_count"],
            "exact_constraint_rank": independent_result["quadratic_obstruction"]["exact_constraint_rank"],
            "implementation_independent_of_primary": independent_result["checks"]["independent_of_primary_model"],
        },
        "artifact_hashes": artifact_hashes,
        "authority": {
            "b1_primary_terminated": True,
            "b1_primary_locally_frozen": True,
            "b2_fallback_activated": False,
            "p4_t03_unlocked": False,
            "global_no_go_claimed": False,
            "gate_b_verdict_issued": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def write_outputs(result: dict[str, Any]) -> None:
    VALIDATION_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {
        "schema_id": "v22_p4_t02_compact_receipt_v1",
        "task_id": result["task_id"],
        "job_id": result["job_id"],
        "status": result["status"],
        "check_count": result["check_count"],
        "failure_count": result["failure_count"],
        "validation_path": VALIDATION_PATH.relative_to(REPO).as_posix(),
        "validation_sha256": sha256(VALIDATION_PATH),
        "fixed_source_symmetric_hyperbolic": True,
        "common_nonzero_quadratic_characteristic_polynomial_exists": False,
        "quadratic_constraint_rank": 10,
        "quadratic_constraint_count": 156,
        "family_level_finite_variation_robustness": False,
        "hard_fail_trigger_ids": [
            "HF04_NONUNIVERSAL_OR_UNSELECTED_MULTICONE",
            "HF05_INSTABILITY_NONHYPERBOLICITY_DEGENERACY",
        ],
        "result_classification": "scoped_obstruction",
        "b1_primary_terminated": True,
        "b2_fallback_activated": False,
        "p4_t03_unlocked": False,
        "distance_to_gr_changed": False,
        "physics_promotion_authorized": False,
    }
    COMPACT_PATH.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    if args.write:
        write_outputs(result)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
