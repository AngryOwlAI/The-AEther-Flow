#!/usr/bin/env python3
"""Validate the exact RT-20260729-010 P8-T06 allowlist-order recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TARGET_JOB_ID = "AJ-RT-20260729-009-001"
TARGET_ROLE_REF = "external-red-team-reviewer@0.1.0--RT-20260729-009"
TARGET_JOB_PATH = Path(
    "research_control/tasks/RT-20260729-009/jobs/AJ-RT-20260729-009-001.yaml"
)
TARGET_ROLE_PATH = Path(
    "research_control/tasks/RT-20260729-009/roles/"
    "external-red-team-reviewer@0.1.0--RT-20260729-009.yaml"
)
AGENT_JOB_REGISTRY_PATH = Path("registries/AGENT_JOB_REGISTRY.csv")
ROLE_EXECUTION_REGISTRY_PATH = Path("registries/ROLE_EXECUTION_REGISTRY.csv")
REPORT_PATH = Path(
    "research_control/tasks/RT-20260729-010/artifacts/"
    "p8_t06_allowlist_order_parity_recovery_receipt.json"
)
EXPECTED_TARGET_JOB_SHA256 = (
    "7a836fd1be75b2cacfe14892f5c1ae639bd9cab97ff66c20396075800d2b3da3"
)
EXPECTED_ROLE_NON_ALLOWLIST_SHA256 = (
    "f6bb206a40d83c4e83856f66bb326a33b17accdd06f8d829ad2fd6b9e2721b4e"
)
EXPECTED_ROLE_REGISTRY_NON_ALLOWLIST_SHA256 = (
    "24c754f041c94dcfa38a934e69fd32e9728d2d3eb232f99898b84fff623e4c08"
)
EXPECTED_ALLOWED_PATH_COUNT = 28
PROTECTED_HASHES = {
    "research_control/tasks/RT-20260729-009/00_TASK.yaml":
        "d2bdeae3123c60127af15fe17a3aa8ddfe3a8f8dffb33d828b0ee1d221fd41cf",
    "research_control/tasks/RT-20260729-009/DDR-20260729-009.md":
        "51b62450dc10b4c7991691af891ce3503c2c6470da52ab37999b3ba60f69af0b",
    "research_control/tasks/RT-20260729-009/documentation_impact.yaml":
        "323e32d5e1bffc59ad7177a8854a75e779fc7c85484d351d0eff12dee8a454f8",
    "research_control/tasks/RT-20260729-009/jobs/completions/"
    "AJC-AJ-RT-20260729-009-001.yaml":
        "72930cd1b39b983d3a2948360f6f7e6c79f34b661df8de58c21c6f3bde7236f8",
    "research_control/handoffs/handoff-0905.yaml":
        "c9c3bea0f05e58330bbc2780b18709488aa54c4d14f40ac3f8796b9d56680aae",
    "research_control/handoffs/handoff-0905.md":
        "8a7f52b9566c5317aee6b5c4661f0e258bff61a482f09031d57807f324a0c56f",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "blind_mathematical_review_status_v1.yaml":
        "31df9d0532a29dc3a716d2c3e5059839f258e5346952efb96d9fe676029e13f0",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "child_phys_math_p8_t06_closure_review.yaml":
        "d8811e0f8e6dcd215cb66055559b22f0f24a966afb389c65d8175e3de7ef705a",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "child_phys_phil_p8_t06_closure_review.yaml":
        "ecca114f88f60f66109756e3b0be7387c78fe834267203c0df2143c5a8a2f3d4",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "closure_symbolic_reproduction_v1.yaml":
        "310f2d5d38f1f6822628eae87ceeb0bc6cc1368f5f65bcc077867f3dbf23a2db",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "independent_review_human_action_v1.yaml":
        "b0e6cae3efcf5501a0f751e21aa1e96478751cd869364a9507dfac4f9d7a1cba",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "p8_t06_closure_red_team_review_v1.yaml":
        "ea95f6c5a89c36ee827194501db08b53e570e9f2badbf77e10320bbc813fbde7",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "p8_t06_closure_review_compact_receipt_v1.json":
        "47452627a0b1fdad22a2ea69cdd7b5612092c746b3074a7b36baa17017616403",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "p8_t06_closure_review_receipt.md":
        "5e668e3179bf391c63a65773bf98b95f345a9eb44b987dee98d7d8aa00514a95",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "p8_t06_closure_review_validation_v1.json":
        "76acd92e19b85cec772ecc6612a99f738c9c05879d0f66f6cf9ebb81f67e081d",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "p8_t06_closure_smuggling_audit_v1.yaml":
        "43034c9cfbc51dee2c505e1d1c5abab2ea9863c87f1017d560b7784ec14abd57",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "p8_t06_gate_d_readiness_matrix_v1.yaml":
        "ca3f9252d1fe8e2e0814110dbc6a25b274f710d9220ec0e9d7933e82f3b1b3d0",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "parent_conflict_review_p8_t06_closure_review.yaml":
        "a36903dbe73ebbe295335fb331148f353986d1e80e2203eb3f3a8d65df86a4d0",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "parent_fusion_notes_p8_t06_closure_review.md":
        "8196140d56e09d4142552ee08d3f575a796ff7fc806d0aefff2fdde24288f4a4",
    "research_control/tasks/RT-20260729-009/artifacts/"
    "validate_p8_t06_closure_review.py":
        "58fe5673e6faa6e6bee2205822bc6f4425983d126d903b7889d0fa86627047a8",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "7cc8390047c0b19ded7880e379c26ef180330571cc08d691687a9faa1457863c",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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

    role_non_allowlist = dict(target_role)
    role_non_allowlist.pop("allowed_write_paths", None)
    observed_role_non_allowlist_sha256 = canonical_json_sha256(role_non_allowlist)
    checks["target_role_non_allowlist_sha256"] = (
        observed_role_non_allowlist_sha256
    )
    checks["target_role_only_allowlist_changed"] = (
        observed_role_non_allowlist_sha256
        == EXPECTED_ROLE_NON_ALLOWLIST_SHA256
    )
    if not checks["target_role_only_allowlist_changed"]:
        errors.append("target_role_non_allowlist_content_changed")

    role_row_non_allowlist = dict(role_row)
    role_row_non_allowlist.pop("allowed_write_paths", None)
    observed_role_row_non_allowlist_sha256 = canonical_json_sha256(
        role_row_non_allowlist
    )
    checks["target_role_registry_non_allowlist_sha256"] = (
        observed_role_row_non_allowlist_sha256
    )
    checks["target_role_registry_only_allowlist_changed"] = (
        observed_role_row_non_allowlist_sha256
        == EXPECTED_ROLE_REGISTRY_NON_ALLOWLIST_SHA256
    )
    if not checks["target_role_registry_only_allowlist_changed"]:
        errors.append("target_role_registry_non_allowlist_content_changed")

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
    checks["next_worker_skill"] = program_state.get("next_worker_skill")
    recovery = program_state.get("p8_t06_allowlist_order_parity_recovery")
    if not isinstance(recovery, dict):
        errors.append("program_state_recovery_block_missing")
        recovery = {}
    checks["p8_t06_reexecuted"] = recovery.get("p8_t06_reexecuted")
    checks["p8_t07_executed"] = recovery.get("p8_t07_executed")
    checks["scientific_claims_changed"] = recovery.get("scientific_claims_changed")
    checks["distance_to_gr_delta_changed"] = recovery.get(
        "distance_to_gr_delta_changed"
    )
    if checks["active_task_id"] != "RT-20260729-010":
        errors.append("active_task_id_mismatch")
    if checks["latest_handoff_id"] != "handoff-0906":
        errors.append("latest_handoff_id_mismatch")
    if checks["next_worker_skill"] != "none_until_human_authorization":
        errors.append("protected_next_worker_boundary_changed")
    if checks["p8_t06_reexecuted"] is not False:
        errors.append("p8_t06_execution_boundary_changed")
    if checks["p8_t07_executed"] is not False:
        errors.append("p8_t07_execution_boundary_changed")
    if checks["scientific_claims_changed"] is not False:
        errors.append("scientific_claim_boundary_changed")
    if checks["distance_to_gr_delta_changed"] is not False:
        errors.append("distance_to_gr_boundary_changed")

    return {
        "schema_id": "p8_t06_allowlist_order_parity_recovery_receipt_v1",
        "task_id": "RT-20260729-010",
        "job_id": "AJ-RT-20260729-010-001",
        "source_job_id": TARGET_JOB_ID,
        "strategy_id": "repair_p8_t06_allowlist_order_parity_after_checkpoint_v1",
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "validation_status": "PASS" if not errors else "FAIL",
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "p8_t06_reexecuted": False,
            "p8_t07_executed": False,
            "independent_review_claimed": False,
            "gate_d_verdict_authorized": False,
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
