#!/usr/bin/env python3
"""Validate the bounded P5-T03 cubic-amplitude dynamics packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_ROOT = REPO_ROOT / "research_control/tasks/RT-20260725-008/artifacts"
SPEC_PATH = ARTIFACT_ROOT / "cubic_amplitude_source_dynamics_spec_v1.yaml"
TEX_PATH = ARTIFACT_ROOT / "cubic_amplitude_source_dynamics_v1.tex"
CHILD_MATH_PATH = ARTIFACT_ROOT / "child_phys_math_cubic_amplitude_dynamics.yaml"
CHILD_PHIL_PATH = ARTIFACT_ROOT / "child_phys_phil_cubic_amplitude_dynamics.yaml"
CONFLICT_PATH = ARTIFACT_ROOT / "parent_conflict_review_cubic_amplitude_dynamics.yaml"
FUSION_PATH = ARTIFACT_ROOT / "parent_fusion_notes_cubic_amplitude_dynamics.md"
REPORT_PATH = ARTIFACT_ROOT / "cubic_amplitude_source_dynamics_validation_receipt_v1.json"

REQUIRED_PROPERTIES = {
    "P5T03-PROP-GLOBAL-FORWARD",
    "P5T03-PROP-PHI-COMPATIBILITY",
    "P5T03-PROP-RANGE",
    "P5T03-PROP-NO-GLOBAL-R-ACTION",
    "P5T03-PROP-LYAPUNOV",
}
REQUIRED_CONTROLS = {
    "P5T03-CONTROL-ZERO-RATE",
    "P5T03-CONTROL-NEGATIVE-RATE",
    "P5T03-CONTROL-LAMBDA-SQUARED",
    "P5T03-CONTROL-OFF-TANGENT",
    "P5T03-CONTROL-TARGET-IMPORT",
    "P5T03-CONTROL-PHYSICAL-OVERREAD",
}


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} must contain a mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_check(checks: list[dict[str, Any]], check_id: str, ok: bool, detail: str) -> None:
    checks.append(
        {"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail}
    )


def flow(amplitude: float, parameter: float, gamma: float) -> float:
    return amplitude / math.sqrt(1.0 + 2.0 * gamma * amplitude * amplitude * parameter)


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
            "schema_id": "cubic_amplitude_source_dynamics_validation_receipt_v1",
            "result_status": "FAIL",
            "error": str(exc),
            "checks": checks,
            "finding_counts": {
                "pass": sum(c["status"] == "PASS" for c in checks),
                "fail": sum(c["status"] == "FAIL" for c in checks) + 1,
            },
        }

    candidate = spec.get("selected_candidate", {})
    generator = candidate.get("generator", {}) if isinstance(candidate, dict) else {}
    equation = candidate.get("equation", {}) if isinstance(candidate, dict) else {}
    solution = candidate.get("solution", {}) if isinstance(candidate, dict) else {}
    action = candidate.get("induced_action", {}) if isinstance(candidate, dict) else {}
    add_check(
        checks,
        "candidate_typing",
        candidate.get("formalism") == "autonomous_first_order_amplitude_update_rule"
        and generator.get("signature") == "X_gamma:Q_amp->TQ_amp"
        and generator.get("admissible_variation_compatible") is True
        and equation.get("amplitude_form") == "da/dlambda=-gamma a^3",
        "generator and equation are typed on the exact P5-T01 amplitude witness",
    )
    add_check(
        checks,
        "explicit_solution",
        solution.get("formula")
        == "a(lambda)=a0/sqrt(1+2 gamma a0^2 lambda)"
        and solution.get("global_forward") is True
        and solution.get("unique") is True
        and solution.get("nontrivial_for_nonzero_a0") is True,
        "the declared equation has a unique global nontrivial forward solution",
    )
    add_check(
        checks,
        "p5_t02_compatibility",
        all(
            action.get(field) is True
            for field in (
                "identity",
                "composition",
                "joint_smoothness",
                "admissibility",
                "redundancy_compatibility",
                "generator_recovered",
            )
        ),
        "the induced maps satisfy the P5-T02 forward-action requirements",
    )

    property_ids = {
        str(item.get("property_id", ""))
        for item in spec.get("proved_properties", [])
        if isinstance(item, dict)
    }
    add_check(
        checks,
        "property_manifest",
        property_ids == REQUIRED_PROPERTIES,
        "globality, action compatibility, range, backward extension, and Lyapunov results are explicit",
    )

    numeric_cases = [
        (0.25, 0.4, 0.7, 1.3),
        (-1.2, 0.2, 0.9, 0.8),
        (2.0, 1.1, 0.3, 2.2),
    ]
    semigroup_ok = all(
        math.isclose(
            flow(flow(a, mu, gamma), lam, gamma),
            flow(a, lam + mu, gamma),
            rel_tol=1e-12,
            abs_tol=1e-12,
        )
        for a, lam, mu, gamma in numeric_cases
    )
    add_check(
        checks,
        "finite_semigroup_checks",
        semigroup_ok,
        "finite symbolic-surrogate evaluations reproduce forward composition",
    )

    gamma = 1.0
    a0 = 1.0
    parameter = 1.0
    positive = flow(a0, parameter, gamma)
    expected = 1.0 / math.sqrt(3.0)
    lyapunov_before = 0.5 * a0 * a0
    lyapunov_after = 0.5 * positive * positive
    add_check(
        checks,
        "positive_control",
        math.isclose(positive, expected, rel_tol=1e-12)
        and positive != a0
        and lyapunov_after < lyapunov_before,
        "gamma=1, a0=1, lambda=1 yields 1/sqrt(3) and decreases the control functional",
    )

    sample_parameter = 0.6
    sample_gamma = 1.4
    range_bound = 1.0 / math.sqrt(2.0 * sample_gamma * sample_parameter)
    sampled = [flow(value, sample_parameter, sample_gamma) for value in (-1e6, -2, 0, 2, 1e6)]
    add_check(
        checks,
        "range_and_forward_only",
        all(abs(value) < range_bound for value in sampled)
        and sampled == sorted(sampled),
        "positive-parameter maps are injective and remain inside their proper bounded range",
    )

    control_ids = {
        str(item.get("control_id", ""))
        for item in spec.get("controls", [])
        if isinstance(item, dict) and str(item.get("result", "")).startswith("fail_closed")
    }
    add_check(
        checks,
        "control_matrix",
        control_ids == REQUIRED_CONTROLS,
        "trivial, unstable, composition, off-tangent, target-import, and overread controls fail closed",
    )

    scale = spec.get("scale_and_provenance", {})
    add_check(
        checks,
        "scale_provenance",
        scale.get("formal_unit_relation") == "[gamma]=[lambda]^-1[a]^-2"
        and scale.get("physical_dimensionful_scale_introduced") is False
        and "gamma a0^2 lambda" in str(scale.get("invariant_orbit_combination", "")),
        "all formal scales and their nonphysical provenance are explicit",
    )

    boundary = spec.get("claim_boundary", {})
    false_fields = (
        "target_import_allowed",
        "canonical_ontology_modified",
        "canonical_ontology_candidate",
        "source_law_adopted",
        "source_law_rejected",
        "source_dynamics_adopted",
        "physical_dynamics_selected",
        "physical_time_claimed",
        "physical_clock_scale_fixed",
        "physical_energy_claimed",
        "Hamiltonian_claimed",
        "source_manifold_locality_claimed",
        "reconstruction_selected",
        "metric_constructed",
        "matter_coupling_constructed",
        "Einstein_equations_derived",
        "benchmark_promoted",
        "physics_promotion_authorized",
        "proof_authority",
    )
    add_check(
        checks,
        "claim_boundary",
        boundary.get("source_only") is True
        and boundary.get("source_dynamics_candidate_constructed") is True
        and all(boundary.get(field) is False for field in false_fields),
        "candidate construction is separated from adoption, physical interpretation, and downstream GR claims",
    )

    no_fog = spec.get("candidate_constructor_result", {})
    add_check(
        checks,
        "no_fog_result",
        no_fog.get("result_type") == "constructed_candidate"
        and no_fog.get("no_fog_check") is True
        and no_fog.get("claim_boundary_preserved") is True
        and no_fog.get("next_required_role") == "ontology-formalizer@0.2.0",
        "Candidate Constructor ends with one decisive constructed-candidate result",
    )

    required_tex_markers = [
        r"X_\gamma(q_a)=-\gamma a^3e",
        r"\frac{a_0}{\sqrt{1+2\gamma a_0^2\lambda}}",
        r"\Phi^\gamma_{\lambda+\mu}",
        r"\operatorname{ran}f^\gamma_\lambda",
        r"\frac{dL}{d\lambda}",
        "Current adoption is blocked while",
        "P5-T04",
    ]
    add_check(
        checks,
        "source_tex_content",
        all(marker in tex for marker in required_tex_markers),
        "registered TeX contains the generator, solution, laws, range, Lyapunov result, status, and successor boundary",
    )

    add_check(
        checks,
        "parent_child_synthesis",
        child_math.get("status") == "completed"
        and child_phil.get("status") == "completed"
        and conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == []
        and "injective" in fusion.lower()
        and "physical energy" in fusion.lower(),
        "both internal perspectives completed and the parent resolved mathematical and interpretive tensions",
    )

    source_hashes = {
        path.relative_to(REPO_ROOT).as_posix(): sha256(path) for path in required_paths
    }
    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "cubic_amplitude_source_dynamics_validation_receipt_v1",
        "validator_ids": [
            "p5_t03_cubic_amplitude_dynamics_validator_v1",
            "p5_t03_forward_semigroup_symbolic_check_v1",
            "p5_t03_range_and_backward_extension_review_v1",
            "p5_t03_lyapunov_and_scale_review_v1",
            "p5_t03_parent_child_synthesis_review_v1",
            "p5_t03_no_physical_overread_audit_v1",
        ],
        "result_status": "PASS" if not failed else "FAIL",
        "plan_task_id": "P5-T03",
        "object_id": spec.get("object_id", ""),
        "claim_status": "draft/control proposal-only source-extension data",
        "claim_boundary_summary": (
            "One task-local cubic-amplitude source-order dynamics candidate is "
            "constructed. No canonical adoption, physical time, energy, locality, "
            "reconstruction, metric, matter, Einstein-equation, benchmark, proof, "
            "publication, push, or completed-derivation authority follows."
        ),
        "checks": checks,
        "finding_counts": {
            "pass": sum(item["status"] == "PASS" for item in checks),
            "fail": len(failed),
            "warning": 0,
        },
        "source_hashes": source_hashes,
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
    if args.check and not REPORT_PATH.is_file():
        report["result_status"] = "FAIL"
        report.setdefault("checks", []).append(
            {
                "check_id": "report_exists",
                "status": "FAIL",
                "detail": "validation receipt is missing",
            }
        )
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("result_status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
