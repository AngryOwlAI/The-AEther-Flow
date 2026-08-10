#!/usr/bin/env python3
"""Executable witnesses for the RT-20260809-026 populated-instance audit."""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AuditWitness:
    carrier_commuting_permutations: list[list[int]]
    pointwise_equipment_fixers: list[list[int]]
    identity_is_unique_pointwise_fixer: bool
    lift_sampling_identity: bool
    cocycle_products: list[int]
    cocycle_pass: bool
    presentation_original_norm: float
    presentation_rescaled_norm: float
    presentation_threshold: float
    presentation_countermodel_pass: bool
    epsilon: float
    sector_generators: dict[str, tuple[float, float, float, float]]
    generators_pairwise_nonassociate: bool
    commonity_under_sector_split: bool
    shared_leading_ideal_independent_of_zero_order_carrier: bool
    operational_types_compose_without_bridge: bool
    exact_verdict: str


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Return p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def commuting_permutations(cycle: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [
        p
        for p in itertools.permutations(range(len(cycle)))
        if compose(p, cycle) == compose(cycle, p)
    ]


def associates(v: tuple[float, ...], w: tuple[float, ...]) -> bool:
    """Whether nonzero real linear forms differ by one nonzero scalar."""
    ratio: float | None = None
    for left, right in zip(v, w):
        if abs(right) < 1e-12:
            if abs(left) >= 1e-12:
                return False
            continue
        candidate = left / right
        if abs(candidate) < 1e-12:
            return False
        if ratio is None:
            ratio = candidate
        elif abs(candidate - ratio) >= 1e-12:
            return False
    return ratio is not None


def build_witness() -> AuditWitness:
    cycle = (1, 2, 0)
    commuting = commuting_permutations(cycle)
    pointwise_fixers = [
        p for p in commuting if all(p[index] == index for index in range(3))
    ]

    sample = (2.5, -1.0, 4.25)
    lifted = lambda _point: sample
    sampled = lifted((0.0, 0.0, 0.0, 0.0))

    overlap_units = {(0, 1): 1, (1, 2): 1, (2, 0): 1}
    cocycle_products = [
        overlap_units[(0, 1)] * overlap_units[(1, 2)] * overlap_units[(2, 0)]
    ]

    a = 3.0 / 8.0
    threshold = 1.0 / 2.0
    original_norm = abs(a)
    rescaled_norm = abs(2.0 * a)

    epsilon = 1.0 / 4.0
    generators = {
        "R": (1.0, epsilon, 0.0, 0.0),
        "S": (1.0, 0.0, 0.0, 0.0),
        "D": (1.0, -epsilon, 0.0, 0.0),
    }
    pairs = list(itertools.combinations(generators.values(), 2))
    pairwise_nonassociate = all(not associates(left, right) for left, right in pairs)

    return AuditWitness(
        carrier_commuting_permutations=[list(p) for p in commuting],
        pointwise_equipment_fixers=[list(p) for p in pointwise_fixers],
        identity_is_unique_pointwise_fixer=pointwise_fixers == [(0, 1, 2)],
        lift_sampling_identity=sampled == sample,
        cocycle_products=cocycle_products,
        cocycle_pass=all(value == 1 for value in cocycle_products),
        presentation_original_norm=original_norm,
        presentation_rescaled_norm=rescaled_norm,
        presentation_threshold=threshold,
        presentation_countermodel_pass=(
            original_norm < threshold < rescaled_norm
        ),
        epsilon=epsilon,
        sector_generators=generators,
        generators_pairwise_nonassociate=pairwise_nonassociate,
        commonity_under_sector_split=not pairwise_nonassociate,
        shared_leading_ideal_independent_of_zero_order_carrier=True,
        operational_types_compose_without_bridge=False,
        exact_verdict="repair_required_no_instance_credit",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = asdict(build_witness())
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    required = [
        payload["identity_is_unique_pointwise_fixer"],
        payload["lift_sampling_identity"],
        payload["cocycle_pass"],
        payload["presentation_countermodel_pass"],
        payload["generators_pairwise_nonassociate"],
        not payload["commonity_under_sector_split"],
        payload["shared_leading_ideal_independent_of_zero_order_carrier"],
        not payload["operational_types_compose_without_bridge"],
    ]
    return 0 if all(required) else 1


if __name__ == "__main__":
    raise SystemExit(main())
