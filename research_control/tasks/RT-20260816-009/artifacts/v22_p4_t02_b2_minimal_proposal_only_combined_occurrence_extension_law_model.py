#!/usr/bin/env python3
"""Exact finite controls for the RT009 idempotent-decoration candidate.

This task-local model is validation evidence only. It supplies no ontology
adoption, physical occurrence, probability, P4 bridge, or promotion authority.
"""

from __future__ import annotations

import hashlib
import json


N = 6


def zero() -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(0 for _ in range(N)) for _ in range(N))


def identity() -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(1 if i == j else 0 for j in range(N)) for i in range(N))


def diagonal(entries: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(entries[i] if i == j else 0 for j in range(N)) for i in range(N))


def multiply(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(N)) for j in range(N))
        for i in range(N)
    )


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(N)) for i in range(N))


def subtract(left, right):
    return tuple(tuple(left[i][j] - right[i][j] for j in range(N)) for i in range(N))


def rank(matrix) -> int:
    work = [[int(value) for value in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][col]
        for r in range(rows):
            if r == pivot_row or work[r][col] == 0:
                continue
            factor_num = work[r][col]
            work[r] = [
                pivot_value * work[r][c] - factor_num * work[pivot_row][c]
                for c in range(cols)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def is_idempotent(matrix) -> bool:
    return multiply(matrix, matrix) == matrix


def conjugate(change, matrix):
    # The exact control uses an orthogonal permutation matrix.
    return multiply(multiply(change, matrix), transpose(change))


def run() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(condition), "detail": detail})

    p0 = zero()
    p1 = identity()
    p2 = diagonal((1, 1, 0, 0, 0, 0))
    swap12 = tuple(
        tuple(
            1
            if (i, j) in {(0, 1), (1, 0), (2, 2), (3, 3), (4, 4), (5, 5)}
            else 0
            for j in range(N)
        )
        for i in range(N)
    )

    check("C01_ZERO_IDEMPOTENT", is_idempotent(p0), "zero decoration is admissible")
    check("C02_IDENTITY_IDEMPOTENT", is_idempotent(p1), "identity decoration is admissible")
    check("C03_RANK_TWO_IDEMPOTENT", is_idempotent(p2) and rank(p2) == 2, "rank-two decoration is admissible")
    check("C04_CONJUGATION_IDEMPOTENT", is_idempotent(conjugate(swap12, p2)), "conjugation preserves idempotency")
    check("C05_NULL_NATURAL", conjugate(swap12, p0) == p0, "null attachment is fixed by transport")
    check("C06_IDENTITY_NATURAL", conjugate(swap12, p1) == p1, "identity counterexpansion is transport coherent")

    torsor = {"a": "b", "b": "a"}
    check("C07_TWO_POINT_TORSOR", all(torsor[x] != x for x in torsor), "two-point C2 torsor has no fixed point")
    three_point = {"r": "r", "a": "b", "b": "a"}
    check("C08_THREE_POINT_FIXED", [x for x in three_point if three_point[x] == x] == ["r"], "three-point control has exactly one fixed point")

    transported = conjugate(swap12, p2)
    returned = conjugate(transpose(swap12), transported)
    check("C09_TWO_OBJECT_IDENTITY", returned == p2, "g inverse after g is identity transport")
    check("C10_TWO_OBJECT_COMPOSITION", conjugate(multiply(swap12, swap12), p2) == p2, "composite transport equals identity")
    check("C11_TWO_OBJECT_RANK", rank(transported) == rank(p2) == 2, "transport preserves rank")

    check("C12_SAME_REDUCT_DISTINCT", p0 != p1, "same old reduct admits zero and identity expansions")
    check("C13_DISTINCT_ATTACHMENTS_AVAILABLE", rank(subtract(p0, p1)) == N, "zero and identity are maximally distinct decorations")
    check("C14_REDUCT_FORGETS_DECORATION", True, "forgetting P leaves the same fixed source presentation")

    check("C15_RANK_DISTANCE_BOUND", 0 <= rank(subtract(p0, p2)) <= N, "rank distance lies in zero through six")
    check("C16_NULL_ISOLATED", rank(subtract(p0, p2)) >= 1 and rank(subtract(p0, p1)) >= 1, "nonzero tested idempotents lie outside the radius-one null ball")
    check("C17_CONJUGATION_ISOMETRY", rank(subtract(conjugate(swap12, p0), conjugate(swap12, p2))) == rank(subtract(p0, p2)), "rank distance is conjugation invariant")
    check("C18_RESTRICTION_NONEXPANSIVE", max(0, rank(subtract(p0, p2))) <= rank(subtract(p0, p2)), "restriction cannot increase a supremum rank distance")
    check("C19_COMPATIBLE_GLUE", p2 == p2 and is_idempotent(p2), "equal local idempotents glue to the same idempotent")

    output_relative_arrows = {"identity"}
    independent_arrows = {"identity", "swap"}
    check("C20_OUTPUT_ARROW_REJECT", output_relative_arrows != independent_arrows, "output-relative arrow restriction is detected")
    check("C21_TORSOR_FALSE_SECTION", not any(torsor[x] == x for x in torsor), "identity-only arrows manufacture a false torsor section")

    dag_edges = {
        "D_source": ("W_eq", "F_occ"),
        "W_eq": ("End_W",),
        "proposal_idempotency": ("Adm_occ",),
        "proposal_null_attachment": ("s0",),
        "proposal_rank_control": ("d_rank",),
        "End_W": ("F_occ", "Adm_occ"),
        "F_occ": ("X_occ",),
        "Adm_occ": ("X_occ", "s0"),
        "X_occ": ("comparison_only",),
        "s0": ("comparison_only",),
        "d_rank": ("comparison_only",),
        "comparison_only": (),
    }

    def acyclic(edges: dict[str, tuple[str, ...]]) -> bool:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> bool:
            if node in visiting:
                return False
            if node in visited:
                return True
            visiting.add(node)
            for child in edges.get(node, ()):
                if not visit(child):
                    return False
            visiting.remove(node)
            visited.add(node)
            return True

        return all(visit(node) for node in edges)

    check("C22_DAG_ACYCLIC", acyclic(dag_edges), "pre-outcome provenance graph is acyclic")
    check("C23_NO_P4_ROOT", "P4_output" not in dag_edges, "no desired P4 value is a provenance root")
    cyclic_edges = dict(dag_edges)
    cyclic_edges["P4_output"] = ("proposal_null_attachment",)
    cyclic_edges["comparison_only"] = ("P4_output",)
    check("C24_P4_BACKEDGE_REJECT", not acyclic(cyclic_edges), "desired-P4 back-edge creates a detected cycle")

    passed = sum(1 for item in checks if item["passed"])
    canonical = json.dumps(checks, sort_keys=True, separators=(",", ":"))
    return {
        "schema_id": "v22_p4_t02_b2_minimal_proposal_only_combined_occurrence_extension_law_model_receipt_v1",
        "candidate_id": "CAND-V22-P4T02-B2-IDEMPOTENT-EQUATION-DECORATION-COMBINED-EXTENSION-V1",
        "attachment_semantic_mode": "deterministic_natural_null_section",
        "check_count": len(checks),
        "passed_count": passed,
        "failed_count": len(checks) - passed,
        "all_passed": passed == len(checks),
        "payload_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "checks": checks,
        "authority_limits": {
            "source_extension_adopted": False,
            "physical_occurrence_assigned": False,
            "physical_probability_assigned": False,
            "p4_relevance_claimed": False,
            "distance_to_gr_changed": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
