#!/usr/bin/env python3
"""Exact source-principal calculations for V22 P4-T01.

Only the fixed P3-T02 six-channel transport datum is used.  The module uses
standard-library rational arithmetic and does not construct a metric.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations
from math import prod


Vector = tuple[int, int, int, int]
Exponent = tuple[int, int, int, int]
Polynomial = dict[Exponent, Fraction]

SOURCE_VECTORS: tuple[Vector, ...] = (
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (1, 0, 0, 1),
    (1, 1, 1, 0),
    (1, 0, 1, 2),
    (1, 2, 0, 1),
)


def pairing(vector: Vector, covector: Vector) -> int:
    return sum(left * right for left, right in zip(vector, covector, strict=True))


def factors(covector: Vector) -> tuple[int, ...]:
    return tuple(pairing(vector, covector) for vector in SOURCE_VECTORS)


def principal_polynomial(covector: Vector) -> int:
    return prod(factors(covector))


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exp, right_exp, strict=True))
            result[exponent] = result.get(exponent, Fraction()) + left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def expanded_polynomial() -> Polynomial:
    polynomial: Polynomial = {(0, 0, 0, 0): Fraction(1)}
    for vector in SOURCE_VECTORS:
        linear: Polynomial = {}
        for index, coefficient in enumerate(vector):
            if coefficient:
                exponent = tuple(1 if axis == index else 0 for axis in range(4))
                linear[exponent] = Fraction(coefficient)
        polynomial = multiply(polynomial, linear)
    return polynomial


def evaluate_expansion(polynomial: Polynomial, covector: Vector) -> Fraction:
    result = Fraction()
    for exponent, coefficient in polynomial.items():
        monomial = prod(Fraction(value) ** power for value, power in zip(covector, exponent, strict=True))
        result += coefficient * monomial
    return result


def matrix_rank(rows: list[Vector]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    for column in range(4):
        pivot = next((index for index in range(rank, len(matrix)) if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for index, row in enumerate(matrix):
            if index == rank or not row[column]:
                continue
            multiplier = row[column]
            matrix[index] = [value - multiplier * pivot_value for value, pivot_value in zip(row, matrix[rank], strict=True)]
        rank += 1
    return rank


def branch_rank_report() -> dict[str, object]:
    subset_reports: dict[str, list[dict[str, object]]] = {}
    for size in range(2, 7):
        reports: list[dict[str, object]] = []
        for subset in combinations(range(6), size):
            rank = matrix_rank([SOURCE_VECTORS[index] for index in subset])
            reports.append(
                {
                    "branches": [index + 1 for index in subset],
                    "rank": rank,
                    "nonzero_intersection_dimension": 4 - rank,
                }
            )
        subset_reports[str(size)] = reports
    fourfold_witness: Vector = (1, 0, -1, -1)
    witness_factors = factors(fourfold_witness)
    return {
        "pair_count": len(subset_reports["2"]),
        "pair_rank_two_count": sum(item["rank"] == 2 for item in subset_reports["2"]),
        "triple_count": len(subset_reports["3"]),
        "triple_rank_three_count": sum(item["rank"] == 3 for item in subset_reports["3"]),
        "nonzero_fourfold_subsets": [
            item for item in subset_reports["4"] if item["nonzero_intersection_dimension"] > 0
        ],
        "maximum_nonzero_corank": 4,
        "fourfold_witness": list(fourfold_witness),
        "fourfold_witness_factors": list(witness_factors),
        "fourfold_zero_branches": [index + 1 for index, value in enumerate(witness_factors) if value == 0],
        "fivefold_nonzero_intersection_count": sum(
            item["nonzero_intersection_dimension"] > 0 for item in subset_reports["5"]
        ),
        "sixfold_nonzero_intersection_count": sum(
            item["nonzero_intersection_dimension"] > 0 for item in subset_reports["6"]
        ),
    }


def transform_vector(vector: Vector) -> Vector:
    time, first, second, third = vector
    return (time, first + second, second, third)


def transform_covector(covector: Vector) -> Vector:
    time, first, second, third = covector
    return (time, first, second - first, third)


def passive_chart_report() -> dict[str, object]:
    covectors: tuple[Vector, ...] = (
        (2, -1, 3, 1),
        (1, 0, -1, -1),
        (3, 2, -2, 4),
    )
    cases = []
    for covector in covectors:
        original = factors(covector)
        transformed_covector = transform_covector(covector)
        transformed = tuple(pairing(transform_vector(vector), transformed_covector) for vector in SOURCE_VECTORS)
        cases.append(
            {
                "covector": list(covector),
                "transformed_covector": list(transformed_covector),
                "original_factors": list(original),
                "transformed_factors": list(transformed),
                "factor_parity": original == transformed,
                "polynomial_parity": prod(original) == prod(transformed),
            }
        )
    return {
        "chart_map": "s0'=s0, s1'=s1+s2, s2'=s2, s3'=s3",
        "cases": cases,
        "all_factor_pairings_invariant": all(case["factor_parity"] for case in cases),
        "all_polynomials_invariant": all(case["polynomial_parity"] for case in cases),
        "source_coordinate_density_weight": 0,
    }


def frame_covariance_report() -> dict[str, object]:
    equation_scales = (2, 3, 5, 7, 11, 13)
    field_scales = (17, 19, 23, 29, 31, 37)
    covector: Vector = (2, -1, 3, 1)
    base_factors = factors(covector)
    transformed_diagonal = tuple(
        Fraction(equation_scale * factor, field_scale)
        for equation_scale, field_scale, factor in zip(
            equation_scales, field_scales, base_factors, strict=True
        )
    )
    relative_multiplier = Fraction(prod(equation_scales), prod(field_scales))
    transformed_determinant = prod(transformed_diagonal, start=Fraction(1))
    expected = relative_multiplier * principal_polynomial(covector)
    return {
        "field_frame_scales": list(field_scales),
        "equation_frame_scales": list(equation_scales),
        "base_polynomial": principal_polynomial(covector),
        "relative_multiplier_numerator": relative_multiplier.numerator,
        "relative_multiplier_denominator": relative_multiplier.denominator,
        "transformed_determinant_numerator": transformed_determinant.numerator,
        "transformed_determinant_denominator": transformed_determinant.denominator,
        "relative_determinant_law_exact": transformed_determinant == expected,
        "characteristic_zero_set_preserved": relative_multiplier != 0,
        "determinant_line": "det(equation fiber) tensor det(reduced field fiber)^*",
    }


def evaluate() -> dict[str, object]:
    expansion = expanded_polynomial()
    test_covectors: tuple[Vector, ...] = (
        (1, 0, 0, 0),
        (2, -1, 3, 1),
        (1, 0, -1, -1),
        (3, 2, -2, 4),
    )
    expansion_checks = [
        evaluate_expansion(expansion, covector) == principal_polynomial(covector)
        for covector in test_covectors
    ]
    branch_report = branch_rank_report()
    chart_report = passive_chart_report()
    frame_report = frame_covariance_report()
    normalized_vectors_distinct = len(set(SOURCE_VECTORS)) == len(SOURCE_VECTORS)
    temporal_factors = factors((1, 0, 0, 0))
    spatial_fixture = (0, 1, 2, 3)
    spatial_factor_values = factors(spatial_fixture)
    checks = {
        "six_nonzero_normalized_source_vectors": len(SOURCE_VECTORS) == 6 and all(vector[0] == 1 for vector in SOURCE_VECTORS),
        "global_linear_factors_pairwise_distinct": normalized_vectors_distinct,
        "expanded_polynomial_degree_six": all(sum(exponent) == 6 for exponent in expansion),
        "expanded_polynomial_matches_product": all(expansion_checks),
        "pure_source_time_noncharacteristic": temporal_factors == (1, 1, 1, 1, 1, 1),
        "passive_chart_covariance": chart_report["all_factor_pairings_invariant"] is True,
        "relative_frame_covariance": frame_report["relative_determinant_law_exact"] is True,
        "all_pair_intersections_rank_two": branch_report["pair_rank_two_count"] == 15,
        "all_triple_intersections_rank_three": branch_report["triple_rank_three_count"] == 20,
        "unique_nonzero_fourfold_subset": branch_report["nonzero_fourfold_subsets"] == [
            {"branches": [2, 3, 4, 6], "rank": 3, "nonzero_intersection_dimension": 1}
        ],
        "no_nonzero_fivefold_or_sixfold_intersection": branch_report["fivefold_nonzero_intersection_count"] == 0 and branch_report["sixfold_nonzero_intersection_count"] == 0,
    }
    return {
        "schema_id": "v22_p4_t01_principal_symbol_model_result_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "candidate_id": "CAND-V22-B1-SIX-TRANSPORT-REDUCED-PRINCIPAL-V1",
        "reduced_symbol": {
            "matrix": "diag(k(X_1),...,k(X_6))",
            "field_dimension": 6,
            "equation_dimension": 6,
            "algebraic_constraint_count": 0,
            "differential_constraint_count": 0,
            "internal_gauge_generator_count": 0,
            "algebraic_redundancy_count": 0,
            "determinant_lawful": True,
        },
        "principal_polynomial": {
            "factor_vectors": [list(vector) for vector in SOURCE_VECTORS],
            "factor_expression": "(w+x)(w+y)(w+z)(w+x+y)(w+y+2z)(w+2x+z)",
            "homogeneous_degree": 6,
            "global_irreducible_factor_count": 6,
            "global_factor_multiplicities": [1, 1, 1, 1, 1, 1],
            "source_coordinate_density_weight": 0,
            "expanded_term_count": len(expansion),
            "test_values": [
                {
                    "covector": list(covector),
                    "factors": list(factors(covector)),
                    "polynomial": principal_polynomial(covector),
                }
                for covector in test_covectors
            ],
        },
        "branch_report": branch_report,
        "fixed_spatial_direction_example": {
            "spatial_covector": list(spatial_fixture[1:]),
            "omega_zero_factor_values": list(spatial_factor_values),
            "characteristic_omega_roots": [-1, -2, -3, -3, -8, -5],
            "root_minus_three_multiplicity": 2,
            "interpretation": "direction-dependent branch crossing, not a repeated global irreducible factor",
        },
        "passive_chart_covariance": chart_report,
        "field_equation_frame_covariance": frame_report,
        "checks": checks,
        "authority": {
            "source_polynomial_only": True,
            "metric_inserted": False,
            "physical_cone_claimed": False,
            "lorentzian_signature_claimed": False,
            "effective_metric_constructed": False,
            "source_law_adopted": False,
            "distance_to_gr_changed": False,
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
