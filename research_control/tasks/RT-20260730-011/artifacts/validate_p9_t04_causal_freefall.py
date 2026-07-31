#!/usr/bin/env python3
"""Validate the exact, source-only P9-T04 causal/free-fall packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent

SOURCE_HASHES = {
    "research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_protocol_v1.tex":
        "88ef097bf712ad115e9af62cc18a8b3eabb12f8545350f714ad065f702471007",
    "research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_case_schema_v1.yaml":
        "5045de8fbaeb6c80b89ec88b71143a8aeaca1c892efadc4b7293cb438ee808d8",
    "research_control/tasks/RT-20260729-012/artifacts/target_import_firewall_v1.yaml":
        "ccb9297f817a9b4eeb886834a510e1f21d518a2668bc3fde9695b909d6884acf",
    "research_control/tasks/RT-20260727-007/artifacts/source_matter_sector_charge_taxonomy_v1.yaml":
        "0b7bb06a63b20469185badab4b2664eaa23d5b4e47752b953d51c2508f283c59",
    "research_control/tasks/RT-20260728-001/artifacts/source_matter_finite_transition_kernel_candidate_v1.tex":
        "65ac095f5cdf4c2e319365c8b0e024d031b19d9fc2b8102e59997afa1e8f9129",
    "research_control/tasks/RT-20260728-002/artifacts/source_operational_device_suite_candidate_v1.tex":
        "d6c818ee29f1a7e659e2f454aec21431d680b3d2d4df048fcf36f4aba87ba22a",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex":
        "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    "research_control/tasks/RT-20260730-008/artifacts/p9_t02_vacuum_minkowski_case_v1.yaml":
        "2fadb19c5849f1da5843c0e0599dbdc31790eab46587ce6718abbf4d3a0be79c",
    "research_control/tasks/RT-20260730-010/artifacts/p9_t03_weak_field_clock_case_v1.yaml":
        "45b79d5e3e371b3a2bcdde3f26296dad8c6ff65306d17cdf672bf76383eeb864",
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


def matmul_row(row: tuple[Fraction, Fraction],
               matrix: tuple[tuple[Fraction, Fraction],
                             tuple[Fraction, Fraction]]) -> tuple[Fraction, Fraction]:
    return (
        row[0] * matrix[0][0] + row[1] * matrix[1][0],
        row[0] * matrix[0][1] + row[1] * matrix[1][1],
    )


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
        "finite_two_sector_causal_freefall_nonselection_v1.tex",
        "p9_t04_causal_freefall_case_v1.yaml",
        "p9_t04_sector_comparison_matrix_v1.yaml",
        "p9_t04_equivalence_principle_residuals_v1.yaml",
        "p9_t04_provenance_dag_v1.yaml",
        "p9_t04_source_output_seal_v1.json",
        "p9_t04_target_exposure_ledger_v1.yaml",
        "p9_t04_causal_freefall_receipt_v1.json",
        "child_phys_math_p9_t04_causal_freefall.yaml",
        "child_phys_phil_p9_t04_causal_freefall.yaml",
        "parent_conflict_review_p9_t04_causal_freefall.yaml",
        "parent_fusion_notes_p9_t04_causal_freefall.md",
    ]
    record("required_artifacts",
           all((ARTIFACT_DIR / name).is_file() for name in required),
           "all bounded P9-T04 artifacts exist")

    for relpath, expected in SOURCE_HASHES.items():
        path = ROOT / relpath
        actual = sha256(path) if path.is_file() else ""
        record(f"source_hash:{relpath}", actual == expected,
               f"expected={expected} actual={actual}")

    case = load_yaml("p9_t04_causal_freefall_case_v1.yaml")
    matrix = load_yaml("p9_t04_sector_comparison_matrix_v1.yaml")
    residuals = load_yaml("p9_t04_equivalence_principle_residuals_v1.yaml")
    dag = load_yaml("p9_t04_provenance_dag_v1.yaml")
    exposure = load_yaml("p9_t04_target_exposure_ledger_v1.yaml")
    seal = load_json("p9_t04_source_output_seal_v1.json")
    receipt = load_json("p9_t04_causal_freefall_receipt_v1.json")

    half = Fraction(1, 2)
    movable = ((half, half), (Fraction(0), Fraction(1)))
    identity = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    mu = (Fraction(1), Fraction(0))
    endpoint = []
    current = mu
    for _ in range(4):
        current = matmul_row(current, movable)
        endpoint.append(current[1])
    record("movable_kernel_power",
           endpoint == [Fraction(1, 2), Fraction(3, 4),
                        Fraction(7, 8), Fraction(15, 16)],
           f"endpoint responses={endpoint}")
    record("identity_kernel_power",
           matmul_row(mu, identity) == mu,
           "identity-only endpoint response remains zero")

    common = ["0", "0", "0", "0", "0"]
    split = ["1", "1/2", "1/4", "1/4", "1/4"]
    matrix_records = {r["record_id"]: r for r in matrix.get("records", [])}
    residual_records = {r["record_id"]: r for r in residuals.get("records", [])}
    record("common_residual_vector",
           matrix_records.get("E_common", {}).get("exact_residual_vector") == common
           and residual_records.get("E_common", {}).get("residual_vector") == common
           and seal.get("source_output", {}).get("common_residual_vector") == common,
           "common equipment record has exact zero residual")
    record("split_residual_vector",
           matrix_records.get("E_split", {}).get("exact_residual_vector") == split
           and residual_records.get("E_split", {}).get("residual_vector") == split
           and seal.get("source_output", {}).get("split_residual_vector") == split,
           "split equipment record has exact nonzero residual")

    record("case_disposition",
           case.get("candidate_constructor_result") == "precise_obstruction"
           and case.get("execution_status") == "INCONCLUSIVE"
           and case.get("secondary_label") == "FORMAL_ANALOGY"
           and case.get("case_classification", {}).get("benchmark_pass") is False,
           "precise obstruction, INCONCLUSIVE, FORMAL_ANALOGY, zero pass")
    record("obstruction_identity",
           case.get("obstruction_id")
           == "OBST-P9T04-SECTOR-CAUSAL-FREEFALL-SELECTOR-ABSENT-001"
           and receipt.get("mathematical_payload", {}).get("exact_failure"),
           "missing total sector/role operational selector is explicit")
    record("firewall",
           case.get("source_stage_firewall_status") == "PASS"
           and dag.get("forbidden_reachability_result", {}).get(
               "target_to_source_stage_path_count") == 0
           and exposure.get("source_stage_exposure", {}).get(
               "target_oracle_opened") is False
           and seal.get("target_oracle_opened") is False
           and seal.get("target_informed_rerun_count") == 0,
           "no forbidden target-to-source path or target-informed rerun")
    record("physical_boundary",
           case.get("model_to_world_map", {}).get("status") == "MISSING"
           and case.get("local_inertial_audit", {}).get("disposition")
           == "NO_LOCAL_INERTIAL_APPROXIMATION_CONSTRUCTED"
           and case.get("authority_limits", {}).get(
               "equivalence_principle_established") is False,
           "physical causal, inertial, and free-fall interpretations remain unset")
    record("cumulative_status",
           receipt.get("case_classification", {}).get(
               "cumulative_executed_case_count") == 3
           and receipt.get("case_classification", {}).get(
               "passed_case_count") == 0,
           "three executed P9 cases and zero passes")

    text = (ARTIFACT_DIR /
            "finite_two_sector_causal_freefall_nonselection_v1.tex").read_text(
                encoding="utf-8")
    markers = [
        "P9T04-THM-SECTOR-CAUSAL-FREEFALL-NONSELECTION-001",
        "OBST-P9T04-SECTOR-CAUSAL-FREEFALL-SELECTOR-ABSENT-001",
        "blocked\\_adoption\\_open\\_continuation",
        "not a physical propagation speed",
        "INCONCLUSIVE",
        "FORMAL\\_ANALOGY",
    ]
    record("tex_claim_markers",
           all(marker in text for marker in markers),
           "TeX contains decisive result and interpretation boundaries")

    passed = all(item["status"] == "PASS" for item in checks)
    result = {
        "schema_id": "p9_t04_causal_freefall_validation_v1",
        "task_id": "RT-20260730-011",
        "job_id": "AJ-RT-20260730-011-001",
        "status": "PASS" if passed else "FAIL",
        "check_count": len(checks),
        "failure_count": sum(item["status"] == "FAIL" for item in checks),
        "checks": checks,
        "authority_limits": {
            "validator_is_physics_proof": False,
            "benchmark_pass_established": False,
            "physics_promotion_authorized": False,
        },
    }
    print(json.dumps(result, indent=2 if args.json else None, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
