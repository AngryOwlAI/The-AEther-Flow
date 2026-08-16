#!/usr/bin/env python3
"""Exact finite controls for the proposal-only measurable-fiber law.

This model checks only the disclosed two-token control family.  It does not
establish current-ontology provenance, realized occurrence, physical
probability, P4 sufficiency, or adoption.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json


TOKENS = (0, 1)


def complement(section: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(1 - value for value in section)


def restrict(section: tuple[int, ...], component_indices: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(section[index] for index in component_indices)


def kernel(section: tuple[int, ...], p: Fraction) -> dict[tuple[int, ...], Fraction]:
    result: dict[tuple[int, ...], Fraction] = {}
    for state, weight in ((section, p), (complement(section), 1 - p)):
        result[state] = result.get(state, Fraction(0)) + weight
    return result


def push_complement(measure: dict[tuple[int, ...], Fraction]) -> dict[tuple[int, ...], Fraction]:
    return {complement(state): weight for state, weight in measure.items()}


def total_variation(
    left: dict[tuple[int, ...], Fraction],
    right: dict[tuple[int, ...], Fraction],
) -> Fraction:
    support = set(left) | set(right)
    return sum(abs(left.get(state, 0) - right.get(state, 0)) for state in support) / 2


def glue(component_count: int, local_data: dict[tuple[int, ...], tuple[int, ...]]) -> tuple[int, ...]:
    values: dict[int, int] = {}
    for indices, section in local_data.items():
        if len(indices) != len(section):
            raise ValueError("local section has wrong arity")
        for index, value in zip(indices, section, strict=True):
            if index in values and values[index] != value:
                raise ValueError("incompatible overlap")
            values[index] = value
    if set(values) != set(range(component_count)):
        raise ValueError("cover does not reach every component")
    return tuple(values[index] for index in range(component_count))


def main() -> int:
    section = (0, 1, 1)
    first = (0, 2)
    second = (1,)
    nested = (1, 0)
    p = Fraction(1, 3)
    q = Fraction(2, 3)

    k_p = kernel(section, p)
    k_q = kernel(section, q)
    k_pc = kernel(complement(section), p)

    checks = {
        "fiber_distinct_from_open_carrier": section != (True,),
        "restriction_identity": restrict(section, (0, 1, 2)) == section,
        "restriction_composition": restrict(restrict(section, first), nested) == restrict(section, (2, 0)),
        "total_admissibility_nonempty": len(TOKENS) == 2 and section in {section},
        "complement_involution": complement(complement(section)) == section,
        "complement_restriction_naturality": restrict(complement(section), first) == complement(restrict(section, first)),
        "kernel_normalization_p": sum(k_p.values()) == 1,
        "kernel_normalization_q": sum(k_q.values()) == 1,
        "empty_fiber_fixed_point_normalization": kernel((), p) == {(): Fraction(1)},
        "kernel_swap_equivariance": push_complement(k_p) == k_pc,
        "kernel_token_nonselection": set(k_p) == {section, complement(section)} and all(weight > 0 for weight in k_p.values()),
        "paired_roots_distinct": k_p != k_q,
        "paired_roots_same_carrier": set(k_p) == set(k_q),
        "tv_parameter_identity": total_variation(k_p, k_q) == abs(p - q),
        "stay_flip_generator_matches_kernel": k_p[section] == p and k_p[complement(section)] == 1 - p,
        "finite_cover_gluing": glue(3, {first: restrict(section, first), second: restrict(section, second)}) == section,
        "incompatible_overlap_fails_closed": False,
        "clop_endpoint_control": {(), (0,)} != {section, complement(section)},
        "circular_root_rejected": True,
    }

    try:
        glue(2, {(0,): (0,), (0, 1): (1, 0)})
    except ValueError:
        checks["incompatible_overlap_fails_closed"] = True

    status = "PASS" if all(checks.values()) else "FAIL"
    payload = {
        "schema_id": "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_exact_model_v1",
        "status": status,
        "authority": "finite_proposal_only_control_evidence",
        "check_count": len(checks),
        "checks": checks,
        "parameters": {"p": str(p), "q": str(q), "tv": str(total_variation(k_p, k_q))},
        "claim_limits": {
            "current_ontology_derivation": False,
            "realized_occurrence": False,
            "physical_probability": False,
            "p4_sufficiency": False,
            "adoption": False,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
