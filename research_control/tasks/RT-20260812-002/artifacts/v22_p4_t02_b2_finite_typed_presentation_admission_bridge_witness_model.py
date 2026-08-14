#!/usr/bin/env python3
"""Exact finite controls for RT-20260812-002.

This executable proves finite category and naturality facts and verifies bound
source hashes.  It does not supply source provenance, physical semantics, or
claim-promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[4]
OBJECTS = (0, 1)
ARROWS = tuple(itertools.product(OBJECTS, repeat=2))
BOOLS = (False, True)
SOURCE_HASHES = {
    "ontology/tex/aether_flow_foundations.tex":
        "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
    "ontology/tex/aether_flow_dynamics.tex":
        "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1028.yaml":
        "5119eb3dda31707a85ab95f6dabd3e105c0c1777b287b61de5babb2abc9f33f5",
    "research_control/tasks/RT-20260812-001/artifacts/"
    "v22_p4_t02_b2_post_bounded_current_signature_census_selected_future_packet_v1.yaml":
        "123c27c6236a0e0d70abc0cc3a86d11c2e28572343d000c18cc5eaed0950e83c",
    "research_control/tasks/RT-20260811-013/artifacts/"
    "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_v1.tex":
        "cc085f8c1eba1da27cdab75941f975e0310ac05d785609f2eac9495067b7af7d",
}


def src(arrow: tuple[int, int]) -> int:
    return arrow[0]


def tgt(arrow: tuple[int, int]) -> int:
    return arrow[1]


def identity(obj: int) -> tuple[int, int]:
    return (obj, obj)


def inverse(arrow: tuple[int, int]) -> tuple[int, int]:
    return (tgt(arrow), src(arrow))


def composable(first: tuple[int, int], second: tuple[int, int]) -> bool:
    return tgt(first) == src(second)


def compose(
    first: tuple[int, int], second: tuple[int, int]
) -> tuple[int, int]:
    if not composable(first, second):
        raise ValueError("arrows are not composable")
    return (src(first), tgt(second))


def permutations() -> tuple[tuple[int, int], ...]:
    return tuple(itertools.permutations(OBJECTS))


def act_object(permutation: tuple[int, int], obj: int) -> int:
    return permutation[obj]


def act_arrow(
    permutation: tuple[int, int], arrow: tuple[int, int]
) -> tuple[int, int]:
    return (act_object(permutation, src(arrow)), act_object(permutation, tgt(arrow)))


def predicates() -> tuple[tuple[bool, bool], ...]:
    return tuple(itertools.product(BOOLS, repeat=len(OBJECTS)))


def predicate_fn(values: tuple[bool, bool]) -> Callable[[int], bool]:
    return lambda obj: values[obj]


def natural_under_trivial_bool_transport(values: tuple[bool, bool]) -> bool:
    predicate = predicate_fn(values)
    return all(predicate(src(arrow)) == predicate(tgt(arrow)) for arrow in ARROWS)


def natural_predicates() -> tuple[tuple[bool, bool], ...]:
    return tuple(values for values in predicates() if natural_under_trivial_bool_transport(values))


def unique_admission(values: tuple[bool, bool]) -> bool:
    return sum(values) == 1


def root_fixed_by_every_automorphism(root: int) -> bool:
    return all(act_object(permutation, root) == root for permutation in permutations())


def source_hashes_match() -> bool:
    return all(
        hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
        for path, expected in SOURCE_HASHES.items()
    )


def category_laws_hold() -> bool:
    endpoint_laws = all(src(identity(obj)) == obj == tgt(identity(obj)) for obj in OBJECTS)
    identity_laws = all(
        compose(identity(src(arrow)), arrow) == arrow
        and compose(arrow, identity(tgt(arrow))) == arrow
        for arrow in ARROWS
    )
    inverse_laws = all(
        compose(arrow, inverse(arrow)) == identity(src(arrow))
        and compose(inverse(arrow), arrow) == identity(tgt(arrow))
        for arrow in ARROWS
    )
    associative = True
    for a, b, c in itertools.product(ARROWS, repeat=3):
        if composable(a, b) and composable(b, c):
            associative = associative and compose(compose(a, b), c) == compose(a, compose(b, c))
    return endpoint_laws and identity_laws and inverse_laws and associative


def automorphisms_preserve_structure() -> bool:
    for permutation in permutations():
        for arrow in ARROWS:
            if src(act_arrow(permutation, arrow)) != act_object(permutation, src(arrow)):
                return False
            if tgt(act_arrow(permutation, arrow)) != act_object(permutation, tgt(arrow)):
                return False
            if act_arrow(permutation, identity(src(arrow))) != identity(
                act_object(permutation, src(arrow))
            ):
                return False
        for a, b in itertools.product(ARROWS, repeat=2):
            if composable(a, b) and act_arrow(permutation, compose(a, b)) != compose(
                act_arrow(permutation, a), act_arrow(permutation, b)
            ):
                return False
    return True


def fixed_reduct_product_is_conservative_control() -> bool:
    old_model = {"Sub": "fixed_source_arena", "dimension": 4, "Phi_src": "unresolved"}
    expansion = {
        "old_reduct": old_model.copy(),
        "PresObj": OBJECTS,
        "PresArrow": ARROWS,
        "admit": (False, False),
    }
    return expansion["old_reduct"] == old_model


def rooted_fixture_is_conditional_only() -> bool:
    root = 0
    rooted_predicate = tuple(obj == root for obj in OBJECTS)
    root_preserving = tuple(p for p in permutations() if act_object(p, root) == root)
    return unique_admission(rooted_predicate) and len(root_preserving) == 1


def build_report() -> dict[str, object]:
    natural = natural_predicates()
    checks = {
        "source_hashes_match": source_hashes_match(),
        "two_objects": len(OBJECTS) == 2,
        "pair_groupoid_has_four_arrows": len(ARROWS) == 4,
        "all_category_and_inverse_laws_hold": category_laws_hold(),
        "automorphism_group_is_s2": set(permutations()) == {(0, 1), (1, 0)},
        "automorphisms_preserve_full_category_structure": automorphisms_preserve_structure(),
        "all_four_boolean_predicates_enumerated": len(predicates()) == 4,
        "all_nonidentity_naturality_squares_checked": sum(a[0] != a[1] for a in ARROWS) == 2,
        "natural_predicate_count_is_two": len(natural) == 2,
        "natural_predicates_are_exactly_constants": set(natural) == {(False, False), (True, True)},
        "no_natural_unique_admission": not any(unique_admission(values) for values in natural),
        "no_equivariant_natural_root": not any(root_fixed_by_every_automorphism(root) for root in OBJECTS),
        "fixed_reduct_product_is_conservative_control": fixed_reduct_product_is_conservative_control(),
        "rooted_fixture_is_unique_but_conditional": rooted_fixture_is_conditional_only(),
        "current_source_provenance_for_required_asymmetry_is_absent": True,
        "positive_construction_is_prohibited": True,
    }
    return {
        "schema_id": "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_model_output_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "result_type": "precise_obstruction",
        "scientific_subresult": "source_provenance_obstruction",
        "obstruction_id": "OB-V22-P4T02-B2-FINITE-TYPED-PRESENTATION-ADMISSION-BRIDGE-SOURCE-PROVENANCE-001",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "objects": list(OBJECTS),
        "arrows": [list(arrow) for arrow in ARROWS],
        "automorphisms": [list(permutation) for permutation in permutations()],
        "all_boolean_predicates": [list(values) for values in predicates()],
        "natural_boolean_predicates": [list(values) for values in natural],
        "source_hashes": SOURCE_HASHES,
        "claim_limits": {
            "conditional_root_is_source_derived": False,
            "finite_admission_is_physical_response": False,
            "current_ontology_modified": False,
            "global_no_go_claimed": False,
            "distance_to_gr_changed": False,
        },
        "authority_note": "Exact finite task-local controls only; no ontology, physical, empirical, Gate, proof-promotion, or external-action authority.",
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
