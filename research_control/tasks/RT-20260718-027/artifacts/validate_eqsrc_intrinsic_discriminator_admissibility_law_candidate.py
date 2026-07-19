#!/usr/bin/env python3
"""Validate the RT-20260718-027 chain-homology EqSrc law candidate."""

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
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-027"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / (
    "eqsrc_intrinsic_discriminator_admissibility_law_candidate_v1.tex"
)
REPORT_PATH = ARTIFACT_ROOT / (
    "eqsrc_intrinsic_discriminator_admissibility_law_candidate_validation.json"
)
COMPLETION_PATH = TASK_ROOT / (
    "jobs/completions/AJC-AJ-RT-20260718-027-001.yaml"
)
HANDOFF_PATH = REPO_ROOT / "research_control/handoffs/handoff-0752.yaml"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = (
    "TEX-EQSRC-INTRINSIC-DISCRIMINATOR-ADMISSIBILITY-LAW-CANDIDATE-V1"
)
FUSION_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-027-PARENT-FUSION-NOTES-"
    "EQSRC-INTRINSIC-DISCRIMINATOR-LAW"
)
RECEIPT_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-027-EQSRC-INTRINSIC-"
    "DISCRIMINATOR-ADMISSIBILITY-LAW-CANDIDATE-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_intrinsic_discriminator_law.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_intrinsic_discriminator_law.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_intrinsic_discriminator_law.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_intrinsic_discriminator_law.md",
    ARTIFACT_ROOT
    / "eqsrc_intrinsic_discriminator_admissibility_law_candidate_receipt.md",
    COMPLETION_PATH,
    HANDOFF_PATH,
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Formal Source Objects, Domains, and Maps",
    "Variation-Class Independence Certificate",
    "Source-Automorphism Naturality Theorem",
    "Uniqueness up to Intrinsic Codomain Gauge",
    "Finite-Variation Robustness and Sharpness",
    "Concrete Finite Source-Object Witness",
    "Fail-Closed Branches",
    "No-Target and No-Process Guard",
    "Distance-to-GR, Freeze, and Next Route",
    "Forbidden Conclusions",
]

REQUIRED_TOKENS = [
    "candidate_result: candidate_formalized_pending_fresh_smuggling_audit",
    "EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v1",
    "intrinsic_discriminator: chi_E:Z_1(E)->H_1(E;F2)",
    "source_local_boundary_moves_defined_before_chi_E",
    "chain_isomorphism_natural",
    "unique_up_to_intrinsic_codomain_gauge",
    "witness_class_count: 4",
    "witness_class_size: 2",
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
    "general EqSrc is discharged",
    "canonical ontology is modified",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
    "global theory is rejected",
    "future source extension is impossible",
]


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


def add(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(a ^ b for a, b in zip(left, right, strict=True))


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
    boundary = (1, 1, 0)
    boundary_group = {(0, 0, 0), boundary}

    def equivalent(left: tuple[int, int, int], right: tuple[int, int, int]) -> bool:
        return add(left, right) in boundary_group

    classes: list[set[tuple[int, int, int]]] = []
    unseen = set(states)
    while unseen:
        representative = min(unseen)
        orbit = {state for state in states if equivalent(representative, state)}
        classes.append(orbit)
        unseen -= orbit

    if len(classes) != 4 or any(len(orbit) != 2 for orbit in classes):
        errors.append("finite witness must have four two-element homology classes")

    for state in states:
        if not equivalent(state, add(state, boundary)):
            errors.append("boundary generator failed to preserve a homology class")

    e2 = (0, 0, 1)
    for state in states:
        if equivalent(state, add(state, e2)):
            errors.append("out-of-class e2 translation unexpectedly preserved a class")

    for length in range(5):
        for word in itertools.product(((0, 0, 0), boundary), repeat=length):
            total = (0, 0, 0)
            for move in word:
                total = add(total, move)
            if total not in boundary_group:
                errors.append("finite boundary word left the boundary subgroup")

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
            errors.append("completion distinct chain route must be not_frozen")
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
        "task_id": "RT-20260718-027",
        "plan_task_id": "ordinary_eqsrc_intrinsic_discriminator_admissibility_law",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "candidate_result": "candidate_formalized_pending_fresh_smuggling_audit",
        "candidate_name": (
            "EqSrcIntrinsicDiscriminatorAdmissibilityLaw_src^cand,v1"
        ),
        "formal_model": "finite_2_truncated_chain_complex_over_F2",
        "mechanized_cycle_count": len(states),
        "mechanized_boundary_count": len(boundary_group),
        "mechanized_class_count": len(classes),
        "mechanized_class_sizes": sorted(len(orbit) for orbit in classes),
        "mechanized_boundary_robustness": "PASS",
        "mechanized_out_of_class_sharpness": "PASS",
        "naturality_theorem_present": True,
        "independence_certificate_present": True,
        "quotient_uniqueness_theorem_present": True,
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
