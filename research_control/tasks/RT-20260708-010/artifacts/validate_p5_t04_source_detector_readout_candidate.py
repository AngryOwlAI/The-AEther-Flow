#!/usr/bin/env python3
"""Validate v18 P5-T04 source detector/readout candidate construction."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-010"
ARTIFACTS = TASK / "artifacts"
CANDIDATE = ARTIFACTS / "source_detector_readout_candidate_v1.tex"
COMPLETION = TASK / "jobs/completions/AJC-AJ-RT-20260708-010-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0703.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
TEX_REGISTRY = ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
REPORT = ARTIFACTS / "p5_t04_source_detector_readout_candidate_report.json"


EXPECTED_COMPLETION_FIELDS = {
    "candidate_name": "SourceReadoutCandidate_EStar_v1",
    "result_type": "constructed_candidate",
    "source_domain": "SMScope(E_*)",
    "readout_interface": "Readout_src(E_*): Readable_src(E_*) -> Tok_R(E_*)",
    "detector_source_record": "Det_src(E_*)",
    "certificate_bundle": "Cert_R(E_*)",
    "finite_local_witness": "W_R(E_*)",
    "compatible_with_K_Estar": True,
    "status": "draft_control_candidate",
    "no_empirical_protocol_import": True,
    "no_proper_time_import": True,
    "no_target_metric_import": True,
    "detector_semantics_adopted": False,
    "matter_coupling_derived": False,
    "obstruction_recorded": False,
}

REQUIRED_TEX_PHRASES = [
    "This artifact completes v18 P5-T04.",
    "SourceReadoutCandidate_EStar_v1",
    "source_detector_readout_candidate:",
    "source_domain: \"SMScope(E_*)\"",
    "readout_interface: \"Readout_src(E_*): Readable_src(E_*) -> Tok_R(E_*)\"",
    "detector_source_record: \"Det_src(E_*)",
    "certificate_bundle: \"Cert_R(E_*)",
    "finite_local_witness: \"W_R(E_*)\"",
    "compatible_with_K_Estar: true",
    "status: \"draft_control_candidate\"",
    "no_empirical_protocol_import: true",
    "no_proper_time_import: true",
    "no_target_metric_import: true",
    "detector_semantics_adopted: false",
    "matter_coupling_derived: false",
    "no_fog_check: true",
    "finite/local witness",
    "Limited compatibility holds",
    "No empirical protocol, proper time, or target metric imported",
    "The Distance-to-GR ledger is unchanged",
    "P5-T05",
]

FORBIDDEN_PROMOTION_SNIPPETS = [
    "Det_src adopted",
    "Readout_src adopted",
    "detector semantics adopted",
    "source detector/readout semantics adopted",
    "matter coupling derived",
    "coupling law adopted",
    "Einstein equations derived",
    "benchmark promoted",
    "completed derivation achieved",
]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def tex_verbatim_block_contains(text: str, marker: str) -> bool:
    pattern = re.compile(r"\\begin\{verbatim\}(.*?)\\end\{verbatim\}", re.DOTALL)
    return any(marker in match.group(1) for match in pattern.finditer(text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    for path in [CANDIDATE, COMPLETION, HANDOFF, PROGRAM_STATE, TEX_REGISTRY]:
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    text = CANDIDATE.read_text(encoding="utf-8") if CANDIDATE.exists() else ""
    for phrase in REQUIRED_TEX_PHRASES:
        if phrase not in text:
            failures.append(f"candidate TeX missing phrase: {phrase}")

    if not tex_verbatim_block_contains(text, "source_detector_readout_candidate:"):
        failures.append("candidate TeX missing required source_detector_readout_candidate verbatim block")
    if not tex_verbatim_block_contains(text, "source_detector_readout_result:"):
        failures.append("candidate TeX missing required source_detector_readout_result verbatim block")

    for snippet in FORBIDDEN_PROMOTION_SNIPPETS:
        if snippet in text:
            failures.append(f"candidate TeX contains forbidden promotion snippet: {snippet}")

    completion = load_yaml(COMPLETION) if COMPLETION.exists() else {}
    if completion.get("plan_task_id") != "P5-T04":
        failures.append("completion plan_task_id must be P5-T04")
    if completion.get("objective_result") != "completed":
        failures.append("completion objective_result must be completed")
    result = completion.get("candidate_result", {})
    for key, expected in EXPECTED_COMPLETION_FIELDS.items():
        if result.get(key) != expected:
            failures.append(f"candidate_result.{key} expected {expected!r} got {result.get(key)!r}")
    if result.get("selected_next_plan_task_id") != "P5-T05":
        failures.append("candidate_result.selected_next_plan_task_id must be P5-T05")
    if completion.get("distance_to_gr_delta", {}).get("changed") is not False:
        failures.append("completion distance_to_gr_delta.changed must be false")
    if completion.get("no_fog_result", {}).get("no_fog_check") is not True:
        failures.append("completion no_fog_result.no_fog_check must be true")
    if completion.get("no_fog_result", {}).get("result_type") != "constructed_candidate":
        failures.append("completion no_fog_result.result_type must be constructed_candidate")

    program_state = load_yaml(PROGRAM_STATE) if PROGRAM_STATE.exists() else {}
    if program_state.get("active_task_id") != "RT-20260708-010":
        failures.append("program_state active_task_id must be RT-20260708-010")
    if program_state.get("latest_handoff_id") != "handoff-0703":
        failures.append("program_state latest_handoff_id must be handoff-0703")

    handoff = load_yaml(HANDOFF) if HANDOFF.exists() else {}
    selected_next = handoff.get("selected_next_route", {})
    if selected_next.get("plan_task_id") != "P5-T05":
        failures.append("handoff selected_next_route.plan_task_id must be P5-T05")
    if selected_next.get("role_family") != "smuggling-auditor@0.2.0":
        failures.append("handoff selected_next_route.role_family must be smuggling-auditor@0.2.0")

    registry_text = TEX_REGISTRY.read_text(encoding="utf-8") if TEX_REGISTRY.exists() else ""
    if "TEX-V18-P5-T04-SOURCE-DETECTOR-READOUT-CANDIDATE" not in registry_text:
        failures.append("TEX_SOURCE_REGISTRY missing P5-T04 candidate row")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "plan_task_id": "P5-T04",
        "candidate_name": "SourceReadoutCandidate_EStar_v1",
        "result_type": "constructed_candidate",
        "obstruction_recorded": False,
        "selected_next_plan_task_id": "P5-T05",
        "adoption_requested": False,
        "ledger_row_updated": False,
        "physics_promotion_authorized": False,
        "no_fog_check": True,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
