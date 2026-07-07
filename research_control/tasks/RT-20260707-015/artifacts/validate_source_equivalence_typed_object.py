#!/usr/bin/env python3
"""Validate the v18 P2-T03 source-equivalence typed object packet."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260707-015"
TEX_PATH = TASK_ROOT / "artifacts/source_equivalence_typed_object_v1.tex"
REPORT_PATH = TASK_ROOT / "artifacts/source_equivalence_typed_object_validation.json"
SOURCE_EQ_REGISTRY_PATH = REPO_ROOT / "registries/SOURCE_EQUIVALENCE_OBJECT_REGISTRY.csv"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"

OBJECT_ID = "SEO-V18-P2-T03-SOURCE-EQUIVALENCE-TYPED-OBJECT-V1"
TEX_OBJECT_ID = "TEX-V18-P2-T03-SOURCE-EQUIVALENCE-TYPED-OBJECT-V1"

REQUIRED_SECTIONS = [
    "Control Status",
    "Prior Record-Local Theorem",
    "Typed Source Family",
    "Source Objects",
    "Admissible Source Morphisms or Relabelings",
    "Invariant Ledger",
    "Source-Only Comparison Rule",
    "Identity Closure",
    "Inverse Closure",
    "Composition Closure",
    "\\(\\RetainH\\) Boundary",
    "\\(\\GenH\\) Boundary",
    "No-Target Guard",
    "Family-Level Burden",
    "Countermodel Slots",
    "Distance-to-GR Effect",
    "Forbidden Conclusions",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "SourceEquivalenceTypedObject",
    "EqSrc_T",
    "draft/control",
    "no proof authority",
    "does not discharge general",
    "does not adopt",
    "target topology",
    "target metric",
    "detector protocol",
    "stress-energy",
    "matter action",
    "benchmark behavior",
    "registry metadata",
    "validator status",
    "countermodel",
    "no distance delta",
]

FORBIDDEN_SNIPPETS = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "source law is adopted",
    "Einstein equations are derived",
    "is a completed derivation",
    "claims completed derivation",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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

    if not SOURCE_EQ_REGISTRY_PATH.exists():
        errors.append("missing SOURCE_EQUIVALENCE_OBJECT_REGISTRY.csv")
        source_eq_rows: list[dict[str, str]] = []
    else:
        source_eq_rows = read_csv(SOURCE_EQ_REGISTRY_PATH)
    matching_source_eq_rows = [row for row in source_eq_rows if row.get("object_id") == OBJECT_ID]
    if len(matching_source_eq_rows) != 1:
        errors.append(f"expected exactly one source-equivalence object row for {OBJECT_ID}")
    else:
        row = matching_source_eq_rows[0]
        expected = {
            "artifact_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
            "task_id": "RT-20260707-015",
            "source_family_symbol": "F_src",
            "object_set_status": "explicit",
            "morphism_status": "explicit",
            "invariant_ledger_status": "partial",
            "comparison_rule_status": "explicit",
            "identity_closure_status": "supplied",
            "inverse_closure_status": "missing",
            "composition_closure_status": "missing",
            "retainh_status": "required",
            "genh_status": "required",
            "no_target_guard_status": "explicit",
            "proof_state": "draft_control",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                errors.append(f"source-equivalence row {key}={row.get(key)!r}; expected {value!r}")

    if not TEX_REGISTRY_PATH.exists():
        errors.append("missing TEX_SOURCE_REGISTRY.csv")
        tex_rows: list[dict[str, str]] = []
    else:
        tex_rows = read_csv(TEX_REGISTRY_PATH)
    matching_tex_rows = [row for row in tex_rows if row.get("object_id") == TEX_OBJECT_ID]
    if len(matching_tex_rows) != 1:
        errors.append(f"expected exactly one TeX registry row for {TEX_OBJECT_ID}")
    else:
        row = matching_tex_rows[0]
        if row.get("path") != TEX_PATH.relative_to(REPO_ROOT).as_posix():
            errors.append("TeX registry path mismatch")
        if row.get("source_hash") != tex_hash:
            errors.append("TeX registry source_hash mismatch")
        if row.get("claim_status") != "proposal":
            errors.append("TeX registry claim_status must remain proposal")
        if row.get("ontology_promotion_status") != "not_applicable":
            errors.append("TeX registry ontology_promotion_status must be not_applicable")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260707-015",
        "plan_task_id": "P2-T03",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "source_equivalence_object_id": OBJECT_ID,
        "tex_object_id": TEX_OBJECT_ID,
        "general_eqsrc_discharged": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "distance_to_gr_delta": "no_distance_delta",
        "next_route": "P2-T04",
        "errors": errors,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
