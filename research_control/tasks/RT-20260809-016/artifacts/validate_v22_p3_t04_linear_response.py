#!/usr/bin/env python3
"""Deterministic validation for the V22 P3-T04 linear-response packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping: {path}")
    return value


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate() -> dict[str, Any]:
    primary_path = ARTIFACTS / "v22_p3_t04_linear_response_model.py"
    independent_path = ARTIFACTS / "v22_p3_t04_independent_linearization.py"
    spec_path = ARTIFACTS / "v22_p3_t04_background_linear_response_specification_v1.yaml"
    ledger_path = ARTIFACTS / "v22_p3_t04_countermodel_adequacy_ledger_v1.yaml"
    fixture_path = ARTIFACTS / "fixtures/v22_p3_t04_background_linear_response_cases.yaml"
    math_child_path = ARTIFACTS / "child_phys_math_p3_t04_linear_response.yaml"
    phil_child_path = ARTIFACTS / "child_phys_phil_p3_t04_smuggling_refutation.yaml"
    conflict_path = ARTIFACTS / "parent_conflict_review_p3_t04_linear_response.yaml"
    fusion_path = ARTIFACTS / "parent_fusion_notes_p3_t04_linear_response.md"
    tex_path = ARTIFACTS / "v22_p3_t04_background_linear_response_preprincipal_v1.tex"

    primary = load_module(primary_path, "p3t04_primary").evaluate()
    independent = load_module(independent_path, "p3t04_independent").evaluate()
    specification = load_yaml(spec_path)
    ledger = load_yaml(ledger_path)
    fixtures = load_yaml(fixture_path)
    math_child = load_yaml(math_child_path)
    phil_child = load_yaml(phil_child_path)
    conflict = load_yaml(conflict_path)
    fusion = fusion_path.read_text(encoding="utf-8")
    tex = tex_path.read_text(encoding="utf-8")

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    check("primary_status", primary["status"] == "PASS", str(primary["status"]))
    for key, value in primary["checks"].items():
        check(f"primary_{key}", value is True, str(value))
    check("independent_status", independent["status"] == "PASS", str(independent["status"]))
    check("independent_separate", independent["implementation_independent_of_primary"] is True, "no primary import")
    check("independent_error", independent["max_linearization_error"] < 1.0e-8, str(independent["max_linearization_error"]))
    check("independent_rank", independent["response_rank_check"]["rank_two"] is True, "rank two")
    check("independent_no_target", independent["target_geometry_inputs"] == 0, "zero target inputs")

    background = specification["background_classification"]
    check("background_nontrivial", background["selected_fixture"]["nontrivial"] is True, "nonconstant exact witness")
    check("background_residuals", background["selected_fixture"]["equation_residuals"] == [0] * 6, "six exact zeros")
    check("background_margin", background["selected_fixture"]["q6_margin"] == 3, "q6 margin 3")
    check("background_source_selected", background["selection_frozen_before_target_access"] is True, "frozen source rule")
    check("background_no_target", background["target_convenience_used"] is False, "no target convenience")
    check("background_no_vacuum", background["physical_vacuum_claimed"] is False, "no vacuum claim")
    check("background_no_minkowski", background["minkowski_background_claimed"] is False, "no Minkowski claim")

    linear = specification["tangent_and_linearized_equations"]
    check("linear_rule", linear["derivative"] == "DE_D|qbar[u]=(X_1u1,...,X_6u6)", linear["derivative"])
    check("linear_background_independent", linear["background_independent_for_fixed_D"] is True, "fixed D")
    check("linear_smooth", "C-infinity" in linear["differentiability"], linear["differentiability"])
    check("coefficient_variations_excluded", linear["coefficient_variations_included"] is False, "candidate identity sealed")

    reduction = specification["constraint_and_equivalence_reduction"]
    check("no_algebraic_constraints", reduction["algebraic_field_constraints"] == [], "none")
    check("no_secondary_constraints", reduction["secondary_field_constraints"] == [], "none")
    check("no_internal_gauge", reduction["internal_field_gauge_generators"] == [], "zero internal generators")
    check("no_physical_gauge", reduction["physical_gauge_generators"] == [], "no physical gauge supplied")
    check("passive_not_gauge", "representation" in reduction["passive_source_chart_generators"], reduction["passive_source_chart_generators"])
    check("regularity_not_constraint", reduction["open_conditions_are_linearized_constraints"] is False, "open locus")
    check("gauge_resolved", reduction["unresolved_gauge_degeneracy"] is False, "zero vertical space")

    response = specification["response_operator"]
    adequacy = specification["source_adequacy_result"]
    check("response_rank", response["response_rank"] == 2, str(response["response_rank"]))
    check("response_minor", response["rank_two_minor"] > 0.0, str(response["rank_two_minor"]))
    check("response_numeric", response["numerical_jacobian_max_error"] < 1.0e-9, str(response["numerical_jacobian_max_error"]))
    check("adequacy_verdict", adequacy["verdict"] == "necessary_condition_met_not_sufficient", adequacy["verdict"])
    check("adequacy_capacity", adequacy["computed_capacity_rank"] == 2, "capacity 2")
    check("adequacy_required", adequacy["required_declared_response_rank"] == 2, "required 2")
    check("adequacy_no_physical_probes", adequacy["physical_probe_admission_count"] == 0, "zero fully typed physical probes")
    check("adequacy_not_sufficient", adequacy["sufficiency_for_geometry"] is False, "not geometry sufficiency")

    parity = specification["finite_to_continuum_linearization_parity"]
    check("parity_levels", parity["levels"] == [24, 32, 48, 64], str(parity["levels"]))
    check("parity_values", parity["all_value_errors_strictly_decrease"] is True, "strictly decreasing")
    check("parity_c1", parity["all_c1_errors_strictly_decrease"] is True, "strictly decreasing")
    check("parity_cfl", parity["maximum_source_cfl"] <= 0.35 + 1.0e-12, str(parity["maximum_source_cfl"]))
    check("parity_no_metric_norm", parity["target_metric_norm_used"] is False, "source norm only")
    check("parity_no_physical_norm", parity["physical_derivative_norm_claimed"] is False, "no physical derivative norm")

    counter = specification["counterfamily"]
    check("counter_background", counter["selected_background_preserved"] is True, "background preserved")
    check("counter_source_only", counter["source_only"] is True, "source-only terms")
    check("counter_zero_sets", counter["principal_zero_sets_differ"] is True, "two explicit covectors")
    check("counter_changes_law", counter["changes_sealed_p3_t02_law"] is True, "candidate identity changes")
    check("counter_outside_identity", counter["inside_fixed_candidate_identity"] is False, "outside fixed candidate")
    check("counter_no_physical", counter["physical_inequivalence_claimed"] is False, "no physical inequivalence")
    check("fixed_candidate_unfrozen", counter["freeze_fixed_candidate"] is False, counter["freeze_reason"])
    check("counter_ledger_cases", len(ledger["countermodel_cases"]) == 10, "ten countermodel cases")
    check("counter_overread_frozen", ledger["freeze_evaluation"]["cross_law_uniqueness_overread_frozen"] is True, "cross-law overread frozen")

    crosscut = specification["cross_cutting_freeze"]
    check("scalar_route_frozen", crosscut["one_amplitude_route_status"] == "frozen", "V22-X03")
    check("graph_route_frozen", crosscut["unchanged_graph_decoder_route_status"] == "frozen", "V22-X03")
    check("no_decoder", crosscut["downstream_decoder_added"] is False, "no elaborate decoder")

    source_purity = specification["source_purity"]
    for field in ("target_atlas_input_count", "target_metric_input_count", "target_fit_count", "physical_clock_input_count"):
        check(f"purity_{field}", source_purity[field] == 0, f"{field}=0")
    check("purity_no_physical_gauge", source_purity["physical_gauge_assumed"] is False, "none assumed")

    authority = specification["authority_limits"]
    for field in (
        "ontology_modified", "source_law_adopted", "background_adopted",
        "physical_causal_cone_claimed", "lorentzian_signature_claimed",
        "effective_metric_constructed", "distance_to_gr_changed",
        "physics_promotion_authorized", "gate_chair_verdict_authorized",
        "completed_derivation_authorized",
    ):
        check(f"authority_{field}", authority[field] is False, f"{field}=false")

    cases = fixtures["cases"]
    check("fixture_count", len(cases) == 32, "32 frozen cases")
    check("fixture_unique", len({case["case_id"] for case in cases}) == len(cases), "unique case ids")
    check("fixture_status", fixtures["status"] == "frozen_before_target_access", fixtures["status"])
    check("math_child", math_child["status"] == "completed" and math_child["claim_boundary_preserved"] is True, "completed")
    check("phil_child", phil_child["status"] == "completed" and phil_child["claim_boundary_preserved"] is True, "completed")
    check("conflict_status", conflict["status"] == "resolved", conflict["status"])
    check("conflict_count", conflict["resolved_conflict_count"] == 5, "five resolved")
    check("no_conflicts", conflict["unresolved_conflicts"] == [], "none unresolved")

    required_tex = (
        "Selected regular affine witness", "Exact discrete commutation",
        "Uniform source-chart $C^1$ parity bound", "Counterfamily",
        "Expanded Distance-to-GR matrix", "constructed\\_candidate",
        "necessary\\_condition\\_met\\_not\\_sufficient",
    )
    for marker in required_tex:
        check(f"tex_{hashlib.sha256(marker.encode()).hexdigest()[:10]}", marker in tex, marker)
    check("fusion_result", "constructed draft/control candidate" in fusion, "decisive no-fog result")
    check("fusion_p4", "P4-T01" in fusion, "next route named")

    failed = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "v22_p3_t04_linear_response_validation_v1",
        "task_id": "RT-20260809-016",
        "job_id": "AJ-RT-20260809-016-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "checks": checks,
        "primary_result": primary,
        "independent_result": independent,
        "source_hashes": {
            path.name: digest(path)
            for path in (primary_path, independent_path, spec_path, ledger_path, fixture_path, math_child_path, phil_child_path, conflict_path, fusion_path, tex_path)
        },
        "claim_boundary": {
            "target_input_count": 0,
            "source_law_adopted": False,
            "physical_cone_constructed": False,
            "lorentzian_signature_constructed": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compact-output", type=Path)
    args = parser.parse_args()
    report = evaluate()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.compact_output:
        compact = {
            "schema_id": "v22_p3_t04_compact_receipt_v1",
            "task_id": report["task_id"],
            "job_id": report["job_id"],
            "status": report["status"],
            "check_count": report["check_count"],
            "failure_count": report["failure_count"],
            "selected_background": "qbar=(s1-s0,s2-s0,0,0,0,3)",
            "response_rank": report["primary_result"]["response"]["rank_two_minor"] > 0.0,
            "max_independent_linearization_error": report["independent_result"]["max_linearization_error"],
            "value_errors_strictly_decrease": report["primary_result"]["finite_continuum_parity"]["value_errors_strictly_decrease"],
            "c1_errors_strictly_decrease": report["primary_result"]["finite_continuum_parity"]["c1_errors_strictly_decrease"],
            "counterfamily_zero_sets_differ": report["primary_result"]["counterfamily"]["principal_zero_sets_differ"],
            "adequacy_verdict": "necessary_condition_met_not_sufficient",
            "result_type": "constructed_candidate",
            "p4_t01_selected": True,
            "claim_boundary": report["claim_boundary"],
        }
        args.compact_output.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
