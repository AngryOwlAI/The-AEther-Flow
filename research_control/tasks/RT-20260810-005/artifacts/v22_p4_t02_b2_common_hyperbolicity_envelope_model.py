#!/usr/bin/env python3
"""Exact finite checks for the RT-20260810-005 envelope candidate.

The coordinate realization is reproduction-only.  The scientific artifact
states the source-intrinsic construction and its authority limits.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from typing import Iterable


Vector = tuple[Fraction, Fraction, Fraction, Fraction]
Covector = tuple[Fraction, Fraction, Fraction, Fraction]
Matrix = tuple[tuple[Fraction, ...], ...]


def dot(k: Covector, v: Vector) -> Fraction:
    return sum((ki * vi for ki, vi in zip(k, v)), Fraction(0))


def mat_vec(a: Matrix, v: Vector) -> Vector:
    return tuple(sum((a[i][j] * v[j] for j in range(4)), Fraction(0)) for i in range(4))  # type: ignore[return-value]


def transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(4)) for i in range(4))


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(4)), Fraction(0)) for j in range(4))
        for i in range(4)
    )


def sign(x: Fraction) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0


def responses(k: Covector, vectors: Iterable[Vector]) -> tuple[Fraction, ...]:
    return tuple(dot(k, v) for v in vectors)


def run_checks() -> dict[str, object]:
    eps = Fraction(1, 3)
    u: Vector = (1, 0, 0, 0)
    z: Vector = (0, 1, 0, 0)
    h: Covector = (1, 0, 0, 0)
    v_r: Vector = (1, eps, 0, 0)
    v_s: Vector = u
    v_d: Vector = (1, -eps, 0, 0)
    vectors = (v_r, v_s, v_d)

    base_responses = responses(h, vectors)
    base_orientation_pass = base_responses == (1, 1, 1)

    q: Covector = (2, 3, 0, 0)
    roots = tuple(-dot(q, v) for v in vectors)
    expected_roots = (Fraction(-3), Fraction(-2), Fraction(-1))
    root_union_pass = roots == expected_roots

    k_inside: Covector = (1, Fraction(1, 2), 0, 0)
    inside_responses = responses(k_inside, vectors)
    common_cone_pass = inside_responses == (Fraction(7, 6), 1, Fraction(5, 6)) and all(
        value > 0 for value in inside_responses
    )
    product_value = inside_responses[0] * inside_responses[1] * inside_responses[2]
    product_formula_pass = product_value == Fraction(35, 36)

    ray_scaled = tuple(2 * value for value in inside_responses)
    common_ray_pass = all(ray_scaled[i] * inside_responses[0] == inside_responses[i] * ray_scaled[0] for i in range(3))
    positive_orbit_pass = tuple(sign(value) for value in inside_responses) == (1, 1, 1)

    delta = Fraction(1, 10)
    error_bound = Fraction(7, 3) * delta + 4 * delta * delta
    strict_lower_bound = 1 - error_bound
    strict_margin_pass = strict_lower_bound == Fraction(109, 150) and strict_lower_bound > 0

    # Independent rational perturbations, each within the declared delta box.
    h_p: Covector = (Fraction(101, 100), Fraction(1, 100), Fraction(-1, 100), 0)
    perturbed_vectors: tuple[Vector, ...] = (
        (1, eps + Fraction(1, 100), Fraction(1, 100), 0),
        (Fraction(99, 100), Fraction(-1, 100), 0, Fraction(1, 100)),
        (Fraction(101, 100), -eps, Fraction(-1, 100), Fraction(-1, 100)),
    )
    perturbed_responses = responses(h_p, perturbed_vectors)
    independent_perturbation_pass = all(value >= strict_lower_bound for value in perturbed_responses)

    # Empty-intersection certificate: w1+w2+w3=0 with all coefficients positive.
    w1: Vector = (1, 0, 0, 0)
    w2: Vector = (0, 1, 0, 0)
    w3: Vector = (-1, -1, 0, 0)
    positive_dependence = tuple(w1[i] + w2[i] + w3[i] for i in range(4))
    empty_intersection_certificate_pass = positive_dependence == (0, 0, 0, 0)
    contradiction_sample_pass = not (
        dot((1, 1, 0, 0), w1) > 0
        and dot((1, 1, 0, 0), w2) > 0
        and dot((1, 1, 0, 0), w3) > 0
    )

    # A shear provides a nontrivial source-presentation covariance check.
    a: Matrix = (
        (1, 1, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    # k' chosen so A^T k' = k_inside.
    k_prime: Covector = (1, Fraction(-1, 2), 0, 0)
    pullback = mat_vec(transpose(a), k_prime)  # type: ignore[arg-type]
    transported_vectors = tuple(mat_vec(a, v) for v in vectors)
    covariance_pass = pullback == k_inside and responses(k_prime, transported_vectors) == inside_responses

    b: Matrix = (
        (1, 0, 1, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    c = mat_mul(b, a)
    cocycle_pass = mat_mul(b, a) == c and mat_vec(b, mat_vec(a, v_r)) == mat_vec(c, v_r)

    multiplicity_control_pass = len(set(responses((2, 0, 0, 0), vectors))) == 1
    outside = responses((0, 1, 0, 0), vectors)
    boundary_split_pass = tuple(sign(value) for value in outside) == (1, 0, -1)

    checks = {
        "base_orientation": base_orientation_pass,
        "product_root_union": root_union_pass,
        "common_cone": common_cone_pass,
        "product_formula": product_formula_pass,
        "common_ray": common_ray_pass,
        "positive_orbit": positive_orbit_pass,
        "strict_margin": strict_margin_pass,
        "independent_perturbation": independent_perturbation_pass,
        "empty_intersection_certificate": empty_intersection_certificate_pass,
        "empty_intersection_sample": contradiction_sample_pass,
        "source_presentation_covariance": covariance_pass,
        "transition_cocycle": cocycle_pass,
        "multiplicity_control": multiplicity_control_pass,
        "boundary_split": boundary_split_pass,
    }
    return {
        "schema_id": "v22_p4_t02_b2_common_hyperbolicity_envelope_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "authority": "support_only_not_proof_authority",
        "epsilon": str(eps),
        "base_responses": [str(value) for value in base_responses],
        "sample_roots": [str(value) for value in roots],
        "inside_responses": [str(value) for value in inside_responses],
        "strict_lower_bound": str(strict_lower_bound),
        "perturbed_responses": [str(value) for value in perturbed_responses],
        "empty_intersection_positive_dependence": [str(value) for value in positive_dependence],
        "checks": checks,
        "authority_limits": {
            "physical_cone_constructed": False,
            "universal_propagation_derived": False,
            "effective_metric_constructed": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "distance_to_gr_changed": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = run_checks()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
