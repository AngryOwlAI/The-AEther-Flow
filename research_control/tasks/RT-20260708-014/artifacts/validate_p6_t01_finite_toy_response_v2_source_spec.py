#!/usr/bin/env python3
"""Validate v18 P6-T01 finite toy response v2 source specification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260708-014"
ARTIFACTS = TASK / "artifacts"
SPEC = ARTIFACTS / "finite_toy_response_v2_source_spec.tex"
COMPLETION = TASK / "jobs/completions/AJC-AJ-RT-20260708-014-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0707.yaml"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
TEX_REGISTRY = ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
REPORT = ARTIFACTS / "p6_t01_finite_toy_response_v2_source_spec_report.json"


REQUIRED_TEX_PHRASES = [
    "This artifact implements v18 P6-T01.",
    "finite_toy_response_v2:",
    "finite_source_set: \"S_v2 = {a,b,c}\"",
    "source_relation_family: \"A_v2 path adjacency and Inc_v2 incidence records\"",
    "invariant_orbit_structure: \"Aut(P3) vertex and unordered-pair orbits\"",
    "induced_response_relation: \"R_v2({x,y}) = d_A(x,y)\"",
    "explicit_target_tags_forbidden: true",
    "target_metric_import_forbidden: true",
    "empirical_detector_import_forbidden: true",
    "relabeling_invariance_test: \"distance is invariant under Aut(P3)\"",
    "tag_removal_stress: \"erase presentation labels but retain source relation\"",
    "candidate_placeholder_nonadopted",
    "old route: response read from explicit tags",
    "P6-T01 route: response induced from source relation orbits",
    "The next route is P6-T02",
]

FORBIDDEN_SUCCESS_STRINGS = [
    "Det_src_adopted: true",
    "Readout_src_adopted: true",
    "detector_semantics_adopted: true",
    "source_law_adopted: true",
    "coupling_law_adopted: true",
    "matter_coupling_derived: true",
    "g_eff_constructed: true",
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
    for path in [SPEC, COMPLETION, HANDOFF, PROGRAM_STATE, TEX_REGISTRY]:
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    text = SPEC.read_text(encoding="utf-8") if SPEC.exists() else ""
    for phrase in REQUIRED_TEX_PHRASES:
        if phrase not in text:
            failures.append(f"spec TeX missing phrase: {phrase}")
    lowered = text.lower()
    for snippet in FORBIDDEN_SUCCESS_STRINGS:
        if snippet.lower() in lowered:
            failures.append(f"spec TeX contains forbidden success string: {snippet}")

    completion = load_yaml(COMPLETION) if COMPLETION.exists() else {}
    if completion.get("plan_task_id") != "P6-T01":
        failures.append("completion plan_task_id must be P6-T01")
    if completion.get("objective_result") != "completed":
        failures.append("completion objective_result must be completed")

    spec = completion.get("finite_toy_response_v2", {})
    expected = {
        "finite_source_set": "S_v2 = {a,b,c}",
        "source_relation_family": "A_v2 path adjacency and Inc_v2 incidence records",
        "invariant_orbit_structure": "Aut(P3) vertex and unordered-pair orbits",
        "induced_response_relation": "R_v2({x,y}) = d_A(x,y)",
        "explicit_target_tags_forbidden": True,
        "target_metric_import_forbidden": True,
        "empirical_detector_import_forbidden": True,
        "detector_readout_status": "candidate_placeholder_nonadopted",
        "selected_next_plan_task_id": "P6-T02",
    }
    for key, value in expected.items():
        if spec.get(key) != value:
            failures.append(f"finite_toy_response_v2.{key} expected {value!r} got {spec.get(key)!r}")
    if completion.get("distance_to_gr_delta", {}).get("changed") is not False:
        failures.append("completion distance_to_gr_delta.changed must be false")
    if completion.get("physics_promotion_authorized") is not False:
        failures.append("completion physics_promotion_authorized must be false")

    program_state = load_yaml(PROGRAM_STATE) if PROGRAM_STATE.exists() else {}
    if program_state.get("active_task_id") != "RT-20260708-014":
        failures.append("program_state active_task_id must be RT-20260708-014")
    if program_state.get("latest_handoff_id") != "handoff-0707":
        failures.append("program_state latest_handoff_id must be handoff-0707")

    handoff = load_yaml(HANDOFF) if HANDOFF.exists() else {}
    selected_next = handoff.get("selected_next_route", {})
    if selected_next.get("plan_task_id") != "P6-T02":
        failures.append("handoff selected_next_route.plan_task_id must be P6-T02")
    if selected_next.get("role_family") != "candidate-constructor@0.2.0":
        failures.append("handoff selected_next_route.role_family must be candidate-constructor@0.2.0")

    registry_text = TEX_REGISTRY.read_text(encoding="utf-8") if TEX_REGISTRY.exists() else ""
    if "TEX-V18-P6-T01-FINITE-TOY-RESPONSE-V2-SOURCE-SPEC" not in registry_text:
        failures.append("TEX_SOURCE_REGISTRY missing P6-T01 source spec row")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "plan_task_id": "P6-T01",
        "finite_source_set": "S_v2 = {a,b,c}",
        "source_relation_family": "A_v2 path adjacency and Inc_v2 incidence records",
        "induced_response_relation": "R_v2({x,y}) = d_A(x,y)",
        "explicit_target_tags_forbidden": True,
        "target_metric_import_forbidden": True,
        "empirical_detector_import_forbidden": True,
        "detector_readout_status": "candidate_placeholder_nonadopted",
        "selected_next_plan_task_id": "P6-T02",
        "ledger_row_updated": False,
        "physics_promotion_authorized": False,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
