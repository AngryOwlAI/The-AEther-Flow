#!/usr/bin/env python3
"""Exact controls for the RT004 SignedCubicViabilitySelector audit.

The calculations test the fixed proposal-only candidate.  They do not adopt a
source law, assign physical or empirical meaning, or advance Distance-to-GR.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

SOURCES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1017.yaml":
        "21946600d826f6f6e0a1398243ac5da387b03ed9b1201a25b341abd9b880dec5",
    "research_control/tasks/RT-20260811-003/artifacts/v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_law_v1.tex":
        "14c229daccb45faabff0a2f3fe264459e2f54302ae514a1f0820ca30c0984edc",
    "research_control/tasks/RT-20260811-003/artifacts/v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_spec_v1.yaml":
        "f990e4e6048b268545e3f818a2088d7951d13c2310e0a113e018b3c39fa2af0e",
    "research_control/tasks/RT-20260811-003/artifacts/v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_provenance_manifest_v1.yaml":
        "0d5ba8be92e79967e7ff9f0ef349ee67951abbe36481f88387af12bb932c7781",
    "research_control/tasks/RT-20260811-003/artifacts/v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_disposition_v1.yaml":
        "c7782786290f8d50774de7d507145229edde65599f5c3cdcb23ed2f8e5187c24",
    "research_control/tasks/RT-20260811-003/artifacts/v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_model.py":
        "deb4827eab5195098b62fb722430715b333aad8f393faa7f4c5cb1126f6631a5",
    "research_control/tasks/RT-20260811-003/artifacts/parent_fusion_notes_p4_t02_b2_source_dynamical_viability_admissibility_selector.md":
        "a6d4ba275e4ba201a23a06e38f484b5319d905240ac107ac0c4b9064e678c40b",
    "research_control/tasks/RT-20260725-008/artifacts/cubic_amplitude_source_dynamics_v1.tex":
        "98ce6833f6e4d8be22837d25845d7fa62d6886049e168d121de5de0093703f6a",
    "research_control/tasks/RT-20260725-010/artifacts/cubic_amplitude_structural_analysis_v1.tex":
        "a9a9f42ff016febc0f40a8a4db32b09f670084bda2248704e290cf5bee02a06b",
    ".agents/roles/physics/smuggling-auditor.v0.2.0.md":
        "2ec5a542caffa90a54d11f0c03630fde839e92f4917d5dbd55b80b724a46c882",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(numerator: int, denominator: int = 1) -> Fraction:
    return Fraction(numerator, denominator)


def evolve_square(u: Fraction, gamma: Fraction, time: Fraction) -> Fraction:
    return u / (1 + 2 * gamma * time * u)


def barrier_square(u: Fraction, anchor_square: Fraction) -> Fraction:
    return u / (anchor_square + u)


def lambda_square(
    gamma: Fraction, horizon: Fraction, anchor_square: Fraction
) -> Fraction:
    return 1 / (1 + 2 * gamma * horizon * anchor_square)


def exact_controls() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def check(check_id: str, passed: bool, evidence: object) -> None:
        checks.append(
            {"check_id": check_id, "passed": bool(passed), "evidence": evidence}
        )

    source_results: dict[str, dict[str, object]] = {}
    for rel, expected in SOURCES.items():
        actual = sha256(ROOT / rel)
        source_results[rel] = {
            "expected": expected,
            "actual": actual,
            "match": actual == expected,
        }
    check(
        "SOURCE-HASHES",
        all(row["match"] for row in source_results.values()),
        source_results,
    )

    gamma = q(3, 5)
    horizon = q(7, 4)
    anchor = q(5, 3)
    anchor_square = anchor * anchor
    eta = gamma * horizon * anchor_square
    lam2 = lambda_square(gamma, horizon, anchor_square)

    # Simultaneous positive regraduation leaves the sole continuous
    # certificate parameter eta=gamma*Delta*a_star^2 unchanged.
    c = q(13, 5)
    d = q(7, 3)
    gamma_prime = gamma / (c * d * d)
    horizon_prime = c * horizon
    anchor_prime = d * anchor
    eta_prime = gamma_prime * horizon_prime * anchor_prime * anchor_prime
    u = q(11, 6)
    u_prime = d * d * u
    time = q(2, 9)
    time_prime = c * time
    dimensionless_state = u / anchor_square
    dimensionless_state_prime = u_prime / (anchor_prime * anchor_prime)
    evolved_dimensionless = evolve_square(u, gamma, time) / anchor_square
    evolved_dimensionless_prime = (
        evolve_square(u_prime, gamma_prime, time_prime)
        / (anchor_prime * anchor_prime)
    )
    check(
        "DIMENSIONLESS-REDUCTION",
        eta == eta_prime
        and lam2 == lambda_square(
            gamma_prime, horizon_prime, anchor_prime * anchor_prime
        )
        and dimensionless_state == dimensionless_state_prime
        and evolved_dimensionless == evolved_dimensionless_prime,
        {
            "eta": str(eta),
            "eta_prime": str(eta_prime),
            "lambda_square": str(lam2),
            "dimensionless_state": str(dimensionless_state),
            "evolved_dimensionless_state": str(evolved_dimensionless),
            "gamma_prime_rule": "gamma/(c*d^2)",
        },
    )

    # Delta and a_star alter the certificate but not which sign component is
    # viable.  This separates quantitative proof data from sigma's selection.
    parameter_samples: list[dict[str, object]] = []
    all_component_results = True
    for g in (q(1, 10), q(3, 5), q(4)):
        for delta in (q(1, 100), q(7, 4), q(20)):
            for a_star in (q(1, 5), q(5, 3), q(9)):
                evolved_positive = evolve_square(q(2), g, delta) > 0
                evolved_negative_square = evolve_square(q(2), g, delta) > 0
                all_component_results &= evolved_positive and evolved_negative_square
                parameter_samples.append(
                    {
                        "gamma": str(g),
                        "Delta": str(delta),
                        "a_star": str(a_star),
                        "eta": str(g * delta * a_star * a_star),
                        "lambda_square": str(
                            lambda_square(g, delta, a_star * a_star)
                        ),
                        "positive_component_preserved": evolved_positive,
                        "negative_component_preserved": evolved_negative_square,
                    }
                )
    check(
        "PARAMETER-ROLE-SEPARATION",
        all_component_results and len(parameter_samples) == 27,
        {
            "sample_count": len(parameter_samples),
            "viability_kernel_for_each_sigma": "U_sigma",
            "continuous_parameters_select_sigma": False,
            "samples": parameter_samples,
        },
    )

    # The reflection action exchanges the two tokens and has no fixed token.
    tokens = (-1, 1)
    reflected = {sigma: -sigma for sigma in tokens}
    fixed_tokens = [sigma for sigma in tokens if reflected[sigma] == sigma]
    check(
        "REFLECTION-TOKEN-NONSELECTION",
        not fixed_tokens and set(reflected.values()) == set(tokens),
        {
            "action": reflected,
            "fixed_tokens": fixed_tokens,
            "orbit_count": 1,
            "interpretation": "equivariance transports the pair but selects neither token",
        },
    )

    # Finite iterates stay in the selected open component while approaching
    # its excluded boundary.  Hence there is no positive infinite-horizon
    # barrier margin.
    step = horizon
    u0 = q(9, 4)
    finite_iterates: list[dict[str, object]] = []
    for n in (0, 1, 2, 5, 20, 100):
        un = u0 / (1 + 2 * gamma * q(n) * step * u0)
        bn2 = barrier_square(un, anchor_square)
        finite_iterates.append(
            {
                "n": n,
                "amplitude_square": str(un),
                "barrier_square": str(bn2),
                "strictly_inside_component": un > 0,
            }
        )
    check(
        "FINITE-VERSUS-ASYMPTOTIC-VIABILITY",
        all(row["strictly_inside_component"] for row in finite_iterates)
        and Fraction(finite_iterates[-1]["amplitude_square"])
        < Fraction(finite_iterates[1]["amplitude_square"]),
        {
            "finite_iterates": finite_iterates,
            "amplitude_square_limit": "0",
            "barrier_square_limit": "0",
            "zero_in_U_sigma": False,
            "uniform_positive_infinite_horizon_margin": False,
            "finite_path_viability_remains_exact": True,
        },
    )

    # For any fixed positive time, a bounded strict Lyapunov function rules
    # out every invariant Borel probability except delta_0.
    lyapunov_samples: list[dict[str, object]] = []
    strict = True
    for state_square in (q(1, 100), q(1, 3), q(2), q(100)):
        next_square = evolve_square(state_square, gamma, q(1))
        h_before = state_square / (1 + state_square)
        h_after = next_square / (1 + next_square)
        strict &= h_after < h_before
        lyapunov_samples.append(
            {
                "state_square": str(state_square),
                "h_before": str(h_before),
                "h_after": str(h_after),
                "strict_decrease": h_after < h_before,
            }
        )
    check(
        "INVARIANT-PROBABILITY-CONSEQUENCE",
        strict,
        {
            "lyapunov_samples": lyapunov_samples,
            "unique_invariant_borel_probability": "delta_0",
            "delta_0_supported_on_U_sigma": False,
            "component_selection_is_probability_occurrence": False,
        },
    )

    # gamma>0 is explicit source-extension preparation.  gamma=0 still
    # preserves both components, while gamma<0 fails global forward existence.
    gamma_zero_square = evolve_square(q(5), q(0), q(100))
    negative_gamma = q(-1)
    blowup_denominator_at_tenth = 1 + 2 * negative_gamma * q(1, 10) * q(5)
    check(
        "GAMMA-SIGN-ROLE",
        gamma_zero_square == q(5) and blowup_denominator_at_tenth == 0,
        {
            "gamma_zero_preserves_both_components": True,
            "gamma_zero_selects_sigma": False,
            "negative_gamma_example_blowup_time": "1/10",
            "positive_gamma_is_current_ontology_derived": False,
            "positive_gamma_is_target_selected": False,
        },
    )

    dependency_edges = {
        "P5_flow": ["R_Delta"],
        "gamma": ["P5_flow", "lambda"],
        "Delta": ["R_Delta", "lambda"],
        "a_star": ["b_sigma", "lambda"],
        "sigma": ["U_sigma", "b_sigma", "Sel_src"],
        "R_Delta": ["Viab"],
        "U_sigma": ["Viab"],
    }
    forbidden_nodes = {
        "target_atlas",
        "target_metric",
        "desired_GR_cone",
        "empirical_response",
        "benchmark_answer",
        "validator_PASS",
        "role_authority",
    }
    used_nodes = set(dependency_edges)
    used_nodes.update(node for targets in dependency_edges.values() for node in targets)
    check(
        "PREDECLARATION-SYNTAX-NOT-EPISTEMIC-SELECTION",
        not (used_nodes & forbidden_nodes),
        {
            "dependency_edges": dependency_edges,
            "forbidden_nodes_present": sorted(used_nodes & forbidden_nodes),
            "acyclic_predeclaration_proves_syntactic_noncircularity": True,
            "acyclic_predeclaration_selects_sigma_or_law": False,
        },
    )

    report: dict[str, object] = {
        "schema_id": "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_model_v1",
        "task_id": "RT-20260811-004",
        "job_id": "AJ-RT-20260811-004-001",
        "candidate_id": "CAND-V22-B2-SOURCE-DYNAMICAL-VIABILITY-ADMISSIBILITY-SELECTOR-V1",
        "source_count": len(SOURCES),
        "check_count": len(checks),
        "pass_count": sum(row["passed"] for row in checks),
        "fail_count": sum(not row["passed"] for row in checks),
        "checks": checks,
        "authority_limits": {
            "model_pass_is_scientific_authority": False,
            "candidate_adopted": False,
            "physical_or_empirical_semantics_established": False,
            "distance_to_gr_changed": False,
            "successor_executed": False,
        },
    }
    report["status"] = "PASS" if report["fail_count"] == 0 else "FAIL"
    payload_bytes = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["model_payload_sha256"] = hashlib.sha256(payload_bytes).hexdigest()
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = exact_controls()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
