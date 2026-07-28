#!/usr/bin/env python3
"""Deterministic support-only validation for the P7-T04 draft/control packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent
SPEC_PATH = ARTIFACTS / "common_source_propagation_spec_v1.yaml"
CONTROLS_PATH = ARTIFACTS / "common_source_propagation_controls_v1.yaml"
ASSUMPTIONS_PATH = ARTIFACTS / "common_source_propagation_assumption_dependency_table_v1.yaml"
TEX_PATH = ARTIFACTS / "common_source_propagation_profile_candidate_v1.tex"
CHILD_MATH_PATH = ARTIFACTS / "child_phys_math_p7_t04_common_propagation.yaml"
CHILD_PHIL_PATH = ARTIFACTS / "child_phys_phil_p7_t04_common_propagation.yaml"
CONFLICT_PATH = ARTIFACTS / "parent_conflict_review_p7_t04_common_propagation.yaml"
FUSION_PATH = ARTIFACTS / "parent_fusion_notes_p7_t04_common_propagation.md"
REPORT_PATH = ARTIFACTS / "common_source_propagation_validation_v1.json"
COMPACT_PATH = ARTIFACTS / "common_source_propagation_compact_receipt_v1.json"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def boolean_product(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    n = len(left)
    return [
        [int(any(left[i][k] and right[k][j] for k in range(n))) for j in range(n)]
        for i in range(n)
    ]


def scc_count(matrix: list[list[int]]) -> int:
    n = len(matrix)
    seen: set[int] = set()
    order: list[int] = []

    def visit(v: int) -> None:
        seen.add(v)
        for w, edge in enumerate(matrix[v]):
            if edge and w not in seen:
                visit(w)
        order.append(v)

    for vertex in range(n):
        if vertex not in seen:
            visit(vertex)

    transpose = [[matrix[j][i] for j in range(n)] for i in range(n)]
    seen.clear()
    count = 0

    def reverse_visit(v: int) -> None:
        seen.add(v)
        for w, edge in enumerate(transpose[v]):
            if edge and w not in seen:
                reverse_visit(w)

    for vertex in reversed(order):
        if vertex not in seen:
            count += 1
            reverse_visit(vertex)
    return count


def reduced_cycle(matrix: list[list[int]]) -> bool:
    n = len(matrix)
    state = [0] * n

    def visit(v: int) -> bool:
        state[v] = 1
        for w, edge in enumerate(matrix[v]):
            if not edge or v == w:
                continue
            if state[w] == 1 or (state[w] == 0 and visit(w)):
                return True
        state[v] = 2
        return False

    return any(state[v] == 0 and visit(v) for v in range(n))


def reachability_diameter(matrix: list[list[int]]) -> int:
    n = len(matrix)
    maximum = 0
    for source in range(n):
        distance = [-1] * n
        distance[source] = 0
        queue: deque[int] = deque([source])
        while queue:
            v = queue.popleft()
            for w, edge in enumerate(matrix[v]):
                if edge and distance[w] < 0:
                    distance[w] = distance[v] + 1
                    queue.append(w)
        maximum = max(maximum, *(d for d in distance if d >= 0))
    return maximum


def reduced_edge_count(matrix: list[list[int]]) -> int:
    return sum(edge for i, row in enumerate(matrix) for j, edge in enumerate(row) if i != j)


def profile(matrix: list[list[int]]) -> list[Any]:
    return [
        len(matrix),
        reduced_edge_count(matrix),
        scc_count(matrix),
        reduced_cycle(matrix),
        reachability_diameter(matrix),
    ]


def permutation_equivalent(left: list[list[int]], right: list[list[int]]) -> bool:
    if len(left) != len(right):
        return False
    if len(left) == 2:
        permutations = [(0, 1), (1, 0)]
    elif len(left) == 3:
        permutations = [
            (0, 1, 2), (0, 2, 1), (1, 0, 2),
            (1, 2, 0), (2, 0, 1), (2, 1, 0),
        ]
    else:
        permutations = [tuple(range(len(left)))]
    for perm in permutations:
        transported = [[left[perm[i]][perm[j]] for j in range(len(left))] for i in range(len(left))]
        if transported == right:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    required = [
        SPEC_PATH, CONTROLS_PATH, ASSUMPTIONS_PATH, TEX_PATH,
        CHILD_MATH_PATH, CHILD_PHIL_PATH, CONFLICT_PATH, FUSION_PATH,
    ]
    for path in required:
        check(f"exists:{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    spec = load_yaml(SPEC_PATH)
    controls = load_yaml(CONTROLS_PATH)
    assumptions = load_yaml(ASSUMPTIONS_PATH)
    tex = TEX_PATH.read_text(encoding="utf-8")

    check("spec_schema", spec.get("schema_id") == "common_source_propagation_spec_v1", "spec schema")
    check("task_id", spec.get("task_id") == "RT-20260728-003", "task identity")
    check("job_id", spec.get("job_id") == "AJ-RT-20260728-003-001", "job identity")
    check("plan_task_id", spec.get("plan_task_id") == "P7-T04", "plan identity")
    check("proposal_only", spec.get("candidate_status") == "proposal-only", "candidate status")
    check("adoption_blocked", spec.get("adoption_status") == "blocked_adoption_open_continuation", "adoption status")
    check(
        "obstruction_id",
        spec.get("obstruction_id") == "OBST-P7T04-FULL-SUITE-COMMON-PROPAGATION-001",
        "precise obstruction identity",
    )

    protocols = spec.get("protocol_profiles", {})
    expected_profiles = {
        "clock": [2, 2, 1, True, 1],
        "rod": [3, 2, 3, False, 2],
        "signal": [3, 2, 3, False, 2],
        "detector": [3, 2, 3, False, 2],
        "freefall_baseline": [2, 1, 2, False, 1],
        "freefall_blocked": [2, 0, 2, False, 0],
    }
    matrices: dict[str, list[list[int]]] = {}
    for name, expected in expected_profiles.items():
        record = protocols.get(name, {})
        matrix = record.get("adjacency", [])
        matrices[name] = matrix
        check(f"matrix_square:{name}", bool(matrix) and all(len(row) == len(matrix) for row in matrix), name)
        check(f"profile:{name}", profile(matrix) == expected, f"{profile(matrix)} == {expected}")

    chain2 = boolean_product(matrices["signal"], matrices["signal"])
    check("chain_one_step_0_to_2", matrices["signal"][0][2] == 0, "no direct 0-to-2 edge")
    check("chain_two_step_0_to_2", chain2[0][2] == 1, "two-step Boolean reachability")
    check("rod_signal_equal", matrices["rod"] == matrices["signal"], "declared b_RS intertwines")
    check("signal_detector_equal", matrices["signal"] == matrices["detector"], "P7-T03 b_SD intertwines")
    check(
        "clock_freefall_nonisomorphic",
        not permutation_equivalent(matrices["clock"], matrices["freefall_baseline"]),
        "equal-cardinality minimal countermodel",
    )
    check(
        "clock_freefall_scc_difference",
        scc_count(matrices["clock"]) == 1 and scc_count(matrices["freefall_baseline"]) == 2,
        "SCC invariant differs",
    )
    check(
        "clock_freefall_cycle_difference",
        reduced_cycle(matrices["clock"]) and not reduced_cycle(matrices["freefall_baseline"]),
        "directed-cycle invariant differs",
    )
    check(
        "freefall_intervention_changes_relation",
        matrices["freefall_baseline"] != matrices["freefall_blocked"],
        "baseline and blocked relations differ",
    )

    universality = spec.get("universality_claim", {})
    check("universality_precisely_obstructed", universality.get("status") == "precisely obstructed for the current explicit suite", "scoped result")
    check("no_global_no_go", universality.get("global_no_go_claimed") is False, "global no-go false")
    check("future_extension_open", universality.get("future_source_extension_impossibility_claimed") is False, "future extension remains open")

    boundary = spec.get("principal_symbol_boundary", {})
    for key in [
        "principal_symbol_computed",
        "characteristic_set_computed",
        "cone_or_metric_derived",
        "energy_or_scale_regime_supplied",
        "finite_matrix_spectrum_is_physical_dispersion",
    ]:
        check(f"boundary_false:{key}", boundary.get(key) is False, key)

    required_tex = [
        "P7T04-FULL-SUITE-COMMON-PROPAGATION-001",
        "Boolean support transport",
        "Common three-address source skeleton",
        "Why no principal symbol, cone, or metric follows",
        "blocked\\_adoption\\_open\\_continuation",
        "future source extension",
    ]
    for token in required_tex:
        check(f"tex_token:{token[:28]}", token in tex, token)

    control_records = controls.get("controls", [])
    control_ids = {str(item.get("control_id", "")) for item in control_records if isinstance(item, dict)}
    for control_id in [
        "P7T04-CTRL-CHAIN-BOOLEAN-REACHABILITY-001",
        "P7T04-CTRL-CLOCK-FREEFALL-MINIMAL-COUNTERMODEL-001",
        "P7T04-CTRL-MATRIX-SPECTRUM-SMUGGLING-001",
        "P7T04-CTRL-LOW-ENERGY-UNDERDETERMINED-001",
        "P7T04-CTRL-FUTURE-EXTENSION-OPEN-001",
    ]:
        check(f"control:{control_id}", control_id in control_ids, control_id)

    result_ids = {
        str(item.get("result_id", ""))
        for item in assumptions.get("results", [])
        if isinstance(item, dict)
    }
    for result_id in ["P7T04-R01", "P7T04-R02", "P7T04-R03", "P7T04-R04", "P7T04-R05"]:
        check(f"assumption_result:{result_id}", result_id in result_ids, result_id)

    if CHILD_MATH_PATH.is_file():
        child_math = load_yaml(CHILD_MATH_PATH)
        check("child_math_identity", child_math.get("execution_unit_id") == "child_phys_math", "physicist-mathematician child")
        check("child_math_completed", child_math.get("status") == "completed", "child status")
    if CHILD_PHIL_PATH.is_file():
        child_phil = load_yaml(CHILD_PHIL_PATH)
        check("child_phil_identity", child_phil.get("execution_unit_id") == "child_phys_phil", "physicist-philosopher child")
        check("child_phil_completed", child_phil.get("status") == "completed", "child status")
    if CONFLICT_PATH.is_file():
        conflict = load_yaml(CONFLICT_PATH)
        check("conflict_resolved", conflict.get("verdict") in {"resolved", "no_conflict"}, "parent conflict verdict")
        check("no_unresolved_conflicts", conflict.get("unresolved_conflicts") in ([], None), "no unresolved conflicts")

    failed = [item for item in checks if item["status"] != "PASS"]
    source_paths = [SPEC_PATH, CONTROLS_PATH, ASSUMPTIONS_PATH, TEX_PATH]
    for optional in [CHILD_MATH_PATH, CHILD_PHIL_PATH, CONFLICT_PATH, FUSION_PATH]:
        if optional.is_file():
            source_paths.append(optional)
    report = {
        "schema_id": "common_source_propagation_validation_v1",
        "artifact_id": "P7T04-COMMON-SOURCE-PROPAGATION-VALIDATION-V1",
        "task_id": "RT-20260728-003",
        "job_id": "AJ-RT-20260728-003-001",
        "plan_task_id": "P7-T04",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in source_paths
        },
        "claim_boundary_summary": "Finite source support theorem and scoped full-suite U_bij obstruction only; no physical principal symbol cone metric coupling GR proof or promotion.",
        "proof_authority": False,
        "physics_promotion_authorized": False,
    }
    compact = {
        "schema_id": "common_source_propagation_compact_receipt_v1",
        "artifact_id": "P7T04-COMMON-SOURCE-PROPAGATION-COMPACT-RECEIPT-V1",
        "task_id": "RT-20260728-003",
        "job_id": "AJ-RT-20260728-003-001",
        "status": report["status"],
        "result_status": "PRECISE_SCOPED_OBSTRUCTION_WITH_COMMON_THREE_ADDRESS_SUBFAMILY",
        "obstruction_id": "OBST-P7T04-FULL-SUITE-COMMON-PROPAGATION-001",
        "check_count": report["check_count"],
        "failed_check_count": report["failed_check_count"],
        "protocol_profile_count": len(expected_profiles),
        "common_subfamily_role_count": 3,
        "minimal_countermodel_vertex_count_each": 2,
        "principal_symbol_computed": False,
        "physical_cone_or_metric_derived": False,
        "global_no_go_claimed": False,
        "source_hashes": report["source_hashes"],
        "claim_boundary_summary": report["claim_boundary_summary"],
    }

    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        COMPACT_PATH.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output = compact if args.check else report
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(f"{report['status']} checks={report['check_count']} failed={report['failed_check_count']}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
