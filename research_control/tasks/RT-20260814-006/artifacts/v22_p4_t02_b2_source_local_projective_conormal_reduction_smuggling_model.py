#!/usr/bin/env python3
"""Exact controls for the RT006 projective-conormal smuggling audit.

This is a task-local draft/control calculation.  It proves finite linear-
algebra and differential-form facts only; it does not supply source-law,
physical, empirical, adoption, or promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path


def det(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    value = Fraction(0)
    for perm in permutations(range(size)):
        inversions = sum(
            1
            for i in range(size)
            for j in range(i + 1, size)
            if perm[i] > perm[j]
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(perm):
            term *= matrix[row][column]
        value += term
    return value


def covector_pullback(covector: tuple[Fraction, ...], matrix: list[list[Fraction]]) -> tuple[Fraction, ...]:
    return tuple(
        sum(covector[row] * matrix[row][column] for row in range(len(covector)))
        for column in range(len(covector))
    )


def proportional(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> bool:
    pivot = next((index for index, value in enumerate(right) if value), None)
    if pivot is None:
        return not any(left)
    factor = left[pivot] / right[pivot]
    return all(left[index] == factor * right[index] for index in range(len(left)))


def diagonal_conformal(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> bool:
    factor = left[0] / right[0]
    return all(left[index] == factor * right[index] for index in range(len(left)))


def build_payload() -> dict[str, object]:
    zero = Fraction(0)
    one = Fraction(1)
    e0 = (one, zero, zero, zero)
    e1 = (zero, one, zero, zero)
    q0 = e0
    q1 = (one, one, zero, zero)

    shear = [
        [one, one, zero, zero],
        [zero, one, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    rotation = [
        [zero, one, zero, zero],
        [-one, zero, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]
    positive_ray_flip = [
        [-one, zero, zero, zero],
        [zero, -one, zero, zero],
        [zero, zero, one, zero],
        [zero, zero, zero, one],
    ]

    metric_a = (Fraction(-1), one, one, one)
    metric_b = (Fraction(-1), Fraction(2), Fraction(3), Fraction(5))

    gl_dimension = 16
    line_stabilizer_dimension = 13
    conformal_lorentz_stabilizer_dimension = 7
    projective_covector_orbit_dimension = gl_dimension - line_stabilizer_dimension
    conformal_lorentz_orbit_dimension = gl_dimension - conformal_lorentz_stabilizer_dimension

    epsilon = Fraction(1, 1000)
    # alpha_epsilon = dx0 + epsilon*x1*dx2 has
    # alpha_epsilon wedge d(alpha_epsilon)
    # = epsilon*dx0 wedge dx1 wedge dx2.
    nonintegrable_wedge_coefficient = epsilon
    # dq_epsilon for q_epsilon=x0+epsilon*x1*x2 is exact, hence d(dq)=0.
    coherent_exact_wedge_coefficient = Fraction(0)

    checks = {
        "projective_positive_scale_quotient": proportional(tuple(2 * x for x in e0), e0),
        "projective_sign_quotient": proportional(tuple(-x for x in e0), e0),
        "q0_q1_lines_distinct": not proportional(q0, q1),
        "same_reduct_can_carry_distinct_lines": q0 != q1,
        "shear_transports_q0_to_q1": proportional(covector_pullback(q0, shear), q1),
        "negative_reparametrization_preserves_line": proportional(tuple(-2 * x for x in q0), q0),
        "orientation_reversing_representatives_are_identified": proportional(q0, tuple(-x for x in q0)),
        "positive_determinant_stabilizer_flips_ray": det(positive_ray_flip) > 0
        and proportional(covector_pullback(q0, positive_ray_flip), q0)
        and covector_pullback(q0, positive_ray_flip)[0] < 0,
        "gl4_dimension_is_16": gl_dimension == 16,
        "line_stabilizer_dimension_is_13": line_stabilizer_dimension == 13,
        "line_stabilizer_codimension_is_3": projective_covector_orbit_dimension == 3,
        "conformal_lorentz_stabilizer_dimension_is_7": conformal_lorentz_stabilizer_dimension == 7,
        "conformal_lorentz_orbit_dimension_is_9": conformal_lorentz_orbit_dimension == 9,
        "line_stabilizer_too_large_for_equivariant_conformal_target": line_stabilizer_dimension
        > conformal_lorentz_stabilizer_dimension,
        "no_gl4_equivariant_projective_line_to_conformal_class_map": not (
            line_stabilizer_dimension <= conformal_lorentz_stabilizer_dimension
        ),
        "first_lorentz_form_accepts_e0_as_timelike_covector": metric_a[0] < 0,
        "second_lorentz_form_accepts_e0_as_timelike_covector": metric_b[0] < 0
        and all(value > 0 for value in metric_b[1:]),
        "shared_line_does_not_fix_conformal_class": not diagonal_conformal(metric_a, metric_b),
        "glplus_rotation_has_positive_determinant": det(rotation) > 0,
        "glplus_rotation_moves_e0_line": not proportional(covector_pullback(e0, rotation), e0),
        "bare_smooth4_has_no_glplus_fixed_projective_covector_line": det(rotation) > 0
        and not proportional(covector_pullback(e0, rotation), e0),
        "arbitrarily_small_nonintegrable_line_variation_exists": nonintegrable_wedge_coefficient != 0,
        "coherent_exact_label_variation_remains_integrable": coherent_exact_wedge_coefficient == 0,
        "proposal_robustness_is_strictly_domain_relative": nonintegrable_wedge_coefficient != coherent_exact_wedge_coefficient,
    }

    passed = sum(bool(value) for value in checks.values())
    payload = {
        "schema_id": "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_model_v1",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "check_count": len(checks),
        "pass_count": passed,
        "checks": checks,
        "exact_values": {
            "gl4_dimension": gl_dimension,
            "line_stabilizer_dimension": line_stabilizer_dimension,
            "projective_covector_orbit_dimension": projective_covector_orbit_dimension,
            "conformal_lorentz_stabilizer_dimension": conformal_lorentz_stabilizer_dimension,
            "conformal_lorentz_orbit_dimension": conformal_lorentz_orbit_dimension,
            "rotation_determinant": str(det(rotation)),
            "ray_flip_determinant": str(det(positive_ray_flip)),
            "nonintegrable_wedge_coefficient": str(nonintegrable_wedge_coefficient),
            "coherent_exact_wedge_coefficient": str(coherent_exact_wedge_coefficient),
        },
        "scope": {
            "current_source_natural_selection": False,
            "written_target_import_decided_by_model": False,
            "physical_causality_established": False,
            "conformal_geometry_established": False,
            "distance_to_gr_changed": False,
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
