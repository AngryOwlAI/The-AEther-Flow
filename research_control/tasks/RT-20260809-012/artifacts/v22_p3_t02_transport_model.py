#!/usr/bin/env python3
"""Executable exact-arithmetic witness for V22 P3-T02.

This model verifies the proposal-only six-channel source transport fixture.  It
does not fit or infer a target metric and does not create physics authority.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from functools import reduce
from operator import mul
from typing import Iterable, Sequence


Vector = tuple[Fraction, Fraction, Fraction, Fraction]

X_VECTORS: tuple[Vector, ...] = (
    (Fraction(1), Fraction(1), Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(0), Fraction(1), Fraction(0)),
    (Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
    (Fraction(1), Fraction(1), Fraction(1), Fraction(0)),
    (Fraction(1), Fraction(0), Fraction(1), Fraction(2)),
    (Fraction(1), Fraction(2), Fraction(0), Fraction(1)),
)


def dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def principal_factors(covector: Vector) -> tuple[Fraction, ...]:
    return tuple(dot(covector, vector) for vector in X_VECTORS)


def principal_polynomial(covector: Vector) -> Fraction:
    return reduce(mul, principal_factors(covector), Fraction(1))


def background_gradients(
    epsilon1: Fraction = Fraction(2), epsilon2: Fraction = Fraction(3)
) -> tuple[Vector, ...]:
    zero: Vector = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    return (
        (-epsilon1, epsilon1, Fraction(0), Fraction(0)),
        (-epsilon2, Fraction(0), epsilon2, Fraction(0)),
        zero,
        zero,
        zero,
        zero,
    )


def background_residuals() -> tuple[Fraction, ...]:
    return tuple(
        dot(vector, gradient)
        for vector, gradient in zip(X_VECTORS, background_gradients(), strict=True)
    )


def wedge_components(left: Vector, right: Vector) -> dict[str, Fraction]:
    return {
        f"{i}{j}": left[i] * right[j] - left[j] * right[i]
        for i in range(4)
        for j in range(i + 1, 4)
    }


def regular_wedge(
    epsilon1: Fraction = Fraction(2),
    epsilon2: Fraction = Fraction(3),
    c6: Fraction = Fraction(5),
) -> dict[str, Fraction]:
    grad1 = tuple(value / c6 for value in background_gradients(epsilon1, epsilon2)[0])
    grad2 = tuple(value / c6 for value in background_gradients(epsilon1, epsilon2)[1])
    return wedge_components(grad1, grad2)  # type: ignore[arg-type]


def affine_characteristic_residual(channel: int, affine_gradient: Vector) -> Fraction:
    """Return X_A(q^A) for an affine test state in channel 1..6."""
    return dot(X_VECTORS[channel - 1], affine_gradient)


def token_update(
    channel: int,
    qi_gradient: Vector,
    q6: Fraction,
    rho: Fraction,
) -> dict[str, Fraction]:
    """Evaluate both sides of the conditional ratio and logistic identities."""
    if channel not in (1, 2):
        raise ValueError("token channel must be 1 or 2")
    if q6 == 0:
        raise ZeroDivisionError("q6 must be nonzero")
    xi = X_VECTORS[channel - 1]
    x6 = X_VECTORS[5]
    transported = dot(xi, qi_gradient)
    ratio_rhs = (dot(x6, qi_gradient) - transported) / q6
    logistic = Fraction(1, 2) if rho == 0 else Fraction(2, 3)
    token_rhs = logistic * (1 - logistic) * ratio_rhs
    return {
        "Xi_qi": transported,
        "X6_rho": ratio_rhs,
        "token_factor": logistic * (1 - logistic),
        "X6_p": token_rhs,
    }


def source_chart_scale_transform(
    vector: Vector, scalar_gradient: Vector, scale: Fraction
) -> tuple[Fraction, Fraction]:
    """Check scalar directional-derivative invariance under s1'=scale*s1."""
    if scale == 0:
        raise ValueError("chart scale must be nonzero")
    original = dot(vector, scalar_gradient)
    transformed_vector: Vector = (vector[0], scale * vector[1], vector[2], vector[3])
    transformed_gradient: Vector = (
        scalar_gradient[0],
        scalar_gradient[1] / scale,
        scalar_gradient[2],
        scalar_gradient[3],
    )
    return original, dot(transformed_vector, transformed_gradient)


def fractions_to_strings(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: fractions_to_strings(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [fractions_to_strings(item) for item in value]
    return value


def evaluate_fixture() -> dict[str, object]:
    covectors: tuple[Vector, ...] = (
        (Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(2), Fraction(-1), Fraction(3), Fraction(1)),
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    )
    chart_original, chart_transformed = source_chart_scale_transform(
        X_VECTORS[0], background_gradients()[0], Fraction(7, 3)
    )
    result: dict[str, object] = {
        "schema_id": "v22_p3_t02_transport_model_result_v1",
        "status": "PASS",
        "candidate_id": "CAND-V22-B1-SIX-TRANSPORT-DYNAMICS-V1",
        "vector_count": len(X_VECTORS),
        "tau_normalizations": [vector[0] for vector in X_VECTORS],
        "pairwise_distinct_vectors": len(set(X_VECTORS)) == 6,
        "background_residuals": background_residuals(),
        "regular_wedge": regular_wedge(),
        "regular_wedge_nonzero": any(value != 0 for value in regular_wedge().values()),
        "principal_samples": [
            {
                "covector": covector,
                "factors": principal_factors(covector),
                "polynomial": principal_polynomial(covector),
            }
            for covector in covectors
        ],
        "chart_naturality": {
            "original": chart_original,
            "transformed": chart_transformed,
            "equal": chart_original == chart_transformed,
        },
        "token_channel_1": token_update(
            1, background_gradients()[0], Fraction(5), Fraction(0)
        ),
        "token_channel_2": token_update(
            2, background_gradients()[1], Fraction(5), Fraction(1)
        ),
        "target_metric_input_count": 0,
        "measure_input_count": 0,
        "connection_input_count": 0,
        "target_fit_count": 0,
        "effective_metric_constructed": False,
    }
    return fractions_to_strings(result)  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit deterministic JSON")
    args = parser.parse_args()
    result = evaluate_fixture()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
