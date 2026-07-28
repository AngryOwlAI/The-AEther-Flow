#!/usr/bin/env python3
"""Deterministic support checker for the P7-T07 matter-package audit.

The checker validates fixed source hashes, exact finite counterexamples,
artifact markers, and the bounded semantic-suite receipt. PASS is operational
evidence only and is not proof, ontology, Gate C, or promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260728-006"
ART = TASK / "artifacts"
REPORT = ART / "matter_package_audit_validation_v1.json"

SOURCES = {
    "research_control/tasks/RT-20260727-007/artifacts/source_matter_ontology_and_sector_taxonomy_v1.tex":
        "8d160217bf223078a11bc63fde6593c11c39d5b50d9c48fbad7b12084f8a752d",
    "research_control/tasks/RT-20260728-001/artifacts/source_matter_finite_transition_kernel_candidate_v1.tex":
        "65ac095f5cdf4c2e319365c8b0e024d031b19d9fc2b8102e59997afa1e8f9129",
    "research_control/tasks/RT-20260728-002/artifacts/source_operational_device_suite_candidate_v1.tex":
        "d6c818ee29f1a7e659e2f454aec21431d680b3d2d4df048fcf36f4aba87ba22a",
    "research_control/tasks/RT-20260728-003/artifacts/common_source_propagation_profile_candidate_v1.tex":
        "87014253023cdb8945ed67f606355d762486884ce3a6de4fa2d32e2af32e2b43",
    "research_control/tasks/RT-20260728-004/artifacts/universal_source_coupling_map_candidate_v1.tex":
        "5a9a8f5542a7c8b714bbff7ec06c06449b0c66c0196266051562caf9ce602c6b",
    "research_control/tasks/RT-20260728-005/artifacts/source_kernel_variational_object_candidate_v1.tex":
        "386769e40167c35604625ef7250c027dc1712c82db4790e2895e0b31ac3cfbf7",
}

POLICY_SOURCES = {
    "research_control/tasks/RT-20260614-257/artifacts/286_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_MATTER_COUPLING_BRIDGE_TARGET_V1_FORMALIZATION.tex":
        "3d1c6dfb2ea543c8ea455ee2f3553e3cac76e3072902213ed07aff0db514605e",
    "research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex":
        "2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986",
    "research_control/tasks/RT-20260722-006/artifacts/semantic_smuggling_validation.json":
        "2e81deb36fe1750ed8c9c362c29228ded29930e74cf25000a8a39176d1d5d12c",
    "research_control/tasks/RT-20260722-006/artifacts/semantic_smuggling_compact_receipt.json":
        "6c5f956eb538a88fe3ff25f831dec4494a6220fdf757f7a7b22135e18709adb7",
    "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_operational_meaning_gate_policy.md":
        "7d679cbcbc05bf771333ba7d3afddb351159b87d0edd92e720942428389b62c6",
}

REQUIRED_ARTIFACTS = [
    "matter_package_smuggling_audit_v1.tex",
    "refuter_stress_matter_package_v1.yaml",
    "gate_c_readiness_matrix_v1.yaml",
    "child_phys_math_p7_t07_matter_package_audit.yaml",
    "child_phys_phil_p7_t07_matter_package_audit.yaml",
    "parent_conflict_review_p7_t07_matter_package_audit.yaml",
    "parent_fusion_notes_p7_t07_matter_package_audit.md",
    "matter_package_audit_compact_receipt_v1.json",
    "matter_package_audit_receipt.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mat_transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*matrix)]


def run_checks() -> dict:
    checks: list[dict[str, str]] = []

    def record(check_id: str, passed: bool, detail: str) -> None:
        checks.append({
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        })

    for rel, expected in {**SOURCES, **POLICY_SOURCES}.items():
        path = ROOT / rel
        actual = sha256(path) if path.is_file() else ""
        record(f"source_hash::{rel}", actual == expected, f"expected={expected} actual={actual}")

    artifact_hashes: dict[str, str] = {}
    for name in REQUIRED_ARTIFACTS:
        path = ART / name
        present = path.is_file()
        record(f"artifact_present::{name}", present, str(path))
        if present:
            artifact_hashes[str(path.relative_to(ROOT))] = sha256(path)

    clock = [[1, 1], [1, 1]]
    freefall = [[1, 1], [0, 1]]
    signal = [[1, 1, 0], [0, 1, 1], [0, 0, 1]]
    record("clock_signal_cardinality_mismatch", len(clock) != len(signal), "2 versus 3 vertices")
    record(
        "clock_freefall_reduced_edge_mismatch",
        sum(clock[i][j] for i in range(2) for j in range(2) if i != j)
        != sum(freefall[i][j] for i in range(2) for j in range(2) if i != j),
        "clock has two reduced directed edges; baseline FreeFall has one",
    )
    record(
        "clock_cycle_freefall_acyclic",
        clock[0][1] == clock[1][0] == 1 and freefall[0][1] == 1 and freefall[1][0] == 0,
        "directed two-cycle invariant differs",
    )

    identity_edges = {(0, 0), (1, 1)}
    forward_edges = identity_edges | {(0, 1)}
    record(
        "same_sector_support_edge_nonselection",
        len(identity_edges) == 2 and len(forward_edges) == 3,
        "same two-state sector controls have two versus three support edges",
    )

    p_forward = [
        [Fraction(1, 2), Fraction(1, 2)],
        [Fraction(0), Fraction(1)],
    ]
    p_transpose = mat_transpose(p_forward)
    residual = [
        [Fraction(int(i == j)) - p_forward[i][j] for j in range(2)]
        for i in range(2)
    ]
    record("directional_residual_nonsymmetric", residual != mat_transpose(residual), str(residual))
    conductance = [
        [(p_forward[i][j] + p_transpose[i][j]) / 2 for j in range(2)]
        for i in range(2)
    ]
    record("symmetric_conductance", conductance == mat_transpose(conductance), str(conductance))
    laplacian = [
        [Fraction(1, 4), Fraction(-1, 4)],
        [Fraction(-1, 4), Fraction(1, 4)],
    ]
    record(
        "finite_laplacian_zero_row_sum",
        all(sum(row) == 0 for row in laplacian),
        "finite algebraic balance identity only",
    )

    semantic_report = json.loads(
        (ROOT / "research_control/tasks/RT-20260722-006/artifacts/semantic_smuggling_validation.json")
        .read_text(encoding="utf-8")
    )
    record("semantic_suite_status", semantic_report.get("status") == "PASS", "bounded suite report")
    record("semantic_suite_fixture_count", semantic_report.get("fixture_count") == 19, "expected 19 fixtures")
    record(
        "semantic_suite_zero_probe_errors",
        semantic_report.get("semantic_metrics", {}).get("false_negative") == 0
        and semantic_report.get("semantic_metrics", {}).get("false_positive") == 0,
        str(semantic_report.get("semantic_metrics")),
    )

    gate_text = (ART / "gate_c_readiness_matrix_v1.yaml").read_text(encoding="utf-8")
    required_gate_markers = [
        'status: "proposed"',
        'status: "multiple_unresolved"',
        'status: "conditional"',
        'status: "specified"',
        'status: "same_context_role_review"',
        'outcome: "blocked"',
        "review_executed: true",
        "physics_promotion_authorized: false",
    ]
    for marker in required_gate_markers:
        record(f"gate_marker::{marker}", marker in gate_text, "required Gate C marker")

    tex = (ART / "matter_package_smuggling_audit_v1.tex").read_text(encoding="utf-8")
    required_tex_markers = [
        "OBST-P7T07-CROSS-LAYER-COMPOSITION-GAP-001",
        "P7T07-THM-TYPED-INTERFACE-CUTSET-001",
        "P7T07-PROP-COMPONENTWISE-BALANCE-COMPATIBILITY-001",
        "blocked\\_gate\\_c\\_readiness",
        "not a global no-go",
        "Materially new conservative source-side extensions remain open",
        "not positive source provenance",
        "Clock--signal agreement",
        "validator or checkpoint PASS",
    ]
    for marker in required_tex_markers:
        record(f"boundary_marker::{marker}", marker in tex, "required audit marker")

    stress_text = (ART / "refuter_stress_matter_package_v1.yaml").read_text(encoding="utf-8")
    for marker in [
        "ready_gate_c_dimension_count: 0",
        "required_gate_c_dimension_count: 7",
        "ready_plan_criterion_count: 0",
        "required_plan_criterion_count: 10",
    ]:
        record(f"stress_gate_marker::{marker}", marker in stress_text, "required plan Gate C count")
    for stress_id in [
        "P7T07-STRESS-SECTOR-DELETION",
        "P7T07-STRESS-PRESENTATION-RELABEL",
        "P7T07-STRESS-FIELD-REDEFINITION",
        "P7T07-STRESS-INTERACTION-CHANGE",
        "P7T07-STRESS-FINITE-VARIATION",
        "P7T07-STRESS-ANOMALY",
        "P7T07-STRESS-CLOCK-SIGNAL-AGREEMENT",
        "P7T07-STRESS-FULL-SUITE-UNIVERSALITY",
        "P7T07-STRESS-EQUIVALENCE-PRINCIPLE",
        "P7T07-STRESS-PROCESS-AUTHORITY",
    ]:
        record(f"stress_present::{stress_id}", stress_id in stress_text, "required stress case")
    record(
        "componentwise_balance_refinement",
        "zero sum on every connected component" in tex
        and "componentwise_algebraic_compatibility" in stress_text,
        "global zero sum is insufficient on disconnected support",
    )

    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "p7_t07_matter_package_audit_validation_v1",
        "task_id": "RT-20260728-006",
        "job_id": "AJ-RT-20260728-006-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "source_hashes": SOURCES,
        "policy_source_hashes": POLICY_SOURCES,
        "artifact_hashes": artifact_hashes,
        "semantic_suite": {
            "fixture_count": semantic_report.get("fixture_count"),
            "attack_fixture_count": semantic_report.get("attack_fixture_count"),
            "benign_fixture_count": semantic_report.get("benign_fixture_count"),
            "semantic_metrics": semantic_report.get("semantic_metrics"),
        },
        "checks": checks,
        "authority_note": "Operational validation only; no theorem truth, ontology, source-law, Gate C verdict, physics promotion, proof, publication, push, or completed-derivation authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = run_checks()
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not (args.write_report or args.check):
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
