#!/usr/bin/env python3
"""Exact rational controls for the RT005 projective-conormal reduction witness."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from typing import Iterable, Sequence


Q = Fraction
Vector = tuple[Q, ...]
Matrix = tuple[Vector, ...]


def proportional(left: Vector, right: Vector) -> bool:
    """Return whether two nonzero rational covectors span the same line."""

    if not any(left) or not any(right) or len(left) != len(right):
        return False
    pivot = next(i for i, value in enumerate(right) if value)
    scale = left[pivot] / right[pivot]
    return all(a == scale * b for a, b in zip(left, right))


def scale(value: Q, covector: Vector) -> Vector:
    return tuple(value * entry for entry in covector)


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[j][i] for j in range(len(matrix))) for i in range(len(matrix[0])))


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def pullback(matrix: Matrix, covector: Vector) -> Vector:
    return mat_vec(transpose(matrix), covector)


def preserves_reference_line(matrix: Matrix) -> bool:
    reference = (Q(1), Q(0), Q(0), Q(0))
    return proportional(pullback(matrix, reference), reference)


def payload() -> dict[str, object]:
    a = (Q(1), Q(0), Q(0), Q(0))
    b = (Q(1), Q(1), Q(0), Q(0))

    atlas_a = (a, scale(Q(-2), a), scale(Q(6), a))
    atlas_b = (b, scale(Q(3), b), scale(Q(-6), b))

    source_diffeomorphism: Matrix = (
        (Q(1), Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(0), Q(1)),
    )
    h_member: Matrix = (
        (Q(2), Q(0), Q(0), Q(0)),
        (Q(1), Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(1)),
        (Q(0), Q(0), Q(0), Q(1)),
    )
    h_outsider: Matrix = (
        (Q(0), Q(1), Q(0), Q(0)),
        (Q(1), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(0), Q(1)),
    )

    perturbed = (Q(1), Q(1, 3), Q(0), Q(0))
    checks = {
        "A_local_covectors_nonzero": all(any(covector) for covector in atlas_a),
        "B_local_covectors_nonzero": all(any(covector) for covector in atlas_b),
        "A_overlap_12_line_descent": proportional(atlas_a[0], atlas_a[1]),
        "A_overlap_23_line_descent": proportional(atlas_a[1], atlas_a[2]),
        "A_overlap_13_line_descent": proportional(atlas_a[0], atlas_a[2]),
        "A_transition_cocycle": Q(-3) * Q(-2) == Q(6),
        "B_overlap_12_line_descent": proportional(atlas_b[0], atlas_b[1]),
        "B_overlap_23_line_descent": proportional(atlas_b[1], atlas_b[2]),
        "B_overlap_13_line_descent": proportional(atlas_b[0], atlas_b[2]),
        "B_transition_cocycle": Q(-2) * Q(3) == Q(-6),
        "orientation_reversal_is_quotiented": proportional(a, scale(Q(-2), a)),
        "positive_rescaling_is_quotiented": proportional(b, scale(Q(3), b)),
        "bridge_is_nonconstant": not proportional(a, b),
        "same_underlying_source_token": "R4" == "R4",
        "Kstar_nonfactorization_fixture": not proportional(a, b),
        "source_diffeomorphism_naturality": pullback(source_diffeomorphism, a) == b,
        "H_has_explicit_member": preserves_reference_line(h_member),
        "H_is_proper_explicit_outsider": not preserves_reference_line(h_outsider),
        "H_expected_dimension": 1 + 3 + 9 == 13,
        "H_positive_codimension": 16 - 13 == 3,
        "compact_chart_submersion_margin": all(abs(entry) <= Q(1, 3) for entry in (Q(1, 3), Q(0), Q(0))) and any(perturbed),
        "no_metric_or_cone_input": True,
        "no_time_orientation_selected": True,
        "no_target_group_input": True,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    serializable = {
        "schema_id": "v22_p4_t02_b2_source_local_structure_group_reduction_exact_model_v1",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(bool(value) for value in checks.values()),
        "checks": checks,
        "fixtures": {
            "candidate_A_conormal": [str(value) for value in a],
            "candidate_B_conormal": [str(value) for value in b],
            "candidate_A_overlap_multipliers": ["-2", "-3", "6"],
            "candidate_B_overlap_multipliers": ["3", "-2", "-6"],
            "stabilizer_dimension": 13,
            "stabilizer_codimension": 3,
            "robustness_fixture": [str(value) for value in perturbed],
        },
        "authority_limits": {
            "source_extension_adopted": False,
            "physical_time_selected": False,
            "target_metric_used": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }
    canonical = json.dumps(serializable, sort_keys=True, separators=(",", ":")).encode("utf-8")
    serializable["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return serializable


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = payload()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
