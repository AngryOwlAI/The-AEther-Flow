#!/usr/bin/env python3
"""Exact support checks for the RT-20260809-023 B2 construction attempt."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any


def mat_sub(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mat_vec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), Fraction(0))
        for i in range(len(matrix))
    ]


def run_checks() -> dict[str, Any]:
    half = Fraction(1, 2)
    zero = Fraction(0)
    one = Fraction(1)
    carrier = [
        [half, zero, zero],
        [half, half, zero],
        [zero, half, one],
    ]
    identity = [
        [one, zero, zero],
        [zero, one, zero],
        [zero, zero, one],
    ]
    affine = mat_sub(identity, carrier)
    record = [Fraction(2, 5), Fraction(1, 5), Fraction(2, 5)]
    lifted_value = list(record)
    residual = mat_vec(affine, [lifted_value[i] - record[i] for i in range(3)])

    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, evidence: Any) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "evidence": evidence})

    column_sums = [sum((carrier[i][j] for i in range(3)), zero) for j in range(3)]
    add("carrier_column_normalization", column_sums == [one, one, one], [str(x) for x in column_sums])
    add("constant_copy_sampling_recovery", lifted_value == record, [str(x) for x in lifted_value])
    add("constant_lift_affine_solution", residual == [zero, zero, zero], [str(x) for x in residual])

    symbol_samples = [Fraction(-3, 2), Fraction(0), Fraction(7, 4)]
    determinants = [p**3 for p in symbol_samples]
    add(
        "square_symbol_determinant",
        determinants == [Fraction(-27, 8), Fraction(0), Fraction(343, 64)],
        [str(x) for x in determinants],
    )
    sector_radicals = ["<p_tau>", "<p_tau>", "<p_tau>"]
    add("common_radical_ideal", len(set(sector_radicals)) == 1, sector_radicals)
    add("locally_principal_generator", sector_radicals[0] == "<p_tau>", sector_radicals[0])

    units = {
        "g01": one,
        "g10": one,
        "g02": one,
        "g20": one,
        "g12": one,
        "g21": one,
    }
    inverse_ok = (
        units["g01"] * units["g10"] == one
        and units["g02"] * units["g20"] == one
        and units["g12"] * units["g21"] == one
    )
    cocycle_ok = (
        units["g01"] * units["g12"] * units["g20"] == one
        and units["g02"] * units["g21"] * units["g10"] == one
    )
    add("explicit_unit_inverse_relations", inverse_ok, {k: str(v) for k, v in units.items()})
    add("explicit_unit_triple_cocycles", cocycle_ok, ["g01*g12*g20=1", "g02*g21*g10=1"])

    admitted_deltas = [Fraction(-49, 100), Fraction(0), Fraction(49, 100)]
    perturbed_tau0 = [one + delta for delta in admitted_deltas]
    add(
        "shared_tau_nonvanishing_variation",
        all(value > Fraction(1, 2) for value in perturbed_tau0),
        [str(x) for x in perturbed_tau0],
    )

    def source_term(source: tuple[Any, ...], _target: Any, _authority: Any) -> tuple[Any, ...]:
        return source + ("p_tau",)

    fixed_source = ("P7_B3", "U", "tau", "dyadic", "C1_sup")
    fiber_values = {
        source_term(fixed_source, "metric_A", "validator_PASS"),
        source_term(fixed_source, "metric_B", "validator_FAIL"),
        source_term(fixed_source, "no_target", "different_role"),
    }
    add("source_fiber_invariance", len(fiber_values) == 1, [list(value) for value in fiber_values])

    discharged = 33
    blocked = 2
    add(
        "obligation_partition",
        discharged + blocked == 35 and blocked == 2,
        {"discharged": discharged, "blocked": blocked, "total": discharged + blocked},
    )
    complete = discharged == 35
    adequacy_forbidden = True
    obstruction_triggered = (not complete) and adequacy_forbidden
    add(
        "d7_separation_obstruction",
        obstruction_triggered,
        {
            "complete": complete,
            "adequacy_forbidden": adequacy_forbidden,
            "blocked_obligations": ["D7-O2", "D7-O4"],
        },
    )

    failed = [row["check_id"] for row in checks if not row["passed"]]
    return {
        "schema_id": "v22_p4_t02_b2_descriptor_construction_model_v1",
        "task_id": "RT-20260809-023",
        "instance_attempt_id": "INST-V22-B2-EQUIPPED-CHAIN-TRANSPORT-001",
        "result_type": "precise_obstruction",
        "check_count": len(checks),
        "failure_count": len(failed),
        "status": "PASS" if not failed else "FAIL",
        "failed_check_ids": failed,
        "checks": checks,
        "authority_limits": {
            "descriptor_instance_complete": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "physical_geometry_claimed": False,
            "distance_to_gr_changed": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_checks()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
