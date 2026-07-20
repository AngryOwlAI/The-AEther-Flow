#!/usr/bin/env python3
"""Deterministic controls for the proposal-only flow-generated orbit law."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path


REPORT_PATH = Path(__file__).with_name(
    "eqsrc_flow_generated_graded_orbit_root_law_candidate_validation.json"
)

Transformation = tuple[int, ...]


def reachability(n: int, generators: tuple[Transformation, ...]) -> list[list[bool]]:
    reach = [[False] * n for _ in range(n)]
    for start in range(n):
        queue: deque[int] = deque([start])
        reach[start][start] = True
        while queue:
            current = queue.popleft()
            for generator in generators:
                nxt = generator[current]
                if not reach[start][nxt]:
                    reach[start][nxt] = True
                    queue.append(nxt)
    return reach


def weakly_connected(reach: list[list[bool]]) -> bool:
    n = len(reach)
    seen = {0}
    queue: deque[int] = deque([0])
    while queue:
        current = queue.popleft()
        for other in range(n):
            if other not in seen and (reach[current][other] or reach[other][current]):
                seen.add(other)
                queue.append(other)
    return len(seen) == n


def cover_edges(reach: list[list[bool]]) -> set[tuple[int, int]]:
    n = len(reach)
    covers: set[tuple[int, int]] = set()
    for lower in range(n):
        for upper in range(n):
            if lower == upper or not reach[lower][upper]:
                continue
            if not any(
                middle not in {lower, upper}
                and reach[lower][middle]
                and reach[middle][upper]
                for middle in range(n)
            ):
                covers.add((lower, upper))
    return covers


def classify_finite_action(
    n: int,
    generators: tuple[Transformation, ...],
    *,
    provenance: str = "source_intrinsic",
    observer_truncated: bool = False,
) -> tuple[bool, str, dict[str, object]]:
    forbidden = {
        "target",
        "benchmark",
        "validator",
        "registry",
        "role",
        "handoff",
        "file_order",
        "task_process",
    }
    if provenance in forbidden:
        return False, "target_or_process_import", {}
    if observer_truncated:
        return False, "observer_truncation_minimum", {}
    if provenance != "source_intrinsic":
        return False, "missing_ordered_action", {}
    if n <= 0 or any(len(generator) != n for generator in generators):
        return False, "missing_ordered_action", {}
    if any(any(value < 0 or value >= n for value in generator) for generator in generators):
        return False, "missing_ordered_action", {}

    reach = reachability(n, generators)
    if not weakly_connected(reach):
        return False, "not_full_action_component", {}
    if any(
        left != right and reach[left][right] and reach[right][left]
        for left in range(n)
        for right in range(n)
    ):
        return False, "periodic_or_nonantisymmetric_reachability", {}

    minima = [
        point
        for point in range(n)
        if not any(other != point and reach[other][point] for other in range(n))
    ]
    if not minima:
        return False, "no_global_minimum", {}
    if len(minima) != 1:
        return False, "nonunique_global_minimum", {"minima": minima}
    root = minima[0]
    if not all(reach[root][point] for point in range(n)):
        return False, "no_global_minimum", {}

    covers = cover_edges(reach)
    predecessor_count = {
        point: sum(other != point and reach[other][point] for other in range(n))
        for point in range(n)
    }
    lengths: dict[int, set[int]] = {point: set() for point in range(n)}
    lengths[root] = {0}
    for point in sorted(range(n), key=predecessor_count.get):
        if point == root:
            continue
        parents = [lower for lower, upper in covers if upper == point]
        for parent in parents:
            lengths[point].update(length + 1 for length in lengths[parent])
        if not lengths[point] or len(lengths[point]) != 1:
            return False, "non_graded_or_infinite_rank", {
                "root": root,
                "cover_edges": sorted(covers),
                "rank_length_sets": {
                    str(key): sorted(value) for key, value in lengths.items()
                },
            }

    ranks = {point: next(iter(values)) for point, values in lengths.items()}
    even = sorted(point for point, rank in ranks.items() if rank % 2 == 0)
    odd = sorted(point for point, rank in ranks.items() if rank % 2 == 1)
    if not even or not odd:
        return False, "empty_parity_block", {"ranks": ranks}
    return True, "admitted", {
        "root": root,
        "cover_edges": sorted(covers),
        "ranks": ranks,
        "partition": {"even": even, "odd": odd},
    }


def relation_pairs() -> set[tuple[tuple[int, int], tuple[int, int]]]:
    states = list(itertools.product((0, 1), repeat=2))
    boundary = {(0, 0), (0, 1)}
    return {
        (left, right)
        for left in states
        for right in states
        if (left[0] ^ right[0], left[1] ^ right[1]) in boundary
    }


def conjugate(generator: Transformation, permutation: Transformation) -> Transformation:
    inverse = [0] * len(permutation)
    for old, new in enumerate(permutation):
        inverse[new] = old
    return tuple(permutation[generator[inverse[new]]] for new in range(len(permutation)))


def enumerate_unary_actions(n: int) -> dict[str, object]:
    counts: Counter[str] = Counter()
    for generator in itertools.product(range(n), repeat=n):
        _, tag, _ = classify_finite_action(n, (generator,))
        counts[tag] += 1
    return {
        "total_actions": n**n,
        "classification_counts": dict(sorted(counts.items())),
    }


def run_checks() -> dict[str, object]:
    chain = (1, 2, 3, 3)
    chain_ok, chain_tag, chain_data = classify_finite_action(4, (chain,))
    assert chain_ok and chain_tag == "admitted"
    assert chain_data["root"] == 0
    assert chain_data["cover_edges"] == [(0, 1), (1, 2), (2, 3)]
    assert chain_data["ranks"] == {0: 0, 1: 1, 2: 2, 3: 3}
    assert chain_data["partition"] == {"even": [0, 2], "odd": [1, 3]}

    periodic = (1, 2, 3, 0)
    assert classify_finite_action(4, (periodic,))[1] == (
        "periodic_or_nonantisymmetric_reachability"
    )

    multi_min_u = (2, 1, 2)
    multi_min_v = (0, 2, 2)
    multi_ok, multi_tag, multi_data = classify_finite_action(
        3, (multi_min_u, multi_min_v)
    )
    assert not multi_ok and multi_tag == "nonunique_global_minimum"
    assert multi_data["minima"] == [0, 1]

    non_graded_generators = (
        (1, 1, 2, 3, 4),
        (0, 4, 2, 3, 4),
        (2, 1, 2, 3, 4),
        (0, 1, 3, 3, 4),
        (0, 1, 2, 4, 4),
    )
    nongraded_ok, nongraded_tag, nongraded_data = classify_finite_action(
        5, non_graded_generators
    )
    assert not nongraded_ok and nongraded_tag == "non_graded_or_infinite_rank"
    assert nongraded_data["rank_length_sets"]["4"] == [2, 3]

    assert classify_finite_action(4, (chain,), observer_truncated=True)[1] == (
        "observer_truncation_minimum"
    )
    assert classify_finite_action(4, (chain,), provenance="target")[1] == (
        "target_or_process_import"
    )

    relabel = (2, 0, 3, 1)
    relabeled_chain = conjugate(chain, relabel)
    relabeled_ok, _, relabeled_data = classify_finite_action(4, (relabeled_chain,))
    assert relabeled_ok
    assert {
        relabel[point]: rank for point, rank in chain_data["ranks"].items()
    } == relabeled_data["ranks"]

    square_x = (1, 1, 3, 3)
    square_y = (2, 3, 2, 3)
    square_ok, _, square_data = classify_finite_action(4, (square_x, square_y))
    assert square_ok and square_data["partition"] == {
        "even": [0, 3],
        "odd": [1, 2],
    }
    swap_coordinates = (0, 2, 1, 3)
    assert conjugate(square_x, swap_coordinates) == square_y
    assert conjugate(square_y, swap_coordinates) == square_x

    reverse_top = (0, 1, 2, 0)
    assert classify_finite_action(4, (chain, reverse_top))[1] == (
        "periodic_or_nonantisymmetric_reachability"
    )

    dense_midpoints = []
    left, right = Fraction(0), Fraction(1)
    for _ in range(8):
        midpoint = (left + right) / 2
        assert left < midpoint < right
        dense_midpoints.append(str(midpoint))
        right = midpoint
    assert len(set(dense_midpoints)) == 8

    pairs = relation_pairs()
    assert len(pairs) == 8
    classes = {
        state: frozenset(right for left, right in pairs if left == state)
        for state in itertools.product((0, 1), repeat=2)
    }
    assert len(set(classes.values())) == 2
    assert all(len(block) == 2 for block in set(classes.values()))

    return {
        "schema_version": "eqsrc-flow-generated-graded-orbit-root-validation.v1",
        "candidate": "EqSrcFlowGeneratedGradedOrbitRootLaw_src^cand,v1",
        "status": "PASS",
        "authority": "finite and symbolic mathematical control only; not ontology or physics authority",
        "positive_control": {
            "name": "four_event_discrete_action_chain",
            **chain_data,
            "relation_pair_count": len(pairs),
            "relation_class_count": 2,
        },
        "finite_countermodels": {
            "periodic_cycle": "periodic_or_nonantisymmetric_reachability",
            "multiple_minima": multi_data,
            "non_graded": nongraded_data,
            "observer_truncation": "observer_truncation_minimum",
            "target_import": "target_or_process_import",
        },
        "infinite_countermodels": {
            "bi_infinite_shift": "rootless: every integer has a predecessor",
            "dense_nonnegative_rational_translation": {
                "result": "non_locally_finite_or_no_cover_graph",
                "strict_midpoint_controls": dense_midpoints,
            },
        },
        "naturality_controls": {
            "conjugate_state_relabeling": "PASS",
            "ordered_monoid_generator_swap_on_boolean_square": "PASS",
            "rank_transport": relabeled_data["ranks"],
        },
        "finite_variation_controls": {
            "action_isomorphic_relabeling": "PASS",
            "cycle_introducing_generator": "FAIL_CLOSED",
        },
        "unary_action_census": {
            f"n{n}": enumerate_unary_actions(n) for n in range(1, 5)
        },
        "claim_boundary": {
            "current_ontology_derives_candidate": False,
            "physical_admissibility_established": False,
            "general_EqSrc_discharged": False,
            "distance_to_gr_ledger_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    result = run_checks()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
    if args.json or not args.write_report:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
