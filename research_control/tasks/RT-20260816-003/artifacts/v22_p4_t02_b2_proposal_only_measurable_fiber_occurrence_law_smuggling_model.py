#!/usr/bin/env python3
"""Exact controls for the measurable-fiber occurrence-law smuggling audit.

This finite model checks proposal mathematics only.  It assigns no physical
probability, occurrence, time, response, causal, metric, or adoption meaning.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction


State = tuple[int, ...]


def complement(state: State) -> State:
    return tuple(1 - bit for bit in state)


def shared_kernel(state: State, p: Fraction) -> dict[State, Fraction]:
    return {state: p, complement(state): 1 - p}


def componentwise_iid_kernel(state: State, p: Fraction) -> dict[State, Fraction]:
    out: dict[State, Fraction] = {}
    for mask in range(1 << len(state)):
        flips = tuple((mask >> index) & 1 for index in range(len(state)))
        target = tuple(bit ^ flip for bit, flip in zip(state, flips))
        weight = Fraction(1)
        for flip in flips:
            weight *= p if flip == 0 else 1 - p
        out[target] = out.get(target, Fraction(0)) + weight
    return out


def token_class_kernel(state: State, p: Fraction) -> dict[State, Fraction]:
    """Use one independent stay/flip driver for each token value present."""
    classes = tuple(sorted(set(state)))
    out: dict[State, Fraction] = {}
    for mask in range(1 << len(classes)):
        flip_for = {token: (mask >> index) & 1 for index, token in enumerate(classes)}
        target = tuple(bit ^ flip_for[bit] for bit in state)
        weight = Fraction(1)
        for token in classes:
            weight *= p if flip_for[token] == 0 else 1 - p
        out[target] = out.get(target, Fraction(0)) + weight
    return out


def marginal(kernel: dict[State, Fraction], coordinate: int) -> dict[int, Fraction]:
    out = {0: Fraction(0), 1: Fraction(0)}
    for state, weight in kernel.items():
        out[state[coordinate]] += weight
    return out


def push_complement(kernel: dict[State, Fraction]) -> dict[State, Fraction]:
    return {complement(state): weight for state, weight in kernel.items()}


def restrict_state(state: State, component_map: tuple[int, ...]) -> State:
    return tuple(state[source_index] for source_index in component_map)


def push_restriction(
    kernel: dict[State, Fraction], component_map: tuple[int, ...]
) -> dict[State, Fraction]:
    out: dict[State, Fraction] = {}
    for state, weight in kernel.items():
        target = restrict_state(state, component_map)
        out[target] = out.get(target, Fraction(0)) + weight
    return out


def one_bit_kernel(bit: int, p: Fraction) -> dict[int, Fraction]:
    return {bit: p, 1 - bit: 1 - p}


def apply_one_bit(initial: dict[int, Fraction], p: Fraction) -> dict[int, Fraction]:
    out = {0: Fraction(0), 1: Fraction(0)}
    for bit, mass in initial.items():
        for target, weight in one_bit_kernel(bit, p).items():
            out[target] += mass * weight
    return out


def tv(left: dict[int, Fraction], right: dict[int, Fraction]) -> Fraction:
    return sum(abs(left[k] - right[k]) for k in set(left) | set(right)) / 2


def build_payload() -> dict[str, object]:
    p = Fraction(1, 3)
    q = Fraction(2, 3)
    x = (0, 1)
    shared = shared_kernel(x, p)
    componentwise_iid = componentwise_iid_kernel(x, p)
    token_class = token_class_kernel(x, p)
    uniform = {0: Fraction(1, 2), 1: Fraction(1, 2)}
    delta0 = {0: Fraction(1), 1: Fraction(0)}
    delta1 = {0: Fraction(0), 1: Fraction(1)}

    shared_from_complement = shared_kernel(complement(x), p)
    componentwise_iid_from_complement = componentwise_iid_kernel(complement(x), p)
    token_class_from_complement = token_class_kernel(complement(x), p)
    shared_marginal_0 = marginal(shared, 0)
    shared_marginal_1 = marginal(shared, 1)
    componentwise_iid_marginal_0 = marginal(componentwise_iid, 0)
    componentwise_iid_marginal_1 = marginal(componentwise_iid, 1)
    token_class_marginal_0 = marginal(token_class, 0)
    token_class_marginal_1 = marginal(token_class, 1)
    expected_marginal = one_bit_kernel(0, p)
    expected_second_marginal = one_bit_kernel(1, p)
    connected_state = (0,)
    split_map = (0, 0)
    mixed_map = (0, 1, 0)

    checks = {
        "shared_kernel_normalized": sum(shared.values()) == 1,
        "componentwise_iid_kernel_normalized": sum(componentwise_iid.values()) == 1,
        "token_class_kernel_normalized": sum(token_class.values()) == 1,
        "shared_and_token_class_are_distinct_on_mixed_section": shared != token_class,
        "shared_support_is_two_point_complement_orbit": set(shared) == {x, complement(x)},
        "token_class_has_four_outcomes_on_mixed_section": len(token_class) == 4,
        "shared_first_projection_natural": shared_marginal_0 == expected_marginal,
        "shared_second_projection_natural": shared_marginal_1 == expected_second_marginal,
        "componentwise_iid_first_marginal": componentwise_iid_marginal_0 == expected_marginal,
        "componentwise_iid_second_marginal": componentwise_iid_marginal_1 == expected_second_marginal,
        "token_class_first_projection_natural": token_class_marginal_0 == expected_marginal,
        "token_class_second_projection_natural": token_class_marginal_1 == expected_second_marginal,
        "shared_and_token_class_have_same_one_component_marginals": shared_marginal_0 == token_class_marginal_0 and shared_marginal_1 == token_class_marginal_1,
        "shared_complement_equivariant": push_complement(shared) == shared_from_complement,
        "componentwise_iid_complement_equivariant": push_complement(componentwise_iid) == componentwise_iid_from_complement,
        "token_class_complement_equivariant": push_complement(token_class) == token_class_from_complement,
        "shared_handles_connected_to_disconnected_restriction": push_restriction(shared_kernel(connected_state, p), split_map) == shared_kernel(restrict_state(connected_state, split_map), p),
        "componentwise_iid_fails_connected_to_disconnected_restriction": push_restriction(componentwise_iid_kernel(connected_state, p), split_map) != componentwise_iid_kernel(restrict_state(connected_state, split_map), p),
        "token_class_handles_connected_to_disconnected_restriction": push_restriction(token_class_kernel(connected_state, p), split_map) == token_class_kernel(restrict_state(connected_state, split_map), p),
        "token_class_handles_mixed_restriction_with_duplication": push_restriction(token_class_kernel(x, p), mixed_map) == token_class_kernel(restrict_state(x, mixed_map), p),
        "paired_p_roots_distinct": one_bit_kernel(0, p) != one_bit_kernel(0, q),
        "paired_p_roots_same_uniform_stationary_law": apply_one_bit(uniform, p) == uniform and apply_one_bit(uniform, q) == uniform,
        "kernel_does_not_select_initial_token": apply_one_bit(delta0, p) != apply_one_bit(delta1, p),
        "nonempty_orbit_tv_identity": tv(one_bit_kernel(0, p), one_bit_kernel(0, q)) == abs(p - q),
        "empty_open_tv_degenerates": tv({0: Fraction(1)}, {0: Fraction(1)}) == 0,
        "one_step_generator_identity": all(
            (1 if target == bit else 0)
            + ((1 - p) * ((1 if target == 1 - bit else 0) - (1 if target == bit else 0)))
            == one_bit_kernel(bit, p)[target]
            for bit in (0, 1)
            for target in (0, 1)
        ),
        "positive_clock_rescaling_changes_only_declared_rate": (1 - p) / 2 != 1 - p and (1 - p) / 2 > 0,
    }
    payload_basis = {
        "p": str(p),
        "q": str(q),
        "shared_joint": {str(k): str(v) for k, v in sorted(shared.items())},
        "componentwise_iid_joint": {str(k): str(v) for k, v in sorted(componentwise_iid.items())},
        "token_class_joint": {str(k): str(v) for k, v in sorted(token_class.items())},
        "uniform_stationary": {str(k): str(v) for k, v in uniform.items()},
    }
    payload_sha256 = hashlib.sha256(
        json.dumps(payload_basis, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "schema_id": "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_exact_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "authority": "finite_proposal_only_audit_control_evidence",
        "check_count": len(checks),
        "pass_count": sum(bool(value) for value in checks.values()),
        "checks": checks,
        "payload": payload_basis,
        "payload_sha256": payload_sha256,
        "claim_limits": {
            "written_source_purity_verdict": False,
            "independent_source_provenance": False,
            "physical_probability": False,
            "realized_occurrence": False,
            "physical_clock": False,
            "p4_sufficiency": False,
            "adoption": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["status"])
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
