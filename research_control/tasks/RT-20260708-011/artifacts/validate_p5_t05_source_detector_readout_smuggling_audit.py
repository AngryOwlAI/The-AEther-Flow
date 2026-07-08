#!/usr/bin/env python3
"""Validate v18 P5-T05 source detector/readout smuggling audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-011"
ARTIFACTS = TASK / "artifacts"
AUDIT = ARTIFACTS / "source_detector_readout_smuggling_audit_v1.tex"
COMPLETION = TASK / "jobs/completions/AJC-AJ-RT-20260708-011-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0704.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
TEX_REGISTRY = ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
REPORT = ARTIFACTS / "p5_t05_source_detector_readout_smuggling_audit_report.json"


REQUIRED_TEX_PHRASES = [
    "This artifact implements v18 P5-T05.",
    "SourceReadoutCandidate_EStar_v1",
    "source_detector_readout_smuggling_audit_result:",
    "result_type: \"source_pure_as_written\"",
    "empirical_detector_protocol_import: \"pass_absent\"",
    "empirical_calibration_import: \"pass_absent\"",
    "proper_time_import: \"pass_absent\"",
    "target_topology_import: \"pass_absent\"",
    "target_atlas_import: \"pass_absent\"",
    "target_metric_import: \"pass_absent\"",
    "benchmark_success_import: \"pass_absent\"",
    "stress_energy_semantics_import: \"pass_absent\"",
    "matter_action_import: \"pass_absent\"",
    "einstein_equation_premise_import: \"pass_absent\"",
    "process_authority_import: \"pass_absent\"",
    "candidate_as_adoption: \"pass_absent\"",
    "detector_readout_semantics_adopted: false",
    "Det_src_adopted: false",
    "Readout_src_adopted: false",
    "matter_coupling_derived: false",
    "selected_next_plan_task_id: \"P5-T06\"",
    "The Distance-to-GR ledger is unchanged",
]

FORBIDDEN_SUCCESS_STRINGS = [
    "detector_readout_semantics_adopted: true",
    "Det_src_adopted: true",
    "Readout_src_adopted: true",
    "source_law_adopted: true",
    "coupling_law_adopted: true",
    "matter_coupling_derived: true",
    "matter_coupling_adopted: true",
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
    for path in [AUDIT, COMPLETION, HANDOFF, PROGRAM_STATE, TEX_REGISTRY]:
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    text = AUDIT.read_text(encoding="utf-8") if AUDIT.exists() else ""
    for phrase in REQUIRED_TEX_PHRASES:
        if phrase not in text:
            failures.append(f"audit TeX missing phrase: {phrase}")

    lowered = text.lower()
    for snippet in FORBIDDEN_SUCCESS_STRINGS:
        if snippet.lower() in lowered:
            failures.append(f"audit TeX contains forbidden success string: {snippet}")

    completion = load_yaml(COMPLETION) if COMPLETION.exists() else {}
    if completion.get("plan_task_id") != "P5-T05":
        failures.append("completion plan_task_id must be P5-T05")
    if completion.get("objective_result") != "completed":
        failures.append("completion objective_result must be completed")
    result = completion.get("source_detector_readout_smuggling_audit_result", {})
    expected_result = {
        "result_type": "source_pure_as_written",
        "audited_candidate": "SourceReadoutCandidate_EStar_v1",
        "empirical_detector_protocol_import": "pass_absent",
        "proper_time_import": "pass_absent",
        "target_metric_import": "pass_absent",
        "benchmark_success_import": "pass_absent",
        "stress_energy_semantics_import": "pass_absent",
        "matter_action_import": "pass_absent",
        "process_authority_import": "pass_absent",
        "candidate_as_adoption": "pass_absent",
        "detector_readout_semantics_adopted": False,
        "matter_coupling_derived": False,
        "selected_next_plan_task_id": "P5-T06",
    }
    for key, expected in expected_result.items():
        if result.get(key) != expected:
            failures.append(f"audit_result.{key} expected {expected!r} got {result.get(key)!r}")
    if completion.get("distance_to_gr_delta", {}).get("changed") is not False:
        failures.append("completion distance_to_gr_delta.changed must be false")
    if completion.get("physics_promotion_authorized") is not False:
        failures.append("completion physics_promotion_authorized must be false")

    program_state = load_yaml(PROGRAM_STATE) if PROGRAM_STATE.exists() else {}
    if program_state.get("active_task_id") != "RT-20260708-011":
        failures.append("program_state active_task_id must be RT-20260708-011")
    if program_state.get("latest_handoff_id") != "handoff-0704":
        failures.append("program_state latest_handoff_id must be handoff-0704")

    handoff = load_yaml(HANDOFF) if HANDOFF.exists() else {}
    selected_next = handoff.get("selected_next_route", {})
    if selected_next.get("plan_task_id") != "P5-T06":
        failures.append("handoff selected_next_route.plan_task_id must be P5-T06")
    if selected_next.get("role_family") != "refuter@0.2.0":
        failures.append("handoff selected_next_route.role_family must be refuter@0.2.0")

    registry_text = TEX_REGISTRY.read_text(encoding="utf-8") if TEX_REGISTRY.exists() else ""
    if "TEX-V18-P5-T05-SOURCE-DETECTOR-READOUT-SMUGGLING-AUDIT-V1" not in registry_text:
        failures.append("TEX_SOURCE_REGISTRY missing P5-T05 audit row")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "plan_task_id": "P5-T05",
        "audit_result": "source_pure_as_written",
        "audited_candidate": "SourceReadoutCandidate_EStar_v1",
        "selected_next_plan_task_id": "P5-T06",
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
