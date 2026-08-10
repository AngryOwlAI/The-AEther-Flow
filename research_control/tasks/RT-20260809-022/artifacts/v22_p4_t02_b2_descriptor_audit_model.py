#!/usr/bin/env python3
"""Executable support model for the RT-20260809-022 smuggling audit.

This model checks bounded witnesses for the source-fiber invariance criterion,
the homogeneous polynomial counterexample, and exact audit cardinalities.  It
does not prove a descriptor instance or supply physics authority.
"""

from __future__ import annotations

import argparse
import itertools
import json
from typing import Any


COMPONENT_IDS = (
    "D0_SECTOR_SET",
    "D1_CONTINUUM_FIELDS",
    "D2_FINITE_TO_CONTINUUM_LIFT",
    "D3_SOURCE_QUOTIENT",
    "D3_OUTPUT_QUOTIENT",
    "D4_SECTOR_EQUATIONS",
    "D5_COMPATIBILITY_RELATION",
    "D5_COMMON_PRINCIPAL_TARGET",
    "D6_OPERATIONAL_NO_TARGET_RECEIPT",
    "D7_ADEQUACY_PROCEDURE",
)

OBLIGATION_IDS = tuple(
    f"D{family}-O{index}"
    for family in range(1, 8)
    for index in range(1, 6)
)


def source_term(source: tuple[int, int], target: str, authority: str) -> int:
    """A deliberately source-only term used to exercise fiber invariance."""
    del target, authority
    return source[0] * source[0] + 3 * source[1]


def polynomial_counterexample(bound: int = 3) -> dict[str, Any]:
    checked = 0
    mismatches: list[tuple[int, int, int, int]] = []
    for k in itertools.product(range(-bound, bound + 1), repeat=4):
        if k == (0, 0, 0, 0):
            continue
        k0, k1, _, _ = k
        p = k0
        q = k0 * (k0 * k0 + k1 * k1)
        checked += 1
        if (p == 0) != (q == 0):
            mismatches.append(k)
    nonunit_witness = (0, 0, 1, 0)
    coefficient_at_witness = nonunit_witness[0] ** 2 + nonunit_witness[1] ** 2
    return {
        "bounded_nonzero_covectors_checked": checked,
        "real_zero_set_mismatch_count": len(mismatches),
        "nonunit_projective_witness": list(nonunit_witness),
        "quotient_factor_at_witness": coefficient_at_witness,
        "quotient_factor_is_nowhere_zero": coefficient_at_witness != 0,
        "symbolic_reason": (
            "Over the reals, k0^2+k1^2=0 implies k0=k1=0, a subset of "
            "k0=0; the quotient factor vanishes there and is not a unit."
        ),
    }


def fiber_invariance_witness() -> dict[str, Any]:
    sources = ((0, 0), (1, 2), (-2, 5))
    targets = ("none", "desired_gr_cone", "target_metric")
    authorities = ("role_a", "role_b", "validator_pass", "validator_fail")
    failure_count = 0
    comparison_count = 0
    for source in sources:
        expected = source_term(source, targets[0], authorities[0])
        for target in targets:
            for authority in authorities:
                comparison_count += 1
                if source_term(source, target, authority) != expected:
                    failure_count += 1
    return {
        "source_fibers_checked": len(sources),
        "target_authority_comparisons": comparison_count,
        "failure_count": failure_count,
        "factorization_witness": "F_source(s0,s1)=s0^2+3*s1",
    }


def run() -> dict[str, Any]:
    polynomial = polynomial_counterexample()
    fibers = fiber_invariance_witness()
    checks = {
        "component_count_is_10": len(COMPONENT_IDS) == 10,
        "component_ids_unique": len(set(COMPONENT_IDS)) == 10,
        "obligation_count_is_35": len(OBLIGATION_IDS) == 35,
        "obligation_ids_unique": len(set(OBLIGATION_IDS)) == 35,
        "fiber_invariance_witness_passes": fibers["failure_count"] == 0,
        "bounded_real_zero_sets_agree": polynomial["real_zero_set_mismatch_count"] == 0,
        "quotient_factor_has_zero": polynomial["quotient_factor_is_nowhere_zero"] is False,
    }
    failures = [name for name, passed in checks.items() if not passed]
    return {
        "schema_id": "v22_p4_t02_b2_descriptor_audit_model_v1",
        "task_id": "RT-20260809-022",
        "job_id": "AJ-RT-20260809-022-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "checks": checks,
        "component_ids": list(COMPONENT_IDS),
        "obligation_ids": list(OBLIGATION_IDS),
        "fiber_invariance": fibers,
        "polynomial_counterexample": polynomial,
        "authority_limits": {
            "bounded_model_is_general_proof": False,
            "descriptor_instance_constructed": False,
            "source_law_adopted": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "physical_cone_constructed": False,
            "proof_authority": False,
        },
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
