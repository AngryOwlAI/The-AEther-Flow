#!/usr/bin/env python3
"""Deterministic support checker for the P5-T07 audit artifacts.

This checker verifies algebraic identities, finite stress samples, exact source
hashes, and required boundary markers.  PASS is not proof or promotion
authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260725-014"
ART = TASK / "artifacts"
REPORT = ART / "source_dynamics_audit_validation_receipt_v1.json"

SOURCES = {
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_object_v1.tex":
        "2520f82e54edcb2668446579ceed7a7dfc7a8abf995572aa9889a3d9a3a4467c",
    "research_control/tasks/RT-20260725-007/artifacts/phi_src_semiflow_semantics_v1.tex":
        "60f7358e0643195d4e2b79f7fda921da223ef940d00968588a4175d23cc0b70f",
    "research_control/tasks/RT-20260725-008/artifacts/cubic_amplitude_source_dynamics_v1.tex":
        "98ce6833f6e4d8be22837d25845d7fa62d6886049e168d121de5de0093703f6a",
    "research_control/tasks/RT-20260725-010/artifacts/cubic_amplitude_structural_analysis_v1.tex":
        "a9a9f42ff016febc0f40a8a4db32b09f670084bda2248704e290cf5bee02a06b",
    "research_control/tasks/RT-20260725-012/artifacts/cubic_amplitude_background_phase_analysis_v1.tex":
        "73895f1325fa83799c343e0c88d525e1d9e006254844b8f8bd7bb8fe2286f48d",
    "research_control/tasks/RT-20260725-013/artifacts/source_amplitude_resolution_coarse_graining_v1.tex":
        "a798e69875603ec3d0f9202ea67de18fcbc3dabf1cb1a178713f8dde9aefd074",
}

REQUIRED_ARTIFACTS = [
    "source_dynamics_package_audit_v1.tex",
    "refuter_stress_source_dynamics_v1.yaml",
    "candidate_disposition_freeze_v1.yaml",
    "child_phys_math_source_dynamics_audit.yaml",
    "child_phys_phil_source_dynamics_audit.yaml",
    "parent_conflict_review_source_dynamics_audit.yaml",
    "parent_fusion_notes_source_dynamics_audit.md",
    "source_dynamics_audit_receipt.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flow(a: float, lam: float, m: int, gamma: float) -> float:
    return a / (1.0 + 2.0 * m * gamma * (a ** (2 * m)) * lam) ** (1.0 / (2 * m))


def quantize(a: float, epsilon: float) -> float:
    if a == 0.0:
        return 0.0
    return epsilon * math.copysign(math.floor(abs(a) / epsilon + 0.5), a)


def close(x: float, y: float, tol: float = 2e-11) -> bool:
    return abs(x - y) <= tol * max(1.0, abs(x), abs(y))


def run_checks() -> dict:
    checks: list[dict] = []

    def record(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    for rel, expected in SOURCES.items():
        path = ROOT / rel
        actual = sha256(path) if path.is_file() else ""
        record(f"source_hash::{rel}", actual == expected, f"expected={expected} actual={actual}")

    artifact_hashes = {}
    for name in REQUIRED_ARTIFACTS:
        path = ART / name
        present = path.is_file()
        record(f"artifact_present::{name}", present, str(path))
        if present:
            artifact_hashes[str(path.relative_to(ROOT))] = sha256(path)

    samples = [-3.0, -1.25, -0.4, 0.0, 0.3, 1.5, 2.75]
    times = [0.0, 0.05, 0.4, 1.7]
    for m in (1, 2, 3, 4):
        gamma = 0.7 + 0.2 * m
        total_ok = all(math.isfinite(flow(a, lam, m, gamma)) for a in samples for lam in times)
        record(f"odd_power_total_m{m}", total_ok, "finite forward samples")
        odd_ok = all(close(flow(-a, lam, m, gamma), -flow(a, lam, m, gamma)) for a in samples for lam in times)
        record(f"odd_power_odd_m{m}", odd_ok, "reflection samples")
        semigroup_ok = all(
            close(flow(flow(a, s, m, gamma), t, m, gamma), flow(a, s + t, m, gamma))
            for a in samples for s in times for t in times
        )
        record(f"odd_power_semigroup_m{m}", semigroup_ok, "composition samples")
        attraction_ok = all(abs(flow(a, 1.0, m, gamma)) < abs(a) for a in samples if a != 0.0)
        record(f"odd_power_attraction_m{m}", attraction_ok, "strict nonzero contraction")

    relabel_ok = True
    for m in (1, 2, 3):
        gamma, c, d = 1.7, 2.3, 1.4
        gamma_prime = gamma / (c * d ** (2 * m))
        for b in samples:
            lhs = -(d / c) * gamma * (b / d) ** (2 * m + 1)
            rhs = -gamma_prime * b ** (2 * m + 1)
            relabel_ok = relabel_ok and close(lhs, rhs)
    record("coefficient_relabel_identity", relabel_ok, "gamma'=gamma/(c d^(2m))")

    resolution_ok = True
    for epsilon in (0.2, 0.7, 1.1):
        for d in (0.5, 1.3, 2.0):
            for a in [-2.2, -1.05, -0.51, -0.49, 0.0, 0.49, 0.51, 1.05, 2.2]:
                resolution_ok = resolution_ok and close(quantize(d * a, d * epsilon), d * quantize(a, epsilon))
    record("resolution_relabel_identity", resolution_ok, "N_(d epsilon)(d a)=d N_epsilon(a)")

    error_ok = True
    odd_ok = True
    for epsilon in (0.2, 0.7, 1.1):
        for k in range(-80, 81):
            a = k * epsilon / 17.0
            error_ok = error_ok and abs(quantize(a, epsilon) - a) <= epsilon / 2.0 + 1e-12
            odd_ok = odd_ok and close(quantize(-a, epsilon), -quantize(a, epsilon))
    record("quantizer_uniform_error", error_ok, "|N_epsilon(a)-a|<=epsilon/2")
    record("quantizer_oddness", odd_ok, "away-from-zero tie convention")

    tex = (ART / "source_dynamics_package_audit_v1.tex").read_text(encoding="utf-8")
    for marker in [
        "OBST-P5T07-QAMP-INTRINSIC-LAW-SCALE-ROBUSTNESS-001",
        "locally frozen",
        "not a global no-go theorem",
        "conservative source extensions remain possible",
        "gamma'=",
        "N_{d\\varepsilon}",
    ]:
        record(f"boundary_marker::{marker}", marker in tex, "required audit marker")

    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "p5_t07_audit_validation_receipt_v1",
        "task_id": "RT-20260725-014",
        "job_id": "AJ-RT-20260725-014-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "stress_family_members_checked": 4,
        "artifact_hashes": artifact_hashes,
        "source_hashes": SOURCES,
        "checks": checks,
        "authority_note": "Operational validation only; no theorem, ontology, promotion, publication, or completed-derivation authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = run_checks()
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not (args.write_report or args.check):
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
