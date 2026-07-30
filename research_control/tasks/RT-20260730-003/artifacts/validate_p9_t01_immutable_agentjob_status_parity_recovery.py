#!/usr/bin/env python3
"""Validate the exact P9-T01 predecessor AgentJob status-parity repair."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260730-003/artifacts/"
    "p9_t01_immutable_agentjob_status_parity_recovery_receipt.json"
)
TARGET_PATH = (
    "research_control/tasks/RT-20260729-012/jobs/"
    "AJ-RT-20260729-012-001.yaml"
)
BEFORE_SHA256 = "0de2bcf0b70cffde72dd4a823ee0b56a18d92b0c1ee33504769c3bb821191bd0"
AFTER_SHA256 = "c1444fb0cd15f4248c1f3886daab4fdfbe7f6f80dc4a42ead25af3e32a24848a"
OLD_TOKEN = b'status: "active"\n'
NEW_TOKEN = b'status: "completed"\n'

PROTECTED_HASHES = {
    "research_control/tasks/RT-20260729-012/jobs/completions/"
    "AJC-AJ-RT-20260729-012-001.yaml":
        "645d5934a58ded9cafbbbd3af59ad9d3aa91efd5ec9bfe51ab231fd7488c07c4",
    "research_control/tasks/RT-20260729-012/artifacts/"
    "source_derived_benchmark_protocol_v1.tex":
        "88ef097bf712ad115e9af62cc18a8b3eabb12f8545350f714ad065f702471007",
    "research_control/handoffs/handoff-0908.yaml":
        "6b690aa475ae901cb981eb2a444145db21c098d34ed88b77d78142835a40ff58",
    "research_control/handoffs/handoff-0908.md":
        "d2edce09694674ffb5d716f89705b086613b3a3cc4b6dbb7d9962254f637c058",
    "research_control/handoffs/handoff-0909.yaml":
        "9168059352723b2d6d36b920e48d054c506563cac134aabf9050510ffe0b4a35",
    "research_control/handoffs/handoff-0909.md":
        "9ec6f581009f9113e7ce397aade276a583583a2c3e477a0db21a45cf6aa88bbe",
    "research_control/tasks/RT-20260730-001/jobs/completions/"
    "AJC-AJ-RT-20260730-001-001.yaml":
        "fcc1f5d90ee5b4c70293b1cf98e4fef92db542721bee847c14b7ec169978248a",
    "research_control/tasks/RT-20260730-002/artifacts/"
    "validation_blocker_precheckpoint_immutable_agentjob_registry_status_parity_v1.yaml":
        "398d1ef9b552d7c1b8fcfdfae306464c7cda028b446c69d828533f9cc27cbc98",
    "research_control/tasks/RT-20260730-002/jobs/completions/"
    "AJC-AJ-RT-20260730-002-001.yaml":
        "13c0096045d19668b13abe1a4ca9c72ab042fb4f0fca7429ddfc8a3958815b8a",
    "research_control/handoffs/handoff-0910.yaml":
        "ef01f2cb955ee2c98d4dd3d947110e29093bb9cee88f4dc80efd8a102abc6227",
    "research_control/handoffs/handoff-0910.md":
        "4955c6a514bd8a6764643ed20173b63d1d49e71fec2a54b58dcefc3fb1303107",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def add_check(checks: list[dict[str, object]], name: str, ok: bool, detail: str) -> None:
    checks.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})


def build_report() -> dict[str, object]:
    checks: list[dict[str, object]] = []
    target = REPO_ROOT / TARGET_PATH
    current = target.read_bytes()
    current_hash = sha256_bytes(current)
    add_check(checks, "target_after_hash", current_hash == AFTER_SHA256, current_hash)

    first_token_is_completed = current.startswith(
        b'job_id: "AJ-RT-20260729-012-001"\n'
        b'task_id: "RT-20260729-012"\n'
        b'decision_id: "DDR-20260729-012"\n'
        b'role_id: "ontology-formalizer"\n'
        b'role_version: "0.2.0"\n'
        b'execution_role_ref: "ontology-formalizer@0.2.0--RT-20260729-012"\n'
        + NEW_TOKEN
    )
    add_check(
        checks,
        "top_level_status_completed",
        first_token_is_completed,
        "the first top-level lifecycle status is completed",
    )

    reconstructed = current.replace(NEW_TOKEN, OLD_TOKEN, 1)
    reconstructed_hash = sha256_bytes(reconstructed)
    add_check(
        checks,
        "sealed_preimage_reconstructed",
        reconstructed_hash == BEFORE_SHA256,
        reconstructed_hash,
    )
    add_check(
        checks,
        "exact_token_length_delta",
        len(current) - len(reconstructed) == len(NEW_TOKEN) - len(OLD_TOKEN) == 3,
        f"before={len(reconstructed)} after={len(current)} delta={len(current)-len(reconstructed)}",
    )

    protected_mismatches: list[str] = []
    for relative, expected in PROTECTED_HASHES.items():
        actual = sha256_file(REPO_ROOT / relative)
        if actual != expected:
            protected_mismatches.append(f"{relative}:{actual}")
    add_check(
        checks,
        "protected_hashes",
        not protected_mismatches,
        "all exact" if not protected_mismatches else ";".join(protected_mismatches),
    )

    registry_path = REPO_ROOT / "registries/AGENT_JOB_REGISTRY.csv"
    with registry_path.open(newline="", encoding="utf-8") as handle:
        rows = {
            row["job_id"]: row
            for row in csv.DictReader(handle)
            if row.get("job_id")
        }
    registry_row = rows.get("AJ-RT-20260729-012-001", {})
    add_check(
        checks,
        "registry_status_completed",
        registry_row.get("status") == "completed",
        str(registry_row.get("status", "")),
    )
    add_check(
        checks,
        "registry_validation_pass",
        registry_row.get("validation_status") == "PASS",
        str(registry_row.get("validation_status", "")),
    )

    program_state = (REPO_ROOT / "research_control/program_state.yaml").read_text(
        encoding="utf-8"
    )
    add_check(
        checks,
        "program_state_routes_recovery",
        'active_task_id: "RT-20260730-003"' in program_state
        and 'latest_handoff_id: "handoff-0911"' in program_state,
        "RT-20260730-003 and handoff-0911 are active",
    )
    add_check(
        checks,
        "p9_t02_unexecuted",
        "p9_t02_executed: true" not in program_state
        and "benchmark_case_executed: true" not in program_state,
        "no P9-T02 or benchmark execution token is present",
    )

    handoff_path = REPO_ROOT / "research_control/handoffs/handoff-0911.yaml"
    handoff_text = handoff_path.read_text(encoding="utf-8")
    add_check(
        checks,
        "handoff_preserves_blocked_zero_execution",
        'handoff_id: "handoff-0911"' in handoff_text
        and 'repair_p9_recovery_task_plan_identity_and_ordinary_guard_parity_v1'
        in handoff_text
        and "p9_t02_executed: true" not in handoff_text,
        "P9-T02 remains unexecuted behind the distinct plan-identity recovery",
    )

    failures = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "p9_t01_immutable_agentjob_status_parity_recovery_receipt_v1",
        "task_id": "RT-20260730-003",
        "job_id": "AJ-RT-20260730-003-001",
        "strategy_id": "repair_p9_t01_immutable_agentjob_registry_status_parity_v1",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "error_count": len(failures),
        "target_path": TARGET_PATH,
        "target_sha256_before": BEFORE_SHA256,
        "target_sha256_after": current_hash,
        "reconstructed_preimage_sha256": reconstructed_hash,
        "protected_hash_count": len(PROTECTED_HASHES),
        "protected_hash_mismatch_count": len(protected_mismatches),
        "p9_t01_reexecuted": False,
        "p9_t02_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.write_report == args.check:
        parser.error("choose exactly one of --write-report or --check")

    report = build_report()
    if args.write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    elif not REPORT_PATH.exists():
        report["status"] = "FAIL"
        report["error_count"] = int(report["error_count"]) + 1
        report["checks"].append(
            {"name": "receipt_exists", "status": "FAIL", "detail": str(REPORT_PATH)}
        )
    else:
        expected = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if REPORT_PATH.read_text(encoding="utf-8") != expected:
            report["status"] = "FAIL"
            report["error_count"] = int(report["error_count"]) + 1
            report["checks"].append(
                {"name": "receipt_fresh", "status": "FAIL", "detail": str(REPORT_PATH)}
            )

    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
