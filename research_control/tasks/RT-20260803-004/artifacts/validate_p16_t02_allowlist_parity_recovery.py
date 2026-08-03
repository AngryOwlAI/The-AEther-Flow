#!/usr/bin/env python3
"""Validate the exact RT-20260803-004 P16-T02 allowlist-parity recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TARGET_JOB_ID = "AJ-RT-20260803-003-001"
TARGET_ROLE_REF = "external-red-team-reviewer@0.1.0--RT-20260803-003"
TARGET_SIGNAL_ID = "PIS-RT-20260803-003-001"
TARGET_JOB_PATH = Path(
    "research_control/tasks/RT-20260803-003/jobs/AJ-RT-20260803-003-001.yaml"
)
TARGET_ROLE_PATH = Path(
    "research_control/tasks/RT-20260803-003/roles/"
    "external-red-team-reviewer@0.1.0--RT-20260803-003.yaml"
)
AGENT_JOB_REGISTRY_PATH = Path("registries/AGENT_JOB_REGISTRY.csv")
ROLE_EXECUTION_REGISTRY_PATH = Path("registries/ROLE_EXECUTION_REGISTRY.csv")
SIGNAL_REGISTRY_PATH = Path("registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv")
REPORT_PATH = Path(
    "research_control/tasks/RT-20260803-004/artifacts/"
    "p16_t02_allowlist_parity_recovery_receipt.json"
)
EXPECTED_TARGET_JOB_SHA256 = (
    "9205f277f7e057e367ab8648820d3032a84743c515751d83ac205697149505d0"
)
EXPECTED_TARGET_ROLE_NON_ALLOWLIST_SHA256 = (
    "480169fb3231e6c3a56cc950894efd226cb1fa9d5de44d356694534d0324cb71"
)
EXPECTED_AGENT_ROW_NON_ALLOWLIST_SHA256 = (
    "16223158bd1cf6d8d2625f521f59c806c098d9ed5b4413c17a8b93ee4958b8b6"
)
EXPECTED_ROLE_ROW_NON_ALLOWLIST_SHA256 = (
    "92d74f56d123ec098c8a6536d4439cb91b40b9c01430c1167616c68f6b577601"
)
EXPECTED_ALLOWED_PATH_COUNT = 26
PROTECTED_HASHES = {
    "research_control/tasks/RT-20260803-003/00_TASK.yaml":
        "47c6ac96e13def693492295366f5461896068ea073549318d958b2bef6222d76",
    "research_control/tasks/RT-20260803-003/DDR-20260803-003.md":
        "57e5136dd12f2beb736555e3ef3bf5aee84d4cc60c14ec0deae70f1080e33bb2",
    "research_control/tasks/RT-20260803-003/documentation_impact.yaml":
        "401111df784ae4b8a982d9f9dc6dcdacb049aebd3f1ddd28a11f9dd31358c685",
    "research_control/tasks/RT-20260803-003/jobs/completions/"
    "AJC-AJ-RT-20260803-003-001.yaml":
        "99aca5806525200bb9d08db5e25765a1d7f3603e5fb49a79a20b4f9d0075c4ac",
    "research_control/handoffs/handoff-0945.yaml":
        "fcf800fe995731180f71bdf85e8b25b9d91cca3463e5d004fc288af014f8d906",
    "research_control/handoffs/handoff-0945.md":
        "e3fc712638f4054a3d071dc3510fee8761df33b9d1b4e4c232d025536eaef938",
    "research_control/project_improvement_handoffs/"
    "improve-project-handoff_20260803_003.yaml":
        "1c2e18cf29c6448f38898ca7d9e9bffcc6f8f48a5a41f821fd1e183b1ea4a04b",
    "research_control/project_improvement_handoffs/"
    "improve-project-handoff_20260803_003.md":
        "b58699bd1cdfc6e8dc0edc34d17c3b95ce877e52cad01b72b44437f0ddb4de71",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "child_phys_math_p16_t02_gate_consistency.yaml":
        "d614cc3f4aa556dbd11797884e9b42bb170d188b05113aff896c5f35ea8b1138",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "child_phys_phil_p16_t02_gate_consistency.yaml":
        "ccfdb9967068a147e02a95f9abf22e10de7e1387d7b8304af0cdbebcc4214cb5",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "parent_conflict_review_p16_t02_gate_consistency.yaml":
        "bb3c6b2c2a938f4b32835328fd3e03bfd75bbad286a154c29bea638f8a9342d9",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "parent_fusion_notes_p16_t02_gate_consistency.md":
        "98a50d65b464b24641247d0185b953f217020378de5deeba09d3e660cfba8ba4",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "v21_p16_t02_authority_path_map.yaml":
        "c74551dd8fe9cfc64f5a66e410813fc0f16fe55c26723a42c098444ea913df3e",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "v21_p16_t02_compact_receipt.json":
        "2e2377a5a357fe43e3b18333c0994732a2e0d6cff7717de68bbfd1c8396db577",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "v21_p16_t02_gate_consistency_audit.md":
        "5daa24b57b805af51633f85e176b8da5699aaca8000794f57eb5ff4a3ddfde8c",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "v21_p16_t02_overread_findings.yaml":
        "f4f434fb0a8b0cd90809eb5cf40df9f8ac57d7aab1605b94dc79e914ab0dc08c",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "v21_p16_t02_validation.json":
        "d12496fb50fc6b153c3349e87a1c352cd7641c31e139eddeb3c9cfc9dad3b758",
    "research_control/tasks/RT-20260803-003/artifacts/"
    "validate_p16_t02_gate_consistency.py":
        "3328f60fd6e71a82e80e4a3b5d555c7834c458d29d9c6ef65dfc085df2cf9924",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "6b81b42bc7ed83f74f8062f2ade26988e8b369aa2d23744fc9e392279e1de5d8",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
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


def non_allowlist_sha256(value: dict[str, Any]) -> str:
    payload = dict(value)
    payload.pop("allowed_write_paths", None)
    return canonical_sha256(payload)


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

    non_allowlist_checks = {
        "execution_role": (
            non_allowlist_sha256(target_role),
            EXPECTED_TARGET_ROLE_NON_ALLOWLIST_SHA256,
        ),
        "agent_job_registry_row": (
            non_allowlist_sha256(agent_row),
            EXPECTED_AGENT_ROW_NON_ALLOWLIST_SHA256,
        ),
        "role_execution_registry_row": (
            non_allowlist_sha256(role_row),
            EXPECTED_ROLE_ROW_NON_ALLOWLIST_SHA256,
        ),
    }
    checks["non_allowlist_field_hashes"] = {
        name: {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": observed == expected,
        }
        for name, (observed, expected) in non_allowlist_checks.items()
    }
    for name, (observed, expected) in non_allowlist_checks.items():
        if observed != expected:
            errors.append(f"non_allowlist_fields_changed:{name}")

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

    signal_row = registry_row(
        REPO_ROOT / SIGNAL_REGISTRY_PATH, "signal_id", TARGET_SIGNAL_ID
    )
    checks["source_signal_status"] = signal_row.get("status")
    checks["source_signal_resolution_evidence_path"] = signal_row.get(
        "resolution_evidence_path"
    )
    checks["source_signal_resolved_by_job_id"] = signal_row.get(
        "resolved_by_job_id"
    )
    if checks["source_signal_status"] != "open":
        errors.append("source_status_taxonomy_signal_not_open")
    if checks["source_signal_resolution_evidence_path"]:
        errors.append("source_status_taxonomy_signal_has_resolution_evidence")
    if checks["source_signal_resolved_by_job_id"]:
        errors.append("source_status_taxonomy_signal_has_resolving_job")

    program_state = load_yaml(REPO_ROOT / "research_control/program_state.yaml")
    checks["active_task_id"] = program_state.get("active_task_id")
    checks["latest_handoff_id"] = program_state.get("latest_handoff_id")
    recovery = program_state.get("p16_t02_allowlist_parity_recovery")
    if not isinstance(recovery, dict):
        errors.append("program_state_recovery_block_missing")
        recovery = {}
    checks["p16_t02_reexecuted"] = recovery.get("p16_t02_reexecuted")
    checks["p16_t02_status_taxonomy_repair_executed"] = recovery.get(
        "p16_t02_status_taxonomy_repair_executed"
    )
    checks["p16_t03_executed"] = recovery.get("p16_t03_executed")
    checks["p16_t04_executed"] = recovery.get("p16_t04_executed")
    checks["scientific_claims_changed"] = recovery.get(
        "scientific_claims_changed"
    )
    checks["distance_to_gr_delta_changed"] = recovery.get(
        "distance_to_gr_delta_changed"
    )
    if checks["active_task_id"] != "RT-20260803-004":
        errors.append("active_task_id_mismatch")
    if checks["latest_handoff_id"] != "handoff-0946":
        errors.append("latest_handoff_id_mismatch")
    for name in (
        "p16_t02_reexecuted",
        "p16_t02_status_taxonomy_repair_executed",
        "p16_t03_executed",
        "p16_t04_executed",
        "scientific_claims_changed",
        "distance_to_gr_delta_changed",
    ):
        if checks[name] is not False:
            errors.append(f"authority_boundary_changed:{name}")

    return {
        "schema_id": "p16_t02_allowlist_parity_recovery_receipt_v1",
        "task_id": "RT-20260803-004",
        "job_id": "AJ-RT-20260803-004-001",
        "source_job_id": TARGET_JOB_ID,
        "source_signal_id": TARGET_SIGNAL_ID,
        "strategy_id": "reroute_generation_230_p16_t02_allowlist_parity_repair_v1",
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "validation_status": "PASS" if not errors else "FAIL",
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "p16_t02_reexecuted": False,
            "p16_t02_status_taxonomy_repair_executed": False,
            "p16_t03_executed": False,
            "p16_t04_executed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_external_action_or_push_authorized": False,
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
