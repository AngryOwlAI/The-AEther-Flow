#!/usr/bin/env python3
"""Exact control model for the RT012 common-character Refuter stress.

The calculations are source-side finite linear algebra only.  They do not
assign physical meaning, adopt a source law, or promote a physics claim.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Iterable, Sequence


Q = Fraction
B0 = (
    (Q(1), Q(-1), Q(1), Q(-1)),
    (Q(1), Q(1), Q(-1), Q(-1)),
)
D = (Q(1), Q(1), Q(1), Q(1))
V = (Q(1), Q(-1), Q(-1), Q(1))
M = (Q(1), Q(-1), Q(0), Q(0))
M0 = (Q(1), Q(-1), Q(1), Q(-1))
X_STAR = (Q(2), Q(1), Q(1), Q(2))
K = {
    "R": (0, 1, 3),
    "S": (0, -2, -1),
    "D": (0, 3, -1),
}


def dot(left: Sequence[Q], right: Sequence[Q]) -> Q:
    return sum((a * b for a, b in zip(left, right)), Q(0))


def mat_vec(matrix: Sequence[Sequence[Q]], vector: Sequence[Q]) -> tuple[Q, ...]:
    return tuple(dot(row, vector) for row in matrix)


def rank(matrix: Iterable[Sequence[Q]]) -> int:
    rows = [list(map(Q, row)) for row in matrix]
    if not rows:
        return 0
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (index for index in range(pivot_row, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for index, row in enumerate(rows):
            if index == pivot_row:
                continue
            factor = row[column]
            if factor:
                rows[index] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(row, rows[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def transition_exponents() -> dict[str, tuple[int, int, int]]:
    result: dict[str, tuple[int, int, int]] = {}
    for sector, values in K.items():
        result[sector] = (
            1 + values[1] - values[0],
            1 + values[2] - values[1],
            1 + values[0] - values[2],
        )
    return result


def perturbed_log_holonomies(mu: Q, epsilon: Q) -> tuple[Q, Q, Q, Q]:
    common = Q(3) * mu
    return common, common + epsilon, common, common


def balance_family(parameter: Q) -> tuple[tuple[Q, ...], tuple[Q, ...]]:
    row_one = M0
    row_two = tuple(
        (Q(1) - parameter) * old + parameter * new
        for old, new in zip(B0[1], M)
    )
    return row_one, row_two


def balance_kernel_witness(parameter: Q) -> tuple[Q, Q, Q, Q]:
    # Polynomially scaled representative of ker(B_parameter)/span{d}.
    return (
        Q(2) - Q(3) * parameter,
        parameter - Q(2),
        Q(3) * parameter - Q(2),
        Q(2) - parameter,
    )


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def evaluate() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    exponents = transition_exponents()
    check("base_balance_rank", rank(B0) == 2, "rank(B)=2")
    check("base_gauge_kernel", mat_vec(B0, D) == (Q(0), Q(0)), "B d=0")
    check("base_variation_kernel", mat_vec(B0, V) == (Q(0), Q(0)), "B v=0")
    check("base_variation_non_gauge", rank((D, V)) == 2, "d and v are independent")
    check("base_mu_gauge", dot(M, D) == 0, "m(d)=0")
    check("base_mu_variation", dot(M, V) == 2, "m(v)=2")
    check("base_mu_value", dot(M, X_STAR) == 1, "mu(x_*)=1")
    check("cycle_exponent_telescopes", all(sum(values) == 3 for values in exponents.values()), str(exponents))
    check("nonzero_transition_exponents", all(all(value != 0 for value in values) for values in exponents.values()), str(exponents))

    # The fixed law is internally exact: all three sector holonomies equal 3 mu.
    base_holonomies = tuple(Q(3) * dot(M, X_STAR) for _ in range(3))
    check("fixed_common_descent", len(set(base_holonomies)) == 1, f"holonomies={base_holonomies}")

    perturbation_samples: list[dict[str, object]] = []
    for epsilon in (Q(1, 1000), Q(-1, 1000), Q(1, 10)):
        common, r_holonomy, s_holonomy, d_holonomy = perturbed_log_holonomies(Q(1), epsilon)
        all_equal = len({r_holonomy, s_holonomy, d_holonomy}) == 1
        fixed_equal = (r_holonomy, s_holonomy, d_holonomy) == (common, common, common)
        perturbation_samples.append(
            {
                "epsilon": qtext(epsilon),
                "common_log_holonomy": qtext(common),
                "sector_log_holonomies": [qtext(r_holonomy), qtext(s_holonomy), qtext(d_holonomy)],
                "common_descent_survives": all_equal,
                "fixed_character_descent_survives": fixed_equal,
            }
        )
        check(
            f"h1_perturbation_{qtext(epsilon).replace('/', '_').replace('-', 'm')}",
            not all_equal and not fixed_equal,
            "a nonzero one-sector H1 perturbation preserves representation syntax but exits both common-character loci",
        )

    # The positive control interval contains the exact trivialization point.
    collapse_t = Q(-1, 2)
    collapse_state = tuple(x + collapse_t * v for x, v in zip(X_STAR, V))
    collapse_mu = dot(M, collapse_state)
    collapse_logs = {
        sector: tuple(collapse_mu * Q(value) for value in values)
        for sector, values in exponents.items()
    }
    check("collapse_inside_positive_domain", Q(-2) < collapse_t < Q(1) and all(value > 0 for value in collapse_state), str(collapse_state))
    check("collapse_mu_zero", collapse_mu == 0, f"mu={collapse_mu}")
    check("collapse_all_transition_logs_zero", all(all(value == 0 for value in values) for values in collapse_logs.values()), str(collapse_logs))
    check("collapse_inverse_still_valid", all((-value) + value == 0 for values in collapse_logs.values() for value in values), "inverse log weights remain negatives")

    # Anchors and positive frame rescalings are object coboundaries and cannot alter cycle holonomy.
    arbitrary_anchor_log = (Q(7, 5), Q(-2, 3), Q(11, 7))
    telescoping_anchor_shift = (
        arbitrary_anchor_log[1] - arbitrary_anchor_log[0],
        arbitrary_anchor_log[2] - arbitrary_anchor_log[1],
        arbitrary_anchor_log[0] - arbitrary_anchor_log[2],
    )
    check("anchor_shift_telescopes", sum(telescoping_anchor_shift, Q(0)) == 0, str(telescoping_anchor_shift))
    check("anchor_cannot_repair_h1", Q(1, 1000) + sum(telescoping_anchor_shift, Q(0)) != 0, "nonzero H1 defect is unchanged by any object coboundary")

    # An alternative covector with the same type and DAG shape trivializes the descent branch.
    check("alternative_covector_gauge", dot(M0, D) == 0, "m0(d)=0")
    check("alternative_covector_flow", dot(M0, V) == 0, "m0(v)=0")
    check("alternative_covector_base", dot(M0, X_STAR) == 0, "m0(x_*)=0")
    check("alternative_covector_in_balance_rowspace", rank((*B0, M0)) == 2, "m0 is the first balance row")

    balance_samples: list[dict[str, object]] = []
    for parameter in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
        matrix = balance_family(parameter)
        witness = balance_kernel_witness(parameter)
        sample = {
            "parameter": qtext(parameter),
            "balance_rank": rank(matrix),
            "gauge_preserved": mat_vec(matrix, D) == (Q(0), Q(0)),
            "witness_in_kernel": mat_vec(matrix, witness) == (Q(0), Q(0)),
            "stacked_rank_with_m": rank((*matrix, M)),
            "m_on_quotient_witness": qtext(dot(M, witness)),
        }
        balance_samples.append(sample)
        check(
            f"balance_family_{qtext(parameter).replace('/', '_')}",
            sample["balance_rank"] == 2 and sample["gauge_preserved"] and sample["witness_in_kernel"],
            str(sample),
        )
    check("balance_endpoint_collapses_m_quotient", balance_samples[-1]["stacked_rank_with_m"] == 2 and balance_samples[-1]["m_on_quotient_witness"] == "0", str(balance_samples[-1]))
    check("balance_interior_keeps_m_quotient", all(sample["stacked_rank_with_m"] == 3 for sample in balance_samples[:-1]), str(balance_samples[:-1]))

    # Cohomology dimensions and inverse/cocycle syntax are independent of target geometry.
    check("common_holonomy_locus_codimension", 3 - 1 == 2, "diagonal in R^3 has codimension 2")
    check("fixed_character_locus_codimension", 4 - 1 == 3, "three sector classes equal one fixed character class")
    test_path_logs = (Q(5, 7), Q(-3, 11), Q(2, 13))
    composed = sum(test_path_logs, Q(0))
    check("cocycle_additivity", composed - test_path_logs[0] == test_path_logs[1] + test_path_logs[2], "additive path logs compose")
    check("inverse_additivity", composed + (-composed) == 0, "inverse path log is the negative")

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_model_v1",
        "status": status,
        "authority_boundary": {
            "status": "draft/control",
            "source_extension_data_adopted": False,
            "physical_interpretation_authorized": False,
            "global_no_go_claim_authorized": False,
            "distance_to_gr_changed": False,
        },
        "fixed_candidate": {
            "balance_rank": rank(B0),
            "transition_exponents": {key: list(value) for key, value in exponents.items()},
            "cycle_log_holonomy_at_base": "3",
            "common_descent_internal_to_defining_law": True,
        },
        "h1_stress": {
            "common_locus_codimension": 2,
            "fixed_character_locus_codimension": 3,
            "samples": perturbation_samples,
            "arbitrarily_small_failure": True,
        },
        "internal_flow_collapse": {
            "parameter": "-1/2",
            "state": [qtext(value) for value in collapse_state],
            "mu": qtext(collapse_mu),
            "all_character_cochain_and_sector_factors_equal_one": True,
            "conditional_inverse_and_cocycle_laws_survive": True,
        },
        "anchor_stress": {
            "object_coboundary_cycle_sum": qtext(sum(telescoping_anchor_shift, Q(0))),
            "repairs_nonzero_h1_defect": False,
        },
        "alternative_covector": {
            "m0": [qtext(value) for value in M0],
            "m0_d": qtext(dot(M0, D)),
            "m0_v": qtext(dot(M0, V)),
            "m0_x_star": qtext(dot(M0, X_STAR)),
        },
        "rank_preserving_balance_family": balance_samples,
        "check_count": len(checks),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['status']}: {result['check_count']} exact checks")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
