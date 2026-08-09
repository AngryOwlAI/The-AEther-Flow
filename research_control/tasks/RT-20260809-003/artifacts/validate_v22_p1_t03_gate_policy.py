#!/usr/bin/env python3
"""Validate the bounded V22 P1-T03 Position A and no-postulate packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent
VALIDATION_PATH = ARTIFACTS / "v22_p1_t03_gate_policy_validation.json"
COMPACT_PATH = ARTIFACTS / "v22_p1_t03_compact_receipt.json"
GENERATED_AT = "2026-08-09T03:30:17Z"

PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v22.md"
BACKLOG = ROOT / "research_control/design/v22_recommendation_backlog.yaml"
P7_DECISION = ROOT / "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex"
P7_LEDGER = ROOT / "research_control/tasks/RT-20260729-001/artifacts/p7_t08_constitutive_postulate_ledger_v1.yaml"
P7_AUDIT = ROOT / "research_control/tasks/RT-20260728-006/artifacts/matter_package_smuggling_audit_v1.tex"

TEX = ARTIFACTS / "v22_p1_t03_matter_position_no_postulate_gate_policy_v1.tex"
CONTRACT = ARTIFACTS / "v22_p1_t03_p7_conditional_input_contract_v1.yaml"
POSITION_B = ARTIFACTS / "v22_p1_t03_position_b_reopening_criteria_v1.yaml"
POLICY = ARTIFACTS / "v22_p1_t03_no_postulate_gate_policy_v1.yaml"
FIXTURES = ARTIFACTS / "fixtures/v22_p1_t03_gate_decision_cases.yaml"
CHILD_MATH = ARTIFACTS / "child_phys_math_p1_t03_gate_invariance.yaml"
CHILD_PHIL = ARTIFACTS / "child_phys_phil_p1_t03_authority_audit.yaml"
CONFLICT = ARTIFACTS / "parent_conflict_review_p1_t03_gate_policy.yaml"
FUSION = ARTIFACTS / "parent_fusion_notes_p1_t03_gate_policy.md"

EXPECTED_SOURCE_HASHES = {
    "TEX-V21-P7-T01-SOURCE-MATTER-ONTOLOGY-SECTOR-TAXONOMY-V1": (
        "research_control/tasks/RT-20260727-007/artifacts/source_matter_ontology_and_sector_taxonomy_v1.tex",
        "8d160217bf223078a11bc63fde6593c11c39d5b50d9c48fbad7b12084f8a752d",
    ),
    "TEX-V21-P7-T02-SOURCE-MATTER-FINITE-TRANSITION-KERNEL-V1": (
        "research_control/tasks/RT-20260728-001/artifacts/source_matter_finite_transition_kernel_candidate_v1.tex",
        "65ac095f5cdf4c2e319365c8b0e024d031b19d9fc2b8102e59997afa1e8f9129",
    ),
    "TEX-V21-P7-T03-SOURCE-OPERATIONAL-DEVICE-SUITE-V1": (
        "research_control/tasks/RT-20260728-002/artifacts/source_operational_device_suite_candidate_v1.tex",
        "d6c818ee29f1a7e659e2f454aec21431d680b3d2d4df048fcf36f4aba87ba22a",
    ),
    "TEX-V21-P7-T04-COMMON-SOURCE-PROPAGATION-PROFILE-V1": (
        "research_control/tasks/RT-20260728-003/artifacts/common_source_propagation_profile_candidate_v1.tex",
        "87014253023cdb8945ed67f606355d762486884ce3a6de4fa2d32e2af32e2b43",
    ),
    "TEX-V21-P7-T05-UNIVERSAL-SOURCE-COUPLING-MAP-V1": (
        "research_control/tasks/RT-20260728-004/artifacts/universal_source_coupling_map_candidate_v1.tex",
        "5a9a8f5542a7c8b714bbff7ec06c06449b0c66c0196266051562caf9ce602c6b",
    ),
    "TEX-V21-P7-T06-SOURCE-KERNEL-VARIATIONAL-OBJECT-V1": (
        "research_control/tasks/RT-20260728-005/artifacts/source_kernel_variational_object_candidate_v1.tex",
        "386769e40167c35604625ef7250c027dc1712c82db4790e2895e0b31ac3cfbf7",
    ),
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


def evaluate_fixture(case: dict[str, Any]) -> str:
    evidence = case["evidence"]
    if evidence["disqualifying_failure"]:
        return "CANDIDATE_INSUFFICIENT"
    if evidence["established"] == evidence["required_total"]:
        return "POSITIVE"
    return "NOT_READY"


def build_result() -> tuple[dict[str, Any], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    errors: list[str] = []

    def check(check_id: str, condition: bool, evidence: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "evidence": evidence})
        if not condition:
            errors.append(f"{check_id}: {evidence}")

    required_files = [TEX, CONTRACT, POSITION_B, POLICY, FIXTURES, CHILD_MATH, CHILD_PHIL, CONFLICT, FUSION]
    for path in required_files:
        check(f"file_exists::{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    plan_text = PLAN.read_text(encoding="utf-8")
    backlog = load_yaml(BACKLOG)
    p7_ledger = load_yaml(P7_LEDGER)
    tex_text = TEX.read_text(encoding="utf-8")
    contract = load_yaml(CONTRACT)
    position_b = load_yaml(POSITION_B)
    policy = load_yaml(POLICY)
    fixtures = load_yaml(FIXTURES)
    child_math = load_yaml(CHILD_MATH)
    child_phil = load_yaml(CHILD_PHIL)
    conflict = load_yaml(CONFLICT)
    fusion_text = FUSION.read_text(encoding="utf-8")
    normalized_tex = " ".join(tex_text.split())
    normalized_fusion = " ".join(fusion_text.split())

    check("plan_hash", sha256(PLAN) == "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65", sha256(PLAN))
    check("plan_position_a", "Adopt Position A for the next cycle" in plan_text, "V22-R09 Position A directive present")
    check("plan_no_postulate", "do not allow it to change evidential truth values" in plan_text, "V22-R14 truth-value rule present")
    check("backlog_p1_t03", any(x.get("plan_task_id") == "P1-T03" for x in backlog.get("items", [])), "P1-T03 backlog row present")

    check("p7_decision_hash", sha256(P7_DECISION) == "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827", sha256(P7_DECISION))
    check("p7_ledger_hash", sha256(P7_LEDGER) == "e11f5e4ae886932cad618caa3ee97e973bbd38d363db25776fe1fbd2c27451dc", sha256(P7_LEDGER))
    check("p7_audit_hash", sha256(P7_AUDIT) == "f6e0b456dcef8ec4285d6293c76ccc6c6fbe04095e3f0d17023565ee9337187c", sha256(P7_AUDIT))
    check("p7_postulate_count", len(p7_ledger.get("postulates", [])) == 8, str(len(p7_ledger.get("postulates", []))))

    members = contract["source_package"]["package_members"]
    check("contract_member_count", len(members) == 6, str(len(members)))
    member_map = {item["object_id"]: item for item in members}
    for object_id, (rel_path, expected_hash) in EXPECTED_SOURCE_HASHES.items():
        member = member_map.get(object_id, {})
        check(f"contract_member::{object_id}", member.get("path") == rel_path and member.get("sha256") == expected_hash, rel_path)
        check(f"live_source_hash::{object_id}", sha256(ROOT / rel_path) == expected_hash, expected_hash)

    check("contract_position_a", contract.get("position") == "A" and contract.get("decision") == "fixed_matter_theory_is_conditional_input_to_geometry_reconstruction", str(contract.get("decision")))
    check("contract_adopted_meaning_count", len(contract["source_package"]["adopted_meanings"]) == 8, str(len(contract["source_package"]["adopted_meanings"])))
    check("contract_open_obstruction", contract["open_obstruction"] == {"obstruction_id": "OBST-P7T07-CROSS-LAYER-COMPOSITION-GAP-001", "status": "open_derivational_gap_after_constitutive_adoption", "changed_by_p1_t03": False}, str(contract["open_obstruction"]))
    required_exclusions = {"realistic continuum matter", "Standard Model sectors", "quantum statistics", "Hilbert or algebraic state structure", "microcausality", "target stress tensor T_mu_nu", "derived universal target coupling", "g_eff", "Einstein equations", "Gate B or Gate D evidence"}
    check("contract_exclusions", required_exclusions.issubset(set(contract["excluded_outputs"])), str(sorted(required_exclusions)))
    check("contract_no_target_constructor", contract["typed_interface"]["source_to_target_constructor_present"] is False, str(contract["typed_interface"]))
    check("contract_authority_false", all(value is False for value in contract["authority_limits"].values()), str(contract["authority_limits"]))

    check("position_b_not_open", position_b.get("position_b_status") == "not_open", str(position_b.get("position_b_status")))
    check("position_b_predicate_count", len(position_b["program_opening_predicates"]) == 6, str(len(position_b["program_opening_predicates"])))
    check("position_b_obligation_count", len(position_b["required_research_obligations"]) >= 8, str(len(position_b["required_research_obligations"])))
    check("position_b_all_required", position_b.get("all_required") is True and position_b["reopening_evaluator"]["missing_predicate_result"] == "NOT_OPEN", str(position_b["reopening_evaluator"]))
    check("position_b_no_truth_override", position_b["reopening_evaluator"]["protected_selection_may_change_truth_values"] is False, str(position_b["reopening_evaluator"]))

    check("policy_gate_scope", policy.get("applies_to") == ["Gate B", "Gate D"], str(policy.get("applies_to")))
    check("policy_b_count", len(policy["gate_b_required_evidence"]) == 8, str(len(policy["gate_b_required_evidence"])))
    check("policy_b_supplement_count", len(policy["gate_b_supplementary_evidence"]) == 5, str(len(policy["gate_b_supplementary_evidence"])))
    check("policy_d_count", len(policy["gate_d_required_evidence"]) == 7, str(len(policy["gate_d_required_evidence"])))
    check("policy_invalid_evidence", len(policy["invalid_evidence_classes"]) >= 7, str(len(policy["invalid_evidence_classes"])))
    check("policy_factorization", policy["formal_evaluator"]["factorization_rule"] == "extended_gate = evidence_gate composed with pi_E", str(policy["formal_evaluator"]))
    check("policy_authority_false", all(value is False for value in policy["authority_limits"].values()), str(policy["authority_limits"]))

    cases = fixtures["cases"]
    fixture_failures = []
    for case in cases:
        observed = evaluate_fixture(case)
        if observed != case["expected_result"]:
            fixture_failures.append({"case_id": case["case_id"], "expected": case["expected_result"], "observed": observed})
    check("fixture_count", len(cases) == 14, str(len(cases)))
    check("fixture_unique_ids", len({case["case_id"] for case in cases}) == len(cases), str([case["case_id"] for case in cases]))
    check("fixture_evaluator", not fixture_failures, json.dumps(fixture_failures, sort_keys=True))
    check("fixture_allowed_selection", sum(case["expected_disposition"].startswith("allowed") for case in cases) >= 4, "at least four allowed selection/route cases")
    check("fixture_forbidden_override", sum(case["expected_disposition"].startswith("reject") for case in cases) >= 9, "at least nine rejected override cases")

    required_tex_phrases = [
        "Position A is adopted as the planning boundary",
        "Realistic matter emergence is explicitly outside the current cycle",
        "Conditional-input non-entailment lemma",
        "Evidence-projection invariance theorem",
        "protected selection cannot make the gate positive",
        "Position B is not active",
        "P1-T04 may separately lock Gate B",
    ]
    check("tex_required_claims", all(phrase in normalized_tex for phrase in required_tex_phrases), str(required_tex_phrases))
    check("tex_no_global_no_go", "not a global impossibility theorem" in normalized_tex, "contract-relative limitation present")
    check("tex_no_gate_verdict", "not a new protected Gate verdict" in normalized_tex, "non-verdict status present")

    check("child_math_complete", child_math.get("status") == "completed" and child_math.get("external_review") is False, str(child_math.get("status")))
    check("child_math_payload_count", len(child_math.get("new_mathematical_payload", [])) == 2, str(len(child_math.get("new_mathematical_payload", []))))
    check("child_phil_complete", child_phil.get("status") == "completed" and child_phil.get("external_review") is False, str(child_phil.get("status")))
    check("child_review_provenance", child_phil["review_provenance"]["class"] == "same_context_internal_ai_review_only", str(child_phil["review_provenance"]))
    check("conflicts_resolved", conflict.get("status") == "resolved" and conflict.get("blocking_conflict_count") == 0 and len(conflict.get("conflicts", [])) == 4, str(conflict.get("status")))
    check("fusion_internal_only", "not external review" in normalized_fusion and "no Distance-to-GR delta" in normalized_fusion, "internal-only and zero-delta language present")

    artifact_paths = [TEX, CONTRACT, POSITION_B, POLICY, FIXTURES, CHILD_MATH, CHILD_PHIL, CONFLICT, FUSION, Path(__file__).resolve()]
    artifact_hashes = {str(path.relative_to(ROOT)): sha256(path) for path in artifact_paths}
    status = "PASS" if not errors else "FAIL"
    result = {
        "schema_id": "v22_p1_t03_gate_policy_validation_v1",
        "task_id": "RT-20260809-003",
        "job_id": "AJ-RT-20260809-003-001",
        "generated_at": GENERATED_AT,
        "status": status,
        "check_count": len(checks),
        "failure_count": len(errors),
        "fixture_count": len(cases),
        "fixture_failure_count": len(fixture_failures),
        "checks": checks,
        "errors": errors,
        "fixture_failures": fixture_failures,
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
        "gate_id": "V22-P1-T03-FOCUSED-POLICY-VALIDATION",
        "task_id": "RT-20260809-003",
        "job_id": "AJ-RT-20260809-003-001",
        "status": status,
        "receipt_path": str(VALIDATION_PATH.relative_to(ROOT)),
        "content_hash": f"sha256:{validation_digest}",
        "counts": {"error_count": len(errors), "warning_count": 0, "finding_count": len(errors)},
        "relevant_finding_ids": [error.split(":", 1)[0] for error in errors],
        "summary": f"{len(checks) - len(errors)}/{len(checks)} focused checks and {len(cases) - len(fixture_failures)}/{len(cases)} Gate B/D fixtures pass.",
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
            "fixture_count": result["fixture_count"],
            "fixture_failure_count": result["fixture_failure_count"],
            "receipt_path": str(VALIDATION_PATH.relative_to(ROOT)),
            "compact_receipt_path": str(COMPACT_PATH.relative_to(ROOT)),
            "errors": result["errors"],
        }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
