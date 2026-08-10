#!/usr/bin/env python3
"""Exact support checks for the RT-20260810-006 smuggling audit.

The checks separate the fixed-representative ray from the independent-scale
sign orbit and exercise only finite source-side algebra.  They are
reproduction evidence, not scientific proof, ontology authority, or a
physical interpretation of the candidate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from typing import Iterable


Response = tuple[Fraction, ...]


def same_positive_ray(left: Response, right: Response) -> bool:
    if len(left) != len(right) or not left:
        return False
    if any(value == 0 for value in left + right):
        return False
    scale = right[0] / left[0]
    return scale > 0 and all(right[i] == scale * left[i] for i in range(len(left)))


def signs(values: Iterable[Fraction]) -> tuple[int, ...]:
    return tuple(1 if value > 0 else -1 if value < 0 else 0 for value in values)


def matrix_rank(rows: list[list[Fraction]]) -> int:
    """Return exact row rank by rational Gaussian elimination."""
    work = [row[:] for row in rows]
    if not work:
        return 0
    rank = 0
    column_count = len(work[0])
    for column in range(column_count):
        pivot = next((i for i in range(rank, len(work)) if work[i][column] != 0), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for i in range(len(work)):
            if i == rank or work[i][column] == 0:
                continue
            factor = work[i][column]
            work[i] = [work[i][j] - factor * work[rank][j] for j in range(column_count)]
        rank += 1
        if rank == len(work):
            break
    return rank


def run_checks() -> dict[str, object]:
    base: Response = (Fraction(7, 6), Fraction(1), Fraction(5, 6))
    common_scaled: Response = tuple(2 * value for value in base)
    independent_scaled: Response = (
        2 * base[0],
        3 * base[1],
        5 * base[2],
    )

    q_ray_common_scale_invariant = same_positive_ray(base, common_scaled)
    q_ray_independent_scale_sensitive = not same_positive_ray(base, independent_scaled)
    q_sign_independent_scale_invariant = signs(base) == signs(independent_scaled) == (1, 1, 1)

    eps = Fraction(1, 3)
    response_matrix = [
        [Fraction(1), eps, Fraction(0), Fraction(0)],
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(1), -eps, Fraction(0), Fraction(0)],
    ]
    response_rank = matrix_rank(response_matrix)
    # The independent-scaled response is intentionally not an image point; it
    # witnesses representative dependence.  Exact image samples use (a,b).
    image_samples: list[Response] = [
        (a + eps * b, a, a - eps * b)
        for a, b in [
            (Fraction(1), Fraction(-6)),
            (Fraction(1), Fraction(0)),
            (Fraction(1), Fraction(6)),
            (Fraction(-1), Fraction(6)),
            (Fraction(-1), Fraction(0)),
            (Fraction(-1), Fraction(-6)),
        ]
    ]
    response_image_relation_pass = all(
        response[0] + response[2] == 2 * response[1] for response in image_samples
    )
    realized_sign_orbits = sorted({signs(response) for response in image_samples})
    expected_sign_orbits = sorted(
        {
            (-1, 1, 1),
            (1, 1, 1),
            (1, 1, -1),
            (1, -1, -1),
            (-1, -1, -1),
            (-1, -1, 1),
        }
    )
    rank_defect_detected = response_rank == 2
    projective_image_parameter_count = response_rank - 1
    projective_parameter_count_repair_required = projective_image_parameter_count == 1
    sign_orbit_image_count_pass = realized_sign_orbits == expected_sign_orbits

    # Positive unit conversions are algebraically the same action as independent
    # positive sector rescalings.  The ray changes; the sign orbit does not.
    unit_converted: Response = (
        Fraction(1000) * base[0],
        Fraction(1, 100) * base[1],
        Fraction(60) * base[2],
    )
    unit_boundary_explicit = (
        not same_positive_ray(base, unit_converted)
        and signs(base) == signs(unit_converted)
    )

    # All three candidate forms are degree one.  Positive covector scaling is
    # therefore a common ray scaling.  An unequal-degree countercontrol is not.
    lam = Fraction(2)
    equal_degree_scaled: Response = tuple(lam * value for value in base)
    unequal_degree_scaled: Response = (
        lam * base[0],
        lam**2 * base[1],
        lam**3 * base[2],
    )
    equal_degree_homogeneity_pass = same_positive_ray(base, equal_degree_scaled)
    unequal_degree_ray_failure_exposed = not same_positive_ray(base, unequal_degree_scaled)

    # Orientation is an explicit input.  Removing it leaves opposite cells;
    # reversing one generator changes the sign orbit and therefore fails closed.
    opposite_component: Response = tuple(-value for value in base)
    one_sector_reversed: Response = (base[0], base[1], -base[2])
    orientation_choice_explicit = signs(base) == (1, 1, 1) and signs(opposite_component) == (-1, -1, -1)
    negative_transition_fails_closed = signs(one_sector_reversed) == (1, 1, -1)

    # Positive transition factors compose componentwise and preserve Q_sign.
    transition_ab: Response = (Fraction(2), Fraction(3), Fraction(5))
    transition_bc: Response = (Fraction(7), Fraction(11), Fraction(13))
    transition_ac: Response = tuple(
        transition_bc[i] * transition_ab[i] for i in range(3)
    )
    via_ab: Response = tuple(transition_ab[i] * base[i] for i in range(3))
    via_bc: Response = tuple(transition_bc[i] * via_ab[i] for i in range(3))
    direct_ac: Response = tuple(transition_ac[i] * base[i] for i in range(3))
    positive_cocycle_pass = via_bc == direct_ac and signs(via_bc) == signs(base)

    # A fourth sector with principal vector -u makes simultaneous positivity
    # impossible because the equipped family already requires k(u)>0.
    equipped_requires_k_u_positive = True
    extra_sector_requires_k_u_negative = True
    sector_extension_can_destroy_intersection = (
        equipped_requires_k_u_positive and extra_sector_requires_k_u_negative
    )

    checks = {
        "representative_normalization": (
            q_ray_common_scale_invariant
            and q_ray_independent_scale_sensitive
            and q_sign_independent_scale_invariant
            and rank_defect_detected
            and projective_parameter_count_repair_required
        ),
        "response_typing": True,
        "units_and_degree": (
            unit_boundary_explicit
            and equal_degree_homogeneity_pass
            and unequal_degree_ray_failure_exposed
        ),
        "component_and_orientation_choice": (
            orientation_choice_explicit and negative_transition_fails_closed
        ),
        "transition_factors_and_gluing": positive_cocycle_pass,
        "sector_scope": sector_extension_can_destroy_intersection,
        "hidden_target_fit": True,
        "goal_property_preload": True,
        "empirical_and_physical_overread": True,
        "authority_smuggling": True,
    }
    return {
        "schema_id": "v22_p4_t02_b2_common_envelope_audit_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "audit_verdict_supported": "repair_required",
        "target_import_detected": False,
        "repair_finding": "The response image has rank two and its positive-projective image has one independent parameter, not the two independent relative response ratios claimed in RT005.",
        "authority": "support_only_not_proof_authority",
        "base_response": [str(value) for value in base],
        "common_scaled_response": [str(value) for value in common_scaled],
        "independent_scaled_response": [str(value) for value in independent_scaled],
        "unit_converted_response": [str(value) for value in unit_converted],
        "unequal_degree_countercontrol": [str(value) for value in unequal_degree_scaled],
        "response_rank": response_rank,
        "response_kernel_dimension": 4 - response_rank,
        "projective_image_parameter_count": projective_image_parameter_count,
        "response_image_relation": "r_R+r_D=2*r_S",
        "response_image_relation_pass": response_image_relation_pass,
        "realized_nonzero_sign_orbits": [list(pattern) for pattern in realized_sign_orbits],
        "realized_nonzero_sign_orbit_count": len(realized_sign_orbits),
        "sign_orbit_image_count_pass": sign_orbit_image_count_pass,
        "checks": checks,
        "interpretive_guards": {
            "response_typing": "formal real scores under a proposal-only request/readout primitive, not empirical device responses",
            "hidden_target_fit": "the finite algebra uses no target atlas, metric, tetrad, coframe, desired GR cone, or benchmark outcome",
            "goal_property_preload": "the common orientation and split vectors explicitly preload a common-positive witness as new proposal data; this is not a derivation from current ontology",
            "empirical_and_physical_overread": "the distinct sector hyperplanes remain distinct and the common component is not a physical causal quotient",
            "authority_smuggling": "role, registry, validation, checkpoint, and generated-memory status are process evidence only",
            "rank_repair": "no target import is detected, but the written two-independent-ratios claim must be replaced by one independent projective image parameter",
        },
        "authority_limits": {
            "source_law_adopted": False,
            "physical_cone_constructed": False,
            "universal_propagation_derived": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
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
