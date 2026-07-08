#!/usr/bin/env python3
"""Validate the v18 P7-T01 support formalization target selector packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260708-019"
ARTIFACTS = TASK_DIR / "artifacts"
COMPLETION = TASK_DIR / "jobs/completions/AJC-AJ-RT-20260708-019-001.yaml"
REPORT = ARTIFACTS / "p7_t01_support_formalization_target_selector_v18_report.json"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    required_paths = [
        TASK_DIR / "00_TASK.yaml",
        TASK_DIR / "DDR-20260708-019.md",
        TASK_DIR / "roles/theoretical-continuation-selector@0.1.0--RT-20260708-019.yaml",
        TASK_DIR / "jobs/AJ-RT-20260708-019-001.yaml",
        COMPLETION,
        ARTIFACTS / "support_formalization_target_selector_v18_receipt.md",
        ARTIFACTS / "child_phys_math_support_formalization_target_selector_v18.yaml",
        ARTIFACTS / "child_phys_phil_support_formalization_target_selector_v18.yaml",
        ARTIFACTS / "parent_conflict_review_support_formalization_target_selector_v18.yaml",
        ARTIFACTS / "parent_fusion_notes_support_formalization_target_selector_v18.md",
    ]

    errors: list[str] = []
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(ROOT)}")

    completion = load_yaml(COMPLETION) if COMPLETION.exists() else {}
    decision = completion.get("theoretical_decision_output", {})
    selector = completion.get("support_formalization_target_selector", {})
    candidates = selector.get("candidate_targets", [])
    selected = [item for item in candidates if item.get("disposition") == "selected"]

    if decision.get("selected_formalization_target") != "typed_EqSrc_orbit_checker":
        errors.append("selected_formalization_target must be typed_EqSrc_orbit_checker")
    if decision.get("selected_next_plan_task_id") != "P7-T02":
        errors.append("selected_next_plan_task_id must be P7-T02")
    if decision.get("selected_next_packet_type") != "bounded_theoretical_calculation":
        errors.append("selected_next_packet_type must be bounded_theoretical_calculation")
    if decision.get("preserves_claim_blocks") is not True:
        errors.append("preserves_claim_blocks must be true")
    if decision.get("requires_human_gate") is not False:
        errors.append("requires_human_gate must be false")

    if len(selected) != 1:
        errors.append(f"expected exactly one selected candidate, found {len(selected)}")
    elif selected[0].get("target_id") != "typed_EqSrc_orbit_checker":
        errors.append("the selected candidate row must be typed_EqSrc_orbit_checker")

    claim_boundary = completion.get("claim_boundary", {})
    for key in (
        "proof_authority",
        "physics_promotion_authorized",
        "source_law_adopted",
        "matter_coupling_derived",
        "einstein_equations_derived",
        "benchmark_promoted",
        "completed_derivation_claimed",
    ):
        if claim_boundary.get(key) is not False:
            errors.append(f"claim_boundary.{key} must be false")

    receipt_text = (ARTIFACTS / "support_formalization_target_selector_v18_receipt.md").read_text(
        encoding="utf-8"
    ) if (ARTIFACTS / "support_formalization_target_selector_v18_receipt.md").exists() else ""
    for phrase in [
        "typed_EqSrc_orbit_checker",
        "support_only: true",
        "proof_authority: false",
        "P7-T02",
    ]:
        if phrase not in receipt_text:
            errors.append(f"receipt missing phrase: {phrase}")

    report = {
        "schema_id": "p7_t01_support_formalization_target_selector_v18_validation_report_v1",
        "task_id": "RT-20260708-019",
        "job_id": "AJ-RT-20260708-019-001",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "selected_formalization_target": decision.get("selected_formalization_target"),
        "selected_next_plan_task_id": decision.get("selected_next_plan_task_id"),
        "support_only": claim_boundary.get("support_only"),
        "proof_authority": claim_boundary.get("proof_authority"),
        "physics_promotion_authorized": claim_boundary.get("physics_promotion_authorized"),
        "candidate_count": len(candidates),
        "selected_candidate_count": len(selected),
    }

    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
