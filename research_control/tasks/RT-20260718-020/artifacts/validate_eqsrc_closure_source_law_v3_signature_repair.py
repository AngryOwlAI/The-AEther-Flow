#!/usr/bin/env python3
"""Validate the RT-20260718-020 EqSrc v3 signature-repair packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-020"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_family_closure_source_law_candidate_v3.tex"
REPORT_PATH = ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_signature_repair_validation.json"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-FAMILY-CLOSURE-SOURCE-LAW-CANDIDATE-V3"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-020-PARENT-FUSION-NOTES-"
    "EQSRC-CLOSURE-V3-SIGNATURE-REPAIR"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-020-EQSRC-CLOSURE-"
    "SOURCE-LAW-V3-SIGNATURE-REPAIR-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_closure_v3_signature_repair.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_closure_v3_signature_repair.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_closure_v3_signature_repair.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_closure_v3_signature_repair.md",
    ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_signature_repair_receipt.md",
]

REQUIRED_SECTIONS = [
    "Control Status and Repair Question",
    "Exact Closed Typed Source Signature",
    "Acyclic Acceptance and Source-Purity Guard",
    "Candidate Accepted-Totality and Coherence Law",
    "Conditional Equivalence Theorem",
    "Obstruction Repair and Fail-Closed Branches",
    "Distance-to-GR Matrix and Freeze Evaluation",
    "Authority Boundary and Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "candidate_status: proposal-only",
    "OBST-EQSRC-CLOSURE-SIGNATURE-001",
    "statement_level_signature_and_noncircularity_repair_supplied",
    "proxy_constructor_signature: explicit_and_typed",
    "component_congruences: explicit_and_typed",
    "negative_control_domain: explicit_raw_certificate_fiber",
    "acceptance_dependency_order: finite_acyclic_rank_0_through_rank_4",
    "acceptance_recursion: forbidden",
    "declaration_closed_pending_fresh_audit",
    "Accepted identity totality",
    "Accepted inverse totality",
    "Accepted composition totality",
    "Acyclic acceptance is total and non-circular",
    "Declaration closure at statement level",
    "Complete no-target and no-process guard",
    "blocked\\_adoption\\_open\\_continuation",
    "general_EqSrc_discharged: false",
    "RetainH_adopted: false",
    "GenH_adopted: false",
    "The Distance-to-GR ledger is unchanged",
    "fresh bounded",
    "smuggling-auditor@0.2.0",
]

FORBIDDEN_SNIPPETS = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "M_src is adopted",
    "the source law is adopted",
    "canonical ontology is modified",
    "Einstein equations are derived",
    "the benchmark is promoted",
    "this is a completed derivation",
    "the global theory is rejected",
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


def require_order(text: str, markers: list[str], errors: list[str]) -> None:
    positions = [text.find(marker) for marker in markers]
    if any(position < 0 for position in positions):
        return
    if positions != sorted(positions):
        errors.append(f"dependency-order markers are not ordered: {markers}")


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

    require_order(
        tex_text,
        [
            "Rank-0 source carriers and comparisons",
            "Rank-1 total ledger and proxy constructors",
            "Rank-2 raw certificate fibers and constructors",
            "Rank-2 source-only decision maps",
            "Rank-3 acceptance",
            "Proposal-only candidate closure law v3",
        ],
        errors,
    )

    require_markers(
        ARTIFACT_ROOT / "child_phys_math_eqsrc_closure_v3_signature_repair.yaml",
        [
            "child_phys_math",
            "typed_signature",
            "acyclic",
            "conditional_equivalence",
            "completed",
        ],
        errors,
    )
    require_markers(
        ARTIFACT_ROOT / "child_phys_phil_eqsrc_closure_v3_signature_repair.yaml",
        [
            "child_phys_phil",
            "blocked_adoption_open_continuation",
            "no_target_no_process_guard",
            "fresh_smuggling_auditor",
            "completed",
        ],
        errors,
    )
    require_markers(
        ARTIFACT_ROOT / "parent_conflict_review_eqsrc_closure_v3_signature_repair.yaml",
        ['status: "resolved"', "unresolved_conflicts: []"],
        errors,
    )
    require_markers(
        ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_closure_v3_signature_repair.md",
        [
            "proposal-only",
            "OBST-EQSRC-CLOSURE-SIGNATURE-001",
            "rank-0",
            "blocked_adoption_open_continuation",
            "Smuggling Auditor",
        ],
        errors,
    )
    require_markers(
        ARTIFACT_ROOT / "eqsrc_closure_source_law_v3_signature_repair_receipt.md",
        [
            "statement_level_signature_and_noncircularity_repair_supplied",
            "conditional_theorem_candidate",
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
        "task_id": "RT-20260718-020",
        "plan_task_id": "ordinary_eqsrc_closure_source_law_candidate_v3_signature_repair",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "candidate_status": "proposal-only",
        "adoption_status": "blocked_adoption_open_continuation",
        "repair_target": "OBST-EQSRC-CLOSURE-SIGNATURE-001",
        "repair_result": "statement_level_signature_and_noncircularity_repair_supplied",
        "signature_closure_result": "declaration_closed_pending_fresh_audit",
        "acceptance_dependency_result": "finite_acyclic_rank_0_through_rank_4",
        "conditional_equivalence_result": "theorem_with_hypotheses_and_proof",
        "general_eqsrc_discharged": False,
        "source_law_adopted": False,
        "distance_to_gr_effect": "no_distance_delta",
        "next_required_role": "smuggling-auditor@0.2.0",
        "errors": errors,
    }
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
        for error in errors:
            print(f"ERROR: {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
