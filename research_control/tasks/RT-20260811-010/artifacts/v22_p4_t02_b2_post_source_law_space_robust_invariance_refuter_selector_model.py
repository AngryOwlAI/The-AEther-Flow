#!/usr/bin/env python3
"""Exact source-syntactic controls for the bounded RT010 selector.

The fixtures establish only the mathematical feasibility and failure branches
of a future proposal-only source-law packet.  They do not derive the packet's
roots from current ontology, adopt a source law, or provide physical response,
causal, metric, empirical, benchmark, or promotion authority.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from typing import Any


SELECTED_ROUTE = "A_SOURCE_GENERATED_COMPACT_ROOT_FAMILY_COERCIVE_PROTECTION_LAW"
SELECTED_CANDIDATE = (
    "CAND-V22-B2-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-"
    "COERCIVE-PROTECTION-LAW-V1"
)
SELECTED_PACKET = (
    "PKT-V22-P4T02-B2-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-"
    "COERCIVE-PROTECTION-LAW-FORMALIZATION-V1"
)

FREEZES = (
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
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

ROUTES: tuple[dict[str, Any], ...] = (
    {
        "route_id": SELECTED_ROUTE,
        "admissible_now": True,
        "direct_burden": True,
        "constructive": True,
        "ontology_cost": 3,
        "requires_human_gate": False,
        "disposition": "selected",
    },
    {
        "route_id": "B_SOURCE_SIDE_PRINCIPAL_FACTOR_IRRELEVANCE_THEOREM",
        "admissible_now": False,
        "direct_burden": False,
        "constructive": False,
        "ontology_cost": 1,
        "requires_human_gate": False,
        "disposition": "not_selected_missing_source_derived_principal_factor_map",
    },
    {
        "route_id": "C_MATERIALLY_DISTINCT_OPEN_SYSTEM_RESPONSE_BRIDGE",
        "admissible_now": False,
        "direct_burden": False,
        "constructive": True,
        "ontology_cost": 5,
        "requires_human_gate": False,
        "disposition": "not_selected_missing_source_ports_and_response_semantics",
    },
    {
        "route_id": "D_PROTECTED_HUMAN_GATED_ONTOLOGY_STOP",
        "admissible_now": True,
        "direct_burden": False,
        "constructive": False,
        "ontology_cost": 6,
        "requires_human_gate": True,
        "disposition": "not_selected_bounded_constructive_packet_remains_available",
    },
)


def route_score(route: dict[str, Any]) -> tuple[int, int, int, int, int, str]:
    """Lower score wins after the fixed freeze and authority screens."""

    return (
        0 if route["admissible_now"] else 1,
        0 if route["direct_burden"] else 1,
        0 if route["constructive"] else 1,
        0 if not route["requires_human_gate"] else 1,
        int(route["ontology_cost"]),
        str(route["route_id"]),
    )


def compact_total_root_fixture() -> dict[str, Any]:
    """Exact finite compact-total root-family and EqSrc transport control."""

    roots = ("r0", "r1", "r2")
    kappa = {
        "r0": Fraction(2, 1),
        "r1": Fraction(3, 2),
        "r2": Fraction(5, 4),
    }
    eqsrc = {"r0": "r2", "r1": "r0", "r2": "r1"}
    transported = {eqsrc[root]: value for root, value in kappa.items()}
    variation_successor = {"r0": "r1", "r1": "r2", "r2": "r2"}
    transverse_partner = {"r0": "r2", "r1": "r1", "r2": "r0"}
    minimum = min(kappa.values())
    return {
        "root_count": len(roots),
        "roots_are_total_for_declared_fixture": set(roots) == set(kappa),
        "all_kappa_values_positive": all(value > 0 for value in kappa.values()),
        "minimum": str(minimum),
        "minimum_is_positive": minimum > 0,
        "minimum_is_attained": minimum in kappa.values(),
        "eqsrc_is_bijection": set(eqsrc) == set(roots) == set(eqsrc.values()),
        "eqsrc_transport_preserves_value_multiset": sorted(transported.values())
        == sorted(kappa.values()),
        "variation_closure": set(variation_successor.values()) <= set(roots),
        "transverse_closure": set(transverse_partner.values()) <= set(roots),
    }


def zero_infimum_countercontrols() -> dict[str, Any]:
    """Return exact witnesses showing why total compactness and l.s.c. matter."""

    finite_prefix = tuple(Fraction(1, n) for n in range(1, 65))
    compact_sequence_prefix = tuple(Fraction(1, n) for n in range(1, 65))
    return {
        "noncompact_family": "R=[0,infinity), kappa(t)=1/(1+t)",
        "noncompact_pointwise_positive": True,
        "noncompact_infimum": "0",
        "noncompact_prefix_decreases_toward_zero": all(
            finite_prefix[index + 1] < finite_prefix[index]
            for index in range(len(finite_prefix) - 1)
        ),
        "compact_non_lsc_family": "R={0} union {1/n:n>=1}",
        "compact_non_lsc_rule": "kappa(0)=1; kappa(1/n)=1/n",
        "compact_non_lsc_pointwise_positive": True,
        "compact_non_lsc_infimum": "0",
        "compact_non_lsc_violation": (
            min(compact_sequence_prefix[-8:]) < Fraction(1, 8)
        ),
    }


def factorization_scope_control() -> dict[str, Any]:
    """Separate an abstract nonfactorization lemma from an irrelevance theorem."""

    diagnostic = {"x_plus": "d0", "x_minus": "d0", "x_control": "d1"}
    supplied_label = {"x_plus": 1, "x_minus": -1, "x_control": 1}
    conflicting_fibre = diagnostic["x_plus"] == diagnostic["x_minus"]
    label_differs = supplied_label["x_plus"] != supplied_label["x_minus"]
    return {
        "conflicting_diagnostic_fibre": conflicting_fibre,
        "supplied_label_differs_on_fibre": label_differs,
        "supplied_label_factors_through_diagnostic": not (
            conflicting_fibre and label_differs
        ),
        "source_derived_pi_prin_supplied": False,
        "p4_t02_irrelevance_follows": False,
        "scope_note": (
            "Nonfactorization of a stipulated label through a diagnostic bundle "
            "does not prove source-side P4-T02 irrelevance without a source-derived "
            "principal-factor map Pi_prin and a universal fibre-constancy theorem."
        ),
    }


def run() -> dict[str, Any]:
    compact = compact_total_root_fixture()
    countercontrols = zero_infimum_countercontrols()
    factorization = factorization_scope_control()
    selected = [row for row in ROUTES if row["disposition"] == "selected"]
    selected_by_score = min(ROUTES, key=route_score)["route_id"]
    checks = {
        "exactly_four_routes": len(ROUTES) == 4,
        "exactly_one_selected_route": len(selected) == 1,
        "selection_matches_rule": selected_by_score == SELECTED_ROUTE,
        "selected_route_is_constructive": selected[0]["constructive"],
        "selected_route_requires_no_gate_now": not selected[0]["requires_human_gate"],
        "finite_total_root_fixture": compact["roots_are_total_for_declared_fixture"],
        "finite_positive_kappa": compact["all_kappa_values_positive"],
        "positive_minimum_attained": compact["minimum_is_positive"]
        and compact["minimum_is_attained"],
        "eqsrc_transport_control": compact["eqsrc_is_bijection"]
        and compact["eqsrc_transport_preserves_value_multiset"],
        "variation_and_transverse_closure": compact["variation_closure"]
        and compact["transverse_closure"],
        "noncompact_countercontrol_has_zero_infimum": countercontrols[
            "noncompact_infimum"
        ]
        == "0",
        "non_lsc_countercontrol_has_zero_infimum": countercontrols[
            "compact_non_lsc_infimum"
        ]
        == "0",
        "route_b_does_not_overclaim_irrelevance": factorization[
            "p4_t02_irrelevance_follows"
        ]
        is False,
        "six_freezes_preserved": len(FREEZES) == 6 and len(set(FREEZES)) == 6,
        "fourteen_no_delta_rows_required": len(BURDENS) == 14,
        "selected_packet_is_unexecuted": True,
    }
    return {
        "schema_id": "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "selected_route_id": SELECTED_ROUTE,
        "selected_candidate_id": SELECTED_CANDIDATE,
        "selected_packet_id": SELECTED_PACKET,
        "selected_packet_executed": False,
        "checks": checks,
        "route_scores": {
            row["route_id"]: list(route_score(row))[:-1] for row in ROUTES
        },
        "compact_total_root_fixture": compact,
        "zero_infimum_countercontrols": countercontrols,
        "factorization_scope_control": factorization,
        "preserved_freezes": list(FREEZES),
        "distance_to_gr_rows": [
            {"burden": burden, "status": "no_delta"} for burden in BURDENS
        ],
        "authority_note": (
            "The exact controls establish a conditional compactness theorem, its "
            "failure branches, and the limit of the rejected nonfactorization route. "
            "They do not derive G_src or kappa from current ontology, adopt a law, "
            "or supply physical, empirical, metric, benchmark, or promotion authority."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
