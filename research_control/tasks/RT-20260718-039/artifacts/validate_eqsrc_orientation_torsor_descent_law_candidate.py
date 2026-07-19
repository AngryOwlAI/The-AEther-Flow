#!/usr/bin/env python3
"""Validate the RT-20260718-039 orientation-torsor EqSrc candidate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import sys
from collections import deque
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260718-039"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
TEX_PATH = ARTIFACT_ROOT / "eqsrc_orientation_torsor_descent_law_candidate_v1.tex"
REPORT_PATH = ARTIFACT_ROOT / (
    "eqsrc_orientation_torsor_descent_law_candidate_validation.json"
)
COMPLETION_PATH = TASK_ROOT / (
    "jobs/completions/AJC-AJ-RT-20260718-039-001.yaml"
)
HANDOFF_PATH = REPO_ROOT / "research_control/handoffs/handoff-0764.yaml"
TEX_REGISTRY_PATH = REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
MARKDOWN_REGISTRY_PATH = REPO_ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"

TEX_OBJECT_ID = "TEX-EQSRC-ORIENTATION-TORSOR-DESCENT-LAW-CANDIDATE-V1"
FUSION_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-039-PARENT-FUSION-NOTES-"
    "EQSRC-ORIENTATION-TORSOR-DESCENT-LAW"
)
RECEIPT_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260718-039-EQSRC-ORIENTATION-TORSOR-"
    "DESCENT-LAW-CANDIDATE-RECEIPT"
)

REQUIRED_FILES = [
    TASK_ROOT / "00_TASK.yaml",
    TASK_ROOT / "DDR-20260718-039.md",
    TASK_ROOT / "roles/ontology-formalizer@0.2.0--RT-20260718-039.yaml",
    TASK_ROOT / "jobs/AJ-RT-20260718-039-001.yaml",
    ARTIFACT_ROOT / "child_phys_math_eqsrc_orientation_torsor_descent_law.yaml",
    ARTIFACT_ROOT / "child_phys_phil_eqsrc_orientation_torsor_descent_law.yaml",
    ARTIFACT_ROOT / "parent_conflict_review_eqsrc_orientation_torsor_descent_law.yaml",
    ARTIFACT_ROOT / "parent_fusion_notes_eqsrc_orientation_torsor_descent_law.md",
    ARTIFACT_ROOT / "eqsrc_orientation_torsor_descent_law_candidate_receipt.md",
]

REQUIRED_SECTIONS = [
    "Control Status",
    "Admitted Unordered Source Records",
    "Orientation Torsor, Fibre Data, and Dependency Order",
    "Independent Variation Control",
    "Associated State and Relation Objects",
    "Inverse, Cocycle, Equivariance, and Functoriality",
    "Fibre Pullback and Strict Scalar Non-Descent",
    "Natural-Section Obstruction and Pointed-Torsor Repair",
    "Two-Point Witness and Exhaustive Finite Checks",
    "Parity, Full-Symmetry, and Fail-Closed Branches",
    "No-Target and No-Process Guard",
    "Distance-to-GR, Freeze, and Next Route",
    "Forbidden Conclusions",
]

REQUIRED_TOKENS = [
    "candidate_result: candidate_formalized_pending_fresh_smuggling_audit",
    "EqSrcOrientationTorsorDescentLaw_src^cand,v1",
    "free_unpointed_C2_torsor",
    "Abar_U=(O_U times A_U)/C2",
    "bundle_descent: proved_on_admitted_source_groupoid",
    "strict_scalar_descent_on_original_A_U: disproved",
    "fibre_pullback: exact_under_each_trivialization",
    "categories_with_orientation_exchange_automorphism",
    "equivalent_to_selecting_candidate_v1_fibre",
    "constant_one_translation_defined_pre_relation",
    "three_line_projective_orbit_or_tagged_bottom",
    "distinct_candidate_not_fibre_descent",
    "physical_gauge_equivalence_established: false",
    "physical_admissibility_established: false",
    "blocked_adoption_open_continuation",
    "general_EqSrc_discharged: false",
    "distance_to_gr_ledger_changed: false",
    "freeze_decision: not_frozen",
    "fresh_smuggling_auditor_review",
]

FORBIDDEN_SNIPPETS = [
    "source law is adopted",
    "physical gauge equivalence is established",
    "physical admissibility is established",
    "general EqSrc is discharged",
    "canonical ontology is modified",
    "Einstein equations are derived",
    "benchmark is promoted",
    "is a completed derivation",
    "global theory is rejected",
    "future source extension is impossible",
]

Vector = tuple[int, int]
Matrix = tuple[tuple[int, int], tuple[int, int]]
ZERO: Vector = (0, 0)
P: Vector = (1, 0)
Q: Vector = (0, 1)
D: Vector = (1, 1)
STATES: tuple[Vector, ...] = (ZERO, P, Q, D)


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
    return (left[0] ^ right[0], left[1] ^ right[1])


def complement(vector: Vector) -> Vector:
    return (vector[1], vector[0])


def line(generator: Vector) -> frozenset[Vector]:
    return frozenset({ZERO, generator})


def relation(boundary: frozenset[Vector]) -> frozenset[tuple[Vector, Vector]]:
    return frozenset(
        (left, right)
        for left in STATES
        for right in STATES
        if add(left, right) in boundary
    )


def generated_join(
    left: frozenset[tuple[Vector, Vector]],
    right: frozenset[tuple[Vector, Vector]],
) -> frozenset[tuple[Vector, Vector]]:
    adjacency = {state: set() for state in STATES}
    for source, target in left | right:
        adjacency[source].add(target)
    result: set[tuple[Vector, Vector]] = set()
    for source in STATES:
        queue = deque([source])
        seen = {source}
        while queue:
            current = queue.popleft()
            for target in adjacency[current]:
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        result.update((source, target) for target in seen)
    return frozenset(result)


def associated_orbit(orientation: int, vector: Vector) -> frozenset[tuple[int, Vector]]:
    return frozenset(
        {
            (orientation, vector),
            (1 - orientation, complement(vector)),
        }
    )


def matrix_apply(matrix: Matrix, vector: Vector) -> Vector:
    return (
        (matrix[0][0] * vector[0] + matrix[0][1] * vector[1]) % 2,
        (matrix[1][0] * vector[0] + matrix[1][1] * vector[1]) % 2,
    )


def determinant(matrix: Matrix) -> int:
    return (
        matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    ) % 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--precompletion", action="store_true")
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

    boundary_zero = line(Q)
    boundary_one = line(P)
    relation_zero = relation(boundary_zero)
    relation_one = relation(boundary_one)
    equality = frozenset((state, state) for state in STATES)
    universal = frozenset(itertools.product(STATES, repeat=2))

    if len(boundary_zero) != 2 or len(boundary_one) != 2:
        errors.append("both boundary lines must have two elements")
    if len(relation_zero) != 8 or len(relation_one) != 8:
        errors.append("both fibre relations must have eight ordered pairs")
    if relation_zero == relation_one:
        errors.append("strict scalar non-descent witness relations must differ")
    if relation_zero & relation_one != equality:
        errors.append("fibre-relation meet must be equality")
    if generated_join(relation_zero, relation_one) != universal:
        errors.append("generated fibre-relation join must be universal")

    if any(complement(complement(state)) != state for state in STATES):
        errors.append("complement transport is not involutive")
    for left, right in itertools.product(STATES, repeat=2):
        source_related = (left, right) in relation_zero
        target_related = (
            complement(left),
            complement(right),
        ) in relation_one
        if source_related != target_related:
            errors.append("relation equivariance failed")
            break

    associated_states = {
        associated_orbit(orientation, state)
        for orientation in (0, 1)
        for state in STATES
    }
    associated_relation: set[
        tuple[frozenset[tuple[int, Vector]], frozenset[tuple[int, Vector]]]
    ] = set()
    for orientation, fibre_relation in (
        (0, relation_zero),
        (1, relation_one),
    ):
        for left, right in fibre_relation:
            associated_relation.add(
                (
                    associated_orbit(orientation, left),
                    associated_orbit(orientation, right),
                )
            )
    if len(associated_states) != 4:
        errors.append("associated state must have four diagonal C2 orbits")
    if len(associated_relation) != 8:
        errors.append("associated relation must have eight ordered pairs")
    for orientation, expected in ((0, relation_zero), (1, relation_one)):
        pullback = frozenset(
            (left, right)
            for left, right in itertools.product(STATES, repeat=2)
            if (
                associated_orbit(orientation, left),
                associated_orbit(orientation, right),
            )
            in associated_relation
        )
        if pullback != expected:
            errors.append(f"orientation {orientation} pullback mismatch")

    if any((1 - orientation) == orientation for orientation in (0, 1)):
        errors.append("orientation exchange unexpectedly has a fixed point")

    independent_variations = {
        tuple(add(state, shift) for state in STATES)
        for shift in (ZERO, D)
    }
    if len(independent_variations) != 2:
        errors.append("constant-one control family must contain two maps")
    for shift in (ZERO, D):
        for fibre_relation in (relation_zero, relation_one):
            transported = frozenset(
                (add(left, shift), add(right, shift))
                for left, right in fibre_relation
            )
            if transported != fibre_relation:
                errors.append("constant-one control failed relation preservation")

    matrices: list[Matrix] = []
    for entries in itertools.product((0, 1), repeat=4):
        matrix: Matrix = (
            (entries[0], entries[1]),
            (entries[2], entries[3]),
        )
        if determinant(matrix) == 1:
            matrices.append(matrix)
    if len(matrices) != 6:
        errors.append("GL(2,2) must contain six matrices")

    projective_lines = {line(P), line(Q), line(D)}
    orbit = {
        frozenset(matrix_apply(matrix, state) for state in line(P))
        for matrix in matrices
    }
    if orbit != projective_lines:
        errors.append("GL(2,2) must act transitively on the three lines")
    coordinate_pair = {line(P), line(Q)}
    pair_stabilizer_count = sum(
        {
            frozenset(matrix_apply(matrix, state) for state in line(P)),
            frozenset(matrix_apply(matrix, state) for state in line(Q)),
        }
        == coordinate_pair
        for matrix in matrices
    )
    if pair_stabilizer_count != 2:
        errors.append("coordinate-line pair stabilizer must have order two")

    subspaces = {
        frozenset({ZERO}),
        line(P),
        line(Q),
        line(D),
        frozenset(STATES),
    }
    complement_invariant = {
        space
        for space in subspaces
        if frozenset(complement(state) for state in space) == space
    }
    gl_invariant = {
        space
        for space in subspaces
        if all(
            frozenset(matrix_apply(matrix, state) for state in space) == space
            for matrix in matrices
        )
    }
    if len(complement_invariant) != 3:
        errors.append("C2 must preserve exactly 0, diagonal, and A subspaces")
    if len(gl_invariant) != 2:
        errors.append("full GL(2,2) must preserve only 0 and A subspaces")

    affine_maps: set[tuple[Vector, ...]] = set()
    fibre_stabilizers = 0
    both_fibre_stabilizers = 0
    for matrix in matrices:
        for shift in STATES:
            mapping = tuple(
                add(matrix_apply(matrix, state), shift) for state in STATES
            )
            affine_maps.add(mapping)
            image_zero = frozenset(
                (mapping[STATES.index(left)], mapping[STATES.index(right)])
                for left, right in relation_zero
            )
            image_one = frozenset(
                (mapping[STATES.index(left)], mapping[STATES.index(right)])
                for left, right in relation_one
            )
            if image_zero == relation_zero:
                fibre_stabilizers += 1
            if image_zero == relation_zero and image_one == relation_one:
                both_fibre_stabilizers += 1
    if len(affine_maps) != 24:
        errors.append("AGL(2,2) must contain twenty-four affine bijections")
    if fibre_stabilizers != 8 or both_fibre_stabilizers != 4:
        errors.append("expected strict affine stabilizer hierarchy 2<4<8")

    parity_branches = {
        "odd_odd": "bundle_admitted",
        "odd_even": "parity_points_torsor",
        "even_odd": "parity_points_torsor",
        "even_even": "both_fibres_bottom",
    }

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
            errors.append("completion distinct bundle route must be not_frozen")
        next_route = completion.get("next_recommendation", {})
        if not isinstance(next_route, dict) or (
            next_route.get("role_id") != "smuggling-auditor"
        ):
            errors.append("completion next role must be smuggling-auditor")

    elif not args.precompletion:
        errors.append(f"missing completion: {COMPLETION_PATH.relative_to(REPO_ROOT)}")

    if HANDOFF_PATH.exists():
        handoff = yaml.safe_load(HANDOFF_PATH.read_text(encoding="utf-8"))
        if handoff.get("status") != "completed":
            errors.append("handoff-0764 must be completed")
        required_next = handoff.get("required_next_packet", {})
        if not isinstance(required_next, dict) or (
            required_next.get("role_id") != "smuggling-auditor"
        ):
            errors.append("handoff required next role must be smuggling-auditor")
    elif not args.precompletion:
        errors.append(f"missing handoff: {HANDOFF_PATH.relative_to(REPO_ROOT)}")

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
        "task_id": "RT-20260718-039",
        "plan_task_id": "ordinary_eqsrc_orientation_torsor_descent_law",
        "tex_path": TEX_PATH.relative_to(REPO_ROOT).as_posix(),
        "tex_hash": tex_hash,
        "tex_object_id": TEX_OBJECT_ID,
        "candidate_result": "candidate_formalized_pending_fresh_smuggling_audit",
        "candidate_name": "EqSrcOrientationTorsorDescentLaw_src^cand,v1",
        "formal_model": "finite_both_odd_unordered_bipartition_records_over_F2",
        "mechanized_state_count": len(STATES),
        "mechanized_ordered_pair_count": len(universal),
        "fibre_boundary_sizes": [len(boundary_zero), len(boundary_one)],
        "fibre_relation_pair_counts": [len(relation_zero), len(relation_one)],
        "associated_state_count": len(associated_states),
        "associated_relation_pair_count": len(associated_relation),
        "strict_scalar_descent": False,
        "bundle_descent": True,
        "pullbacks_exact": not any(
            error.endswith("pullback mismatch") for error in errors
        ),
        "no_natural_section_on_exchange_witness": True,
        "complement_invariant_subspace_count": len(complement_invariant),
        "gl2_matrix_count": len(matrices),
        "gl2_invariant_subspace_count": len(gl_invariant),
        "projective_line_orbit_size": len(orbit),
        "coordinate_pair_stabilizer_count": pair_stabilizer_count,
        "affine_bijection_count": len(affine_maps),
        "independent_control_count": len(independent_variations),
        "both_fibre_stabilizer_count": both_fibre_stabilizers,
        "single_fibre_stabilizer_count": fibre_stabilizers,
        "parity_branches": parity_branches,
        "physical_gauge_equivalence_established": False,
        "physical_admissibility_established": False,
        "adoption_status": "blocked_adoption_open_continuation",
        "general_EqSrc_discharged": False,
        "distance_to_gr_ledger_changed": False,
        "next_role": "smuggling-auditor@0.2.0",
        "errors": errors,
    }

    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
