#!/usr/bin/env python3
"""Validate generation-250 RT-017 ordered allowlist parity recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TARGET_JOB = ROOT / "research_control/tasks/RT-20260803-017/jobs/AJ-RT-20260803-017-001.yaml"
TARGET_ROLE = ROOT / "research_control/tasks/RT-20260803-017/roles/process-integrity-auditor@0.1.0--RT-20260803-017.yaml"
AGENT_JOB_REGISTRY = ROOT / "registries/AGENT_JOB_REGISTRY.csv"
ROLE_EXECUTION_REGISTRY = ROOT / "registries/ROLE_EXECUTION_REGISTRY.csv"
REPORT = ROOT / "research_control/tasks/RT-20260803-018/artifacts/p16_t04_rt017_allowlist_parity_recovery_receipt.json"

EXPECTED_JOB_SHA256 = "5a94fdd4fa9fcd80ae44588cb2ba3eacdc707b3235caba2af301c1881a949adc"
EXPECTED_ROLE_NON_ALLOWLIST_SHA256 = "67b247ac072065b197808ca03b57f16f633f2eb4cd91a1f9f0e02bc89f1338ac"
EXPECTED_JOB_REGISTRY_NON_ALLOWLIST_SHA256 = "265fef3f67672cf8aafc9e25fe745e0eca35dc694616aea58cd2679231de5d22"
EXPECTED_ROLE_REGISTRY_NON_ALLOWLIST_SHA256 = "f12b3b739f909ea944706693e18025fcbb069145d8cb272458df16673d446352"
EXPECTED_ALLOWED_WRITE_PATH_COUNT = 61

PROTECTED_HASHES = {
    "research_control/tasks/RT-20260803-017/00_TASK.yaml": "1646ed4f7a06cf79c472872cff6f8e3a6fa6a740beda8694268e847d3e07c252",
    "research_control/tasks/RT-20260803-017/DDR-20260803-017.md": "dd3fb4169bd5026190d29193ad23f792c8aedd542020f90f1bcd132553daef4e",
    "research_control/tasks/RT-20260803-017/documentation_impact.yaml": "5802c90e8f1aa95f66e553f4be6a39fd58481177d44a1ba12db94940d14c4101",
    "research_control/tasks/RT-20260803-017/jobs/completions/AJC-AJ-RT-20260803-017-001.yaml": "ba5502b980e5868eab6f004f85583f555b8d31056f916b2af5e7318a355af9db",
    "research_control/handoffs/handoff-0958.yaml": "295bc8a3f881c9dc03312468b5427c156bcdd895a9812055cbf4adf673b19f24",
    "research_control/handoffs/handoff-0958.md": "bd005b5ff32da57f589d5a7da0a1434f862b96564dee50bed822d0374faff606",
    "research_control/tasks/RT-20260803-017/artifacts/checkpoint_blocker_generation_248_rt015_folder_map_coverage_v1.yaml": "a6215a79cf70cfd7d2221c191e7f96c06a8288a639eadfd162b25558287d5785",
    "research_control/tasks/RT-20260803-017/artifacts/generation_247_red_team_template_path_classifier_recovery_receipt.json": "1cfd469287f13b086c75247c2817b28b6fffa3d7761ac9b369f998bc063c4bd8",
    "research_control/templates/RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml": "d021d204205b648bbf179e47afbcb632bdc93f393e50dd559dab30d02785eca8",
    "scripts/project_control/classify_project_changes.py": "a398b694f699e5cd6c14c5edbc6fed0147b7da0d265b4774912225ce29fbcba8",
    "research_control/tasks/RT-20260803-015/artifacts/p16_t04_internal_review_label_contract_validation.json": "97edc8ab306c30ce453f978442226c9cae3fa012acf1efe842343266fb37f629",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(payload)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping: {path}")
    return value


def csv_row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        matches = [row for row in csv.DictReader(handle) if row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected one {key}={value} row in {path}, found {len(matches)}")
    return matches[0]


def split_paths(value: str) -> list[str]:
    return [] if not value else value.split(";")


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    job = load_yaml(TARGET_JOB)
    role = load_yaml(TARGET_ROLE)
    job_row = csv_row(AGENT_JOB_REGISTRY, "job_id", "AJ-RT-20260803-017-001")
    role_row = csv_row(
        ROLE_EXECUTION_REGISTRY,
        "execution_role_ref",
        "process-integrity-auditor@0.1.0--RT-20260803-017",
    )

    job_paths = list(job.get("allowed_write_paths") or [])
    role_paths = list(role.get("allowed_write_paths") or [])
    job_registry_paths = split_paths(job_row.get("allowed_write_paths", ""))
    role_registry_paths = split_paths(role_row.get("allowed_write_paths", ""))
    representations = {
        "agent_job": job_paths,
        "execution_role": role_paths,
        "agent_job_registry": job_registry_paths,
        "role_execution_registry": role_registry_paths,
    }

    job_sha = sha256_bytes(TARGET_JOB.read_bytes())
    if job_sha != EXPECTED_JOB_SHA256:
        errors.append(f"immutable job hash mismatch: {job_sha}")
    if len(job_paths) != EXPECTED_ALLOWED_WRITE_PATH_COUNT:
        errors.append(f"expected {EXPECTED_ALLOWED_WRITE_PATH_COUNT} job paths, found {len(job_paths)}")
    for name, paths in representations.items():
        if paths != job_paths:
            errors.append(f"ordered allowlist mismatch: {name}")

    role_non_allowlist = {key: value for key, value in role.items() if key != "allowed_write_paths"}
    job_row_non_allowlist = {key: value for key, value in job_row.items() if key != "allowed_write_paths"}
    role_row_non_allowlist = {key: value for key, value in role_row.items() if key != "allowed_write_paths"}
    non_allowlist_hashes = {
        "execution_role": canonical_sha(role_non_allowlist),
        "agent_job_registry": canonical_sha(job_row_non_allowlist),
        "role_execution_registry": canonical_sha(role_row_non_allowlist),
    }
    expected_non_allowlist_hashes = {
        "execution_role": EXPECTED_ROLE_NON_ALLOWLIST_SHA256,
        "agent_job_registry": EXPECTED_JOB_REGISTRY_NON_ALLOWLIST_SHA256,
        "role_execution_registry": EXPECTED_ROLE_REGISTRY_NON_ALLOWLIST_SHA256,
    }
    for name, expected in expected_non_allowlist_hashes.items():
        if non_allowlist_hashes[name] != expected:
            errors.append(f"non-allowlist field drift: {name}")

    protected_results: list[dict[str, Any]] = []
    for relative, expected in PROTECTED_HASHES.items():
        path = ROOT / relative
        actual = sha256_bytes(path.read_bytes()) if path.is_file() else None
        matched = actual == expected
        if not matched:
            errors.append(f"protected hash mismatch: {relative}")
        protected_results.append(
            {"path": relative, "expected_sha256": expected, "actual_sha256": actual, "matched": matched}
        )

    return {
        "schema_id": "p16_t04_rt017_allowlist_parity_recovery_receipt_v1",
        "task_id": "RT-20260803-018",
        "job_id": "AJ-RT-20260803-018-001",
        "strategy_id": "repair_p16_t04_rt017_agentjob_execution_role_allowlist_parity_v1",
        "status": "PASS" if not errors else "FAIL",
        "immutable_route_sha256": "257bde39d376fbdc14e8ae45467ef3156d75370a6e9c8f6ba132ff504e9ff006",
        "source_job_path": str(TARGET_JOB.relative_to(ROOT)),
        "source_job_sha256": job_sha,
        "representation_count": len(representations),
        "allowed_write_path_count": len(job_paths),
        "ordered_representation_sha256": {
            name: canonical_sha(paths) for name, paths in representations.items()
        },
        "all_four_ordered_representations_equal": len({canonical_sha(paths) for paths in representations.values()}) == 1,
        "non_allowlist_field_sha256": non_allowlist_hashes,
        "protected_hashes": protected_results,
        "protected_hash_mismatch_count": sum(1 for item in protected_results if not item["matched"]),
        "existing_documentation_blocker_preserved": any(
            item["path"].endswith("checkpoint_blocker_generation_248_rt015_folder_map_coverage_v1.yaml")
            and item["matched"]
            for item in protected_results
        ),
        "rt015_rt016_documentation_receipts_modified": False,
        "rt017_agent_job_modified": job_sha != EXPECTED_JOB_SHA256,
        "generation_248_checkpoint_replayed": False,
        "checkpoint_invocation_count": 0,
        "p16_t04_reaudit_executed": False,
        "p16_t05_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "errors": errors,
    }


def encoded(report: dict[str, Any]) -> bytes:
    return (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        REPORT.write_bytes(encoded(report))
    if args.check:
        if not REPORT.is_file():
            report["errors"].append("missing recovery receipt")
            report["status"] = "FAIL"
        elif REPORT.read_bytes() != encoded(report):
            report["errors"].append("recovery receipt is stale")
            report["status"] = "FAIL"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
