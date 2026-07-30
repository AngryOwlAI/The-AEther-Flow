#!/usr/bin/env python3
"""Validate generation 172's exact P9-T01 task-taxonomy slug recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
TARGET = REPO_ROOT / "research_control/tasks/RT-20260729-012/00_TASK.yaml"
RECEIPT = (
    REPO_ROOT
    / "research_control/tasks/RT-20260730-005/artifacts/"
    "p9_t01_task_taxonomy_candidate_family_slug_recovery_receipt.json"
)
OLD = b'candidate_family: "SourceDerivedBenchmarkProtocol_v1"'
NEW = b'candidate_family: "source_derived_benchmark_protocol_v1"'
TARGET_BEFORE = "4f85641999afa719e6f81156fff3f5e6a089ece5d9c92849f51d849b9ac959d0"
TARGET_AFTER = "249885ae2e010f43868bdf3d44b0336ac3058ed568c4120cd1781658905eeec9"
PROTECTED_HASHES = {
    "research_control/handoffs/handoff-0912.yaml":
        "8a7f732c1729047a4b403496d1419925ba603b6d067e57e6e22f14bcf2d451a8",
    "research_control/handoffs/handoff-0912.md":
        "eefaed992c3e0beff04010aa435ed946e85efbe08841f4aa13ddaafac5eb4465",
    "research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_protocol_v1.tex":
        "88ef097bf712ad115e9af62cc18a8b3eabb12f8545350f714ad065f702471007",
    "research_control/tasks/RT-20260730-002/00_TASK.yaml":
        "6c06056bca781c7d197c2d7469cb9f3db88a366bba645448c2efc1749615221e",
    "research_control/tasks/RT-20260730-003/00_TASK.yaml":
        "4356cafade0ab6a868e04c6df560b2dd0dee9d5ae49049e93b09c2a46c444cfe",
    "research_control/tasks/RT-20260730-004/00_TASK.yaml":
        "04c700471a0b251ae5c5699d73c10004565d755f6971d2f8611b24aa4a4479d6",
    "research_control/tasks/RT-20260730-004/jobs/completions/"
    "AJC-AJ-RT-20260730-004-001.yaml":
        "590535e876fa70e84e8de5f48e2fa9a22fe32afed7a6cec27698b5c284f9c1ce",
    "research_control/tasks/RT-20260730-004/artifacts/"
    "validation_blocker_precheckpoint_p9_t01_task_taxonomy_candidate_family_slug_v1.yaml":
        "4fd172c52b27469da5b34bf4ccf78860afbe6a221697529b8df2753ee1db0e92",
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run_json(command: list[str]) -> tuple[int, dict[str, Any], str]:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError:
        parsed = {}
    return completed.returncode, parsed, completed.stderr.strip()


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: Any) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )

    payload = TARGET.read_bytes()
    add("target_sha256_after", sha256_bytes(payload) == TARGET_AFTER, sha256_bytes(payload))
    add("normalized_scalar_count", payload.count(NEW) == 1, payload.count(NEW))
    add("original_scalar_absent", payload.count(OLD) == 0, payload.count(OLD))
    reconstructed = payload.replace(NEW, OLD, 1)
    add(
        "sealed_preimage_reconstructed",
        sha256_bytes(reconstructed) == TARGET_BEFORE,
        sha256_bytes(reconstructed),
    )

    protected_mismatches: list[dict[str, str]] = []
    for relative_path, expected in PROTECTED_HASHES.items():
        actual = sha256_path(REPO_ROOT / relative_path)
        if actual != expected:
            protected_mismatches.append(
                {"path": relative_path, "expected": expected, "actual": actual}
            )
    add(
        "protected_generation_171_hashes",
        not protected_mismatches,
        protected_mismatches,
    )

    taxonomy_rc, taxonomy, taxonomy_stderr = run_json(
        [
            sys.executable,
            "scripts/research_control/task_taxonomy.py",
            "--validate-repository",
            "--json",
        ]
    )
    add(
        "repository_task_taxonomy",
        taxonomy_rc == 0
        and taxonomy.get("status") == "PASS"
        and taxonomy.get("explicit_required_error_count") == 0
        and taxonomy.get("historical_source_mutation_count") == 0
        and taxonomy.get("stronger_science_inference_count") == 0,
        {
            "returncode": taxonomy_rc,
            "status": taxonomy.get("status"),
            "explicit_required_error_count": taxonomy.get(
                "explicit_required_error_count"
            ),
            "historical_source_mutation_count": taxonomy.get(
                "historical_source_mutation_count"
            ),
            "stronger_science_inference_count": taxonomy.get(
                "stronger_science_inference_count"
            ),
            "stderr": taxonomy_stderr,
        },
    )

    protocol_rc, protocol, protocol_stderr = run_json(
        [
            sys.executable,
            "research_control/tasks/RT-20260729-012/artifacts/"
            "validate_source_derived_benchmark_protocol.py",
            "--check",
            "--json",
        ]
    )
    add(
        "p9_t01_protocol_preserved",
        protocol_rc == 0
        and protocol.get("status") == "PASS"
        and protocol.get("check_count") == 84
        and protocol.get("failure_count") == 0,
        {
            "returncode": protocol_rc,
            "status": protocol.get("status"),
            "check_count": protocol.get("check_count"),
            "failure_count": protocol.get("failure_count"),
            "stderr": protocol_stderr,
        },
    )
    add(
        "all_benchmark_cases_not_run",
        protocol.get("case_template_count") == 6
        and protocol.get("executed_case_count") == 0
        and protocol.get("passed_case_count") == 0,
        {
            "case_template_count": protocol.get("case_template_count"),
            "executed_case_count": protocol.get("executed_case_count"),
            "passed_case_count": protocol.get("passed_case_count"),
        },
    )
    add(
        "scientific_authority_unchanged",
        protocol.get("distance_to_gr_changed") is False
        and protocol.get("physics_promotion_authorized") is False,
        {
            "distance_to_gr_changed": protocol.get("distance_to_gr_changed"),
            "physics_promotion_authorized": protocol.get(
                "physics_promotion_authorized"
            ),
        },
    )

    failure_count = sum(check["status"] == "FAIL" for check in checks)
    return {
        "schema_id": "p9_t01_task_taxonomy_candidate_family_slug_recovery_receipt_v1",
        "task_id": "RT-20260730-005",
        "job_id": "AJ-RT-20260730-005-001",
        "strategy_id": "repair_p9_t01_benchmark_protocol_task_taxonomy_candidate_family_slug_v1",
        "status": "PASS" if failure_count == 0 else "FAIL",
        "check_count": len(checks),
        "failure_count": failure_count,
        "target_path": "research_control/tasks/RT-20260729-012/00_TASK.yaml",
        "target_field_path": "task_taxonomy.candidate_family",
        "target_value_before": OLD.decode().split('"')[1],
        "target_value_after": NEW.decode().split('"')[1],
        "target_sha256_before": TARGET_BEFORE,
        "target_sha256_after": TARGET_AFTER,
        "reconstructed_preimage_sha256": sha256_bytes(reconstructed),
        "protected_hash_count": len(PROTECTED_HASHES),
        "protected_hash_mismatch_count": len(protected_mismatches),
        "p9_t01_reexecuted": False,
        "p9_t02_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "checks": checks,
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
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        receipt_matches = False
        if RECEIPT.is_file():
            try:
                receipt_matches = json.loads(RECEIPT.read_text(encoding="utf-8")) == report
            except json.JSONDecodeError:
                receipt_matches = False
        if not receipt_matches:
            report["status"] = "FAIL"
            report["failure_count"] += 1
        report["receipt_matches"] = receipt_matches

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered if args.json else f"{report['status']}: {report['failure_count']} failures")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
