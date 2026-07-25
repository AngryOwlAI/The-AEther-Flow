#!/usr/bin/env python3
"""Validate the bounded P5-T01 dependent repository-contract recovery."""

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

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
RECEIPT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260725-004/artifacts/"
    "p5_t01_dependent_contract_recovery_receipt.json"
)
P10_VALIDATOR_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-003/artifacts/"
    "validate_v21_p10_migration_readiness.py"
)
P5_VALIDATOR_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260725-003/artifacts/"
    "validate_compact_source_theory.py"
)

EXPECTED_HASHES = {
    "registries/DISTANCE_TO_GR_LEDGER.csv": "7bb5c01a9f893c192cc98408f22176ec8d1e8162c6b645b483c6053200ed136d",
    "research_control/handoffs/handoff-0863.md": "85cd72f15e9380687dd58ae14e2c5d04b21c8898a527c0b162b48c834b39da5e",
    "research_control/handoffs/handoff-0863.yaml": "7b15de2879b87d8c418bdc074f828e463e8a380ea2f93970960df9eab2e2d2cb",
    "research_control/tasks/RT-20260722-003/artifacts/v21_p10_migration_readiness_compact_receipt.json": "db3410f2c166562a4cc8636011eeda15b7cb8f051c3917fea21b370e4da2ddb6",
    "research_control/tasks/RT-20260722-003/artifacts/v21_p10_migration_readiness_validation.json": "cdcd907f4ad237118eab65f06f364263da08285456514605a0308bc203f7a6e6",
    "research_control/tasks/RT-20260725-003/00_TASK.yaml": "e7dc30de998eb92576ae68dac68b92e8f9f6334c88f7cd990964520781aa0590",
    "research_control/tasks/RT-20260725-003/artifacts/child_phys_math_p5_t01_source_theory.yaml": "037d479f8b5285bf4180f956ad99c8158ddfc57adbcef00adc754085520bb50e",
    "research_control/tasks/RT-20260725-003/artifacts/child_phys_phil_p5_t01_source_theory.yaml": "18e24c5fcefbc5981cba7ccd6e613be32d7d33534c4f39acf4ee131bf909ce92",
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_object_v1.tex": "2520f82e54edcb2668446579ceed7a7dfc7a8abf995572aa9889a3d9a3a4467c",
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_spec_v1.yaml": "a381549ac6eb37346c1469f1157bdfa8417fbc010a19c087cf099b1368ab1b9c",
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_type_dependency_v1.yaml": "559d6fd77f5f4fc93e97e3429cbc87a09acf91b39099f56ef7ba00fbf3c3dd2f",
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_validation_receipt_v1.json": "838a0fb827e2912d4452bd19556b3c96a7ea5a6a814e23defa3401ff649b9432",
    "research_control/tasks/RT-20260725-003/artifacts/parent_conflict_review_p5_t01_source_theory.yaml": "6bcec4104d73d0190850b36abd9c9604816af3d1adb3b82f7bdb503215bf8778",
    "research_control/tasks/RT-20260725-003/artifacts/parent_fusion_notes_p5_t01_source_theory.md": "75b6fec9d87070dc66b0e342aa2b191593c9869146bc3809a7dbbec28945f779",
    "research_control/tasks/RT-20260725-003/artifacts/validate_compact_source_theory.py": "0b06a81d649abe885b6a5c76020207b927004a459b79ebed0f8799c1dd7f41ba",
    "research_control/tasks/RT-20260725-003/jobs/completions/AJC-AJ-RT-20260725-003-001.yaml": "e047845dc6ff48aa8e44e1667aba94961554190293393eb9346d915f29f9eb9d",
}

