#!/usr/bin/env python3
"""Validate the bounded V22 plan-namespace route-guard repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT_BOOTSTRAP = Path(__file__).resolve().parents[4]
if str(ROOT_BOOTSTRAP) not in sys.path:
    sys.path.insert(0, str(ROOT_BOOTSTRAP))

from scripts.project_control.classify_project_changes import classify_paths
from scripts.research_control.ordinary_route_guard import (
    AUTHORITY_LIMITS,
    CHECKPOINT_RECOVERY_SCHEMA_ID,
    DEFAULT_PLAN_ID,
    EVALUATION_SCHEMA_ID,
    EXCEPTION_SCHEMA_ID,
    PLAN_BACKLOG_PATHS,
    POLICY_ID,
    THRESHOLD,
    completed_plan_task_identities,
    derive_consecutive_project_system_tasks,
    discover_ready_science_routes,
    evaluate_agent_job_route_admission,
    evaluate_guard_record,
    evaluate_research_handoff_guard,
)


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260808-004"
JOB_ID = "AJ-RT-20260808-004-001"
PLAN_V21 = DEFAULT_PLAN_ID
PLAN_V22 = "recommendations_implementation_plan_continue_task-v22"
CREATED_AT = "2026-08-08T23:48:18Z"
HANDOFF_ID = "handoff-0969"
HANDOFF_PATH = ROOT / "research_control/handoffs/handoff-0969.yaml"
HANDOFF_SHA256 = "e18d9ad8454c27a75034a35e727a35738e540e616fd58dcf4954510da4f1ff95"
BLOCKER_PATH = ROOT / (
    "research_control/tasks/RT-20260808-003/artifacts/"
    "v22_p0_t03_runtime_route_collision_blocker.yaml"
)
BLOCKER_SHA256 = "15c98d0a1a9ef4ec3c8cad493c0cdd7319d34274c5d04e4846c6e199dbd5f974"
JOB_PATH = ROOT / f"research_control/tasks/{TASK_ID}/jobs/{JOB_ID}.yaml"
REPORT_PATH = ROOT / (
    f"research_control/tasks/{TASK_ID}/artifacts/"
    "v22_plan_namespace_guard_repair_validation.json"
)
COMPACT_PATH = ROOT / (
    f"research_control/tasks/{TASK_ID}/artifacts/"
    "v22_plan_namespace_guard_repair_compact_receipt.json"
)
EXPECTED_SOURCE_HASHES = {
    "scripts/research_control/ordinary_route_guard.py": "7487051d0b4ddd564fd67d809e3ac55f20967990a7546398c9e82589cb064173",
    "scripts/project_control/classify_project_changes.py": "37bd183299ff0ac1c3ed94cb19e9e27dfca4edcbd4499c0d832ea291164023dc",
    ".agents/schemas/AGENT_JOB_SCHEMA.md": "d804e9e2138eb24ddfd3c8ee3ab7fc829094d1073b82efe3e32dbe017ed92d75",
    "research_control/tasks/RT-20260722-015/artifacts/ordinary_route_guard_policy_v1.md": "00f34722e9e9f50182acccf9143cc295f4cdf8439321820e41f25b5b0bfbc0c8",
    "research_control/tasks/RT-20260722-015/artifacts/ordinary_route_exception_schema_v1.md": "1f39db8b1efce9828bfc6226794f6d7b102910f7bc03d2cfde19cf5e628f8e16",
    "research_control/design/v22_recommendation_backlog.yaml": "b2c9c01a29a701b92e23023496e2d901275ccc96777740a086ded86c7374ed6f",
    "research_control/design/v22_recommendation_backlog_schema.md": "f7bd3b52220d0d5ffe374a06676fd8b1c012e297932f9b363ff89161c127c30c",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def require(
    condition: bool,
    finding_id: str,
    message: str,
    findings: list[dict[str, str]],
) -> None:
    if not condition:
        findings.append({"finding_id": finding_id, "message": message})


def backlog_item(plan_id: str, plan_task_id: str) -> dict[str, Any]:
    path = ROOT / PLAN_BACKLOG_PATHS[plan_id]
    backlog = load_yaml(path)
    return next(
        (
            item
            for item in backlog.get("items", [])
            if isinstance(item, dict) and item.get("plan_task_id") == plan_task_id
        ),
        {},
    )


def synthetic_v22_handoff_guard() -> tuple[dict[str, Any], dict[str, Any]]:
    selected = backlog_item(PLAN_V22, "P1-T01")
    ready = discover_ready_science_routes(ROOT, CREATED_AT, PLAN_V22)
    run_length = derive_consecutive_project_system_tasks(ROOT, CREATED_AT)
    ready_ids = [str(item["plan_task_id"]) for item in ready]
    ready_refs = [f"{PLAN_V22}:{item}" for item in ready_ids]
    record = {
        "schema_id": EVALUATION_SCHEMA_ID,
        "policy_id": POLICY_ID,
        "evaluation_id": "ORE-V22-P1-T01-SYNTHETIC",
        "ordinary_handoff_id": "handoff-v22-p1-t01-synthetic",
        "selected_plan_id": PLAN_V22,
        "threshold": THRESHOLD,
        "consecutive_project_system_tasks_before_selection": run_length,
        "ready_science_plan_task_ids": ready_ids,
        "ready_science_plan_task_refs": ready_refs,
        "selected_plan_task_id": "P1-T01",
        "selected_route_class": "project_system",
        "selected_worker_skill": "improve-project-system",
        "outcome": "all_ready_science_blocked_exception",
        "ordinary_research_handoff_authoritative": True,
        "project_system_sidecar_supersedes": False,
        "exception_receipt": {
            "active": True,
            "schema_id": EXCEPTION_SCHEMA_ID,
            "exception_id": "ORE-V22-P1-T01-SYNTHETIC-EXCEPTION-001",
            "exception_class": "all_ready_science_blocked",
            "ordinary_handoff_id": "handoff-v22-p1-t01-synthetic",
            "ready_science_plan_task_ids": ready_ids,
            "ready_science_plan_task_refs": ready_refs,
            "blocked_routes": [],
            "authority_limits": dict(AUTHORITY_LIMITS),
        },
        "authority_limits": dict(AUTHORITY_LIMITS),
    }
    result = evaluate_guard_record(
        record,
        handoff_id="handoff-v22-p1-t01-synthetic",
        selected_plan_id=PLAN_V22,
        selected_plan_task_id="P1-T01",
        selected_plan_item=selected,
        ready_science_routes=ready,
        observed_run_length=run_length,
        repo_root=ROOT,
        backlog_path=PLAN_BACKLOG_PATHS[PLAN_V22],
    )
    return record, result


def build_report() -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    require(
        PLAN_BACKLOG_PATHS
        == {
            PLAN_V21: "research_control/design/v21_recommendation_backlog.yaml",
            PLAN_V22: "research_control/design/v22_recommendation_backlog.yaml",
        },
        "V22-NS-001",
        "registered recommendation-plan backlog map differs",
        findings,
    )

    v21_p1 = backlog_item(PLAN_V21, "P1-T01")
    v22_p1 = backlog_item(PLAN_V22, "P1-T01")
    require(v21_p1.get("task_class") == "science", "V22-NS-002", "V21 P1-T01 class changed", findings)
    require(v21_p1.get("worker_skill") == "continue-research", "V22-NS-003", "V21 P1-T01 route changed", findings)
    expected_v22_route = {
        "work_kind": "construction_or_implementation",
        "task_class": "project_system",
        "role_family": "project-control-maintainer@0.2.0",
        "controlling_launcher": "continue-research-goal@v4",
        "worker_skill": "improve-project-system",
        "route_label": "ordinary-research-packet",
        "target_derivation_milestone": "none",
        "expected_result_kind": "implemented_and_validated_or_precisely_blocked",
        "requires_human_gate": False,
        "dependency_independent_after_other_human_gates": True,
        "allow_scope_expansion": False,
    }
    for key, expected in expected_v22_route.items():
        require(v22_p1.get(key) == expected, "V22-NS-004", f"V22 P1-T01 runtime field mismatch: {key}", findings)

    completed = completed_plan_task_identities(ROOT, CREATED_AT)
    require((PLAN_V22, "P0-T03") in completed, "V22-NS-005", "fresh qualifying V22 P0-T03 completion is absent", findings)
    require((PLAN_V22, "P1-T01") not in completed, "V22-NS-006", "V21 completion cross-satisfied V22 P1-T01", findings)

    handoff = load_yaml(HANDOFF_PATH)
    handoff_result = evaluate_research_handoff_guard(handoff, ROOT)
    require(sha256(HANDOFF_PATH) == HANDOFF_SHA256, "V22-NS-007", "source handoff hash changed", findings)
    require(handoff_result.get("status") == "PASS", "V22-NS-008", f"handoff-0969 guard failed: {handoff_result}", findings)

    job = load_yaml(JOB_PATH)
    admission_result = evaluate_agent_job_route_admission(job, created_at=str(job.get("created_at", "")), repo_root=ROOT)
    require(job.get("checkpoint_recovery", {}).get("schema_id") == CHECKPOINT_RECOVERY_SCHEMA_ID, "V22-NS-009", "atomic checkpoint-recovery schema missing", findings)
    require(admission_result.get("status") == "PASS", "V22-NS-010", f"repair AgentJob route admission failed: {admission_result}", findings)

    synthetic_record, synthetic_result = synthetic_v22_handoff_guard()
    require(synthetic_result.get("status") == "PASS", "V22-NS-011", f"synthetic V22 P1-T01 routing failed: {synthetic_result}", findings)
    require(synthetic_result.get("selected_plan_id") == PLAN_V22, "V22-NS-012", "synthetic route did not retain V22 identity", findings)

    classifier = classify_paths(
        [
            ".gitignore",
            "research_control/design/v22_recommendation_backlog.yaml",
        ],
        registry_root=ROOT,
    )
    tags = set(classifier.get("path_family_tags", []))
    require("unknown_governed_path" not in tags, "V22-NS-013", "required recovery paths remain unknown to classifier", findings)
    require("ci_orchestration" in tags, "V22-NS-014", ".gitignore classification missing", findings)
    require({"control_state", "role_or_schema_contract"}.issubset(tags), "V22-NS-015", "versioned backlog classification missing", findings)

    require(sha256(BLOCKER_PATH) == BLOCKER_SHA256, "V22-NS-016", "source blocker hash changed", findings)
    source_hashes = {
        path: sha256(ROOT / path) for path in EXPECTED_SOURCE_HASHES
    }
    for path, expected in EXPECTED_SOURCE_HASHES.items():
        require(source_hashes[path] == expected, "V22-NS-017", f"repair source hash mismatch: {path}", findings)

    return {
        "schema_id": "v22_plan_namespace_guard_repair_validation_v1",
        "status": "PASS" if not findings else "FAIL",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "created_at": CREATED_AT,
        "finding_count": len(findings),
        "findings": findings,
        "source_handoff": {"handoff_id": HANDOFF_ID, "path": str(HANDOFF_PATH.relative_to(ROOT)), "sha256": HANDOFF_SHA256, "guard_result": handoff_result},
        "source_blocker": {"path": str(BLOCKER_PATH.relative_to(ROOT)), "sha256": BLOCKER_SHA256},
        "registered_plan_backlogs": dict(PLAN_BACKLOG_PATHS),
        "plan_local_collision_fixture": {
            "local_plan_task_id": "P1-T01",
            "v21_task_class": v21_p1.get("task_class"),
            "v21_worker_skill": v21_p1.get("worker_skill"),
            "v22_task_class": v22_p1.get("task_class"),
            "v22_worker_skill": v22_p1.get("worker_skill"),
        },
        "completed_identity_checks": {
            "v22_p0_t03_qualifying_complete": (PLAN_V22, "P0-T03") in completed,
            "v22_p1_t01_complete": (PLAN_V22, "P1-T01") in completed,
        },
        "repair_agentjob_admission": admission_result,
        "synthetic_v22_p1_t01_guard": {
            "record": synthetic_record,
            "result": synthetic_result,
        },
        "classifier": {
            "reason_codes": classifier.get("reason_codes", []),
            "path_family_tags": classifier.get("path_family_tags", []),
            "recommended_validation_profile": classifier.get("recommended_validation_profile", ""),
        },
        "source_hashes": source_hashes,
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "p1_t01_execution_authorized": False,
            "external_action_authorized": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()
    payload = json_bytes(report)
    report_matches = REPORT_PATH.is_file() and REPORT_PATH.read_bytes() == payload
    if args.write:
        REPORT_PATH.write_bytes(payload)
        report_matches = True
    report_hash = hashlib.sha256(payload).hexdigest()
    compact = {
        "schema_id": "v22_plan_namespace_guard_repair_compact_receipt_v1",
        "status": report["status"],
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "created_at": CREATED_AT,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "report_sha256": report_hash,
        "finding_count": report["finding_count"],
        "v22_p0_t03_qualifying_complete": report["completed_identity_checks"]["v22_p0_t03_qualifying_complete"],
        "v22_p1_t01_selected_not_executed": report["synthetic_v22_p1_t01_guard"]["result"]["status"] == "PASS",
        "scientific_status_changed": False,
        "distance_to_gr_changed": False,
        "physics_promotion_authorized": False,
        "external_action_authorized": False,
    }
    compact_payload = json_bytes(compact)
    compact_matches = COMPACT_PATH.is_file() and COMPACT_PATH.read_bytes() == compact_payload
    if args.write:
        COMPACT_PATH.write_bytes(compact_payload)
        compact_matches = True
    if not args.write:
        require(report_matches, "V22-NS-018", "validation report is missing or stale", report["findings"])
        require(compact_matches, "V22-NS-019", "compact receipt is missing or stale", report["findings"])
        report["finding_count"] = len(report["findings"])
        report["status"] = "PASS" if not report["findings"] else "FAIL"
    if args.json:
        print(json.dumps({
            "status": report["status"],
            "finding_count": report["finding_count"],
            "report_path": str(REPORT_PATH.relative_to(ROOT)),
            "report_sha256": report_hash,
            "compact_path": str(COMPACT_PATH.relative_to(ROOT)),
            "outputs_current": report_matches and compact_matches,
        }, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" and report_matches and compact_matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
