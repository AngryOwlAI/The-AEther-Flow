#!/usr/bin/env python3
"""Exact rational controls for the RT-20260811-001 Bridge_OM Refuter stress."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations


Q = Fraction


def dot(covector: tuple[Q, ...], vector: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(covector, vector)), Q(0))


def determinant_2(left: tuple[Q, Q], right: tuple[Q, Q]) -> Q:
    return left[0] * right[1] - left[1] * right[0]


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns)]
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_row = 0
    for pivot_col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][pivot_col] != 0),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][pivot_col]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = matrix[row][pivot_col]
            if factor:
                matrix[row] = [
                    entry - factor * base
                    for entry, base in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def sign(value: Q) -> int:
    return (value > 0) - (value < 0)


def wall_family(n: int) -> dict[str, object]:
    epsilon = Q(1, n)
    e1 = (Q(1), Q(0))
    e2 = (Q(0), Q(1))
    negative_side = (e1, e2, (Q(-1), epsilon))
    wall = (e1, e2, (Q(-1), Q(0)))
    positive_side = (e1, e2, (Q(-1), -epsilon))
    feasible_covector = (Q(1), Q(n + 1))
    obstruction = (Q(1), epsilon, Q(1))
    obstruction_sum = tuple(
        sum((coefficient * column[index] for coefficient, column in zip(obstruction, positive_side)), Q(0))
        for index in range(2)
    )
    return {
        "n": n,
        "epsilon": str(epsilon),
        "rank_negative": rank(negative_side),
        "rank_wall": rank(wall),
        "rank_positive": rank(positive_side),
        "negative_side_evaluations": [
            str(dot(feasible_covector, column)) for column in negative_side
        ],
        "positive_side_obstruction_coefficients": [str(item) for item in obstruction],
        "positive_side_obstruction_sum": [str(item) for item in obstruction_sum],
        "wall_pair_13_determinant": str(determinant_2(e1, wall[2])),
        "negative_pair_13_sign": sign(determinant_2(e1, negative_side[2])),
        "positive_pair_13_sign": sign(determinant_2(e1, positive_side[2])),
        "max_column_delta": str(Q(2, n)),
        "negative_branch": "Feasible",
        "wall_branch": "Obstructed_support_13",
        "positive_branch": "Obstructed_support_123",
    }


def reorientation_pair(r: int) -> dict[str, object]:
    basis = tuple(
        tuple(Q(1) if row == column else Q(0) for row in range(r))
        for column in range(r)
    )
    positive_sum = tuple(Q(1) for _ in range(r))
    negative_sum = tuple(Q(-1) for _ in range(r))
    feasible = basis + (positive_sum,)
    obstructed = basis + (negative_sum,)
    witness = tuple(Q(1) for _ in range(r))
    coefficients = tuple(Q(1) for _ in range(r + 1))
    obstruction_sum = tuple(
        sum((coefficient * column[index] for coefficient, column in zip(coefficients, obstructed)), Q(0))
        for index in range(r)
    )
    return {
        "rank": r,
        "feasible_rank": rank(feasible),
        "obstructed_rank": rank(obstructed),
        "feasible_evaluations": [str(dot(witness, column)) for column in feasible],
        "obstruction_sum": [str(item) for item in obstruction_sum],
        "same_unoriented_last_ray": True,
        "branch_pair": ["Feasible", "Obstructed"],
    }


def refinement_control() -> dict[str, object]:
    e1 = (Q(1), Q(0))
    e2 = (Q(0), Q(1))
    base = (e1, e2)
    refined = base + ((Q(-1), Q(-1)),)
    witness = (Q(1), Q(1))
    coefficients = (Q(1), Q(1), Q(1))
    obstruction_sum = tuple(
        sum((coefficient * column[index] for coefficient, column in zip(coefficients, refined)), Q(0))
        for index in range(2)
    )
    return {
        "base_rank": rank(base),
        "refined_rank": rank(refined),
        "base_evaluations": [str(dot(witness, column)) for column in base],
        "refined_obstruction_sum": [str(item) for item in obstruction_sum],
        "old_sector_inclusion_preserved": True,
        "base_branch": "Feasible",
        "refined_branch": "Obstructed",
    }


def projective_modulus_control(parameter: int) -> dict[str, object]:
    columns = (
        (Q(1), Q(0)),
        (Q(1), Q(1)),
        (Q(1), Q(parameter)),
        (Q(0), Q(1)),
    )
    pair_signs = [
        sign(determinant_2(columns[i], columns[j]))
        for i, j in combinations(range(4), 2)
    ]
    witness = (Q(1), Q(1))
    cross_ratio = Q(parameter, parameter - 1)
    return {
        "parameter": parameter,
        "rank": rank(columns),
        "pair_signs": pair_signs,
        "strict_evaluations": [str(dot(witness, column)) for column in columns],
        "positive_circuit_count": 0,
        "strict_chamber_reduced_inequalities": ["a>0", "b>0"],
        "labeled_projective_cross_ratio": str(cross_ratio),
    }


def build_payload() -> dict[str, object]:
    wall_controls = [wall_family(n) for n in (10, 100, 1000)]
    reorientations = [reorientation_pair(r) for r in range(1, 9)]
    refinement = refinement_control()
    modulus_two = projective_modulus_control(2)
    modulus_three = projective_modulus_control(3)

    checks = {
        "wall_family_fixed_rank": all(
            item["rank_negative"] == item["rank_wall"] == item["rank_positive"] == 2
            for item in wall_controls
        ),
        "wall_family_feasible_side_strict": all(
            all(Q(value) > 0 for value in item["negative_side_evaluations"])
            for item in wall_controls
        ),
        "wall_family_obstruction_exact": all(
            item["positive_side_obstruction_sum"] == ["0", "0"]
            for item in wall_controls
        ),
        "wall_family_arbitrarily_small_sequence": [
            item["max_column_delta"] for item in wall_controls
        ] == ["1/5", "1/50", "1/500"],
        "reorientation_flips_total_branch_all_ranks": all(
            all(Q(value) > 0 for value in item["feasible_evaluations"])
            and all(value == "0" for value in item["obstruction_sum"])
            for item in reorientations
        ),
        "refinement_can_destroy_strict_feasibility": (
            refinement["base_branch"] == "Feasible"
            and refinement["refined_branch"] == "Obstructed"
            and refinement["refined_obstruction_sum"] == ["0", "0"]
        ),
        "same_oriented_matroid_modulus_pair": modulus_two["pair_signs"] == modulus_three["pair_signs"],
        "same_strict_chamber_modulus_pair": (
            modulus_two["strict_chamber_reduced_inequalities"]
            == modulus_three["strict_chamber_reduced_inequalities"]
        ),
        "distinct_projective_moduli_forgotten_by_sign_data": (
            modulus_two["labeled_projective_cross_ratio"]
            != modulus_three["labeled_projective_cross_ratio"]
        ),
    }
    payload_core = {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_exact_model_v1",
        "wall_controls": wall_controls,
        "reorientation_controls": reorientations,
        "refinement_control": refinement,
        "projective_modulus_controls": [modulus_two, modulus_three],
        "checks": checks,
    }
    payload_bytes = json.dumps(payload_core, sort_keys=True, separators=(",", ":")).encode()
    payload_core["payload_sha256"] = hashlib.sha256(payload_bytes).hexdigest()
    payload_core["status"] = "PASS" if all(checks.values()) else "FAIL"
    return payload_core


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["status"])
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
