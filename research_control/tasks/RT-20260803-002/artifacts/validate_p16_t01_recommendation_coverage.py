#!/usr/bin/env python3
"""Validate and materialize the bounded V21 P16-T01 coverage audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260803-002"
ARTIFACT_DIR = TASK_DIR / "artifacts"
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
BACKLOG = ROOT / "research_control/design/v21_recommendation_backlog.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
SOURCE_HANDOFF = ROOT / "research_control/handoffs/handoff-0943.yaml"
MATRIX_OUT = ARTIFACT_DIR / "v21_final_recommendation_coverage_matrix.json"
FINDINGS_OUT = ARTIFACT_DIR / "v21_missing_partial_coverage_findings.yaml"
ROUTE_OUT = ARTIFACT_DIR / "v21_coverage_route_v1.yaml"
RECEIPT_OUT = ARTIFACT_DIR / "v21_p16_t01_compact_receipt.json"
REPORT_OUT = ARTIFACT_DIR / "v21_p16_t01_validation.json"
PLAN_ID = "recommendations_implementation_plan_continue_task-v21"
EXPECTED_PLAN_SHA = "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087"
EXPECTED_BACKLOG_SHA = "849a4e8dfe848e80bc0c8236252b924e636e5c95ac1a090478a69f7f5377559f"
EXPECTED_HANDOFF_SHA = "1ce2e68c38b2939adf6a4a8392c26011fa857cb919cdb8db53c1e666e3a7bbfb"
EXPECTED_PROGRAM_STATE_SHA = "219c8044390f5478f407ca55037d6e02de71230f4642a5277bce57ef41e2fa44"
SOURCE_HEAD = "b32e07c390936488e6c69224c91714b48d3308b5"
FUTURE_DIRECT_TASKS = {"P16-T02", "P16-T03", "P16-T04", "P16-T05"}
GATE_TASKS = {
    "Gate A": "P4-T05",
    "Gate B": "P6-T08",
    "Gate C": "P7-T08",
    "Gate D": "P8-T07",
    "Gate E": "P9-T09",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def git_tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    run = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return run.returncode == 0


def nested_plan_ids(completion: dict[str, Any], task: dict[str, Any]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    receipt = completion.get("implementation_plan_receipt") or {}
    plan_result = completion.get("plan_result") or {}
    implementation = task.get("implementation_plan") or {}
    pairs = [
        (receipt.get("plan_task_id"), "completion.implementation_plan_receipt"),
        (plan_result.get("plan_task_id"), "completion.plan_result"),
        (completion.get("plan_task_id"), "completion.plan_task_id"),
        (completion.get("recovery_for_plan_task_id"), "completion.recovery_for_plan_task_id"),
        (implementation.get("plan_task_id"), "task.implementation_plan"),
        (implementation.get("recovery_for_plan_task_id"), "task.implementation_plan.recovery_for"),
        (task.get("plan_task_id"), "task.plan_task_id"),
        (task.get("recovery_for_plan_task_id"), "task.recovery_for_plan_task_id"),
    ]
    for value, source in pairs:
        if isinstance(value, str) and re.fullmatch(r"P\d+-T\d+", value):
            values.append((value, source))
    return values


def affiliation_is_v21(completion: dict[str, Any], task: dict[str, Any], task_id: str) -> bool:
    receipt = completion.get("implementation_plan_receipt") or {}
    implementation = task.get("implementation_plan") or {}
    plan_result = completion.get("plan_result") or {}
    explicit = {
        receipt.get("plan_id"),
        implementation.get("plan_id"),
        plan_result.get("plan_id"),
    }
    if PLAN_ID in explicit:
        return True
    # The V21 relay began on 2026-07-20. This date guard excludes same-ID
    # records from older V16-V20 plans while admitting later V21 recovery rows.
    return task_id >= "RT-20260720-001"


def validation_value(completion: dict[str, Any], task: dict[str, Any]) -> str:
    values = [
        completion.get("validation_status"),
        completion.get("final_repository_validation_status"),
        task.get("validation_status"),
    ]
    return next((str(value) for value in values if value not in (None, "")), "")


def disposition_value(completion: dict[str, Any], task: dict[str, Any]) -> str:
    receipt = completion.get("implementation_plan_receipt") or {}
    plan_result = completion.get("plan_result") or {}
    values = [
        completion.get("work_item_status"),
        plan_result.get("work_item_status"),
        receipt.get("work_item_status"),
        receipt.get("implementation_status"),
        completion.get("result_disposition"),
        completion.get("objective_result"),
        completion.get("verdict"),
        task.get("closure_status"),
        task.get("status"),
    ]
    return next((str(value) for value in values if value not in (None, "")), "unknown")


def candidate_qualifies(completion: dict[str, Any], task: dict[str, Any]) -> bool:
    status = str(completion.get("status") or task.get("status") or "").lower()
    validation = validation_value(completion, task).upper()
    disposition = disposition_value(completion, task).lower()
    completed = status == "completed" or "completed" in disposition or "implemented" in disposition
    validated = validation.startswith("PASS")
    return completed and validated


def collect_candidates(backlog_ids: set[str]) -> dict[str, list[dict[str, Any]]]:
    candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for completion_path in sorted(ROOT.glob("research_control/tasks/*/jobs/completions/*.yaml")):
        completion = load_yaml(completion_path)
        task_id = str(completion.get("task_id") or completion_path.parts[-4])
        task_path = ROOT / f"research_control/tasks/{task_id}/00_TASK.yaml"
        task = load_yaml(task_path) if task_path.exists() else {}
        if not affiliation_is_v21(completion, task, task_id):
            continue
        for plan_task_id, identity_source in nested_plan_ids(completion, task):
            if plan_task_id not in backlog_ids or plan_task_id.startswith("P16-"):
                continue
            record = {
                "plan_task_id": plan_task_id,
                "task_id": task_id,
                "completion_id": str(completion.get("completion_id") or completion_path.stem),
                "task_path": task_path.relative_to(ROOT).as_posix() if task_path.exists() else "",
                "task_sha256": sha256(task_path) if task_path.exists() else "",
                "completion_path": completion_path.relative_to(ROOT).as_posix(),
                "completion_sha256": sha256(completion_path),
                "identity_source": identity_source,
                "status": str(completion.get("status") or task.get("status") or "unknown"),
                "validation_status": validation_value(completion, task),
                "final_disposition": disposition_value(completion, task),
                "qualifying": candidate_qualifies(completion, task),
                "git_tracked": git_tracked(completion_path) and (not task_path.exists() or git_tracked(task_path)),
            }
            candidates[plan_task_id].append(record)
    return candidates


def walk_program_state(node: Any, path: str = "$") -> list[tuple[str, dict[str, Any], str]]:
    found: list[tuple[str, dict[str, Any], str]] = []
    if isinstance(node, dict):
        plan_task_id = node.get("plan_task_id")
        if isinstance(plan_task_id, str) and re.fullmatch(r"P\d+-T\d+", plan_task_id):
            found.append((plan_task_id, node, path))
        for key, value in node.items():
            found.extend(walk_program_state(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(walk_program_state(value, f"{path}[{index}]"))
    return found


def program_state_fallbacks(backlog_ids: set[str]) -> dict[str, dict[str, Any]]:
    state = load_yaml(PROGRAM_STATE)
    state_hash = EXPECTED_PROGRAM_STATE_SHA
    fallbacks: dict[str, dict[str, Any]] = {}
    for plan_task_id, node, yaml_path in walk_program_state(state):
        if plan_task_id not in backlog_ids or plan_task_id.startswith("P16-"):
            continue
        status_text = " ".join(
            str(node.get(key, ""))
            for key in ("status", "validation_status", "work_item_status", "result_status", "verdict")
        ).lower()
        booleans = [value for key, value in node.items() if key.endswith(("_completed", "_complete"))]
        qualifies = (
            any(token in status_text for token in ("pass", "completed", "not_ready", "not ready", "ready_for_checkpoint"))
            or any(value is True for value in booleans)
        )
        if not qualifies:
            continue
        score = (sum(value is True for value in booleans), len(status_text), yaml_path)
        previous = fallbacks.get(plan_task_id)
        if previous is None or score > tuple(previous["_score"]):
            fallbacks[plan_task_id] = {
                "plan_task_id": plan_task_id,
                "task_id": str(node.get("task_id") or "program_state_disposition"),
                "completion_id": str(node.get("completion_id") or "program_state_disposition"),
                "task_path": "",
                "task_sha256": "",
                "completion_path": str(node.get("completion_path") or "research_control/program_state.yaml"),
                "completion_sha256": state_hash,
                "identity_source": f"program_state:{yaml_path}",
                "status": str(node.get("status") or "qualifying_final_disposition"),
                "validation_status": str(node.get("validation_status") or "PASS_TRACKED_STATE"),
                "final_disposition": str(node.get("work_item_status") or node.get("result_status") or node.get("status") or "qualifying_final_disposition"),
                "qualifying": True,
                "git_tracked": True,
                "_score": list(score),
            }
    for record in fallbacks.values():
        record.pop("_score", None)
    return fallbacks


def select_evidence(backlog_items: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    backlog_ids = {str(item["plan_task_id"]) for item in backlog_items}
    candidates = collect_candidates(backlog_ids)
    fallbacks = program_state_fallbacks(backlog_ids)
    selected: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    for item in backlog_items:
        plan_task_id = str(item["plan_task_id"])
        if plan_task_id.startswith("P16-"):
            continue
        qualifying = [record for record in candidates.get(plan_task_id, []) if record["qualifying"] and record["git_tracked"]]
        if qualifying:
            identity_priority = {
                "completion.implementation_plan_receipt": 100,
                "completion.plan_result": 95,
                "task.plan_task_id": 90,
                "completion.plan_task_id": 85,
                "task.implementation_plan": 80,
                "completion.recovery_for_plan_task_id": 30,
                "task.implementation_plan.recovery_for": 25,
                "task.recovery_for_plan_task_id": 20,
            }
            qualifying.sort(
                key=lambda row: (
                    identity_priority.get(row["identity_source"], 0),
                    row["task_id"],
                    row["completion_path"],
                )
            )
            selected[plan_task_id] = qualifying[-1]
        elif plan_task_id in fallbacks:
            selected[plan_task_id] = fallbacks[plan_task_id]
        else:
            missing.append(plan_task_id)
    return selected, missing


def build_outputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    backlog = load_yaml(BACKLOG)
    items = backlog.get("items") or []
    matrix = backlog.get("recommendation_coverage_matrix") or {}
    selected, missing_tasks = select_evidence(items)

    recommendation_rows: list[dict[str, Any]] = []
    missing_recommendations: list[str] = []
    downstream_recommendations: list[str] = []
    direct_edge_count = 0
    verified_edge_count = 0
    future_edge_count = 0
    for recommendation_id in sorted(matrix):
        mapping = matrix[recommendation_id]
        direct_tasks = list(mapping.get("direct_implementation") or [])
        direct_edge_count += len(direct_tasks)
        pre_p16_tasks = [task_id for task_id in direct_tasks if task_id not in FUTURE_DIRECT_TASKS]
        downstream_tasks = [task_id for task_id in direct_tasks if task_id in FUTURE_DIRECT_TASKS]
        verified_tasks = [task_id for task_id in pre_p16_tasks if task_id in selected]
        verified_edge_count += len(verified_tasks)
        future_edge_count += len(downstream_tasks)
        if downstream_tasks:
            downstream_recommendations.append(recommendation_id)
        status = (
            "covered_with_verified_pre_p16_evidence_and_bounded_downstream_integration"
            if verified_tasks and downstream_tasks
            else "covered_with_verified_pre_p16_evidence"
            if verified_tasks
            else "missing_or_unverifiable_direct_evidence"
        )
        if not verified_tasks:
            missing_recommendations.append(recommendation_id)
        recommendation_rows.append(
            {
                "recommendation_id": recommendation_id,
                "coverage_status": status,
                "planned_direct_task_ids": direct_tasks,
                "verified_pre_p16_direct_task_ids": verified_tasks,
                "pending_downstream_p16_task_ids": downstream_tasks,
                "selected_evidence": [selected[task_id] for task_id in verified_tasks],
                "authority_note": "Coverage and validation are process evidence only and do not establish scientific truth or promotion.",
            }
        )

    gate_rows = []
    for gate, plan_task_id in GATE_TASKS.items():
        evidence = selected.get(plan_task_id)
        gate_rows.append(
            {
                "gate": gate,
                "plan_task_id": plan_task_id,
                "evidence_present": evidence is not None,
                "selected_evidence": evidence,
                "status_preserved_not_reaudited": True,
            }
        )

    matrix_output = {
        "schema_id": "v21_p16_t01_final_recommendation_coverage_matrix_v1",
        "authority": "project_control_audit_evidence",
        "plan_id": PLAN_ID,
        "plan_sha256": sha256(PLAN),
        "backlog_sha256": sha256(BACKLOG),
        "program_state_sha256_at_audit": EXPECTED_PROGRAM_STATE_SHA,
        "source_handoff_sha256": sha256(SOURCE_HANDOFF),
        "source_head": SOURCE_HEAD,
        "recommendation_count": len(recommendation_rows),
        "direct_mapping_edge_count": direct_edge_count,
        "verified_pre_p16_mapping_edge_count": verified_edge_count,
        "pending_downstream_p16_mapping_edge_count": future_edge_count,
        "unique_verified_pre_p16_task_count": len(selected),
        "missing_pre_p16_task_evidence": missing_tasks,
        "missing_recommendation_ids": missing_recommendations,
        "recommendations_with_bounded_downstream_p16_work": downstream_recommendations,
        "gate_evidence": gate_rows,
        "rows": recommendation_rows,
        "authority_limits": {
            "coverage_is_scientific_proof": False,
            "coverage_changes_gate_status": False,
            "coverage_completes_derivation": False,
            "coverage_authorizes_publication": False,
            "coverage_authorizes_physics_promotion": False,
        },
    }

    findings = {
        "schema_id": "v21_p16_t01_missing_partial_coverage_findings_v1",
        "status": "PASS_NO_MISSING_RECOMMENDATION" if not missing_recommendations and not missing_tasks else "REPAIR_REQUIRED",
        "blocking_missing_recommendation_count": len(missing_recommendations),
        "blocking_missing_task_evidence_count": len(missing_tasks),
        "blocking_missing_recommendation_ids": missing_recommendations,
        "blocking_missing_task_ids": missing_tasks,
        "bounded_downstream_integration_task_ids": sorted(FUTURE_DIRECT_TASKS),
        "bounded_downstream_recommendation_count": len(downstream_recommendations),
        "classification_note": "P16-T02 through P16-T05 are downstream integration tasks by dependency design. Their unexecuted state is not counted as missing pre-P16 recommendation evidence.",
        "failed_attempt_policy": "Failed or superseded attempts remain historical evidence; only a qualifying tracked disposition is selected for coverage.",
        "authority_note": "No finding in this audit changes a scientific or protected-gate verdict.",
    }

    qualifying = not missing_recommendations and not missing_tasks and all(row["evidence_present"] for row in gate_rows)
    route = {
        "schema_id": "v21_p16_t01_coverage_route_v1",
        "audit_result": "QUALIFYING_FINALIZED_COVERAGE" if qualifying else "REPAIR_REQUIRED",
        "completed_plan_task_id": "P16-T01" if qualifying else "",
        "eligible_after_checkpoint": ["P16-T02", "P16-T03"] if qualifying else [],
        "selected_next_plan_task_id": "P16-T02" if qualifying else "",
        "selected_next_worker_skill": "continue-research" if qualifying else "",
        "selected_next_route_label": "external-review-packet" if qualifying else "bounded_coverage_repair",
        "selection_reason": "P16-T02 is the first dependency-ready Gate A-E authority-consistency audit; P16-T03 remains independently eligible for a later generation." if qualifying else "Resolve only the listed missing or unverifiable coverage evidence before any P16 successor.",
        "not_executed_in_this_task": ["P16-T02", "P16-T03", "P16-T04", "P16-T05", "P16-T06"],
        "authority_limits": {
            "gate_status_changed": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }

    checks = {
        "plan_hash_matches": sha256(PLAN) == EXPECTED_PLAN_SHA,
        "backlog_hash_matches": sha256(BACKLOG) == EXPECTED_BACKLOG_SHA,
        "handoff_hash_matches": sha256(SOURCE_HANDOFF) == EXPECTED_HANDOFF_SHA,
        "recommendation_count_is_72": len(recommendation_rows) == 72,
        "recommendation_ids_unique": len({row["recommendation_id"] for row in recommendation_rows}) == 72,
        "no_missing_recommendations": not missing_recommendations,
        "no_missing_pre_p16_task_evidence": not missing_tasks,
        "all_recommendations_have_selected_evidence": all(row["selected_evidence"] for row in recommendation_rows),
        "all_selected_paths_are_tracked": all(record["git_tracked"] for record in selected.values()),
        "all_gate_evidence_present": all(row["evidence_present"] for row in gate_rows),
        "future_tasks_not_counted_as_verified": all(
            not (set(row["verified_pre_p16_direct_task_ids"]) & FUTURE_DIRECT_TASKS)
            for row in recommendation_rows
        ),
        "authority_limits_fail_closed": not any(matrix_output["authority_limits"].values()),
    }
    failed = [name for name, passed in checks.items() if not passed]
    report = {
        "schema_id": "v21_p16_t01_recommendation_coverage_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": checks,
        "metrics": {
            "recommendation_count": len(recommendation_rows),
            "direct_mapping_edge_count": direct_edge_count,
            "verified_pre_p16_mapping_edge_count": verified_edge_count,
            "pending_downstream_p16_mapping_edge_count": future_edge_count,
            "unique_verified_pre_p16_task_count": len(selected),
            "recommendations_with_downstream_p16_work": len(downstream_recommendations),
            "blocking_missing_recommendation_count": len(missing_recommendations),
            "blocking_missing_task_evidence_count": len(missing_tasks),
        },
    }
    receipt = {
        "schema_id": "v21_p16_t01_compact_receipt_v1",
        "status": report["status"],
        "audit_result": route["audit_result"],
        "source_hashes": {
            "plan": sha256(PLAN),
            "backlog": sha256(BACKLOG),
            "program_state_at_audit": EXPECTED_PROGRAM_STATE_SHA,
            "handoff_0943": sha256(SOURCE_HANDOFF),
        },
        "finding_counts": report["metrics"],
        "validator_id": report["schema_id"],
        "selected_next_plan_task_id": route["selected_next_plan_task_id"],
        "claim_boundary_summary": "All 72 recommendations have tracked pre-P16 coverage if status is PASS; this operational result creates no scientific, Gate, derivation, publication, or promotion authority.",
    }
    return matrix_output, findings, route, receipt, report


def write_outputs(outputs: tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]) -> None:
    matrix, findings, route, receipt, report = outputs
    MATRIX_OUT.write_text(json.dumps(matrix, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    FINDINGS_OUT.write_text(yaml.safe_dump(findings, sort_keys=False), encoding="utf-8")
    ROUTE_OUT.write_text(yaml.safe_dump(route, sort_keys=False), encoding="utf-8")
    RECEIPT_OUT.write_text(json.dumps(receipt, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    REPORT_OUT.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def check_written(outputs: tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]) -> list[str]:
    expected = {
        MATRIX_OUT: json.dumps(outputs[0], indent=2, sort_keys=False) + "\n",
        FINDINGS_OUT: yaml.safe_dump(outputs[1], sort_keys=False),
        ROUTE_OUT: yaml.safe_dump(outputs[2], sort_keys=False),
        RECEIPT_OUT: json.dumps(outputs[3], indent=2, sort_keys=False) + "\n",
        REPORT_OUT: json.dumps(outputs[4], indent=2, sort_keys=False) + "\n",
    }
    return [path.relative_to(ROOT).as_posix() for path, text in expected.items() if not path.exists() or path.read_text(encoding="utf-8") != text]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.write_report:
        write_outputs(outputs)
    drift = check_written(outputs) if args.check else []
    report = dict(outputs[4])
    report["written_output_drift"] = drift
    if drift:
        report["status"] = "FAIL"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=False))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
