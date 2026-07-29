#!/usr/bin/env python3
"""Validate the sealed one-file P7-T08 EOF-only checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260729-002"
JOB_ID = "AJ-RT-20260729-002-001"
GOAL_ID = "crg-20260720T161354Z-96bc2664ce31bfe0"
GENERATION = 155
ROUTE_SHA256 = "247bb15632630937ef3fa8ba20e1de6e60519f763f6be2089caf2d30e7160a54"
DIRTY_MANIFEST_SHA256 = (
    "9248e8128ed25f2e93cb471f86f85c88493effcf16c4829260ded2eb02e122ef"
)
BLOCKER_SHA256 = (
    "b200ae6b0bea1d67ad7937a7ca319a7bde88b2714928798529bd306b19bd60a1"
)
CHECKPOINT_RECEIPT_SHA256 = (
    "1a29f74f3bf66c5db2b24a62bfac058b770c64df0487d737089e92bfafa6e246"
)
FAILED_GATE_STDOUT_SHA256 = (
    "0f0aaaf4e167858676c2aae33878f488e16bb360a013983cf12e0174f8f37be4"
)
SOURCE_HEAD = "79d9564df65e6f09b2742dc0b47f3d039c2ec658"
TARGET = "research_control/handoffs/handoff-0897.md"
EXPECTED_TARGET_BEFORE = (
    "d9cf6ec5be8d4a91e054cb9eb1f987f6cbbc5215697d17583b19d5f52b1eda45"
)
EXPECTED_TARGET_AFTER = (
    "55a0fbc58436ec6518bf26e5d29171b777c065c1822cb3720eedc95e84d97bff"
)
GOAL_PATH = (
    ROOT
    / ".codex/skills/continue-research-goal/goals/"
    "goal-crg-20260720T161354Z-96bc2664ce31bfe0.md"
)
BLOCKER_PATH = (
    ROOT
    / "research_control/tasks/RT-20260729-001/artifacts/"
    "validation_blocker_checkpoint_single_eof_handoff_0897_v1.yaml"
)
CHECKPOINT_RECEIPT_PATH = (
    ROOT
    / ".local/validation-receipts/"
    "528658a2d6edc8398b2ed0909f94147fc3d7c2041a6c0943243cfa662bb6ba5b/"
    "RUN-CHECKPOINT-26e4b355976485c9/receipt.json"
)
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260729-002/artifacts/"
    "p7_t08_eof_checkpoint_recovery_receipt.json"
)

PROTECTED_LIVE_PATHS = {
    "research_control/approvals/approval-20260729-001.yaml": (
        "936d831daa555eb60e836e3f1d84beff72f7864dd83a36c082ca6783163b2e14"
    ),
    "research_control/handoffs/handoff-0897.yaml": (
        "5462a222734037f7b21eb3b99954e480bb71e9b3b93a48c922b469d5e032b2ef"
    ),
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "human_authorization_p7_t08_physical_matter_adoption_v1.yaml"
    ): "9da90540e60a9bc1b624689a4b694460c77ac5d99306319dcedefb291be9a6f2",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "child_phys_math_p7_t08_gate_c_adoption.yaml"
    ): "633b022b8ac4944523ca3a970166d706a54105710f41e6ead547ef18f7b2be9f",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "child_phys_phil_p7_t08_gate_c_adoption.yaml"
    ): "d926f936442816cb402e9184059d02369b8b1ffa1b367305bd388d04999c39c7",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "parent_conflict_review_p7_t08_gate_c_adoption.yaml"
    ): "e183c92a3bd9543f1b89f47ae01e7eef73b3f763077e16c7ef8c7eb0e62899ab",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "parent_fusion_notes_p7_t08_gate_c_adoption.md"
    ): "da3f65a242b878c58312caf1dff7cd88dc9a5e04754c24a68416cc61fd9371aa",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "p7_t08_gate_c_decision_v1.tex"
    ): "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "p7_t08_dimension_adoption_matrix_v1.yaml"
    ): "d2675d6476591f895b6f4131090cc97f80fbb916f912ea9f7ee841b91f4d049a",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "p7_t08_constitutive_postulate_ledger_v1.yaml"
    ): "e11f5e4ae886932cad618caa3ee97e973bbd38d363db25776fe1fbd2c27451dc",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "p7_t08_scientific_status_v1.yaml"
    ): "5f84e9c0495514632e7b6c25a809e4e6c1044c69f159ce0e1e38900fc5229d73",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "p7_t08_gate_c_compact_receipt_v1.json"
    ): "334173c85231f2066509aab5feb4ab4674119829aa5a1683d0e228a824e73ad3",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "p7_t08_gate_c_validation_v1.json"
    ): "116e07af1684016cbc09086f4e10ae42d5d70d9bef7940c3c3b07c1f1ff27cec",
    (
        "research_control/tasks/RT-20260729-001/artifacts/"
        "validate_p7_t08_gate_c_adoption.py"
    ): "d8c2bb51282c3e5e40ec1e5f34f56b886cb87586a395625e093d3c2113218a17",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(file_path: Path) -> str:
    return sha256_bytes(file_path.read_bytes())


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def load_goal() -> dict[str, Any]:
    text = GOAL_PATH.read_text(encoding="utf-8")
    frontmatter, _ = text[4:].split("\n---\n", 1)
    payload = yaml.safe_load(frontmatter)
    if not isinstance(payload, dict):
        raise ValueError("goal frontmatter is not a mapping")
    return payload


def recovery_route(goal: dict[str, Any]) -> dict[str, Any]:
    entries = goal.get("recovery_ledger", [])
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("approved_for_generation") != GENERATION:
            continue
        route = entry.get("route")
        if isinstance(route, dict):
            return route
    raise ValueError("generation-155 recovery route is missing")


def checkpoint_failure_stdout(receipt: dict[str, Any]) -> str:
    for gate in receipt.get("gate_results", []):
        if not isinstance(gate, dict) or gate.get("gate_id") != "git_diff_check":
            continue
        stdout_path = gate.get("stdout_path")
        if isinstance(stdout_path, str) and Path(stdout_path).is_file():
            return Path(stdout_path).read_text(encoding="utf-8")
    return ""


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    route = recovery_route(load_goal())
    manifest = route.get("dirty_state_manifest", {})
    manifest_entries = manifest.get("changed_paths", [])
    manifest_by_path = {
        str(item["path"]): str(item["sha256"])
        for item in manifest_entries
        if isinstance(item, dict) and item.get("path") and item.get("sha256")
    }

    if canonical_sha256(route) != ROUTE_SHA256:
        errors.append("immutable route canonical hash mismatch")
    if canonical_sha256(manifest) != DIRTY_MANIFEST_SHA256:
        errors.append("dirty manifest canonical hash mismatch")
    if len(manifest_by_path) != 66:
        errors.append(f"expected 66 manifest paths, observed {len(manifest_by_path)}")
    if manifest_by_path.get(TARGET) != EXPECTED_TARGET_BEFORE:
        errors.append("repair target is absent or has the wrong sealed before hash")

    target_data = (ROOT / TARGET).read_bytes()
    target_after = sha256_bytes(target_data)
    exact_one_newline_removed = (
        target_after == EXPECTED_TARGET_AFTER
        and target_data.endswith(b"\n")
        and not target_data.endswith(b"\n\n")
        and sha256_bytes(target_data + b"\n") == EXPECTED_TARGET_BEFORE
    )
    if not exact_one_newline_removed:
        errors.append("target is not the exact authorized one-newline deletion")

    non_target_mismatches: list[str] = []
    for relative, expected in manifest_by_path.items():
        if relative == TARGET:
            continue
        live_path = ROOT / relative
        if not live_path.is_file() or sha256(live_path) != expected:
            non_target_mismatches.append(relative)
    if non_target_mismatches:
        errors.append(
            f"{len(non_target_mismatches)} non-target dirty-manifest paths changed"
        )

    if sha256(BLOCKER_PATH) != BLOCKER_SHA256:
        errors.append("tracked blocker hash mismatch")
    checkpoint_receipt_hash = sha256(CHECKPOINT_RECEIPT_PATH)
    if checkpoint_receipt_hash != CHECKPOINT_RECEIPT_SHA256:
        errors.append("failed checkpoint receipt hash mismatch")
    checkpoint_receipt = json.loads(
        CHECKPOINT_RECEIPT_PATH.read_text(encoding="utf-8")
    )
    failure_stdout = checkpoint_failure_stdout(checkpoint_receipt)
    failure_stdout_hash = sha256_bytes(failure_stdout.encode("utf-8"))
    if failure_stdout_hash != FAILED_GATE_STDOUT_SHA256:
        errors.append("failed git-diff evidence hash mismatch")
    if TARGET not in failure_stdout:
        errors.append("failed git-diff evidence does not name the repair target")

    protected_checks: dict[str, Any] = {}
    for relative, expected in PROTECTED_LIVE_PATHS.items():
        observed = sha256(ROOT / relative)
        match = observed == expected
        protected_checks[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": match,
        }
        if not match:
            errors.append(f"protected P7-T08 hash mismatch: {relative}")

    return {
        "schema_id": "p7_t08_eof_checkpoint_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "goal_id": GOAL_ID,
        "generation": GENERATION,
        "strategy_id": "repair_p7_t08_single_eof_blank_line_and_checkpoint_v1",
        "route_sha256": ROUTE_SHA256,
        "dirty_state_manifest_sha256": DIRTY_MANIFEST_SHA256,
        "source_head": SOURCE_HEAD,
        "source_task_id": "RT-20260729-001",
        "source_job_id": "AJ-RT-20260729-001-001",
        "source_handoff_id": "handoff-0897",
        "checks": {
            "manifest_path_count": len(manifest_by_path),
            "target_path_count": 1,
            "non_target_path_count": len(manifest_by_path) - 1,
            "non_target_hash_mismatch_count": len(non_target_mismatches),
            "non_target_hash_mismatches": non_target_mismatches,
            "target": {
                "path": TARGET,
                "before_sha256": EXPECTED_TARGET_BEFORE,
                "after_sha256": target_after,
                "exact_one_final_newline_removed": exact_one_newline_removed,
                "ends_with_one_newline": target_data.endswith(b"\n")
                and not target_data.endswith(b"\n\n"),
            },
            "blocker_sha256": sha256(BLOCKER_PATH),
            "checkpoint_receipt_sha256": checkpoint_receipt_hash,
            "checkpoint_failure_stdout_sha256": failure_stdout_hash,
            "protected_live_paths": protected_checks,
            "p7_t08_science_payload_modified": False,
            "p7_t08_reexecuted": False,
            "approval_reused": False,
            "p8_t01_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
        },
        "authority_limits": {
            "scientific_adoption_result_preserved": True,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized_by_recovery": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "p8_t01_executed": False,
        },
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }


def check_sealed_report() -> dict[str, Any]:
    errors: list[str] = []
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    checks = report.get("checks", {})
    if report.get("validation_status") != "PASS":
        errors.append("sealed recovery receipt is not PASS")
    if report.get("route_sha256") != ROUTE_SHA256:
        errors.append("sealed recovery receipt route hash mismatch")
    if checks.get("manifest_path_count") != 66:
        errors.append("sealed recovery receipt manifest count mismatch")
    if checks.get("non_target_hash_mismatch_count") != 0:
        errors.append("sealed recovery receipt records non-target drift")

    target_data = (ROOT / TARGET).read_bytes()
    target_match = (
        sha256_bytes(target_data) == EXPECTED_TARGET_AFTER
        and target_data.endswith(b"\n")
        and not target_data.endswith(b"\n\n")
    )
    if not target_match:
        errors.append("live target recovery hash mismatch")

    live_protected: dict[str, Any] = {}
    for relative, expected in PROTECTED_LIVE_PATHS.items():
        observed = sha256(ROOT / relative)
        match = observed == expected
        live_protected[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": match,
        }
        if not match:
            errors.append(f"live protected P7-T08 hash mismatch: {relative}")

    return {
        "schema_id": "p7_t08_eof_checkpoint_recovery_check_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "sealed_receipt_sha256": sha256(REPORT_PATH),
        "live_target_after_sha256": sha256_bytes(target_data),
        "live_target_match": target_match,
        "live_protected_checks": live_protected,
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = check_sealed_report() if args.check else build_report()
    if args.write_report and not args.check:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
