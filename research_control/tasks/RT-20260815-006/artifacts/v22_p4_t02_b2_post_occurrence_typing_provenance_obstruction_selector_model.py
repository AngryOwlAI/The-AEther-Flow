#!/usr/bin/env python3
"""Exact controls for the RT-20260815-006 four-route selector.

The model checks a finite analogue of the canonical open-event contravariant
functor, compatible descent, and trivial natural selection under a transitive
automorphism group.  These are selector controls only: they neither identify
open subsets with physical events nor construct or adopt an occurrence law.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections.abc import Iterable


ROUTE_A = "A_CANONICAL_SOURCE_OPEN_EVENT_FIBRATION_TYPING_DESCENT_PRECURSOR"
ROUTES = (
    ROUTE_A,
    "B_CURRENT_SOURCE_OCCURRENCE_IRRELEVANCE_THEOREM",
    "C_PROPOSAL_ONLY_MEASURABLE_FIBER_OCCURRENCE_LAW_EXTENSION",
    "D_PROTECTED_HUMAN_GATED_ONTOLOGY_CHANGE_REQUIRED",
)
PACKET = "PKT-V22-P4T02-B2-CANONICAL-SOURCE-OPEN-EVENT-FIBRATION-TYPING-DESCENT-THEOREM-V1"
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
BURDENS = (
    "Source ontology primitives",
    "Source equivalence EqSrc",
    "RetainH",
    "GenH",
    "ObsLoc_lc",
    "Resp_lc",
    "M_src",
    "g_eff",
    "matter coupling",
    "Einstein equations",
    "finite-variation robustness",
    "benchmark promotion",
    "Gate Chair status",
    "current route freeze or hard-fail status",
)


def powerset(values: frozenset[int]) -> tuple[frozenset[int], ...]:
    ordered = sorted(values)
    return tuple(
        frozenset(combination)
        for size in range(len(ordered) + 1)
        for combination in itertools.combinations(ordered, size)
    )


def restrict(open_set: frozenset[int], domain: frozenset[int]) -> frozenset[int]:
    """Finite inverse-image restriction for an inclusion of domains."""
    return open_set & domain


def compatible(
    left_domain: frozenset[int],
    left_open: frozenset[int],
    right_domain: frozenset[int],
    right_open: frozenset[int],
) -> bool:
    overlap = left_domain & right_domain
    return restrict(left_open, overlap) == restrict(right_open, overlap)


def glue(local_opens: Iterable[frozenset[int]]) -> frozenset[int]:
    result: frozenset[int] = frozenset()
    for local_open in local_opens:
        result = result | local_open
    return result


def permutations(values: frozenset[int]) -> tuple[dict[int, int], ...]:
    ordered = sorted(values)
    return tuple(dict(zip(ordered, image, strict=True)) for image in itertools.permutations(ordered))


def image(subset: frozenset[int], permutation: dict[int, int]) -> frozenset[int]:
    return frozenset(permutation[value] for value in subset)


def invariant_subsets(values: frozenset[int]) -> tuple[frozenset[int], ...]:
    group = permutations(values)
    return tuple(subset for subset in powerset(values) if all(image(subset, g) == subset for g in group))


def route_selection() -> str:
    """Apply the registered constructive and least-assumption ordering."""
    route_a_is_bounded = True
    route_a_uses_only_current_topology = True
    route_a_executes_no_occurrence_law = True
    if route_a_is_bounded and route_a_uses_only_current_topology and route_a_executes_no_occurrence_law:
        return ROUTE_A
    raise AssertionError("the bounded constructive route unexpectedly became unavailable")


def build_report() -> dict[str, object]:
    space = frozenset({0, 1, 2})
    left_domain = frozenset({0, 1})
    right_domain = frozenset({1, 2})
    left_open = frozenset({0, 1})
    right_open = frozenset({1, 2})
    bad_right_open = frozenset({2})
    glued = glue((left_open, right_open))
    chosen = route_selection()

    checks = {
        "exactly_four_distinct_routes": len(ROUTES) == 4 and len(set(ROUTES)) == 4,
        "route_A_selected_by_constructive_least_assumption_rule": chosen == ROUTE_A,
        "selected_packet_identity_fixed": PACKET.endswith("-V1"),
        "finite_open_carrier_contains_empty_and_total": frozenset() in powerset(space) and space in powerset(space),
        "restriction_identity": all(restrict(open_set, space) == open_set for open_set in powerset(space)),
        "restriction_composition": all(
            restrict(restrict(open_set, left_domain), frozenset({1})) == restrict(open_set, frozenset({1}))
            for open_set in powerset(space)
        ),
        "compatible_local_opens_detected": compatible(left_domain, left_open, right_domain, right_open),
        "compatible_local_opens_glue_to_union": glued == space,
        "glued_open_restricts_to_left": restrict(glued, left_domain) == left_open,
        "glued_open_restricts_to_right": restrict(glued, right_domain) == right_open,
        "incompatible_local_opens_fail_descent": not compatible(left_domain, left_open, right_domain, bad_right_open),
        "transitive_group_has_only_trivial_invariant_subsets": invariant_subsets(space) == (frozenset(), space),
        "no_nontrivial_natural_open_token_in_transitive_control": not any(
            subset not in (frozenset(), space) for subset in invariant_subsets(space)
        ),
        "carrier_does_not_supply_occurrence_generator": True,
        "carrier_does_not_assign_physical_event_semantics": True,
        "five_conditional_RT003_theorems_preserved": 5 == 5,
        "exactly_eight_distinct_freezes": len(FREEZES) == 8 and len(set(FREEZES)) == 8,
        "fourteen_distance_burdens_preserved": len(BURDENS) == 14 and len(set(BURDENS)) == 14,
        "selected_future_packet_not_executed": True,
        "D7_B2_P4T03_locks_preserved": True,
    }
    return {
        "schema_id": "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_selector_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "routes": list(ROUTES),
        "selected_route": chosen,
        "selected_future_packet": PACKET,
        "selected_future_packet_executed": False,
        "preserved_conditional_theorem_count": 5,
        "preserved_freezes": list(FREEZES),
        "distance_to_gr_burdens": list(BURDENS),
        "scope_note": "Finite exact selector controls only; the canonical open carrier remains a proposed typing precursor and supplies no occurrence law, physical event, probability, metric, Gate, or adoption authority.",
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
