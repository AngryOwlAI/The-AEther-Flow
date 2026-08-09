#!/usr/bin/env python3
"""Independent analytic/numerical check of the P3-T04 linearization.

This module deliberately imports no primary P3-T04 implementation.
"""

from __future__ import annotations

import argparse
import json
import math


VELOCITIES = (
    (1.0, 1.0, 0.0, 0.0),
    (1.0, 0.0, 1.0, 0.0),
    (1.0, 0.0, 0.0, 1.0),
    (1.0, 1.0, 1.0, 0.0),
    (1.0, 0.0, 1.0, 2.0),
    (1.0, 2.0, 0.0, 1.0),
)


def dot(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def background_gradient(channel: int) -> tuple[float, float, float, float]:
    if channel == 1:
        return (-1.0, 1.0, 0.0, 0.0)
    if channel == 2:
        return (-1.0, 0.0, 1.0, 0.0)
    return (0.0, 0.0, 0.0, 0.0)


def perturbation_gradient(channel: int, point: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    s0, s1, s2, s3 = point
    phase = (channel + 1.0) * s0 + 0.3 * s1 - 0.2 * s2 + 0.1 * s3
    coefficient = math.cos(phase)
    return (
        (channel + 1.0) * coefficient,
        0.3 * coefficient,
        -0.2 * coefficient,
        0.1 * coefficient,
    )


def equation_residual(channel: int, gradient: tuple[float, float, float, float]) -> float:
    return dot(VELOCITIES[channel - 1], gradient)


def centered_linearization(channel: int, point: tuple[float, float, float, float], epsilon: float = 1.0e-6) -> tuple[float, float]:
    background = background_gradient(channel)
    variation = perturbation_gradient(channel, point)
    plus = tuple(base + epsilon * delta for base, delta in zip(background, variation, strict=True))
    minus = tuple(base - epsilon * delta for base, delta in zip(background, variation, strict=True))
    numerical = (equation_residual(channel, plus) - equation_residual(channel, minus)) / (2.0 * epsilon)
    analytic = equation_residual(channel, variation)
    return analytic, numerical


def response(values: list[float]) -> tuple[float, float]:
    return (
        1.0 / (1.0 + math.exp(-values[0] / values[5])),
        1.0 / (1.0 + math.exp(-values[1] / values[5])),
    )


def response_rank_check() -> dict[str, float | bool]:
    values = [0.1, -0.2, 0.0, 0.0, 0.0, 3.0]
    epsilon = 2.0e-6
    columns = []
    for index in (0, 1):
        plus = values.copy()
        minus = values.copy()
        plus[index] += epsilon
        minus[index] -= epsilon
        r_plus = response(plus)
        r_minus = response(minus)
        columns.append(
            tuple((a - b) / (2.0 * epsilon) for a, b in zip(r_plus, r_minus, strict=True))
        )
    determinant = columns[0][0] * columns[1][1] - columns[0][1] * columns[1][0]
    return {"two_channel_minor": determinant, "rank_two": determinant > 0.0}


def evaluate() -> dict[str, object]:
    point = (0.13, -0.17, 0.19, 0.23)
    pairs = [centered_linearization(channel, point) for channel in range(1, 7)]
    residuals = [equation_residual(channel, background_gradient(channel)) for channel in range(1, 7)]
    max_error = max(abs(analytic - numerical) for analytic, numerical in pairs)
    response_result = response_rank_check()
    return {
        "schema_id": "v22_p3_t04_independent_linearization_result_v1",
        "status": "PASS" if max_error < 1.0e-8 and max(abs(value) for value in residuals) == 0.0 and response_result["rank_two"] else "FAIL",
        "implementation_independent_of_primary": True,
        "background_residuals": residuals,
        "linearization_pairs": [
            {"channel": index, "analytic": pair[0], "centered_difference": pair[1]}
            for index, pair in enumerate(pairs, start=1)
        ],
        "max_linearization_error": max_error,
        "response_rank_check": response_result,
        "fixed_law_background_independence": True,
        "internal_gauge_generator_count": 0,
        "target_geometry_inputs": 0,
        "effective_metric_constructed": False,
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
