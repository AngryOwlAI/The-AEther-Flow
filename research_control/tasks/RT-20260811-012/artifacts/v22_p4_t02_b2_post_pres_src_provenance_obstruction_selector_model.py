#!/usr/bin/env python3
"""Exact finite controls for the RT012 post-Pres_src selector.

The executable fixtures are conformance controls.  They do not establish
physical meaning, current-ontology derivation, or a global no-go theorem.
"""

from __future__ import annotations

import itertools
import json
from typing import Hashable, Iterable, Mapping


def factors_through_on_image(
    forgetful: Mapping[Hashable, Hashable],
    output: Mapping[Hashable, Hashable],
) -> bool:
    """Return whether output is constant on every nonempty forgetful fibre."""
    seen: dict[Hashable, Hashable] = {}
    for expansion, reduct in forgetful.items():
        value = output[expansion]
        if reduct in seen and seen[reduct] != value:
            return False
        seen[reduct] = value
    return True


def extension_count(
    image_values: Mapping[Hashable, Hashable],
    full_reducts: Iterable[Hashable],
    codomain: Iterable[Hashable],
) -> int:
    """Count extensions from im(U) to a finite ambient reduct set."""
    unused = set(full_reducts) - set(image_values)
    return len(tuple(codomain)) ** len(unused)


def c2_equivariant_point_selectors() -> list[str]:
    """Enumerate equivariant maps from a trivial singleton to a free C2 orbit."""
    orbit = ("p", "q")
    swap = {"p": "q", "q": "p"}
    return [value for value in orbit if swap[value] == value]


def witness_translation_breaks_finite_invariance(points: set[tuple[int, ...]]) -> tuple[int, ...]:
    """Produce an integer translation that does not preserve a finite nonempty set."""
    if not points:
        raise ValueError("the nonempty finite-set hypothesis is required")
    dimension = len(next(iter(points)))
    if any(len(point) != dimension for point in points):
        raise ValueError("all points must have one dimension")
    first_coordinates = [point[0] for point in points]
    step = max(first_coordinates) - min(first_coordinates) + 1
    translation = (step,) + (0,) * (dimension - 1)
    translated = {
        tuple(point[index] + translation[index] for index in range(dimension))
        for point in points
    }
    assert translated != points
    return translation


def finite_boolean_grammar_counts(max_depth: int = 2) -> list[int]:
    """Close a finite term grammar to bounded depth and return cumulative counts."""
    terms = {"TRUE", "FALSE", "SRC_ATOM"}
    counts = [len(terms)]
    for _ in range(max_depth):
        previous = sorted(terms)
        expanded = set(previous)
        expanded.update(f"NOT({term})" for term in previous)
        expanded.update(
            f"AND({left},{right})"
            for left, right in itertools.combinations_with_replacement(previous, 2)
        )
        terms = expanded
        counts.append(len(terms))
    return counts


def route_selection() -> dict[str, object]:
    routes = [
        {
            "route_id": "A_CANONICAL_REDUCT_EXPANSION_FIBRE_NONSELECTION_THEOREM",
            "admissible_now": True,
            "constructive": False,
            "replays_rt011_if_standalone": True,
        },
        {
            "route_id": "B_SOURCE_INTRINSIC_PRESENTATION_ADMISSION_GENERATOR_EXTENSION",
            "admissible_now": False,
            "constructive": True,
            "replays_rt011_if_standalone": True,
        },
        {
            "route_id": "C_BOUNDED_NATURAL_INVARIANT_ADMISSION_CENSUS",
            "admissible_now": True,
            "constructive": True,
            "replays_rt011_if_standalone": False,
        },
        {
            "route_id": "D_PROTECTED_HUMAN_GATED_ONTOLOGY_STOP",
            "admissible_now": False,
            "constructive": False,
            "replays_rt011_if_standalone": False,
        },
    ]
    admissible = [route for route in routes if route["admissible_now"]]
    constructive = [route for route in admissible if route["constructive"]]
    pool = constructive or admissible
    selected = [route for route in pool if not route["replays_rt011_if_standalone"]]
    assert len(selected) == 1
    return {"routes": routes, "selected_route_id": selected[0]["route_id"]}


def build_receipt() -> dict[str, object]:
    forgetful = {"one_root": "R", "two_root": "R"}
    nonconstant = {"one_root": "one", "two_root": "two"}
    constant = {"one_root": "same", "two_root": "same"}
    finite_sets = [
        {(0, 0, 0, 0)},
        {(0, 0, 0, 0), (1, 0, 0, 0)},
        {(-2, 1, 0, 4), (3, -1, 2, 0), (0, 0, 0, 0)},
    ]
    translations = [witness_translation_breaks_finite_invariance(points) for points in finite_sets]
    counts = finite_boolean_grammar_counts()
    selection = route_selection()

    checks = {
        "nonconstant_output_does_not_factor_on_image": not factors_through_on_image(forgetful, nonconstant),
        "constant_output_factors_on_image": factors_through_on_image(forgetful, constant),
        "factor_on_image_has_two_ambient_extensions_when_U_not_surjective": extension_count({"R": 0}, {"R", "unused"}, {0, 1}) == 2,
        "surjective_U_gives_unique_extension": extension_count({"R": 0}, {"R"}, {0, 1}) == 1,
        "free_C2_orbit_has_no_equivariant_point_selector": c2_equivariant_point_selectors() == [],
        "three_finite_translation_controls_break_invariance": len(translations) == 3,
        "bounded_finite_grammar_counts_are_exact": counts == [3, 12, 93],
        "route_C_selected": selection["selected_route_id"] == "C_BOUNDED_NATURAL_INVARIANT_ADMISSION_CENSUS",
    }
    assert all(checks.values())
    return {
        "schema_id": "v22_p4_t02_b2_post_pres_src_provenance_obstruction_selector_model_receipt_v1",
        "status": "PASS",
        "checks": checks,
        "factorization_scope": "existence and uniqueness on im(U); uniqueness on all Red_src additionally requires surjective U",
        "translation_scope": "finite nonempty subsets under the affine translation action on R^4 only",
        "finite_grammar_counts": counts,
        "translation_witnesses": [list(vector) for vector in translations],
        "selection": selection,
        "authority_limits": {
            "global_no_go_proved": False,
            "current_ontology_derivation_proved": False,
            "selected_packet_executed": False,
            "physical_status_changed": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(build_receipt(), indent=2, sort_keys=True))
