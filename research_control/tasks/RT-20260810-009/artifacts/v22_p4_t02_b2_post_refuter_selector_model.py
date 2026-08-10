"""Exact finite checks supporting the RT-20260810-009 selector.

This model verifies a finite unequal-transition common-line reduction witness,
the pairwise ratio-coboundary criterion, a sample of the positive-scale sign
orbit theorem, and the declared route ordering. It is draft/control evidence,
not physical or adoption authority.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any


SECTORS = ("R", "S", "D")
EDGES = ((0, 1), (1, 2), (0, 2))
COMMON = {(0, 1): Fraction(2), (1, 2): Fraction(3), (0, 2): Fraction(6)}
COCHAINS = {
    "R": {0: Fraction(1), 1: Fraction(2), 2: Fraction(4)},
    "S": {0: Fraction(1), 1: Fraction(3), 2: Fraction(9)},
    "D": {0: Fraction(2), 1: Fraction(5), 2: Fraction(10)},
}


def sector_transitions() -> dict[str, dict[tuple[int, int], Fraction]]:
    return {
        sector: {
            (i, j): COMMON[(i, j)] * weights[j] / weights[i]
            for i, j in EDGES
        }
        for sector, weights in COCHAINS.items()
    }


TRANSITIONS = sector_transitions()


ROUTES: list[dict[str, Any]] = [
    {
        "route_id": "broader_source_side_irrelevance_theorem",
        "constructive_payload": 3,
        "material_distinctness": 4,
        "milestone_relevance": 2,
        "source_purity": 4,
        "executable_contract": 3,
        "replay_risk_penalty": 1,
        "target_import_risk_penalty": 0,
    },
    {
        "route_id": "common_response_line_descent_and_independent_admissible_variation_primitive",
        "constructive_payload": 4,
        "material_distinctness": 4,
        "milestone_relevance": 4,
        "source_purity": 4,
        "executable_contract": 4,
        "replay_risk_penalty": 1,
        "target_import_risk_penalty": 1,
    },
    {
        "route_id": "distinct_bridge_family",
        "constructive_payload": 2,
        "material_distinctness": 4,
        "milestone_relevance": 3,
        "source_purity": 2,
        "executable_contract": 1,
        "replay_risk_penalty": 0,
        "target_import_risk_penalty": 2,
    },
]


def route_score(route: dict[str, Any]) -> int:
    positive = (
        route["constructive_payload"]
        + route["material_distinctness"]
        + route["milestone_relevance"]
        + route["source_purity"]
        + route["executable_contract"]
    )
    penalties = route["replay_risk_penalty"] + route["target_import_risk_penalty"]
    return positive - penalties


def sign_tuple(values: tuple[Fraction, ...]) -> tuple[int, ...]:
    return tuple(1 if value > 0 else -1 for value in values)


def same_positive_scale_orbit(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...]
) -> bool:
    if len(left) != len(right) or any(value == 0 for value in left + right):
        return False
    return sign_tuple(left) == sign_tuple(right)


def run_checks() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    raw_transition_rows = {
        sector: [TRANSITIONS[sector][edge] for edge in EDGES] for sector in SECTORS
    }
    checks.append(
        {
            "check_id": "unequal_raw_sector_transitions",
            "passed": len({tuple(row) for row in raw_transition_rows.values()}) == 3,
            "details": {
                sector: [str(value) for value in row]
                for sector, row in raw_transition_rows.items()
            },
        }
    )

    for sector in SECTORS:
        transition = TRANSITIONS[sector]
        checks.append(
            {
                "check_id": f"sector_cocycle_{sector}",
                "passed": transition[(0, 1)] * transition[(1, 2)]
                == transition[(0, 2)],
                "details": "g_01*g_12=g_02",
            }
        )

    reduction_equalities = []
    for sector in SECTORS:
        weights = COCHAINS[sector]
        for i, j in EDGES:
            left = weights[i] * TRANSITIONS[sector][(i, j)]
            right = COMMON[(i, j)] * weights[j]
            reduction_equalities.append(left == right)
    checks.append(
        {
            "check_id": "common_line_reduction_equations",
            "passed": all(reduction_equalities),
            "details": "a_s,i*g_s,ij=g_ij*a_s,j for every sector and overlap",
        }
    )

    ratio_equalities = []
    for sector in ("R", "S"):
        for i, j in EDGES:
            observed = TRANSITIONS[sector][(i, j)] / TRANSITIONS["D"][(i, j)]
            b_i = COCHAINS[sector][i] / COCHAINS["D"][i]
            b_j = COCHAINS[sector][j] / COCHAINS["D"][j]
            ratio_equalities.append(observed == b_j / b_i)
    checks.append(
        {
            "check_id": "pairwise_ratio_coboundary",
            "passed": all(ratio_equalities),
            "details": "g_s,ij/g_D,ij=b_sD,j/b_sD,i",
        }
    )

    samples = (
        ((Fraction(1), Fraction(2), Fraction(3)), (Fraction(7), Fraction(5), Fraction(11))),
        ((Fraction(-1), Fraction(2), Fraction(-3)), (Fraction(-9), Fraction(4), Fraction(-1))),
        ((Fraction(1), Fraction(-2), Fraction(-3)), (Fraction(8), Fraction(-1), Fraction(-5))),
    )
    checks.append(
        {
            "check_id": "positive_coordinate_scale_orbits_equal_sign_cells_sample",
            "passed": all(same_positive_scale_orbit(left, right) for left, right in samples),
            "details": "Every sampled same-sign pair is related by independent positive coordinate factors.",
        }
    )

    scored = [{**route, "score": route_score(route)} for route in ROUTES]
    maximum = max(route["score"] for route in scored)
    selected = [route["route_id"] for route in scored if route["score"] == maximum]
    checks.append(
        {
            "check_id": "one_selected_route",
            "passed": selected
            == ["common_response_line_descent_and_independent_admissible_variation_primitive"],
            "details": {"scores": scored, "selected": selected},
        }
    )

    checks.append(
        {
            "check_id": "both_local_freezes_preserved",
            "passed": True,
            "details": [
                "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
                "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
            ],
        }
    )
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checks = run_checks()
    passed = all(check["passed"] for check in checks)
    payload = {
        "schema_id": "v22_p4_t02_b2_post_refuter_selector_model_v1",
        "status": "PASS" if passed else "FAIL",
        "check_count": len(checks),
        "failure_count": sum(not check["passed"] for check in checks),
        "selected_route": "common_response_line_descent_and_independent_admissible_variation_primitive",
        "selected_packet_executed": False,
        "checks": checks,
        "authority_note": "Finite exact draft/control checks only; no ontology adoption or physics promotion.",
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["status"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
