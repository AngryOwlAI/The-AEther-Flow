#!/usr/bin/env python3
"""Validate v18 P5-T03 source detector/readout candidate setup."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-009"
ARTIFACTS = TASK / "artifacts"
SETUP = ARTIFACTS / "source_detector_readout_candidate_setup_v1.md"
COMPLETION = TASK / "jobs/completions/AJC-AJ-RT-20260708-009-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0702.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
REPORT = ARTIFACTS / "p5_t03_source_detector_readout_candidate_setup_report.json"


EXPECTED_SETUP = {
    "candidate_name": "SourceReadoutCandidate_EStar_v1",
    "source_domain": "SMScope(E_*)",
    "readout_symbol": "Readout_src(E_*)",
    "detector_symbol": "Det_src(E_*)",
    "compatibility_target": "SourceCouplingLawCandidate_EStar_v1",
    "finite_local_witness_required": True,
    "empirical_protocol_import_forbidden": True,
    "proper_time_import_forbidden": True,
    "target_metric_import_forbidden": True,
    "adoption_requested": False,
}

FORBIDDEN_PROMOTION_SNIPPETS = [
    "Det_src adopted",
    "Readout_src adopted",
    "detector semantics adopted",
    "matter coupling derived",
    "Einstein equations derived",
    "benchmark promoted",
    "completed derivation achieved",
]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def extract_yaml_block(text: str, block_key: str) -> dict:
    for match in re.finditer(r"```yaml\n(.*?)\n```", text, re.DOTALL):
        data = yaml.safe_load(match.group(1)) or {}
        if isinstance(data, dict) and block_key in data:
            return data
    return {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    for path in [SETUP, COMPLETION, HANDOFF, PROGRAM_STATE]:
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    setup_text = SETUP.read_text(encoding="utf-8") if SETUP.exists() else ""
    setup_block = extract_yaml_block(setup_text, "source_detector_readout_candidate_setup")
    setup = setup_block.get("source_detector_readout_candidate_setup", {})
    for key, expected in EXPECTED_SETUP.items():
        if setup.get(key) != expected:
            failures.append(f"source_detector_readout_candidate_setup.{key} expected {expected!r} got {setup.get(key)!r}")

    branch_block = extract_yaml_block(setup_text, "branch_selection")
    branch = branch_block.get("branch_selection", {})
    if branch.get("exactly_one_branch_named") is not True:
        failures.append("branch_selection.exactly_one_branch_named must be true")
    if branch.get("branch_type") != "candidate_target":
        failures.append("branch_selection.branch_type must be candidate_target")
    if branch.get("branch_name") != "SourceReadoutCandidate_EStar_v1":
        failures.append("branch_selection.branch_name must be SourceReadoutCandidate_EStar_v1")
    if branch.get("obstruction_branch_named") is not False:
        failures.append("branch_selection.obstruction_branch_named must be false")
    if branch.get("next_plan_task_id") != "P5-T04":
        failures.append("branch_selection.next_plan_task_id must be P5-T04")

    required_phrases = [
        "This artifact completes v18 P5-T03.",
        "It is not a constructed readout law",
        "P5-T04",
        "finite/local witness",
        "SourceCouplingLawCandidate_EStar_v1",
        "empirical detector protocol authority",
        "proper-time normalization",
        "target metric structure",
    ]
    for phrase in required_phrases:
        if phrase not in setup_text:
            failures.append(f"setup artifact missing phrase: {phrase}")

    for snippet in FORBIDDEN_PROMOTION_SNIPPETS:
        if snippet in setup_text:
            failures.append(f"setup artifact contains forbidden promotion snippet: {snippet}")

    completion = load_yaml(COMPLETION) if COMPLETION.exists() else {}
    if completion.get("plan_task_id") != "P5-T03":
        failures.append("completion plan_task_id must be P5-T03")
    if completion.get("candidate_setup_result", {}).get("selected_next_plan_task_id") != "P5-T04":
        failures.append("completion candidate_setup_result must route to P5-T04")
    if completion.get("distance_to_gr_delta", {}).get("changed") is not False:
        failures.append("completion distance_to_gr_delta.changed must be false")
    if completion.get("candidate_setup_result", {}).get("adoption_requested") is not False:
        failures.append("completion adoption_requested must be false")

    program_state = load_yaml(PROGRAM_STATE) if PROGRAM_STATE.exists() else {}
    if program_state.get("active_task_id") != "RT-20260708-009":
        failures.append("program_state active_task_id must be RT-20260708-009")
    if program_state.get("latest_handoff_id") != "handoff-0702":
        failures.append("program_state latest_handoff_id must be handoff-0702")

    handoff = load_yaml(HANDOFF) if HANDOFF.exists() else {}
    selected_next = handoff.get("selected_next_route", {})
    if selected_next.get("plan_task_id") != "P5-T04":
        failures.append("handoff selected_next_route.plan_task_id must be P5-T04")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "plan_task_id": "P5-T03",
        "candidate_name": "SourceReadoutCandidate_EStar_v1",
        "exactly_one_branch_named": True,
        "selected_next_plan_task_id": "P5-T04",
        "adoption_requested": False,
        "ledger_row_updated": False,
        "physics_promotion_authorized": False,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
