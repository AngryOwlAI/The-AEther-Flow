#!/usr/bin/env python3
"""Validate the P14-T02 metrics interpretation artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260702-049"
RAW_METRICS = TASK_DIR / "artifacts/p14_t02_physics_progress_metrics_raw.json"
INTERPRETATION = TASK_DIR / "artifacts/p14_t02_physics_progress_metrics_interpretation.md"
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
LEDGER = ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"


EXPECTED = {
    "source_extension_evidence_accepted": 7,
    "source_extension_adopted": 9,
    "obstruction_records_created": 32,
    "precise_obstruction_count": 26,
    "route_frozen_count": 1,
    "freeze_reviews_triggered_by_repetition": 207,
    "candidate_construct_audit_stress_selector_cycles": 10,
    "construct_audit_stress_cycle_count": 37,
    "gate_chair_tasks": 30,
    "completion_validation_records": 637,
    "support_only_checker_reports": 2,
    "claim_boundary_rows_active": 598,
    "tasks_with_forbidden_conclusion_summary": 311,
    "remaining_open_gr_burden_classes": 8,
}


REQUIRED_PHRASES = [
    "AI-system diagnostic",
    "does not authorize physics claim promotion",
    "Scoped evidence/precondition results",
    "Adopted source-only or scoped source-extension object statuses",
    "Obstruction records created",
    "Frozen routes",
    "route cycles detected",
    "Gate Chair review tasks",
    "Completion validation records",
    "Support-only checker validation reports",
    "Active claim-boundary rows used by status/linter hygiene",
    "remaining open GR-burden classes",
    "Einstein-equation derivation",
    "exact-GR benchmark promotion",
    "P14-T03 current frontier final refresh",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    metrics = json.loads(RAW_METRICS.read_text())
    text = INTERPRETATION.read_text()

    physics_counts = metrics["metrics"]["physics_progress_metrics"]["physics_progress_status_counts"]
    physics_metrics = metrics["metrics"]["physics_progress_metrics"]
    route_metrics = metrics["metrics"]["route_orbit_risk_metrics"]
    workflow_metrics = metrics["metrics"]["agent_workflow_metrics"]
    validation_metrics = metrics["metrics"]["operational_validation_metrics"]
    claim_metrics = metrics["metrics"]["claim_hygiene_metrics"]

    observed = {
        "source_extension_evidence_accepted": physics_counts["source_extension_evidence_accepted"],
        "source_extension_adopted": physics_counts["source_extension_adopted"],
        "obstruction_records_created": physics_metrics["obstruction_records_created"],
        "precise_obstruction_count": physics_metrics["precise_obstruction_count"],
        "route_frozen_count": physics_metrics["route_frozen_count"],
        "freeze_reviews_triggered_by_repetition": route_metrics["freeze_reviews_triggered_by_repetition"],
        "candidate_construct_audit_stress_selector_cycles": route_metrics[
            "candidate_construct_audit_stress_selector_cycles"
        ],
        "construct_audit_stress_cycle_count": workflow_metrics["construct_audit_stress_cycle_count"],
        "gate_chair_tasks": validation_metrics["gate_chair_tasks"],
        "completion_validation_records": sum(validation_metrics["completion_validation_status_counts"].values()),
        "support_only_checker_reports": validation_metrics["support_only_checker_status_counts"]["pass_support_only"],
        "claim_boundary_rows_active": claim_metrics["claim_boundary_rows_active"],
        "tasks_with_forbidden_conclusion_summary": claim_metrics["tasks_with_forbidden_conclusion_summary"],
        "remaining_open_gr_burden_classes": len(
            re.findall(r"(?m)^[0-9]+\. ", text.split("## Interpretation", 1)[0])
        ),
    }

    for key, expected_value in EXPECTED.items():
        if observed.get(key) != expected_value:
            failures.append(f"{key}: expected {expected_value}, observed {observed.get(key)}")

    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            failures.append(f"missing required phrase: {phrase}")

    if metrics["authority_boundary"]["physics_claim_promotion_authorized"] is not False:
        failures.append("metrics authority boundary must keep physics_claim_promotion_authorized false")

    if "P14-T02: Physics-progress metrics report" not in PLAN.read_text():
        failures.append("v14 plan does not contain P14-T02 section")

    if "einstein_equations" not in LEDGER.read_text():
        failures.append("Distance-to-GR ledger inspection did not include einstein_equations row")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "observed": observed,
        "expected": EXPECTED,
        "source_hashes": {
            "raw_metrics": sha256(RAW_METRICS),
            "interpretation": sha256(INTERPRETATION),
            "plan": sha256(PLAN),
            "distance_to_gr_ledger": sha256(LEDGER),
        },
        "claim_boundary": {
            "metrics_are_operational": metrics["authority_boundary"]["metrics_are_operational"],
            "physics_claim_promotion_authorized": metrics["authority_boundary"][
                "physics_claim_promotion_authorized"
            ],
        },
    }

    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
