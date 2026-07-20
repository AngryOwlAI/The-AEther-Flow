#!/usr/bin/env python3
"""Deterministic finite controls for the proposal-only rooted partition law."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import deque
from pathlib import Path


REPORT_PATH = Path(__file__).with_name(
    "eqsrc_ordered_motion_rooted_partition_law_candidate_validation.json"
)


def directed_edges(n: int) -> list[tuple[int, int]]:
    return [(u, v) for u in range(n) for v in range(n) if u != v]


def edge_set(n: int, mask: int) -> frozenset[tuple[int, int]]:
    edges = directed_edges(n)
    return frozenset(edge for bit, edge in enumerate(edges) if mask & (1 << bit))


def classify_record(
    n: int,
    edges: frozenset[tuple[int, int]],
    root: int | None,
    provenance: str = "source_intrinsic",
) -> tuple[bool, str, dict[int, int]]:
    if provenance in {"target", "benchmark", "validator", "registry", "role", "handoff", "file_order"}:
        return False, "target_or_process_import", {}
    if provenance == "sampling_start":
        return False, "observer_truncation_root", {}
    if provenance != "source_intrinsic":
        return False, "missing_transition_provenance", {}
    if root is None or root < 0 or root >= n:
        return False, "nonunique_or_nonnatural_root", {}

    outgoing: dict[int, list[int]] = {u: [] for u in range(n)}
    for u, v in edges:
        outgoing[u].append(v)

    parity = {root: 0}
    queue: deque[int] = deque([root])
    while queue:
        u = queue.popleft()
        for v in outgoing[u]:
            expected = 1 - parity[u]
            if v in parity and parity[v] != expected:
                return False, "mixed_path_parity_or_odd_cycle", {}
            if v not in parity:
                parity[v] = expected
                queue.append(v)

    if len(parity) != n:
        return False, "disconnected_or_unreachable_component", {}
    values = set(parity.values())
    if values != {0, 1}:
        return False, "empty_parity_block", {}
    return True, "admitted", parity


def is_automorphism(n: int, edges: frozenset[tuple[int, int]], perm: tuple[int, ...]) -> bool:
    transported = frozenset((perm[u], perm[v]) for u, v in edges)
    return transported == edges


def natural_singleton_roots(n: int, edges: frozenset[tuple[int, int]]) -> list[int]:
    automorphisms = [
        perm
        for perm in itertools.permutations(range(n))
        if is_automorphism(n, edges, perm)
    ]
    return [root for root in range(n) if all(perm[root] == root for perm in automorphisms)]


def relation_pairs() -> set[tuple[tuple[int, int], tuple[int, int]]]:
    states = list(itertools.product((0, 1), repeat=2))
    boundary = {(0, 0), (0, 1)}
    return {
        (a, b)
        for a in states
        for b in states
        if (a[0] ^ b[0], a[1] ^ b[1]) in boundary
    }


def enumerate_graphs(n: int) -> dict[str, int]:
    total = 0
    admitted = 0
    failure_counts: dict[str, int] = {}
    edges_count = n * (n - 1)
    for mask in range(1 << edges_count):
        edges = edge_set(n, mask)
        for root in range(n):
            total += 1
            ok, tag, _ = classify_record(n, edges, root)
            if ok:
                admitted += 1
            else:
                failure_counts[tag] = failure_counts.get(tag, 0) + 1
    result = {"total_rooted_graphs": total, "admitted": admitted}
    result.update({f"failed_{key}": value for key, value in sorted(failure_counts.items())})
    return result


def run_checks() -> dict[str, object]:
    positive_edges = frozenset({(0, 1)})
    positive_ok, positive_tag, positive_parity = classify_record(2, positive_edges, 0)
    assert positive_ok and positive_tag == "admitted"
    assert positive_parity == {0: 0, 1: 1}

    two_cycle = frozenset({(0, 1), (1, 0)})
    assert natural_singleton_roots(2, two_cycle) == []

    mixed_parity = frozenset({(0, 1), (1, 2), (0, 2)})
    assert classify_record(3, mixed_parity, 0)[1] == "mixed_path_parity_or_odd_cycle"

    disconnected = frozenset({(0, 1)})
    assert classify_record(3, disconnected, 0)[1] == "disconnected_or_unreachable_component"
    assert classify_record(2, positive_edges, 0, "sampling_start")[1] == "observer_truncation_root"
    assert classify_record(2, positive_edges, 0, "target")[1] == "target_or_process_import"

    pairs = relation_pairs()
    assert len(pairs) == 8
    classes = {
        state: frozenset(other for left, other in pairs if left == state)
        for state in itertools.product((0, 1), repeat=2)
    }
    assert len(set(classes.values())) == 2
    assert all(len(block) == 2 for block in set(classes.values()))

    automorphism_checks = 0
    for mask in range(1 << 6):
        edges = edge_set(3, mask)
        for root in range(3):
            ok, _, parity = classify_record(3, edges, root)
            if not ok:
                continue
            for perm in itertools.permutations(range(3)):
                if is_automorphism(3, edges, perm) and perm[root] == root:
                    automorphism_checks += 1
                    assert all(parity[perm[x]] == parity[x] for x in range(3))

    order_parameters = [-3.0, 0.0, 2.0]
    transformed = [7.0 * value + 11.0 for value in order_parameters]
    assert all(
        (order_parameters[i] < order_parameters[j])
        == (transformed[i] < transformed[j])
        for i in range(len(order_parameters))
        for j in range(len(order_parameters))
    )

    variation_pass = classify_record(2, frozenset({(1, 0)}), 1)
    variation_fail = classify_record(2, frozenset({(1, 0)}), 0)
    assert variation_pass[0]
    assert not variation_fail[0]

    return {
        "schema_version": "eqsrc-ordered-motion-rooted-partition-validation.v1",
        "candidate": "EqSrcOrderedMotionRootedPartitionLaw_src^cand,v1",
        "status": "PASS",
        "authority": "finite mathematical control only; not ontology or physics authority",
        "positive_control": {
            "name": "certified_rooted_two_event_path",
            "parity": {str(key): value for key, value in positive_parity.items()},
            "partition": {"even": [0], "odd": [1]},
            "relation_pair_count": len(pairs),
            "relation_class_count": 2,
        },
        "negative_controls": {
            "unrooted_two_cycle_natural_singleton_roots": 0,
            "mixed_path_parity": "rejected",
            "disconnected_component": "rejected",
            "sampling_root": "rejected",
            "target_import": "rejected",
        },
        "small_graph_census": {
            "n2": enumerate_graphs(2),
            "n3": enumerate_graphs(3),
            "n4": enumerate_graphs(4),
        },
        "root_preserving_automorphism_checks_n3": automorphism_checks,
        "strictly_increasing_reparameterization_check": "PASS",
        "finite_variation_controls": {
            "root_preserving_reversal": "PASS",
            "root_not_preserved": "FAIL_CLOSED",
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
