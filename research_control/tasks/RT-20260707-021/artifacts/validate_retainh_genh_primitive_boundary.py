#!/usr/bin/env python3
"""Validate the v18 P3-T03 RetainH/GenH primitive-boundary artifact."""

from __future__ import annotations

import json
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
ARTIFACT = TASK_DIR / "artifacts" / "retainh_genh_primitive_boundary_v1.tex"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260707-021-001.yaml"
REPORT = TASK_DIR / "artifacts" / "retainh_genh_primitive_boundary_validation.json"

REQUIRED_SECTIONS = [
    "Control Status",
    "Inputs from P3-T02",
    "RetainH Boundary",
    "GenH Boundary",
    "Primitive Needed, Primitive Avoided, or Primitive Deferred Classification",
    "Minimal Witness or Countermodel",
    "No-Target Import Guard",
    "Distance-to-GR Effect",
    "Forbidden Conclusions",
    "Source Materials",
]

REQUIRED_PHRASES = [
    "primitive_boundary_extracted_no_adoption",
    "RetainH_status_for_closed_declared_family: not_required_here",
    "RetainH_status_for_H_retention_extension: candidate_definition_needed",
    "GenH_status_for_closed_declared_family: not_required_here",
    "GenH_status_for_H_generated_extension: candidate_definition_needed",
    "RetainH_adopted: false",
    "GenH_adopted: false",
    "adoption_requested: false",
    "apply_H_retention_without_RetainH",
    "expand_source_family_without_GenH",
    "target metric",
    "stress-energy",
    "effect: no_distance_delta",
    "P3-T04",
]

FORBIDDEN_TRUE_PHRASES = [
    "RetainH_adopted: true",
    "GenH_adopted: true",
    "adoption_requested: true",
    "general_EqSrc_discharged: true",
    "source_law_adopted: true",
    "benchmark_promoted: true",
    "completed_derivation_claimed: true",
]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not ARTIFACT.exists():
        errors.append(f"missing artifact: {ARTIFACT}")
        text = ""
    else:
        text = ARTIFACT.read_text(encoding="utf-8")

    if not COMPLETION.exists():
        errors.append(f"missing completion: {COMPLETION}")
        completion_text = ""
    else:
        completion_text = COMPLETION.read_text(encoding="utf-8")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required section phrase: {section}")

    combined = text + "\n" + completion_text
    for phrase in REQUIRED_PHRASES:
        if phrase not in combined:
            errors.append(f"missing required phrase: {phrase}")

    for phrase in FORBIDDEN_TRUE_PHRASES:
        if phrase in combined:
            errors.append(f"forbidden true phrase present: {phrase}")

    if "countermodel_blocks_current_route" in text and "No classification in this packet is" not in text:
        warnings.append("countermodel_blocks_current_route appears without explicit non-selection context")

    report = {
        "schema_id": "retainh_genh_primitive_boundary_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260707-021",
        "plan_task_id": "P3-T03",
        "primitive_boundary_result": "primitive_boundary_extracted_no_adoption",
        "classifications": {
            "RetainH_closed_declared_family": "not_required_here",
            "RetainH_H_retention_extension": "candidate_definition_needed",
            "GenH_closed_declared_family": "not_required_here",
            "GenH_H_generated_extension": "candidate_definition_needed",
        },
        "errors": errors,
        "warnings": warnings,
        "checked_paths": [
            str(ARTIFACT.relative_to(TASK_DIR.parents[1])) if ARTIFACT.exists() else str(ARTIFACT),
            str(COMPLETION.relative_to(TASK_DIR.parents[1])) if COMPLETION.exists() else str(COMPLETION),
        ],
        "no_promotion_boundary": {
            "general_EqSrc_discharged": False,
            "RetainH_adopted": False,
            "GenH_adopted": False,
            "source_law_adopted": False,
            "matter_coupling_derived": False,
            "einstein_equations_derived": False,
            "benchmark_promoted": False,
            "completed_derivation_claimed": False,
        },
        "next_route": "P3-T04",
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
