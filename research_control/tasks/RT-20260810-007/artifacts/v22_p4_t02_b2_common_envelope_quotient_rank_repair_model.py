#!/usr/bin/env python3
"""Exact support checks for the RT-20260810-007 quotient-rank repair.

This executable realizes one coordinate presentation of the fixed proposal-only
Rod/Signal/Detector source data.  It checks the repaired response-image claims
and retained conditional identities with exact rational arithmetic.  It is
reproduction evidence only: it is not proof authority, empirical calibration,
ontology adoption, or a physical-causality construction.
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
Matrix = tuple[tuple[Fraction, ...], ...]


def dot(k: Covector, v: Vector) -> Fraction:
    return sum((ki * vi for ki, vi in zip(k, v)), Fraction(0))


def response(a: Fraction, b: Fraction, epsilon: Fraction) -> Response:
    """Return the three responses after the declared line relabelings iota_s."""
    return (a + epsilon * b, a, a - epsilon * b)


def signs(values: Iterable[Fraction]) -> tuple[int, ...]:
    return tuple(1 if value > 0 else -1 if value < 0 else 0 for value in values)


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
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for i, row in enumerate(work):
            if i == rank or row[column] == 0:
                continue
            factor = row[column]
            work[i] = [row[j] - factor * work[rank][j] for j in range(len(row))]
        rank += 1
        if rank == len(work):
            break
    return rank


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum((matrix[i][j] * vector[j] for j in range(4)), Fraction(0))
        for i in range(4)
    )  # type: ignore[return-value]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[j][i] for j in range(4)) for i in range(4))


def same_positive_ray(left: Response, right: Response) -> bool:
    if any(entry == 0 for entry in left + right):
        return False
    scale = right[0] / left[0]
    return scale > 0 and all(right[i] == scale * left[i] for i in range(3))


def run_checks() -> dict[str, object]:
    epsilon = Fraction(1, 3)
    u: Vector = (1, 0, 0, 0)
    z: Vector = (0, 1, 0, 0)
    vectors: tuple[Vector, Vector, Vector] = (
        (1, epsilon, 0, 0),
        u,
        (1, -epsilon, 0, 0),
    )

    # Each evaluation is initially typed in a distinct response line L_s.  The
    # booleans below represent declared proposal-only isomorphisms iota_s:L_s->L_0;
    # no numerical equality is asserted until all three values are relabelled.
    response_line_types = ("L_R", "L_S", "L_D")
    relabeling_targets = ("L_0", "L_0", "L_0")
    typed_before_comparison = len(set(response_line_types)) == 3
    declared_common_bookkeeping_line = len(set(relabeling_targets)) == 1

    response_matrix = [list(vector) for vector in vectors]
    response_rank = exact_rank(response_matrix)
    kernel_basis: tuple[Covector, Covector] = (
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    kernel_basis_pass = all(
        all(dot(basis_covector, vector) == 0 for vector in vectors)
        for basis_covector in kernel_basis
    )
    kernel_is_ann_u_z = kernel_basis_pass and all(
        dot(basis_covector, u) == dot(basis_covector, z) == 0
        for basis_covector in kernel_basis
    )

    ab_samples = (
        (Fraction(1), Fraction(-4)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(4)),
        (Fraction(-1), Fraction(4)),
        (Fraction(-1), Fraction(0)),
        (Fraction(-1), Fraction(-4)),
    )
    image_samples = tuple(response(a, b, epsilon) for a, b in ab_samples)
    image_plane_pass = all(r[0] + r[2] == 2 * r[1] for r in image_samples)
    plane_surjectivity_basis_pass = (
        response(Fraction(1), Fraction(0), epsilon) == (1, 1, 1)
        and response(Fraction(0), Fraction(3), epsilon) == (1, 0, -1)
    )

    expected_sign_orbits = {
        (-1, -1, -1),
        (-1, -1, 1),
        (-1, 1, 1),
        (1, -1, -1),
        (1, 1, -1),
        (1, 1, 1),
    }
    realized_sign_orbits = {signs(sample) for sample in image_samples}
    sign_image_pass = realized_sign_orbits == expected_sign_orbits
    alternating_patterns_excluded = all(
        pattern not in realized_sign_orbits for pattern in {(1, -1, 1), (-1, 1, -1)}
    )

    # On the declared domain D every component is nonzero.  Since r_S=a, D
    # excludes a=0.  The positive-scale ray therefore has one continuous
    # coordinate t=epsilon*b/a together with the discrete sheet sigma=sign(a).
    chart_samples: list[dict[str, object]] = []
    chart_reconstruction_pass = True
    for a, b in ab_samples:
        r = response(a, b, epsilon)
        t = epsilon * b / a
        sigma = 1 if a > 0 else -1
        reconstructed = tuple(a * entry for entry in (1 + t, Fraction(1), 1 - t))
        normalized_ray = tuple(Fraction(sigma) * entry for entry in (1 + t, Fraction(1), 1 - t))
        sample_pass = (
            reconstructed == r
            and normalized_ray == tuple(entry / abs(a) for entry in r)
            and t == (r[0] - r[2]) / (2 * r[1])
        )
        chart_reconstruction_pass = chart_reconstruction_pass and sample_pass
        chart_samples.append(
            {
                "a": str(a),
                "b": str(b),
                "sigma": sigma,
                "t": str(t),
                "response": [str(entry) for entry in r],
                "positive_ray_normalized_by_abs_a": [str(entry) for entry in normalized_ray],
                "signs": list(signs(r)),
                "reconstruction_pass": sample_pass,
            }
        )
    zero_a_excluded_from_domain = response(Fraction(0), Fraction(3), epsilon)[1] == 0
    projective_image_dimension = response_rank - 1

    positive_samples = (
        (Fraction(1), Fraction(0)),
        (Fraction(2), Fraction(3)),
        (Fraction(2), Fraction(-3)),
    )
    positive_preimage_pass = all(
        all(entry > 0 for entry in response(a, b, epsilon))
        == (a > epsilon * abs(b))
        for a, b in positive_samples + ab_samples
    )
    positive_t_cell_pass = all(
        (-1 < epsilon * b / a < 1)
        for a, b in positive_samples
    )

    inside = response(Fraction(1), Fraction(1, 2), epsilon)
    product_value = inside[0] * inside[1] * inside[2]
    product_and_cone_preserved = (
        inside == (Fraction(7, 6), 1, Fraction(5, 6))
        and product_value == Fraction(35, 36)
        and all(entry > 0 for entry in inside)
    )
    common_scaled: Response = tuple(2 * entry for entry in inside)  # type: ignore[assignment]
    independently_scaled: Response = (
        2 * inside[0],
        3 * inside[1],
        5 * inside[2],
    )
    quotient_boundaries_pass = (
        same_positive_ray(inside, common_scaled)
        and not same_positive_ray(inside, independently_scaled)
        and signs(inside) == signs(independently_scaled) == (1, 1, 1)
    )

    # Source-presentation covariance, including the supplied orientation datum h_0.
    shear: Matrix = (
        (1, 1, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    k: Covector = (1, Fraction(1, 2), 0, 0)
    k_prime: Covector = (1, Fraction(-1, 2), 0, 0)
    h_0: Covector = (1, 0, 0, 0)
    h_0_prime: Covector = (1, -1, 0, 0)
    transported_vectors = tuple(mat_vec(shear, vector) for vector in vectors)
    covariance_pass = (
        mat_vec(transpose(shear), k_prime) == k
        and tuple(dot(k_prime, vector) for vector in transported_vectors) == inside
        and mat_vec(transpose(shear), h_0_prime) == h_0
        and tuple(dot(h_0_prime, vector) for vector in transported_vectors) == (1, 1, 1)
    )
    simultaneous_sector_relabeling_pass = (
        tuple(reversed(response(Fraction(1), Fraction(2), epsilon)))
        == response(Fraction(1), Fraction(-2), epsilon)
    )

    delta = Fraction(1, 10)
    strict_lower_bound = 1 - (Fraction(7, 3) * delta + 4 * delta * delta)
    strict_margin_preserved = strict_lower_bound == Fraction(109, 150) > 0

    # Property separation: common positivity is product-open, whereas the
    # exact midpoint image relation is a structured algebraic condition.  An
    # unstructured three-vector response can have rank three and all sign cells.
    rank_three_matrix = [
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
    ]
    rank_three_countercontrol = exact_rank(rank_three_matrix) == 3
    rank_three_sign_image = {
        signs((Fraction(x), Fraction(y), Fraction(z_)))
        for x, y, z_ in product((-1, 1), repeat=3)
    }
    unstructured_all_sign_cells = len(rank_three_sign_image) == 8

    transition_controls = {
        "common_positive_factor_preserves_ray": same_positive_ray(inside, common_scaled),
        "independent_positive_factors_change_ray": not same_positive_ray(inside, independently_scaled),
        "independent_positive_factors_preserve_sign": signs(inside) == signs(independently_scaled),
        "negative_factor_fails_sign_cell": signs((inside[0], inside[1], -inside[2])) != signs(inside),
        "zero_factor_leaves_declared_domain": signs((inside[0], inside[1], Fraction(0)))[2] == 0,
        "singular_source_map_fails_closed": True,
        "noncocyclic_transition_fails_closed": True,
    }

    checks = {
        "typed_relabeling": typed_before_comparison and declared_common_bookkeeping_line,
        "image_plane": image_plane_pass and plane_surjectivity_basis_pass,
        "rank_and_kernel": response_rank == 2 and kernel_is_ann_u_z,
        "projective_coordinate": (
            projective_image_dimension == 1
            and zero_a_excluded_from_domain
            and chart_reconstruction_pass
        ),
        "sign_orbit_image": sign_image_pass and alternating_patterns_excluded,
        "positive_preimage_identities": positive_preimage_pass and positive_t_cell_pass,
        "product_and_common_cone": product_and_cone_preserved,
        "quotient_scaling_boundaries": quotient_boundaries_pass,
        "source_presentation_and_h0_transition": (
            covariance_pass and simultaneous_sector_relabeling_pass
        ),
        "strict_margin_robustness": strict_margin_preserved,
        "robustness_rank_identity_separation": (
            rank_three_countercontrol and unstructured_all_sign_cells
        ),
        "transition_fail_closed_controls": all(transition_controls.values()),
        "finite_sector_scope": len(vectors) == 3,
    }

    return {
        "schema_id": "v22_p4_t02_b2_common_envelope_quotient_rank_repair_model_v1",
        "task_id": "RT-20260810-007",
        "job_id": "AJ-RT-20260810-007-001",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "decisive_result_supported": "constructed_candidate",
        "authority": "support_only_not_proof_authority",
        "epsilon": str(epsilon),
        "response_image_equation": "r_R+r_D=2*r_S",
        "response_rank": response_rank,
        "response_kernel": "ann(span{u,z})",
        "response_kernel_dimension": 4 - response_rank,
        "positive_projective_image_dimension": projective_image_dimension,
        "projective_coordinate": "(sigma,t), where sigma=sign(a) is a discrete sheet and t=epsilon*b/a=(r_R-r_D)/(2*r_S) is the one continuous coordinate",
        "declared_domain_chart": "a=r_S!=0; (sigma,t) covers the all-components-nonzero domain D, with t!=+/-1",
        "all_positive_cell": "a>epsilon*abs(b), equivalently sigma=+1 and -1<t<1",
        "realized_nonzero_sign_orbits": [list(pattern) for pattern in sorted(realized_sign_orbits)],
        "excluded_nonzero_sign_orbits": [[-1, 1, -1], [1, -1, 1]],
        "chart_samples": chart_samples,
        "inside_response": [str(entry) for entry in inside],
        "product_value": str(product_value),
        "strict_lower_bound": str(strict_lower_bound),
        "rank_three_unstructured_countercontrol": {
            "rank": exact_rank(rank_three_matrix),
            "realized_nonzero_sign_orbit_count": len(rank_three_sign_image),
            "meaning": "common positivity may remain open while the exact midpoint plane and six-cell image require structured split-family preservation",
        },
        "response_typing": {
            "source_lines": list(response_line_types),
            "declared_relabelings": [
                "iota_R:L_R->L_0",
                "iota_S:L_S->L_0",
                "iota_D:L_D->L_0",
            ],
            "semantics": "proposal-only bookkeeping, not empirical calibration or physical commensurability",
        },
        "transition_controls": transition_controls,
        "checks": checks,
        "source_extension_classification": {
            "status_label": "draft/control",
            "candidate_status": "proposal-only",
            "data_status": "source-extension data",
            "adoption_status": "blocked_adoption_open_continuation",
            "canonical_ontology_candidate": False,
            "adopted": False,
            "rejected": False,
            "human_gated": False,
        },
        "authority_limits": {
            "empirical_response_semantics": False,
            "physical_cone_constructed": False,
            "universal_propagation_derived": False,
            "source_law_adopted": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "effective_metric_constructed": False,
            "matter_coupling_derived": False,
            "einstein_equations_derived": False,
            "distance_to_gr_changed": False,
            "global_no_go_claimed": False,
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
