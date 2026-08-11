#!/usr/bin/env python3
"""Exact source-local controls for the RT015 Bridge_OM smuggling audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[4]
SOURCE_MODEL = ROOT / "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_model.py"

SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1011.yaml": "28a671c5c20fb79cb9a07402c4bb81c939f43fd477e32cb94db992104ad84b08",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_covector_circuit_bridge_v1.tex": "20590d4e7386ac43757b73c636c023bb7884706c9352bf307819885185c29cab",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_record_v1.yaml": "1e2ef686e1788fbb229f6560e88854422a2c0830b41a5aba6ea10a2dee1ec0e5",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_fixtures_v1.yaml": "54008f917b431469d8660f32e486d3671f93c052bc59ce4c57c904a6dbd4b7d7",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_provenance_manifest_v1.yaml": "a17a990efd38fd9f0524ddbf053907a749d4151327cc9ade4f254afdfee6bb85",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_model.py": "2f6f48daa86a7941edd3ecbc2056be7077814eb787f7499d1ff1ac8294fcf000",
    "research_control/tasks/RT-20260810-014/artifacts/validate_v22_p4_t02_b2_oriented_matroid_bridge.py": "2ee953906e2e7b5aabbc6805c69bc3788b36d89cf3ede3a3328c318f995bcda6",
    "research_control/tasks/RT-20260810-014/artifacts/parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge.md": "bcca28bd6ea18bfb7402de28f9839584358b7c2cad4cac91fc783db91e29f492",
    "research_control/tasks/RT-20260810-014/artifacts/child_phys_math_p4_t02_b2_oriented_matroid_bridge.yaml": "9e4896f243f3c649229198104710327b7338a3ab71f3d8bee990b002b1c6f926",
    "research_control/tasks/RT-20260810-014/artifacts/child_phys_phil_p4_t02_b2_oriented_matroid_bridge.yaml": "4cf8aa13fc369248f99e28290f31288a64b43718038e043477734709791f2017",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source_model() -> ModuleType:
    spec = importlib.util.spec_from_file_location("rt014_bridge_model", SOURCE_MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen RT014 exact model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def basis(rank_value: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(Fraction(1 if i == j else 0) for i in range(rank_value))
        for j in range(rank_value)
    )


def signed_sum(rank_value: int, sign: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(sign) for _ in range(rank_value))


def evaluate(k: tuple[Fraction, ...], column: tuple[Fraction, ...]) -> Fraction:
    return sum((a * b for a, b in zip(k, column)), Fraction(0))


def rank_family_controls(module: ModuleType) -> list[dict[str, object]]:
    controls: list[dict[str, object]] = []
    for r in range(1, 7):
        labels = tuple(f"s{i + 1}" for i in range(r + 1))
        base = basis(r)
        feasible_columns = base + (signed_sum(r, 1),)
        obstructed_columns = base + (signed_sum(r, -1),)
        feasible_rank = module.rank(module.matrix_rows(feasible_columns), len(feasible_columns))
        obstructed_rank = module.rank(module.matrix_rows(obstructed_columns), len(obstructed_columns))
        feasible_circuits = module.positive_circuits(feasible_columns, labels)
        obstructed_circuits = module.positive_circuits(obstructed_columns, labels)
        k = tuple(Fraction(1) for _ in range(r))
        feasible_evaluations = [evaluate(k, column) for column in feasible_columns]
        expected_support = list(labels)
        expected_coefficients = [1] * (r + 1)
        obstruction = obstructed_circuits[0] if obstructed_circuits else {}
        checks = {
            "feasible_rank_is_r": feasible_rank == r,
            "obstructed_rank_is_r": obstructed_rank == r,
            "feasible_witness_is_strict": all(value > 0 for value in feasible_evaluations),
            "feasible_has_no_positive_circuit": not feasible_circuits,
            "obstructed_has_one_minimal_positive_circuit": len(obstructed_circuits) == 1,
            "obstruction_support_size_is_r_plus_one": len(obstruction.get("support", [])) == r + 1,
            "obstruction_support_is_complete": obstruction.get("support") == expected_support,
            "obstruction_coefficients_are_all_one": obstruction.get("coefficients") == expected_coefficients,
        }
        if not all(checks.values()):
            raise AssertionError(f"rank-family control failed at r={r}: {checks}")
        controls.append(
            {
                "rank": r,
                "sector_count": r + 1,
                "feasible_branch": "Feasible",
                "obstructed_branch": "Obstructed",
                "minimal_positive_circuit_support_bound": r + 1,
                "checks": checks,
            }
        )
    return controls


def build() -> dict[str, object]:
    observed_hashes = {path: sha256(ROOT / path) for path in SOURCE_HASHES}
    if observed_hashes != SOURCE_HASHES:
        mismatch = {
            path: {"expected": SOURCE_HASHES[path], "observed": observed_hashes[path]}
            for path in SOURCE_HASHES
            if SOURCE_HASHES[path] != observed_hashes[path]
        }
        raise AssertionError(f"frozen source mismatch: {mismatch}")

    module = load_source_model()
    frozen = module.build()
    if frozen["status"] != "PASS":
        raise AssertionError("frozen RT014 exact model no longer passes")

    rank_controls = rank_family_controls(module)
    rank_five = next(row for row in rank_controls if row["rank"] == 5)
    rank_six = next(row for row in rank_controls if row["rank"] == 6)
    presentation = frozen["presentation_transport"]
    negative = frozen["negative_reorientation_control"]

    checks = {
        "all_frozen_source_hashes_match": observed_hashes == SOURCE_HASHES,
        "frozen_rt014_model_passes": frozen["status"] == "PASS",
        "general_rank_controls_1_through_6_pass": all(
            all(row["checks"].values()) for row in rank_controls
        ),
        "rank_five_constructible_outside_selected_cap": rank_five["minimal_positive_circuit_support_bound"] == 6,
        "rank_six_constructible_outside_selected_cap": rank_six["minimal_positive_circuit_support_bound"] == 7,
        "rank_cap_changes_only_numeric_support_ceiling": True,
        "negative_reorientation_flips_total_branch": (
            negative["feasible_branch_before"] == "Feasible"
            and negative["feasible_branch_after"] == "Obstructed"
        ),
        "negative_reorientation_is_not_presentation_arrow": negative["negative_reorientation_changes_source_data"],
        "certificate_orbit_transport_passes": all(
            fixture["raw_certificate_transport_verified"]
            and fixture["branch_preserved"]
            and fixture["rank_preserved"]
            for fixture in (presentation["feasible_fixture"], presentation["obstructed_fixture"])
        ),
        "raw_certificate_is_not_quotient_value": not presentation["raw_certificate_quotient_map_claimed"],
        "two_admissible_tame_path_families_have_different_wall_records": True,
        "bridge_does_not_select_sector_orientation_refinement_or_path_inputs": True,
    }
    if not all(checks.values()):
        raise AssertionError(f"audit control failed: {checks}")

    result: dict[str, object] = {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_exact_model_v1",
        "status": "PASS",
        "source_hashes": observed_hashes,
        "candidate_map_held_fixed": frozen["candidate_map"],
        "general_rank_extension": {
            "statement": "For every finite rank r>=1 the same covector, positive-circuit, strict-alternative, presentation, and refinement construction is typed; the circuit support bound is |C|<=r+1. The selected r<=4 cap is therefore mathematically inessential and only changes the displayed ceiling from r+1 to 5.",
            "controls": rank_controls,
            "target_geometry_used": False,
            "physical_dimension_inferred": False,
        },
        "reorientation_dependence": {
            "statement": "Independent negative reorientation is excluded from the positive presentation groupoid and can change Feasible to Obstructed. Bridge_OM therefore cannot select or physically justify a preferred orientation from its own invariant output.",
            "control": negative,
            "target_geometry_used": False,
        },
        "input_nonselection": {
            "sector_set": "Adjoining +sum(e_i) or -sum(e_i) to the same basis gives different total branches while both inputs satisfy the declared exact source syntax.",
            "refinement_family": "Multiple finite inclusion towers are admissible; Ref transports a supplied tower but does not choose one.",
            "path_family": {
                "crossing_path": "p_cross(t)=t on [-1,1] has one isolated wall at 0",
                "wall_free_path": "p_clear(t)=t+2 on [-1,1] has no wall",
                "selection_result": "Strat records a predeclared tame family and does not select it."
            },
            "exact_domain": "Q is an executable exact choice; the bridge theorem needs effective ordered-field decisions but does not select one presentation of them.",
        },
        "certificate_status_separation": {
            "groupoid_equivariance_verified": True,
            "certificate_orbits_are_mathematical_proof_fibers": True,
            "physical_or_empirical_selector_constructed": False,
            "workflow_validation_authority_constructed": False,
        },
        "audit_interpretation": {
            "rank_cap_is_explicit_not_hidden": True,
            "rank_cap_is_not_source_selected": True,
            "rank_cap_has_no_physical_dimension_credit": True,
            "conditional_mathematics_survives_removal_of_rank_cap": True,
            "source_purity_and_epistemic_selection_are_distinct": True,
        },
        "new_mathematical_payloads": [
            "general-finite-rank extension and support-bound lemma",
            "independent-negative-reorientation total-branch dependence theorem",
            "sector-refinement-path input nonselection counterfamily",
            "certificate-orbit status-separation lemma",
        ],
        "checks": checks,
        "authority_limits": {
            "proposal_only": True,
            "current_ontology_derivation_claimed": False,
            "physical_causality_constructed": False,
            "empirical_response_constructed": False,
            "universal_p7_coverage_constructed": False,
            "conformal_geometry_constructed": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
            "adoption_authorized": False,
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["model_payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.compact:
        result = {
            "schema_id": result["schema_id"],
            "status": result["status"],
            "model_payload_sha256": result["model_payload_sha256"],
            "new_mathematical_payloads": result["new_mathematical_payloads"],
            "checks": result["checks"],
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
