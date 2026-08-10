#!/usr/bin/env python3
"""Focused validator for RT-20260809-026."""

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
REPORT = HERE / "v22_p4_t02_b2_populated_instance_audit_validation.json"
COMPACT = HERE / "v22_p4_t02_b2_populated_instance_audit_compact_receipt.json"


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
    path = HERE / "v22_p4_t02_b2_populated_instance_audit_model.py"
    spec = importlib.util.spec_from_file_location("rt026_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load model")
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
        HERE / "v22_p4_t02_b2_populated_instance_smuggling_audit_v1.tex",
        HERE / "v22_p4_t02_b2_populated_instance_audit_matrix_v1.yaml",
        HERE / "v22_p4_t02_b2_sector_split_and_presentation_countermodels_v1.yaml",
        HERE / "v22_p4_t02_b2_operational_interface_obstruction_v1.yaml",
        HERE / "v22_p4_t02_b2_populated_instance_audit_disposition_v1.yaml",
        HERE / "v22_p4_t02_b2_populated_instance_audit_model.py",
        HERE / "child_phys_math_p4_t02_b2_populated_instance_audit.yaml",
        HERE / "child_phys_phil_p4_t02_b2_populated_instance_audit.yaml",
        HERE / "parent_conflict_review_p4_t02_b2_populated_instance_audit.yaml",
        HERE / "parent_fusion_notes_p4_t02_b2_populated_instance_audit.md",
        HERE / "v22_p4_t02_b2_populated_instance_audit_latex_compile_receipt.json",
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260809-026.md",
        TASK / "documentation_impact.yaml",
        TASK / "roles/smuggling-auditor@0.2.0--RT-20260809-026.yaml",
        TASK / "jobs/AJ-RT-20260809-026-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260809-026-001.yaml",
        REPO / "research_control/handoffs/handoff-0996.yaml",
        REPO / "research_control/handoffs/handoff-0996.md",
    ]
    check(all(path.is_file() for path in required), "required_files", "All task, synthesis, receipt, completion, and handoff files exist.", rows)

    source_hashes = {
        "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
        "research_control/handoffs/handoff-0995.yaml": "14ecd144792ed6292b4b17407be243e023897e1aa09943af92ae39891444039f",
        "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_equipped_chain_descriptor_attempt_v1.tex": "6b35e208631b287cd4ec5c6e27bc73c8389c555cad1c8a3cde24021e35be4169",
        "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_equipped_chain_descriptor_population_v1.yaml": "fde2dbbfb1622f6877067408db184d24d477d40acaee953d48585385c4ceeed9",
        "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_atomic_obligation_construction_matrix_v1.yaml": "ce44c482a60ff04f1228ed68d4adbc510f3c4350c2278927ed38e611e5a19219",
        "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_source_factorization_provenance_v1.yaml": "023084b678b9771796652520e1df0c876f2425f622e6431ff59fc2c95d905245",
        "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_explicit_unit_cocycle_v1.yaml": "1e070af78bcb24d426f44123f3186dfbefb6244192cc77cf1983ec095681f07f",
        "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_d7_separation_obstruction_v1.yaml": "95577e04db61fdc37d8597a367dfd0025fbdeb30f8c9ce9e1d86806cb6b52dc2",
    }
    mismatches = [
        relative
        for relative, expected in source_hashes.items()
        if not (REPO / relative).is_file() or sha256(REPO / relative) != expected
    ]
    check(not mismatches, "immutable_source_hashes", f"Immutable mismatch list: {mismatches}", rows)

    matrix = load_yaml(HERE / "v22_p4_t02_b2_populated_instance_audit_matrix_v1.yaml")
    components = matrix.get("components", [])
    counts = matrix.get("anchored_audit_counts", {})
    check(len(components) == 10, "component_count", f"Observed {len(components)} populated component rows.", rows)
    verdicts = [item.get("anchored_verdict") for item in components if isinstance(item, dict)]
    check(verdicts.count("repair_required") == 5, "repair_count", f"Anchored verdicts: {verdicts}", rows)
    check(verdicts.count("pass") == 4 and verdicts.count("conditional") == 1, "pass_conditional_count", f"Counts: {counts}", rows)
    check(matrix.get("exact_verdict") == "repair_required_no_instance_credit", "matrix_verdict", "Matrix preserves the exact verdict.", rows)
    check(matrix.get("direct_target_import_count") == 0 and matrix.get("direct_authority_import_count") == 0, "direct_import_counts", "No direct target or authority import is alleged.", rows)

    countermodels = load_yaml(HERE / "v22_p4_t02_b2_sector_split_and_presentation_countermodels_v1.yaml")
    countermodel_rows = countermodels.get("countermodels", [])
    check(len(countermodel_rows) == 3, "countermodel_count", f"Observed {len(countermodel_rows)} exact countermodels.", rows)
    check(all(not item.get("target_geometry_used", True) for item in countermodel_rows), "countermodels_source_only", "All countermodels avoid target geometry.", rows)
    check(countermodels.get("repair_scope", {}).get("freeze_now") is False, "freeze_decision", "No premature family freeze.", rows)

    obstruction = load_yaml(HERE / "v22_p4_t02_b2_operational_interface_obstruction_v1.yaml")
    check(obstruction.get("exact_result") == "composition_undefined_under_declared_types", "operational_type_result", "The missing bridge is stated as a type obstruction.", rows)
    check(obstruction.get("missing_interface", {}).get("declared_in_subject") is False, "operational_bridge_absent", "B_s is absent from the audited subject.", rows)

    disposition = load_yaml(HERE / "v22_p4_t02_b2_populated_instance_audit_disposition_v1.yaml")
    findings = disposition.get("repair_blocking_findings", [])
    claim_boundary = disposition.get("claim_boundary", {})
    check(len(findings) == 5, "finding_count", f"Observed {len(findings)} repair-blocking findings.", rows)
    check(disposition.get("exact_verdict") == "repair_required_no_instance_credit", "disposition_verdict", "Disposition uses the exact guarded verdict.", rows)
    check(disposition.get("source_extension_classification") == "new_ontology_primitives_with_repairable_goal_property_preload", "source_extension_classification", "Goal-property preload is distinguished from target import.", rows)
    blocked_flags = [
        not claim_boundary.get("descriptor_instance_complete", True),
        not claim_boundary.get("adequacy_reevaluated", True),
        not claim_boundary.get("b2_activated", True),
        not claim_boundary.get("p4_t03_unlocked", True),
        not claim_boundary.get("global_no_go_claimed", True),
    ]
    check(all(blocked_flags), "downstream_blocks", "Instance, adequacy, activation, P4-T03, and global no-go remain false.", rows)

    model = load_model().build_witness()
    check(model.identity_is_unique_pointwise_fixer, "model_carrier_automorphism", "Identity is the unique pointwise equipment fixer.", rows)
    check(model.lift_sampling_identity and model.cocycle_pass, "model_scoped_algebra", "Lift/sampling and unit cocycle passes reproduce.", rows)
    check(model.presentation_countermodel_pass, "model_presentation_counterexample", "3/8 crosses the threshold after the factor-two rescaling.", rows)
    check(model.generators_pairwise_nonassociate and not model.commonity_under_sector_split, "model_sector_split_counterexample", "The three perturbed linear generators are pairwise nonassociate.", rows)
    check(not model.operational_types_compose_without_bridge, "model_operational_type", "No composition is admitted without B_s.", rows)

    tex = (HERE / "v22_p4_t02_b2_populated_instance_smuggling_audit_v1.tex").read_text(encoding="utf-8")
    required_tex_tokens = [
        "Weak source-fiber factorization",
        "Anchored source derivation",
        "Coordinate-rescaling witness",
        "Shared-leading-factor preload",
        "Sector-split countermodel",
        "Operational interface obstruction",
        "repair\\_required\\_no\\_instance\\_credit",
        "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    ]
    missing_tokens = [token for token in required_tex_tokens if token not in tex]
    check(not missing_tokens, "manuscript_payload", f"Missing manuscript tokens: {missing_tokens}", rows)

    math_child = load_yaml(HERE / "child_phys_math_p4_t02_b2_populated_instance_audit.yaml")
    phil_child = load_yaml(HERE / "child_phys_phil_p4_t02_b2_populated_instance_audit.yaml")
    conflict = load_yaml(HERE / "parent_conflict_review_p4_t02_b2_populated_instance_audit.yaml")
    check(math_child.get("status") == phil_child.get("status") == "completed", "child_outputs_complete", "Both internal perspectives completed.", rows)
    check(conflict.get("unresolved_blocking_parent_conflicts") == [], "parent_conflicts_resolved", "No blocking synthesis conflict remains.", rows)
    check(conflict.get("fused_verdict") == "repair_required_no_instance_credit", "fused_verdict", "Parent fusion preserves the exact verdict.", rows)

    compile_receipt = load_json(HERE / "v22_p4_t02_b2_populated_instance_audit_latex_compile_receipt.json")
    check(compile_receipt.get("status") == "PASS", "latex_compile", "Scratch compile passed.", rows)
    check(compile_receipt.get("visual_inspection_status") == "PASS", "latex_visual", "Rendered pages were visually inspected.", rows)

    task = load_yaml(TASK / "00_TASK.yaml")
    job = load_yaml(TASK / "jobs/AJ-RT-20260809-026-001.yaml")
    role = load_yaml(TASK / "roles/smuggling-auditor@0.2.0--RT-20260809-026.yaml")
    completion = load_yaml(TASK / "jobs/completions/AJC-AJ-RT-20260809-026-001.yaml")
    handoff = load_yaml(REPO / "research_control/handoffs/handoff-0996.yaml")
    check(task.get("status") == job.get("status") == role.get("status") == "completed", "control_statuses", "Task, AgentJob, and role overlay are completed.", rows)
    check(completion.get("status") == "completed" and completion.get("result") == "completed", "completion_status", "Completion is terminalized precheckpoint.", rows)
    check(handoff.get("selected_next_route", {}).get("strategy_id") == "repair_v22_p4_t02_b2_populated_descriptor_source_intrinsic_interfaces_v1", "successor_route", "Handoff selects the guarded repair route.", rows)
    check(handoff.get("selected_next_route", {}).get("executed") is False, "successor_not_executed", "The repair route was not executed in this invocation.", rows)

    backlog = (REPO / "research_control/design/v22_recommendation_backlog.yaml").read_text(encoding="utf-8")
    program = (REPO / "research_control/program_state.yaml").read_text(encoding="utf-8")
    registry_tex = (REPO / "registries/TEX_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
    registry_md = (REPO / "registries/MARKDOWN_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
    check("b2_populated_instance_audit_repair_required_no_instance_credit" in backlog, "backlog_status", "Backlog records the exact audit outcome.", rows)
    check("v22_p4_t02_b2_populated_instance_smuggling_audit" in program and "handoff-0996" in program, "program_state", "Program state records RT026 and handoff-0996.", rows)
    check("TEX-V22-P4-T02-B2-POPULATED-INSTANCE-SMUGGLING-AUDIT-V1" in registry_tex, "tex_registry", "Audit manuscript is registered.", rows)
    check("MD-V22-P4-T02-B2-PARENT-FUSION-POPULATED-INSTANCE-AUDIT-V1" in registry_md, "markdown_registry", "Parent fusion source is registered.", rows)

    failures = [row for row in rows if row["status"] != "PASS"]
    return {
        "schema_id": "v22_p4_t02_b2_populated_instance_audit_validation_v1",
        "task_id": "RT-20260809-026",
        "job_id": "AJ-RT-20260809-026-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(rows),
        "pass_count": len(rows) - len(failures),
        "fail_count": len(failures),
        "checks": rows,
        "tree_scope": "RT-20260809-026 audit artifacts and control records plus immutable RT-023 subject hashes",
        "claim_effects": {
            "scientific_status_changed": False,
            "physical_status_changed": False,
            "distance_to_gr_changed": False,
            "descriptor_instance_complete": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "physics_promotion_authorized": False,
        },
    }


def write_outputs(report: dict[str, Any]) -> None:
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {
        "schema_id": "v22_p4_t02_b2_populated_instance_audit_compact_receipt_v1",
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "status": report["status"],
        "check_count": report["check_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "exact_verdict": "repair_required_no_instance_credit",
        "repair_blocking_finding_count": 5,
        "direct_target_import_count": 0,
        "direct_authority_import_count": 0,
        "descriptor_instance_complete": False,
        "adequacy_reevaluated": False,
        "b2_activated": False,
        "p4_t03_unlocked": False,
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
