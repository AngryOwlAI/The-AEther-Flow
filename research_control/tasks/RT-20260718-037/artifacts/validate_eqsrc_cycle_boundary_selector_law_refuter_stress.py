#!/usr/bin/env python3
"""Validate the bounded cycle-boundary selector Refuter stress.

The finite checks support a draft/control obstruction record. PASS is not
physics proof, ontology adoption, or claim-promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260718-037"
ART = TASK / "artifacts"
CANDIDATE = ROOT / (
    "research_control/tasks/RT-20260718-035/artifacts/"
    "eqsrc_cycle_boundary_selector_law_candidate_v1.tex"
)
AUDIT = ROOT / (
    "research_control/tasks/RT-20260718-036/artifacts/"
    "eqsrc_cycle_boundary_selector_law_smuggling_audit.tex"
)
REPORT = ART / "eqsrc_cycle_boundary_selector_law_refuter_stress_validation.json"
EXPECTED_CANDIDATE_HASH = (
    "64901302bd6f37819ebd30aaaebaf39611d2c71c97d45b6cea6a39df11e0df94"
)
EXPECTED_AUDIT_HASH = (
    "6169702f60659488e05cf0386afedc4b58b7395926923d5a2d365512182ca78f"
)
STATES = tuple(itertools.product((0, 1), repeat=2))
ZERO = (0, 0)
P = (1, 0)
Q = (0, 1)
D = (1, 1)
LINES = (
    frozenset((ZERO, P)),
    frozenset((ZERO, Q)),
    frozenset((ZERO, D)),
)


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] ^ b[0], a[1] ^ b[1])


def mat_vec(
    matrix: tuple[int, int, int, int], vector: tuple[int, int]
) -> tuple[int, int]:
    return (
        matrix[0] * vector[0] ^ matrix[1] * vector[1],
        matrix[2] * vector[0] ^ matrix[3] * vector[1],
    )


def invertible_matrices() -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        matrix
        for matrix in itertools.product((0, 1), repeat=4)
        if matrix[0] * matrix[3] ^ matrix[1] * matrix[2]
    )


def relation(line: frozenset[tuple[int, int]]) -> frozenset[tuple[object, object]]:
    return frozenset(
        (left, right)
        for left in STATES
        for right in STATES
        if add(left, right) in line
    )


def compose_affine(
    left: tuple[tuple[int, int, int, int], tuple[int, int]],
    right: tuple[tuple[int, int, int, int], tuple[int, int]],
) -> tuple[tuple[int, int, int, int], tuple[int, int]]:
    lm, lt = left
    rm, rt = right
    columns = (mat_vec(lm, (rm[0], rm[2])), mat_vec(lm, (rm[1], rm[3])))
    product = (columns[0][0], columns[1][0], columns[0][1], columns[1][1])
    return (product, add(mat_vec(lm, rt), lt))


def element_order(
    item: tuple[tuple[int, int, int, int], tuple[int, int]]
) -> int:
    identity = ((1, 0, 0, 1), ZERO)
    value = identity
    for order in range(1, 9):
        value = compose_affine(value, item)
        if value == identity:
            return order
    raise AssertionError("unexpected affine element order")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    matrices = invertible_matrices()
    line_orbit = {
        frozenset(mat_vec(matrix, vector) for vector in LINES[0])
        for matrix in matrices
    }
    common_invariant_lines = [
        line
        for line in LINES
        if all(
            frozenset(mat_vec(matrix, vector) for vector in line) == line
            for matrix in matrices
        )
    ]

    candidate_line = LINES[1]
    candidate_relation = relation(candidate_line)
    complement_relation = relation(LINES[0])
    relation_stabilizers = []
    label_fixers = []
    declared = []
    for matrix in matrices:
        for translation in STATES:
            affine = (matrix, translation)
            image = {
                state: add(mat_vec(matrix, state), translation) for state in STATES
            }
            preserves_relation = all(
                ((left, right) in candidate_relation)
                == ((image[left], image[right]) in candidate_relation)
                for left in STATES
                for right in STATES
            )
            fixes_label = all(image[state][0] == state[0] for state in STATES)
            if preserves_relation:
                relation_stabilizers.append(affine)
            if fixes_label:
                label_fixers.append(affine)
            if matrix == (1, 0, 0, 1) and translation in candidate_line:
                declared.append(affine)

    relation_orders = sorted(element_order(item) for item in relation_stabilizers)
    label_orders = sorted(element_order(item) for item in label_fixers)
    declared_orders = sorted(element_order(item) for item in declared)

    field_cases = []
    for prime in (2, 3, 5):
        for mark_size in range(1, 11):
            coefficient = mark_size % prime
            kernel_size = prime if coefficient else prime * prime
            field_cases.append(
                {
                    "prime": prime,
                    "mark_size": mark_size,
                    "collapsed": coefficient == 0,
                    "kernel_size": kernel_size,
                }
            )

    required_files = [
        ART / "child_phys_math_eqsrc_cycle_boundary_selector_law_refuter_stress.yaml",
        ART / "child_phys_phil_eqsrc_cycle_boundary_selector_law_refuter_stress.yaml",
        ART / "parent_conflict_review_eqsrc_cycle_boundary_selector_law_refuter_stress.yaml",
        ART / "parent_fusion_notes_eqsrc_cycle_boundary_selector_law_refuter_stress.md",
        ART / "eqsrc_cycle_boundary_selector_law_refuter_stress.tex",
        ART / "eqsrc_cycle_boundary_selector_law_refuter_stress_receipt.md",
        ART / "eqsrc_cycle_boundary_selector_law_refuter_countermodel.yaml",
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260718-037.md",
        TASK / "documentation_impact.yaml",
        TASK / "jobs/AJ-RT-20260718-037-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260718-037-001.yaml",
        TASK / "roles/refuter@0.2.0--RT-20260718-037.yaml",
        ROOT / "research_control/handoffs/handoff-0762.yaml",
        ROOT / "research_control/handoffs/handoff-0762.md",
    ]
    missing_files = [
        str(path.relative_to(ROOT)) for path in required_files if not path.is_file()
    ]
    fused_text = (ART / "eqsrc_cycle_boundary_selector_law_refuter_stress.tex").read_text()
    required_tokens = [
        "scoped\\_obstruction",
        "locally\\_frozen",
        "orientation-descent countermodel",
        "characteristic--cardinality branch theorem",
        "strict \\(2<4<8\\) variation hierarchy",
        "theoretical-continuation-selector",
    ]
    missing_tokens = [token for token in required_tokens if token not in fused_text]

    checks = {
        "candidate_hash_matches": hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
        == EXPECTED_CANDIDATE_HASH,
        "audit_hash_matches": hashlib.sha256(AUDIT.read_bytes()).hexdigest()
        == EXPECTED_AUDIT_HASH,
        "gl2_order_is_6": len(matrices) == 6,
        "three_nonzero_proper_lines": len(LINES) == 3,
        "gl2_line_action_is_transitive": line_orbit == set(LINES),
        "no_common_invariant_proper_line": not common_invariant_lines,
        "complement_relations_differ": candidate_relation != complement_relation,
        "complement_relation_symmetric_difference_is_8": len(
            candidate_relation.symmetric_difference(complement_relation)
        )
        == 8,
        "relation_stabilizer_order_is_8": len(relation_stabilizers) == 8,
        "label_fixer_order_is_4": len(label_fixers) == 4,
        "declared_variation_order_is_2": len(declared) == 2,
        "variation_inclusions_are_strict": set(declared) < set(label_fixers)
        < set(relation_stabilizers),
        "relation_stabilizer_has_d8_order_profile": relation_orders
        == [1, 2, 2, 2, 2, 2, 4, 4],
        "label_fixer_has_v4_order_profile": label_orders == [1, 2, 2, 2],
        "declared_has_c2_order_profile": declared_orders == [1, 2],
        "field_cardinality_branch_formula": all(
            (case["kernel_size"] == case["prime"] * case["prime"])
            == (case["mark_size"] % case["prime"] == 0)
            for case in field_cases
        ),
        "required_files_present": not missing_files,
        "required_tokens_present": not missing_tokens,
    }
    payload = {
        "schema": "eqsrc-cycle-boundary-selector-refuter-stress-validation.v1",
        "task_id": "RT-20260718-037",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "support_only": True,
        "counts": {
            "gl2_order": len(matrices),
            "nonzero_proper_lines": len(LINES),
            "line_orbit_size": len(line_orbit),
            "affine_group_order": len(matrices) * len(STATES),
            "relation_stabilizer_order": len(relation_stabilizers),
            "pointwise_label_fixer_order": len(label_fixers),
            "declared_variation_order": len(declared),
            "orientation_relation_symmetric_difference": len(
                candidate_relation.symmetric_difference(complement_relation)
            ),
            "field_cardinality_cases": len(field_cases),
        },
        "group_order_profiles": {
            "relation_stabilizer": relation_orders,
            "pointwise_label_fixer": label_orders,
            "declared_variations": declared_orders,
        },
        "checks": checks,
        "missing_files": missing_files,
        "missing_tokens": missing_tokens,
        "authority_note": (
            "Operational finite support only; not physics proof, ontology "
            "adoption, or claim-promotion authority."
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
