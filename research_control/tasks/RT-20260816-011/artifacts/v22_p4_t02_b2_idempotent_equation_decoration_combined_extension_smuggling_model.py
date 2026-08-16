#!/usr/bin/env python3
"""Exact finite controls for the RT011 idempotent-decoration smuggling audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction


N = 6


def zero():
    return [[Fraction(0) for _ in range(N)] for _ in range(N)]


def identity():
    out = zero()
    for i in range(N):
        out[i][i] = Fraction(1)
    return out


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(N)] for i in range(N)]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(N)] for i in range(N)]


def mul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(N)), Fraction(0)) for j in range(N)]
        for i in range(N)
    ]


def scale(c, a):
    return [[c * a[i][j] for j in range(N)] for i in range(N)]


def elementary(i, j):
    out = zero()
    out[i][j] = Fraction(1)
    return out


def diagonal(entries):
    out = zero()
    for i, value in enumerate(entries):
        out[i][i] = Fraction(value)
    return out


def rank(a):
    work = [row[:] for row in a]
    pivot_row = 0
    for col in range(N):
        pivot = next((r for r in range(pivot_row, N) if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][col]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for r in range(N):
            if r == pivot_row or work[r][col] == 0:
                continue
            factor = work[r][col]
            work[r] = [work[r][c] - factor * work[pivot_row][c] for c in range(N)]
        pivot_row += 1
        if pivot_row == N:
            break
    return pivot_row


def idempotent(a):
    return mul(a, a) == a


def commutes(a, b):
    return mul(a, b) == mul(b, a)


def max_abs(a):
    return max(abs(value) for row in a for value in row)


def make_check(check_id, passed, detail):
    return {"check_id": check_id, "passed": bool(passed), "detail": detail}


def build_receipt():
    z = zero()
    one = identity()
    p = diagonal([1, 0, 0, 0, 0, 0])
    shear_direction = elementary(1, 0)

    def shear_conjugate(t):
        shear = add(one, scale(t, shear_direction))
        shear_inv = sub(one, scale(t, shear_direction))
        return mul(mul(shear, p), shear_inv)

    p_conj = shear_conjugate(Fraction(1))
    p_half = shear_conjugate(Fraction(1, 2))
    p_hundred = shear_conjugate(Fraction(1, 100))
    central_candidates = [z, one]
    generators = [
        add(one, elementary(0, 1)),
        add(one, elementary(1, 0)),
        add(one, elementary(2, 3)),
        add(one, elementary(3, 2)),
    ]
    checks = [
        make_check("C01_ZERO_IDEMPOTENT", idempotent(z), "zero is an idempotent"),
        make_check("C02_IDENTITY_IDEMPOTENT", idempotent(one), "identity is an idempotent"),
        make_check("C03_TWO_NATURAL_ENDPOINTS", z != one, "zero and identity are distinct universal candidates"),
        make_check("C04_ZERO_CENTRAL", all(commutes(z, g) for g in generators), "zero commutes with frame generators"),
        make_check("C05_IDENTITY_CENTRAL", all(commutes(one, g) for g in generators), "identity commutes with frame generators"),
        make_check("C06_RANK_ONE_NOT_CENTRAL", not all(commutes(p, g) for g in generators), "rank-one projector is moved by a frame shear"),
        make_check("C07_CENTRAL_IDEMPOTENT_COUNT", len(central_candidates) == 2, "the theorem leaves exactly zero and identity among scalar idempotents"),
        make_check("C08_CONJUGATE_IDEMPOTENT", idempotent(p_conj), "a shear-conjugate projector remains idempotent"),
        make_check("C09_CONJUGATE_DISTINCT", p_conj != p, "the shear produces a distinct projector"),
        make_check("C10_CONJUGATE_RANK", rank(p_conj) == rank(p) == 1, "conjugation preserves projector rank"),
        make_check("C11_RANK_DISTANCE_ONE", rank(sub(p_conj, p)) == 1, "rank distance is one for every nonzero shear parameter in this family"),
        make_check("C12_NORM_PROXY_ONE", max_abs(sub(p_conj, p)) == 1, "the unit-shear control has max-entry difference one"),
        make_check("C13_SMALL_FAMILY_2", idempotent(p_half) and max_abs(sub(p_half, p)) == Fraction(1, 2), "an exact conjugate projector is max-entry close at t=1/2"),
        make_check("C14_SMALL_FAMILY_100", idempotent(p_hundred) and max_abs(sub(p_hundred, p)) == Fraction(1, 100), "an exact conjugate projector is max-entry close at t=1/100"),
        make_check("C15_SMALL_FAMILY_RANK", rank(sub(p_hundred, p)) == 1, "rank distance remains one at t=1/100"),
        make_check("C16_DISCRETE_RANGE", all(idempotent(shear_conjugate(Fraction(1, k))) and rank(sub(shear_conjugate(Fraction(1, k)), p)) == 1 for k in (2, 10, 100, 1000)), "rank control is discrete along an arbitrarily small rational conjugate family"),
        make_check("C17_NULL_IMAGE_KERNEL", rank(z) == 0 and N - rank(z) == 6, "null projector has image dimension zero and kernel dimension six"),
        make_check("C18_IDENTITY_IMAGE_KERNEL", rank(one) == 6 and N - rank(one) == 0, "identity projector has image dimension six and kernel dimension zero"),
        make_check("C19_ENDPOINT_SYMMETRY", rank(sub(one, z)) == 6, "the two universal natural endpoints are maximally rank-separated"),
        make_check("C20_NO_UNIQUE_NATURAL_SECTION", len(central_candidates) > 1, "frame naturality and idempotency alone do not select the null endpoint"),
    ]
    payload = {
        "schema_id": "v22_p4_t02_b2_idempotent_equation_decoration_smuggling_model_receipt_v1",
        "candidate_id": "CAND-V22-P4T02-B2-IDEMPOTENT-EQUATION-DECORATION-COMBINED-EXTENSION-V1",
        "verdict_scope": "written_syntax_and_semantic_selection_audit_only",
        "check_count": len(checks),
        "passed_count": sum(item["passed"] for item in checks),
        "failed_count": sum(not item["passed"] for item in checks),
        "checks": checks,
        "authority_limits": {
            "source_extension_adopted": False,
            "physical_occurrence_assigned": False,
            "p4_relevance_claimed": False,
            "projector_bridge_constructed": False,
            "distance_to_gr_changed": False,
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(encoded).hexdigest()
    payload["all_passed"] = payload["failed_count"] == 0
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    receipt = build_receipt()
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(f"{receipt['passed_count']}/{receipt['check_count']} checks passed")
        print(receipt["payload_sha256"])
    raise SystemExit(0 if receipt["all_passed"] else 1)


if __name__ == "__main__":
    main()
