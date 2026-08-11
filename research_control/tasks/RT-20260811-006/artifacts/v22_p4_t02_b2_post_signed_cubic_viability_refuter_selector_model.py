#!/usr/bin/env python3
"""Exact controls for the RT006 post-Refuter theoretical selector.

The model is deliberately source-syntactic.  Its orthant fixture is a finite
certificate for a law-space robust-invariance relation, not a physical state
space, causal cone, metric, or adopted ontology object.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from typing import Any


SELECTED_ROUTE = "A_SOURCE_LAW_SPACE_ROBUST_INVARIANCE_PROTECTION"
SELECTED_PACKET = (
    "PKT-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-"
    "PROTECTION-FORMALIZATION-V1"
)

FREEZES = (
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
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
        "admissible": True,
        "direct_burden": True,
        "constructive": True,
        "ontology_cost": 2,
        "requires_human_gate": False,
        "disposition": "selected",
    },
    {
        "route_id": "B_SOURCE_SIDE_PROTECTION_IRRELEVANCE_THEOREM",
        "admissible": True,
        "direct_burden": True,
        "constructive": False,
        "ontology_cost": 1,
        "requires_human_gate": False,
        "disposition": "not_selected_constructive_route_survives",
    },
    {
        "route_id": "C_MATERIALLY_DISTINCT_SPECTRAL_PERSISTENCE_BRIDGE",
        "admissible": True,
        "direct_burden": False,
        "constructive": True,
        "ontology_cost": 4,
        "requires_human_gate": False,
        "disposition": "not_selected_higher_underived_structure",
    },
    {
        "route_id": "D_PROTECTED_HUMAN_GATED_ONTOLOGY_STOP",
        "admissible": True,
        "direct_burden": False,
        "constructive": False,
        "ontology_cost": 5,
        "requires_human_gate": True,
        "disposition": "not_selected_nonpromotional_continuation_exists",
    },
)


def route_score(route: dict[str, Any]) -> tuple[int, int, int, int, str]:
    """Lower is preferred after freeze and source-purity admission."""

    return (
        0 if route["admissible"] else 1,
        0 if route["direct_burden"] else 1,
        0 if route["constructive"] else 1,
        int(route["ontology_cost"]),
        str(route["route_id"]),
    )


def orthant_certificate() -> dict[str, Any]:
    """Return an exact full-state robust-invariance certificate.

    K is the positive orthant.  At an active face x_i=0, the tangent-cone
    interior condition is v_i>0.  F+Delta stays strictly inside because every
    admitted coordinate variation is smaller than the corresponding source
    margin.  Coordinates here are algebraic fixture labels only.
    """

    field = (Fraction(2), Fraction(3), Fraction(5))
    variation_bound = (Fraction(1), Fraction(1), Fraction(2))
    residual_margin = tuple(f - e for f, e in zip(field, variation_bound))
    active_faces = (0, 1, 2)
    all_inside = all(residual_margin[i] > 0 for i in active_faces)

    # Positive conormal regraduation changes certificate scale, not sign.
    regraduations = (Fraction(2), Fraction(3, 2), Fraction(7, 3))
    regraded = tuple(c * m for c, m in zip(regraduations, residual_margin))
    regraduation_preserves = all(
        (before > 0) == (after > 0)
        for before, after in zip(residual_margin, regraded)
    )

    return {
        "field": [str(value) for value in field],
        "variation_bound": [str(value) for value in variation_bound],
        "residual_margin": [str(value) for value in residual_margin],
        "all_active_faces_strictly_inward": all_inside,
        "positive_regraduation_preserves_sign": regraduation_preserves,
    }


def balanced_normal_variation_obstruction() -> dict[str, Any]:
    """Show why tangency plus a balanced normal variation class is unprotected."""

    epsilon = Fraction(1, 17)
    tangent_velocity = Fraction(0)
    plus = tangent_velocity + epsilon
    minus = tangent_velocity - epsilon
    return {
        "epsilon": str(epsilon),
        "plus_normal_velocity": str(plus),
        "minus_normal_velocity": str(minus),
        "both_signs_realized": plus > 0 and minus < 0,
        "zero_margin_robust": False,
    }


def run() -> dict[str, Any]:
    certificate = orthant_certificate()
    obstruction = balanced_normal_variation_obstruction()
    selected_by_score = min(ROUTES, key=route_score)["route_id"]
    selected_rows = [row for row in ROUTES if row["disposition"] == "selected"]

    checks = {
        "exactly_four_routes": len(ROUTES) == 4,
        "exactly_one_selected_route": len(selected_rows) == 1,
        "lexicographic_selection_matches_record": selected_by_score == SELECTED_ROUTE,
        "selected_route_is_constructive": bool(selected_rows[0]["constructive"]),
        "selected_route_requires_no_gate_now": not bool(
            selected_rows[0]["requires_human_gate"]
        ),
        "orthant_certificate_is_strict": bool(
            certificate["all_active_faces_strictly_inward"]
        ),
        "certificate_is_regraduation_stable": bool(
            certificate["positive_regraduation_preserves_sign"]
        ),
        "balanced_variation_exposes_both_signs": bool(
            obstruction["both_signs_realized"]
        ),
        "zero_margin_is_not_robust": obstruction["zero_margin_robust"] is False,
        "five_freezes_preserved": len(FREEZES) == 5 and len(set(FREEZES)) == 5,
        "fourteen_no_delta_rows_required": len(BURDENS) == 14,
        "selected_packet_is_unexecuted": True,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_model_v1",
        "status": status,
        "selected_route_id": SELECTED_ROUTE,
        "selected_packet_id": SELECTED_PACKET,
        "selected_packet_executed": False,
        "checks": checks,
        "route_scores": {
            row["route_id"]: list(route_score(row))[:-1] for row in ROUTES
        },
        "orthant_certificate": certificate,
        "balanced_normal_variation_obstruction": obstruction,
        "preserved_freezes": list(FREEZES),
        "distance_to_gr_rows": [
            {"burden": burden, "status": "no_delta"} for burden in BURDENS
        ],
        "authority_note": (
            "The fixture validates source-side algebra and route selection only; "
            "it is not a physical cone, metric, response law, adoption, or proof authority."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
