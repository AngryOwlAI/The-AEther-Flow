#!/usr/bin/env python3
"""Validate the v17 P13-T02 final validation report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_LAYERS = {
    "memory_preflight",
    "memory_bootstrap",
    "research_control_validation",
    "diff_validation",
    "claim_language_linter",
    "accepted_calibration_advisory_report",
    "documentation_impact_validation",
    "registry_consistency",
    "current_frontier_render_check",
    "compact_frontier_render_check",
    "dependency_graph_check",
    "claim_graph_validation",
    "task_index_validation",
    "metric_use_ledger_validation",
    "proof_normal_form_validation",
    "support_only_formalization_validation",
    "unit_tests",
    "ci_workflow_syntax_check_where_available",
}

PASS_STATUSES = {"PASS", "PASS_WITH_ADVISORY"}


def load_report(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(report: dict[str, Any], report_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    expected_fields = {
        "schema_id": "v17_final_validation_report_v1",
        "task_id": "RT-20260706-038",
        "job_id": "AJ-RT-20260706-038-001",
        "plan_task_id": "P13-T02",
        "aggregate_status": "PASS",
    }
    for field, expected in expected_fields.items():
        if report.get(field) != expected:
            errors.append(f"{field} must be {expected!r}")

    if report.get("operational_receipt_only") is not True:
        errors.append("operational_receipt_only must be true")
    for flag in (
        "proof_authority",
        "physics_promotion_authorized",
        "validators_as_physics_proof",
    ):
        if report.get(flag) is not False:
            errors.append(f"{flag} must be false")

    delta = report.get("v17_distance_to_gr_delta", {})
    if delta.get("effect") != "no_distance_delta":
        errors.append("v17_distance_to_gr_delta.effect must be no_distance_delta")
    if delta.get("changed") is not False:
        errors.append("v17_distance_to_gr_delta.changed must be false")

    receipt = report.get("implementation_plan_receipt", {})
    if receipt.get("implemented_v17_plan_tasks_after_completion") != 55:
        errors.append("implemented_v17_plan_tasks_after_completion must be 55")
    if receipt.get("deferred_v17_plan_tasks_after_completion") != ["P13-T03", "P13-T04"]:
        errors.append("deferred_v17_plan_tasks_after_completion must be P13-T03 and P13-T04")
    if receipt.get("selected_next_plan_task_id") != "P13-T03":
        errors.append("selected_next_plan_task_id must be P13-T03")
    if receipt.get("phase_p13_completed") is not False:
        errors.append("phase_p13_completed must remain false after P13-T02")
    if receipt.get("all_applicable_plan_tasks_proven") is not False:
        errors.append("all_applicable_plan_tasks_proven must remain false after P13-T02")

    statuses = {
        str(layer.get("layer_id")): str(layer.get("status"))
        for layer in report.get("layer_statuses", [])
        if isinstance(layer, dict)
    }
    missing = sorted(REQUIRED_LAYERS - set(statuses))
    if missing:
        errors.append("missing required layers: " + ", ".join(missing))
    for layer_id in sorted(REQUIRED_LAYERS & set(statuses)):
        if statuses[layer_id] not in PASS_STATUSES:
            errors.append(f"{layer_id} status must be PASS or PASS_WITH_ADVISORY")

    pending_layers = report.get("pending_layers")
    if pending_layers != []:
        errors.append("pending_layers must be an empty list")

    next_route = report.get("next_route", {})
    if next_route.get("plan_task_id") != "P13-T03":
        errors.append("next_route.plan_task_id must be P13-T03")

    hard_blocks = " ".join(str(item) for item in report.get("hard_blocks_preserved", []))
    for required in (
        "source-law adoption",
        "matter-coupling derivation or adoption",
        "Einstein equations",
        "Gate Chair verdict",
        "completed derivation",
    ):
        if required not in hard_blocks:
            errors.append(f"hard_blocks_preserved missing {required}")

    if report_path.name != "v17_final_validation_report.json":
        warnings.append("non-default report path used")

    return {
        "schema_id": "p13_t02_final_validation_report_validator_v1",
        "report_path": str(report_path),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checked_layer_count": len(statuses),
        "required_layer_count": len(REQUIRED_LAYERS),
        "pending_layer_count": len(pending_layers or []),
        "aggregate_status": report.get("aggregate_status"),
        "next_plan_task_id": next_route.get("plan_task_id"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        default="research_control/tasks/RT-20260706-038/artifacts/v17_final_validation_report.json",
        help="Report JSON path to validate.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON receipt.")
    args = parser.parse_args()

    path = Path(args.report)
    receipt = validate(load_report(path), path)
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(f"status={receipt['status']}")
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
