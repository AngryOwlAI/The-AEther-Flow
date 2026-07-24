#!/usr/bin/env python3
"""Validate the exact RT-20260724-008 allowlist-identity recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TARGET_JOB_ID = "AJ-RT-20260724-007-001"
TARGET_ROLE_REF = "validator-engineer@0.2.0--RT-20260724-007"
TARGET_JOB_PATH = Path(
    "research_control/tasks/RT-20260724-007/jobs/AJ-RT-20260724-007-001.yaml"
)
TARGET_ROLE_PATH = Path(
    "research_control/tasks/RT-20260724-007/roles/"
    "validator-engineer@0.2.0--RT-20260724-007.yaml"
)
AGENT_JOB_REGISTRY_PATH = Path("registries/AGENT_JOB_REGISTRY.csv")
ROLE_EXECUTION_REGISTRY_PATH = Path("registries/ROLE_EXECUTION_REGISTRY.csv")
REPORT_PATH = Path(
    "research_control/tasks/RT-20260724-008/artifacts/"
    "active_job_allowlist_contract_recovery_receipt.json"
)
EXPECTED_TARGET_JOB_SHA256 = (
    "e459320a6cf27f7b52aa1448371b78c847b41c0aaf03e4b5fb7e759494172737"
)
EXPECTED_ALLOWED_PATH_COUNT = 49
REQUIRED_EXPLICIT_REGISTRY_PATHS = [
    "registries/AGENT_JOB_REGISTRY.csv",
    "registries/CLAIM_BOUNDARY_REGISTRY.csv",
    "registries/DIRECTOR_DECISION_REGISTRY.csv",
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "registries/MARKDOWN_SOURCE_REGISTRY.csv",
    "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv",
    "registries/RESEARCH_TASK_REGISTRY.csv",
    "registries/ROLE_EXECUTION_REGISTRY.csv",
    "registries/TEX_SOURCE_REGISTRY.csv",
    "registries/CONTENT_SEMANTIC_REGISTRY*",
    "registries/FILE_OBJECT_REGISTRY*",
    "registries/OBJECT_RELATIONSHIP_REGISTRY*",
    "registries/OBSIDIAN_VAULT_REGISTRY*",
    "registries/WIKI_ARTIFACT_REGISTRY*",
]
PROTECTED_HASHES = {
    "research_control/handoffs/handoff-0857.yaml":
        "c4a4621f6cf027c7dc909a9c2414824f2817ae522864a474972c13c382051c4d",
    "research_control/handoffs/handoff-0857.md":
        "4a4964beb7864773e2f71bbf884a89b8dd22af7cbe3531fac4cd4829284ebd04",
    "research_control/tasks/RT-20260724-007/jobs/completions/"
    "AJC-AJ-RT-20260724-007-001.yaml":
        "8ee9d5b739b25a95907660118d1b857c3cf4bd0d015336da2610d063d335ec7d",
    "research_control/tasks/RT-20260724-007/artifacts/"
    "validation_blocker_checkpoint_active_job_allowlist_contract_drift_v1.yaml":
        "504d0c5682060fbb1b17bea4c1bd79c09b20b1cf4398cb773ff8d73401087cfd",
    "research_control/tasks/RT-20260724-007/artifacts/"
    "p4_t06_checkpoint_allowlist_control_failure_v1.yaml":
        "b424062a2ab7b4b0d352649bfd8ebe704e2a3f680084c27745525001830b8fd0",
    "research_control/tasks/RT-20260724-007/artifacts/"
    "repository_test_contract_recovery_receipt.json":
        "76560fa286a58aa57e322105da8c746e0c3a871b261556911dede242e3a8bd1c",
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

    broad_glob_present = {
        name: "registries/**" in paths for name, paths in representations.items()
    }
    checks["broad_registry_glob_present"] = broad_glob_present
    if any(broad_glob_present.values()):
        errors.append("broad_registries_glob_present")
    checks["required_explicit_registry_paths_present"] = {
        name: all(item in paths for item in REQUIRED_EXPLICIT_REGISTRY_PATHS)
        for name, paths in representations.items()
    }
    if not all(checks["required_explicit_registry_paths_present"].values()):
        errors.append("required_explicit_registry_path_missing")

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
    recovery = program_state.get("p4_t05_active_job_allowlist_contract_recovery")
    if not isinstance(recovery, dict):
        errors.append("program_state_recovery_block_missing")
        recovery = {}
    checks["p4_t06_executed"] = recovery.get("p4_t06_executed")
    checks["scientific_claims_changed"] = recovery.get("scientific_claims_changed")
    checks["distance_to_gr_delta_changed"] = recovery.get(
        "distance_to_gr_delta_changed"
    )
    if checks["active_task_id"] != "RT-20260724-008":
        errors.append("active_task_id_mismatch")
    if checks["p4_t06_executed"] is not False:
        errors.append("p4_t06_execution_boundary_changed")
    if checks["scientific_claims_changed"] is not False:
        errors.append("scientific_claim_boundary_changed")
    if checks["distance_to_gr_delta_changed"] is not False:
        errors.append("distance_to_gr_boundary_changed")

    return {
        "schema_id": "active_job_allowlist_contract_recovery_receipt_v1",
        "task_id": "RT-20260724-008",
        "job_id": "AJ-RT-20260724-008-001",
        "source_job_id": TARGET_JOB_ID,
        "strategy_id": "repair_p4_t05_checkpoint_active_job_allowlist_contract_drift_v1",
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "validation_status": "PASS" if not errors else "FAIL",
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "p4_t06_executed": False,
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
