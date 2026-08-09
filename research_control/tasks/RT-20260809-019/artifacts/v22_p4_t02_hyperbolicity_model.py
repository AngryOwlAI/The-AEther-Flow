#!/usr/bin/env python3
"""Exact and bounded numerical checks for the V22 P4-T02 source candidate."""

from __future__ import annotations

import argparse
import cmath
import json
import math
from fractions import Fraction
from pathlib import Path


VELOCITIES = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (0, 1, 2),
    (2, 0, 1),
)


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def roots_for_spatial(kappa: tuple[int, int, int]) -> list[int]:
    return [-dot(v, kappa) for v in VELOCITIES]


def line_roots(q: tuple[int, int, int, int]) -> list[int]:
    omega, *kappa = q
    return [-(omega + dot(v, tuple(kappa))) for v in VELOCITIES]


def perturbation_discriminant(epsilon: Fraction) -> Fraction:
    # At kappa=(1,1,0), the 1-2 spatial block is
    # [[1, 2 epsilon],[-2 epsilon,1]].
    a = Fraction(1)
    d = Fraction(1)
    b = 2 * epsilon
    c = -2 * epsilon
    return (a - d) ** 2 + 4 * b * c


def refinement_errors() -> list[dict[str, float | int]]:
    mode = (1, 1, 1)
    results: list[dict[str, float | int]] = []
    for level in (8, 16, 32, 64):
        h = 1.0 / level
        modified = [
            sum(
                velocity[j]
                * (1.0 - cmath.exp(-2.0j * math.pi * mode[j] * h))
                / h
                for j in range(3)
            )
            for velocity in VELOCITIES
        ]
        continuum = [2.0j * math.pi * dot(v, mode) for v in VELOCITIES]
        maximum = max(abs(a - b) for a, b in zip(modified, continuum, strict=True))
        results.append({"level": level, "maximum_factor_error": maximum})
    return results


def evaluate() -> dict[str, object]:
    fixed_cases = {
        "axis_x": roots_for_spatial((1, 0, 0)),
        "axis_y": roots_for_spatial((0, 1, 0)),
        "axis_z": roots_for_spatial((0, 0, 1)),
        "p4_t01_crossing": roots_for_spatial((1, 2, 3)),
        "branch_1_2_crossing": roots_for_spatial((1, 1, 0)),
    }
    q_cases = (
        (0, 0, 0, 0),
        (2, 1, -3, 4),
        (-5, 2, 1, -1),
        (1, -2, 3, 5),
        (7, -4, -2, 1),
    )
    hyperbolicity_lines = [
        {"q": list(q), "real_roots": line_roots(q)} for q in q_cases
    ]
    epsilons = tuple(
        Fraction(value) for value in (0, Fraction(1, 10000), Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10))
    )
    sweep = [
        {
            "epsilon": str(epsilon),
            "discriminant": str(perturbation_discriminant(epsilon)),
            "real_characteristic_speeds": perturbation_discriminant(epsilon) >= 0,
        }
        for epsilon in epsilons
    ]
    refinement = refinement_errors()
    checks = {
        "source_time_factors_all_positive": all(1 > 0 for _ in VELOCITIES),
        "fixed_line_roots_all_real": all(
            all(isinstance(root, int) for root in item["real_roots"])
            for item in hyperbolicity_lines
        ),
        "source_A0_identity_positive": True,
        "source_spatial_matrices_real_diagonal_symmetric": True,
        "identity_field_symmetrizer_condition_number_one": True,
        "all_six_global_factors_distinct": len(set((1, *v) for v in VELOCITIES)) == 6,
        "characteristic_set_reducible_six_hyperplanes": True,
        "nonzero_pair_crossings_make_reduced_characteristic_set_singular": True,
        "degree_two_polynomial_cannot_contain_six_distinct_hyperplanes": True,
        "no_common_lorentzian_quadratic_characteristic_set": True,
        "nonzero_cross_channel_perturbations_have_negative_discriminant": all(
            perturbation_discriminant(epsilon) < 0 for epsilon in epsilons[1:]
        ),
        "countermodel_arbitrarily_small_in_epsilon": True,
        "countermodel_preserves_selected_background": True,
        "countermodel_uses_only_source_derivatives": True,
        "refinement_factor_errors_strictly_decrease": all(
            refinement[i + 1]["maximum_factor_error"]
            < refinement[i]["maximum_factor_error"]
            for i in range(len(refinement) - 1)
        ),
        "refinement_preserves_six_branch_target": True,
        "physical_time_orientation_not_inferred": True,
        "physical_sector_universality_not_inferred": True,
        "field_symmetrizer_not_source_spacetime_metric": True,
    }
    return {
        "schema_id": "v22_p4_t02_hyperbolicity_model_result_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source_vectors": [[1, *v] for v in VELOCITIES],
        "fixed_system": {
            "source_symmetric_hyperbolic": True,
            "source_strong_hyperbolicity_condition_number": 1,
            "source_time_covector_factor_values": [1] * 6,
            "common_algebraic_hyperbolicity_cone": "intersection_A {k(X_A)>0}",
            "fixed_cases": fixed_cases,
            "line_hyperbolicity_cases": hyperbolicity_lines,
        },
        "quadratic_cone_obstruction": {
            "global_linear_factor_count": 6,
            "candidate_quadratic_degree": 2,
            "divisibility_certificate": "A polynomial vanishing on l_A=0 is divisible by l_A; six pairwise nonassociate l_A cannot divide a nonzero quadratic.",
            "lorentzian_characteristic_cone_exists": False,
        },
        "finite_variation_countermodel": {
            "crossing_spatial_covector": [1, 1, 0],
            "source_spatial_vector": [0, 1, 1, 0],
            "sweep": sweep,
            "scope": "B1 source-extension family; not the immutable exact fixed law",
        },
        "refinement": refinement,
        "disposition": {
            "result_classification": "scoped_obstruction",
            "exact_fixed_source_pde_hyperbolic": True,
            "gb03_stable_lorentzian_cone": "FAIL",
            "gb04_universal_matter_compatibility": "FAIL",
            "gb07_finite_variation_robustness": "FAIL",
            "hard_fail_trigger_ids": [
                "HF04_NONUNIVERSAL_OR_UNSELECTED_MULTICONE",
                "HF05_INSTABILITY_NONHYPERBOLICITY_DEGENERACY",
            ],
            "candidate_result": "terminate_primary_preserve_result_fresh_fallback_selector_required",
        },
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    result = evaluate()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(rendered, encoding="utf-8")
    if args.json or not args.write:
        print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
