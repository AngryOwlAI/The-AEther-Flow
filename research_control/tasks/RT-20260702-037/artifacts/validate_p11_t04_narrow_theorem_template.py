#!/usr/bin/env python3
"""Validate the bounded P11-T04 narrow theorem task template packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260702-037"
TEMPLATE = ROOT / "research_control" / "design" / "narrow_theorem_task_template.md"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260702-037-001.yaml"
HANDOFF = ROOT / "research_control" / "handoffs" / "handoff-0490.yaml"

REQUIRED_SECTIONS = [
    "## Required Task Fields",
    "### Exact Theorem Question",
    "### Assumptions",
    "### Source Certificates Required",
    "### `RR_E` Handling",
    "### No-Target Hygiene",
    "### Accepted Evidence And Preconditions Used",
    "### Forbidden Downstream Overreads",
    "### Stress And Refuter Requirements",
    "### Adoption Status After Theorem",
    "### Selector And Gate Requirements",
    "## No-Target Hygiene Theorem Seed",
    "## Machine-Readable Checklist",
]

REQUIRED_FIELD_MARKERS = [
    "exact_theorem_question_required: true",
    "assumptions_required: true",
    "source_certificates_required: true",
    "rr_e_handling_required: true",
    "no_target_hygiene_required: true",
    "accepted_evidence_preconditions_required: true",
    "forbidden_downstream_overreads_required: true",
    "stress_refuter_requirements_required: true",
    "adoption_status_after_theorem_required: true",
    "selector_gate_requirements_required: true",
]

COMPLETION_MARKERS = [
    'related_plan_task_id: "P11-T04"',
    "narrow_theorem_template:",
    'template_path: "research_control/design/narrow_theorem_task_template.md"',
    "control_template_no_distance_delta",
]

HANDOFF_MARKERS = [
    'task_type: "v14_p11_t05_matter_coupling_moratorium_validation"',
    "P11-T05",
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

    template_text = read_text(TEMPLATE)
    completion_text = read_text(COMPLETION)
    handoff_text = read_text(HANDOFF)

    checks: list[dict[str, object]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    missing_sections = [item for item in REQUIRED_SECTIONS if item not in template_text]
    record("required_sections_present", not missing_sections, f"missing={missing_sections}")

    missing_fields = [item for item in REQUIRED_FIELD_MARKERS if item not in template_text]
    record("machine_readable_fields_present", not missing_fields, f"missing={missing_fields}")

    no_promotion_terms = [
        "source-law adoption",
        "matter-semantics adoption",
        "detector-semantics adoption",
        "coupling-law adoption",
        "matter-coupling derivation or adoption",
        "stress-energy semantics",
        "matter action",
        "Einstein equations",
        "benchmark promotion",
        "completed derivation",
    ]
    lower_template = template_text.lower()
    missing_no_promotion = [item for item in no_promotion_terms if item.lower() not in lower_template]
    record("no_promotion_boundary_present", not missing_no_promotion, f"missing={missing_no_promotion}")

    missing_completion = [item for item in COMPLETION_MARKERS if item not in completion_text]
    record("completion_markers_present", not missing_completion, f"missing={missing_completion}")

    missing_handoff = [item for item in HANDOFF_MARKERS if item not in handoff_text]
    record("handoff_routes_to_p11_t05", not missing_handoff, f"missing={missing_handoff}")

    passed = all(check["status"] == "PASS" for check in checks)
    report = {
        "validator_id": "validate_p11_t04_narrow_theorem_template",
        "task_id": "RT-20260702-037",
        "job_id": "AJ-RT-20260702-037-001",
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
