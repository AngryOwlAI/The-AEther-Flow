#!/usr/bin/env python3
"""Deterministic support checker for the P6-T01 target formalization.

PASS is operational evidence only. It is not theorem truth, ontology or
source-law adoption, physical causality, effective geometry, proof authority,
publication authority, or physics promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260726-002"
ART = TASK / "artifacts"
REPORT = ART / "causal_characteristic_target_validation_receipt_v1.json"

SOURCES = {
    "research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex":
        "a2b9c6670cdb0e09ca2e19ff30f71d9bb954e3ab2fc73a5c9727a2df10db93aa",
    "research_control/tasks/RT-20260726-001/artifacts/p6_geometry_input_contract_v1.yaml":
        "7b0eee4ea249a3acf99d38d312bd14619dedea79977d7b802062e9410f5b8557",
    "research_control/tasks/RT-20260726-001/jobs/completions/AJC-AJ-RT-20260726-001-001.yaml":
        "d866758ebe728146486b117d5825a687035dda311ada6c59eb4c17cde482dcb0",
    "research_control/handoffs/handoff-0875.yaml":
        "fd9cbbc8c28d44179a33c1ac63631d47bb9843cfeb113e8294d33d712dbe2a70",
    "ontology/tex/aether_flow_foundations.tex":
        "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
    "ontology/tex/aether_flow_dynamics.tex":
        "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
    "ontology/tex/aether_flow_geometry.tex":
        "f60a81b63f814b03cca7190b3ac6285842a55317f4aed058cc6e75154cc0b4d7",
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "research_control/tasks/RT-20260614-216/artifacts/245_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_METRICFORMASSIGN_GEFF_CANDIDATE_OR_OBSTRUCTION.tex":
        "dd30573519ed1df66b3800d29ee0adc9fcc94d9c8d3b9b5a7fcffde503d5f0ef",
    "research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex":
        "3ce8cbc6cd79c6852d78f81045633beea44c4dfc6e2912c604b08e3c8bdb0257",
    "registries/METRIC_USE_LEDGER.csv":
        "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf",
}

REQUIRED_ARTIFACTS = [
    "causal_characteristic_target_v1.tex",
    "source_influence_characteristic_spec_v1.yaml",
    "gate_b_readiness_checklist_v1.yaml",
    "child_phys_math_p6_t01_causal_characteristic_target.yaml",
    "child_phys_phil_p6_t01_causal_characteristic_target.yaml",
    "parent_conflict_review_p6_t01_causal_characteristic_target.yaml",
    "parent_fusion_notes_p6_t01_causal_characteristic_target.md",
    "causal_characteristic_target_receipt.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phi(x: float, tau: float, gamma: float) -> float:
    return x / math.sqrt(1.0 + 2.0 * gamma * tau * x * x)


def dphi(x: float, tau: float, gamma: float) -> float:
    return (1.0 + 2.0 * gamma * tau * x * x) ** -1.5


def response(x: float, tau: float, gamma: float, coupling: float) -> list[list[float]]:
    scalar = dphi(x, tau, gamma)
    transverse = math.exp(-2.0 * coupling * tau)
    return [
        [
            0.5 * scalar * (1.0 + transverse),
            0.5 * scalar * (1.0 - transverse),
        ],
        [
            0.5 * scalar * (1.0 - transverse),
            0.5 * scalar * (1.0 + transverse),
        ],
    ]


def multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(2))
            for j in range(2)
        ]
        for i in range(2)
    ]


def close(x: float, y: float, tol: float = 2e-9) -> bool:
    return abs(x - y) <= tol * max(1.0, abs(x), abs(y))


def matrices_close(a: list[list[float]], b: list[list[float]]) -> bool:
    return all(close(a[i][j], b[i][j]) for i in range(2) for j in range(2))


def matrices_close_tol(
    a: list[list[float]],
    b: list[list[float]],
    tol: float,
) -> bool:
    return all(
        close(a[i][j], b[i][j], tol)
        for i in range(2)
        for j in range(2)
    )


def run_checks() -> dict:
    checks: list[dict] = []

    def record(check_id: str, passed: bool, detail: str) -> None:
        checks.append({
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        })

    for rel, expected in SOURCES.items():
        path = ROOT / rel
        actual = sha256(path) if path.is_file() else ""
        record(
            f"source_hash::{rel}",
            actual == expected,
            f"expected={expected} actual={actual}",
        )

    artifact_hashes = {}
    for name in REQUIRED_ARTIFACTS:
        path = ART / name
        present = path.is_file()
        record(f"artifact_present::{name}", present, str(path))
        if present:
            artifact_hashes[str(path.relative_to(ROOT))] = sha256(path)

    symmetric_ok = True
    degenerate_ok = True
    positive_ok = True
    cocycle_ok = True
    generator_ok = True
    for gamma in (0.3, 1.0, 2.2):
        for x in (-2.1, -0.4, 0.0, 0.7, 1.9):
            for coupling in (0.0, 0.2, 1.4):
                for tau in (0.05, 0.6, 1.7):
                    matrix = response(x, tau, gamma, coupling)
                    scalar = dphi(x, tau, gamma)
                    symmetric_ok = symmetric_ok and close(
                        matrix[0][0] + matrix[0][1], scalar
                    )
                    symmetric_ok = symmetric_ok and close(
                        matrix[1][0] + matrix[1][1], scalar
                    )
                    if coupling == 0.0:
                        degenerate_ok = (
                            degenerate_ok
                            and close(matrix[0][1], 0.0)
                            and close(matrix[1][0], 0.0)
                        )
                    else:
                        positive_ok = (
                            positive_ok
                            and matrix[0][1] > 0.0
                            and matrix[1][0] > 0.0
                        )
                first = 0.31
                second = 0.73
                lhs = response(x, first + second, gamma, coupling)
                rhs = multiply(
                    response(phi(x, first, gamma), second, gamma, coupling),
                    response(x, first, gamma, coupling),
                )
                cocycle_ok = cocycle_ok and matrices_close(lhs, rhs)

                h = 1e-5
                finite_generator = [
                    [
                        (
                            response(x, h, gamma, coupling)[i][j]
                            - response(x, -h, gamma, coupling)[i][j]
                        ) / (2.0 * h)
                        for j in range(2)
                    ]
                    for i in range(2)
                ]
                expected_generator = [
                    [-3.0 * gamma * x * x - coupling, coupling],
                    [coupling, -3.0 * gamma * x * x - coupling],
                ]
                generator_ok = generator_ok and matrices_close_tol(
                    finite_generator, expected_generator, 2e-7
                )

    record(
        "two_site_symmetric_response_independent_of_c",
        symmetric_ok,
        "row sums equal the P5 diagonal tangent response",
    )
    record(
        "two_site_degenerate_control",
        degenerate_ok,
        "c=0 has zero cross-site response",
    )
    record(
        "two_site_positive_control",
        positive_ok,
        "c>0 and tau>0 have positive cross-site response",
    )
    record(
        "two_site_response_cocycle",
        cocycle_ok,
        "R(t+s,x)=R(s,phi_t(x))R(t,x)",
    )
    record(
        "two_site_generator",
        generator_ok,
        "response derivative at zero matches the displayed Jacobian",
    )

    spec = yaml.safe_load(
        (ART / "source_influence_characteristic_spec_v1.yaml").read_text()
    )
    record(
        "spec_result_status",
        spec["result_status"]
        == "target_defined_with_precise_scoped_nonselection_obstruction",
        spec["result_status"],
    )
    record(
        "spec_metric_free",
        (
            spec["formal_influence_relation"]["metric_required"] is False
            and spec["formal_influence_relation"]["target_metric_allowed_as_premise"]
            is False
            and spec["formal_influence_relation"]["gr_null_cone_allowed_as_premise"]
            is False
        ),
        str(spec["formal_influence_relation"]),
    )
    record(
        "spec_nonselection_scope",
        (
            spec["two_site_countermodel_family"]["diagonal_invariant"] is True
            and spec["two_site_countermodel_family"][
                "symmetric_response_independent_of_c"
            ] is True
            and spec["authority"]["global_no_go_claimed"] is False
        ),
        str(spec["two_site_countermodel_family"]),
    )
    record(
        "spec_next_route",
        (
            spec["disposition"]["next_plan_task_id"] == "P6-T02"
            and spec["disposition"]["next_allowed_route"]
            == "candidate_constructor"
        ),
        str(spec["disposition"]),
    )

    checklist = yaml.safe_load(
        (ART / "gate_b_readiness_checklist_v1.yaml").read_text()
    )
    record(
        "gate_b_overall",
        (
            checklist["overall_result"]
            == "NOT_READY_PRECISE_SCOPED_OBSTRUCTION"
            and checklist["physical_gate_passed"] is False
        ),
        checklist["overall_result"],
    )
    record(
        "gate_b_target_and_import_guard",
        (
            checklist["fields"]["metric_free_target_definition"]["status"]
            == "PASS"
            and checklist["fields"]["target_metric_import_guard"]["status"]
            == "PASS"
        ),
        "metric-free target and no-target-import guard pass",
    )
    record(
        "gate_b_controls",
        set(checklist["controls"]) == {
            "positive", "degenerate", "acausal", "multi_cone"
        }
        and all(
            item["status"] == "PASS"
            for item in checklist["controls"].values()
        ),
        str(checklist["controls"]),
    )
    record(
        "gate_b_scale_deferred",
        (
            checklist["fields"]["metric_scale"]["status"]
            == "DEFERRED_TO_LATER_WORK_ITEM"
            and checklist["metric_scale_deferred"] is True
        ),
        str(checklist["fields"]["metric_scale"]),
    )

    tex = (ART / "causal_characteristic_target_v1.tex").read_text()
    for marker in [
        "P6T01-THM-RESPONSE-SUPPORT-COMPOSITION",
        "P6T01-THM-DIAGONAL-RESPONSE-NONSELECTION",
        "P6T01-PROP-PRECISE-SCOPED-OBSTRUCTION",
        "formal source influence",
        "not yet physical causality",
        "blocked\\_adoption\\_open\\_continuation",
        "not a global no-go theorem",
        "GR null cone",
        "P6-T02",
    ]:
        record(
            f"boundary_marker::{marker}",
            marker in tex,
            "required manuscript marker",
        )

    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v21_p6_t01_causal_characteristic_target_validation_receipt_v1",
        "task_id": "RT-20260726-002",
        "job_id": "AJ-RT-20260726-002-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "fixed_source_hash_count": len(SOURCES),
        "metric_free_target_definition_count": 3,
        "new_theorem_level_statement_count": 2,
        "precise_scoped_obstruction_count": 1,
        "finite_countermodel_family_count": 1,
        "gate_b_control_count": 4,
        "physical_gate_b_pass_count": 0,
        "target_metric_premise_count": 0,
        "artifact_hashes": artifact_hashes,
        "source_hashes": SOURCES,
        "checks": checks,
        "authority_note": (
            "Operational validation only; no theorem truth, ontology or "
            "source-law adoption, physical causality, effective geometry, "
            "proof, publication, promotion, or completed-derivation authority."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = run_checks()
    if args.write_report:
        REPORT.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json or not (args.write_report or args.check):
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
