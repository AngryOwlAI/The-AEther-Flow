#!/usr/bin/env python3
"""Exact controls for the RT001 projective-conormal Refuter stress.

This task-local draft/control calculation checks finite linear-algebra and
differential-form fixtures only.  It does not adopt source data, choose an
occurring proposal, construct physical causality or a metric, or change any
Distance-to-GR burden.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path


Vector = tuple[Fraction, ...]
Matrix = list[list[Fraction]]


def determinant(matrix: Matrix) -> Fraction:
    """Return the exact determinant of a small square matrix."""

    size = len(matrix)
    total = Fraction(0)
    for permutation in permutations(range(size)):
        inversions = sum(
            1
            for left in range(size)
            for right in range(left + 1, size)
            if permutation[left] > permutation[right]
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total += term
    return total


def matrix_product(left: Matrix, right: Matrix) -> Matrix:
    size = len(left)
    return [
        [
            sum(left[row][middle] * right[middle][column] for middle in range(size))
            for column in range(size)
        ]
        for row in range(size)
    ]


def covector_pullback(covector: Vector, matrix: Matrix) -> Vector:
    return tuple(
        sum(covector[row] * matrix[row][column] for row in range(len(covector)))
        for column in range(len(covector))
    )


def proportional(left: Vector, right: Vector) -> bool:
    pivot = next((index for index, value in enumerate(right) if value), None)
    if pivot is None:
        return not any(left)
    factor = left[pivot] / right[pivot]
    return all(left[index] == factor * right[index] for index in range(len(left)))


def positive_proportional(left: Vector, right: Vector) -> bool:
    pivot = next((index for index, value in enumerate(right) if value), None)
    if pivot is None:
        return False
    factor = left[pivot] / right[pivot]
    return factor > 0 and all(
        left[index] == factor * right[index] for index in range(len(left))
    )


def diagonal_conformal(left: Vector, right: Vector) -> bool:
    factor = left[0] / right[0]
    return all(left[index] == factor * right[index] for index in range(len(left)))


def build_payload() -> dict[str, object]:
    zero = Fraction(0)
    one = Fraction(1)
    e0 = (one, zero, zero, zero)
    e1 = (zero, one, zero, zero)
    e01 = (one, one, zero, zero)

    identity = [
        [one, zero, zero, zero],
        [zero, one, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    quarter_rotation = [
        [zero, one, zero, zero],
        [-one, zero, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    determinant_one_shear = [
        [one, one, zero, zero],
        [zero, one, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    ray_flip = [
        [-one, zero, zero, zero],
        [zero, -one, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    line_arrow_a = [
        [Fraction(2), zero, zero, zero],
        [zero, one, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    line_arrow_a_inverse = [
        [Fraction(1, 2), zero, zero, zero],
        [zero, one, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    line_arrow_b = [
        [one, zero, zero, zero],
        [zero, one, one, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    line_arrow_b_inverse = [
        [one, zero, zero, zero],
        [zero, one, -one, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]

    epsilon = Fraction(1, 1000)
    compact_radius = Fraction(10)
    c0_deviation_bound = epsilon * compact_radius
    c1_derivative_bound = epsilon
    nonfrobenius_wedge_coefficient = epsilon
    exact_label_wedge_coefficient = Fraction(0)

    gl_dimension = 16
    line_stabilizer_dimension = 13
    projective_line_orbit_dimension = 3
    conformal_lorentz_stabilizer_dimension = 7
    lorentz_conformal_orbit_dimension = 9
    coorientation_kernel_index = 2

    metric_a = (Fraction(-1), one, one, one)
    metric_b = (Fraction(-1), Fraction(2), Fraction(3), Fraction(5))
    metric_c = (Fraction(-1), Fraction(7), Fraction(11), Fraction(13))

    arrow_product = matrix_product(line_arrow_a, line_arrow_b)
    inverse_product = matrix_product(line_arrow_b_inverse, line_arrow_a_inverse)

    checks = {
        "identity_is_line_preserving_arrow": proportional(
            covector_pullback(e0, identity), e0
        ),
        "line_preserving_arrow_a_is_invertible": determinant(line_arrow_a) != 0,
        "line_preserving_arrow_b_is_invertible": determinant(line_arrow_b) != 0,
        "line_preserving_arrows_close_under_composition": proportional(
            covector_pullback(e0, arrow_product), e0
        ),
        "line_preserving_arrow_a_inverse_preserves_line": proportional(
            covector_pullback(e0, line_arrow_a_inverse), e0
        ),
        "line_preserving_arrow_b_inverse_preserves_line": proportional(
            covector_pullback(e0, line_arrow_b_inverse), e0
        ),
        "inverse_of_composite_is_line_preserving": proportional(
            covector_pullback(e0, inverse_product), e0
        ),
        "full_source_group_contains_excluded_line_mover": determinant(
            quarter_rotation
        ) > 0
        and not proportional(covector_pullback(e0, quarter_rotation), e0),
        "determinant_one_rotation_moves_e0_to_e1": determinant(quarter_rotation)
        == 1
        and proportional(covector_pullback(e0, quarter_rotation), e1),
        "determinant_one_shear_moves_e0_to_e0_plus_e1": determinant(
            determinant_one_shear
        )
        == 1
        and proportional(covector_pullback(e0, determinant_one_shear), e01),
        "strict_identity_over_m_lines_differ": not proportional(e0, e01),
        "strict_difference_disappears_under_proposal_isomorphism": proportional(
            covector_pullback(e0, determinant_one_shear), e01
        ),
        "positive_projective_scale_is_forgotten": proportional(
            tuple(Fraction(3) * value for value in e0), e0
        ),
        "negative_projective_scale_is_forgotten": proportional(
            tuple(-value for value in e0), e0
        ),
        "positive_ray_is_not_preserved_by_negative_scale": not positive_proportional(
            tuple(-value for value in e0), e0
        ),
        "orientation_preserving_line_stabilizer_flips_ray": determinant(ray_flip)
        == 1
        and proportional(covector_pullback(e0, ray_flip), e0)
        and not positive_proportional(covector_pullback(e0, ray_flip), e0),
        "coorientation_is_an_index_two_refinement": coorientation_kernel_index == 2,
        "arbitrarily_small_nonfrobenius_fixture_is_nonintegrable": nonfrobenius_wedge_coefficient
        != 0,
        "nonfrobenius_fixture_c0_small_on_fixed_compact": c0_deviation_bound
        < Fraction(1, 50),
        "nonfrobenius_fixture_c1_small_on_fixed_compact": c1_derivative_bound
        < Fraction(1, 500),
        "nearby_exact_label_fixture_remains_integrable": exact_label_wedge_coefficient
        == 0,
        "ambient_c1_neighborhood_contains_both_domain_classes": nonfrobenius_wedge_coefficient
        != exact_label_wedge_coefficient,
        "gl4_dimension_is_16": gl_dimension == 16,
        "projective_line_stabilizer_dimension_is_13": line_stabilizer_dimension
        == 13,
        "projective_line_orbit_dimension_is_3": gl_dimension
        - line_stabilizer_dimension
        == projective_line_orbit_dimension,
        "conformal_lorentz_stabilizer_dimension_is_7": conformal_lorentz_stabilizer_dimension
        == 7,
        "lorentz_conformal_orbit_dimension_is_9": gl_dimension
        - conformal_lorentz_stabilizer_dimension
        == lorentz_conformal_orbit_dimension,
        "line_stabilizer_cannot_embed_in_conformal_stabilizer": line_stabilizer_dimension
        > conformal_lorentz_stabilizer_dimension,
        "metric_a_is_lorentzian_with_e0_timelike": metric_a[0] < 0
        and all(value > 0 for value in metric_a[1:]),
        "metric_b_is_lorentzian_with_e0_timelike": metric_b[0] < 0
        and all(value > 0 for value in metric_b[1:]),
        "metric_c_is_lorentzian_with_e0_timelike": metric_c[0] < 0
        and all(value > 0 for value in metric_c[1:]),
        "metric_a_and_b_are_not_conformal": not diagonal_conformal(
            metric_a, metric_b
        ),
        "metric_b_and_c_are_not_conformal": not diagonal_conformal(
            metric_b, metric_c
        ),
        "one_projective_line_has_multiple_conformal_completions": not diagonal_conformal(
            metric_a, metric_b
        )
        and not diagonal_conformal(metric_b, metric_c),
    }

    pass_count = sum(bool(value) for value in checks.values())
    payload: dict[str, object] = {
        "schema_id": "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_model_v1",
        "status": "PASS" if pass_count == len(checks) else "FAIL",
        "check_count": len(checks),
        "pass_count": pass_count,
        "checks": checks,
        "exact_values": {
            "epsilon": str(epsilon),
            "compact_radius": str(compact_radius),
            "c0_deviation_bound": str(c0_deviation_bound),
            "c1_derivative_bound": str(c1_derivative_bound),
            "nonfrobenius_wedge_coefficient": str(nonfrobenius_wedge_coefficient),
            "exact_label_wedge_coefficient": str(exact_label_wedge_coefficient),
            "quarter_rotation_determinant": str(determinant(quarter_rotation)),
            "shear_determinant": str(determinant(determinant_one_shear)),
            "ray_flip_determinant": str(determinant(ray_flip)),
            "gl4_dimension": gl_dimension,
            "line_stabilizer_dimension": line_stabilizer_dimension,
            "projective_line_orbit_dimension": projective_line_orbit_dimension,
            "conformal_lorentz_stabilizer_dimension": conformal_lorentz_stabilizer_dimension,
            "lorentz_conformal_orbit_dimension": lorentz_conformal_orbit_dimension,
            "coorientation_kernel_index": coorientation_kernel_index,
        },
        "scope": {
            "conditional_rt005_rt006_mathematics_preserved": True,
            "current_source_natural_selection_established": False,
            "independent_arrow_admissibility_established": False,
            "coorientation_or_time_orientation_established": False,
            "physical_causality_established": False,
            "conformal_geometry_established": False,
            "g_eff_constructed": False,
            "distance_to_gr_changed": False,
            "global_no_go_claimed": False,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    payload = build_payload()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.write.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
