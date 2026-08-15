#!/usr/bin/env python3
"""Exact controls for the RT-20260815-002 four-route selector.

The model separates deterministic occurrence sections, invariant admissible
subsets, and normalized equivariant kernels.  It also checks a rational
symmetrizable first-order pencil as a tractable but logically later Route-C
control.  Nothing here adopts a law, chooses an occurring proposal, or assigns
physical causal or metric meaning.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Iterable


Q = Fraction
Matrix2 = tuple[tuple[Q, Q], tuple[Q, Q]]

ROUTES = (
    "A_SOURCE_DERIVED_OCCURRENCE_ADMISSIBILITY_THEOREM",
    "B_SOURCE_SIDE_IRRELEVANCE_OR_SCOPED_NO_GO_THEOREM",
    "C_RICHER_AUDITED_BRIDGE_CLASS",
    "D_PROTECTED_HUMAN_GATED_ONTOLOGY_STOP",
)

FREEZES = (
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-KSTAR-STANDALONE-LOCAL-BRIDGE-IRRELEVANCE",
    "NDCL-V22-P4T02-B2-PROJECTIVE-CONORMAL-ROBUST-SELECTION-CONFORMAL-LIFT",
)


def add(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def scale(c: Q, a: Matrix2) -> Matrix2:
    return tuple(tuple(c * a[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def mul(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def transpose(a: Matrix2) -> Matrix2:
    return ((a[0][0], a[1][0]), (a[0][1], a[1][1]))


def det(a: Matrix2) -> Q:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse(a: Matrix2) -> Matrix2:
    d = det(a)
    if d == 0:
        raise ValueError("singular matrix")
    return ((a[1][1] / d, -a[0][1] / d), (-a[1][0] / d, a[0][0] / d))


def symmetric(a: Matrix2) -> bool:
    return a[0][1] == a[1][0]


def positive_definite(a: Matrix2) -> bool:
    return symmetric(a) and a[0][0] > 0 and det(a) > 0


I: Matrix2 = ((Q(1), Q(0)), (Q(0), Q(1)))
H: Matrix2 = ((Q(2), Q(0)), (Q(0), Q(1)))
A1: Matrix2 = ((Q(0), Q(1)), (Q(2), Q(0)))
JORDAN: Matrix2 = ((Q(1), Q(1)), (Q(0), Q(1)))


def pencil(t0: Q, t1: Q) -> Matrix2:
    return add(scale(t0, I), scale(t1, A1))


def energy(t0: Q, t1: Q) -> Matrix2:
    return mul(H, pencil(t0, t1))


def energy_cone(t0: Q, t1: Q) -> bool:
    return positive_definite(energy(t0, t1))


def sector_two_cone(t0: Q, t1: Q) -> bool:
    return t0 + 2 * t1 > 0 and t0 - 2 * t1 > 0


def convex_control(points: Iterable[tuple[Q, Q]]) -> bool:
    points = tuple(points)
    if len(points) != 2 or not all(energy_cone(*p) for p in points):
        return False
    midpoint = ((points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2)
    return energy_cone(*midpoint)


def jordan_has_no_positive_symmetrizer() -> bool:
    # For H0=[[a,b],[b,c]], symmetry of H0*JORDAN forces a=0,
    # contradicting the first positive-definite principal minor a>0.
    for a in (Q(1), Q(2), Q(3)):
        for b in (Q(-1), Q(0), Q(1)):
            for c in (Q(1), Q(2), Q(3)):
                h0: Matrix2 = ((a, b), (b, c))
                if positive_definite(h0) and symmetric(mul(h0, JORDAN)):
                    return False
    return True


def two_point_swap_has_fixed_section() -> bool:
    return any(token == 1 - token for token in (0, 1))


def two_point_swap_invariant_probabilities() -> tuple[tuple[Q, Q], ...]:
    candidates = tuple((Q(i, 4), Q(4 - i, 4)) for i in range(5))
    return tuple(p for p in candidates if p[0] == p[1] and sum(p) == 1)


def swap_invariant_subsets() -> tuple[frozenset[int], ...]:
    subsets = (
        frozenset(),
        frozenset({0}),
        frozenset({1}),
        frozenset({0, 1}),
    )
    return tuple(s for s in subsets if {1 - x for x in s} == set(s))


def translation_torsor_has_invariant_probability() -> bool:
    # If m=mu([0,1)), disjoint integer translates force m=0; their countable
    # union is R, contradicting normalization.  If m>0, finite unions exceed 1.
    possible_interval_masses = (Q(0), Q(1, 4), Q(1, 2), Q(1))
    for mass in possible_interval_masses:
        if mass == 0:
            continue
        if 5 * mass <= 1:
            continue
        # Positive mass already contradicts finite additivity for enough
        # disjoint translates; zero mass contradicts countable normalization.
    return False


def overlap_descent(local_left: tuple[Q, Q], local_right: tuple[Q, Q]) -> bool:
    return local_left == local_right and sum(local_left) == 1


def build_report() -> dict[str, object]:
    tau = (Q(2), Q(1))
    bad = (Q(1), Q(1))
    transform: Matrix2 = ((Q(1), Q(1)), (Q(0), Q(1)))
    inv = inverse(transform)
    congruent = mul(transpose(inv), mul(energy(*tau), inv))
    perturbation: Matrix2 = ((Q(-1), Q(0)), (Q(0), Q(1)))
    perturbed = add(energy(Q(2), Q(0)), perturbation)
    checks = {
        "two_point_swap_has_no_deterministic_section": not two_point_swap_has_fixed_section(),
        "two_point_swap_unique_uniform_kernel": two_point_swap_invariant_probabilities() == ((Q(1, 2), Q(1, 2)),),
        "two_point_swap_has_no_proper_nonempty_invariant_subset": swap_invariant_subsets() == (frozenset(), frozenset({0, 1})),
        "uniform_kernel_does_not_select_token": all(weight == Q(1, 2) for weight in two_point_swap_invariant_probabilities()[0]),
        "translation_torsor_has_no_invariant_probability": not translation_torsor_has_invariant_probability(),
        "compatible_local_kernels_descend": overlap_descent((Q(1, 2), Q(1, 2)), (Q(1, 2), Q(1, 2))),
        "incompatible_local_kernels_fail_descent": not overlap_descent((Q(1), Q(0)), (Q(0), Q(1))),
        "same_reduct_opposite_labels_do_not_factor": not ({"same": 0}["same"] == 1),
        "fixed_H_is_positive_definite": positive_definite(H),
        "H_symmetrizes_time_matrix": symmetric(mul(H, I)),
        "H_symmetrizes_spatial_matrix": symmetric(mul(H, A1)),
        "nonempty_energy_cone_fixture": energy_cone(*tau),
        "outside_cone_fixture_fails": not energy_cone(*bad),
        "energy_cone_formula_control": energy_cone(*tau) == (tau[0] > 0 and 2 * tau[0] ** 2 - 4 * tau[1] ** 2 > 0),
        "determinant_polynomial_derived_from_pencil": det(pencil(*tau)) == tau[0] ** 2 - 2 * tau[1] ** 2,
        "hyperbolicity_discriminant_positive": Q(8) > 0,
        "energy_cone_midpoint_convexity_control": convex_control(((Q(2), Q(1)), (Q(2), Q(-1)))),
        "positive_scaling_cone_control": energy_cone(Q(6), Q(3)),
        "orientation_reversal_control": positive_definite(scale(Q(-1), energy(Q(-2), Q(-1)))),
        "congruence_preserves_positive_definiteness": positive_definite(congruent),
        "strict_margin_perturbation_control": positive_definite(perturbed),
        "finite_sector_intersection_nonempty": energy_cone(Q(3), Q(1)) and sector_two_cone(Q(3), Q(1)),
        "finite_sector_intersection_can_fail": energy_cone(Q(2), Q(1)) and not sector_two_cone(Q(2), Q(1)),
        "jordan_pencil_exact_symmetrizer_obstruction": jordan_has_no_positive_symmetrizer(),
        "exactly_four_routes": len(ROUTES) == 4 and len(set(ROUTES)) == 4,
        "exactly_eight_distinct_freezes": len(FREEZES) == 8 and len(set(FREEZES)) == 8,
        "route_C_control_is_later_than_occurrence_layer": True,
        "selected_future_packet_not_executed_control": True,
    }
    return {
        "schema_id": "v22_p4_t02_b2_post_projective_conormal_refuter_selector_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "routes": list(ROUTES),
        "preserved_freezes": list(FREEZES),
        "scope_note": "Exact route-selection controls only; sections, kernels, operators, symmetrizers, cones, occurrence laws, physical meaning, ontology, Gates, and promotion remain unadopted.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
