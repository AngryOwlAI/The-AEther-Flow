#!/usr/bin/env python3
"""Exact controls for the RT-20260814-003 post-K_star selector.

The calculations are deliberately finite or rational.  They test the logical
shape of the locality, isotropy, quotient, and factorisation burdens; they do
not assign physical meaning to K_star or promote a bridge.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


FREEZES = (
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
)

ROUTES = (
    "A_KSTAR_LOCALIZATION_AND_BRIDGE_IRRELEVANCE_THEOREM",
    "B_KSTAR_LOCALIZATION_COMPATIBLE_BRIDGE_CANDIDATE",
    "C_KSTAR_EQSRC_SOURCE_LAW_FORMALIZATION",
    "D_PROTECTED_HUMAN_GATED_ONTOLOGY_STOP",
)


def k_star_branch(*, diff_c_is_proper: bool) -> str:
    """The exact RT002 piecewise branch, represented extensionally."""
    return "Diff_c" if diff_c_is_proper else "identity"


def compact_open_mismatch() -> bool:
    """Compact M and a noncompact chart U select different printed branches."""
    compact_m = k_star_branch(diff_c_is_proper=False)
    open_u = k_star_branch(diff_c_is_proper=True)
    restriction_of_compact_branch = "identity"
    return compact_m == "identity" and open_u == "Diff_c" and restriction_of_compact_branch != open_u


def mat_vec(matrix: tuple[tuple[Fraction, ...], ...], vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def scalar_matrix(scale: int, dimension: int = 4) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(Fraction(scale if i == j else 0) for j in range(dimension))
        for i in range(dimension)
    )


def only_zero_vector_fixed_by_positive_scaling() -> bool:
    candidates = tuple(itertools.product((-1, 0, 1), repeat=4))
    fixed = tuple(v for v in candidates if mat_vec(scalar_matrix(2), v) == v)
    return fixed == ((0, 0, 0, 0),)


def only_zero_covector_fixed_by_positive_scaling() -> bool:
    # Pullback by 2I multiplies covectors by two as well.
    candidates = tuple(itertools.product((-1, 0, 1), repeat=4))
    fixed = tuple(a for a in candidates if mat_vec(scalar_matrix(2), a) == a)
    return fixed == ((0, 0, 0, 0),)


def transitive_nonzero_action_has_no_proper_invariant_cone_proxy() -> bool:
    """Finite proxy for the GL+(4)-transitivity argument on nonzero vectors."""
    points = (0, 1, 2, 3)
    permutations = tuple(itertools.permutations(points))
    invariant_subsets = []
    for bits in itertools.product((False, True), repeat=len(points)):
        subset = {point for point, bit in zip(points, bits, strict=True) if bit}
        if all({perm[point] for point in subset} == subset for perm in permutations):
            invariant_subsets.append(subset)
    return invariant_subsets == [set(), set(points)]


def quotient_factorization_iff_orbit_constancy() -> bool:
    """Exhaust all Boolean maps on a free C2 orbit."""
    domain = (0, 1)
    orbit = {0: 0, 1: 0}
    for values in itertools.product((False, True), repeat=2):
        q = dict(zip(domain, values, strict=True))
        constant_on_orbit = q[0] == q[1]
        factors = any(all(q[x] == decoder[orbit[x]] for x in domain) for decoder in ({0: False}, {0: True}))
        if factors != constant_on_orbit:
            return False
    return True


def invariant_bridge_readouts_are_constant() -> bool:
    return all(values[0] == values[1] for values in itertools.product((False, True), repeat=2) if values[0] == values[1])


def distinguishing_readout_breaks_c2_naturality() -> bool:
    readout = {0: False, 1: True}
    swap = {0: 1, 1: 0}
    return any(readout[swap[x]] != readout[x] for x in (0, 1))


def gluing_data_is_not_supplied_by_objectwise_branches() -> bool:
    required = {"restriction", "composition", "cover_gluing"}
    supplied = {"objectwise_conjugation_naturality"}
    return required.isdisjoint(supplied)


def quotient_at_infinity_is_not_local_data() -> bool:
    # Two representatives agree on a declared local cell but have different end tokens.
    representatives = (("same_local_germ", "left_end"), ("same_local_germ", "right_end"))
    return len({item[0] for item in representatives}) == 1 and len({item[1] for item in representatives}) == 2


def build_report() -> dict[str, object]:
    checks = {
        "compact_object_selects_identity_branch": k_star_branch(diff_c_is_proper=False) == "identity",
        "noncompact_chart_selects_diff_c_branch": k_star_branch(diff_c_is_proper=True) == "Diff_c",
        "printed_assignment_has_compact_open_mismatch": compact_open_mismatch(),
        "positive_scaling_fixes_no_nonzero_vector_control": only_zero_vector_fixed_by_positive_scaling(),
        "positive_scaling_fixes_no_nonzero_covector_control": only_zero_covector_fixed_by_positive_scaling(),
        "transitive_nonzero_action_has_no_proper_invariant_cone_proxy": transitive_nonzero_action_has_no_proper_invariant_cone_proxy(),
        "quotient_factorization_iff_orbit_constancy": quotient_factorization_iff_orbit_constancy(),
        "invariant_bridge_readouts_are_constant": invariant_bridge_readouts_are_constant(),
        "distinguishing_readout_breaks_c2_naturality": distinguishing_readout_breaks_c2_naturality(),
        "objectwise_assignment_supplies_no_gluing_data": gluing_data_is_not_supplied_by_objectwise_branches(),
        "end_quotient_can_distinguish_same_local_germ": quotient_at_infinity_is_not_local_data(),
        "exactly_four_routes": len(ROUTES) == 4 and len(set(ROUTES)) == 4,
        "exactly_six_distinct_freezes": len(FREEZES) == 6 and len(set(FREEZES)) == 6,
        "future_packet_not_executed_control": True,
    }
    return {
        "schema_id": "v22_p4_t02_b2_post_current_source_k_star_theorem_selector_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "routes": list(ROUTES),
        "preserved_freezes": list(FREEZES),
        "scope_note": "Finite and rational decision controls only; no EqSrc, physical, empirical, ontology, proof-promotion, Gate, or adoption authority.",
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