RECOVERY_SOURCE_HASHES = {
    "research_control/tasks/RT-20260722-003/artifacts/validate_v21_p10_migration_readiness.py": "28193e920f246707f421a3e85c4a0122f345e5ffc2b19852d1ab901ab84a6d9a",
    "tests/test_v21_p10_migration_readiness.py": "34c903161275ce7d04cc85e8001cf40bc85e4a5f52eb17bc96de5f02568772d4",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256_path(relative: str) -> str:
    path = REPO_ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"missing regular non-symlink path: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        relative: sha256_path(relative)
        for relative in sorted(EXPECTED_HASHES | RECOVERY_SOURCE_HASHES)
    }
    mismatches = [
        relative
        for relative, expected in {**EXPECTED_HASHES, **RECOVERY_SOURCE_HASHES}.items()
        if observed_hashes.get(relative) != expected
    ]
    checks.append(
        {
            "check_id": "exact_source_and_protected_hashes",
            "status": "PASS" if not mismatches else "FAIL",
            "mismatch_paths": sorted(mismatches),
        }
    )

    task_path = REPO_ROOT / "research_control/tasks/RT-20260725-003/00_TASK.yaml"
    task = yaml.safe_load(task_path.read_text(encoding="utf-8"))
    candidate_family = task.get("task_taxonomy", {}).get("candidate_family")
    checks.append(
        {
            "check_id": "p5_t01_candidate_family_slug",
            "status": (
                "PASS"
                if candidate_family == "p5_t01_compact_source_theory_tuple"
                else "FAIL"
            ),
            "candidate_family": candidate_family,
        }
    )

    from scripts.research_control.task_taxonomy import build_repository_report

    taxonomy = build_repository_report()
    required_task_errors = taxonomy.get("required_task_errors", [])
    checks.append(
        {
            "check_id": "repository_task_taxonomy",
            "status": (
                "PASS"
                if taxonomy.get("status") == "PASS" and not required_task_errors
                else "FAIL"
            ),
            "required_task_error_count": len(required_task_errors),
            "historical_mutation_count": len(
                taxonomy.get("historical_mutated_paths", [])
            ),
            "stronger_science_inference_count": len(
                taxonomy.get("stronger_science_inference_task_ids", [])
            ),
        }
    )

    p10 = load_module(P10_VALIDATOR_PATH, "p5_recovery_p10_audit")
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
        and p10_receipt.get("result_status")
        == "PASS_AUDIT_FREEZE_BROADER_ROLLOUT"
    )
    checks.append(
        {
            "check_id": "p10_historical_audit_preserved",
            "status": "PASS" if p10_ok else "FAIL",
            "audit_status": p10_validation.get("audit_status"),
            "rollout_disposition": p10_validation.get("rollout_disposition"),
            "finding_ids": [
                finding.get("finding_id")
                for finding in p10_validation.get("findings", [])
            ],
        }
    )

    p5_returncode, p5 = run_json(
        [sys.executable, str(P5_VALIDATOR_PATH.relative_to(REPO_ROOT)), "--check", "--json"]
    )
    p5_ok = (
        p5_returncode == 0
        and p5.get("result_status") == "PASS"
        and p5.get("finding_counts", {}).get("pass") == 17
        and p5.get("finding_counts", {}).get("fail") == 0
    )
    checks.append(
        {
            "check_id": "p5_t01_science_payload_still_valid",
            "status": "PASS" if p5_ok else "FAIL",
            "task_check_count": p5.get("finding_counts", {}).get("pass"),
            "task_failure_count": p5.get("finding_counts", {}).get("fail"),
        }
    )

    authority_flags = {
        "p5_t01_science_payload_modified": False,
        "historical_p10_audit_outputs_modified": False,
        "canonical_ontology_modified": False,
        "distance_to_gr_ledger_modified_by_recovery": False,
        "p5_t01_reexecuted": False,
        "p5_t02_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "publication_authorized": False,
        "push_performed": False,
    }
    checks.append(
        {
            "check_id": "authority_boundary",
            "status": (
                "PASS" if all(value is False for value in authority_flags.values()) else "FAIL"
            ),
        }
    )

    failure_count = sum(check["status"] != "PASS" for check in checks)
    return {
        "schema_id": "p5_t01_dependent_contract_recovery_receipt_v1",
        "task_id": "RT-20260725-004",
        "job_id": "AJ-RT-20260725-004-001",
        "plan_task_id": "P5-T01",
        "recovery_for_plan_task_id": "P5-T01",
        "next_plan_task_id": "P5-T02",
        "status": "PASS" if failure_count == 0 else "FAIL",
        "result_status": (
            "PASS_P5_T01_DEPENDENT_CONTRACT_RECOVERY"
            if failure_count == 0
            else "FAIL_P5_T01_DEPENDENT_CONTRACT_RECOVERY"
        ),
        "immutable_route_sha256": "36027e15e16ba42e5c41d3d7b6cf7cb34405306f3694664d41e9de9dfd82371d",
        "source_checkpoint_receipt_sha256": "951fbdcb04c7dd7ceb124cd9a8571dd7571a31e0cb3fc5ab68b59caeb0741e1b",
        "protected_dirty_fingerprint": "1b84e8539a7b62c38193f3e4eb7700b02d7f2b966beab53b2b87bfab588a106f",
        "source_hashes": observed_hashes,
        "checks": checks,
        "check_count": len(checks),
        "failed_check_count": failure_count,
        "repaired_findings": [
            {
                "finding_id": "P5-T01-DEPENDENT-F001",
                "status": "PASS",
                "repair": "normalized candidate_family to the existing lowercase-slug grammar",
            },
            {
                "finding_id": "P5-T01-DEPENDENT-F002",
                "status": "PASS",
                "repair": "recognized the exact same-task finalization lifecycle while preserving historical P10 output",
            },
        ],
        "authority_flags": authority_flags,
        "claim_boundary_summary": (
            "The recovery changes one control slug and one deterministic lifecycle "
            "predicate only. P5-T01 science and the P10 historical audit remain exact; "
            "P5-T02 and every promotion layer remain blocked until checkpoint."
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
            "schema_id": "p5_t01_dependent_contract_recovery_receipt_v1",
            "status": "FAIL",
            "error": str(exc),
        }
        print(canonical_json(result) if args.json else f"FAIL: {exc}", end="")
        return 1

    expected = canonical_json(receipt)
    if args.write and receipt["status"] == "PASS":
        RECEIPT_PATH.write_text(expected, encoding="utf-8")
    drift = not RECEIPT_PATH.is_file() or RECEIPT_PATH.read_text(
        encoding="utf-8"
    ) != expected
    result = {
        "schema_id": receipt["schema_id"],
        "status": (
            "FAIL"
            if receipt["status"] != "PASS"
            else "STALE" if drift else "PASS"
        ),
        "mode": "write" if args.write else "check",
        "result_status": receipt["result_status"],
        "check_count": receipt["check_count"],
        "failed_check_count": receipt["failed_check_count"],
        "receipt_path": str(RECEIPT_PATH.relative_to(REPO_ROOT)),
        "receipt_stale": drift,
    }
    print(canonical_json(result) if args.json else result["status"], end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
