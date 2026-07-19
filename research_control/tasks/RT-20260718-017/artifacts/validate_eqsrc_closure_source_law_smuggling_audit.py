#!/usr/bin/env python3
"""Validate the RT-20260718-017 EqSrc closure source-law smuggling audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-017"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_closure_source_law_smuggling_audit_v1.tex"
REPORT_PATH = ARTIFACT_ROOT / "eqsrc_closure_source_law_smuggling_audit_validation.json"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-CLOSURE-SOURCE-LAW-SMUGGLING-AUDIT-V1"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-017-PARENT-FUSION-NOTES-"
    "EQSRC-CLOSURE-SOURCE-LAW-SMUGGLING-AUDIT"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-017-EQSRC-CLOSURE-"
    "SOURCE-LAW-SMUGGLING-AUDIT-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_closure_source_law_audit.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_closure_source_law_audit.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_closure_source_law_audit.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_closure_source_law_audit.md",
    ARTIFACT_ROOT / "eqsrc_closure_source_law_smuggling_audit_receipt.md",
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Artifact and Question Under Audit",
    "Audit Method",
    "Source-Purity Audit",
    "Formal Sufficiency Audit",
    "Minimal Source-Side Countermodels",
    "Exact Obstruction",
    "Required Repair",
    "Audit Result",
    "Distance-to-GR Effect",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "source_pure_textually_formally_insufficient_repair_required",
    "source_purity_result: pass_with_semantic_guard",
    "formal_sufficiency_result: fail_totality_not_stated",
    "OBST-EQSRC-CLOSURE-TOTALITY-001",
    "source\\_pure\\_as\\_written",
    "formally\\_insufficient\\_as\\_written",
    "repair\\_required\\_before\\_refuter\\_stress",
    "accepted identity token",
    "necessary condition",
    "Reflexivity countermodel",
    "Symmetry countermodel",
    "Transitivity countermodel",
    "source-invariant ledger annotations",
    "permitted proxy incidence",
    "negative controls",
    "blocked\\_adoption\\_open\\_continuation",
    "ontology-formalizer@0.2.0",
    "general_EqSrc_discharged: false",
    "RetainH_adopted: false",
    "GenH_adopted: false",
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
        "task_id": "RT-20260718-017",
        "plan_task_id": "ordinary_eqsrc_closure_source_law_candidate_smuggling_audit",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "audit_result": "source_pure_textually_formally_insufficient_repair_required",
        "source_purity_result": "pass_with_semantic_guard",
        "formal_sufficiency_result": "fail_totality_not_stated",
        "obstruction_id": "OBST-EQSRC-CLOSURE-TOTALITY-001",
        "general_eqsrc_discharged": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "distance_to_gr_delta": "obstruction_recorded_no_ledger_change",
        "next_required_role": "ontology-formalizer@0.2.0",
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
