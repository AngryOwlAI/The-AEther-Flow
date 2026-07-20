#!/usr/bin/env python3
"""Exact finite controls for the rooted-partition-law Refuter stress."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-045"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
REPORT_PATH = (
    ARTIFACT_ROOT
    / "eqsrc_ordered_motion_rooted_partition_law_refuter_stress_validation.json"
)
CANDIDATE_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260718-043/artifacts/"
    "eqsrc_ordered_motion_rooted_partition_law_candidate_v1.tex"
)
AUDIT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260718-044/artifacts/"
    "eqsrc_ordered_motion_rooted_partition_law_smuggling_audit.tex"
)
COUNTERMODEL_PATH = (
    ARTIFACT_ROOT
    / "eqsrc_ordered_motion_rooted_partition_law_refuter_countermodel.yaml"
)
FUSED_PATH = (
    ARTIFACT_ROOT / "eqsrc_ordered_motion_rooted_partition_law_refuter_stress.tex"
)

CANDIDATE_SHA256 = (
    "24992d4b41d64bba860f5cd61d505d6b1ecaad3917e9195e0cbd3d897d955aef"
)
AUDIT_SHA256 = (
    "36d4f057ad811ce30795a1d8f1a83093b981f7b40221423f291ca81d611deef0"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parity_partition(
    mask: int, root: int, vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...]
) -> int | None:
    adjacency: list[list[int]] = [[] for _ in vertices]
    for edge_index, (source, target) in enumerate(edges):
        if mask & (1 << edge_index):
            adjacency[source].append(target)

    parity: list[int | None] = [None] * len(vertices)
    parity[root] = 0
    queue: deque[int] = deque([root])
    while queue:
        source = queue.popleft()
        assert parity[source] is not None
        for target in adjacency[source]:
            expected = parity[source] ^ 1
            if parity[target] is None:
                parity[target] = expected
                queue.append(target)
            elif parity[target] != expected:
                return None

    if any(value is None for value in parity):
        return None
    if len(set(parity)) != 2:
        return None
    return sum((value == 1) << index for index, value in enumerate(parity))


def permute_mask(mask: int, permutation: tuple[int, ...], n: int) -> int:
    result = 0
    for index in range(n):
        if mask & (1 << index):
            result |= 1 << permutation[index]
    return result


def run_controls() -> dict[str, object]:
    require(sha256(CANDIDATE_PATH) == CANDIDATE_SHA256, "candidate hash drift")
    require(sha256(AUDIT_PATH) == AUDIT_SHA256, "audit hash drift")

    candidate_text = CANDIDATE_PATH.read_text(encoding="utf-8")
    audit_text = AUDIT_PATH.read_text(encoding="utf-8")
    countermodel_text = COUNTERMODEL_PATH.read_text(encoding="utf-8")
    fused_text = FUSED_PATH.read_text(encoding="utf-8")
    for marker in (
        "proposal-only",
        "blocked_adoption_open_continuation",
        "current_ontology_derives_finite_record_law: false",
        "physical_covariance_established: false",
    ):
        require(marker in candidate_text, f"candidate marker missing: {marker}")
    for marker in (
        "Universal ordered-partition realization",
        "264",
        "48",
        "physical covariance",
    ):
        require(marker in audit_text, f"audit marker missing: {marker}")
    for marker in (
        "CM-EQSRC-ORDERED-MOTION-ROOTED-PARTITION-001",
        "minimal_two_token_directed_cycle",
        "four_token_directed_cycle_strengthening",
        "global_no_go_claim_authorized: false",
    ):
        require(marker in countermodel_text, f"countermodel marker missing: {marker}")
    for marker in (
        r"scoped\_obstruction",
        "1088",
        "557",
        "265",
        "182",
        "locally frozen",
    ):
        require(marker in fused_text, f"fused artifact marker missing: {marker}")

    vertices = tuple(range(4))
    edges = tuple((source, target) for source in vertices for target in vertices if source != target)
    by_partition: Counter[int] = Counter()
    root_count_distribution: Counter[int] = Counter()
    relation_count_distribution: Counter[int] = Counter()
    edge_count_distribution: Counter[int] = Counter()
    admitted_graph_count = 0
    multi_relation_graph_count = 0

    for mask in range(1 << len(edges)):
        rooted_partitions: list[int] = []
        for root in vertices:
            partition = parity_partition(mask, root, vertices, edges)
            if partition is not None:
                rooted_partitions.append(partition)
                by_partition[partition] += 1
        if not rooted_partitions:
            continue
        admitted_graph_count += 1
        root_count_distribution[len(rooted_partitions)] += 1
        distinct_relations = len(set(rooted_partitions))
        relation_count_distribution[distinct_relations] += 1
        edge_count_distribution[mask.bit_count()] += 1
        if distinct_relations > 1:
            multi_relation_graph_count += 1

    rooted_record_count = sum(by_partition.values())
    odd_block_size_counts = Counter()
    per_partition_counts = {}
    for partition, count in by_partition.items():
        odd_block_size_counts[partition.bit_count()] += count
        per_partition_counts.setdefault(partition.bit_count(), set()).add(count)

    require(len(edges) == 12, "unexpected four-token edge count")
    require(rooted_record_count == 1088, "unexpected admitted rooted-record count")
    require(admitted_graph_count == 557, "unexpected admitted graph count")
    require(multi_relation_graph_count == 265, "unexpected multi-relation graph count")
    require(root_count_distribution == Counter({1: 292, 2: 108, 3: 48, 4: 109}), "root distribution drift")
    require(relation_count_distribution == Counter({1: 292, 2: 265}), "relation distribution drift")
    require(edge_count_distribution == Counter({3: 64, 4: 186, 5: 192, 6: 88, 7: 24, 8: 3}), "edge distribution drift")
    require(odd_block_size_counts == Counter({1: 96, 2: 960, 3: 32}), "odd-block count drift")
    require(per_partition_counts == {1: {24}, 2: {160}, 3: {8}}, "per-partition count drift")

    partitions = tuple(range(1, (1 << 4) - 1))
    hamming_distance_counts = Counter(
        (left ^ right).bit_count()
        for left in partitions
        for right in partitions
        if left != right
    )
    require(hamming_distance_counts == Counter({1: 48, 2: 72, 3: 48, 4: 14}), "variation orbit drift")

    permutations = tuple(itertools.permutations(vertices))
    stabilizers = 0
    changers = 0
    for partition in partitions:
        for permutation in permutations:
            if permute_mask(partition, permutation, 4) == partition:
                stabilizers += 1
            else:
                changers += 1
    require((stabilizers, changers) == (72, 264), "permutation census drift")

    cycle_edges = {(0, 1), (1, 2), (2, 3), (3, 0)}
    cycle_mask = sum(1 << index for index, edge in enumerate(edges) if edge in cycle_edges)
    cycle_roots = {
        root: parity_partition(cycle_mask, root, vertices, edges) for root in vertices
    }
    require(cycle_roots == {0: 10, 1: 5, 2: 10, 3: 5}, "cycle root relations drift")
    cycle_automorphisms = tuple(
        permutation
        for permutation in permutations
        if {(permutation[source], permutation[target]) for source, target in cycle_edges}
        == cycle_edges
    )
    require(len(cycle_automorphisms) == 4, "cycle automorphism group drift")
    require({permutation[0] for permutation in cycle_automorphisms} == set(vertices), "cycle root orbit drift")
    cycle_relation_stabilizer = sum(
        permute_mask(cycle_roots[0], permutation, 4) == cycle_roots[0]
        for permutation in cycle_automorphisms
    )
    require(cycle_relation_stabilizer == 2, "cycle relation stabilizer drift")

    return {
        "schema_id": "eqsrc_ordered_motion_rooted_partition_law_refuter_stress_validation_v1",
        "status": "PASS",
        "candidate_sha256": CANDIDATE_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "four_token_census": {
            "loop_free_directed_graphs": 4096,
            "graph_root_configurations": 16384,
            "admitted_rooted_records": rooted_record_count,
            "admitted_transition_graphs": admitted_graph_count,
            "graphs_with_one_relation": relation_count_distribution[1],
            "graphs_with_two_root_induced_relations": multi_relation_graph_count,
            "root_count_distribution": dict(sorted(root_count_distribution.items())),
            "edge_count_distribution": dict(sorted(edge_count_distribution.items())),
            "rooted_records_by_odd_block_size": dict(sorted(odd_block_size_counts.items())),
            "rooted_records_per_partition_by_odd_block_size": {
                size: next(iter(counts)) for size, counts in sorted(per_partition_counts.items())
            },
        },
        "directed_four_cycle": {
            "automorphism_group_order": len(cycle_automorphisms),
            "root_orbit_size": len({permutation[0] for permutation in cycle_automorphisms}),
            "admissible_root_count": len(cycle_roots),
            "distinct_relation_count": len(set(cycle_roots.values())),
            "relation_stabilizer_order": cycle_relation_stabilizer,
            "root_to_odd_block_mask": cycle_roots,
        },
        "relation_variation_orbit": {
            "nontrivial_partitions": len(partitions),
            "ordered_distinct_relation_changes": sum(hamming_distance_counts.values()),
            "hamming_distance_counts": dict(sorted(hamming_distance_counts.items())),
            "permutation_cases": stabilizers + changers,
            "permutation_stabilizers": stabilizers,
            "permutation_changers": changers,
        },
        "classification": {
            "refuter_result": "scoped_obstruction",
            "conditional_algebraic_core_survives": True,
            "current_ontology_derives_unique_relation": False,
            "minimal_countermodel_available": True,
            "candidate_cycle_freeze": "locally_frozen",
            "global_no_go_claim_authorized": False,
            "future_source_extension_impossibility_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = run_controls()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
    if args.json or not args.write_report:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
