#!/usr/bin/env python3
"""Validate the v18 recommendation backlog materialized by RT-20260707-005."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v18.md"
BACKLOG = ROOT / "research_control/design/v18_recommendation_backlog.yaml"
REPORT = ROOT / "research_control/tasks/RT-20260707-005/artifacts/v18_backlog_validation.json"
EXPECTED_RECS = [f"V18-R{i:02d}" for i in range(1, 11)]
REQUIRED_FIELDS = {
    "plan_task_id",
    "phase_id",
    "title",
    "recommendation_ids",
    "depends_on",
    "role_family",
    "task_type",
    "target_derivation_milestone",
    "milestone_burden",
    "expected_outputs",
    "required_validators",
    "physics_delta_allowed",
    "promotion_allowed",
    "human_gate_required",
    "next_route_on_success",
    "next_route_on_failure",
}


def main() -> int:
    plan_text = PLAN.read_text()
    plan_tasks = re.findall(r"^### (P\d+-T\d+):\s*(.+)$", plan_text, re.M)
    plan_ids = [task_id for task_id, _ in plan_tasks]
    data = yaml.safe_load(BACKLOG.read_text())
    items = data.get("items", [])
    ids = [item.get("plan_task_id") for item in items]
    id_to_index = {task_id: idx for idx, task_id in enumerate(ids)}
    errors = []

    if data.get("authority") != "project_control":
        errors.append("backlog authority is not project_control")
    if data.get("scope", {}).get("task_count") != len(plan_ids):
        errors.append("scope task_count does not match plan heading count")
    if len(items) != len(plan_ids):
        errors.append(f"item count {len(items)} does not match plan count {len(plan_ids)}")
    if Counter(ids) != Counter(plan_ids):
        missing = sorted(set(plan_ids) - set(ids))
        extra = sorted(set(ids) - set(plan_ids))
        duplicates = sorted(task_id for task_id, count in Counter(ids).items() if count > 1)
        errors.append({"plan_id_mismatch": {"missing": missing, "extra": extra, "duplicates": duplicates}})

    for item in items:
        missing_fields = sorted(REQUIRED_FIELDS - set(item))
        if missing_fields:
            errors.append({item.get("plan_task_id", "unknown"): {"missing_fields": missing_fields}})
        if item.get("promotion_allowed") is not False:
            errors.append({item.get("plan_task_id"): "promotion_allowed must be false"})
        if not isinstance(item.get("human_gate_required"), bool):
            errors.append({item.get("plan_task_id"): "human_gate_required must be boolean"})
        if not item.get("expected_outputs"):
            errors.append({item.get("plan_task_id"): "expected_outputs must be nonempty"})
        if not item.get("required_validators"):
            errors.append({item.get("plan_task_id"): "required_validators must be nonempty"})
        if item.get("physics_delta_allowed") is False and item.get("project_system_boundary_authorized_by_plan") is not True:
            errors.append({item.get("plan_task_id"): "project-system/no-delta task lacks project_system_boundary_authorized_by_plan"})
        for dep in item.get("depends_on", []):
            if dep not in id_to_index:
                errors.append({item.get("plan_task_id"): f"unknown dependency {dep}"})
            elif id_to_index[dep] >= id_to_index[item["plan_task_id"]]:
                errors.append({item.get("plan_task_id"): f"dependency {dep} is not earlier"})

    if items and items[0].get("depends_on") != []:
        errors.append("first task must have no dependencies")
    p0_t02 = next((item for item in items if item.get("plan_task_id") == "P0-T02"), None)
    if not p0_t02 or p0_t02.get("depends_on") != ["P0-T01"]:
        errors.append("P0-T02 must depend on P0-T01")
    if not p0_t02 or p0_t02.get("next_route_on_success") != "P0-T03":
        errors.append("P0-T02 next route must be P0-T03")

    first_physics = next((item.get("plan_task_id") for item in items if item.get("physics_delta_allowed") is True), None)
    if first_physics != "P2-T01":
        errors.append(f"first physics-bearing task after P0 must be P2-T01, got {first_physics}")

    direct_by_rec = defaultdict(list)
    final_by_rec = defaultdict(list)
    for item in items:
        for rec in item.get("recommendation_ids", []):
            if item.get("recommendation_coverage_role") == "direct_implementation":
                direct_by_rec[rec].append(item["plan_task_id"])
            if item.get("recommendation_coverage_role") == "final_coverage_audit":
                final_by_rec[rec].append(item["plan_task_id"])
    for rec in EXPECTED_RECS:
        if not direct_by_rec[rec]:
            errors.append({rec: "missing direct implementation task"})
        if final_by_rec[rec] != ["P11-T05"]:
            errors.append({rec: f"final coverage audit should be P11-T05, got {final_by_rec[rec]}"})

    report = {
        "status": "PASS" if not errors else "FAIL",
        "plan_task_count": len(plan_ids),
        "backlog_item_count": len(items),
        "first_physics_bearing_task_after_p0": first_physics,
        "dependencies_acyclic": not any(isinstance(e, dict) and "dependency" in str(e) for e in errors),
        "promotion_allowed_true_items": [item["plan_task_id"] for item in items if item.get("promotion_allowed") is not False],
        "project_system_boundary_authorized_by_plan_checked": True,
        "recommendation_direct_coverage": {rec: direct_by_rec[rec] for rec in EXPECTED_RECS},
        "recommendation_final_audit_coverage": {rec: final_by_rec[rec] for rec in EXPECTED_RECS},
        "next_route_after_p0_t02": p0_t02.get("next_route_on_success") if p0_t02 else None,
        "errors": errors,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
