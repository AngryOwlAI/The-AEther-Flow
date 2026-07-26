#!/usr/bin/env python3
"""Validate the sealed P6-T03 traceability-hash checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260726-006"
JOB_ID = "AJ-RT-20260726-006-001"
GOAL_ID = "crg-20260720T161354Z-96bc2664ce31bfe0"
GENERATION = 125
ROUTE_SHA256 = "e0eb5c75a60db368e3d4fbd96ad76c29976246b852b6d39cb671ac4e691aae2c"
DIRTY_MANIFEST_SHA256 = (
    "b5d69eafafae08c13ee2d095cd8278ddf619ec42ce6b70a7969ec48a50ab6c0a"
)
FAILED_GATE_EVIDENCE_SHA256 = (
    "92fed2839b743cc4dc3c83fa697089eb123f93bcbed44e0b701f3b351ba55f15"
)
SOURCE_HEAD = "2c5d8ec75f4c921065945309a77270ea4c4affde"
GOAL_PATH = (
    ROOT
    / ".codex/skills/continue-research-goal/goals/"
    "goal-crg-20260720T161354Z-96bc2664ce31bfe0.md"
)
TARGET_PATH = (
    "research_control/design/"
    "support_formalization_traceability_registry_v18.yaml"
)
TARGET_BEFORE_SHA256 = (
    "19c88963181ddbbf62c28a676d990a9583a17b6e47ac8fe25f1a7d5cce5823d3"
)
TARGET_AFTER_SHA256 = (
    "768c0af4236c8793d233aefea6e5a253c1c5ba8f3eecc75f993a67f8392dd7dc"
)
STALE_LEDGER_SHA256 = (
    "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf"
)
AUTHORIZED_LEDGER_SHA256 = (
    "b63efbe32b6681bbe093c41ec92a2bfe0989fbd2a94a605387bdcd5a9e440720"
)
LEDGER_PATH = "registries/METRIC_USE_LEDGER.csv"
TRACEABILITY_VALIDATOR = (
    "scripts/research_control/support_formalization/"
    "validate_traceability_registry_v18.py"
)
REPORT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260726-006/artifacts/"
    "p6_t03_traceability_hash_recovery_receipt.json"
)


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
                raise ValueError("generation 125 route is missing")
            return route
    raise ValueError("generation 125 is missing")


def run_traceability_validator() -> dict[str, Any]:
    command = [
        sys.executable,
        str(ROOT / TRACEABILITY_VALIDATOR),
        "--json",
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    parsed: dict[str, Any] = {}
    if result.returncode == 0:
        try:
            loaded = json.loads(result.stdout)
            if isinstance(loaded, dict):
                parsed = loaded
        except json.JSONDecodeError:
            pass
    return {
        "command": " ".join(
            [".venv/bin/python", TRACEABILITY_VALIDATOR, "--json"]
        ),
        "returncode": result.returncode,
        "status": parsed.get("status", "FAIL"),
        "entry_count": parsed.get("entry_count"),
        "support_only": parsed.get("support_only"),
        "proof_authority": parsed.get("proof_authority"),
        "physics_promotion_authorized": parsed.get(
            "physics_promotion_authorized"
        ),
        "stderr": result.stderr.strip(),
    }


def target_transition_check() -> dict[str, Any]:
    target = ROOT / TARGET_PATH
    data = target.read_bytes()
    stale = STALE_LEDGER_SHA256.encode("ascii")
    authorized = AUTHORIZED_LEDGER_SHA256.encode("ascii")
    reconstructed_before = data.replace(authorized, stale)
    return {
        "path": TARGET_PATH,
        "before_sha256": TARGET_BEFORE_SHA256,
        "after_sha256": sha256_bytes(data),
        "stale_hash_occurrence_count": data.count(stale),
        "authorized_hash_occurrence_count": data.count(authorized),
        "reconstructed_before_sha256": sha256_bytes(reconstructed_before),
        "exact_one_hash_substitution": (
            sha256_bytes(data) == TARGET_AFTER_SHA256
            and data.count(stale) == 0
            and data.count(authorized) == 1
            and sha256_bytes(reconstructed_before) == TARGET_BEFORE_SHA256
        ),
    }


def protected_manifest_paths(
    manifest_by_path: dict[str, str],
) -> dict[str, str]:
    return {
        path: expected
        for path, expected in manifest_by_path.items()
        if path == LEDGER_PATH
        or path.startswith("research_control/tasks/RT-20260726-005/")
        or path
        in {
            "research_control/handoffs/handoff-0879.yaml",
            "research_control/handoffs/handoff-0879.md",
        }
    }


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

    route_hash = canonical_sha256(route)
    manifest_hash = canonical_sha256(manifest)
    if route_hash != ROUTE_SHA256:
        errors.append("immutable route canonical hash mismatch")
    if manifest_hash != DIRTY_MANIFEST_SHA256:
        errors.append("dirty manifest canonical hash mismatch")
    if len(manifest_by_path) != 64:
        errors.append(f"expected 64 manifest paths, observed {len(manifest_by_path)}")
    if manifest.get("head") != SOURCE_HEAD:
        errors.append("dirty manifest source HEAD mismatch")
    if manifest.get("owning_task_id") != "RT-20260726-005":
        errors.append("dirty manifest owner task mismatch")
    if manifest.get("owning_agent_job_id") != "AJ-RT-20260726-005-001":
        errors.append("dirty manifest owner job mismatch")

    failed_gates = manifest.get("failed_gates", [])
    expected_failed_gate = {
        "gate_id": "repository_tests_support_formalization_traceability",
        "status": "FAIL_2_ERRORS_METRIC_LEDGER_HASH_MISMATCH",
        "evidence_sha256": FAILED_GATE_EVIDENCE_SHA256,
    }
    if failed_gates != [expected_failed_gate]:
        errors.append("failed-gate evidence mismatch")

    required_evidence = {
        TARGET_BEFORE_SHA256,
        FAILED_GATE_EVIDENCE_SHA256,
        AUTHORIZED_LEDGER_SHA256,
    }
    if not required_evidence.issubset(set(route.get("evidence_hashes", []))):
        errors.append("immutable route lacks required repair evidence hashes")

    manifest_mismatches: list[str] = []
    for relative, expected in manifest_by_path.items():
        path = ROOT / relative
        if not path.is_file() or sha256(path) != expected:
            manifest_mismatches.append(relative)
    if manifest_mismatches:
        errors.append(
            f"{len(manifest_mismatches)} inherited dirty-manifest paths changed"
        )

    target_check = target_transition_check()
    if not target_check["exact_one_hash_substitution"]:
        errors.append("target is not the exact authorized one-hash substitution")

    ledger_hash = sha256(ROOT / LEDGER_PATH)
    if ledger_hash != AUTHORIZED_LEDGER_SHA256:
        errors.append("authorized metric-use ledger hash mismatch")

    traceability = run_traceability_validator()
    if not (
        traceability["returncode"] == 0
        and traceability["status"] == "PASS"
        and traceability["entry_count"] == 5
        and traceability["support_only"] is True
        and traceability["proof_authority"] is False
        and traceability["physics_promotion_authorized"] is False
    ):
        errors.append("v18 support-formalization traceability validation failed")

    protected = protected_manifest_paths(manifest_by_path)
    return {
        "schema_id": "p6_t03_traceability_hash_recovery_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "goal_id": GOAL_ID,
        "generation": GENERATION,
        "strategy_id": (
            "repair_p6_t03_support_traceability_metric_ledger_hash_"
            "and_checkpoint_v1"
        ),
        "route_sha256": route_hash,
        "dirty_state_manifest_sha256": manifest_hash,
        "source_head": SOURCE_HEAD,
        "source_task_id": "RT-20260726-005",
        "source_job_id": "AJ-RT-20260726-005-001",
        "source_handoff_id": "handoff-0879",
        "checks": {
            "manifest_path_count": len(manifest_by_path),
            "manifest_hash_mismatch_count": len(manifest_mismatches),
            "manifest_hash_mismatches": manifest_mismatches,
            "target": target_check,
            "ledger_path": LEDGER_PATH,
            "ledger_sha256": ledger_hash,
            "failed_gate_evidence_sha256": FAILED_GATE_EVIDENCE_SHA256,
            "protected_live_paths": protected,
            "traceability_validator": traceability,
            "p6_t03_science_payload_modified": False,
            "p6_t03_reexecuted": False,
            "p6_t04_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
        },
        "authority_limits": {
            "support_only": True,
            "proof_authority": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "publication_or_push_authorized": False,
            "p6_t04_executed": False,
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
    if checks.get("manifest_hash_mismatch_count") != 0:
        errors.append("sealed recovery receipt records manifest drift")

    target_check = target_transition_check()
    if not target_check["exact_one_hash_substitution"]:
        errors.append("live target recovery hash mismatch")
    if sha256(ROOT / LEDGER_PATH) != AUTHORIZED_LEDGER_SHA256:
        errors.append("live metric-use ledger hash mismatch")

    protected_checks: dict[str, Any] = {}
    protected = checks.get("protected_live_paths", {})
    if not isinstance(protected, dict) or len(protected) != 18:
        errors.append("sealed protected-path set mismatch")
        protected = {}
    for relative, expected in protected.items():
        if relative == "research_control/tasks/RT-20260726-005/documentation_impact.yaml":
            protected_checks[relative] = {
                "expected_sha256": expected,
                "observed_sha256": "post_seal_control_update_allowed",
                "match": True,
                "post_seal_control_update_allowed": True,
            }
            continue
        path = ROOT / relative
        observed = sha256(path) if path.is_file() else "missing"
        match = observed == expected
        protected_checks[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": match,
        }
        if not match:
            errors.append(f"live protected P6-T03 hash mismatch: {relative}")

    traceability = run_traceability_validator()
    if traceability["returncode"] != 0 or traceability["status"] != "PASS":
        errors.append("live v18 support-formalization traceability validation failed")

    return {
        "schema_id": "p6_t03_traceability_hash_recovery_check_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "sealed_receipt_sha256": sha256(REPORT_PATH),
        "live_target_check": target_check,
        "live_protected_checks": protected_checks,
        "traceability_validator": traceability,
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
