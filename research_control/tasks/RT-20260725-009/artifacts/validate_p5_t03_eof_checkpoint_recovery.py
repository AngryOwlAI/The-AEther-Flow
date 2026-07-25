#!/usr/bin/env python3
"""Validate the sealed four-file P5-T03 EOF-only checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260725-009"
JOB_ID = "AJ-RT-20260725-009-001"
GOAL_ID = "crg-20260720T161354Z-96bc2664ce31bfe0"
GENERATION = 114
ROUTE_SHA256 = "7d890c50eabed262d8891ca971ae8af771bc9758b51788163e4f3207c6ee0782"
DIRTY_MANIFEST_SHA256 = "12623c97f8e7a24cd5ff2b3f2320a74f890abc5f5dae2b7db2e9e04023db5517"
FAILED_GATE_EVIDENCE_SHA256 = (
    "e7b1fa1516c822f090cddf435be01e1e6ab23d605fe7fdbd45cc8eb000111a11"
)
CHECKPOINT_RECEIPT_SHA256 = (
    "39b13b993728ae16dd298e34f8c85abbff60591cef01749d38eef0adc338ba4c"
)
SOURCE_HEAD = "48799f729758a06efd31c234c1724f590516ebcd"
GOAL_PATH = (
    ROOT
    / ".codex/skills/continue-research-goal/goals/"
    "goal-crg-20260720T161354Z-96bc2664ce31bfe0.md"
)
CHECKPOINT_RECEIPT_PATH = (
    ROOT
    / ".local/validation-receipts/"
    "5fdb4a94a5136a980b14c90b290edc80d5bffc547f521ef9a53db6c9866d794a/"
    "RUN-CHECKPOINT-6da96bdf9481f46e/receipt.json"
)
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260725-009/artifacts/"
    "p5_t03_eof_checkpoint_recovery_receipt.json"
)

TARGETS = {
    "research_control/tasks/RT-20260725-008/00_TASK.yaml",
    (
        "research_control/tasks/RT-20260725-008/artifacts/"
        "child_phys_math_cubic_amplitude_dynamics.yaml"
    ),
    (
        "research_control/tasks/RT-20260725-008/artifacts/"
        "child_phys_phil_cubic_amplitude_dynamics.yaml"
    ),
    (
        "research_control/tasks/RT-20260725-008/artifacts/"
        "parent_conflict_review_cubic_amplitude_dynamics.yaml"
    ),
}

PROTECTED_LIVE_PATHS = {
    "research_control/handoffs/handoff-0868.yaml": (
        "51fd10d660bb680f66a19f5e442b608bc72598486e453c5aff5ac75fda794d76"
    ),
    "research_control/handoffs/handoff-0868.md": (
        "701942a5895aff28ca7362c156ea0ec7f7dba74aec3095c64071ef32e997128d"
    ),
    (
        "research_control/tasks/RT-20260725-008/artifacts/"
        "cubic_amplitude_source_dynamics_v1.tex"
    ): "98ce6833f6e4d8be22837d25845d7fa62d6886049e168d121de5de0093703f6a",
    (
        "research_control/tasks/RT-20260725-008/artifacts/"
        "cubic_amplitude_source_dynamics_spec_v1.yaml"
    ): "2007c7a5b9f3ffa5cc43d8a82f8de685428b75075195ee1ca16e7fa4889c64f9",
    (
        "research_control/tasks/RT-20260725-008/artifacts/"
        "cubic_amplitude_source_dynamics_validation_receipt_v1.json"
    ): "22f2eff6b0fe2c9898511c43b7626ccdd5c91323f19e220ae5d081d3fd9dd0f5",
    (
        "research_control/tasks/RT-20260725-008/artifacts/"
        "parent_fusion_notes_cubic_amplitude_dynamics.md"
    ): "9253ea792f3dde14612223654da10bce974a70193febae4feb3fd250588ada36",
    (
        "research_control/tasks/RT-20260725-008/artifacts/"
        "validate_cubic_amplitude_source_dynamics.py"
    ): "76ae106db3ec30822be5b0b1e63b63d33158a4d5065d94a7da68a7def8c79f03",
    (
        "research_control/tasks/RT-20260725-008/jobs/"
        "AJ-RT-20260725-008-001.yaml"
    ): "cbf7c879d17e3aca0346e1610286809aabd8c068e0b2bc2e37749193875b2890",
    (
        "research_control/tasks/RT-20260725-008/jobs/completions/"
        "AJC-AJ-RT-20260725-008-001.yaml"
    ): "6fd8e2360cc543505c3cb85fcab5f9e7e1f050a3bcc6d9d838ad53bcbbe91ec6",
    (
        "research_control/tasks/RT-20260725-008/roles/"
        "candidate-constructor@0.2.0--RT-20260725-008.yaml"
    ): "75c5c72334700098946d1c704ab0a623c4bb75e13bdc29ffafc9690247bffa44",
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
                raise ValueError("generation 114 route is missing")
            return route
    raise ValueError("generation 114 is missing")


def checkpoint_failure_stdout(receipt: dict[str, Any]) -> str:
    results = receipt.get("gate_results", [])
    if isinstance(results, list):
        for gate in results:
            if not isinstance(gate, dict) or gate.get("gate_id") != "git_diff_check":
                continue
            stdout_path = gate.get("stdout_path")
            if isinstance(stdout_path, str) and Path(stdout_path).is_file():
                return Path(stdout_path).read_text(encoding="utf-8")
    gates = receipt.get("gates", {})
    if isinstance(gates, dict):
        gate = gates.get("git_diff_check", {})
        if isinstance(gate, dict):
            for key in ("stdout", "output", "details"):
                value = gate.get(key)
                if isinstance(value, str):
                    return value
    for value in receipt.values():
        if isinstance(value, dict):
            found = checkpoint_failure_stdout(value)
            if found:
                return found
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
        errors.append("one or more repair targets are absent from the dirty manifest")
    if len(manifest_by_path) != 55:
        errors.append(f"expected 55 manifest paths, observed {len(manifest_by_path)}")

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
            errors.append(f"protected P5-T03 hash mismatch: {relative}")

    return {
        "schema_id": "p5_t03_eof_checkpoint_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "goal_id": GOAL_ID,
        "generation": GENERATION,
        "strategy_id": "repair_p5_t03_four_eof_blank_lines_and_checkpoint_v1",
        "route_sha256": ROUTE_SHA256,
        "dirty_state_manifest_sha256": DIRTY_MANIFEST_SHA256,
        "source_head": SOURCE_HEAD,
        "source_task_id": "RT-20260725-008",
        "source_job_id": "AJ-RT-20260725-008-001",
        "source_handoff_id": "handoff-0868",
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
            "p5_t03_science_payload_modified": False,
            "p5_t03_reexecuted": False,
            "p5_t04_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
        },
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "p5_t04_executed": False,
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
    if checks.get("manifest_path_count") != 55:
        errors.append("sealed recovery receipt manifest count mismatch")
    if checks.get("target_path_count") != 4:
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
            errors.append(f"live protected P5-T03 hash mismatch: {relative}")

    return {
        "schema_id": "p5_t03_eof_checkpoint_recovery_check_v1",
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
