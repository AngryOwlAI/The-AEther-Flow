#!/usr/bin/env python3
"""Validate the v18 P3-T01 EqSrc family-closure setup artifact."""

from __future__ import annotations

import json
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
ARTIFACT = TASK_DIR / "eqsrc_family_closure_packet_setup_v1.md"
REPORT = TASK_DIR / "eqsrc_family_closure_packet_setup_validation.json"


REQUIRED_STRINGS = [
    'source_family_symbol: "F_src"',
    'typed_object_artifact: "research_control/tasks/RT-20260707-015/artifacts/source_equivalence_typed_object_v1.tex"',
    'theorem_or_countermodel_artifact: "eqsrc_family_closure_theorem_or_countermodel_v1.tex"',
    'selected_packet_target: "P3_T02_family_level_eqsrc_closure_theorem_or_minimal_countermodel_attempt"',
    "max_primary_payload_count: 1",
    'family_level_eqsrc_closure_theorem_candidate',
    'minimal_family_closure_countermodel',
    'RetainH_primitive_required',
    'GenH_primitive_required',
    'scoped_freeze_obstruction',
    "countermodel_obligation_required: true",
    "no_target_import_guard_required: true",
    "adoption_requested: false",
    'next_route: "P3-T02"',
    "RetainH_status_one_of",
    "GenH_status_one_of",
    "not_required_here",
    "required_but_missing",
    "candidate_definition_needed",
    "countermodel_blocks_current_route",
    "deferred",
    "missing_inverse_countermodel",
    "missing_composition_countermodel",
    "invariant_ledger_not_family_stable_countermodel",
    "target_import_needed_countermodel",
    "RetainH_needed_countermodel",
    "GenH_needed_countermodel",
    "target metric",
    "target proper time",
    "target stress-energy tensor",
    "matter action",
    "Einstein equations",
    "benchmark status",
    "Gate Chair status",
    "generated validator status",
    "commit status",
    "changed: false",
    'effect: "no_distance_delta"',
]


FORBIDDEN_BOUNDARY_STRINGS = [
    "general `EqSrc` discharge",
    "`RetainH` adoption",
    "`GenH` adoption",
    "source-law adoption",
    "Einstein-equation derivation",
    "benchmark promotion",
    "completed derivation",
    "global no-go claim",
]


def main() -> int:
    errors: list[str] = []

    if not ARTIFACT.exists():
        errors.append(f"missing artifact: {ARTIFACT}")
        text = ""
    else:
        text = ARTIFACT.read_text(encoding="utf-8")

    for required in REQUIRED_STRINGS:
        if required not in text:
            errors.append(f"missing required string: {required}")

    for forbidden in FORBIDDEN_BOUNDARY_STRINGS:
        if forbidden not in text:
            errors.append(f"missing explicit forbidden boundary: {forbidden}")

    selected_count = text.count("P3_T02_family_level_eqsrc_closure_theorem_or_minimal_countermodel_attempt")
    if selected_count < 2:
        errors.append("selected packet target must be declared in setup and prose")

    branch_terms = [
        "family_level_eqsrc_closure_theorem_candidate",
        "minimal_family_closure_countermodel",
        "RetainH_primitive_required",
        "GenH_primitive_required",
        "scoped_freeze_obstruction",
    ]
    for term in branch_terms:
        if text.count(term) < 2:
            errors.append(f"allowed primary payload lacks setup plus branch coverage: {term}")

    report = {
        "artifact": str(ARTIFACT.relative_to(TASK_DIR.parents[3])),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checked_required_string_count": len(REQUIRED_STRINGS),
        "checked_forbidden_boundary_count": len(FORBIDDEN_BOUNDARY_STRINGS),
        "selected_packet_target_count": selected_count,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

