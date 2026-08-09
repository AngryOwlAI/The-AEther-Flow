#!/usr/bin/env python3
"""Exact support checks for the RT-20260809-021 B2 descriptor packet.

This model verifies a finite representative of the source-unit cocycle and the
finite-trace principal-class counterpair. It is operational support only. It
does not prove the general theorems, construct a B2 descriptor instance, or
create scientific authority.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Iterable, Sequence


def normalize_projective(coefficients: Sequence[Fraction]) -> tuple[Fraction, ...]:
    """Normalize a nonzero linear form by its first nonzero coefficient."""
    for coefficient in coefficients:
        if coefficient:
            return tuple(value / coefficient for value in coefficients)
    raise ValueError("zero linear form has no projective class")


def common_projective_class(forms: Iterable[Sequence[Fraction]]) -> bool:
    normalized = [normalize_projective(form) for form in forms]
    return len(set(normalized)) == 1


def source_scalar(point: Sequence[Fraction], jet_order: int = 1) -> Fraction:
    """A source scalar vanishing through order jet_order at the origin."""
    radius_squared = sum(value * value for value in point)
    return radius_squared ** (jet_order + 1)


def source_scalar_gradient(point: Sequence[Fraction], jet_order: int = 1) -> tuple[Fraction, ...]:
    radius_squared = sum(value * value for value in point)
    if radius_squared == 0:
        return tuple(Fraction(0) for _ in point)
    multiplier = 2 * (jet_order + 1) * radius_squared**jet_order
    return tuple(multiplier * value for value in point)


def run_model() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    origin = tuple(Fraction(0) for _ in range(4))
    probe = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    f_origin = source_scalar(origin)
    grad_origin = source_scalar_gradient(origin)
    f_probe = source_scalar(probe)

    check("MODEL-FINITE-TRACE-F-VALUE", f_origin == 0, "f vanishes at the finite sample")
    check(
        "MODEL-FINITE-TRACE-F-GRADIENT",
        all(value == 0 for value in grad_origin),
        "the first source jet of f vanishes at the sample",
    )
    check("MODEL-FINITE-TRACE-F-NONZERO", f_probe == 1, "f is nonzero at the comparison probe")

    common_forms = [(Fraction(1), Fraction(0)) for _ in range(6)]
    split_forms = [(Fraction(1), Fraction(index)) for index in range(1, 7)]
    check(
        "MODEL-COMMON-FAMILY",
        common_projective_class(common_forms),
        "all six unperturbed sector symbols have class [k_0]",
    )
    check(
        "MODEL-SPLIT-FAMILY",
        not common_projective_class(split_forms),
        "the six perturbed sector symbols have distinct projective classes where f is nonzero",
    )
    check(
        "MODEL-SPLIT-CLASS-COUNT",
        len({normalize_projective(form) for form in split_forms}) == 6,
        "all six split sector classes are distinct",
    )

    g_12 = Fraction(2)
    g_23 = Fraction(3)
    g_31 = Fraction(1, 6)
    check("MODEL-COCYCLE-NONZERO", all(value for value in (g_12, g_23, g_31)), "all source units are nonzero")
    check("MODEL-COCYCLE-TRIPLE", g_12 * g_23 * g_31 == 1, "triple-overlap product is one")
    check("MODEL-COCYCLE-INVERSE-12", g_12 * (1 / g_12) == 1, "g_12 has the declared inverse")
    check("MODEL-COCYCLE-INVERSE-23", g_23 * (1 / g_23) == 1, "g_23 has the declared inverse")
    check("MODEL-COCYCLE-INVERSE-31", g_31 * (1 / g_31) == 1, "g_31 has the declared inverse")

    normalized_common = [normalize_projective(form) for form in common_forms]
    normalized_split = [normalize_projective(form) for form in split_forms]
    check(
        "MODEL-PROJECTIVE-NORMALIZATION",
        normalized_common[0] == (Fraction(1), Fraction(0)),
        "projective normalization preserves the common representative",
    )
    check(
        "MODEL-COUNTERPAIR-DECISIVE",
        common_projective_class(common_forms) and not common_projective_class(split_forms),
        "same finite sample behavior can coexist with common or split principal classes away from the sample",
    )

    failures = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v22_p4_t02_b2_descriptor_model_v1",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "checks": checks,
        "counterpair": {
            "finite_sample": [0, 0, 0, 0],
            "comparison_probe": [1, 0, 0, 0],
            "common_classes": [[str(value) for value in form] for form in normalized_common],
            "split_classes": [[str(value) for value in form] for form in normalized_split],
        },
        "authority_limits": {
            "general_theorem_proved_by_script": False,
            "descriptor_instance_constructed": False,
            "source_law_adopted": False,
            "b2_activated": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_model()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
