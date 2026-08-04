#!/usr/bin/env python3
"""Validate the bounded V21 P16-T05 final status synthesis."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = REPO_ROOT / "research_control/tasks/RT-20260804-003"
ARTIFACT_DIR = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACT_DIR / "v21_p16_t05_validation.json"
RESULT_STATUS = "PASS_P16_T05_FINAL_STATUS_SYNTHESIS_CALIBRATED"

EXPECTED_SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/tasks/RT-20260803-002/artifacts/v21_recommendation_coverage_audit.md": "653f8205a160cf7d94ac5a462590cb88284566f3bee6454a606f28edd8d9eab0",
    "research_control/tasks/RT-20260803-012/artifacts/v21_p16_t02_post_repair_gate_consistency_reaudit.md": "a8afd3cecf381198e018f9b9c0f03891f95435bc5edea4fe1a7f74d392735ae5",
    "research_control/tasks/RT-20260803-013/artifacts/v21_p16_t03_final_provenance_audit.md": "72316ad40fdab3b5d88c88602c1832de99045616421eba244143e436ec87ca59",
    "research_control/tasks/RT-20260804-001/artifacts/v21_p16_t04_post_repair_final_reaudit_report.md": "20bbc6082b3b55fad3a7401dc4e4b84295c2baa376f9a2f3ea03286f17da0d30",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
    "research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex": "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml": "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex": "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex": "035ea88a612d861a00d0703ec2bd1094e01194c113d7ff2588e3a4ad8bf47d63",
    "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex": "7f28103e40664f0a004af0134f3216932136f8efb160f0c7c59039efa5225b0b",
}

ARTIFACT_PATHS = {
    "synthesis": "research_control/tasks/RT-20260804-003/artifacts/v21_p16_t05_final_status_synthesis.md",
    "science_scorecard": "research_control/tasks/RT-20260804-003/artifacts/v21_p16_t05_science_scorecard.yaml",
    "system_scorecard": "research_control/tasks/RT-20260804-003/artifacts/v21_p16_t05_system_scorecard.yaml",
    "child_phys_math": "research_control/tasks/RT-20260804-003/artifacts/child_phys_math_p16_t05_final_status_synthesis.yaml",
    "child_phys_phil": "research_control/tasks/RT-20260804-003/artifacts/child_phys_phil_p16_t05_final_status_synthesis.yaml",
    "conflict_review": "research_control/tasks/RT-20260804-003/artifacts/parent_conflict_review_p16_t05_final_status_synthesis.yaml",
    "fusion_notes": "research_control/tasks/RT-20260804-003/artifacts/parent_fusion_notes_p16_t05_final_status_synthesis.md",
    "validator": "research_control/tasks/RT-20260804-003/artifacts/validate_p16_t05_final_status_synthesis.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def nested(value: dict[str, Any], *keys: str) -> Any:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    for rel_path, expected in EXPECTED_SOURCE_HASHES.items():
        path = REPO_ROOT / rel_path
        actual = sha256(path) if path.is_file() else "missing"
        add(f"SOURCE_HASH::{rel_path}", actual == expected, f"expected={expected}; actual={actual}")

    task = load_yaml(TASK_DIR / "00_TASK.yaml")
    job = load_yaml(TASK_DIR / "jobs/AJ-RT-20260804-003-001.yaml")
    completion = load_yaml(TASK_DIR / "jobs/completions/AJC-AJ-RT-20260804-003-001.yaml")
    science = load_yaml(ARTIFACT_DIR / "v21_p16_t05_science_scorecard.yaml")
    system = load_yaml(ARTIFACT_DIR / "v21_p16_t05_system_scorecard.yaml")
    child_math = load_yaml(ARTIFACT_DIR / "child_phys_math_p16_t05_final_status_synthesis.yaml")
    child_phil = load_yaml(ARTIFACT_DIR / "child_phys_phil_p16_t05_final_status_synthesis.yaml")
    conflict = load_yaml(ARTIFACT_DIR / "parent_conflict_review_p16_t05_final_status_synthesis.yaml")
    handoff = load_yaml(REPO_ROOT / "research_control/handoffs/handoff-0964.yaml")
    program = load_yaml(REPO_ROOT / "research_control/program_state.yaml")
    receipt = load_json(ARTIFACT_DIR / "v21_p16_t05_compact_receipt.json")
    synthesis = (ARTIFACT_DIR / "v21_p16_t05_final_status_synthesis.md").read_text(encoding="utf-8")
    fusion = (ARTIFACT_DIR / "parent_fusion_notes_p16_t05_final_status_synthesis.md").read_text(encoding="utf-8")

    add("TASK_FINAL", task.get("status") == "completed" and task.get("validation_status") == "PASS_PRECHECKPOINT", "task is completed and precheckpoint-valid")
    add("JOB_FINAL", job.get("status") == "completed" and job.get("validation_status") == "PASS_PRECHECKPOINT", "job is completed and precheckpoint-valid")
    add("COMPLETION_RESULT", completion.get("status") == "completed" and nested(completion, "implementation_plan_receipt", "result_status") == RESULT_STATUS, "completion records the exact P16-T05 result")
    add("SCIENCE_VERDICT", nested(science, "answer_first", "first_principles_gr_derivation_status") == "OPEN_NOT_COMPLETED", "first-principles derivation remains open")
    add("BENCHMARK_COUNTS", nested(science, "answer_first", "benchmark_case_count") == 6 and nested(science, "answer_first", "benchmark_pass_count") == 0 and nested(science, "answer_first", "independent_replication_count") == 0, "six cases, zero passes, zero qualifying replications")
    gate_status = science.get("gate_status", {})
    add("GATE_STATUS", nested(gate_status, "Gate_B", "status") == "NOT_READY" and nested(gate_status, "Gate_D", "status") == "NOT_READY" and nested(gate_status, "Gate_E", "status") == "NOT_READY", "Gates B, D, and E remain NOT_READY")
    add("DISTANCE_UNCHANGED", nested(science, "distance_to_gr_status", "ledger_changed_by_task") is False and nested(science, "authority_limits", "distance_to_gr_changed") is False, "no Distance-to-GR change")
    statement = str(nested(science, "new_mathematical_payload", "statement") or "")
    scope = str(nested(science, "new_mathematical_payload", "scope") or "")
    add("CLOSURE_NONENTAILMENT", "reflexive-transitive closure" in statement and "empty intersection" in statement and "non-derivability" in scope, "formal payload uses closure non-membership rather than external falsity")
    add("SYSTEM_COVERAGE", nested(system, "dimensions", "recommendation_coverage", "recommendation_count") == 72 and nested(system, "dimensions", "recommendation_coverage", "missing_recommendation_count") == 0, "all 72 recommendations have qualifying coverage")
    add("SYSTEM_NOT_PHYSICS", nested(system, "dual_budget_result", "system_success_counts_as_physics") is False and nested(system, "dual_budget_result", "system_success_counts_as_distance_to_gr") is False, "system success supplies no physics or Distance credit")
    add("CHILDREN_COMPLETE", child_math.get("status") == "completed" and child_phil.get("status") == "completed" and nested(child_math, "verification", "files_changed_by_child") == [] and nested(child_phil, "verification", "files_changed_by_child") == [], "both read-only child perspectives completed without edits")
    add("CONFLICT_RESOLVED", conflict.get("status") == "resolved" and conflict.get("blocking_conflict_count") == 0 and conflict.get("unresolved_conflicts") == [], "parent conflict review resolved without blocking conflict")
    add("FUSION_RESULT", RESULT_STATUS in fusion and "P16-T06" in fusion, "fusion records exact result and successor exclusion")
    required_phrases = ["first-principles derivation", "zero passes", "separate research-system status", "reflexive-transitive closure", "p16-t06"]
    synthesis_lower = synthesis.lower()
    add("SYNTHESIS_CONTENT", all(phrase in synthesis_lower for phrase in required_phrases), "answer-first synthesis contains the required scientific and route boundaries")
    add("HANDOFF_ROUTE", handoff.get("plan_task_id") == "P16-T06" and nested(handoff, "selected_next_route", "worker_skill") == "continue-research" and nested(handoff, "selected_next_route", "executed") is False, "handoff selects but does not execute P16-T06")
    add("PROGRAM_ROUTE", program.get("active_task_id") == "RT-20260804-003" and program.get("next_plan_task_id") == "P16-T06" and program.get("next_worker_skill") == "continue-research", "program state routes P16-T06")
    add("AUTHORITY_LIMITS", all(nested(completion, "authorization_layers", key) is False for key in ["push_authorized", "external_publication_authorized", "public_release_authorized", "benchmark_promotion_authorized", "completed_derivation_authorized"]), "completion preserves all protected and outward-action limits")

    receipt_hashes = receipt.get("artifact_hashes", {})
    artifact_hash_ok = True
    for key, rel_path in ARTIFACT_PATHS.items():
        actual = sha256(REPO_ROOT / rel_path)
        if receipt_hashes.get(key) != actual:
            artifact_hash_ok = False
    add("COMPACT_RECEIPT_HASHES", artifact_hash_ok, "compact receipt binds every primary task-local artifact")
    add("COMPACT_RECEIPT_STATUS", receipt.get("result_status") == RESULT_STATUS and receipt.get("p16_t06_executed") is False and receipt.get("physics_promotion_authorized") is False, "compact receipt preserves result and authority")

    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    report_status = "PASS" if pass_count == len(checks) else "FAIL"
    return {
        "schema_id": "v21_p16_t05_final_status_validation_v1",
        "task_id": "RT-20260804-003",
        "job_id": "AJ-RT-20260804-003-001",
        "result_status": RESULT_STATUS,
        "status": report_status,
        "check_count": len(checks),
        "pass_count": pass_count,
        "fail_count": len(checks) - pass_count,
        "checks": checks,
        "authority_limits": {
            "validator_pass_is_scientific_proof": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
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
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        if not REPORT_PATH.is_file():
            report["status"] = "FAIL"
            report["report_error"] = "validation report is missing"
        else:
            saved = load_json(REPORT_PATH)
            if saved != report:
                report["status"] = "FAIL"
                report["report_error"] = "saved validation report differs from live recomputation"

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
