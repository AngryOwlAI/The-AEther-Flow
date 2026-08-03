#!/usr/bin/env python3
"""Validate post-repair P16-T02 audit evidence as control evidence only."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260803-012"
JOB_ID = "AJ-RT-20260803-012-001"
REPORT_PATH = REPO_ROOT / "research_control/tasks/RT-20260803-012/artifacts/v21_p16_t02_post_repair_reaudit_validation.json"
GATE_A_OBJECT_ID = "TEX-V21-P4-T05-ONTOLOGY-REGIME-GATE-CHAIR-DECISION-V1"
GATE_A_SOURCE_PATH = "research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex"
GATE_A_SOURCE_SHA256 = "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934"

PROTECTED_HASHES = {
    "research_control/tasks/RT-20260724-004/artifacts/human_authorization_p4_t05_continuum_first_v1.yaml": "3421808c71a64279ef5ba62df5376ab4999d2c67978d4f7ceabbeb0ae9b2bde6",
    GATE_A_SOURCE_PATH: GATE_A_SOURCE_SHA256,
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
REPAIR_HASHES = {
    "research_control/tasks/RT-20260803-011/artifacts/validate_p16_t02_gate_a_registry_validator_identity_parity.py": "b75f243a293c652b99a0d7c9e1972511b26b83e746232e497bd456b974dd8190",
    "research_control/tasks/RT-20260803-011/artifacts/p16_t02_gate_a_registry_validator_identity_parity_validation.json": "e94b5dcb5b54754a25a2f48ffb040c0e4040783b8aff19634be8610187f116d9",
    "research_control/tasks/RT-20260803-011/artifacts/p16_t02_gate_a_registry_validator_identity_parity_receipt.json": "0fd2cf483b7db6cc4e220d57365faba2eec9d8388fd0fbc2d52925887138adaf",
    "research_control/tasks/RT-20260803-011/jobs/completions/AJC-AJ-RT-20260803-011-001.yaml": "20b08b8f3988b71828467475d8437ae6ff7801b064c6eb816143b5c595214031",
    "research_control/tasks/RT-20260803-005/artifacts/validate_p16_t02_gate_status_layer_contract.py": "9ba655982225774beef866ec43f0a8fd116182f8987088afab78736fec5ac5e7",
    "research_control/tasks/RT-20260803-005/artifacts/p16_t02_gate_status_layer_contract_validation.json": "330c35edb94d153553f33e449bfa94b2a3e88c435cb6ce99e95f7a89d56fc401",
}
REQUIRED_ARTIFACTS = [
    "research_control/tasks/RT-20260803-012/artifacts/child_phys_math_p16_t02_post_repair_reaudit.yaml",
    "research_control/tasks/RT-20260803-012/artifacts/child_phys_phil_p16_t02_post_repair_reaudit.yaml",
    "research_control/tasks/RT-20260803-012/artifacts/parent_conflict_review_p16_t02_post_repair_reaudit.yaml",
    "research_control/tasks/RT-20260803-012/artifacts/parent_fusion_notes_p16_t02_post_repair_reaudit.md",
    "research_control/tasks/RT-20260803-012/artifacts/v21_p16_t02_post_repair_authority_path_reaudit.yaml",
    "research_control/tasks/RT-20260803-012/artifacts/v21_p16_t02_post_repair_gate_consistency_reaudit.md",
    "research_control/tasks/RT-20260803-012/artifacts/v21_p16_t02_post_repair_reaudit_findings.yaml",
    "research_control/tasks/RT-20260803-012/artifacts/v21_p16_t02_post_repair_reaudit_compact_receipt.json",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_row(relative_path: str, key: str, value: str) -> dict[str, str]:
    with (REPO_ROOT / relative_path).open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get(key) == value]
    if len(rows) != 1:
        raise ValueError(f"row_count:{relative_path}:{key}={value}:{len(rows)}")
    return rows[0]


def record(checks: dict[str, Any], errors: list[str], name: str, observed: Any, expected: Any) -> None:
    match = observed == expected
    checks[name] = {"expected": expected, "observed": observed, "match": match}
    if not match:
        errors.append(f"{name}_mismatch")


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, Any] = {}
    for group, expected_map in (("protected", PROTECTED_HASHES), ("repair", REPAIR_HASHES)):
        group_checks: dict[str, Any] = {}
        for relative_path, expected in expected_map.items():
            path = REPO_ROOT / relative_path
            observed = sha256(path) if path.is_file() and not path.is_symlink() else None
            match = observed == expected
            group_checks[relative_path] = {"expected": expected, "observed": observed, "match": match}
            if not match:
                errors.append(f"{group}_hash_mismatch:{relative_path}")
        checks[f"{group}_hashes"] = group_checks

    gate_a = csv_row("registries/TEX_SOURCE_REGISTRY.csv", "object_id", GATE_A_OBJECT_ID)
    record(checks, errors, "gate_a_path", gate_a.get("path"), GATE_A_SOURCE_PATH)
    record(checks, errors, "gate_a_registry_source_hash", gate_a.get("source_hash"), GATE_A_SOURCE_SHA256)
    record(checks, errors, "gate_a_registry_validation_status", gate_a.get("validation_status"), "PASS")
    record(checks, errors, "gate_a_registry_last_validated_at", gate_a.get("last_validated_at"), "2026-08-03T16:47:10Z")

    matter = csv_row("registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "matter_coupling")
    gate_e = csv_row("registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "gate_chair_status")
    layers = {
        "matter_control_status": (matter.get("control_status"), "gate_review_completed"),
        "matter_mathematical_status": (matter.get("mathematical_status"), "parameterized_finite_local_witness_precondition"),
        "matter_physical_status": (matter.get("physical_status"), "not_target_matter_coupling_source_side_postulate_adoption_only"),
        "matter_promotion_status": (matter.get("promotion_status"), "scoped_source_postulate_adoption_only"),
        "gate_e_control_status": (gate_e.get("control_status"), "gate_review_completed"),
        "gate_e_mathematical_status": (gate_e.get("mathematical_status"), "protected_negative_verdict_recorded_positive_closure_missing"),
        "gate_e_physical_status": (gate_e.get("physical_status"), "no_positive_benchmark_closure"),
        "gate_e_promotion_status": (gate_e.get("promotion_status"), "human_gate_required"),
    }
    for name, (observed, expected) in layers.items():
        record(checks, errors, name, observed, expected)

    artifact_checks = {path: (REPO_ROOT / path).is_file() for path in REQUIRED_ARTIFACTS}
    checks["required_artifacts"] = artifact_checks
    errors.extend(f"missing_artifact:{path}" for path, present in artifact_checks.items() if not present)
    return {
        "schema_id": "v21_p16_t02_post_repair_gate_consistency_reaudit_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "result_status": "PASS_P16_T02_GATE_CHAIN_CURRENT_ALIGNMENT" if not errors else "FAIL",
        "audit_disposition": "P16_T02_COMPLETED_NO_PROMOTION" if not errors else "BLOCKED",
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "authority_limits": {"validator_pass_is_science": False, "scientific_status_changed": False, "distance_to_gr_changed": False, "physics_promotion_authorized": False, "proof_authority": False, "publication_external_action_or_push_authorized": False},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.check:
        if not REPORT_PATH.is_file():
            report["errors"].append("stored_report_missing")
        elif json.loads(REPORT_PATH.read_text(encoding="utf-8")) != report:
            report["errors"].append("stored_report_drift")
        report["error_count"] = len(report["errors"])
        report["result_status"] = "PASS_P16_T02_GATE_CHAIN_CURRENT_ALIGNMENT" if not report["errors"] else "FAIL"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["result_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
