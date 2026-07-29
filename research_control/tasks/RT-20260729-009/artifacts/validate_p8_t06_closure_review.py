#!/usr/bin/env python3
"""Validate the bounded P8-T06 closure red-team review packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


VALIDATOR_ID = "validate_p8_t06_closure_review_v1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REPORT = HERE / "p8_t06_closure_review_validation_v1.json"
COMPACT = HERE / "p8_t06_closure_review_compact_receipt_v1.json"

SOURCES = {
    "P8_T02_target": (
        ROOT / "research_control/tasks/RT-20260729-005/artifacts/local_effective_action_closure_target_v1.tex",
        "13402c3d80f114b643a0216484b0ba775a2f02d1f0733f33d8cf86044e6add96",
    ),
    "P8_T02_envelope": (
        ROOT / "research_control/tasks/RT-20260729-005/artifacts/local_effective_action_assumption_envelope_v1.yaml",
        "da939b16a0cb4da082068ab9954d11c4c7a7a658e746c50295dc20347fc82a65",
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
    "P8_T04_equation": (
        ROOT / "research_control/tasks/RT-20260729-007/artifacts/finite_source_field_equation_identity_v1.tex",
        "12a1cfae87cd673241aefe88144ab974b49fc3bad284a81baff90b2e806d5168",
    ),
    "P8_T04_spec": (
        ROOT / "research_control/tasks/RT-20260729-007/artifacts/finite_source_field_equation_identity_spec_v1.yaml",
        "d37fdff6d320751d0174459c3d10bec75aa04be62c72c368480f1cafdb46e5f8",
    ),
    "P8_T04_map": (
        ROOT / "research_control/tasks/RT-20260729-007/artifacts/source_to_effective_equation_map_v1.yaml",
        "1c2b24a0b09023ed92bf1c03cf6ec1cf0d56db52a847fad5ed7eae03e817c452",
    ),
    "P8_T05_stress": (
        ROOT / "research_control/tasks/RT-20260729-008/artifacts/finite_constraint_dynamical_viability_stress_v1.tex",
        "ddd39764c3b6f86e86574458b885e90271a2b044d1d141ae931723e80599acb1",
    ),
    "P8_T05_countermodels": (
        ROOT / "research_control/tasks/RT-20260729-008/artifacts/finite_constraint_dynamic_completion_countermodels_v1.yaml",
        "c73615d9dd69a4f81f75da037e94801de4c7ec0ef8ba062abe5aafc7626e81a1",
    ),
}

ARTIFACTS = {
    "review": HERE / "p8_t06_closure_red_team_review_v1.yaml",
    "smuggling_audit": HERE / "p8_t06_closure_smuggling_audit_v1.yaml",
    "reproduction": HERE / "closure_symbolic_reproduction_v1.yaml",
    "blind_status": HERE / "blind_mathematical_review_status_v1.yaml",
    "human_action": HERE / "independent_review_human_action_v1.yaml",
    "gate_d_matrix": HERE / "p8_t06_gate_d_readiness_matrix_v1.yaml",
    "child_math": HERE / "child_phys_math_p8_t06_closure_review.yaml",
    "child_phil": HERE / "child_phys_phil_p8_t06_closure_review.yaml",
    "conflict_review": HERE / "parent_conflict_review_p8_t06_closure_review.yaml",
    "fusion_notes": HERE / "parent_fusion_notes_p8_t06_closure_review.md",
    "receipt": HERE / "p8_t06_closure_review_receipt.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse as an object")
    return data


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [
        sum((entry * vector[index] for index, entry in enumerate(row)), Fraction(0))
        for row in matrix
    ]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


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

    for name, (path, expected_hash) in SOURCES.items():
        check(f"source_exists::{name}", path.is_file(), str(path.relative_to(ROOT)))
        check(
            f"source_hash::{name}",
            path.is_file() and sha256(path) == expected_hash,
            expected_hash,
        )

    parsed: dict[str, dict[str, Any]] = {}
    for name, path in ARTIFACTS.items():
        check(f"artifact_exists::{name}", path.is_file(), path.name)
        check(
            f"artifact_nonempty::{name}",
            path.is_file() and path.stat().st_size > 100,
            path.name,
        )
        if path.suffix == ".yaml" and path.is_file():
            try:
                parsed[name] = load_yaml(path)
                check(f"yaml_parse::{name}", True, path.name)
            except Exception as exc:
                parsed[name] = {}
                check(f"yaml_parse::{name}", False, str(exc))

    review = parsed.get("review", {})
    context = review.get("review_context", {})
    check("review::verdict", review.get("verdict") == "repair_required", "repair_required")
    check(
        "review::same_context",
        context.get("classification") == "same_context_role_review",
        "same_context_role_review",
    )
    check("review::not_blind", context.get("blind_packet_received") is False, "not blind")
    check("review::review_executed", context.get("review_executed") is True, "review executed")
    check("review::no_replication", context.get("replication_executed") is False, "no replication")
    claims = context.get("claims", {})
    for key in (
        "external_review_completed",
        "human_expert_review_completed",
        "independent_replication_completed",
    ):
        check(f"review::claim_false::{key}", claims.get(key) is False, key)
    check(
        "review::workflow_disregarded",
        review.get("workflow_success_disregarded_as_evidence") is True,
        "workflow success excluded",
    )
    check(
        "review::validator_disregarded",
        review.get("validator_success_disregarded_as_evidence") is True,
        "validator success excluded",
    )
    check(
        "review::promotion_false",
        review.get("physics_promotion_authorized") is False,
        "no physics promotion",
    )

    audit = parsed.get("smuggling_audit", {})
    counts = audit.get("finding_counts", {})
    conclusion = audit.get("conclusion", {})
    check("audit::result", audit.get("result") == "REPAIR_REQUIRED_NO_TARGET_IMPORT_DETECTED", "exact result")
    check("audit::blocking_count", counts.get("blocking") == 1, "one blocking finding")
    check("audit::total_count", counts.get("total") == 5, "five calibrated findings")
    check("audit::hidden_import_zero", counts.get("hidden_target_imports") == 0, "zero hidden target imports")
    check("audit::algebra_error_zero", counts.get("algebraic_errors_in_finite_core") == 0, "zero finite-core algebra errors")
    check(
        "audit::gate_d_not_ready",
        conclusion.get("Gate_D_readiness") == "NOT_READY_REPAIR_AND_INDEPENDENT_REVIEW_REQUIRED",
        "Gate D not ready",
    )

    reproduction = parsed.get("reproduction", {})
    pressure = reproduction.get("assumption_pressure", {})
    check("reproduction::finite_core", reproduction.get("result", {}).get("finite_core_algebra") == "PASS", "finite algebra")
    check("reproduction::A4_fail", str(pressure.get("A4", "")).startswith("FAIL_"), "A4 missing data")
    check("reproduction::A9_static", "STATIC" in str(pressure.get("A9", "")), "A9 static only")
    check("reproduction::not_independent", reproduction.get("independent_replication") is False, "not independent")

    quarter = Fraction(1, 4)
    laplacian = [[quarter, -quarter], [-quarter, quarter]]
    u = [Fraction(3), Fraction(-3)]
    response = matvec(laplacian, u)
    check("math::source_response", response == [Fraction(3, 2), Fraction(-3, 2)], str(response))
    check("math::component_balance", sum(response, Fraction(0)) == 0, "balanced")
    h = u
    residual = [a - b for a, b in zip(matvec(laplacian, h), response)]
    check("math::euler_residual", residual == [0, 0], str(residual))
    source_action = dot(u, response) / 2
    closure_action = dot(h, matvec(laplacian, h)) / 2 - dot(response, h)
    check("math::on_shell", closure_action == -source_action == Fraction(-9, 2), str(closure_action))
    check(
        "math::quotient_eigenvector",
        matvec(laplacian, [Fraction(1), Fraction(-1)])
        == [Fraction(1, 2), Fraction(-1, 2)],
        "nonzero eigenvalue 1/2",
    )

    blind = parsed.get("blind_status", {})
    check("blind::not_acquired", blind.get("status") == "NOT_ACQUIRED", "blind review missing")
    check(
        "blind::gate_blocked",
        blind.get("disposition", {}).get("Gate_D_positive_readiness") == "BLOCKED",
        "positive Gate D blocked",
    )
    human = parsed.get("human_action", {})
    check("human_action::required", human.get("status") == "HUMAN_ACTION_REQUIRED", "exact human action")
    check("human_action::five_steps", len(human.get("exact_actions", [])) == 5, "five exact actions")

    matrix = parsed.get("gate_d_matrix", {})
    check(
        "matrix::overall",
        matrix.get("overall_readiness") == "NOT_READY_REPAIR_AND_INDEPENDENT_REVIEW_REQUIRED",
        "not ready",
    )
    check("matrix::ten_criteria", len(matrix.get("criteria", [])) == 10, "ten criteria")
    check("matrix::promotion_false", matrix.get("authority_limits", {}).get("physics_promotion_authorized") is False, "no promotion")

    conflict = parsed.get("conflict_review", {})
    check("synthesis::conflicts_resolved", conflict.get("status") == "resolved", "resolved")
    check("synthesis::resolved_count", conflict.get("resolved_conflict_count") == 5, "five resolved conflicts")
    check("synthesis::no_unresolved", conflict.get("unresolved_conflicts") == [], "zero unresolved")
    for child_name in ("child_math", "child_phil"):
        check(
            f"synthesis::{child_name}_complete",
            parsed.get(child_name, {}).get("status") == "completed",
            child_name,
        )
        check(
            f"synthesis::{child_name}_no_subagent",
            parsed.get(child_name, {}).get("subagent_count") == 0,
            child_name,
        )

    receipt_text = ARTIFACTS["receipt"].read_text(encoding="utf-8") if ARTIFACTS["receipt"].is_file() else ""
    fusion_text = ARTIFACTS["fusion_notes"].read_text(encoding="utf-8") if ARTIFACTS["fusion_notes"].is_file() else ""
    for token in (
        "REPAIR_REQUIRED_NOT_READY_FOR_POSITIVE_GATE_D",
        "same-context internal AI review",
        "NOT_DERIVED",
        "NOT_COMPLETE",
    ):
        check(f"receipt_token::{token}", token in receipt_text, token)
    for token in (
        "A4",
        "coarse-graining map",
        "not external human review or independent replication",
        "No hidden target atlas",
    ):
        check(f"fusion_token::{token}", token in fusion_text, token)

    failures = [item for item in findings if item["status"] == "FAIL"]
    result = {
        "validator_id": VALIDATOR_ID,
        "task_id": "RT-20260729-009",
        "plan_task_id": "P8-T06",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(findings),
        "failure_count": len(failures),
        "warning_count": 0,
        "result_classification": "repair_required_not_ready_for_positive_gate_d",
        "finding_counts": {
            "blocking": 1,
            "high": 3,
            "medium": 1,
            "hidden_target_imports": 0,
            "finite_core_algebra_errors": 0,
        },
        "review_context_classification": "same_context_role_review",
        "blind_review_completed": False,
        "independent_replication_completed": False,
        "physics_promotion_authorized": False,
        "findings": findings,
    }
    compact = {
        "schema_id": "p8_t06_closure_review_compact_receipt_v1",
        "task_id": "RT-20260729-009",
        "plan_task_id": "P8-T06",
        "result_status": "REPAIR_REQUIRED_NOT_READY_FOR_POSITIVE_GATE_D",
        "source_hashes": {
            name: expected for name, (_, expected) in SOURCES.items()
        },
        "finding_counts": result["finding_counts"],
        "validator_ids": [
            VALIDATOR_ID,
            "validate_red_team_review_artifact",
            "validate_claim_language",
            "validate_research_control",
        ],
        "review_context_classification": "same_context_role_review",
        "blind_review_completed": False,
        "independent_replication_completed": False,
        "Gate_D_positive_readiness": "NOT_READY",
        "claim_boundary_summary": "Finite proposal-scope algebra reproduced; A4 and A9 status repair plus evidenced independent review required; no physical gravity Einstein equation Gate Chair verdict benchmark proof publication push or promotion.",
        "physics_promotion_authorized": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    compact_rendered = json.dumps(compact, indent=2, sort_keys=True) + "\n"

    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8")
        COMPACT.write_text(compact_rendered, encoding="utf-8")
    if args.check:
        check(
            "report::fresh",
            REPORT.is_file() and REPORT.read_text(encoding="utf-8") == rendered,
            REPORT.name,
        )
        check(
            "compact::fresh",
            COMPACT.is_file() and COMPACT.read_text(encoding="utf-8") == compact_rendered,
            COMPACT.name,
        )
        failures = [item for item in findings if item["status"] == "FAIL"]
        result["status"] = "PASS" if not failures else "FAIL"
        result["check_count"] = len(findings)
        result["failure_count"] = len(failures)
        result["findings"] = findings

    if args.json or True:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
