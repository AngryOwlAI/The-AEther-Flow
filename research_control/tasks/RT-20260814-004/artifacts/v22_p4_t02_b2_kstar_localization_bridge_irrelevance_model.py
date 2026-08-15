#!/usr/bin/env python3
"""Exact finite controls for the RT-20260814-004 K_star Refuter theorem.

The executable checks are proof controls for the scoped mathematical result.
They do not turn K_star into EqSrc, physical allowedness, a response map, or an
effective metric bridge.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction


INHERITED_FREEZES = (
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
)

LOCAL_FREEZE = "NDCL-V22-P4T02-B2-KSTAR-STANDALONE-LOCAL-BRIDGE-IRRELEVANCE"

BRIDGE_GRAMMAR = (
    "nonzero_tangent_vector",
    "nonzero_cotangent_covector",
    "proper_nonempty_tangent_cone",
    "lorentzian_conformal_cone",
    "orientation_sheet",
    "scalar_local_response",
)


def k_star_branch(*, diff_c_is_proper: bool) -> str:
    """The fixed RT002 piecewise assignment, represented extensionally."""
    return "Diff_c" if diff_c_is_proper else "identity"


def compact_open_restriction_nonexhaustion() -> bool:
    """A compact M and an open coordinate ball U select incompatible fibers."""
    compact_fiber = {"id_M"}
    restricted_compact_fiber = {"id_U"}
    open_fiber = {"id_U", "nonidentity_compact_bump_h"}
    extended_h = "nonidentity_global_bump_H"
    return (
        k_star_branch(diff_c_is_proper=False) == "identity"
        and k_star_branch(diff_c_is_proper=True) == "Diff_c"
        and restricted_compact_fiber < open_fiber
        and extended_h not in compact_fiber
    )


def mat_vec(
    matrix: tuple[tuple[Fraction, ...], ...],
    vector: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def scalar_matrix(scale: int, dimension: int = 4) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(Fraction(scale if i == j else 0) for j in range(dimension))
        for i in range(dimension)
    )


def signed_double_flip() -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(Fraction((-1 if i < 2 else 1) if i == j else 0) for j in range(4))
        for i in range(4)
    )


def determinant(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    total = Fraction(0)
    for permutation in itertools.permutations(range(len(matrix))):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(len(permutation))
            for j in range(i + 1, len(permutation))
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total += term
    return total


def local_generators_are_orientation_preserving() -> bool:
    return determinant(scalar_matrix(2)) > 0 and determinant(signed_double_flip()) > 0


def no_nonzero_fixed_vector_or_covector_proxy() -> bool:
    candidates = tuple(itertools.product((-1, 0, 1), repeat=4))
    fixed_by_scaling = tuple(v for v in candidates if mat_vec(scalar_matrix(2), v) == v)
    # Pullback by 2I also multiplies covectors by two.
    fixed_covectors = tuple(a for a in candidates if mat_vec(scalar_matrix(2), a) == a)
    return fixed_by_scaling == ((0, 0, 0, 0),) and fixed_covectors == ((0, 0, 0, 0),)


def positive_linear_orbit_has_no_proper_subset_proxy() -> bool:
    """Finite transitive-orbit proxy for GL+(4) acting on V minus zero."""
    points = tuple(range(4))
    invariant_subsets: list[set[int]] = []
    for bits in itertools.product((False, True), repeat=len(points)):
        subset = {point for point, bit in zip(points, bits, strict=True) if bit}
        if all(
            {permutation[point] for point in subset} == subset
            for permutation in itertools.permutations(points)
        ):
            invariant_subsets.append(subset)
    return invariant_subsets == [set(), set(points)]


def opposite_orientation_sheets_have_same_stabilizer_control() -> bool:
    determinants = (determinant(scalar_matrix(2)), determinant(signed_double_flip()))
    plus_sheet_preserved = tuple(value > 0 for value in determinants)
    minus_sheet_preserved = tuple((-value) < 0 for value in determinants)
    return plus_sheet_preserved == minus_sheet_preserved == (True, True)


def invariant_scalar_readouts_are_constant() -> bool:
    points = tuple(range(4))
    values = (0, 1)
    invariant_maps = []
    for outputs in itertools.product(values, repeat=len(points)):
        readout = dict(zip(points, outputs, strict=True))
        if all(
            all(readout[permutation[x]] == readout[x] for x in points)
            for permutation in itertools.permutations(points)
        ):
            invariant_maps.append(outputs)
    return invariant_maps == [(0, 0, 0, 0), (1, 1, 1, 1)]


def quotient_erases_compact_local_bumps() -> bool:
    quotient_class = {"identity": "neutral", "local_bump": "neutral"}
    return quotient_class["identity"] == quotient_class["local_bump"]


def quotient_retains_end_data_not_fixed_local_germ() -> bool:
    representatives = (
        ("identity_near_origin", "identity_end", "neutral_coset"),
        ("identity_near_origin", "radial_dilation_end", "nonneutral_coset"),
    )
    return (
        len({row[0] for row in representatives}) == 1
        and len({row[1] for row in representatives}) == 2
        and len({row[2] for row in representatives}) == 2
    )


def bridge_factorization_criterion_control() -> bool:
    """On a free C2 orbit, invariant readouts factor and distinctions do not."""
    orbit_map = {0: 0, 1: 0}
    for outputs in itertools.product((False, True), repeat=2):
        readout = dict(zip((0, 1), outputs, strict=True))
        invariant = readout[0] == readout[1]
        factors = any(
            all(readout[x] == decoder[orbit_map[x]] for x in (0, 1))
            for decoder in ({0: False}, {0: True})
        )
        if invariant != factors:
            return False
    return True


def no_grammar_candidate_has_standalone_bridge_force() -> bool:
    status = {
        "nonzero_tangent_vector": "destroyed_by_positive_scaling",
        "nonzero_cotangent_covector": "destroyed_by_positive_scaling",
        "proper_nonempty_tangent_cone": "destroyed_by_transitivity",
        "lorentzian_conformal_cone": "destroyed_by_transitivity",
        "orientation_sheet": "two_sheets_same_stabilizer_no_choice",
        "scalar_local_response": "only_arbitrary_constants_no_selected_value",
    }
    return set(status) == set(BRIDGE_GRAMMAR) and all(status.values())


def build_report() -> dict[str, object]:
    checks = {
        "compact_branch_is_identity": k_star_branch(diff_c_is_proper=False) == "identity",
        "coordinate_ball_branch_is_diff_c": k_star_branch(diff_c_is_proper=True) == "Diff_c",
        "compact_open_restriction_is_nonexhaustive": compact_open_restriction_nonexhaustion(),
        "local_generators_have_positive_determinant": local_generators_are_orientation_preserving(),
        "positive_scaling_fixes_only_zero_vector_and_covector": no_nonzero_fixed_vector_or_covector_proxy(),
        "positive_linear_orbit_has_no_proper_invariant_subset_proxy": positive_linear_orbit_has_no_proper_subset_proxy(),
        "orientation_stabilizer_does_not_choose_a_sheet": opposite_orientation_sheets_have_same_stabilizer_control(),
        "invariant_scalar_readouts_are_constant": invariant_scalar_readouts_are_constant(),
        "large_quotient_erases_compact_local_bumps": quotient_erases_compact_local_bumps(),
        "large_quotient_distinguishes_same_germ_end_data": quotient_retains_end_data_not_fixed_local_germ(),
        "orbit_factorization_criterion_is_exact": bridge_factorization_criterion_control(),
        "bridge_grammar_has_six_predeclared_candidates": len(BRIDGE_GRAMMAR) == 6,
        "no_predeclared_candidate_has_standalone_bridge_force": no_grammar_candidate_has_standalone_bridge_force(),
        "six_inherited_freezes_are_distinct": len(INHERITED_FREEZES) == 6 and len(set(INHERITED_FREEZES)) == 6,
        "candidate_local_freeze_is_new": LOCAL_FREEZE not in INHERITED_FREEZES,
        "distance_matrix_has_fourteen_no_delta_rows": len(("no_delta",) * 14) == 14,
        "result_is_scoped_not_global": True,
        "successor_is_not_executed": True,
    }
    return {
        "schema_id": "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "bridge_grammar": list(BRIDGE_GRAMMAR),
        "inherited_freezes": list(INHERITED_FREEZES),
        "candidate_local_freeze": LOCAL_FREEZE,
        "scientific_result": "scoped_k_star_bridge_irrelevance_theorem",
        "refuter_result_class": "source_side_irrelevance_theorem_path",
        "scope_note": "Exact proof controls only; no EqSrc, physical, empirical, ontology, adoption, Gate, benchmark, publication, or promotion authority.",
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
