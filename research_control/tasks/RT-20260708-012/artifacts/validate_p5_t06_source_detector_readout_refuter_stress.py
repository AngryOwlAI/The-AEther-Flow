#!/usr/bin/env python3
"""Validate v18 P5-T06 source detector/readout Refuter stress."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-012"
ARTIFACTS = TASK / "artifacts"
STRESS = ARTIFACTS / "source_detector_readout_refuter_stress_v1.tex"
COMPLETION = TASK / "jobs/completions/AJC-AJ-RT-20260708-012-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0705.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
TEX_REGISTRY = ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
REPORT = ARTIFACTS / "p5_t06_source_detector_readout_refuter_stress_report.json"


REQUIRED_TEX_PHRASES = [
    "This artifact implements v18 P5-T06.",
    "SourceReadoutCandidate_EStar_v1",
    "source_detector_readout_refuter_stress_result:",
    "result_type: \"survives_as_draft_control_candidate\"",
    "bridge_or_fail_category: \"bridge_facing_candidate_path\"",
    "readout_interface_erasure: \"live_obligation\"",
    "source_record_removal: \"fail_closed\"",
    "empirical_detector_protocol_substitution: \"fail_closed\"",
    "proper_time_substitution: \"fail_closed\"",
    "target_metric_substitution: \"fail_closed\"",
    "benchmark_behavior_substitution: \"fail_closed\"",
    "finite_local_witness_perturbation: \"stress_pass\"",
    "K_Estar_compatibility_failure: \"live_obligation\"",
    "placeholder_as_adoption_laundering: \"blocked\"",
    "process_authority_pressure: \"blocked\"",
    "detector_readout_semantics_adopted: false",
    "Det_src_adopted: false",
    "Readout_src_adopted: false",
    "matter_coupling_derived: false",
    "selected_next_plan_task_id: \"P5-T07\"",
    "The Refuter category is:",
]

FORBIDDEN_SUCCESS_STRINGS = [
    "detector_readout_semantics_adopted: true",
    "Det_src_adopted: true",
    "Readout_src_adopted: true",
    "source_law_adopted: true",
    "coupling_law_adopted: true",
    "matter_coupling_derived: true",
    "matter_coupling_adopted: true",
    "einstein_equations_derived: true",
    "benchmark_promoted: true",
    "completed_derivation_claimed: true",
]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    for path in [STRESS, COMPLETION, HANDOFF, PROGRAM_STATE, TEX_REGISTRY]:
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    text = STRESS.read_text(encoding="utf-8") if STRESS.exists() else ""
    for phrase in REQUIRED_TEX_PHRASES:
        if phrase not in text:
            failures.append(f"stress TeX missing phrase: {phrase}")

    lowered = text.lower()
    for snippet in FORBIDDEN_SUCCESS_STRINGS:
        if snippet.lower() in lowered:
            failures.append(f"stress TeX contains forbidden success string: {snippet}")

    completion = load_yaml(COMPLETION) if COMPLETION.exists() else {}
    if completion.get("plan_task_id") != "P5-T06":
        failures.append("completion plan_task_id must be P5-T06")
    if completion.get("objective_result") != "completed":
        failures.append("completion objective_result must be completed")
    result = completion.get("source_detector_readout_refuter_stress_result", {})
    expected_result = {
        "result_type": "survives_as_draft_control_candidate",
        "bridge_or_fail_category": "bridge_facing_candidate_path",
        "stressed_candidate": "SourceReadoutCandidate_EStar_v1",
        "source_record_removal": "fail_closed",
        "empirical_detector_protocol_substitution": "fail_closed",
        "proper_time_substitution": "fail_closed",
        "target_metric_substitution": "fail_closed",
        "benchmark_behavior_substitution": "fail_closed",
        "finite_local_witness_perturbation": "stress_pass",
        "K_Estar_compatibility_failure": "live_obligation",
        "placeholder_as_adoption_laundering": "blocked",
        "process_authority_pressure": "blocked",
        "detector_readout_semantics_adopted": False,
        "matter_coupling_derived": False,
        "selected_next_plan_task_id": "P5-T07",
    }
    for key, expected in expected_result.items():
        if result.get(key) != expected:
            failures.append(f"stress_result.{key} expected {expected!r} got {result.get(key)!r}")
    if completion.get("loop_risk_decision", {}).get("category") != "bridge_facing_candidate_path":
        failures.append("completion loop_risk_decision.category must be bridge_facing_candidate_path")
    if completion.get("freeze_criteria_status", {}).get("freeze_decision") != "not_frozen":
        failures.append("completion freeze_criteria_status.freeze_decision must be not_frozen")
    if completion.get("distance_to_gr_delta", {}).get("changed") is not False:
        failures.append("completion distance_to_gr_delta.changed must be false")
    if completion.get("physics_promotion_authorized") is not False:
        failures.append("completion physics_promotion_authorized must be false")

    program_state = load_yaml(PROGRAM_STATE) if PROGRAM_STATE.exists() else {}
    if program_state.get("active_task_id") != "RT-20260708-012":
        failures.append("program_state active_task_id must be RT-20260708-012")
    if program_state.get("latest_handoff_id") != "handoff-0705":
        failures.append("program_state latest_handoff_id must be handoff-0705")

    handoff = load_yaml(HANDOFF) if HANDOFF.exists() else {}
    selected_next = handoff.get("selected_next_route", {})
    if selected_next.get("plan_task_id") != "P5-T07":
        failures.append("handoff selected_next_route.plan_task_id must be P5-T07")
    if selected_next.get("role_family") != "theoretical-continuation-selector@0.1.0":
        failures.append(
            "handoff selected_next_route.role_family must be theoretical-continuation-selector@0.1.0"
        )

    registry_text = TEX_REGISTRY.read_text(encoding="utf-8") if TEX_REGISTRY.exists() else ""
    if "TEX-V18-P5-T06-SOURCE-DETECTOR-READOUT-REFUTER-STRESS-V1" not in registry_text:
        failures.append("TEX_SOURCE_REGISTRY missing P5-T06 stress row")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "plan_task_id": "P5-T06",
        "stress_result": "survives_as_draft_control_candidate",
        "bridge_or_fail_category": "bridge_facing_candidate_path",
        "stressed_candidate": "SourceReadoutCandidate_EStar_v1",
        "selected_next_plan_task_id": "P5-T07",
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
