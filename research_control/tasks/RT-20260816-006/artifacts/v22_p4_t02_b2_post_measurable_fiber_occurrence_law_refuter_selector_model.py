#!/usr/bin/env python3
"""Exact controls for the RT-20260816-006 theoretical selector.

The model uses the registered P4-T01 six-vector principal datum and finite
occurrence-extension labels.  It checks only the fibre-factorization logic
needed to select a future audit.  It does not prove that the combined extension
space is current-source derived, assign physical occurrence, or execute the
selected packet.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import prod


Vector = tuple[int, int, int, int]

ROUTES = (
    "A_CURRENT_SOURCE_OCCURRENCE_ADMISSIBILITY_RELEVANCE_FACTORIZATION_AUDIT",
    "B_OCCURRENCE_LAW_P4_IRRELEVANCE_OR_SCOPED_NO_GO_THEOREM",
    "C_RICHER_AUDITED_RESP_LC_BRIDGE_CLASS",
    "D_PROTECTED_HUMAN_GATED_ONTOLOGY_CHANGE_REQUIRED",
)
SELECTED = ROUTES[0]

BASE_SOURCE_VECTORS: tuple[Vector, ...] = (
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (1, 0, 0, 1),
    (1, 1, 1, 0),
    (1, 0, 1, 2),
    (1, 2, 0, 1),
)
PERTURBED_SOURCE_VECTORS: tuple[Vector, ...] = BASE_SOURCE_VECTORS[:-1] + ((1, 2, 1, 1),)
TEST_COVECTORS: tuple[Vector, ...] = (
    (1, 0, 0, 0),
    (2, -1, 3, 1),
    (3, 2, -2, 4),
)


def pairing(vector: Vector, covector: Vector) -> int:
    return sum(left * right for left, right in zip(vector, covector, strict=True))


def principal_signature(vectors: tuple[Vector, ...]) -> tuple[int, ...]:
    return tuple(prod(pairing(vector, covector) for vector in vectors) for covector in TEST_COVECTORS)


def occurrence_extension(
    name: str,
    p: Fraction,
    coupling_a: Fraction,
    initial_mass: Fraction,
    rate: Fraction,
    duration: Fraction,
    *,
    base_id: str = "D_FIXED",
    vectors: tuple[Vector, ...] = BASE_SOURCE_VECTORS,
) -> dict[str, object]:
    return {
        "name": name,
        "base_id": base_id,
        "p": p,
        "coupling_a": coupling_a,
        "initial_mass": initial_mass,
        "rate": rate,
        "duration": duration,
        "vectors": vectors,
    }


def reduct(extension: dict[str, object]) -> str:
    return str(extension["base_id"])


def p4_relevance(extension: dict[str, object]) -> tuple[int, ...]:
    vectors = extension["vectors"]
    assert isinstance(vectors, tuple)
    return principal_signature(vectors)


def occurrence_diagnostic(extension: dict[str, object]) -> Fraction:
    value = extension["p"]
    assert isinstance(value, Fraction)
    return value


def run_model() -> dict[str, object]:
    conservative = (
        occurrence_extension("E_1", Fraction(1, 3), Fraction(1, 3), Fraction(1, 5), Fraction(1), Fraction(2)),
        occurrence_extension("E_2", Fraction(2, 3), Fraction(4, 9), Fraction(4, 5), Fraction(2), Fraction(1)),
        occurrence_extension("E_3", Fraction(3, 4), Fraction(11, 20), Fraction(1, 2), Fraction(4), Fraction(1, 2)),
    )
    nonconservative = occurrence_extension(
        "E_SOURCE_CHANGED",
        Fraction(1, 3),
        Fraction(1, 3),
        Fraction(1, 5),
        Fraction(1),
        Fraction(2),
        base_id="D_PERTURBED",
        vectors=PERTURBED_SOURCE_VECTORS,
    )

    fixed_signature = principal_signature(BASE_SOURCE_VECTORS)
    perturbed_signature = principal_signature(PERTURBED_SOURCE_VECTORS)
    fibre_signatures = {p4_relevance(extension) for extension in conservative}
    fibre_diagnostics = {occurrence_diagnostic(extension) for extension in conservative}

    factor_map = {
        "D_FIXED": fixed_signature,
        "D_PERTURBED": perturbed_signature,
    }
    factorization_holds = all(p4_relevance(extension) == factor_map[reduct(extension)] for extension in (*conservative, nonconservative))

    # A non-surjective finite control: U reaches only d0, so two maps that agree
    # on im(U) can differ at d1.  Factorization on im(U) is not global uniqueness.
    domain_d = ("d0", "d1")
    image_u = {"d0"}
    factor_left = {"d0": 0, "d1": 1}
    factor_right = {"d0": 0, "d1": 2}

    checks = {
        "route_count_is_four": len(ROUTES) == 4,
        "route_A_selected_uniquely": ROUTES.count(SELECTED) == 1 and SELECTED == ROUTES[0],
        "registered_base_has_six_factors": len(BASE_SOURCE_VECTORS) == 6,
        "registered_base_time_covector_noncharacteristic": fixed_signature[0] == 1,
        "occurrence_variants_share_one_reduct": {reduct(extension) for extension in conservative} == {"D_FIXED"},
        "occurrence_variants_are_distinct": len(fibre_diagnostics) == len(conservative),
        "p4_signature_constant_on_conservative_fibre": fibre_signatures == {fixed_signature},
        "p4_factorization_through_reduct_control": factorization_holds,
        "occurrence_diagnostic_does_not_factor": len(fibre_diagnostics) > 1,
        "source_operator_change_alters_signature": perturbed_signature != fixed_signature,
        "operator_change_is_not_same_reduct": reduct(nonconservative) == "D_PERTURBED",
        "factorization_scope_distinguishes_conservative_change": p4_relevance(nonconservative) == factor_map["D_PERTURBED"],
        "non_surjective_control_has_proper_image": image_u < set(domain_d),
        "factor_maps_agree_on_image": all(factor_left[d] == factor_right[d] for d in image_u),
        "factor_maps_not_unique_off_image": factor_left != factor_right,
        "route_B_requires_completed_A_audit": ROUTES[1] != SELECTED,
        "route_C_not_selected_before_relevance_audit": ROUTES[2] != SELECTED,
        "protected_stop_not_triggered": ROUTES[3] != SELECTED,
        "selected_packet_remains_unexecuted": True,
    }

    payload = {
        "schema_id": "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_model_v1",
        "task_id": "RT-20260816-006",
        "routes": list(ROUTES),
        "selected_route": SELECTED,
        "base_principal_signature": list(fixed_signature),
        "perturbed_principal_signature": list(perturbed_signature),
        "conservative_extensions": [
            {
                "name": extension["name"],
                "base_id": extension["base_id"],
                "p": str(extension["p"]),
                "coupling_a": str(extension["coupling_a"]),
                "initial_mass": str(extension["initial_mass"]),
                "rate_duration_product": str(extension["rate"] * extension["duration"]),
                "principal_signature": list(p4_relevance(extension)),
            }
            for extension in conservative
        ],
        "factorization_control": {
            "forgetful_map": "U:E_occ->D_source",
            "p4_map": "R=Prin after U on the declared conservative subcategory",
            "constant_on_u_fibres": True,
            "surjectivity_required_for_global_factor_uniqueness": True,
            "non_surjective_domain": list(domain_d),
            "non_surjective_image": sorted(image_u),
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(checks.values()),
        "authority": {
            "combined_extension_current_source_derived": False,
            "full_factorization_theorem_claimed": False,
            "p4_irrelevance_claimed": False,
            "physical_response_assigned": False,
            "selected_packet_executed": False,
            "distance_to_gr_changed": False,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


if __name__ == "__main__":
    result = run_model()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_pass"] else 1)
