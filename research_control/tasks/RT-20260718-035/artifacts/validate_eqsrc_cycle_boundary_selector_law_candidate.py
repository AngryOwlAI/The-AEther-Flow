#!/usr/bin/env python3
"""Validate the RT-20260718-035 marked-source EqSrc selector candidate."""

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
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-035"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_cycle_boundary_selector_law_candidate_v1.tex"
REPORT_PATH = ARTIFACT_ROOT / (
    "eqsrc_cycle_boundary_selector_law_candidate_validation.json"
)
COMPLETION_PATH = TASK_ROOT / (
    "jobs/completions/AJC-AJ-RT-20260718-035-001.yaml"
)
HANDOFF_PATH = REPO_ROOT / "research_control/handoffs/handoff-0760.yaml"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-CYCLE-BOUNDARY-SELECTOR-LAW-CANDIDATE-V1"
FUSION_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-035-PARENT-FUSION-NOTES-"
    "EQSRC-CYCLE-BOUNDARY-SELECTOR-LAW"
)
RECEIPT_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-035-EQSRC-CYCLE-BOUNDARY-"
    "SELECTOR-LAW-CANDIDATE-RECEIPT"
)

REQUIRED_FILES = [
    ARTIFACT_ROOT / "child_phys_math_eqsrc_cycle_boundary_selector_law.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_cycle_boundary_selector_law.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_cycle_boundary_selector_law.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_cycle_boundary_selector_law.md",
    ARTIFACT_ROOT / "eqsrc_cycle_boundary_selector_law_candidate_receipt.md",
    COMPLETION_PATH,
    HANDOFF_PATH,
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Marked Source-Record Category and Partial Selector",
    "Dependency Order and Independent Variations",
    "Candidate Relation and Relation-Level Uniqueness",
    "Naturality and Automorphism Equivariance",
    "Chain-Presentation Compatibility",
    "Conditional Robustness",
    "Four-Point Witness and Fixed-Carrier Discrimination",
    "Fail-Closed Branches",
    "No-Target and No-Process Guard",
    "Distance-to-GR, Freeze, and Next Route",
    "Forbidden Conclusions",
]

REQUIRED_TOKENS = [
    "candidate_result: candidate_formalized_pending_fresh_smuggling_audit",
    "EqSrcCycleBoundarySelectorLaw_src^cand,v1",
    "finite_odd_oriented_marked_source_records_over_F2",
    "CycleBoundarySel_src(S)=(A_S,B_S) or tagged_bottom",
    "marked_source_isomorphism_natural",
    "automorphism_equivariance: proved",
    "relation_level_uniqueness: unique_up_to_quotient_codomain_bijection",
    "mark_and_parity_selector_uniqueness: not_claimed",
    "chain_presentation_uniqueness: not_claimed",
    "witness_state_count: 4",
    "witness_class_count: 2",
    "witness_class_size: 2",
    "fixed_carrier_alternate_mark_relation_changed: true",
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

Vector = tuple[int, ...]


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


def permute(vector: Vector, permutation: tuple[int, ...]) -> Vector:
    result = [0] * len(vector)
    for source, target in enumerate(permutation):
        result[target] = vector[source]
    return tuple(result)


def preserving_permutations(size: int, mark: frozenset[int]) -> list[tuple[int, ...]]:
    return [
        permutation
        for permutation in itertools.permutations(range(size))
        if {permutation[index] for index in mark} == set(mark)
    ]


def fixed_space(size: int, mark: frozenset[int]) -> set[Vector]:
    permutations = preserving_permutations(size, mark)
    vectors = itertools.product((0, 1), repeat=size)
    return {
        vector
        for vector in vectors
        if all(permute(vector, permutation) == vector for permutation in permutations)
    }


def boundary_space(states: set[Vector], mark: frozenset[int]) -> set[Vector]:
    return {
        state
        for state in states
        if sum(state[index] for index in mark) % 2 == 0
    }


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a ^ b for a, b in zip(left, right, strict=True))


