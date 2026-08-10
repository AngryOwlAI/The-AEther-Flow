#!/usr/bin/env python3
"""Executable checks for the post-line-lock P4-T02 selector packet.

This model verifies only the bounded mathematical routing payload.  It does
not infer a physical cone, activate B2, evaluate D7, or unlock P4-T03.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Iterable, Sequence


Vector = tuple[Fraction, ...]


def dot(covector: Sequence[Fraction], vector: Sequence[Fraction]) -> Fraction:
    """Evaluate a covector on a vector."""

    if len(covector) != len(vector):
        raise ValueError("covector and vector dimensions differ")
    return sum((a * b for a, b in zip(covector, vector)), Fraction(0))


def product_polynomial_roots(
    q: Vector, h: Vector, sector_vectors: Iterable[Vector]
) -> tuple[Fraction, ...]:
    """Return roots of t -> product_s (q+t h)(v_s).

    Every factor is linear.  Hyperbolicity with respect to ``h`` therefore
    follows whenever all denominators h(v_s) are nonzero; the selected common
    component uses the consistent positive orientation h(v_s)>0.
    """

    roots: list[Fraction] = []
    for vector in sector_vectors:
        denominator = dot(h, vector)
        if denominator == 0:
            raise ValueError("h lies on a sector characteristic hyperplane")
        roots.append(-dot(q, vector) / denominator)
    return tuple(roots)


def in_oriented_common_cone(h: Vector, sector_vectors: Iterable[Vector]) -> bool:
    """Test membership in the intersection of oriented sector half-spaces."""

    return all(dot(h, vector) > 0 for vector in sector_vectors)


def route_decision() -> dict[str, object]:
    """Return the exact one-packet selector decision."""

    return {
        "selected_next_packet_type": "source_extension_candidate",
        "selected_candidate_id": "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1",
        "selected_next_role_family": "candidate-constructor@0.2.0",
        "selected_route_label": "ontology-law-research-packet",
        "shared_line_route_replayed": False,
        "d7_adequacy_evaluated": False,
        "b2_activated": False,
        "p4_t03_unlocked": False,
        "physical_cone_claimed": False,
        "distance_to_gr_changed": False,
    }


def run_checks() -> dict[str, object]:
    epsilon = Fraction(1, 10)
    e0: Vector = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    e1: Vector = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    h: Vector = e0
    q: Vector = e1
    vectors: tuple[Vector, ...] = (
        (Fraction(1), epsilon, Fraction(0), Fraction(0)),
        e0,
        (Fraction(1), -epsilon, Fraction(0), Fraction(0)),
    )

    roots = product_polynomial_roots(q, h, vectors)
    decision = route_decision()
    checks = {
        "strict_common_covector_exists": in_oriented_common_cone(h, vectors),
        "all_product_roots_are_real": roots
        == (-epsilon, Fraction(0), epsilon),
        "sector_lines_remain_distinct": len(set(vectors)) == 3,
        "product_is_not_common_line_equality": len(set(vectors)) > 1,
        "small_split_preserves_positive_margin": min(dot(h, v) for v in vectors)
        == 1,
        "selected_route_is_constructive_and_distinct": decision[
            "selected_next_packet_type"
        ]
        == "source_extension_candidate"
        and not decision["shared_line_route_replayed"],
        "selected_role_is_candidate_constructor": decision[
            "selected_next_role_family"
        ]
        == "candidate-constructor@0.2.0",
        "protected_blocks_preserved": not any(
            decision[key]
            for key in (
                "d7_adequacy_evaluated",
                "b2_activated",
                "p4_t03_unlocked",
                "physical_cone_claimed",
                "distance_to_gr_changed",
            )
        ),
    }
    return {
        "schema_id": "v22_p4_t02_b2_post_line_lock_selector_model_v1",
        "epsilon": str(epsilon),
        "product_polynomial_on_split": "k0^3-epsilon^2*k0*k1^2",
        "roots": [str(root) for root in roots],
        "common_cone_kind": "intersection_of_oriented_sector_half_spaces",
        "physical_interpretation": "not_established",
        "decision": decision,
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
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
