#!/usr/bin/env python3
"""Validate the bounded V22 P4-T02 post-line-lock selector transaction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260810-002"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_post_line_lock_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_post_line_lock_selector_compact_receipt.json"
GENERATED_AT = "2026-08-10T07:44:48Z"

DECISION = ART / "v22_p4_t02_b2_post_line_lock_selector_decision_v1.yaml"
COMPARISON = ART / "v22_p4_t02_b2_post_line_lock_route_comparison_v1.yaml"
PACKET = ART / "v22_p4_t02_b2_common_hyperbolicity_envelope_packet_v1.yaml"
PROVENANCE = ART / "v22_p4_t02_b2_post_line_lock_source_provenance_manifest_v1.yaml"
MODEL = ART / "v22_p4_t02_b2_post_line_lock_selector_model.py"
TEX = ART / "v22_p4_t02_b2_post_line_lock_route_selection_v1.tex"
CHILD_MATH = ART / "child_phys_math_p4_t02_b2_post_line_lock_selector.yaml"
CHILD_PHIL = ART / "child_phys_phil_p4_t02_b2_post_line_lock_selector.yaml"
CONFLICT = ART / "parent_conflict_review_p4_t02_b2_post_line_lock_selector.yaml"
FUSION = ART / "parent_fusion_notes_p4_t02_b2_post_line_lock_selector.md"
COMPILE = ART / "v22_p4_t02_b2_post_line_lock_selector_latex_compile_receipt.json"

EXPECTED_SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-0998.yaml":
        "46bdd9daaecb8a8563c0c00b6c054e23a6ba009e2afe9961cdf42823716d2ab7",
    "research_control/tasks/RT-20260810-001/artifacts/v22_p4_t02_b2_source_intrinsic_interface_repair_v1.tex":
        "f1b8d1e851a56109e0976ff4cfde8ff2adce4e1376581547f048c55a6a0b3497",
    "research_control/tasks/RT-20260810-001/artifacts/v22_p4_t02_b2_line_selector_obstruction_v1.yaml":
        "3c4d53632f274ce2fa49612f369363e4b3c7ebdffd7a451c102f791f0e0f6b1e",
    "research_control/tasks/RT-20260810-001/artifacts/v22_p4_t02_b2_typed_operational_bridge_v1.yaml":
        "60a891df7a590c43917c4cb6e0f9ac25e61bcbf328711718d5ad947123d00a08",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_equipped_chain_descriptor_attempt_v1.tex":
        "6b35e208631b287cd4ec5c6e27bc73c8389c555cad1c8a3cde24021e35be4169",
    "research_control/tasks/RT-20260809-019/artifacts/v22_p4_t02_hyperbolicity_universality_robustness_hard_fail_screen_v1.tex":
        "6eec0961cd84b3ec8f88845de1e5f87c13fee009b151fa557655d09a0fa6b50a",
    "research_control/tasks/RT-20260809-009/artifacts/v22_p2_t04_fallback_matter_principal_candidate_v1.yaml":
        "11917a5c868b6ed50633e1b7528b59079db40f10c003c32176d1887df5dae6e5",
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
        DECISION, COMPARISON, PACKET, PROVENANCE, MODEL, TEX, CHILD_MATH,
        CHILD_PHIL, CONFLICT, FUSION, COMPILE,
    ]
    for path in core_paths:
        check(f"exists_{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    yaml_paths = [DECISION, COMPARISON, PACKET, PROVENANCE, CHILD_MATH, CHILD_PHIL, CONFLICT]
    loaded: dict[str, dict[str, Any]] = {}
    for path in yaml_paths:
        try:
            loaded[path.name] = load_yaml(path)
            check(f"yaml_{path.name}", True, "parsed")
        except Exception as exc:
            loaded[path.name] = {}
            check(f"yaml_{path.name}", False, str(exc))

    decision = loaded[DECISION.name]
    comparison = loaded[COMPARISON.name]
    packet = loaded[PACKET.name]
    provenance = loaded[PROVENANCE.name]
    child_math = loaded[CHILD_MATH.name]
    child_phil = loaded[CHILD_PHIL.name]
    conflict = loaded[CONFLICT.name]

    check("decision_identity", decision.get("decision_id") == "V22-P4-T02-B2-POST-LINE-LOCK-PACKET-SELECTION-001", decision.get("decision_id"))
    check("plan_task", decision.get("plan_task_id") == "P4-T02", decision.get("plan_task_id"))
    check("selected_candidate", get_path(decision, "selected_path", "candidate_id") == "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1", get_path(decision, "selected_path", "candidate_id"))
    check("selected_packet_type", get_path(decision, "theoretical_decision_output", "selected_next_packet_type") == "source_extension_candidate", get_path(decision, "theoretical_decision_output", "selected_next_packet_type"))
    check("selected_role", get_path(decision, "selected_path", "next_role_family") == "candidate-constructor@0.2.0", get_path(decision, "selected_path", "next_role_family"))
    check("selected_route_label", get_path(decision, "selected_path", "route_label") == "ontology-law-research-packet", get_path(decision, "selected_path", "route_label"))
    check("selected_not_executed", get_path(decision, "selected_path", "execution_authorized_in_this_task") is False, get_path(decision, "selected_path", "execution_authorized_in_this_task"))
    check("claim_blocks_preserved", get_path(decision, "theoretical_decision_output", "preserves_claim_blocks") is True, get_path(decision, "theoretical_decision_output", "preserves_claim_blocks"))
    check("human_gate_not_required", get_path(decision, "theoretical_decision_output", "requires_human_gate") is False, get_path(decision, "theoretical_decision_output", "requires_human_gate"))
    check("source_extension_class", get_path(decision, "source_extension_decision", "category") == "new_ontology_primitive_candidate", get_path(decision, "source_extension_decision", "category"))
    check("no_target_import", get_path(decision, "source_extension_decision", "target_gr_import_detected_in_selector") is False, get_path(decision, "source_extension_decision", "target_gr_import_detected_in_selector"))

    routes = comparison.get("routes", [])
    selected_routes = [row for row in routes if isinstance(row, dict) and row.get("disposition") == "selected"]
    check("one_route_selected", len(selected_routes) == 1, len(selected_routes))
    if selected_routes:
        check("comparison_selected_envelope", selected_routes[0].get("route_id") == "CONSTRUCT_COMMON_HYPERBOLICITY_ENVELOPE", selected_routes[0].get("route_id"))
    frozen = [row for row in routes if isinstance(row, dict) and row.get("route_id") == "REPLAY_SHARED_LINE_LOCK"]
    check("shared_line_excluded", bool(frozen) and frozen[0].get("disposition") == "excluded_by_local_freeze", frozen[0].get("disposition") if frozen else None)
    check("global_no_go_not_selected", any(row.get("route_id") == "PROVE_BROADER_B2_NO_GO" and str(row.get("disposition", "")).startswith("not_selected") for row in routes if isinstance(row, dict)), "route comparison")

    lemma = packet.get("product_hyperbolicity_lemma", {})
    check("lemma_identity", lemma.get("lemma_id") == "LEM-V22-P4T02-B2-COMMON-HYPERBOLICITY-PRODUCT-001", lemma.get("lemma_id"))
    check("lemma_hypotheses", len(lemma.get("hypotheses", [])) >= 3, len(lemma.get("hypotheses", [])))
    check("lemma_conclusion", "intersection" in str(lemma.get("conclusion", "")), lemma.get("conclusion"))
    check("packet_selected_not_executed", packet.get("packet_status") == "selected_not_executed", packet.get("packet_status"))
    check("packet_result_binary", packet.get("result_contract", {}).get("permitted_result_types") == ["constructed_candidate", "precise_obstruction"], get_path(packet, "result_contract", "permitted_result_types"))
    check("packet_adequacy_block", get_path(packet, "authority_limits", "adequacy_reevaluated") is False, get_path(packet, "authority_limits", "adequacy_reevaluated"))
    check("packet_physical_cone_block", get_path(packet, "authority_limits", "physical_cone_constructed") is False, get_path(packet, "authority_limits", "physical_cone_constructed"))

    model_run = subprocess.run(
        [sys.executable, str(MODEL), "--json"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    try:
        model_result = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model_result = {}
    check("model_exit", model_run.returncode == 0, model_run.returncode)
    check("model_status", model_result.get("status") == "PASS", model_result.get("status"))
    check("model_check_count", len(model_result.get("checks", {})) == 8, len(model_result.get("checks", {})))
    check("model_all_checks", all(model_result.get("checks", {}).values()), model_result.get("checks", {}))

    check("child_math_completed", child_math.get("status") == "completed", child_math.get("status"))
    check("child_math_route", get_path(child_math, "selected_mathematical_route", "candidate_id") == "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1", get_path(child_math, "selected_mathematical_route", "candidate_id"))
    check("child_math_not_executed", get_path(child_math, "selected_mathematical_route", "execution_authorized_in_this_job") is False, get_path(child_math, "selected_mathematical_route", "execution_authorized_in_this_job"))
    check("child_phil_completed", child_phil.get("status") == "completed", child_phil.get("status"))
    check("child_phil_packet_type", get_path(child_phil, "theoretical_decision_output", "selected_next_packet_type") == "source_extension_candidate", get_path(child_phil, "theoretical_decision_output", "selected_next_packet_type"))
    check("child_phil_not_executed", child_phil.get("construction_executed") is False, child_phil.get("construction_executed"))
    check("child_math_hash", sha256(CHILD_MATH) == "074018f25304f49d56c26d9944a750a6586954e0ff2402292768b3e8f42f72e8", sha256(CHILD_MATH))
    check("child_phil_hash", sha256(CHILD_PHIL) == "355277d12d7fe1125f9e100254999f5219d62ec53cd7aeb418fd890a625ef306", sha256(CHILD_PHIL))
    check("conflict_resolved", conflict.get("status") == "resolved", conflict.get("status"))
    check("conflict_count", conflict.get("resolved_conflict_count") == 2, conflict.get("resolved_conflict_count"))
    check("no_unresolved_conflicts", conflict.get("unresolved_conflicts") == [], conflict.get("unresolved_conflicts"))
    check("one_outer_job", get_path(conflict, "fusion_result", "outer_agentjob_count") == 1, get_path(conflict, "fusion_result", "outer_agentjob_count"))
    check("zero_child_jobs", get_path(conflict, "fusion_result", "child_agentjob_count") == 0, get_path(conflict, "fusion_result", "child_agentjob_count"))

    for path_text, expected_hash in EXPECTED_SOURCE_HASHES.items():
        path = ROOT / path_text
        actual = sha256(path) if path.is_file() else ""
        check(f"source_hash_{hashlib.sha256(path_text.encode()).hexdigest()[:10]}", actual == expected_hash, actual)
    provenance_rows = {
        row.get("path"): row.get("sha256")
        for row in provenance.get("sources", [])
        if isinstance(row, dict)
    }
    for path_text, expected_hash in EXPECTED_SOURCE_HASHES.items():
        check(f"provenance_{hashlib.sha256(path_text.encode()).hexdigest()[:10]}", provenance_rows.get(path_text) == expected_hash, provenance_rows.get(path_text))

    tex_text = TEX.read_text(encoding="utf-8") if TEX.is_file() else ""
    fusion_text = FUSION.read_text(encoding="utf-8") if FUSION.is_file() else ""
    for token in [
        "LEM-V22-P4T02-B2-COMMON-HYPERBOLICITY-PRODUCT-001",
        "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1",
        "blocked\\_adoption\\_open\\_continuation",
        "common time-covector domain",
        "universal propagation",
        "P4--T03 is locked",
    ]:
        check(f"tex_{hashlib.sha256(token.encode()).hexdigest()[:10]}", token in tex_text, token)
    for token in [
        "common hyperbolicity envelope",
        "weaker than universal propagation",
        "There are no unresolved blocking conflicts",
        "B2 remains inactive",
    ]:
        check(f"fusion_{hashlib.sha256(token.encode()).hexdigest()[:10]}", token in fusion_text, token)

    try:
        compile_receipt = json.loads(COMPILE.read_text(encoding="utf-8"))
    except Exception as exc:
        compile_receipt = {}
        check("compile_receipt_parse", False, str(exc))
    else:
        check("compile_receipt_parse", True, "parsed")
    check("compile_status", compile_receipt.get("status") == "PASS", compile_receipt.get("status"))
    check("visual_status", compile_receipt.get("visual_inspection_status") == "PASS", compile_receipt.get("visual_inspection_status"))
    check("box_warning_zero", compile_receipt.get("overfull_or_underfull_box_warning_count") == 0, compile_receipt.get("overfull_or_underfull_box_warning_count"))

    control_paths = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260810-002-001.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260810-002-001.yaml",
        "role": TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260810-002.yaml",
        "documentation": TASK / "documentation_impact.yaml",
        "handoff": ROOT / "research_control/handoffs/handoff-0999.yaml",
    }
    controls: dict[str, dict[str, Any]] = {}
    for label, path in control_paths.items():
        check(f"control_exists_{label}", path.is_file(), str(path.relative_to(ROOT)))
        if path.is_file():
            try:
                controls[label] = load_yaml(path)
                check(f"control_parse_{label}", True, "parsed")
            except Exception as exc:
                controls[label] = {}
                check(f"control_parse_{label}", False, str(exc))
    task = controls.get("task", {})
    job = controls.get("job", {})
    completion = controls.get("completion", {})
    handoff = controls.get("handoff", {})
    check("task_completed", task.get("status") == "completed", task.get("status"))
    check("task_p4_t02", get_path(task, "implementation_plan", "plan_task_id") == "P4-T02", get_path(task, "implementation_plan", "plan_task_id"))
    check("job_completed", job.get("status") == "completed", job.get("status"))
    check("job_selector_role", job.get("role_id") == "theoretical-continuation-selector", job.get("role_id"))
    check("job_decomposition", get_path(job, "role_decomposition", "mode") == "parent_child_parallel_synthesis", get_path(job, "role_decomposition", "mode"))
    check("completion_completed", completion.get("status") == "completed", completion.get("status"))
    check("completion_theory_output", get_path(completion, "theoretical_decision_output", "selected_next_packet_type") == "source_extension_candidate", get_path(completion, "theoretical_decision_output", "selected_next_packet_type"))
    check("completion_distance_zero", get_path(completion, "distance_to_gr_delta", "changed") is False, get_path(completion, "distance_to_gr_delta", "changed"))
    check("handoff_identity", handoff.get("handoff_id") == "handoff-0999", handoff.get("handoff_id"))
    check("handoff_next_role", get_path(handoff, "selected_next_route", "role_family") == "candidate-constructor@0.2.0", get_path(handoff, "selected_next_route", "role_family"))
    check("handoff_packet_unexecuted", get_path(handoff, "selected_next_route", "executed") is False, get_path(handoff, "selected_next_route", "executed"))

    backlog_path = ROOT / "research_control/design/v22_recommendation_backlog.yaml"
    try:
        backlog = load_yaml(backlog_path)
        rows = [row for row in backlog.get("items", []) if isinstance(row, dict) and row.get("plan_task_id") == "P4-T02"]
    except Exception as exc:
        rows = []
        check("backlog_parse", False, str(exc))
    else:
        check("backlog_parse", True, "parsed")
    check("backlog_unique_p4_t02", len(rows) == 1, len(rows))
    if rows:
        row = rows[0]
        check("backlog_selector_executed", row.get("runtime_theoretical_continuation_selector_executed") is True, row.get("runtime_theoretical_continuation_selector_executed"))
        check("backlog_next_candidate", row.get("runtime_selected_next_candidate_id") == "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1", row.get("runtime_selected_next_candidate_id"))
        check("backlog_b2_inactive", row.get("runtime_b2_fallback_activated") is False, row.get("runtime_b2_fallback_activated"))

    program = load_yaml(ROOT / "research_control/program_state.yaml")
    check("program_task", program.get("active_task_id") == "RT-20260810-002", program.get("active_task_id"))
    check("program_job", program.get("active_agent_job_id") == "AJ-RT-20260810-002-001", program.get("active_agent_job_id"))
    check("program_handoff", program.get("latest_handoff_id") == "handoff-0999", program.get("latest_handoff_id"))
    check("program_next_p4_t02", program.get("next_plan_task_id") == "P4-T02", program.get("next_plan_task_id"))

    registry_expectations = {
        "registries/RESEARCH_TASK_REGISTRY.csv": "RT-20260810-002",
        "registries/AGENT_JOB_REGISTRY.csv": "AJ-RT-20260810-002-001",
        "registries/DIRECTOR_DECISION_REGISTRY.csv": "DDR-20260810-002",
        "registries/ROLE_EXECUTION_REGISTRY.csv": "theoretical-continuation-selector@0.1.0--RT-20260810-002",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv": "CB-V22-P4-T02-B2-POST-LINE-LOCK-THEORETICAL-SELECTION-001",
        "registries/TEX_SOURCE_REGISTRY.csv": "TEX-V22-P4-T02-B2-POST-LINE-LOCK-ROUTE-SELECTION-V1",
        "registries/MARKDOWN_SOURCE_REGISTRY.csv": "MD-V22-P4-T02-B2-PARENT-FUSION-POST-LINE-LOCK-SELECTION-V1",
    }
    for path_text, token in registry_expectations.items():
        text = (ROOT / path_text).read_text(encoding="utf-8")
        check(f"registry_{hashlib.sha256(token.encode()).hexdigest()[:10]}", token in text, token)

    formatting_paths = [path for path in TASK.rglob("*") if path.is_file()]
    formatting_paths.extend([
        ROOT / "research_control/handoffs/handoff-0999.yaml",
        ROOT / "research_control/handoffs/handoff-0999.md",
    ])
    trailing = []
    missing_newline = []
    for path in formatting_paths:
        if not path.is_file() or path.suffix in {".pdf", ".pyc"}:
            continue
        data = path.read_bytes()
        if data and not data.endswith(b"\n"):
            missing_newline.append(str(path.relative_to(ROOT)))
        try:
            lines = data.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        if any(line.endswith((" ", "\t")) for line in lines):
            trailing.append(str(path.relative_to(ROOT)))
    check("no_trailing_whitespace", not trailing, trailing)
    check("final_newlines", not missing_newline, missing_newline)

    failed = [item for item in checks if not item["passed"]]
    report = {
        "schema_id": "v22_p4_t02_b2_post_line_lock_selector_validation_v1",
        "generated_at": GENERATED_AT,
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "selected_candidate_id": "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1",
        "selected_next_packet_type": "source_extension_candidate",
        "selected_next_role_family": "candidate-constructor@0.2.0",
        "selected_packet_executed": False,
        "b2_activated": False,
        "p4_t03_unlocked": False,
        "checks": checks,
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_post_line_lock_selector_compact_receipt_v1",
        "generated_at": GENERATED_AT,
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
        "selected_candidate_id": report["selected_candidate_id"],
        "selected_next_packet_type": report["selected_next_packet_type"],
        "selected_next_role_family": report["selected_next_role_family"],
        "selected_packet_executed": False,
        "shared_line_route_replayed": False,
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
            failed.append({"check_id": "receipt_mismatch", "passed": False})
    summary = {
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": len(failed),
        "failed_check_ids": [item["check_id"] for item in failed],
        "report_path": str(REPORT.relative_to(ROOT)),
        "compact_receipt_path": str(COMPACT.relative_to(ROOT)),
    }
    print(json.dumps(summary, indent=2, sort_keys=True) if args.json else f"{summary['status']}: {summary['check_count'] - summary['failure_count']}/{summary['check_count']} checks")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
