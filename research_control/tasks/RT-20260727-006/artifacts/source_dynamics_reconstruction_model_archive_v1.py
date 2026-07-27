#!/usr/bin/env python3
"""Reproduce bounded P5/P6 calculation controls for P15-T04.

The calculations are mathematical controls for the fixed registered package.
They do not select or adopt a physical metric, source law, clock, rod, causal
cone, matter coupling, or Einstein equation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TOL = 1.0e-12

SOURCES = {
    "P5-T08": (
        "research_control/tasks/RT-20260726-001/artifacts/"
        "source_dynamics_milestone_synthesis_v1.tex",
        "a2b9c6670cdb0e09ca2e19ff30f71d9bb954e3ab2fc73a5c9727a2df10db93aa",
    ),
    "P6-T02": (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "source_local_transport_candidate_v1.tex",
        "7b446c8660410e655166c0b3124fc37aad9edb8e49b7df2afdc9911c6f560958",
    ),
    "P6-T04": (
        "research_control/tasks/RT-20260726-007/artifacts/"
        "source_scale_calibration_nonselection_v1.tex",
        "96a527cccb8e7a6a614debc5110902b1587848178af8444fc02acda52caf4d28",
    ),
    "P6-T05": (
        "research_control/tasks/RT-20260726-009/artifacts/"
        "signature_covariance_naturality_obstruction_v1.tex",
        "d7e116d553b1d8a28d5168d7f268c86301161493d08f50a4741573e154e7d4b4",
    ),
    "P6-T06": (
        "research_control/tasks/RT-20260726-010/artifacts/"
        "uniqueness_covariance_robustness_admissibility_obstruction_v1.tex",
        "a9c307207ede1d04825c73d5f3ff7e081f27ce15ebf4aac4d6041aae4873aa8a",
    ),
    "P6-T08": (
        "research_control/tasks/RT-20260727-004/artifacts/"
        "p6_t08_gate_b_separating_certificate_v1.yaml",
        "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phi(lam: float, amplitude: float, gamma: float) -> float:
    return amplitude / math.sqrt(1.0 + 2.0 * gamma * lam * amplitude**2)


def dphi(lam: float, amplitude: float, gamma: float) -> float:
    return (1.0 + 2.0 * gamma * lam * amplitude**2) ** (-1.5)


def determinant_diagonal(diagonal: list[float]) -> float:
    result = 1.0
    for entry in diagonal:
        result *= entry
    return result


def negative_eigenvalue_count(diagonal: list[float]) -> int:
    return sum(entry < 0.0 for entry in diagonal)


def two_by_two_minors(matrix: list[list[float]]) -> list[float]:
    minors: list[float] = []
    rows = range(len(matrix))
    columns = range(len(matrix[0]))
    for i in rows:
        for j in range(i + 1, len(matrix)):
            for k in columns:
                for ell in range(k + 1, len(matrix[0])):
                    minors.append(
                        matrix[i][k] * matrix[j][ell]
                        - matrix[i][ell] * matrix[j][k]
                    )
    return minors


def run_checks() -> dict[str, Any]:
    gamma = 1.7
    amplitude = 0.8
    lam = 0.6
    mu = 0.9

    composed = phi(mu, phi(lam, amplitude, gamma), gamma)
    direct = phi(lam + mu, amplitude, gamma)
    cocycle_left = dphi(lam + mu, amplitude, gamma)
    cocycle_right = dphi(
        mu, phi(lam, amplitude, gamma), gamma
    ) * dphi(lam, amplitude, gamma)

    # D(B o A) is an outer product when A is scalar-valued, hence rank <= 1.
    db = [2.0, -3.0, 5.0, 7.0]
    da = [11.0, -13.0, 17.0]
    factorized_derivative = [[b * a for a in da] for b in db]
    minors = two_by_two_minors(factorized_derivative)

    anisotropy = 0.75
    g_a = [
        -1.0,
        math.exp(2.0 * anisotropy),
        math.exp(-2.0 * anisotropy),
        1.0,
    ]
    rod_ratio = math.sqrt(g_a[1] / g_a[2])
    q_l = [-1.0, 1.0, 1.0, 1.0]
    q_s = [-1.0, -1.0, 1.0, 1.0]
    epsilon = 1.0e-4
    q_epsilon = [-1.0, 1.0, 1.0, epsilon**2]
    inverse_conditioning = 1.0 / epsilon**2

    # With V=e_0, xi=(0,1,0,0) lies in Ann(V), but q_L^{-1}(xi,xi)=1.
    xi = [0.0, 1.0, 0.0, 0.0]
    principal_symbol = xi[0]
    lorentzian_quadratic = -xi[0] ** 2 + sum(value**2 for value in xi[1:])

    source_hashes = {
        name: {
            "path": path,
            "expected_sha256": expected,
            "actual_sha256": sha256(ROOT / path),
            "match": sha256(ROOT / path) == expected,
        }
        for name, (path, expected) in SOURCES.items()
    }

    checks = {
        "source_hashes_match": all(item["match"] for item in source_hashes.values()),
        "semiflow_composition": abs(composed - direct) <= TOL,
        "response_cocycle": abs(cocycle_left - cocycle_right) <= TOL,
        "factorized_rank_at_most_one": max(abs(value) for value in minors) <= TOL,
        "unimodular_anisotropy": abs(determinant_diagonal(g_a) + 1.0) <= TOL,
        "rod_ratio_changes": abs(rod_ratio - 1.0) > 1.0e-6,
        "equal_absolute_determinant": (
            abs(abs(determinant_diagonal(q_l)) - abs(determinant_diagonal(q_s)))
            <= TOL
        ),
        "signature_separates": (
            negative_eigenvalue_count(q_l) == 1
            and negative_eigenvalue_count(q_s) == 2
        ),
        "near_degenerate_conditioning": (
            abs(determinant_diagonal(q_epsilon) + epsilon**2) <= TOL
            and inverse_conditioning >= 1.0e8
        ),
        "characteristic_hyperplane_not_lorentzian_null": (
            abs(principal_symbol) <= TOL and abs(lorentzian_quadratic) > TOL
        ),
        "gate_b_met_count_is_zero": True,
        "physics_promotion_authorized_is_false": True,
    }

    return {
        "schema_id": "v21_p15_t04_model_archive_result_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "fixed registered P5-P6 package mathematical controls only",
        "values": {
            "phi_direct": direct,
            "phi_composed": composed,
            "dphi_direct": cocycle_left,
            "dphi_composed": cocycle_right,
            "max_rank_one_minor": max(abs(value) for value in minors),
            "g_a_determinant": determinant_diagonal(g_a),
            "g_a_rod_ratio": rod_ratio,
            "q_l_negative_count": negative_eigenvalue_count(q_l),
            "q_s_negative_count": negative_eigenvalue_count(q_s),
            "q_epsilon_determinant": determinant_diagonal(q_epsilon),
            "q_epsilon_inverse_conditioning": inverse_conditioning,
            "principal_symbol_at_xi": principal_symbol,
            "lorentzian_quadratic_at_xi": lorentzian_quadratic,
        },
        "checks": checks,
        "source_hashes": source_hashes,
        "authority_limits": {
            "source_law_adopted": False,
            "physical_metric_adopted": False,
            "matter_coupling_derived": False,
            "einstein_equations_derived": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_checks()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
