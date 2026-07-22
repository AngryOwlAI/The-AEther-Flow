#!/usr/bin/env python3
"""Validate the deterministic P12-T04 ordinary-route guard fixture suite."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.research_control.ordinary_route_guard import (  # noqa: E402
    AUTHORITY_LIMITS,
    BACKLOG_PATH,
    EVALUATION_SCHEMA_ID,
    EXCEPTION_SCHEMA_ID,
    POLICY_ID,
    THRESHOLD,
    evaluate_guard_record,
)


TASK_ROOT = ROOT / "research_control/tasks/RT-20260722-015"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
FIXTURE_PATH = ARTIFACT_ROOT / "fixtures/ordinary_route_guard_cases.json"
REPORT_PATH = ARTIFACT_ROOT / "ordinary_route_guard_validation_report.json"
RECEIPT_PATH = ARTIFACT_ROOT / "ordinary_route_guard_compact_receipt.json"
POLICY_PATH = ARTIFACT_ROOT / "ordinary_route_guard_policy_v1.md"
EXCEPTION_SCHEMA_PATH = ARTIFACT_ROOT / "ordinary_route_exception_schema_v1.md"
EVALUATOR_PATH = ROOT / "scripts/research_control/ordinary_route_guard.py"
GENERATED_AT = "2026-07-22T19:00:53Z"
HANDOFF_ID = "handoff-9000"
CONTROL_EVIDENCE_PATH = "research_control/tasks/RT-FIXTURE/artifacts/control_failure.yaml"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ready_route(plan_task_id: str, *, human_gate: bool = False) -> dict[str, Any]:
    return {
        "plan_task_id": plan_task_id,
        "work_kind": "protected_gate_review" if human_gate else "formalization_or_theorem",
        "route_label": "human-gated-ontology-decision" if human_gate else "philosophy-foundations-packet",
        "worker_skill": "none_until_human_authorization" if human_gate else "continue-research",
        "requires_human_gate": human_gate,
        "dependencies": ["P0-T05"],
    }


def ready_routes(kind: str) -> list[dict[str, Any]]:
    human = ready_route("P4-T05", human_gate=True)
    unblocked = ready_route("P14-T01")
    if kind == "human_gate_only":
        return [human]
    if kind == "unblocked_only":
        return [unblocked]
    if kind == "none":
        return []
    return [human, unblocked]


def selected_item(kind: str) -> tuple[str, dict[str, Any]]:
    if kind == "physics":
        return "P14-T01", {
            "plan_task_id": "P14-T01",
            "task_class": "science",
            "worker_skill": "continue-research",
            "requires_human_gate": False,
        }
    if kind == "human_gate":
        return "P4-T05", {
            "plan_task_id": "P4-T05",
            "task_class": "science",
            "worker_skill": "none_until_human_authorization",
            "requires_human_gate": True,
        }
    return "P12-T05", {
        "plan_task_id": "P12-T05",
        "task_class": "project_system",
        "worker_skill": "improve-project-system",
        "requires_human_gate": False,
    }


def inactive_receipt() -> dict[str, Any]:
    return {"active": False}


def active_receipt(
    routes: list[dict[str, Any]],
    blocked_routes: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "active": True,
        "schema_id": EXCEPTION_SCHEMA_ID,
        "exception_id": "ORE-FIXTURE-001",
        "exception_class": "all_ready_science_blocked",
        "ordinary_handoff_id": HANDOFF_ID,
        "ready_science_plan_task_ids": [route["plan_task_id"] for route in routes],
        "blocked_routes": blocked_routes,
        "authority_limits": dict(AUTHORITY_LIMITS),
    }


def write_fixture_evidence(repo_root: Path) -> tuple[str, str]:
    backlog_path = repo_root / BACKLOG_PATH
    backlog_path.parent.mkdir(parents=True, exist_ok=True)
    backlog_path.write_text("schema_id: fixture_backlog\n", encoding="utf-8")
    control_path = repo_root / CONTROL_EVIDENCE_PATH
    control_path.parent.mkdir(parents=True, exist_ok=True)
    control_path.write_text(
        "schema_id: ordinary_route_control_failure_v1\n"
        "failure_id: ORE-FIXTURE-CONTROL-001\n"
        "plan_task_id: P14-T01\n"
        "failure_class: claim_boundary_hard_failure\n"
        "status: active_blocking\n"
        "blocks_scientific_execution: true\n",
        encoding="utf-8",
    )
    return sha256_path(backlog_path), sha256_path(control_path)


def build_case(case: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    routes = ready_routes(str(case.get("ready_set", "mixed")))
    selected_plan_task_id, item = selected_item(str(case.get("selected_kind", "project_system")))
    backlog_hash, control_hash = write_fixture_evidence(repo_root)
    mode = str(case.get("exception_mode", "inactive"))
    tracked = {BACKLOG_PATH, CONTROL_EVIDENCE_PATH}
    receipt = inactive_receipt()
    if mode in {"valid_human_gate", "stale_hash"}:
        evidence_hash = backlog_hash if mode == "valid_human_gate" else "0" * 64
        receipt = active_receipt(
            routes,
            [
                {
                    "plan_task_id": "P4-T05",
                    "failure_class": "human_gate_required",
                    "evidence_path": BACKLOG_PATH,
                    "evidence_sha256": evidence_hash,
                }
            ],
        )
    elif mode in {"valid_control_failure", "untracked"}:
        receipt = active_receipt(
            routes,
            [
                {
                    "plan_task_id": "P14-T01",
                    "failure_class": "claim_boundary_hard_failure",
                    "evidence_path": CONTROL_EVIDENCE_PATH,
                    "evidence_sha256": control_hash,
                }
            ],
        )
        if mode == "untracked":
            tracked.remove(CONTROL_EVIDENCE_PATH)
    elif mode == "partial":
        receipt = active_receipt(
            routes,
            [
                {
                    "plan_task_id": "P4-T05",
                    "failure_class": "human_gate_required",
                    "evidence_path": BACKLOG_PATH,
                    "evidence_sha256": backlog_hash,
                }
            ],
        )

    run_length = int(case.get("run_length", 0))
    selected_kind = str(case.get("selected_kind", "project_system"))
    if run_length < THRESHOLD:
        outcome = "below_threshold"
    elif selected_kind == "physics":
        outcome = "physics_bearing_route_selected"
    elif selected_kind == "human_gate":
        outcome = "blocked"
    else:
        outcome = "all_ready_science_blocked_exception"
    sidecar_supersedes = case.get("sidecar_supersedes") is True
    record = {
        "schema_id": EVALUATION_SCHEMA_ID,
        "policy_id": POLICY_ID,
        "evaluation_id": f"ORE-{case['case_id']}",
        "ordinary_handoff_id": HANDOFF_ID,
        "threshold": THRESHOLD,
        "consecutive_project_system_tasks_before_selection": run_length,
        "ready_science_plan_task_ids": [route["plan_task_id"] for route in routes],
        "selected_plan_task_id": selected_plan_task_id,
        "selected_route_class": "physics_bearing" if item["task_class"] == "science" else "project_system",
        "selected_worker_skill": item["worker_skill"],
        "outcome": outcome,
        "ordinary_research_handoff_authoritative": True,
        "project_system_sidecar_supersedes": sidecar_supersedes,
        "exception_receipt": receipt,
        "authority_limits": dict(AUTHORITY_LIMITS),
    }
    result = evaluate_guard_record(
        record,
        handoff_id=HANDOFF_ID,
        selected_plan_task_id=selected_plan_task_id,
        selected_plan_item=item,
        ready_science_routes=routes,
        observed_run_length=run_length,
        repo_root=repo_root,
        tracked_paths=tracked,
    )
    expected = str(case.get("expected_status", "FAIL"))
    return {
        "case_id": case["case_id"],
        "expected_status": expected,
        "observed_status": result["status"],
        "matches_expected": result["status"] == expected,
        "error_ids": result["errors"],
        "warning_ids": result["warnings"],
    }


def build_validation_report() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    case_results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="ordinary-route-guard-") as temp_dir:
        temp_root = Path(temp_dir)
        for case in fixture["cases"]:
            case_results.append(build_case(case, temp_root))
    passed = sum(1 for result in case_results if result["matches_expected"])
    return {
        "schema_id": "ordinary_route_guard_validation_report_v1",
        "policy_id": POLICY_ID,
        "implements_plan_task_id": "P12-T04",
        "generated_at": GENERATED_AT,
        "status": "PASS" if passed == len(case_results) else "FAIL",
        "fixture_case_count": len(case_results),
        "fixture_pass_count": passed,
        "fixture_failure_count": len(case_results) - passed,
        "case_results": case_results,
        "source_hashes": {
            "fixture_suite": sha256_path(FIXTURE_PATH),
            "evaluator": sha256_path(EVALUATOR_PATH),
            "policy": sha256_path(POLICY_PATH),
            "exception_schema": sha256_path(EXCEPTION_SCHEMA_PATH),
        },
        "validated_controls": [
            "below_threshold_pass",
            "advisory_warning_before_hard_block",
            "physics_bearing_selection",
            "missing_exception_rejection",
            "all_ready_science_accounting",
            "human_gate_blocking",
            "active_control_failure_evidence",
            "stale_hash_rejection",
            "untracked_evidence_rejection",
            "sidecar_substitution_rejection",
        ],
        "authority_boundary": {
            "project_control_only": True,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def build_compact_receipt(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "ordinary_route_guard_compact_receipt_v1",
        "policy_id": POLICY_ID,
        "implements_plan_task_id": "P12-T04",
        "generated_at": GENERATED_AT,
        "status": report["status"],
        "threshold": THRESHOLD,
        "warning_at": THRESHOLD - 1,
        "fixture_case_count": report["fixture_case_count"],
        "fixture_pass_count": report["fixture_pass_count"],
        "fixture_failure_count": report["fixture_failure_count"],
        "source_hashes": report["source_hashes"],
        "ordinary_research_handoff_authoritative": True,
        "project_system_sidecar_supersedes": False,
        "exceptions_hash_bound": True,
        "all_ready_science_required": True,
        "historical_records_unchanged": True,
        "system_success_counts_as_physics": False,
        "system_success_counts_as_distance_to_gr": False,
        "scientific_claims_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def serialized(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = build_validation_report()
    receipt = build_compact_receipt(report)
    generated = {REPORT_PATH: serialized(report), RECEIPT_PATH: serialized(receipt)}
    check_ok = True
    if args.write:
        for path, content in generated.items():
            path.write_text(content, encoding="utf-8")
    if args.check:
        check_ok = all(path.is_file() and path.read_text(encoding="utf-8") == content for path, content in generated.items())
    output = {
        "status": report["status"] if check_ok else "FAIL",
        "fixture_case_count": report["fixture_case_count"],
        "fixture_pass_count": report["fixture_pass_count"],
        "fixture_failure_count": report["fixture_failure_count"],
        "generated_files_match": check_ok,
    }
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(output["status"])
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
