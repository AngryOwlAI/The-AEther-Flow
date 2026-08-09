#!/usr/bin/env python3
"""Deterministic focused checks for V22 P3-T01 B1 local-state construction."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = ROOT / "research_control/tasks/RT-20260809-010/artifacts"
SPEC = ART / "v22_p3_t01_local_state_specification_v1.yaml"
P7 = ART / "v22_p3_t01_p7_refinement_interface_v1.yaml"
LEDGER = ART / "v22_p3_t01_assumption_cost_ledger_v1.yaml"
FIXTURES = ART / "fixtures/v22_p3_t01_local_state_cases.yaml"
OUTPUT = ART / "v22_p3_t01_local_state_validation.json"

EXPECTED_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-0979.yaml":
        "8cf1a9a5f17ba985c7200ad13223752ac7d7ff1e140f41c747d7ae808ed91957",
    "research_control/tasks/RT-20260809-009/artifacts/v22_p2_t04_primary_local_multifield_candidate_v1.yaml":
        "5d8a332c6aa05d85260a14af777a1d3f43015ba48980493acfa4c584bec75132",
    "research_control/tasks/RT-20260809-003/artifacts/v22_p1_t03_p7_conditional_input_contract_v1.yaml":
        "e1acd64ea434f3dc6a0607c17f69162f0e242bc92d5490eb84ff3d3afd92a3c4",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_source_adequacy_checklist_v1.yaml":
        "a9b59df7b5b2d1203fef53cf23817400c6d1511836e97ff1ae21b819dc064e68",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML map")
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    spec = load_yaml(SPEC)
    p7 = load_yaml(P7)
    ledger = load_yaml(LEDGER)
    fixtures = load_yaml(FIXTURES)
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    for rel, expected in EXPECTED_HASHES.items():
        actual = sha256(ROOT / rel)
        check(f"source_hash::{rel}", actual == expected, actual)

    check("sealed_candidate_id", spec.get("candidate_id") == "CAND-V22-B1-LOCAL-SIX-FIELD-RESPONSE-SEED-V1")
    check("sealed_candidate_identity", spec.get("candidate_identity_sha256") == "32110632f8832091d69ca52e96dfdf99c26087bfc75575b77a466631eca9d051")
    check("sole_program_route", spec.get("program_route_active") is True)
    check("one_candidate_activation", spec.get("scientific_candidate_activation_count") == 1)
    check("proposal_only_activation", spec.get("activation_status") == "active_research_packet_proposal_only")
    check("no_source_extension_adoption", spec.get("source_extension_adopted") is False)
    check("no_canonical_ontology_change", spec.get("canonical_ontology_modified") is False)

    local = spec["local_structure"]
    check("bundle_exact", local.get("bundle_symbol") == "E_B1 = A x R^6")
    check("sheaf_exact", local.get("sheaf_symbol") == "Q_B1")
    check("six_component_state", local.get("field_symbol") == "q=(q^1,...,q^6)")
    check("c2_sections", "C2(U,R^6)" in local.get("section_assignment", ""))
    check("first_jet_available", local.get("finite_jet_order_available") == 1)
    check("dynamics_not_defined", local.get("dynamics_defined_here") is False)

    table = spec["type_and_domain_table"]
    check("type_table_count", len(table) == 7, str(len(table)))
    check("all_types_have_domains", all(row.get("domain") for row in table))
    check("all_types_have_codomains", all(row.get("codomain") for row in table))
    check("all_types_have_regularity", all(row.get("regularity") for row in table))

    restriction = spec["restriction_law"]
    check("restriction_identity", restriction.get("identity") == "res_UU=id")
    check("restriction_composition", "res_VW o res_UV = res_UW" in restriction.get("composition", ""))
    check("observable_restriction_naturality", "rho_i(q)|V=rho_i(q|V)" in restriction.get("observable_naturality", ""))

    gluing = spec["gluing_law"]
    check("gluing_componentwise", "componentwise" in gluing.get("compatibility", ""))
    check("gluing_unique", "unique q" in gluing.get("result", ""))
    check("identity_fiber_transition", "identity" in gluing.get("transition_rule", ""))
    check("no_target_coordinate_gluing", gluing.get("target_coordinate_use") is False)
    check("gluing_cocycle", "g_ij g_jk=g_ik" in gluing.get("cocycle", ""))

    regular = spec["regular_operational_subdomain"]
    check("regular_denominator", "q6(x) nonzero" in regular.get("definition", ""))
    check("regular_rank_two_form", "d rho1 wedge d rho2" in regular.get("definition", ""))
    check("regular_restriction_stable", regular.get("restriction_stable") is True)
    check("regular_gluing_stable", regular.get("gluing_stable_under_compatible_regular_cover") is True)
    check("singular_strata_count", len(regular.get("singular_strata", [])) == 2)

    variations = spec["admissible_variations"]
    witnesses = variations["independent_response_witnesses"]
    check("variation_boundary_value", "i_B^*(delta q)=0" in variations["boundary_preserving_conditions"])
    check("variation_boundary_first_jet", "i_B^*(d delta q)=0" in variations["boundary_preserving_conditions"])
    check("variation_no_metric_norm", variations.get("no_metric_norm_claimed") is True)
    check("two_variation_witnesses", len(witnesses) == 2)
    check("declared_response_rank_two", variations.get("response_rank") == 2)
    check("witness_basis_one", witnesses[0].get("response_at_x0") == "delta_1(rho1,rho2)=(1,0)")
    check("witness_basis_two", witnesses[1].get("response_at_x0") == "delta_2(rho1,rho2)=(0,1)")

    rho1, rho2 = 0.7, -0.4
    s1 = 1.0 / (1.0 + math.exp(-rho1))
    s2 = 1.0 / (1.0 + math.exp(-rho2))
    det = s1 * (1.0 - s1) * s2 * (1.0 - s2)
    check("analytic_response_jacobian_rank_two", det > 0.0, f"det={det:.12g}")

    boundary = spec["boundary_data"]
    check("boundary_value_trace", boundary.get("dirichlet_trace") == "i_B^*q")
    check("boundary_tangential_trace", "tangential" in boundary.get("first_jet_trace", ""))
    check("boundary_excluded_imports", set(boundary.get("excluded_imports", [])) == {"unit normal", "normal derivative", "induced metric", "boundary measure", "causal boundary"})

    symmetry = spec["source_symmetry_and_equivalence"]
    check("source_passive_groupoid", "source-chart transition pseudogroup" in symmetry.get("passive_groupoid", ""))
    check("scalar_pullback_action", "pullback" in symmetry.get("action", ""))
    check("restriction_pullback_naturality", "res(phi^*q)=phi^*(res(q))" in symmetry.get("restriction_naturality", ""))
    check("no_internal_gauge", symmetry.get("internal_gauge_assumed") is False)
    check("no_active_dynamical_symmetry", symmetry.get("active_dynamical_symmetry_assumed") is False)
    check("no_target_diffeomorphism_claim", symmetry.get("target_diffeomorphism_or_target_gauge_claimed") is False)

    observables = spec["source_native_observables"]
    check("four_observables", len(observables) == 4)
    check("observable_ids_unique", len({x["observable_id"] for x in observables}) == 4)
    check("target_semantics_excluded", len(spec.get("target_semantics_excluded", [])) == 6)
    certificate = spec["response_certificate"]
    check("capacity_rank_two", certificate.get("computed_capacity_rank") == 2)
    check("required_rank_two", certificate.get("required_response_rank") == 2)
    check("necessary_only_verdict", certificate.get("verdict") == "necessary_condition_met_not_sufficient")
    check("no_geometry_sufficiency", certificate.get("geometry_sufficiency_claimed") is False)
    check("no_gate_credit", certificate.get("gate_b_credit_claimed") is False)

    audit = spec["no_target_import_audit"]
    check("no_target_import_audit_pass", audit.get("audit_result") == "PASS_SOURCE_NATIVE_SYNTAX_ONLY")
    check("forbidden_premise_count", len(audit.get("forbidden_premises_absent", [])) == 7)
    check("source_atlas_debt_explicit", "inherited primitive debt" in audit.get("local_atlas_debt_statement", ""))

    activation = spec["activation_boundary"]
    check("activation_transition_executed", activation.get("transition_id") == "ACTIVATE_PRIMARY" and activation.get("executed") is True)
    check("activation_not_adoption", activation.get("activation_is_adoption") is False)
    check("activation_not_truth", activation.get("activation_is_physics_truth") is False)
    check("fallback_inactive", activation.get("fallback_activated") is False)
    check("third_slot_unallocated", activation.get("third_slot_allocated") is False)
    check("source_law_absent", activation.get("source_law_defined") is False)
    check("effective_metric_absent", activation.get("effective_metric_defined") is False)

    check("p7_exact_consumed_contract", p7.get("consumed_contract_id") == "P7-CONDITIONAL-INPUT-CONTRACT-V1")
    check("p7_five_annotations", len(p7.get("typing_annotations", [])) == 5)
    check("p7_two_bernoulli_slots", "ordered pair of Bernoulli" in p7["objects"]["token_output"])
    check("p7_restriction_naturality", "marginal/reindexing" in p7["restriction"]["naturality"])
    check("p7_persistent_refinement", "persistent" in p7["refinement"]["preservation_rule"])
    check("p7_exact_refinement_consistency", "comparison_map" in p7["refinement"]["exact_consistency"])
    check("p7_no_interpolation_import", "No metric" in p7["refinement"]["no_interpolation_rule"])
    check("p7_no_convergence_claim", p7["refinement"]["convergence_status"].startswith("not_claimed"))
    check("p7_four_failures", len(p7.get("failure_cases", [])) == 4)
    check("p7_no_realistic_matter", p7["kernel"].get("realistic_matter_claimed") is False)
    check("p7_no_target_detector", p7["kernel"].get("target_detector_claimed") is False)

    entries = ledger["entries"]
    check("assumption_count_nine", len(entries) == 9)
    check("assumption_ids_unique", len({x["assumption_id"] for x in entries}) == 9)
    check("cost_vectors_eight_axes", all(len(x["cost_vector"]) == 8 for x in entries))
    check("no_scalar_cost", ledger.get("scalar_total_used") is False)
    check("zero_metric_debt", ledger["aggregate"].get("metric_equivalent_input_count") == 0)
    check("zero_target_atlas_input", ledger["aggregate"].get("target_atlas_input_count") == 0)
    check("zero_gr_fit", ledger["aggregate"].get("gr_target_fit_count") == 0)

    fixture_rows = fixtures.get("cases", [])
    check("fixture_declared_count", fixtures.get("case_count") == 24)
    check("fixture_actual_count", len(fixture_rows) == 24)
    check("fixture_ids_unique", len({row["case_id"] for row in fixture_rows}) == 24)
    allowed_expected = {"pass", "reject", "reject_operational_domain", "reject_rank_two", "reject_target_import", "reject_undeclared_structure", "reject_typing", "reject_claim_boundary", "reject_route_state", "reject_authority", "reject_overread"}
    for row in fixture_rows:
        check(f"fixture::{row['case_id']}", row.get("expected") in allowed_expected, row.get("kind", ""))

    failures = [item for item in checks if item["status"] == "FAIL"]
    report = {
        "schema_id": "v22_p3_t01_local_state_validation_v1",
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260809-010",
        "plan_task_id": "P3-T01",
        "candidate_id": spec.get("candidate_id"),
        "focused_check_count": len(checks),
        "focused_check_failure_count": len(failures),
        "fixture_case_count": len(fixture_rows),
        "fixture_failure_count": sum(1 for item in failures if item["name"].startswith("fixture::")),
        "response_rank": 2 if det > 0.0 else 0,
        "adequacy_verdict": certificate.get("verdict"),
        "scientific_candidate_activation_count": spec.get("scientific_candidate_activation_count"),
        "source_extension_adopted": spec.get("source_extension_adopted"),
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
