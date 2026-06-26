"""Marked finite graph support checker for RT-20260614-181.

This script is scaffolding only. It is not proof authority and does not adopt
MetricData(E), construct g_eff, or promote downstream GR claims.
"""

from __future__ import annotations

import json
from pathlib import Path

Vertex = str
Edge = tuple[Vertex, Vertex]


def reachability(vertices: list[Vertex], edges: list[Edge]) -> dict[Vertex, set[Vertex]]:
    """Return strict transitive reachability for a finite directed graph."""
    vertex_set = set(vertices)
    if len(vertex_set) != len(vertices):
        raise ValueError("duplicate vertex")
    reach = {vertex: set() for vertex in vertices}
    for src, dst in edges:
        if src not in vertex_set or dst not in vertex_set:
            raise ValueError("edge endpoint outside vertex set")
        if src == dst:
            raise ValueError("self loop is outside the acyclic family")
        reach[src].add(dst)
    changed = True
    while changed:
        changed = False
        for src in vertices:
            expanded = set(reach[src])
            for mid in list(reach[src]):
                expanded.update(reach[mid])
            if expanded != reach[src]:
                reach[src] = expanded
                changed = True
    for vertex in vertices:
        if vertex in reach[vertex]:
            raise ValueError("cycle detected")
    return reach


def response_profiles(
    vertices: list[Vertex], reach: dict[Vertex, set[Vertex]]
) -> dict[Vertex, tuple[int, int]]:
    """Return incoming and outgoing reachability counts for each source site."""
    profiles: dict[Vertex, tuple[int, int]] = {}
    for vertex in vertices:
        outgoing = len(reach[vertex])
        incoming = sum(1 for other in vertices if vertex in reach[other])
        profiles[vertex] = (incoming, outgoing)
    return profiles


def marked_profiles(
    vertices: list[Vertex],
    reach: dict[Vertex, set[Vertex]],
    beta: dict[Vertex, str],
) -> dict[Vertex, tuple[int, int, str]]:
    """Return marked profiles using reachability counts and explicit beta."""
    profiles = response_profiles(vertices, reach)
    return {
        vertex: (profiles[vertex][0], profiles[vertex][1], beta[vertex])
        for vertex in vertices
    }


def profiles_distinguish_sites(profiles: dict[Vertex, tuple]) -> bool:
    """Return true when all site profiles are distinct."""
    return len(set(profiles.values())) == len(profiles)


def is_beta_separated_marked_graph(
    vertices: list[Vertex], edges: list[Edge], beta: dict[Vertex, str]
) -> tuple[bool, str]:
    """Check the declared beta-separated marked finite DAG family shape."""
    if set(beta) != set(vertices):
        return False, "beta domain does not match vertices"
    if len(set(beta.values())) != len(vertices):
        return False, "beta labels are not injective"
    try:
        reachability(vertices, edges)
    except ValueError as exc:
        return False, str(exc)
    return True, "ok"


def classify_candidate(vertices: list[Vertex], edges: list[Edge], beta: dict[Vertex, str]) -> dict:
    """Classify pass, collapse, malformed domain, or finite-variation pressure."""
    is_member, reason = is_beta_separated_marked_graph(vertices, edges, beta)
    if not is_member:
        unmarked_profiles = {}
        try:
            reach = reachability(vertices, edges)
            unmarked_profiles = response_profiles(vertices, reach)
        except ValueError:
            pass
        return {
            "classification": "malformed_or_bottom_domain",
            "reason": reason,
            "unmarked_profiles": unmarked_profiles,
        }
    reach = reachability(vertices, edges)
    unmarked = response_profiles(vertices, reach)
    marked = marked_profiles(vertices, reach, beta)
    return {
        "classification": "beta_separated_marked_graph_candidate_support",
        "vertices": vertices,
        "edges": edges,
        "beta": beta,
        "unmarked_profiles": unmarked,
        "marked_profiles": marked,
        "unmarked_profiles_distinguish_sites": profiles_distinguish_sites(unmarked),
        "marked_profiles_distinguish_sites": profiles_distinguish_sites(marked),
        "claim_limit": "support only; TeX controls proof",
    }


def diamond_pressure_case() -> dict:
    """Return marked and unmarked diamond pressure-test results."""
    vertices = ["r", "u1", "u2", "t"]
    edges = [("r", "u1"), ("r", "u2"), ("u1", "t"), ("u2", "t")]
    beta = {"r": "root", "u1": "branch_1", "u2": "branch_2", "t": "terminal"}
    marked = classify_candidate(vertices, edges, beta)
    merged_beta = {"r": "root", "u1": "branch", "u2": "branch", "t": "terminal"}
    merged = classify_candidate(vertices, edges, merged_beta)
    return {
        "case": "diamond_pressure",
        "marked_beta_case": marked,
        "merged_beta_case": merged,
        "claim_limit": "unmarked or non-injective beta collapses or fails closed",
    }


def main() -> None:
    cases = [
        classify_candidate(
            ["a", "b", "c"],
            [("a", "b"), ("b", "c")],
            {"a": "a_beta", "b": "b_beta", "c": "c_beta"},
        ),
        classify_candidate(
            ["r", "x1", "x2", "y"],
            [("r", "x1"), ("x1", "x2"), ("r", "y")],
            {"r": "root", "x1": "tail_1", "x2": "tail_2", "y": "short_branch"},
        ),
    ]
    report = {
        "artifact_id": "marked_finite_graph_witness_checker_report",
        "task_id": "RT-20260614-181",
        "proof_authority": "none; TeX artifact controls mathematical claims",
        "metric_data_adopted": False,
        "g_eff_constructed": False,
        "arbitrary_finite_dag_theorem": False,
        "beta_separated_cases_checked": cases,
        "diamond_pressure": diamond_pressure_case(),
        "malformed_domain_cases": [
            classify_candidate(["a", "b"], [("a", "b")], {"a": "same", "b": "same"}),
            classify_candidate(["a", "b"], [("a", "b"), ("b", "a")], {"a": "a_beta", "b": "b_beta"}),
            classify_candidate(["a", "b"], [("a", "b")], {"a": "a_beta"}),
        ],
        "finite_variation_pressure_cases": [
            {
                "case": "delete_beta_label",
                "status": "bottom_or_source_repair_required",
            },
            {
                "case": "external_target_repair",
                "status": "blocked_not_source_repair",
            },
        ],
    }
    out_path = Path(__file__).with_name("marked_finite_graph_witness_checker_report.json")
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
