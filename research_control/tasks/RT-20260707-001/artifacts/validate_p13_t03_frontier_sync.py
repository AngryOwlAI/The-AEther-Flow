#!/usr/bin/env python3
"""Validate the v17 P13-T03 frontier and ledger synchronization receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_PATH = REPO_ROOT / "research_control/tasks/RT-20260707-001/artifacts/v17_current_frontier_ledger_sync_report.json"


EXPECTED = {
    "task_id": "RT-20260707-001",
    "job_id": "AJ-RT-20260707-001-001",
    "plan_task_id": "P13-T03",
    "next_plan_task_id": "P13-T04",
    "latest_handoff_id": "handoff-0671",
    "active_task_id": "RT-20260707-001",
    "distance_to_gr_ledger_sha256": "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61",
    "metric_use_ledger_sha256": "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf",
}

HASH_FIELDS = {
    "current_frontier_md_sha256": "research_control/current_frontier.md",
    "compact_frontier_yaml_sha256": "output/compact_current_frontier_v16.yaml",
    "compact_frontier_json_sha256": "output/compact_current_frontier_v16.json",
    "claim_graph_json_sha256": "output/claim_graph_v1.json",
    "dependency_graph_json_sha256": "output/research_dependency_graph.json",
    "dependency_graph_dot_sha256": "output/research_dependency_graph.dot",
    "dependency_graph_markdown_sha256": "wiki/indexes/research_dependency_graph.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def validate() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    require(REPORT_PATH.exists(), errors, f"missing report: {REPORT_PATH.relative_to(REPO_ROOT)}")
    report = read_json(REPORT_PATH) if REPORT_PATH.exists() else {}

    require(report.get("schema_id") == "v17_current_frontier_ledger_sync_report_v1", errors, "unexpected schema_id")
    require(report.get("task_id") == EXPECTED["task_id"], errors, "unexpected task_id")
    require(report.get("job_id") == EXPECTED["job_id"], errors, "unexpected job_id")
    require(report.get("plan_task_id") == EXPECTED["plan_task_id"], errors, "unexpected plan_task_id")
    require(report.get("aggregate_status") == "PASS", errors, "aggregate_status must be PASS")
    require(report.get("operational_receipt_only") is True, errors, "report must be operational receipt only")
    require(report.get("proof_authority") is False, errors, "report must not claim proof authority")
    require(report.get("physics_promotion_authorized") is False, errors, "report must not authorize physics promotion")

    receipt = report.get("implementation_plan_receipt", {})
    require(receipt.get("selected_next_plan_task_id") == EXPECTED["next_plan_task_id"], errors, "next plan task must be P13-T04")
    require(receipt.get("implemented_v17_plan_tasks_after_completion") == 56, errors, "implemented task count must be 56")
    require(receipt.get("deferred_v17_plan_tasks_after_completion") == ["P13-T04"], errors, "only P13-T04 may remain deferred")
    require(receipt.get("phase_p13_completed") is False, errors, "P13 must remain incomplete until P13-T04")
    require(receipt.get("all_applicable_plan_tasks_proven") is False, errors, "all plan tasks must not be claimed complete in P13-T03")

    ledger = report.get("ledger_integrity", {})
    require(ledger.get("distance_to_gr_ledger_before_sha256") == EXPECTED["distance_to_gr_ledger_sha256"], errors, "unexpected Distance-to-GR before hash")
    require(ledger.get("distance_to_gr_ledger_after_sha256") == EXPECTED["distance_to_gr_ledger_sha256"], errors, "unexpected Distance-to-GR after hash")
    require(ledger.get("metric_use_ledger_before_sha256") == EXPECTED["metric_use_ledger_sha256"], errors, "unexpected metric-use before hash")
    require(ledger.get("metric_use_ledger_after_sha256") == EXPECTED["metric_use_ledger_sha256"], errors, "unexpected metric-use after hash")
    require(ledger.get("distance_to_gr_status_changed") is False, errors, "Distance-to-GR status must be unchanged")
    require(ledger.get("metric_use_status_changed") is False, errors, "metric-use status must be unchanged")
    require(ledger.get("protected_authority_for_status_change") is False, errors, "P13-T03 must not claim protected authority for ledger status change")

    require(sha256(REPO_ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv") == EXPECTED["distance_to_gr_ledger_sha256"], errors, "live Distance-to-GR ledger hash changed")
    require(sha256(REPO_ROOT / "registries/METRIC_USE_LEDGER.csv") == EXPECTED["metric_use_ledger_sha256"], errors, "live metric-use ledger hash changed")

    surface_hashes = report.get("surface_hashes", {})
    for field, rel_path in HASH_FIELDS.items():
        path = REPO_ROOT / rel_path
        require(path.exists(), errors, f"missing synchronized surface: {rel_path}")
        if path.exists():
            require(surface_hashes.get(field) == sha256(path), errors, f"stale report hash for {rel_path}")

    done = report.get("done_criteria", [])
    require(len(done) == 5, errors, "expected five P13-T03 done criteria")
    for item in done:
        require(item.get("status") == "PASS", errors, f"done criterion not PASS: {item.get('criterion')}")

    program_state = (REPO_ROOT / "research_control/program_state.yaml").read_text(encoding="utf-8")
    require(f'active_task_id: "{EXPECTED["active_task_id"]}"' in program_state, errors, "program_state active task mismatch")
    require(f'latest_handoff_id: "{EXPECTED["latest_handoff_id"]}"' in program_state, errors, "program_state latest handoff mismatch")

    current_frontier = (REPO_ROOT / "research_control/current_frontier.md").read_text(encoding="utf-8")
    require(EXPECTED["latest_handoff_id"] in current_frontier, errors, "current frontier does not name handoff-0671")
    require("P13-T04" in current_frontier, errors, "current frontier does not route to P13-T04")

    handoff = (REPO_ROOT / "research_control/handoffs/handoff-0671.yaml").read_text(encoding="utf-8")
    require('selected_next_plan_task_id: "P13-T04"' in handoff, errors, "handoff does not select P13-T04")
    require('completed_plan_task_id: "P13-T03"' in handoff, errors, "handoff does not complete P13-T03")

    status = "PASS" if not errors else "FAIL"
    return {
        "schema_id": "v17_p13_t03_frontier_sync_validation_report_v1",
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "checked_failure_modes": [
            "report_missing_or_wrong_schema",
            "wrong_task_or_job",
            "aggregate_status_not_pass",
            "ledger_hash_changed",
            "ledger_status_changed_without_authority",
            "surface_hash_stale",
            "current_frontier_not_synced_to_handoff",
            "handoff_not_routing_p13_t04",
            "premature_all_tasks_complete_claim"
        ],
        "ledger_hashes": {
            "distance_to_gr": sha256(REPO_ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"),
            "metric_use": sha256(REPO_ROOT / "registries/METRIC_USE_LEDGER.csv"),
        },
        "surface_hashes": {field: sha256(REPO_ROOT / rel_path) for field, rel_path in HASH_FIELDS.items() if (REPO_ROOT / rel_path).exists()},
        "next_plan_task_id": report.get("implementation_plan_receipt", {}).get("selected_next_plan_task_id"),
        "operational_receipt_only": report.get("operational_receipt_only"),
        "physics_proof_authority": report.get("proof_authority"),
        "physics_promotion_authorized": report.get("physics_promotion_authorized"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args()
    result = validate()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
