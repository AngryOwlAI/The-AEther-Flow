#!/usr/bin/env python3
"""Finite audit checks for RT-20260718-044.

The script verifies the bounded mathematical claims in the Smuggling Auditor
artifact. It does not validate ontology, physical admissibility, or promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CANDIDATE = ROOT / (
    "research_control/tasks/RT-20260718-043/artifacts/"
    "eqsrc_ordered_motion_rooted_partition_law_candidate_v1.tex"
)
AUDIT = ROOT / (
    "research_control/tasks/RT-20260718-044/artifacts/"
    "eqsrc_ordered_motion_rooted_partition_law_smuggling_audit.tex"
)
REPORT = ROOT / (
    "research_control/tasks/RT-20260718-044/artifacts/"
    "eqsrc_ordered_motion_rooted_partition_law_smuggling_audit_validation.json"
)
EXPECTED_CANDIDATE_SHA256 = (
    "24992d4b41d64bba860f5cd61d505d6b1ecaad3917e9195e0cbd3d897d955aef"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask(vertices: set[int]) -> int:
    return sum(1 << vertex for vertex in vertices)


def canonical_realization(n: int, q_block: set[int]) -> tuple[int, set[tuple[int, int]]]:
    """Return the rooted DAG that realizes P=X\\Q as even and Q as odd."""
    p_block = set(range(n)) - q_block
    root = min(p_block)
    bridge = min(q_block)
    edges = {(root, q) for q in q_block}
    edges.update((bridge, p) for p in p_block if p != root)
    return root, edges


def path_lengths(root: int, target: int, edges: set[tuple[int, int]]) -> list[int]:
    adjacency: dict[int, list[int]] = {}
    for source, destination in edges:
        adjacency.setdefault(source, []).append(destination)

    lengths: list[int] = []

    def visit(vertex: int, seen: set[int], length: int) -> None:
        if vertex == target:
            lengths.append(length)
            return
        for destination in adjacency.get(vertex, []):
            if destination not in seen:
                visit(destination, seen | {destination}, length + 1)

    visit(root, {root}, 0)
    return lengths


def relation_pair_count(n: int, q_block: set[int]) -> int:
    q = mask(q_block)
    p = mask(set(range(n)) - q_block)
    state = {0, p, q, p ^ q}
    boundary = {0, q}
    return sum(1 for left in state for right in state if left ^ right in boundary)


def permute_mask(value: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for source, destination in enumerate(permutation):
        if value & (1 << source):
            result |= 1 << destination
    return result


def build_report() -> dict[str, object]:
    candidate_hash = sha256(CANDIDATE)
    if candidate_hash != EXPECTED_CANDIDATE_SHA256:
        raise AssertionError("candidate hash mismatch")

    realization_census: dict[str, dict[str, int]] = {}
    all_relation_pair_counts: set[int] = set()
    for n in range(2, 6):
        partitions = 0
        realized = 0
        distinct_boundaries: set[int] = set()
        for q_mask in range(1, (1 << n) - 1):
            q_block = {vertex for vertex in range(n) if q_mask & (1 << vertex)}
            p_block = set(range(n)) - q_block
            root, edges = canonical_realization(n, q_block)
            parities: dict[int, int] = {}
            for vertex in range(n):
                lengths = path_lengths(root, vertex, edges)
                if not lengths or len({length % 2 for length in lengths}) != 1:
                    raise AssertionError("canonical realization is not parity-admitted")
                parities[vertex] = lengths[0] % 2
            if {vertex for vertex, parity in parities.items() if parity == 0} != p_block:
                raise AssertionError("even block mismatch")
            if {vertex for vertex, parity in parities.items() if parity == 1} != q_block:
                raise AssertionError("odd block mismatch")
            pair_count = relation_pair_count(n, q_block)
            if pair_count != 8:
                raise AssertionError("unexpected relation pair count")
            all_relation_pair_counts.add(pair_count)
            distinct_boundaries.add(mask(q_block))
            partitions += 1
            realized += 1
        expected = (1 << n) - 2
        if partitions != expected or realized != expected or len(distinct_boundaries) != expected:
            raise AssertionError("universal realization census mismatch")
        realization_census[f"n{n}"] = {
            "ordered_nontrivial_partitions": partitions,
            "canonical_records_realized": realized,
            "distinct_boundary_lines": len(distinct_boundaries),
        }

    n = 4
    permutation_cases = 0
    relation_stabilizers = 0
    relation_changers = 0
    transfer_cases = 0
    transfer_relation_changes = 0
    for q_mask in range(1, (1 << n) - 1):
        q_block = {vertex for vertex in range(n) if q_mask & (1 << vertex)}
        for permutation in itertools.permutations(range(n)):
            permutation_cases += 1
            if permute_mask(q_mask, permutation) == q_mask:
                relation_stabilizers += 1
            else:
                relation_changers += 1
        p_block = set(range(n)) - q_block
        if len(q_block) > 1:
            for vertex in q_block:
                transfer_cases += 1
                changed = q_block - {vertex}
                if mask(changed) != q_mask:
                    transfer_relation_changes += 1
        if len(p_block) > 1:
            for vertex in p_block:
                transfer_cases += 1
                changed = q_block | {vertex}
                if mask(changed) != q_mask:
                    transfer_relation_changes += 1

    if (permutation_cases, relation_stabilizers, relation_changers) != (336, 72, 264):
        raise AssertionError("four-token permutation census mismatch")
    if (transfer_cases, transfer_relation_changes) != (48, 48):
        raise AssertionError("single-token transfer census mismatch")

    swap = (1, 0)
    invariant_singletons = sum(
        1 for vertex in range(2) if permute_mask(1 << vertex, swap) == (1 << vertex)
    )
    if invariant_singletons != 0:
        raise AssertionError("unrooted two-cycle unexpectedly has a natural singleton")

    audit_text = AUDIT.read_text(encoding="utf-8")
    required_phrases = [
        "Universal ordered-partition realization",
        "category-by-preservation",
        "not physical covariance",
        "blocked_adoption_open_continuation",
        "proposal-only",
        "no explicit target-GR import",
        "General EqSrc remains",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in audit_text]
    if missing_phrases:
        raise AssertionError(f"audit artifact missing required phrases: {missing_phrases}")

    return {
        "schema_id": "eqsrc_ordered_motion_rooted_partition_law_smuggling_audit_validation_v1",
        "status": "PASS",
        "candidate_sha256": candidate_hash,
        "universal_realization_census": realization_census,
        "relation_pair_counts": sorted(all_relation_pair_counts),
        "four_token_audit": {
            "ordered_nontrivial_partitions": 14,
            "permutation_cases": permutation_cases,
            "relation_stabilizers": relation_stabilizers,
            "relation_changers": relation_changers,
            "single_token_transfer_cases": transfer_cases,
            "single_token_relation_changes": transfer_relation_changes,
        },
        "unrooted_two_cycle_invariant_singleton_roots": invariant_singletons,
        "interpretation": {
            "universal_realization": "Every nontrivial ordered finite partition can be encoded by one admitted canonical rooted DAG when the transition and root data are freely supplied.",
            "category_scope": "Relation preservation is automatic inside a category already required to preserve the relation-determining source data.",
            "variation_scope": "Every valid one-token partition transfer changes the boundary line and lies outside the candidate-preserving variation class.",
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
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
