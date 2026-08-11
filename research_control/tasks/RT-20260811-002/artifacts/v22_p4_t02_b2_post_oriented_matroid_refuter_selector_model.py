#!/usr/bin/env python3
"""Exact controls for the RT019 post-Bridge_OM continuation selector.

This module is draft/control evidence.  It compares route dependencies and
checks a rational barrier-certificate fixture.  It does not derive a source
law, physical cone, response semantics, or effective metric.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction


ROUTES = (
    {
        "route_id": "A_SOURCE_DYNAMICAL_VIABILITY_ADMISSIBILITY_THEOREM",
        "constructive": 3,
        "materially_distinct": 3,
        "addresses_occurrence_selection": 3,
        "addresses_variation_stability": 3,
        "preserves_freezes": 3,
        "extra_unselected_structure": 1,
        "human_gate_now": 0,
    },
    {
        "route_id": "B_REALIZATION_SENSITIVE_MARGIN_BRIDGE",
        "constructive": 3,
        "materially_distinct": 3,
        "addresses_occurrence_selection": 1,
        "addresses_variation_stability": 2,
        "preserves_freezes": 3,
        "extra_unselected_structure": 3,
        "human_gate_now": 0,
    },
    {
        "route_id": "C_SOURCE_SIDE_IRRELEVANCE_THEOREM",
        "constructive": 0,
        "materially_distinct": 3,
        "addresses_occurrence_selection": 0,
        "addresses_variation_stability": 1,
        "preserves_freezes": 3,
        "extra_unselected_structure": 1,
        "human_gate_now": 0,
    },
    {
        "route_id": "D_PROTECTED_HUMAN_GATED_ONTOLOGY_STOP",
        "constructive": 0,
        "materially_distinct": 3,
        "addresses_occurrence_selection": 0,
        "addresses_variation_stability": 0,
        "preserves_freezes": 3,
        "extra_unselected_structure": 0,
        "human_gate_now": 3,
    },
)


def route_score(route: dict[str, int | str]) -> int:
    return (
        3 * int(route["constructive"])
        + 3 * int(route["materially_distinct"])
        + 3 * int(route["addresses_occurrence_selection"])
        + 2 * int(route["addresses_variation_stability"])
        + 2 * int(route["preserves_freezes"])
        - 2 * int(route["extra_unselected_structure"])
        - 3 * int(route["human_gate_now"])
    )


def barrier_fixture() -> dict[str, object]:
    """Check b(F_q(t)) >= lambda*b(t) on exact rational samples.

    The RT018 wall fixture has a feasible side t>0 and a wall at t=0.  A
    separately supplied source transition q*t with q bounded below by a
    positive lambda preserves that side.  A sign-flipping transition does not.
    This exhibits the missing law; it does not supply or adopt it.
    """

    lamb = Fraction(1, 3)
    qs = (Fraction(1, 3), Fraction(1, 2), Fraction(1), Fraction(2))
    starts = (Fraction(1, 1000), Fraction(1, 10), Fraction(1), Fraction(7, 3))
    rows: list[dict[str, str | bool]] = []
    for t in starts:
        for q in qs:
            nxt = q * t
            rows.append(
                {
                    "t": str(t),
                    "q": str(q),
                    "next_t": str(nxt),
                    "barrier_bound": str(lamb * t),
                    "positive_side_preserved": nxt > 0,
                    "multiplicative_barrier_holds": nxt >= lamb * t,
                }
            )
    sign_flip_start = Fraction(1, 10)
    sign_flip_end = -sign_flip_start
    return {
        "barrier": "b(t)=t",
        "admissible_domain": "t>0",
        "lambda": str(lamb),
        "sample_rows": rows,
        "all_positive_side_preserved": all(bool(r["positive_side_preserved"]) for r in rows),
        "all_barrier_bounds_hold": all(bool(r["multiplicative_barrier_holds"]) for r in rows),
        "unprotected_sign_flip_control": {
            "start": str(sign_flip_start),
            "end": str(sign_flip_end),
            "crosses_wall": sign_flip_end < 0,
        },
    }


def build_payload() -> dict[str, object]:
    scored = [dict(route, score=route_score(route)) for route in ROUTES]
    ranked = sorted(scored, key=lambda row: (-int(row["score"]), str(row["route_id"])))
    fixture = barrier_fixture()
    checks = {
        "exactly_four_routes": len(scored) == 4,
        "unique_route_ids": len({r["route_id"] for r in scored}) == 4,
        "route_a_unique_score_maximum": ranked[0]["route_id"]
        == "A_SOURCE_DYNAMICAL_VIABILITY_ADMISSIBILITY_THEOREM"
        and int(ranked[0]["score"]) > int(ranked[1]["score"]),
        "constructive_route_available": any(int(r["constructive"]) > 0 for r in scored),
        "all_routes_preserve_freezes": all(int(r["preserves_freezes"]) == 3 for r in scored),
        "barrier_fixture_exact_pass": bool(fixture["all_positive_side_preserved"])
        and bool(fixture["all_barrier_bounds_hold"]),
        "missing_law_countercontrol_crosses_wall": bool(
            fixture["unprotected_sign_flip_control"]["crosses_wall"]  # type: ignore[index]
        ),
        "selected_packet_unexecuted": True,
        "distance_to_gr_unchanged": True,
    }
    payload: dict[str, object] = {
        "schema_id": "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_exact_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "route_scores": scored,
        "ranked_route_ids": [r["route_id"] for r in ranked],
        "selected_route_id": ranked[0]["route_id"],
        "selected_future_packet_id": "PKT-V22-P4T02-B2-SOURCE-DYNAMICAL-VIABILITY-ADMISSIBILITY-SELECTOR-FORMALIZATION-V1",
        "selected_future_packet_type": "ontology_law_research_packet",
        "selected_next_role": "ontology-formalizer@0.2.0",
        "barrier_fixture": fixture,
        "checks": checks,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["status"])
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
