#!/usr/bin/env python3
"""Validate the RT-20260718-022 EqSrc closure candidate v3 Refuter stress."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-022"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_refuter_stress.tex"
REPORT_PATH = (
    ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_refuter_stress_validation.json"
)
COMPLETION_PATH = (
    TASK_ROOT / "jobs/completions/AJC-AJ-RT-20260718-022-001.yaml"
)
HANDOFF_PATH = REPO_ROOT / "research_control/handoffs/handoff-0747.yaml"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-CLOSURE-SOURCE-LAW-V3-REFUTER-STRESS"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-022-PARENT-FUSION-NOTES-"
    "EQSRC-CLOSURE-V3-REFUTER-STRESS"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-022-EQSRC-CLOSURE-"
    "SOURCE-LAW-V3-REFUTER-STRESS-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_closure_v3_refuter_stress.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_closure_v3_refuter_stress.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_closure_v3_refuter_stress.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_closure_v3_refuter_stress.md",
    ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_refuter_stress_receipt.md",
    COMPLETION_PATH,
    HANDOFF_PATH,
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Inputs and Stress Method",
    "Nontrivial Two-Object Source-Only Witness",
    "Transitive Source-Root Provenance Stress",
    "Malformed Definitions and Typed Fail Closure",
    "Congruence, Accepted Totality, and Coherence",
    "Degenerate-Model Pressure",
    "Law-Preserving Finite-Variation Countermodel",
    "Refuter Obstruction Record",
    "Stress Result and Loop Classification",
    "Source-Extension and Adoption Classification",
    "Distance-to-GR Status",
    "Freeze and Route-Cycle Evaluation",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "stress_result: scoped_obstruction",
    "refuter_loop_classification: scoped_obstruction",
    "OBST-EQSRC-CLOSURE-V3-VARIATION-SELECTOR-001",
    "finite_congruence_quotient_witness",
    "Two-entry source-decision variation",
    "finite-congruence-quotient",
    "meta_level_model_rejection",
    "freeze_decision: \"not_frozen\"",
    "candidate-constructor@0.2.0",
    "blocked_adoption_open_continuation",
    "general_EqSrc_discharged: false",
    "RetainH_adopted: false",
    "GenH_adopted: false",
    "distance_to_gr_ledger_changed: false",
]

FORBIDDEN_SNIPPETS = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "source law is adopted",
    "canonical ontology is modified",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
    "global theory is rejected",
    "future source extension is impossible",
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required artifact: {path.relative_to(REPO_ROOT)}")

    if TEX_PATH.exists():
        tex_text = TEX_PATH.read_text(encoding="utf-8")
        tex_hash = sha256(TEX_PATH)
    else:
        tex_text = ""
        tex_hash = ""
        errors.append(f"missing TeX artifact: {TEX_PATH.relative_to(REPO_ROOT)}")

    for section in REQUIRED_SECTIONS:
        if section not in tex_text:
            errors.append(f"missing required section: {section}")
    for token in REQUIRED_TOKENS:
        if token not in tex_text:
            errors.append(f"missing required token: {token}")
    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in tex_text:
            errors.append(f"forbidden promotional snippet present: {snippet}")

    completion: dict[str, object] = {}
    if COMPLETION_PATH.exists():
        completion = yaml.safe_load(COMPLETION_PATH.read_text(encoding="utf-8"))
        if completion.get("refuter_loop_classification") != "scoped_obstruction":
            errors.append("completion refuter_loop_classification must be scoped_obstruction")
        stress_result = completion.get("stress_result", {})
        if not isinstance(stress_result, dict) or (
            stress_result.get("result_type") != "scoped_obstruction"
        ):
            errors.append("completion stress_result.result_type must be scoped_obstruction")
        progress = completion.get("physics_progress_status", {})
        if not isinstance(progress, dict) or (
            progress.get("status") != "precise_obstruction_found"
        ):
            errors.append(
                "completion physics_progress_status.status must be "
                "precise_obstruction_found"
            )
        obstruction = completion.get("refuter_obstruction_record", {})
        if not isinstance(obstruction, dict) or (
            obstruction.get("obstruction_id")
            != "OBST-EQSRC-CLOSURE-V3-VARIATION-SELECTOR-001"
        ):
            errors.append("completion Refuter obstruction record mismatch")
        freeze = completion.get("freeze_criteria_status", {})
        if not isinstance(freeze, dict) or (
            freeze.get("freeze_decision") != "not_frozen"
        ):
            errors.append("completion freeze decision must be not_frozen")
        if completion.get("next_recommended_role") != "candidate-constructor@0.2.0":
            errors.append("completion next recommended role mismatch")

    tex_rows = read_csv(TEX_REGISTRY_PATH)
    tex_row = require_single_row(errors, tex_rows, TEX_OBJECT_ID, "TeX registry")
    if tex_row:
        if tex_row.get("path") != TEX_PATH.relative_to(REPO_ROOT).as_posix():
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

    markdown_rows = read_csv(MARKDOWN_REGISTRY_PATH)
    require_single_row(errors, markdown_rows, FUSION_MD_OBJECT_ID, "Markdown registry")
    require_single_row(errors, markdown_rows, RECEIPT_MD_OBJECT_ID, "Markdown registry")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260718-022",
        "plan_task_id": (
            "ordinary_eqsrc_closure_source_law_candidate_v3_refuter_stress"
        ),
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "stress_result": "scoped_obstruction",
        "refuter_loop_classification": "scoped_obstruction",
        "obstruction_id": "OBST-EQSRC-CLOSURE-V3-VARIATION-SELECTOR-001",
        "nontrivial_model_result": "finite_congruence_quotient_witness",
        "finite_variation_result": "two_entry_selector_countermodel",
        "current_ontology_instantiation": "not_established",
        "general_eqsrc_discharged": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "distance_to_gr_delta": "scoped_obstruction_no_ledger_change",
        "freeze_decision": "not_frozen",
        "next_required_role": "candidate-constructor@0.2.0",
        "errors": errors,
    }
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
