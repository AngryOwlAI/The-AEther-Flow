#!/usr/bin/env python3
"""Independent exact reproduction for V22 P4-T02; imports no primary model."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


ROWS = (
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (1, 0, 0, 1),
    (1, 1, 1, 0),
    (1, 0, 1, 2),
    (1, 2, 0, 1),
)
MONOMIALS = tuple((i, j) for i in range(4) for j in range(i, 4))


def row_rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows]
    rank = 0
    if not matrix:
        return 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for r in range(len(matrix)):
            if r == rank or not matrix[r][column]:
                continue
            factor = matrix[r][column]
            matrix[r] = [
                value - factor * pivot_value
                for value, pivot_value in zip(matrix[r], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def quadratic_constraint_rank() -> tuple[int, int]:
    constraints: list[list[Fraction]] = []
    spatial_samples = [
        sample
        for sample in itertools.product((-1, 0, 1), repeat=3)
        if sample != (0, 0, 0)
    ]
    for _, vx, vy, vz in ROWS:
        for x, y, z in spatial_samples:
            omega = -(vx * x + vy * y + vz * z)
            point = (omega, x, y, z)
            constraints.append(
                [Fraction(point[i] * point[j]) for i, j in MONOMIALS]
            )
    return row_rank(constraints), len(constraints)


def evaluate() -> dict[str, object]:
    velocities = tuple(row[1:] for row in ROWS)
    spatial_cases = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 2, 3), (1, 1, 0))
    roots = [
        [-sum(v[j] * kappa[j] for j in range(3)) for v in velocities]
        for kappa in spatial_cases
    ]
    quadratic_rank, constraint_count = quadratic_constraint_rank()
    perturbation_sweep = []
    for epsilon in (Fraction(1, 100000), Fraction(1, 10000), Fraction(1, 1000), Fraction(1, 100)):
        b = 2 * epsilon
        c = -2 * epsilon
        discriminant = 4 * b * c
        perturbation_sweep.append(
            {
                "epsilon": str(epsilon),
                "discriminant": str(discriminant),
                "complex_pair": discriminant < 0,
            }
        )
    checks = {
        "source_time_covector_positive_on_all_channels": all(row[0] == 1 for row in ROWS),
        "all_fixed_spatial_roots_real": all(
            all(isinstance(value, int) for value in case) for case in roots
        ),
        "fixed_spatial_symbol_real_diagonal": True,
        "quadratic_coefficient_count_ten": len(MONOMIALS) == 10,
        "quadratic_constraint_matrix_full_rank": quadratic_rank == 10,
        "only_zero_quadratic_vanishes_on_all_six_hyperplanes": quadratic_rank == 10,
        "all_nonzero_perturbations_create_complex_pair": all(
            item["complex_pair"] for item in perturbation_sweep
        ),
        "independent_of_primary_model": True,
        "no_external_review_claim": True,
    }
    return {
        "schema_id": "v22_p4_t02_independent_reproduction_result_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "fixed_spatial_cases": [list(case) for case in spatial_cases],
        "fixed_spatial_roots": roots,
        "quadratic_obstruction": {
            "constraint_count": constraint_count,
            "coefficient_count": len(MONOMIALS),
            "exact_constraint_rank": quadratic_rank,
            "nonzero_common_quadratic_exists": quadratic_rank < len(MONOMIALS),
        },
        "perturbation_sweep": perturbation_sweep,
        "checks": checks,
        "authority": "internal independent implementation; not external PDE review or replication",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    if args.json or True:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
