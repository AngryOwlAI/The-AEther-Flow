#!/usr/bin/env python3
"""Validate the fresh P16-T02 re-audit evidence without repairing it.

This task-local validator is operational support only.  A PASS means that the
audit faithfully records the current Gate A registry/validator identity drift;
it does not mean that P16-T02 or any scientific Gate passes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_PATH = REPO_ROOT / "research_control/tasks/RT-20260803-010/artifacts/v21_p16_t02_reaudit_validation.json"

PROTECTED_HASHES = {
    "research_control/tasks/RT-20260724-004/artifacts/human_authorization_p4_t05_continuum_first_v1.yaml": "3421808c71a64279ef5ba62df5376ab4999d2c67978d4f7ceabbeb0ae9b2bde6",
    "research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex": "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml": "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_external_red_team_review_v1.yaml": "77779a4db679492b47ebd0652cd67c2a3f17e69aa7ee06917ab8089bcdabafae",
    "research_control/tasks/RT-20260729-001/artifacts/human_authorization_p7_t08_physical_matter_adoption_v1.yaml": "9da90540e60a9bc1b624689a4b694460c77ac5d99306319dcedefb291be9a6f2",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex": "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_scientific_status_v1.yaml": "5f84e9c0495514632e7b6c25a809e4e6c1044c69f159ce0e1e38900fc5229d73",
    "research_control/tasks/RT-20260729-011/artifacts/human_authorization_p8_t07_gate_d_review_v1.yaml": "c1de70d4431e432a9f9b0f092cf4469b4f514ba6154a35976c62cfe44636d56d",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex": "035ea88a612d861a00d0703ec2bd1094e01194c113d7ff2588e3a4ad8bf47d63",
    "research_control/tasks/RT-20260731-004/artifacts/human_authorization_p9_t09_gate_e_review_v1.yaml": "b248937b11448f7b1cd0fcb1a751ac643844107c9489a29b4e702779ab492646",
    "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex": "7f28103e40664f0a004af0134f3216932136f8efb160f0c7c59039efa5225b0b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_row(relative_path: str, key: str, value: str) -> dict[str, str]:
    with (REPO_ROOT / relative_path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get(key) == value:
                return row
    raise ValueError(f"missing_row:{relative_path}:{key}={value}")


def build_report() -> dict[str, object]:
    errors: list[str] = []
    protected = {}
    for relative_path, expected in PROTECTED_HASHES.items():
        observed = sha256(REPO_ROOT / relative_path)
        match = observed == expected
        protected[relative_path] = {"expected": expected, "observed": observed, "match": match}
        if not match:
            errors.append(f"protected_hash_mismatch:{relative_path}")

    gate_a = csv_row(
        "registries/TEX_SOURCE_REGISTRY.csv",
        "object_id",
        "TEX-V21-P4-T05-ONTOLOGY-REGIME-GATE-CHAIR-DECISION-V1",
    )
    repair_validator_path = REPO_ROOT / "research_control/tasks/RT-20260803-005/artifacts/validate_p16_t02_gate_status_layer_contract.py"
    repair_validator_text = repair_validator_path.read_text(encoding="utf-8")
    gate_a_checks = {
        "exact_gate_a_registry_validation_status": gate_a.get("validation_status"),
        "expected_unrepaired_status": "PENDING",
        "historical_repair_validator_sha256": sha256(repair_validator_path),
        "historical_validator_targets_foundations_object": "TEX-ONTOLOGY-AETHER-FLOW-FOUNDATIONS" in repair_validator_text,
        "historical_validator_targets_exact_gate_a_object": "TEX-V21-P4-T05-ONTOLOGY-REGIME-GATE-CHAIR-DECISION-V1" in repair_validator_text,
    }
    identity_drift_confirmed = (
        gate_a_checks["exact_gate_a_registry_validation_status"] == "PENDING"
        and gate_a_checks["historical_validator_targets_foundations_object"] is True
        and gate_a_checks["historical_validator_targets_exact_gate_a_object"] is False
    )
    gate_a_checks["identity_drift_confirmed"] = identity_drift_confirmed
    if not identity_drift_confirmed:
        errors.append("gate_a_registry_validator_identity_drift_not_exactly_preserved")

    matter = csv_row("registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "matter_coupling")
    gate_e = csv_row("registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "gate_chair_status")
    expected_layers = {
        "matter_control_status": (matter.get("control_status"), "gate_review_completed"),
        "matter_mathematical_status": (matter.get("mathematical_status"), "parameterized_finite_local_witness_precondition"),
        "matter_physical_status": (matter.get("physical_status"), "not_target_matter_coupling_source_side_postulate_adoption_only"),
        "matter_promotion_status": (matter.get("promotion_status"), "scoped_source_postulate_adoption_only"),
        "gate_e_control_status": (gate_e.get("control_status"), "gate_review_completed"),
        "gate_e_mathematical_status": (gate_e.get("mathematical_status"), "protected_negative_verdict_recorded_positive_closure_missing"),
        "gate_e_physical_status": (gate_e.get("physical_status"), "no_positive_benchmark_closure"),
        "gate_e_promotion_status": (gate_e.get("promotion_status"), "human_gate_required"),
    }
    layer_checks = {}
    for check_id, (observed, expected) in expected_layers.items():
        match = observed == expected
        layer_checks[check_id] = {"expected": expected, "observed": observed, "match": match}
        if not match:
            errors.append(f"status_layer_mismatch:{check_id}")

    required_artifacts = [
        "research_control/tasks/RT-20260803-010/artifacts/child_phys_math_p16_t02_gate_consistency_reaudit.yaml",
        "research_control/tasks/RT-20260803-010/artifacts/child_phys_phil_p16_t02_gate_consistency_reaudit.yaml",
        "research_control/tasks/RT-20260803-010/artifacts/parent_conflict_review_p16_t02_gate_consistency_reaudit.yaml",
        "research_control/tasks/RT-20260803-010/artifacts/parent_fusion_notes_p16_t02_gate_consistency_reaudit.md",
        "research_control/tasks/RT-20260803-010/artifacts/v21_p16_t02_authority_path_reaudit.yaml",
        "research_control/tasks/RT-20260803-010/artifacts/v21_p16_t02_gate_consistency_reaudit.md",
        "research_control/tasks/RT-20260803-010/artifacts/v21_p16_t02_reaudit_findings.yaml",
        "research_control/tasks/RT-20260803-010/artifacts/v21_p16_t02_reaudit_compact_receipt.json",
    ]
    artifact_checks = {path: (REPO_ROOT / path).is_file() for path in required_artifacts}
    errors.extend(f"missing_artifact:{path}" for path, present in artifact_checks.items() if not present)

    return {
        "schema_id": "v21_p16_t02_gate_consistency_reaudit_validation_v1",
        "task_id": "RT-20260803-010",
        "result_status": "PASS_REPAIR_REQUIRED_FINDING_PRESERVED" if not errors else "FAIL",
        "audit_disposition": "REPAIR_REQUIRED_GATE_A_REGISTRY_VALIDATOR_IDENTITY_DRIFT",
        "protected_hashes": protected,
        "gate_a_identity_checks": gate_a_checks,
        "status_layer_checks": layer_checks,
        "required_artifacts": artifact_checks,
        "errors": errors,
        "authority_limits": {
            "validator_pass_is_science": False,
            "scientific_status_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["result_status"])
    return 0 if report["result_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
