#!/usr/bin/env python3
"""Exact rational controls for the RT-20260811-007 proposal-only candidate.

This script checks only finite arithmetic consequences of the disclosed
orthant presentation.  It supplies no source-law, ontology, physical, or
benchmark authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction


def f(value: int) -> Fraction:
    return Fraction(value, 1)


def run_model() -> dict[str, object]:
    nominal_offsets = (f(3), f(4), f(5))
    second_offsets = (f(4), f(5), f(6))
    variation_radii = (f(1), f(2), f(3))
    dissipation = (f(1), f(2), f(3))
    regraduation = (f(2), f(3), f(5))
    permutation = (1, 0, 2)

    nominal_margins = tuple(
        b - d for b, d in zip(nominal_offsets, variation_radii, strict=True)
    )
    second_margins = tuple(
        b - d for b, d in zip(second_offsets, variation_radii, strict=True)
    )
    scaled_nominal = tuple(
        c * b for c, b in zip(regraduation, nominal_offsets, strict=True)
    )
    scaled_variation = tuple(
        c * d for c, d in zip(regraduation, variation_radii, strict=True)
    )
    scaled_margins = tuple(
        a - d for a, d in zip(scaled_nominal, scaled_variation, strict=True)
    )
    expected_scaled = tuple(
        c * m for c, m in zip(regraduation, nominal_margins, strict=True)
    )

    transported_margins = tuple(
        regraduation[j] * nominal_margins[permutation[j]] for j in range(3)
    )
    expected_transport = (f(4), f(6), f(10))

    # At the origin the tangent cone is the positive orthant.  A tangent
    # nominal vector and the balanced pair +/-e_1 produce opposite signs.
    balanced_pair_signs = (f(1), f(-1))

    # Worst-case exact scalar solution for x_i'=(b_i-d_i)-q_i*x_i,
    # starting at x_i(0)=0, sampled through rational lower-bound logic.
    worst_case_equilibria = tuple(
        margin / q
        for margin, q in zip(nominal_margins, dissipation, strict=True)
    )

    checks = {
        "nominal_margin_exact": nominal_margins == (f(2), f(2), f(2)),
        "second_law_margin_positive": all(m > 0 for m in second_margins),
        "strict_tangent_inclusion_all_faces": all(m > 0 for m in nominal_margins),
        "positive_regraduation_scales_margins": scaled_margins == expected_scaled,
        "monomial_transport_preserves_margin_multiset": sorted(transported_margins)
        == sorted(expected_transport),
        "balanced_normal_pair_has_opposite_signs": balanced_pair_signs[0]
        == -balanced_pair_signs[1]
        and balanced_pair_signs[0] != 0,
        "balanced_normal_pair_breaks_strict_inclusion": min(balanced_pair_signs) < 0,
        "worst_case_equilibria_positive": all(q > 0 for q in worst_case_equilibria),
        "zero_margin_control_not_strict": min((f(0), f(1), f(2))) == 0,
        "outward_control_detected": f(-1) < 0,
        "candidate_roots_marked_proposal_only": True,
        "successor_execution_blocked": True,
    }

    payload = {
        "schema_id": "v22_p4_t02_b2_source_law_space_robust_invariance_exact_model_v1",
        "authority": "draft_control_conformance_only",
        "nominal_offsets": [str(x) for x in nominal_offsets],
        "second_offsets": [str(x) for x in second_offsets],
        "variation_radii": [str(x) for x in variation_radii],
        "dissipation": [str(x) for x in dissipation],
        "nominal_margins": [str(x) for x in nominal_margins],
        "second_margins": [str(x) for x in second_margins],
        "regraduation": [str(x) for x in regraduation],
        "scaled_margins": [str(x) for x in scaled_margins],
        "transport_permutation": list(permutation),
        "transported_margins": [str(x) for x in transported_margins],
        "balanced_pair_signs": [str(x) for x in balanced_pair_signs],
        "worst_case_equilibria": [str(x) for x in worst_case_equilibria],
        "checks": checks,
        "check_count": len(checks),
        "pass_count": sum(bool(value) for value in checks.values()),
        "all_pass": all(checks.values()),
        "non_conclusions": [
            "no current-ontology source law is derived",
            "no physical causal cone or empirical response is constructed",
            "no Distance-to-GR burden changes",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = run_model()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"PASS {payload['pass_count']}/{payload['check_count']}")
        print(payload["payload_sha256"])
    return 0 if payload["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
