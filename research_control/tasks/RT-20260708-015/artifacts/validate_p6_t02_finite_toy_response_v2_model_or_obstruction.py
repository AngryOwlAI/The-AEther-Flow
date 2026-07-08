#!/usr/bin/env python3
"""Validate the v18 P6-T02 finite toy response v2 model-or-obstruction packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260708-015"
ARTIFACT = TASK_DIR / "artifacts" / "finite_toy_response_v2_model_or_obstruction.tex"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260708-015-001.yaml"
REPORT = TASK_DIR / "artifacts" / "p6_t02_finite_toy_response_v2_model_or_obstruction_report.json"


REQUIRED_MARKERS = {
    "plan_task_id": "plan_task_id: P6-T02",
    "task_type": "task_type: finite_toy_response_v2_model_or_obstruction",
    "positive_model": "positive_toy_model: true",
    "no_obstruction": "precise_obstruction: false",
    "finite_source_set": "finite_source_set: S_v2 = {a,b,c}",
    "source_relations": "source_relations:",
    "orbit_structure": "orbit_or_invariant_structure:",
    "induced_response": "induced_response_relation: R_v2({x,y}) = d_A(x,y)",
    "tag_independence": "tag_independence_argument:",
    "relabeling_invariance": "relabeling_invariance_argument:",
    "no_target_metric_import": "no_target_metric_import: true",
    "not_g_eff": "not_g_eff: true",
    "not_matter_coupling": "not_matter_coupling: true",
    "candidate_result": "candidate_constructor_result:",
    "constructed_candidate": "result_type: constructed_candidate",
    "next_route": "next_plan_task_id: P6-T03",
}

FORBIDDEN_SUBSTRINGS = {
    "target_metric_import_false": "no_target_metric_import: false",
    "not_g_eff_false": "not_g_eff: false",
    "not_matter_coupling_false": "not_matter_coupling: false",
    "positive_and_obstruction": "precise_obstruction: true",
    "benchmark_promoted": "benchmark_status_changed: true",
    "old_response_tag_epsilon": "epsilon",
    "old_response_tag_lambda": "lambda",
    "old_response_tag_tau": "tau",
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

    lower_text = text.lower()
    for label, marker in FORBIDDEN_SUBSTRINGS.items():
        if marker.lower() in lower_text:
            errors.append(f"forbidden artifact marker {label}: {marker}")

    if "source adjacency relation -> graph distance d_A" not in text:
        errors.append("missing source adjacency to graph-distance map")
    if "graph distance -> response relation R_v2" not in text:
        errors.append("missing graph-distance to response-relation map")
    if "source automorphism orbits -> invariant response classes" not in text:
        errors.append("missing automorphism-orbit response map")
    if "P6-T03 relabeling and tag-removal stress" not in text:
        errors.append("missing P6-T03 proof obligation")
    if "finite-variation fail-closed stress" not in text:
        errors.append("missing finite-variation stress obligation")

    if COMPLETION.exists():
        for marker in (
            'plan_task_id: "P6-T02"',
            'result_type: "constructed_candidate"',
            'next_required_role: "refuter"',
            'claim_boundary_preserved: true',
            'selected_next_plan_task_id: "P6-T03"',
        ):
            if marker not in completion_text:
                errors.append(f"missing completion marker: {marker}")
    else:
        warnings.append(f"completion file not present yet: {COMPLETION}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "completion": str(COMPLETION.relative_to(ROOT)),
        "selected_next_plan_task_id": "P6-T03",
        "positive_toy_model": True,
        "precise_obstruction": False,
        "required_marker_count": len(REQUIRED_MARKERS),
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
