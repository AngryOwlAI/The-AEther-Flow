#!/usr/bin/env python3
"""Focused deterministic validator for V22 P4-T01."""

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
VALIDATION_PATH = ARTIFACTS / "v22_p4_t01_principal_symbol_validation.json"
COMPACT_PATH = ARTIFACTS / "v22_p4_t01_compact_receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate() -> dict[str, Any]:
    spec_path = ARTIFACTS / "v22_p4_t01_principal_symbol_specification_v1.yaml"
    ledger_path = ARTIFACTS / "v22_p4_t01_factorization_branch_ledger_v1.yaml"
    provenance_path = ARTIFACTS / "v22_p4_t01_source_provenance_manifest_v1.yaml"
    fixture_path = ARTIFACTS / "fixtures/v22_p4_t01_principal_symbol_cases.yaml"
    tex_path = ARTIFACTS / "v22_p4_t01_gauge_reduced_principal_symbol_v1.tex"
    math_child_path = ARTIFACTS / "child_phys_math_p4_t01_principal_symbol.yaml"
    phil_child_path = ARTIFACTS / "child_phys_phil_p4_t01_scope_refutation.yaml"
    conflict_path = ARTIFACTS / "parent_conflict_review_p4_t01_principal_symbol.yaml"
    fusion_path = ARTIFACTS / "parent_fusion_notes_p4_t01_principal_symbol.md"
    evidence_path = ARTIFACTS / "validator_engineer_p4_t01_independent_evidence.yaml"
    primary_path = ARTIFACTS / "v22_p4_t01_principal_symbol_model.py"
    independent_path = ARTIFACTS / "v22_p4_t01_independent_reproduction.py"

    specification = load_yaml(spec_path)
    ledger = load_yaml(ledger_path)
    provenance = load_yaml(provenance_path)
    fixtures = load_yaml(fixture_path)
    math_child = load_yaml(math_child_path)
    phil_child = load_yaml(phil_child_path)
    conflict = load_yaml(conflict_path)
    evidence = load_yaml(evidence_path)
    tex = tex_path.read_text(encoding="utf-8")
    fusion = fusion_path.read_text(encoding="utf-8")

    primary = load_module(primary_path, "v22_p4_t01_primary")
    independent = load_module(independent_path, "v22_p4_t01_independent")
    primary_result = primary.evaluate()
    independent_result = independent.evaluate()

    checks: dict[str, bool] = {}

    def check(name: str, value: object) -> None:
        checks[name] = bool(value)

    check("spec_schema", specification["schema_id"] == "v22_p4_t01_principal_symbol_specification_v1")
    check("spec_candidate", specification["candidate_id"] == "CAND-V22-B1-SIX-TRANSPORT-REDUCED-PRINCIPAL-V1")
    check("spec_plan_task", specification["plan_task_id"] == "P4-T01")
    check("fixed_law_six_vectors", len(specification["fixed_law"]["source_vectors"]) == 6)
    check("coefficient_datum_fixed", specification["fixed_law"]["coefficient_datum_held_fixed"] is True)
    check("source_law_not_adopted", specification["fixed_law"]["source_law_adopted"] is False)
    check("zero_algebraic_constraints", specification["reduction"]["algebraic_field_constraints"] == [])
    check("zero_differential_constraints", specification["reduction"]["differential_constraints"] == [])
    check("zero_internal_gauge", specification["reduction"]["internal_field_gauge_generators"] == [])
    check("zero_algebraic_redundancy", specification["reduction"]["algebraic_equation_redundancies"] == [])
    check("open_conditions_not_constraints", specification["reduction"]["open_conditions_are_constraints"] is False)
    check("physical_interpretation_incomplete", specification["reduction"]["physical_interpretation_complete"] is False)
    check("determinant_lawful", specification["reduction"]["determinant_lawful_after_reduction"] is True)
    check("symbol_diagonal", specification["principal_symbol"]["abstract"] == "sigma_L(x,k)=diag(k(X_1),...,k(X_6))")
    check("polynomial_degree_six", specification["principal_symbol"]["homogeneous_degree"] == 6)
    check("polynomial_nontrivial", specification["principal_symbol"]["nontrivial_witness"] == "P_D(d tau)=1")
    check("density_weight_zero", specification["principal_symbol"]["source_coordinate_density_weight"] == 0)
    check("determinant_line_stated", "det(equation fiber)" in specification["principal_symbol"]["determinant_line"])
    check("six_global_factors", specification["principal_symbol"]["global_factor_count"] == 6)
    check("all_global_multiplicities_one", specification["principal_symbol"]["global_factor_multiplicities"] == [1] * 6)
    check("global_square_free", specification["principal_symbol"]["global_square_free"] is True)
    check("fifteen_pairs", specification["characteristic_structure"]["pairwise_intersection_count"] == 15)
    check("twenty_triples", specification["characteristic_structure"]["triple_subset_count"] == 20)
    check("fourfold_branches_exact", specification["characteristic_structure"]["unique_nonzero_fourfold_branches"] == [2, 3, 4, 6])
    check("fourfold_witness_exact", specification["characteristic_structure"]["fourfold_witness_factors"] == [1, 0, 0, 0, -2, 0])
    check("maximum_corank_four", specification["characteristic_structure"]["maximum_nonzero_corank"] == 4)
    check("no_nonzero_fivefold", specification["characteristic_structure"]["nonzero_fivefold_intersection_count"] == 0)
    check("no_nonzero_sixfold", specification["characteristic_structure"]["nonzero_sixfold_intersection_count"] == 0)
    check("directional_crossing_classified", specification["characteristic_structure"]["fixed_spatial_crossing_example"]["classification"] == "direction-dependent crossing of distinct global branches")
    check("chart_polynomial_invariant", specification["covariance_and_weight"]["polynomial_chart_invariant"] is True)
    check("gauge_invariance_vacuous_explicit", "vacuous" in specification["covariance_and_weight"]["internal_gauge_choice_invariance"])
    check("physical_units_unresolved", "unresolved" in specification["covariance_and_weight"]["physical_units_status"])
    check("no_hyperbolicity_verdict", specification["authority_limits"]["hyperbolicity_verdict_issued"] is False)
    check("no_physical_cone", specification["authority_limits"]["physical_causal_cone_constructed"] is False)
    check("no_effective_metric", specification["authority_limits"]["effective_metric_constructed"] is False)
    check("no_distance_delta", specification["authority_limits"]["distance_to_gr_changed"] is False)

    check("ledger_six_factors", len(ledger["global_factorization"]["factors"]) == 6)
    check("ledger_square_free", ledger["global_factorization"]["square_free"] is True)
    check("ledger_no_repeated_global", ledger["global_factorization"]["repeated_global_factor_count"] == 0)
    check("ledger_pair_ranks", ledger["intersection_strata"]["pairwise"]["rank_two_count"] == 15)
    check("ledger_triple_ranks", ledger["intersection_strata"]["triple"]["rank_three_count"] == 20)
    check("ledger_distinct_triple_points", ledger["intersection_strata"]["triple"]["distinct_projective_point_count"] == 17)
    check("ledger_fourfold_rank", ledger["intersection_strata"]["fourfold"]["row_rank"] == 3)
    check("ledger_fourfold_corank", ledger["intersection_strata"]["fourfold"]["symbol_corank"] == 4)
    check("ledger_no_fivefold", ledger["intersection_strata"]["fivefold"]["nonzero_intersection_count"] == 0)
    check("ledger_crossing_not_global_repeat", "not a repeated global factor" in ledger["branch_crossings"]["example"]["classification"])

    check("primary_status", primary_result["status"] == "PASS")
    for name, value in primary_result["checks"].items():
        check(f"primary_{name}", value)
    check("primary_factor_expression", primary_result["principal_polynomial"]["factor_expression"] == specification["principal_symbol"]["chart_expression"])
    check("primary_term_count", primary_result["principal_polynomial"]["expanded_term_count"] == 51)
    check("primary_max_corank", primary_result["branch_report"]["maximum_nonzero_corank"] == 4)
    check("primary_metric_not_inserted", primary_result["authority"]["metric_inserted"] is False)

    check("independent_status", independent_result["status"] == "PASS")
    check("independent_imports_no_primary", independent_result["implementation_independent_of_primary"] is True)
    for name, value in independent_result["checks"].items():
        check(f"independent_{name}", value)
    check("independent_five_cases", len(independent_result["cases"]) == 5)
    check("independent_fourfold_kernel", next(case for case in independent_result["cases"] if case["covector"] == [1, 0, -1, -1])["kernel_dimension"] == 4)
    check("independent_no_external_claim", independent_result["external_independent_review_claimed"] is False)

    check("fixture_case_count", len(fixtures["cases"]) == 32)
    check("fixture_ids_unique", len({case["case_id"] for case in fixtures["cases"]}) == 32)
    check("fixture_frozen", fixtures["status"] == "frozen_before_target_access")
    check("provenance_input_count", provenance["input_count"] == 6 and len(provenance["inputs"]) == 6)
    check("provenance_target_geometry_zero", provenance["target_geometry_input_count"] == 0)
    check("provenance_metric_factor_zero", provenance["metric_factor_input_count"] == 0)
    check("checkpoint_prerequisite_commit", provenance["checkpoint_prerequisite"]["commit"] == "2c0cefed9d55ab43fce3ce1532a56ce26d3f1f25")
    for source in provenance["inputs"]:
        check(f"source_hash_{source['object_id']}", sha256(REPO / source["path"]) == source["sha256"])

    check("math_child_complete", math_child["status"] == "completed")
    check("math_child_payload", len(math_child["new_mathematical_payload"]) == 3)
    check("phil_child_complete", phil_child["status"] == "completed")
    check("phil_child_no_imports", phil_child["result"]["prohibited_imports_detected"] == [])
    check("children_preserve_boundary", math_child["claim_boundary_preserved"] is True and phil_child["claim_boundary_preserved"] is True)
    check("parent_conflicts_resolved", conflict["status"] == "resolved" and conflict["resolved_conflict_count"] == 5)
    check("parent_no_blocking_conflicts", conflict["blocking_conflict_count"] == 0 and conflict["unresolved_conflicts"] == [])
    check("evidence_independent", evidence["independence"]["independent_imports_primary"] is False)
    check("evidence_no_global_validator_change", evidence["global_validator_semantics_changed"] is False)

    tex_phrases = (
        "C_{\\rm alg}=C_{\\rm diff}=G_{\\rm int}=R_{\\rm alg}=\\{0\\}",
        "\\sigmaL(x,k)=\\operatorname{diag}",
        "(\\omega+\\kappa_1)(\\omega+\\kappa_2)(\\omega+\\kappa_3)",
        "\\det(\\Eeq)\\otimes\\det(\\Vred)^*",
        "k_\\star=(1,0,-1,-1)",
        "maximum symbol corank at a nonzero covector is four",
        "source-principal structure, not a physical",
        "No strong/symmetric hyperbolicity",
        "constructed source-principal candidate pending P4--T02 stress",
    )
    for index, phrase in enumerate(tex_phrases, start=1):
        check(f"tex_required_phrase_{index}", phrase in tex)
    check("fusion_exact_polynomial", "(w+x)(w+y)(w+z)(w+x+y)(w+y+2z)(w+2x+z)" in fusion)
    check("fusion_p4_t02_boundary", "P4-T02" in fusion and "No branch is" in fusion)
    check("fusion_no_metric_claim", "no Lorentzian signature" in fusion)

    tracked_artifacts = (
        spec_path,
        ledger_path,
        provenance_path,
        fixture_path,
        tex_path,
        math_child_path,
        phil_child_path,
        conflict_path,
        fusion_path,
        evidence_path,
        primary_path,
        independent_path,
        Path(__file__).resolve(),
    )
    artifact_hashes = {path.relative_to(ARTIFACTS).as_posix(): sha256(path) for path in tracked_artifacts}
    failures = sorted(name for name, passed in checks.items() if not passed)
    return {
        "schema_id": "v22_p4_t01_principal_symbol_validation_v1",
        "task_id": "RT-20260809-018",
        "job_id": "AJ-RT-20260809-018-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "failures": failures,
        "checks": checks,
        "primary_result_summary": {
            "status": primary_result["status"],
            "expanded_term_count": primary_result["principal_polynomial"]["expanded_term_count"],
            "maximum_nonzero_corank": primary_result["branch_report"]["maximum_nonzero_corank"],
        },
        "independent_result_summary": {
            "status": independent_result["status"],
            "case_count": len(independent_result["cases"]),
            "implementation_independent_of_primary": independent_result["implementation_independent_of_primary"],
        },
        "artifact_hashes": artifact_hashes,
        "authority": {
            "source_principal_candidate_constructed": True,
            "proof_authority": False,
            "external_review_completed": False,
            "physical_cone_constructed": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def write_outputs(result: dict[str, Any]) -> None:
    VALIDATION_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {
        "schema_id": "v22_p4_t01_compact_receipt_v1",
        "task_id": result["task_id"],
        "job_id": result["job_id"],
        "status": result["status"],
        "check_count": result["check_count"],
        "failure_count": result["failure_count"],
        "validation_path": VALIDATION_PATH.relative_to(REPO).as_posix(),
        "validation_sha256": sha256(VALIDATION_PATH),
        "principal_polynomial_degree": 6,
        "global_factor_count": 6,
        "global_repeated_factor_count": 0,
        "maximum_nonzero_corank": 4,
        "independent_case_count": result["independent_result_summary"]["case_count"],
        "metric_factor_inserted": False,
        "physical_cone_constructed": False,
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
