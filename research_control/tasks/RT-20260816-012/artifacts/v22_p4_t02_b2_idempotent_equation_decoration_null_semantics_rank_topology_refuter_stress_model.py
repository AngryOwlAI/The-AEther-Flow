#!/usr/bin/env python3
"""Exact finite controls for the RT012 idempotent-decoration Refuter stress.

This model is conformance evidence only. It neither adopts an ontology nor
assigns occurrence, probability, physical, empirical, or P4 meaning.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction


def matmul(a, b):
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0)) for j in range(len(b[0])))
        for i in range(len(a))
    )


def matsub(a, b):
    return tuple(tuple(a[i][j] - b[i][j] for j in range(len(a[0]))) for i in range(len(a)))


def eye(n):
    return tuple(tuple(Fraction(int(i == j)) for j in range(n)) for i in range(n))


def zero(n):
    return tuple(tuple(Fraction(0) for _ in range(n)) for _ in range(n))


def rank(matrix):
    a = [list(row) for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col] != 0), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [v / scale for v in a[pivot_row]]
        for r in range(rows):
            if r == pivot_row:
                continue
            factor = a[r][col]
            if factor:
                a[r] = [a[r][c] - factor * a[pivot_row][c] for c in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def upper_shear(n, t):
    g = [list(row) for row in eye(n)]
    g[0][1] = t
    return tuple(tuple(row) for row in g)


def upper_shear_inverse(n, t):
    return upper_shear(n, -t)


def diag_projector(n, r):
    return tuple(tuple(Fraction(int(i == j and i < r)) for j in range(n)) for i in range(n))


def check(name, condition, evidence):
    return {"id": name, "pass": bool(condition), "evidence": evidence}


def main():
    n = 6
    z = zero(n)
    ident = eye(n)
    p1 = diag_projector(n, 1)
    p3 = diag_projector(n, 3)
    t = Fraction(1, 1000)
    g = upper_shear(n, t)
    gi = upper_shear_inverse(n, t)
    pt = matmul(matmul(g, p1), gi)
    delta = matsub(pt, p1)
    eps = Fraction(1, 1000)
    qeps = tuple(tuple(eps * ident[i][j] for j in range(n)) for i in range(n))
    qdef = matsub(matmul(qeps, qeps), qeps)

    checks = [
        check("EX-01", matmul(z, z) == z, "zero is idempotent"),
        check("EX-02", matmul(ident, ident) == ident, "identity is idempotent"),
        check("EX-03", rank(z) == 0, "rank zero endpoint is 0"),
        check("EX-04", rank(ident) == 6, "rank identity endpoint is 6"),
        check("EX-05", z != ident, "two full-GL6-natural endpoints are distinct"),
        check("EX-06", matmul(pt, pt) == pt, "conjugated rank-one family stays exactly idempotent"),
        check("EX-07", rank(pt) == 1, "conjugation preserves rank one"),
        check("EX-08", rank(delta) == 1, "rank(P_t-P_0)=1 for nonzero shear"),
        check("EX-09", delta[0][1] == -t, "entrywise perturbation magnitude is 1/1000"),
        check("EX-10", matmul(p3, p3) == p3 and rank(p3) == 3, "intermediate exact rank stratum exists"),
        check("EX-11", matmul(qeps, qeps) != qeps, "epsilon identity is not exactly idempotent"),
        check("EX-12", qdef[0][0] == eps * eps - eps, "approximate defect is epsilon(epsilon-1)"),
        check("EX-13", abs(qdef[0][0]) == Fraction(999, 1_000_000), "exact defect magnitude at epsilon=1/1000"),
        check("EX-14", rank(matsub(ident, z)) == 6, "rank distance separates natural endpoints by six"),
        check("EX-15", rank(matsub(p3, z)) == 3, "rank descendant varies over same reduct"),
        check("EX-16", rank(matsub(p3, ident)) == 3, "complementary kernel descendant also varies"),
        check("EX-17", matmul(g, gi) == ident and matmul(gi, g) == ident, "shear inverse exact"),
        check("EX-18", matmul(matmul(g, z), gi) == z, "zero fixed by conjugation"),
        check("EX-19", matmul(matmul(g, ident), gi) == ident, "identity fixed by conjugation"),
        check("EX-20", pt != p1, "noncentral projectors move under full-frame conjugation"),
        check("EX-21", rank(p1) != rank(ident), "rank cannot factor through a forgetful map with both decorations"),
        check("EX-22", p1 != ident and p1 != z, "nontrivial proper projector requires extra selection data"),
        check("EX-23", len({rank(diag_projector(n, r)) for r in range(n + 1)}) == 7, "all exact ranks 0 through 6 occur"),
        check("EX-24", all(matmul(diag_projector(n, r), diag_projector(n, r)) == diag_projector(n, r) for r in range(n + 1)), "canonical representatives for all rank strata are idempotent"),
    ]
    payload_core = {
        "model_id": "MODEL-V22-P4T02-B2-IDEMPOTENT-NULL-RANK-TOPOLOGY-REFUTER-V1",
        "dimension": n,
        "check_count": len(checks),
        "pass_count": sum(item["pass"] for item in checks),
        "checks": checks,
        "authority": {
            "source_law_adopted": False,
            "physical_semantics_established": False,
            "p4_credit": False,
            "global_no_go": False,
        },
    }
    encoded = json.dumps(payload_core, sort_keys=True, separators=(",", ":")).encode()
    payload_core["payload_sha256"] = hashlib.sha256(encoded).hexdigest()
    print(json.dumps(payload_core, indent=2, sort_keys=True))
    if payload_core["pass_count"] != payload_core["check_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
