#!/usr/bin/env python3
"""Focused validator for RT-20260816-005."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260816-005"
ART = TASK / "artifacts"
sys.dont_write_bytecode = True


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, check_id: str, checks: list[dict[str, str]], detail: str = ""):
    checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    checks: list[dict[str, str]] = []

    paths = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260816-005-001.yaml",
        "role": TASK / "roles/refuter@0.2.0--RT-20260816-005.yaml",
        "matrix": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress_matrix_v1.yaml",
        "disposition": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress_disposition_v1.yaml",
        "model": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress_model.py",
        "tex": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress_v1.tex",
        "child_math": ART / "child_phys_math_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress.yaml",
        "child_phil": ART / "child_phys_phil_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress.yaml",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress.md",
        "provenance": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress_provenance_manifest_v1.yaml",
        "compile": ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress_latex_compile_receipt.json",
        "documentation": TASK / "documentation_impact.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260816-005-001.yaml",
        "handoff": ROOT / "research_control/handoffs/handoff-1048.yaml",
    }
    for name, path in paths.items():
        check(path.exists(), f"exists_{name}", checks, str(path.relative_to(ROOT)))
    if not all(path.exists() for path in paths.values()):
        payload = {"status": "FAIL", "checks": checks}
        print(json.dumps(payload, indent=2))
        return 1

    parsed = {}
    for name in ("task", "job", "role", "matrix", "disposition", "child_math", "child_phil", "conflict", "provenance", "documentation", "completion", "handoff"):
        try:
            parsed[name] = load_yaml(paths[name])
            check(True, f"yaml_{name}", checks)
        except Exception as exc:
            check(False, f"yaml_{name}", checks, str(exc))

    task = parsed["task"]
    job = parsed["job"]
    role = parsed["role"]
    matrix = parsed["matrix"]
    disposition = parsed["disposition"]
    conflict = parsed["conflict"]
    completion = parsed["completion"]
    handoff = parsed["handoff"]
    provenance = parsed["provenance"]

    check(task.get("status") == "completed", "task_completed", checks)
    check(job.get("status") == "completed", "job_completed", checks)
    check(role.get("status") == "expired", "role_expired", checks)
    check(task.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED", "task_validation", checks)
    check(job.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED", "job_validation", checks)
    check(role.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED", "role_validation", checks)
    check(job.get("allowed_write_paths") == role.get("allowed_write_paths"), "ordered_allowlist_parity", checks)
    check(job.get("role_decomposition", {}).get("mode") == "parent_child_parallel_synthesis", "parent_child_mode", checks)
    check(len(job.get("role_decomposition", {}).get("children", [])) == 2, "two_children", checks)

    check(matrix.get("decisive_result_class") == "scoped_obstruction", "matrix_result", checks)
    check(len(matrix.get("stress_branches", [])) == 10, "ten_stress_branches", checks)
    check(len(matrix.get("new_mathematical_payload", [])) == 6, "six_payloads", checks)
    check(len(matrix.get("preserved_freezes", [])) == 8, "eight_inherited_freezes", checks)
    check(matrix.get("new_candidate_local_freeze", {}).get("status") == "active_new_local_freeze", "new_local_freeze", checks)
    dgr = matrix.get("distance_to_gr_status", [])
    check(len(dgr) == 14, "fourteen_distance_rows", checks)
    check(all(row.get("task_delta") == "no_delta" for row in dgr), "all_distance_no_delta", checks)
    check(matrix.get("selected_successor", {}).get("status") == "selected_not_executed", "matrix_successor_unexecuted", checks)
    check(matrix.get("authority_limits", {}).get("global_no_go_claimed") is False, "matrix_no_global_nogo", checks)

    result = disposition.get("refuter_stress_result", {})
    check(result.get("result_type") == "scoped_obstruction" and result.get("selected_class_count") == 1, "disposition_one_result", checks)
    obstruction = disposition.get("refuter_obstruction_record", {})
    required_obstruction = {
        "obstruction_id", "target_claim", "target_milestone", "failed_premise",
        "minimal_countermodel_available", "countermodel_path", "countermodel_scope",
        "certificate_gap", "source_extension_repair_possible",
        "global_no_go_claim_authorized", "future_source_extension_impossibility_authorized",
        "freeze_criteria_status", "route_cycle_control", "forbidden_conclusions",
    }
    check(required_obstruction.issubset(obstruction), "obstruction_schema", checks)
    check(obstruction.get("minimal_countermodel_available") is True and bool(obstruction.get("countermodel_path")), "countermodel_bound", checks)
    check(obstruction.get("global_no_go_claim_authorized") is False, "no_global_nogo_authority", checks)
    check(obstruction.get("future_source_extension_impossibility_authorized") is False, "no_future_impossibility_authority", checks)
    check(disposition.get("freeze_criteria_status", {}).get("active_freeze_count_after_result") == 9, "nine_total_freezes", checks)
    check(len(disposition.get("distance_to_gr_status", [])) == 14, "disposition_distance_rows", checks)

    for name in ("child_math", "child_phil"):
        text = paths[name].read_text(encoding="utf-8")
        check("scoped_obstruction" in text, f"{name}_result", checks)
        check("OB-V22-P4T02-B2-MEASURABLE-FIBER-OCCURRENCE-LAW-ROBUST-SELECTION-EMBEDDABILITY-001" in text, f"{name}_obstruction_id", checks)
        check("NDCL-V22-P4T02-B2-MEASURABLE-FIBER-OCCURRENCE-LAW-ROBUST-SELECTION-EMBEDDABILITY" in text, f"{name}_freeze_id", checks)
        check("PKT-V22-P4T02-B2-POST-MEASURABLE-FIBER-OCCURRENCE-LAW-REFUTER-THEORETICAL-CONTINUATION-SELECTION-V1" in text, f"{name}_successor_id", checks)

    check(conflict.get("unresolved_blocking_conflict_count") == 0, "zero_blocking_conflicts", checks)
    check(conflict.get("fused_result") == "scoped_obstruction", "conflict_fused_result", checks)
    check(completion.get("status") == "completed", "completion_status", checks)
    check(completion.get("scientific_result", {}).get("result_type") == "scoped_obstruction", "completion_result", checks)
    check(handoff.get("task_id") == "RT-20260816-005", "handoff_task", checks)
    check(handoff.get("required_next_packet", {}).get("executed") is False, "handoff_successor_unexecuted", checks)

    spec = importlib.util.spec_from_file_location("rt005_model", paths["model"])
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    model = module.run_checks()
    check(model.get("check_count") == 25 and model.get("pass_count") == 25 and model.get("fail_count") == 0, "model_25_of_25", checks, model.get("payload_sha256", ""))
    check(model.get("payload_sha256") == "8b276a37ca52b8c2eaed25928777c8951021912480ddf08c17ba6d54a2f35766", "model_payload", checks)

    tex = paths["tex"].read_text(encoding="utf-8")
    for phrase in (
        "d_{\\TV}(J_a,J_b)=2|a-b|",
        "K_p^n=K_{1-p}^n",
        "if and only if $p>1/2$",
        "scoped\\_obstruction",
        "No program-wide no-go",
    ):
        check(phrase in tex, f"tex_phrase_{hashlib.sha1(phrase.encode()).hexdigest()[:8]}", checks, phrase)

    compile_receipt = json.loads(paths["compile"].read_text(encoding="utf-8"))
    check(compile_receipt.get("status") == "PASS", "latex_compile", checks)
    check(compile_receipt.get("visual_inspection", {}).get("status") == "PASS", "latex_visual", checks)

    manifest_rows = provenance.get("governing_sources", [])
    all_hashes = True
    for row in manifest_rows:
        source = ROOT / row["path"]
        all_hashes = all_hashes and source.exists() and sha(source) == row["sha256"]
    check(bool(manifest_rows) and all_hashes, "provenance_hashes", checks, f"{len(manifest_rows)} sources")

    for path in TASK.rglob("*"):
        if path.is_file() and path.suffix not in {".pyc", ".pyo"} and "__pycache__" not in path.parts:
            text = path.read_text(encoding="utf-8", errors="ignore")
            check("\t" not in text and all(line == line.rstrip() for line in text.splitlines()), f"whitespace_{path.name}", checks)

    tex_registry = (ROOT / "registries/TEX_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
    md_registry = (ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
    check("TEX-V22-P4-T02-B2-PROPOSAL-ONLY-MEASURABLE-FIBER-OCCURRENCE-LAW-REFUTER-STRESS-V1" in tex_registry, "tex_registry_row", checks)
    check("MD-V22-P4-T02-B2-PARENT-FUSION-PROPOSAL-ONLY-MEASURABLE-FIBER-OCCURRENCE-LAW-REFUTER-STRESS-V1" in md_registry, "markdown_registry_row", checks)

    failed = [row for row in checks if row["status"] != "PASS"]
    payload = {
        "schema_id": "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress_validation_v1",
        "task_id": "RT-20260816-005",
        "job_id": "AJ-RT-20260816-005-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "checks": checks,
        "authority": "validation_receipt_only",
    }
    if args.write:
        report = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_refuter_stress_validation.json"
        report.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
