#!/usr/bin/env python3
"""Validate the RT-20260718-031 cross-complex reflection-scope repair."""

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
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-031"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / (
    "eqsrc_intrinsic_discriminator_admissibility_law_candidate_v3.tex"
)
REPORT_PATH = ARTIFACT_ROOT / (
    "eqsrc_intrinsic_discriminator_admissibility_law_candidate_v3_validation.json"
)
COMPLETION_PATH = TASK_ROOT / (
    "jobs/completions/AJC-AJ-RT-20260718-031-001.yaml"
)
HANDOFF_PATH = REPO_ROOT / "research_control/handoffs/handoff-0756.yaml"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = (
    "TEX-EQSRC-INTRINSIC-DISCRIMINATOR-ADMISSIBILITY-LAW-CANDIDATE-V3"
)
FUSION_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-031-PARENT-FUSION-NOTES-"
    "EQSRC-CROSS-COMPLEX-REFLECTION-SCOPE-REPAIR"
)
RECEIPT_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-031-EQSRC-INTRINSIC-"
    "DISCRIMINATOR-ADMISSIBILITY-LAW-CANDIDATE-V3-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT
    / "child_phys_math_eqsrc_cross_complex_reflection_scope_repair.yaml",
    ARTIFACT_ROOT
    / "child_phys_phil_eqsrc_cross_complex_reflection_scope_repair.yaml",
    ARTIFACT_ROOT
    / "parent_conflict_review_eqsrc_cross_complex_reflection_scope_repair.yaml",
    ARTIFACT_ROOT
    / "parent_fusion_notes_eqsrc_cross_complex_reflection_scope_repair.md",
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_candidate_v3_receipt.md",
    COMPLETION_PATH,
    HANDOFF_PATH,
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Supplied Source Packages",
    "Typed Cross-Complex Relation Predicates",
    "Chain-Map Reflection Theorem",
    "Four-State Noninvertible Reflecting Witness",
    "Surviving v2 Self-Map Core",
    "Repaired Fail-Closed Branches",
    "Primitive Selection and Physical Scope",
    "No-Target and No-Process Guard",
    "Distance-to-GR, Freeze, and Next Route",
    "Forbidden Conclusions",
]

