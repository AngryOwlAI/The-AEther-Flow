#!/usr/bin/env python3
"""Validate the RT-20260718-028 intrinsic-discriminator smuggling audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-028"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = (
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_smuggling_audit.tex"
)
REPORT_PATH = (
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_smuggling_audit_validation.json"
)
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = (
    "TEX-EQSRC-INTRINSIC-DISCRIMINATOR-ADMISSIBILITY-LAW-SMUGGLING-AUDIT"
)
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-028-PARENT-FUSION-NOTES-"
    "EQSRC-INTRINSIC-DISCRIMINATOR-SMUGGLING-AUDIT"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-028-EQSRC-INTRINSIC-"
    "DISCRIMINATOR-ADMISSIBILITY-LAW-SMUGGLING-AUDIT-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT
    / "child_phys_math_eqsrc_intrinsic_discriminator_smuggling_audit.yaml",
    ARTIFACT_ROOT
    / "child_phys_phil_eqsrc_intrinsic_discriminator_smuggling_audit.yaml",
    ARTIFACT_ROOT
    / "parent_conflict_review_eqsrc_intrinsic_discriminator_smuggling_audit.yaml",
    ARTIFACT_ROOT
    / "parent_fusion_notes_eqsrc_intrinsic_discriminator_smuggling_audit.md",
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_smuggling_audit_receipt.md",
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Artifact and Audit Questions",
    "Audit Method",
    "Declaration and Dependency Audit",
    "Primitive Selection and Formal Independence",
    "Naturality and Conditional Uniqueness",
    "Pointwise Stability versus Relation Preservation",
    "Finite Witness Audit",
    "Target and Process Authority Audit",
    "Exact Obstruction",
    "Source-Extension and Adoption Classification",
    "Distance-to-GR Status",
    "Freeze Evaluation",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "source_pure_as_written_with_precise_repairable_relation_label_obstruction",
    "source_purity_result: no_explicit_target_or_process_import_detected",
    (
        "formal_independence_result: "
        "syntactic_nonreference_pass_shared_root_physical_selection_unproved"
    ),
    "OBST-EQSRC-INTRINSIC-DISCRIMINATOR-RELATION-LABEL-001",
    "Translation label--relation separation",
    "all \\(64\\) ordered-pair relation comparisons are preserved",
    "L(e_0+e_1)=e_2",
    "new\\_ontology\\_primitive\\_candidate",
    "blocked\\_adoption\\_open\\_continuation",
    "ontology-formalizer@0.2.0",
    "general_EqSrc_discharged: false",
    "RetainH_adopted: false",
    "GenH_adopted: false",
    "M_src_adopted: false",
    "distance_to_gr_ledger_changed: false",
]

FORBIDDEN_SNIPPETS = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "M_src is adopted",
    "source law is adopted",
    "canonical ontology is modified",
    "physical admissibility is established",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
    "global theory is rejected",
]

Vector = tuple[int, int, int]
ZERO: Vector = (0, 0, 0)
BOUNDARY: Vector = (1, 1, 0)
E2: Vector = (0, 0, 1)


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


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a ^ b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def related(left: Vector, right: Vector) -> bool:
    return add(left, right) in {ZERO, BOUNDARY}


def quotient_label(value: Vector) -> tuple[int, int]:
    return (value[0] ^ value[1], value[2])


def linear_witness(value: Vector) -> Vector:
    """L(e0)=e0, L(e1)=e0+e2, L(e2)=e1."""

    x0, x1, x2 = value
    return (x0 ^ x1, x2, x1)


def mechanized_checks(errors: list[str]) -> dict[str, object]:
    states: list[Vector] = list(itertools.product((0, 1), repeat=3))
    classes: dict[tuple[int, int], list[Vector]] = {}
    for state in states:
        classes.setdefault(quotient_label(state), []).append(state)
    if len(classes) != 4 or sorted(map(len, classes.values())) != [2, 2, 2, 2]:
        errors.append("expected four two-element quotient classes")

    boundary_label_changes = sum(
        quotient_label(add(state, BOUNDARY)) != quotient_label(state)
        for state in states
    )
    if boundary_label_changes != 0:
        errors.append("boundary translation changed a quotient label")

    e2_label_changes = sum(
        quotient_label(add(state, E2)) != quotient_label(state) for state in states
    )
    if e2_label_changes != 8:
        errors.append("e2 translation must change all eight quotient labels")

    e2_relation_mismatches = sum(
        related(left, right) != related(add(left, E2), add(right, E2))
        for left in states
        for right in states
    )
    if e2_relation_mismatches != 0:
        errors.append("e2 translation must preserve all ordered-pair relations")

    all_translation_mismatches = sum(
        related(left, right) != related(add(left, shift), add(right, shift))
        for shift in states
        for left in states
        for right in states
    )
    if all_translation_mismatches != 0:
        errors.append("every fixed translation must preserve the kernel relation")

    images = {linear_witness(state) for state in states}
    if len(images) != 8:
        errors.append("linear audit witness must be invertible")
    if linear_witness(BOUNDARY) != E2:
        errors.append("linear witness must map the boundary generator to e2")
    linear_relation_mismatches = sum(
        related(left, right)
        != related(linear_witness(left), linear_witness(right))
        for left in states
        for right in states
    )
    if linear_relation_mismatches == 0:
        errors.append("linear audit witness must change the relation")

    return {
        "state_count": len(states),
        "class_count": len(classes),
        "class_sizes": sorted(map(len, classes.values())),
        "boundary_translation_label_changes": boundary_label_changes,
        "e2_translation_label_changes": e2_label_changes,
        "e2_ordered_pair_relation_checks": len(states) ** 2,
        "e2_relation_mismatches": e2_relation_mismatches,
        "translations_checked": len(states),
        "all_translation_ordered_pair_checks": len(states) ** 3,
        "all_translation_relation_mismatches": all_translation_mismatches,
        "linear_witness_image_count": len(images),
        "linear_witness_boundary_image": list(linear_witness(BOUNDARY)),
        "linear_witness_relation_mismatches": linear_relation_mismatches,
    }


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

    math_results = mechanized_checks(errors)

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
        "task_id": "RT-20260718-028",
        "plan_task_id": (
            "ordinary_eqsrc_intrinsic_discriminator_admissibility_law_"
            "smuggling_audit"
        ),
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "audit_result": (
            "source_pure_as_written_with_precise_repairable_"
            "relation_label_obstruction"
        ),
        "source_purity_result": "no_explicit_target_or_process_import_detected",
        "formal_independence_result": (
            "syntactic_nonreference_pass_shared_root_physical_selection_unproved"
        ),
        "obstruction_id": (
            "OBST-EQSRC-INTRINSIC-DISCRIMINATOR-RELATION-LABEL-001"
        ),
        "next_required_role": "ontology-formalizer@0.2.0",
        "mechanized_checks": math_results,
        "general_eqsrc_discharged": False,
        "physical_admissibility_established": False,
        "distance_to_gr_delta": "precise_obstruction_no_ledger_change",
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
