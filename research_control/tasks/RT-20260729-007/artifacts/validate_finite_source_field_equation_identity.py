#!/usr/bin/env python3
"""Validate the exact RT-20260729-007 P8-T04 finite equation packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260729-007"
ARTIFACT_DIR = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACT_DIR / "finite_source_field_equation_identity_validation_v1.json"

FIXED_SOURCES = {
    "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_constraint_candidate_v1.tex":
        "82dd10d8e91be3781ca4f21e7f9fbf2ce1a9108ae7191db22fed9dfe6086f2fa",
    "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_constraint_spec_v1.yaml":
        "8840b205e8aa12d73f3e782ec6936eb96385bb5694c298b1bf41a2bdfe472626",
    "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_coefficient_ledger_v1.yaml":
        "5948e1ab75e42f622e5cc7309c9a6598720021ff2c893126f93c6b0bc21b7372",
    "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_controls_v1.yaml":
        "b91f240487fd22b9b95b7c7752e429128d20ccb59b3a202c3430ffbbd2922b6e",
    "research_control/tasks/RT-20260729-005/artifacts/local_effective_action_closure_target_v1.tex":
        "13402c3d80f114b643a0216484b0ba775a2f02d1f0733f33d8cf86044e6add96",
    "research_control/tasks/RT-20260728-005/artifacts/source_kernel_variational_object_candidate_v1.tex":
        "386769e40167c35604625ef7250c027dc1712c82db4790e2895e0b31ac3cfbf7",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex":
        "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml":
        "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
}

REQUIRED_ARTIFACTS = [
    "finite_source_field_equation_identity_v1.tex",
    "finite_source_field_equation_identity_spec_v1.yaml",
    "source_to_effective_equation_map_v1.yaml",
    "finite_source_field_equation_identity_controls_v1.yaml",
    "finite_source_field_equation_identity_receipt.md",
    "child_phys_math_p8_t04_finite_field_equation.yaml",
    "child_phys_phil_p8_t04_finite_field_equation.yaml",
    "parent_conflict_review_p8_t04_finite_field_equation.yaml",
    "parent_fusion_notes_p8_t04_finite_field_equation.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    data = yaml.safe_load((ARTIFACT_DIR / name).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{name} is not a YAML mapping")
    return data


def mat_vec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((entry * value for entry, value in zip(row, vector)), Fraction(0))
            for row in matrix]


def vec_sub(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return [a - b for a, b in zip(left, right)]


def vec_scale(scale: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [scale * value for value in vector]


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][col]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][col]
            if factor:
                work[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def laplacian(conductance: list[list[Fraction]]) -> list[list[Fraction]]:
    size = len(conductance)
    result: list[list[Fraction]] = []
    for x in range(size):
        row: list[Fraction] = []
        for y in range(size):
            if x == y:
                row.append(sum(
                    (conductance[x][z] for z in range(size) if z != x),
                    Fraction(0),
                ))
            else:
                row.append(-conductance[x][y])
        result.append(row)
    return result


def flux_divergence(
    conductance: list[list[Fraction]],
    h: list[Fraction],
    u: list[Fraction],
    alpha: Fraction,
    beta: Fraction,
) -> tuple[list[list[Fraction]], list[Fraction]]:
    size = len(conductance)
    flux = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            flux[x][y] = conductance[x][y] * (
                alpha * (h[x] - h[y]) - beta * (u[x] - u[y])
            )
    divergence = [sum(row, Fraction(0)) for row in flux]
    return flux, divergence


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({
            "name": name,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        })

    for name in REQUIRED_ARTIFACTS:
        artifact = ARTIFACT_DIR / name
        check(f"artifact_exists:{name}", artifact.is_file(), str(artifact.relative_to(ROOT)))

    for relative, expected in FIXED_SOURCES.items():
        source = ROOT / relative
        actual = sha256(source) if source.is_file() else ""
        check(f"fixed_source_hash:{relative}", actual == expected,
              f"expected={expected} actual={actual}")

    tex = (ARTIFACT_DIR / "finite_source_field_equation_identity_v1.tex").read_text(
        encoding="utf-8"
    )
    receipt = (ARTIFACT_DIR / "finite_source_field_equation_identity_receipt.md").read_text(
        encoding="utf-8"
    )
    fusion = (ARTIFACT_DIR / "parent_fusion_notes_p8_t04_finite_field_equation.md").read_text(
        encoding="utf-8"
    )
    spec = load_yaml("finite_source_field_equation_identity_spec_v1.yaml")
    equation_map = load_yaml("source_to_effective_equation_map_v1.yaml")
    controls = load_yaml("finite_source_field_equation_identity_controls_v1.yaml")
    math_child = load_yaml("child_phys_math_p8_t04_finite_field_equation.yaml")
    philosophy_child = load_yaml("child_phys_phil_p8_t04_finite_field_equation.yaml")
    conflict = load_yaml("parent_conflict_review_p8_t04_finite_field_equation.yaml")

    required_tex_tokens = [
        "exact_finite_equation_and_precise_scoped_obstruction",
        r"\alpha L_Ch-\beta L_Cu",
        r"[h]=\frac{\beta}{\alpha}[u]",
        "J_{xy}(h,u)",
        r"\sum_{x\in K}\mathcal E_{C,x}^{\alpha,\beta}",
        r"k^{\mathsf T}\Eop",
        r"D_uS_C^{\alpha,\beta}",
        "OBST-P8T04-FINITE-CONSTRAINT-EINSTEIN-TYPE-DATA-ABSENT-001",
        "blocked_adoption_open_continuation",
        "not a global no-go theorem",
        "P8-T05",
    ]
    for token in required_tex_tokens:
        check(f"tex_token:{token}", token in tex, token)

    required_boundary_tokens = [
        "not an Einstein equation",
        "not a contracted Bianchi",
        "not a target stress-energy conservation law",
        "No target atlas",
        "No canonical ontology",
        "No target-spacetime codomain",
        "not a global no-go theorem",
    ]
    normalized_tex = " ".join(tex.lower().split())
    for token in required_boundary_tokens:
        check(
            f"authority_boundary:{token}",
            " ".join(token.lower().split()) in normalized_tex,
            token,
        )

    check("spec_task_id", spec.get("task_id") == "RT-20260729-007", str(spec.get("task_id")))
    check("spec_plan_task_id", spec.get("plan_task_id") == "P8-T04",
          str(spec.get("plan_task_id")))
    check("spec_result",
          spec.get("ontology_formalizer_result")
          == "exact_finite_equation_and_precise_scoped_obstruction",
          str(spec.get("ontology_formalizer_result")))
    check("spec_status", spec.get("status") == "draft/control", str(spec.get("status")))
    check("spec_candidate_status", spec.get("candidate_status") == "proposal-only",
          str(spec.get("candidate_status")))
    check("spec_material_class", spec.get("material_class") == "source-extension data",
          str(spec.get("material_class")))
    check("spec_adoption",
          spec.get("adoption_status") == "blocked_adoption_open_continuation",
          str(spec.get("adoption_status")))

    field_equation = spec.get("field_equation", {})
    check("field_equation_exact",
          field_equation.get("equation") == "E_C^(alpha,beta)=0",
          str(field_equation.get("equation")))
    check("field_equation_solution",
          field_equation.get("exact_solution_class") == "[h]=(beta/alpha)[u]",
          str(field_equation.get("exact_solution_class")))
    check("field_equation_no_Einstein",
          field_equation.get("Einstein_equation_status") == "not_derived",
          str(field_equation.get("Einstein_equation_status")))

    identity = spec.get("identity_structure", {})
    check("identity_off_shell",
          "off shell" in str(identity.get("component_identity", "")),
          str(identity.get("component_identity")))
    check("identity_complete",
          "generated by ker L_C" in str(identity.get("completeness", "")),
          str(identity.get("completeness")))
    check("identity_not_Bianchi",
          identity.get("contracted_Bianchi_identity_status") == "not_derived",
          str(identity.get("contracted_Bianchi_identity_status")))
    check("identity_not_covariant_conservation",
          identity.get("target_covariant_conservation_status") == "not_derived",
          str(identity.get("target_covariant_conservation_status")))

    diagnostic = spec.get("joint_variation_diagnostic", {})
    check("source_slot_fixed", diagnostic.get("candidate_declares_u_fixed") is True,
          str(diagnostic.get("candidate_declares_u_fixed")))
    check("joint_collapse",
          diagnostic.get("combined_result") == "[h]=[u]=0",
          str(diagnostic.get("combined_result")))
    check("joint_new_dynamics_required",
          diagnostic.get("new_joint_dynamics_required") is True,
          str(diagnostic.get("new_joint_dynamics_required")))

    obstruction = spec.get("obstruction", {})
    check("obstruction_id",
          obstruction.get("obstruction_id")
          == "OBST-P8T04-FINITE-CONSTRAINT-EINSTEIN-TYPE-DATA-ABSENT-001",
          str(obstruction.get("obstruction_id")))
    check("obstruction_category",
          obstruction.get("category") == "derivation_critical_missing_source_law",
          str(obstruction.get("category")))
    check("obstruction_scoped",
          obstruction.get("no_go_theorem_status") == "not_proved",
          str(obstruction.get("no_go_theorem_status")))
    check("continuation_open",
          obstruction.get("same_milestone_continuation") == "open",
          str(obstruction.get("same_milestone_continuation")))

    result = spec.get("result", {})
    for key in [
        "exact_finite_field_equation_derived",
        "exact_finite_identity_derived",
        "identity_completeness_derived",
        "source_to_effective_equation_map_derived",
        "joint_variation_diagnostic_derived",
        "precise_scoped_obstruction_recorded",
        "new_mathematical_payload_supplied",
    ]:
        check(f"result_true:{key}", result.get(key) is True, str(result.get(key)))
    for key in [
        "physical_gravitational_interpretation_established",
        "effective_metric_constructed",
        "target_stress_energy_constructed",
        "diffeomorphism_invariance_derived",
        "contracted_Bianchi_identity_derived",
        "target_covariant_conservation_derived",
        "Einstein_equations_derived",
        "exact_GR_recovery_proved",
    ]:
        check(f"result_false:{key}", result.get(key) is False, str(result.get(key)))
    check("next_plan_task", result.get("next_plan_task_id") == "P8-T05",
          str(result.get("next_plan_task_id")))

    maps = equation_map.get("maps", {})
    check("map_source_to_equation",
          maps.get("source_to_equation", {}).get("rule") == "[u] -> beta L_Cu",
          str(maps.get("source_to_equation", {}).get("rule")))
    check("map_source_to_solution",
          maps.get("source_to_solution", {}).get("rule") == "[u] -> (beta/alpha)[u]",
          str(maps.get("source_to_solution", {}).get("rule")))
    target_bridge = equation_map.get("target_bridge", {})
    for key in [
        "source_to_target_stress_energy_map",
        "finite_carrier_to_Lorentzian_metric_map",
        "finite_operator_to_curvature_operator_map",
        "finite_identity_to_contracted_Bianchi_map",
        "continuum_limit",
        "physical_coefficient_map",
    ]:
        check(f"target_bridge_missing:{key}", target_bridge.get(key) == "missing",
              str(target_bridge.get(key)))

    check("controls_target_comparison_after_derivation",
          controls.get("derivation_controls", {}).get(
              "target_comparison_only_after_derivation"
          ) is True,
          str(controls.get("derivation_controls", {}).get(
              "target_comparison_only_after_derivation"
          )))
    check("controls_new_payload",
          controls.get("freeze_controls", {}).get(
              "repeated_burden_without_new_payload"
          ) is False,
          str(controls.get("freeze_controls", {}).get(
              "repeated_burden_without_new_payload"
          )))
    check("controls_freeze_reinterpretation",
          controls.get("freeze_controls", {}).get(
              "freeze_unchanged_candidate_against_target_reinterpretation"
          ) is True,
          str(controls.get("freeze_controls", {}).get(
              "freeze_unchanged_candidate_against_target_reinterpretation"
          )))

    check("math_child_completed", math_child.get("status") == "completed",
          str(math_child.get("status")))
    check("philosophy_child_completed", philosophy_child.get("status") == "completed",
          str(philosophy_child.get("status")))
    check("no_child_jobs",
          math_child.get("child_agentjob_count") == 0
          and philosophy_child.get("child_agentjob_count") == 0,
          "internal perspectives only")
    check("no_subagents",
          math_child.get("subagent_count") == 0
          and philosophy_child.get("subagent_count") == 0,
          "subagent_count=0")
    check("conflicts_resolved", conflict.get("status") == "resolved",
          str(conflict.get("status")))
    check("unresolved_conflicts_zero", conflict.get("unresolved_conflict_count") == 0,
          str(conflict.get("unresolved_conflict_count")))
    check("six_conflicts", len(conflict.get("conflicts", [])) == 6,
          str(len(conflict.get("conflicts", []))))

    for corpus_name, corpus in [
        ("receipt", receipt),
        ("fusion", fusion),
    ]:
        for token in [
            "exact_finite_equation_and_precise_scoped_obstruction",
            "OBST-P8T04-FINITE-CONSTRAINT-EINSTEIN-TYPE-DATA-ABSENT-001",
            "blocked_adoption_open_continuation",
            "not a global no-go theorem",
            "P8-T05",
        ]:
            check(f"{corpus_name}_token:{token}", token.lower() in corpus.lower(), token)

    conductance = [
        [Fraction(0), Fraction(1, 4)],
        [Fraction(1, 4), Fraction(0)],
    ]
    lap = laplacian(conductance)
    check("two_state_laplacian",
          lap == [
              [Fraction(1, 4), Fraction(-1, 4)],
              [Fraction(-1, 4), Fraction(1, 4)],
          ],
          str(lap))
    alpha = Fraction(2)
    beta = Fraction(3)
    u = [Fraction(2), Fraction(-2)]
    h = vec_scale(beta / alpha, u)
    equation_value = vec_sub(
        vec_scale(alpha, mat_vec(lap, h)),
        vec_scale(beta, mat_vec(lap, u)),
    )
    check("exact_solution_zero_response",
          equation_value == [Fraction(0), Fraction(0)],
          str(equation_value))
    check("finite_operator_rank", rank(lap) == 1, str(rank(lap)))
    check("finite_identity_nullity", len(lap) - rank(lap) == 1,
          str(len(lap) - rank(lap)))

    offshell_h = [Fraction(1), Fraction(0)]
    offshell_u = [Fraction(0), Fraction(1)]
    flux, divergence = flux_divergence(
        conductance, offshell_h, offshell_u, alpha, beta
    )
    direct = vec_sub(
        vec_scale(alpha, mat_vec(lap, offshell_h)),
        vec_scale(beta, mat_vec(lap, offshell_u)),
    )
    check("flux_antisymmetric",
          flux[0][1] == -flux[1][0],
          f"{flux[0][1]} {-flux[1][0]}")
    check("flux_divergence_equals_response", divergence == direct,
          f"divergence={divergence} direct={direct}")
    check("component_sum_zero", sum(direct, Fraction(0)) == 0, str(sum(direct)))

    disconnected_c = [
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0)],
    ]
    disconnected_lap = laplacian(disconnected_c)
    check("disconnected_rank", rank(disconnected_lap) == 1,
          str(rank(disconnected_lap)))
    check("disconnected_identity_count",
          len(disconnected_lap) - rank(disconnected_lap) == 2,
          str(len(disconnected_lap) - rank(disconnected_lap)))
    arbitrary_h = [Fraction(3), Fraction(-1), Fraction(7)]
    arbitrary_u = [Fraction(-2), Fraction(4), Fraction(5)]
    disconnected_response = vec_sub(
        vec_scale(alpha, mat_vec(disconnected_lap, arbitrary_h)),
        vec_scale(beta, mat_vec(disconnected_lap, arbitrary_u)),
    )
    check("first_component_identity",
          disconnected_response[0] + disconnected_response[1] == 0,
          str(disconnected_response[:2]))
    check("isolated_component_identity",
          disconnected_response[2] == 0,
          str(disconnected_response[2]))

    authority = spec.get("authority_limits", {})
    for key in [
        "canonical_ontology_modified",
        "source_law_adopted_or_rejected",
        "candidate_adopted",
        "physical_interpretation_established",
        "physics_promotion_authorized",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
    ]:
        check(f"authority_false:{key}", authority.get(key) is False,
              str(authority.get(key)))

    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "finite_source_field_equation_identity_validation_v1",
        "task_id": "RT-20260729-007",
        "plan_task_id": "P8-T04",
        "result": "exact_finite_equation_and_precise_scoped_obstruction",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "checks": checks,
        "authority_limits": {
            "physical_gravity_established": False,
            "Einstein_equations_derived": False,
            "exact_GR_recovery_proved": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authorized": False,
            "push_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        if not REPORT_PATH.is_file():
            report["status"] = "FAIL"
            report["failure_count"] = int(report["failure_count"]) + 1
            report["checks"].append({
                "name": "report_exists",
                "status": "FAIL",
                "detail": str(REPORT_PATH.relative_to(ROOT)),
            })
        else:
            saved = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
            if saved != report:
                report["status"] = "FAIL"
                report["failure_count"] = int(report["failure_count"]) + 1
                report["checks"].append({
                    "name": "report_fresh",
                    "status": "FAIL",
                    "detail": "saved validation report differs from current evaluation",
                })
    if args.json:
        print(json.dumps({
            "status": report["status"],
            "task_id": report["task_id"],
            "plan_task_id": report["plan_task_id"],
            "result": report["result"],
            "check_count": report["check_count"],
            "failure_count": report["failure_count"],
            "report_path": str(REPORT_PATH.relative_to(ROOT)),
        }, sort_keys=True))
    else:
        print(f"{report['status']}: {report['check_count']} checks, "
              f"{report['failure_count']} failures")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
