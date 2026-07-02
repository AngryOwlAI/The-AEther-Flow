#!/usr/bin/env python3
"""Validate the bounded P12-T02 positive semantics requirement packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DOC_PATH = "research_control/design/positive_semantics_requirement_note.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
HANDOFF_PATH = "research_control/handoffs/handoff-0493.yaml"

REQUIRED_ELEMENTS = [
    "source-side matter record domain",
    "source-side semantic labels or structures",
    "admissibility conditions",
    "equivalence or separation relation",
    "stability under source relabeling or finite variation",
    "fail-closed obstruction branches",
    "relation to `PositiveMSProfile_v1`",
    "relation to `RR_E` transport/invariance",
    "explicit non-import of detector semantics, stress-energy, action, and benchmark",
]

PROMOTION_BLOCKS = [
    "does not adopt `PositiveMSProfile_v1`",
    "source-side matter semantics",
    "detector semantics",
    "stress-energy semantics",
    "matter action",
    "a coupling law",
    "Einstein equations",
    "benchmark recovery",
    "completed derivation",
]

MACHINE_FLAGS = [
    "requires_source_side_matter_record_domain: true",
    "requires_source_side_semantic_labels_or_structures: true",
    "requires_admissibility_conditions: true",
    "requires_equivalence_or_separation_relation: true",
    "requires_stability_under_source_relabeling_or_finite_variation: true",
    "requires_fail_closed_obstruction_branches: true",
    "requires_relation_to_PositiveMSProfile_v1: true",
    "requires_relation_to_RR_E_transport_or_invariance: true",
    "requires_explicit_non_import_of_detector_stress_energy_action_benchmark: true",
    "no_physics_promotion_authorized: true",
    "no_source_law_adoption_authorized: true",
    "no_matter_semantics_adoption_authorized: true",
    "no_benchmark_promotion_authorized: true",
    "no_completed_derivation_authorized: true",
    'next_required_packet: "P12-T03 no-target hygiene linter and examples integration"',
]


def digest(rel: str) -> str:
    return hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()


def load_handoff_task_type() -> str:
    text = (REPO_ROOT / HANDOFF_PATH).read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("task_type:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def normalize(text: str) -> str:
    return " ".join(text.split())


def validate() -> dict[str, object]:
    errors: list[str] = []
    doc = (REPO_ROOT / DOC_PATH).read_text(encoding="utf-8")
    normalized_doc = normalize(doc)

    missing_elements = [item for item in REQUIRED_ELEMENTS if normalize(item) not in normalized_doc]
    if missing_elements:
        errors.append(f"missing required positive elements: {missing_elements}")

    missing_blocks = [item for item in PROMOTION_BLOCKS if item not in doc]
    if missing_blocks:
        errors.append(f"missing promotion boundaries: {missing_blocks}")

    missing_flags = [item for item in MACHINE_FLAGS if item not in doc]
    if missing_flags:
        errors.append(f"missing machine flags: {missing_flags}")

    if "No no-target, no-detector, no-stress-energy, no-action, no-benchmark, or" not in doc:
        errors.append("missing negative-certificate substitution boundary")

    if load_handoff_task_type() != "v14_p12_t03_no_target_hygiene_linter_examples_integration":
        errors.append("handoff-0493 must route to P12-T03 no-target hygiene linter and examples integration")

    return {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260702-040",
        "validator_id": "validate_p12_t02_positive_semantics_requirement",
        "doc_path": DOC_PATH,
        "doc_hash": digest(DOC_PATH),
        "plan_path": PLAN_PATH,
        "plan_hash": digest(PLAN_PATH),
        "required_positive_element_count": len(REQUIRED_ELEMENTS),
        "promotion_boundary_count": len(PROMOTION_BLOCKS),
        "machine_flag_count": len(MACHINE_FLAGS),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
