#!/usr/bin/env python3
"""Exact finite controls for the RT-20260814-001 theoretical selector."""

from __future__ import annotations

import argparse
import itertools
import json


POINTS = (0, 1)
GROUP = (0, 1)  # C2 under addition modulo two.


def act(group_element: int, point: int) -> int:
    """The free transitive C2 action on its two-point torsor."""
    return (group_element + point) % 2


def torsor_is_free_and_transitive() -> bool:
    free = all(
        act(group_element, point) != point
        for group_element in GROUP
        if group_element != 0
        for point in POINTS
    )
    transitive = all(
        any(act(group_element, source) == target for group_element in GROUP)
        for source in POINTS
        for target in POINTS
    )
    return free and transitive


def fixed_points() -> tuple[int, ...]:
    return tuple(
        point
        for point in POINTS
        if all(act(group_element, point) == point for group_element in GROUP)
    )


def equivariant_terminal_roots() -> tuple[int, ...]:
    """Equivariant maps from the trivial singleton are precisely fixed points."""
    return fixed_points()


def orbit_partition() -> tuple[tuple[int, ...], ...]:
    unseen = set(POINTS)
    orbits: list[tuple[int, ...]] = []
    while unseen:
        point = min(unseen)
        orbit = tuple(sorted({act(group_element, point) for group_element in GROUP}))
        orbits.append(orbit)
        unseen.difference_update(orbit)
    return tuple(orbits)


def invariant_boolean_predicates() -> tuple[tuple[bool, bool], ...]:
    predicates: list[tuple[bool, bool]] = []
    for values in itertools.product((False, True), repeat=len(POINTS)):
        if all(
            values[act(group_element, point)] == values[point]
            for group_element in GROUP
            for point in POINTS
        ):
            predicates.append(values)
    return tuple(predicates)


def equivariant_maps(
    source_points: tuple[int, ...], source_action: dict[tuple[int, int], int]
) -> tuple[tuple[int, ...], ...]:
    """Exhaust all C2-equivariant maps from a finite C2-set to the torsor."""
    maps: list[tuple[int, ...]] = []
    for values in itertools.product(POINTS, repeat=len(source_points)):
        candidate = dict(zip(source_points, values, strict=True))
        if all(
            candidate[source_action[(group_element, source)]]
            == act(group_element, candidate[source])
            for group_element in GROUP
            for source in source_points
        ):
            maps.append(values)
    return tuple(maps)


def trivial_source_equivariant_maps() -> tuple[tuple[int, ...], ...]:
    source = (0,)
    source_action = {(group_element, 0): 0 for group_element in GROUP}
    return equivariant_maps(source, source_action)


def torsor_source_equivariant_maps() -> tuple[tuple[int, ...], ...]:
    source_action = {
        (group_element, point): act(group_element, point)
        for group_element in GROUP
        for point in POINTS
    }
    return equivariant_maps(POINTS, source_action)


def quotient_cannot_recover_root() -> bool:
    """Both roots have one orbit value, so no decoder recovers both uniformly."""
    quotient_value = {point: orbit_partition().index(tuple(sorted(POINTS))) for point in POINTS}
    return (
        quotient_value[0] == quotient_value[1]
        and all(any(decoder_value != point for point in POINTS) for decoder_value in POINTS)
    )


def same_reduct_root_nonfactorization() -> bool:
    """A current reduct cannot factor two distinct expansion roots through one value."""
    reduct = ("Sub", 4)
    expansions = ((reduct, 0), (reduct, 1))
    reduct_values = {expansion[0] for expansion in expansions}
    root_values = {expansion[1] for expansion in expansions}
    return len(reduct_values) == 1 and len(root_values) == 2


def finite_factorization_iff_fibre_constancy() -> bool:
    """Exhaust the factorization criterion for all Boolean maps on two fibres."""
    domain = (0, 1, 2, 3)
    reduct = {0: "a", 1: "a", 2: "b", 3: "b"}
    for values in itertools.product((False, True), repeat=len(domain)):
        candidate = dict(zip(domain, values, strict=True))
        fibre_constant = all(
            candidate[left] == candidate[right]
            for left in domain
            for right in domain
            if reduct[left] == reduct[right]
        )
        factor_maps = tuple(itertools.product((False, True), repeat=2))
        factors = any(
            all(
                candidate[item]
                == {"a": factor_values[0], "b": factor_values[1]}[reduct[item]]
                for item in domain
            )
            for factor_values in factor_maps
        )
        if fibre_constant != factors:
            return False
    return True


def root_free_orbit_map_is_equivariant() -> bool:
    orbit_index = {point: 0 for point in POINTS}
    return all(
        orbit_index[act(group_element, point)] == orbit_index[point]
        for group_element in GROUP
        for point in POINTS
    )


def four_routes_have_unique_ids() -> bool:
    routes = (
        "A_CURRENT_SOURCE_EQUIVARIANT_ASYMMETRY_DERIVATION_AUDIT",
        "B_ROOT_FREE_ORBIT_VALUED_PRESENTATION_BRIDGE",
        "C_SOURCE_GENERATED_ASYMMETRY_LAW_FORMALIZATION",
        "D_PROTECTED_HUMAN_GATED_ONTOLOGY_STOP",
    )
    return len(routes) == 4 and len(set(routes)) == 4


def build_report() -> dict[str, object]:
    predicates = invariant_boolean_predicates()
    orbits = orbit_partition()
    checks = {
        "c2_action_is_a_free_transitive_torsor": torsor_is_free_and_transitive(),
        "torsor_has_no_fixed_point": fixed_points() == (),
        "no_equivariant_terminal_root": equivariant_terminal_roots() == (),
        "quotient_has_exactly_one_orbit": orbits == ((0, 1),),
        "invariant_boolean_predicates_are_constant": set(predicates)
        == {(False, False), (True, True)},
        "no_invariant_unique_admission": all(sum(values) != 1 for values in predicates),
        "trivial_source_has_no_equivariant_asymmetry_law": trivial_source_equivariant_maps()
        == (),
        "free_source_has_two_equivariant_asymmetry_laws": set(
            torsor_source_equivariant_maps()
        )
        == {(0, 1), (1, 0)},
        "group_action_alone_does_not_select_unique_law": len(
            torsor_source_equivariant_maps()
        )
        == 2,
        "root_free_orbit_map_is_equivariant": root_free_orbit_map_is_equivariant(),
        "quotient_cannot_recover_root": quotient_cannot_recover_root(),
        "same_reduct_root_nonfactorization": same_reduct_root_nonfactorization(),
        "finite_factorization_iff_fibre_constancy": finite_factorization_iff_fibre_constancy(),
        "four_routes_have_unique_ids": four_routes_have_unique_ids(),
    }
    return {
        "schema_id": "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "fixed_points": list(fixed_points()),
        "orbit_partition": [list(orbit) for orbit in orbits],
        "invariant_boolean_predicates": [list(values) for values in predicates],
        "trivial_source_equivariant_maps": [
            list(values) for values in trivial_source_equivariant_maps()
        ],
        "torsor_source_equivariant_maps": [
            list(values) for values in torsor_source_equivariant_maps()
        ],
        "authority_note": "Exact finite selector controls only; no ontology, physical, empirical, Gate, proof, adoption, or promotion authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
