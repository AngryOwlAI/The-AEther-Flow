#!/usr/bin/env python3
"""Deterministic P3-T04 background and linear-response model.

All coordinates, differences, and norms in this module are source-chart
comparison data.  They are not physical lengths, clocks, cones, or a target
metric.  The fixed continuum law is the proposal-only P3-T02 six-channel
transport system.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Sequence


SpatialVelocity = tuple[int, int, int]
SourceVector = tuple[float, float, float, float]
Covector = tuple[float, float, float, float]

VELOCITIES: tuple[SpatialVelocity, ...] = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (0, 1, 2),
    (2, 0, 1),
)
SOURCE_VECTORS: tuple[SourceVector, ...] = tuple(
    (1.0, float(v[0]), float(v[1]), float(v[2])) for v in VELOCITIES
)
LEVELS: tuple[int, ...] = (24, 32, 48, 64)
FINAL_TIME = 0.05
CFL_TARGET = 0.35


def logistic(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def selected_background(point: Covector) -> tuple[float, ...]:
    """Return the predeclared affine source background at (s0,s1,s2,s3)."""
    s0, s1, s2, _ = point
    return (s1 - s0, s2 - s0, 0.0, 0.0, 0.0, 3.0)


def selected_background_gradients() -> tuple[Covector, ...]:
    return (
        (-1.0, 1.0, 0.0, 0.0),
        (-1.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    )


def pair(vector: SourceVector, covector: Covector) -> float:
    return sum(component * dual for component, dual in zip(vector, covector, strict=True))


def background_residuals() -> list[float]:
    return [
        pair(vector, gradient)
        for vector, gradient in zip(SOURCE_VECTORS, selected_background_gradients(), strict=True)
    ]


def response(values: Sequence[float]) -> tuple[float, float]:
    q6 = values[5]
    if q6 == 0.0:
        raise ValueError("q6 must be nonzero")
    return logistic(values[0] / q6), logistic(values[1] / q6)


def analytic_response_jacobian(values: Sequence[float]) -> list[list[float]]:
    q1, q2, _, _, _, q6 = values
    if q6 == 0.0:
        raise ValueError("q6 must be nonzero")
    p1, p2 = response(values)
    d1 = p1 * (1.0 - p1)
    d2 = p2 * (1.0 - p2)
    return [
        [d1 / q6, 0.0, 0.0, 0.0, 0.0, -d1 * q1 / (q6 * q6)],
        [0.0, d2 / q6, 0.0, 0.0, 0.0, -d2 * q2 / (q6 * q6)],
    ]


def numerical_response_jacobian(values: Sequence[float], epsilon: float = 1.0e-6) -> list[list[float]]:
    columns: list[tuple[float, float]] = []
    for index in range(6):
        plus = list(values)
        minus = list(values)
        plus[index] += epsilon
        minus[index] -= epsilon
        r_plus = response(plus)
        r_minus = response(minus)
        columns.append(
            (
                (r_plus[0] - r_minus[0]) / (2.0 * epsilon),
                (r_plus[1] - r_minus[1]) / (2.0 * epsilon),
            )
        )
    return [[columns[column][row] for column in range(6)] for row in range(2)]


def jacobian_max_error(analytic: Sequence[Sequence[float]], numerical: Sequence[Sequence[float]]) -> float:
    return max(
        abs(left - right)
        for analytic_row, numerical_row in zip(analytic, numerical, strict=True)
        for left, right in zip(analytic_row, numerical_row, strict=True)
    )


def perturbation_value(channel: int, x: float) -> float:
    amplitude = 1.0 + 0.05 * channel
    return amplitude * math.sin(2.0 * math.pi * x) + 0.15 * math.cos(4.0 * math.pi * x)


def perturbation_derivative(channel: int, x: float) -> float:
    amplitude = 1.0 + 0.05 * channel
    return amplitude * 2.0 * math.pi * math.cos(2.0 * math.pi * x) - 0.6 * math.pi * math.sin(4.0 * math.pi * x)


def upwind_step(state: Sequence[float], cfl: float) -> list[float]:
    return [
        (1.0 - cfl) * state[index] + cfl * state[(index - 1) % len(state)]
        for index in range(len(state))
    ]


def channel_parity(level: int, channel: int) -> dict[str, float | int]:
    speed = sum(VELOCITIES[channel - 1])
    h = 1.0 / level
    steps = max(1, math.ceil(FINAL_TIME * speed / (CFL_TARGET * h)))
    dt = FINAL_TIME / steps
    cfl = dt * speed / h
    state = [perturbation_value(channel, index * h) for index in range(level)]
    for _ in range(steps):
        state = upwind_step(state, cfl)
    exact = [
        perturbation_value(channel, (index * h - speed * FINAL_TIME) % 1.0)
        for index in range(level)
    ]
    exact_derivative = [
        perturbation_derivative(channel, (index * h - speed * FINAL_TIME) % 1.0)
        for index in range(level)
    ]
    discrete_derivative = [
        (state[index] - state[(index - 1) % level]) / h for index in range(level)
    ]
    return {
        "channel": channel,
        "effective_source_speed": speed,
        "n": level,
        "h": h,
        "dt": dt,
        "steps": steps,
        "cfl": cfl,
        "value_error": max(abs(value - reference) for value, reference in zip(state, exact, strict=True)),
        "c1_difference_error": max(
            abs(value - reference)
            for value, reference in zip(discrete_derivative, exact_derivative, strict=True)
        ),
    }


def parity_study() -> dict[str, object]:
    levels: list[dict[str, object]] = []
    for level in LEVELS:
        channels = [channel_parity(level, channel) for channel in range(1, 7)]
        levels.append(
            {
                "n": level,
                "h": 1.0 / level,
                "max_value_error": max(float(item["value_error"]) for item in channels),
                "max_c1_difference_error": max(float(item["c1_difference_error"]) for item in channels),
                "max_cfl": max(float(item["cfl"]) for item in channels),
                "channels": channels,
            }
        )
    value_orders = [
        math.log(float(coarse["max_value_error"]) / float(fine["max_value_error"]))
        / math.log(float(coarse["h"]) / float(fine["h"]))
        for coarse, fine in zip(levels, levels[1:])
    ]
    c1_orders = [
        math.log(float(coarse["max_c1_difference_error"]) / float(fine["max_c1_difference_error"]))
        / math.log(float(coarse["h"]) / float(fine["h"]))
        for coarse, fine in zip(levels, levels[1:])
    ]
    return {
        "levels": levels,
        "value_orders": value_orders,
        "c1_orders": c1_orders,
        "value_errors_strictly_decrease": all(
            float(coarse["max_value_error"]) > float(fine["max_value_error"])
            for coarse, fine in zip(levels, levels[1:])
        ),
        "c1_errors_strictly_decrease": all(
            float(coarse["max_c1_difference_error"]) > float(fine["max_c1_difference_error"])
            for coarse, fine in zip(levels, levels[1:])
        ),
    }


def transform_vector(vector: SourceVector) -> SourceVector:
    time, x, y, z = vector
    return (time, x + y, y, z)


def transform_covector(covector: Covector) -> Covector:
    time, x, y, z = covector
    return (time, x, y - x, z)


def representation_parity() -> dict[str, object]:
    covector: Covector = (2.0, -1.0, 3.0, 1.0)
    original = [pair(vector, covector) for vector in SOURCE_VECTORS]
    transformed = [
        pair(transform_vector(vector), transform_covector(covector))
        for vector in SOURCE_VECTORS
    ]
    rho1: Covector = (-1.0 / 3.0, 1.0 / 3.0, 0.0, 0.0)
    rho2: Covector = (-1.0 / 3.0, 0.0, 1.0 / 3.0, 0.0)
    transformed_rho1 = transform_covector(rho1)
    transformed_rho2 = transform_covector(rho2)
    original_minor = rho1[1] * rho2[2] - rho1[2] * rho2[1]
    transformed_minor = (
        transformed_rho1[1] * transformed_rho2[2]
        - transformed_rho1[2] * transformed_rho2[1]
    )
    return {
        "chart_map": "s0'=s0, s1'=s1+s2, s2'=s2, s3'=s3",
        "principal_pairings_original": original,
        "principal_pairings_transformed": transformed,
        "max_pairing_difference": max(abs(left - right) for left, right in zip(original, transformed, strict=True)),
        "rank_minor_original": original_minor,
        "rank_minor_transformed": transformed_minor,
        "passive_representation_only": True,
        "physical_gauge_inferred": False,
    }


def principal_polynomial(covector: Covector) -> float:
    return math.prod(pair(vector, covector) for vector in SOURCE_VECTORS)


def coupled_counterfamily_polynomial(covector: Covector, parameter: float = 1.0) -> float:
    first = pair(SOURCE_VECTORS[0], covector)
    second = pair(SOURCE_VECTORS[1], covector)
    z_vector = tuple(
        left - right for left, right in zip(SOURCE_VECTORS[0], SOURCE_VECTORS[1], strict=True)
    )
    z_factor = pair(z_vector, covector)  # type: ignore[arg-type]
    return (first * second - parameter * parameter * z_factor * z_factor) * math.prod(
        pair(vector, covector) for vector in SOURCE_VECTORS[2:]
    )


def counterfamily_study() -> dict[str, object]:
    base_zero_covector: Covector = (0.0, 0.0, 1.0, 1.0)
    golden = (math.sqrt(5.0) - 1.0) / 2.0
    coupled_zero_covector: Covector = (golden, 1.0, 0.0, 1.0)
    cases = []
    for case_id, covector in (
        ("base_zero_coupled_nonzero", base_zero_covector),
        ("coupled_zero_base_nonzero", coupled_zero_covector),
    ):
        cases.append(
            {
                "case_id": case_id,
                "covector": list(covector),
                "base_polynomial": principal_polynomial(covector),
                "coupled_polynomial": coupled_counterfamily_polynomial(covector),
            }
        )
    return {
        "family": "E_1^lambda=X_1q1+lambda*Z(q2-qbar2); E_2^lambda=X_2q2+lambda*Z(q1-qbar1), Z=X_1-X_2",
        "selected_background_preserved": True,
        "source_only_inputs": True,
        "changes_sealed_source_law": True,
        "inside_fixed_candidate_identity": False,
        "physical_inequivalence_claimed": False,
        "principal_zero_sets_differ": (
            abs(float(cases[0]["base_polynomial"])) < 1.0e-12
            and abs(float(cases[0]["coupled_polynomial"])) > 1.0e-8
            and abs(float(cases[1]["coupled_polynomial"])) < 1.0e-8
            and abs(float(cases[1]["base_polynomial"])) > 1.0e-8
        ),
        "cases": cases,
        "disposition": "source-law-selection debt outside the fixed P3-T02 candidate; blocks uniqueness overread but does not refute fixed-law linearization readiness",
    }


def evaluate() -> dict[str, object]:
    point: Covector = (0.1, 0.2, -0.1, 0.05)
    background = selected_background(point)
    analytic = analytic_response_jacobian(background)
    numerical = numerical_response_jacobian(background)
    parity = parity_study()
    representation = representation_parity()
    counterfamily = counterfamily_study()
    two_by_two_minor = analytic[0][0] * analytic[1][1] - analytic[0][1] * analytic[1][0]
    checks = {
        "background_residuals_zero": max(abs(value) for value in background_residuals()) == 0.0,
        "q6_positive_margin": background[5] == 3.0,
        "response_rank_two": two_by_two_minor > 0.0,
        "response_jacobian_numeric_match": jacobian_max_error(analytic, numerical) < 1.0e-9,
        "value_parity_decreases": parity["value_errors_strictly_decrease"] is True,
        "c1_parity_decreases": parity["c1_errors_strictly_decrease"] is True,
        "source_cfl_respected": max(float(level["max_cfl"]) for level in parity["levels"]) <= CFL_TARGET + 1.0e-12,
        "passive_pairings_invariant": representation["max_pairing_difference"] < 1.0e-12,
        "rank_minor_invariant": abs(float(representation["rank_minor_original"]) - float(representation["rank_minor_transformed"])) < 1.0e-12,
        "counterfamily_zero_sets_differ": counterfamily["principal_zero_sets_differ"] is True,
    }
    return {
        "schema_id": "v22_p3_t04_linear_response_model_result_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "selected_background": {
            "point": list(point),
            "values": list(background),
            "equation_residuals": background_residuals(),
            "rho_gradient_wedge_minor_s1_s2": 1.0 / 9.0,
            "selection_rule": "lexicographically fixed rational affine member of the P3-T02 regular solution class, chosen before target access",
        },
        "linearization": {
            "rule": "L_D u=(X_1u1,...,X_6u6)",
            "background_independent": True,
            "frechet_smoothness": "affine-linear C-infinity map from C2 source sections to C1 residuals for fixed D",
            "field_constraint_count": 0,
            "internal_gauge_generator_count": 0,
        },
        "response": {
            "map": "q -> (logistic(q1/q6), logistic(q2/q6))",
            "analytic_jacobian": analytic,
            "numerical_jacobian": numerical,
            "jacobian_max_error": jacobian_max_error(analytic, numerical),
            "rank_two_minor": two_by_two_minor,
            "adequacy_verdict": "necessary_condition_met_not_sufficient",
            "physical_geometry_typing_complete": False,
        },
        "finite_continuum_parity": parity,
        "representation_parity": representation,
        "counterfamily": counterfamily,
        "checks": checks,
        "source_purity": {
            "target_atlas_input_count": 0,
            "target_metric_input_count": 0,
            "target_fit_count": 0,
            "physical_clock_input_count": 0,
            "physical_gauge_assumed": False,
            "effective_metric_constructed": False,
        },
        "authority": {
            "candidate_law_adopted": False,
            "physical_cone_constructed": False,
            "lorentzian_signature_constructed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
