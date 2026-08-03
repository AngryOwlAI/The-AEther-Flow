#!/usr/bin/env python3
"""Validate the bounded RT-20260803-005 Gate status-layer repair."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260803-005"
JOB_ID = "AJ-RT-20260803-005-001"
REPORT_PATH = Path(
    "research_control/tasks/RT-20260803-005/artifacts/"
    "p16_t02_gate_status_layer_contract_validation.json"
)

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
    "research_control/tasks/RT-20260803-003/artifacts/v21_p16_t02_gate_consistency_audit.md": "5daa24b57b805af51633f85e176b8da5699aaca8000794f57eb5ff4a3ddfde8c",
    "research_control/tasks/RT-20260803-003/artifacts/v21_p16_t02_overread_findings.yaml": "f4f434fb0a8b0cd90809eb5cf40df9f8ac57d7aab1605b94dc79e914ab0dc08c",
    "research_control/tasks/RT-20260803-003/artifacts/v21_p16_t02_authority_path_map.yaml": "c74551dd8fe9cfc64f5a66e410813fc0f16fe55c26723a42c098444ea913df3e",
    "research_control/tasks/RT-20260803-003/artifacts/v21_p16_t02_validation.json": "d12496fb50fc6b153c3349e87a1c352cd7641c31e139eddeb3c9cfc9dad3b758",
}

EXPECTED_MATTER_LAYERS = {
    "control_status": "gate_review_completed",
    "mathematical_status": "parameterized_finite_local_witness_precondition",
    "physical_status": "not_target_matter_coupling_source_side_postulate_adoption_only",
    "promotion_status": "scoped_source_postulate_adoption_only",
}
EXPECTED_MATTER_GUARDS = {
    "no_source_law_adoption",
    "no_metricdata_e_adoption",
    "no_geff_scope_expansion",
    "no_unscoped_or_target_coupling_law_adoption",
    "no_matter_coupling_derivation",
    "no_target_matter_coupling_adoption",
    "no_target_stress_energy_semantics",
    "no_target_stress_energy_tensor",
    "no_target_matter_action",
    "no_target_detector_semantics",
    "no_einstein_equations",
    "no_benchmark_promotion",
    "no_completed_derivation",
}
FORBIDDEN_UNQUALIFIED_MATTER_GUARDS = {
    "no_coupling_law_adoption",
    "no_matter_coupling_adoption",
    "no_stress_energy_semantics",
    "no_stress_energy_tensor",
    "no_matter_action",
    "no_detector_semantics",
}
EXPECTED_GATE_E_LAYERS = {
    "control_status": "gate_review_completed",
    "mathematical_status": "protected_negative_verdict_recorded_positive_closure_missing",
    "physical_status": "no_positive_benchmark_closure",
    "promotion_status": "human_gate_required",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(relative_path: str) -> dict[str, Any]:
    value = yaml.safe_load((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative_path} is not a YAML mapping")
    return value


def csv_row(relative_path: str, key: str, value: str) -> dict[str, str]:
    with (REPO_ROOT / relative_path).open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get(key) == value]
    if len(rows) != 1:
        raise ValueError(f"{relative_path} has {len(rows)} rows for {key}={value}")
    return rows[0]


def expect_equal(
    errors: list[str], checks: dict[str, Any], check_id: str, observed: Any, expected: Any
) -> None:
    checks[check_id] = {"expected": expected, "observed": observed, "match": observed == expected}
    if observed != expected:
        errors.append(f"{check_id}_mismatch")


def build_report() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, Any] = {}

    protected_results: dict[str, dict[str, Any]] = {}
    for relative_path, expected_hash in PROTECTED_HASHES.items():
        path = REPO_ROOT / relative_path
        observed_hash = sha256(path) if path.is_file() else None
        protected_results[relative_path] = {
            "expected_sha256": expected_hash,
            "observed_sha256": observed_hash,
            "match": observed_hash == expected_hash,
        }
        if observed_hash != expected_hash:
            errors.append(f"protected_hash_mismatch:{relative_path}")
    checks["protected_hashes"] = protected_results

    matter = csv_row("registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "matter_coupling")
    for field_name, expected in EXPECTED_MATTER_LAYERS.items():
        expect_equal(errors, checks, f"matter_{field_name}", matter.get(field_name), expected)
    matter_guards = {item for item in matter.get("overread_guard", "").split(";") if item}
    missing_matter_guards = sorted(EXPECTED_MATTER_GUARDS - matter_guards)
    stale_matter_guards = sorted(FORBIDDEN_UNQUALIFIED_MATTER_GUARDS & matter_guards)
    checks["matter_guard_contract"] = {
        "missing_required": missing_matter_guards,
        "stale_unqualified": stale_matter_guards,
    }
    if missing_matter_guards:
        errors.append("matter_required_guards_missing")
    if stale_matter_guards:
        errors.append("matter_unqualified_guards_present")

    gate_e = csv_row("registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "gate_chair_status")
    for field_name, expected in EXPECTED_GATE_E_LAYERS.items():
        expect_equal(errors, checks, f"gate_e_{field_name}", gate_e.get(field_name), expected)
    expect_equal(
        errors,
        checks,
        "gate_e_negative_verdict_authority_path",
        gate_e.get("last_evidence_path"),
        "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex",
    )

    tex_row = csv_row(
        "registries/TEX_SOURCE_REGISTRY.csv",
        "object_id",
        "TEX-ONTOLOGY-AETHER-FLOW-FOUNDATIONS",
    )
    expect_equal(errors, checks, "gate_a_tex_current_validation", tex_row.get("validation_status"), "PASS")
    expect_equal(
        errors,
        checks,
        "gate_a_tex_history_timestamp",
        tex_row.get("last_validated_at"),
        "2026-07-27T03:04:15Z",
    )

    aliases = load_yaml("research_control/design/distance_to_gr_status_aliases.yaml")
    alias_rows = aliases.get("row_aliases", {})
    matter_alias = alias_rows.get("matter_coupling", {}) if isinstance(alias_rows, dict) else {}
    gate_e_alias = alias_rows.get("gate_chair_status", {}) if isinstance(alias_rows, dict) else {}
    expect_equal(
        errors,
        checks,
        "matter_alias_positive_term",
        matter_alias.get("scoped_positive_term"),
        "protected_source_matter_postulate_adoption_derivational_gap_open",
    )
    expect_equal(
        errors,
        checks,
        "gate_e_alias_positive_term",
        gate_e_alias.get("scoped_positive_term"),
        "protected_negative_verdict_recorded_future_positive_closure_human_gated",
    )

    v1 = load_yaml("research_control/design/accepted_status_calibration_v1.yaml")
    v1_matter = v1.get("accepted_status_calibration_v1", {}).get("high_risk_objects", {}).get("matter_coupling", {})
    v2 = load_yaml("research_control/design/accepted_status_calibration_v2.yaml")
    v2_matter = v2.get("accepted_status_calibration_v2", {}).get("high_risk_objects", {}).get("matter_coupling", {}).get("status_card_v2", {})
    for check_id, text in {
        "v1_positive_status": v1_matter.get("positive_status_sentence", ""),
        "v2_positive_status": v2_matter.get("positive_status", ""),
        "v2_public_summary": v2_matter.get("public_summary", ""),
    }.items():
        has_adoption = "adopt" in str(text).lower() and "p7" in str(text).lower()
        checks[check_id] = {"observed": text, "source_adoption_explicit": has_adoption}
        if not has_adoption:
            errors.append(f"{check_id}_missing_source_adoption")
    v2_blob = json.dumps(v2_matter, sort_keys=True).lower()
    checks["v2_open_derivational_boundary"] = {
        "mentions_g_eff": "g_eff" in v2_blob,
        "blocks_derivation": "matter-coupling derivation" in v2_blob,
    }
    if "g_eff" not in v2_blob or "matter-coupling derivation" not in v2_blob:
        errors.append("v2_open_derivational_boundary_missing")

    generated_surfaces = {
        "research_control/current_frontier.md": (
            "P7SourceMatterPackage_v1",
            "not_target_matter_coupling_source_side_postulate_adoption_only",
            "protected_negative_verdict_recorded_positive_closure_missing",
        ),
        "output/compact_current_frontier_v16.json": (
            "P7SourceMatterPackage_v1",
            "scoped_source_postulate_adoption_only",
            "no_positive_benchmark_closure",
        ),
    }
    for relative_path, required_terms in generated_surfaces.items():
        path = REPO_ROOT / relative_path
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        missing = [term for term in required_terms if term not in text]
        checks[f"generated_surface:{relative_path}"] = {"required_terms": list(required_terms), "missing": missing}
        if missing:
            errors.append(f"generated_surface_missing_terms:{relative_path}")

    return {
        "schema_id": "p16_t02_gate_status_layer_contract_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "checks": checks,
        "errors": errors,
        "error_count": len(errors),
        "validation_status": "PASS" if not errors else "FAIL",
        "authority_limits": {
            "canonical_science_modified": False,
            "scientific_status_changed": False,
            "distance_to_gr_scientific_delta": False,
            "matter_coupling_derived": False,
            "target_matter_coupling_adopted": False,
            "gate_e_verdict_changed": False,
            "benchmark_promotion_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_external_action_or_push_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    destination = REPO_ROOT / REPORT_PATH
    if args.write_report:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        if not destination.is_file():
            report["errors"].append("stored_report_missing")
        else:
            stored = json.loads(destination.read_text(encoding="utf-8"))
            if stored != report:
                report["errors"].append("stored_report_drift")
        report["error_count"] = len(report["errors"])
        report["validation_status"] = "PASS" if not report["errors"] else "FAIL"
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
