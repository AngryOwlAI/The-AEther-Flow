#!/usr/bin/env python3
"""Validate the bounded V22 P4-T02 common-hyperbolicity envelope transaction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260810-005"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_common_hyperbolicity_envelope_validation.json"
COMPACT = ART / "v22_p4_t02_b2_common_hyperbolicity_envelope_compact_receipt.json"
GENERATED_AT = "2026-08-10T10:55:24Z"

TEX = ART / "v22_p4_t02_b2_common_hyperbolicity_envelope_candidate_v1.tex"
ENVELOPE = ART / "v22_p4_t02_b2_common_hyperbolicity_envelope_record_v1.yaml"
QUOTIENT = ART / "v22_p4_t02_b2_operational_response_ray_quotient_v1.yaml"
STRESS = ART / "v22_p4_t02_b2_common_envelope_stress_matrix_v1.yaml"
MODEL = ART / "v22_p4_t02_b2_common_hyperbolicity_envelope_model.py"
CHILD_MATH = ART / "child_phys_math_p4_t02_b2_common_hyperbolicity_envelope.yaml"
CHILD_PHIL = ART / "child_phys_phil_p4_t02_b2_common_hyperbolicity_envelope.yaml"
CONFLICT = ART / "parent_conflict_review_p4_t02_b2_common_hyperbolicity_envelope.yaml"
FUSION = ART / "parent_fusion_notes_p4_t02_b2_common_hyperbolicity_envelope.md"
COMPILE = ART / "v22_p4_t02_b2_common_hyperbolicity_envelope_latex_compile_receipt.json"

TASK_FILE = TASK / "00_TASK.yaml"
JOB = TASK / "jobs/AJ-RT-20260810-005-001.yaml"
COMPLETION = TASK / "jobs/completions/AJC-AJ-RT-20260810-005-001.yaml"
ROLE = TASK / "roles/candidate-constructor@0.2.0--RT-20260810-005.yaml"
DOCUMENTATION = TASK / "documentation_impact.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-1002.yaml"

EXPECTED_SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1001.yaml":
        "5fcf334f67049e58c8761bec0c567ca9639663ae69fbe296fd08d34c56e2bfae",
    "research_control/tasks/RT-20260810-002/artifacts/v22_p4_t02_b2_common_hyperbolicity_envelope_packet_v1.yaml":
        "ab2231c9796f150b8404ca4e7f092a0e486b023bf64390ed313a6bec30704289",
    "research_control/tasks/RT-20260810-002/artifacts/v22_p4_t02_b2_post_line_lock_route_selection_v1.tex":
        "c1c55815eb6c55574f2d7c7ed81a56e63fa1f73024685a506e8996789d2894bd",
    "research_control/tasks/RT-20260810-002/artifacts/parent_fusion_notes_p4_t02_b2_post_line_lock_selector.md":
        "36bf554115481b81a6a11b3d734be815d77966f48abbe69f33d4a479751ac1cd",
    "research_control/tasks/RT-20260810-001/artifacts/v22_p4_t02_b2_source_intrinsic_interface_repair_v1.tex":
        "f1b8d1e851a56109e0976ff4cfde8ff2adce4e1376581547f048c55a6a0b3497",
    "research_control/tasks/RT-20260810-001/artifacts/v22_p4_t02_b2_line_selector_obstruction_v1.yaml":
        "3c4d53632f274ce2fa49612f369363e4b3c7ebdffd7a451c102f791f0e0f6b1e",
    "research_control/tasks/RT-20260810-001/artifacts/v22_p4_t02_b2_typed_operational_bridge_v1.yaml":
        "60a891df7a590c43917c4cb6e0f9ac25e61bcbf328711718d5ad947123d00a08",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}

EXPECTED_ARTIFACT_HASHES = {
    CHILD_MATH: "ef2109f8a04224e7a5681015c1df78ef413674aedae67f0e8f2744893754eef1",
    CHILD_PHIL: "e956c306c166c465148dd057c6417fa7820015188a3c5719872a6c5008f03e6f",
    CONFLICT: "946dc98583a151164f4d7a506a358306f31046f87b8f2f3bd4eb8af3a03deec7",
    FUSION: "0b1cd29b64da343da70906ac313f803275618e45889d07cea91f878e5618c0c0",
    TEX: "eeac27624e437851726b3865b8900a78f8bed39aa116fc99fd4dfd3a24689152",
    ENVELOPE: "60fbd716099176e2f9faff5eb70cc1c02336cde2c730fea6719bb0088213c7bf",
    QUOTIENT: "a9138de596a1810bb5533f47b56a60d2e4f83a54d5e2e4163b3dd25fa322637e",
    STRESS: "e37f67862d3e26bf9865085b76e303df8b3f0ee304a060051cb40c4feb8bea93",
    MODEL: "9f8e9c58749397921c48a64bae904d5c9dc258d17a9aec16c51250dd3153e958",
    COMPILE: "05727b19ac7a0ea44453aba7235fb85af0f411abf5f5491324940983805ac633",
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


def registry_key_count(path: Path, key: str) -> tuple[int, int]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return 0, 0
    width = len(rows[0])
    matches = [row for row in rows[1:] if row and row[0] == key and len(row) == width]
    return len(matches), width


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
        TEX, ENVELOPE, QUOTIENT, STRESS, MODEL, CHILD_MATH, CHILD_PHIL,
        CONFLICT, FUSION, COMPILE, TASK_FILE, JOB, COMPLETION, ROLE,
        DOCUMENTATION, HANDOFF,
    ]
    for path in core_paths:
        check(f"exists_{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    yaml_paths = [
        ENVELOPE, QUOTIENT, STRESS, CHILD_MATH, CHILD_PHIL, CONFLICT,
        TASK_FILE, JOB, COMPLETION, ROLE, DOCUMENTATION, HANDOFF,
    ]
    loaded: dict[Path, dict[str, Any]] = {}
    for path in yaml_paths:
        try:
            loaded[path] = load_yaml(path)
            check(f"yaml_{path.name}", True, "parsed")
        except Exception as exc:
            loaded[path] = {}
            check(f"yaml_{path.name}", False, str(exc))

    envelope = loaded[ENVELOPE]
    quotient = loaded[QUOTIENT]
    stress = loaded[STRESS]
    child_math = loaded[CHILD_MATH]
    child_phil = loaded[CHILD_PHIL]
    conflict = loaded[CONFLICT]
    task = loaded[TASK_FILE]
    job = loaded[JOB]
    completion = loaded[COMPLETION]
    role = loaded[ROLE]
    documentation = loaded[DOCUMENTATION]
    handoff = loaded[HANDOFF]

    for path_text, expected in EXPECTED_SOURCE_HASHES.items():
        path = ROOT / path_text
        actual = sha256(path) if path.is_file() else ""
        check(f"source_hash_{hashlib.sha256(path_text.encode()).hexdigest()[:10]}", actual == expected, actual)
    for path, expected in EXPECTED_ARTIFACT_HASHES.items():
        actual = sha256(path) if path.is_file() else ""
        check(f"artifact_hash_{path.name}", actual == expected, actual)

    check("candidate_identity", envelope.get("candidate_id") == "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1", envelope.get("candidate_id"))
    check("decisive_result", envelope.get("decisive_result") == "constructed_candidate", envelope.get("decisive_result"))
    check("no_fog", envelope.get("no_fog_check") is True, envelope.get("no_fog_check"))
    check("proposal_only", envelope.get("status_label") == "proposal-only", envelope.get("status_label"))
    check("source_extension_data", envelope.get("material_class") == "source-extension data", envelope.get("material_class"))
    check("exact_sector_set", get_path(envelope, "sector_domain", "equipped_sector_ids") == ["R", "S", "D"], get_path(envelope, "sector_domain", "equipped_sector_ids"))
    check("sector_set_finite", get_path(envelope, "sector_domain", "finite") is True, get_path(envelope, "sector_domain", "finite"))
    check("no_full_sector_claim", get_path(envelope, "sector_domain", "full_p7_sector_domain_claimed") is False, get_path(envelope, "sector_domain", "full_p7_sector_domain_claimed"))
    check("independent_boundaries", get_path(envelope, "sector_principal_forms", "independent_characteristic_boundaries") is True, get_path(envelope, "sector_principal_forms", "independent_characteristic_boundaries"))
    check("no_shared_line", get_path(envelope, "sector_principal_forms", "shared_characteristic_line_required") is False, get_path(envelope, "sector_principal_forms", "shared_characteristic_line_required"))
    product = get_path(envelope, "product_envelope", "product_polynomial") or ""
    common_cone = get_path(envelope, "product_envelope", "common_cone") or ""
    check("product_formula", "k(u)^2-epsilon^2 k(z)^2" in product, product)
    check("common_cone_formula", "k(u)>|epsilon k(z)|" in common_cone, common_cone)
    check("product_degree", get_path(envelope, "product_envelope", "product_degree") == 3, get_path(envelope, "product_envelope", "product_degree"))
    check("covariance_no_target", get_path(envelope, "source_presentation_covariance", "target_atlas_used") is False, get_path(envelope, "source_presentation_covariance", "target_atlas_used"))
    check("robustness_constructed", get_path(envelope, "strict_margin_robustness", "finite_variation_robustness_status") == "constructed_on_declared_neighborhood", get_path(envelope, "strict_margin_robustness", "finite_variation_robustness_status"))
    check("strict_bound", "109/150>0" in str(get_path(envelope, "strict_margin_robustness", "reproduction_chart_only", "bound")), get_path(envelope, "strict_margin_robustness", "reproduction_chart_only", "bound"))
    check("multiplicity_exposed", get_path(envelope, "multiplicity_and_degeneracy", "reducible_product") is True, get_path(envelope, "multiplicity_and_degeneracy", "reducible_product"))
    check("strong_hyperbolicity_not_claimed", get_path(envelope, "multiplicity_and_degeneracy", "strong_or_symmetric_hyperbolicity_claimed") is False, get_path(envelope, "multiplicity_and_degeneracy", "strong_or_symmetric_hyperbolicity_claimed"))

    ray = get_path(quotient, "operational_quotient_layers", "response_ray") or {}
    sign = get_path(quotient, "operational_quotient_layers", "sign_orbit") or {}
    check("ray_constructed", ray.get("status") == "constructed for the explicitly fixed proposal-only sector representatives", ray.get("status"))
    check("ray_formula", ray.get("quotient_name") == "Q_ray" and "R_{>0}" in str(ray.get("formula")), ray.get("formula"))
    check("ray_keeps_ratios", "relative response ratios" in str(ray.get("invariant_data")), ray.get("invariant_data"))
    check("ray_common_scale_invariant", ray.get("common_scale_invariant") is True, ray.get("common_scale_invariant"))
    check("ray_not_independent_scale_invariant", ray.get("independent_sector_scale_invariant") is False, ray.get("independent_sector_scale_invariant"))
    check("ray_preimage", ray.get("common_cone_preimage") == "Gamma_intersection=Q_ray^{-1}(C_+++)", ray.get("common_cone_preimage"))
    check("sign_formula", sign.get("quotient_name") == "Q_sign" and "G_+" in str(sign.get("formula")), sign.get("formula"))
    check("sign_independent_scale_invariant", sign.get("independent_sector_scale_invariant") is True, sign.get("independent_sector_scale_invariant"))
    check("sign_preimage", sign.get("common_cone_preimage") == "Gamma_intersection=Q_sign^{-1}(O_+++)", sign.get("common_cone_preimage"))
    check("quotient_no_physical_causality", get_path(quotient, "operational_quotient_layers", "shared_properties", "physical_causality_claimed") is False, get_path(quotient, "operational_quotient_layers", "shared_properties", "physical_causality_claimed"))
    check("quotient_no_empirical_response", get_path(quotient, "response_map", "empirical_response_claimed") is False, get_path(quotient, "response_map", "empirical_response_claimed"))
    check("protocol_not_adopted", get_path(quotient, "proposal_only_protocol_extension", "proposal_adopted") is False, get_path(quotient, "proposal_only_protocol_extension", "proposal_adopted"))

    rows = stress.get("stress_rows", [])
    row_ids = {row.get("stress_id") for row in rows if isinstance(row, dict)}
    expected_rows = {
        "CHE-BASE-PRODUCT", "CHE-INDEPENDENT-MARGIN", "CHE-EMPTY-INTERSECTION",
        "CHE-ORIENTATION-AMBIGUITY", "CHE-ZERO-FACTOR", "CHE-MULTIPLICITY",
        "CHE-NORMALIZATION", "CHE-INVERSE-DEFECT", "CHE-COCYCLE-DEFECT",
        "CHE-SECTOR-SCOPE", "CHE-TARGET-IMPORT", "CHE-PHYSICAL-OVERREAD",
    }
    check("stress_count", len(rows) == 12, len(rows))
    check("stress_ids", row_ids == expected_rows, sorted(row_ids))
    branches = stress.get("refuter_failure_branches", {})
    check("five_refuter_branches", set(branches) == {"collapse", "nonuniqueness", "inverse_defect", "cocycle_defect", "variation_fragility"}, sorted(branches))
    check("freeze_not_frozen", get_path(stress, "freeze_criteria_status", "freeze_decision") == "not_frozen_constructed_candidate_requires_audit", get_path(stress, "freeze_criteria_status", "freeze_decision"))
    check("stress_next_role", get_path(stress, "freeze_criteria_status", "next_required_role") == "smuggling-auditor@0.2.0", get_path(stress, "freeze_criteria_status", "next_required_role"))
    check("stress_no_distance_delta", get_path(stress, "summary", "distance_to_gr_changed") is False, get_path(stress, "summary", "distance_to_gr_changed"))

    model_run = subprocess.run([sys.executable, str(MODEL), "--json"], cwd=ROOT, check=False, text=True, capture_output=True)
    try:
        model_result = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model_result = {}
    check("model_exit", model_run.returncode == 0, model_run.returncode)
    check("model_status", model_result.get("status") == "PASS", model_result.get("status"))
    check("model_check_count", len(model_result.get("checks", {})) == 14, len(model_result.get("checks", {})))
    check("model_all_checks", all(model_result.get("checks", {}).values()), model_result.get("checks", {}))
    check("model_roots", model_result.get("sample_roots") == ["-3", "-2", "-1"], model_result.get("sample_roots"))
    check("model_strict_bound", model_result.get("strict_lower_bound") == "109/150", model_result.get("strict_lower_bound"))
    check("model_physical_block", get_path(model_result, "authority_limits", "physical_cone_constructed") is False, get_path(model_result, "authority_limits", "physical_cone_constructed"))

    check("child_math_result", get_path(child_math, "no_fog_recommendation", "permitted_result_type_selected") == "constructed_candidate", get_path(child_math, "no_fog_recommendation", "permitted_result_type_selected"))
    check("child_math_next_role", get_path(child_math, "no_fog_recommendation", "next_role_family") == "smuggling-auditor@0.2.0", get_path(child_math, "no_fog_recommendation", "next_role_family"))
    check("child_phil_result", get_path(child_phil, "independent_result", "result_type") == "constructed_candidate", get_path(child_phil, "independent_result", "result_type"))
    check("child_phil_next_role", get_path(child_phil, "independent_result", "next_role_family") == "smuggling-auditor@0.2.0", get_path(child_phil, "independent_result", "next_role_family"))
    check("child_phil_no_fog", get_path(child_phil, "independent_result", "no_fog_check") is True, get_path(child_phil, "independent_result", "no_fog_check"))
    check("conflict_resolved", conflict.get("status") == "resolved", conflict.get("status"))
    check("conflict_one_resolution", conflict.get("resolved_conflict_count") == 1, conflict.get("resolved_conflict_count"))
    check("no_unresolved_conflicts", conflict.get("unresolved_conflicts") == [] and conflict.get("blocking_conflict_count") == 0, conflict.get("unresolved_conflicts"))
    check("conflict_fused_result", conflict.get("fused_result_type") == "constructed_candidate", conflict.get("fused_result_type"))
    check("conflict_next_role", conflict.get("fused_next_role") == "smuggling-auditor@0.2.0", conflict.get("fused_next_role"))

    tex_text = TEX.read_text(encoding="utf-8") if TEX.is_file() else ""
    fusion_text = FUSION.read_text(encoding="utf-8") if FUSION.is_file() else ""
    for token in [
        "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1",
        "Operational two-layer response-quotient candidate",
        "\\Qray^{-1}(\\mathcal C_{+++})",
        "\\Qsign^{-1}(\\mathcal O_{+++})",
        "109/150",
        "blocked\\_adoption\\_open\\_continuation",
        "smuggling-auditor@0.2.0",
        "constructed\\_candidate",
    ]:
        check(f"tex_{hashlib.sha256(token.encode()).hexdigest()[:10]}", token in tex_text, token)
    for token in [
        "Two-layer quotient resolution", "Q_ray", "Q_sign",
        "common time-covector admissibility is not universal propagation",
        "source_extension_smuggling_audit", "smuggling-auditor@0.2.0",
    ]:
        passed = token.lower() in fusion_text.lower()
        check(f"fusion_{hashlib.sha256(token.encode()).hexdigest()[:10]}", passed, token)

    try:
        compile_receipt = json.loads(COMPILE.read_text(encoding="utf-8"))
        check("compile_receipt_parse", True, "parsed")
    except Exception as exc:
        compile_receipt = {}
        check("compile_receipt_parse", False, str(exc))
    check("compile_status", compile_receipt.get("status") == "PASS", compile_receipt.get("status"))
    check("compile_source_hash", compile_receipt.get("source_sha256") == sha256(TEX), compile_receipt.get("source_sha256"))
    check("compile_page_count", compile_receipt.get("page_count") == 6, compile_receipt.get("page_count"))
    check("compile_all_pages_rendered", compile_receipt.get("rendered_page_count") == 6 and compile_receipt.get("visually_inspected_pages") == [1, 2, 3, 4, 5, 6], compile_receipt.get("visually_inspected_pages"))
    check("visual_status", compile_receipt.get("visual_inspection_status") == "PASS", compile_receipt.get("visual_inspection_status"))
    visual_findings = compile_receipt.get("visual_findings", {})
    check("visual_findings_clear", visual_findings and not any(visual_findings.values()), visual_findings)
    check("temporary_pdf_only", compile_receipt.get("tracked_pdf_created") is False and compile_receipt.get("pdf_authority") == "temporary_human_reading_derivative_only", compile_receipt.get("pdf_authority"))

    check("task_completed", task.get("status") == "completed", task.get("status"))
    check("task_validation", task.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED", task.get("validation_status"))
    check("task_plan", get_path(task, "implementation_plan", "plan_task_id") == "P4-T02", get_path(task, "implementation_plan", "plan_task_id"))
    check("task_boundary_closed", get_path(task, "claim_boundary", "boundary_status") == "completed_closed", get_path(task, "claim_boundary", "boundary_status"))
    check("job_completed", job.get("status") == "completed", job.get("status"))
    check("job_role", job.get("role_id") == "candidate-constructor" and job.get("role_version") == "0.2.0", f"{job.get('role_id')}@{job.get('role_version')}")
    check("job_milestone", job.get("target_derivation_milestone") == "effective_metric_g_eff", job.get("target_derivation_milestone"))
    check("job_two_children", get_path(job, "role_decomposition", "subagent_count") == 2, get_path(job, "role_decomposition", "subagent_count"))
    check("role_expired", role.get("status") == "expired_completed", role.get("status"))
    check("completion_completed", completion.get("status") == "completed", completion.get("status"))
    check("completion_candidate_result", get_path(completion, "candidate_constructor_result", "result_type") == "constructed_candidate", get_path(completion, "candidate_constructor_result", "result_type"))
    check("completion_no_fog", get_path(completion, "candidate_constructor_result", "no_fog_check") is True, get_path(completion, "candidate_constructor_result", "no_fog_check"))
    check("completion_physics_status", get_path(completion, "physics_progress_status", "status") == "candidate_constructed_pending_audit", get_path(completion, "physics_progress_status", "status"))
    check("completion_distance_zero", get_path(completion, "distance_to_gr_delta", "changed") is False, get_path(completion, "distance_to_gr_delta", "changed"))
    check("completion_payload_count", len(completion.get("mathematical_payload_manifest", [])) == 5, len(completion.get("mathematical_payload_manifest", [])))
    check("completion_burden_count", len(completion.get("distance_to_gr_status", [])) == 14, len(completion.get("distance_to_gr_status", [])))
    check("completion_freeze", get_path(completion, "freeze_criteria_status", "freeze_decision") == "not_frozen", get_path(completion, "freeze_criteria_status", "freeze_decision"))
    check("completion_next_role", get_path(completion, "candidate_constructor_result", "next_required_role") == "smuggling-auditor", get_path(completion, "candidate_constructor_result", "next_required_role"))
    check("completion_next_unexecuted", get_path(completion, "selected_next_route", "executed") is False, get_path(completion, "selected_next_route", "executed"))
    check("completion_no_promotion", get_path(completion, "forbidden_conclusion_summary", "physics_promotion_authorized") is False, get_path(completion, "forbidden_conclusion_summary", "physics_promotion_authorized"))
    check("handoff_identity", handoff.get("handoff_id") == "handoff-1002", handoff.get("handoff_id"))
    check("handoff_result", get_path(handoff, "claim_boundary", "decisive_result") == "constructed_candidate", get_path(handoff, "claim_boundary", "decisive_result"))
    check("handoff_next_role", get_path(handoff, "selected_next_route", "role_family") == "smuggling-auditor@0.2.0", get_path(handoff, "selected_next_route", "role_family"))
    check("handoff_audit_unexecuted", get_path(handoff, "selected_next_route", "executed") is False, get_path(handoff, "selected_next_route", "executed"))
    check("documentation_completed", documentation.get("status") == "completed", documentation.get("status"))
    check("documentation_no_shared_policy_edit", "existing shared policy" in str(documentation.get("no_update_rationale", "")).lower(), documentation.get("no_update_rationale"))

    backlog = load_yaml(ROOT / "research_control/design/v22_recommendation_backlog.yaml")
    items = [row for row in backlog.get("items", []) if isinstance(row, dict) and row.get("plan_task_id") == "P4-T02"]
    check("backlog_unique_p4_t02", len(items) == 1, len(items))
    if items:
        row = items[0]
        check("backlog_constructor_executed", row.get("runtime_common_hyperbolicity_envelope_executed") is True, row.get("runtime_common_hyperbolicity_envelope_executed"))
        check("backlog_constructed_result", row.get("runtime_common_hyperbolicity_envelope_result") == "constructed_candidate", row.get("runtime_common_hyperbolicity_envelope_result"))
        check("backlog_next_role", row.get("runtime_selected_next_role_family") == "smuggling-auditor@0.2.0", row.get("runtime_selected_next_role_family"))
        check("backlog_audit_unexecuted", row.get("runtime_source_extension_smuggling_audit_executed") is False, row.get("runtime_source_extension_smuggling_audit_executed"))
        check("backlog_b2_inactive", row.get("runtime_b2_fallback_activated") is False, row.get("runtime_b2_fallback_activated"))
        check("backlog_p4_t03_locked", row.get("runtime_p4_t03_unlocked") is False, row.get("runtime_p4_t03_unlocked"))

    program = load_yaml(ROOT / "research_control/program_state.yaml")
    check("program_task", program.get("active_task_id") == "RT-20260810-005", program.get("active_task_id"))
    check("program_job", program.get("active_agent_job_id") == "AJ-RT-20260810-005-001", program.get("active_agent_job_id"))
    check("program_handoff", program.get("latest_handoff_id") == "handoff-1002", program.get("latest_handoff_id"))
    pblock = program.get("v22_p4_t02_b2_common_hyperbolicity_envelope_candidate", {})
    check("program_candidate_result", pblock.get("decisive_result") == "constructed_candidate", pblock.get("decisive_result"))
    check("program_next_role", pblock.get("selected_next_role_family") == "smuggling-auditor@0.2.0", pblock.get("selected_next_role_family"))
    check("program_no_distance_delta", pblock.get("distance_to_gr_ledger_unchanged") is True, pblock.get("distance_to_gr_ledger_unchanged"))

    registry_expectations = {
        "registries/RESEARCH_TASK_REGISTRY.csv": "RT-20260810-005",
        "registries/AGENT_JOB_REGISTRY.csv": "AJ-RT-20260810-005-001",
        "registries/DIRECTOR_DECISION_REGISTRY.csv": "DDR-20260810-005",
        "registries/ROLE_EXECUTION_REGISTRY.csv": "candidate-constructor@0.2.0--RT-20260810-005",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv": "CB-V22-P4-T02-B2-COMMON-HYPERBOLICITY-ENVELOPE-CONSTRUCTION-001",
        "registries/TEX_SOURCE_REGISTRY.csv": "TEX-V22-P4-T02-B2-COMMON-HYPERBOLICITY-ENVELOPE-CANDIDATE-V1",
        "registries/MARKDOWN_SOURCE_REGISTRY.csv": "MD-V22-P4-T02-B2-PARENT-FUSION-COMMON-HYPERBOLICITY-ENVELOPE-V1",
    }
    for path_text, key in registry_expectations.items():
        count, width = registry_key_count(ROOT / path_text, key)
        check(f"registry_{hashlib.sha256(key.encode()).hexdigest()[:10]}", count == 1, {"count": count, "width": width})

    authority_fields = [
        "physical_cone_constructed", "universal_matter_propagation_derived",
        "full_p7_sector_coverage_derived", "source_law_adopted",
        "canonical_ontology_modified", "adequacy_reevaluated", "b2_activated",
        "p4_t03_unlocked", "effective_metric_constructed", "physics_promotion_authorized",
    ]
    limits = envelope.get("authority_limits", {})
    check("envelope_authority_blocks", all(limits.get(field) is False for field in authority_fields), {field: limits.get(field) for field in authority_fields})
    completion_auth = completion.get("authorization_layers", {})
    check("completion_authority_blocks", all(value is False for value in completion_auth.values() if isinstance(value, bool)), completion_auth)

    formatting_paths = [path for path in TASK.rglob("*") if path.is_file()]
    formatting_paths.extend([HANDOFF, ROOT / "research_control/handoffs/handoff-1002.md"])
    trailing: list[str] = []
    missing_newline: list[str] = []
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
        "schema_id": "v22_p4_t02_b2_common_hyperbolicity_envelope_validation_v1",
        "generated_at": GENERATED_AT,
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "candidate_id": "CAND-V22-B2-COMMON-HYPERBOLICITY-ENVELOPE-V1",
        "decisive_result": "constructed_candidate",
        "response_quotient_layers": ["Q_ray", "Q_sign"],
        "selected_next_packet_type": "source_extension_smuggling_audit",
        "selected_next_role_family": "smuggling-auditor@0.2.0",
        "selected_next_packet_executed": False,
        "physical_cone_constructed": False,
        "distance_to_gr_changed": False,
        "b2_activated": False,
        "p4_t03_unlocked": False,
        "checks": checks,
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_common_hyperbolicity_envelope_compact_receipt_v1",
        "generated_at": GENERATED_AT,
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
        "candidate_id": report["candidate_id"],
        "decisive_result": report["decisive_result"],
        "response_quotient_layer_count": 2,
        "stress_row_count": 12,
        "model_check_count": 14,
        "rendered_page_count": 6,
        "selected_next_packet_type": report["selected_next_packet_type"],
        "selected_next_role_family": report["selected_next_role_family"],
        "selected_next_packet_executed": False,
        "shared_line_route_replayed": False,
        "source_law_adopted": False,
        "physical_cone_constructed": False,
        "distance_to_gr_changed": False,
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
            failed.append({"check_id": "receipt_mismatch", "passed": False})
    summary = {
        "status": "PASS" if not failed else "FAIL",
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
