#!/usr/bin/env python3
"""Validate the bounded V22 P4-T02 B2 fallback selector transaction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260809-020"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_selector_compact_receipt.json"
GENERATED_AT = "2026-08-09T21:27:35Z"

DECISION = ART / "v22_p4_t02_b2_selector_decision_v1.yaml"
READINESS = ART / "v22_p4_t02_b2_activation_readiness_matrix_v1.yaml"
DEPENDENCY = ART / "v22_p4_t02_b2_descriptor_dependency_map_v1.yaml"
PROVENANCE = ART / "v22_p4_t02_b2_source_provenance_manifest_v1.yaml"
TEX = ART / "v22_p4_t02_b2_fallback_descriptor_selection_v1.tex"
CHILD_MATH = ART / "child_phys_math_p4_t02_b2_selector.yaml"
CHILD_PHIL = ART / "child_phys_phil_p4_t02_b2_selector.yaml"
CONFLICT = ART / "parent_conflict_review_p4_t02_b2_selector.yaml"
FUSION = ART / "parent_fusion_notes_p4_t02_b2_selector.md"

EXPECTED_SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-0989.yaml":
        "617872c1b63574d036c0505075af879385192293fac672b2f8acd99a3ed3939a",
    "research_control/tasks/RT-20260809-009/artifacts/v22_p2_t04_fallback_matter_principal_candidate_v1.yaml":
        "11917a5c868b6ed50633e1b7528b59079db40f10c003c32176d1887df5dae6e5",
    "research_control/tasks/RT-20260809-009/artifacts/v22_p2_t04_activation_handoff_v1.yaml":
        "4fddf53e2f072825081c0412023a6ce5ce24f633e6f6b6464e81606143ab1fc0",
    "research_control/tasks/RT-20260809-019/artifacts/v22_p4_t02_hyperbolicity_universality_robustness_hard_fail_screen_v1.tex":
        "6eec0961cd84b3ec8f88845de1e5f87c13fee009b151fa557655d09a0fa6b50a",
    "research_control/tasks/RT-20260809-019/artifacts/v22_p4_t02_candidate_termination_budget_transition_v1.yaml":
        "84e7a8c9f94377f6cb6de30e987e442b0381988e40fff2460282451cfaf43e8c",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_source_adequacy_checklist_v1.yaml":
        "a9b59df7b5b2d1203fef53cf23817400c6d1511836e97ff1ae21b819dc064e68",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return value


def get_path(data: dict[str, Any], *parts: str) -> Any:
    value: Any = data
    for part in parts:
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: Any) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    core_paths = [
        DECISION, READINESS, DEPENDENCY, PROVENANCE, TEX,
        CHILD_MATH, CHILD_PHIL, CONFLICT, FUSION,
    ]
    for path in core_paths:
        check(f"exists_{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    try:
        decision = load_yaml(DECISION)
        readiness = load_yaml(READINESS)
        dependency = load_yaml(DEPENDENCY)
        provenance = load_yaml(PROVENANCE)
        child_math = load_yaml(CHILD_MATH)
        child_phil = load_yaml(CHILD_PHIL)
        conflict = load_yaml(CONFLICT)
    except Exception as exc:
        check("yaml_parse", False, str(exc))
        decision = readiness = dependency = provenance = {}
        child_math = child_phil = conflict = {}
    else:
        check("yaml_parse", True, "seven YAML artifacts parse as mappings")

    check("candidate_exact", decision.get("candidate_id") == "CAND-V22-B2-P7-COMMON-PRINCIPAL-LIFT-V1", decision.get("candidate_id"))
    check("family_exact", decision.get("candidate_family_id") == "FAM-V22-B2-MATTER-PRINCIPAL-POLYNOMIAL", decision.get("candidate_family_id"))
    check("plan_exact", decision.get("plan_task_id") == "P4-T02", decision.get("plan_task_id"))
    check("selected_path_exact", get_path(decision, "selected_path", "path_id") == "FORMALIZE_B2_CONTINUUM_LIFT_DESCRIPTOR_V1", get_path(decision, "selected_path", "path_id"))
    check("next_role_exact", get_path(decision, "selected_path", "next_role_family") == "ontology-formalizer@0.2.0", get_path(decision, "selected_path", "next_role_family"))
    check("route_label_exact", get_path(decision, "selected_path", "route_label") == "ontology-law-research-packet", get_path(decision, "selected_path", "route_label"))
    check("next_plan_stays_p4_t02", get_path(decision, "selected_path", "next_plan_task_id") == "P4-T02", get_path(decision, "selected_path", "next_plan_task_id"))
    check("b2_activation_effect_false", get_path(decision, "selected_path", "b2_activation_effect") is False, get_path(decision, "selected_path", "b2_activation_effect"))
    check("p4_t03_unlock_effect_false", get_path(decision, "selected_path", "p4_t03_unlock_effect") is False, get_path(decision, "selected_path", "p4_t03_unlock_effect"))

    vector = get_path(decision, "decision_basis", "readiness_vector")
    check("decision_readiness_vector", vector == [1, 1, 1, 1, 0, 0], vector)
    check("decision_activation_zero", get_path(decision, "decision_basis", "activation_value") == 0, get_path(decision, "decision_basis", "activation_value"))
    check("readiness_vector_exact", readiness.get("readiness_vector") == [1, 1, 1, 1, 0, 0], readiness.get("readiness_vector"))
    check("readiness_activation_false", readiness.get("activation_value") is False, readiness.get("activation_value"))
    check("readiness_not_activated", readiness.get("activation_decision") == "NOT_ACTIVATED", readiness.get("activation_decision"))
    rows = readiness.get("rows", [])
    row_map = {row.get("predicate_id"): row.get("value") for row in rows if isinstance(row, dict)}
    expected_row_map = {
        "R1_B1_TERMINATED": True,
        "R2_ZERO_OTHER_ACTIVE": True,
        "R3_FRESH_EXACT_SELECTOR": True,
        "R4_P7_HASHES_UNCHANGED": True,
        "R5_DESCRIPTOR_COMPLETE": False,
        "R6_ADEQUACY_REEVALUATED": False,
    }
    for key, value in expected_row_map.items():
        check(f"predicate_{key}", row_map.get(key) is value, row_map.get(key))
    check("activation_boolean_reproduced", all(expected_row_map.values()) is False, all(expected_row_map.values()))
    check("repair_predicate_descriptor", readiness.get("selected_repair_predicate") == "R5_DESCRIPTOR_COMPLETE", readiness.get("selected_repair_predicate"))
    check("ordered_followup_adequacy", readiness.get("ordered_followup_predicate") == "R6_ADEQUACY_REEVALUATED", readiness.get("ordered_followup_predicate"))
    check("activation_theorem_present", get_path(readiness, "theorem", "theorem_id") == "THM-V22-P4T02-B2-CONJUNCTIVE-ACTIVATION-EXCLUSION", get_path(readiness, "theorem", "theorem_id"))

    theory = decision.get("theoretical_decision_output", {})
    check("packet_type_ontology_law", theory.get("selected_next_packet_type") == "ontology_law_research_packet", theory.get("selected_next_packet_type"))
    check("claim_blocks_preserved", theory.get("preserves_claim_blocks") is True, theory.get("preserves_claim_blocks"))
    check("human_gate_not_required_now", theory.get("requires_human_gate") is False, theory.get("requires_human_gate"))
    for key in ["decision_basis", "theoretical_method", "human_gate_reason", "decision_consequence", "new_payload_novelty", "source_extension_category", "source_extension_import_classification"]:
        check(f"theory_{key}_nonblank", bool(str(theory.get(key, "")).strip()), theory.get(key))

    ontology = decision.get("ontology_law_research_packet", {})
    check("ontology_route_exact", ontology.get("route") == "ontology-law-research-packet", ontology.get("route"))
    check("trigger_exact", ontology.get("trigger_classification") == "derivation_critical_missing_source_law", ontology.get("trigger_classification"))
    check("milestone_exact", ontology.get("target_derivation_milestone") == "effective_metric_g_eff", ontology.get("target_derivation_milestone"))
    check("missing_source_law_nonblank", bool(str(ontology.get("missing_source_law", "")).strip()), ontology.get("missing_source_law"))
    under = str(ontology.get("underdetermination_statement", ""))
    check("underdetermination_precise", under.startswith("Current ontology does not derive"), under)
    check("no_go_not_proved", ontology.get("no_go_theorem_status") == "not_proved", ontology.get("no_go_theorem_status"))
    check("blocked_open_status", get_path(ontology, "adoption_status", "status_pair") == "blocked_adoption_open_continuation", get_path(ontology, "adoption_status", "status_pair"))
    check("payload_mode_exact", ontology.get("packet_payload_mode") == "candidate_law_payload", ontology.get("packet_payload_mode"))
    payload = ontology.get("candidate_law_payload", {})
    check("payload_status_draft", payload.get("status_label") == "draft/control", payload.get("status_label"))
    check("payload_proposal_only", payload.get("candidate_status") == "proposal-only", payload.get("candidate_status"))
    check("payload_source_extension_data", payload.get("material_class") == "source-extension data", payload.get("material_class"))
    check("formal_object_count_ten", len(payload.get("formal_objects", [])) == 10, len(payload.get("formal_objects", [])))
    check("proof_obligations_nonempty", len(payload.get("proof_obligations", [])) >= 6, len(payload.get("proof_obligations", [])))
    forbidden_sources = set(get_path(ontology, "no_target_import_audit_scope", "forbidden_source_classes") or [])
    for token in ["target_atlas", "target_metric", "benchmark_success", "candidate_reconstruction", "generated_derivative", "registry_metadata_authority", "role_authority", "validation_authority"]:
        check(f"forbidden_source_{token}", token in forbidden_sources, sorted(forbidden_sources))
    check("human_gate_before_adoption", get_path(ontology, "human_gate_request", "required_before_adoption") is True, get_path(ontology, "human_gate_request", "required_before_adoption"))

    formal_tuple = dependency.get("formal_tuple", [])
    check("dependency_tuple_ten", len(formal_tuple) == 10, len(formal_tuple))
    nodes = dependency.get("nodes", [])
    edges = dependency.get("edges", [])
    check("dependency_node_count_nine", len(nodes) == 9, len(nodes))
    check("dependency_edge_count_ten", len(edges) == 10, len(edges))
    check("dependency_selected_first_missing", dependency.get("selected_next_node") == "D1_CONTINUUM_FIELDS_REGULARITY", dependency.get("selected_next_node"))
    node_map = {node.get("node_id"): node.get("status") for node in nodes if isinstance(node, dict)}
    check("finite_input_present", node_map.get("D0_FINITE_P7_INPUT") == "present_conditional_input", node_map.get("D0_FINITE_P7_INPUT"))
    check("adequacy_blocked", node_map.get("D7_P2_T01_ADEQUACY_REEVALUATION") == "blocked_by_descriptor", node_map.get("D7_P2_T01_ADEQUACY_REEVALUATION"))
    check("later_activation_blocked", node_map.get("D8_LATER_ACTIVATION_SELECTOR") == "blocked", node_map.get("D8_LATER_ACTIVATION_SELECTOR"))

    for path_text, expected_hash in EXPECTED_SOURCE_HASHES.items():
        path = ROOT / path_text
        actual = sha256(path) if path.is_file() else ""
        check(f"source_hash_{Path(path_text).name}", actual == expected_hash, actual)
    provenance_rows = {
        row.get("path"): row.get("sha256")
        for row in provenance.get("entries", [])
        if isinstance(row, dict)
    }
    for path_text, expected_hash in EXPECTED_SOURCE_HASHES.items():
        check(f"provenance_hash_{Path(path_text).name}", provenance_rows.get(path_text) == expected_hash, provenance_rows.get(path_text))

    check("child_math_completed", child_math.get("status") == "completed", child_math.get("status"))
    check("child_math_vector", get_path(child_math, "results", "readiness_vector") == [1, 1, 1, 1, 0, 0], get_path(child_math, "results", "readiness_vector"))
    check("child_math_activation_zero", get_path(child_math, "results", "activation_value") == 0, get_path(child_math, "results", "activation_value"))
    check("child_phil_completed", child_phil.get("status") == "completed", child_phil.get("status"))
    check("child_phil_five_layers", len(child_phil.get("layer_separation", {})) == 5, sorted(child_phil.get("layer_separation", {})))
    check("conflict_resolved", conflict.get("status") == "resolved", conflict.get("status"))
    check("conflict_count_four", conflict.get("resolved_conflict_count") == 4, conflict.get("resolved_conflict_count"))
    check("unresolved_conflicts_zero", conflict.get("unresolved_conflicts") == [], conflict.get("unresolved_conflicts"))
    check("child_agentjobs_zero", get_path(conflict, "fusion_result", "child_agentjob_count") == 0, get_path(conflict, "fusion_result", "child_agentjob_count"))

    tex_text = TEX.read_text(encoding="utf-8") if TEX.is_file() else ""
    fusion_text = FUSION.read_text(encoding="utf-8") if FUSION.is_file() else ""
    for token in [
        "THM-V22-P4T02-B2-CONJUNCTIVE-ACTIVATION-EXCLUSION",
        "blocked\\_adoption\\_open\\_continuation",
        "ontology-law-research-packet",
        "(R_1,R_2,R_3,R_4,R_5,R_6)=(1,1,1,1,0,0)",
        "P4-T03 remains",
    ]:
        check(f"tex_token_{hashlib.sha256(token.encode()).hexdigest()[:8]}", token in tex_text, token)
    for token in [
        "activation is false",
        "ontology-law-research-packet",
        "B2 remains inactive",
        "P4-T03 remains",
        "There are no unresolved blocking conflicts",
    ]:
        check(f"fusion_token_{hashlib.sha256(token.encode()).hexdigest()[:8]}", token in fusion_text, token)

    authority = decision.get("authority_limits", {})
    for key in ["scientific_status_changed", "physical_status_changed", "distance_to_gr_changed", "b2_activated", "source_extension_adopted", "canonical_ontology_modified", "p4_t03_unlocked", "gate_b_verdict_issued", "physics_promotion_authorized", "proof_authority"]:
        check(f"authority_{key}_false", authority.get(key) is False, authority.get(key))
    check("b1_termination_preserved", authority.get("b1_termination_preserved") is True, authority.get("b1_termination_preserved"))

    control_paths = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260809-020-001.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260809-020-001.yaml",
        "role": TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260809-020.yaml",
        "ddr": TASK / "DDR-20260809-020.md",
        "documentation": TASK / "documentation_impact.yaml",
        "handoff_yaml": ROOT / "research_control/handoffs/handoff-0990.yaml",
        "handoff_md": ROOT / "research_control/handoffs/handoff-0990.md",
    }
    controls: dict[str, dict[str, Any]] = {}
    for label, path in control_paths.items():
        check(f"control_exists_{label}", path.is_file(), str(path.relative_to(ROOT)))
        if path.suffix in {".yaml", ".yml"} and path.is_file():
            try:
                controls[label] = load_yaml(path)
                check(f"control_yaml_{label}", True, "parsed")
            except Exception as exc:
                check(f"control_yaml_{label}", False, str(exc))
    task = controls.get("task", {})
    job = controls.get("job", {})
    completion = controls.get("completion", {})
    handoff = controls.get("handoff_yaml", {})
    role = controls.get("role", {})
    check("task_completed", task.get("status") == "completed", task.get("status"))
    check("task_plan_p4_t02", get_path(task, "implementation_plan", "plan_task_id") == "P4-T02", get_path(task, "implementation_plan", "plan_task_id"))
    check("task_b2_inactive", get_path(task, "completion_contract", "b2_activated") is False, get_path(task, "completion_contract", "b2_activated"))
    check("job_role_selector", job.get("role_id") == "theoretical-continuation-selector", job.get("role_id"))
    check("job_status_completed", job.get("status") == "completed", job.get("status"))
    check("job_parent_child", get_path(job, "role_decomposition", "mode") == "parent_child_parallel_synthesis", get_path(job, "role_decomposition", "mode"))
    check("completion_status_completed", completion.get("status") == "completed", completion.get("status"))
    check("completion_selector_output", get_path(completion, "theoretical_decision_output", "selected_next_packet_type") == "ontology_law_research_packet", get_path(completion, "theoretical_decision_output", "selected_next_packet_type"))
    check("completion_distance_unchanged", get_path(completion, "distance_to_gr_delta", "changed") is False, get_path(completion, "distance_to_gr_delta", "changed"))
    check("completion_payload_present", bool(completion.get("new_mathematical_payload")), len(completion.get("new_mathematical_payload", [])))
    check("handoff_0990", handoff.get("handoff_id") == "handoff-0990", handoff.get("handoff_id"))
    check("handoff_next_role_formalizer", get_path(handoff, "selected_next_route", "role_family") == "ontology-formalizer@0.2.0", get_path(handoff, "selected_next_route", "role_family"))
    check("handoff_b2_inactive", get_path(handoff, "active_state_boundary", "b2_fallback_activated") is False, get_path(handoff, "active_state_boundary", "b2_fallback_activated"))
    check("role_overlay", role.get("role_execution_kind") == "task_overlay", role.get("role_execution_kind"))

    registry_expectations = {
        "registries/RESEARCH_TASK_REGISTRY.csv": "RT-20260809-020",
        "registries/AGENT_JOB_REGISTRY.csv": "AJ-RT-20260809-020-001",
        "registries/DIRECTOR_DECISION_REGISTRY.csv": "DDR-20260809-020",
        "registries/ROLE_EXECUTION_REGISTRY.csv": "theoretical-continuation-selector@0.1.0--RT-20260809-020",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv": "CB-V22-P4-T02-B2-DESCRIPTOR-SELECTOR-001",
        "registries/TEX_SOURCE_REGISTRY.csv": "TEX-V22-P4-T02-B2-FALLBACK-DESCRIPTOR-SELECTION-V1",
        "registries/MARKDOWN_SOURCE_REGISTRY.csv": "MD-V22-P4-T02-B2-PARENT-FUSION-SELECTION-V1",
    }
    for path_text, token in registry_expectations.items():
        path = ROOT / path_text
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        check(f"registry_{Path(path_text).stem}_{token[:12]}", token in text, token)

    backlog = load_yaml(ROOT / "research_control/design/v22_recommendation_backlog.yaml")
    p4_t02_rows = [
        row for row in backlog.get("items", [])
        if isinstance(row, dict) and row.get("plan_task_id") == "P4-T02"
    ]
    check("backlog_p4_t02_unique", len(p4_t02_rows) == 1, len(p4_t02_rows))
    if p4_t02_rows:
        row = p4_t02_rows[0]
        check("backlog_descriptor_pending", row.get("implementation_status") == "fallback_descriptor_path_selected_construction_pending", row.get("implementation_status"))
        check("backlog_runtime_formalizer", row.get("runtime_role_family") == "ontology-formalizer@0.2.0", row.get("runtime_role_family"))
        check("backlog_b2_inactive", row.get("runtime_b2_fallback_activated") is False, row.get("runtime_b2_fallback_activated"))
    program = load_yaml(ROOT / "research_control/program_state.yaml")
    check("program_active_task", program.get("active_task_id") == "RT-20260809-020", program.get("active_task_id"))
    check("program_active_job", program.get("active_agent_job_id") == "AJ-RT-20260809-020-001", program.get("active_agent_job_id"))
    check("program_handoff", program.get("latest_handoff_id") == "handoff-0990", program.get("latest_handoff_id"))
    check("program_next_p4_t02", program.get("next_plan_task_id") == "P4-T02", program.get("next_plan_task_id"))

    failed = [item for item in checks if not item["passed"]]
    report = {
        "schema_id": "v22_p4_t02_b2_selector_validation_v1",
        "generated_at": GENERATED_AT,
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "readiness_vector": [1, 1, 1, 1, 0, 0],
        "activation_value": 0,
        "selected_path_id": "FORMALIZE_B2_CONTINUUM_LIFT_DESCRIPTOR_V1",
        "selected_next_packet_type": "ontology_law_research_packet",
        "selected_next_role_family": "ontology-formalizer@0.2.0",
        "b2_activated": False,
        "p4_t03_unlocked": False,
        "checks": checks,
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_selector_compact_receipt_v1",
        "generated_at": GENERATED_AT,
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
        "readiness_vector": report["readiness_vector"],
        "activation_value": report["activation_value"],
        "selected_path_id": report["selected_path_id"],
        "selected_next_packet_type": report["selected_next_packet_type"],
        "selected_next_role_family": report["selected_next_role_family"],
        "b2_activated": False,
        "p4_t03_unlocked": False,
    }

    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.check:
        existing_report = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.is_file() else None
        existing_compact = json.loads(COMPACT.read_text(encoding="utf-8")) if COMPACT.is_file() else None
        if existing_report != report or existing_compact != compact:
            report["status"] = "FAIL"
            report["receipt_mismatch"] = True
            failed.append({"check_id": "receipt_mismatch", "passed": False})
    summary = {
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": len(failed),
        "failed_check_ids": [item["check_id"] for item in failed],
        "report_path": str(REPORT.relative_to(ROOT)),
        "compact_receipt_path": str(COMPACT.relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"{summary['status']}: {summary['check_count'] - summary['failure_count']}/{summary['check_count']} checks")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
