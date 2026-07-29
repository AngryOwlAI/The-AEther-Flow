#!/usr/bin/env python3
"""Validate the bounded P8-T03 finite source closure candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260729-006"
ART = TASK / "artifacts"
SPEC_PATH = ART / "finite_source_closure_constraint_spec_v1.yaml"
COEFF_PATH = ART / "finite_source_closure_coefficient_ledger_v1.yaml"
CONTROL_PATH = ART / "finite_source_closure_controls_v1.yaml"
TEX_PATH = ART / "finite_source_closure_constraint_candidate_v1.tex"
MATH_CHILD = ART / "child_phys_math_p8_t03_finite_source_closure.yaml"
PHIL_CHILD = ART / "child_phys_phil_p8_t03_finite_source_closure.yaml"
CONFLICT_PATH = ART / "parent_conflict_review_p8_t03_finite_source_closure.yaml"
REPORT_PATH = ART / "finite_source_closure_constraint_validation_v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse to an object")
    return data


def matmul(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((a * b for a, b in zip(row, vector)), Fraction(0)) for row in matrix]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    required = [
        SPEC_PATH,
        COEFF_PATH,
        CONTROL_PATH,
        TEX_PATH,
        MATH_CHILD,
        PHIL_CHILD,
        CONFLICT_PATH,
        ART / "parent_fusion_notes_p8_t03_finite_source_closure.md",
        ART / "finite_source_closure_constraint_receipt.md",
    ]
    for path in required:
        check(f"file:{path.name}", path.is_file(), "required task-local artifact exists")

    spec = load_yaml(SPEC_PATH)
    coeff = load_yaml(COEFF_PATH)
    controls = load_yaml(CONTROL_PATH)
    math_child = load_yaml(MATH_CHILD)
    phil_child = load_yaml(PHIL_CHILD)
    conflicts = load_yaml(CONFLICT_PATH)

    check("status:draft_control", spec.get("status") == "draft/control", "candidate status is draft/control")
    check("status:proposal_only", spec.get("candidate_status") == "proposal-only", "candidate is proposal-only")
    check(
        "status:blocked_adoption_open_continuation",
        spec.get("adoption_status") == "blocked_adoption_open_continuation",
        "adoption remains blocked while continuation remains open",
    )
    check(
        "result:constructed_candidate",
        spec.get("candidate_constructor_result") == "constructed_candidate",
        "one decisive Candidate Constructor result is named",
    )

    for source in spec.get("source_basis", []):
        source_path = ROOT / source["path"]
        check(f"source_exists:{source['source_id']}", source_path.is_file(), source["path"])
        check(
            f"source_hash:{source['source_id']}",
            source_path.is_file() and sha256(source_path) == source["sha256"],
            source["sha256"],
        )

    assumptions = spec.get("closure_target_instantiation", [])
    check("assumptions:count", len(assumptions) == 10, "A0 through A9 are present")
    check(
        "assumptions:ids",
        [item.get("assumption_id") for item in assumptions] == [f"A{i}" for i in range(10)],
        "assumption identifiers are exact and ordered",
    )
    check(
        "assumptions:finite_constructed",
        all(item.get("status") == "constructed_in_finite_candidate" for item in assumptions),
        "every assumption is qualified to the finite candidate",
    )

    P = [[Fraction(1, 2), Fraction(1, 2)], [Fraction(0), Fraction(1)]]
    C = [[(P[i][j] + P[j][i]) / 2 for j in range(2)] for i in range(2)]
    L = [[Fraction(1, 4), Fraction(-1, 4)], [Fraction(-1, 4), Fraction(1, 4)]]
    check("math:C_fixed", C == [[Fraction(1, 2), Fraction(1, 4)], [Fraction(1, 4), Fraction(1)]], str(C))
    check("math:L_symmetric", L[0][1] == L[1][0], "L_C is symmetric")
    check("math:L_row_sum", all(sum(row, Fraction(0)) == 0 for row in L), "component constants are zero modes")

    u = [Fraction(3), Fraction(-3)]
    a = matmul(L, u)
    h = u
    residual = [x - y for x, y in zip(matmul(L, h), a)]
    source_action = dot(u, a) / 2
    closure_action = dot(h, matmul(L, h)) / 2 - dot(a, h)
    check("math:source_response", a == [Fraction(3, 2), Fraction(-3, 2)], str(a))
    check("math:component_balance", sum(a, Fraction(0)) == 0, "source response is balanced")
    check("math:constraint", residual == [0, 0], str(residual))
    check("math:on_shell", closure_action == -source_action, f"{closure_action} == {-source_action}")

    eta = [Fraction(5), Fraction(-2)]
    first_variation = dot(eta, residual)
    check("math:first_variation_on_shell", first_variation == 0, str(first_variation))

    result = spec.get("result", {})
    for key in (
        "constructed_candidate",
        "nontrivial_constraint_constructed",
        "source_to_closure_map_constructed",
        "finite_Helmholtz_check_passed",
        "finite_gluing_check_passed",
        "component_balance_bridge_constructed",
    ):
        check(f"result:{key}", result.get(key) is True, key)
    for key in (
        "target_effective_gravitational_action_constructed",
        "physical_gravitational_interpretation_established",
        "target_atlas_constructed_or_assumed",
        "target_metric_constructed_or_assumed",
        "target_stress_energy_constructed",
        "Einstein_Hilbert_action_constructed_or_assumed",
        "Einstein_equations_derived_or_assumed",
        "exact_GR_recovery_proved",
        "benchmark_promotion_authorized",
    ):
        check(f"blocked:{key}", result.get(key) is False, key)

    coefficient_rows = coeff.get("coefficients", [])
    check("coefficients:count", len(coefficient_rows) == 3, "alpha, beta, and C_xy are explicit")
    check(
        "coefficients:no_target_matching",
        all(row.get("fixed_by_target_matching") is False for row in coefficient_rows),
        "no coefficient is fixed by target matching",
    )
    conclusions = coeff.get("coefficient_conclusions", {})
    check("coefficients:target_matched_zero", conclusions.get("target_matched_count") == 0, "zero target-matched coefficients")
    check("coefficients:dimensionful_zero", conclusions.get("dimensionful_constant_count") == 0, "no physical dimensionful constant")

    audit = controls.get("no_target_import_audit", {})
    check("audit:no_target_import", audit.get("explicit_target_import_found") is False, "no target premise")
    check(
        "audit:all_prohibited_absent",
        all(value is True for value in audit.get("prohibited_premises_absent", {}).values()),
        "all enumerated prohibited premises are absent",
    )
    check("controls:failure_count", len(controls.get("failure_branches", [])) == 5, "five exact fail-closed branches")
    check("controls:forbidden_count", len(controls.get("forbidden_conclusions", [])) >= 12, "downstream overreads are blocked")

    check("decomposition:math_status", math_child.get("status") == "completed", "math perspective completed")
    check("decomposition:phil_status", phil_child.get("status") == "completed", "philosophy perspective completed")
    check("decomposition:no_subagents_math", math_child.get("subagent_count") == 0, "no math subagent was created")
    check("decomposition:no_subagents_phil", phil_child.get("subagent_count") == 0, "no philosophy subagent was created")
    check("conflicts:resolved", conflicts.get("status") == "resolved", "parent review resolved all conflicts")
    check("conflicts:count", len(conflicts.get("conflicts", [])) == 5, "five conflicts are explicit")
    check("conflicts:unresolved_zero", conflicts.get("unresolved_conflict_count") == 0, "zero unresolved conflicts")

    tex = TEX_PATH.read_text(encoding="utf-8")
    for token in (
        "FiniteSourceClosureConstraintCandidate",
        "constructed\\_candidate",
        "blocked\\_adoption\\_open\\_continuation",
        "\\alpha L_Ch=\\beta",
        "not an Einstein",
    ):
        check(f"tex:{token}", token in tex, f"required source token {token!r}")

    completion_path = TASK / "jobs/completions/AJC-AJ-RT-20260729-006-001.yaml"
    if completion_path.is_file():
        completion = load_yaml(completion_path)
        cc_result = completion.get("candidate_constructor_result", {})
        check(
            "completion:constructed_candidate",
            cc_result.get("result_type") == "constructed_candidate",
            "completion has one decisive constructed_candidate result",
        )
        check("completion:no_fog", cc_result.get("no_fog_check") is True, "Candidate Constructor no-fog check passes")
        check(
            "completion:claim_boundary",
            cc_result.get("claim_boundary_preserved") is True,
            "completion preserves the claim boundary",
        )

    failed = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "finite_source_closure_constraint_validation_v1",
        "task_id": "RT-20260729-006",
        "candidate_id": "FiniteSourceClosureConstraintCandidate_v1",
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
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
