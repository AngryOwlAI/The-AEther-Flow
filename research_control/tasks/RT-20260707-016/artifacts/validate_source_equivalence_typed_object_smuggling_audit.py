#!/usr/bin/env python3
"""Validate the v18 P2-T04 source-equivalence typed object smuggling audit."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260707-016"
TEX_PATH = TASK_ROOT / "artifacts/source_equivalence_typed_object_smuggling_audit_v1.tex"
REPORT_PATH = TASK_ROOT / "artifacts/source_equivalence_typed_object_smuggling_audit_validation.json"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-V18-P2-T04-SOURCE-EQUIVALENCE-TYPED-OBJECT-SMUGGLING-AUDIT-V1"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260707-016-PARENT-FUSION-NOTES-"
    "SOURCE-EQUIVALENCE-TYPED-OBJECT-SMUGGLING-AUDIT"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260707-016-SOURCE-EQUIVALENCE-TYPED-"
    "OBJECT-SMUGGLING-AUDIT-RECEIPT"
)

REQUIRED_SECTIONS = [
    "Control Status",
    "Artifact Under Audit",
    "Audit Method",
    "Target-Import Audit Matrix",
    "Process-Authority Audit Matrix",
    "Source-Purity Lemma",
    "Audit Result",
    "Residual Risks",
    "Distance-to-GR Effect",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "source\\_pure\\_as\\_written",
    "target topology import",
    "target smooth atlas import",
    "target Lorentzian metric import",
    "proper-time normalization import",
    "detector protocol import",
    "empirical calibration import",
    "stress-energy semantics import",
    "matter-action import",
    "Einstein-equation premise import",
    "benchmark behavior import",
    "validation status as premise",
    "registry metadata as theorem premise",
    "role identity as theorem premise",
    "handoff state as theorem premise",
    "commit state as theorem premise",
    "generated derivative as theorem premise",
    "not detected",
    "does not discharge general",
    "does not adopt",
    "No Distance-to-GR ledger row is changed",
    "P2-T05 Refuter stress",
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

    for section in REQUIRED_SECTIONS:
        if section not in tex_text:
            errors.append(f"missing required section: {section}")

    for token in REQUIRED_TOKENS:
        if token not in tex_text:
            errors.append(f"missing required token: {token}")

    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in tex_text:
            errors.append(f"forbidden promotional snippet present: {snippet}")

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
            if tex_row.get("ontology_promotion_status") != "not_applicable":
                errors.append("TeX registry ontology_promotion_status must be not_applicable")
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
        "task_id": "RT-20260707-016",
        "plan_task_id": "P2-T04",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "audit_result": "source_pure_as_written",
        "general_eqsrc_discharged": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "distance_to_gr_delta": "no_distance_delta",
        "next_route": "P2-T05",
        "errors": errors,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
