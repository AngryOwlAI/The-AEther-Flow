#!/usr/bin/env python3
"""Validate the bounded P16-T02 Gate A-E consistency audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260803-003"
REPORT = TASK / "artifacts/v21_p16_t02_validation.json"

EXPECTED_HASHES = {
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
    "research_control/handoffs/handoff-0944.yaml": "0e35b85993731d9e7ba7a26d58a2038527850017ea5fe0e744dd94720c737d60",
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping: {path}")
    return value


def csv_row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get(key) == value:
                return row
    raise KeyError(f"missing {key}={value} in {path}")


def build_report() -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    hash_failures = []
    for relative, expected in EXPECTED_HASHES.items():
        path = ROOT / relative
        actual = sha256(path) if path.is_file() else "MISSING"
        if actual != expected:
            hash_failures.append(f"{relative}:{actual}")
    add("GATE_SOURCE_HASHES", not hash_failures, "all exact Gate and route source hashes match" if not hash_failures else ";".join(hash_failures))

    authority_map = load_yaml(TASK / "artifacts/v21_p16_t02_authority_path_map.yaml")
    gates = authority_map.get("gates", [])
    gate_ids = [item.get("gate_id") for item in gates if isinstance(item, dict)]
    add("FIVE_GATE_PATHS", gate_ids == ["Gate_A", "Gate_B", "Gate_C", "Gate_D", "Gate_E"], f"gate_ids={gate_ids}")

    map_text = (TASK / "artifacts/v21_p16_t02_authority_path_map.yaml").read_text(encoding="utf-8")
    add("GATE_B_NOT_READY", "NOT_READY_EIGHT_OF_EIGHT_CRITERIA_UNMET" in map_text, "Gate B remains not ready")
    add("GATE_D_NOT_READY", "NOT_READY_EINSTEIN_SECTOR_DERIVATION_REQUIREMENTS_UNMET" in map_text, "Gate D remains not ready")
    add("GATE_E_NOT_READY", "NOT_READY_BENCHMARK_AND_COMPLETED_DERIVATION_REQUIREMENTS_UNMET" in map_text, "Gate E remains not ready")

    gate_c_auth = (ROOT / "research_control/tasks/RT-20260729-001/artifacts/human_authorization_p7_t08_physical_matter_adoption_v1.yaml").read_text(encoding="utf-8")
    required_adoption_tokens = [
        "ADOPTED_AS_CANONICAL_PHYSICAL_MATTER_BY_EXPLICIT_HUMAN_POSTULATE",
        "operational_detector_semantics: true",
        "obstruction_status_after_adoption: \"open_derivational_gap_after_constitutive_adoption\"",
    ]
    add("GATE_C_EXACT_ADOPTION", all(token in gate_c_auth for token in required_adoption_tokens), "protected source-side adoption and open derivational gap are both present")

    ledger_matter = csv_row(ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "matter_coupling")
    ledger_guard = ledger_matter.get("overread_guard", "")
    ledger_physical = ledger_matter.get("physical_status", "")
    add("MATTER_LEDGER_DRIFT_DETECTED", "no_matter_coupling_adoption" in ledger_guard and "not_matter_coupling" in ledger_physical, "current ledger denies the exact source-side adoption without a layer qualifier")

    aliases = (ROOT / "research_control/design/distance_to_gr_status_aliases.yaml").read_text(encoding="utf-8")
    add("MATTER_ALIAS_DRIFT_DETECTED", "no_matter_coupling_adoption" in aliases and "detector-semantics adoption" in aliases, "current alias surface retains stale adoption denials")

    gate_chair = csv_row(ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv", "burden_id", "gate_chair_status")
    add("GATE_E_AUTHORITY_LABEL_DRIFT_DETECTED", gate_chair.get("mathematical_status") == "protected_verdict_missing", "negative protected verdict exists while only future positive closure remains missing")

    tex_gate_a = csv_row(ROOT / "registries/TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V21-P4-T05-ONTOLOGY-REGIME-GATE-CHAIR-DECISION-V1")
    add("GATE_A_REGISTRY_DRIFT_DETECTED", tex_gate_a.get("validation_status") == "PENDING", "current registry row remains PENDING after canonical integration")

    findings = load_yaml(TASK / "artifacts/v21_p16_t02_overread_findings.yaml")
    add("ONE_BLOCKING_FINDING", findings.get("blocking_finding_count") == 1, f"blocking_finding_count={findings.get('blocking_finding_count')}")
    finding_ids = [item.get("finding_id") for item in findings.get("findings", []) if isinstance(item, dict)]
    add("PRIMARY_FINDING_PRESERVED", "P16T02-STATUS-C-GEFF-CUTSET-001" in finding_ids, f"finding_ids={finding_ids}")

    shortcut = authority_map.get("forbidden_shortcut_attempt", {})
    add("FORBIDDEN_SHORTCUT_REJECTED", shortcut.get("attempted") is True and shortcut.get("result") == "rejected_type_error", "strongest forbidden Gate composition rejected")

    certificate = authority_map.get("typed_dependency_certificate", {})
    add("NEW_MATHEMATICAL_PAYLOAD", certificate.get("certificate_id") == "GateChainTypedRefinementCertificate_v1" and certificate.get("payload_kind") == "dependency_map_update_and_cutset_certificate", "typed Gate C cut-set certificate present")

    children = [
        load_yaml(TASK / "artifacts/child_phys_math_p16_t02_gate_consistency.yaml"),
        load_yaml(TASK / "artifacts/child_phys_phil_p16_t02_gate_consistency.yaml"),
    ]
    add("PARALLEL_CHILDREN_COMPLETE", all(child.get("status") == "completed" for child in children), "both required internal perspectives completed")

    conflict = load_yaml(TASK / "artifacts/parent_conflict_review_p16_t02_gate_consistency.yaml")
    add("PARENT_CONFLICT_REVIEW", conflict.get("unresolved_child_conflicts") == [] and conflict.get("final_verdict") == "REPAIR_REQUIRED_STATUS_LAYER_DRIFT", "child differences resolved without hiding the open project-system finding")

    audit_text = (TASK / "artifacts/v21_p16_t02_gate_consistency_audit.md").read_text(encoding="utf-8")
    forbidden = [
        "Role separation is not external human",
        "not a first-principles derivation",
        "may not edit the exact Gate A-E scientific decisions",
        "P16-T02 remains `REPAIR_REQUIRED`",
    ]
    add("CLAIM_BOUNDARY_EXPLICIT", all(token in audit_text for token in forbidden), "audit preserves review derivation repair and closure limits")

    signal = findings.get("project_improvement_signal", {})
    add("BOUNDED_REPAIR_ROUTE", signal.get("signal_id") == "PIS-RT-20260803-003-001" and signal.get("recommended_skill") == "improve-project-system", "one bounded project-system repair selected")

    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v21_p16_t02_validation_report_v1",
        "validator_id": "VAL-V21-P16-T02-GATE-CONSISTENCY-001",
        "task_id": "RT-20260803-003",
        "plan_task_id": "P16-T02",
        "audit_result": "REPAIR_REQUIRED_STATUS_LAYER_DRIFT",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "blocking_scientific_conflict_count": 0,
        "blocking_project_system_finding_count": 1,
        "checks": checks,
        "authority_note": "PASS validates exact detection and routing of the blocking drift; it is not a physics proof, repair completion, Gate promotion, or external-review credential.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.check:
        if not REPORT.is_file():
            raise SystemExit("validation report is missing")
        stored = json.loads(REPORT.read_text(encoding="utf-8"))
        if stored != report:
            raise SystemExit("validation report is stale")
    if args.json or not (args.write_report or args.check):
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
