#!/usr/bin/env python3
"""Validate the sealed one-file P6-T02 EOF-only checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260726-004"
JOB_ID = "AJ-RT-20260726-004-001"
GOAL_ID = "crg-20260720T161354Z-96bc2664ce31bfe0"
GENERATION = 123
ROUTE_SHA256 = "56b77727400bb9731c5f3d4656fb86ab790faab8b70509410f23b4fceaab1816"
DIRTY_MANIFEST_SHA256 = (
    "f39a2c8856ffc11442fc79648de2bcc67ff6767a70ea68b8f6dca566f7244767"
)
FAILED_GATE_EVIDENCE_SHA256 = (
    "67fe7ce5b1678c0faa618457e783aded2c7fa684e770195ded793cabd5fb6330"
)
CHECKPOINT_RECEIPT_SHA256 = (
    "7b6c139a4b1f43557665e6856e09041447f08fb1fd4af5b4a083a13c61af416e"
)
SOURCE_HEAD = "6f50f4997ae97e870b317616c8a895fe641b00f1"
GOAL_PATH = (
    ROOT
    / ".codex/skills/continue-research-goal/goals/"
    "goal-crg-20260720T161354Z-96bc2664ce31bfe0.md"
)
CHECKPOINT_RECEIPT_PATH = (
    ROOT
    / ".local/validation-receipts/"
    "5fdb4a94a5136a980b14c90b290edc80d5bffc547f521ef9a53db6c9866d794a/"
    "RUN-CHECKPOINT-64db3af728856054/receipt.json"
)
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260726-004/artifacts/"
    "p6_t02_eof_checkpoint_recovery_receipt.json"
)

TARGETS = {
    "research_control/tasks/RT-20260726-003/DDR-20260726-003.md",
}

PROTECTED_LIVE_PATHS = {
    "research_control/handoffs/handoff-0877.yaml": (
        "594d9b485507bac3e82fd04b1f04defd8d366dbe2f9054f2429f11e855dc07db"
    ),
    "research_control/handoffs/handoff-0877.md": (
        "16c6e3cb4968f72bd9afd688f98f3707566c9fd4854f283e31d365788750af7c"
    ),
    "research_control/tasks/RT-20260726-003/00_TASK.yaml": (
        "e83c795ce688975ab6acf4faf9a7ccb283ecdf099da719a36e69fee2ca6a889d"
    ),
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "child_phys_math_p6_t02_source_local_transport.yaml"
    ): "d005c3e5e2eb59b7d504cde93a26d6516be4df3d3d633691a722d782fd87c350",
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "child_phys_phil_p6_t02_source_local_transport.yaml"
    ): "ac52b8a6dd47623e9e6a652435a35dfec8522f2f81b31fcb6e33b7bd90cd477f",
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "parent_conflict_review_p6_t02_source_local_transport.yaml"
    ): "cfe2dbf3570257ce7cdbfbf94746f664b3ee71f4a17eb2d5e9adf9bb215c2a46",
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "parent_fusion_notes_p6_t02_source_local_transport.md"
    ): "f0479873342f29d9503436f81fd76b195d0e41e2e4974862beca36145b68b284",
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "source_local_transport_candidate_receipt.md"
    ): "a49aaf6fd34f92c0191041ab27641328e05c3f69880044b4c848b8d443b50ce2",
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "source_local_transport_candidate_spec_v1.yaml"
    ): "6c9ae2f1f4e3d68ad31940a396ac427e4cdc5744235ea9da1f4edaab6e673c91",
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "source_local_transport_candidate_v1.tex"
    ): "7b446c8660410e655166c0b3124fc37aad9edb8e49b7df2afdc9911c6f560958",
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "source_local_transport_candidate_validation_receipt_v1.json"
    ): "db447660d5a67b27120ebc70785863f51aebb0e2e9071a0f4a96c4cd198daacb",
    (
        "research_control/tasks/RT-20260726-003/artifacts/"
        "validate_source_local_transport_candidate.py"
    ): "8dc1b4eef798da2fc19caf74f635d897dce0230bf71fc6e17764c10e0899b7af",
    (
        "research_control/tasks/RT-20260726-003/jobs/"
        "AJ-RT-20260726-003-001.yaml"
    ): "f758f5116fac18fc4de439f4f76e4d4d74eb38b7b9f92d3df2ca1966c88ec982",
    (
        "research_control/tasks/RT-20260726-003/jobs/completions/"
        "AJC-AJ-RT-20260726-003-001.yaml"
    ): "3a6f1820072975c56dae168bea65074ad67d4fbb0a4434c936b69430d5659ea6",
    (
        "research_control/tasks/RT-20260726-003/roles/"
        "candidate-constructor@0.2.0--RT-20260726-003.yaml"
    ): "0a56ddb2250a537526c7d0265d8de3523292c22c5d09b037147c680c9ca5681f",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(encoded)


def load_goal() -> dict[str, Any]:
    text = GOAL_PATH.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("goal file lacks YAML frontmatter")
    frontmatter, _ = text[4:].split("\n---\n", 1)
    payload = yaml.safe_load(frontmatter)
    if not isinstance(payload, dict):
        raise ValueError("goal frontmatter is not a mapping")
    return payload


def generation_route(goal: dict[str, Any]) -> dict[str, Any]:
    generations = goal.get("generations", {})
    items = generations.values() if isinstance(generations, dict) else generations
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("generation") == GENERATION:
            route = item.get("route")
            if not isinstance(route, dict):
                raise ValueError("generation 123 route is missing")
            return route
    raise ValueError("generation 123 is missing")


def checkpoint_failure_stdout(receipt: dict[str, Any]) -> str:
    results = receipt.get("gate_results", [])
    if isinstance(results, list):
        for gate in results:
            if not isinstance(gate, dict) or gate.get("gate_id") != "git_diff_check":
                continue
            stdout_path = gate.get("stdout_path")
            if isinstance(stdout_path, str) and Path(stdout_path).is_file():
                return Path(stdout_path).read_text(encoding="utf-8")
    return ""


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    goal = load_goal()
    route = generation_route(goal)
    manifest = route.get("dirty_state_manifest", {})
    changed_paths = manifest.get("changed_paths", [])
    manifest_by_path = {
        str(item["path"]): str(item["sha256"])
        for item in changed_paths
        if isinstance(item, dict) and item.get("path") and item.get("sha256")
    }

    if canonical_sha256(manifest) != DIRTY_MANIFEST_SHA256:
        errors.append("dirty manifest canonical hash mismatch")
    if canonical_sha256(route) != ROUTE_SHA256:
        errors.append("immutable route canonical hash mismatch")
    if set(TARGETS) - set(manifest_by_path):
        errors.append("the repair target is absent from the dirty manifest")
    if len(manifest_by_path) != 64:
        errors.append(f"expected 64 manifest paths, observed {len(manifest_by_path)}")

    target_checks: dict[str, Any] = {}
    non_target_mismatches: list[str] = []
    for relative, expected_before in manifest_by_path.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"manifest path missing: {relative}")
            continue
        data = path.read_bytes()
        observed = sha256_bytes(data)
        if relative in TARGETS:
            exact_one_newline_removed = (
                data.endswith(b"\n")
                and not data.endswith(b"\n\n")
                and sha256_bytes(data + b"\n") == expected_before
            )
            target_checks[relative] = {
                "before_sha256": expected_before,
                "after_sha256": observed,
                "exact_one_final_newline_removed": exact_one_newline_removed,
                "ends_with_one_newline": data.endswith(b"\n")
                and not data.endswith(b"\n\n"),
            }
            if not exact_one_newline_removed:
                errors.append(f"target is not an exact one-newline deletion: {relative}")
        elif observed != expected_before:
            non_target_mismatches.append(relative)

    if non_target_mismatches:
        errors.append(
            f"{len(non_target_mismatches)} non-target dirty-manifest hashes changed"
        )

    checkpoint_receipt_hash = sha256(CHECKPOINT_RECEIPT_PATH)
    if checkpoint_receipt_hash != CHECKPOINT_RECEIPT_SHA256:
        errors.append("checkpoint receipt hash mismatch")
    checkpoint_receipt = json.loads(
        CHECKPOINT_RECEIPT_PATH.read_text(encoding="utf-8")
    )
    failure_stdout = checkpoint_failure_stdout(checkpoint_receipt)
    if sha256_bytes(failure_stdout.encode("utf-8")) != FAILED_GATE_EVIDENCE_SHA256:
        errors.append("checkpoint git-diff failure evidence hash mismatch")
    for relative in sorted(TARGETS):
        if relative not in failure_stdout:
            errors.append(f"checkpoint failure does not name target: {relative}")

    protected_checks = {}
    for relative, expected in PROTECTED_LIVE_PATHS.items():
        observed = sha256(ROOT / relative)
        match = observed == expected
        protected_checks[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": match,
        }
        if not match:
            errors.append(f"protected P6-T02 hash mismatch: {relative}")

    return {
        "schema_id": "p6_t02_eof_checkpoint_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "goal_id": GOAL_ID,
        "generation": GENERATION,
        "strategy_id": "repair_p6_t02_single_eof_blank_line_and_checkpoint_v1",
        "route_sha256": ROUTE_SHA256,
        "dirty_state_manifest_sha256": DIRTY_MANIFEST_SHA256,
        "source_head": SOURCE_HEAD,
        "source_task_id": "RT-20260726-003",
        "source_job_id": "AJ-RT-20260726-003-001",
        "source_handoff_id": "handoff-0877",
        "checks": {
            "manifest_path_count": len(manifest_by_path),
            "target_path_count": len(TARGETS),
            "non_target_path_count": len(manifest_by_path) - len(TARGETS),
            "non_target_hash_mismatch_count": len(non_target_mismatches),
            "non_target_hash_mismatches": non_target_mismatches,
            "targets": target_checks,
            "checkpoint_receipt_sha256": checkpoint_receipt_hash,
            "checkpoint_failure_evidence_sha256": sha256_bytes(
                failure_stdout.encode("utf-8")
            ),
            "checkpoint_failure_target_count": sum(
                relative in failure_stdout for relative in TARGETS
            ),
            "protected_live_paths": protected_checks,
            "p6_t02_science_payload_modified": False,
            "p6_t02_reexecuted": False,
            "p6_t03_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
        },
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "p6_t03_executed": False,
        },
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }


def check_sealed_report() -> dict[str, Any]:
    errors: list[str] = []
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    if report.get("validation_status") != "PASS":
        errors.append("sealed recovery receipt is not PASS")
    if report.get("route_sha256") != ROUTE_SHA256:
        errors.append("sealed recovery receipt route hash mismatch")
    checks = report.get("checks", {})
    if checks.get("manifest_path_count") != 64:
        errors.append("sealed recovery receipt manifest count mismatch")
    if checks.get("target_path_count") != 1:
        errors.append("sealed recovery receipt target count mismatch")
    if checks.get("non_target_hash_mismatch_count") != 0:
        errors.append("sealed recovery receipt records non-target hash drift")

    live_targets = {}
    for relative in sorted(TARGETS):
        expected_after = checks.get("targets", {}).get(relative, {}).get("after_sha256")
        data = (ROOT / relative).read_bytes()
        observed = sha256_bytes(data)
        match = (
            isinstance(expected_after, str)
            and observed == expected_after
            and data.endswith(b"\n")
            and not data.endswith(b"\n\n")
        )
        live_targets[relative] = {
            "expected_after_sha256": expected_after,
            "observed_sha256": observed,
            "match": match,
        }
        if not match:
            errors.append(f"live target recovery hash mismatch: {relative}")

    live_protected = {}
    for relative, expected in PROTECTED_LIVE_PATHS.items():
        observed = sha256(ROOT / relative)
        match = observed == expected
        live_protected[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": match,
        }
        if not match:
            errors.append(f"live protected P6-T02 hash mismatch: {relative}")

    return {
        "schema_id": "p6_t02_eof_checkpoint_recovery_check_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "sealed_receipt_sha256": sha256(REPORT_PATH),
        "live_target_checks": live_targets,
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

    if args.check:
        report = check_sealed_report()
    else:
        report = build_report()
        if args.write_report:
            REPORT_PATH.write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
