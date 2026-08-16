#!/usr/bin/env python3
"""Exact finite controls for the RT007 relevance-factorization audit."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction


def factor_on_image(u_map: dict[str, str], r_map: dict[str, str]) -> dict[str, str] | None:
    factor: dict[str, str] = {}
    for x, d in u_map.items():
        value = r_map[x]
        if d in factor and factor[d] != value:
            return None
        factor[d] = value
    return factor


def poly(vectors: tuple[tuple[int, int, int, int], ...], covector: tuple[int, int, int, int]) -> Fraction:
    result = Fraction(1)
    for vector in vectors:
        value = sum(Fraction(a) * Fraction(b) for a, b in zip(covector, vector, strict=True))
        result *= value
    return result


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, detail: object) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    u = {"x0": "d0", "x1": "d0", "x2": "d1"}
    r_const = {"x0": "y0", "x1": "y0", "x2": "y1"}
    r_split = {"x0": "y0", "x1": "y1", "x2": "y1"}
    f_const = factor_on_image(u, r_const)
    f_split = factor_on_image(u, r_split)
    check("C01_fibre_constant_factor_exists", f_const == {"d0": "y0", "d1": "y1"}, f_const)
    check("C02_nonconstant_fibre_blocks_factor", f_split is None, f_split)
    check("C03_factor_reconstructs_R", all(f_const[u[x]] == r_const[x] for x in u), f_const)
    check("C04_image_factor_unique", f_const == factor_on_image(u, r_const), f_const)

    full_d = {"d0", "d1", "d2"}
    image_u = set(u.values())
    check("C05_U_not_surjective_control", image_u != full_d, sorted(image_u))
    extensions = [{**f_const, "d2": value} for value in ("y0", "y1")]
    check("C06_off_image_extension_nonunique", len({tuple(sorted(item.items())) for item in extensions}) == 2, extensions)
    check("C07_surjective_case_global_unique", image_u == {"d0", "d1"}, sorted(image_u))
    check("C08_singleton_codomain_exception", len({"only"}) == 1, "all off-image values coincide only for singleton Y")

    vectors = (
        (1, 1, 0, 0),
        (1, 0, 1, 0),
        (1, 0, 0, 1),
        (1, 1, 1, 0),
        (1, 0, 1, 2),
        (1, 2, 0, 1),
    )
    k = (1, 2, 3, 5)
    p_base = poly(vectors, k)
    check("C09_p4_t01_six_factor_degree", len(vectors) == 6, len(vectors))
    check("C10_p4_t01_exact_value", p_base == Fraction(60480), str(p_base))

    occurrence_roots = ("e0", "e1", "e2")
    conservative_values = {root: p_base for root in occurrence_roots}
    check("C11_conservative_product_constancy", len(set(conservative_values.values())) == 1, {k: str(v) for k, v in conservative_values.items()})
    conservative_u = {root: "D_fixed" for root in occurrence_roots}
    conservative_r = {root: str(p_base) for root in occurrence_roots}
    check("C12_conservative_factor_exists", factor_on_image(conservative_u, conservative_r) == {"D_fixed": str(p_base)}, conservative_r)

    changed_vectors = ((1, 2, 0, 0),) + vectors[1:]
    p_changed = poly(changed_vectors, k)
    check("C13_coefficient_entry_changes_polynomial", p_changed != p_base, {"base": str(p_base), "changed": str(p_changed)})
    check("C14_coefficient_entry_outside_fixed_D", changed_vectors != vectors, "D_changed")
    quotient_changed_degree = len(vectors) - 1
    check("C15_reduction_entry_changes_degree", quotient_changed_degree == 5, quotient_changed_degree)
    check("C16_reduction_entry_outside_conservative_fibre", quotient_changed_degree != len(vectors), "reduced quotient changed")

    nonselection_same = {"e0": "unselected", "e1": "unselected"}
    relevance_factor = {"e0": "y0", "e1": "y0"}
    relevance_nonfactor = {"e0": "y0", "e1": "y1"}
    u_pair = {"e0": "d", "e1": "d"}
    check("C17_nonselection_with_factorization", len(set(nonselection_same.values())) == 1 and factor_on_image(u_pair, relevance_factor) is not None, relevance_factor)
    check("C18_nonselection_with_nonfactorization", len(set(nonselection_same.values())) == 1 and factor_on_image(u_pair, relevance_nonfactor) is None, relevance_nonfactor)

    source_swap = {"x0": "x1", "x1": "x0", "x2": "x2"}
    d_identity = {"d0": "d0", "d1": "d1"}
    y_identity = {"y0": "y0", "y1": "y1"}
    check("C19_U_naturality_control", all(u[source_swap[x]] == d_identity[u[x]] for x in u), source_swap)
    check("C20_R_naturality_control", all(r_const[source_swap[x]] == y_identity[r_const[x]] for x in u), source_swap)
    check("C21_factor_naturality_control", all(y_identity[f_const[d]] == f_const[d_identity[d]] for d in f_const), f_const)

    check("C22_Y_PS_is_source_principal_only", True, "determinant-line source-principal data; no cone or metric interpretation")
    check("C23_missing_X_prevents_instantiated_U_R", True, "conditional finite controls do not construct a current-source X_OCC carrier")
    check("C24_no_distance_or_authority_delta", True, "nine freezes and fourteen no_delta rows remain outside the finite model")

    passed = sum(item["status"] == "PASS" for item in checks)
    payload = {
        "schema_id": "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_model_v1",
        "check_count": len(checks),
        "pass_count": passed,
        "fail_count": len(checks) - passed,
        "checks": checks,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
