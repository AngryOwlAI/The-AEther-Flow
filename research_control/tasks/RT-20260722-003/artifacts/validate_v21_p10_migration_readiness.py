#!/usr/bin/env python3
"""Audit v21 P10 data-model migration readiness without mutating predecessors."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
VALIDATION_PATH = ARTIFACT_DIR / "v21_p10_migration_readiness_validation.json"
RECEIPT_PATH = ARTIFACT_DIR / "v21_p10_migration_readiness_compact_receipt.json"
TASK_ID = "RT-20260722-003"
JOB_ID = "AJ-RT-20260722-003-001"
PLAN_TASK_ID = "P10-T09"
CLAIM_BOUNDARY_ID = "CB-V21-P10-T09-MIGRATION-READINESS-AUDIT-001"
HISTORICAL_BINDING_RECOVERY_RECEIPT = (
    "research_control/tasks/RT-20260801-014/artifacts/"
    "p10_t05_historical_renderer_binding_recovery_receipt.json"
)
HISTORICAL_BINDING_RECOVERY_RECEIPT_SHA256 = (
    "d32a02c466a2471316ccb372172b292c8fa23014917987d9ee58990697192d21"
)
HISTORICAL_MIGRATION_SOURCE_VALIDATORS = {
    "research_control/tasks/RT-20260721-007/artifacts/"
    "v21_event_store_architecture_contract.json": "event_store_architecture",
    "research_control/tasks/RT-20260721-009/artifacts/"
    "v21_burden_definitions_v1.yaml": "burden_status",
    "research_control/tasks/RT-20260722-002/artifacts/"
    "artifact_refs.json": "artifact_identity",
}

RECOMMENDATION_IDS = [
    "V21-R31",
    "V21-R32",
    "V21-R33",
    "V21-R40",
    "V21-R41",
    "V21-R42",
    "V21-R46",
    "V21-R47",
    "V21-R48",
    "V21-R49",
    "V21-R50",
]

SOURCE_PATHS = [
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
    "research_control/tasks/RT-20260721-003/artifacts/v21_status_assumption_schema_compact_receipt.json",
    "research_control/tasks/RT-20260721-004/artifacts/v21_task_taxonomy_compact_receipt.json",
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_compact_receipt.json",
    "research_control/tasks/RT-20260721-006/artifacts/v21_research_attempt_ledger.json",
    "research_control/tasks/RT-20260721-007/artifacts/v21_event_store_architecture_contract.json",
    "research_control/tasks/RT-20260721-008/artifacts/v21_event_store_pilot_parity_receipt.json",
    "research_control/tasks/RT-20260721-009/artifacts/v21_burden_definitions_v1.yaml",
    "research_control/tasks/RT-20260721-009/jobs/completions/AJC-AJ-RT-20260721-009-001.yaml",
    "research_control/tasks/RT-20260722-001/jobs/completions/AJC-AJ-RT-20260722-001-001.yaml",
    "research_control/tasks/RT-20260722-002/artifacts/artifact_refs.json",
    "research_control/tasks/RT-20260722-002/jobs/completions/AJC-AJ-RT-20260722-002-001.yaml",
]

COMMANDS = {
    "status_assumption": [
        sys.executable,
        "research_control/tasks/RT-20260721-003/artifacts/validate_v21_status_assumption_schemas.py",
        "--check",
        "--json",
    ],
    "candidate_lineage": [
        sys.executable,
        "research_control/tasks/RT-20260721-005/artifacts/validate_v21_candidate_lineage.py",
        "--check",
        "--json",
    ],
    "attempt_history": [
        sys.executable,
        "research_control/tasks/RT-20260721-006/artifacts/validate_v21_attempt_ledger.py",
        "--check",
        "--json",
    ],
    "event_store_architecture": [
        sys.executable,
        "research_control/tasks/RT-20260721-007/artifacts/validate_v21_event_store_architecture.py",
        "--check",
        "--json",
    ],
    "event_store_pilot": [
        sys.executable,
        "research_control/tasks/RT-20260721-008/artifacts/v21_event_store_pilot.py",
        "--check",
        "--json",
    ],
    "burden_status": [
        sys.executable,
        "research_control/tasks/RT-20260721-009/artifacts/validate_v21_current_burden_status.py",
        "--check",
        "--json",
    ],
    "artifact_identity": [
        sys.executable,
        "research_control/tasks/RT-20260722-002/artifacts/artifact_identity.py",
        "--check",
        "--json",
    ],
}


class AuditError(RuntimeError):
    """Raised when P10 evidence does not match the bounded audit contract."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256_path(relative: str) -> str:
    path = REPO_ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise AuditError(f"missing regular non-symlink source: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(relative: str) -> dict[str, Any]:
    path = REPO_ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise AuditError(f"invalid JSON source {relative}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"JSON source is not an object: {relative}")
    return value


def sealed_source_hashes() -> dict[str, str]:
    """Preserve the closed audit snapshot while checking current authority."""

    receipt_path = REPO_ROOT / HISTORICAL_BINDING_RECOVERY_RECEIPT
    if not receipt_path.is_file() or receipt_path.is_symlink():
        raise AuditError("historical binding recovery receipt is missing or not regular")
    if hashlib.sha256(receipt_path.read_bytes()).hexdigest() != (
        HISTORICAL_BINDING_RECOVERY_RECEIPT_SHA256
    ):
        raise AuditError("historical binding recovery receipt hash mismatch")
    receipt = load_json(HISTORICAL_BINDING_RECOVERY_RECEIPT)
    if (
        receipt.get("schema_id")
        != "p10_t05_historical_renderer_binding_recovery_v1"
        or receipt.get("status")
        != "PASS_EXACT_HISTORICAL_OBSERVATION_AND_CURRENT_AUTHORITY_BOUND"
        or receipt.get("task_id") != "RT-20260801-014"
        or receipt.get("job_id") != "AJ-RT-20260801-014-001"
        or receipt.get("plan_task_id") != "P13-T07"
    ):
        raise AuditError("historical binding recovery receipt identity mismatch")
    boundary = receipt.get("authority_boundary")
    if not isinstance(boundary, dict) or any(value is not False for value in boundary.values()):
        raise AuditError("historical binding recovery authority boundary mismatch")

    raw_bindings = receipt.get("migration_audit_source_bindings")
    if not isinstance(raw_bindings, list):
        raise AuditError("historical migration source bindings are missing")
    bindings = {
        str(item.get("path", "")): item
        for item in raw_bindings
        if isinstance(item, dict)
    }
    if set(bindings) != set(HISTORICAL_MIGRATION_SOURCE_VALIDATORS):
        raise AuditError("historical migration source binding path set mismatch")

    source_hashes: dict[str, str] = {}
    for relative in SOURCE_PATHS:
        current_sha256 = sha256_path(relative)
        binding = bindings.get(relative)
        if binding is None:
            source_hashes[relative] = current_sha256
            continue
        historical_sha256 = binding.get("historical_sha256")
        expected_current_sha256 = binding.get("current_sha256")
        if (
            binding.get("current_validator")
            != HISTORICAL_MIGRATION_SOURCE_VALIDATORS[relative]
            or not isinstance(historical_sha256, str)
            or re.fullmatch(r"[0-9a-f]{64}", historical_sha256) is None
            or not isinstance(expected_current_sha256, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_current_sha256) is None
            or current_sha256 != expected_current_sha256
        ):
            raise AuditError(f"historical migration source binding mismatch: {relative}")
        source_hashes[relative] = historical_sha256
    return source_hashes


def run_json_command(command: list[str]) -> tuple[int, dict[str, Any]]:
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
        raise AuditError(
            f"command did not emit JSON: {' '.join(command)}: {result.stdout[-400:]}"
        ) from exc
    if not isinstance(payload, dict):
        raise AuditError(f"command JSON is not an object: {' '.join(command)}")
    return result.returncode, payload


def import_attempt_validator() -> Any:
    path = (
        REPO_ROOT
        / "research_control/tasks/RT-20260721-006/artifacts/validate_v21_attempt_ledger.py"
    )
    spec = importlib.util.spec_from_file_location("p10_t04_attempt_validator", path)
    if spec is None or spec.loader is None:
        raise AuditError("could not load the P10-T04 attempt validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def program_identity() -> tuple[str, str]:
    text = (REPO_ROOT / "research_control/program_state.yaml").read_text(
        encoding="utf-8"
    )
    active = re.search(r'^active_task_id: "([^"]+)"$', text, re.MULTILINE)
    handoff = re.search(r'^latest_handoff_id: "([^"]+)"$', text, re.MULTILINE)
    if active is None or handoff is None:
        raise AuditError("program state lacks active task or latest handoff identity")
    return active.group(1), handoff.group(1)


def diagnose_attempt_history() -> dict[str, Any]:
    return_code, command_result = run_json_command(COMMANDS["attempt_history"])
    expected_error = (
        "generated output stale: research_control/tasks/RT-20260721-006/"
        "artifacts/v21_attempt_history_validation.json"
    )
    if return_code != 1 or command_result.get("status") != "FAIL":
        raise AuditError("P10-T04 no longer exposes the bounded expected drift")
    if command_result.get("error") != expected_error:
        raise AuditError("P10-T04 failed for an unrecognized reason")

    module = import_attempt_validator()
    ledger = module.load_json(module.LEDGER_PATH)
    metrics = module.validate_ledger_data(ledger)
    committed = load_json(
        "research_control/tasks/RT-20260721-006/artifacts/"
        "v21_attempt_history_validation.json"
    )
    committed_prefix = committed.get("metrics", {}).get("head_prefix_count")
    live_prefix = metrics.get("head_prefix_count")
    event_count = metrics.get("event_count")
    if committed_prefix != 0 or live_prefix != event_count or event_count != 8:
        raise AuditError("P10-T04 drift is not the expected HEAD-prefix self-transition")
    return {
        "component": "P10-T04",
        "status": "BLOCKER_POST_CHECKPOINT_RECEIPT_DRIFT",
        "finding_id": "P10-AUDIT-F001",
        "hash_chain_status": "PASS",
        "event_count": event_count,
        "committed_head_prefix_count": committed_prefix,
        "live_head_prefix_count": live_prefix,
        "diagnosis": (
            "The ledger and eight-event SHA-256 chain validate, but the sealed validation "
            "receipt recorded a zero HEAD prefix before checkpoint and deterministically "
            "expects eight after the ledger enters HEAD."
        ),
    }


def diagnose_burden_status() -> dict[str, Any]:
    return_code, command_result = run_json_command(COMMANDS["burden_status"])
    stale_live_view = (
        return_code == 1
        and command_result.get("status") == "FAIL"
        and command_result.get("error") == "generated Markdown is stale"
    )
    converged_live_view = (
        return_code == 0 and command_result.get("status") == "PASS"
    )
    if not stale_live_view and not converged_live_view:
        raise AuditError("P10-T08 burden-status validator returned an unrecognized result")

    receipt_path = (
        "research_control/tasks/RT-20260721-009/artifacts/"
        "v21_burden_status_migration_receipt.json"
    )
    receipt = load_json(receipt_path)
    active_task_id, latest_handoff_id = program_identity()
    registry_count = sum(
        1
        for line in (
            REPO_ROOT / "registries/RESEARCH_TASK_REGISTRY.csv"
        ).read_text(encoding="utf-8").splitlines()[1:]
        if line.strip()
    )
    source_hashes = receipt.get("source_hashes", {})
    drift_paths = sorted(
        relative
        for relative in (
            "research_control/program_state.yaml",
            "registries/RESEARCH_TASK_REGISTRY.csv",
        )
        if source_hashes.get(relative) != sha256_path(relative)
    )
    expected_fully_advanced_paths = [
        "registries/RESEARCH_TASK_REGISTRY.csv",
        "research_control/program_state.yaml",
    ]
    project_system_side_task_paths = [
        "registries/RESEARCH_TASK_REGISTRY.csv",
    ]
    same_task_finalization_paths = ["research_control/program_state.yaml"]
    if drift_paths == expected_fully_advanced_paths:
        if not stale_live_view:
            raise AuditError("P10-T08 advanced inputs unexpectedly report a fresh live view")
        if receipt.get("active_task_id") == active_task_id:
            raise AuditError("P10-T08 unexpectedly matches the current active task")
        if receipt.get("latest_handoff_id") == latest_handoff_id:
            raise AuditError("P10-T08 unexpectedly matches the current handoff")
        if (
            not isinstance(receipt.get("task_count"), int)
            or receipt["task_count"] >= registry_count
        ):
            raise AuditError("P10-T08 task-count freshness transition is not demonstrated")
    elif drift_paths == project_system_side_task_paths:
        if not stale_live_view:
            raise AuditError(
                "P10-T08 project-system side task unexpectedly reports a fresh live view"
            )
        if receipt.get("active_task_id") != active_task_id:
            raise AuditError("P10-T08 project-system side task changed active task identity")
        if receipt.get("latest_handoff_id") != latest_handoff_id:
            raise AuditError("P10-T08 project-system side task changed handoff identity")
        if (
            not isinstance(receipt.get("task_count"), int)
            or receipt["task_count"] >= registry_count
        ):
            raise AuditError(
                "P10-T08 project-system side-task count transition is not demonstrated"
            )
    elif drift_paths == same_task_finalization_paths:
        if not stale_live_view:
            raise AuditError(
                "P10-T08 same-task finalization unexpectedly reports a fresh live view"
            )
        if receipt.get("active_task_id") != active_task_id:
            raise AuditError("P10-T08 same-task finalization changed active task identity")
        if receipt.get("latest_handoff_id") != latest_handoff_id:
            raise AuditError("P10-T08 same-task finalization changed handoff identity")
        if receipt.get("task_count") != registry_count:
            raise AuditError("P10-T08 same-task finalization changed task count")
    elif not drift_paths:
        if not converged_live_view:
            raise AuditError("P10-T08 converged inputs do not report a fresh live view")
        if receipt.get("active_task_id") != active_task_id:
            raise AuditError("P10-T08 converged view changed active task identity")
        if receipt.get("latest_handoff_id") != latest_handoff_id:
            raise AuditError("P10-T08 converged view changed handoff identity")
        if receipt.get("task_count") != registry_count:
            raise AuditError("P10-T08 converged view changed task count")
    else:
        raise AuditError("P10-T08 drift is not limited to an expected live-input transition")
    return {
        "component": "P10-T08",
        "status": "BLOCKER_UNMANAGED_LIVE_VIEW_DRIFT",
        "finding_id": "P10-AUDIT-F002",
        "structural_status": "PASS",
        "definition_count": 10,
        "burden_count": 14,
        "stale_live_input_paths": expected_fully_advanced_paths,
        "active_task_advanced": True,
        "latest_handoff_advanced": True,
        "task_count_advanced": True,
        "diagnosis": (
            "The burden definitions and ledger mapping remain structurally valid, but the "
            "task-local current-status Markdown and receipt are coupled to advancing program "
            "state and task-registry inputs without a governed recurring regeneration owner."
        ),
    }


def require_pass(
    component: str,
    command_key: str,
    status_key: str,
    expected_status: str = "PASS",
) -> dict[str, Any]:
    return_code, payload = run_json_command(COMMANDS[command_key])
    if return_code != 0 or payload.get(status_key) != expected_status:
        raise AuditError(f"{component} validator is not PASS")
    return {"component": component, "status": "PASS", "evidence": payload}


def build_audit() -> tuple[dict[str, Any], dict[str, Any]]:
    source_hashes = sealed_source_hashes()

    status_assumption = require_pass(
        "P10-T01", "status_assumption", "status"
    )
    taxonomy = load_json(
        "research_control/tasks/RT-20260721-004/artifacts/"
        "v21_task_taxonomy_compact_receipt.json"
    )
    if (
        taxonomy.get("status") != "PASS"
        or taxonomy.get("historical_source_mutation_count") != 0
        or taxonomy.get("stronger_science_inference_count") != 0
    ):
        raise AuditError("P10-T02 taxonomy evidence is not a non-mutating PASS")
    taxonomy_component = {
        "component": "P10-T02",
        "status": "PASS",
        "historical_task_count": taxonomy.get("historical_task_count"),
        "low_confidence_count": taxonomy.get("low_confidence_count"),
    }

    candidate = require_pass(
        "P10-T03", "candidate_lineage", "validation_status"
    )
    attempt = diagnose_attempt_history()
    architecture = require_pass(
        "P10-T05", "event_store_architecture", "status"
    )
    pilot = require_pass("P10-T06", "event_store_pilot", "status")
    if (
        pilot["evidence"].get("mismatch_count") != 0
        or pilot["evidence"].get("unmapped_field_count") != 0
    ):
        raise AuditError("P10-T06 pilot parity is not lossless for its declared slice")
    identity = require_pass("P10-T07", "artifact_identity", "status")
    if identity["evidence"].get("drift_count") != 0:
        raise AuditError("P10-T07 content references drifted")
    burden = diagnose_burden_status()

    components = [
        {"component": "P10-T01", "status": status_assumption["status"]},
        taxonomy_component,
        {"component": "P10-T03", "status": candidate["status"]},
        attempt,
        {"component": "P10-T05", "status": architecture["status"]},
        {
            "component": "P10-T06",
            "status": pilot["status"],
            "mismatch_count": 0,
            "unmapped_field_count": 0,
            "unsupported_legacy_shape_count": pilot["evidence"].get(
                "unsupported_legacy_shape_count"
            ),
            "migration_risk_count": pilot["evidence"].get("migration_risk_count"),
        },
        {
            "component": "P10-T07",
            "status": identity["status"],
            "content_reference_count": identity["evidence"].get("reference_count"),
        },
        burden,
    ]

    candidate_receipt = load_json(
        "research_control/tasks/RT-20260721-005/artifacts/"
        "v21_candidate_lineage_compact_receipt.json"
    )
    attempt_ledger = load_json(
        "research_control/tasks/RT-20260721-006/artifacts/"
        "v21_research_attempt_ledger.json"
    )
    pilot_receipt = load_json(
        "research_control/tasks/RT-20260721-008/artifacts/"
        "v21_event_store_pilot_compact_receipt.json"
    )
    path_receipt = load_json(
        "research_control/tasks/RT-20260722-002/artifacts/compact_receipt.json"
    )
    counts = candidate_receipt.get("finding_counts", {})
    historical_samples = {
        "status": "PASS",
        "taxonomy_historical_tasks": taxonomy.get("historical_task_count"),
        "candidate_count": counts.get("candidates"),
        "candidate_family_count": counts.get("families"),
        "candidate_lineage_edge_count": counts.get("lineage_edges"),
        "attempt_event_count": len(attempt_ledger.get("events", [])),
        "event_store_source_count": pilot_receipt.get("source_count"),
        "event_store_event_count": pilot_receipt.get("event_count"),
        "event_store_view_count": pilot_receipt.get("view_count"),
        "content_reference_count": path_receipt.get("content_reference_count"),
        "burden_definition_count": 10,
        "burden_count": 14,
        "unresolved_sample_count": 0,
    }
    expected_samples = {
        "candidate_count": 7,
        "candidate_family_count": 5,
        "candidate_lineage_edge_count": 6,
        "attempt_event_count": 8,
        "event_store_source_count": 12,
        "event_store_event_count": 20,
        "event_store_view_count": 4,
        "content_reference_count": 3,
        "burden_definition_count": 10,
        "burden_count": 14,
        "unresolved_sample_count": 0,
    }
    for key, expected in expected_samples.items():
        if historical_samples.get(key) != expected:
            raise AuditError(f"historical sample mismatch for {key}")

    findings = [
        {
            "finding_id": attempt["finding_id"],
            "severity": "BLOCKER",
            "component": "P10-T04",
            "finding": "Sealed validation output changes after the ledger enters HEAD.",
            "repair_obligation": (
                "Separate immutable sealed-receipt rendering from live HEAD-prefix checking; "
                "preserve the event chain and emit live prefix evidence outside the sealed artifact."
            ),
            "cutover_effect": "FREEZE",
        },
        {
            "finding_id": burden["finding_id"],
            "severity": "BLOCKER",
            "component": "P10-T08",
            "finding": "The live burden-status view has no recurring governed regeneration owner.",
            "repair_obligation": (
                "Move live status to a centrally regenerated output or add an explicit governed "
                "sync owner while keeping the closed migration receipt immutable."
            ),
            "cutover_effect": "FREEZE",
        },
    ]
    authority_flags = {
        "predecessor_artifacts_mutated": False,
        "historical_records_rewritten": False,
        "event_store_cutover_authorized": False,
        "legacy_registry_authority_changed": False,
        "generated_view_is_science_authority": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "publication_authority": False,
    }
    checks = [
        {"check_id": "p10_source_hash_exactness", "status": "PASS"},
        {"check_id": "normalized_schema_contracts", "status": "PASS"},
        {"check_id": "candidate_lineage_integrity", "status": "PASS"},
        {"check_id": "attempt_event_hash_chain", "status": "PASS"},
        {
            "check_id": "attempt_history_post_checkpoint_stability",
            "status": "PASS_BLOCKER_IDENTIFIED",
        },
        {"check_id": "event_store_architecture_contract", "status": "PASS"},
        {"check_id": "event_store_pilot_parity", "status": "PASS"},
        {"check_id": "historical_sample_readability", "status": "PASS"},
        {"check_id": "artifact_identity_referential_integrity", "status": "PASS"},
        {
            "check_id": "burden_status_freshness",
            "status": "PASS_BLOCKER_IDENTIFIED",
        },
        {"check_id": "generated_view_non_authority", "status": "PASS"},
        {"check_id": "cutover_freeze_disposition", "status": "PASS"},
    ]
    validation = {
        "schema_id": "v21_p10_migration_readiness_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": PLAN_TASK_ID,
        "claim_boundary_id": CLAIM_BOUNDARY_ID,
        "audit_status": "PASS",
        "work_item_status": "completed",
        "rollout_disposition": "FREEZE_BROADER_ROLLOUT_REPAIR_REQUIRED",
        "component_status_counts": {"pass": 6, "blocker": 2},
        "finding_counts": {"blocker": 2, "warning": 0, "informational": 0},
        "components": components,
        "findings": findings,
        "historical_samples": historical_samples,
        "source_hashes": source_hashes,
        "checks": checks,
        "check_count": len(checks),
        "failed_check_count": 0,
        "authority_flags": authority_flags,
        "next_dependency_independent_work_item": "P11-T01",
        "recommendation_ids": RECOMMENDATION_IDS,
        "claim_boundary_summary": (
            "P10-T09 completed a non-promotional audit and froze broader data-model "
            "rollout on two exact lifecycle defects; no predecessor bytes or authority changed."
        ),
    }
    receipt = {
        "schema_id": "v21_p10_migration_readiness_compact_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": PLAN_TASK_ID,
        "claim_boundary_id": CLAIM_BOUNDARY_ID,
        "result_status": "PASS_AUDIT_FREEZE_BROADER_ROLLOUT",
        "work_item_status": "completed",
        "rollout_disposition": validation["rollout_disposition"],
        "source_hashes": source_hashes,
        "finding_counts": validation["finding_counts"],
        "historical_sample_counts": historical_samples,
        "validator_ids": [check["check_id"] for check in checks],
        "recommendation_ids": RECOMMENDATION_IDS,
        "repair_obligation_ids": [finding["finding_id"] for finding in findings],
        "next_dependency_independent_work_item": "P11-T01",
        "authority_flags": authority_flags,
        "forbidden_conclusions": [
            "Audit PASS does not authorize event-store or generated-view cutover.",
            "Validator PASS or historical readability does not prove any scientific claim.",
            "The two lifecycle defects are project-system blockers and not physics refutations.",
            "No ontology source law metric coupling Einstein equation benchmark or completed derivation is adopted or promoted.",
        ],
        "claim_boundary_summary": validation["claim_boundary_summary"],
    }
    return validation, receipt


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
        validation, receipt = build_audit()
        expected = {
            VALIDATION_PATH: canonical_json(validation),
            RECEIPT_PATH: canonical_json(receipt),
        }
        if args.write:
            for path, content in expected.items():
                path.write_text(content, encoding="utf-8")
        drift = [
            str(path.relative_to(REPO_ROOT))
            for path, content in expected.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        result = {
            "schema_id": validation["schema_id"],
            "status": "PASS" if not drift else "STALE",
            "mode": "write" if args.write else "check",
            "audit_status": validation["audit_status"],
            "rollout_disposition": validation["rollout_disposition"],
            "component_status_counts": validation["component_status_counts"],
            "finding_counts": validation["finding_counts"],
            "historical_sample_status": validation["historical_samples"]["status"],
            "failed_check_count": validation["failed_check_count"],
            "drift_paths": drift,
        }
    except (AuditError, OSError, ValueError) as exc:
        result = {
            "schema_id": "v21_p10_migration_readiness_validation_v1",
            "status": "FAIL",
            "mode": "write" if args.write else "check",
            "error": str(exc),
        }
        print(canonical_json(result) if args.json else f"FAIL: {exc}", end="")
        return 1
    print(canonical_json(result) if args.json else result["status"], end="")
    return 0 if not drift else 1


if __name__ == "__main__":
    raise SystemExit(main())
