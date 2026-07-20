#!/usr/bin/env python3
"""Validate the bounded orientation-torsor descent-law Refuter stress.

The exhaustive finite checks support a draft/control obstruction record.
PASS is not physics proof, ontology adoption, or claim-promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260718-041"
ART = TASK / "artifacts"
CANDIDATE = ROOT / (
    "research_control/tasks/RT-20260718-039/artifacts/"
    "eqsrc_orientation_torsor_descent_law_candidate_v1.tex"
)
AUDIT = ROOT / (
    "research_control/tasks/RT-20260718-040/artifacts/"
    "eqsrc_orientation_torsor_descent_law_smuggling_audit.tex"
)
REPORT = ART / "eqsrc_orientation_torsor_descent_law_refuter_stress_validation.json"
EXPECTED_CANDIDATE_HASH = (
    "81b24c69403c304889a94caec8b2a99a6a360a49f40266764da4cfd3ba4edd5f"
)
EXPECTED_AUDIT_HASH = (
    "06275c74d2d83ca68e518c755dfdda6f548e927bcc9c47fe4c74794c6fc685f1"
)

Vector = tuple[int, int]
Matrix = tuple[int, int, int, int]
Affine = tuple[Matrix, Vector]
STATES: tuple[Vector, ...] = tuple(itertools.product((0, 1), repeat=2))
ZERO, Q, P, D = STATES
IDENTITY: Matrix = (1, 0, 0, 1)
COMPLEMENT: Matrix = (0, 1, 1, 0)
LINES: tuple[frozenset[Vector], ...] = (
    frozenset((ZERO, P)),
    frozenset((ZERO, Q)),
    frozenset((ZERO, D)),
)


def add(left: Vector, right: Vector) -> Vector:
    return (left[0] ^ right[0], left[1] ^ right[1])


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    return (
        matrix[0] * vector[0] ^ matrix[1] * vector[1],
        matrix[2] * vector[0] ^ matrix[3] * vector[1],
    )


def matrices() -> tuple[Matrix, ...]:
    return tuple(
        matrix
        for matrix in itertools.product((0, 1), repeat=4)
        if matrix[0] * matrix[3] ^ matrix[1] * matrix[2]
    )


def relation(line: frozenset[Vector]) -> frozenset[tuple[Vector, Vector]]:
    return frozenset(
        (left, right)
        for left in STATES
        for right in STATES
        if add(left, right) in line
    )


def image_line(matrix: Matrix, line: frozenset[Vector]) -> frozenset[Vector]:
    return frozenset(mat_vec(matrix, vector) for vector in line)


def preserves(affine: Affine, rel: frozenset[tuple[Vector, Vector]]) -> bool:
    matrix, translation = affine
    image = {
        state: add(mat_vec(matrix, state), translation) for state in STATES
    }
    return all(
        ((left, right) in rel) == ((image[left], image[right]) in rel)
        for left in STATES
        for right in STATES
    )


def generated_join(
    relations: tuple[frozenset[tuple[Vector, Vector]], ...],
) -> frozenset[tuple[Vector, Vector]]:
    adjacency = {state: set() for state in STATES}
    for rel in relations:
        for left, right in rel:
            adjacency[left].add(right)
    joined: set[tuple[Vector, Vector]] = set()
    for start in STATES:
        seen = {start}
        queue = deque((start,))
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        joined.update((start, target) for target in seen)
    return frozenset(joined)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    gl = matrices()
    affine_group = tuple(itertools.product(gl, STATES))
    relations = tuple(relation(line) for line in LINES)
    stabilizers = tuple(
        tuple(affine for affine in affine_group if preserves(affine, rel))
        for rel in relations
    )
    common_stabilizer = set(stabilizers[0]).intersection(*map(set, stabilizers[1:]))
    translations = {(IDENTITY, translation) for translation in STATES}
    line_orbit = {image_line(matrix, LINES[0]) for matrix in gl}
    invariant_lines = {
        line
        for line in LINES
        if all(image_line(matrix, line) == line for matrix in gl)
    }
    complement_images = tuple(image_line(COMPLEMENT, line) for line in LINES)
    meet = set(relations[0]).intersection(*map(set, relations[1:]))
    join = generated_join(relations)
    pairwise_differences = tuple(
        len(relations[left].symmetric_difference(relations[right]))
        for left, right in itertools.combinations(range(3), 2)
    )

    required_files = [
        ART / "child_phys_math_eqsrc_orientation_torsor_descent_law_refuter_stress.yaml",
        ART / "child_phys_phil_eqsrc_orientation_torsor_descent_law_refuter_stress.yaml",
        ART / "parent_conflict_review_eqsrc_orientation_torsor_descent_law_refuter_stress.yaml",
        ART / "parent_fusion_notes_eqsrc_orientation_torsor_descent_law_refuter_stress.md",
        ART / "eqsrc_orientation_torsor_descent_law_refuter_stress.tex",
        ART / "eqsrc_orientation_torsor_descent_law_refuter_stress_receipt.md",
        ART / "eqsrc_orientation_torsor_descent_law_refuter_countermodel.yaml",
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260718-041.md",
        TASK / "documentation_impact.yaml",
        TASK / "jobs/AJ-RT-20260718-041-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260718-041-001.yaml",
        TASK / "roles/refuter@0.2.0--RT-20260718-041.yaml",
        ROOT / "research_control/handoffs/handoff-0766.yaml",
        ROOT / "research_control/handoffs/handoff-0766.md",
    ]
    missing_files = [
        str(path.relative_to(ROOT)) for path in required_files if not path.is_file()
    ]
    fused_text = (
        ART / "eqsrc_orientation_torsor_descent_law_refuter_stress.tex"
    ).read_text()
    required_tokens = [
        "scoped\\_obstruction",
        "OB-EQSRC-ORIENTATION-TORSOR-LINE-SELECTION-001",
        "intersection of the three",
        "sixteen ordered pairs",
        "locally frozen",
        "theoretical-continuation-selector",
    ]
    missing_tokens = [token for token in required_tokens if token not in fused_text]

    checks = {
        "candidate_hash_matches": sha256(CANDIDATE) == EXPECTED_CANDIDATE_HASH,
        "audit_hash_matches": sha256(AUDIT) == EXPECTED_AUDIT_HASH,
        "gl2_order_is_6": len(gl) == 6,
        "agl2_order_is_24": len(affine_group) == 24,
        "three_nonzero_proper_lines": len(set(LINES)) == 3,
        "each_relation_has_8_ordered_pairs": all(
            len(rel) == 8 for rel in relations
        ),
        "gl2_line_action_is_transitive": line_orbit == set(LINES),
        "no_full_gl_invariant_proper_line": not invariant_lines,
        "pairwise_relations_are_distinct": pairwise_differences == (8, 8, 8),
        "each_affine_stabilizer_has_order_8": all(
            len(stabilizer) == 8 for stabilizer in stabilizers
        ),
        "common_stabilizer_has_order_4": len(common_stabilizer) == 4,
        "common_stabilizer_is_exactly_translations": common_stabilizer
        == translations,
        "complement_swaps_coordinates_and_fixes_diagonal": complement_images
        == (LINES[1], LINES[0], LINES[2]),
        "meet_is_equality_with_4_pairs": len(meet) == 4
        and meet == {(state, state) for state in STATES},
        "generated_join_is_universal_with_16_pairs": len(join) == 16,
        "odd_odd_transfer_exits_domain": all(
            ((left - 1) % 2 == 0 and (right + 1) % 2 == 0)
            for left, right in ((1, 1), (1, 3), (3, 1), (3, 3))
        ),
        "required_files_present": not missing_files,
        "required_tokens_present": not missing_tokens,
    }
    payload = {
        "schema": "eqsrc-orientation-torsor-descent-law-refuter-stress-validation.v1",
        "task_id": "RT-20260718-041",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "support_only": True,
        "classification": "scoped_obstruction",
        "obstruction_id": "OB-EQSRC-ORIENTATION-TORSOR-LINE-SELECTION-001",
        "counts": {
            "gl2_order": len(gl),
            "agl2_order": len(affine_group),
            "line_count": len(LINES),
            "relation_ordered_pairs_each": [len(rel) for rel in relations],
            "affine_stabilizer_orders": [
                len(stabilizer) for stabilizer in stabilizers
            ],
            "common_affine_stabilizer_order": len(common_stabilizer),
            "line_orbit_size": len(line_orbit),
            "meet_ordered_pairs": len(meet),
            "join_ordered_pairs": len(join),
        },
        "checks": checks,
        "missing_files": missing_files,
        "missing_tokens": missing_tokens,
        "authority_note": (
            "Operational finite support only; not physics proof, ontology "
            "adoption, physical-admissibility, or claim-promotion authority."
        ),
    }
    if args.write_report:
        REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["status"])
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
