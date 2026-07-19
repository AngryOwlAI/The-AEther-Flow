#!/usr/bin/env python3
"""Validate the RT-20260718-021 EqSrc closure candidate v3 audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-021"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_smuggling_audit.tex"
REPORT_PATH = ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_smuggling_audit_validation.json"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-CLOSURE-SOURCE-LAW-V3-SMUGGLING-AUDIT"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-021-PARENT-FUSION-NOTES-"
    "EQSRC-CLOSURE-V3-SMUGGLING-AUDIT"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-021-EQSRC-CLOSURE-"
    "SOURCE-LAW-V3-SMUGGLING-AUDIT-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_closure_v3_smuggling_audit.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_closure_v3_smuggling_audit.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_closure_v3_smuggling_audit.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_closure_v3_smuggling_audit.md",
    ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_smuggling_audit_receipt.md",
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Audit Questions and Method",
    "Typed Declaration and Dependency Audit",
    "Congruence and Acceptance Audit",
    "Accepted-Totality and Conditional-Theorem Audit",
    "Semantic Source-Factorization Audit",
    "Target and Process Authority Audit",
    "Minimal Mathematical Witnesses",
    "Audit Result and Open Burdens",
    "Source-Extension and Adoption Classification",
    "Distance-to-GR Status",
    "Freeze Evaluation",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "statement_level_smuggling_audit_pass_with_instantiation_provenance_limit",
    "declaration_closure_result: pass_at_statement_level",
    "dependency_acyclicity_result: pass",
    "congruence_invariance_result: pass",
    "source_purity_result: pass_as_written_admissibility_condition",
    "accepted_totality_result: conditional_equivalence_core_valid",
    "Certificate-acceptance congruence",
    "Acyclic factorization propagation",
    "One-object source-only consistency witness",
    "Coarse equivalence does not imply the full law",
    "OBST-EQSRC-CLOSURE-SIGNATURE-001",
    "blocked\\_adoption\\_open\\_continuation",
    "refuter@0.2.0",
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
        "task_id": "RT-20260718-021",
        "plan_task_id": "ordinary_eqsrc_closure_source_law_candidate_v3_smuggling_audit",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "audit_result": (
            "statement_level_smuggling_audit_pass_with_"
            "instantiation_provenance_limit"
        ),
        "declaration_closure_result": "pass_at_statement_level",
        "dependency_acyclicity_result": "pass",
        "congruence_invariance_result": "pass",
        "source_purity_result": "pass_as_written_admissibility_condition",
        "accepted_totality_result": "conditional_equivalence_core_valid",
        "current_ontology_instantiation": "not_established",
        "conservativity_result": "not_established",
        "general_eqsrc_discharged": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "distance_to_gr_delta": "candidate_audited_no_ledger_change",
        "next_required_role": "refuter@0.2.0",
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
