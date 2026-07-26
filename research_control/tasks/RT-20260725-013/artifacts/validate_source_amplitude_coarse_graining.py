#!/usr/bin/env python3
"""Validate the bounded P5-T06 source-amplitude coarse-graining packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_ROOT = REPO_ROOT / "research_control/tasks/RT-20260725-013/artifacts"
SPEC_PATH = ARTIFACT_ROOT / "source_amplitude_coarse_graining_spec_v1.yaml"
LEDGER_PATH = ARTIFACT_ROOT / "source_amplitude_scale_error_ledger_v1.yaml"
TEX_PATH = ARTIFACT_ROOT / "source_amplitude_resolution_coarse_graining_v1.tex"
CHILD_MATH_PATH = ARTIFACT_ROOT / "child_phys_math_source_amplitude_coarse_graining.yaml"
CHILD_PHIL_PATH = ARTIFACT_ROOT / "child_phys_phil_source_amplitude_coarse_graining.yaml"
CONFLICT_PATH = ARTIFACT_ROOT / "parent_conflict_review_source_amplitude_coarse_graining.yaml"
FUSION_PATH = ARTIFACT_ROOT / "parent_fusion_notes_source_amplitude_coarse_graining.md"
REPORT_PATH = ARTIFACT_ROOT / "source_amplitude_coarse_graining_validation_receipt_v1.json"
OBSTRUCTION_ID = "OBST-P5T06-QAMP-LOCAL-FIELD-RANK-001"


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


def quantize(amplitude: float, epsilon: float) -> float:
    if amplitude == 0.0:
        return 0.0
    return math.copysign(
        epsilon * math.floor(abs(amplitude) / epsilon + 0.5), amplitude
    )


def flow(amplitude: float, parameter: float, gamma: float) -> float:
    return amplitude / math.sqrt(
        1.0 + 2.0 * gamma * amplitude * amplitude * parameter
    )


def lattice_flow(code: float, epsilon: float, parameter: float, gamma: float) -> float:
    return quantize(flow(code, parameter, gamma), epsilon)


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required_paths = [
        SPEC_PATH,
        LEDGER_PATH,
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
        ledger = load_mapping(LEDGER_PATH)
        child_math = load_mapping(CHILD_MATH_PATH)
        child_phil = load_mapping(CHILD_PHIL_PATH)
        conflict = load_mapping(CONFLICT_PATH)
        tex = TEX_PATH.read_text(encoding="utf-8")
        fusion = FUSION_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {
            "schema_id": "source_amplitude_coarse_graining_validation_receipt_v1",
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
        and source.get("flow") == "f_lambda(a)=a/sqrt(1+2 gamma a^2 lambda)",
        "the exact P5-T03 state family, generator, and flow remain unchanged",
    )

    resolution = spec.get("resolution_map", {})
    add_check(
        checks,
        "map_typing",
        resolution.get("domain") == "Q_amp"
        and resolution.get("codomain") == "O_epsilon=epsilon Z with discrete topology"
        and resolution.get("coarse_graining_map") == "C_epsilon(q_a)=N_epsilon(a)"
        and resolution.get("reconstruction_map") == "R_epsilon(c)=q_c"
        and resolution.get("target_data_consumed") is False,
        "domain, codomain, coarse map, decoder, and source-only boundary are explicit",
    )

    epsilon = 0.2
    quantizer_cases = {
        2.3 * epsilon: 2.0 * epsilon,
        -2.5 * epsilon: -3.0 * epsilon,
        0.49 * epsilon: 0.0,
        0.51 * epsilon: epsilon,
        0.0: 0.0,
    }
    add_check(
        checks,
        "tie_and_threshold_controls",
        all(
            math.isclose(quantize(a, epsilon), expected, abs_tol=1e-12)
            for a, expected in quantizer_cases.items()
        ),
        "analytic examples reproduce the odd away-from-zero tie convention",
    )

    sample_amplitudes = [index * 0.037 for index in range(-500, 501)]
    amplitude_bounds = [
        abs(quantize(a, epsilon) - a) <= epsilon / 2.0 + 1e-12
        for a in sample_amplitudes
    ]
    add_check(
        checks,
        "uniform_amplitude_error",
        all(amplitude_bounds)
        and spec.get("approximation", {}).get("amplitude_error")
        == "|N_epsilon(a)-a|<=epsilon/2",
        "a dense finite grid satisfies the exact global half-bin error bound",
    )

    lattice_codes = [index * epsilon for index in range(-20, 21)]
    add_check(
        checks,
        "exact_code_round_trip",
        all(
            math.isclose(quantize(code, epsilon), code, abs_tol=1e-12)
            for code in lattice_codes
        ),
        "every sampled lattice code decodes and re-encodes exactly",
    )

    reflection_cases = [
        math.isclose(
            quantize(-a, epsilon), -quantize(a, epsilon), abs_tol=1e-12
        )
        for a in sample_amplitudes
    ]
    covariance = spec.get("covariance", {})
    add_check(
        checks,
        "declared_source_covariance",
        all(reflection_cases)
        and covariance.get("identity_redundancy_covariance") is True
        and covariance.get("target_diffeomorphism_covariance_claimed") is False
        and covariance.get("undeclared_source_isomorphism_covariance_claimed")
        is False,
        "reflection equivariance is exact and no broader covariance is inferred",
    )

    information = spec.get("information_loss", {})
    add_check(
        checks,
        "information_loss",
        information.get("noninjective_for_positive_resolution") is True
        and information.get("zero_fiber") == "|a|<epsilon/2"
        and information.get("half_grid_endpoints_in_zero_fiber") is False
        and "independent patch data"
        in information.get("lost_or_absent_observables", []),
        "fibers, zero-bin sign loss, and absent local data are explicit",
    )

    amplitude_envelope = 3.0
    quadratic_cases = []
    for amplitude in [
        -3.0,
        -2.37,
        -0.1,
        0.0,
        0.11,
        1.83,
        3.0,
    ]:
        code = quantize(amplitude, epsilon)
        actual = abs(amplitude * amplitude / 2.0 - code * code / 2.0)
        bound = amplitude_envelope * epsilon / 2.0 + epsilon * epsilon / 8.0
        quadratic_cases.append(actual <= bound + 1e-12)
    add_check(
        checks,
        "bounded_quadratic_error",
        all(quadratic_cases),
        "bounded-amplitude samples satisfy the declared quadratic-observable error",
    )

    gamma_values = (0.3, 1.0, 2.7)
    parameters = (0.0, 0.2, 1.4, 9.0)
    raw_cases: list[bool] = []
    lattice_cases: list[bool] = []
    for gamma in gamma_values:
        for parameter in parameters:
            for amplitude in sample_amplitudes[::17]:
                source_code = quantize(
                    flow(amplitude, parameter, gamma), epsilon
                )
                raw_effective = flow(
                    quantize(amplitude, epsilon), parameter, gamma
                )
                lattice_effective = quantize(raw_effective, epsilon)
                raw_cases.append(
                    abs(source_code - raw_effective) <= epsilon + 1e-12
                )
                lattice_cases.append(
                    abs(source_code - lattice_effective)
                    <= 1.5 * epsilon + 1e-12
                )
    add_check(
        checks,
        "dynamic_compatibility",
        all(raw_cases)
        and all(lattice_cases)
        and spec.get("dynamics", {}).get("source_flow_lipschitz_constant") == 1,
        "finite controls satisfy raw and lattice semiconjugacy bounds",
    )

    semigroup_cases: list[bool] = []
    for gamma in gamma_values:
        for parameter in (0.0, 0.3, 2.0):
            for second_parameter in (0.0, 0.7, 4.0):
                for code in lattice_codes:
                    composed = lattice_flow(
                        lattice_flow(code, epsilon, second_parameter, gamma),
                        epsilon,
                        parameter,
                        gamma,
                    )
                    direct = lattice_flow(
                        code, epsilon, parameter + second_parameter, gamma
                    )
                    semigroup_cases.append(
                        abs(composed - direct) <= 1.5 * epsilon + 1e-12
                    )
    add_check(
        checks,
        "lattice_semigroup_defect",
        all(semigroup_cases),
        "finite controls satisfy the declared lattice semigroup-defect bound",
    )

    averaging = spec.get("averaging_control", {})
    add_check(
        checks,
        "averaging_dichotomy",
        averaging.get("independent_local_modes_created") is False
        and "same one global amplitude"
        in averaging.get("nonzero_probe_result", "")
        and "collapses to zero" in averaging.get("zero_probe_result", ""),
        "linear source probes recover one amplitude or collapse it",
    )

    dimension = spec.get("dimension_and_smoothness", {})
    add_check(
        checks,
        "dimension_and_smoothness",
        dimension.get("domain_dimension") == 1
        and dimension.get("codomain_topology")
        == "countable zero-dimensional discrete lattice"
        and dimension.get("discontinuity_set")
        == "half-grid amplitude thresholds"
        and dimension.get("physical_dimension_inferred") is False
        and dimension.get("smooth_effective_geometry_inferred") is False,
        "source dimension, discrete codomain, discontinuities, and nonconclusions are explicit",
    )

    obstruction = spec.get("local_reconstruction_obstruction", {})
    add_check(
        checks,
        "rank_locality_obstruction",
        obstruction.get("obstruction_id") == OBSTRUCTION_ID
        and obstruction.get("source_extension_continuation") == "open"
        and obstruction.get("global_no_go_claimed") is False
        and len(obstruction.get("combined_basis", [])) == 3,
        "the exact current-family obstruction combines rank, patching, and phase evidence",
    )

    causal_path = spec.get("path_to_causal_structure", {})
    add_check(
        checks,
        "causal_structure_path",
        causal_path.get("status") == "explicit_unmet_dependency_chain"
        and len(causal_path.get("required_steps", [])) == 5
        and causal_path.get("supplied_by_current_map") is False,
        "the route to causal structure is explicit and remains unmet",
    )

    ledger_errors = {
        item.get("error_id"): item
        for item in ledger.get("error_ledger", [])
        if isinstance(item, dict)
    }
    add_check(
        checks,
        "scale_error_ledger",
        len(ledger.get("scale_registry", [])) == 2
        and set(ledger_errors)
        == {
            "P5T06-ERR-AMPLITUDE",
            "P5T06-ERR-SOURCE-STATE",
            "P5T06-ERR-QUADRATIC-OBSERVABLE",
            "P5T06-ERR-RAW-DYNAMICS",
            "P5T06-ERR-LATTICE-DYNAMICS",
            "P5T06-ERR-LATTICE-SEMIGROUP",
        },
        "all declared scales and six approximation errors have ledger entries",
    )

    branch_ids = {
        str(item.get("branch_id", ""))
        for item in spec.get("failure_branches", [])
        if isinstance(item, dict)
    }
    add_check(
        checks,
        "failure_branch_manifest",
        branch_ids
        == {
            "P5T06-FAIL-TARGET-THRESHOLDS",
            "P5T06-FAIL-LOCAL-FIELD-OVERREAD",
            "P5T06-FAIL-PHYSICAL-SCALE-OVERREAD",
            "P5T06-FAIL-SMOOTHNESS-OVERREAD",
            "P5T06-FAIL-INFORMATION-CREATION",
            "P5T06-FAIL-AVERAGING-COLLAPSE",
        },
        "target import, locality, scale, smoothness, information, and averaging failures are fail closed",
    )

    add_check(
        checks,
        "parent_child_synthesis",
        child_math.get("status") == "completed"
        and child_phil.get("status") == "completed"
        and child_math.get("ontology_formalizer_result", {}).get("result_type")
        == "bridge_map_candidate_with_scoped_obstruction"
        and child_phil.get("ontology_formalizer_result", {}).get("result_type")
        == "bridge_map_candidate_with_scoped_obstruction"
        and conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == [],
        "both internal perspectives agree on the map and scoped obstruction",
    )

    required_tex_markers = (
        "Resolution-indexed source map",
        "Information loss and surviving observables",
        "Controlled dynamical compatibility",
        "Scoped rank and locality obstruction",
        "The explicit path to causal structure",
        OBSTRUCTION_ID,
    )
    add_check(
        checks,
        "fused_tex_markers",
        all(marker in tex for marker in required_tex_markers),
        "the fused TeX source contains the map, errors, obstruction, and causal path",
    )

    forbidden_positive_claims = (
        "canonical ontology is adopted",
        "physical coarse-graining is established",
        "physical scale is derived",
        "causal structure is reconstructed",
        "effective metric is constructed",
        "all source extensions are impossible",
        "the theory is rejected",
        "einstein equations are derived",
    )
    combined = f"{tex}\n{fusion}".lower()
    add_check(
        checks,
        "claim_boundary",
        not any(marker in combined for marker in forbidden_positive_claims),
        "the packet contains no adoption, physical-scale, geometry, global-no-go, or downstream-GR promotion",
    )

    result = spec.get("result", {})
    add_check(
        checks,
        "decisive_result",
        result.get("result_kind")
        == "source_observable_coarse_graining_candidate_with_precise_local_reconstruction_obstruction"
        and result.get("plan_task_status") == "completed_ready_for_checkpoint"
        and result.get("next_plan_task_id") == "P5-T07"
        and result.get("route_frozen") is False,
        "P5-T06 has a decisive map-plus-obstruction result and a distinct audit successor",
    )

    overall = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    artifact_hashes = {
        path.relative_to(REPO_ROOT).as_posix(): sha256(path)
        for path in required_paths
        if path.is_file()
    }
    return {
        "schema_id": "source_amplitude_coarse_graining_validation_receipt_v1",
        "result_status": overall,
        "task_id": "RT-20260725-013",
        "job_id": "AJ-RT-20260725-013-001",
        "plan_task_id": "P5-T06",
        "candidate_id": "V21-P5-T03-CUBIC-AMPLITUDE-SOURCE-DYNAMICS-V1",
        "candidate_unchanged": True,
        "result_kind": (
            "source_observable_coarse_graining_candidate_with_precise_"
            "local_reconstruction_obstruction"
        ),
        "obstruction_id": OBSTRUCTION_ID,
        "obstruction_scope": "exact current Q_amp family only",
        "route_frozen": False,
        "finding_counts": {
            "pass": sum(item["status"] == "PASS" for item in checks),
            "fail": sum(item["status"] == "FAIL" for item in checks),
            "theorems": 3,
            "propositions": 2,
            "analytic_examples": 4,
            "negative_controls": 3,
            "scoped_obstructions": 1,
            "unresolved_conflicts": 0,
        },
        "validator_ids": [
            "candidate_lock",
            "map_typing",
            "tie_and_threshold_controls",
            "uniform_amplitude_error",
            "exact_code_round_trip",
            "declared_source_covariance",
            "information_loss",
            "bounded_quadratic_error",
            "dynamic_compatibility",
            "lattice_semigroup_defect",
            "averaging_dichotomy",
            "dimension_and_smoothness",
            "rank_locality_obstruction",
            "causal_structure_path",
            "scale_error_ledger",
            "failure_branch_manifest",
            "parent_child_synthesis",
            "claim_boundary",
            "decisive_result",
        ],
        "claim_boundary_summary": (
            "Candidate-specific draft/control source-amplitude resolution map, "
            "source-state reconstruction, error bounds, and precise local-field "
            "obstruction only; no canonical ontology or source-law adoption, "
            "physical scale, local field, causal structure, M_src, g_eff, "
            "downstream GR, promotion, global theory rejection, or future-"
            "extension impossibility authority."
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
