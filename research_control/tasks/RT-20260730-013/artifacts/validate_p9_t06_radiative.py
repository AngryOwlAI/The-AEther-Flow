#!/usr/bin/env python3
"""Deterministic task-local validation for the P9-T06 radiative case."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((ART / name).read_text(encoding="utf-8"))


def mat_vec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def close(left: float, right: float, tol: float = 1.0e-12) -> bool:
    return abs(left - right) <= tol


def reachable(edges: list[list[str]], start: str, target: str) -> bool:
    graph: dict[str, list[str]] = {}
    for left, right in edges:
        graph.setdefault(left, []).append(right)
    frontier = [start]
    seen: set[str] = set()
    while frontier:
        node = frontier.pop()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(graph.get(node, []))
    return False


def run_checks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    record = load_yaml("source_radiative_completion_family_v1.yaml")
    case = load_yaml("p9_t06_radiative_case_v1.yaml")
    matrix = load_yaml("p9_t06_radiative_comparison_matrix_v1.yaml")
    dag = load_yaml("p9_t06_provenance_dag_v1.yaml")
    exposure = load_yaml("p9_t06_target_exposure_ledger_v1.yaml")
    child_math = load_yaml("child_phys_math_p9_t06_radiative.yaml")
    child_phil = load_yaml("child_phys_phil_p9_t06_radiative.yaml")
    conflict = load_yaml("parent_conflict_review_p9_t06_radiative.yaml")
    seal = json.loads((ART / "p9_t06_source_output_seal_v1.json").read_text())
    receipt = json.loads((ART / "p9_t06_radiative_receipt_v1.json").read_text())

    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    check("record_identity", record.get("artifact_id") == "FiniteRadiativeCompletionFamily_v1")
    check("case_identity", case.get("case_id") == "P9-BENCH-RADIATIVE-V1")
    check("case_outcome", case.get("execution_status") == "INCONCLUSIVE")
    check("secondary_label", case.get("secondary_label") == "FORMAL_ANALOGY")
    check("zero_benchmark_passes", case["case_classification"]["benchmark_pass_count"] == 0)
    check("zero_target_reruns", exposure["source_stage_exposure"]["target_informed_rerun_count"] == 0)

    laplacian = record["finite_carrier"]["laplacian"]
    check("laplacian_symmetric", all(laplacian[i][j] == laplacian[j][i] for i in range(4) for j in range(4)))
    check("laplacian_row_sums", all(sum(row) == 0 for row in laplacian))

    basis = record["finite_carrier"]["eigenbasis"]
    for item in basis:
        vec = item["coordinates"]
        lam = item["eigenvalue"]
        residual = [a - lam * b for a, b in zip(mat_vec(laplacian, vec), vec)]
        check(f"eigenpair_{item['id']}", max(abs(value) for value in residual) < 1.0e-12)
    check("basis_orthonormal", all(close(dot(a["coordinates"], b["coordinates"]), 1.0 if a is b else 0.0) for a in basis for b in basis))
    check("quotient_dimension", record["finite_carrier"]["quotient_dimension"] == 3)
    check("quotient_spectrum", [item["eigenvalue"] for item in basis if item["quotient_mode"]] == [2, 2, 4])

    fixtures = {item["id"]: item for item in record["fixtures"]}
    check("two_completion_fixtures", set(fixtures) == {"completion_A", "completion_B"})
    check("same_static_equation", record["completion_family"]["stationary_equation"] == "L_C q = 0")
    check("positive_kinetic_fixtures", all(item["m"] > 0 for item in fixtures.values()))
    check("distinct_completion_parameters", (fixtures["completion_A"]["m"], fixtures["completion_A"]["gamma"]) != (fixtures["completion_B"]["m"], fixtures["completion_B"]["gamma"]))

    response = record["exact_response_fixture"]
    check("completion_A_v1_response", close(response["completion_A"]["v1_coefficient"], math.cos(math.sqrt(2))))
    check("completion_A_v3_response", close(response["completion_A"]["v3_coefficient"], math.cos(2)))
    omega2 = math.sqrt(7) / 4
    omega4 = math.sqrt(15) / 4
    response_b2 = math.exp(-0.25) * (math.cos(omega2) + 0.25 / omega2 * math.sin(omega2))
    response_b4 = math.exp(-0.25) * (math.cos(omega4) + 0.25 / omega4 * math.sin(omega4))
    check("completion_B_v1_response", close(response["completion_B"]["v1_coefficient"], response_b2))
    check("completion_B_v3_response", close(response["completion_B"]["v3_coefficient"], response_b4))
    check("completion_responses_disagree", not close(response["completion_A"]["v1_coefficient"], response["completion_B"]["v1_coefficient"]))

    ranks = [item["rank"] for item in record["radiative_projector_family"]]
    check("projector_rank_counterfamily", ranks == [2, 3])
    check("projectors_unselected", not any(item["physical_polarization_map"] for item in record["radiative_projector_family"]))
    check("detector_map_unselected", record["detector_readout_family"]["physical_detector_coupling_selected"] is False)

    source_hash_ok = True
    for item in seal["source_files"]:
        source_hash_ok &= sha256(ROOT / item["path"]) == item["sha256"]
    check("source_hash_manifest", source_hash_ok)
    check("source_sealed", seal["status"] == "SEALED" and seal["sealed_before_target_comparison"])

    edges = dag["edges"]
    forbidden = any(
        reachable(edges, "target_radiative_burden", node)
        for node in ("cycle_C4_fixture", "completion_counterfamily", "projector_readout_counterfamily", "source_output_seal")
    )
    check("target_firewall_dag", not forbidden and dag["forbidden_reachability_result"]["status"] == "PASS")
    check("target_opened_after_seal", exposure["comparison_stage"]["opened_after_source_seal"] is True)
    check("no_post_comparison_source_mutation", exposure["comparison_stage"]["source_mutation_after_open_count"] == 0)

    check("comparison_matrix_all_inconclusive", all(row["disposition"] == "INCONCLUSIVE" for row in matrix["rows"]))
    check("internal_children_bounded", child_math["subagent_count"] == 0 and child_phil["subagent_count"] == 0)
    check("parent_conflicts_resolved", conflict["unresolved_conflict_count"] == 0)
    fusion_text = (ART / "parent_fusion_notes_p9_t06_radiative.md").read_text(encoding="utf-8")
    check("fusion_records_obstruction", "OBST-P9T06-RADIATIVE-DYNAMICS-DETECTOR-NONSELECTION-001" in fusion_text)

    artifact_paths = {
        "source_artifact": ART / "finite_radiative_completion_nonselection_v1.tex",
        "source_record": ART / "source_radiative_completion_family_v1.yaml",
        "case": ART / "p9_t06_radiative_case_v1.yaml",
        "comparison_matrix": ART / "p9_t06_radiative_comparison_matrix_v1.yaml",
        "provenance_dag": ART / "p9_t06_provenance_dag_v1.yaml",
        "source_seal": ART / "p9_t06_source_output_seal_v1.json",
        "target_exposure_ledger": ART / "p9_t06_target_exposure_ledger_v1.yaml",
    }
    receipt_hashes_ok = all(receipt["artifact_hashes"][name] == sha256(path) for name, path in artifact_paths.items())
    check("receipt_artifact_hashes", receipt_hashes_ok)
    check("receipt_declares_pass", receipt["status"] == "PASS" and receipt["failed_check_count"] == 0)

    summary = {
        "status": "PASS" if all(item["passed"] for item in checks) else "FAIL",
        "check_count": len(checks),
        "failed_check_count": sum(not item["passed"] for item in checks),
        "failed_checks": [item for item in checks if not item["passed"]],
        "source_hash_check_count": len(seal["source_files"]),
        "benchmark_pass_count": case["case_classification"]["benchmark_pass_count"],
        "target_informed_rerun_count": exposure["source_stage_exposure"]["target_informed_rerun_count"],
        "case_outcome": case["execution_status"],
        "secondary_label": case["secondary_label"],
    }
    check("receipt_check_count", receipt["check_count"] == len(checks) + 1)
    summary["status"] = "PASS" if all(item["passed"] for item in checks) else "FAIL"
    summary["check_count"] = len(checks)
    summary["failed_check_count"] = sum(not item["passed"] for item in checks)
    summary["failed_checks"] = [item for item in checks if not item["passed"]]
    return checks, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    _, summary = run_checks()
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"{summary['status']}: {summary['check_count']} checks, {summary['failed_check_count']} failed")
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
