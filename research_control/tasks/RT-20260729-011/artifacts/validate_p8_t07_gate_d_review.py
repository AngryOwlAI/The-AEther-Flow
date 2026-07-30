#!/usr/bin/env python3
"""Validate the bounded P8-T07 protected Gate D decision packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260729-011"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
REPORT_PATH = ARTIFACT_ROOT / "p8_t07_gate_d_validation_v1.json"
VERDICT = "NOT_READY_EINSTEIN_SECTOR_DERIVATION_REQUIREMENTS_UNMET"

FIXED_HASHES = {
    "research_control/tasks/RT-20260729-005/artifacts/local_effective_action_closure_target_v1.tex":
        "13402c3d80f114b643a0216484b0ba775a2f02d1f0733f33d8cf86044e6add96",
    "research_control/tasks/RT-20260729-005/artifacts/local_effective_action_assumption_envelope_v1.yaml":
        "da939b16a0cb4da082068ab9954d11c4c7a7a658e746c50295dc20347fc82a65",
    "research_control/tasks/RT-20260729-006/artifacts/finite_source_closure_constraint_candidate_v1.tex":
        "82dd10d8e91be3781ca4f21e7f9fbf2ce1a9108ae7191db22fed9dfe6086f2fa",
    "research_control/tasks/RT-20260729-007/artifacts/finite_source_field_equation_identity_v1.tex":
        "12a1cfae87cd673241aefe88144ab974b49fc3bad284a81baff90b2e806d5168",
    "research_control/tasks/RT-20260729-008/artifacts/finite_constraint_dynamical_viability_stress_v1.tex":
        "ddd39764c3b6f86e86574458b885e90271a2b044d1d141ae931723e80599acb1",
    "research_control/tasks/RT-20260729-009/artifacts/p8_t06_gate_d_readiness_matrix_v1.yaml":
        "ca3f9252d1fe8e2e0814110dbc6a25b274f710d9220ec0e9d7933e82f3b1b3d0",
    "research_control/tasks/RT-20260729-009/artifacts/p8_t06_closure_red_team_review_v1.yaml":
        "ea95f6c5a89c36ee827194501db08b53e570e9f2badbf77e10320bbc813fbde7",
    "research_control/tasks/RT-20260729-009/artifacts/blind_mathematical_review_status_v1.yaml":
        "31df9d0532a29dc3a716d2c3e5059839f258e5346952efb96d9fe676029e13f0",
    "research_control/tasks/RT-20260729-009/artifacts/independent_review_human_action_v1.yaml":
        "b0e6cae3efcf5501a0f751e21aa1e96478751cd869364a9507dfac4f9d7a1cba",
}

REQUIRED_OUTPUTS = [
    "research_control/approvals/approval-20260729-002.yaml",
    "research_control/tasks/RT-20260729-011/00_TASK.yaml",
    "research_control/tasks/RT-20260729-011/DDR-20260729-011.md",
    "research_control/tasks/RT-20260729-011/roles/gate-chair@0.1.0--RT-20260729-011.yaml",
    "research_control/tasks/RT-20260729-011/jobs/AJ-RT-20260729-011-001.yaml",
    "research_control/tasks/RT-20260729-011/artifacts/human_authorization_p8_t07_gate_d_review_v1.yaml",
    "research_control/tasks/RT-20260729-011/artifacts/child_phys_math_p8_t07_gate_d_review.yaml",
    "research_control/tasks/RT-20260729-011/artifacts/child_phys_phil_p8_t07_gate_d_review.yaml",
    "research_control/tasks/RT-20260729-011/artifacts/parent_conflict_review_p8_t07_gate_d_review.yaml",
    "research_control/tasks/RT-20260729-011/artifacts/parent_fusion_notes_p8_t07_gate_d_review.md",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_verdict_matrix_v1.yaml",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_scientific_status_v1.yaml",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_compact_receipt_v1.json",
    "research_control/tasks/RT-20260729-011/jobs/completions/AJC-AJ-RT-20260729-011-001.yaml",
    "research_control/tasks/RT-20260729-011/documentation_impact.yaml",
    "research_control/handoffs/handoff-0907.yaml",
    "research_control/handoffs/handoff-0907.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(rel_path: str) -> dict[str, Any]:
    value = yaml.safe_load((REPO_ROOT / rel_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{rel_path} is not a YAML mapping")
    return value


def csv_matches(rel_path: str, key: str, value: str) -> list[dict[str, str]]:
    with (REPO_ROOT / rel_path).open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get(key) == value]


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"name": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    for rel_path in REQUIRED_OUTPUTS:
        check(f"output_exists:{rel_path}", (REPO_ROOT / rel_path).is_file(), rel_path)

    for rel_path, expected in FIXED_HASHES.items():
        path = REPO_ROOT / rel_path
        actual = sha256(path) if path.is_file() else ""
        check(f"fixed_hash:{rel_path}", actual == expected, f"expected={expected} actual={actual}")

    approval = load_yaml("research_control/approvals/approval-20260729-002.yaml")
    check("approval_exact_text", approval.get("source_message_text") == "I authorize it all", "exact user text")
    check("approval_consumed_once", approval.get("status") == "consumed" and approval.get("one_time_use") is True,
          "one-time approval consumed")
    check("approval_scope", approval.get("decision_code") ==
          "AUTHORIZED_SCOPED_GATE_D_REVIEW_EVIDENCE_BOUND_VERDICT_ONLY", "bounded decision authority")

    job = load_yaml("research_control/tasks/RT-20260729-011/jobs/AJ-RT-20260729-011-001.yaml")
    role = load_yaml("research_control/tasks/RT-20260729-011/roles/gate-chair@0.1.0--RT-20260729-011.yaml")
    check("one_worker_invocation", job.get("goal_receipt", {}).get("worker_invocation_count") == 1,
          "single consumed worker invocation")
    check("generation_165", job.get("goal_receipt", {}).get("generation") == 165, "relay generation")
    check("route_hash", job.get("immutable_route_sha256") ==
          "dc0b7b9ef680a242ef144504e7af0f762d78109f088d208d6e0ba24763b6086a",
          "immutable route")
    check("allowlist_order_parity", job.get("allowed_write_paths") == role.get("allowed_write_paths"),
          "AgentJob and role overlay write paths match exactly")

    matrix = load_yaml("research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_verdict_matrix_v1.yaml")
    criteria = matrix.get("criteria", [])
    check("matrix_verdict", matrix.get("decision_code") == VERDICT and matrix.get("overall_readiness") == "NOT_READY",
          "protected negative verdict")
    check("matrix_ten_criteria", isinstance(criteria, list) and len(criteria) == 10, "ten Gate D criteria")
    check("matrix_unique_ids", [item.get("criterion_id") for item in criteria] ==
          [f"GD-{index:02d}" for index in range(1, 11)], "ordered GD-01 through GD-10")
    check("matrix_counts", matrix.get("counts") == {
        "pass_or_narrow_pass": 4, "fail_or_not_established": 6, "deferred": 0, "total": 10
    }, "four narrow passes and six unmet criteria")

    status = load_yaml("research_control/tasks/RT-20260729-011/artifacts/p8_t07_scientific_status_v1.yaml")
    check("scientific_status_verdict", status.get("decision_code") == VERDICT, "verdict parity")
    disposition = status.get("scientific_disposition", {})
    check("no_distance_delta", disposition.get("distance_to_gr_changed") is False, "no GR-distance reduction")
    check("open_continuation", disposition.get("not_a_global_no_go") is True and
          disposition.get("future_material_repair_open") is True, "local freeze only")

    for child_name in ("child_phys_math_p8_t07_gate_d_review.yaml", "child_phys_phil_p8_t07_gate_d_review.yaml"):
        child = load_yaml(f"research_control/tasks/RT-20260729-011/artifacts/{child_name}")
        check(f"child_completed:{child_name}", child.get("status") == "completed", "child perspective completed")
        check(f"child_subagent_count:{child_name}", child.get("subagent_count") == 2, "two internal subagents")
        check(f"child_verdict:{child_name}", VERDICT in json.dumps(child), "verdict present")

    conflict = load_yaml(
        "research_control/tasks/RT-20260729-011/artifacts/parent_conflict_review_p8_t07_gate_d_review.yaml"
    )
    check("conflicts_resolved", conflict.get("status") == "resolved" and
          conflict.get("unresolved_conflicts") == [], "no unresolved parent-child conflict")

    tex = (ARTIFACT_ROOT / "p8_t07_gate_d_decision_v1.tex").read_text(encoding="utf-8")
    for token in ("NOT\\_READY", "blocked", "P9-T01", "global no-go", "independent"):
        check(f"tex_token:{token}", token in tex, token)

    receipt = json.loads((ARTIFACT_ROOT / "p8_t07_gate_d_compact_receipt_v1.json").read_text(encoding="utf-8"))
    check("compact_receipt_verdict", receipt.get("decision_code") == VERDICT, "compact verdict")
    check("compact_receipt_no_promotion",
          receipt.get("authority_limits", {}).get("physics_promotion_authorized") is False,
          "promotion remains blocked")

    registry_specs = [
        ("registries/RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260729-011"),
        ("registries/DIRECTOR_DECISION_REGISTRY.csv", "decision_id", "DDR-20260729-011"),
        ("registries/AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260729-011-001"),
        ("registries/ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref",
         "gate-chair@0.1.0--RT-20260729-011"),
        ("registries/CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id",
         "CB-V21-P8-T07-PROTECTED-GATE-D-NOT-READY-001"),
        ("registries/TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V21-P8-T07-GATE-D-DECISION-V1"),
    ]
    for rel_path, key, value in registry_specs:
        matches = csv_matches(rel_path, key, value)
        check(f"registry_row:{value}", len(matches) == 1, f"count={len(matches)}")

    ledger_rows = csv_matches("registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "einstein_equations")
    check("ledger_unique_einstein_row", len(ledger_rows) == 1, f"count={len(ledger_rows)}")
    if ledger_rows:
        check("ledger_gate_d_path", ledger_rows[0].get("last_evidence_path") ==
              "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex",
              "protected decision is latest evidence")
        check("ledger_not_ready", VERDICT in ledger_rows[0].get("notes", ""), "verdict in ledger notes")

    handoff = load_yaml("research_control/handoffs/handoff-0907.yaml")
    check("handoff_next", handoff.get("next_plan_task_id") == "P9-T01", "protocol design follows checkpoint")
    check("handoff_verdict", VERDICT in json.dumps(handoff), "handoff preserves verdict")
    state = load_yaml("research_control/program_state.yaml")
    check("program_active_task", state.get("active_task_id") == "RT-20260729-011", "active task")
    check("program_latest_handoff", state.get("latest_handoff_id") == "handoff-0907", "latest handoff")

    failures = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "p8_t07_gate_d_validation_v1",
        "task_id": "RT-20260729-011",
        "job_id": "AJ-RT-20260729-011-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failures),
        "decision_code": VERDICT,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['status']}: {report['check_count'] - report['failed_check_count']} of "
              f"{report['check_count']} checks pass")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
