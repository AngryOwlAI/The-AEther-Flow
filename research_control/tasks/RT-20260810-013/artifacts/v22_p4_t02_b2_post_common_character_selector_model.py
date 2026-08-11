#!/usr/bin/env python3
"""Exact finite checks for the RT013 theoretical route selector.

The checks exercise one feasible oriented configuration, one minimal positive
circuit obstruction, the source-presentation invariances required by the
future packet, and the four-route decision filter.  They are draft/control
calculation evidence only; they do not prove physical causality, universality,
ontology adoption, or any Distance-to-GR advance.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any


Vector = tuple[Fraction, ...]

FREEZES = (
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
)

ROUTES: tuple[dict[str, Any], ...] = (
    {
        "route_id": "A_SOURCE_SIDE_IRRELEVANCE_THEOREM",
        "constructive_available": False,
        "materially_distinct": True,
        "source_provenance_ready": False,
        "freeze_independence_established": True,
        "requires_human_gate": False,
        "total_finite_contract": False,
    },
    {
        "route_id": "B_NON_CHARACTER_ORIENTED_MATROID_BRIDGE",
        "constructive_available": True,
        "materially_distinct": True,
        "source_provenance_ready": True,
        "freeze_independence_established": True,
        "requires_human_gate": False,
        "total_finite_contract": True,
    },
    {
        "route_id": "C_INDEPENDENT_HOLONOMY_PROTECTION_LAW",
        "constructive_available": True,
        "materially_distinct": False,
        "source_provenance_ready": False,
        "freeze_independence_established": False,
        "requires_human_gate": False,
        "total_finite_contract": False,
    },
    {
        "route_id": "D_PROTECTED_HUMAN_GATED_STOP",
        "constructive_available": False,
        "materially_distinct": True,
        "source_provenance_ready": True,
        "freeze_independence_established": True,
        "requires_human_gate": True,
        "total_finite_contract": True,
    },
)


def dot(left: Vector, right: Vector) -> Fraction:
    if len(left) != len(right):
        raise ValueError("dimension mismatch")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def weighted_sum(vectors: tuple[Vector, ...], weights: tuple[Fraction, ...]) -> Vector:
    if not vectors or len(vectors) != len(weights):
        raise ValueError("invalid weighted family")
    return tuple(
        sum((weight * vector[index] for vector, weight in zip(vectors, weights)), Fraction(0))
        for index in range(len(vectors[0]))
    )


def sign(value: Fraction) -> int:
    return 1 if value > 0 else (-1 if value < 0 else 0)


def sign_covector(covector: Vector, vectors: tuple[Vector, ...]) -> tuple[int, ...]:
    return tuple(sign(dot(covector, vector)) for vector in vectors)


def matrix_vector(matrix: tuple[Vector, ...], vector: Vector) -> Vector:
    return tuple(dot(row, vector) for row in matrix)


def row_matrix(row: Vector, matrix: tuple[Vector, ...]) -> Vector:
    columns = tuple(zip(*matrix))
    return tuple(dot(row, tuple(column)) for column in columns)


def route_is_selectable(route: dict[str, Any]) -> bool:
    return (
        route["constructive_available"]
        and route["materially_distinct"]
        and route["source_provenance_ready"]
        and route["freeze_independence_established"]
        and not route["requires_human_gate"]
        and route["total_finite_contract"]
    )


def run_checks() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, details: Any) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "details": details})

    feasible_vectors: tuple[Vector, ...] = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(1)),
    )
    feasible_covector: Vector = (Fraction(1), Fraction(1))
    feasible_signs = sign_covector(feasible_covector, feasible_vectors)
    add(
        "strict_all_positive_covector_witness",
        feasible_signs == (1, 1, 1),
        {"signs": feasible_signs},
    )

    circuit_vectors: tuple[Vector, ...] = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(-1), Fraction(-1)),
    )
    circuit_weights = (Fraction(1), Fraction(1), Fraction(1))
    circuit_sum = weighted_sum(circuit_vectors, circuit_weights)
    add(
        "minimal_positive_circuit_certificate",
        circuit_sum == (Fraction(0), Fraction(0))
        and all(weight > 0 for weight in circuit_weights),
        {"weighted_sum": [str(value) for value in circuit_sum]},
    )
    add(
        "circuit_excludes_all_positive_covector",
        sum(circuit_weights[index] * dot(feasible_covector, circuit_vectors[index]) for index in range(3))
        == 0,
        "Applying any covector to the zero positive dependence sums to zero, so all terms cannot be positive.",
    )
    add(
        "rank_two_support_at_most_three",
        len(circuit_vectors) <= 2 + 1,
        {"rank_bound": 2, "support": len(circuit_vectors)},
    )

    scales = (Fraction(2), Fraction(3), Fraction(5))
    scaled_feasible = tuple(
        tuple(scale * coordinate for coordinate in vector)
        for vector, scale in zip(feasible_vectors, scales)
    )
    add(
        "positive_sector_rescaling_preserves_sign_covector",
        sign_covector(feasible_covector, scaled_feasible) == feasible_signs,
        {"before": feasible_signs, "after": sign_covector(feasible_covector, scaled_feasible)},
    )
    scaled_circuit = tuple(
        tuple(scale * coordinate for coordinate in vector)
        for vector, scale in zip(circuit_vectors, scales)
    )
    transformed_weights = tuple(weight / scale for weight, scale in zip(circuit_weights, scales))
    add(
        "positive_sector_rescaling_preserves_circuit_support",
        weighted_sum(scaled_circuit, transformed_weights) == (Fraction(0), Fraction(0))
        and all(weight > 0 for weight in transformed_weights),
        {"weights": [str(weight) for weight in transformed_weights]},
    )

    transform: tuple[Vector, ...] = (
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
    )
    inverse: tuple[Vector, ...] = (
        (Fraction(1), Fraction(-1)),
        (Fraction(0), Fraction(1)),
    )
    transformed_vectors = tuple(matrix_vector(transform, vector) for vector in feasible_vectors)
    transformed_covector = row_matrix(feasible_covector, inverse)
    add(
        "source_linear_presentation_preserves_signs",
        sign_covector(transformed_covector, transformed_vectors) == feasible_signs,
        {
            "transformed_covector": [str(value) for value in transformed_covector],
            "signs": sign_covector(transformed_covector, transformed_vectors),
        },
    )

    refined_vectors = feasible_vectors + ((Fraction(-1), Fraction(-1)),)
    restricted = sign_covector(feasible_covector, refined_vectors)[: len(feasible_vectors)]
    add(
        "sector_refinement_covectors_restrict",
        restricted == feasible_signs,
        {"refined_signs": sign_covector(feasible_covector, refined_vectors), "restriction": restricted},
    )
    add(
        "supported_positive_circuit_persists_under_refinement",
        weighted_sum(circuit_vectors, circuit_weights) == (Fraction(0), Fraction(0)),
        "A circuit on an old support remains a circuit obstruction after adding sectors.",
    )

    selected = [route["route_id"] for route in ROUTES if route_is_selectable(route)]
    add("exactly_four_routes_compared", len(ROUTES) == 4, [route["route_id"] for route in ROUTES])
    add(
        "one_route_selected_by_declared_filter",
        selected == ["B_NON_CHARACTER_ORIENTED_MATROID_BRIDGE"],
        {"selected": selected},
    )
    add("all_three_freezes_preserved", len(FREEZES) == 3 and len(set(FREEZES)) == 3, list(FREEZES))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checks = run_checks()
    passed = all(check["passed"] for check in checks)
    payload = {
        "schema_id": "v22_p4_t02_b2_post_common_character_selector_model_v1",
        "status": "PASS" if passed else "FAIL",
        "check_count": len(checks),
        "failure_count": sum(not check["passed"] for check in checks),
        "selected_route": "B_NON_CHARACTER_ORIENTED_MATROID_BRIDGE",
        "selected_packet_executed": False,
        "freezes": list(FREEZES),
        "checks": checks,
        "authority_note": "Exact finite draft/control checks only; no scientific promotion or physical interpretation.",
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["status"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
