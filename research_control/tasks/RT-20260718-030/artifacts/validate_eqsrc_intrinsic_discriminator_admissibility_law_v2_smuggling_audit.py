#!/usr/bin/env python3
"""Validate the RT-20260718-030 intrinsic-discriminator v2 smuggling audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-030"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = (
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_v2_smuggling_audit.tex"
)
REPORT_PATH = (
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_v2_smuggling_audit_validation.json"
)
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = (
    "TEX-EQSRC-INTRINSIC-DISCRIMINATOR-ADMISSIBILITY-LAW-V2-SMUGGLING-AUDIT"
)
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-030-PARENT-FUSION-NOTES-"
    "EQSRC-INTRINSIC-DISCRIMINATOR-V2-SMUGGLING-AUDIT"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-030-EQSRC-INTRINSIC-"
    "DISCRIMINATOR-ADMISSIBILITY-LAW-V2-SMUGGLING-AUDIT-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT
    / "child_phys_math_eqsrc_intrinsic_discriminator_v2_smuggling_audit.yaml",
    ARTIFACT_ROOT
    / "child_phys_phil_eqsrc_intrinsic_discriminator_v2_smuggling_audit.yaml",
    ARTIFACT_ROOT
    / "parent_conflict_review_eqsrc_intrinsic_discriminator_v2_smuggling_audit.yaml",
    ARTIFACT_ROOT
    / "parent_fusion_notes_eqsrc_intrinsic_discriminator_v2_smuggling_audit.md",
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_v2_smuggling_audit_receipt.md",
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Artifact and Audit Questions",
    "Audit Method",
    "Declaration and Dependency Audit",
    "Primitive Selection and Formal Independence",
    "Quotient Factorization and Typed Relations",
    "Translation and Linear Stabilizer Audit",
    "Finite Witness Census",
    "Chain-Map Reflection Obstruction",
    "Target and Process Authority Audit",
    "Source-Extension and Adoption Classification",
    "Distance-to-GR Status",
    "Freeze Evaluation",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    (
        "source_pure_as_written_with_precise_repairable_"
        "chain_map_reflection_scope_obstruction"
    ),
    "source_purity_result: no_explicit_target_or_process_import_detected",
    (
        "formal_independence_result: "
        "syntactic_nonreference_pass_shared_root_physical_selection_unproved"
    ),
    "OBST-EQSRC-INTRINSIC-DISCRIMINATOR-CHAIN-MAP-REFLECTION-001",
    "induced_H1_injectivity_not_chain_map_invertibility",
    "all \\(512\\) linear endomorphisms",
    "zero mismatches over all \\(16\\) ordered pairs",
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

Vector3 = tuple[int, int, int]
Matrix3 = tuple[Vector3, Vector3, Vector3]
ZERO3: Vector3 = (0, 0, 0)
BOUNDARY3: Vector3 = (1, 1, 0)
E2: Vector3 = (0, 0, 1)

Vector2 = tuple[int, int]
ZERO2: Vector2 = (0, 0)
BOUNDARY2: Vector2 = (1, 0)


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


def add3(left: Vector3, right: Vector3) -> Vector3:
    return tuple(a ^ b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def related3(left: Vector3, right: Vector3) -> bool:
    return add3(left, right) in {ZERO3, BOUNDARY3}


def quotient_label3(value: Vector3) -> tuple[int, int]:
    return (value[0] ^ value[1], value[2])


def linear_witness(value: Vector3) -> Vector3:
    """L(e0)=e0, L(e1)=e0+e2, L(e2)=e1."""

    x0, x1, x2 = value
    return (x0 ^ x1, x2, x1)


def matrix_apply(matrix: Matrix3, value: Vector3) -> Vector3:
    return tuple(
        sum(coefficient * coordinate for coefficient, coordinate in zip(row, value))
        % 2
        for row in matrix
    )  # type: ignore[return-value]


def add2(left: Vector2, right: Vector2) -> Vector2:
    return (left[0] ^ right[0], left[1] ^ right[1])


def related2(left: Vector2, right: Vector2) -> bool:
    return add2(left, right) in {ZERO2, BOUNDARY2}


def reflection_counterexample_map(value: Vector2) -> Vector2:
    """F1(a)=0 and F1(b)=b in coordinates (a,b)."""

    return (0, value[1])


def mechanized_checks(errors: list[str]) -> dict[str, object]:
    states3: list[Vector3] = list(itertools.product((0, 1), repeat=3))
    classes: dict[tuple[int, int], list[Vector3]] = {}
    for state in states3:
        classes.setdefault(quotient_label3(state), []).append(state)
    if len(classes) != 4 or sorted(map(len, classes.values())) != [2, 2, 2, 2]:
        errors.append("expected four two-element E_star quotient classes")

    boundary_label_changes = sum(
        quotient_label3(add3(state, BOUNDARY3)) != quotient_label3(state)
        for state in states3
    )
    if boundary_label_changes != 0:
        errors.append("boundary translation changed a quotient label")

    e2_label_changes = sum(
        quotient_label3(add3(state, E2)) != quotient_label3(state)
        for state in states3
    )
    if e2_label_changes != 8:
        errors.append("e2 translation must change all eight quotient labels")

    e2_relation_mismatches = sum(
        related3(left, right) != related3(add3(left, E2), add3(right, E2))
        for left in states3
        for right in states3
    )
    if e2_relation_mismatches != 0:
        errors.append("e2 translation must preserve all ordered-pair relations")

    all_translation_mismatches = sum(
        related3(left, right)
        != related3(add3(left, shift), add3(right, shift))
        for shift in states3
        for left in states3
        for right in states3
    )
    if all_translation_mismatches != 0:
        errors.append("every fixed translation must preserve the kernel relation")

    witness_images = {linear_witness(state) for state in states3}
    if len(witness_images) != 8:
        errors.append("linear audit witness must be invertible")
    if linear_witness(BOUNDARY3) != E2:
        errors.append("linear witness must map the boundary generator to e2")
    witness_relation_mismatches = sum(
        related3(left, right)
        != related3(linear_witness(left), linear_witness(right))
        for left in states3
        for right in states3
    )
    if witness_relation_mismatches != 16:
        errors.append("linear audit witness must have exactly 16 relation mismatches")

    matrices: list[Matrix3] = [
        (entries[0:3], entries[3:6], entries[6:9])
        for entries in itertools.product((0, 1), repeat=9)
    ]
    relation_preserving_count = 0
    invertible_count = 0
    invertible_relation_automorphism_count = 0
    for matrix in matrices:
        images = {matrix_apply(matrix, state) for state in states3}
        invertible = len(images) == 8
        relation_preserving = matrix_apply(matrix, BOUNDARY3) in {
            ZERO3,
            BOUNDARY3,
        }
        relation_automorphism = (
            invertible and matrix_apply(matrix, BOUNDARY3) == BOUNDARY3
        )
        relation_preserving_count += int(relation_preserving)
        invertible_count += int(invertible)
        invertible_relation_automorphism_count += int(relation_automorphism)

    expected_census = (128, 168, 24)
    observed_census = (
        relation_preserving_count,
        invertible_count,
        invertible_relation_automorphism_count,
    )
    if observed_census != expected_census:
        errors.append(
            f"linear endomorphism census mismatch: {observed_census} != {expected_census}"
        )

    states2: list[Vector2] = list(itertools.product((0, 1), repeat=2))
    reflection_images = {
        reflection_counterexample_map(state) for state in states2
    }
    if len(reflection_images) != 2:
        errors.append("reflection counterexample F1 must be noninvertible of rank one")
    reflection_relation_mismatches = sum(
        related2(left, right)
        != related2(
            reflection_counterexample_map(left),
            reflection_counterexample_map(right),
        )
        for left in states2
        for right in states2
    )
    if reflection_relation_mismatches != 0:
        errors.append("noninvertible counterexample must preserve and reflect relation")

    mismatch_formula_specialization = 2 * (2**3) * ((2**1) - (2**0))
    if mismatch_formula_specialization != witness_relation_mismatches:
        errors.append("mismatch formula specialization does not match witness census")

    return {
        "e_star_state_count": len(states3),
        "e_star_class_count": len(classes),
        "e_star_class_sizes": sorted(map(len, classes.values())),
        "boundary_translation_label_changes": boundary_label_changes,
        "e2_translation_label_changes": e2_label_changes,
        "e2_ordered_pair_relation_checks": len(states3) ** 2,
        "e2_relation_mismatches": e2_relation_mismatches,
        "translations_checked": len(states3),
        "all_translation_ordered_pair_checks": len(states3) ** 3,
        "all_translation_relation_mismatches": all_translation_mismatches,
        "linear_witness_image_count": len(witness_images),
        "linear_witness_boundary_image": list(linear_witness(BOUNDARY3)),
        "linear_witness_relation_mismatches": witness_relation_mismatches,
        "linear_endomorphisms_checked": len(matrices),
        "linear_relation_preserving_count": relation_preserving_count,
        "linear_invertible_count": invertible_count,
        "linear_invertible_relation_automorphism_count": (
            invertible_relation_automorphism_count
        ),
        "reflection_counterexample_state_count": len(states2),
        "reflection_counterexample_image_count": len(reflection_images),
        "reflection_counterexample_induced_h1_map": "identity",
        "reflection_counterexample_ordered_pair_checks": len(states2) ** 2,
        "reflection_counterexample_relation_mismatches": (
            reflection_relation_mismatches
        ),
        "mismatch_formula_specialization": mismatch_formula_specialization,
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
        "task_id": "RT-20260718-030",
        "plan_task_id": (
            "ordinary_eqsrc_intrinsic_discriminator_admissibility_law_v2_"
            "smuggling_audit"
        ),
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "audit_result": (
            "source_pure_as_written_with_precise_repairable_"
            "chain_map_reflection_scope_obstruction"
        ),
        "source_purity_result": "no_explicit_target_or_process_import_detected",
        "formal_independence_result": (
            "syntactic_nonreference_pass_shared_root_physical_selection_unproved"
        ),
        "obstruction_id": (
            "OBST-EQSRC-INTRINSIC-DISCRIMINATOR-CHAIN-MAP-REFLECTION-001"
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
