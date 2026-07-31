#!/usr/bin/env python3
"""Validate the exact generation-187 checkpoint allowlist recovery."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260731-003"
JOB_ID = "AJ-RT-20260731-003-001"
ROLE_REF = "process-integrity-auditor@0.1.0--RT-20260731-003"
JOB_PATH = Path(
    "research_control/tasks/RT-20260731-003/jobs/AJ-RT-20260731-003-001.yaml"
)
ROLE_PATH = Path(
    "research_control/tasks/RT-20260731-003/roles/"
    "process-integrity-auditor@0.1.0--RT-20260731-003.yaml"
)
REPORT_PATH = Path(
    "research_control/tasks/RT-20260731-003/artifacts/"
    "p9_t08_distance_ledger_checkpoint_allowlist_recovery_receipt.json"
)
AGENT_JOB_REGISTRY_PATH = Path("registries/AGENT_JOB_REGISTRY.csv")
ROLE_EXECUTION_REGISTRY_PATH = Path("registries/ROLE_EXECUTION_REGISTRY.csv")
REQUIRED_LEDGER_PATH = "registries/DISTANCE_TO_GR_LEDGER.csv"
EXPECTED_ROUTE_SHA256 = (
    "c2a5a1437447e91263073904fe60604a1ee4a150102710e3bac20ddba7872dbc"
)
EXPECTED_MANIFEST_SHA256 = (
    "430966fe77b99ef0e396106b54bd03b8ea7c721a954ecae1e2b51300e2580921"
)
EXPECTED_FAILURE_EVIDENCE_SHA256 = (
    "a27d4ffee08261b44ad0056d6ddb0d555c626c34fec9a506d511f61d04af5bd5"
)
EXPECTED_BLOCKER_FINGERPRINT = (
    "d87f7d0a1fb661acfe1d705f4bebc5ca3a865e0be75501d6f8cf4f3da099da31"
)
EXPECTED_STRATEGY_ID = (
    "repair_rt_20260731_002_distance_ledger_checkpoint_allowlist_v1"
)
PROTECTED_HASHES = {
    "research_control/tasks/RT-20260731-002/00_TASK.yaml":
        "3f9d30df57852fa420354d4d8cec3060c8cb1a07f0d229c352940c628e41cc50",
    "research_control/tasks/RT-20260731-002/DDR-20260731-002.md":
        "bde6917253444416db1750ce9777724c2edf4b0d5c671b3e0debf3c0089b2f10",
    "research_control/tasks/RT-20260731-002/jobs/AJ-RT-20260731-002-001.yaml":
        "7fdffaca3677179e2d96383e788dafbe4b80c777854cfe25bed3fcb945a66f69",
    "research_control/tasks/RT-20260731-002/jobs/completions/"
    "AJC-AJ-RT-20260731-002-001.yaml":
        "831568d91dc239c57f40b6d307606e218121759602bde060e73f2c31fe91d981",
    "research_control/tasks/RT-20260731-002/roles/"
    "process-integrity-auditor@0.1.0--RT-20260731-002.yaml":
        "660e3f494aa3f2c2272630550224f80876137ee7905be9df7d0e9f5cc7922d1e",
    "research_control/handoffs/handoff-0924.yaml":
        "bac3da3b29573721d1ab93a145a2aafbe55b5680c29306baee5813d4729b9758",
    "research_control/handoffs/handoff-0924.md":
        "d2665c24013bc481621cb2d5e9a438580eb5b06ff85132c5fed4fa4e795db368",
    REQUIRED_LEDGER_PATH:
        "1e081225cd047aa02a9fd0d53582c4625be5e4cd019df3f5cd6719502d1a241e",
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


def git_changed_paths() -> list[str]:
    output = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO_ROOT,
        text=True,
    )
    return sorted(line[3:] for line in output.splitlines())


def allowed(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/**") and path.startswith(pattern[:-3] + "/"):
            return True
        if fnmatch.fnmatchcase(path, pattern):
            return True
    return False


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, Any] = {}

    job = load_yaml(REPO_ROOT / JOB_PATH)
    role = load_yaml(REPO_ROOT / ROLE_PATH)
    agent_row = registry_row(
        REPO_ROOT / AGENT_JOB_REGISTRY_PATH, "job_id", JOB_ID
    )
    role_row = registry_row(
        REPO_ROOT / ROLE_EXECUTION_REGISTRY_PATH,
        "execution_role_ref",
        ROLE_REF,
    )

    job_paths = job.get("allowed_write_paths")
    role_paths = role.get("allowed_write_paths")
    if not isinstance(job_paths, list) or not all(
        isinstance(item, str) for item in job_paths
    ):
        errors.append("agent_job_allowed_write_paths_invalid")
        job_paths = []
    if not isinstance(role_paths, list) or not all(
        isinstance(item, str) for item in role_paths
    ):
        errors.append("execution_role_allowed_write_paths_invalid")
        role_paths = []
    representations = {
        "agent_job": job_paths,
        "execution_role": role_paths,
        "agent_job_registry": split_paths(agent_row.get("allowed_write_paths", "")),
        "role_execution_registry": split_paths(
            role_row.get("allowed_write_paths", "")
        ),
    }
    checks["allowed_write_path_counts"] = {
        name: len(paths) for name, paths in representations.items()
    }
    checks["allowed_write_paths_equal"] = all(
        paths == job_paths for paths in representations.values()
    )
    if not checks["allowed_write_paths_equal"]:
        errors.append("allowed_write_path_representations_differ")
    checks["ledger_path_count"] = job_paths.count(REQUIRED_LEDGER_PATH)
    if checks["ledger_path_count"] != 1:
        errors.append("distance_ledger_not_admitted_exactly_once")
    if len(job_paths) != len(set(job_paths)):
        errors.append("agent_job_allowed_write_paths_duplicate")

    changed_paths = git_changed_paths()
    disallowed = [path for path in changed_paths if not allowed(path, job_paths)]
    checks["changed_path_count"] = len(changed_paths)
    checks["disallowed_changed_paths"] = disallowed
    if disallowed:
        errors.append("live_changed_path_outside_recovery_allowlist")

    source_job = load_yaml(
        REPO_ROOT
        / "research_control/tasks/RT-20260731-002/jobs/"
        "AJ-RT-20260731-002-001.yaml"
    )
    checks["source_job_ledger_path_count"] = list(
        source_job.get("allowed_write_paths", [])
    ).count(REQUIRED_LEDGER_PATH)
    if checks["source_job_ledger_path_count"] != 0:
        errors.append("immutable_source_job_allowlist_changed")

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

    checks["route_sha256"] = job.get("immutable_route_sha256")
    checks["strategy_id"] = job.get("route_label")
    checks["blocker_fingerprint"] = job.get("route_blocker_fingerprint")
    checks["dirty_manifest_sha256"] = job.get("dirty_state_manifest_sha256")
    checks["failure_evidence_sha256"] = job.get("failed_gate_evidence_sha256")
    if checks["route_sha256"] != EXPECTED_ROUTE_SHA256:
        errors.append("immutable_route_sha256_mismatch")
    if checks["strategy_id"] != EXPECTED_STRATEGY_ID:
        errors.append("strategy_id_mismatch")
    if checks["blocker_fingerprint"] != EXPECTED_BLOCKER_FINGERPRINT:
        errors.append("blocker_fingerprint_mismatch")
    if checks["dirty_manifest_sha256"] != EXPECTED_MANIFEST_SHA256:
        errors.append("dirty_manifest_sha256_mismatch")
    if checks["failure_evidence_sha256"] != EXPECTED_FAILURE_EVIDENCE_SHA256:
        errors.append("failure_evidence_sha256_mismatch")

    program_state = load_yaml(REPO_ROOT / "research_control/program_state.yaml")
    recovery = program_state.get(
        "p9_t08_distance_ledger_checkpoint_allowlist_recovery"
    )
    if not isinstance(recovery, dict):
        errors.append("program_state_recovery_block_missing")
        recovery = {}
    checks["active_task_id"] = program_state.get("active_task_id")
    checks["latest_handoff_id"] = program_state.get("latest_handoff_id")
    checks["next_worker_skill"] = program_state.get("next_worker_skill")
    checks["p9_t08_reexecuted"] = recovery.get("p9_t08_reexecuted")
    checks["p9_t09_executed"] = recovery.get("p9_t09_executed")
    checks["scientific_claims_changed"] = recovery.get(
        "scientific_claims_changed"
    )
    checks["distance_to_gr_delta_changed"] = recovery.get(
        "distance_to_gr_delta_changed"
    )
    checks["ledger_changed_by_recovery"] = recovery.get(
        "ledger_changed_by_recovery"
    )
    if checks["active_task_id"] != TASK_ID:
        errors.append("active_task_id_mismatch")
    if checks["latest_handoff_id"] != "handoff-0925":
        errors.append("latest_handoff_id_mismatch")
    if checks["next_worker_skill"] != "none_until_human_authorization":
        errors.append("protected_next_worker_boundary_changed")
    for key in (
        "p9_t08_reexecuted",
        "p9_t09_executed",
        "scientific_claims_changed",
        "distance_to_gr_delta_changed",
        "ledger_changed_by_recovery",
    ):
        if checks[key] is not False:
            errors.append(f"authority_boundary_changed:{key}")

    return {
        "schema_id": "p9_t08_distance_ledger_checkpoint_allowlist_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_task_id": "RT-20260731-002",
        "source_job_id": "AJ-RT-20260731-002-001",
        "strategy_id": EXPECTED_STRATEGY_ID,
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "validation_status": "PASS" if not errors else "FAIL",
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "ledger_changed_by_recovery": False,
            "p9_t08_reexecuted": False,
            "p9_t09_executed": False,
            "gate_e_verdict_authorized": False,
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
