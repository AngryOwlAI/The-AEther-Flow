#!/usr/bin/env python3
"""Validate the bounded P9-T09 protected Gate E review transaction."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260731-004"
JOB_ID = "AJ-RT-20260731-004-001"
DECISION_ID = "DDR-20260731-004"
ROLE_REF = "gate-chair@0.1.0--RT-20260731-004"
APPROVAL_ID = "approval-20260731-001"
HANDOFF_ID = "handoff-0926"
DECISION_CODE = "NOT_READY_BENCHMARK_AND_COMPLETED_DERIVATION_REQUIREMENTS_UNMET"

TASK_DIR = Path("research_control/tasks/RT-20260731-004")
ARTIFACT_DIR = TASK_DIR / "artifacts"
FULL_REPORT = ARTIFACT_DIR / "p9_t09_gate_e_validation_v1.json"
COMPACT_REPORT = ARTIFACT_DIR / "p9_t09_gate_e_compact_receipt_v1.json"

FIXED_EVIDENCE = {
    "research_control/handoffs/handoff-0925.yaml": "82c243a8925214d880be811497089cba4411edd48fd5ed67572ab07d4906ff13",
    "research_control/handoffs/handoff-0925.md": "89658c0528ef75c1c65e96e49dba7dc6cab83f68fba3fbdb260d4c545e9b1a93",
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "ontology/tex/aether_flow_dynamics.tex": "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
    "ontology/tex/aether_flow_relativistic_recovery.tex": "77d5c2db56f122870343834f853bf2f375a912116a347d7c5710405c8707d69c",
    "ontology/tex/aether_flow_consistency.tex": "d965519639ee8764a5c5a63798d15e8a9a380d7e208dffc43a0be02b6f245ba1",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_verdict_matrix_v1.yaml": "89e484d18aca681a9f79484331a38ee9b98478e5169af4bb9de2762c71e473a4",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_scientific_status_v1.yaml": "af2f291a03511116c51db1a78bcd62caedd3c1e1b161acc749b8bb371093ac2e",
    "research_control/tasks/RT-20260729-012/artifacts/parent_fusion_notes_p9_t01_benchmark_protocol.md": "9ca58abe6eb1151614b4e5124df9a2e2aac4ecff301cea634dc4e7ad6cbcde03",
    "research_control/tasks/RT-20260731-001/artifacts/p9_t08_gate_e_readiness_matrix_v1.yaml": "2f2483dedb86f65d2b969959416b5bea0d4a39b0b26918107275c1784c253db8",
    "research_control/tasks/RT-20260731-001/artifacts/p9_t08_independent_replication_status_v1.yaml": "c3089818ea1ad682a7f246c3ec102d6eff34f80285265644de72c9fc9fff1dfc",
    "research_control/tasks/RT-20260731-001/artifacts/p9_t08_benchmark_suite_red_team_review_v1.yaml": "9d28acf5ba647801b12674b65772406700af28fc2229973b4a242d8b0a0c32b7",
    "research_control/tasks/RT-20260731-001/artifacts/p9_t08_benchmark_smuggling_audit_v1.yaml": "c5b05dad23261d479e624b9cf08a3d02c2773d05df4d15246793067525acd229",
    "research_control/tasks/RT-20260731-001/artifacts/p9_t08_cross_case_assumption_consistency_v1.yaml": "c1be5c75415fea6321b3490bad45e1b4a83c6cda302a8e6683c1c4b1658082e2",
    "research_control/tasks/RT-20260731-001/jobs/completions/AJC-AJ-RT-20260731-001-001.yaml": "29e12eca665ad418d9ac6d310eadc63b35fe199fca94dd06515abe7cc8267ab9",
}


def digest(path: Path) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load_yaml(path: str | Path) -> dict[str, Any]:
    value = yaml.safe_load((ROOT / Path(path)).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} is not a YAML mapping")
    return value


def csv_rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def one_row(path: str, key: str, value: str) -> dict[str, str] | None:
    rows = [row for row in csv_rows(path) if row.get(key) == value]
    return rows[0] if len(rows) == 1 else None


def check(condition: bool, finding_id: str, details: Any, findings: list[dict[str, Any]]) -> None:
    findings.append(
        {
            "finding_id": finding_id,
            "status": "PASS" if condition else "FAIL",
            "details": details,
        }
    )


def main() -> int:
    findings: list[dict[str, Any]] = []

    observed_hashes: dict[str, str] = {}
    for path, expected in FIXED_EVIDENCE.items():
        observed = digest(Path(path)) if (ROOT / path).is_file() else "MISSING"
        observed_hashes[path] = observed
        check(observed == expected, f"fixed_hash::{path}", {"expected": expected, "observed": observed}, findings)

    approval = load_yaml("research_control/approvals/approval-20260731-001.yaml")
    check(approval.get("approval_id") == APPROVAL_ID, "approval_id", approval.get("approval_id"), findings)
    check(approval.get("source_message_sha256") == "217f1cbcdf3c81deec5d7908b41d6f62e160b864b50d141e503df35e22f07620", "approval_message_hash", approval.get("source_message_sha256"), findings)
    check(approval.get("status") == "consumed", "approval_status", approval.get("status"), findings)
    check(approval.get("consumed_by") == JOB_ID, "approval_consumed_by", approval.get("consumed_by"), findings)
    check(approval.get("one_time_use") is True, "approval_one_time", approval.get("one_time_use"), findings)

    authorization = load_yaml(ARTIFACT_DIR / "human_authorization_p9_t09_gate_e_review_v1.yaml")
    check(authorization.get("controlling_handoff_id") == "handoff-0925", "authorization_handoff", authorization.get("controlling_handoff_id"), findings)
    check(authorization.get("positive_verdict_predetermined") is False, "authorization_not_predetermined", authorization.get("positive_verdict_predetermined"), findings)
    check(authorization.get("consumed_once") is True, "authorization_consumed_once", authorization.get("consumed_once"), findings)

    task = load_yaml(TASK_DIR / "00_TASK.yaml")
    job = load_yaml(TASK_DIR / "jobs/AJ-RT-20260731-004-001.yaml")
    role = load_yaml(TASK_DIR / "roles/gate-chair@0.1.0--RT-20260731-004.yaml")
    check(task.get("task_id") == TASK_ID and task.get("status") == "completed", "task_identity_status", {"id": task.get("task_id"), "status": task.get("status")}, findings)
    check(job.get("job_id") == JOB_ID and job.get("status") == "completed", "job_identity_status", {"id": job.get("job_id"), "status": job.get("status")}, findings)
    check(job.get("approval_id") == APPROVAL_ID and job.get("requires_human_gate") is False, "job_gate_satisfied", {"approval": job.get("approval_id"), "requires": job.get("requires_human_gate")}, findings)
    check(role.get("execution_role_ref") == ROLE_REF and role.get("human_gate_satisfied_by") == APPROVAL_ID, "role_identity_gate", {"ref": role.get("execution_role_ref"), "gate": role.get("human_gate_satisfied_by")}, findings)

    matrix = load_yaml(ARTIFACT_DIR / "p9_t09_gate_e_verdict_matrix_v1.yaml")
    check(matrix.get("decision_code") == DECISION_CODE, "matrix_decision", matrix.get("decision_code"), findings)
    check(matrix.get("overall_readiness") == "NOT_READY", "matrix_readiness", matrix.get("overall_readiness"), findings)
    counts = matrix.get("counts", {})
    check(counts == {"pass_or_narrow_pass": 3, "fail_or_not_established": 7, "deferred": 0, "total": 10, "executed_case_count": 6, "inconclusive_case_count": 6, "passed_case_count": 0, "qualifying_independent_replication_count": 0}, "matrix_counts", counts, findings)
    criteria = matrix.get("criteria", [])
    check(len(criteria) == 10 and {row.get("criterion_id") for row in criteria} == {f"GE-{i:02d}" for i in range(1, 11)}, "matrix_criteria", [row.get("criterion_id") for row in criteria], findings)
    disposition = matrix.get("protected_disposition", {})
    expected_dispositions = {
        "benchmark_promotion": "DENIED_NOT_READY",
        "exact_GR_recovery": "NOT_ESTABLISHED",
        "controlled_approximate_or_effective_GR_recovery": "NOT_ESTABLISHED",
        "completed_first_principles_derivation": "MAY_NOT_BE_CLAIMED",
    }
    check(all(disposition.get(key) == value for key, value in expected_dispositions.items()), "matrix_separate_dispositions", disposition, findings)

    predecessor_matrix = load_yaml("research_control/tasks/RT-20260731-001/artifacts/p9_t08_gate_e_readiness_matrix_v1.yaml")
    check(predecessor_matrix.get("overall_readiness") == "NOT_READY_NO_BENCHMARK_PASS_NO_QUALIFYING_INDEPENDENT_REPLICATION", "predecessor_readiness_preserved", predecessor_matrix.get("overall_readiness"), findings)
    check(predecessor_matrix.get("counts", {}).get("passed_case_count") == 0, "predecessor_zero_pass", predecessor_matrix.get("counts", {}), findings)
    replication = load_yaml("research_control/tasks/RT-20260731-001/artifacts/p9_t08_independent_replication_status_v1.yaml")
    check(replication.get("qualifying_independent_replication_completed") is False, "replication_absent", replication.get("qualifying_independent_replication_completed"), findings)

    scientific = load_yaml(ARTIFACT_DIR / "p9_t09_scientific_status_v1.yaml")
    package = scientific.get("package_status", {})
    check(scientific.get("decision_code") == DECISION_CODE, "scientific_decision", scientific.get("decision_code"), findings)
    check(package.get("benchmark_cases_inconclusive") == 6 and package.get("benchmark_cases_passed") == 0, "scientific_case_counts", package, findings)
    check(package.get("exact_GR_recovery_established") is False and package.get("controlled_approximate_GR_recovery_established") is False and package.get("completed_first_principles_derivation_established") is False, "scientific_recovery_boundaries", package, findings)

    child_math = load_yaml(ARTIFACT_DIR / "child_phys_math_p9_t09_gate_e_review.yaml")
    child_phil = load_yaml(ARTIFACT_DIR / "child_phys_phil_p9_t09_gate_e_review.yaml")
    conflict = load_yaml(ARTIFACT_DIR / "parent_conflict_review_p9_t09_gate_e_review.yaml")
    check(child_math.get("status") == "completed" and child_math.get("formal_result", {}).get("decision_code") == DECISION_CODE, "child_math", child_math.get("formal_result", {}), findings)
    check(child_phil.get("status") == "completed" and child_phil.get("philosophical_disposition", {}).get("benchmark_status_promoted") is False, "child_phil", child_phil.get("philosophical_disposition", {}), findings)
    check(conflict.get("status") == "resolved" and conflict.get("blocking_conflict_count") == 0 and conflict.get("unresolved_conflicts") == [], "conflict_resolution", conflict, findings)

    tex = (ROOT / ARTIFACT_DIR / "p9_t09_gate_e_decision_v1.tex").read_text(encoding="utf-8")
    normalized_tex = " ".join(tex.split())
    for marker in (
        "NOT\\_READY\\_BENCHMARK\\_AND\\_COMPLETED\\_DERIVATION\\_REQUIREMENTS\\_UNMET",
        "Benchmark promotion & denied; not ready",
        "Exact GR recovery & not established",
        "Controlled approximate/effective GR recovery & not established",
        "Completed first-principles derivation & may not be claimed",
        "not a global no-go theorem",
    ):
        check(
            marker in tex or marker in normalized_tex,
            f"tex_marker::{marker}",
            marker,
            findings,
        )

    registry_expectations = [
        ("registries/AGENT_JOB_REGISTRY.csv", "job_id", JOB_ID),
        ("registries/CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id", "CB-V21-P9-T09-PROTECTED-GATE-E-NOT-READY-001"),
        ("registries/DIRECTOR_DECISION_REGISTRY.csv", "decision_id", DECISION_ID),
        ("registries/RESEARCH_TASK_REGISTRY.csv", "task_id", TASK_ID),
        ("registries/ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref", ROLE_REF),
        ("registries/TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V21-P9-T09-PROTECTED-GATE-E-DECISION-V1"),
        ("registries/MARKDOWN_SOURCE_REGISTRY.csv", "object_id", "MD-V21-P9-T09-PARENT-FUSION-GATE-E-REVIEW-V1"),
    ]
    for path, key, value in registry_expectations:
        row = one_row(path, key, value)
        check(row is not None, f"registry::{path}::{value}", row or "missing_or_duplicate", findings)

    ledger = {row["burden_id"]: row for row in csv_rows("registries/DISTANCE_TO_GR_LEDGER.csv")}
    benchmark_row = ledger.get("benchmark_promotion", {})
    chair_row = ledger.get("gate_chair_status", {})
    check(benchmark_row.get("control_status") == "blocked", "ledger_benchmark_status", benchmark_row, findings)
    check(chair_row.get("control_status") == "human_gated", "ledger_gate_chair_status", chair_row, findings)
    check(benchmark_row.get("last_evidence_path") == "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex" and DECISION_CODE in benchmark_row.get("notes", ""), "ledger_benchmark_negative_decision", benchmark_row, findings)
    check(chair_row.get("last_evidence_path") == "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex" and "protected Gate E verdict is NOT READY" in chair_row.get("notes", ""), "ledger_gate_chair_negative_decision", chair_row, findings)

    program = load_yaml("research_control/program_state.yaml")
    check(program.get("active_task_id") == TASK_ID and program.get("latest_handoff_id") == HANDOFF_ID, "program_state", {"task": program.get("active_task_id"), "handoff": program.get("latest_handoff_id")}, findings)
    handoff = load_yaml("research_control/handoffs/handoff-0926.yaml") if (ROOT / "research_control/handoffs/handoff-0926.yaml").is_file() else {}
    check(handoff.get("handoff_id") == HANDOFF_ID and handoff.get("task_id") == TASK_ID, "handoff_identity", {"handoff": handoff.get("handoff_id"), "task": handoff.get("task_id")}, findings)
    check(handoff.get("claim_boundary", {}).get("benchmark_promotion_authorized") is False, "handoff_no_promotion", handoff.get("claim_boundary", {}), findings)

    failed = [finding for finding in findings if finding["status"] == "FAIL"]
    artifact_hashes = {
        str(path): digest(path)
        for path in sorted(
            [
                ARTIFACT_DIR / "human_authorization_p9_t09_gate_e_review_v1.yaml",
                ARTIFACT_DIR / "child_phys_math_p9_t09_gate_e_review.yaml",
                ARTIFACT_DIR / "child_phys_phil_p9_t09_gate_e_review.yaml",
                ARTIFACT_DIR / "parent_conflict_review_p9_t09_gate_e_review.yaml",
                ARTIFACT_DIR / "parent_fusion_notes_p9_t09_gate_e_review.md",
                ARTIFACT_DIR / "p9_t09_gate_e_decision_v1.tex",
                ARTIFACT_DIR / "p9_t09_gate_e_verdict_matrix_v1.yaml",
                ARTIFACT_DIR / "p9_t09_scientific_status_v1.yaml",
            ],
            key=str,
        )
    }
    report = {
        "schema_id": "p9_t09_gate_e_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "decision_code": DECISION_CODE,
        "validation_status": "PASS" if not failed else "FAIL",
        "check_count": len(findings),
        "pass_count": len(findings) - len(failed),
        "error_count": len(failed),
        "errors": [finding["finding_id"] for finding in failed],
        "findings": findings,
        "fixed_evidence_hashes": observed_hashes,
        "artifact_hashes": artifact_hashes,
        "authority_limits": {
            "benchmark_promotion_authorized": False,
            "exact_or_approximate_recovery_authorized": False,
            "completed_derivation_authorized": False,
            "publication_authorized": False,
            "push_authorized": False,
        },
    }
    compact = {
        "schema_id": "p9_t09_gate_e_compact_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "decision_code": DECISION_CODE,
        "validation_status": report["validation_status"],
        "check_count": report["check_count"],
        "pass_count": report["pass_count"],
        "error_count": report["error_count"],
        "errors": report["errors"],
        "benchmark_case_count": 6,
        "benchmark_pass_count": 0,
        "qualifying_independent_replication_count": 0,
        "benchmark_promotion": "DENIED_NOT_READY",
        "exact_GR_recovery": "NOT_ESTABLISHED",
        "controlled_approximate_GR_recovery": "NOT_ESTABLISHED",
        "completed_first_principles_derivation": "MAY_NOT_BE_CLAIMED",
        "artifact_hashes": artifact_hashes,
    }
    (ROOT / FULL_REPORT).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ROOT / COMPACT_REPORT).write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(compact, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
