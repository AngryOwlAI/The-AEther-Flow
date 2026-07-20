#!/usr/bin/env python3
"""Finite checks for the RT-20260720-009 P1-T01 smuggling audit.

This validates only the stated finite combinatorics and exact candidate
identity. It provides no ontology, physical-admissibility, or promotion
authority.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CANDIDATE = ROOT / (
    "research_control/tasks/RT-20260718-047/artifacts/"
    "eqsrc_flow_generated_graded_orbit_root_law_candidate_v1.tex"
)
AUDIT = ROOT / (
    "research_control/tasks/RT-20260720-009/artifacts/"
    "eqsrc_flow_generated_graded_orbit_root_smuggling_audit.tex"
)
REPORT = ROOT / (
    "research_control/tasks/RT-20260720-009/artifacts/"
    "eqsrc_flow_generated_graded_orbit_root_smuggling_audit_validation.json"
)
EXPECTED_CANDIDATE_SHA256 = (
    "b712552d328f144491bff689b702eba6dc2027ce1cc61c7052adbca84b0639f7"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def action_maps(n: int, p_block: set[int], q_block: set[int]) -> list[tuple[int, ...]]:
    root = min(p_block)
    bridge = min(q_block)
    maps: list[tuple[int, ...]] = []
    for q in sorted(q_block):
        transform = list(range(n))
        transform[root] = q
        maps.append(tuple(transform))
    for p in sorted(p_block - {root}):
        transform = list(range(n))
        transform[bridge] = p
        maps.append(tuple(transform))
    return maps


def closure(maps: list[tuple[int, ...]]) -> set[tuple[int, int]]:
    n = len(maps[0])
    reachable = {(x, x) for x in range(n)}
    reachable.update((x, transform[x]) for transform in maps for x in range(n))
    changed = True
    while changed:
        changed = False
        for left, middle in tuple(reachable):
            for middle2, right in tuple(reachable):
                if middle == middle2 and (left, right) not in reachable:
                    reachable.add((left, right))
                    changed = True
    return reachable


def covers(reachable: set[tuple[int, int]], n: int) -> set[tuple[int, int]]:
    strict = {(a, b) for a, b in reachable if a != b}
    return {
        (a, b)
        for a, b in strict
        if not any((a, c) in strict and (c, b) in strict for c in range(n))
    }


def ranks_from_root(root: int, cover_edges: set[tuple[int, int]], n: int) -> dict[int, int]:
    ranks = {root: 0}
    for _ in range(n):
        for left, right in cover_edges:
            if left in ranks:
                proposed = ranks[left] + 1
                if right in ranks and ranks[right] != proposed:
                    raise AssertionError("non-graded realization")
                ranks[right] = proposed
    if len(ranks) != n:
        raise AssertionError("unreachable realization vertex")
    return ranks


def permute_subset(subset: frozenset[int], permutation: tuple[int, ...]) -> frozenset[int]:
    return frozenset(permutation[index] for index in subset)


def build_report() -> dict[str, object]:
    candidate_hash = sha256(CANDIDATE)
    if candidate_hash != EXPECTED_CANDIDATE_SHA256:
        raise AssertionError("candidate hash mismatch")

    partition_counts: dict[str, int] = {}
    parameterization_counts: dict[str, int] = {}
    for n in range(2, 7):
        partitions = 0
        parameterizations = 0
        carrier = set(range(n))
        for size in range(1, n):
            for q_tuple in itertools.combinations(range(n), size):
                q_block = set(q_tuple)
                p_block = carrier - q_block
                root = min(p_block)
                reachable = closure(action_maps(n, p_block, q_block))
                if any(a != b and (b, a) in reachable for a, b in reachable):
                    raise AssertionError("realization is not antisymmetric")
                if not all((root, x) in reachable for x in carrier):
                    raise AssertionError("root is not global")
                rank = ranks_from_root(root, covers(reachable, n), n)
                even = {x for x, value in rank.items() if value % 2 == 0}
                odd = carrier - even
                if even != p_block or odd != q_block:
                    raise AssertionError("ordered partition realization mismatch")
                partitions += 1
                parameterizations += len(p_block) * len(q_block)
        if partitions != (1 << n) - 2:
            raise AssertionError("partition census mismatch")
        expected_parameters = n * (n - 1) * (1 << (n - 2))
        if parameterizations != expected_parameters:
            raise AssertionError("root-bridge parameterization mismatch")
        partition_counts[f"n{n}"] = partitions
        parameterization_counts[f"n{n}"] = parameterizations

    carrier = frozenset(range(4))
    permutation_cases = 0
    stabilizers = 0
    changers = 0
    transfer_cases = 0
    transfer_changes = 0
    for size in range(1, 4):
        for q_tuple in itertools.combinations(range(4), size):
            q_block = frozenset(q_tuple)
            p_block = carrier - q_block
            for permutation in itertools.permutations(range(4)):
                permutation_cases += 1
                if permute_subset(q_block, permutation) == q_block:
                    stabilizers += 1
                else:
                    changers += 1
            if len(q_block) > 1:
                for vertex in q_block:
                    transfer_cases += 1
                    transfer_changes += int(q_block - {vertex} != q_block)
            if len(p_block) > 1:
                for vertex in p_block:
                    transfer_cases += 1
                    transfer_changes += int(q_block | {vertex} != q_block)

    if (permutation_cases, stabilizers, changers) != (336, 72, 264):
        raise AssertionError("four-token permutation census mismatch")
    if (transfer_cases, transfer_changes) != (48, 48):
        raise AssertionError("single-token transfer census mismatch")

    full_component = tuple(range(-1, 4))
    full_action = {i: min(i + 1, 3) for i in full_component}
    window = tuple(range(4))
    restricted_action = {i: full_action[i] for i in window}
    positive_action = {i: min(i + 1, 3) for i in window}
    if restricted_action != positive_action or full_action[-1] != 0:
        raise AssertionError("forward-invariant truncation witness mismatch")

    audit_text = AUDIT.read_text(encoding="utf-8")
    required_phrases = [
        "Universal ordered-bipartition action realization",
        "category-by-preservation",
        "not physical covariance",
        "blocked\\_adoption\\_open\\_continuation",
        "no explicit target-GR import",
        "General EqSrc remains",
        "P1-T02",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in audit_text]
    if missing:
        raise AssertionError(f"audit artifact missing required phrases: {missing}")

    return {
        "schema_id": "eqsrc_flow_generated_graded_orbit_root_smuggling_audit_validation_v1",
        "status": "PASS",
        "candidate_sha256": candidate_hash,
        "ordered_partition_counts": partition_counts,
        "root_bridge_parameterization_counts": parameterization_counts,
        "four_token_audit": {
            "ordered_nontrivial_partitions": 14,
            "permutation_cases": permutation_cases,
            "relation_stabilizers": stabilizers,
            "relation_changers": changers,
            "single_token_transfer_cases": transfer_cases,
            "single_token_relation_changes": transfer_changes,
        },
        "truncation_pair": {
            "full_component": list(full_component),
            "window": list(window),
            "restricted_action_matches_positive_witness": True,
            "window_has_external_predecessor": True,
        },
        "interpretation": {
            "action_realization": "Every nontrivial ordered finite partition is realizable when the action is freely supplied.",
            "completeness": "The isolated record does not certify absence of an ambient predecessor.",
            "authority": "Finite PASS is draft/control audit evidence only.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
