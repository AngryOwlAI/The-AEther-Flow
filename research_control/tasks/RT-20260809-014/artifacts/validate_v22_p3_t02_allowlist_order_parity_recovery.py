#!/usr/bin/env python3
"""Validate the exact V22 P3-T02 post-checkpoint allowlist-order recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260809-014"
JOB_ID = "AJ-RT-20260809-014-001"
SOURCE_TASK_ID = "RT-20260809-013"
SOURCE_JOB_ID = "AJ-RT-20260809-013-001"
SOURCE_ROLE_REF = "process-integrity-auditor@0.1.0--RT-20260809-013"
SOURCE_HEAD = "92209bb3f773fa6a09554b5cde8b457d973c6d81"
SOURCE_JOB_PATH = Path(
    "research_control/tasks/RT-20260809-013/jobs/AJ-RT-20260809-013-001.yaml"
)
SOURCE_ROLE_PATH = Path(
    "research_control/tasks/RT-20260809-013/roles/"
    "process-integrity-auditor@0.1.0--RT-20260809-013.yaml"
)
AGENT_JOB_REGISTRY_PATH = Path("registries/AGENT_JOB_REGISTRY.csv")
ROLE_EXECUTION_REGISTRY_PATH = Path("registries/ROLE_EXECUTION_REGISTRY.csv")
BLOCKER_PATH = Path(
    "research_control/tasks/RT-20260809-014/artifacts/"
    "v22_p3_t02_allowlist_order_parity_blocker.yaml"
)
REPORT_PATH = Path(
    "research_control/tasks/RT-20260809-014/artifacts/"
    "v22_p3_t02_allowlist_order_parity_recovery_validation.json"
)
CHECKPOINT_RECEIPT_PATH = Path(
    ".local/validation-receipts/"
    "8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/"
    "RUN-CHECKPOINT-8dd847a94ff78979/receipt.json"
)
EXPECTED_SOURCE_JOB_SHA256 = (
    "7f74b13bf35bc2fae51474837d9f8261f3fc918c6db2465836111d29cd2f7c7d"
)
EXPECTED_SOURCE_ROLE_NON_ALLOWLIST_SHA256 = (
    "a5a3bfcbfeb6cc687de8a13dc82e193976cc0ae9d3a29f5e2505f9a6a623942f"
)
EXPECTED_SOURCE_ROLE_ROW_NON_ALLOWLIST_SHA256 = (
    "054b28a71154ad97f2009520c1642342a9c5395b32e9a04feac0ff066f83bda6"
)
EXPECTED_BLOCKER_SHA256 = (
    "6ae02c400ed7d32975223b2d6863685965f23c2eeccb02711c8fb9f67681cec1"
)
EXPECTED_CHECKPOINT_RECEIPT_SHA256 = (
    "d23e599f5110ebd8ebce44457afe008861973bb0cdd6dbf776862ff11e3e02fb"
)
EXPECTED_SOURCE_ALLOWLIST_COUNT = 17

PROTECTED_HASHES = {
    "research_control/tasks/RT-20260809-013/00_TASK.yaml":
        "842fcf16c6bc7524d754cbcb227219887a5108d59ef81a4a686723021e72901c",
    "research_control/tasks/RT-20260809-013/DDR-20260809-013.md":
        "91268a659d583ece07d8ed6e9fa6c61eb1a45061d3d9e8171bc44df77821c440",
    "research_control/tasks/RT-20260809-013/documentation_impact.yaml":
        "2047e05c95b6c10f50b50ffe6fd40b351cd94952d86d4f49391c2d6dae25b847",
    "research_control/tasks/RT-20260809-013/artifacts/"
    "inherited_dirty_manifest_v22_p3_t02_staged_acceptance.json":
        "5cecce1202562261c78477d31a4ec25c10b959ebc45c48d47c07800f8d24cc1c",
    "research_control/tasks/RT-20260809-013/artifacts/"
    "p3_t02_staged_acceptance_checkpoint_blocker.yaml":
        "f2f1536a9e8a072b79abccd1b42bece2d3dd7110eab31914954a2d2b9861fc97",
    "research_control/tasks/RT-20260809-013/artifacts/"
    "v22_p3_t02_staged_acceptance_recovery_validation.json":
        "2566b9bbca92994a2233256c2ce924739bcfa2cea4d5050b526aca4b3a127d7d",
    "research_control/tasks/RT-20260809-013/artifacts/"
    "validate_v22_p3_t02_staged_acceptance_recovery.py":
        "e3c8e2bc599d846813331d3d511535fd52e8d110ab47a67ee980c1beacefc31f",
    "research_control/tasks/RT-20260809-013/jobs/"
    "AJ-RT-20260809-013-001.yaml": EXPECTED_SOURCE_JOB_SHA256,
    "research_control/tasks/RT-20260809-013/jobs/completions/"
    "AJC-AJ-RT-20260809-013-001.yaml":
        "f25ba5f311c04a00dee341363ee9d0c5c208d0d851179c4276155666d4edbd22",
    "research_control/handoffs/handoff-0983.yaml":
        "974c3913f14c7c00ed4a3ce2dcccbe5d0a86a7e891116db41c99b290969c9055",
    "research_control/handoffs/handoff-0983.md":
        "3c038389ab18c511b3c0f2421f795a01da7a6887b178765094ddec553d624825",
    "research_control/tasks/RT-20260809-012/artifacts/"
    "v22_p3_t02_source_dynamics_without_hidden_geometry_v1.tex":
        "f26c77a175e7a5783e859eacc5de24270e1089a253e73493114a1403bbd61037",
    "research_control/tasks/RT-20260809-012/artifacts/"
    "v22_p3_t02_source_dynamics_specification_v1.yaml":
        "941e16e8a535622fcbcf6a5ac1802cd4bb86a5950af49260a22d2c69d279f46e",
    "research_control/tasks/RT-20260809-012/artifacts/"
    "v22_p3_t02_source_dynamics_validation.json":
        "651bc8f00ecc7dbf651a2b7ea4dda8d3f067d6e04e965457da99149142e16893",
    "research_control/tasks/RT-20260809-012/artifacts/"
    "v22_p3_t02_compact_receipt.json":
        "39edbdde60ac9996a888f6553648f331cd3ccfaf046833ee9661800e4f310493",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return value


def registry_row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get(key) == value]
    if len(rows) != 1:
        raise ValueError(f"{path} has {len(rows)} rows for {key}={value}")
    return rows[0]


def split_paths(value: str) -> list[str]:
    return [] if not value else value.split(";")


def validate_representation_group(
    *,
    label: str,
    job_id: str,
    role_ref: str,
    expected_count: int | None = None,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    job_row = registry_row(
        ROOT / AGENT_JOB_REGISTRY_PATH, "job_id", job_id
    )
    role_row = registry_row(
        ROOT / ROLE_EXECUTION_REGISTRY_PATH, "execution_role_ref", role_ref
    )
    job = load_yaml(ROOT / job_row["job_path"])
    role = load_yaml(ROOT / role_row["record_path"])
    representations = {
        "agent_job": job.get("allowed_write_paths"),
        "execution_role": role.get("allowed_write_paths"),
        "agent_job_registry": split_paths(job_row.get("allowed_write_paths", "")),
        "role_execution_registry": split_paths(
            role_row.get("allowed_write_paths", "")
        ),
    }
    for name, paths in list(representations.items()):
        if not isinstance(paths, list) or not all(
            isinstance(item, str) for item in paths
        ):
            errors.append(f"{label}_{name}_allowlist_invalid")
            representations[name] = []
    canonical = representations["agent_job"]
    ordered_equal = all(paths == canonical for paths in representations.values())
    if not ordered_equal:
        errors.append(f"{label}_allowlist_representations_differ")
    if len(set(canonical)) != len(canonical):
        errors.append(f"{label}_agent_job_allowlist_contains_duplicates")
    if expected_count is not None and len(canonical) != expected_count:
        errors.append(f"{label}_agent_job_allowlist_count_mismatch")
    return errors, {
        "counts": {name: len(paths) for name, paths in representations.items()},
        "ordered_equal": ordered_equal,
        "duplicate_count": len(canonical) - len(set(canonical)),
        "canonical_order": canonical,
    }


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, Any] = {}

    source_errors, source_checks = validate_representation_group(
        label="source",
        job_id=SOURCE_JOB_ID,
        role_ref=SOURCE_ROLE_REF,
        expected_count=EXPECTED_SOURCE_ALLOWLIST_COUNT,
    )
    errors.extend(source_errors)
    checks["source_allowlist_parity"] = source_checks

    new_role_ref = "process-integrity-auditor@0.1.0--RT-20260809-014"
    new_errors, new_checks = validate_representation_group(
        label="recovery", job_id=JOB_ID, role_ref=new_role_ref
    )
    errors.extend(new_errors)
    checks["recovery_allowlist_parity"] = new_checks

    observed_source_job_sha256 = sha256(ROOT / SOURCE_JOB_PATH)
    checks["source_job_sha256"] = observed_source_job_sha256
    checks["source_job_byte_preserved"] = (
        observed_source_job_sha256 == EXPECTED_SOURCE_JOB_SHA256
    )
    if not checks["source_job_byte_preserved"]:
        errors.append("source_agent_job_bytes_changed")

    source_role = load_yaml(ROOT / SOURCE_ROLE_PATH)
    source_role.pop("allowed_write_paths", None)
    observed_role_non_allowlist = canonical_json_sha256(source_role)
    checks["source_role_non_allowlist_sha256"] = observed_role_non_allowlist
    checks["source_role_only_allowlist_order_changed"] = (
        observed_role_non_allowlist
        == EXPECTED_SOURCE_ROLE_NON_ALLOWLIST_SHA256
    )
    if not checks["source_role_only_allowlist_order_changed"]:
        errors.append("source_role_non_allowlist_content_changed")

    source_role_row = registry_row(
        ROOT / ROLE_EXECUTION_REGISTRY_PATH,
        "execution_role_ref",
        SOURCE_ROLE_REF,
    )
    source_role_row.pop("allowed_write_paths", None)
    observed_row_non_allowlist = canonical_json_sha256(source_role_row)
    checks["source_role_row_non_allowlist_sha256"] = observed_row_non_allowlist
    checks["source_role_row_only_allowlist_order_changed"] = (
        observed_row_non_allowlist
        == EXPECTED_SOURCE_ROLE_ROW_NON_ALLOWLIST_SHA256
    )
    if not checks["source_role_row_only_allowlist_order_changed"]:
        errors.append("source_role_registry_non_allowlist_content_changed")

    protected_results: dict[str, dict[str, Any]] = {}
    for relative, expected in PROTECTED_HASHES.items():
        path = ROOT / relative
        observed = sha256(path) if path.is_file() else None
        protected_results[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": observed == expected,
        }
        if observed != expected:
            errors.append(f"protected_hash_mismatch:{relative}")
    checks["protected_hashes"] = protected_results

    blocker_hash = sha256(ROOT / BLOCKER_PATH)
    checkpoint_hash = sha256(ROOT / CHECKPOINT_RECEIPT_PATH)
    checks["blocker_sha256"] = blocker_hash
    checks["checkpoint_receipt_sha256"] = checkpoint_hash
    if blocker_hash != EXPECTED_BLOCKER_SHA256:
        errors.append("blocker_hash_mismatch")
    if checkpoint_hash != EXPECTED_CHECKPOINT_RECEIPT_SHA256:
        errors.append("source_checkpoint_receipt_hash_mismatch")

    blocker = load_yaml(ROOT / BLOCKER_PATH)
    mismatch = blocker.get("mismatch", {})
    if (
        mismatch.get("same_set") is not True
        or mismatch.get("same_order") is not False
        or mismatch.get("first_mismatch_index") != 7
        or mismatch.get("second_mismatch_index") != 8
    ):
        errors.append("blocker_does_not_bind_exact_order_only_mismatch")

    state = load_yaml(ROOT / "research_control/program_state.yaml")
    handoff = load_yaml(ROOT / "research_control/handoffs/handoff-0984.yaml")
    checks["active_task_id"] = state.get("active_task_id")
    checks["active_agent_job_id"] = state.get("active_agent_job_id")
    checks["latest_handoff_id"] = state.get("latest_handoff_id")
    checks["next_plan_task_id"] = state.get("next_plan_task_id")
    if state.get("active_task_id") != TASK_ID:
        errors.append("active_task_id_mismatch")
    if state.get("active_agent_job_id") != JOB_ID:
        errors.append("active_agent_job_id_mismatch")
    if state.get("latest_handoff_id") != "handoff-0984":
        errors.append("latest_handoff_id_mismatch")
    if state.get("next_plan_task_id") != "P3-T03":
        errors.append("next_plan_task_id_mismatch")
    recovery = state.get("v22_p3_t02_allowlist_order_parity_recovery", {})
    for key, expected in {
        "p3_t02_reexecuted": False,
        "p3_t03_executed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "validator_semantics_changed": False,
    }.items():
        if recovery.get(key) is not expected:
            errors.append(f"program_state_boundary_mismatch:{key}")
    if handoff.get("plan_task_id") != "P3-T03":
        errors.append("handoff_plan_task_id_mismatch")
    if handoff.get("ordinary_route_guard", {}).get("outcome") != "below_threshold":
        errors.append("handoff_ordinary_route_guard_outcome_mismatch")
    if handoff.get("claim_boundary", {}).get("p3_t03_executed") is not False:
        errors.append("handoff_p3_t03_execution_boundary_changed")

    return {
        "schema_id": "v22_p3_t02_allowlist_order_parity_recovery_validation_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_job_id": SOURCE_JOB_ID,
        "source_head": SOURCE_HEAD,
        "strategy_id": "repair_v22_p3_t02_allowlist_order_parity_after_checkpoint_v1",
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "validation_status": "PASS" if not errors else "FAIL",
        "authority_limits": {
            "validator_semantics_changed": False,
            "p3_t02_reexecuted": False,
            "p3_t03_executed": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    destination = ROOT / REPORT_PATH
    if args.write_report:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        if not destination.is_file():
            report["errors"].append("stored_report_missing")
        else:
            stored = json.loads(destination.read_text(encoding="utf-8"))
            if stored != report:
                report["errors"].append("stored_report_drift")
        report["error_count"] = len(report["errors"])
        report["validation_status"] = (
            "PASS" if not report["errors"] else "FAIL"
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
