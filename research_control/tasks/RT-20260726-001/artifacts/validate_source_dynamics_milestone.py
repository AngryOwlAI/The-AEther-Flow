#!/usr/bin/env python3
"""Deterministic support checker for the P5-T08 milestone synthesis.

PASS is operational evidence only.  It is not theorem truth, ontology
adoption, proof authority, publication authority, or physics promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260726-001"
ART = TASK / "artifacts"
REPORT = ART / "source_dynamics_milestone_validation_receipt_v1.json"

SOURCES = {
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_object_v1.tex":
        "2520f82e54edcb2668446579ceed7a7dfc7a8abf995572aa9889a3d9a3a4467c",
    "research_control/tasks/RT-20260725-007/artifacts/phi_src_semiflow_semantics_v1.tex":
        "60f7358e0643195d4e2b79f7fda921da223ef940d00968588a4175d23cc0b70f",
    "research_control/tasks/RT-20260725-008/artifacts/cubic_amplitude_source_dynamics_v1.tex":
        "98ce6833f6e4d8be22837d25845d7fa62d6886049e168d121de5de0093703f6a",
    "research_control/tasks/RT-20260725-010/artifacts/cubic_amplitude_structural_analysis_v1.tex":
        "a9a9f42ff016febc0f40a8a4db32b09f670084bda2248704e290cf5bee02a06b",
    "research_control/tasks/RT-20260725-012/artifacts/cubic_amplitude_background_phase_analysis_v1.tex":
        "73895f1325fa83799c343e0c88d525e1d9e006254844b8f8bd7bb8fe2286f48d",
    "research_control/tasks/RT-20260725-013/artifacts/source_amplitude_resolution_coarse_graining_v1.tex":
        "a798e69875603ec3d0f9202ea67de18fcbc3dabf1cb1a178713f8dde9aefd074",
    "research_control/tasks/RT-20260725-014/artifacts/source_dynamics_package_audit_v1.tex":
        "f2f7d51db7eb2ebe8c7bb266d150a3a0d4f7f8bf1c0edcf9020cccc70973e394",
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
}

REQUIRED_ARTIFACTS = [
    "source_dynamics_milestone_synthesis_v1.tex",
    "source_dynamics_theorem_inventory_v1.yaml",
    "source_ontology_distance_status_decision_v1.yaml",
    "p6_geometry_input_contract_v1.yaml",
    "parent_fusion_notes_source_dynamics_milestone.md",
    "source_dynamics_milestone_receipt.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phi(a: float, lam: float, gamma: float) -> float:
    return a / math.sqrt(1.0 + 2.0 * gamma * lam * a * a)


def dphi(a: float, lam: float, gamma: float) -> float:
    return (1.0 + 2.0 * gamma * lam * a * a) ** -1.5


def close(x: float, y: float, tol: float = 2e-9) -> bool:
    return abs(x - y) <= tol * max(1.0, abs(x), abs(y))


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
        record(f"source_hash::{rel}", actual == expected,
               f"expected={expected} actual={actual}")

    artifact_hashes = {}
    for name in REQUIRED_ARTIFACTS:
        path = ART / name
        present = path.is_file()
        record(f"artifact_present::{name}", present, str(path))
        if present:
            artifact_hashes[str(path.relative_to(ROOT))] = sha256(path)

    samples = [-3.0, -1.1, -0.2, 0.0, 0.4, 1.7, 2.8]
    for gamma in (0.3, 1.0, 2.4):
        for lam in (0.0, 0.05, 0.7, 2.0):
            derivative_ok = True
            for a in samples:
                h = 1e-6
                finite_difference = (phi(a + h, lam, gamma)
                                     - phi(a - h, lam, gamma)) / (2.0 * h)
                derivative_ok = derivative_ok and close(
                    finite_difference, dphi(a, lam, gamma), 2e-7)
            record(f"tangent_response::gamma={gamma}::lambda={lam}",
                   derivative_ok, "centered finite difference")

    cocycle_ok = True
    for gamma in (0.5, 1.8):
        for a in samples:
            for lam in (0.0, 0.2, 1.1):
                for mu in (0.0, 0.4, 1.6):
                    lhs = dphi(a, lam + mu, gamma)
                    rhs = dphi(phi(a, lam, gamma), mu, gamma) * dphi(
                        a, lam, gamma)
                    cocycle_ok = cocycle_ok and close(lhs, rhs)
    record("response_cocycle", cocycle_ok,
           "Dphi_(lambda+mu)=Dphi_mu(phi_lambda)Dphi_lambda")

    rank_bound_ok = True
    for u in ([1.0, 2.0, -0.5], [0.2, -1.4, 3.0]):
        for v in ([2.0, -0.3, 1.1, 0.7], [-1.0, 0.4, 2.2, -0.8]):
            matrix = [[vi * uj for uj in u] for vi in v]
            for i in range(len(v)):
                for k in range(i + 1, len(v)):
                    for j in range(len(u)):
                        for ell in range(j + 1, len(u)):
                            minor = (matrix[i][j] * matrix[k][ell]
                                     - matrix[i][ell] * matrix[k][j])
                            rank_bound_ok = rank_bound_ok and close(minor, 0.0)
    record("factor_through_amplitude_rank_bound", rank_bound_ok,
           "all 2x2 minors of representative outer products vanish")

    inventory = yaml.safe_load(
        (ART / "source_dynamics_theorem_inventory_v1.yaml").read_text())
    record("inventory_status",
           inventory["milestone_disposition"]
           == "completed_with_precise_scoped_obstruction",
           inventory["milestone_disposition"])
    record("inventory_new_theorems",
           inventory["counts"]["new_p5_t08_theorem_count"] == 3,
           str(inventory["counts"]))
    record("inventory_no_positive_geometry",
           inventory["counts"]["positive_local_geometry_input_count"] == 0,
           str(inventory["counts"]))

    decision = yaml.safe_load(
        (ART / "source_ontology_distance_status_decision_v1.yaml").read_text())
    record("decision_adoption_boundary",
           decision["adoption_status"]
           == "blocked_adoption_open_continuation",
           decision["adoption_status"])
    record("decision_input_split",
           (decision["conditional_p6_formalization_input_available"] is True
            and decision["positive_local_geometry_input_available"] is False),
           "conditional=true positive_local=false")
    record("decision_no_global_no_go",
           decision["authority"]["global_no_go_claimed"] is False,
           str(decision["authority"]))

    contract = yaml.safe_load(
        (ART / "p6_geometry_input_contract_v1.yaml").read_text())
    record("p6_contract_qualification",
           (contract["qualification"]["lawful_for_p6_target_formalization"]
            is True
            and contract["qualification"]["positive_local_geometry_input"]
            is False
            and contract["qualification"]["geometry_reconstruction_unlocked"]
            is False),
           str(contract["qualification"]))
    record("p6_contract_no_target_import",
           (contract["authority"]["target_atlas_imported"] is False
            and contract["authority"]["target_metric_imported"] is False),
           str(contract["authority"]))

    tex = (ART / "source_dynamics_milestone_synthesis_v1.tex").read_text()
    for marker in [
        "P5T08-THM-CONDITIONAL-TANGENT-RESPONSE",
        "P5T08-THM-FACTOR-THROUGH-AMPLITUDE-RANK-BOUND",
        "P5T08-THM-SOURCE-DYNAMICS-MILESTONE-CLOSURE",
        "blocked\\_adoption\\_open\\_continuation",
        "not a global no-go theorem",
        "positive local geometry input",
        "mathcal I^{\\mathrm{cond}}_6",
    ]:
        record(f"boundary_marker::{marker}", marker in tex,
               "required manuscript marker")

    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v21_p5_t08_source_dynamics_milestone_validation_receipt_v1",
        "task_id": "RT-20260726-001",
        "job_id": "AJ-RT-20260726-001-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "fixed_source_hash_count": len(SOURCES),
        "new_theorem_level_statement_count": 3,
        "preserved_or_new_scoped_obstruction_count": 4,
        "positive_local_geometry_input_count": 0,
        "conditional_p6_formalization_input_count": 1,
        "artifact_hashes": artifact_hashes,
        "source_hashes": SOURCES,
        "checks": checks,
        "authority_note": (
            "Operational validation only; no theorem truth, ontology or "
            "source-law adoption, positive geometry, proof, publication, "
            "promotion, or completed-derivation authority."
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
