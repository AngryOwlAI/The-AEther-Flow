#!/usr/bin/env python3
"""Exact checks for the RT017 focused general-rank source-purity audit.

This is draft/control conformance support.  It does not establish physical
dimension, source-law adoption, P7 universality, a causal cone, or g_eff.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parents[4]
RT016 = REPO / "research_control/tasks/RT-20260810-016/artifacts"
CANDIDATE = RT016 / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_v1.tex"
RECORD = RT016 / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_record_v1.yaml"
CONTROLS = RT016 / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_controls_v1.yaml"

EXPECTED_HASHES = {
    CANDIDATE: "c977c9a93e3a543fe18378f51b83773211b483df3377d4187c506ff88768bba4",
    RECORD: "117a330c085dcbb384e5e4e236642ea0a65b3afbb151dbb2e978ffe2f931a035",
    CONTROLS: "1ddcedd031a1eb6688e897cde0be52bc9ae61c134f4d4a5decb2aefdd49fb5f5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((i for i in range(pivot_row, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [x / scale for x in a[pivot_row]]
        for i in range(rows):
            if i == pivot_row or not a[i][col]:
                continue
            factor = a[i][col]
            a[i] = [x - factor * y for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def standard_sum_matrix(r: int, sign: int) -> list[list[Fraction]]:
    """Rows of [e_1 ... e_r sign*1_r]."""
    return [
        [Fraction(int(i == j)) for j in range(r)] + [Fraction(sign)]
        for i in range(r)
    ]


def embed_zero_rows(matrix: list[list[Fraction]], extra: int) -> list[list[Fraction]]:
    return matrix + [[Fraction(0) for _ in matrix[0]] for _ in range(extra)]


def column_signs(matrix: list[list[Fraction]], covector: Iterable[Fraction]) -> tuple[int, ...]:
    coeffs = list(covector)
    values = [sum(coeffs[i] * matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))]
    return tuple(1 if value > 0 else -1 if value < 0 else 0 for value in values)


def audit() -> dict[str, object]:
    source_hashes = {str(path.relative_to(REPO)): sha256(path) for path in EXPECTED_HASHES}
    hash_checks = {str(path.relative_to(REPO)): source_hashes[str(path.relative_to(REPO))] == expected for path, expected in EXPECTED_HASHES.items()}

    rank_checks: list[dict[str, object]] = []
    for r in range(1, 9):
        plus = standard_sum_matrix(r, 1)
        minus = standard_sum_matrix(r, -1)
        for label, matrix in (("plus", plus), ("minus", minus)):
            embedded = embed_zero_rows(matrix, 3)
            base_covector = [Fraction(1)] * r
            embedded_covector = base_covector + [Fraction(7), Fraction(-11), Fraction(13)]
            rank_checks.append(
                {
                    "rank": r,
                    "branch": label,
                    "base_rank": rank(matrix),
                    "embedded_rank": rank(embedded),
                    "base_signs": column_signs(matrix, base_covector),
                    "embedded_signs": column_signs(embedded, embedded_covector),
                    "embedding_neutral": rank(matrix) == rank(embedded) == r
                    and column_signs(matrix, base_covector) == column_signs(embedded, embedded_covector),
                }
            )

    tested_ranks = tuple(range(1, 9))
    caps = tuple(range(max(tested_ranks), max(tested_ranks) + 9))
    cap_memberships = {cap: tuple(r <= cap for r in tested_ranks) for cap in caps}
    finite_window_nonidentifiable = len(set(cap_memberships.values())) == 1 and all(next(iter(cap_memberships.values())))

    counts = {
        r: {
            "covectors_each_sign": 3 ** (r + 1) - 2 ** (r + 2) + 2,
            "topes_each_sign": 2 ** (r + 1) - 2,
            "negative_circuit_support": r + 1,
        }
        for r in (5, 6)
    }
    aggregate_covectors = 2 * sum(item["covectors_each_sign"] for item in counts.values())
    aggregate_topes = 2 * sum(item["topes_each_sign"] for item in counts.values())

    candidate_text = CANDIDATE.read_text(encoding="utf-8")
    quarantine_tokens = {
        "arbitrary_finite_domain": "arbitrary finite rank" in candidate_text,
        "sharp_support_bound": "r+1" in candidate_text or "r + 1" in candidate_text,
        "nonphysical_conformance": "nonphysical conformance" in candidate_text,
        "former_cap_not_general_domain": "1\\le r\\le4" not in candidate_text.replace(" ", ""),
    }

    checks = {
        "source_hashes": all(hash_checks.values()),
        "effective_span_embedding_neutral": all(item["embedding_neutral"] for item in rank_checks),
        "finite_window_cap_nonidentifiable": finite_window_nonidentifiable,
        "rank_five_six_counts": aggregate_covectors == 5072 and aggregate_topes == 376,
        "sharp_crossing_supports": counts[5]["negative_circuit_support"] == 6 and counts[6]["negative_circuit_support"] == 7,
        "conformance_quarantine_tokens": all(quarantine_tokens.values()),
    }
    return {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_general_rank_post_repair_audit_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "authority": "draft_control_conformance_only",
        "checks": checks,
        "source_hash_checks": hash_checks,
        "rank_embedding_checks": rank_checks,
        "finite_window_nonidentifiability": {
            "tested_ranks": tested_ranks,
            "compatible_finite_caps": caps,
            "all_caps_agree_on_test_window": finite_window_nonidentifiable,
            "inference_block": "Finite fixture success selects neither an unrestricted theorem domain nor a physical dimension.",
        },
        "rank_five_six_controls": {
            "counts": counts,
            "aggregate_covectors": aggregate_covectors,
            "aggregate_topes": aggregate_topes,
        },
        "quarantine_tokens": quarantine_tokens,
        "claim_boundary": {
            "source_purity_inferred_from_validator": False,
            "physical_dimension_inferred": False,
            "p7_universality_inferred": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
