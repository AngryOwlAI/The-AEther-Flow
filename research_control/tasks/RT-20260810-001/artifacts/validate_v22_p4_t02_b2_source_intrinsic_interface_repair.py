#!/usr/bin/env python3
"""Focused validator for the RT-20260810-001 P4-T02 repair packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

import yaml


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
TASK = HERE.parent
REPORT = HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_validation.json"
COMPACT = HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_compact_receipt.json"
OBSTRUCTION_ID = "OBST-V22-P4T02-B2-NATURAL-LINE-LOCK-001"
FREEZE_LABEL = "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return payload


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def load_model() -> Any:
    path = HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_model.py"
    spec = importlib.util.spec_from_file_location("rt028_source_interface_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load source-interface model")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check(condition: bool, check_id: str, detail: str, rows: list[dict[str, Any]]) -> None:
    rows.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        }
    )


def validate() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    required = [
        HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_v1.tex",
        HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_matrix_v1.yaml",
        HERE / "v22_p4_t02_b2_line_selector_obstruction_v1.yaml",
        HERE / "v22_p4_t02_b2_typed_operational_bridge_v1.yaml",
        HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_model.py",
        HERE / "child_phys_math_p4_t02_b2_source_intrinsic_interface_repair.yaml",
        HERE / "child_phys_phil_p4_t02_b2_source_intrinsic_interface_repair.yaml",
        HERE / "parent_conflict_review_p4_t02_b2_source_intrinsic_interface_repair.yaml",
        HERE / "parent_fusion_notes_p4_t02_b2_source_intrinsic_interface_repair.md",
        HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_latex_compile_receipt.json",
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260810-001.md",
        TASK / "documentation_impact.yaml",
        TASK / "roles/candidate-constructor@0.2.0--RT-20260810-001.yaml",
        TASK / "jobs/AJ-RT-20260810-001-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260810-001-001.yaml",
        REPO / "research_control/handoffs/handoff-0998.yaml",
        REPO / "research_control/handoffs/handoff-0998.md",
    ]
    check(
        all(path.is_file() for path in required),
        "required_files",
        "All task, payload, synthesis, receipt, completion, documentation, and handoff files exist.",
        rows,
    )

    source_hashes = {
        "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
        "research_control/handoffs/handoff-0997.yaml": "13f4e4a8c62510dbaea44600ba5257a91e264f2beb3a133ce609bf19e8057a5f",
        "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_equipped_chain_descriptor_attempt_v1.tex": "6b35e208631b287cd4ec5c6e27bc73c8389c555cad1c8a3cde24021e35be4169",
        "research_control/tasks/RT-20260809-026/artifacts/v22_p4_t02_b2_populated_instance_smuggling_audit_v1.tex": "8404fc7bd3586c353155cdce00bbede9e107ed4b38231b69953f4242bc5d90f0",
        "research_control/tasks/RT-20260727-007/artifacts/source_matter_ontology_and_sector_taxonomy_v1.tex": "8d160217bf223078a11bc63fde6593c11c39d5b50d9c48fbad7b12084f8a752d",
        "research_control/tasks/RT-20260728-002/artifacts/source_operational_device_suite_candidate_v1.tex": "d6c818ee29f1a7e659e2f454aec21431d680b3d2d4df048fcf36f4aba87ba22a",
        "research_control/tasks/RT-20260728-004/artifacts/universal_source_coupling_map_candidate_v1.tex": "5a9a8f5542a7c8b714bbff7ec06c06449b0c66c0196266051562caf9ce602c6b",
    }
    mismatches = [
        relative
        for relative, expected in source_hashes.items()
        if not (REPO / relative).is_file() or sha256(REPO / relative) != expected
    ]
    check(
        not mismatches,
        "immutable_source_hashes",
        f"Immutable mismatch list: {mismatches}",
        rows,
    )

    packet_hashes = {
        "v22_p4_t02_b2_source_intrinsic_interface_repair_v1.tex": "f1b8d1e851a56109e0976ff4cfde8ff2adce4e1376581547f048c55a6a0b3497",
        "v22_p4_t02_b2_source_intrinsic_interface_repair_matrix_v1.yaml": "bf0cf4db51af0a53d446aa9b0dfdcb21fcd63302da273efa2366d08799ede0b9",
        "v22_p4_t02_b2_line_selector_obstruction_v1.yaml": "3c4d53632f274ce2fa49612f369363e4b3c7ebdffd7a451c102f791f0e0f6b1e",
        "v22_p4_t02_b2_typed_operational_bridge_v1.yaml": "60a891df7a590c43917c4cb6e0f9ac25e61bcbf328711718d5ad947123d00a08",
        "v22_p4_t02_b2_source_intrinsic_interface_repair_model.py": "98659826bf35a83069870834ed2a38716741da8d35f7df62de3a1d7291349aee",
        "child_phys_math_p4_t02_b2_source_intrinsic_interface_repair.yaml": "c6da8413e19ef420db1e8ef284f4009eff02adf968ea9bdab980200b74b40563",
        "child_phys_phil_p4_t02_b2_source_intrinsic_interface_repair.yaml": "aae79beb0aec2e67533bd893d64004f3e9080e4455d51c1fdcc1fb2d9bd8f1be",
        "parent_conflict_review_p4_t02_b2_source_intrinsic_interface_repair.yaml": "1489115a8fe88743d0f4f271cd8b7ab4aa12d6a0944ed0746d398f42d07df5a1",
        "parent_fusion_notes_p4_t02_b2_source_intrinsic_interface_repair.md": "df589fcd266902d291bffe5b4a98ad02bbb7a6392609f36d626397ab2fae16de",
        "v22_p4_t02_b2_source_intrinsic_interface_repair_latex_compile_receipt.json": "0b2d67b45bdb59323476b0d441ad722accc6b1308be176c1daca4a3a05a48eac",
    }
    packet_mismatches = [
        name
        for name, expected in packet_hashes.items()
        if not (HERE / name).is_file() or sha256(HERE / name) != expected
    ]
    check(
        not packet_mismatches,
        "packet_artifact_hashes",
        f"Packet artifact mismatch list: {packet_mismatches}",
        rows,
    )

    matrix = load_yaml(HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_matrix_v1.yaml")
    repair_rows = matrix.get("repair_rows", [])
    finding_ids = {
        row.get("finding_id") for row in repair_rows if isinstance(row, dict)
    }
    expected_findings = {
        "F1-SECTOR-COVERAGE",
        "F2-PRESENTATION-NORM",
        "F3-SHARED-LEADING-PRELOAD",
        "F4-SECTOR-SPLIT-VARIATION",
        "F5-UNTYPED-OPERATIONAL-BRIDGE",
    }
    check(
        len(repair_rows) == 5 and finding_ids == expected_findings,
        "five_finding_matrix",
        f"Observed findings: {sorted(str(value) for value in finding_ids)}",
        rows,
    )
    summary = matrix.get("summary", {})
    check(
        matrix.get("decisive_result") == "precise_obstruction"
        and matrix.get("obstruction_id") == OBSTRUCTION_ID,
        "matrix_decisive_result",
        "The matrix records the exact scoped obstruction.",
        rows,
    )
    check(
        summary.get("repaired_on_declared_domain_count") == 2
        and summary.get("precise_obstruction_count") == 2
        and len(summary.get("full_descriptor_blocking_finding_ids", [])) == 4,
        "matrix_disposition_counts",
        f"Matrix summary: {summary}",
        rows,
    )
    check(
        summary.get("direct_target_import_count") == 0
        and summary.get("direct_authority_import_count") == 0,
        "matrix_direct_import_counts",
        "No direct target or authority import is recorded.",
        rows,
    )
    freeze = matrix.get("freeze_criteria", {})
    check(
        freeze.get("freeze_decision") == "locally_frozen"
        and freeze.get("active_freeze_label") == FREEZE_LABEL
        and freeze.get("next_allowed_route") == "theoretical_selector",
        "matrix_local_freeze",
        "Only the named shared-line route is locally frozen.",
        rows,
    )

    bridge = load_yaml(HERE / "v22_p4_t02_b2_typed_operational_bridge_v1.yaml")
    layers = bridge.get("bridge_layers", {})
    exact_layer = layers.get("exact_existing_protocol_bridge", {})
    extended_layer = layers.get("finite_preparation_extension_bridge", {})
    check(
        exact_layer.get("map_name") == "B_s^0"
        and exact_layer.get("status") == "typed_total_but_constant"
        and exact_layer.get("preserves_sample_information") is False
        and exact_layer.get("exact_protocol_modified") is False,
        "exact_bridge_layer",
        "The exact P7 bridge is total, constant, sample-forgetting, and non-mutating.",
        rows,
    )
    check(
        extended_layer.get("map_name") == "B_{s,N}^{ext}"
        and extended_layer.get("protocol_extension_adopted") is False
        and extended_layer.get("exact_protocol_modified") is False
        and "finite subset of Q" in str(extended_layer.get("rationalizer_image", "")),
        "finite_extension_bridge_layer",
        "The nontrivial finite-image bridge is an unadopted proposal-only extension.",
        rows,
    )
    check(
        extended_layer.get("zero_branch")
        == "all clipped-rationalized samples zero implies mu=delta_b0",
        "bridge_zero_branch",
        "The finite extension has an explicit zero branch.",
        rows,
    )
    bridge_limits = bridge.get("authority_limits", {})
    check(
        bridge.get("sector_domain", {}).get("full_p7_sector_bridge_claimed") is False
        and bridge_limits.get("exact_nonconstant_bridge_derived") is False
        and bridge_limits.get("finite_protocol_extension_adopted") is False,
        "bridge_scope_limits",
        "Full-sector, exact-nonconstant, and adoption overreads remain blocked.",
        rows,
    )

    obstruction = load_yaml(HERE / "v22_p4_t02_b2_line_selector_obstruction_v1.yaml")
    record = obstruction.get("obstruction_record", {})
    check(
        record.get("present") is True
        and record.get("obstruction_id") == OBSTRUCTION_ID
        and record.get("current_ontology_implication") == "does_not_derive"
        and record.get("source_extension_implication") == "new_primitive_required",
        "obstruction_record",
        "The exact current-ontology obstruction and extension implication are preserved.",
        rows,
    )
    theorems = obstruction.get("theorems", [])
    theorem_ids = {row.get("theorem_id") for row in theorems if isinstance(row, dict)}
    check(
        theorem_ids
        == {
            "THM-V22-P4T02-B2-NO-NATURAL-LINE-SELECTOR-001",
            "THM-V22-P4T02-B2-DIAGONAL-EMPTY-INTERIOR-001",
        },
        "obstruction_theorems",
        f"Observed theorem IDs: {sorted(str(value) for value in theorem_ids)}",
        rows,
    )
    branches = obstruction.get("refuter_failure_branches", {})
    check(
        set(branches)
        == {"collapse", "nonuniqueness", "inverse_defect", "cocycle_defect", "variation_fragility"},
        "refuter_branch_coverage",
        f"Observed branches: {sorted(branches)}",
        rows,
    )
    obstruction_freeze = obstruction.get("freeze_criteria_status", {})
    check(
        obstruction_freeze.get("freeze_decision") == "locally_frozen"
        and obstruction_freeze.get("active_freeze_label") == FREEZE_LABEL
        and obstruction.get("authority_limits", {}).get("global_no_go_claim_authorized") is False,
        "obstruction_local_not_global",
        "The obstruction triggers a local freeze and no global no-go.",
        rows,
    )

    model = load_model().run_checks()
    check(
        model.get("status") == "PASS"
        and model.get("check_count") == 10
        and model.get("failure_count") == 0
        and model.get("failed_check_ids") == [],
        "executable_model",
        f"Model status={model.get('status')} checks={model.get('check_count')} failures={model.get('failure_count')}",
        rows,
    )
    check(
        model.get("result_type") == "precise_obstruction"
        and model.get("obstruction_id") == OBSTRUCTION_ID,
        "model_decisive_result",
        "The executable model reproduces the decisive obstruction.",
        rows,
    )

    math_child = load_yaml(HERE / "child_phys_math_p4_t02_b2_source_intrinsic_interface_repair.yaml")
    phil_child = load_yaml(HERE / "child_phys_phil_p4_t02_b2_source_intrinsic_interface_repair.yaml")
    conflict = load_yaml(HERE / "parent_conflict_review_p4_t02_b2_source_intrinsic_interface_repair.yaml")
    check(
        math_child.get("status") == phil_child.get("status") == "completed",
        "child_outputs_complete",
        "Both internal perspectives completed.",
        rows,
    )
    check(
        conflict.get("unresolved_blocking_parent_conflicts") == []
        and conflict.get("blocking_conflict_count") == 0,
        "parent_conflicts_resolved",
        "No blocking parent-child conflict remains.",
        rows,
    )
    check(
        conflict.get("fused_result_type") == "precise_obstruction"
        and conflict.get("fused_obstruction_id") == OBSTRUCTION_ID
        and conflict.get("fused_freeze_label") == FREEZE_LABEL
        and conflict.get("fused_next_role") == "theoretical-continuation-selector@0.1.0",
        "parent_fusion_result",
        "Parent fusion preserves the obstruction, local freeze, and next role.",
        rows,
    )
    tension_ids = {
        row.get("tension_id")
        for row in conflict.get("resolved_tensions", [])
        if isinstance(row, dict)
    }
    check(
        tension_ids
        == {"T1-EXACT-PROTOCOL-VERSUS-NONTRIVIAL-SAMPLE-BRIDGE", "T2-RATIONALIZER-SPECIFICATION"},
        "parent_tensions_resolved",
        f"Resolved tension IDs: {sorted(str(value) for value in tension_ids)}",
        rows,
    )

    tex = (HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_v1.tex").read_text(encoding="utf-8")
    required_tex_tokens = [
        "compact-open first-jet topology",
        "B_s^0",
        "B_{s,N}^{\\rm ext}",
        "No natural line from fixed finite controls",
        "The common-line diagonal has empty interior",
        "OBST-V22-P4T02-B2-NATURAL-LINE-LOCK-001",
        "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
        "theoretical-",
        "not forbid a future conservative source extension",
    ]
    missing_tokens = [token for token in required_tex_tokens if token not in tex]
    check(
        not missing_tokens,
        "manuscript_payload",
        f"Missing manuscript tokens: {missing_tokens}",
        rows,
    )

    compile_receipt = load_json(HERE / "v22_p4_t02_b2_source_intrinsic_interface_repair_latex_compile_receipt.json")
    check(
        compile_receipt.get("status") == "PASS"
        and compile_receipt.get("page_count") == 7
        and compile_receipt.get("rendered_page_count") == 7,
        "latex_compile",
        "The scratch build passes with seven rendered letter pages.",
        rows,
    )
    check(
        compile_receipt.get("visual_inspection_status") == "PASS"
        and compile_receipt.get("visually_inspected_pages") == [1, 2, 3, 4, 5, 6, 7]
        and compile_receipt.get("overfull_box_count") == 0
        and compile_receipt.get("underfull_box_count") == 0,
        "latex_visual_and_layout",
        "All seven pages were inspected and no box warning remains.",
        rows,
    )

    task = load_yaml(TASK / "00_TASK.yaml")
    job = load_yaml(TASK / "jobs/AJ-RT-20260810-001-001.yaml")
    role = load_yaml(TASK / "roles/candidate-constructor@0.2.0--RT-20260810-001.yaml")
    completion = load_yaml(TASK / "jobs/completions/AJC-AJ-RT-20260810-001-001.yaml")
    handoff = load_yaml(REPO / "research_control/handoffs/handoff-0998.yaml")
    check(
        task.get("status") == job.get("status") == role.get("status") == "completed",
        "control_statuses",
        "Task, AgentJob, and role overlay are completed.",
        rows,
    )
    check(
        completion.get("status") == "completed"
        and completion.get("result") == "completed"
        and completion.get("candidate_constructor_result", {}).get("result_type") == "precise_obstruction",
        "completion_status",
        "Completion is terminalized with one precise obstruction.",
        rows,
    )
    check(
        completion.get("obstruction_record", {}).get("obstruction_id") == OBSTRUCTION_ID
        and completion.get("freeze_criteria_status", {}).get("freeze_decision") == "locally_frozen",
        "completion_obstruction_and_freeze",
        "Completion preserves the exact obstruction and local freeze.",
        rows,
    )
    selected = handoff.get("selected_next_route", {})
    check(
        selected.get("strategy_id")
        == "select_distinct_v22_p4_t02_b2_post_line_lock_obstruction_packet_v1"
        and selected.get("role_family") == "theoretical-continuation-selector@0.1.0"
        and selected.get("route_label") == "ordinary-research-packet",
        "successor_route",
        "Handoff selects one materially distinct theoretical selector route.",
        rows,
    )
    check(
        selected.get("executed") is False
        and selected.get("execution_ready_now") is False
        and selected.get("dependency_ready_after_checkpoint") is True,
        "successor_not_executed",
        "The theoretical selector is not executed in this invocation.",
        rows,
    )

    backlog = (REPO / "research_control/design/v22_recommendation_backlog.yaml").read_text(encoding="utf-8")
    program = (REPO / "research_control/program_state.yaml").read_text(encoding="utf-8")
    registry_job = (REPO / "registries/AGENT_JOB_REGISTRY.csv").read_text(encoding="utf-8")
    registry_claim = (REPO / "registries/CLAIM_BOUNDARY_REGISTRY.csv").read_text(encoding="utf-8")
    registry_tex = (REPO / "registries/TEX_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
    registry_md = (REPO / "registries/MARKDOWN_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
    check(
        "b2_source_intrinsic_interface_precise_obstruction_shared_tau_locally_frozen_checkpoint_pending" in backlog
        and "runtime_source_intrinsic_interface_repair_executed: true" in backlog
        and "runtime_theoretical_continuation_selector_executed: false" in backlog,
        "backlog_status",
        "Backlog records execution, precise obstruction, local freeze, and unexecuted selector.",
        rows,
    )
    check(
        "v22_p4_t02_b2_source_intrinsic_interface_repair" in program
        and "handoff-0998" in program
        and OBSTRUCTION_ID in program,
        "program_state",
        "Program state records RT-20260810-001, handoff-0998, and the exact obstruction.",
        rows,
    )
    check(
        "AJ-RT-20260810-001-001" in registry_job
        and "CB-V22-P4-T02-B2-SOURCE-INTRINSIC-INTERFACE-REPAIR-001" in registry_claim,
        "control_registries",
        "AgentJob and claim-boundary rows are registered.",
        rows,
    )
    check(
        "TEX-V22-P4-T02-B2-SOURCE-INTRINSIC-INTERFACE-REPAIR-V1" in registry_tex,
        "tex_registry",
        "The repair manuscript is registered.",
        rows,
    )
    check(
        "MD-V22-P4-T02-B2-PARENT-FUSION-SOURCE-INTRINSIC-INTERFACE-REPAIR-V1" in registry_md,
        "markdown_registry",
        "The parent-fusion source is registered.",
        rows,
    )

    failures = [row for row in rows if row["status"] != "PASS"]
    return {
        "schema_id": "v22_p4_t02_b2_source_intrinsic_interface_repair_validation_v1",
        "task_id": "RT-20260810-001",
        "job_id": "AJ-RT-20260810-001-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(rows),
        "pass_count": len(rows) - len(failures),
        "fail_count": len(failures),
        "failed_check_ids": [row["check_id"] for row in failures],
        "checks": rows,
        "tree_scope": "RT-20260810-001 source-interface payload and controls plus hash-bound P7, RT023, RT026, plan, and handoff inputs",
        "claim_effects": {
            "scientific_status_changed": False,
            "physical_status_changed": False,
            "distance_to_gr_changed": False,
            "source_intrinsic_topology_repaired": True,
            "exact_protocol_bridge_constant_only": True,
            "nontrivial_bridge_requires_finite_preparation_extension": True,
            "descriptor_instance_complete": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "local_freeze_applied": True,
            "global_no_go_claimed": False,
            "physics_promotion_authorized": False,
        },
    }


def write_outputs(report: dict[str, Any]) -> None:
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {
        "schema_id": "v22_p4_t02_b2_source_intrinsic_interface_repair_compact_receipt_v1",
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "status": report["status"],
        "check_count": report["check_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "failed_check_ids": report["failed_check_ids"],
        "result_type": "precise_obstruction",
        "obstruction_id": OBSTRUCTION_ID,
        "active_freeze_label": FREEZE_LABEL,
        "repair_finding_count": 5,
        "source_intrinsic_topology_repaired": True,
        "exact_protocol_bridge_constant_only": True,
        "nontrivial_bridge_requires_finite_preparation_extension": True,
        "descriptor_instance_complete": False,
        "adequacy_reevaluated": False,
        "b2_activated": False,
        "p4_t03_unlocked": False,
        "global_no_go_claimed": False,
        "next_role": "theoretical-continuation-selector@0.1.0",
        "next_role_executed": False,
    }
    COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        write_outputs(report)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: {report['pass_count']}/{report['check_count']} checks")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
