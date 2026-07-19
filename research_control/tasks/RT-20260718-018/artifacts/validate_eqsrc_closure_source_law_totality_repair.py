#!/usr/bin/env python3
"""Validate the RT-20260718-018 EqSrc accepted-totality repair packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-018"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_family_closure_source_law_candidate_v2.tex"
REPORT_PATH = ARTIFACT_ROOT / "eqsrc_closure_source_law_totality_repair_validation.json"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-FAMILY-CLOSURE-SOURCE-LAW-CANDIDATE-V2"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-018-PARENT-FUSION-NOTES-"
    "EQSRC-CLOSURE-TOTALITY-REPAIR"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-018-EQSRC-CLOSURE-"
    "SOURCE-LAW-TOTALITY-REPAIR-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_closure_totality_repair.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_closure_totality_repair.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_closure_totality_repair.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_closure_totality_repair.md",
    ARTIFACT_ROOT / "eqsrc_closure_source_law_totality_repair_receipt.md",
]

REQUIRED_SECTIONS = [
    "Control Status and Repair Question",
    "Closed Typed Source Grammar",
    "Candidate Accepted-Totality Law",
    "Conditional Equivalence Theorem",
    "Obstruction Repair and Fail-Closed Branches",
    "Distance-to-GR Matrix and Freeze Evaluation",
    "Authority Boundary and Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "candidate_status: proposal-only",
    "OBST-EQSRC-CLOSURE-TOTALITY-001",
    "statement_level_totality_repair_supplied",
    "accepted_identity_totality: explicit",
    "accepted_inverse_totality: explicit",
    "accepted_composition_totality: explicit",
    "closed_and_target_free_by_construction",
    "Accepted identity totality",
    "Accepted inverse totality",
    "Accepted composition totality",
    "Closed provenance term algebra",
    "Unit compatibility",
    "Inverse compatibility",
    "Associativity compatibility",
    "Ledger congruence and constructor closure",
    "Equivalence under the repaired candidate law",
    "blocked\\_adoption\\_open\\_continuation",
    "general_EqSrc_discharged: false",
    "RetainH_adopted: false",
    "GenH_adopted: false",
    "fresh_smuggling_auditor_review",
    "smuggling-auditor@0.2.0",
    "The Distance-to-GR ledger is unchanged",
]

FORBIDDEN_SNIPPETS = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "M_src is adopted",
    "source law is adopted",
    "canonical ontology is modified",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
    "global theory is rejected",
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


def require_markers(path: Path, markers: list[str], errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing required artifact: {path.relative_to(REPO_ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{path.name}: missing marker {marker!r}")


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

    require_markers(
        ARTIFACT_ROOT / "child_phys_math_eqsrc_closure_totality_repair.yaml",
        [
            "child_phys_math",
            "accepted-identity",
            "accepted-inverse",
            "accepted-composition",
            "conditional",
            "completed",
        ],
        errors,
    )
    require_markers(
        ARTIFACT_ROOT / "child_phys_phil_eqsrc_closure_totality_repair.yaml",
        [
            "child_phys_phil",
            "blocked_adoption_open_continuation",
            "source",
            "fresh",
            "completed",
        ],
        errors,
    )
    require_markers(
        ARTIFACT_ROOT / "parent_conflict_review_eqsrc_closure_totality_repair.yaml",
        ['status: "resolved"', "unresolved_conflicts: []"],
        errors,
    )
    require_markers(
        ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_closure_totality_repair.md",
        [
            "proposal-only",
            "OBST-EQSRC-CLOSURE-TOTALITY-001",
            "blocked_adoption_open_continuation",
            "Smuggling Auditor",
        ],
        errors,
    )
    require_markers(
        ARTIFACT_ROOT / "eqsrc_closure_source_law_totality_repair_receipt.md",
        [
            "statement_level_totality_repair_supplied",
            "no_distance_delta",
            "Smuggling Auditor",
        ],
        errors,
    )

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
        "task_id": "RT-20260718-018",
        "plan_task_id": "ordinary_eqsrc_closure_source_law_candidate_accepted_totality_repair",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "candidate_status": "proposal-only",
        "adoption_status": "blocked_adoption_open_continuation",
        "repair_target": "OBST-EQSRC-CLOSURE-TOTALITY-001",
        "repair_result": "statement_level_totality_repair_supplied",
        "general_eqsrc_discharged": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "distance_to_gr_effect": "no_distance_delta",
        "next_required_role": "smuggling-auditor@0.2.0",
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
