#!/usr/bin/env python3
"""Validate v18 P5-T02 source detector/readout DAG and ledger question setup."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-008"
ARTIFACTS = TASK / "artifacts"
QUESTION = ARTIFACTS / "source_detector_readout_ledger_delta_question_v1.yaml"
PATCH = ARTIFACTS / "source_detector_readout_dag_patch_proposal_v1.md"
RECEIPT = ARTIFACTS / "source_detector_readout_dag_ledger_question_receipt.md"
COMPLETION = TASK / "jobs/completions/AJC-AJ-RT-20260708-008-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0701.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
DAG = ROOT / "research_control/design/matter_coupling_dependency_dag_v1.md"
LEDGER = ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"
REPORT = ARTIFACTS / "p5_t02_source_detector_readout_dag_ledger_question_report.json"

EXPECTED_DAG_HASH = "8cca047480ae21c3b0641a5221277ae43cd5fdf1eb688a9080a168e27b1e98c3"
EXPECTED_LEDGER_HASH = "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    for path in [QUESTION, PATCH, RECEIPT, COMPLETION, HANDOFF, PROGRAM_STATE]:
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    question = load_yaml(QUESTION) if QUESTION.exists() else {}
    ledger_question = question.get("ledger_delta_question", {})
    expected_fields = {
        "proposed_burden_id": "source_detector_readout_semantics",
        "proposed_status": "proposal_burden_only",
        "proposed_control_status": "burden_proposed_not_adopted",
        "proposed_mathematical_status": "readout_law_missing",
        "proposed_physical_status": "not_detector_semantics_not_matter_coupling",
        "promotion_status": "none",
        "requires_protected_authority_to_update_ledger": True,
        "update_performed_in_this_task": False,
    }
    for key, expected in expected_fields.items():
        if ledger_question.get(key) != expected:
            failures.append(f"ledger_delta_question.{key} expected {expected!r} got {ledger_question.get(key)!r}")

    if question.get("distance_to_gr_delta", {}).get("changed") is not False:
        failures.append("distance_to_gr_delta.changed must be false")
    if question.get("distance_to_gr_delta", {}).get("ledger_row_updated") is not False:
        failures.append("distance_to_gr_delta.ledger_row_updated must be false")
    if question.get("decision_result", {}).get("selected_next_plan_task_id") != "P5-T03":
        failures.append("selected next plan task must be P5-T03")

    patch_text = PATCH.read_text(encoding="utf-8") if PATCH.exists() else ""
    for phrase in [
        "patch proposal only",
        "No populated DAG edit is performed in P5-T02.",
        "No Distance-to-GR ledger update is performed in P5-T02.",
        "source_detector_readout_semantics",
        "P5-T03",
    ]:
        if phrase not in patch_text:
            failures.append(f"patch proposal missing phrase: {phrase}")

    if sha256(DAG) != EXPECTED_DAG_HASH:
        failures.append("matter-coupling DAG hash changed; P5-T02 may not edit it")
    if sha256(LEDGER) != EXPECTED_LEDGER_HASH:
        failures.append("Distance-to-GR ledger hash changed; P5-T02 may not edit it")

    if "mc_source_detector_readout_semantics_burden" in DAG.read_text(encoding="utf-8"):
        failures.append("proposal node appears in canonical DAG; P5-T02 must not apply it")

    ledger_rows = list(csv.DictReader(LEDGER.open(newline="", encoding="utf-8")))
    if any(row.get("burden_id") == "source_detector_readout_semantics" for row in ledger_rows):
        failures.append("source_detector_readout_semantics row appears in Distance-to-GR ledger")

    completion = load_yaml(COMPLETION) if COMPLETION.exists() else {}
    if completion.get("objective_result") != "completed":
        failures.append("completion objective_result must be completed")
    if completion.get("distance_to_gr_delta", {}).get("ledger_row_updated") is not False:
        failures.append("completion must record no ledger update")
    if completion.get("selector_result", {}).get("selected_next_plan_task_id") != "P5-T03":
        failures.append("completion selector_result must route to P5-T03")

    program_state = load_yaml(PROGRAM_STATE) if PROGRAM_STATE.exists() else {}
    if program_state.get("active_task_id") != "RT-20260708-008":
        failures.append("program_state active_task_id must be RT-20260708-008")
    if program_state.get("latest_handoff_id") != "handoff-0701":
        failures.append("program_state latest_handoff_id must be handoff-0701")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "plan_task_id": "P5-T02",
        "selected_next_plan_task_id": "P5-T03",
        "ledger_row_updated": False,
        "dag_updated": False,
        "physics_promotion_authorized": False,
        "dag_hash": sha256(DAG),
        "ledger_hash": sha256(LEDGER),
    }

    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