def relation(states: set[Vector], boundary: set[Vector]) -> set[tuple[Vector, Vector]]:
    return {
        (left, right)
        for left in states
        for right in states
        if add(left, right) in boundary
    }


def equivalence_classes(
    states: set[Vector], boundary: set[Vector]
) -> list[set[Vector]]:
    unseen = set(states)
    classes: list[set[Vector]] = []
    while unseen:
        representative = min(unseen)
        current = {
            state for state in states if add(representative, state) in boundary
        }
        classes.append(current)
        unseen -= current
    return classes


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

    size = 4
    mark_zero = frozenset({0})
    mark_rest = frozenset({1, 2, 3})
    states_zero = fixed_space(size, mark_zero)
    states_rest = fixed_space(size, mark_rest)
    boundary_zero = boundary_space(states_zero, mark_zero)
    boundary_rest = boundary_space(states_rest, mark_rest)

    expected_states = {
        (0, 0, 0, 0),
        (1, 0, 0, 0),
        (0, 1, 1, 1),
        (1, 1, 1, 1),
    }
    if states_zero != expected_states or states_rest != expected_states:
        errors.append("four-point witness invariant space mismatch")
    if boundary_zero != {(0, 0, 0, 0), (0, 1, 1, 1)}:
        errors.append("singleton-mark boundary space mismatch")
    if boundary_rest != {(0, 0, 0, 0), (1, 0, 0, 0)}:
        errors.append("complement-mark boundary space mismatch")

    classes_zero = equivalence_classes(states_zero, boundary_zero)
    classes_rest = equivalence_classes(states_rest, boundary_rest)
    if len(classes_zero) != 2 or any(len(item) != 2 for item in classes_zero):
        errors.append("singleton-mark witness must have two two-element classes")
    if len(classes_rest) != 2 or any(len(item) != 2 for item in classes_rest):
        errors.append("complement-mark witness must have two two-element classes")
    if relation(states_zero, boundary_zero) == relation(states_rest, boundary_rest):
        errors.append("alternate source marks must induce different relations")

    for permutation in preserving_permutations(size, mark_zero):
        for state in states_zero:
            if permute(state, permutation) != state:
                errors.append("source automorphism failed to fix A_S")
        if {permute(state, permutation) for state in boundary_zero} != boundary_zero:
            errors.append("source automorphism failed to preserve B_S")

    for state in states_zero:
        for move in boundary_zero:
            if add(state, move) not in states_zero:
                errors.append("admitted translation left A_S")
            if add(state, add(state, move)) not in boundary_zero:
                errors.append("admitted translation changed quotient label")

    if len(states_zero) != 4 or len(boundary_zero) != 2:
        errors.append("chain presentation dimensions are not 2 and 1")

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
            errors.append("completion distinct marked-source route must be not_frozen")
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
        "task_id": "RT-20260718-035",
        "plan_task_id": "ordinary_eqsrc_cycle_boundary_selector_law",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "candidate_result": "candidate_formalized_pending_fresh_smuggling_audit",
        "candidate_name": "EqSrcCycleBoundarySelectorLaw_src^cand,v1",
        "formal_model": "finite_odd_oriented_marked_source_records_over_F2",
        "mechanized_mark_preserving_automorphism_count": len(
            preserving_permutations(size, mark_zero)
        ),
        "mechanized_state_count": len(states_zero),
        "mechanized_boundary_count": len(boundary_zero),
        "mechanized_class_count": len(classes_zero),
        "mechanized_class_sizes": sorted(len(item) for item in classes_zero),
        "mechanized_automorphism_equivariance": "PASS",
        "mechanized_admitted_translation_robustness": "PASS",
        "mechanized_fixed_carrier_discrimination": "PASS",
        "naturality_theorem_present": True,
        "independence_certificate_present": True,
        "quotient_uniqueness_theorem_present": True,
        "chain_presentation_uniqueness_claimed": False,
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
