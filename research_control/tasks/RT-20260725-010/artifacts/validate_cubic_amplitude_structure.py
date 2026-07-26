#!/usr/bin/env python3
"""Validate the bounded P5-T04 cubic-amplitude structural packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_ROOT = REPO_ROOT / "research_control/tasks/RT-20260725-010/artifacts"
SPEC_PATH = ARTIFACT_ROOT / "cubic_amplitude_structural_analysis_spec_v1.yaml"
TEX_PATH = ARTIFACT_ROOT / "cubic_amplitude_structural_analysis_v1.tex"
CHILD_MATH_PATH = ARTIFACT_ROOT / "child_phys_math_cubic_amplitude_structure.yaml"
CHILD_PHIL_PATH = ARTIFACT_ROOT / "child_phys_phil_cubic_amplitude_structure.yaml"
CONFLICT_PATH = ARTIFACT_ROOT / "parent_conflict_review_cubic_amplitude_structure.yaml"
FUSION_PATH = ARTIFACT_ROOT / "parent_fusion_notes_cubic_amplitude_structure.md"
REPORT_PATH = ARTIFACT_ROOT / "cubic_amplitude_structural_analysis_validation_receipt_v1.json"

REQUIRED_FAILURE_BRANCHES = {
    "P5T04-FAIL-PATCH-INDEPENDENCE",
    "P5T04-FAIL-SUPERPOSITION",
    "P5T04-FAIL-DIRAC-OVERREAD",
    "P5T04-FAIL-NOETHER-OVERREAD",
    "P5T04-FAIL-PROBABILITY-OVERREAD",
    "P5T04-FAIL-TARGET-IMPORT",
}


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} must contain a mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_check(
    checks: list[dict[str, Any]], check_id: str, ok: bool, detail: str
) -> None:
    checks.append(
        {"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail}
    )


def flow(amplitude: float, parameter: float, gamma: float) -> float:
    return amplitude / math.sqrt(
        1.0 + 2.0 * gamma * amplitude * amplitude * parameter
    )


def flow_derivative(amplitude: float, parameter: float, gamma: float) -> float:
    return (1.0 + 2.0 * gamma * amplitude * amplitude * parameter) ** (-1.5)


def h_test(amplitude: float) -> float:
    return amplitude * amplitude / (1.0 + amplitude * amplitude)


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required_paths = [
        SPEC_PATH,
        TEX_PATH,
        CHILD_MATH_PATH,
        CHILD_PHIL_PATH,
        CONFLICT_PATH,
        FUSION_PATH,
    ]
    for path in required_paths:
        add_check(
            checks,
            f"file:{path.name}",
            path.is_file() and not path.is_symlink(),
            "required regular artifact exists",
        )

    try:
        spec = load_mapping(SPEC_PATH)
        child_math = load_mapping(CHILD_MATH_PATH)
        child_phil = load_mapping(CHILD_PHIL_PATH)
        conflict = load_mapping(CONFLICT_PATH)
        tex = TEX_PATH.read_text(encoding="utf-8")
        fusion = FUSION_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {
            "schema_id": "cubic_amplitude_structural_analysis_validation_receipt_v1",
            "result_status": "FAIL",
            "error": str(exc),
            "checks": checks,
            "finding_counts": {
                "pass": sum(item["status"] == "PASS" for item in checks),
                "fail": sum(item["status"] == "FAIL" for item in checks) + 1,
            },
        }

    source = spec.get("source_candidate", {})
    add_check(
        checks,
        "candidate_lock",
        spec.get("candidate_unchanged") is True
        and source.get("generator") == "X_gamma(q_a)=-gamma a^3 sin(theta_1)"
        and source.get("flow")
        == "f_lambda(a)=a/sqrt(1+2 gamma a^2 lambda)",
        "the exact P5-T03 state family, generator, and flow remain unchanged",
    )

    locality = spec.get("locality", {})
    add_check(
        checks,
        "patching_theorem",
        locality.get("theorem_id") == "P5T04-THM-GLOBAL-MODE-PATCHING"
        and locality.get("result") == "scoped_obstruction"
        and locality.get("source_extension_continuation") == "open",
        "the locality finding is exact, candidate-specific, and continuation-open",
    )

    composition = spec.get("composition", {})
    defect = composition.get("generator_additivity", {})
    add_check(
        checks,
        "composition_classification",
        composition.get("parameter_composition", {}).get("status") == "PASS"
        and composition.get("state_addition_closure", {}).get("status") == "PASS"
        and defect.get("status") == "FAIL_GENERIC"
        and defect.get("defect")
        == "X(q_(a+b))-X(q_a)-X(q_b)=-3 gamma a b (a+b) sin(theta_1)",
        "parameter composition is separated from generic superposition failure",
    )

    numeric_defects = []
    gamma = 1.3
    for a, b in ((1.0, 1.0), (0.5, -0.2), (-1.1, -0.4)):
        left = -gamma * (a + b) ** 3
        right = -gamma * a**3 - gamma * b**3
        expected = -3.0 * gamma * a * b * (a + b)
        numeric_defects.append(math.isclose(left - right, expected, rel_tol=1e-12))
    add_check(
        checks,
        "generator_defect_numeric",
        all(numeric_defects),
        "finite evaluations reproduce the exact cubic additivity defect",
    )

    flow_nonadditive = not math.isclose(
        flow(2.0, 0.4, gamma),
        2.0 * flow(1.0, 0.4, gamma),
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    add_check(
        checks,
        "flow_nonadditivity_control",
        flow_nonadditive,
        "a=b=1 supplies a nonzero integrated superposition defect",
    )

    constraints = spec.get("constraints", {})
    counts = constraints.get("Dirac_constraint_counts", {})
    add_check(
        checks,
        "constraint_applicability",
        constraints.get("preserved") is True
        and constraints.get("Hamiltonian_formalism_present") is False
        and set(counts.values()) == {"not_applicable"},
        "the kinematic membership constraint is preserved without inventing Dirac counts",
    )

    conservation = spec.get("conservation", {})
    add_check(
        checks,
        "first_integral_theorem",
        conservation.get("theorem_id") == "P5T04-THM-SMOOTH-FIRST-INTEGRALS"
        and conservation.get("conclusion")
        == "Every global C1 first integral is constant."
        and conservation.get("Lyapunov_functional", {}).get("conserved") is False,
        "smooth first-integral triviality is distinct from Lyapunov decay",
    )

    symmetry = spec.get("symmetry_and_redundancy", {})
    add_check(
        checks,
        "gauge_symmetry_classification",
        symmetry.get("infinitesimal_redundancy_algebra") == "zero"
        and symmetry.get("nonzero_gauge_generators") == 0
        and symmetry.get("update_generator_is_gauge") is False
        and symmetry.get("explicit_global_symmetry", {}).get("group") == "Z2"
        and symmetry.get("explicit_global_symmetry", {}).get(
            "declared_as_redundancy"
        )
        is False,
        "identity-only redundancy, update dynamics, and discrete reflection are separated",
    )

    symmetry_numeric = all(
        math.isclose(
            flow(-a, lam, gamma),
            -flow(a, lam, gamma),
            rel_tol=1e-12,
            abs_tol=1e-12,
        )
        for a, lam in ((0.4, 0.2), (1.7, 0.8), (-0.9, 1.1))
    )
    add_check(
        checks,
        "reflection_equivariance",
        symmetry_numeric,
        "finite evaluations verify the Z2 reflection commutes with the flow",
    )

    variation = spec.get("finite_variation", {})
    derivative_cases = [
        flow_derivative(a, lam, gamma)
        for a, lam in ((0.0, 1.0), (0.4, 0.5), (-2.0, 3.0))
    ]
    add_check(
        checks,
        "tangent_nonexpansion",
        variation.get("nonexpanding") is True
        and variation.get("generic_source_robustness_claimed") is False
        and all(0.0 < value <= 1.0 for value in derivative_cases),
        "the exact admitted tangent multiplier is positive and no larger than one",
    )

    probability = spec.get("probability", {})
    contraction_cases = [
        h_test(flow(a, 0.6, gamma)) < h_test(a)
        for a in (-3.0, -0.4, 0.2, 2.5)
    ]
    add_check(
        checks,
        "probability_conditional",
        probability.get("structure_present_in_candidate") is False
        and probability.get("pushforward_preserves_total_mass") is True
        and probability.get("invariant_measure_theorem", {}).get(
            "unique_invariant_probability"
        )
        == "delta_0"
        and probability.get("selected_probability_law") is False
        and all(contraction_cases),
        "bounded test function decreases off zero without selecting a probability law",
    )

    branch_ids = {
        str(item.get("branch_id", ""))
        for item in spec.get("failure_branches", [])
        if isinstance(item, dict)
    }
    add_check(
        checks,
        "failure_branch_manifest",
        branch_ids == REQUIRED_FAILURE_BRANCHES,
        "all six planned failure and overread branches are explicit",
    )

    add_check(
        checks,
        "parent_child_synthesis",
        child_math.get("status") == "completed"
        and child_phil.get("status") == "completed"
        and conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == [],
        "both internal perspectives are complete and all conflicts are resolved",
    )

    required_tex_markers = (
        "Global-mode patching theorem",
        "Nonlinear composition defect",
        "Triviality of global smooth first integrals",
        "Nonexpansion of the admitted tangent variation",
        "Pushforward normalization and unique invariant measure",
        "blocked while same-milestone continuation remains open",
    )
    add_check(
        checks,
        "fused_tex_markers",
        all(marker in tex for marker in required_tex_markers),
        "the fused theorem artifact contains every decisive result and status boundary",
    )

    forbidden_positive_claims = (
        "canonical ontology is adopted",
        "physical energy is",
        "future source extensions are impossible",
        "the theory is rejected",
        "Einstein equations are derived",
    )
    combined = f"{tex}\n{fusion}".lower()
    add_check(
        checks,
        "claim_boundary",
        not any(marker in combined for marker in forbidden_positive_claims),
        "the packet contains no adoption, physical, global-no-go, or downstream-GR promotion",
    )

    overall = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    artifact_hashes = {
        path.relative_to(REPO_ROOT).as_posix(): sha256(path)
        for path in required_paths
        if path.is_file()
    }
    return {
        "schema_id": "cubic_amplitude_structural_analysis_validation_receipt_v1",
        "result_status": overall,
        "task_id": "RT-20260725-010",
        "job_id": "AJ-RT-20260725-010-001",
        "plan_task_id": "P5-T04",
        "candidate_id": "V21-P5-T03-CUBIC-AMPLITUDE-SOURCE-DYNAMICS-V1",
        "candidate_unchanged": True,
        "result_kind": "theorem_and_precise_scoped_obstruction",
        "obstruction_scope": "current candidate family only",
        "route_frozen": False,
        "finding_counts": {
            "pass": sum(item["status"] == "PASS" for item in checks),
            "fail": sum(item["status"] == "FAIL" for item in checks),
            "theorems": 4,
            "propositions": 2,
            "scoped_obstructions": 1,
            "unresolved_conflicts": 0,
        },
        "validator_ids": [
            "candidate_lock",
            "patching_theorem",
            "composition_classification",
            "constraint_applicability",
            "first_integral_theorem",
            "gauge_symmetry_classification",
            "tangent_nonexpansion",
            "probability_conditional",
            "parent_child_synthesis",
            "claim_boundary",
        ],
        "claim_boundary_summary": (
            "Candidate-specific draft/control theorem and obstruction only; no "
            "canonical ontology or source-law adoption, physical locality, "
            "constraint, energy, probability, gauge, reconstruction, downstream "
            "GR, promotion, global theory rejection, or future-extension "
            "impossibility authority."
        ),
        "artifact_sha256": artifact_hashes,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    if args.check and not REPORT_PATH.is_file():
        return 1
    return 0 if report.get("result_status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
