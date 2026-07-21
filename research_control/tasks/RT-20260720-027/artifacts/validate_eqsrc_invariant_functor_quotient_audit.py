#!/usr/bin/env python3
"""Validate the bounded P3-T06 invariant-functor EqSrc audit and stress."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260720-027"
ARTIFACT_DIR = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACT_DIR / "eqsrc_invariant_functor_quotient_audit_validation.json"
VERDICT = "conditional_local_source_purity_pass_with_arbitrary_partition_and_interface_completeness_obstruction"
EXPECTED_HASHES = {
    "research_control/tasks/RT-20260720-026/artifacts/eqsrc_invariant_functor_quotient_relation_candidate_v1.tex": "badc60c72ff16f84fe88568b825ff738a8f160a225f011715f027c1da2cfa1c3",
    "research_control/tasks/RT-20260720-026/artifacts/eqsrc_invariant_functor_quotient_relation_spec_v1.yaml": "9c40dd2a83c5d9ee25a62c977b5b47eb5e2770890c8a7aa90dbe342cc7936ad1",
    "research_control/tasks/RT-20260720-026/artifacts/eqsrc_invariant_functor_quotient_relation_finite_witnesses_v1.json": "6f101a2b3e7bc808e165349ab9cab33f44fcb671d2eb3f294ac8bf6071d38ecd",
    "research_control/tasks/RT-20260720-026/jobs/completions/AJC-AJ-RT-20260720-026-001.yaml": "ac959bea2c7ed6aa752ae5ebf9848f77dfe0106a8e8b57cee0a80fe2f65fb502",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"expected mapping in {path}")
    return data


def check(checks: list[dict], check_id: str, ok: bool, detail: str) -> None:
    checks.append({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail})


def components(vertices: list[str], edges: list[list[str]]) -> int:
    unseen = set(vertices)
    count = 0
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            vertex = stack.pop()
            found = adjacency[vertex] & unseen
            unseen.difference_update(found)
            stack.extend(found)
    return count


def betti(graph: dict) -> list[int]:
    beta0 = components(graph["vertices"], graph["edges"])
    return [beta0, len(graph["edges"]) - len(graph["vertices"]) + beta0]


def canonical_partition(blocks: list[list[str]]) -> tuple[tuple[str, ...], ...]:
    return tuple(sorted((tuple(sorted(block)) for block in blocks)))


def validate() -> dict:
    checks: list[dict] = []
    for rel, expected in EXPECTED_HASHES.items():
        path = ROOT / rel
        observed = sha256(path) if path.is_file() else "missing"
        check(checks, f"hash:{rel}", observed == expected, f"expected={expected} observed={observed}")

    stress = json.loads((ARTIFACT_DIR / "eqsrc_invariant_functor_quotient_stress_cases_v1.json").read_text(encoding="utf-8"))
    verdict = load_yaml(ARTIFACT_DIR / "eqsrc_invariant_functor_quotient_audit_verdict_v1.yaml")
    audit_text = (ARTIFACT_DIR / "eqsrc_invariant_functor_quotient_smuggling_audit_v1.tex").read_text(encoding="utf-8")

    partition_data = stress["arbitrary_partition_realization"]
    partitions = partition_data["partitions"]
    expected_partitions = {
        (("a",), ("b",), ("c",)),
        (("a", "b"), ("c",)),
        (("a", "c"), ("b",)),
        (("a",), ("b", "c")),
        (("a", "b", "c"),),
    }
    observed_partitions = {canonical_partition(row["blocks"]) for row in partitions}
    check(checks, "bell_three_partition_exhaustion", observed_partitions == expected_partitions, f"count={len(observed_partitions)}")
    check(checks, "partition_count", len(partitions) == partition_data["partition_count"] == 5, f"count={len(partitions)}")
    for row in partitions:
        mapping = row["object_map"]
        block_of = {obj: index for index, block in enumerate(row["blocks"]) for obj in block}
        kernel_matches = all((mapping[left] == mapping[right]) == (block_of[left] == block_of[right]) for left in mapping for right in mapping)
        pair_count = sum(mapping[left] == mapping[right] for left in mapping for right in mapping)
        check(checks, f"partition_kernel:{row['partition_id']}", kernel_matches and pair_count == row["kernel_pair_count"], f"pair_count={pair_count}")
    extremes = {row["extreme"] for row in partitions}
    check(checks, "identity_constant_extremes", {"identity", "constant"}.issubset(extremes), f"extremes={sorted(extremes)}")

    graph_data = stress["graph_homology_stress"]
    graphs = {row["graph_id"]: row for row in graph_data["graphs"]}
    for graph_id, graph in graphs.items():
        observed = betti(graph)
        check(checks, f"betti:{graph_id}", observed == graph["expected_invariant"], f"expected={graph['expected_invariant']} observed={observed}")
    cases = {row["case_id"]: row for row in graph_data["cases"]}
    check(checks, "incomplete_cycle_pair", betti(graphs["C3"]) == betti(graphs["C4"]) and len(graphs["C3"]["vertices"]) != len(graphs["C4"]["vertices"]), "C3 and C4 share H but differ in size")
    check(checks, "tree_quotient_collapse", len({tuple(betti(graphs[name])) for name in cases["STRESS-QUOTIENT-COLLAPSE-TREES"]["members"]}) == 1, "bounded tree class collapsed")
    check(checks, "relabeling_control", betti(graphs["C3"]) == betti(graphs["C3_RELABELED"]), "relabeling preserved")
    check(checks, "component_control", betti(graphs["K2_MARKED"]) != betti(graphs["TWO_EDGES"]), "component count separated")

    countermodel = stress["marked_interface_counterexample"]
    left = graphs[countermodel["left_input"]]
    right = graphs[countermodel["right_input"]]

    def add_marked_edge(graph: dict) -> dict:
        endpoints = graph["marked_endpoints"]
        edge_set = {frozenset(edge) for edge in graph["edges"]}
        edge_set.add(frozenset(endpoints))
        return {"vertices": graph["vertices"], "edges": [sorted(edge) for edge in edge_set]}

    left_after = betti(add_marked_edge(left))
    right_after = betti(add_marked_edge(right))
    check(checks, "marked_interface_inputs_related", betti(left) == betti(right) == [1, 0], f"left={betti(left)} right={betti(right)}")
    check(checks, "marked_interface_outputs_split", left_after == [1, 0] and right_after == [1, 1], f"left={left_after} right={right_after}")
    check(checks, "IFQ2_scope_preserved", countermodel["direct_refutation_of_IFQ2"] is False, "countermodel targets missing comparison premise")

    check(checks, "verdict_identity", verdict["audit_verdict"] == stress["disposition"]["verdict"] == VERDICT, "verdicts agree")
    check(checks, "source_purity_scoped", verdict["source_pure_as_written"]["status"] is True and verdict["source_pure_as_written"]["explicit_target_import_count"] == 0 and verdict["source_pure_as_written"]["explicit_process_import_count"] == 0, "direct source-purity result")
    check(checks, "conditional_theorems_not_refuted", verdict["stress_results"]["IFQ2_refuted"] is False and verdict["theorem_validity"]["candidate_theorem_repair_required"] is False, "conditional theorem package preserved")
    check(checks, "scoped_freeze", verdict["candidate_disposition"]["not_a_global_rejection"] is True and verdict["candidate_disposition"]["blocked_adoption_open_continuation"] is True and len(verdict["candidate_disposition"]["reopening_criteria"]) == 4, "local freeze and reopening criteria present")
    authority = verdict["authority"]
    protected_flags = [
        "canonical_ontology_edit_authorized", "source_law_adoption_authorized",
        "source_law_rejection_authorized", "candidate_repair_executed",
        "P3_T07_executed", "physical_equivalence_established",
        "general_eqsrc_discharged", "distance_to_gr_ledger_changed",
        "metric_use_ledger_changed", "proof_authority",
        "physics_promotion_authorized", "external_publication_authorized",
        "global_no_go_authorized",
    ]
    check(checks, "authority_boundary", all(authority[key] is False for key in protected_flags), "all protected authority flags false")

    normalized_audit = " ".join(audit_text.split())
    required_phrases = [
        "source-pure as written", "every finite partition", "identity relation",
        "constant functor", "marked-interface", "does not refute",
        "not a global rejection", "P3-T07", "selected but not executed",
    ]
    check(checks, "audit_boundary_language", all(phrase in normalized_audit for phrase in required_phrases), "required scoped language present")

    child_paths = [
        ARTIFACT_DIR / "child_phys_math_eqsrc_invariant_functor_audit_stress.yaml",
        ARTIFACT_DIR / "child_phys_phil_eqsrc_invariant_functor_audit_stress.yaml",
    ]
    check(checks, "child_outputs_present", all(path.is_file() for path in child_paths), f"present={sum(path.is_file() for path in child_paths)}/2")
    if all(path.is_file() for path in child_paths):
        children = [load_yaml(path) for path in child_paths]
        check(checks, "child_outputs_completed", all(row.get("status") in {"completed", "PASS", "draft/control"} for row in children), f"statuses={[row.get('status') for row in children]}")

    failures = [row for row in checks if row["status"] != "PASS"]
    return {
        "schema_id": "eqsrc-invariant-functor-quotient-audit-validation.v1",
        "task_id": "RT-20260720-027",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failures),
        "failed_check_count": len(failures),
        "verdict": VERDICT,
        "source_hash_count": len(EXPECTED_HASHES),
        "finite_partition_count": len(partitions),
        "graph_count": len(graphs),
        "marked_interface_countermodel_count": 1,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']} {report['passed_check_count']}/{report['check_count']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
