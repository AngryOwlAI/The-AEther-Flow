#!/usr/bin/env python3
"""Validate the bounded P9-T02 source-only vacuum/Minkowski case."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260730-008"
ART = TASK / "artifacts"
CASE_PATH = ART / "p9_t02_vacuum_minkowski_case_v1.yaml"
DAG_PATH = ART / "p9_t02_provenance_dag_v1.yaml"
SEAL_PATH = ART / "p9_t02_source_output_seal_v1.json"
EXPOSURE_PATH = ART / "p9_t02_target_exposure_ledger_v1.yaml"
RECEIPT_PATH = ART / "p9_t02_benchmark_case_receipt_v1.json"
TEX_PATH = ART / "finite_source_null_background_benchmark_attempt_v1.tex"
MATH_CHILD = ART / "child_phys_math_p9_t02_vacuum_minkowski_case.yaml"
PHIL_CHILD = ART / "child_phys_phil_p9_t02_vacuum_minkowski_case.yaml"
CONFLICT_PATH = ART / "parent_conflict_review_p9_t02_vacuum_minkowski_case.yaml"
FUSION_PATH = ART / "parent_fusion_notes_p9_t02_vacuum_minkowski_case.md"
REPORT_PATH = ART / "p9_t02_benchmark_case_validation_v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


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


def matmul(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((a * b for a, b in zip(row, vector)), Fraction(0)) for row in matrix]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail}
        )

    required = [
        CASE_PATH,
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
    dag = load_yaml(DAG_PATH)
    seal = load_json(SEAL_PATH)
    exposure = load_yaml(EXPOSURE_PATH)
    receipt = load_json(RECEIPT_PATH)
    math_child = load_yaml(MATH_CHILD)
    phil_child = load_yaml(PHIL_CHILD)
    conflicts = load_yaml(CONFLICT_PATH)

    check("case:id", case.get("case_id") == "P9-BENCH-VACUUM-MINKOWSKI-V1", "exact case")
    check("case:plan", case.get("downstream_plan_task_id") == "P9-T02", "exact plan item")
    check("case:status", case.get("execution_status") == "INCONCLUSIVE", "honest outcome")
    check("case:source_executed", case.get("source_execution_status") == "COMPLETED", "source ran")
    check("case:comparison_not_opened", case.get("target_comparison_status") == "NOT_OPENED", "oracle closed")
    check("case:constructor_result", case.get("candidate_constructor_result") == "constructed_candidate", "one decisive construction")

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
        "all protocol-required case fields are instantiated",
    )
    check("case:imported_assumptions_empty", case.get("imported_assumptions") == [], "no target imports")

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

    P = [[Fraction(1, 2), Fraction(1, 2)], [Fraction(0), Fraction(1)]]
    C = [[(P[i][j] + P[j][i]) / 2 for j in range(2)] for i in range(2)]
    L = [[Fraction(1, 4), Fraction(-1, 4)], [Fraction(-1, 4), Fraction(1, 4)]]
    u0 = [Fraction(1), Fraction(1)]
    delta_u = [Fraction(3), Fraction(-3)]
    check("math:C", C == [[Fraction(1, 2), Fraction(1, 4)], [Fraction(1, 4), Fraction(1)]], str(C))
    check("math:L_symmetric", L[0][1] == L[1][0], "L_C symmetric")
    check("math:L_rows_zero", all(sum(row, Fraction(0)) == 0 for row in L), "constants in kernel")
    check("math:null_response", matmul(L, u0) == [0, 0], str(matmul(L, u0)))
    check("math:perturbation_response", matmul(L, delta_u) == [Fraction(3, 2), Fraction(-3, 2)], str(matmul(L, delta_u)))

    source_output = seal.get("source_output")
    check(
        "seal:output_hash",
        isinstance(source_output, dict) and canonical_hash(source_output) == seal.get("source_output_sha256"),
        str(seal.get("source_output_sha256")),
    )
    check("seal:case", seal.get("case_id") == case.get("case_id"), "case identity sealed")
    check("seal:protocol", seal.get("protocol_version") == "SourceDerivedBenchmarkProtocol_v1", "protocol exact")
    check("seal:target_content_absent", seal.get("target_reference_content_available_before_seal") is False, "target unavailable")
    check("seal:target_hashes_absent", seal.get("target_reference_hashes_in_source_manifest") == [], "no target content hash")
    check("seal:randomness", seal.get("randomness_policy") == "deterministic_exact_rational_no_randomness", "deterministic")
    check("seal:dag_hash", seal.get("provenance_dag_sha256") == sha256(DAG_PATH), "DAG sealed")
    check("case:dag_hash", case.get("provenance_dag", {}).get("sha256") == sha256(DAG_PATH), "case binds DAG")

    dag_nodes = {node["node_id"]: node for node in dag.get("nodes", [])}
    edges = [tuple(edge) for edge in dag.get("edges", [])]
    source_stage = {node_id for node_id, node in dag_nodes.items() if node.get("stage") in {"source_root", "source_stage", "seal"}}
    target_nodes = {node_id for node_id, node in dag_nodes.items() if node.get("stage") == "target_root"}
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in dag_nodes}
    indegree: dict[str, int] = {node_id: 0 for node_id in dag_nodes}
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
    check("dag:acyclic", len(visited) == len(dag_nodes), "finite DAG")
    forbidden_paths = 0
    for root in target_nodes:
        stack = list(adjacency[root])
        seen: set[str] = set()
        while stack:
            node_id = stack.pop()
            if node_id in seen:
                continue
            seen.add(node_id)
            if node_id in source_stage:
                forbidden_paths += 1
            stack.extend(adjacency[node_id])
    check("dag:target_to_source_zero", forbidden_paths == 0, str(forbidden_paths))
    check("dag:oracle_closed", dag.get("target_oracle_opened") is False, "oracle not opened")
    check(
        "dag:firewall",
        dag.get("forbidden_reachability_result", {}).get("firewall_result") == "PASS_SOURCE_STAGE",
        "source-stage firewall passes",
    )

    check("exposure:not_blind", exposure.get("known_before_execution", {}).get("blindness_claimed") is False, "prior target-family knowledge disclosed")
    check("exposure:oracle_closed", exposure.get("oracle_access", {}).get("target_oracle_opened") is False, "oracle closed")
    check("exposure:no_target_files", exposure.get("oracle_access", {}).get("target_reference_files_opened_during_case_source_stage") == [], "zero target files")
    check("exposure:no_rerun", exposure.get("oracle_access", {}).get("target_informed_rerun_count") == 0, "zero target-informed reruns")

    bridge = case.get("model_to_world_map", {})
    check("bridge:missing", bridge.get("status") == "MISSING", "physical bridge absent")
    check("reproduction:missing", case.get("independent_reproduction", {}).get("status") == "NOT_ACQUIRED", "no independent reproduction")
    check("corrections:uncontrolled", case.get("residual_corrections", {}).get("physical_correction_control") == "ABSENT", "physical corrections absent")
    check("tolerance:unset", case.get("numerical_tolerance", {}).get("status") == "UNSET", "no fitted tolerance")

    result = receipt.get("result", {})
    check("receipt:source_case_count", result.get("executed_source_case_count") == 1, "one source stage executed")
    check("receipt:inconclusive_count", result.get("inconclusive_case_count") == 1, "one inconclusive case")
    check("receipt:pass_count", result.get("passed_case_count") == 0, "zero case passes")
    check("receipt:oracle_count", result.get("opened_target_oracle_count") == 0, "zero opened target oracles")
    check("receipt:no_promotion", result.get("benchmark_promotion_authorized") is False, "no promotion")

    check("decomposition:math", math_child.get("status") == "completed", "math perspective complete")
    check("decomposition:phil", phil_child.get("status") == "completed", "philosophy perspective complete")
    check("decomposition:no_subagents_math", math_child.get("subagent_count") == 0, "no subagent")
    check("decomposition:no_subagents_phil", phil_child.get("subagent_count") == 0, "no subagent")
    check("conflicts:resolved", conflicts.get("status") == "resolved", "all conflicts resolved")
    check("conflicts:five", len(conflicts.get("conflicts", [])) == 5, "five explicit conflicts")
    check("conflicts:none_open", conflicts.get("unresolved_conflict_count") == 0, "none unresolved")

    tex = TEX_PATH.read_text(encoding="utf-8")
    for token in (
        "FiniteSourceNullBackgroundBenchmarkAttempt",
        "constructed\\_candidate",
        "INCONCLUSIVE",
        "OBST-P9T02-PHYSICAL-MINKOWSKI-BRIDGE-ABSENT-001",
        "not a physical vacuum",
        "target oracle is not opened",
    ):
        check(f"tex:{token}", token in tex, f"required token {token!r}")

    completion_path = TASK / "jobs/completions/AJC-AJ-RT-20260730-008-001.yaml"
    if completion_path.is_file():
        completion = load_yaml(completion_path)
        cc = completion.get("candidate_constructor_result", {})
        check("completion:constructed", cc.get("result_type") == "constructed_candidate", "decisive result")
        check("completion:no_fog", cc.get("no_fog_check") is True, "no-fog discipline")
        check("completion:case_inconclusive", completion.get("benchmark_case_result", {}).get("outcome") == "INCONCLUSIVE", "case outcome")

    failed = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "p9_t02_benchmark_case_validation_v1",
        "task_id": "RT-20260730-008",
        "case_id": "P9-BENCH-VACUUM-MINKOWSKI-V1",
        "candidate_id": "FiniteSourceNullBackgroundBenchmarkAttempt_v1",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "failure_count": len(failed),
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): sha256(path)
            for path in required
            if path.is_file()
        },
        "checks": checks,
        "authority_limits": {
            "validator_is_physics_proof": False,
            "physical_Minkowski_recovery_established": False,
            "benchmark_pass_established": False,
            "benchmark_promotion_authorized": False,
            "proof_authority": False,
        },
    }
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
