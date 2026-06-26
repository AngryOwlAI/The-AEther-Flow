"""Finite graph support checker for RT-20260614-163.

This script is scaffolding only. It is not proof authority and does not adopt
MetricData(E), construct g_eff, or promote downstream GR claims.
"""

from __future__ import annotations

import json
from pathlib import Path


def reachability(n: int, edges: list[tuple[int, int]]) -> list[list[bool]]:
    """Return transitive reachability matrix for vertices 0..n-1."""
    reach = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        reach[i][i] = True
    for src, dst in edges:
        if src < 0 or dst < 0 or src >= n or dst >= n:
            raise ValueError("edge endpoint outside vertex set")
        reach[src][dst] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    reach[i][j] = reach[i][j] or reach[k][j]
    return reach


def response_profiles(
    reach: list[list[bool]], omit_identity: bool = True
) -> list[tuple[int, int]]:
    """Return outgoing and incoming reachability counts for each source site."""
    n = len(reach)
    profiles: list[tuple[int, int]] = []
    for i in range(n):
        outgoing = 0
        incoming = 0
        for j in range(n):
            if omit_identity and i == j:
                continue
            if reach[i][j]:
                outgoing += 1
            if reach[j][i]:
                incoming += 1
        profiles.append((outgoing, incoming))
    return profiles


def profiles_distinguish_sites(profiles: list[tuple[int, int]]) -> bool:
    """Return true when all site profiles are distinct."""
    return len(set(profiles)) == len(profiles)


def is_chain_family_member(n: int, edges: list[tuple[int, int]]) -> bool:
    """Check the declared finite chain source-family shape for n vertices."""
    return sorted(edges) == [(i, i + 1) for i in range(n - 1)]


def diamond_pressure_case() -> dict:
    """Return the diamond graph pressure-test result."""
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    reach = reachability(4, edges)
    profiles = response_profiles(reach)
    return {
        "case": "diamond",
        "vertices": 4,
        "edges": edges,
        "profiles": profiles,
        "profiles_distinguish_sites": profiles_distinguish_sites(profiles),
        "classification": "collapse",
        "claim_limit": "diamond collapse blocks arbitrary finite-DAG overread",
    }


def classify_candidate(n: int, edges: list[tuple[int, int]]) -> dict:
    """Classify pass, collapse, malformed domain, or finite-variation pressure."""
    if n < 3:
        return {"classification": "malformed_domain", "reason": "need n>=3 vertices"}
    try:
        reach = reachability(n, edges)
    except ValueError as exc:
        return {"classification": "malformed_domain", "reason": str(exc)}
    profiles = response_profiles(reach)
    if not is_chain_family_member(n, edges):
        return {
            "classification": "outside_declared_chain_family",
            "profiles": profiles,
            "profiles_distinguish_sites": profiles_distinguish_sites(profiles),
        }
    if not profiles_distinguish_sites(profiles):
        return {"classification": "collapse", "profiles": profiles}
    return {
        "classification": "chain_family_candidate_support",
        "profiles": profiles,
        "claim_limit": "support only; TeX controls proof",
    }


def main() -> None:
    chain_cases = []
    for vertices in range(3, 8):
        edges = [(i, i + 1) for i in range(vertices - 1)]
        chain_cases.append(classify_candidate(vertices, edges))
    report = {
        "artifact_id": "finite_graph_witness_checker_report",
        "task_id": "RT-20260614-163",
        "proof_authority": "none; TeX artifact controls mathematical claims",
        "metric_data_adopted": False,
        "g_eff_constructed": False,
        "chain_cases_checked": chain_cases,
        "diamond_pressure": diamond_pressure_case(),
    }
    out_path = Path(__file__).with_name("finite_graph_witness_checker_report.json")
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
