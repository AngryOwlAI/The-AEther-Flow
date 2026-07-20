#!/usr/bin/env python3
"""Validate the bounded EqSrc orientation-torsor descent-law smuggling audit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260718-040"
ART = TASK / "artifacts"
CANDIDATE = (
    ROOT
    / "research_control/tasks/RT-20260718-039/artifacts/"
    "eqsrc_orientation_torsor_descent_law_candidate_v1.tex"
)
REPORT = ART / "eqsrc_orientation_torsor_descent_law_smuggling_audit_validation.json"
EXPECTED_CANDIDATE_HASH = (
    "81b24c69403c304889a94caec8b2a99a6a360a49f40266764da4cfd3ba4edd5f"
)

State = tuple[int, int]
Matrix = tuple[int, int, int, int]

ZERO: State = (0, 0)
P: State = (1, 0)
Q: State = (0, 1)
D: State = (1, 1)


def add(a: State, b: State) -> State:
    return (a[0] ^ b[0], a[1] ^ b[1])


def complement(a: State) -> State:
    return (a[1], a[0])


def mat_vec(matrix: Matrix, vector: State) -> State:
    return (
        matrix[0] * vector[0] ^ matrix[1] * vector[1],
        matrix[2] * vector[0] ^ matrix[3] * vector[1],
    )


def invertible_matrices() -> list[Matrix]:
    return [
        matrix
        for matrix in itertools.product((0, 1), repeat=4)
        if (matrix[0] * matrix[3] ^ matrix[1] * matrix[2]) == 1
    ]


def line(vector: State) -> frozenset[State]:
    return frozenset((ZERO, vector))


def same_coset(a: State, b: State, kernel: frozenset[State]) -> bool:
    return add(a, b) in kernel


def canonical_associated_class(orientation: int, state: State) -> State:
    """Use the orientation-zero fibre as an enumeration gauge, not source data."""
    return state if orientation == 0 else complement(state)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    states = list(itertools.product((0, 1), repeat=2))
    nonzero_lines = [line(P), line(Q), line(D)]
    fibre_lines = {0: line(Q), 1: line(P)}

    equivariance_holds = all(
        frozenset(complement(value) for value in fibre_lines[orientation])
        == fibre_lines[1 - orientation]
        for orientation in (0, 1)
    )
    descended_candidate_line = frozenset(
        canonical_associated_class(orientation, value)
        for orientation in (0, 1)
        for value in fibre_lines[orientation]
    )

    equivariant_line_families: list[tuple[frozenset[State], frozenset[State]]] = []
    descended_lines: set[frozenset[State]] = set()
    for base_line in nonzero_lines:
        partner = frozenset(complement(value) for value in base_line)
        equivariant_line_families.append((base_line, partner))
        descended_lines.add(
            frozenset(
                canonical_associated_class(orientation, value)
                for orientation, family_line in ((0, base_line), (1, partner))
                for value in family_line
            )
        )

    source_swap_fixed_classes = sum(
        canonical_associated_class(1 - orientation, complement(state))
        == canonical_associated_class(orientation, state)
        for orientation in (0, 1)
        for state in states
    )

    candidate_relation_pairs = {
        (a, b)
        for a in states
        for b in states
        if same_coset(a, b, descended_candidate_line)
    }
    fibre_pullback_mismatches = 0
    for orientation in (0, 1):
        for a in states:
            for b in states:
                fibre_relation = same_coset(a, b, fibre_lines[orientation])
                associated_relation = (
                    (
                        canonical_associated_class(orientation, a),
                        canonical_associated_class(orientation, b),
                    )
                    in candidate_relation_pairs
                )
                fibre_pullback_mismatches += int(
                    fibre_relation != associated_relation
                )

    constant_one_translation_failures = 0
    full_translation_failures = 0
    for kernel in nonzero_lines:
        for translation in (ZERO, D):
            constant_one_translation_failures += sum(
                same_coset(a, b, kernel)
                != same_coset(add(a, translation), add(b, translation), kernel)
                for a in states
                for b in states
            )
        for translation in states:
            full_translation_failures += sum(
                same_coset(a, b, kernel)
                != same_coset(add(a, translation), add(b, translation), kernel)
                for a in states
                for b in states
            )

    matrices = invertible_matrices()
    line_orbit = {
        frozenset(mat_vec(matrix, value) for value in line(Q))
        for matrix in matrices
    }
    affine_maps = [
        (matrix, translation)
        for matrix in matrices
        for translation in states
    ]
    relation_stabilizers_by_line: list[int] = []
    quotient_label_fixers_by_line: list[int] = []
    affine_line_subset_stabilizers_by_line: list[int] = []
    for kernel in nonzero_lines:
        stabilizers = 0
        label_fixers = 0
        subset_stabilizers = 0
        for matrix, translation in affine_maps:
            image = {
                state: add(mat_vec(matrix, state), translation)
                for state in states
            }
            stabilizers += int(
                all(
                    same_coset(a, b, kernel)
                    == same_coset(image[a], image[b], kernel)
                    for a in states
                    for b in states
                )
            )
            label_fixers += int(
                all(same_coset(image[state], state, kernel) for state in states)
            )
            subset_stabilizers += int(
                frozenset(image[state] for state in kernel) == kernel
            )
        relation_stabilizers_by_line.append(stabilizers)
        quotient_label_fixers_by_line.append(label_fixers)
        affine_line_subset_stabilizers_by_line.append(subset_stabilizers)

    coordinate_relation_joint_stabilizers = 0
    coordinate_relation_pair_stabilizers = 0
    for matrix, translation in affine_maps:
        image = {
            state: add(mat_vec(matrix, state), translation)
            for state in states
        }
        preserved_coordinate_kernels = [
            all(
                same_coset(a, b, kernel)
                == same_coset(image[a], image[b], kernel)
                for a in states
                for b in states
            )
            for kernel in (line(P), line(Q))
        ]
        coordinate_relation_joint_stabilizers += int(
            all(preserved_coordinate_kernels)
        )
        matrix_images = {
            frozenset(mat_vec(matrix, value) for value in kernel)
            for kernel in (line(P), line(Q))
        }
        coordinate_relation_pair_stabilizers += int(
            matrix_images == {line(P), line(Q)}
        )

    constant_one_label_fixed_lines = sum(
        all(same_coset(add(state, D), state, kernel) for state in states)
        for kernel in nonzero_lines
    )

    internal_complement_image = frozenset(
        complement(value) for value in descended_candidate_line
    )

    parity_transfer_cases = 0
    parity_transfer_exits = 0
    for total in (2, 4, 6, 8):
        for p_size in range(1, total, 2):
            q_size = total - p_size
            if q_size % 2 != 1:
                continue
            if p_size > 1:
                parity_transfer_cases += 1
                parity_transfer_exits += int(
                    (p_size - 1) % 2 == 0 and (q_size + 1) % 2 == 0
                )
            if q_size > 1:
                parity_transfer_cases += 1
                parity_transfer_exits += int(
                    (p_size + 1) % 2 == 0 and (q_size - 1) % 2 == 0
                )

    required_files = [
        ART / "child_phys_math_eqsrc_orientation_torsor_descent_law_smuggling_audit.yaml",
        ART / "child_phys_phil_eqsrc_orientation_torsor_descent_law_smuggling_audit.yaml",
        ART / "parent_conflict_review_eqsrc_orientation_torsor_descent_law_smuggling_audit.yaml",
        ART / "parent_fusion_notes_eqsrc_orientation_torsor_descent_law_smuggling_audit.md",
        ART / "eqsrc_orientation_torsor_descent_law_smuggling_audit.tex",
        ART / "eqsrc_orientation_torsor_descent_law_smuggling_audit_receipt.md",
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260718-040.md",
        TASK / "documentation_impact.yaml",
        TASK / "jobs/AJ-RT-20260718-040-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260718-040-001.yaml",
        TASK / "roles/smuggling-auditor@0.2.0--RT-20260718-040.yaml",
        ROOT / "research_control/handoffs/handoff-0765.yaml",
        ROOT / "research_control/handoffs/handoff-0765.md",
    ]
    missing_files = [
        str(path.relative_to(ROOT)) for path in required_files if not path.is_file()
    ]
    candidate_hash = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
    audit_path = ART / "eqsrc_orientation_torsor_descent_law_smuggling_audit.tex"
    audit_text = audit_path.read_text() if audit_path.is_file() else ""
    required_tokens = [
        "blocked\\_adoption\\_open\\_continuation",
        "new\\_ontology\\_primitive\\_candidate",
        "Three equivariant line families",
        "Associated-state retyping",
        "Variation nondiscrimination",
        "next lawful route",
    ]
    missing_tokens = [token for token in required_tokens if token not in audit_text]

    checks = {
        "candidate_hash_matches": candidate_hash == EXPECTED_CANDIDATE_HASH,
        "candidate_fibre_equivariance_holds": equivariance_holds,
        "descended_candidate_line_is_q_line": descended_candidate_line == line(Q),
        "three_equivariant_line_families": len(equivariant_line_families) == 3,
        "three_distinct_descended_lines": descended_lines == set(nonzero_lines),
        "source_swap_is_identity_on_all_associated_classes": (
            source_swap_fixed_classes == 8
        ),
        "exact_fibre_pullback": fibre_pullback_mismatches == 0,
        "associated_relation_has_eight_pairs": len(candidate_relation_pairs) == 8,
        "constant_one_controls_preserve_all_three_relations": (
            constant_one_translation_failures == 0
        ),
        "all_translations_preserve_all_three_relations": (
            full_translation_failures == 0
        ),
        "gl2_count_is_6": len(matrices) == 6,
        "full_gl2_line_orbit_has_three_lines": line_orbit == set(nonzero_lines),
        "affine_group_count_is_24": len(affine_maps) == 24,
        "each_line_has_eight_affine_relation_stabilizers": (
            relation_stabilizers_by_line == [8, 8, 8]
        ),
        "each_line_has_four_quotient_label_fixers": (
            quotient_label_fixers_by_line == [4, 4, 4]
        ),
        "each_line_has_four_affine_subset_stabilizers": (
            affine_line_subset_stabilizers_by_line == [4, 4, 4]
        ),
        "coordinate_relations_have_four_joint_stabilizers": (
            coordinate_relation_joint_stabilizers == 4
        ),
        "unordered_coordinate_pair_has_eight_stabilizers": (
            coordinate_relation_pair_stabilizers == 8
        ),
        "constant_one_translation_fixes_only_one_line_quotient": (
            constant_one_label_fixed_lines == 1
        ),
        "internal_complement_exchanges_coordinate_lines": (
            internal_complement_image == line(P)
        ),
        "one_point_transfers_exit_both_odd_domain": (
            parity_transfer_cases > 0
            and parity_transfer_exits == parity_transfer_cases
        ),
        "required_files_present": not missing_files,
        "required_audit_tokens_present": not missing_tokens,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    payload = {
        "status": status,
        "candidate_hash": candidate_hash,
        "states": len(states),
        "orientation_state_pairs": 2 * len(states),
        "associated_classes": len(
            {
                canonical_associated_class(orientation, state)
                for orientation in (0, 1)
                for state in states
            }
        ),
        "candidate_relation_ordered_pairs": len(candidate_relation_pairs),
        "equivariant_line_family_count": len(equivariant_line_families),
        "distinct_descended_line_count": len(descended_lines),
        "source_swap_fixed_associated_classes": source_swap_fixed_classes,
        "fibre_pullback_mismatches": fibre_pullback_mismatches,
        "constant_one_translation_failures": constant_one_translation_failures,
        "full_translation_failures": full_translation_failures,
        "gl2_count": len(matrices),
        "full_gl2_line_orbit_size": len(line_orbit),
        "affine_group_count": len(affine_maps),
        "relation_stabilizers_by_line": relation_stabilizers_by_line,
        "quotient_label_fixers_by_line": quotient_label_fixers_by_line,
        "affine_line_subset_stabilizers_by_line": (
            affine_line_subset_stabilizers_by_line
        ),
        "coordinate_relation_joint_stabilizers": (
            coordinate_relation_joint_stabilizers
        ),
        "coordinate_relation_pair_stabilizers": (
            coordinate_relation_pair_stabilizers
        ),
        "constant_one_label_fixed_lines": constant_one_label_fixed_lines,
        "parity_transfer_cases": parity_transfer_cases,
        "parity_transfer_exits": parity_transfer_exits,
        "missing_files": missing_files,
        "missing_tokens": missing_tokens,
        "checks": checks,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
