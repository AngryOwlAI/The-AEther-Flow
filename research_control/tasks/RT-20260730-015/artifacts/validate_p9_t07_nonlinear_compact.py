#!/usr/bin/env python3
"""Deterministic task-local validation for the P9-T07 nonlinear compact case."""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((ART / name).read_text(encoding="utf-8"))


def frac(value: Any) -> Fraction:
    return Fraction(str(value))


def mat_vec(
    matrix: list[list[Fraction]], vector: list[Fraction]
) -> list[Fraction]:
    return [
        sum((entry * component for entry, component in zip(row, vector)), Fraction(0))
        for row in matrix
    ]


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
    record = load_yaml("source_nonlinear_compact_control_v1.yaml")
    case = load_yaml("p9_t07_nonlinear_compact_case_v1.yaml")
    matrix = load_yaml("p9_t07_nonlinear_compact_comparison_matrix_v1.yaml")
    dag = load_yaml("p9_t07_provenance_dag_v1.yaml")
    exposure = load_yaml("p9_t07_target_exposure_ledger_v1.yaml")
    child_math = load_yaml("child_phys_math_p9_t07_nonlinear_compact.yaml")
    child_phil = load_yaml("child_phys_phil_p9_t07_nonlinear_compact.yaml")
    conflict = load_yaml("parent_conflict_review_p9_t07_nonlinear_compact.yaml")
    seal = json.loads((ART / "p9_t07_source_output_seal_v1.json").read_text())
    constraint_receipt = json.loads(
        (ART / "p9_t07_constraint_propagation_receipt_v1.json").read_text()
    )
    receipt = json.loads(
        (ART / "p9_t07_nonlinear_compact_receipt_v1.json").read_text()
    )

    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    check(
        "record_identity",
        record.get("artifact_id") == "FiniteNonlinearCompactControl_v1",
    )
    check("case_identity", case.get("case_id") == "P9-BENCH-NONLINEAR-COMPACT-V1")
    check("case_outcome", case.get("execution_status") == "INCONCLUSIVE")
    check("secondary_label", case.get("secondary_label") == "FORMAL_ANALOGY")
    check("zero_benchmark_passes", case["case_classification"]["benchmark_pass_count"] == 0)
    check(
        "zero_target_reruns",
        exposure["source_stage_exposure"]["target_informed_rerun_count"] == 0,
    )

    transition = [
        [frac(value) for value in row]
        for row in record["finite_carrier"]["transition_matrix"]
    ]
    weights = [
        [frac(value) for value in row]
        for row in record["finite_carrier"]["symmetric_edge_weights"]
    ]
    laplacian = [
        [frac(value) for value in row]
        for row in record["finite_carrier"]["laplacian"]
    ]
    identity_minus_transition = [
        [
            Fraction(int(i == j)) - transition[i][j]
            for j in range(3)
        ]
        for i in range(3)
    ]
    check(
        "transition_row_normalization",
        all(sum(row, Fraction(0)) == 1 for row in transition),
    )
    check(
        "transition_and_weights_symmetric",
        all(
            transition[i][j] == transition[j][i]
            and weights[i][j] == weights[j][i]
            for i in range(3)
            for j in range(3)
        ),
    )
    check("laplacian_definition", laplacian == identity_minus_transition)
    check("laplacian_row_sums", all(sum(row, Fraction(0)) == 0 for row in laplacian))

    v1 = [Fraction(2), Fraction(-1), Fraction(-1)]
    v2 = [Fraction(0), Fraction(1), Fraction(-1)]
    check("laplacian_quotient_eigenpair_v1", mat_vec(laplacian, v1) == v1)
    check("laplacian_quotient_eigenpair_v2", mat_vec(laplacian, v2) == v2)

    raw = [frac(value) for value in record["compact_source"]["raw_matter_token"]]
    rho = [frac(value) for value in record["compact_source"]["balanced_source"]]
    expected_rho = mat_vec(laplacian, raw)
    check(
        "compact_raw_support",
        sum(value != 0 for value in raw) == 1
        and record["compact_source"]["raw_support_cardinality"] == 1,
    )
    check("balanced_source", rho == expected_rho == [Fraction(4, 3), Fraction(-2, 3), Fraction(-2, 3)])
    check("balanced_source_sum", sum(rho, Fraction(0)) == 0)

    h = [frac(value) for value in record["exact_solution"]["h_star"]]
    residual = []
    nonlinear_contribution_nonzero = False
    for i in range(3):
        value = Fraction(0)
        for j in range(3):
            if i == j:
                continue
            delta = h[i] - h[j]
            nonlinear_contribution_nonzero |= delta**3 != 0
            value += weights[i][j] * (delta + delta**3)
        residual.append(value - rho[i])
    check("exact_solution_quotient", sum(h, Fraction(0)) == 0)
    check("exact_nonlinear_residual", residual == [0, 0, 0])
    check("nonlinear_term_active", nonlinear_contribution_nonzero)

    hessian = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(i + 1, 3):
            edge_weight = weights[i][j] * (1 + 3 * (h[i] - h[j]) ** 2)
            hessian[i][i] += edge_weight
            hessian[j][j] += edge_weight
            hessian[i][j] -= edge_weight
            hessian[j][i] -= edge_weight
    check(
        "hessian_quotient_eigenpair_v1",
        mat_vec(hessian, v1) == [4 * value for value in v1],
    )
    check(
        "hessian_quotient_eigenpair_v2",
        mat_vec(hessian, v2) == [2 * value for value in v2],
    )
    check(
        "strict_convexity_witness",
        record["exact_solution"]["uniqueness_basis"]
        == "strict convexity on the component-shift quotient",
    )

    sample_h = [Fraction(5, 7), Fraction(-2, 7), Fraction(-3, 7)]
    flux = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    sample_residual = []
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            delta = sample_h[i] - sample_h[j]
            flux[i][j] = weights[i][j] * (delta + delta**3)
        sample_residual.append(sum(flux[i], Fraction(0)) - rho[i])
    check(
        "edge_flux_antisymmetry",
        all(flux[i][j] == -flux[j][i] for i in range(3) for j in range(3)),
    )
    check("off_shell_total_residual_sum", sum(sample_residual, Fraction(0)) == 0)
    check("finite_cut_identity", record["conservation"]["cut_identity_exact"] is True)

    getcontext().prec = 80
    d = Decimal(0)
    step = Decimal(1) / Decimal(20)
    monotone = True
    for _ in range(200):
        next_d = d + step * (Decimal(2) - d - d**3)
        monotone &= d <= next_d <= Decimal(1)
        d = next_d
    check(
        "relaxation_constraint_propagation",
        record["constraint_propagation"]["zero_sum_derivative"] == "0",
    )
    check(
        "relaxation_lyapunov_identity",
        record["constraint_propagation"]["lyapunov_identity"]
        == "dS_NL/dlambda=-||E||^2",
    )
    check("explicit_euler_monotone", monotone)
    check("explicit_euler_error_bound", abs(Decimal(1) - d) < Decimal("1.3e-19"))

    source_hash_ok = True
    for item in seal["source_files"]:
        source_hash_ok &= sha256(ROOT / item["path"]) == item["sha256"]
    check("source_hash_manifest", source_hash_ok)
    check("source_sealed", seal["status"] == "SEALED" and seal["sealed_before_target_comparison"])

    forbidden_nodes = (
        "triangle_uniform_fixture",
        "compact_raw_token",
        "quartic_edge_action",
        "exact_nonlinear_solution",
        "conservation_constraint_receipt",
        "source_output_seal",
    )
    forbidden = any(
        reachable(dag["edges"], "target_compact_source_burden", node)
        for node in forbidden_nodes
    )
    check(
        "target_firewall_dag",
        not forbidden and dag["forbidden_reachability_result"]["status"] == "PASS",
    )
    check(
        "target_opened_after_seal",
        exposure["comparison_stage"]["opened_after_source_seal"] is True,
    )
    check(
        "no_post_comparison_source_mutation",
        exposure["comparison_stage"]["source_mutation_after_open_count"] == 0,
    )

    check(
        "comparison_matrix_all_inconclusive",
        all(row["disposition"] == "INCONCLUSIVE" for row in matrix["rows"]),
    )
    check(
        "internal_children_bounded",
        child_math["subagent_count"] == 0 and child_phil["subagent_count"] == 0,
    )
    check("parent_conflicts_resolved", conflict["unresolved_conflict_count"] == 0)
    fusion_text = (
        ART / "parent_fusion_notes_p9_t07_nonlinear_compact.md"
    ).read_text(encoding="utf-8")
    check(
        "fusion_records_obstruction",
        "OBST-P9T07-NONLINEAR-COMPACT-SOURCE-MODEL-TO-WORLD-NONSELECTION-001"
        in fusion_text,
    )
    check(
        "constraint_receipt_exact",
        constraint_receipt["status"] == "PASS"
        and constraint_receipt["exact_euler_residual"] == ["0", "0", "0"]
        and constraint_receipt["constraint_residual_bound"] == "0",
    )
    check(
        "cumulative_case_accounting",
        case["case_classification"]["cumulative_executed_case_count"] == 6
        and case["case_classification"]["cumulative_inconclusive_case_count"] == 6,
    )

    artifact_paths = {
        "source_artifact": ART / "finite_nonlinear_compact_source_nonselection_v1.tex",
        "source_record": ART / "source_nonlinear_compact_control_v1.yaml",
        "case": ART / "p9_t07_nonlinear_compact_case_v1.yaml",
        "comparison_matrix": ART / "p9_t07_nonlinear_compact_comparison_matrix_v1.yaml",
        "provenance_dag": ART / "p9_t07_provenance_dag_v1.yaml",
        "source_seal": ART / "p9_t07_source_output_seal_v1.json",
        "target_exposure_ledger": ART / "p9_t07_target_exposure_ledger_v1.yaml",
        "constraint_propagation_receipt": ART / "p9_t07_constraint_propagation_receipt_v1.json",
    }
    receipt_hashes_ok = all(
        receipt["artifact_hashes"][name] == sha256(path)
        for name, path in artifact_paths.items()
    )
    check("receipt_artifact_hashes", receipt_hashes_ok)
    check(
        "receipt_declares_pass",
        receipt["status"] == "PASS" and receipt["failed_check_count"] == 0,
    )
    check("receipt_check_count", receipt["check_count"] == len(checks) + 1)

    summary = {
        "status": "PASS" if all(item["passed"] for item in checks) else "FAIL",
        "check_count": len(checks),
        "failed_check_count": sum(not item["passed"] for item in checks),
        "failed_checks": [item for item in checks if not item["passed"]],
        "source_hash_check_count": len(seal["source_files"]),
        "benchmark_pass_count": case["case_classification"]["benchmark_pass_count"],
        "target_informed_rerun_count": exposure["source_stage_exposure"][
            "target_informed_rerun_count"
        ],
        "case_outcome": case["execution_status"],
        "secondary_label": case["secondary_label"],
        "explicit_euler_final_d": str(d),
    }
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
        print(
            f"{summary['status']}: {summary['check_count']} checks, "
            f"{summary['failed_check_count']} failed"
        )
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
