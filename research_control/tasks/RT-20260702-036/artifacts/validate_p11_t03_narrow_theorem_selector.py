#!/usr/bin/env python3
"""Validate the bounded P11-T03 narrow theorem target selector packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260702-036"
ARTIFACT = TASK_DIR / "artifacts" / "p11_t03_narrow_theorem_target_selector_v1.yaml"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260702-036-001.yaml"
HANDOFF = ROOT / "research_control" / "handoffs" / "handoff-0489.yaml"

REQUIRED_ROUTE_IDS = [
    "source_side_matter_semantics_equivalence_class_theorem",
    "PositiveMSProfile_v1_stability_theorem",
    "RR_E_separation_preservation_theorem",
    "no_target_certificate_hygiene_theorem",
    "coupling_law_target_formalization_only",
    "detector_semantics_alternative_target_formalization_only",
    "scoped_obstruction_or_freeze",
]

ARTIFACT_MARKERS = [
    'selected_route: "no_target_certificate_hygiene_theorem_first"',
    'selected_next_plan_task_id: "P11-T04"',
    'selected_next_role_family: "documentation-curator@2.0.0"',
    "candidate_route_matrix:",
    "selected_target:",
    "gate_ready_warning_resolution:",
]

COMPLETION_MARKERS = [
    'related_plan_task_id: "P11-T03"',
    "theoretical_decision_output:",
    'selected_next_control_packet_type: "task_template_control_packet"',
    "parent_child_synthesis:",
    "selector_only_no_distance_delta",
    "new_mathematical_payload:",
]

HANDOFF_MARKERS = [
    'task_type: "v14_p11_t04_narrow_theorem_task_template"',
    'role_id: "documentation-curator"',
    "P11-T04",
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

    missing_route_ids = [item for item in REQUIRED_ROUTE_IDS if item not in artifact_text]
    record("candidate_routes_present", not missing_route_ids, f"missing={missing_route_ids}")

    missing_artifact = [item for item in ARTIFACT_MARKERS if item not in artifact_text]
    record("selector_artifact_markers_present", not missing_artifact, f"missing={missing_artifact}")

    missing_completion = [item for item in COMPLETION_MARKERS if item not in completion_text]
    record("completion_markers_present", not missing_completion, f"missing={missing_completion}")

    missing_handoff = [item for item in HANDOFF_MARKERS if item not in handoff_text]
    record("handoff_routes_to_p11_t04", not missing_handoff, f"missing={missing_handoff}")

    child_paths = [
        TASK_DIR / "artifacts" / "child_phys_math_p11_t03_narrow_theorem_selector.yaml",
        TASK_DIR / "artifacts" / "child_phys_phil_p11_t03_narrow_theorem_selector.yaml",
        TASK_DIR / "artifacts" / "parent_conflict_review_p11_t03_narrow_theorem_selector.yaml",
        TASK_DIR / "artifacts" / "parent_fusion_notes_p11_t03_narrow_theorem_selector.md",
    ]
    record(
        "parent_child_synthesis_artifacts_present",
        all(read_text(path).strip() for path in child_paths),
        "child math child phil conflict review and fusion notes checked",
    )

    no_promotion_terms = [
        "no source-law adoption",
        "no matter-semantics adoption",
        "no detector-semantics adoption",
        "no coupling-law adoption",
        "no matter-coupling derivation or adoption",
        "no Einstein equations",
        "no benchmark promotion",
        "no completed derivation",
    ]
    lower_artifact_text = artifact_text.lower()
    missing_no_promotion = [item for item in no_promotion_terms if item.lower() not in lower_artifact_text]
    record("no_promotion_boundary_present", not missing_no_promotion, f"missing={missing_no_promotion}")

    selected_before_template = "P11-T04 should create the narrow theorem task template" in artifact_text
    record("template_precedes_execution", selected_before_template, "P11-T04 template precedes P12 execution")

    passed = all(check["status"] == "PASS" for check in checks)
    report = {
        "validator_id": "validate_p11_t03_narrow_theorem_selector",
        "task_id": "RT-20260702-036",
        "job_id": "AJ-RT-20260702-036-001",
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
