#!/usr/bin/env python3
"""Validate the exact RT-20260729-004 P8-T01 allowlist-parity recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TARGET_JOB_ID = "AJ-RT-20260729-003-001"
TARGET_ROLE_REF = "theoretical-continuation-selector@0.1.0--RT-20260729-003"
TARGET_JOB_PATH = Path(
    "research_control/tasks/RT-20260729-003/jobs/AJ-RT-20260729-003-001.yaml"
)
TARGET_ROLE_PATH = Path(
    "research_control/tasks/RT-20260729-003/roles/"
    "theoretical-continuation-selector@0.1.0--RT-20260729-003.yaml"
)
AGENT_JOB_REGISTRY_PATH = Path("registries/AGENT_JOB_REGISTRY.csv")
ROLE_EXECUTION_REGISTRY_PATH = Path("registries/ROLE_EXECUTION_REGISTRY.csv")
REPORT_PATH = Path(
    "research_control/tasks/RT-20260729-004/artifacts/"
    "p8_t01_allowlist_parity_recovery_receipt.json"
)
EXPECTED_TARGET_JOB_SHA256 = (
    "dc7a44410b6a2349dcd87e148fa0e7da99afdfa0c0f149dd6269ad4b2fa17b98"
)
EXPECTED_ALLOWED_PATH_COUNT = 27
PROTECTED_HASHES = {
    "research_control/tasks/RT-20260729-003/jobs/completions/"
    "AJC-AJ-RT-20260729-003-001.yaml":
        "ed2ccb3170f09488f48f5edaeb025f55441f89f82f2bcfd481115017f1b72392",
    "research_control/handoffs/handoff-0899.yaml":
        "87c86cba003dc5c82897cbe6c569d3423530fa01160af7d3e6545cd8783435cd",
    "research_control/handoffs/handoff-0899.md":
        "54088d36c144aa019d2e0e5bcea2102b54568137da04b589968ca97f31569880",
    "research_control/tasks/RT-20260729-003/artifacts/"
    "gravitational_closure_route_decision_v1.yaml":
        "49af80465727038a7022371bac9dbe8fc4442b01a37fe14e9442873b1d8fa82f",
    "research_control/tasks/RT-20260729-003/artifacts/"
    "gravitational_closure_hypothesis_comparison_v1.yaml":
        "c337169583c60d1e4889e820ac0388c17ead67b190875268788805dae72b63d2",
    "research_control/tasks/RT-20260729-003/artifacts/"
    "frozen_gravitational_closure_alternatives_v1.yaml":
        "523f3db4b98b13089ea3f7f54d91a8907790117deb4da00d89319805953a5049",
    "research_control/tasks/RT-20260729-003/artifacts/"
    "gravitational_closure_route_selection_receipt.md":
        "5124e401a146b89c1a9019d45eb86d36a9151faca28354b9bc38a2ba011d5617",
    "research_control/tasks/RT-20260729-003/artifacts/"
    "gravitational_closure_route_selection_validation_v1.json":
        "04f76dc6ad09e0f1ceab033701739a048ab2728a8880db637e57ba37d41469da",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "ab63bd245a7822cc14f24caf436bce18d062d23839c3af203330cddd32c8c2ce",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return value


def registry_row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get(key) == value]
    if len(rows) != 1:
        raise ValueError(f"{path} has {len(rows)} rows for {key}={value}")
    return rows[0]


def split_paths(value: str) -> list[str]:
    return [] if not value else value.split(";")


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, Any] = {}

    target_job = load_yaml(REPO_ROOT / TARGET_JOB_PATH)
    target_role = load_yaml(REPO_ROOT / TARGET_ROLE_PATH)
    agent_row = registry_row(
        REPO_ROOT / AGENT_JOB_REGISTRY_PATH, "job_id", TARGET_JOB_ID
    )
    role_row = registry_row(
        REPO_ROOT / ROLE_EXECUTION_REGISTRY_PATH,
        "execution_role_ref",
        TARGET_ROLE_REF,
    )

    job_paths = target_job.get("allowed_write_paths")
    role_paths = target_role.get("allowed_write_paths")
    agent_row_paths = split_paths(agent_row.get("allowed_write_paths", ""))
    role_row_paths = split_paths(role_row.get("allowed_write_paths", ""))
    if not isinstance(job_paths, list) or not all(
        isinstance(item, str) for item in job_paths
    ):
        errors.append("target_job_allowed_write_paths_invalid")
        job_paths = []
    if not isinstance(role_paths, list) or not all(
        isinstance(item, str) for item in role_paths
    ):
        errors.append("target_role_allowed_write_paths_invalid")
        role_paths = []

    representations = {
        "agent_job": job_paths,
        "execution_role": role_paths,
        "agent_job_registry": agent_row_paths,
        "role_execution_registry": role_row_paths,
    }
    checks["allowed_write_path_counts"] = {
        name: len(paths) for name, paths in representations.items()
    }
    checks["allowed_write_paths_equal"] = all(
        paths == job_paths for paths in representations.values()
    )
    if not checks["allowed_write_paths_equal"]:
        errors.append("allowed_write_path_representations_differ")
    if len(job_paths) != EXPECTED_ALLOWED_PATH_COUNT:
        errors.append("target_job_allowed_write_path_count_mismatch")
    if len(set(job_paths)) != len(job_paths):
        errors.append("target_job_allowed_write_paths_duplicate")

    observed_job_sha256 = sha256(REPO_ROOT / TARGET_JOB_PATH)
    checks["target_job_sha256"] = observed_job_sha256
    checks["target_job_byte_preserved"] = (
        observed_job_sha256 == EXPECTED_TARGET_JOB_SHA256
    )
    if not checks["target_job_byte_preserved"]:
        errors.append("target_agent_job_bytes_changed")

    protected_results: dict[str, dict[str, Any]] = {}
    for relative_path, expected_hash in PROTECTED_HASHES.items():
        path = REPO_ROOT / relative_path
        observed_hash = sha256(path) if path.is_file() else None
        protected_results[relative_path] = {
            "expected_sha256": expected_hash,
            "observed_sha256": observed_hash,
            "match": observed_hash == expected_hash,
        }
        if observed_hash != expected_hash:
            errors.append(f"protected_hash_mismatch:{relative_path}")
    checks["protected_hashes"] = protected_results

    program_state = load_yaml(REPO_ROOT / "research_control/program_state.yaml")
    checks["active_task_id"] = program_state.get("active_task_id")
    checks["latest_handoff_id"] = program_state.get("latest_handoff_id")
    recovery = program_state.get("p8_t01_allowlist_parity_recovery")
    if not isinstance(recovery, dict):
        errors.append("program_state_recovery_block_missing")
        recovery = {}
    checks["p8_t01_reexecuted"] = recovery.get("p8_t01_reexecuted")
    checks["p8_t02_executed"] = recovery.get("p8_t02_executed")
    checks["scientific_claims_changed"] = recovery.get("scientific_claims_changed")
    checks["distance_to_gr_delta_changed"] = recovery.get(
        "distance_to_gr_delta_changed"
    )
    if checks["active_task_id"] != "RT-20260729-004":
        errors.append("active_task_id_mismatch")
    if checks["latest_handoff_id"] != "handoff-0900":
        errors.append("latest_handoff_id_mismatch")
    if checks["p8_t01_reexecuted"] is not False:
        errors.append("p8_t01_execution_boundary_changed")
    if checks["p8_t02_executed"] is not False:
        errors.append("p8_t02_execution_boundary_changed")
    if checks["scientific_claims_changed"] is not False:
        errors.append("scientific_claim_boundary_changed")
    if checks["distance_to_gr_delta_changed"] is not False:
        errors.append("distance_to_gr_boundary_changed")

    return {
        "schema_id": "p8_t01_allowlist_parity_recovery_receipt_v1",
        "task_id": "RT-20260729-004",
        "job_id": "AJ-RT-20260729-004-001",
        "source_job_id": TARGET_JOB_ID,
        "strategy_id": "repair_p8_t01_allowlist_parity_after_checkpoint_v1",
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "validation_status": "PASS" if not errors else "FAIL",
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "p8_t01_reexecuted": False,
            "p8_t02_executed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        destination = REPO_ROOT / REPORT_PATH
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        destination = REPO_ROOT / REPORT_PATH
        if not destination.is_file():
            report["errors"].append("stored_report_missing")
            report["error_count"] = len(report["errors"])
            report["validation_status"] = "FAIL"
        else:
            stored = json.loads(destination.read_text(encoding="utf-8"))
            if stored != report:
                report["errors"].append("stored_report_drift")
                report["error_count"] = len(report["errors"])
                report["validation_status"] = "FAIL"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
