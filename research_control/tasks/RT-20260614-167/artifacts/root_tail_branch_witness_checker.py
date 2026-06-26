#!/usr/bin/env python3
"""Support-only profile checker for RT-20260614-167.

The TeX artifact is proof authority. This script only reproduces small
finite graph profile calculations used as deterministic scaffolding.
"""

from __future__ import annotations

import json
from pathlib import Path


def transitive_closure(vertices: list[str], edges: list[tuple[str, str]]) -> set[tuple[str, str]]:
    closure = set(edges)
    changed = True
    while changed:
        changed = False
        additions: set[tuple[str, str]] = set()
        for a, b in closure:
            for c, d in closure:
                if b == c and a != d and (a, d) not in closure:
                    additions.add((a, d))
        if additions:
            closure |= additions
            changed = True
    return {(a, b) for (a, b) in closure if a in vertices and b in vertices and a != b}


def profiles(vertices: list[str], edges: list[tuple[str, str]]) -> dict[str, tuple[int, int]]:
    reach = transitive_closure(vertices, edges)
    return {
        v: (
            sum(1 for a, _ in reach if a == v),
            sum(1 for _, b in reach if b == v),
        )
        for v in vertices
    }


def rooted_tail_branch(n: int) -> dict[str, object]:
    vertices = ["r", "y"] + [f"x_{i}" for i in range(1, n + 1)]
    edges = [("r", "x_1"), ("r", "y")]
    edges.extend((f"x_{i}", f"x_{i + 1}") for i in range(1, n))
    prof = profiles(vertices, edges)
    return {
        "n": n,
        "classification": "rooted_tail_branch_candidate_support",
        "vertices": vertices,
        "edges": edges,
        "profiles": prof,
        "profiles_distinguish_sites": len(set(prof.values())) == len(vertices),
        "claim_limit": "support only; TeX controls proof",
    }


def diamond_pressure() -> dict[str, object]:
    vertices = ["0", "1", "2", "3"]
    edges = [("0", "1"), ("0", "2"), ("1", "3"), ("2", "3")]
    prof = profiles(vertices, edges)
    return {
        "case": "diamond",
        "vertices": vertices,
        "edges": edges,
        "profiles": prof,
        "profiles_distinguish_sites": len(set(prof.values())) == len(vertices),
        "classification": "collapse",
        "claim_limit": "diamond collapse blocks arbitrary finite-DAG overread",
    }


def main() -> None:
    report = {
        "artifact_id": "root_tail_branch_witness_checker_report",
        "task_id": "RT-20260614-167",
        "proof_authority": "none; TeX artifact controls mathematical claims",
        "metric_data_adopted": False,
        "g_eff_constructed": False,
        "rooted_tail_branch_cases_checked": [rooted_tail_branch(n) for n in range(2, 7)],
        "diamond_pressure": diamond_pressure(),
    }
    output_path = Path(__file__).with_name("root_tail_branch_witness_checker_report.json")
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
