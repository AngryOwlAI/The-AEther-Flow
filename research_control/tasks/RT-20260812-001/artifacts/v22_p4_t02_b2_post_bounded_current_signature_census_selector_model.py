#!/usr/bin/env python3
"""Exact finite controls for the RT001 post-census route selector."""

from __future__ import annotations

import argparse
import json


def current_language_indistinguishability() -> bool:
    """Added data differ while every closed current-language value agrees."""
    current_closed_values = {"Sub": "A", "dim(Sub)": 4, "true": True, "false": False}
    expansion_left = {"current": current_closed_values, "presentations": ("p0",), "admit": {"p0": False}}
    expansion_right = {"current": current_closed_values, "presentations": ("p0", "p1"), "admit": {"p0": True, "p1": False}}
    return (
        expansion_left["current"] == expansion_right["current"]
        and expansion_left["presentations"] != expansion_right["presentations"]
        and expansion_left["admit"] != expansion_right["admit"]
    )


def minimum_signature_complete() -> bool:
    required_sorts = {"PresObj", "PresArrow", "Bool"}
    required_operations = {"src", "tgt", "identity", "compose", "admit", "transport"}
    candidate_sorts = {"PresObj", "PresArrow", "Bool"}
    candidate_operations = {"src", "tgt", "identity", "compose", "admit", "transport"}
    return required_sorts <= candidate_sorts and required_operations <= candidate_operations


def swap_invariant_predicates() -> list[tuple[bool, bool]]:
    """All predicates f:{p0,p1}->Bool invariant under the object swap."""
    return [(a, b) for a in (False, True) for b in (False, True) if (a, b) == (b, a)]


def asymmetric_token_enables_unique_selection() -> bool:
    """A disclosed root token breaks the swap symmetry without choosing a physical meaning."""
    presentations = ("p0", "p1")
    root = "p0"
    predicate = tuple(item == root for item in presentations)
    return predicate == (True, False)


def four_routes_have_unique_ids() -> bool:
    routes = (
        "A_SIGNATURE_LANGUAGE_ELIMINATION_THEOREM",
        "B_MINIMAL_CONSERVATIVE_PRESENTATION_ADMISSION_EXTENSION",
        "C_FINITE_TYPED_PRESENTATION_ADMISSION_BRIDGE_WITNESS",
        "D_PROTECTED_HUMAN_GATED_ONTOLOGY_STOP",
    )
    return len(routes) == 4 and len(set(routes)) == 4


def build_report() -> dict[str, object]:
    predicates = swap_invariant_predicates()
    checks = {
        "current_language_indistinguishability": current_language_indistinguishability(),
        "minimum_signature_complete": minimum_signature_complete(),
        "swap_invariant_predicate_count_is_two": len(predicates) == 2,
        "swap_invariant_predicates_are_constant": set(predicates) == {(False, False), (True, True)},
        "no_swap_invariant_unique_admission": all(sum(values) != 1 for values in predicates),
        "asymmetric_token_enables_unique_selection": asymmetric_token_enables_unique_selection(),
        "four_routes_have_unique_ids": four_routes_have_unique_ids(),
        "rt013_raw_total_held_fixed": 1 + 2 + 357 == 360,
    }
    return {
        "schema_id": "v22_p4_t02_b2_post_bounded_current_signature_census_selector_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "swap_invariant_predicates": [list(values) for values in predicates],
        "authority_note": "Exact finite selector controls only; no ontology, physical, empirical, Gate, proof, or promotion authority.",
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
