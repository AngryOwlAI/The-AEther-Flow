#!/usr/bin/env python3
"""Validate the bounded V22 P1-T04 Gate-B-only physics lock packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent
VALIDATION_PATH = ARTIFACTS / "v22_p1_t04_gate_lock_validation.json"
COMPACT_PATH = ARTIFACTS / "v22_p1_t04_compact_receipt.json"
GENERATED_AT = "2026-08-09T04:35:00Z"

PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v22.md"
BACKLOG = ROOT / "research_control/design/v22_recommendation_backlog.yaml"
GATE_B_SOURCE = ROOT / "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml"
P1_T03_SOURCE = ROOT / "research_control/tasks/RT-20260809-003/artifacts/v22_p1_t03_matter_position_no_postulate_gate_policy_v1.tex"
BASELINE = ROOT / "research_control/tasks/RT-20260808-002/artifacts/v21_terminal_baseline_release_manifest_v1.json"

TEX = ARTIFACTS / "v22_p1_t04_gate_b_only_physics_lock_v1.tex"
POLICY = ARTIFACTS / "v22_p1_t04_gate_lock_policy_v1.yaml"
ADMISSION = ARTIFACTS / "v22_p1_t04_physics_admission_matrix_v1.yaml"
PARKED = ARTIFACTS / "v22_p1_t04_parked_route_registry_v1.yaml"
TYPES = ARTIFACTS / "v22_p1_t04_physical_type_checklist_v1.yaml"
HISTORY = ARTIFACTS / "v22_p1_t04_historical_obstruction_index_v1.yaml"
FIXTURES = ARTIFACTS / "fixtures/v22_p1_t04_route_decision_cases.yaml"
CHILD_MATH = ARTIFACTS / "child_phys_math_p1_t04_dependency_lock.yaml"
CHILD_PROCESS = ARTIFACTS / "child_process_integrity_p1_t04_audit.yaml"
CONFLICT = ARTIFACTS / "parent_conflict_review_p1_t04_gate_lock.yaml"
FUSION = ARTIFACTS / "parent_fusion_notes_p1_t04_gate_lock.md"

DIRECT = {
    "gate_b_necessary_condition",
    "gate_b_candidate_construction",
    "gate_b_scoped_obstruction",
    "minimal_source_extension_comparison",
    "gate_b_robustness_or_uniqueness_test",
}
REJECTED = {
    "protected_decision_as_gate_b_evidence",
    "validator_or_checkpoint_as_gate_b_evidence",
    "untyped_physical_label",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} is not a mapping")
    return loaded


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def evaluate_route(case: dict[str, Any]) -> str:
    route_class = case["route_class"]
    if route_class in DIRECT:
        if not case["direct_gate_b_burden_typed"] or not case["physical_type_complete"]:
            return "REJECTED"
        return "ELIGIBLE"
    if route_class in REJECTED:
        return "REJECTED"
    if route_class == "P6-T01":
        return "CONTROL_DEFINITION_ONLY_PHYSICS_PARKED"
    if route_class == "historical_gate_c_p7":
        return "PRESERVED_HISTORICAL_NOT_RERUN"
    return "PARKED" if not case["gate_b_positive"] else "PREREQUISITE_REVIEW_REQUIRED"


def evaluate_type(case: dict[str, Any]) -> str:
    if case["finite_token_only"]:
        return "REJECT_UNTYPED"
    if case["common_witness_count"] == 6 and case["label_specific_complete"]:
        return "TYPED_FOR_REVIEW"
    return "REJECT_UNTYPED"


def build_result() -> tuple[dict[str, Any], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    errors: list[str] = []

    def check(check_id: str, condition: bool, evidence: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "evidence": evidence})
        if not condition:
            errors.append(f"{check_id}: {evidence}")

    required_files = [TEX, POLICY, ADMISSION, PARKED, TYPES, HISTORY, FIXTURES, CHILD_MATH, CHILD_PROCESS, CONFLICT, FUSION]
    for path in required_files:
        check(f"file_exists::{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    plan_text = PLAN.read_text(encoding="utf-8")
    backlog = load_yaml(BACKLOG)
    gate_b = load_yaml(GATE_B_SOURCE)
    policy = load_yaml(POLICY)
    admission = load_yaml(ADMISSION)
    parked = load_yaml(PARKED)
    types = load_yaml(TYPES)
    history = load_yaml(HISTORY)
    fixtures = load_yaml(FIXTURES)
    child_math = load_yaml(CHILD_MATH)
    child_process = load_yaml(CHILD_PROCESS)
    conflict = load_yaml(CONFLICT)
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    tex_text = " ".join(TEX.read_text(encoding="utf-8").split())
    fusion_text = " ".join(FUSION.read_text(encoding="utf-8").split())

    check("plan_hash", sha256(PLAN) == "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65", sha256(PLAN))
    check("plan_gate_b_first", "Make Gate B the sole active physics gate" in plan_text, "P1-T04 directive present")
    check("plan_physical_typing", "physical-typing gate that rejects untyped `clock`, `signal`, `free-fall`," in plan_text, "physical-label directive present")
    items = {item.get("plan_task_id"): item for item in backlog.get("items", [])}
    check("backlog_p1_t04_complete", items.get("P1-T04", {}).get("implementation_status") == "completed_checkpoint_pending", str(items.get("P1-T04", {}).get("implementation_status")))
    check("backlog_p2_t01_routable", items.get("P2-T01", {}).get("worker_skill") == "continue-research" and items.get("P2-T01", {}).get("target_derivation_milestone") == "effective_metric_g_eff", str(items.get("P2-T01", {}).get("worker_skill")))

    check("gate_b_source_hash", sha256(GATE_B_SOURCE) == "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b", sha256(GATE_B_SOURCE))
    check("p1_t03_source_hash", sha256(P1_T03_SOURCE) == "7e2eae747432b1c3931f8edf63012f841cad64863625b0c12839dec8d67817c5", sha256(P1_T03_SOURCE))
    gate_b_matrix = gate_b.get("gate_b_matrix", {})
    check("gate_b_zero_of_eight", gate_b_matrix.get("met_count") == 0 and gate_b_matrix.get("criterion_count") == 8, f"{gate_b_matrix.get('met_count')}/{gate_b_matrix.get('criterion_count')}")
    check("baseline_hash", sha256(BASELINE) == "cd4b3fa94e6b1fe3cd5eb576953d3e918b683e3628c0fe63887d9135281d4043", sha256(BASELINE))
    check("baseline_identity", baseline["baseline"]["commit"] == "233e5dd7024fc068032d0afe86d85dc25e2246e9" and baseline["baseline"]["tree"] == "a7d9c9448de8e204643b093878ba4d84bd58f020", str(baseline["baseline"]))

    check("policy_active_milestone", policy.get("active_derivation_milestone") == "effective_metric_g_eff", str(policy.get("active_derivation_milestone")))
    check("policy_sole_gate", policy.get("sole_active_physics_gate") == "Gate B" and policy.get("active_gate_count", policy["formal_rule"]["active_gate_count"]) == 1, str(policy.get("sole_active_physics_gate")))
    check("policy_direct_class_count", len(policy["directly_admissible_physics_classes"]) == 5, str(len(policy["directly_admissible_physics_classes"])))
    check("policy_direct_class_identity", {x["class_id"] for x in policy["directly_admissible_physics_classes"]} == DIRECT, str(sorted(DIRECT)))
    check("policy_gate_b_criteria", len(policy["gate_b_required_evidence"]) == 8, str(len(policy["gate_b_required_evidence"])))
    check("policy_historical_gate_c", policy["historical_gate_c"]["preserved"] is True and policy["historical_gate_c"]["rerun"] is False and policy["historical_gate_c"]["supplies_gate_b_evidence"] is False, str(policy["historical_gate_c"]))
    check("policy_no_authority", all(value is False for value in policy["authority_limits"].values()), str(policy["authority_limits"]))

    entries = admission["entries"]
    observed_counts = {
        "eligible_count": sum(x["eligibility"] == "ELIGIBLE" for x in entries),
        "parked_count": sum(x["eligibility"] == "PARKED" for x in entries),
        "control_only_physics_parked_count": sum(x["eligibility"] == "CONTROL_DEFINITION_ONLY_PHYSICS_PARKED" for x in entries),
        "rejected_count": sum(x["eligibility"] == "REJECTED" for x in entries),
    }
    check("admission_entry_count", len(entries) == 19, str(len(entries)))
    check("admission_counts", all(admission["summary"][key] == value for key, value in observed_counts.items()), str(observed_counts))
    check("admission_no_bypass", admission["summary"]["downstream_bypass_count"] == 0, str(admission["summary"]))

    parked_entries = {x["route_id"]: x for x in parked["entries"]}
    required_parked = {"new_gate_c", "gate_d", "gate_e", "einstein_route", "benchmark_execution", "P5-T01", "P5-T02", "P5-T03", "P6-T02", "P6-T03"}
    check("parked_registry_routes", required_parked.issubset(parked_entries), str(sorted(parked_entries)))
    check("parked_registry_statuses", all(parked_entries[key]["status"] == "PARKED" and parked_entries[key]["execution_authorized"] is False for key in required_parked), str(sorted(required_parked)))
    check("p6_t01_execution_false", parked_entries["P6-T01"]["status"] == "CONTROL_DEFINITION_ONLY_PHYSICS_PARKED" and parked_entries["P6-T01"]["execution_authorized"] is False, str(parked_entries["P6-T01"]))
    check("historical_gate_c_not_rerun", parked_entries["historical_gate_c_p7"]["status"] == "PRESERVED_HISTORICAL_NOT_RERUN" and parked_entries["historical_gate_c_p7"]["execution_authorized"] is False, str(parked_entries["historical_gate_c_p7"]))

    check("type_common_witness_count", len(types["common_required_witnesses"]) == 6, str(len(types["common_required_witnesses"])))
    check("type_label_set", {x["label"] for x in types["labels"]} == {"clock", "signal", "free-fall", "gravity", "metric", "compact source"}, str([x["label"] for x in types["labels"]]))
    check("type_tokens_fail", all(x["token_alone_is_sufficient"] is False for x in types["labels"]), "all token shortcuts false")

    task_roots = history["preservation_scope"]["task_roots"]
    task_prefixes = {x["task_id"]: f"research_control/tasks/{x['task_id']}/" for x in task_roots}
    inventory = baseline["repository_archive_inventory"]
    selected = [entry for entry in inventory if any(entry["path"].startswith(prefix) for prefix in task_prefixes.values())]
    check("history_task_root_count", len(task_roots) == 16 and len(task_prefixes) == 16, str(len(task_roots)))
    check("history_entry_count", len(selected) == 66, str(len(selected)))
    history_failures: list[dict[str, str]] = []
    for root_spec in task_roots:
        prefix = task_prefixes[root_spec["task_id"]]
        count = sum(entry["path"].startswith(prefix) for entry in selected)
        check(f"history_root_count::{root_spec['plan_task_id']}", count == root_spec["expected_archive_entries"], str(count))
    for entry in selected:
        live_path = ROOT / entry["path"]
        if not live_path.is_file():
            history_failures.append({"path": entry["path"], "error": "missing"})
        elif sha256(live_path) != entry["sha256"]:
            history_failures.append({"path": entry["path"], "error": "hash_mismatch"})
    check("history_all_live_hashes", not history_failures, json.dumps(history_failures, sort_keys=True))
    snapshot = history["scientific_status_snapshot"]
    check("history_negative_status", snapshot["Gate_D"] == "NOT_READY" and snapshot["Gate_E"] == "NOT_READY" and snapshot["benchmark_inconclusive_count"] == 6 and snapshot["benchmark_pass_count"] == 0 and snapshot["independent_replication_count"] == 0, str(snapshot))

    route_failures = []
    for case in fixtures["cases"]:
        observed = evaluate_route(case)
        if observed != case["expected"]:
            route_failures.append({"case_id": case["case_id"], "expected": case["expected"], "observed": observed})
    type_failures = []
    for case in fixtures["physical_type_cases"]:
        observed = evaluate_type(case)
        if observed != case["expected"]:
            type_failures.append({"case_id": case["case_id"], "expected": case["expected"], "observed": observed})
    check("route_fixture_count", len(fixtures["cases"]) == 19, str(len(fixtures["cases"])))
    check("route_fixture_results", not route_failures, json.dumps(route_failures, sort_keys=True))
    check("type_fixture_count", len(fixtures["physical_type_cases"]) == 6, str(len(fixtures["physical_type_cases"])))
    check("type_fixture_results", not type_failures, json.dumps(type_failures, sort_keys=True))

    required_tex_phrases = [
        "Gate B is the sole active physics gate",
        "Gate-lock dependency-closure theorem",
        "Finite-token physical-typing lemma",
        "Historical projection and nonpromotion theorem",
        "all 66 live paths and hashes",
        "P6-T01 may define a protocol early only as a nonexecuting control artifact",
        "selection is not execution",
    ]
    check("tex_required_claims", all(phrase.lower() in tex_text.lower() for phrase in required_tex_phrases), str(required_tex_phrases))
    check("tex_no_global_no_go", "not a proof that Gate B can never be passed" in tex_text, "same-milestone continuation remains open")
    check("tex_no_gate_verdict", "not a positive Gate B verdict" in tex_text, "non-verdict status present")

    check("child_math_complete", child_math.get("status") == "completed" and child_math.get("external_review") is False and len(child_math.get("new_mathematical_payload", [])) == 3, str(child_math.get("status")))
    check("child_process_complete", child_process.get("status") == "completed" and child_process.get("blocking_finding_count") == 0 and child_process.get("external_review") is False, str(child_process.get("status")))
    check("conflicts_resolved", conflict.get("status") == "resolved" and conflict.get("blocking_conflict_count") == 0 and len(conflict.get("conflicts", [])) == 4, str(conflict.get("status")))
    check("fusion_authority_boundary", "not external review or independent replication" in fusion_text and "no Distance-to-GR delta" in fusion_text, "internal-only and no-distance-delta language present")

    artifact_paths = required_files + [Path(__file__).resolve()]
    artifact_hashes = {str(path.relative_to(ROOT)): sha256(path) for path in artifact_paths}
    status = "PASS" if not errors else "FAIL"
    result = {
        "schema_id": "v22_p1_t04_gate_lock_validation_v1",
        "task_id": "RT-20260809-004",
        "job_id": "AJ-RT-20260809-004-001",
        "generated_at": GENERATED_AT,
        "status": status,
        "check_count": len(checks),
        "failure_count": len(errors),
        "route_fixture_count": len(fixtures["cases"]),
        "route_fixture_failure_count": len(route_failures),
        "physical_type_fixture_count": len(fixtures["physical_type_cases"]),
        "physical_type_fixture_failure_count": len(type_failures),
        "historical_archive_entry_count": len(selected),
        "historical_archive_failure_count": len(history_failures),
        "checks": checks,
        "errors": errors,
        "route_fixture_failures": route_failures,
        "physical_type_fixture_failures": type_failures,
        "historical_archive_failures": history_failures,
        "artifact_hashes": artifact_hashes,
        "authority_limits": {
            "validator_pass_counts_as_physics": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "gate_verdict_authorized": False,
            "physics_promotion_authorized": False,
        },
    }
    validation_digest = hashlib.sha256(json_bytes(result)).hexdigest()
    compact = {
        "schema_id": "compact_validation_receipt_v1",
        "gate_id": "V22-P1-T04-FOCUSED-GATE-LOCK-VALIDATION",
        "task_id": "RT-20260809-004",
        "job_id": "AJ-RT-20260809-004-001",
        "status": status,
        "receipt_path": str(VALIDATION_PATH.relative_to(ROOT)),
        "content_hash": f"sha256:{validation_digest}",
        "counts": {"error_count": len(errors), "warning_count": 0, "finding_count": len(errors)},
        "relevant_finding_ids": [error.split(":", 1)[0] for error in errors],
        "summary": f"{len(checks) - len(errors)}/{len(checks)} focused checks, {len(fixtures['cases']) - len(route_failures)}/{len(fixtures['cases'])} route fixtures, {len(fixtures['physical_type_cases']) - len(type_failures)}/{len(fixtures['physical_type_cases'])} type fixtures, and {len(selected) - len(history_failures)}/{len(selected)} historical archive hashes pass.",
        "authority_note": "This operational receipt is not source authority, a Gate verdict, scientific truth, or physics promotion.",
    }
    return result, compact


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result, compact = build_result()
    if args.write:
        VALIDATION_PATH.write_bytes(json_bytes(result))
        COMPACT_PATH.write_bytes(json_bytes(compact))
    else:
        if not VALIDATION_PATH.exists() or VALIDATION_PATH.read_bytes() != json_bytes(result):
            result["status"] = "FAIL"
            result["errors"].append("validation_output_freshness: tracked validation output differs from deterministic result")
            result["failure_count"] += 1
        if not COMPACT_PATH.exists() or COMPACT_PATH.read_bytes() != json_bytes(compact):
            result["status"] = "FAIL"
            result["errors"].append("compact_output_freshness: tracked compact receipt differs from deterministic result")
            result["failure_count"] += 1

    if args.json:
        print(json.dumps({
            "status": result["status"],
            "check_count": result["check_count"],
            "failure_count": result["failure_count"],
            "route_fixture_count": result["route_fixture_count"],
            "route_fixture_failure_count": result["route_fixture_failure_count"],
            "physical_type_fixture_count": result["physical_type_fixture_count"],
            "physical_type_fixture_failure_count": result["physical_type_fixture_failure_count"],
            "historical_archive_entry_count": result["historical_archive_entry_count"],
            "historical_archive_failure_count": result["historical_archive_failure_count"],
            "receipt_path": str(VALIDATION_PATH.relative_to(ROOT)),
            "compact_receipt_path": str(COMPACT_PATH.relative_to(ROOT)),
            "errors": result["errors"],
        }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
