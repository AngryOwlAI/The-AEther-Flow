#!/usr/bin/env python3
"""Validate the RT-20260718-029 relation-label scope repair candidate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-029"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / (
    "eqsrc_intrinsic_discriminator_admissibility_law_candidate_v2.tex"
)
REPORT_PATH = ARTIFACT_ROOT / (
    "eqsrc_intrinsic_discriminator_admissibility_law_candidate_v2_validation.json"
)
COMPLETION_PATH = TASK_ROOT / (
    "jobs/completions/AJC-AJ-RT-20260718-029-001.yaml"
)
HANDOFF_PATH = REPO_ROOT / "research_control/handoffs/handoff-0754.yaml"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = (
    "TEX-EQSRC-INTRINSIC-DISCRIMINATOR-ADMISSIBILITY-LAW-CANDIDATE-V2"
)
FUSION_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-029-PARENT-FUSION-NOTES-"
    "EQSRC-RELATION-LABEL-SCOPE-REPAIR"
)
RECEIPT_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-029-EQSRC-INTRINSIC-"
    "DISCRIMINATOR-ADMISSIBILITY-LAW-CANDIDATE-V2-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_relation_label_scope_repair.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_relation_label_scope_repair.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_relation_label_scope_repair.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_relation_label_scope_repair.md",
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_candidate_v2_receipt.md",
    COMPLETION_PATH,
    HANDOFF_PATH,
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Source Objects and Surviving Candidate Core",
    "Pointwise Labels and Kernel-Pair Relations",
    "Exact Translation Classification",
    "Corrected Finite Witness",
    "Typed Ambient Relation-Changing Witness",
    "Surviving Naturality, Uniqueness, and Robustness",
    "Fail-Closed Branches",
    "No-Target and No-Process Guard",
    "Distance-to-GR, Freeze, and Next Route",
    "Forbidden Conclusions",
]

REQUIRED_TOKENS = [
    "candidate_result: candidate_repaired_pending_fresh_smuggling_audit",
    "EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v2",
    "OBST-EQSRC-INTRINSIC-DISCRIMINATOR-RELATION-LABEL-001",
    "pointwise_label_stability: defined_separately",
    "kernel_pair_relation_preservation: defined_separately",
    "translation_label_fixing: iff_translation_vector_is_boundary",
    "translation_relation_status: every_translation_is_relation_automorphism",
    "e2_pointwise_labels_changed: 8",
    "e2_relation_mismatches: 0",
    "ambient_linear_witness_relation_mismatches: 16",
    "ambient_linear_witness_is_chain_map: false",
    "physical_admissibility_established: false",
    "blocked_adoption_open_continuation",
    "general_EqSrc_discharged: false",
    "distance_to_gr_ledger_changed: false",
    "freeze_decision: not_frozen",
    "fresh_smuggling_auditor_review",
]

FORBIDDEN_SNIPPETS = [
    "source law is adopted",
    "physical admissibility is established",
    "physical covariance is established",
    "general EqSrc is discharged",
    "canonical ontology is modified",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
    "global theory is rejected",
    "future source extension is impossible",
]


Vector = tuple[int, int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def single_row(
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
    return tuple(a ^ b for a, b in zip(left, right, strict=True))


def linear_witness(state: Vector) -> Vector:
    """L(e0)=e0, L(e1)=e0+e2, L(e2)=e1."""

    x0, x1, x2 = state
    return (x0 ^ x1, x2, x1)


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

    states = list(itertools.product((0, 1), repeat=3))
    zero: Vector = (0, 0, 0)
    boundary: Vector = (1, 1, 0)
    e2: Vector = (0, 0, 1)
    boundary_group = {zero, boundary}

    def equivalent(left: Vector, right: Vector) -> bool:
        return add(left, right) in boundary_group

    classes: list[set[Vector]] = []
    unseen = set(states)
    while unseen:
        representative = min(unseen)
        orbit = {state for state in states if equivalent(representative, state)}
        classes.append(orbit)
        unseen -= orbit

    if len(classes) != 4 or any(len(orbit) != 2 for orbit in classes):
        errors.append("finite witness must have four two-element quotient classes")

    translation_pointwise_checks = 0
    boundary_translation_pointwise_matches = 0
    nonboundary_translation_pointwise_changes = 0
    translation_relation_pair_checks = 0
    translation_relation_mismatches = 0
    for translation in states:
        for state in states:
            translation_pointwise_checks += 1
            fixes_label = equivalent(state, add(state, translation))
            if translation in boundary_group and fixes_label:
                boundary_translation_pointwise_matches += 1
            if translation not in boundary_group and not fixes_label:
                nonboundary_translation_pointwise_changes += 1
        for left in states:
            for right in states:
                translation_relation_pair_checks += 1
                before = equivalent(left, right)
                after = equivalent(
                    add(left, translation),
                    add(right, translation),
                )
                if before != after:
                    translation_relation_mismatches += 1

    e2_pointwise_changes = sum(
        not equivalent(state, add(state, e2)) for state in states
    )
    e2_relation_mismatches = sum(
        equivalent(left, right)
        != equivalent(add(left, e2), add(right, e2))
        for left in states
        for right in states
    )

    linear_outputs = {linear_witness(state) for state in states}
    linear_true_to_false = 0
    linear_false_to_true = 0
    for left in states:
        for right in states:
            before = equivalent(left, right)
            after = equivalent(linear_witness(left), linear_witness(right))
            if before and not after:
                linear_true_to_false += 1
            elif not before and after:
                linear_false_to_true += 1
    linear_mismatches = linear_true_to_false + linear_false_to_true
    linear_pointwise_fixes = sum(
        equivalent(state, linear_witness(state)) for state in states
    )

    expected_counts = {
        "translation_pointwise_checks": (translation_pointwise_checks, 64),
        "boundary_translation_pointwise_matches": (
            boundary_translation_pointwise_matches,
            16,
        ),
        "nonboundary_translation_pointwise_changes": (
            nonboundary_translation_pointwise_changes,
            48,
        ),
        "translation_relation_pair_checks": (
            translation_relation_pair_checks,
            512,
        ),
        "translation_relation_mismatches": (
            translation_relation_mismatches,
            0,
        ),
        "e2_pointwise_changes": (e2_pointwise_changes, 8),
        "e2_relation_mismatches": (e2_relation_mismatches, 0),
        "linear_unique_outputs": (len(linear_outputs), 8),
        "linear_relation_mismatches": (linear_mismatches, 16),
        "linear_true_to_false": (linear_true_to_false, 8),
        "linear_false_to_true": (linear_false_to_true, 8),
        "linear_pointwise_fixes": (linear_pointwise_fixes, 2),
    }
    for label, (observed, expected) in expected_counts.items():
        if observed != expected:
            errors.append(f"{label}: expected {expected}, observed {observed}")

    if linear_witness(boundary) != e2:
        errors.append("linear witness must map the boundary generator to e2")

    completion: dict[str, object] = {}
    if COMPLETION_PATH.exists():
        completion = yaml.safe_load(COMPLETION_PATH.read_text(encoding="utf-8"))
        progress = completion.get("physics_progress_status", {})
        if not isinstance(progress, dict) or (
            progress.get("status") != "candidate_constructed_pending_audit"
        ):
            errors.append(
                "completion physics_progress_status.status must be "
                "candidate_constructed_pending_audit"
            )
        delta = completion.get("distance_to_gr_delta", {})
        if not isinstance(delta, dict) or delta.get("changed") is not False:
            errors.append("completion must record no Distance-to-GR ledger change")
        freeze = completion.get("freeze_criteria_status", {})
        if not isinstance(freeze, dict) or (
            freeze.get("freeze_decision") != "not_frozen"
        ):
            errors.append("completion repaired chain route must be not_frozen")
        next_route = completion.get("next_recommendation", {})
        if not isinstance(next_route, dict) or (
            next_route.get("role_id") != "smuggling-auditor"
        ):
            errors.append("completion next role must be smuggling-auditor")

    tex_rows = read_csv(TEX_REGISTRY_PATH)
    tex_row = single_row(errors, tex_rows, TEX_OBJECT_ID, "TeX registry")
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
    single_row(errors, markdown_rows, FUSION_OBJECT_ID, "Markdown registry")
    single_row(errors, markdown_rows, RECEIPT_OBJECT_ID, "Markdown registry")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260718-029",
        "plan_task_id": (
            "ordinary_eqsrc_intrinsic_discriminator_admissibility_law_"
            "relation_label_scope_repair"
        ),
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "candidate_result": "candidate_repaired_pending_fresh_smuggling_audit",
        "candidate_name": (
            "EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v2"
        ),
        "obstruction_addressed": (
            "OBST-EQSRC-INTRINSIC-DISCRIMINATOR-RELATION-LABEL-001"
        ),
        "mechanized_state_count": len(states),
        "mechanized_boundary_count": len(boundary_group),
        "mechanized_class_count": len(classes),
        "mechanized_class_sizes": sorted(len(orbit) for orbit in classes),
        "translation_pointwise_checks": translation_pointwise_checks,
        "boundary_translation_pointwise_matches": (
            boundary_translation_pointwise_matches
        ),
        "nonboundary_translation_pointwise_changes": (
            nonboundary_translation_pointwise_changes
        ),
        "translation_relation_pair_checks": translation_relation_pair_checks,
        "translation_relation_mismatches": translation_relation_mismatches,
        "e2_pointwise_changes": e2_pointwise_changes,
        "e2_relation_mismatches": e2_relation_mismatches,
        "linear_unique_outputs": len(linear_outputs),
        "linear_relation_mismatches": linear_mismatches,
        "linear_true_to_false_mismatches": linear_true_to_false,
        "linear_false_to_true_mismatches": linear_false_to_true,
        "linear_pointwise_quotient_fixes": linear_pointwise_fixes,
        "ambient_linear_witness_is_chain_map": False,
        "physical_admissibility_established": False,
        "current_ontology_derives_candidate": False,
        "general_eqsrc_discharged": False,
        "distance_to_gr_delta": "no_ledger_change",
        "freeze_decision": "not_frozen",
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
