#!/usr/bin/env python3
"""Validate the v18 P6-T03 finite toy response v2 Refuter stress packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260708-016"
ARTIFACT = TASK_DIR / "artifacts" / "finite_toy_response_v2_refuter_stress.tex"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260708-016-001.yaml"
REPORT = TASK_DIR / "artifacts" / "p6_t03_finite_toy_response_v2_refuter_stress_report.json"


REQUIRED_MARKERS = {
    "plan_task_id": "plan_task_id: P6-T03",
    "task_type": "task_type: finite_toy_response_v2_invariance_tag_stress",
    "stress_result": "stress_result: survives_as_finite_toy_model",
    "bridge_category": "bridge_or_fail_category: bridge_facing_candidate_path",
    "target_milestone": "target_derivation_milestone: finite_toy_metric_response",
    "no_target_metric_import": "no_target_metric_import: true",
    "not_g_eff": "not_g_eff: true",
    "not_matter_coupling": "not_matter_coupling: true",
    "freeze_decision": "freeze_decision: not_frozen",
    "next_route": "next_plan_task_id: P6-T04",
    "refuter_result": "finite_toy_response_v2_refuter_result:",
}

STRESS_MODES = [
    "remove_explicit_labels_or_tags",
    "relabel_source_tokens",
    "perturb_source_relation_edges",
    "collapse_invariant_orbit_structure",
    "substitute_target_distance",
    "substitute_physical_metric",
    "substitute_empirical_readout",
    "treat_toy_response_as_g_eff",
    "treat_toy_response_as_matter_coupling",
]

FORBIDDEN_SUBSTRINGS = {
    "target_metric_import_false": "no_target_metric_import: false",
    "not_g_eff_false": "not_g_eff: false",
    "not_matter_coupling_false": "not_matter_coupling: false",
    "benchmark_promoted": "benchmark_promoted: true",
    "completed_derivation": "completed_derivation_claimed: true",
    "freeze_route_result": "stress_result: freeze_route",
    "scoped_obstruction_result": "stress_result: scoped_obstruction",
}


def validate() -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    text = ARTIFACT.read_text(encoding="utf-8") if ARTIFACT.exists() else ""
    completion_text = COMPLETION.read_text(encoding="utf-8") if COMPLETION.exists() else ""

    if not ARTIFACT.exists():
        errors.append(f"missing artifact: {ARTIFACT}")
    for label, marker in REQUIRED_MARKERS.items():
        if marker not in text:
            errors.append(f"missing required artifact marker {label}: {marker}")

    for mode in STRESS_MODES:
        if mode not in text:
            errors.append(f"missing stress mode: {mode}")

    lower_text = text.lower()
    for label, marker in FORBIDDEN_SUBSTRINGS.items():
        if marker.lower() in lower_text:
            errors.append(f"forbidden artifact marker {label}: {marker}")

    for marker in (
        "Tag erasure preserves the finite toy response",
        "Source relabeling preserves the response",
        "Edge perturbation is not physical robustness",
        "Target and downstream substitutions are blocked overreads",
        "OB-V18-P6T03-TARGET-OVERREAD-001",
    ):
        if marker not in text:
            errors.append(f"missing stress lemma or obstruction marker: {marker}")

    if COMPLETION.exists():
        for marker in (
            'plan_task_id: "P6-T03"',
            'stress_result: "survives_as_finite_toy_model"',
            'category: "bridge_facing_candidate_path"',
            'selected_next_plan_task_id: "P6-T04"',
            'claim_boundary_preserved: true',
        ):
            if marker not in completion_text:
                errors.append(f"missing completion marker: {marker}")
    else:
        warnings.append(f"completion file not present yet: {COMPLETION}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "completion": str(COMPLETION.relative_to(ROOT)),
        "selected_next_plan_task_id": "P6-T04",
        "stress_result": "survives_as_finite_toy_model",
        "bridge_or_fail_category": "bridge_facing_candidate_path",
        "required_marker_count": len(REQUIRED_MARKERS),
        "stress_mode_count": len(STRESS_MODES),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
