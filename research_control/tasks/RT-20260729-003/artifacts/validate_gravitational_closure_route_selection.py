#!/usr/bin/env python3
"""Validate the bounded v21 P8-T01 gravitational-closure route selection."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
REPORT_PATH = ARTIFACT_DIR / "gravitational_closure_route_selection_validation_v1.json"

DECISION_PATH = ARTIFACT_DIR / "gravitational_closure_route_decision_v1.yaml"
COMPARISON_PATH = ARTIFACT_DIR / "gravitational_closure_hypothesis_comparison_v1.yaml"
FROZEN_PATH = ARTIFACT_DIR / "frozen_gravitational_closure_alternatives_v1.yaml"
MATH_CHILD_PATH = ARTIFACT_DIR / "child_phys_math_p8_t01_closure_route_selection.yaml"
PHIL_CHILD_PATH = ARTIFACT_DIR / "child_phys_phil_p8_t01_closure_route_selection.yaml"
REVIEW_PATH = ARTIFACT_DIR / "parent_conflict_review_p8_t01_closure_route_selection.yaml"
FUSION_PATH = ARTIFACT_DIR / "parent_fusion_notes_p8_t01_closure_route_selection.md"
RECEIPT_PATH = ARTIFACT_DIR / "gravitational_closure_route_selection_receipt.md"

SELECTED = "conditional_source_to_local_effective_action_closure_v1"
ROUTES = {
    SELECTED,
    "hypersurface_deformation_closure_v1",
    "gravitational_closure_from_matter_v1",
    "thermodynamic_gravity_closure_v1",
}
FROZEN = ROUTES - {SELECTED}

SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex":
        "a2b9c6670cdb0e09ca2e19ff30f71d9bb954e3ab2fc73a5c9727a2df10db93aa",
    "research_control/tasks/RT-20260726-001/artifacts/p6_geometry_input_contract_v1.yaml":
        "7b0eee4ea249a3acf99d38d312bd14619dedea79977d7b802062e9410f5b8557",
    "research_control/tasks/RT-20260726-011/artifacts/metric_object_naming_decision_v1.yaml":
        "4d67563b2444cfed2bd430e9d027337f26656701624d532f7cb2e357cbac2452",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml":
        "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_theorem_inventory_and_route_v1.yaml":
        "b17afe5f02752f8202f1bbd3bd68d29ca8f42a124b543a08d43796f284c90046",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_constitutive_postulate_ledger_v1.yaml":
        "e11f5e4ae886932cad618caa3ee97e973bbd38d363db25776fe1fbd2c27451dc",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex":
        "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    "ontology/tex/aether_flow_dynamics.tex":
        "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
    "ontology/tex/aether_flow_consistency.tex":
        "d965519639ee8764a5c5a63798d15e8a9a380d7e208dffc43a0be02b6f245ba1",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    required_paths = [
        DECISION_PATH,
        COMPARISON_PATH,
        FROZEN_PATH,
        MATH_CHILD_PATH,
        PHIL_CHILD_PATH,
        REVIEW_PATH,
        FUSION_PATH,
        RECEIPT_PATH,
    ]
    for path in required_paths:
        check(f"exists:{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    try:
        decision = load_yaml(DECISION_PATH)
        comparison = load_yaml(COMPARISON_PATH)
        frozen = load_yaml(FROZEN_PATH)
        math_child = load_yaml(MATH_CHILD_PATH)
        phil_child = load_yaml(PHIL_CHILD_PATH)
        review = load_yaml(REVIEW_PATH)
    except Exception as exc:
        check("yaml_load", False, str(exc))
        decision = comparison = frozen = math_child = phil_child = review = {}
    else:
        check("yaml_load", True, "All six YAML control artifacts parsed.")

    decision_result = decision.get("decision", {})
    check("selected_route", decision_result.get("selected_route_id") == SELECTED, str(decision_result.get("selected_route_id")))
    check("selection_status", decision_result.get("result_status") == "selected_for_formalization_only", str(decision_result.get("result_status")))
    check("next_plan_task", decision_result.get("selected_next_plan_task_id") == "P8-T02", str(decision_result.get("selected_next_plan_task_id")))
    check("next_role", decision_result.get("selected_next_role_family") == "ontology-formalizer@0.2.0", str(decision_result.get("selected_next_role_family")))
    check("next_packet", decision_result.get("selected_next_packet_type") == "ontology_law_research_packet", str(decision_result.get("selected_next_packet_type")))

    compared = comparison.get("routes", [])
    compared_ids = {item.get("route_id") for item in compared if isinstance(item, dict)}
    selected_count = sum(item.get("disposition") == "selected_for_formalization_only" for item in compared if isinstance(item, dict))
    check("route_set", compared_ids == ROUTES, ",".join(sorted(str(value) for value in compared_ids)))
    check("exactly_one_selected", selected_count == 1, str(selected_count))

    frozen_items = frozen.get("frozen_alternatives", [])
    frozen_ids = {item.get("route_id") for item in frozen_items if isinstance(item, dict)}
    thaw_complete = all(bool(item.get("thaw_criteria")) for item in frozen_items if isinstance(item, dict))
    check("frozen_route_set", frozen_ids == FROZEN, ",".join(sorted(str(value) for value in frozen_ids)))
    check("all_freezes_have_thaw_criteria", thaw_complete and len(frozen_items) == 3, str(len(frozen_items)))

    limits = decision.get("authority_limits", {})
    barred_flags = [
        "canonical_ontology_modified",
        "source_law_adopted",
        "effective_geometry_constructed",
        "effective_metric_constructed",
        "local_effective_action_constructed",
        "target_stress_energy_tensor_constructed",
        "equivalence_principle_established_or_refuted",
        "einstein_equations_derived",
        "exact_gr_recovery_proved",
        "benchmark_promoted",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
    ]
    check("authority_flags_false", all(limits.get(flag) is False for flag in barred_flags), ",".join(barred_flags))

    distance = decision.get("distance_to_gr", {})
    check("no_distance_delta", distance.get("changed") is False and distance.get("ledger_row_updated") is False, json.dumps(distance, sort_keys=True))

    for child_name, child in (("math", math_child), ("phil", phil_child)):
        child_findings = child.get("findings", {})
        check(f"{child_name}_child_selection", child_findings.get("recommended_route_id") == SELECTED, str(child_findings.get("recommended_route_id")))
        check(f"{child_name}_child_complete", child.get("status") == "completed", str(child.get("status")))

    check("parent_conflicts_resolved", review.get("status") == "resolved" and review.get("unresolved_conflicts") == [], json.dumps(review.get("unresolved_conflicts")))
    check("no_child_agentjobs", review.get("fusion_result", {}).get("child_agentjob_count") == 0, str(review.get("fusion_result", {}).get("child_agentjob_count")))
    check("no_child_subagents", review.get("fusion_result", {}).get("child_subagent_count") == 0, str(review.get("fusion_result", {}).get("child_subagent_count")))

    next_target = decision.get("next_theorem_target", {})
    forbidden_premise = str(next_target.get("forbidden_premise", ""))
    check("p8_t02_target", next_target.get("target_id") == "LocalEffectiveActionClosureTarget_v1", str(next_target.get("target_id")))
    check("einstein_premise_forbidden", "Einstein-Hilbert" in forbidden_premise and "Einstein equations" in forbidden_premise, forbidden_premise)

    receipt_text = RECEIPT_PATH.read_text(encoding="utf-8") if RECEIPT_PATH.is_file() else ""
    fusion_text = FUSION_PATH.read_text(encoding="utf-8") if FUSION_PATH.is_file() else ""
    combined_text = receipt_text + "\n" + fusion_text
    check("receipt_claim_boundary", "No effective action" in combined_text and "not_started" in combined_text, "Explicit nonconstruction and unchanged burden recorded.")
    check("benchmark_not_source_premise", "forbidden as source premises" in receipt_text, "Receipt excludes benchmark-derived premises.")

    for relative_path, expected in SOURCE_HASHES.items():
        source_path = ROOT / relative_path
        actual = sha256(source_path) if source_path.is_file() else ""
        check(f"source_hash:{relative_path}", actual == expected, actual)

    failed = [item for item in checks if item["status"] == "FAIL"]
    report = {
        "schema_id": "gravitational_closure_route_selection_validation_v1",
        "task_id": "RT-20260729-003",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "selected_route_id": SELECTED,
        "selected_next_plan_task_id": "P8-T02",
        "distance_to_gr_changed": False,
        "checks": checks,
    }

    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json or not args.check:
        print(json.dumps(report, indent=2, sort_keys=True))

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
