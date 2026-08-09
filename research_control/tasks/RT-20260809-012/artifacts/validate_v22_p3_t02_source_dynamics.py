#!/usr/bin/env python3
"""Deterministic focused validation for V22 P3-T02 source dynamics."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = ROOT / "research_control/tasks/RT-20260809-012/artifacts"
SPEC = ART / "v22_p3_t02_source_dynamics_specification_v1.yaml"
COEFFICIENTS = ART / "v22_p3_t02_coefficient_provenance_v1.yaml"
LEDGER = ART / "v22_p3_t02_constraint_identity_ledger_v1.yaml"
UNITS = ART / "v22_p3_t02_units_debt_wellposedness_v1.yaml"
FIXTURES = ART / "fixtures/v22_p3_t02_source_dynamics_cases.yaml"
CHILD_MATH = ART / "child_phys_math_p3_t02_source_dynamics.yaml"
CHILD_PHIL = ART / "child_phys_phil_p3_t02_source_purity.yaml"
CONFLICT = ART / "parent_conflict_review_p3_t02_source_dynamics.yaml"
FUSION = ART / "parent_fusion_notes_p3_t02_source_dynamics.md"
MANUSCRIPT = ART / "v22_p3_t02_source_dynamics_without_hidden_geometry_v1.tex"
MODEL = ART / "v22_p3_t02_transport_model.py"
OUTPUT = ART / "v22_p3_t02_source_dynamics_validation.json"

EXPECTED_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-0981.yaml":
        "711311d64b59c28d7c2c79166d567489b9254d0feacd2e2b39790179229e2031",
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_local_state_specification_v1.yaml":
        "961636349d8bfe73f5f13d33953f92d2a07d7d567f836e8f217dfeef7bb30813",
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_local_multifield_source_state_v1.tex":
        "ce1b852b7ea178dd5d42a204e9cc63fb2c11e9987e8ac0fc733267eb04dbb6db",
    "research_control/tasks/RT-20260809-010/artifacts/v22_p3_t01_p7_refinement_interface_v1.yaml":
        "cfda8abd1905d04d3ec806c4178ad7c2f620f82a736ed6316e0768c17c143baa",
    "research_control/tasks/RT-20260809-009/artifacts/v22_p2_t04_primary_local_multifield_candidate_v1.yaml":
        "5d8a332c6aa05d85260a14af777a1d3f43015ba48980493acfa4c584bec75132",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
}


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML map")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_model() -> Any:
    spec = importlib.util.spec_from_file_location("v22_p3_t02_transport_model", MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load transport model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    spec = load_yaml(SPEC)
    coefficients = load_yaml(COEFFICIENTS)
    ledger = load_yaml(LEDGER)
    units = load_yaml(UNITS)
    fixtures = load_yaml(FIXTURES)
    child_math = load_yaml(CHILD_MATH)
    child_phil = load_yaml(CHILD_PHIL)
    conflict = load_yaml(CONFLICT)
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    fusion = FUSION.read_text(encoding="utf-8")
    model = load_model()
    model_result = model.evaluate_fixture()
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    for rel, expected in EXPECTED_HASHES.items():
        actual = sha256(ROOT / rel)
        check(f"source_hash::{rel}", actual == expected, actual)

    check("candidate_id", spec.get("dynamics_candidate_id") == "CAND-V22-B1-SIX-TRANSPORT-DYNAMICS-V1")
    check("coefficient_id", spec.get("coefficient_datum_id") == "COEF-V22-B1-SIX-TRANSPORT-V1")
    check("sealed_family_identity", spec.get("candidate_identity_sha256") == "32110632f8832091d69ca52e96dfdf99c26087bfc75575b77a466631eca9d051")
    check("proposal_only_status", "proposal-only" in spec.get("claim_status", ""))
    check("deterministic_law", spec["law_choice"].get("class") == "deterministic_first_order_local_transport")
    check("no_action_choice", spec["law_choice"].get("action_used") is False)
    check("no_stochastic_kernel", spec["law_choice"].get("stochastic_kernel_used") is False)
    check("six_components", spec["formal_objects"]["state"].get("components") == 6)
    check("tau_is_source_label", spec["formal_objects"]["evolution_label"].get("physical_clock") is False)
    check("six_vector_symbols", len(spec["formal_objects"]["coefficient_fields"]["symbols"]) == 6)
    check("not_frame", spec["formal_objects"]["coefficient_fields"].get("frame_claimed") is False)
    check("not_cone", spec["formal_objects"]["coefficient_fields"].get("cone_claimed") is False)

    equation = spec["equations"]
    check("equation_map_typed", equation.get("equation_map") == "E_D: C2(U,R6) -> C1(U,R6)")
    check("equation_exact", equation.get("component_rule") == "E_A[D,q]=X_A(q^A)=0")
    check("no_sum", equation.get("index_convention") == "no sum over A")
    check("first_order", equation.get("derivative_order") == 1)
    check("zero_scalar_parameters", equation.get("scalar_free_coefficients") == [])

    naturality = spec["passive_source_naturality"]
    check("passive_equation_identity", "X'_A(q'^A)" in naturality.get("equation_identity", ""))
    check("no_target_diffeomorphism", naturality.get("target_diffeomorphism_claimed") is False)
    check("no_active_gauge", naturality.get("active_physical_gauge_claimed") is False)

    initial = spec["initial_data"]
    boundary = spec["boundary_data"]
    theorem = spec["local_solution_theorem"]
    check("tau_level_surface", "tau^(-1)" in initial.get("source_surface", ""))
    check("transverse_data", initial.get("transversality") == "d tau(X_A)=1")
    check("no_normal_derivative", initial.get("normal_derivative_prescribed") is False)
    check("no_metric_normal", initial.get("metric_normal_used") is False)
    check("inflow_rule", "d b(X_A)<0" in boundary.get("inflow_rule", ""))
    check("outflow_rejected", "do not prescribe" in boundary.get("outflow_rule", ""))
    check("flow_solution_formula", theorem.get("solution_formula") == "q^A(Phi_A^t(y))=f_A(y)")
    check("local_existence", "local existence" in theorem.get("conclusions", []))
    check("local_uniqueness", "local uniqueness" in theorem.get("conclusions", []))
    check("continuous_dependence", any("continuous dependence" in item for item in theorem.get("conclusions", [])))
    check("solution_gluing", any("gluing" in item for item in theorem.get("conclusions", [])))
    check("not_physical_hyperbolicity", theorem.get("physical_hyperbolicity_claimed") is False)
    check("not_physical_causality", theorem.get("physical_causality_claimed") is False)

    witness = spec["explicit_witness"]
    vectors = witness["vector_components_by_channel"]
    check("six_witness_vectors", len(vectors) == 6)
    check("all_tau_components_one", all(row[0] == 1 for row in vectors.values()))
    check("six_distinct_witness_vectors", len({tuple(row) for row in vectors.values()}) == 6)
    check("zero_declared_residuals", witness.get("equation_residuals") == [0, 0, 0, 0, 0, 0])
    check("nonzero_background_parameters", len(witness["background"]["assumptions"]) == 3)
    check("rank_two_witness", witness.get("response_rank") == 2)
    check("no_one_amplitude_collapse", witness.get("one_amplitude_collapse") is False)
    check("fixture_not_target_fit", witness.get("target_fitted") is False)
    check("fixture_not_universal", witness.get("fixture_values_promoted_to_law_constants") is False)

    model_vectors = model_result["tau_normalizations"]
    check("model_pass", model_result.get("status") == "PASS")
    check("model_vector_count", model_result.get("vector_count") == 6)
    check("model_tau_normalization", model_vectors == ["1", "1", "1", "1", "1", "1"])
    check("model_vectors_distinct", model_result.get("pairwise_distinct_vectors") is True)
    check("model_background_residuals", model_result.get("background_residuals") == ["0"] * 6)
    check("model_regular_wedge", model_result.get("regular_wedge_nonzero") is True)
    check("model_chart_naturality", model_result["chart_naturality"].get("equal") is True)
    check("model_token1_on_equation", model_result["token_channel_1"].get("Xi_qi") == "0")
    check("model_token2_on_equation", model_result["token_channel_2"].get("Xi_qi") == "0")
    check("model_zero_target_inputs", model_result.get("target_metric_input_count") == 0)
    check("model_zero_measure_inputs", model_result.get("measure_input_count") == 0)
    check("model_zero_connection_inputs", model_result.get("connection_input_count") == 0)
    check("model_zero_target_fit", model_result.get("target_fit_count") == 0)

    linear = spec["linearization"]
    check("linearization_exact", linear.get("rule") == "delta E_A=X_A(delta q^A)")
    check("principal_symbol_exact", "delta_A^B" in linear.get("principal_symbol", ""))
    check("principal_polynomial_exact", linear.get("principal_polynomial") == "P_D(xi)=product_A xi(X_A)")
    check("principal_degree_six", linear.get("polynomial_degree") == 6)
    check("six_distinct_factors", linear.get("witness_distinct_linear_factors") == 6)
    check("no_reduced_quadratic_cone", linear.get("reduced_quadratic_cone_constructed") is False)
    check("no_physical_scale", linear.get("physical_scale_constructed") is False)
    check("no_effective_metric", linear.get("effective_metric_constructed") is False)
    for index, sample in enumerate(model_result["principal_samples"], start=1):
        factors = sample["factors"]
        product = model.Fraction(1)
        for factor in factors:
            product *= model.Fraction(factor)
        check(f"principal_sample_product::{index}", str(product) == sample["polynomial"], sample["polynomial"])

    observables = spec["operational_observables"]
    check("two_ratios", len(observables["ratios"]) == 2)
    check("two_tokens", len(observables["tokens"]) == 2)
    check("ratio_update_derived", "X_6(rho_i)" in observables["conditional_update"]["ratio_rule"])
    check("token_update_derived", "p_i*(1-p_i)" in observables["conditional_update"]["token_rule"])
    check("no_continuum_limit_claim", observables.get("continuum_limit_claimed") is False)
    check("no_realistic_matter_claim", observables.get("realistic_matter_claimed") is False)
    check("no_detector_claim", observables.get("detector_semantics_claimed") is False)
    check("no_universal_coupling_claim", observables.get("universal_coupling_claimed") is False)

    constraints = spec["constraints"]
    check("three_coefficient_constraints", len(constraints["coefficient"]) == 3)
    check("two_operational_constraints", len(constraints["operational"]) == 2)
    check("no_algebraic_constraints", constraints.get("algebraic_field_constraints") == [])
    check("no_gauge_constraints", constraints.get("gauge_constraints") == [])
    check("no_secondary_constraints", constraints.get("secondary_constraints") == [])
    check("no_global_regular_preservation", constraints.get("global_regular_locus_preservation_proved") is False)

    identities = spec["conditional_identities"]
    check("two_conditional_identities", len(identities) == 2)
    check("composition_not_independent", identities[0].get("independent_physical_law") is False)
    check("composition_not_integrated", identities[0].get("integrated_conservation_law") is False)
    check("token_not_independent", identities[1].get("independent_physical_law") is False)
    check("token_not_matter", identities[1].get("realistic_matter_law") is False)

    bridge = spec["bridge_attempt_status"]
    check("bridge_status_decisive", bridge.get("status") == "source_principal_map_constructed_reduction_missing")
    check("bridge_candidate_map_named", "sigma_D" in bridge.get("candidate_map", ""))
    check("bridge_missing_object_named", "physical cone" in bridge.get("missing_object", ""))
    check("bridge_no_geff", bridge.get("effective_metric_constructed") is False)
    check("bridge_no_global_nogo", bridge.get("global_no_go_claimed") is False)

    refuters = spec["refuter_cases"]
    check("eleven_refuter_cases", len(refuters) == 11)
    check("refuter_ids_unique", len({row["case_id"] for row in refuters}) == 11)
    check("all_refuters_have_expected", all(row.get("expected") for row in refuters))

    purity = spec["source_purity"]
    check("zero_target_imports", purity.get("imported_target_structures") == [])
    check("prohibited_count_zero", purity.get("prohibited_count") == 0)
    check("fifteen_absent_structures", len(purity.get("absent_structures", [])) == 15)
    check("five_exposed_debts", len(purity.get("exposed_source_debt", [])) == 5)

    result = spec["candidate_constructor_result"]
    check("constructed_candidate_result", result.get("result_type") == "constructed_candidate")
    check("constructed_path_named", result.get("constructed_candidate_path") == str(MANUSCRIPT.relative_to(ROOT)))
    check("formal_objects_named", len(result.get("formal_objects", [])) == 4)
    check("maps_named", len(result.get("maps", [])) == 4)
    check("proof_obligations_named", len(result.get("proof_obligations", [])) == 3)
    check("next_role_concrete", result.get("next_required_role") == "candidate-constructor")
    check("no_fog_true", result.get("no_fog_check") is True)
    check("no_fog_explanation_decisive", "constructs" in result.get("no_fog_explanation", "").lower())
    check("claim_boundary_preserved", result.get("claim_boundary_preserved") is True)

    coefficient_rows = coefficients["records"]
    check("seven_coefficient_records", len(coefficient_rows) == 7)
    check("coefficient_ids_unique", len({row["coefficient_id"] for row in coefficient_rows}) == 7)
    check("all_coefficients_proposal_debt", all(row.get("primitive_debt") is True for row in coefficient_rows))
    check("all_coefficients_underived", all(row.get("derived_from_current_ontology") is False for row in coefficient_rows))
    check("all_coefficients_target_free", all(row.get("target_source") == "" for row in coefficient_rows))
    check("zero_free_scalars", coefficients.get("free_scalar_coefficient_count") == 0)
    check("selected_before_target", coefficients.get("selected_before_target_comparison") is True)
    check("zero_coefficient_adoption", coefficients["audit"].get("ontology_adoption_count") == 0)

    constraint_rows = ledger["constraint_records"]
    identity_rows = ledger["identity_records"]
    check("six_constraint_records", len(constraint_rows) == 6)
    check("four_identity_records", len(identity_rows) == 4)
    check("five_failure_records", len(ledger["failure_ledger"]) == 5)
    check("no_physical_identity", all(row.get("independent_postulate") is False for row in identity_rows))
    check("no_global_nogo_failure", ledger["authority_limits"].get("global_no_go_claimed") is False)

    formal_units = units["formal_units"]
    wellposed = units["well_posedness"]
    debts = units["debt_ledger"]
    freeze = units["freeze_evaluation"]
    check("source_time_not_physical", formal_units["source_flow_label"].get("physical_time") is False)
    check("six_channel_units", len(formal_units["state_channels"]["symbols"]) == 6)
    check("no_physical_length", formal_units.get("physical_length_assigned") is False)
    check("no_physical_mass", formal_units.get("physical_mass_assigned") is False)
    check("wellposed_scope_local", "local fixed-coefficient" in wellposed.get("theorem_scope", ""))
    check("no_energy_estimate", wellposed.get("energy_estimate_used") is False)
    check("no_metric_norm", wellposed.get("metric_norm_used") is False)
    check("no_global_existence", wellposed.get("global_existence_claimed") is False)
    check("eight_debt_records", len(debts) == 8)
    check("all_debts_not_adopted", all(row.get("adoption") is False for row in debts))
    check("freeze_evaluated", freeze.get("freeze_evaluation_required") is True)
    check("not_frozen", freeze.get("freeze_decision") == "not_frozen")
    check("next_route_candidate_constructor", freeze.get("next_allowed_route") == "candidate_constructor")

    fixture_rows = fixtures.get("cases", [])
    allowed_expected = {
        "accept", "reject", "accept_zero_residual", "accept_rank_two",
        "reject_rank_collapse", "accept_degree_six", "accept_six_distinct_factors",
        "reject_overread", "accept_invariant_directional_derivative",
        "reject_overdetermined", "accept_conditional_only", "accept_local",
        "accept_no_distance_delta",
    }
    check("fixture_count_34", len(fixture_rows) == 34)
    check("fixture_ids_unique", len({row["case_id"] for row in fixture_rows}) == 34)
    check("fixture_expected_vocabulary", all(row.get("expected") in allowed_expected for row in fixture_rows))
    for row in fixture_rows:
        check(f"fixture::{row['case_id']}", bool(row.get("category") and row.get("mutation") and row.get("expected")), row.get("expected", ""))

    check("math_child_completed", child_math.get("status") == "completed")
    check("math_child_seven_findings", len(child_math.get("findings", [])) == 7)
    check("math_bridge_missing_geff", child_math["bridge_attempt_status"].get("effective_metric_constructed") is False)
    check("phil_child_completed", child_phil.get("status") == "completed")
    check("phil_child_seven_findings", len(child_phil.get("findings", [])) == 7)
    check("phil_purity_pass", child_phil.get("source_purity_verdict") == "PASS_PROPOSAL_ONLY_WITH_EXPLICIT_PRIMITIVE_DEBT")
    check("conflict_resolved", conflict.get("status") == "resolved")
    check("five_conflicts_resolved", conflict.get("resolved_conflict_count") == 5)
    check("no_unresolved_conflicts", conflict.get("unresolved_conflicts") == [])
    check("fusion_decisive_result", "proposal-only constructed candidate" in fusion)
    check("fusion_missing_bridge", "missing bridge" in fusion.lower())

    required_tex_fragments = [
        "E_A[\\D_U,q]:=X_A(q^A)=0",
        "q^A\\bigl(\\Phi_A^t(y)\\bigr)=f_A(y)",
        "\\prod_{A=1}^{6}\\xi(X_A)",
        "\\dd\\bar\\rho_1\\wedge\\dd\\bar\\rho_2",
        "Source ontology primitives",
        "The Candidate Constructor result is \\emph{constructed candidate}",
    ]
    for fragment in required_tex_fragments:
        check(f"manuscript_fragment::{fragment[:24]}", fragment in manuscript)
    check("manuscript_blocks_geff", "does not construct" in manuscript and "effective metric" in manuscript)
    check("manuscript_no_adoption", "no ontology or source law is adopted" in manuscript)

    authority = spec["authority_limits"]
    false_authority_fields = [
        "ontology_modified", "source_law_adopted", "coefficient_datum_adopted",
        "target_geometry_imported", "target_fit_used", "physical_hyperbolicity_claimed",
        "conservation_law_adopted", "realistic_matter_law_adopted",
        "effective_metric_constructed", "distance_to_gr_changed",
        "physics_promotion_authorized", "gate_chair_verdict_authorized",
        "completed_derivation_authorized",
    ]
    for field in false_authority_fields:
        check(f"authority_false::{field}", authority.get(field) is False)

    failures = [item for item in checks if item["status"] == "FAIL"]
    report = {
        "schema_id": "v22_p3_t02_source_dynamics_validation_v1",
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260809-012",
        "plan_task_id": "P3-T02",
        "dynamics_candidate_id": spec.get("dynamics_candidate_id"),
        "coefficient_datum_id": spec.get("coefficient_datum_id"),
        "focused_check_count": len(checks),
        "focused_check_failure_count": len(failures),
        "fixture_case_count": len(fixture_rows),
        "fixture_failure_count": sum(1 for item in failures if item["name"].startswith("fixture::")),
        "model_status": model_result.get("status"),
        "background_residuals": model_result.get("background_residuals"),
        "regular_wedge_nonzero": model_result.get("regular_wedge_nonzero"),
        "principal_polynomial_degree": linear.get("polynomial_degree"),
        "principal_factor_count": linear.get("witness_distinct_linear_factors"),
        "source_extension_adopted": False,
        "effective_metric_constructed": False,
        "distance_to_gr_changed": False,
        "checks": checks,
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write:
        OUTPUT.write_text(encoded, encoding="utf-8")
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != encoded:
            report["status"] = "FAIL"
            report["generated_output_fresh"] = False
            encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json or not (args.write or args.check):
        print(encoded, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
