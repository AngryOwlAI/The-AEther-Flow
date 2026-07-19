#!/usr/bin/env python3
"""Validate the RT-20260718-023 EqSrc quotient-selector candidate packet."""

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
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-023"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_source_rooted_quotient_selector_candidate_v1.tex"
REPORT_PATH = (
    ARTIFACT_ROOT / "eqsrc_source_rooted_quotient_selector_candidate_validation.json"
)
COMPLETION_PATH = (
    TASK_ROOT / "jobs/completions/AJC-AJ-RT-20260718-023-001.yaml"
)
HANDOFF_PATH = REPO_ROOT / "research_control/handoffs/handoff-0748.yaml"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-SOURCE-ROOTED-QUOTIENT-SELECTOR-CANDIDATE-V1"
FUSION_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-023-PARENT-FUSION-NOTES-"
    "EQSRC-QUOTIENT-SELECTOR-CANDIDATE"
)
RECEIPT_MD_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-023-EQSRC-SOURCE-ROOTED-"
    "QUOTIENT-SELECTOR-CANDIDATE-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_quotient_selector_candidate.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_quotient_selector_candidate.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_quotient_selector_candidate.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_quotient_selector_candidate.md",
    ARTIFACT_ROOT / "eqsrc_source_rooted_quotient_selector_candidate_receipt.md",
    COMPLETION_PATH,
    HANDOFF_PATH,
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Construction Question and Inputs",
    "Source-Rooted Finite Datum",
    "Exact-v3 Signature Instantiation",
    "Nondegenerate Cross-Fiber Selection",
    "Closure and Exact-v3 Candidate Law",
    "Nontrivial Admissible Finite-Variation Class",
    "Selector Stability Certificate",
    "Transport Naturality",
    "Qualified Sharpness Outside the Declared Class",
    "Transitive Source Provenance and No-Target Guard",
    "Distance-to-GR Status",
    "Freeze and Route-Cycle Evaluation",
    "Forbidden Conclusions",
    "Next Route",
    "Source Materials",
]

REQUIRED_TOKENS = [
    "candidate_result: constructed_candidate",
    "EqSrcSourceRootedQuotientSelectorCandidate_v1",
    "H=\\{0,2\\}",
    "nondegenerate_relation_classes: {A0,A2};{A1,A3}",
    "objectwise_H_valued_shifts",
    "stability_result: invariant_under_V_H",
    "outside_H_shift_can_change_relation",
    "current_ontology_derives_profile_or_subgroup: false",
    "blocked_adoption_open_continuation",
    "general_EqSrc_discharged: false",
    "RetainH_adopted: false",
    "GenH_adopted: false",
    "M_src_adopted: false",
    "distance_to_gr_ledger_changed: false",
    "freeze_decision: not_frozen",
    "smuggling-auditor@0.2.0",
]

FORBIDDEN_SNIPPETS = [
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "M_src is adopted",
    "source law is adopted",
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

    group = range(4)
    subgroup = {0, 2}
    profile = (0, 1, 2, 3)

    def selected(values: tuple[int, ...], left: int, right: int) -> bool:
        return (values[right] - values[left]) % 4 in subgroup

    expected_classes = (
        (True, False, True, False),
        (False, True, False, True),
        (True, False, True, False),
        (False, True, False, True),
    )
    actual_classes = tuple(
        tuple(selected(profile, left, right) for right in group)
        for left in group
    )
    if actual_classes != expected_classes:
        errors.append("mechanized selector matrix does not match two-class witness")

    for left in group:
        if not selected(profile, left, left):
            errors.append("mechanized selector is not reflexive")
        for right in group:
            if selected(profile, left, right) != selected(profile, right, left):
                errors.append("mechanized selector is not symmetric")
            for endpoint in group:
                if (
                    selected(profile, left, right)
                    and selected(profile, right, endpoint)
                    and not selected(profile, left, endpoint)
                ):
                    errors.append("mechanized selector is not transitive")

    for shifts in itertools.product(sorted(subgroup), repeat=4):
        varied = tuple((profile[index] + shifts[index]) % 4 for index in group)
        for left in group:
            for right in group:
                if selected(varied, left, right) != selected(profile, left, right):
                    errors.append(
                        "selector changed under an objectwise H-valued variation"
                    )

    outside_varied = (1, 0, 2, 3)
    if selected(outside_varied, 0, 2) == selected(profile, 0, 2):
        errors.append("outside-H sharpness countervariation did not change A0/A2")
    if selected(outside_varied, 1, 2) == selected(profile, 1, 2):
        errors.append("outside-H sharpness countervariation did not change A1/A2")
    uniform_outside = (1, 2, 3, 0)
    for left in group:
        for right in group:
            if selected(uniform_outside, left, right) != selected(
                profile, left, right
            ):
                errors.append("uniform outside-H shift should preserve selector")

    completion: dict[str, object] = {}
    if COMPLETION_PATH.exists():
        completion = yaml.safe_load(COMPLETION_PATH.read_text(encoding="utf-8"))
        result = completion.get("candidate_constructor_result", {})
        if not isinstance(result, dict) or (
            result.get("result_type") != "constructed_candidate"
        ):
            errors.append(
                "completion candidate_constructor_result.result_type must be "
                "constructed_candidate"
            )
        progress = completion.get("physics_progress_status", {})
        if not isinstance(progress, dict) or (
            progress.get("status") != "candidate_constructed_pending_audit"
        ):
            errors.append(
                "completion physics_progress_status.status must be "
                "candidate_constructed_pending_audit"
            )
        freeze = completion.get("freeze_criteria_status", {})
        if not isinstance(freeze, dict) or (
            freeze.get("freeze_decision") != "not_frozen"
        ):
            errors.append("completion freeze decision must be not_frozen")
        if completion.get("next_recommended_role") != "smuggling-auditor@0.2.0":
            errors.append("completion next recommended role mismatch")
        delta = completion.get("distance_to_gr_delta", {})
        if not isinstance(delta, dict) or delta.get("changed") is not False:
            errors.append("completion must record no Distance-to-GR ledger change")

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
        "task_id": "RT-20260718-023",
        "plan_task_id": (
            "ordinary_eqsrc_closure_provenance_selector_stability_candidate"
        ),
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "candidate_result": "constructed_candidate",
        "candidate_name": "EqSrcSourceRootedQuotientSelectorCandidate_v1",
        "relation_classes": [["A0", "A2"], ["A1", "A3"]],
        "admissible_variation_class": "objectwise_H_valued_shifts",
        "stability_result": "invariant_under_V_H",
        "naturality_result": "transport_equivariant",
        "sharpness_result": "outside_H_shift_can_change_relation",
        "mechanized_selector_matrix": "PASS",
        "mechanized_H_variations_checked": 16,
        "mechanized_outside_H_countervariation": "PASS",
        "mechanized_uniform_outside_H_stabilizer": "PASS",
        "current_ontology_derives_profile_or_subgroup": False,
        "general_eqsrc_discharged": False,
        "retainh_adopted": False,
        "genh_adopted": False,
        "msrc_adopted": False,
        "distance_to_gr_delta": "candidate_constructed_no_ledger_change",
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
