#!/usr/bin/env python3
"""Validate the bounded P9-T03 source-only weak-field/clock case."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260730-010"
ART = TASK / "artifacts"
CASE_PATH = ART / "p9_t03_weak_field_clock_case_v1.yaml"
TABLE_PATH = ART / "p9_t03_parameter_correction_table_v1.yaml"
DAG_PATH = ART / "p9_t03_provenance_dag_v1.yaml"
SEAL_PATH = ART / "p9_t03_source_output_seal_v1.json"
EXPOSURE_PATH = ART / "p9_t03_target_exposure_ledger_v1.yaml"
RECEIPT_PATH = ART / "p9_t03_weak_field_clock_receipt_v1.json"
TEX_PATH = ART / "weak_field_operational_coupling_nonuniqueness_v1.tex"
MATH_CHILD = ART / "child_phys_math_p9_t03_weak_field_clock.yaml"
PHIL_CHILD = ART / "child_phys_phil_p9_t03_weak_field_clock.yaml"
CONFLICT_PATH = ART / "parent_conflict_review_p9_t03_weak_field_clock.yaml"
FUSION_PATH = ART / "parent_fusion_notes_p9_t03_weak_field_clock.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse to an object")
    return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse to an object")
    return data


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((a * b for a, b in zip(row, vector)), Fraction(0)) for row in matrix]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail}
        )

    required = [
        CASE_PATH,
        TABLE_PATH,
        DAG_PATH,
        SEAL_PATH,
        EXPOSURE_PATH,
        RECEIPT_PATH,
        TEX_PATH,
        MATH_CHILD,
        PHIL_CHILD,
        CONFLICT_PATH,
        FUSION_PATH,
    ]
    for path in required:
        check(f"file:{path.name}", path.is_file(), "required task-local artifact exists")

    case = load_yaml(CASE_PATH)
    table = load_yaml(TABLE_PATH)
    dag = load_yaml(DAG_PATH)
    seal = load_json(SEAL_PATH)
    exposure = load_yaml(EXPOSURE_PATH)
    receipt = load_json(RECEIPT_PATH)
    math_child = load_yaml(MATH_CHILD)
    phil_child = load_yaml(PHIL_CHILD)
    conflicts = load_yaml(CONFLICT_PATH)

    check("case:id", case.get("case_id") == "P9-BENCH-WEAK-FIELD-CLOCK-V1", "exact case")
    check("case:plan", case.get("downstream_plan_task_id") == "P9-T03", "exact plan item")
    check("case:status", case.get("execution_status") == "INCONCLUSIVE", "honest outcome")
    check("case:source", case.get("source_execution_status") == "COMPLETED", "source executed")
    check("case:oracle", case.get("target_comparison_status") == "NOT_OPENED", "oracle closed")
    check(
        "case:constructor",
        case.get("candidate_constructor_result") == "precise_obstruction",
        "decisive result",
    )
    check("case:no_imports", case.get("imported_assumptions") == [], "no target imports")
    check(
        "case:secondary",
        case.get("case_classification", {}).get("secondary_label") == "FORMAL_ANALOGY",
        "formal-only interpretation recorded",
    )

    required_case_fields = [
        "case_id",
        "downstream_plan_task_id",
        "benchmark_scope",
        "source_inputs",
        "derived_intermediate_objects",
        "target_observable",
        "imported_assumptions",
        "approximation_order",
        "residual_corrections",
        "analytic_equivalence",
        "numerical_tolerance",
        "success_criteria",
        "failure_criteria",
        "inconclusive_criteria",
        "source_hash_manifest",
        "code_hash_manifest",
        "provenance_dag",
        "source_output_seal",
        "independent_reproduction",
        "model_to_world_map",
        "target_exposure_ledger",
        "execution_status",
    ]
    check(
        "case:required_fields",
        all(field in case for field in required_case_fields),
        "all protocol-required fields instantiated",
    )

    for item in case.get("source_hash_manifest", []):
        path = ROOT / item["path"]
        check(f"source_exists:{item['source_id']}", path.is_file(), item["path"])
        check(
            f"source_hash:{item['source_id']}",
            path.is_file() and sha256(path) == item["sha256"],
            item["sha256"],
        )
    for item in case.get("code_hash_manifest", []):
        path = ROOT / item["path"]
        check(f"code_exists:{item['code_id']}", path.is_file(), item["path"])
        check(
            f"code_hash:{item['code_id']}",
            path.is_file() and sha256(path) == item["sha256"],
            item["sha256"],
        )

    L = [
        [Fraction(1, 4), Fraction(-1, 4), Fraction(0)],
        [Fraction(-1, 4), Fraction(1, 2), Fraction(-1, 4)],
        [Fraction(0), Fraction(-1, 4), Fraction(1, 4)],
    ]
    u = [Fraction(-1), Fraction(0), Fraction(1)]
    check("math:L_symmetric", all(L[i][j] == L[j][i] for i in range(3) for j in range(3)), "symmetric")
    check("math:L_rows_zero", all(sum(row, Fraction(0)) == 0 for row in L), "component shifts in kernel")
    check("math:weak_response", matvec(L, u) == [Fraction(-1, 4), 0, Fraction(1, 4)], str(matvec(L, u)))

    epsilon = Fraction(1, 4)
    records = {
        "A": (Fraction(0), Fraction(0), Fraction(0)),
        "B": (Fraction(1, 8), Fraction(1, 16), Fraction(1, 4)),
    }
    outputs: dict[str, dict[str, Fraction]] = {}
    for record_id, (clock, signal, freefall) in records.items():
        p_plus = Fraction(1, 2) + clock * epsilon
        p_minus = Fraction(1, 2) - clock * epsilon
        s_forward = Fraction(1, 2) + signal * epsilon
        s_reverse = Fraction(1, 2) - signal * epsilon
        q_plus = Fraction(1, 2) + freefall * epsilon
        q_minus = Fraction(1, 2) - freefall * epsilon
        check(f"math:{record_id}:positive", min(p_plus, p_minus, s_forward, s_reverse, q_plus, q_minus) > 0, "strict positivity")
        check(f"math:{record_id}:freefall_normalized", q_plus + q_minus == 1, "normalized")
        outputs[record_id] = {
            "clock_ratio": p_plus * p_plus / (p_minus * p_minus),
            "signal_ratio": s_forward * s_forward / (s_reverse * s_reverse),
            "freefall_contrast": q_plus - q_minus,
        }
    check("math:counterfamily_distinct", outputs["A"] != outputs["B"], str(outputs))
    check("math:A_zero", outputs["A"] == {"clock_ratio": 1, "signal_ratio": 1, "freefall_contrast": 0}, str(outputs["A"]))
    check("math:B_freefall", outputs["B"]["freefall_contrast"] == Fraction(1, 8), str(outputs["B"]))

    check("table:status", table.get("status") == "completed", "parameter table complete")
    check("table:records", len(table.get("explicit_records", [])) == 2, "two explicit records")
    check("table:ppn_unset", table.get("post_newtonian_parameters", {}).get("status") == "NOT_DEFINED", "no false PPN")

    nodes = {node["node_id"]: node for node in dag.get("nodes", [])}
    edges = [tuple(edge) for edge in dag.get("edges", [])]
    indegree = {node_id: 0 for node_id in nodes}
    adjacency = {node_id: [] for node_id in nodes}
    for left, right in edges:
        adjacency[left].append(right)
        indegree[right] += 1
    queue = [node_id for node_id, degree in indegree.items() if degree == 0]
    visited: list[str] = []
    while queue:
        node_id = queue.pop()
        visited.append(node_id)
        for nxt in adjacency[node_id]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    check("dag:acyclic", len(visited) == len(nodes), "finite DAG")
    target_nodes = {node_id for node_id, node in nodes.items() if node.get("stage") == "target_root"}
    source_nodes = {node_id for node_id, node in nodes.items() if node.get("stage") in {"source_root", "source_stage", "seal"}}
    forbidden = 0
    for root in target_nodes:
        stack = list(adjacency[root])
        seen: set[str] = set()
        while stack:
            node_id = stack.pop()
            if node_id in seen:
                continue
            seen.add(node_id)
            if node_id in source_nodes:
                forbidden += 1
            stack.extend(adjacency[node_id])
    check("dag:target_to_source_zero", forbidden == 0, str(forbidden))
    check("dag:oracle_closed", dag.get("target_oracle_opened") is False, "oracle closed")

    check("seal:case", seal.get("case_id") == case.get("case_id"), "case identity sealed")
    check("seal:oracle", seal.get("target_oracle_opened") is False, "target oracle closed")
    check("seal:no_target_formula", seal.get("target_formula_used_as_source_input") is False, "no target formula")
    check("seal:no_target_value", seal.get("target_value_used_as_source_input") is False, "no target value")
    check("seal:no_tuning", seal.get("target_selected_parameter_count") == 0, "no target tuning")
    check("seal:no_rerun", seal.get("target_informed_rerun_count") == 0, "no target rerun")
    check(
        "seal:obstruction",
        seal.get("source_output", {}).get("obstruction_id")
        == "OBST-P9T03-WEAK-FIELD-OPERATIONAL-COUPLING-LAW-ABSENT-001",
        "exact obstruction",
    )

    check("exposure:not_blind", exposure.get("known_before_execution", {}).get("blindness_claimed") is False, "nonblind disclosed")
    check("exposure:oracle_closed", exposure.get("oracle_access", {}).get("target_oracle_opened") is False, "oracle closed")
    check("exposure:no_target_files", exposure.get("oracle_access", {}).get("target_reference_files_opened_for_case_comparison") == [], "zero comparison files")
    check("exposure:no_rerun", exposure.get("oracle_access", {}).get("target_informed_rerun_count") == 0, "zero reruns")

    check("decomposition:math", math_child.get("status") == "completed", "math complete")
    check("decomposition:phil", phil_child.get("status") == "completed", "philosophy complete")
    check("decomposition:no_subagents_math", math_child.get("subagent_count") == 0, "no subagent")
    check("decomposition:no_subagents_phil", phil_child.get("subagent_count") == 0, "no subagent")
    check("conflicts:resolved", conflicts.get("status") == "resolved", "conflicts resolved")
    check("conflicts:none_open", conflicts.get("unresolved_conflict_count") == 0, "none open")

    result = receipt.get("result", {})
    check("receipt:case", receipt.get("case_id") == case.get("case_id"), "case receipt exact")
    check("receipt:outcome", result.get("case_outcome") == "INCONCLUSIVE", "inconclusive")
    check("receipt:obstruction", result.get("candidate_constructor_result") == "precise_obstruction", "obstruction")
    check("receipt:passes", result.get("passed_case_count") == 0, "zero passes")
    check("receipt:no_promotion", result.get("benchmark_promotion_authorized") is False, "no promotion")

    tex = TEX_PATH.read_text(encoding="utf-8")
    for token in (
        "OBST-P9T03-WEAK-FIELD-OPERATIONAL-COUPLING-LAW-ABSENT-001",
        "precise\\_obstruction",
        "INCONCLUSIVE",
        "FORMAL\\_ANALOGY",
        "current-source nonselection result",
        "target oracle is not opened",
    ):
        check(f"tex:{token}", token in tex, f"required token {token!r}")

    completion_path = TASK / "jobs/completions/AJC-AJ-RT-20260730-010-001.yaml"
    if completion_path.is_file():
        completion = load_yaml(completion_path)
        cc = completion.get("candidate_constructor_result", {})
        check("completion:precise", cc.get("result_type") == "precise_obstruction", "decisive result")
        check("completion:no_fog", cc.get("no_fog_check") is True, "no fog")
        check("completion:outcome", completion.get("benchmark_case_result", {}).get("outcome") == "INCONCLUSIVE", "case outcome")

    failed = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "p9_t03_weak_field_clock_validation_v1",
        "task_id": "RT-20260730-010",
        "case_id": "P9-BENCH-WEAK-FIELD-CLOCK-V1",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "failure_count": len(failed),
        "checks": checks,
        "authority_limits": {
            "validator_is_physics_proof": False,
            "physical_weak_field_recovery_established": False,
            "benchmark_pass_established": False,
            "benchmark_promotion_authorized": False,
            "physics_promotion_authorized": False,
        },
    }
    print(json.dumps(report, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
