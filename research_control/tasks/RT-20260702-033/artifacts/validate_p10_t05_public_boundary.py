#!/usr/bin/env python3
"""Validate the bounded P10-T05 public-boundary scan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260702-033"
ARTIFACT = TASK_DIR / "artifacts" / "p10_t05_public_boundary_scan.yaml"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260702-033-001.yaml"
HANDOFF = ROOT / "research_control" / "handoffs" / "handoff-0486.yaml"

ARTIFACT_MARKERS = [
    'explicit_literature_comparison_mentions_found: false',
    'external_validation_or_resemblance_claims_found: false',
    'direct_public_source_edits_required: false',
    'generated_html_direct_edits_required: false',
    'selected_next_route: "P11-T01"',
    'status: "PASS"',
]

COMPLETION_MARKERS = [
    'related_plan_task_id: "P10-T05"',
    "public_boundary_scan:",
    "documentation_control_no_distance_delta",
    'phase_p10_completed: true',
]

HANDOFF_MARKERS = [
    'task_type: "v14_p11_t01_matter_coupling_moratorium_control_note"',
    'role_id: "project-control-maintainer"',
    "P11-T01",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    artifact_text = read_text(ARTIFACT)
    completion_text = read_text(COMPLETION)
    handoff_text = read_text(HANDOFF)
    checks: list[dict[str, object]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    missing_artifact = [item for item in ARTIFACT_MARKERS if item not in artifact_text]
    record("artifact_boundary_markers_present", not missing_artifact, f"missing={missing_artifact}")

    missing_completion = [item for item in COMPLETION_MARKERS if item not in completion_text]
    record("completion_markers_present", not missing_completion, f"missing={missing_completion}")

    missing_handoff = [item for item in HANDOFF_MARKERS if item not in handoff_text]
    record("handoff_routes_to_p11_t01", not missing_handoff, f"missing={missing_handoff}")

    expected_paths = [
        "README.md",
        "github-facing/**",
        "markdown/html-explainer-specs/**",
        "markdown/publication-briefs/**",
        "html/**",
    ]
    missing_paths = [item for item in expected_paths if item not in artifact_text]
    record("scan_scope_present", not missing_paths, f"missing={missing_paths}")

    no_promotion_terms = [
        "external_resemblance_as_validation_authorized: false",
        "downstream_physics_promotion_authorized: false",
        "benchmark_promotion_authorized: false",
        "completed_derivation_authorized: false",
    ]
    missing_boundary = [item for item in no_promotion_terms if item not in artifact_text]
    record("no_promotion_boundary_present", not missing_boundary, f"missing={missing_boundary}")

    passed = all(check["status"] == "PASS" for check in checks)
    report = {
        "validator_id": "validate_p10_t05_public_boundary",
        "task_id": "RT-20260702-033",
        "job_id": "AJ-RT-20260702-033-001",
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
