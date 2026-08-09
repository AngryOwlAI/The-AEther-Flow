#!/usr/bin/env python3
"""Independent V22 P4-T01 reproduction; imports no primary model code."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import permutations
from math import prod


ROWS = (
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (1, 0, 0, 1),
    (1, 1, 1, 0),
    (1, 0, 1, 2),
    (1, 2, 0, 1),
)


def dot(row: tuple[int, ...], covector: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(row, covector, strict=True))


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def leibniz_determinant(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    return sum(
        Fraction(permutation_sign(permutation))
        * prod((matrix[row][column] for row, column in enumerate(permutation)), start=Fraction(1))
        for permutation in permutations(range(size))
    )


def diagonal_symbol(covector: tuple[int, ...]) -> list[list[Fraction]]:
    diagonal = [Fraction(dot(row, covector)) for row in ROWS]
    return [
        [diagonal[row] if row == column else Fraction() for column in range(6)]
        for row in range(6)
    ]


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    row_index = 0
    column_count = len(work[0]) if work else 0
    for column in range(column_count):
        pivot = next((index for index in range(row_index, len(work)) if work[index][column]), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        scale = work[row_index][column]
        work[row_index] = [value / scale for value in work[row_index]]
        for index in range(len(work)):
            if index == row_index or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [value - scale * pivot_value for value, pivot_value in zip(work[index], work[row_index], strict=True)]
        row_index += 1
    return row_index


def evaluate() -> dict[str, object]:
    covectors = (
        (1, 0, 0, 0),
        (2, -1, 3, 1),
        (1, 0, -1, -1),
        (0, 1, 2, 3),
        (3, 2, -2, 4),
    )
    cases = []
    for covector in covectors:
        values = tuple(dot(row, covector) for row in ROWS)
        matrix = diagonal_symbol(covector)
        determinant = leibniz_determinant(matrix)
        cases.append(
            {
                "covector": list(covector),
                "factors": list(values),
                "product": prod(values),
                "leibniz_determinant_numerator": determinant.numerator,
                "leibniz_determinant_denominator": determinant.denominator,
                "matrix_rank": rank(matrix),
                "kernel_dimension": 6 - rank(matrix),
                "parity": determinant == prod(values),
            }
        )
    transformed_rows = tuple((time, first + second, second, third) for time, first, second, third in ROWS)
    original_covector = (2, -1, 3, 1)
    transformed_covector = (2, -1, 4, 1)
    original_values = tuple(dot(row, original_covector) for row in ROWS)
    transformed_values = tuple(dot(row, transformed_covector) for row in transformed_rows)
    fourfold = next(case for case in cases if case["covector"] == [1, 0, -1, -1])
    checks = {
        "five_independent_determinants_match": all(case["parity"] for case in cases),
        "pure_source_time_rank_six": cases[0]["matrix_rank"] == 6 and cases[0]["product"] == 1,
        "fourfold_witness_rank_two": fourfold["matrix_rank"] == 2 and fourfold["kernel_dimension"] == 4,
        "passive_chart_factor_parity": original_values == transformed_values,
        "six_normalized_rows_distinct": len(set(ROWS)) == 6 and all(row[0] == 1 for row in ROWS),
    }
    return {
        "schema_id": "v22_p4_t01_independent_reproduction_result_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation_independent_of_primary": True,
        "method": "Leibniz determinant of the independently assembled six-by-six rational symbol matrix",
        "cases": cases,
        "passive_chart_case": {
            "original_covector": list(original_covector),
            "transformed_covector": list(transformed_covector),
            "original_factors": list(original_values),
            "transformed_factors": list(transformed_values),
        },
        "checks": checks,
        "target_geometry_inputs": 0,
        "metric_factor_inserted": False,
        "external_independent_review_claimed": False,
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
