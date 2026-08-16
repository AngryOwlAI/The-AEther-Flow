#!/usr/bin/env python3
"""Focused validator for the RT-20260816-003 Smuggling Auditor packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260816-003"
ART = TASK / "artifacts"
SUCCESSOR = (
    "PKT-V22-P4T02-B2-PROPOSAL-ONLY-MEASURABLE-FIBER-OCCURRENCE-LAW-"
    "COUPLING-PARAMETER-STATIONARITY-REFUTER-STRESS-V1"
)
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-KSTAR-STANDALONE-LOCAL-BRIDGE-IRRELEVANCE",
    "NDCL-V22-P4T02-B2-PROJECTIVE-CONORMAL-ROBUST-SELECTION-CONFORMAL-LIFT",
}
DIMENSIONS = {
    "current_source_arena_and_phi_src_boundary",
    "token_set_and_locally_constant_fiber_provenance",
    "total_admissibility_goal_preload",
    "complement_involution_and_token_symmetry_choice",
    "kernel_parameter_and_clock_nonselection",
    "shared_flip_driver_and_coupling_descent_scope",
    "restriction_pullback_arrow_class_and_circularity",
    "total_variation_and_robustness_overread",
    "formal_kernel_probability_and_occurrence_semantics",
    "natural_kernel_root_and_coupling_nonselection",
    "target_empirical_physical_and_workflow_authority_scan",
    "current_ontology_adoption_and_p4_t02_relevance",
}


class UniqueLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueLoader, node: yaml.MappingNode, deep: bool = False) -> Any:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a JSON object")
    return value


def child_verdict(data: dict[str, Any]) -> str:
    if "audit_result" in data:
        return str(data["audit_result"]["audit_verdict"])
    return str(data["decisive_audit_verdict"]["selected_verdict"])


def child_successor(data: dict[str, Any]) -> str:
    return str(data["selected_successor"]["packet_id"])


def check(condition: bool, name: str, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    paths = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260816-003-001.yaml",
        "role": TASK / "roles/smuggling-auditor@0.2.0--RT-20260816-003.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260816-003-001.yaml",
        "documentation": TASK / "documentation_impact.yaml",
        "math": ART / "child_phys_math_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_audit.yaml",
        "phil": ART / "child_phys_phil_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_audit.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_audit.yaml",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_audit.md",
        "matrix": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_matrix_v1.yaml",
        "disposition": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_disposition_v1.yaml",
        "model": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_model.py",
        "tex": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_audit_v1.tex",
        "compile": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_latex_compile_receipt.json",
        "provenance": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_provenance_manifest_v1.yaml",
        "handoff_yaml": ROOT / "research_control/handoffs/handoff-1046.yaml",
        "handoff_md": ROOT / "research_control/handoffs/handoff-1046.md",
    }
    checks: dict[str, bool] = {}
    for key, path in paths.items():
        check(path.exists(), f"exists_{key}", checks)
    if not all(paths[k].exists() for k in paths):
        payload = {"status": "FAIL", "checks": checks}
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    task = load_yaml(paths["task"])
    job = load_yaml(paths["job"])
    role = load_yaml(paths["role"])
    completion = load_yaml(paths["completion"])
    documentation = load_yaml(paths["documentation"])
    math_child = load_yaml(paths["math"])
    phil_child = load_yaml(paths["phil"])
    conflict = load_yaml(paths["conflict"])
    matrix = load_yaml(paths["matrix"])
    disposition = load_yaml(paths["disposition"])
    compile_receipt = load_json(paths["compile"])
    provenance = load_yaml(paths["provenance"])
    handoff = load_yaml(paths["handoff_yaml"])

    check(task.get("task_id") == "RT-20260816-003", "task_identity", checks)
    check(task.get("status") == "completed", "task_completed", checks)
    check(task.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED", "task_validation_pass", checks)
    check(job.get("status") == "completed", "job_completed", checks)
    check(job.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED", "job_validation_pass", checks)
    check(role.get("status") == "completed", "role_completed", checks)
    check(completion.get("status") == "completed", "completion_status", checks)
    check(documentation.get("validation_status") == "PASS", "documentation_pass", checks)

    check(child_verdict(math_child) == "source_pure_as_written", "math_verdict", checks)
    check(child_verdict(phil_child) == "source_pure_as_written", "phil_verdict", checks)
    check(child_successor(math_child) == SUCCESSOR, "math_successor", checks)
    check(child_successor(phil_child) == SUCCESSOR, "phil_successor", checks)
    check(math_child["selected_successor"]["status"] == "selected_not_executed", "math_successor_unexecuted", checks)
    check(phil_child["selected_successor"]["status"] == "selected_not_executed", "phil_successor_unexecuted", checks)
    check(math_child["conflict_status"]["unresolved_conflict_count"] == 0, "math_no_conflict", checks)
    check(phil_child["potential_parent_fusion_conflicts"]["unresolved_blocking_conflict_count"] == "0", "phil_no_conflict", checks)

    matrix_dims = {row["dimension_id"] for row in matrix["audit_dimensions"]}
    check(matrix_dims == DIMENSIONS, "matrix_twelve_dimensions", checks)
    check(matrix["aggregate_disposition"]["verdict"] == "source_pure_as_written", "matrix_verdict", checks)
    check(matrix["aggregate_disposition"]["independent_source_provenance_established"] is False, "matrix_no_provenance", checks)
    check(matrix["aggregate_disposition"]["physical_or_empirical_meaning_established"] is False, "matrix_no_physical_meaning", checks)

    result = disposition["smuggling_audit_result"]
    check(result["result_count"] == 1, "one_disposition_result", checks)
    check(result["result_type"] == "source_pure_as_written", "disposition_verdict", checks)
    check(result["target_import_detected"] is False, "no_target_import", checks)
    check(result["independent_source_provenance_passed"] is False, "no_source_provenance", checks)
    check(result["realized_occurrence_passed"] is False, "no_realized_occurrence", checks)
    check(disposition["source_extension_classification"]["category"] == "new_ontology_primitive", "new_ontology_primitive", checks)
    check(disposition["source_extension_classification"]["adopted"] is False, "not_adopted", checks)
    check(len(disposition["new_mathematical_payload"]) == 6, "six_parent_payloads", checks)
    check(set(disposition["preserved_freeze_labels"]) == FREEZES, "eight_freezes", checks)
    check(len(disposition["distance_to_gr_status"]) == 14, "fourteen_distance_rows", checks)
    check(all(row["status"] == "no_delta" for row in disposition["distance_to_gr_status"]), "all_distance_no_delta", checks)
    check(disposition["selected_successor"]["packet_id"] == SUCCESSOR, "parent_successor", checks)
    check(disposition["selected_successor"]["status"] == "selected_not_executed", "parent_successor_unexecuted", checks)
    check(disposition["selected_successor"]["created"] is False, "successor_not_created", checks)
    check(disposition["selected_successor"]["executed"] is False, "successor_not_executed", checks)

    check(conflict["unresolved_conflict_count"] == 0, "parent_no_conflict", checks)
    check(conflict["shared_consensus"]["decisive_result"] == "source_pure_as_written", "conflict_consensus", checks)
    check(conflict["shared_consensus"]["freeze_count"] == 8, "conflict_freezes", checks)
    check(conflict["shared_consensus"]["distance_to_gr_no_delta_count"] == 14, "conflict_distance", checks)
    check(conflict["successor"]["packet_id"] == SUCCESSOR, "conflict_successor", checks)

    model_run = subprocess.run(
        [sys.executable, str(paths["model"]), "--json"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    model_payload = json.loads(model_run.stdout) if model_run.stdout.strip() else {}
    check(model_run.returncode == 0, "model_exit_zero", checks)
    check(model_payload.get("status") == "PASS", "model_pass", checks)
    check(model_payload.get("check_count") == 27, "model_27_checks", checks)
    check(model_payload.get("pass_count") == 27, "model_27_pass", checks)
    check(model_payload.get("payload_sha256") == "ea0aa7d49c27c94b97b6cbcf48c18d1314f80dab9ec94023822f1000b52134b7", "model_payload_hash", checks)

    fusion_text = paths["fusion"].read_text(encoding="utf-8")
    tex_text = paths["tex"].read_text(encoding="utf-8")
    for token, name in [
        ("source_pure_as_written", "fusion_verdict_text"),
        ("new_ontology_primitive", "fusion_classification_text"),
        (SUCCESSOR, "fusion_successor_text"),
        ("componentwise independence", "fusion_component_countercontrol"),
        ("token-class", "fusion_token_class"),
    ]:
        check(token in fusion_text, name, checks)
    for token, name in [
        ("source\\_pure\\_as\\_written", "tex_verdict_text"),
        ("Natural token-class coupling family", "tex_coupling_theorem"),
        ("Stationary-law classification", "tex_stationary_theorem"),
        ("No occurrence or clock", "tex_occurrence_clock"),
    ]:
        check(token in tex_text, name, checks)

    check(compile_receipt.get("status") == "PASS", "compile_pass", checks)
    check(compile_receipt.get("page_count") == 4, "compile_four_pages", checks)
    check(compile_receipt["visual_inspection"]["status"] == "PASS", "visual_pass", checks)
    check(compile_receipt["source_sha256"] == sha256(paths["tex"]), "compile_source_hash", checks)

    provenance_hashes_ok = True
    for row in provenance["governing_sources"] + provenance["produced_artifacts"]:
        target = ROOT / row["path"]
        provenance_hashes_ok = provenance_hashes_ok and target.exists() and sha256(target) == row["sha256"]
    check(provenance_hashes_ok, "provenance_hashes", checks)
    check(provenance["mutable_registry_files_bound_by_full_hash"] is False, "acyclic_provenance", checks)

    check(handoff.get("handoff_id") == "handoff-1046", "handoff_identity", checks)
    check(handoff.get("selected_packet_id") == SUCCESSOR, "handoff_successor", checks)
    check(handoff.get("selected_packet_executed") is False, "handoff_unexecuted", checks)

    authority = disposition["authority_limits"]
    for field in [
        "source_law_adopted",
        "occurrence_realized",
        "physical_probability_established",
        "physical_time_selected",
        "g_eff_constructed",
        "d7_reevaluated",
        "b2_activated",
        "p4_t03_unlocked",
        "distance_to_gr_changed",
        "physics_promotion_authorized",
        "publication_authorized",
        "push_authorized",
        "external_action_authorized",
    ]:
        check(authority[field] is False, f"authority_false_{field}", checks)

    failed = sorted(name for name, value in checks.items() if not value)
    payload = {
        "schema_id": "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_validation_v1",
        "task_id": "RT-20260816-003",
        "job_id": "AJ-RT-20260816-003-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "failed_checks": failed,
        "checks": checks,
        "model_payload_sha256": model_payload.get("payload_sha256", ""),
        "verdict": "source_pure_as_written",
        "successor": SUCCESSOR,
        "authority": "validation_receipt_only",
    }
    if args.write_report:
        report = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_validation.json"
        compact = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_compact_receipt.json"
        report.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact_payload = {
            "schema_id": "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_compact_receipt_v1",
            "task_id": payload["task_id"],
            "job_id": payload["job_id"],
            "status": payload["status"],
            "check_count": payload["check_count"],
            "pass_count": payload["pass_count"],
            "failed_check_count": len(failed),
            "model_payload_sha256": payload["model_payload_sha256"],
            "verdict": payload["verdict"],
            "successor": payload["successor"],
            "scientific_truth_inferred": False,
            "distance_to_gr_changed": False,
        }
        compact.write_text(json.dumps(compact_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True) if args.json else payload["status"])
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
