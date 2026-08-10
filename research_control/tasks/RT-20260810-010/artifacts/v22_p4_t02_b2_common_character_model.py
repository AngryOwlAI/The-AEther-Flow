#!/usr/bin/env python3
"""Exact finite checks for the proposal-only common-character source law.

This model is control evidence for RT-20260810-010.  It verifies integer and
rational identities only; it does not assign physical or empirical meaning to
the source data and it does not promote the candidate law.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Iterable, Sequence


Matrix = tuple[tuple[Fraction, ...], ...]
Vector = tuple[Fraction, ...]


def dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(dot(row, vector) for row in matrix)


def rank(matrix: Iterable[Iterable[Fraction]]) -> int:
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (candidate for candidate in range(pivot_row, row_count) if rows[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot_value for entry in rows[pivot_row]]
        for candidate in range(row_count):
            if candidate == pivot_row:
                continue
            factor = rows[candidate][column]
            if factor:
                rows[candidate] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(rows[candidate], rows[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def scaled_add(base: Vector, parameter: Fraction, direction: Vector) -> Vector:
    return tuple(value + parameter * delta for value, delta in zip(base, direction, strict=True))


def as_json_number(value: Fraction) -> int | str:
    return value.numerator if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def evaluate() -> dict[str, object]:
    # The source law E_src(x)=B x is fixed independently of any response map.
    balance: Matrix = (
        (Fraction(1), Fraction(-1), Fraction(1), Fraction(-1)),
        (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1)),
    )
    gauge: Vector = tuple(map(Fraction, (1, 1, 1, 1)))
    variation: Vector = tuple(map(Fraction, (1, -1, -1, 1)))
    base_state: Vector = tuple(map(Fraction, (2, 1, 1, 2)))
    mu_covector: Vector = tuple(map(Fraction, (1, -1, 0, 0)))

    balance_rank = rank(balance)
    kernel_dimension = len(base_state) - balance_rank
    quotient_dimension = kernel_dimension - rank((gauge,))
    base_balance = mat_vec(balance, base_state)
    gauge_balance = mat_vec(balance, gauge)
    variation_balance = mat_vec(balance, variation)
    mu_base = dot(mu_covector, base_state)
    mu_gauge = dot(mu_covector, gauge)
    mu_variation = dot(mu_covector, variation)

    # G_src is the fundamental groupoid of an oriented three-cycle.  The
    # integer ell is additive on path concatenation and changes sign on inverse.
    generators = {
        "e01": {"source": 0, "target": 1, "ell": 1},
        "e12": {"source": 1, "target": 2, "ell": 1},
        "e20": {"source": 2, "target": 0, "ell": 1},
    }
    cycle_ell = sum(item["ell"] for item in generators.values())
    character_cycle_log = mu_base * cycle_ell
    character_cycle_variation_log = mu_variation * cycle_ell

    # a_s(i;x)=exp(k_s,i*mu(x)).  Sector transitions are defined in logarithmic
    # coordinates by log rho_s(g)=mu*(ell(g)+k_s,target-k_s,source).
    # Object 0 is a declared source base object.  The cochains are normalized
    # there, a_s(0;x)=1, as proposal-law data.  This fixes the otherwise
    # independent sector-constant intertwiner torsor; it is not physical
    # calibration, and its source legitimacy remains for the next audit.
    cochain_exponents = {
        "R": (0, 1, 3),
        "S": (0, -2, -1),
        "D": (0, 3, -1),
    }
    intertwiner_checks: list[dict[str, object]] = []
    variation_rates: dict[str, dict[str, int]] = {}
    for sector, exponents in cochain_exponents.items():
        variation_rates[sector] = {}
        for edge_name, edge in generators.items():
            source = int(edge["source"])
            target = int(edge["target"])
            ell = int(edge["ell"])
            sector_log_exponent = ell + exponents[target] - exponents[source]
            left = exponents[source] + sector_log_exponent
            right = ell + exponents[target]
            intertwiner_checks.append(
                {
                    "sector": sector,
                    "edge": edge_name,
                    "left_exponent": left,
                    "right_exponent": right,
                    "pass": left == right,
                }
            )
            variation_rates[sector][edge_name] = int(mu_variation) * sector_log_exponent

    # Composition on e01 followed by e12 telescopes in every sector.
    composition_checks: list[dict[str, object]] = []
    for sector, exponents in cochain_exponents.items():
        e01 = 1 + exponents[1] - exponents[0]
        e12 = 1 + exponents[2] - exponents[1]
        e02 = 2 + exponents[2] - exponents[0]
        composition_checks.append(
            {
                "sector": sector,
                "e01_plus_e12": e01 + e12,
                "e02": e02,
                "pass": e01 + e12 == e02,
            }
        )

    sample_parameters = (Fraction(-1, 2), Fraction(0), Fraction(1, 2))
    finite_flow_samples: list[dict[str, object]] = []
    for parameter in sample_parameters:
        state = scaled_add(base_state, parameter, variation)
        finite_flow_samples.append(
            {
                "parameter": as_json_number(parameter),
                "state": [as_json_number(value) for value in state],
                "balance": [as_json_number(value) for value in mat_vec(balance, state)],
                "positive": all(value > 0 for value in state),
                "mu": as_json_number(dot(mu_covector, state)),
            }
        )

    e01_rate_vector = tuple(variation_rates[sector]["e01"] for sector in ("R", "S", "D"))
    checks = {
        "balance_rank_two": balance_rank == 2,
        "kernel_dimension_two": kernel_dimension == 2,
        "gauge_in_kernel": all(value == 0 for value in gauge_balance),
        "variation_in_kernel": all(value == 0 for value in variation_balance),
        "base_is_root": all(value == 0 for value in base_balance),
        "gauge_and_variation_independent": rank((gauge, variation)) == 2,
        "variation_quotient_dimension_one": quotient_dimension == 1,
        "mu_gauge_invariant": mu_gauge == 0,
        "mu_varies_nontrivially": mu_variation == 2,
        "positive_character_at_base": mu_base == 1,
        "nontrivial_cycle_holonomy": character_cycle_log == 3,
        "cycle_holonomy_varies": character_cycle_variation_log == 6,
        "all_intertwiners_exact": all(item["pass"] for item in intertwiner_checks),
        "sector_intertwiner_anchors_fixed": all(
            exponents[0] == 0 for exponents in cochain_exponents.values()
        ),
        "all_compositions_exact": all(item["pass"] for item in composition_checks),
        "finite_flow_stays_on_law": all(
            all(value == 0 for value in mat_vec(balance, scaled_add(base_state, t, variation)))
            for t in sample_parameters
        ),
        "sample_finite_flow_positive": all(item["positive"] for item in finite_flow_samples),
        "sector_transition_variation_non_diagonal": len(set(e01_rate_vector)) == 3,
        "sector_transition_variation_nonzero": all(value != 0 for value in e01_rate_vector),
    }
    return {
        "schema_id": "v22_p4_t02_b2_common_character_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "authority": "draft/control computation only",
        "candidate_status": "proposal-only source-extension data",
        "source_balance_matrix": [[as_json_number(value) for value in row] for row in balance],
        "base_state": [as_json_number(value) for value in base_state],
        "gauge_generator": [as_json_number(value) for value in gauge],
        "variation_generator": [as_json_number(value) for value in variation],
        "mu_covector": [as_json_number(value) for value in mu_covector],
        "balance_rank": balance_rank,
        "kernel_dimension": kernel_dimension,
        "variation_quotient_dimension": quotient_dimension,
        "mu_base": as_json_number(mu_base),
        "mu_variation_rate": as_json_number(mu_variation),
        "groupoid_generators": generators,
        "cycle_winding": cycle_ell,
        "cycle_character_log_at_base": as_json_number(character_cycle_log),
        "cycle_character_log_variation_rate": as_json_number(character_cycle_variation_log),
        "cochain_exponents": cochain_exponents,
        "intertwiner_checks": intertwiner_checks,
        "composition_checks": composition_checks,
        "sector_log_transition_variation_rates": variation_rates,
        "e01_sector_rate_vector": e01_rate_vector,
        "finite_flow_samples": finite_flow_samples,
        "checks": checks,
        "claim_blocks": {
            "current_ontology_derivation": False,
            "source_law_adoption": False,
            "physical_response_or_causality": False,
            "all_sector_universality": False,
            "d7_or_b2_or_p4_t03": False,
            "g_eff_or_downstream_derivation": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Emit the exact check record as JSON.")
    args = parser.parse_args()
    result = evaluate()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
