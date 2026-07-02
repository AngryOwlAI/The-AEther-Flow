#!/usr/bin/env python3
"""Validate the bounded P10-T04 literature findings selector packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260702-032"
ARTIFACT = TASK_DIR / "artifacts" / "p10_t04_literature_findings_selector_v1.yaml"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260702-032-001.yaml"
HANDOFF = ROOT / "research_control" / "handoffs" / "handoff-0485.yaml"

REQUIRED_ROUTE_CLASSES = [
    "repair_needed",
    "red_team_needed",
    "theorem_target",
    "obstruction_candidate",
    "no_action",
    "public_boundary_update",
]

REQUIRED_MARKERS = [
    'selected_next_plan_task_id: "P10-T05"',
    'selected_next_role_family: "documentation-curator@2.0.0"',
    'selected_route: "public_boundary_update_then_p11_moratorium"',
    "gate_ready_warning_resolution:",
    "route_classifications:",
]

COMPLETION_MARKERS = [
    'related_plan_task_id: "P10-T04"',
    "theoretical_decision_output:",
    'selected_next_control_packet_type: "documentation_boundary_packet"',
    "parent_child_synthesis:",
    "selector_only_no_distance_delta",
]

HANDOFF_MARKERS = [
    'task_type: "v14_p10_t05_literature_comparison_public_boundary"',
    'role_id: "documentation-curator"',
    "P10-T05",
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

    missing_route_classes = [item for item in REQUIRED_ROUTE_CLASSES if item not in artifact_text]
    record("route_classes_present", not missing_route_classes, f"missing={missing_route_classes}")

    missing_artifact = [item for item in REQUIRED_MARKERS if item not in artifact_text]
    record("selector_artifact_markers_present", not missing_artifact, f"missing={missing_artifact}")

    missing_completion = [item for item in COMPLETION_MARKERS if item not in completion_text]
    record("completion_markers_present", not missing_completion, f"missing={missing_completion}")

    missing_handoff = [item for item in HANDOFF_MARKERS if item not in handoff_text]
    record("handoff_routes_to_p10_t05", not missing_handoff, f"missing={missing_handoff}")

    child_paths = [
        TASK_DIR / "artifacts" / "child_phys_math_p10_t04_literature_findings_selector.yaml",
        TASK_DIR / "artifacts" / "child_phys_phil_p10_t04_literature_findings_selector.yaml",
        TASK_DIR / "artifacts" / "parent_conflict_review_p10_t04_literature_findings_selector.yaml",
        TASK_DIR / "artifacts" / "parent_fusion_notes_p10_t04_literature_findings_selector.md",
    ]
    record(
        "parent_child_synthesis_artifacts_present",
        all(read_text(path).strip() for path in child_paths),
        "child math child phil conflict review and fusion notes checked",
    )

    no_promotion_terms = [
        "no external validation by resemblance",
        "no source-law adoption",
        "no matter-coupling derivation or adoption",
        "no Einstein equations",
        "no benchmark promotion",
        "no completed derivation",
    ]
    lower_artifact_text = artifact_text.lower()
    missing_no_promotion = [item for item in no_promotion_terms if item.lower() not in lower_artifact_text]
    record("no_promotion_boundary_present", not missing_no_promotion, f"missing={missing_no_promotion}")

    passed = all(check["status"] == "PASS" for check in checks)
    report = {
        "validator_id": "validate_p10_t04_literature_findings_selector",
        "task_id": "RT-20260702-032",
        "job_id": "AJ-RT-20260702-032-001",
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
