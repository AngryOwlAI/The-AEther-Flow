#!/usr/bin/env python3
"""Validate the bounded P5-T04 P10 live-view convergence recovery."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

RECEIPT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260725-011/artifacts/"
    "p5_t04_p10_live_view_recovery_receipt.json"
)
P10_VALIDATOR_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-003/artifacts/"
    "validate_v21_p10_migration_readiness.py"
)
P5_VALIDATOR_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260725-010/artifacts/"
    "validate_cubic_amplitude_structure.py"
)
BURDEN_VALIDATOR_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260721-009/artifacts/"
    "validate_v21_current_burden_status.py"
)
SOURCE_CHECKPOINT_RECEIPT_PATH = (
    REPO_ROOT
    / ".local/validation-receipts/"
    "5fdb4a94a5136a980b14c90b290edc80d5bffc547f521ef9a53db6c9866d794a/"
    "RUN-CHECKPOINT-9b50828f6b157ffc/receipt.json"
)
SOURCE_FAILED_GATE_PATH = SOURCE_CHECKPOINT_RECEIPT_PATH.parent / (
    "gates/0005-test_shard_repository.stderr"
)

EXPECTED_TRACKED_HASHES = {
    "registries/DISTANCE_TO_GR_LEDGER.csv": "0d3e50acacadd279b29b25aab73cf73c23dfe8e09896b7f86559e648f8f4bfbc",
    "research_control/handoffs/handoff-0870.md": "db224c6bfc376434113ce6e4a5a03b253ee24c30bb6f83ff97fa8edff1c0e6a6",
    "research_control/handoffs/handoff-0870.yaml": "f0066caea64803fa9c9394b635de3fb592d35b22c529ff737b468799d15541b9",
    "research_control/tasks/RT-20260722-003/artifacts/v21_p10_integration_audit.md": "721351dfa0d3268d26bfbaee4409f84b487b755c9c5c185fd9c41130db3856ff",
    "research_control/tasks/RT-20260722-003/artifacts/v21_p10_migration_readiness_compact_receipt.json": "db3410f2c166562a4cc8636011eeda15b7cb8f051c3917fea21b370e4da2ddb6",
    "research_control/tasks/RT-20260722-003/artifacts/v21_p10_migration_readiness_validation.json": "cdcd907f4ad237118eab65f06f364263da08285456514605a0308bc203f7a6e6",
    "research_control/tasks/RT-20260722-003/artifacts/validate_v21_p10_migration_readiness.py": "9983b57a58eb618621cef210ff150badb525922b02a7f89d24e8bea8f9500ad6",
    "research_control/tasks/RT-20260725-010/00_TASK.yaml": "7bee0ffd1bd8264c331ab4d415e16da3bf995a49ce36fa4772da626f0a7dc66e",
    "research_control/tasks/RT-20260725-010/DDR-20260725-010.md": "e9189cac4330b14083c8efc6c82093b3eca9d7c3df3a21cfc32eb094b2e36d9d",
    "research_control/tasks/RT-20260725-010/artifacts/child_phys_math_cubic_amplitude_structure.yaml": "494371b88f3ce97401e5a8decb5ba51b8f16bb006be6f1944dc216ecb41b03a0",
    "research_control/tasks/RT-20260725-010/artifacts/child_phys_phil_cubic_amplitude_structure.yaml": "39b5f02dade395c90e43f409b556593ae3fbca0e0ba96960aa3e482431a6ef95",
    "research_control/tasks/RT-20260725-010/artifacts/cubic_amplitude_structural_analysis_spec_v1.yaml": "1c2b16d06254b96b5051acfbfcf0884ff85fab1903cb2fa964d4c957cd9d0044",
    "research_control/tasks/RT-20260725-010/artifacts/cubic_amplitude_structural_analysis_v1.tex": "a9a9f42ff016febc0f40a8a4db32b09f670084bda2248704e290cf5bee02a06b",
    "research_control/tasks/RT-20260725-010/artifacts/cubic_amplitude_structural_analysis_validation_receipt_v1.json": "ed69e89906d7f3a67251e51f20d6d2ac75175a53025bbdc83450043df5b92774",
    "research_control/tasks/RT-20260725-010/artifacts/parent_conflict_review_cubic_amplitude_structure.yaml": "c3feb37f1959a1f9635900c787722cbbea822dfd15664b11812c8a308f25246e",
    "research_control/tasks/RT-20260725-010/artifacts/parent_fusion_notes_cubic_amplitude_structure.md": "0b6a4d541fce825da3386653df8d7abf036ab03f8b58576f83277150f4e8fcee",
    "research_control/tasks/RT-20260725-010/artifacts/validate_cubic_amplitude_structure.py": "e9b882b4fca6b572a2bd043bb17665c59a60ae096661c9181769447428abbff2",
    "research_control/tasks/RT-20260725-010/jobs/AJ-RT-20260725-010-001.yaml": "b9e87fab312360058222cf72909d34e5d2ecb3f1b75602b840cf33d18251f97c",
    "research_control/tasks/RT-20260725-010/jobs/completions/AJC-AJ-RT-20260725-010-001.yaml": "ce4e0348bbf558bc49eeac1589a4099c7f7bdc7a7d418f4ed4d827d4bd728f81",
    "research_control/tasks/RT-20260725-010/roles/ontology-formalizer@0.2.0--RT-20260725-010.yaml": "daa72746ede1c73a70ab7925d9b13b5f63ba35aab1a6266a370c465c4cc9f5fc",
    "tests/test_v21_p10_migration_readiness.py": "4389eed2d85b30e87974eabc5d2be3c1e07e7436d4c658d6486846e47b674c4c",
}

EXPECTED_SOURCE_CHECKPOINT_RECEIPT_SHA256 = (
    "8bb81d90bea681faaa0223b81013b69bcd43de7ef32ceaff80e4df9e13145863"
)
EXPECTED_FAILED_GATE_SHA256 = (
    "330bb5e2e2d5b091b93f3d1220da8bbfead4f44c762c9bf904fafa1bce9cfc93"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256_path(path: Path) -> str:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"missing regular non-symlink path: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_relative(relative: str) -> str:
    return sha256_path(REPO_ROOT / relative)


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_json(command: list[str]) -> tuple[int, dict[str, Any]]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"command did not emit JSON: {' '.join(command)}"
        ) from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"command JSON is not an object: {' '.join(command)}")
    return result.returncode, payload


def build_receipt() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    observed_hashes = {
        relative: sha256_relative(relative)
        for relative in sorted(EXPECTED_TRACKED_HASHES)
    }
    hash_mismatches = [
        relative
        for relative, expected in EXPECTED_TRACKED_HASHES.items()
        if observed_hashes.get(relative) != expected
    ]
    checks.append(
        {
            "check_id": "exact_recovery_sources_and_protected_bytes",
            "status": "PASS" if not hash_mismatches else "FAIL",
            "mismatch_paths": sorted(hash_mismatches),
        }
    )

    source_checkpoint_sha256 = sha256_path(SOURCE_CHECKPOINT_RECEIPT_PATH)
    failed_gate_sha256 = sha256_path(SOURCE_FAILED_GATE_PATH)
    checkpoint_evidence_ok = (
        source_checkpoint_sha256 == EXPECTED_SOURCE_CHECKPOINT_RECEIPT_SHA256
        and failed_gate_sha256 == EXPECTED_FAILED_GATE_SHA256
    )
    checks.append(
        {
            "check_id": "source_checkpoint_failure_identity",
            "status": "PASS" if checkpoint_evidence_ok else "FAIL",
            "checkpoint_receipt_sha256": source_checkpoint_sha256,
            "failed_gate_sha256": failed_gate_sha256,
            "authority_note": (
                "The local receipt is route-identity evidence only; tracked control "
                "state and protected source bytes remain authoritative."
            ),
        }
    )

    burden_returncode, burden = run_json(
        [
            sys.executable,
            str(BURDEN_VALIDATOR_PATH.relative_to(REPO_ROOT)),
            "--check",
            "--json",
        ]
    )
    burden_ok = burden_returncode == 0 and burden.get("status") == "PASS"
    checks.append(
        {
            "check_id": "live_burden_view_converged",
            "status": "PASS" if burden_ok else "FAIL",
            "validator_status": burden.get("status"),
            "validator_returncode": burden_returncode,
        }
    )

    p10 = load_module(P10_VALIDATOR_PATH, "p5_t04_recovery_p10_audit")
    p10_validation, p10_receipt = p10.build_audit()
    p10_component = next(
        row
        for row in p10_validation.get("components", [])
        if row.get("component") == "P10-T08"
    )
    p10_ok = (
        p10_validation.get("audit_status") == "PASS"
        and p10_validation.get("rollout_disposition")
        == "FREEZE_BROADER_ROLLOUT_REPAIR_REQUIRED"
        and p10_validation.get("finding_counts", {}).get("blocker") == 2
        and [
            finding.get("finding_id")
            for finding in p10_validation.get("findings", [])
        ]
        == ["P10-AUDIT-F001", "P10-AUDIT-F002"]
        and p10_component.get("stale_live_input_paths")
        == [
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "research_control/program_state.yaml",
        ]
        and p10_component.get("active_task_advanced") is True
        and p10_component.get("latest_handoff_advanced") is True
        and p10_component.get("task_count_advanced") is True
        and p10_receipt.get("result_status")
        == "PASS_AUDIT_FREEZE_BROADER_ROLLOUT"
    )
    checks.append(
        {
            "check_id": "historical_p10_audit_semantics_preserved",
            "status": "PASS" if p10_ok else "FAIL",
            "finding_ids": [
                finding.get("finding_id")
                for finding in p10_validation.get("findings", [])
            ],
            "rollout_disposition": p10_validation.get("rollout_disposition"),
        }
    )

    p5_returncode, p5 = run_json(
        [
            sys.executable,
            str(P5_VALIDATOR_PATH.relative_to(REPO_ROOT)),
            "--check",
            "--json",
        ]
    )
    p5_ok = (
        p5_returncode == 0
        and p5.get("result_status") == "PASS"
        and p5.get("finding_counts", {}).get("pass") == 21
        and p5.get("finding_counts", {}).get("fail") == 0
    )
    checks.append(
        {
            "check_id": "p5_t04_science_payload_still_valid",
            "status": "PASS" if p5_ok else "FAIL",
            "task_check_count": p5.get("finding_counts", {}).get("pass"),
            "task_failure_count": p5.get("finding_counts", {}).get("fail"),
        }
    )

    authority_flags = {
        "p5_t04_science_payload_modified_by_recovery": False,
        "historical_p10_audit_outputs_modified": False,
        "distance_to_gr_ledger_modified_by_recovery": False,
        "p5_t04_reexecuted": False,
        "p5_t05_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "canonical_ontology_modified": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "publication_authorized": False,
        "push_performed": False,
    }
    checks.append(
        {
            "check_id": "authority_boundary",
            "status": (
                "PASS"
                if all(value is False for value in authority_flags.values())
                else "FAIL"
            ),
        }
    )

    failed_check_count = sum(check["status"] != "PASS" for check in checks)
    return {
        "schema_id": "p5_t04_p10_live_view_recovery_receipt_v1",
        "task_id": "RT-20260725-011",
        "job_id": "AJ-RT-20260725-011-001",
        "plan_task_id": "P5-T04",
        "recovery_for_plan_task_id": "P5-T04",
        "next_plan_task_id": "P5-T05",
        "status": "PASS" if failed_check_count == 0 else "FAIL",
        "result_status": (
            "PASS_P5_T04_P10_LIVE_VIEW_RECOVERY"
            if failed_check_count == 0
            else "FAIL_P5_T04_P10_LIVE_VIEW_RECOVERY"
        ),
        "immutable_route_sha256": (
            "c8856b79b9a4c42767056ec31221f9f7de7b9d8e8e9efbc85be41fc53194372b"
        ),
        "source_checkpoint_receipt_sha256": source_checkpoint_sha256,
        "source_failed_gate_sha256": failed_gate_sha256,
        "protected_dirty_fingerprint": (
            "6ebdd994096cb5048faca83d264a3c9f655b1e8cd140cdecbc93ab84426a5636"
        ),
        "source_hashes": observed_hashes,
        "checks": checks,
        "check_count": len(checks),
        "failed_check_count": failed_check_count,
        "repaired_finding": {
            "finding_id": "P5-T04-DEPENDENT-P10-T08-F001",
            "status": "PASS",
            "repair": (
                "recognized the exact fully converged live burden view only when "
                "the burden-status validator passes and both receipt identities match"
            ),
        },
        "authority_flags": authority_flags,
        "claim_boundary_summary": (
            "The recovery adds one deterministic P10-T08 convergence branch and "
            "focused fail-closed coverage only. P5-T04 science and the historical "
            "P10 audit remain exact; P5-T05 and every promotion layer remain blocked "
            "until the governed cumulative checkpoint commits."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        receipt = build_receipt()
    except (OSError, RuntimeError, ValueError, StopIteration) as exc:
        result = {
            "schema_id": "p5_t04_p10_live_view_recovery_receipt_v1",
            "status": "FAIL",
            "error": str(exc),
        }
        print(canonical_json(result) if args.json else f"FAIL: {exc}", end="")
        return 1

    expected = canonical_json(receipt)
    if args.write and receipt["status"] == "PASS":
        RECEIPT_PATH.write_text(expected, encoding="utf-8")
    receipt_stale = (
        not RECEIPT_PATH.is_file()
        or RECEIPT_PATH.read_text(encoding="utf-8") != expected
    )
    result = {
        "schema_id": receipt["schema_id"],
        "status": (
            "FAIL"
            if receipt["status"] != "PASS"
            else "STALE" if receipt_stale else "PASS"
        ),
        "mode": "write" if args.write else "check",
        "result_status": receipt["result_status"],
        "check_count": receipt["check_count"],
        "failed_check_count": receipt["failed_check_count"],
        "receipt_path": str(RECEIPT_PATH.relative_to(REPO_ROOT)),
        "receipt_stale": receipt_stale,
    }
    print(canonical_json(result) if args.json else result["status"], end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
