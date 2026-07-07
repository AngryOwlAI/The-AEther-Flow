#!/usr/bin/env python3
"""Validate the v18 P3-T05 EqSrc family-closure Refuter stress artifact."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260707-023"
TEX_PATH = TASK_ROOT / "artifacts/eqsrc_family_closure_refuter_stress_v1.tex"
COMPLETION_PATH = TASK_ROOT / "jobs/completions/AJC-AJ-RT-20260707-023-001.yaml"
REPORT_PATH = TASK_ROOT / "artifacts/eqsrc_family_closure_refuter_stress_validation.json"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-V18-P3-T05-EQSRC-FAMILY-CLOSURE-REFUTER-STRESS-V1"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260707-023-PARENT-FUSION-NOTES-"
    "EQSRC-FAMILY-CLOSURE-REFUTER-STRESS"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260707-023-EQSRC-FAMILY-CLOSURE-"
    "REFUTER-STRESS-RECEIPT"
)

REQUIRED_SECTIONS = [
    "Control Status",
    "Inputs and Scope",
    "Stress Method",
    "Stress Mode Matrix",
    "Missing-Inverse Countermodel Retained",
    "Missing-Composition Countermodel",
    "Ledger-Weakening Witness",
    "RetainH and GenH Extension Pressure",
    "Target and Process Authority Attacks",
    "Refuter Obstruction Record",
    "Stress Result",
    "Distance-to-GR Effect",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

STRESS_MODE_TOKENS = [
    "remove_family_identity_closure",
    "remove_inverse_closure",
    "remove_composition_closure",
    "weaken_invariant_ledger",
    "expand_source_family_without_GenH",
    "apply_H_retention_without_RetainH",
    "replace_source_invariant_with_target_success",
    "allow_missing_negative_controls",
    "import_metric_or_detector_protocol",
    "treat_theorem_candidate_as_adopted_EqSrc",
]

REQUIRED_TOKENS = [
    "stress_result: scoped_obstruction",
    "refuter_classification: scoped_obstruction",
    "loop_classification: scoped_obstruction",
    "target_derivation_milestone: source_equivalence_eqsrc",
    "minimal_countermodel_available: true",
    "next_route: P3-T06",
    "general_EqSrc_adopted: false",
    "RetainH_adopted: false",
    "GenH_adopted: false",
    "source_law_adopted: false",
    "distance_to_gr_delta: no_distance_delta",
    "Missing composition blocks transitivity",
    "refuter_obstruction_record:",
    'obstruction_id: "OB-V18-P3T05-EQSRC-FAMILY-CLOSURE-001"',
    'global_no_go_claim_authorized: false',
    'future_source_extension_impossibility_authorized: false',
    'freeze_decision: "not_frozen"',
    "same_milestone_continuation_status: blocked_adoption_open_continuation",
    "selected_stress_result: scoped_obstruction",
    "minimal_countermodel_survives: true",
]

FORBIDDEN_SNIPPETS = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "source law is adopted",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
    "claims completed derivation",
    "future source-extension impossibility follows from this stress",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_single_row(
    errors: list[str],
    rows: list[dict[str, str]],
    object_id: str,
    registry_name: str,
) -> dict[str, str]:
    matches = [row for row in rows if row.get("object_id") == object_id]
    if len(matches) != 1:
        errors.append(f"expected exactly one {registry_name} row for {object_id}")
        return {}
    return matches[0]


def main() -> int:
    errors: list[str] = []

    if not TEX_PATH.exists():
        errors.append(f"missing TeX artifact: {TEX_PATH.relative_to(REPO_ROOT)}")
        tex_text = ""
        tex_hash = ""
    else:
        tex_text = TEX_PATH.read_text(encoding="utf-8")
        tex_hash = sha256(TEX_PATH)

    if not COMPLETION_PATH.exists():
        errors.append(f"missing completion: {COMPLETION_PATH.relative_to(REPO_ROOT)}")
        completion_text = ""
    else:
        completion_text = COMPLETION_PATH.read_text(encoding="utf-8")

    for section in REQUIRED_SECTIONS:
        if section not in tex_text:
            errors.append(f"missing required section: {section}")

    for token in STRESS_MODE_TOKENS:
        if token not in tex_text:
            errors.append(f"missing stress mode token: {token}")

    for token in REQUIRED_TOKENS:
        if token not in tex_text:
            errors.append(f"missing required token: {token}")

    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in tex_text:
            errors.append(f"forbidden promotional snippet present: {snippet}")

    for token in [
        "refuter_obstruction_record:",
        "target_milestone: \"source_equivalence_eqsrc\"",
        "minimal_countermodel_available: true",
        "freeze_criteria_status:",
        "route_cycle_control:",
    ]:
        if token not in completion_text:
            errors.append(f"completion missing required token: {token}")

    if TEX_REGISTRY_PATH.exists():
        tex_rows = read_csv(TEX_REGISTRY_PATH)
        tex_row = require_single_row(errors, tex_rows, TEX_OBJECT_ID, "TeX registry")
        if tex_row:
            expected_path = TEX_PATH.relative_to(REPO_ROOT).as_posix()
            if tex_row.get("path") != expected_path:
                errors.append("TeX registry path mismatch")
            if tex_row.get("source_hash") != tex_hash:
                errors.append("TeX registry source_hash mismatch")
            if tex_row.get("claim_status") != "proposal":
                errors.append("TeX registry claim_status must remain proposal")
            if tex_row.get("research_status") != "draft":
                errors.append("TeX registry research_status must remain draft")
            if tex_row.get("ontology_promotion_status") != "not_applicable":
                errors.append("TeX registry ontology_promotion_status must be not_applicable")
            if tex_row.get("pdf_required") != "false":
                errors.append("TeX registry pdf_required must remain false")
    else:
        errors.append("missing TEX_SOURCE_REGISTRY.csv")

    if MARKDOWN_REGISTRY_PATH.exists():
        markdown_rows = read_csv(MARKDOWN_REGISTRY_PATH)
        require_single_row(errors, markdown_rows, FUSION_MD_OBJECT_ID, "Markdown registry")
        require_single_row(errors, markdown_rows, RECEIPT_MD_OBJECT_ID, "Markdown registry")
    else:
        errors.append("missing MARKDOWN_SOURCE_REGISTRY.csv")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260707-023",
        "plan_task_id": "P3-T05",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "stress_result": "scoped_obstruction",
        "refuter_classification": "scoped_obstruction",
        "target_derivation_milestone": "source_equivalence_eqsrc",
        "minimal_countermodel_available": True,
        "general_eqsrc_adopted": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "distance_to_gr_delta": "no_distance_delta",
        "next_route": "P3-T06",
        "errors": errors,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
