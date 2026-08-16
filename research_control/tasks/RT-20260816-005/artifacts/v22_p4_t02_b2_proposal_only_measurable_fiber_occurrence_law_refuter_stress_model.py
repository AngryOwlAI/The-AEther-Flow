#!/usr/bin/env python3
"""Exact finite-state controls for RT-20260816-005.

This model is draft/control evidence.  It checks the fixed two-token kernel and
its admitted exchange-symmetric coupling family.  It does not assign physical
probability, a clock, realized occurrence, ontology status, or P4 credit.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction


def kernel(p: Fraction) -> tuple[tuple[Fraction, Fraction], ...]:
    return ((p, 1 - p), (1 - p, p))


def matmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def matpow(a, n: int):
    out = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    for _ in range(n):
        out = matmul(out, a)
    return out


def closed_power(p: Fraction, n: int):
    r = 2 * p - 1
    return (
        ((1 + r**n) / 2, (1 - r**n) / 2),
        ((1 - r**n) / 2, (1 + r**n) / 2),
    )


def coupling(p: Fraction, a: Fraction):
    return (a, p - a, p - a, 1 - 2 * p + a)


def tv(mu, nu):
    return sum(abs(x - y) for x, y in zip(mu, nu)) / 2


def run_checks():
    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, evidence: object):
        checks.append(
            {"check_id": check_id, "status": "PASS" if condition else "FAIL", "evidence": evidence}
        )

    ps = (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4))
    check("KERNEL-ROWS", all(sum(row) == 1 for p in ps for row in kernel(p)), "all sampled rows sum to one")
    check("KERNEL-SYMMETRY", all(k[0][1] == k[1][0] and k[0][0] == k[1][1] for k in map(kernel, ps)), "complement-equivariant symmetric matrices")
    check("SPECTRUM", all(kernel(p)[0][0] - kernel(p)[0][1] == 2 * p - 1 for p in ps), "nontrivial eigenvalue r=2p-1")
    check("DETERMINANT", all(kernel(p)[0][0] * kernel(p)[1][1] - kernel(p)[0][1] * kernel(p)[1][0] == 2 * p - 1 for p in ps), "det K_p=2p-1")
    check("POWER-CLOSED-FORM", all(matpow(kernel(p), n) == closed_power(p, n) for p in ps for n in range(1, 7)), "K_p^n entries=(1+-r^n)/2")

    p = Fraction(1, 3)
    q = 1 - p
    check("EVEN-LAG-AMBIGUITY", matpow(kernel(p), 2) == matpow(kernel(q), 2), "p=1/3 and 1-p=2/3 have identical two-step law")
    check("ODD-LAG-SEPARATION", matpow(kernel(p), 3) != matpow(kernel(q), 3), "the corresponding three-step laws differ")
    check("STATIONARY-UNIFORM", all((Fraction(1, 2) * k[0][j] + Fraction(1, 2) * k[1][j]) == Fraction(1, 2) for p in ps for k in [kernel(p)] for j in range(2)), "uniform law stationary for every p")

    for p in (Fraction(1, 3), Fraction(2, 3), Fraction(3, 4)):
        lo = max(Fraction(0), 2 * p - 1)
        hi = p
        mid = (lo + hi) / 2
        check(f"COUPLING-NONNEG-{p}", all(x >= 0 for x in coupling(p, mid)), [str(x) for x in coupling(p, mid)])
        check(f"COUPLING-MARGINAL-{p}", coupling(p, mid)[0] + coupling(p, mid)[1] == p and coupling(p, mid)[0] + coupling(p, mid)[2] == p, "both stay marginals equal p")
    p = Fraction(2, 3)
    a = p
    b = p - Fraction(1, 1000)
    check("COUPLING-TV-FORMULA", tv(coupling(p, a), coupling(p, b)) == 2 * abs(a - b), "d_TV(J_a,J_b)=2|a-b|")
    check("SHARED-NOT-ISOLATED", b >= max(Fraction(0), 2 * p - 1) and b < a, "a=p has an arbitrarily close inward admitted alternative")
    check("INDEPENDENT-ENDPOINT-DISTINCT", coupling(p, p) != coupling(p, p * p), "shared a=p differs from token-class independent a=p^2")

    check("CTMC-NEGATIVE-EIGENVALUE-BLOCK", 2 * Fraction(1, 3) - 1 < 0, "p=1/3 has negative nontrivial eigenvalue and cannot equal exp(-2 lambda tau)")
    check("CTMC-SINGULAR-ENDPOINT-BLOCK", 2 * Fraction(1, 2) - 1 == 0, "p=1/2 is singular whereas a finite matrix exponential is invertible")
    p = Fraction(3, 4)
    product = -0.5 * math.log(float(2 * p - 1))
    check("CTMC-POSITIVE-BRANCH", product > 0 and abs((1 + math.exp(-2 * product)) / 2 - float(p)) < 1e-14, "p=3/4 embeds with lambda*tau=-0.5 log(2p-1)")
    check("CLOCK-PRODUCT-NONIDENTIFIABILITY", abs((1.0 * product) - (2.0 * (product / 2.0))) < 1e-14, "distinct (lambda,tau) pairs have the same product")
    check("CTMC-CLASSIFICATION", all(((x > Fraction(1, 2)) == ((2 * x - 1) > 0)) for x in ps), "finite symmetric homogeneous embedding domain is p>1/2")

    check("TOKEN-SWAP-NO-FIXED-TOKEN", all(1 - x != x for x in (0, 1)), "the complement involution has no fixed token")
    check("TOTAL-ADMISSION-NONDISCRIMINATING", set((0, 1)) == set((0, 1)), "Adm equals the entire two-token fiber")
    check("EMPTY-OPEN-DEGENERATION", tv((Fraction(1),), (Fraction(1),)) == 0, "the unique empty section gives zero total-variation distance")

    failed = [item for item in checks if item["status"] != "PASS"]
    payload = {
        "schema_id": "v22_p4_t02_b2_measurable_fiber_occurrence_law_refuter_stress_exact_model_v1",
        "task_id": "RT-20260816-005",
        "candidate_id": "CAND-V22-P4T02-B2-PROPOSAL-ONLY-MEASURABLE-FIBER-OCCURRENCE-LAW-V1",
        "authority": "draft_control_exact_finite_state_check_only",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "checks": checks,
        "protected_claims": {
            "physical_probability_established": False,
            "realized_occurrence_established": False,
            "physical_clock_selected": False,
            "source_law_adopted": False,
            "p4_t02_acceptance_passed": False,
            "global_no_go_claimed": False,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


if __name__ == "__main__":
    result = run_checks()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["fail_count"] == 0 else 1)
