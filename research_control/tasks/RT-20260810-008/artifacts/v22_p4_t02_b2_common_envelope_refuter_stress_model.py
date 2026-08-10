#!/usr/bin/env python3
"""Exact support checks for the RT-20260810-008 repaired-quotient stress.

The calculations use one rational coordinate presentation of the committed
proposal-only RT007 source extension.  They are reproducibility evidence, not
proof authority, empirical calibration, ontology adoption, or a physical-cone
construction.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from typing import Iterable, Sequence


Vector = tuple[Fraction, Fraction, Fraction, Fraction]
Covector = tuple[Fraction, Fraction, Fraction, Fraction]
Response = tuple[Fraction, Fraction, Fraction]


def dot(k: Covector, v: Vector) -> Fraction:
    return sum((ki * vi for ki, vi in zip(k, v)), Fraction(0))


def exact_rank(rows: Sequence[Sequence[Fraction]]) -> int:
    work = [list(row) for row in rows]
    if not work:
        return 0
    rank = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(rank, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for i, row in enumerate(work):
            if i == rank or row[column] == 0:
                continue
            factor = row[column]
            work[i] = [row[j] - factor * work[rank][j] for j in range(len(row))]
        rank += 1
        if rank == len(work):
            break
    return rank


def signs(values: Iterable[Fraction]) -> tuple[int, ...]:
    return tuple(1 if value > 0 else -1 if value < 0 else 0 for value in values)


def evaluate(k: Covector, vectors: Sequence[Vector]) -> Response:
    return tuple(dot(k, vector) for vector in vectors)  # type: ignore[return-value]


def same_positive_ray(left: Response, right: Response) -> bool:
    if any(value == 0 for value in left + right):
        return False
    scale = right[0] / left[0]
    return scale > 0 and all(right[i] == scale * left[i] for i in range(3))


def run_checks() -> dict[str, object]:
    epsilon = Fraction(1, 3)
    delta = Fraction(1, 10)
    u: Vector = (1, 0, 0, 0)
    z: Vector = (0, 1, 0, 0)
    w: Vector = (0, 0, 1, 0)

    base_vectors: tuple[Vector, Vector, Vector] = (
        (1, epsilon, 0, 0),
        u,
        (1, -epsilon, 0, 0),
    )
    collapsed_vectors: tuple[Vector, Vector, Vector] = (u, u, u)
    perturbed_vectors: tuple[Vector, Vector, Vector] = (
        (1, epsilon, delta, 0),
        u,
        (1, -epsilon, 0, 0),
    )

    base_rank = exact_rank(base_vectors)
    collapsed_rank = exact_rank(collapsed_vectors)
    perturbed_rank = exact_rank(perturbed_vectors)

    # F(v_R,v_S,v_D)=v_R-2v_S+v_D is surjective V^3 -> V, so its
    # kernel (the exact midpoint-law triples) has codimension dim(V)=4.
    constraint_matrix = []
    for coordinate in range(4):
        row = [Fraction(0)] * 12
        row[coordinate] = Fraction(1)
        row[4 + coordinate] = Fraction(-2)
        row[8 + coordinate] = Fraction(1)
        constraint_matrix.append(row)
    constraint_rank = exact_rank(constraint_matrix)
    midpoint_family_dimension = 12 - constraint_rank
    normalized_constraint_matrix = []
    for coordinate in range(3):
        row = [Fraction(0)] * 9
        row[coordinate] = Fraction(1)
        row[3 + coordinate] = Fraction(-2)
        row[6 + coordinate] = Fraction(1)
        normalized_constraint_matrix.append(row)
    normalized_constraint_rank = exact_rank(normalized_constraint_matrix)

    # The e0,e1,e2 minor of the perturbed response vectors is -epsilon*delta.
    perturbed_minor = -epsilon * delta
    arbitrarily_small_rank_jump_samples = {}
    for denominator in (10, 100, 1000):
        sample_delta = Fraction(1, denominator)
        sample = (
            (1, epsilon, sample_delta, 0),
            u,
            (1, -epsilon, 0, 0),
        )
        arbitrarily_small_rank_jump_samples[str(sample_delta)] = exact_rank(sample)

    base_sign_orbits = set()
    for a, b in (
        (1, -4), (1, 0), (1, 4), (-1, 4), (-1, 0), (-1, -4)
    ):
        k: Covector = (Fraction(a), Fraction(b), 0, 0)
        base_sign_orbits.add(signs(evaluate(k, base_vectors)))

    # For every desired response (x,y,zeta), choose
    # a=y, b=(y-zeta)/epsilon, c=(x-2y+zeta)/delta.
    perturbed_sign_orbits = set()
    sign_lift_checks = []
    for x, y, zeta in product((-1, 1), repeat=3):
        a = Fraction(y)
        b = Fraction(y - zeta) / epsilon
        c = Fraction(x - 2 * y + zeta) / delta
        k = (a, b, c, Fraction(0))
        lifted = evaluate(k, perturbed_vectors)
        sign_lift_checks.append(lifted == (x, y, zeta))
        perturbed_sign_orbits.add(signs(lifted))

    common_positive_witness: Covector = (1, 0, 0, 0)
    base_positive = evaluate(common_positive_witness, base_vectors)
    perturbed_positive = evaluate(common_positive_witness, perturbed_vectors)
    collapse_positive = evaluate(common_positive_witness, collapsed_vectors)

    inside_k: Covector = (1, Fraction(1, 2), 0, 0)
    inside = evaluate(inside_k, base_vectors)
    common_scaled: Response = tuple(2 * value for value in inside)  # type: ignore[assignment]
    independent_scaled: Response = (
        2 * inside[0], 3 * inside[1], 5 * inside[2]
    )

    # The diagonal response (1,1,1) already forces three positive transition
    # factors to agree if its positive ray is to remain unchanged.
    diagonal_response: Response = (1, 1, 1)
    unequal_transition_response: Response = (2, 3, 5)
    equal_transition_response: Response = (7, 7, 7)
    common_line_descent_requires_equal_factors = (
        not same_positive_ray(diagonal_response, unequal_transition_response)
        and same_positive_ray(diagonal_response, equal_transition_response)
    )

    kernel_basis: tuple[Covector, Covector] = (
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    response_kernel_pass = all(
        evaluate(basis, base_vectors) == (0, 0, 0) for basis in kernel_basis
    )
    same_response_distinct_covectors = (
        evaluate(inside_k, base_vectors)
        == evaluate((1, Fraction(1, 2), 9, -4), base_vectors)
    )

    collapse_sign_orbits = {
        signs(evaluate((Fraction(a), 0, 0, 0), collapsed_vectors))
        for a in (-1, 1)
    }

    checks = {
        "fixed_rt007_rank_two": base_rank == 2,
        "collapse_rank_one": collapsed_rank == 1 and len(collapse_sign_orbits) == 2,
        "midpoint_family_codimension_four": (
            constraint_rank == 4 and midpoint_family_dimension == 8
        ),
        "normalized_midpoint_family_codimension_three": normalized_constraint_rank == 3,
        "unstructured_rank_three_for_every_nonzero_sample_delta": (
            perturbed_rank == 3
            and perturbed_minor != 0
            and set(arbitrarily_small_rank_jump_samples.values()) == {3}
        ),
        "unstructured_response_realizes_all_eight_sign_orbits": (
            all(sign_lift_checks) and len(perturbed_sign_orbits) == 8
        ),
        "common_positive_witness_survives": (
            base_positive == perturbed_positive == collapse_positive == (1, 1, 1)
        ),
        "independent_positive_transitions_preserve_sign_but_not_ray": (
            signs(inside) == signs(independent_scaled) == (1, 1, 1)
            and same_positive_ray(inside, common_scaled)
            and not same_positive_ray(inside, independent_scaled)
        ),
        "common_line_descent_requires_equal_factors": common_line_descent_requires_equal_factors,
        "response_inverse_has_two_dimensional_kernel": (
            response_kernel_pass and same_response_distinct_covectors
        ),
        "fixed_base_has_six_sign_orbits": len(base_sign_orbits) == 6,
    }

    return {
        "schema_id": "v22_p4_t02_b2_common_envelope_refuter_stress_model_v1",
        "task_id": "RT-20260810-008",
        "job_id": "AJ-RT-20260810-008-001",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "decisive_result_supported": "scoped_obstruction",
        "authority": "support_only_not_proof_authority",
        "parameters": {"epsilon": str(epsilon), "delta": str(delta)},
        "fixed_candidate": {
            "rank": base_rank,
            "kernel_dimension": 4 - base_rank,
            "sign_orbit_count": len(base_sign_orbits),
            "common_positive_witness_response": [str(v) for v in base_positive],
        },
        "collapse": {
            "rank": collapsed_rank,
            "positive_projective_sheet_count": 2,
            "sign_orbit_count": len(collapse_sign_orbits),
            "meaning": "the one-coordinate six-cell classifier collapses to the diagonal two-sheet response",
        },
        "inverse_defect": {
            "response_kernel": "ann(span{u,z})",
            "response_kernel_dimension": 2,
            "positive_ray_fiber_dimension": 3,
            "sign_cell_fiber_dimension": 4,
            "physical_reconstruction_authorized": False,
        },
        "transition_descent": {
            "common_positive_factor_preserves_Q_ray": True,
            "independent_positive_factors_preserve_Q_sign": True,
            "independent_positive_factors_preserve_Q_ray": False,
            "global_Q_ray_requires_common_positive_line_transition": True,
            "common_transition_cocycle_required": True,
        },
        "finite_variation": {
            "midpoint_constraint_rank": constraint_rank,
            "midpoint_family_codimension": constraint_rank,
            "midpoint_family_dimension": midpoint_family_dimension,
            "h0_normalized_midpoint_codimension": normalized_constraint_rank,
            "perturbed_rank": perturbed_rank,
            "nonzero_minor": str(perturbed_minor),
            "arbitrarily_small_rank_jump_samples": arbitrarily_small_rank_jump_samples,
            "perturbed_sign_orbit_count": len(perturbed_sign_orbits),
            "common_positivity_survives": True,
            "exact_midpoint_plane_survives": False,
        },
        "checks": checks,
        "freeze_recommendation": {
            "decision": "locally_frozen",
            "label": "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
            "scope": "presentation_independent_unstructured_robust_source_operational_quotient_claim",
            "same_milestone_continuation_open": True,
            "next_role": "theoretical-continuation-selector@0.1.0",
        },
        "authority_limits": {
            "fixed_candidate_rejected": False,
            "empirical_response_semantics": False,
            "physical_causality_constructed": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "effective_metric_constructed": False,
            "source_law_adopted": False,
            "distance_to_gr_changed": False,
            "global_no_go_claimed": False,
            "future_source_extension_impossibility_claimed": False,
            "proof_authority": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = run_checks()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
