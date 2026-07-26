#!/usr/bin/env python3
"""Validate the bounded P5-T05 cubic-amplitude background packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_ROOT = REPO_ROOT / "research_control/tasks/RT-20260725-012/artifacts"
CATALOG_PATH = ARTIFACT_ROOT / "cubic_amplitude_background_phase_catalog_v1.yaml"
MODES_PATH = ARTIFACT_ROOT / "cubic_amplitude_linearized_modes_v1.yaml"
TEX_PATH = ARTIFACT_ROOT / "cubic_amplitude_background_phase_analysis_v1.tex"
CHILD_MATH_PATH = ARTIFACT_ROOT / "child_phys_math_cubic_amplitude_backgrounds.yaml"
CHILD_PHIL_PATH = ARTIFACT_ROOT / "child_phys_phil_cubic_amplitude_backgrounds.yaml"
CONFLICT_PATH = ARTIFACT_ROOT / "parent_conflict_review_cubic_amplitude_backgrounds.yaml"
FUSION_PATH = ARTIFACT_ROOT / "parent_fusion_notes_cubic_amplitude_backgrounds.md"
REPORT_PATH = ARTIFACT_ROOT / "cubic_amplitude_background_phase_validation_receipt_v1.json"
OBSTRUCTION_ID = "OBST-P5T05-QAMP-NO-RECONSTRUCTION-PHASE-001"


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


def tangent_multiplier(amplitude: float, parameter: float, gamma: float) -> float:
    return (1.0 + 2.0 * gamma * amplitude * amplitude * parameter) ** (-1.5)


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required_paths = [
        CATALOG_PATH,
        MODES_PATH,
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
        catalog = load_mapping(CATALOG_PATH)
        modes = load_mapping(MODES_PATH)
        child_math = load_mapping(CHILD_MATH_PATH)
        child_phil = load_mapping(CHILD_PHIL_PATH)
        conflict = load_mapping(CONFLICT_PATH)
        tex = TEX_PATH.read_text(encoding="utf-8")
        fusion = FUSION_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {
            "schema_id": "cubic_amplitude_background_phase_validation_receipt_v1",
            "result_status": "FAIL",
            "error": str(exc),
            "checks": checks,
            "finding_counts": {
                "pass": sum(item["status"] == "PASS" for item in checks),
                "fail": sum(item["status"] == "FAIL" for item in checks) + 1,
            },
        }

    source = catalog.get("source_candidate", {})
    add_check(
        checks,
        "candidate_lock",
        catalog.get("candidate_unchanged") is True
        and source.get("generator") == "X_gamma(q_a)=-gamma a^3 sin(theta_1)"
        and source.get("flow") == "f_lambda(a)=a/sqrt(1+2 gamma a^2 lambda)",
        "the exact P5-T03 candidate remains unchanged",
    )

    stationary = catalog.get("stationary_backgrounds", {})
    entries = stationary.get("entries", [])
    add_check(
        checks,
        "stationary_background_catalog",
        stationary.get("count") == 1
        and len(entries) == 1
        and entries[0].get("state") == "q_0"
        and entries[0].get("fixed") is True,
        "solving the fixed-point equation yields only q_0",
    )

    strata = catalog.get("invariant_strata", [])
    add_check(
        checks,
        "invariant_strata",
        len(strata) == 3
        and all(item.get("forward_invariant") is True for item in strata)
        and {item.get("amplitude_domain") for item in strata} == {"a>0", "a=0", "a<0"},
        "positive, zero, and negative amplitude strata are complete and invariant",
    )

    gamma = 1.7
    finite_cases = [
        (a, lam, flow(a, lam, gamma))
        for a, lam in ((-2.0, 0.3), (-0.4, 4.0), (0.0, 2.0), (0.7, 1.2))
    ]
    add_check(
        checks,
        "flow_sign_and_attraction",
        all(
            (value == 0.0 if a == 0.0 else math.copysign(1.0, value) == math.copysign(1.0, a))
            and abs(value) <= abs(a)
            for a, _, value in finite_cases
        )
        and all(abs(flow(a, 1e9, gamma)) < 1e-4 for a in (-3.0, -0.2, 0.5, 4.0)),
        "finite controls preserve sign, contract amplitude, and approach zero",
    )

    linearization = modes.get("linearization", {})
    add_check(
        checks,
        "linearized_equation",
        linearization.get("equation")
        == "d eta/dlambda=-3 gamma a_b(lambda)^2 eta"
        and linearization.get("solution")
        == "eta(lambda)=eta0/(1+2 gamma a_b0^2 lambda)^(3/2)",
        "the time-dependent tangent equation and exact solution are recorded",
    )

    derivative_cases = []
    for amplitude, parameter in ((0.0, 1.0), (0.4, 0.7), (-1.3, 2.1)):
        step = 1e-6
        numeric = (
            flow(amplitude + step, parameter, gamma)
            - flow(amplitude - step, parameter, gamma)
        ) / (2.0 * step)
        exact = tangent_multiplier(amplitude, parameter, gamma)
        derivative_cases.append(math.isclose(numeric, exact, rel_tol=2e-8, abs_tol=2e-8))
    add_check(
        checks,
        "linearization_numeric",
        all(derivative_cases),
        "centered finite differences reproduce the exact tangent multiplier",
    )

    counts = modes.get("mode_counts", {})
    add_check(
        checks,
        "mode_count_boundary",
        counts.get("admitted_source_tangent_dimension") == 1
        and counts.get("physical_modes", {}).get("count") == "not_classified"
        and counts.get("gauge_modes", {}).get("count") == 0
        and counts.get("Hamiltonian_constrained_modes", {}).get("count")
        == "not_applicable"
        and counts.get("off_family_modes", {}).get("count") == "not_defined",
        "source, physical, gauge, constrained, and off-family counts remain distinct",
    )

    around_nonzero = counts.get("around_nonzero_trajectory", {})
    around_zero = counts.get("around_zero_stationary_background", {})
    add_check(
        checks,
        "growth_decay_zero_modes",
        around_nonzero == {"growing": 0, "decaying": 1, "zero": 0, "oscillatory": 0}
        and around_zero == {"growing": 0, "decaying": 0, "zero": 1, "oscillatory": 0},
        "the one admitted mode is decaying off zero and neutral at zero",
    )

    zero_stability = modes.get("stability", {}).get("zero_background", {})
    add_check(
        checks,
        "nonlinear_stability",
        zero_stability.get("linear") == "neutral"
        and zero_stability.get("nonlinear") == "globally_asymptotically_stable"
        and zero_stability.get("Lyapunov_stable") is True
        and zero_stability.get("globally_attractive") is True
        and zero_stability.get("exponentially_stable") is False,
        "neutral linearization is separated from nonlinear polynomial attraction",
    )

    scaled_limits = [
        math.sqrt(lam) * abs(flow(a, lam, gamma))
        for a in (0.2, 1.0, -3.0)
        for lam in (1e8,)
    ]
    target = 1.0 / math.sqrt(2.0 * gamma)
    add_check(
        checks,
        "polynomial_decay",
        all(math.isclose(value, target, rel_tol=1e-7) for value in scaled_limits),
        "sqrt(lambda)|a(lambda)| approaches the nonzero polynomial-decay limit",
    )

    symmetry = catalog.get("symmetry_and_order", {})
    add_check(
        checks,
        "symmetry_and_orientation",
        symmetry.get("unique_stationary_background_preserves_symmetry") is True
        and symmetry.get("sign_sectors_dynamically_selected") is False
        and symmetry.get("spontaneous_symmetry_breaking_present") is False
        and symmetry.get("physical_time_orientation_present") is False
        and symmetry.get("source_order_orientation_only") is True,
        "reflection, ordering, and physical-time boundaries are explicit",
    )

    regions = {item.get("region_id"): item for item in modes.get("parameter_regions", [])}
    add_check(
        checks,
        "parameter_regions",
        set(regions) == {
            "P5T05-GAMMA-POSITIVE",
            "P5T05-GAMMA-ZERO",
            "P5T05-GAMMA-NEGATIVE",
        }
        and regions["P5T05-GAMMA-POSITIVE"].get("forward_total") is True
        and regions["P5T05-GAMMA-ZERO"].get("candidate_admitted") is False
        and regions["P5T05-GAMMA-NEGATIVE"].get("forward_total") is False,
        "positive, zero, and negative coefficient controls have exact dispositions",
    )

    reconstruction = catalog.get("reconstruction_phase_result", {})
    add_check(
        checks,
        "precise_obstruction",
        reconstruction.get("result_kind") == "precise_scoped_obstruction"
        and reconstruction.get("obstruction_id") == OBSTRUCTION_ID
        and reconstruction.get("viable_reconstruction_phase_count") == 0
        and reconstruction.get("future_source_extension_continuation") == "open"
        and reconstruction.get("global_no_go_claimed") is False,
        "the reconstruction-phase failure is decisive and candidate-specific",
    )

    add_check(
        checks,
        "parent_child_synthesis",
        child_math.get("status") == "completed"
        and child_phil.get("status") == "completed"
        and child_math.get("candidate_constructor_result", {}).get("result_type")
        == "precise_obstruction"
        and child_phil.get("candidate_constructor_result", {}).get("result_type")
        == "precise_obstruction"
        and conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == [],
        "both internal perspectives return the same decisive result with no unresolved conflict",
    )

    required_tex_markers = (
        "Unique stationary background and invariant sectors",
        "Mode and stability classification",
        "What is and is not counted",
        "No nontrivial reconstruction-suitable phase",
        OBSTRUCTION_ID,
        "candidate-specific obstruction",
    )
    add_check(
        checks,
        "fused_tex_markers",
        all(marker in tex for marker in required_tex_markers),
        "the fused TeX source contains every decisive theorem and boundary",
    )

    forbidden_positive_claims = (
        "canonical ontology is adopted",
        "physical vacuum is established",
        "physical time is derived",
        "all source extensions are impossible",
        "the theory is rejected",
        "einstein equations are derived",
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
        "schema_id": "cubic_amplitude_background_phase_validation_receipt_v1",
        "result_status": overall,
        "task_id": "RT-20260725-012",
        "job_id": "AJ-RT-20260725-012-001",
        "plan_task_id": "P5-T05",
        "candidate_id": "V21-P5-T03-CUBIC-AMPLITUDE-SOURCE-DYNAMICS-V1",
        "candidate_unchanged": True,
        "result_kind": "precise_scoped_obstruction",
        "obstruction_id": OBSTRUCTION_ID,
        "obstruction_scope": "current candidate family only",
        "route_frozen": False,
        "finding_counts": {
            "pass": sum(item["status"] == "PASS" for item in checks),
            "fail": sum(item["status"] == "FAIL" for item in checks),
            "theorems": 3,
            "stationary_backgrounds": 1,
            "trajectory_background_families": 1,
            "admitted_source_tangent_modes": 1,
            "scoped_obstructions": 1,
            "unresolved_conflicts": 0,
        },
        "validator_ids": [
            "candidate_lock",
            "stationary_background_catalog",
            "invariant_strata",
            "linearized_equation",
            "linearization_numeric",
            "mode_count_boundary",
            "growth_decay_zero_modes",
            "nonlinear_stability",
            "polynomial_decay",
            "symmetry_and_orientation",
            "parameter_regions",
            "precise_obstruction",
            "parent_child_synthesis",
            "claim_boundary",
        ],
        "claim_boundary_summary": (
            "Candidate-specific draft/control background, mode, stability, and "
            "precise reconstruction-phase obstruction only; no canonical ontology "
            "or source-law adoption, physical background, phase, mode, time, "
            "reconstruction, downstream GR, promotion, global theory rejection, "
            "or future-extension impossibility authority."
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
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        if not REPORT_PATH.is_file():
            report["result_status"] = "FAIL"
            report["error"] = "validation receipt is absent"
        else:
            stored = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
            if stored != report:
                report["result_status"] = "FAIL"
                report["error"] = "validation receipt is stale"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("result_status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
