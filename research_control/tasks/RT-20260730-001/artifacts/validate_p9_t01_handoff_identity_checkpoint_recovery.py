#!/usr/bin/env python3
"""Validate the sealed one-file P9-T01 handoff-identity checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260730-001"
JOB_ID = "AJ-RT-20260730-001-001"
GOAL_ID = "crg-20260720T161354Z-96bc2664ce31bfe0"
GENERATION = 167
ROUTE_SHA256 = "df43b73405e46c75791ee8499dbec1d30ddb97bfecfdb42fa3089c843da02a28"
DIRTY_MANIFEST_SHA256 = (
    "769f2b443466d320ecb29b4d9b28e7148c22625969b786dc7d1180450c631576"
)
FAILED_GATE_EVIDENCE_SHA256 = (
    "17d12413e2841f9d4c1a79053e2d2f29a368b20ae19fd9e84afd8879b06abb6d"
)
CHECKPOINT_RECEIPT_SHA256 = (
    "274c48f32e09a36fa7b5abd813c1c9d11beee746f54880f8032a730a24819288"
)
SOURCE_HEAD = "c65c2d40cff97ecd96de1c59bd220a9f1274dfc6"
TARGET = "research_control/handoffs/handoff-0908.md"
EXPECTED_TARGET_BEFORE = (
    "6a95b3f7b84e5e97a677e1c7109f2c0432c6a1f6eb1a3e41a0a8f7695342c102"
)
EXPECTED_TARGET_AFTER = (
    "d2edce09694674ffb5d716f89705b086613b3a3cc4b6dbb7d9962254f637c058"
)
OLD_HEADING = b"# Handoff 0908 \xe2\x80\x94 P9-T01 source-derived benchmark protocol\n"
NEW_HEADING = (
    b"# Handoff handoff-0908 \xe2\x80\x94 P9-T01 source-derived benchmark protocol\n"
)
GOAL_PATH = (
    ROOT
    / ".codex/skills/continue-research-goal/goals/"
    "goal-crg-20260720T161354Z-96bc2664ce31bfe0.md"
)
CHECKPOINT_RECEIPT_PATH = (
    ROOT
    / ".local/validation-receipts/"
    "5fdb4a94a5136a980b14c90b290edc80d5bffc547f521ef9a53db6c9866d794a/"
    "RUN-CHECKPOINT-d4b744e9ba969f6e/receipt.json"
)
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260730-001/artifacts/"
    "p9_t01_handoff_identity_checkpoint_recovery_receipt.json"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def load_goal() -> dict[str, Any]:
    lines = GOAL_PATH.read_text(encoding="utf-8").splitlines()
    delimiters = [index for index, line in enumerate(lines) if line == "---"]
    if len(delimiters) < 2:
        raise ValueError("goal frontmatter delimiters are missing")
    payload = json.loads("\n".join(lines[delimiters[0] + 1 : delimiters[1]]))
    if not isinstance(payload, dict):
        raise ValueError("goal frontmatter is not a mapping")
    return payload


def generation_route(goal: dict[str, Any]) -> dict[str, Any]:
    generation = goal.get("generations", {}).get(str(GENERATION), {})
    route = generation.get("route")
    if not isinstance(route, dict):
        raise ValueError("generation-167 route is missing")
    return route


def checkpoint_gate(receipt: dict[str, Any]) -> dict[str, Any]:
    for gate in receipt.get("gate_results", []):
        if isinstance(gate, dict) and gate.get("gate_id") == "test_shard_repository":
            return gate
    return {}


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    goal = load_goal()
    route = generation_route(goal)
    manifest = route.get("dirty_state_manifest", {})
    entries = manifest.get("changed_paths", [])
    manifest_by_path = {
        str(item["path"]): str(item["sha256"])
        for item in entries
        if isinstance(item, dict) and item.get("path") and item.get("sha256")
    }

    if canonical_sha256(route) != ROUTE_SHA256:
        errors.append("immutable route canonical hash mismatch")
    if canonical_sha256(manifest) != DIRTY_MANIFEST_SHA256:
        errors.append("dirty manifest canonical hash mismatch")
    if len(manifest_by_path) != 61:
        errors.append(f"expected 61 manifest paths, observed {len(manifest_by_path)}")
    if manifest_by_path.get(TARGET) != EXPECTED_TARGET_BEFORE:
        errors.append("repair target is absent or has the wrong sealed before hash")
    failed_gates = manifest.get("failed_gates", [])
    if failed_gates != [
        {
            "evidence_sha256": FAILED_GATE_EVIDENCE_SHA256,
            "gate_id": "test_shard_repository",
            "status": "FAIL_HANDOFF_0908_MARKDOWN_IDENTITY_4_FAILURES_1_ERROR",
        }
    ]:
        errors.append("sealed failed-gate identity mismatch")
    if manifest.get("head") != SOURCE_HEAD:
        errors.append("sealed source HEAD mismatch")

    target_data = (ROOT / TARGET).read_bytes()
    target_after = sha256_bytes(target_data)
    exact_identity_insertion = (
        target_after == EXPECTED_TARGET_AFTER
        and target_data.count(NEW_HEADING) == 1
        and target_data.count(OLD_HEADING) == 0
        and sha256_bytes(target_data.replace(NEW_HEADING, OLD_HEADING, 1))
        == EXPECTED_TARGET_BEFORE
        and len(NEW_HEADING) - len(OLD_HEADING) == 8
    )
    if not exact_identity_insertion:
        errors.append("target is not the exact authorized identity insertion")

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

    receipt_hash = sha256(CHECKPOINT_RECEIPT_PATH)
    if receipt_hash != CHECKPOINT_RECEIPT_SHA256:
        errors.append("failed checkpoint receipt hash mismatch")
    checkpoint_receipt = json.loads(
        CHECKPOINT_RECEIPT_PATH.read_text(encoding="utf-8")
    )
    gate = checkpoint_gate(checkpoint_receipt)
    stderr_path = Path(str(gate.get("stderr_path", "")))
    stderr_text = (
        stderr_path.read_text(encoding="utf-8") if stderr_path.is_file() else ""
    )
    failure_literal = (
        "[latest_handoff] research_control/handoffs/handoff-0908.md "
        "does not identify handoff-0908"
    )
    if checkpoint_receipt.get("status") != "FAIL":
        errors.append("source checkpoint receipt is not FAIL")
    if gate.get("status") != "FAIL" or gate.get("exit_code") != 1:
        errors.append("source checkpoint repository gate is not the expected failure")
    if failure_literal not in stderr_text:
        errors.append("source checkpoint failure does not name the identity defect")

    return {
        "schema_id": "p9_t01_handoff_identity_checkpoint_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "goal_id": GOAL_ID,
        "generation": GENERATION,
        "strategy_id": "repair_handoff_0908_markdown_identity_and_checkpoint_p9_t01_v1",
        "route_sha256": ROUTE_SHA256,
        "dirty_state_manifest_sha256": DIRTY_MANIFEST_SHA256,
        "source_head": SOURCE_HEAD,
        "source_task_id": "RT-20260729-012",
        "source_job_id": "AJ-RT-20260729-012-001",
        "source_handoff_id": "handoff-0908",
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
                "exact_eight_byte_identity_insertion": exact_identity_insertion,
                "literal_identity_present": "handoff-0908"
                in target_data.decode("utf-8"),
            },
            "checkpoint_receipt_sha256": receipt_hash,
            "failed_gate_evidence_sha256": FAILED_GATE_EVIDENCE_SHA256,
            "source_checkpoint_status": checkpoint_receipt.get("status"),
            "source_repository_gate_status": gate.get("status"),
            "source_failure_literal_present": failure_literal in stderr_text,
            "p9_t01_science_payload_modified": False,
            "p9_t01_reexecuted": False,
            "p9_t02_executed": False,
            "benchmark_case_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
        },
        "authority_limits": {
            "p9_t01_protocol_preserved": True,
            "benchmark_case_executed": False,
            "Gate_D_changed": False,
            "Gate_E_verdict_issued": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized_by_recovery": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "p9_t02_executed": False,
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
    if checks.get("manifest_path_count") != 61:
        errors.append("sealed recovery receipt manifest count mismatch")
    if checks.get("non_target_hash_mismatch_count") != 0:
        errors.append("sealed recovery receipt records non-target drift")

    target_data = (ROOT / TARGET).read_bytes()
    target_match = (
        sha256_bytes(target_data) == EXPECTED_TARGET_AFTER
        and target_data.count(NEW_HEADING) == 1
        and target_data.count(OLD_HEADING) == 0
    )
    if not target_match:
        errors.append("live target recovery hash mismatch")

    return {
        "schema_id": "p9_t01_handoff_identity_checkpoint_recovery_check_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "sealed_receipt_sha256": sha256(REPORT_PATH),
        "live_target_after_sha256": sha256_bytes(target_data),
        "live_target_match": target_match,
        "p9_t01_reexecuted": False,
        "p9_t02_executed": False,
        "scientific_status_changed": False,
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
