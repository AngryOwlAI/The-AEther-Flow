#!/usr/bin/env python3
"""Validate the bounded P3-T05 invariant-functor quotient packet."""

from __future__ import annotations

import argparse
import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


HERE = Path(__file__).resolve().parent
SPEC_PATH = HERE / "eqsrc_invariant_functor_quotient_relation_spec_v1.yaml"
WITNESS_PATH = HERE / "eqsrc_invariant_functor_quotient_relation_finite_witnesses_v1.json"
MATH_CHILD_PATH = HERE / "child_phys_math_eqsrc_invariant_functor_quotient.yaml"
PHIL_CHILD_PATH = HERE / "child_phys_phil_eqsrc_invariant_functor_quotient.yaml"
CONFLICT_PATH = HERE / "parent_conflict_review_eqsrc_invariant_functor_quotient.yaml"
FUSION_PATH = HERE / "parent_fusion_notes_eqsrc_invariant_functor_quotient.md"
THEOREM_PATH = HERE / "eqsrc_invariant_functor_quotient_relation_candidate_v1.tex"
REPORT_PATH = HERE / "eqsrc_invariant_functor_quotient_relation_validation.json"

EXPECTED_THEOREM_IDS = {
    "IFQ1_KERNEL_EQUIVALENCE",
    "IFQ2_MONOIDAL_COMPOSITION_CONGRUENCE",
    "IFQ3_LOCALIZATION_PRESERVATION",
    "IFQ4_COARSE_GRAINING_PRESERVATION",
    "IFQ5_VARIATION_NATURALITY",
    "IFQ6_PHYSICAL_BRIDGE_GUARD",
}
EXPECTED_RELATION_IDS = {
    "R_POSITIVE_NONISOMORPHIC_CYCLES",
    "R_NEGATIVE_CYCLE_VS_TREE",
    "R_NEGATIVE_COMPONENT_COUNT",
}
EXPECTED_OPERATION_IDS = {
    "O_COMPOSITION_DISJOINT_UNION",
    "O_LOCALIZATION_EDGE_SUBDIVISION",
    "O_COARSE_GRAINING_BRIDGE_CONTRACTION",
    "O_VARIATION_RELABELING",
    "O_INEXACT_CYCLE_EDGE_DELETION",
    "O_INEXACT_CYCLE_COLLAPSE",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a mapping")
    return data


def graph_invariant(graph: dict[str, Any]) -> tuple[int, int]:
    vertices = graph["vertices"]
    edges = graph["edges"]
    if len(vertices) != len(set(vertices)):
        raise ValueError(f"{graph['graph_id']}: duplicate vertex")
    carrier = set(vertices)
    normalized_edges: set[tuple[str, str]] = set()
    adjacency = {vertex: set() for vertex in vertices}
    for raw_edge in edges:
        if not isinstance(raw_edge, list) or len(raw_edge) != 2:
            raise ValueError(f"{graph['graph_id']}: malformed edge")
        left, right = raw_edge
        if left not in carrier or right not in carrier or left == right:
            raise ValueError(f"{graph['graph_id']}: edge outside simple-graph domain")
        edge = tuple(sorted((left, right)))
        if edge in normalized_edges:
            raise ValueError(f"{graph['graph_id']}: duplicate edge")
        normalized_edges.add(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = 0
    remaining = set(vertices)
    while remaining:
        components += 1
        seed = next(vertex for vertex in vertices if vertex in remaining)
        queue: deque[str] = deque([seed])
        remaining.remove(seed)
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    queue.append(neighbor)
    beta_one = len(normalized_edges) - len(vertices) + components
    if beta_one < 0:
        raise ValueError(f"{graph['graph_id']}: negative beta_1")
    return components, beta_one


def check_packet() -> dict[str, Any]:
    errors: list[str] = []
    spec = load_yaml(SPEC_PATH)
    witnesses = json.loads(WITNESS_PATH.read_text(encoding="utf-8"))

    theorem_ids = {item.get("theorem_id") for item in spec.get("theorem_contracts", [])}
    if theorem_ids != EXPECTED_THEOREM_IDS:
        errors.append("theorem-contract ID set mismatch")

    relation = spec.get("candidate_relation", {})
    if relation.get("prospective_definition") is not True:
        errors.append("candidate relation is not marked prospective")
    for key in ("uses_desired_class_labels", "target_atlas_used", "target_metric_used", "benchmark_result_used"):
        if relation.get(key) is not False:
            errors.append(f"candidate relation source guard failed: {key}")

    flags = spec.get("authority_flags", {})
    if not flags or any(value is not False for value in flags.values()):
        errors.append("spec authority flags must all remain false")
    witness_flags = witnesses.get("authority_flags", {})
    if not witness_flags or any(value is not False for value in witness_flags.values()):
        errors.append("witness authority flags must all remain false")

    graph_map: dict[str, tuple[int, int]] = {}
    for graph in witnesses.get("graphs", []):
        graph_id = graph.get("graph_id", "")
        if not graph_id or graph_id in graph_map:
            errors.append("graph identifiers must be nonempty and unique")
            continue
        try:
            computed = graph_invariant(graph)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(str(exc))
            continue
        expected = tuple(graph.get("expected_invariant", []))
        if computed != expected:
            errors.append(f"{graph_id}: computed invariant {computed} != expected {expected}")
        graph_map[graph_id] = computed

    relation_ids: set[str] = set()
    relation_results: list[dict[str, Any]] = []
    for check in witnesses.get("relation_checks", []):
        check_id = check.get("check_id", "")
        relation_ids.add(check_id)
        left = graph_map.get(check.get("left"))
        right = graph_map.get(check.get("right"))
        actual = left is not None and left == right
        expected = check.get("expected_related")
        if actual != expected:
            errors.append(f"{check_id}: relation result mismatch")
        relation_results.append({"check_id": check_id, "actual_related": actual})
    if relation_ids != EXPECTED_RELATION_IDS:
        errors.append("relation-check ID set mismatch")

    operation_ids: set[str] = set()
    operation_results: list[dict[str, Any]] = []
    exact_classes: set[str] = set()
    inexact_count = 0
    for check in witnesses.get("operation_checks", []):
        check_id = check.get("check_id", "")
        operation_ids.add(check_id)
        before = check.get("before_pair", [])
        after = check.get("after_pair", [])
        if len(before) != 2 or len(after) != 2:
            errors.append(f"{check_id}: operation pairs must contain two graph IDs")
            continue
        before_related = graph_map.get(before[0]) == graph_map.get(before[1])
        after_related = graph_map.get(after[0]) == graph_map.get(after[1])
        actual_preserves = (not before_related) or after_related
        expected = check.get("expected_preserves_relation")
        if actual_preserves != expected:
            errors.append(f"{check_id}: operation preservation mismatch")
        if check.get("exact_admissible"):
            exact_classes.add(str(check.get("operation_class")))
            if expected is not True:
                errors.append(f"{check_id}: exact admissible check must preserve the relation")
        else:
            inexact_count += 1
            if expected is not False:
                errors.append(f"{check_id}: inexact control must expose non-preservation")
        operation_results.append(
            {
                "check_id": check_id,
                "before_related": before_related,
                "after_related": after_related,
                "actual_preserves_relation": actual_preserves,
                "exact_admissible": bool(check.get("exact_admissible")),
            }
        )
    if operation_ids != EXPECTED_OPERATION_IDS:
        errors.append("operation-check ID set mismatch")
    if exact_classes != {"composition", "localization", "coarse_graining", "variation"}:
        errors.append("exact operation coverage is incomplete")
    if inexact_count < 2:
        errors.append("at least two inexact coarse-graining controls are required")

    for child_path, perspective in (
        (MATH_CHILD_PATH, "physicist_mathematician"),
        (PHIL_CHILD_PATH, "physicist_philosopher"),
    ):
        try:
            child = load_yaml(child_path)
            if child.get("status") != "completed" or child.get("perspective") != perspective:
                errors.append(f"{child_path.name}: child status or perspective mismatch")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{child_path.name}: {exc}")

    try:
        conflict = load_yaml(CONFLICT_PATH)
        if conflict.get("status") != "resolved" or conflict.get("unresolved_conflicts") != []:
            errors.append("parent conflict review is not fully resolved")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"{CONFLICT_PATH.name}: {exc}")

    try:
        fusion_text = FUSION_PATH.read_text(encoding="utf-8")
        if "Shared consensus" not in fusion_text or "Unresolved limitations" not in fusion_text:
            errors.append("fusion notes omit required synthesis headings")
    except OSError as exc:
        errors.append(f"{FUSION_PATH.name}: {exc}")

    try:
        theorem_text = THEOREM_PATH.read_text(encoding="utf-8")
        normalized_theorem_text = " ".join(theorem_text.replace("\\_", "_").split())
        for theorem_id in EXPECTED_THEOREM_IDS:
            if theorem_id not in normalized_theorem_text:
                errors.append(f"theorem artifact omits marker {theorem_id}")
        for required_phrase in (
            "blocked_adoption_open_continuation",
            "not physical observational equivalence",
            "proposal-only",
        ):
            if required_phrase not in normalized_theorem_text:
                errors.append(f"theorem artifact omits guard phrase: {required_phrase}")
    except OSError as exc:
        errors.append(f"{THEOREM_PATH.name}: {exc}")

    return {
        "schema_id": "eqsrc_invariant_functor_quotient_relation_validation_v1",
        "artifact_id": "EQSRC-INVARIANT-FUNCTOR-QUOTIENT-RELATION-VALIDATION-V1",
        "task_id": "RT-20260720-026",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "PASS" if not errors else "FAIL",
        "graph_count": len(graph_map),
        "relation_check_count": len(relation_results),
        "operation_check_count": len(operation_results),
        "theorem_contract_count": len(theorem_ids),
        "relation_results": relation_results,
        "operation_results": operation_results,
        "errors": errors,
        "authority": "task-local finite verification only; no ontology adoption or physical-equivalence authority",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = check_packet()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
