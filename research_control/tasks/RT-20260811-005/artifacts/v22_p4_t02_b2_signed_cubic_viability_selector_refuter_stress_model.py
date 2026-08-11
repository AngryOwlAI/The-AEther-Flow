#!/usr/bin/env python3
"""Exact controls for the RT005 signed-cubic viability-selector stress."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any


Q = Fraction


def qtext(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def field(a: Fraction, sigma: int, mu: Fraction, gamma: Fraction = Q(1)) -> Fraction:
    """F_{sigma,mu}(a)=-gamma*a^3+mu*sigma."""

    return -gamma * a**3 + mu * sigma


def transverse_field(
    a: Fraction,
    z: Fraction,
    epsilon: Fraction,
    gamma: Fraction = Q(1),
) -> tuple[Fraction, Fraction]:
    return (-gamma * a**3 + epsilon * z, Q(0))


def fixed_squared_flow(u: Fraction, gamma: Fraction, t: Fraction) -> Fraction:
    return u / (1 + 2 * gamma * t * u)


def barrier_squared(u: Fraction, a_star_sq: Fraction) -> Fraction:
    return u / (a_star_sq + u)


def run_model() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(check_id: str, passed: bool, evidence: Any) -> None:
        checks.append({"check_id": check_id, "passed": passed, "evidence": evidence})

    gamma = Q(1)
    epsilon = Q(1, 1000)
    roots = {-epsilon: Q(-1, 10), Q(0): Q(0), epsilon: Q(1, 10)}

    reflection_fixtures = []
    reflection_ok = True
    for mu in (-epsilon, Q(0), epsilon):
        for sigma in (-1, 1):
            for a in (Q(-2), Q(-1, 3), Q(0), Q(1, 4), Q(3)):
                lhs = field(-a, -sigma, mu, gamma)
                rhs = -field(a, sigma, mu, gamma)
                reflection_ok &= lhs == rhs
                reflection_fixtures.append(
                    {
                        "mu": qtext(mu),
                        "sigma": sigma,
                        "a": qtext(a),
                        "lhs": qtext(lhs),
                        "rhs": qtext(rhs),
                    }
                )
    record(
        "reflection_equivariant_mu_family",
        reflection_ok,
        {"fixture_count": len(reflection_fixtures), "fixtures": reflection_fixtures},
    )

    perturbation_ok = True
    perturbation_fixtures = []
    for sigma in (-1, 1):
        for a in (Q(-100), Q(-1), Q(0), Q(2), Q(100)):
            difference = field(a, sigma, -epsilon) - field(a, sigma, Q(0))
            perturbation_ok &= abs(difference) == epsilon
            perturbation_fixtures.append(
                {"sigma": sigma, "a": qtext(a), "difference": qtext(difference)}
            )
    record(
        "uniform_arbitrarily_small_drift",
        perturbation_ok,
        {
            "epsilon": qtext(epsilon),
            "global_C0_distance": qtext(epsilon),
            "derivative_difference_orders_ge_1": "0",
            "fixtures": perturbation_fixtures,
        },
    )

    outward_ok = True
    outward_fixtures = []
    for y in (Q(1, 100), Q(1, 10), Q(1), Q(10)):
        derivative = -gamma * y**3 - epsilon
        outward_ok &= derivative <= -epsilon
        outward_fixtures.append(
            {
                "y": qtext(y),
                "ydot": qtext(derivative),
                "crossing_time_upper_bound": qtext(y / epsilon),
            }
        )
    record(
        "outward_drift_crossing_bound",
        outward_ok,
        {"equation": "ydot=-gamma*y^3-epsilon<=-epsilon", "fixtures": outward_fixtures},
    )

    equilibrium_ok = True
    equilibrium_fixtures = []
    for mu, root in roots.items():
        residual = -gamma * root**3 + mu
        equilibrium_ok &= residual == 0
        equilibrium_fixtures.append(
            {
                "mu": qtext(mu),
                "equilibrium_y": qtext(root),
                "residual": qtext(residual),
                "location": "selected" if root > 0 else "boundary" if root == 0 else "opposite",
            }
        )
    record(
        "exact_boundary_bifurcation",
        equilibrium_ok,
        {"fixtures": equilibrium_fixtures},
    )

    lyapunov_ok = True
    lyapunov_fixtures = []
    for mu, root in roots.items():
        for y in (Q(-2), Q(-1, 10), Q(0), Q(1, 10), Q(2)):
            derivative = -2 * gamma * (y - root) ** 2 * (y**2 + y * root + root**2)
            expected_zero = y == root
            lyapunov_ok &= derivative <= 0 and ((derivative == 0) == expected_zero)
            lyapunov_fixtures.append(
                {
                    "mu": qtext(mu),
                    "root": qtext(root),
                    "y": qtext(y),
                    "Vdot": qtext(derivative),
                }
            )
    record(
        "unique_equilibrium_lyapunov_control",
        lyapunov_ok,
        {"fixture_count": len(lyapunov_fixtures), "fixtures": lyapunov_fixtures},
    )

    transverse_ok = True
    transverse_fixtures = []
    for sigma in (-1, 1):
        z = Q(-sigma)
        for a in (Q(-1), Q(0), Q(2)):
            fa, fz = transverse_field(a, z, epsilon, gamma)
            expected = field(a, sigma, -epsilon, gamma)
            reflected_a, reflected_z = transverse_field(-a, -z, epsilon, gamma)
            transverse_ok &= fa == expected and fz == 0 and reflected_a == -fa and reflected_z == 0
            transverse_fixtures.append(
                {
                    "sigma": sigma,
                    "a": qtext(a),
                    "z": qtext(z),
                    "a_dot": qtext(fa),
                }
            )
        for n in (2, 5, 10, 20):
            near_epsilon = Q(1, n)
            near_z = Q(-sigma, n)
            near_a = Q(sigma, n**2)
            fa, fz = transverse_field(near_a, near_z, near_epsilon, gamma)
            oriented_derivative = sigma * fa
            expected_oriented = -Q(1, n**6) - Q(1, n**2)
            transverse_ok &= fz == 0 and oriented_derivative == expected_oriented
            transverse_fixtures.append(
                {
                    "sigma": sigma,
                    "n": n,
                    "a": qtext(near_a),
                    "z": qtext(near_z),
                    "oriented_derivative": qtext(oriented_derivative),
                    "crossing_time_upper_bound": "1",
                }
            )
    record(
        "transverse_mode_reproduces_outward_countermodel",
        transverse_ok,
        {"fixtures": transverse_fixtures},
    )

    token_ok = True
    token_fixtures = []
    flip_probability = Q(1, 1000)
    for steps in (1, 2, 10, 20):
        survival = (1 - flip_probability) ** steps
        exit_probability = 1 - survival
        endpoint_occupancy = (1 + (1 - 2 * flip_probability) ** steps) / 2
        token_ok &= (
            0 < survival < 1
            and 0 < exit_probability < 1
            and survival <= endpoint_occupancy < 1
            and (survival == endpoint_occupancy) == (steps == 1)
        )
        token_fixtures.append(
            {
                "steps": steps,
                "survival_probability": qtext(survival),
                "exit_probability": qtext(exit_probability),
                "endpoint_selected_occupancy": qtext(endpoint_occupancy),
            }
        )
    token_ok &= token_fixtures[-1]["exit_probability"] != token_fixtures[0]["exit_probability"]
    record(
        "exact_discrete_token_flip_persistence_loss",
        token_ok,
        {"per_step_flip_probability": qtext(flip_probability), "fixtures": token_fixtures},
    )

    finite_path_ok = True
    finite_path_fixtures = []
    u0 = Q(9, 4)
    a_star_sq = Q(4)
    previous = None
    for n in (0, 1, 2, 10, 100, 1000):
        u_n = fixed_squared_flow(u0, gamma, Q(n))
        b2 = barrier_squared(u_n, a_star_sq)
        expected = Q(1, 1) / (1 + a_star_sq / u0 + 2 * gamma * a_star_sq * n)
        finite_path_ok &= u_n > 0 and b2 == expected
        if previous is not None:
            finite_path_ok &= b2 < previous
        previous = b2
        finite_path_fixtures.append(
            {"n": n, "u_n": qtext(u_n), "barrier_squared": qtext(b2)}
        )
    record(
        "finite_positive_but_asymptotically_zero_barrier",
        finite_path_ok,
        {"fixtures": finite_path_fixtures, "limit": "0"},
    )

    boundary_ok = (
        field(Q(0), 1, -epsilon, gamma) == -epsilon
        and field(Q(0), 1, Q(0), gamma) == 0
        and field(Q(0), 1, epsilon, gamma) == epsilon
        and field(Q(0), -1, -epsilon, gamma) == epsilon
        and field(Q(0), -1, epsilon, gamma) == -epsilon
    )
    record(
        "boundary_margin_trichotomy",
        boundary_ok,
        {
            "mu_negative": "outward and nonviable",
            "mu_zero": "exact tangency without open robustness margin",
            "mu_positive": "strictly inward and locally robust",
        },
    )

    passed = sum(1 for item in checks if item["passed"])
    return {
        "schema_id": "v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_model_v1",
        "arithmetic": "fractions.Fraction exact rational controls",
        "check_count": len(checks),
        "passed_check_count": passed,
        "failed_check_count": len(checks) - passed,
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_model()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['status']}: {result['passed_check_count']}/{result['check_count']} checks")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
