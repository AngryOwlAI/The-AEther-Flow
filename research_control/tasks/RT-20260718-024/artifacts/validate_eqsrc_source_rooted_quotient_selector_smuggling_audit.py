#!/usr/bin/env python3
"""Validate the RT-20260718-024 quotient-selector smuggling audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-024"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_source_rooted_quotient_selector_smuggling_audit.tex"
REPORT_PATH = (
    ARTIFACT_ROOT
    / "eqsrc_source_rooted_quotient_selector_smuggling_audit_validation.json"
)
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-SOURCE-ROOTED-QUOTIENT-SELECTOR-SMUGGLING-AUDIT"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-024-PARENT-FUSION-NOTES-"
    "EQSRC-QUOTIENT-SELECTOR-SMUGGLING-AUDIT"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-024-EQSRC-SOURCE-ROOTED-"
    "QUOTIENT-SELECTOR-SMUGGLING-AUDIT-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_quotient_selector_smuggling_audit.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_quotient_selector_smuggling_audit.yaml",
    ARTIFACT_ROOT
    / "parent_conflict_review_eqsrc_quotient_selector_smuggling_audit.yaml",
    ARTIFACT_ROOT
    / "parent_fusion_notes_eqsrc_quotient_selector_smuggling_audit.md",
    ARTIFACT_ROOT
    / "eqsrc_source_rooted_quotient_selector_smuggling_audit_receipt.md",
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Audit Questions and Method",
    "Declaration and Dependency Audit",
    "Transitive Source-Factorization Audit",
    "Arbitrary-Label and Opaque-Lookup Audit",
    "Variation-Class and Stabilizer Audit",
    "Naturality and Covariance Audit",
    "Target and Process Authority Audit",
    "Audit Result and Open Burdens",
    "Source-Extension and Adoption Classification",
    "Distance-to-GR Status",
    "Freeze and Route-Cycle Evaluation",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "formal_source_purity_pass_with_primitive_selection_and_admissibility_limits",
    "declaration_closure_result: pass_for_exact_declared_finite_model",
    "transitive_provenance_result: pass_as_explicit_new_source_leaves_only",
    "profile_table_is_explicit_unselected_primitive",
    "no_hidden_lookup_but_s_is_primitive_table",
    "relative_stability_valid_physical_admissibility_unproved",
    "transported_equivariance_only",
    "new_ontology_primitive_requiring_human_gate",
    "Primitive-profile nonuniqueness certificate",
    "Bare-set symmetry obstruction",
    "Exact formal stabilizer",
    "24",
    "32",
    "blocked\\_adoption\\_open\\_continuation",
    "refuter@0.2.0",
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


def quotient_label(value: int) -> int:
    """Return the Z4/H label for H={0,2}."""

    return value % 2


def relation(profile: tuple[int, ...]) -> tuple[tuple[bool, ...], ...]:
    labels = tuple(quotient_label(value) for value in profile)
    return tuple(
        tuple(labels[left] == labels[right] for right in range(4))
        for left in range(4)
    )


def canonical_partition(profile: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    blocks: dict[int, list[int]] = {}
    for object_index, value in enumerate(profile):
        blocks.setdefault(quotient_label(value), []).append(object_index)
    return tuple(sorted(tuple(block) for block in blocks.values()))


def mechanized_checks(errors: list[str]) -> dict[str, object]:
    original = (0, 1, 2, 3)
    original_relation = relation(original)
    profile_counts = Counter(
        canonical_partition(profile)
        for profile in itertools.permutations(range(4))
    )
    if len(profile_counts) != 3:
        errors.append("bijective profiles did not realize exactly three partitions")
    if sorted(profile_counts.values()) != [8, 8, 8]:
        errors.append("expected eight bijective profiles per two-plus-two partition")

    all_variations = list(itertools.product(range(4), repeat=4))
    stabilizers = []
    for variation in all_variations:
        varied = tuple(
            (original[index] + variation[index]) % 4 for index in range(4)
        )
        if relation(varied) == original_relation:
            stabilizers.append(variation)
    if len(stabilizers) != 32:
        errors.append("expected exactly 32 additive relation stabilizers")

    h = (0, 2)
    v_h = list(itertools.product(h, repeat=4))
    if len(v_h) != 16:
        errors.append("expected exactly 16 H-valued variations")
    if any(variation not in stabilizers for variation in v_h):
        errors.append("an H-valued variation failed to preserve the selector")

    common_coset_variations = [
        variation
        for variation in all_variations
        if len({quotient_label(value) for value in variation}) == 1
    ]
    if set(stabilizers) != set(common_coset_variations):
        errors.append("stabilizers differ from common-quotient-coset variations")

    alternate = (0, 2, 1, 3)
    if relation(alternate) == original_relation:
        errors.append("alternate profile failed to change the selected partition")

    candidate_countervariation = (1, 3, 0, 0)
    countervaried = tuple(
        (original[index] + candidate_countervariation[index]) % 4
        for index in range(4)
    )
    if relation(countervaried) == original_relation:
        errors.append("candidate countervariation failed to change the relation")

    return {
        "bijective_profiles_checked": 24,
        "distinct_two_plus_two_partitions": len(profile_counts),
        "profiles_per_partition": sorted(profile_counts.values()),
        "all_additive_variations_checked": len(all_variations),
        "full_relation_stabilizer_count": len(stabilizers),
        "v_h_variation_count": len(v_h),
        "v_h_index_in_full_stabilizer": len(stabilizers) // len(v_h),
        "common_coset_characterization_confirmed": (
            set(stabilizers) == set(common_coset_variations)
        ),
        "alternate_profile_changes_partition": (
            relation(alternate) != original_relation
        ),
        "candidate_countervariation_changes_relation": (
            relation(countervaried) != original_relation
        ),
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
            errors.append(
                "TeX registry ontology_promotion_status must be not_applicable"
            )
        if tex_row.get("pdf_required") != "false":
            errors.append("TeX registry pdf_required must remain false")

    markdown_rows = read_csv(MARKDOWN_REGISTRY_PATH)
    require_single_row(errors, markdown_rows, FUSION_MD_OBJECT_ID, "Markdown registry")
    require_single_row(
        errors, markdown_rows, RECEIPT_MD_OBJECT_ID, "Markdown registry"
    )

    report = {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260718-024",
        "plan_task_id": "ordinary_eqsrc_quotient_selector_smuggling_audit",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "audit_result": (
            "formal_source_purity_pass_with_primitive_selection_"
            "and_admissibility_limits"
        ),
        "declaration_closure_result": "pass_for_exact_declared_finite_model",
        "transitive_provenance_result": (
            "pass_as_explicit_new_source_leaves_only"
        ),
        "arbitrary_label_result": "profile_table_is_explicit_unselected_primitive",
        "hidden_target_result": "not_detected",
        "opaque_lookup_result": "no_hidden_lookup_but_s_is_primitive_table",
        "process_authority_result": "not_detected",
        "variation_class_result": (
            "relative_stability_valid_physical_admissibility_unproved"
        ),
        "covariance_result": "transported_equivariance_only",
        "source_extension_classification": (
            "new_ontology_primitive_requiring_human_gate"
        ),
        "current_ontology_derivation": "not_established",
        "conservative_definitional_extension": "not_established",
        "general_eqsrc_discharged": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "m_src_adopted": False,
        "distance_to_gr_delta": "candidate_audited_no_ledger_change",
        "next_required_role": "refuter@0.2.0",
        "mechanized_checks": math_results,
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
