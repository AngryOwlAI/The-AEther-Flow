#!/usr/bin/env python3
"""Validate the v15 P10-T03 route-orbit freeze threshold policy artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
POLICY_PATH = REPO_ROOT / "research_control/design/route_orbit_freeze_threshold_policy_v1.md"
PILOT_REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260703-018/artifacts/p10_t02_route_signature_pilot_report.json"
)

REQUIRED_PHRASES = {
    "policy_id": "route_orbit_freeze_threshold_policy_v1",
    "three_task_window": "consecutive three-task window",
    "same_milestone": "target_derivation_milestone",
    "same_burden": "milestone_burden",
    "no_new_mathematics": "No task in the window has a new mathematical payload.",
    "countermodel_guard": "countermodel, finite witness, construction",
    "source_extension_guard": "source-extension classification",
    "validator_repair_guard": "validator failure requiring repair",
    "human_gate_guard": "protected human gate",
    "distance_delta_guard": "Distance-to-GR status",
    "legitimate_theorem_work": "Route Orbit Versus Legitimate Multi-Step Work",
    "global_no_go_guard": "None of these values implies a program-wide no-go conclusion",
    "pilot_consequence": "P10-T02 Pilot Consequence",
    "no_freeze_now": "Therefore P10-T03 does not freeze any route.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    if not POLICY_PATH.exists():
        errors.append(f"missing policy artifact: {POLICY_PATH.relative_to(REPO_ROOT)}")
        text = ""
    else:
        text = POLICY_PATH.read_text(encoding="utf-8")

    missing_phrases = [
        label for label, phrase in REQUIRED_PHRASES.items() if phrase not in text
    ]
    for label in missing_phrases:
        errors.append(f"policy missing required phrase: {label}")

    pilot = load_json(PILOT_REPORT_PATH)
    repeated_burden_count = int(pilot.get("repeated_burden_cycle_count", -1))
    repeated_no_new_payload_count = int(pilot.get("repeated_no_new_payload_cycle_count", -1))
    warning_should_emit = bool(pilot.get("route_orbit_warning_should_emit"))
    pilot_blocks_research = bool(pilot.get("pilot_blocks_research"))

    threshold_window_size = 3
    p10_t02_threshold_met = (
        repeated_burden_count >= threshold_window_size
        and repeated_no_new_payload_count >= 1
        and warning_should_emit
    )

    if repeated_burden_count != 2:
        errors.append("P10-T02 pilot repeated_burden_cycle_count must remain 2")
    if repeated_no_new_payload_count != 0:
        errors.append("P10-T02 pilot repeated_no_new_payload_cycle_count must remain 0")
    if warning_should_emit:
        errors.append("P10-T02 pilot must not emit route-orbit warning")
    if pilot_blocks_research:
        errors.append("P10-T02 pilot must remain non-blocking")
    if p10_t02_threshold_met:
        errors.append("P10-T02 pilot must not meet P10-T03 threshold")

    report = {
        "schema_id": "p10_t03_route_orbit_freeze_threshold_policy_validation_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "policy_path": POLICY_PATH.relative_to(REPO_ROOT).as_posix(),
        "policy_hash": sha256(POLICY_PATH) if POLICY_PATH.exists() else "",
        "pilot_report_path": PILOT_REPORT_PATH.relative_to(REPO_ROOT).as_posix(),
        "pilot_report_hash": sha256(PILOT_REPORT_PATH),
        "threshold_window_size": threshold_window_size,
        "required_policy_phrases_checked": sorted(REQUIRED_PHRASES),
        "missing_policy_phrases": missing_phrases,
        "p10_t02_pilot_evaluation": {
            "repeated_burden_cycle_count": repeated_burden_count,
            "repeated_no_new_payload_cycle_count": repeated_no_new_payload_count,
            "route_orbit_warning_should_emit": warning_should_emit,
            "pilot_blocks_research": pilot_blocks_research,
            "threshold_met": p10_t02_threshold_met,
            "decision": "evaluated_no_freeze",
        },
        "claim_boundary": {
            "route_freeze_triggered": False,
            "physics_promotion_authorized": False,
            "global_no_go_claim_authorized": False,
            "future_source_extension_impossibility_authorized": False,
        },
    }
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write JSON validation report.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif report["status"] == "PASS":
        print("P10-T03 route-orbit freeze threshold policy validation passed.")
    else:
        print("P10-T03 route-orbit freeze threshold policy validation failed.")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
