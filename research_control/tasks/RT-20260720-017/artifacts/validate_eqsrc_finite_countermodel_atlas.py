#!/usr/bin/env python3
"""Validate the P2-T04 finite countermodel atlas.

PASS is finite operational evidence only. It is not ontology, physical-gauge,
covariance, proof-assistant, Gate Chair, or claim-promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = ROOT / "research_control/tasks/RT-20260720-017/artifacts"
FIXTURES = ART / "eqsrc_finite_countermodel_atlas_fixtures.json"
INSTANCE_MAP = ART / "eqsrc_finite_countermodel_theorem_instance_map.yaml"
ATLAS = ART / "eqsrc_finite_countermodel_atlas_v1.tex"
REPORT = ART / "eqsrc_finite_countermodel_atlas_validation.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def generated_group(size: int, generators: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    identity = tuple(range(size))
    normalized = [tuple(generator) for generator in generators]
    for generator in normalized:
        if sorted(generator) != list(range(size)):
            raise ValueError(f"not a permutation: {generator}")
    group = {identity, *normalized}
    changed = True
    while changed:
        changed = False
        for left in tuple(group):
            for right in tuple(group):
                product = compose(left, right)
                if product not in group:
                    group.add(product)
                    changed = True
    return tuple(sorted(group))


def orbit_decomposition(size: int, group: tuple[tuple[int, ...], ...]) -> list[list[int]]:
    unseen = set(range(size))
    orbits: list[list[int]] = []
    while unseen:
        seed = min(unseen)
        orbit = sorted({permutation[seed] for permutation in group})
        orbits.append(orbit)
        unseen.difference_update(orbit)
    return orbits


def fixed_indices(size: int, group: tuple[tuple[int, ...], ...]) -> list[int]:
    return [
        index
        for index in range(size)
        if all(permutation[index] == index for permutation in group)
    ]


def relation_stabilizer_order(
    relation_values: list[str], group: tuple[tuple[int, ...], ...]
) -> int:
    return sum(
        all(relation_values[permutation[index]] == relation_values[index] for index in range(len(relation_values)))
        for permutation in group
    )


Vector = tuple[int, int]
Matrix = tuple[int, int, int, int]
ZERO: Vector = (0, 0)
P: Vector = (1, 0)
Q: Vector = (0, 1)
D: Vector = (1, 1)
LINES = (
    frozenset((ZERO, P)),
    frozenset((ZERO, Q)),
    frozenset((ZERO, D)),
)


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return (
        matrix[0] * vector[0] ^ matrix[1] * vector[1],
        matrix[2] * vector[0] ^ matrix[3] * vector[1],
    )


def gl2_matrices() -> tuple[Matrix, ...]:
    return tuple(
        matrix
        for matrix in itertools.product((0, 1), repeat=4)
        if matrix[0] * matrix[3] ^ matrix[1] * matrix[2]
    )


def orientation_counts() -> dict[str, int]:
    gl2 = gl2_matrices()
    orbit = {
        frozenset(mat_vec(matrix, vector) for vector in LINES[0])
        for matrix in gl2
    }
    fixed = [
        line
        for line in LINES
        if all(
            frozenset(mat_vec(matrix, vector) for vector in line) == line
            for matrix in gl2
        )
    ]
    return {
        "gl2_order": len(gl2),
        "agl2_order": len(gl2) * 4,
        "line_count": len(LINES),
        "line_orbit_size": len(orbit),
        "fixed_line_count": len(fixed),
    }


def parity_partition(mask: int, root: int, n: int, edges: tuple[tuple[int, int], ...]) -> int | None:
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for edge_index, (source, target) in enumerate(edges):
        if mask & (1 << edge_index):
            adjacency[source].append(target)
    parity: list[int | None] = [None] * n
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
    if any(value is None for value in parity) or len(set(parity)) != 2:
        return None
    return sum((value == 1) << index for index, value in enumerate(parity))


def rooted_graph_census() -> dict[str, object]:
    n = 4
    edges = tuple((source, target) for source in range(n) for target in range(n) if source != target)
    rooted_records = 0
    admitted_graphs = 0
    relation_counts: Counter[int] = Counter()
    root_counts: Counter[int] = Counter()
    edge_counts: Counter[int] = Counter()
    odd_sizes: Counter[int] = Counter()
    for mask in range(1 << len(edges)):
        partitions = [
            partition
            for root in range(n)
            if (partition := parity_partition(mask, root, n, edges)) is not None
        ]
        if not partitions:
            continue
        admitted_graphs += 1
        rooted_records += len(partitions)
        root_counts[len(partitions)] += 1
        relation_counts[len(set(partitions))] += 1
        edge_counts[mask.bit_count()] += 1
        for partition in partitions:
            odd_sizes[partition.bit_count()] += 1
    return {
        "loop_free_directed_graphs": 1 << len(edges),
        "graph_root_configurations": (1 << len(edges)) * n,
        "admitted_rooted_records": rooted_records,
        "admitted_transition_graphs": admitted_graphs,
        "graphs_with_one_relation": relation_counts[1],
        "graphs_with_two_relations": relation_counts[2],
        "root_count_distribution": dict(sorted(root_counts.items())),
        "edge_count_distribution": dict(sorted(edge_counts.items())),
        "odd_block_size_distribution": dict(sorted(odd_sizes.items())),
    }


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
    seen = {0}
    queue: deque[int] = deque([0])
    while queue:
        current = queue.popleft()
        for other in range(len(reach)):
            if other not in seen and (reach[current][other] or reach[other][current]):
                seen.add(other)
                queue.append(other)
    return len(seen) == len(reach)


def cover_edges(reach: list[list[bool]]) -> set[tuple[int, int]]:
    covers: set[tuple[int, int]] = set()
    for lower in range(len(reach)):
        for upper in range(len(reach)):
            if lower == upper or not reach[lower][upper]:
                continue
            if not any(
                middle not in {lower, upper}
                and reach[lower][middle]
                and reach[middle][upper]
                for middle in range(len(reach))
            ):
                covers.add((lower, upper))
    return covers


def classify_unary_action(n: int, generator: Transformation) -> str:
    reach = reachability(n, (generator,))
    if not weakly_connected(reach):
        return "not_full_action_component"
    if any(
        left != right and reach[left][right] and reach[right][left]
        for left in range(n)
        for right in range(n)
    ):
        return "periodic_or_nonantisymmetric_reachability"
    minima = [
        point
        for point in range(n)
        if not any(other != point and reach[other][point] for other in range(n))
    ]
    if len(minima) != 1:
        return "nonunique_global_minimum"
    root = minima[0]
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
        for parent in [lower for lower, upper in covers if upper == point]:
            lengths[point].update(length + 1 for length in lengths[parent])
        if not lengths[point] or len(lengths[point]) != 1:
            return "non_graded_or_infinite_rank"
    ranks = {point: next(iter(values)) for point, values in lengths.items()}
    even = [point for point, rank in ranks.items() if rank % 2 == 0]
    odd = [point for point, rank in ranks.items() if rank % 2 == 1]
    if not even or not odd:
        return "empty_parity_block"
    return "admitted"


def unary_action_census() -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for n in range(1, 5):
        counts = Counter(
            classify_unary_action(n, tuple(generator))
            for generator in itertools.product(range(n), repeat=n)
        )
        result[f"n{n}"] = {
            "total_actions": n**n,
            "classification_counts": dict(sorted(counts.items())),
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(FIXTURES.read_text(encoding="utf-8"))
    theorem_map = yaml.safe_load(INSTANCE_MAP.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    for relative_path, expected_hash in manifest["source_hashes"].items():
        checks[f"source_hash::{relative_path}"] = sha256(ROOT / relative_path) == expected_hash

    fixture_results: dict[str, dict[str, object]] = {}
    statuses = Counter()
    families = set()
    fixture_ids = set()
    file_or_process_symmetry_count = 0
    for fixture in manifest["fixtures"]:
        fixture_id = fixture["fixture_id"]
        fixture_ids.add(fixture_id)
        if fixture["family"] != "theorem_control":
            families.add(fixture["family"])
        statuses[fixture["theorem_status"]] += 1
        if fixture["symmetry_basis"] != "source_structure":
            file_or_process_symmetry_count += 1
        size = len(fixture["selection_space"])
        group = generated_group(size, fixture["generators"])
        orbits = orbit_decomposition(size, group)
        fixed = fixed_indices(size, group)
        relation_image_sizes = {
            name: len(set(values)) for name, values in fixture["relation_maps"].items()
        }
        relation_stabilizers = {
            name: relation_stabilizer_order(values, group)
            for name, values in fixture["relation_maps"].items()
        }
        expected = fixture["expected"]
        checks[f"fixture::{fixture_id}::group_order"] = len(group) == expected["group_order"]
        checks[f"fixture::{fixture_id}::orbits"] = orbits == expected["orbits"]
        checks[f"fixture::{fixture_id}::fixed"] = fixed == expected["fixed_indices"]
        checks[f"fixture::{fixture_id}::relation_images"] = relation_image_sizes == expected["relation_image_sizes"]
        checks[f"fixture::{fixture_id}::relation_stabilizers"] = relation_stabilizers == expected["relation_stabilizer_orders"]
        status = fixture["theorem_status"]
        conclusion = expected["conclusion"]
        checks[f"fixture::{fixture_id}::classification"] = (
            (status == "direct_theorem_instance" and fixture["admitted"] and not fixed and conclusion == "no_core_selector")
            or (status == "fixed_point_positive_control" and fixture["admitted"] and len(fixed) == 1 and conclusion == "unique_core_selector_control")
            or (status == "multiple_fixed_point_control" and fixture["admitted"] and len(fixed) > 1 and conclusion == "multiple_core_selectors_control")
            or (status == "guarded_non_instance" and not fixture["admitted"] and conclusion.startswith("guarded_non_instance_"))
        )
        fixture_results[fixture_id] = {
            "group_order": len(group),
            "group_elements": [list(element) for element in group],
            "orbits": orbits,
            "fixed_indices": fixed,
            "relation_image_sizes": relation_image_sizes,
            "relation_stabilizer_orders": relation_stabilizers,
            "theorem_status": status,
            "conclusion": conclusion,
        }

    aggregate = manifest["aggregate_expectations"]
    checks["aggregate::fixture_count"] = len(manifest["fixtures"]) == aggregate["fixture_count"]
    checks["aggregate::fixture_ids_unique"] = len(fixture_ids) == len(manifest["fixtures"])
    checks["aggregate::historical_family_count"] = len(families) == aggregate["historical_family_count"]
    for status_name in (
        "direct_theorem_instance",
        "fixed_point_positive_control",
        "multiple_fixed_point_control",
        "guarded_non_instance",
    ):
        checks[f"aggregate::{status_name}"] = statuses[status_name] == aggregate[f"{status_name}_count"]
    checks["aggregate::no_file_or_process_symmetry"] = file_or_process_symmetry_count == aggregate["file_or_process_symmetry_fixture_count"] == 0

    mapped = {row["fixture_id"]: row for row in theorem_map["mapping"]}
    checks["instance_map::coverage"] = set(mapped) == fixture_ids
    checks["instance_map::status_and_conclusion_parity"] = all(
        mapped[fixture_id]["theorem_status"] == result["theorem_status"]
        and mapped[fixture_id]["exact_conclusion"] == result["conclusion"]
        for fixture_id, result in fixture_results.items()
    )

    orientation = orientation_counts()
    checks["reproduce::orientation_counts"] = orientation == {
        "gl2_order": 6,
        "agl2_order": 24,
        "line_count": 3,
        "line_orbit_size": 3,
        "fixed_line_count": 0,
    }
    rooted = rooted_graph_census()
    checks["reproduce::rooted_graph_census"] = rooted == {
        "loop_free_directed_graphs": 4096,
        "graph_root_configurations": 16384,
        "admitted_rooted_records": 1088,
        "admitted_transition_graphs": 557,
        "graphs_with_one_relation": 292,
        "graphs_with_two_relations": 265,
        "root_count_distribution": {1: 292, 2: 108, 3: 48, 4: 109},
        "edge_count_distribution": {3: 64, 4: 186, 5: 192, 6: 88, 7: 24, 8: 3},
        "odd_block_size_distribution": {1: 96, 2: 960, 3: 32},
    }
    unary = unary_action_census()
    checks["reproduce::graded_unary_action_census"] = unary == {
        "n1": {"total_actions": 1, "classification_counts": {"empty_parity_block": 1}},
        "n2": {"total_actions": 4, "classification_counts": {"admitted": 2, "not_full_action_component": 1, "periodic_or_nonantisymmetric_reachability": 1}},
        "n3": {"total_actions": 27, "classification_counts": {"admitted": 6, "nonunique_global_minimum": 3, "not_full_action_component": 10, "periodic_or_nonantisymmetric_reachability": 8}},
        "n4": {"total_actions": 256, "classification_counts": {"admitted": 24, "nonunique_global_minimum": 40, "not_full_action_component": 114, "periodic_or_nonantisymmetric_reachability": 78}},
    }

    atlas_text = ATLAS.read_text(encoding="utf-8")
    required_tokens = [
        "EQSRC-FINITE-COUNTERMODEL-ATLAS-V1",
        "direct theorem instance",
        "guarded noninstance",
        "multiple-fixed control",
        "Structural automorphisms are not physical gauge transformations",
        "P2-T05",
        "P2-T06",
        "physics_promotion_authorized: false",
    ]
    checks["atlas::required_claim_boundaries"] = all(token in atlas_text for token in required_tokens)
    checks["map::claim_boundaries"] = all(value is False for value in theorem_map["claim_boundary"].values())

    failed = sorted(name for name, passed in checks.items() if not passed)
    payload = {
        "schema_id": "eqsrc-finite-countermodel-atlas-validation.v1",
        "task_id": "RT-20260720-017",
        "atlas_id": manifest["atlas_id"],
        "status": "PASS" if not failed else "FAIL",
        "authority": "Finite operational evidence only; not ontology, physical-gauge, covariance, proof-assistant, or promotion authority.",
        "counts": {
            "check_count": len(checks),
            "passed_check_count": len(checks) - len(failed),
            "failed_check_count": len(failed),
            "fixture_count": len(manifest["fixtures"]),
            "historical_family_count": len(families),
            "direct_theorem_instance_count": statuses["direct_theorem_instance"],
            "fixed_point_positive_control_count": statuses["fixed_point_positive_control"],
            "multiple_fixed_point_control_count": statuses["multiple_fixed_point_control"],
            "guarded_non_instance_count": statuses["guarded_non_instance"],
        },
        "artifact_hashes": {
            "atlas": sha256(ATLAS),
            "fixtures": sha256(FIXTURES),
            "theorem_instance_map": sha256(INSTANCE_MAP),
        },
        "independent_recomputations": {
            "orientation": orientation,
            "rooted_graph_census": rooted,
            "graded_unary_action_census": unary,
        },
        "fixture_results": fixture_results,
        "checks": checks,
        "failed_checks": failed,
        "claim_boundary": theorem_map["claim_boundary"],
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8")
    if args.json or not args.write_report:
        print(rendered, end="")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
