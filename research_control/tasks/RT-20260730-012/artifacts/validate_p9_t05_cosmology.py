#!/usr/bin/env python3
"""Validate the bounded, source-first P9-T05 cosmology packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent

SOURCE_HASHES = {
    "research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex":
        "a2b9c6670cdb0e09ca2e19ff30f71d9bb954e3ab2fc73a5c9727a2df10db93aa",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex":
        "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    "research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_protocol_v1.tex":
        "88ef097bf712ad115e9af62cc18a8b3eabb12f8545350f714ad065f702471007",
    "research_control/tasks/RT-20260730-011/artifacts/p9_t04_causal_freefall_case_v1.yaml":
        "f3ee6d0d7c19f68daf9f6ed9a2e10cec964633694688cc62074edc9089f66255",
}

SEALED_SOURCE_HASHES = {
    "source_homogeneous_amplitude_record_v1.yaml":
        "dc0481df6d3b628b9af402b372d78c10047a48dec94b9dce3cc1b5579707c14b",
    "source_expansion_decoder_nonselection_v1.tex":
        "8de49fa7a57c4e02f1b44147a0fa5f17dad89a1ec5f2ebf5695aaa4d8b14f1cf",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    value = yaml.safe_load((ARTIFACT_DIR / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain a mapping")
    return value


def load_json(name: str) -> dict[str, Any]:
    value = json.loads((ARTIFACT_DIR / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain an object")
    return value


def rk4_endpoint(step: float = 1.0 / 10000.0,
                 endpoint: float = 2.0) -> float:
    """Integrate A'=-A^3, A(0)=1 on the fixed source-only fixture."""
    value = 1.0
    steps = round(endpoint / step)

    def rhs(amplitude: float) -> float:
        return -(amplitude ** 3)

    for _ in range(steps):
        k1 = rhs(value)
        k2 = rhs(value + 0.5 * step * k1)
        k3 = rhs(value + 0.5 * step * k2)
        k4 = rhs(value + step * k3)
        value += step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def record(check_id: str, passed: bool, detail: str) -> None:
        checks.append({
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        })

    required = [
        "source_homogeneous_amplitude_record_v1.yaml",
        "source_expansion_decoder_nonselection_v1.tex",
        "p9_t05_cosmology_case_v1.yaml",
        "p9_t05_cosmology_comparison_matrix_v1.yaml",
        "p9_t05_provenance_dag_v1.yaml",
        "p9_t05_source_output_seal_v1.json",
        "p9_t05_target_exposure_ledger_v1.yaml",
        "p9_t05_cosmology_receipt_v1.json",
        "child_phys_math_p9_t05_cosmology.yaml",
        "child_phys_phil_p9_t05_cosmology.yaml",
        "parent_conflict_review_p9_t05_cosmology.yaml",
        "parent_fusion_notes_p9_t05_cosmology.md",
    ]
    record(
        "required_artifacts",
        all((ARTIFACT_DIR / name).is_file() for name in required),
        "all bounded P9-T05 artifacts exist",
    )

    for relpath, expected in SOURCE_HASHES.items():
        path = ROOT / relpath
        actual = sha256(path) if path.is_file() else ""
        record(
            f"source_hash:{relpath}",
            actual == expected,
            f"expected={expected} actual={actual}",
        )

    seal = load_json("p9_t05_source_output_seal_v1.json")
    sealed_manifest = seal.get("sealed_source_files", {})
    for filename, expected in SEALED_SOURCE_HASHES.items():
        actual = sha256(ARTIFACT_DIR / filename)
        record(
            f"sealed_source_hash:{filename}",
            actual == expected and sealed_manifest.get(filename) == expected,
            f"expected={expected} actual={actual}",
        )

    source = load_yaml("source_homogeneous_amplitude_record_v1.yaml")
    case = load_yaml("p9_t05_cosmology_case_v1.yaml")
    matrix = load_yaml("p9_t05_cosmology_comparison_matrix_v1.yaml")
    dag = load_yaml("p9_t05_provenance_dag_v1.yaml")
    exposure = load_yaml("p9_t05_target_exposure_ledger_v1.yaml")
    receipt = load_json("p9_t05_cosmology_receipt_v1.json")
    math_view = load_yaml("child_phys_math_p9_t05_cosmology.yaml")
    phil_view = load_yaml("child_phys_phil_p9_t05_cosmology.yaml")
    conflict = load_yaml("parent_conflict_review_p9_t05_cosmology.yaml")

    exact_endpoint = 1.0 / math.sqrt(5.0)
    integrated_endpoint = rk4_endpoint()
    integration_error = abs(integrated_endpoint - exact_endpoint)
    record(
        "fixed_step_rk4",
        integration_error < 2.0e-12,
        f"endpoint={integrated_endpoint:.17g} exact={exact_endpoint:.17g} "
        f"absolute_error={integration_error:.3e}",
    )

    exponents = (1.0, 2.0, 4.0)
    endpoint_tokens = tuple(5.0 ** (p / 2.0) for p in exponents)
    endpoint_rates = tuple(p / 5.0 for p in exponents)
    deceleration_tokens = tuple(2.0 / p - 1.0 for p in exponents)
    record(
        "decoder_fixture",
        all(abs(a - b) < 1.0e-14 for a, b in zip(
            endpoint_tokens, (math.sqrt(5.0), 5.0, 25.0)))
        and endpoint_rates == (0.2, 0.4, 0.8)
        and deceleration_tokens == (1.0, 0.0, -0.5),
        f"b={endpoint_tokens} E={endpoint_rates} Q={deceleration_tokens}",
    )
    record(
        "decoder_nonselection",
        len(set(endpoint_tokens)) == 3
        and source.get("decoder_counterfamily", {}).get(
            "selected_decoder") == "ABSENT"
        and source.get("decoder_counterfamily", {}).get(
            "selected_physical_clock_map") == "ABSENT",
        "same amplitude history gives distinct p=1,2,4 tokens and no selector",
    )
    record(
        "density_nonselection",
        source.get("matter_bookkeeping_counterfamily", {}).get(
            "selected_volume_exponent") == "ABSENT"
        and source.get("matter_bookkeeping_counterfamily", {}).get(
            "selected_physical_volume_map") == "ABSENT",
        "density identity is exact while the volume decoder remains unselected",
    )
    record(
        "symmetry_boundary",
        case.get("source_symmetry_audit", {}).get(
            "source_uniformity_satisfied") is True
        and case.get("source_symmetry_audit", {}).get(
            "physical_homogeneity_established") is False
        and case.get("source_symmetry_audit", {}).get(
            "physical_isotropy_established") is False,
        "single-mode source uniformity is not a physical spatial symmetry claim",
    )
    record(
        "constant_term_boundary",
        case.get("constant_term_audit", {}).get(
            "source_derived_constant_to_expansion_map_present") is False
        and case.get("constant_term_audit", {}).get(
            "physical_vacuum_status") == "NOT_ESTABLISHED",
        "no physical vacuum conclusion is inferred from the source ODE",
    )
    record(
        "case_disposition",
        case.get("candidate_constructor_result") == "precise_obstruction"
        and case.get("execution_status") == "INCONCLUSIVE"
        and case.get("secondary_label") == "FORMAL_ANALOGY"
        and case.get("case_classification", {}).get("benchmark_pass") is False,
        "precise obstruction, INCONCLUSIVE, FORMAL_ANALOGY, zero pass",
    )
    record(
        "obstruction_identity",
        case.get("obstruction_id")
        == "OBST-P9T05-SOURCE-COSMOLOGY-DECODER-CALIBRATION-NONSELECTION-001"
        and bool(receipt.get("mathematical_payload", {}).get("exact_failure")),
        "failed total physical decoder and calibration map is explicit",
    )
    record(
        "firewall",
        case.get("source_stage_firewall_status") == "PASS"
        and dag.get("forbidden_reachability_result", {}).get(
            "target_to_source_stage_path_count") == 0
        and dag.get("forbidden_reachability_result", {}).get(
            "source_mutation_after_target_comparison_count") == 0
        and exposure.get("source_stage_exposure", {}).get(
            "target_comparison_opened") is False
        and exposure.get("comparison_stage", {}).get(
            "opened_after_source_seal") is True
        and exposure.get("comparison_stage", {}).get(
            "target_informed_rerun_count") == 0,
        "target comparison opened only after seal with no source mutation or rerun",
    )
    rows = matrix.get("rows", [])
    record(
        "typed_comparison",
        len(rows) == 8
        and matrix.get("summary", {}).get("comparable_row_count") == 0
        and matrix.get("summary", {}).get("benchmark_pass_count") == 0,
        "eight physical burdens are nonunique, absent, or uncontrolled",
    )
    record(
        "model_to_world_boundary",
        case.get("model_to_world_map", {}).get("status") == "MISSING"
        and case.get("authority_limits", {}).get(
            "physical_expansion_law_established") is False
        and case.get("authority_limits", {}).get(
            "dark_energy_established_or_refuted") is False,
        "physical expansion, matter, and vacuum interpretations remain unset",
    )
    record(
        "cumulative_status",
        receipt.get("case_classification", {}).get(
            "cumulative_executed_case_count") == 4
        and receipt.get("case_classification", {}).get(
            "cumulative_inconclusive_case_count") == 4
        and receipt.get("case_classification", {}).get(
            "passed_case_count") == 0,
        "four executed P9 cases are INCONCLUSIVE and zero pass",
    )
    record(
        "internal_fusion",
        math_view.get("result", {}).get(
            "candidate_constructor_result") == "precise_obstruction"
        and phil_view.get("result", {}).get("outcome") == "INCONCLUSIVE"
        and conflict.get("unresolved_conflict_count") == 0
        and math_view.get("subagent_count") == 0
        and phil_view.get("subagent_count") == 0,
        "two internal perspectives fuse without child AgentJobs or subagents",
    )

    tex = (ARTIFACT_DIR /
           "source_expansion_decoder_nonselection_v1.tex").read_text(
               encoding="utf-8")
    fusion = (ARTIFACT_DIR /
              "parent_fusion_notes_p9_t05_cosmology.md").read_text(
                  encoding="utf-8")
    markers = [
        "Exact decoder nonselection",
        "Qtoken_p=\\frac{2}{p}-1",
        "OBST-P9T05-SOURCE-COSMOLOGY-DECODER-CALIBRATION-NONSELECTION-001",
        "blocked_adoption_open_continuation",
        "`INCONCLUSIVE`",
        "`FORMAL_ANALOGY`",
    ]
    combined = tex + "\n" + fusion
    record(
        "claim_markers",
        all(marker in combined for marker in markers),
        "source theorem and fusion note contain the decisive result and boundaries",
    )

    passed = all(item["status"] == "PASS" for item in checks)
    result = {
        "schema_id": "p9_t05_cosmology_validation_v1",
        "task_id": "RT-20260730-012",
        "job_id": "AJ-RT-20260730-012-001",
        "status": "PASS" if passed else "FAIL",
        "check_count": len(checks),
        "failure_count": sum(item["status"] == "FAIL" for item in checks),
        "checks": checks,
        "authority_limits": {
            "validator_is_physics_proof": False,
            "physical_cosmology_established": False,
            "benchmark_pass_established": False,
            "physics_promotion_authorized": False,
        },
    }
    print(json.dumps(result, indent=2 if args.json else None, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