REQUIRED_TOKENS = [
    "candidate_result: candidate_repaired_pending_fresh_smuggling_audit",
    "EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v3",
    "OBST-EQSRC-INTRINSIC-DISCRIMINATOR-CHAIN-MAP-REFLECTION-001",
    "cross_complex_relation_preservation: explicitly_typed",
    "cross_complex_relation_reflection: explicitly_typed",
    "chain_map_reflection: iff_induced_H1_is_injective",
    "chain_isomorphism_status: sufficient_not_necessary",
    "noninvertible_reflecting_witness_pair_checks: 16",
    "noninvertible_reflecting_witness_mismatches: 0",
    "physical_admissibility_established: false",
    "physical_covariance_established: false",
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


Vector2 = tuple[int, int]
Vector3 = tuple[int, int, int]


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


def add2(left: Vector2, right: Vector2) -> Vector2:
    return tuple(a ^ b for a, b in zip(left, right, strict=True))


def add3(left: Vector3, right: Vector3) -> Vector3:
    return tuple(a ^ b for a, b in zip(left, right, strict=True))


def reflecting_map(state: Vector2) -> Vector2:
    """F1(a)=0 and F1(b)=b in coordinates (a,b)."""

    _, beta = state
    return (0, beta)


def ambient_linear_witness(state: Vector3) -> Vector3:
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

    states2 = list(itertools.product((0, 1), repeat=2))
    zero2: Vector2 = (0, 0)
    boundary2: Vector2 = (1, 0)
    boundary_group2 = {zero2, boundary2}

    def equivalent2(left: Vector2, right: Vector2) -> bool:
        return add2(left, right) in boundary_group2

    relation_pair_checks = 0
    related_pairs = 0
    unrelated_pairs = 0
    relation_mismatches = 0
    for left in states2:
        for right in states2:
            relation_pair_checks += 1
            before = equivalent2(left, right)
            after = equivalent2(reflecting_map(left), reflecting_map(right))
            related_pairs += int(before)
            unrelated_pairs += int(not before)
            relation_mismatches += int(before != after)

    reflecting_outputs = {reflecting_map(state) for state in states2}
    reflecting_kernel = {
        state for state in states2 if reflecting_map(state) == zero2
    }
    expected_reflection_counts = {
        "state_count": (len(states2), 4),
        "boundary_count": (len(boundary_group2), 2),
        "relation_pair_checks": (relation_pair_checks, 16),
        "related_pairs": (related_pairs, 8),
        "unrelated_pairs": (unrelated_pairs, 8),
        "relation_mismatches": (relation_mismatches, 0),
        "reflecting_image_size": (len(reflecting_outputs), 2),
        "reflecting_kernel_size": (len(reflecting_kernel), 2),
    }
    for label, (observed, expected) in expected_reflection_counts.items():
        if observed != expected:
            errors.append(f"{label}: expected {expected}, observed {observed}")

    # The nonzero homology class [b] is fixed, so the induced one-dimensional
    # homology map is the identity and therefore injective.
    b: Vector2 = (0, 1)
    induced_h1_identity = equivalent2(reflecting_map(b), b)
    if not induced_h1_identity:
        errors.append("reflecting witness must induce identity on H1")
    if len(reflecting_outputs) == len(states2):
        errors.append("reflecting witness must remain noninvertible")

    # Preserve the two exact v2 finite headline checks.
    states3 = list(itertools.product((0, 1), repeat=3))
    zero3: Vector3 = (0, 0, 0)
    boundary3: Vector3 = (1, 1, 0)
    e2: Vector3 = (0, 0, 1)
    boundary_group3 = {zero3, boundary3}

    def equivalent3(left: Vector3, right: Vector3) -> bool:
        return add3(left, right) in boundary_group3

    e2_relation_mismatches = sum(
        equivalent3(left, right)
        != equivalent3(add3(left, e2), add3(right, e2))
        for left in states3
        for right in states3
    )
    ambient_relation_mismatches = sum(
        equivalent3(left, right)
        != equivalent3(
            ambient_linear_witness(left),
            ambient_linear_witness(right),
        )
        for left in states3
        for right in states3
    )
    if e2_relation_mismatches != 0:
        errors.append("v2 e2 translation must retain zero relation mismatches")
    if ambient_relation_mismatches != 16:
        errors.append("v2 ambient L must retain 16 relation mismatches")

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
            errors.append(
                "TeX registry ontology_promotion_status must be not_applicable"
            )
        if tex_row.get("pdf_required") != "false":
            errors.append("TeX registry pdf_required must remain false")

    markdown_rows = read_csv(MARKDOWN_REGISTRY_PATH)
    single_row(errors, markdown_rows, FUSION_OBJECT_ID, "Markdown registry")
    single_row(errors, markdown_rows, RECEIPT_OBJECT_ID, "Markdown registry")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260718-031",
        "plan_task_id": (
            "ordinary_eqsrc_intrinsic_discriminator_admissibility_law_"
            "cross_complex_reflection_scope_repair"
        ),
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "candidate_result": "candidate_repaired_pending_fresh_smuggling_audit",
        "candidate_name": (
            "EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v3"
        ),
        "obstruction_addressed": (
            "OBST-EQSRC-INTRINSIC-DISCRIMINATOR-CHAIN-MAP-REFLECTION-001"
        ),
        "mechanized_state_count": len(states2),
        "mechanized_boundary_count": len(boundary_group2),
        "mechanized_relation_pair_checks": relation_pair_checks,
        "mechanized_related_pairs": related_pairs,
        "mechanized_unrelated_pairs": unrelated_pairs,
        "mechanized_relation_mismatches": relation_mismatches,
        "mechanized_F1_image_size": len(reflecting_outputs),
        "mechanized_F1_kernel_size": len(reflecting_kernel),
        "mechanized_F1_invertible": len(reflecting_outputs) == len(states2),
        "mechanized_induced_H1_identity": induced_h1_identity,
        "mechanized_induced_H1_injective": induced_h1_identity,
        "preserved_v2_e2_relation_mismatches": e2_relation_mismatches,
        "preserved_v2_ambient_L_relation_mismatches": (
            ambient_relation_mismatches
        ),
        "physical_admissibility_established": False,
        "physical_covariance_established": False,
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
