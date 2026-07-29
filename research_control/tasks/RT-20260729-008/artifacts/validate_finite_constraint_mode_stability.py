#!/usr/bin/env python3
"""Validate the bounded P8-T05 finite constraint and stability packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


VALIDATOR_ID = "validate_finite_constraint_mode_stability_v1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REPORT = HERE / "finite_constraint_mode_stability_validation_v1.json"

SOURCES = {
    "P8_T04_equation": (
        ROOT / "research_control/tasks/RT-20260729-007/artifacts/finite_source_field_equation_identity_v1.tex",
        "12a1cfae87cd673241aefe88144ab974b49fc3bad284a81baff90b2e806d5168",
    ),
    "P8_T03_candidate": (
        ROOT / "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_constraint_candidate_v1.tex",
        "82dd10d8e91be3781ca4f21e7f9fbf2ce1a9108ae7191db22fed9dfe6086f2fa",
    ),
    "P8_T03_spec": (
        ROOT / "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_constraint_spec_v1.yaml",
        "8840b205e8aa12d73f3e782ec6936eb96385bb5694c298b1bf41a2bdfe472626",
    ),
    "P8_T03_coefficients": (
        ROOT / "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_coefficient_ledger_v1.yaml",
        "5948e1ab75e42f622e5cc7309c9a6598720021ff2c893126f93c6b0bc21b7372",
    ),
    "P8_T03_controls": (
        ROOT / "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_controls_v1.yaml",
        "b91f240487fd22b9b95b7c7752e429128d20ccb59b3a202c3430ffbbd2922b6e",
    ),
    "P8_T02_closure_target": (
        ROOT / "research_control/tasks/RT-20260729-005/artifacts/local_effective_action_closure_target_v1.tex",
        "13402c3d80f114b643a0216484b0ba775a2f02d1f0733f33d8cf86044e6add96",
    ),
    "P7_T06_source_action": (
        ROOT / "research_control/tasks/RT-20260728-005/artifacts/source_kernel_variational_object_candidate_v1.tex",
        "386769e40167c35604625ef7250c027dc1712c82db4790e2895e0b31ac3cfbf7",
    ),
    "P7_T08_protected_decision": (
        ROOT / "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex",
        "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    ),
    "P6_T08_gate_b_certificate": (
        ROOT / "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml",
        "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    ),
}

ARTIFACTS = {
    "report": HERE / "finite_constraint_dynamical_viability_stress_v1.tex",
    "countermodels": HERE / "finite_constraint_dynamic_completion_countermodels_v1.yaml",
    "phase_diagram": HERE / "finite_constraint_stability_phase_diagram_v1.yaml",
    "controls": HERE / "finite_constraint_mode_stability_controls_v1.yaml",
    "receipt": HERE / "finite_constraint_mode_stability_receipt.md",
    "child_phys_math": HERE / "child_phys_math_p8_t05_finite_dynamical_viability.yaml",
    "child_phys_phil": HERE / "child_phys_phil_p8_t05_finite_dynamical_viability.yaml",
    "conflict_review": HERE / "parent_conflict_review_p8_t05_finite_dynamical_viability.yaml",
    "fusion_notes": HERE / "parent_fusion_notes_p8_t05_finite_dynamical_viability.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_vector(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((row[j] * vector[j] for j in range(len(vector))), Fraction(0)) for row in matrix]


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if work[i][col] != 0), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][col]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(rows):
            if row == rank or work[row][col] == 0:
                continue
            factor = work[row][col]
            work[row] = [
                work[row][j] - factor * work[rank][j] for j in range(cols)
            ]
        rank += 1
    return rank


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        findings.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    for name, (path, expected) in SOURCES.items():
        check(f"source_exists::{name}", path.is_file(), str(path.relative_to(ROOT)))
        check(f"source_hash::{name}", path.is_file() and sha256(path) == expected, expected)

    for name, path in ARTIFACTS.items():
        check(f"artifact_exists::{name}", path.is_file(), path.name)
        check(f"artifact_nonempty::{name}", path.is_file() and path.stat().st_size > 100, path.name)

    parsed: dict[str, Any] = {}
    for name in (
        "countermodels",
        "phase_diagram",
        "controls",
        "child_phys_math",
        "child_phys_phil",
        "conflict_review",
    ):
        try:
            parsed[name] = yaml.safe_load(ARTIFACTS[name].read_text(encoding="utf-8"))
            check(f"yaml_parse::{name}", isinstance(parsed[name], dict), name)
        except Exception as exc:  # pragma: no cover - surfaced as receipt evidence
            parsed[name] = {}
            check(f"yaml_parse::{name}", False, str(exc))

    report_text = ARTIFACTS["report"].read_text(encoding="utf-8")
    receipt_text = ARTIFACTS["receipt"].read_text(encoding="utf-8")
    fusion_text = ARTIFACTS["fusion_notes"].read_text(encoding="utf-8")

    report_tokens = [
        "scoped\\_obstruction",
        "OBST-P8T05-STATIC-FINITE-CONSTRAINT-DYNAMICS-UNDEFINED-001",
        "zero free homogeneous quotient-response modes",
        "propagating degree-of-freedom count requires",
        "No dynamical principal symbol is defined",
        "\\mathcal L_{+}",
        "\\mathcal L_{-}",
        "same static equation",
        "Near-disconnection control",
        "Positive static curvature is not ghost freedom",
        "It is not a global no-go",
        "future source-extension impossibility",
        "P8-T06",
    ]
    for index, token in enumerate(report_tokens, start=1):
        check(f"report_token::{index:02d}", token in report_text, token)

    receipt_tokens = [
        "PASS_SCOPED_OBSTRUCTION_READY_FOR_CHECKPOINT",
        "n-c",
        "undefined",
        "minimal pair",
        "locally frozen",
        "blocked_adoption_open_continuation",
        "P8-T06",
    ]
    for index, token in enumerate(receipt_tokens, start=1):
        check(f"receipt_token::{index:02d}", token in receipt_text, token)

    fusion_tokens = [
        "scoped_obstruction",
        "Six conflicts were resolved",
        "algebraic response modes from propagating physical degrees of freedom",
        "task-local countermodels from candidate laws or repairs",
        "P8-T06",
    ]
    for index, token in enumerate(fusion_tokens, start=1):
        check(f"fusion_token::{index:02d}", token in fusion_text, token)

    half = Fraction(1, 2)
    quarter = Fraction(1, 4)
    two_state = [[quarter, -quarter], [-quarter, quarter]]
    check(
        "math::two_state_kernel",
        matrix_vector(two_state, [Fraction(1), Fraction(1)]) == [Fraction(0), Fraction(0)],
        "L_C(1,1)=0",
    )
    check(
        "math::two_state_quotient_eigenvector",
        matrix_vector(two_state, [Fraction(1), Fraction(-1)]) == [half, -half],
        "L_C(1,-1)=(1/2)(1,-1)",
    )
    q = [half, -half]
    lq = matrix_vector(two_state, q)
    energy_form = sum((q[i] * lq[i] for i in range(2)), Fraction(0))
    check("math::two_state_quadratic_form", energy_form == Fraction(1, 4), "q^T L_C q=1/4")

    laplacians = [
        (
            [[Fraction(0)]],
            1,
            1,
        ),
        (
            [[quarter, -quarter], [-quarter, quarter]],
            2,
            1,
        ),
        (
            [
                [Fraction(1), Fraction(-1), Fraction(0)],
                [Fraction(-1), Fraction(2), Fraction(-1)],
                [Fraction(0), Fraction(-1), Fraction(1)],
            ],
            3,
            1,
        ),
        (
            [
                [Fraction(1), Fraction(-1), Fraction(0)],
                [Fraction(-1), Fraction(1), Fraction(0)],
                [Fraction(0), Fraction(0), Fraction(0)],
            ],
            3,
            2,
        ),
    ]
    for index, (laplacian, n, components) in enumerate(laplacians, start=1):
        check(
            f"math::rank_nullity_fixture::{index}",
            matrix_rank(laplacian) == n - components,
            f"rank={n-components}",
        )

    countermodels = parsed["countermodels"]
    general_pair = countermodels.get("general_pair", {})
    check(
        "countermodel::shared_static",
        general_pair.get("shared_static_equation") is True,
        "both completions reduce to alpha L_C q=0",
    )
    check(
        "countermodel::incompatible_verdicts",
        general_pair.get("incompatible_dynamical_verdicts") is True,
        "positive and negative kinetic branches differ",
    )
    check(
        "countermodel::not_adopted",
        countermodels.get("scope_controls", {}).get("completion_adopted") is False,
        "logical countermodels only",
    )

    phase = parsed["phase_diagram"]
    mode_count = phase.get("algebraic_mode_count", {})
    check(
        "phase::quotient_count",
        mode_count.get("quotient_coordinate_count") == "n-c",
        "quotient dimension",
    )
    check(
        "phase::algebraic_solution_dimension",
        mode_count.get("fixed_source_solution_dimension_on_quotient") == 0,
        "unique quotient solution",
    )
    check(
        "phase::physical_dof_undefined",
        mode_count.get("propagating_physical_degree_of_freedom_count") == "undefined",
        "no temporal phase space",
    )
    diagnostics = phase.get("diagnostics", [])
    expected_diagnostics = {
        "characteristic_speeds": "UNDEFINED",
        "hyperbolicity": "UNDEFINED",
        "ghosts": "UNDEFINED",
        "tachyons": "UNDEFINED",
        "gradient_instabilities": "UNDEFINED",
        "strong_coupling": "UNDEFINED",
    }
    observed = {row.get("diagnostic"): row.get("result") for row in diagnostics}
    for name, expected in expected_diagnostics.items():
        check(f"phase::diagnostic::{name}", observed.get(name) == expected, expected)

    controls = parsed["controls"]
    for key, value in controls.get("fixed_hashes", {}).items():
        expected = SOURCES.get(key, (None, ""))[1]
        check(
            f"controls::fixed_hash::{key}",
            value.get("sha256") == expected,
            value.get("sha256", ""),
        )
    for key, value in controls.get("authority_limits", {}).items():
        check(f"controls::authority_false::{key}", value is False, key)

    child_math = parsed["child_phys_math"]
    child_phil = parsed["child_phys_phil"]
    conflicts = parsed["conflict_review"]
    check("synthesis::child_math_complete", child_math.get("status") == "completed", "child_phys_math")
    check("synthesis::child_phil_complete", child_phil.get("status") == "completed", "child_phys_phil")
    check("synthesis::conflicts_resolved", conflicts.get("status") == "resolved", "resolved")
    check(
        "synthesis::resolved_count",
        conflicts.get("resolved_conflict_count") == 6,
        "six resolved conflicts",
    )
    check(
        "synthesis::no_unresolved",
        conflicts.get("unresolved_conflicts") == [],
        "no unresolved conflicts",
    )

    forbidden_positive_phrases = [
        "the candidate is ghost-free",
        "the candidate is hyperbolic",
        "the finite equation is an Einstein equation.",
        "exact GR recovery is proved",
        "global impossibility is proved",
    ]
    lowered = report_text.lower()
    for index, phrase in enumerate(forbidden_positive_phrases, start=1):
        check(f"claim_boundary::forbidden_positive::{index}", phrase.lower() not in lowered, phrase)

    failures = [item for item in findings if item["status"] == "FAIL"]
    result = {
        "validator_id": VALIDATOR_ID,
        "task_id": "RT-20260729-008",
        "plan_task_id": "P8-T05",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(findings),
        "failure_count": len(failures),
        "warning_count": 0,
        "finding_count": len(findings),
        "result_classification": "scoped_obstruction",
        "obstruction_id": "OBST-P8T05-STATIC-FINITE-CONSTRAINT-DYNAMICS-UNDEFINED-001",
        "findings": findings,
    }

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8")
    if args.check:
        check(
            "report::fresh",
            REPORT.is_file() and REPORT.read_text(encoding="utf-8") == rendered,
            REPORT.name,
        )
        failures = [item for item in findings if item["status"] == "FAIL"]
        result["status"] = "PASS" if not failures else "FAIL"
        result["check_count"] = len(findings)
        result["failure_count"] = len(failures)
        result["finding_count"] = len(findings)
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json:
        print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
