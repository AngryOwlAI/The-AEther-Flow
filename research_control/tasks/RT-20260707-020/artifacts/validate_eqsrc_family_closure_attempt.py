#!/usr/bin/env python3
"""Validate the v18 P3-T02 EqSrc family-closure attempt artifact."""

from __future__ import annotations

import json
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
ARTIFACT = TASK_DIR / "artifacts" / "eqsrc_family_closure_theorem_or_countermodel_v1.tex"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260707-020-001.yaml"
REPORT = TASK_DIR / "artifacts" / "eqsrc_family_closure_attempt_validation.json"

PRIMARY_MARKERS = [
    "family_closure_theorem_candidate_supplied",
    "minimal_countermodel_supplied",
    "retainh_primitive_required",
    "genh_primitive_required",
    "scoped_freeze_obstruction",
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Prior Record-Local",
    "Typed Source Family",
    "Family Invariant Ledger",
    "Candidate Family-Level",
    "Identity Closure Attempt",
    "Inverse Closure Attempt",
    "Composition Closure Attempt",
    "RetainH",
    "GenH",
    "Minimal Countermodel Search",
    "Theorem Candidate or Obstruction",
    "Distance-to-GR Effect",
    "Forbidden Conclusions",
    "Source Materials",
]

REQUIRED_PHRASES = [
    "missing_inverse_countermodel",
    "RetainH_adopted: false",
    "GenH_adopted: false",
    "adoption_requested: false",
    "changed: false",
    "effect: no_distance_delta",
    "global no-go conclusion",
    "P3-T03",
]

FORBIDDEN_TRUE_PHRASES = [
    "RetainH_adopted: true",
    "GenH_adopted: true",
    "adoption_requested: true",
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

    found_primary = [marker for marker in PRIMARY_MARKERS if marker in text]
    if found_primary != ["family_closure_theorem_candidate_supplied"]:
        errors.append(
            "artifact must contain exactly one primary marker, "
            f"family_closure_theorem_candidate_supplied; found {found_primary}"
        )

    completion_primary = [marker for marker in PRIMARY_MARKERS if marker in completion_text]
    if "family_closure_theorem_candidate_supplied" not in completion_primary:
        errors.append("completion does not record the theorem-candidate primary result")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required section phrase: {section}")

    for phrase in REQUIRED_PHRASES:
        if phrase not in text and phrase not in completion_text:
            errors.append(f"missing required phrase: {phrase}")

    for phrase in FORBIDDEN_TRUE_PHRASES:
        if phrase in text or phrase in completion_text:
            errors.append(f"forbidden true phrase present: {phrase}")

    if "target metric" not in text or "stress-energy" not in text:
        warnings.append("no-target guard language may be too sparse")

    report = {
        "schema_id": "eqsrc_family_closure_attempt_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260707-020",
        "plan_task_id": "P3-T02",
        "primary_result": "family_closure_theorem_candidate_supplied",
        "countermodel_slot_attempted": "missing_inverse_countermodel",
        "errors": errors,
        "warnings": warnings,
        "checked_paths": [
            str(ARTIFACT.relative_to(TASK_DIR.parents[1])),
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
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
