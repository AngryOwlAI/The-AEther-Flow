#!/usr/bin/env python3
"""Validate the bounded P4-T05 lifecycle-status reconciliation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control.ordinary_route_guard import (  # noqa: E402
    evaluate_agent_job_route_admission,
    evaluate_research_handoff_guard,
)

RECEIPT_PATH = Path(__file__).with_name(
    "p4_t05_handoff_route_guard_status_reconciliation_receipt.json"
)
RT007_TASK_PATH = REPO_ROOT / "research_control/tasks/RT-20260724-007/00_TASK.yaml"
TASK_REGISTRY_PATH = REPO_ROOT / "registries/RESEARCH_TASK_REGISTRY.csv"
HANDOFF_0857_PATH = REPO_ROOT / "research_control/handoffs/handoff-0857.yaml"
RT008_JOB_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260724-008/jobs/AJ-RT-20260724-008-001.yaml"
)
PROGRAM_STATE_PATH = REPO_ROOT / "research_control/program_state.yaml"

EXPECTED_HASHES = {
    "research_control/tasks/RT-20260724-007/jobs/AJ-RT-20260724-007-001.yaml":
        "e459320a6cf27f7b52aa1448371b78c847b41c0aaf03e4b5fb7e759494172737",
    "research_control/tasks/RT-20260724-007/jobs/completions/AJC-AJ-RT-20260724-007-001.yaml":
        "8ee9d5b739b25a95907660118d1b857c3cf4bd0d015336da2610d063d335ec7d",
    "research_control/handoffs/handoff-0857.yaml":
        "c4a4621f6cf027c7dc909a9c2414824f2817ae522864a474972c13c382051c4d",
    "research_control/tasks/RT-20260724-008/jobs/AJ-RT-20260724-008-001.yaml":
        "83ca2e5e3cdecfbe01cd36f2e6227fe4fea7272fa94197949e0b29a6c3fd9c62",
    "research_control/tasks/RT-20260724-008/jobs/completions/AJC-AJ-RT-20260724-008-001.yaml":
        "05a29a627ba393e78166c4b41a84d2851496c80ef5e18c0d542f8b69db887fd5",
    "research_control/tasks/RT-20260724-008/artifacts/validation_blocker_precheckpoint_handoff_0857_route_guard_dependency_drift_v1.yaml":
        "ba90f9bb7c8fd9a8b1e989f2fc94fb8b8227c7b735064070e6907d359743bcb7",
    "research_control/tasks/RT-20260724-008/artifacts/p4_t06_precheckpoint_handoff_0857_route_guard_control_failure_v1.yaml":
        "7e1b1e6454446d11656b0008954bccdc0045488e0fcb117da9af8490b9f154e7",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} is not a mapping")
    return value


def load_task_row() -> dict[str, str]:
    with TASK_REGISTRY_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    matches = [row for row in rows if row.get("task_id") == "RT-20260724-007"]
    if len(matches) != 1:
        raise ValueError("RT-20260724-007 registry row is not unique")
    return matches[0]


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    hashes: dict[str, str] = {}
    for relative_path, expected in EXPECTED_HASHES.items():
        path = REPO_ROOT / relative_path
        actual = sha256(path) if path.is_file() and not path.is_symlink() else "missing"
        hashes[relative_path] = actual
        if actual != expected:
            errors.append(f"immutable_hash_mismatch:{relative_path}")

    task = load_yaml(RT007_TASK_PATH)
    row = load_task_row()
    expected_task_fields = {
        "task_id": "RT-20260724-007",
        "status": "completed",
        "validation_status": "FAIL",
        "closed_at": "2026-07-24T20:13:35Z",
        "closure_status":
            "p4_t05_repository_test_contract_recovery_pass_checkpoint_blocked_active_job_allowlist_contract_drift",
    }
    for field_name, expected in expected_task_fields.items():
        if str(task.get(field_name, "")) != expected:
            errors.append(f"rt007_task_field_mismatch:{field_name}")

    expected_row_fields = {
        "task_id": "RT-20260724-007",
        "task_path": "research_control/tasks/RT-20260724-007",
        "task_type":
            "project_system_p4_t05_checkpoint_repository_test_contract_drift_recovery",
        "status": "completed",
        "current_decision_id": "DDR-20260724-007",
        "current_job_id": "AJ-RT-20260724-007-001",
        "parent_task_id": "RT-20260724-006",
        "created_at": "2026-07-24T18:55:34Z",
        "updated_at": "2026-07-24T20:13:35Z",
        "closed_at": "2026-07-24T20:13:35Z",
        "closure_status":
            "p4_t05_repository_test_contract_recovery_pass_checkpoint_blocked_active_job_allowlist_contract_drift",
        "requires_human_gate": "false",
    }
    for field_name, expected in expected_row_fields.items():
        if row.get(field_name, "") != expected:
            errors.append(f"rt007_registry_field_mismatch:{field_name}")

    handoff = load_yaml(HANDOFF_0857_PATH)
    guard_result = evaluate_research_handoff_guard(handoff, REPO_ROOT)
    if guard_result.get("status") != "PASS":
        errors.extend(
            f"handoff_0857_guard:{value}" for value in guard_result.get("errors", [])
        )
    ready_ids = guard_result.get("ready_science_plan_task_ids", [])
    if ready_ids != ["P4-T06"]:
        errors.append(f"handoff_0857_ready_ids_mismatch:{ready_ids!r}")

    rt008_job = load_yaml(RT008_JOB_PATH)
    admission_result = evaluate_agent_job_route_admission(
        rt008_job,
        created_at="2026-07-24T20:50:40Z",
        repo_root=REPO_ROOT,
    )
    if admission_result.get("status") != "PASS":
        errors.extend(
            f"rt008_admission:{value}"
            for value in admission_result.get("errors", [])
        )

    program_state = load_yaml(PROGRAM_STATE_PATH)
    rt008_state = program_state.get("p4_t05_active_job_allowlist_contract_recovery")
    if not isinstance(rt008_state, dict) or rt008_state.get("p4_t06_executed") is not False:
        errors.append("program_state_p4_t06_nonexecution_not_preserved")
    if handoff.get("selected_next_route", {}).get("executed") is not False:
        errors.append("handoff_0857_p4_t06_nonexecution_not_preserved")

    return {
        "schema_id": "p4_t05_handoff_route_guard_status_reconciliation_receipt_v1",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260724-009",
        "job_id": "AJ-RT-20260724-009-001",
        "strategy_id":
            "reconcile_p4_t05_implemented_checkpoint_blocked_status_with_handoff_0857_route_guard_v1",
        "rt007_task_status": str(task.get("status", "")),
        "rt007_validation_status": str(task.get("validation_status", "")),
        "rt007_registry_status": row.get("status", ""),
        "handoff_0857_guard_status": guard_result.get("status", ""),
        "handoff_0857_ready_science_plan_task_ids": ready_ids,
        "rt008_admission_status": admission_result.get("status", ""),
        "immutable_hash_mismatch_count": sum(
            actual != EXPECTED_HASHES[path] for path, actual in hashes.items()
        ),
        "p4_t06_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "immutable_hashes": hashes,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        RECEIPT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
