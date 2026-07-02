#!/usr/bin/env python3
"""Validate the P10-T01 literature-comparison scope selector artifact."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260702-029"
ARTIFACT = TASK_DIR / "artifacts/p10_t01_literature_comparison_scope_selector_v1.yaml"
COMPLETION = TASK_DIR / "jobs/completions/AJC-AJ-RT-20260702-029-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0482.yaml"

REQUIRED_AREAS = {
    "causal_set_theory",
    "metric_reconstruction",
    "operational_spacetime_reconstruction",
    "universal_coupling_reconstruction_and_no_go_constraints",
    "stress_energy_derivation",
    "matter_action_derivation",
    "variational_principles",
    "einstein_equation_derivation_requirements",
    "detector_operational_semantics",
    "lorentzian_geometry_from_causal_order_response_data",
}

REQUIRED_AXES = {
    "order_to_lorentzian_geometry",
    "response_to_detector_semantics",
    "universal_coupling_to_stress_energy",
    "einstein_equation_derivation_requirements",
    "emergent_and_analogue_gravity_cautions",
    "no_target_certificate_hygiene",
}

REQUIRED_SOURCE_FIELDS = {
    "source list with bibliographic metadata",
    "reason each source is relevant",
    "which AEther-Flow burden it may constrain",
    "source-access notes",
    "APA 7 citation candidates",
    "no claim-promotion statement",
}


def load_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text()


def expect(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    artifact = load_text(ARTIFACT)
    completion = load_text(COMPLETION)
    handoff = load_text(HANDOFF)

    comparison_areas = set(re.findall(r'^\s*-\s+"([^"]+)"\s*$', artifact, re.MULTILINE))
    axis_ids = set(re.findall(r'axis_id:\s+"([^"]+)"', artifact))
    source_family_count = len(re.findall(r'family_id:\s+"([^"]+)"', artifact))
    primary_required_count = len(re.findall(r'primary_source_required:\s+true', artifact))

    expect('artifact_type: "theoretical_decision_output"' in artifact, errors, "artifact_type must be theoretical_decision_output")
    expect('selected_scope_id: "operational_causal_metric_universal_coupling_constraints_scope"' in artifact, errors, "unexpected selected_scope_id")
    expect(comparison_areas >= REQUIRED_AREAS, errors, "required comparison areas missing")
    expect(axis_ids == REQUIRED_AXES, errors, "coverage axes mismatch")
    expect(source_family_count >= 6, errors, "at least six source families required")
    expect(primary_required_count == source_family_count, errors, "all source families must require primary sources")
    expect('selected_next_packet_type: "literature_source_acquisition_packet"' in artifact, errors, "next packet must be P10-T02 source acquisition")
    expect('selected_next_plan_task_id: "P10-T02"' in artifact, errors, "next plan task must be P10-T02")
    expect('selected_next_packet_type: "bounded_theoretical_calculation"' in artifact, errors, "theoretical selected_next_packet_type must satisfy allowed selector vocabulary")
    expect('selected_next_control_packet_type: "literature_source_acquisition_packet"' in artifact, errors, "control packet type must route to source acquisition")
    expect('preserves_claim_blocks: true' in artifact, errors, "selector must preserve claim blocks")
    expect('requires_human_gate: false' in artifact, errors, "selector must not require human gate")
    for required_field in REQUIRED_SOURCE_FIELDS:
        expect(f'- "{required_field}"' in artifact, errors, f"P10-T02 required output field missing: {required_field}")
    for key in (
        "proof_authority",
        "ontology_edit_authorized",
        "source_law_adoption_authorized",
        "downstream_physics_promotion_authorized",
        "benchmark_promotion_authorized",
        "completed_derivation_authorized",
        "external_resemblance_as_validation_authorized",
    ):
        expect(f"{key}: false" in artifact, errors, f"claim boundary {key} must be false")

    expect('related_plan_task_id: "P10-T01"' in completion, errors, "completion must identify P10-T01")
    expect('selected_next_control_packet_type: "literature_source_acquisition_packet"' in completion, errors, "completion must route to literature source acquisition")
    expect('status: "no_conflict"' in completion, errors, "parent-child synthesis must have no conflict")
    expect('task_type: "v14_p10_t02_literature_source_acquisition_packet"' in handoff, errors, "handoff must require P10-T02")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "validated_artifact": str(ARTIFACT.relative_to(ROOT)),
        "validated_completion": str(COMPLETION.relative_to(ROOT)),
        "selected_scope_id": "operational_causal_metric_universal_coupling_constraints_scope",
        "selected_next_packet_type": "literature_source_acquisition_packet",
        "coverage_axis_count": len(axis_ids),
        "source_family_count": source_family_count,
        "claim_promotion_authorized": False,
    }
    output_path = Path(args.output)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
