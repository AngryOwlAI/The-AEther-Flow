#!/usr/bin/env python3
"""Focused deterministic validator for the V22 P3-T03 refinement packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260809-015"
ART = TASK / "artifacts"
REPORT = ART / "v22_p3_t03_refinement_validation.json"
COMPACT = ART / "v22_p3_t03_compact_receipt.json"

EXPECTED_SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-0984.yaml": "5f57cb563b1b2fd0a12888bb59aea584cd6a40e4cd50cdb8fd79ab55a02feb1d",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_source_dynamics_without_hidden_geometry_v1.tex": "f26c77a175e7a5783e859eacc5de24270e1089a253e73493114a1403bbd61037",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_source_dynamics_specification_v1.yaml": "941e16e8a535622fcbcf6a5ac1802cd4bb86a5950af49260a22d2c69d279f46e",
    "research_control/design/gr_derivation_burden_map.md": "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
}

REQUIRED_ARTIFACTS = (
    "v22_p3_t03_controlled_refinement_limit_v1.tex",
    "v22_p3_t03_refinement_specification_v1.yaml",
    "v22_p3_t03_error_boundary_universality_ledger_v1.yaml",
    "v22_p3_t03_refinement_model.py",
    "v22_p3_t03_independent_solver.py",
    "fixtures/v22_p3_t03_refinement_cases.yaml",
    "child_phys_math_p3_t03_refinement.yaml",
    "child_phys_phil_p3_t03_source_purity.yaml",
    "validator_engineer_p3_t03_independent_evidence.yaml",
    "parent_conflict_review_p3_t03_refinement.yaml",
    "parent_fusion_notes_p3_t03_refinement.md",
    "v22_p3_t03_latex_compile_receipt.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping: {path}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected object: {path}")
    return value


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def build_report() -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    def check(check_id: str, condition: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    for relative, expected in EXPECTED_SOURCE_HASHES.items():
        path = ROOT / relative
        check(f"source_hash:{relative}", path.is_file() and sha256(path) == expected, expected)

    for relative in REQUIRED_ARTIFACTS:
        check(f"artifact_exists:{relative}", (ART / relative).is_file())

    task = load_yaml(TASK / "00_TASK.yaml")
    job = load_yaml(TASK / "jobs/AJ-RT-20260809-015-001.yaml")
    role = load_yaml(TASK / "roles/candidate-constructor@0.2.0--RT-20260809-015.yaml")
    spec_record = load_yaml(ART / "v22_p3_t03_refinement_specification_v1.yaml")
    ledger = load_yaml(ART / "v22_p3_t03_error_boundary_universality_ledger_v1.yaml")
    fixtures = load_yaml(ART / "fixtures/v22_p3_t03_refinement_cases.yaml")
    child_math = load_yaml(ART / "child_phys_math_p3_t03_refinement.yaml")
    child_phil = load_yaml(ART / "child_phys_phil_p3_t03_source_purity.yaml")
    validator_perspective = load_yaml(ART / "validator_engineer_p3_t03_independent_evidence.yaml")
    conflicts = load_yaml(ART / "parent_conflict_review_p3_t03_refinement.yaml")
    latex = load_json(ART / "v22_p3_t03_latex_compile_receipt.json")

    check("task_identity", task.get("task_id") == "RT-20260809-015")
    check("plan_identity", task.get("implementation_plan", {}).get("plan_task_id") == "P3-T03")
    check("job_identity", job.get("job_id") == "AJ-RT-20260809-015-001")
    check("role_identity", role.get("execution_role_ref") == job.get("execution_role_ref"))
    check("ordered_allowlist_parity", role.get("allowed_write_paths") == job.get("allowed_write_paths"))
    check("ordinary_route", job.get("route_label") == "ordinary-research-packet")
    check("milestone", job.get("target_derivation_milestone") == "effective_metric_g_eff")
    check("payload_admission", job.get("physics_payload_admission", {}).get("payload_type") == "candidate_construction")
    check("one_outer_job", job.get("role_decomposition", {}).get("mode") == "parent_child_parallel_synthesis")
    check("two_children", len(job.get("role_decomposition", {}).get("children", [])) == 2)

    primary = load_module("v22_p3_t03_primary", ART / "v22_p3_t03_refinement_model.py")
    independent = load_module("v22_p3_t03_independent", ART / "v22_p3_t03_independent_solver.py")
    primary_result = primary.evaluate_package()
    independent_result = independent.evaluate()
    contract = fixtures["predeclared_numerical_contract"]

    check("primary_status", primary_result.get("status") == "PASS")
    check("independent_status", independent_result.get("status") == "PASS")
    check("mesh_kinds", primary_result.get("mesh_kinds") == contract["mesh_kinds"])
    check("levels", primary_result.get("levels") == contract["levels"])
    check("nonzero_truncation", primary_result.get("nonzero_truncation_error_observed") is True)
    check("no_zero_remainder_overread", primary_result.get("finite_zero_remainder_used_as_limit_proof") is False)

    numerical_summary: list[dict[str, Any]] = []
    for study in primary_result["convergence_studies"]:
        kind = study["mesh_kind"]
        levels = study["levels"]
        check(f"{kind}:strict_decrease", study["strict_error_decrease"] is True)
        check(f"{kind}:terminal_order", study["observed_orders"][-1] >= contract["minimum_terminal_observed_order"], str(study["observed_orders"][-1]))
        for level in levels:
            n = level["n"]
            check(f"{kind}:{n}:positive_error", level["max_error"] > 0.0)
            check(f"{kind}:{n}:cfl", level["max_cfl"] <= contract["cfl_max"] + 1e-12, str(level["max_cfl"]))
            check(f"{kind}:{n}:mesh_ratio", level["max_mesh_ratio"] <= contract["mesh_ratio_max"] + 1e-12, str(level["max_mesh_ratio"]))
            for channel in level["channel_results"]:
                channel_id = channel["channel"]
                check(f"{kind}:{n}:channel{channel_id}:range_min", channel["final_min"] >= channel["initial_min"] - 1e-12)
                check(f"{kind}:{n}:channel{channel_id}:range_max", channel["final_max"] <= channel["initial_max"] + 1e-12)
        numerical_summary.append(
            {
                "mesh_kind": kind,
                "errors": [level["max_error"] for level in levels],
                "orders": study["observed_orders"],
                "mesh_ratios": [level["max_mesh_ratio"] for level in levels],
            }
        )

    boundary = primary_result["boundary_study"]
    check("boundary_strict_decrease", boundary["strict_error_decrease"] is True)
    check("boundary_outflow_unused", boundary["outflow_data_used"] is False)
    for level in boundary["levels"]:
        check(f"boundary:{level['n']}:positive_error", level["max_error"] > 0.0)
        check(f"boundary:{level['n']}:cfl", level["cfl"] <= contract["cfl_max"] + 1e-12)

    principal = primary_result["principal_study"]
    check("principal_factor_decrease", principal["factor_error_decreases"] is True)
    check("principal_product_decrease", principal["product_error_decreases"] is True)
    check("principal_no_cone", principal["physical_cone_inferred"] is False)
    check("principal_no_signature", principal["lorentzian_signature_inferred"] is False)
    for level in principal["levels"]:
        check(f"principal:{level['n']}:six_factors", level["factor_count"] == 6)
        check(f"principal:{level['n']}:positive_error", level["max_factor_error"] > 0.0)

    check("independent_no_primary_import", independent_result["implementation_independent_of_primary"] is True)
    check("independent_strict_decrease", independent_result["strict_error_decrease"] is True)
    check("independent_terminal_order", independent_result["observed_orders"][-1] >= contract["independent_minimum_terminal_order"])
    check("independent_source_clean", independent_result["target_geometry_inputs"] == 0)

    properties = primary_result["property_preservation"]
    check("physical_cone_precise_unresolved", properties["physical_causal_cone_status"] == "upstream_object_undefined_not_preserved_or_lost")
    check("signature_precise_unresolved", properties["lorentzian_signature_status"] == "upstream_object_undefined_not_preserved_or_lost")
    check("no_physical_property_promotion", properties["physical_property_promotion_authorized"] is False)
    purity = primary_result["source_purity"]
    for key in (
        "target_atlas_input_count",
        "target_metric_input_count",
        "physical_measure_input_count",
        "target_geometry_interpolation_count",
        "target_fit_count",
    ):
        check(f"source_purity:{key}", purity[key] == 0)
    check("source_purity:no_geff", purity["effective_metric_constructed"] is False)

    check("spec_exact_sampling", spec_record["comparison_maps"]["sampling"]["exact"] is True)
    check("spec_exact_reconstruction", spec_record["comparison_maps"]["reconstruction"]["exact"] is True)
    check("spec_no_target_interpolation", spec_record["comparison_maps"]["reconstruction"]["target_geometry_interpolation"] is False)
    check("spec_limit_not_target", spec_record["continuum_limit"]["defined_by_target_agreement"] is False)
    check("ledger_entries", len(ledger["entries"]) >= 12)
    check("child_math_complete", child_math.get("status") == "completed")
    check("child_phil_complete", child_phil.get("status") == "completed")
    check("validator_perspective_complete", validator_perspective.get("status") == "completed")
    check("validator_semantics_unchanged", validator_perspective.get("global_validator_semantics_changed") is False)
    check("conflicts_resolved", conflicts.get("status") == "resolved")
    check("no_blocking_conflict", conflicts.get("blocking_conflict_count") == 0 and conflicts.get("unresolved_conflicts") == [])
    check("latex_pass", latex.get("status") == "PASS")
    check("latex_six_pages", latex.get("page_count") == 6)
    check("latex_layout_clean", latex.get("final_pass_overfull_count") == 0 and latex.get("final_pass_underfull_count") == 0)
    check("latex_no_tracked_pdf", latex.get("tracked_pdf_created") is False)

    tex_text = (ART / "v22_p3_t03_controlled_refinement_limit_v1.tex").read_text(encoding="utf-8")
    fusion_text = (ART / "parent_fusion_notes_p3_t03_refinement.md").read_text(encoding="utf-8")
    for phrase in (
        "Controlled source-semigroup convergence",
        "Protected finite-size window",
        "upstream\\_object",
        "constructed candidate",
        "not establish a physical cone",
    ):
        check(f"tex_phrase:{phrase}", phrase in tex_text)
    check("fusion_no_blocking_conflict", "No blocking conflict remains" in fusion_text)
    check("fusion_routes_p3_t04", "P3-T04" in fusion_text)

    failures = [item for item in checks if item["status"] != "PASS"]
    input_paths = [ART / relative for relative in REQUIRED_ARTIFACTS]
    return {
        "schema_id": "v22_p3_t03_refinement_validation_v1",
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260809-015",
        "job_id": "AJ-RT-20260809-015-001",
        "generated_at": "2026-08-09T16:20:00Z",
        "counts": {
            "check_count": len(checks),
            "failure_count": len(failures),
            "mesh_family_count": len(primary_result["convergence_studies"]),
            "primary_channel_run_count": sum(len(level["channel_results"]) for study in primary_result["convergence_studies"] for level in study["levels"]),
            "boundary_level_count": len(boundary["levels"]),
            "principal_level_count": len(principal["levels"]),
            "independent_level_count": len(independent_result["levels"]),
            "resolved_conflict_count": conflicts["resolved_conflict_count"],
            "unresolved_conflict_count": len(conflicts["unresolved_conflicts"]),
        },
        "numerical_summary": numerical_summary,
        "boundary_errors": [level["max_error"] for level in boundary["levels"]],
        "principal_factor_errors": [level["max_factor_error"] for level in principal["levels"]],
        "independent_errors": [level["max_error"] for level in independent_result["levels"]],
        "independent_orders": independent_result["observed_orders"],
        "causal_signature_status": {
            "physical_causal_cone": properties["physical_causal_cone_status"],
            "lorentzian_signature": properties["lorentzian_signature_status"],
        },
        "input_hashes": {
            str(path.relative_to(ROOT)): sha256(path) for path in input_paths
        },
        "checks": checks,
        "failures": failures,
        "authority": {
            "scientific_truth_inferred_from_validator": False,
            "source_extension_adopted": False,
            "physical_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "effective_metric_constructed": False,
        },
    }


def render(report: dict[str, Any]) -> tuple[str, str]:
    report_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    report_hash = hashlib.sha256(report_text.encode("utf-8")).hexdigest()
    compact = {
        "schema_id": "v22_p3_t03_compact_receipt_v1",
        "status": report["status"],
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "report_path": str(REPORT.relative_to(ROOT)),
        "report_sha256": report_hash,
        "counts": report["counts"],
        "failed_check_ids": [item["check_id"] for item in report["failures"]],
        "causal_signature_status": report["causal_signature_status"],
        "authority_note": "Focused validation is operational evidence only and creates no physics or promotion authority.",
    }
    return report_text, json.dumps(compact, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    report_text, compact_text = render(report)
    if args.write:
        REPORT.write_text(report_text, encoding="utf-8")
        COMPACT.write_text(compact_text, encoding="utf-8")
    else:
        if not REPORT.is_file() or not COMPACT.is_file():
            report["status"] = "FAIL"
            report.setdefault("failures", []).append({"check_id": "tracked_receipts_exist", "status": "FAIL", "detail": ""})
        elif REPORT.read_text(encoding="utf-8") != report_text or COMPACT.read_text(encoding="utf-8") != compact_text:
            report["status"] = "FAIL"
            report.setdefault("failures", []).append({"check_id": "tracked_receipts_fresh", "status": "FAIL", "detail": ""})

    summary = {
        "status": report["status"],
        "check_count": report["counts"]["check_count"],
        "failure_count": len(report.get("failures", [])),
        "failed_check_ids": [item["check_id"] for item in report.get("failures", [])],
        "report_path": str(REPORT.relative_to(ROOT)),
        "compact_path": str(COMPACT.relative_to(ROOT)),
    }
    print(json.dumps(summary, indent=2, sort_keys=True) if args.json else summary["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
