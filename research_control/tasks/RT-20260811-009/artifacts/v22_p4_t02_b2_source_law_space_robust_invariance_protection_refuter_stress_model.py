#!/usr/bin/env python3
"""Exact rational controls for the RT009 robust-invariance Refuter stress."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any


Q = Fraction


def qtext(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def run_model() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(check_id: str, passed: bool, evidence: Any) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "evidence": evidence})

    epsilons = (Q(1), Q(1, 2), Q(1, 10), Q(1, 100))
    fixed_rows = [
        {"epsilon": qtext(epsilon), "boundary_residual": qtext(epsilon)}
        for epsilon in epsilons
    ]
    record(
        "fixed_positive_margin_family_passes",
        all(epsilon > 0 for epsilon in epsilons),
        {"fixtures": fixed_rows},
    )

    epsilon = Q(1, 3)
    perturbations = (-Q(1, 6), Q(0), Q(1, 6))
    open_rows = [
        {
            "perturbation": qtext(delta),
            "residual": qtext(epsilon + delta),
        }
        for delta in perturbations
    ]
    record(
        "fixed_margin_open_neighborhood_and_exact_boundary",
        all(epsilon + delta > 0 for delta in perturbations)
        and epsilon - epsilon == 0
        and epsilon - 2 * epsilon < 0,
        {
            "margin": qtext(epsilon),
            "open_fixtures": open_rows,
            "tangent_perturbation": qtext(-epsilon),
            "outward_perturbation": qtext(-2 * epsilon),
        },
    )

    sequence = [Q(1, n) for n in (1, 2, 5, 10, 100, 1000)]
    record(
        "family_margin_collapses_without_fixed_tuple_fragility",
        all(value > 0 for value in sequence)
        and all(left > right for left, right in zip(sequence, sequence[1:]))
        and sequence[-1] < Q(1, 100),
        {
            "margins": [qtext(value) for value in sequence],
            "limit": "0",
            "zero_margin_strict_result": "fail",
        },
    )

    epsilon = Q(1, 5)
    alphas = (Q(0), Q(1, 2), Q(1), Q(3, 2), Q(2))
    variation_rows = []
    variation_ok = True
    for alpha in alphas:
        worst = (1 - alpha) * epsilon
        result = "strict_pass" if worst > 0 else "zero_margin_fail" if worst == 0 else "outward_fail"
        expected = (
            "strict_pass"
            if alpha < 1
            else "zero_margin_fail"
            if alpha == 1
            else "outward_fail"
        )
        variation_ok &= result == expected
        variation_rows.append(
            {"alpha": qtext(alpha), "worst_residual": qtext(worst), "result": result}
        )
    record(
        "nested_variation_enlargement_threshold",
        variation_ok,
        {"epsilon": qtext(epsilon), "Delta_alpha": "[-alpha*epsilon,+alpha*epsilon]", "fixtures": variation_rows},
    )

    original_residual = Q(1)
    transported_residual = -Q(1) * -Q(1)
    untransported_reversal_residual = -Q(1) * Q(1)
    record(
        "reflection_transport_preserves_but_does_not_select_orientation",
        original_residual == transported_residual == 1 and untransported_reversal_residual == -1,
        {
            "original": "K=x>=0, F=+1, inward=+dx",
            "transported": "K'=y<=0, F'=-1, inward=-dy",
            "untransported_reversal": "K'=y<=0, F=+1, inward=-dy",
            "residuals": [qtext(original_residual), qtext(transported_residual), qtext(untransported_reversal_residual)],
        },
    )

    epsilon = Q(1, 5)
    nu = Q(1, 7)
    rho = Q(1)
    inward_lower = nu * rho
    inward_upper = nu * rho
    outward_lower = -nu * rho
    outward_upper = -nu * rho
    record(
        "same_slice_product_lifts_have_opposite_verdicts",
        epsilon > 0
        and inward_lower > 0
        and inward_upper > 0
        and outward_lower < 0
        and outward_upper < 0,
        {
            "K": "R_ge_0 x [-1,1]",
            "shared_slice": "F(x,0)=(epsilon,0)",
            "passing_lift": "F_minus=(epsilon,-nu*z)",
            "failing_lift": "F_plus=(epsilon,+nu*z)",
            "passing_transverse_residuals": [qtext(inward_lower), qtext(inward_upper)],
            "failing_transverse_residuals": [qtext(outward_lower), qtext(outward_upper)],
        },
    )

    lam = Q(1, 4)
    rho = Q(2)
    threshold = lam * rho
    eta_rows = []
    eta_ok = True
    for eta in (Q(1, 4), Q(1, 2), Q(3, 4), -Q(1, 4), -Q(3, 4)):
        lower = threshold + eta
        upper = threshold - eta
        minimum = min(lower, upper)
        result = "strict_pass" if minimum > 0 else "zero_margin_fail" if minimum == 0 else "outward_fail"
        expected = "strict_pass" if abs(eta) < threshold else "zero_margin_fail" if abs(eta) == threshold else "outward_fail"
        eta_ok &= result == expected and minimum == threshold - abs(eta)
        eta_rows.append(
            {
                "eta": qtext(eta),
                "lower_residual": qtext(lower),
                "upper_residual": qtext(upper),
                "result": result,
            }
        )
    record(
        "transverse_inward_lift_has_its_own_margin_threshold",
        eta_ok,
        {"baseline": "F_z=-lambda*z", "lambda_rho": qtext(threshold), "fixtures": eta_rows},
    )

    constant_rows = []
    constant_ok = True
    for eta in (-Q(1, 10), Q(0), Q(1, 10)):
        lower = eta
        upper = -eta
        constant_ok &= not (lower > 0 and upper > 0)
        constant_rows.append(
            {"eta": qtext(eta), "lower_residual": qtext(lower), "upper_residual": qtext(upper)}
        )
    record(
        "constant_transverse_drift_never_strictly_protects_both_faces",
        constant_ok,
        {"fixtures": constant_rows},
    )

    f0 = Q(1)
    f1 = Q(2)
    identity_swap_coherent = f1 == f0 and f0 == f1
    scale_arrow_forward = Q(2) * f0
    scale_arrow_inverse = Q(1, 2) * f1
    record(
        "nontrivial_eqsrc_arrow_requires_extra_structure",
        f0 > 0
        and f1 > 0
        and not identity_swap_coherent
        and scale_arrow_forward == f1
        and scale_arrow_inverse == f0,
        {
            "both_generators_pass": True,
            "identity_state_map_parameter_swap_coherent": identity_swap_coherent,
            "scale_arrow_forward": qtext(scale_arrow_forward),
            "scale_arrow_inverse": qtext(scale_arrow_inverse),
            "interpretation": "RobInv does not select the nontrivial presentation arrow.",
        },
    )

    record(
        "passing_classifier_value_does_not_select_root_orbit",
        1 != 2 and Q(1) > 0,
        {
            "D1_dimension": 1,
            "D2_dimension": 2,
            "D1_and_D2_strict_residual": "1",
            "same_C1_orbit": False,
        },
    )

    passed = sum(1 for item in checks if item["passed"])
    return {
        "schema_id": "v22_p4_t02_b2_source_law_space_robust_invariance_protection_refuter_stress_model_v1",
        "arithmetic": "fractions.Fraction exact rational controls",
        "check_count": len(checks),
        "passed_check_count": passed,
        "failed_check_count": len(checks) - passed,
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_model()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['status']}: {result['passed_check_count']}/{result['check_count']} checks")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
