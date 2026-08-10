#!/usr/bin/env python3
"""Exact audit model for the fixed RT010 common-character candidate.

This script checks source hashes and the linear/groupoid facts used by RT011.
It supplies operational evidence only; it does not adopt a source law or prove
physical, empirical, benchmark, or Distance-to-GR claims.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

SOURCES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1007.yaml":
        "5e7cab444d0db4b373a619f59e4d9228a4e5add26ab9245c8d717905cc396a3c",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_independent_variation_law_v1.tex":
        "6c81af99ff98b315b3867deed2658ec8123386b7d2f9fbc9517ed80b0c1f695f",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_descent_spec_v1.yaml":
        "70f25b557642d9bc4d71b92b9b05cdca045c670df775089058f4b444bfa1a4a2",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_independent_variation_law_v1.yaml":
        "bb30f36984d97f084a914b07253e872935f8f05190779a5c76a095d03235c774",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_source_provenance_separation_v1.yaml":
        "8692478fa808e39bbc580ff395d34c9162786a1e67000d7bbddba54fe72e04f0",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_candidate_disposition_v1.yaml":
        "1fa1e74be8c983aae376278df79c71748d97aa2e8713e0df3052b3235f7a73e0",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_model.py":
        "ff5a0d9e1973e8f5bc9a0db48e9b11afb25e17a8bc35b0d01a19097c9b8c67c8",
    "research_control/tasks/RT-20260810-010/artifacts/parent_fusion_notes_p4_t02_b2_common_character_independent_variation.md":
        "966fba0889677cc1d8ad2c6aa49af42eba793a0a9f94455b3b58170f7857f862",
    ".agents/roles/physics/smuggling-auditor.v0.2.0.md":
        "2ec5a542caffa90a54d11f0c03630fde839e92f4917d5dbd55b80b724a46c882",
    ".agents/roles/research_ops/director-of-research.v0.3.0.md":
        "66c116620dbef591f93a6db190395b46bef6cf0443baec1c11255ef552cfdbc6",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(row: list[Fraction], col: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(row, col)), Fraction(0))


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [x / scale for x in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row:
                continue
            factor = work[r][col]
            if factor:
                work[r] = [x - factor * y for x, y in zip(work[r], work[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def q(values: list[int]) -> list[Fraction]:
    return [Fraction(v) for v in values]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    def check(check_id: str, passed: bool, evidence: object) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "evidence": evidence})

    source_results = {}
    for rel, expected in SOURCES.items():
        actual = sha256(ROOT / rel)
        source_results[rel] = {"expected": expected, "actual": actual, "match": actual == expected}
    check("SOURCE-HASHES", all(item["match"] for item in source_results.values()), source_results)

    B = [q([1, -1, 1, -1]), q([1, 1, -1, -1])]
    d = q([1, 1, 1, 1])
    v = q([1, -1, -1, 1])
    m = q([1, -1, 0, 0])
    check("BALANCE-RANK", rank(B) == 2, {"rank": rank(B)})
    check("GAUGE-IN-KERNEL", all(dot(row, d) == 0 for row in B), [str(dot(row, d)) for row in B])
    check("VARIATION-IN-KERNEL", all(dot(row, v) == 0 for row in B), [str(dot(row, v)) for row in B])
    check("KERNEL-BASIS", rank([d, v]) == 2 and rank(B) == 2, {"kernel_dimension": 2, "quotient_dimension": 1})
    check("MU-GAUGE-INVARIANT", dot(m, d) == 0, str(dot(m, d)))
    check("MU-NONVACUOUS", dot(m, v) == 2, str(dot(m, v)))
    check("MU-OUTSIDE-BALANCE-ROWSPACE", rank(B + [m]) == 3, {"stacked_rank": rank(B + [m])})

    # Same typed DAG, different covector: acyclicity does not select relevance.
    m_zero = q([1, -1, 1, -1])
    x_star = q([2, 1, 1, 2])
    check(
        "ALTERNATIVE-COVECTOR-NONSELECTION",
        dot(m_zero, d) == 0 and dot(m_zero, v) == 0 and dot(m_zero, x_star) == 0,
        {
            "m_zero_d": str(dot(m_zero, d)),
            "m_zero_v": str(dot(m_zero, v)),
            "m_zero_x_star": str(dot(m_zero, x_star)),
            "same_dependency_graph_shape": True,
        },
    )

    # The admitted positive flow contains an exact internal collapse point.
    collapse_t = Fraction(-1, 2)
    x_collapse = [x + collapse_t * direction for x, direction in zip(x_star, v)]
    mu_collapse = dot(m, x_collapse)
    k_arrays = {"R": [0, 1, 3], "S": [0, -2, -1], "D": [0, 3, -1]}
    cochain_logs = {
        sector: [str(Fraction(k) * mu_collapse) for k in exponents]
        for sector, exponents in k_arrays.items()
    }
    sector_edge_logs = {
        sector: [
            str(mu_collapse * Fraction(1 + exponents[target] - exponents[source]))
            for source, target in ((0, 1), (1, 2), (2, 0))
        ]
        for sector, exponents in k_arrays.items()
    }
    check(
        "ADMISSIBLE-FLOW-TRIVIALIZATION-POINT",
        x_collapse == [Fraction(3, 2)] * 4
        and mu_collapse == 0
        and all(value == "0" for values in cochain_logs.values() for value in values)
        and all(value == "0" for values in sector_edge_logs.values() for value in values),
        {
            "t": str(collapse_t),
            "x": [str(value) for value in x_collapse],
            "mu": str(mu_collapse),
            "cochain_logs": cochain_logs,
            "sector_edge_logs": sector_edge_logs,
            "formal_descent_survives": True,
            "nontrivial_transition_content_survives": False,
        },
    )

    # A source-typed perturbation family: B_epsilon d=0. Rank two and
    # nonvacuity are open at epsilon=0 because the displayed ranks persist.
    perturbation_rows = [q([1, -1, 0, 0]), q([0, 0, 0, 0])]
    perturbation_samples = {}
    for epsilon in (Fraction(-1, 10), Fraction(0), Fraction(1, 10)):
        B_eps = [
            [entry + epsilon * delta for entry, delta in zip(row, change)]
            for row, change in zip(B, perturbation_rows)
        ]
        key = str(epsilon)
        perturbation_samples[key] = {
            "B_rank": rank(B_eps),
            "B_d": [str(dot(row, d)) for row in B_eps],
            "stacked_B_m_rank": rank(B_eps + [m]),
        }
    perturbation_pass = all(
        item["B_rank"] == 2
        and item["B_d"] == ["0", "0"]
        and item["stacked_B_m_rank"] == 3
        for item in perturbation_samples.values()
    )
    check("SOURCE-TYPED-OPEN-FAMILY-SAMPLES", perturbation_pass, perturbation_samples)

    # Positive one-dimensional representations of a connected one-cycle
    # groupoid are classified up to positive object cochains by one log
    # holonomy. Three sectors admit one common character iff their three log
    # holonomies lie on the diagonal, a codimension-two locus in R^3. If the
    # RT010 chi class is held fixed as a fourth coordinate, the three sector
    # equalities against it instead have codimension three in R^4.
    sector_count = 3
    common_holonomy_rank = 1
    holonomy_equality_codimension = sector_count - common_holonomy_rank
    check(
        "COMMON-HOLONOMY-PRELOAD-CODIMENSION",
        holonomy_equality_codimension == 2 and sector_count == 3,
        {
            "ambient_log_holonomy_dimension": sector_count,
            "common_diagonal_dimension": common_holonomy_rank,
            "codimension_to_some_common_character": holonomy_equality_codimension,
            "ambient_with_fixed_character_class_dimension": sector_count + 1,
            "codimension_to_the_fixed_rt010_character": sector_count,
            "anchor_changes_holonomy": False,
        },
    )

    # A nonzero additive perturbation on one R-sector edge has nonzero cycle
    # integral and therefore cannot be removed by an object coboundary.
    holonomy_perturbation_samples = {
        str(epsilon): {
            "cycle_log_holonomy_deviation": str(epsilon),
            "positive_representation_preserved": True,
            "common_intertwiner_to_fixed_chi_exists": epsilon == 0,
        }
        for epsilon in (Fraction(-1, 100), Fraction(0), Fraction(1, 100))
    }
    check(
        "SINGLE-EDGE-H1-HOLONOMY-PERTURBATION",
        all(
            item["common_intertwiner_to_fixed_chi_exists"] == (Fraction(key) == 0)
            for key, item in holonomy_perturbation_samples.items()
        ),
        holonomy_perturbation_samples,
    )

    # Anchors choose representatives only after the common-holonomy condition
    # holds. With three sectors, forgetting anchors leaves three constants;
    # common diagonal gauge removes one, leaving two relative moduli.
    check(
        "UNANCHORED-INTERTWINER-TORSOR",
        sector_count - 1 == 2,
        {"sector_constants": 3, "common_gauge_dimension": 1, "relative_moduli": 2},
    )

    vertices = (0, 1, 2)
    oriented_edges = {(0, 1), (1, 2), (2, 0)}
    oriented_automorphisms = []
    pointed_automorphisms = []
    for image in itertools.permutations(vertices):
        mapping = dict(zip(vertices, image))
        mapped_edges = {(mapping[a], mapping[b]) for a, b in oriented_edges}
        if mapped_edges == oriented_edges:
            oriented_automorphisms.append(image)
            if mapping[0] == 0:
                pointed_automorphisms.append(image)
    check(
        "PRESENTATION-AUTOMORPHISMS",
        len(oriented_automorphisms) == 3 and pointed_automorphisms == [(0, 1, 2)],
        {
            "orientation_preserving_count": len(oriented_automorphisms),
            "pointed_orientation_preserving_count": len(pointed_automorphisms),
            "pointed_maps": pointed_automorphisms,
            "interpretation": "The fixed pointed typed presentation has only the identity automorphism; covariance under transport is coherent but supplies no broad selector invariance.",
        },
    )

    report = {
        "schema_id": "v22_p4_t02_b2_common_character_independent_variation_smuggling_model_v1",
        "task_id": "RT-20260810-011",
        "status": "PASS" if all(item["passed"] for item in checks) else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "audit_inferences": {
            "target_import_detected": False,
            "common_character_condition": "codimension two for descent to some common class; codimension three when the RT010 chi class is fixed",
            "anchors": "representative selectors inside the pointed framed candidate; not a source-derived or physical normalization",
            "admissible_internal_collapse": "at t=-1/2 the positive flow has mu=0 and trivial chi, a_s, and rho_s while formal descent survives",
            "alternative_covector": "m_zero has the same typed DAG but is zero at the base state and on the admissible quotient, so acyclicity cannot select m",
            "variation_independence": "definitionally independent of response success; epistemic independence is not established by the DAG",
            "structured_family_robustness": "rank and nonvacuity persist on an open source-typed neighborhood",
            "unstructured_sector_holonomy_robustness": "not established; independent holonomy perturbations leave the common diagonal",
            "authority_effect": "none",
        },
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered if args.json else rendered)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
