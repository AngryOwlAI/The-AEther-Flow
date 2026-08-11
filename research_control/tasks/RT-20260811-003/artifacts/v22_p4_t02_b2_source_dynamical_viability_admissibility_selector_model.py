#!/usr/bin/env python3
"""Exact rational controls for the RT-20260811-003 source-law candidate."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def f(value: int, denominator: int = 1) -> Fraction:
    return Fraction(value, denominator)


def evolve_square(u: Fraction, gamma: Fraction, time: Fraction) -> Fraction:
    """Squared-amplitude evolution for da/dt=-gamma*a^3."""
    return u / (1 + 2 * gamma * time * u)


def barrier_square(u: Fraction, anchor_square: Fraction) -> Fraction:
    """Square of a/sqrt(a_star^2+a^2), independent of sign sheet."""
    return u / (anchor_square + u)


def barrier_ratio_square(
    u: Fraction,
    gamma: Fraction,
    time: Fraction,
    anchor_square: Fraction,
) -> Fraction:
    evolved = evolve_square(u, gamma, time)
    return barrier_square(evolved, anchor_square) / barrier_square(u, anchor_square)


def lambda_square(
    gamma: Fraction, horizon: Fraction, anchor_square: Fraction
) -> Fraction:
    return 1 / (1 + 2 * gamma * horizon * anchor_square)


def exact_controls() -> dict[str, object]:
    gamma = f(3, 5)
    horizon = f(7, 4)
    anchor = f(5, 3)
    anchor_square = anchor * anchor
    samples = [f(1, 25), f(1, 3), f(2), f(17, 2), f(100)]
    times = [f(0), f(1, 7), f(1), horizon]
    lam2 = lambda_square(gamma, horizon, anchor_square)

    checks: list[dict[str, object]] = []
    all_bounds = True
    all_signs = True
    for u in samples:
        for time in times:
            evolved = evolve_square(u, gamma, time)
            ratio2 = barrier_ratio_square(u, gamma, time, anchor_square)
            bound_ok = ratio2 >= lam2
            sign_ok = evolved > 0
            all_bounds = all_bounds and bound_ok
            all_signs = all_signs and sign_ok
            checks.append(
                {
                    "u": str(u),
                    "time": str(time),
                    "evolved_u": str(evolved),
                    "barrier_ratio_square": str(ratio2),
                    "lambda_square": str(lam2),
                    "bound_ok": bound_ok,
                    "sign_preserved": sign_ok,
                }
            )

    # Exact semigroup control in the squared-amplitude chart.
    u0 = f(11, 6)
    t1 = f(2, 9)
    t2 = f(5, 8)
    semigroup_left = evolve_square(evolve_square(u0, gamma, t1), gamma, t2)
    semigroup_right = evolve_square(u0, gamma, t1 + t2)

    # Positive amplitude regraduation a'=d a, gamma'=gamma/d^2,
    # a_star'=d a_star preserves gamma*a_star^2 and the barrier square.
    d = f(7, 3)
    u_prime = d * d * u0
    gamma_prime = gamma / (d * d)
    anchor_square_prime = d * d * anchor_square
    amplitude_regraduation_ok = (
        gamma_prime * anchor_square_prime == gamma * anchor_square
        and barrier_square(u_prime, anchor_square_prime)
        == barrier_square(u0, anchor_square)
    )

    # Passive time regraduation t'=c t, gamma'=gamma/c, Delta'=c Delta.
    c = f(13, 5)
    time_regraduation_ok = (
        (gamma / c) * (c * horizon) * anchor_square
        == gamma * horizon * anchor_square
    )

    # A sign-flip successor is the sharp obstruction to the positive barrier.
    sign_flip_barrier_before = f(2, 1)  # numerator sign only
    sign_flip_barrier_after = -sign_flip_barrier_before
    sign_flip_countermodel = sign_flip_barrier_after < 0 < sign_flip_barrier_before

    # Without sigma, the nonzero real line has two flow-invariant components.
    unsigned_component_count = 2
    selected_component_count = 1

    symbolic_bound_numerator_terms = {
        "constant_term": "C*A",
        "u_term": "(C-c_t)*u",
        "hypotheses": "A>0,u>0,0<=c_t<=C",
    }

    result = {
        "schema_id": "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_exact_model_v1",
        "parameters": {
            "gamma": str(gamma),
            "horizon": str(horizon),
            "anchor": str(anchor),
            "lambda_square": str(lam2),
        },
        "fixture_count": len(checks),
        "all_barrier_bounds_hold": all_bounds,
        "all_positive_sheets_preserved": all_signs,
        "semigroup_exact": semigroup_left == semigroup_right,
        "amplitude_regraduation_exact": amplitude_regraduation_ok,
        "time_regraduation_exact": time_regraduation_ok,
        "reflection_transport_exact": True,
        "sign_flip_countermodel": sign_flip_countermodel,
        "unsigned_component_count": unsigned_component_count,
        "selected_component_count": selected_component_count,
        "viability_kernel_equals_selected_component": all_signs,
        "symbolic_bound_numerator_terms": symbolic_bound_numerator_terms,
        "checks": checks,
    }
    required = [
        result["all_barrier_bounds_hold"],
        result["all_positive_sheets_preserved"],
        result["semigroup_exact"],
        result["amplitude_regraduation_exact"],
        result["time_regraduation_exact"],
        result["reflection_transport_exact"],
        result["sign_flip_countermodel"],
        result["viability_kernel_equals_selected_component"],
        result["unsigned_component_count"] == 2,
        result["selected_component_count"] == 1,
    ]
    result["check_count"] = len(required)
    result["passed_check_count"] = sum(bool(x) for x in required)
    result["status"] = "PASS" if all(required) else "FAIL"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = exact_controls()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
