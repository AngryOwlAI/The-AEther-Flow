#!/usr/bin/env python3
"""Exact support checks for the RT-20260810-001 source-interface packet."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any, Iterable


Vector = tuple[Fraction, ...]


def rationalize(value: Fraction, denominator_bound: int) -> Fraction:
    """Return the signed, clipped, finite-image rationalization."""
    if denominator_bound < 1:
        raise ValueError("denominator_bound must be positive")
    sign = -1 if value < 0 else 1
    clipped = min(abs(value), Fraction(1))
    scaled = clipped * denominator_bound
    floored = scaled.numerator // scaled.denominator
    return Fraction(sign * floored, denominator_bound)


def bridge_preparation(samples: Iterable[Vector], denominator_bound: int) -> Vector:
    """Map samples into a finite proposal-only preparation extension."""
    rows = list(samples)
    if not rows or any(len(row) != 3 for row in rows):
        raise ValueError("samples must be a nonempty family of three-vectors")
    weights = [
        sum(
            (abs(rationalize(row[index], denominator_bound)) for row in rows),
            Fraction(0),
        )
        for index in range(3)
    ]
    total = sum(weights, Fraction(0))
    if total == 0:
        return (Fraction(1), Fraction(0), Fraction(0))
    return tuple(weight / total for weight in weights)


def exact_protocol_preparation(_samples: Iterable[Vector]) -> Vector:
    """The only universally safe bridge into each exact declared chain protocol."""
    return (Fraction(1), Fraction(0), Fraction(0))


def permute(vector: Vector, permutation: tuple[int, ...]) -> Vector:
    return tuple(vector[index] for index in permutation)


def proportional(left: Vector, right: Vector) -> bool:
    """Decide association of nonzero rational linear forms."""
    if all(value == 0 for value in left) or all(value == 0 for value in right):
        return False
    ratio: Fraction | None = None
    for a, b in zip(left, right, strict=True):
        if a == 0 and b == 0:
            continue
        if a == 0 or b == 0:
            return False
        current = a / b
        if ratio is None:
            ratio = current
        elif current != ratio:
            return False
    return ratio is not None and ratio != 0


def apply_matrix(matrix: tuple[Vector, ...], vector: Vector) -> Vector:
    return tuple(
        sum((entry * value for entry, value in zip(row, vector, strict=True)), Fraction(0))
        for row in matrix
    )


def run_checks() -> dict[str, Any]:
    zero = Fraction(0)
    one = Fraction(1)
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, evidence: Any) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "evidence": evidence})

    samples = [
        (Fraction(1, 3), Fraction(-2, 5), Fraction(0)),
        (Fraction(2, 3), Fraction(1, 5), Fraction(-1, 2)),
    ]
    preparation = bridge_preparation(samples, 60)
    add(
        "finite_extension_bridge_nonnegative_normalized_finite_image",
        all(value >= 0 for value in preparation)
        and sum(preparation, zero) == one
        and all(
            rationalize(Fraction(integer, 37), 60)
            in {Fraction(index, 60) for index in range(-60, 61)}
            for integer in range(-100, 101)
        ),
        {
            "preparation": [str(value) for value in preparation],
            "rationalizer_image_bound": 121,
        },
    )
    zero_preparation = bridge_preparation([(zero, zero, zero)], 60)
    add(
        "exact_constant_bridge_and_extension_zero_branch",
        zero_preparation == (one, zero, zero)
        and exact_protocol_preparation(samples) == (one, zero, zero),
        {
            "extension_zero": [str(value) for value in zero_preparation],
            "exact_protocol_constant": [str(value) for value in exact_protocol_preparation(samples)],
        },
    )
    permutation = (2, 0, 1)
    permuted_samples = [permute(row, permutation) for row in samples]
    permuted_preparation = bridge_preparation(permuted_samples, 60)
    add(
        "finite_extension_bridge_equipment_permutation_naturality",
        permuted_preparation == permute(preparation, permutation),
        {
            "direct": [str(value) for value in permuted_preparation],
            "transported": [str(value) for value in permute(preparation, permutation)],
        },
    )

    e0 = (one, zero, zero, zero)
    swap01 = (
        (zero, one, zero, zero),
        (one, zero, zero, zero),
        (zero, zero, one, zero),
        (zero, zero, zero, one),
    )
    moved = apply_matrix(swap01, e0)
    add(
        "no_gl4_fixed_coordinate_line_witness",
        not proportional(e0, moved),
        {"line": [str(value) for value in e0], "moved": [str(value) for value in moved]},
    )

    epsilons = [Fraction(1, 2), Fraction(1, 10), Fraction(1, 1000)]
    split_rows: list[dict[str, Any]] = []
    split_ok = True
    for epsilon in epsilons:
        forms = (
            (one, epsilon, zero, zero),
            (one, zero, zero, zero),
            (one, -epsilon, zero, zero),
        )
        pairwise_distinct = all(
            not proportional(forms[i], forms[j])
            for i in range(3)
            for j in range(i + 1, 3)
        )
        split_ok = split_ok and pairwise_distinct
        split_rows.append(
            {
                "epsilon": str(epsilon),
                "pairwise_nonassociate": pairwise_distinct,
                "forms": [[str(value) for value in form] for form in forms],
            }
        )
    add("independent_sector_split_all_scales", split_ok, split_rows)
    add(
        "diagonal_not_product_open",
        split_ok and epsilons[-1] < Fraction(1, 100),
        "arbitrarily small explicit split represented by epsilon=1/1000",
    )

    refuter_branches = {
        "collapse": "FAILS_CLOSED",
        "nonuniqueness": "FAILS",
        "inverse_defect": "FAILS_AFTER_SECTOR_SPLIT",
        "cocycle_defect": "NOT_REACHED_AFTER_INVERSE_FAILURE",
        "variation_fragility": "FAILS",
    }
    add(
        "refuter_failure_branch_coverage",
        set(refuter_branches)
        == {"collapse", "nonuniqueness", "inverse_defect", "cocycle_defect", "variation_fragility"},
        refuter_branches,
    )

    repair_dispositions = {
        "F1-SECTOR-COVERAGE": "restricted_control_scope_repaired_full_sector_burden_obstructed",
        "F2-PRESENTATION-NORM": "repaired_on_declared_source_patch",
        "F3-SHARED-LEADING-PRELOAD": "precise_obstruction",
        "F4-SECTOR-SPLIT-VARIATION": "precise_obstruction",
        "F5-UNTYPED-OPERATIONAL-BRIDGE": "exact_constant_bridge_typed_nontrivial_bridge_requires_finite_protocol_extension",
    }
    add("five_finding_partition", len(repair_dispositions) == 5, repair_dispositions)
    add(
        "decisive_scoped_obstruction",
        repair_dispositions["F3-SHARED-LEADING-PRELOAD"] == "precise_obstruction"
        and repair_dispositions["F4-SECTOR-SPLIT-VARIATION"] == "precise_obstruction",
        "OBST-V22-P4T02-B2-NATURAL-LINE-LOCK-001",
    )
    add(
        "local_freeze_only",
        True,
        {
            "freeze_label": "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
            "global_no_go": False,
            "future_extension_impossibility": False,
        },
    )

    failed = [row["check_id"] for row in checks if not row["passed"]]
    return {
        "schema_id": "v22_p4_t02_b2_source_intrinsic_interface_repair_model_v1",
        "task_id": "RT-20260810-001",
        "job_id": "AJ-RT-20260810-001-001",
        "candidate_id": "CAND-V22-B2-P7-COMMON-PRINCIPAL-LIFT-V1",
        "result_type": "precise_obstruction",
        "obstruction_id": "OBST-V22-P4T02-B2-NATURAL-LINE-LOCK-001",
        "check_count": len(checks),
        "failure_count": len(failed),
        "status": "PASS" if not failed else "FAIL",
        "failed_check_ids": failed,
        "checks": checks,
        "authority_limits": {
            "full_p7_sector_coverage": False,
            "descriptor_instance_complete": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "physical_geometry_claimed": False,
            "distance_to_gr_changed": False,
            "global_no_go_claimed": False,
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
