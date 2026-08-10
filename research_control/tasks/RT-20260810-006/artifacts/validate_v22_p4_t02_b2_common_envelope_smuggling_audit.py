#!/usr/bin/env python3
"""Focused validator for RT-20260810-006.

This validator checks the exact mathematical audit payload, parent-child
resolution, control bindings, source registrations, and authority limits.  It
does not establish theorem truth, adopt ontology, or promote physics claims.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260810-006"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_common_envelope_smuggling_audit_validation.json"
COMPACT = ART / "v22_p4_t02_b2_common_envelope_smuggling_audit_compact_receipt.json"

EXPECTED_HASHES = {
    "child_phys_math_p4_t02_b2_common_envelope_smuggling_audit.yaml": "955c393f4a28d10cc87822536cebe2dfa4f1f882709337d1cae7ba021edee402",
    "child_phys_phil_p4_t02_b2_common_envelope_smuggling_audit.yaml": "b37920279e3a75f0a587b807a7ed29ef2db12a4ca00924f5752dbd812452086b",
    "parent_conflict_review_p4_t02_b2_common_envelope_smuggling_audit.yaml": "82ae44f281afd83a04087722cb37b475c3326bb5e8c396a5e52c3816587717ec",
    "parent_fusion_notes_p4_t02_b2_common_envelope_smuggling_audit.md": "8d61ff9bedddf4d0e834d7c6791019f110df1be359ee212b1ce8fcc9bf7e941c",
    "v22_p4_t02_b2_common_envelope_audit_disposition_v1.yaml": "0d6ba43aeba87eea272d8ad38eb5a983798524a1ef0973294c1581c6d1d6859f",
    "v22_p4_t02_b2_common_envelope_audit_model.py": "13dabf54d26b8669e2adb2cf74a0c074bd18b1dbd1317d139a6e54ff519612d7",
    "v22_p4_t02_b2_common_envelope_smuggling_audit_latex_compile_receipt.json": "51a9027c4d9b82e2396b6a3d8dc9bb8bf167c0cedcb91b16159eb011cf6a31ca",
    "v22_p4_t02_b2_common_envelope_smuggling_audit_v1.tex": "7acffba7b7798c86bad06e878989028ee70cca478e801c41cb577b615a61f0bd",
    "v22_p4_t02_b2_common_envelope_smuggling_matrix_v1.yaml": "047b3736f7b0971062d6807c60a5711db2f0d6aedb7b8889d49b1efa537ed188",
}

EXPECTED_CONTROL_HASHES = {
    "00_TASK.yaml": "5e02c5ca25ce7a31d1e602bbc3431833129fa5ddad64794990420c6dc535df3c",
    "DDR-20260810-006.md": "1b59d761a697a3b76a2029cfc27c3d9b605268dd911985f707458fc0aaf65cd8",
    "documentation_impact.yaml": "9bfcd2b3cdf371061ccf35e86811da36fa9f204a865783f58a8e3cf8c51222cd",
    "jobs/AJ-RT-20260810-006-001.yaml": "ff1db9fde5e07a4547060444d51b6604d0ccc724a0c4c58ab077b6e3f2e1a4aa",
    "roles/smuggling-auditor@0.2.0--RT-20260810-006.yaml": "86f66fa0cb98a229d0e2dd97b253c07d4787a725b5006be364b713d771fe3b31",
    "jobs/completions/AJC-AJ-RT-20260810-006-001.yaml": "8115e7c83edd119610c7281c76705a33b4095ccc349fb43c2ea339332ff24ee0",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that refuses duplicate mapping keys."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.Node, deep: bool = False) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UniqueKeyLoader)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        })

    expected_paths = [ART / name for name in EXPECTED_HASHES]
    expected_paths.extend(TASK / name for name in EXPECTED_CONTROL_HASHES)
    expected_paths.extend([
        ROOT / "research_control/handoffs/handoff-1003.yaml",
        ROOT / "research_control/handoffs/handoff-1003.md",
        ROOT / "research_control/program_state.yaml",
        ROOT / "research_control/design/v22_recommendation_backlog.yaml",
    ])
    for path in expected_paths:
        check(f"exists:{path.relative_to(ROOT)}", path.is_file(), "required tracked artifact exists")

    for name, expected in EXPECTED_HASHES.items():
        path = ART / name
        check(f"hash:{name}", path.is_file() and sha256(path) == expected, f"expected SHA-256 {expected}")
    for name, expected in EXPECTED_CONTROL_HASHES.items():
        path = TASK / name
        check(f"control_hash:{name}", path.is_file() and sha256(path) == expected, f"expected SHA-256 {expected}")

    yaml_paths = list(TASK.rglob("*.yaml")) + [
        ROOT / "research_control/handoffs/handoff-1003.yaml",
        ROOT / "research_control/design/v22_recommendation_backlog.yaml",
    ]
    parsed: dict[Path, Any] = {}
    for path in yaml_paths:
        try:
            parsed[path] = load_yaml(path)
            check(f"yaml_unique:{path.relative_to(ROOT)}", True, "YAML parses with unique mapping keys")
        except Exception as exc:  # pragma: no cover - diagnostic path
            check(f"yaml_unique:{path.relative_to(ROOT)}", False, str(exc))
    program_path = ROOT / "research_control/program_state.yaml"
    try:
        parsed[program_path] = yaml.safe_load(program_path.read_text(encoding="utf-8"))
        check("yaml_parse:research_control/program_state.yaml", True, "legacy program state parses")
    except Exception as exc:  # pragma: no cover - diagnostic path
        check("yaml_parse:research_control/program_state.yaml", False, str(exc))

    model_run = subprocess.run(
        [sys.executable, str(ART / "v22_p4_t02_b2_common_envelope_audit_model.py"), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        model = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model = {}
    check("model_exit", model_run.returncode == 0, model_run.stderr.strip() or "model exits zero")
    check("model_status", model.get("status") == "PASS", "model status is PASS")
    check("model_verdict", model.get("audit_verdict_supported") == "repair_required", "model supports repair_required")
    check("model_no_target_import", model.get("target_import_detected") is False, "no target import detected")
    check("model_image_relation", model.get("response_image_relation") == "r_R+r_D=2*r_S", "exact image-plane relation")
    check("model_rank", model.get("response_rank") == 2, "response rank is two")
    check("model_kernel", model.get("response_kernel_dimension") == 2, "kernel dimension is two")
    check("model_projective_dimension", model.get("projective_image_parameter_count") == 1, "positive-projective image has one parameter")
    check("model_sign_orbits", model.get("realized_nonzero_sign_orbit_count") == 6, "six nonzero ordered sign orbits are realized")
    check("model_ten_dimensions", len(model.get("checks", {})) == 10 and all(model.get("checks", {}).values()), "all ten executable audit dimensions pass")

    matrix = parsed.get(ART / "v22_p4_t02_b2_common_envelope_smuggling_matrix_v1.yaml", {})
    rows = matrix.get("audit_rows", []) if isinstance(matrix, dict) else []
    dimensions = {row.get("dimension") for row in rows if isinstance(row, dict)}
    expected_dimensions = {
        "representative_normalization",
        "response_typing",
        "units_and_degree",
        "component_and_orientation_choice",
        "transition_factors_and_gluing",
        "sector_scope",
        "hidden_target_fit",
        "goal_property_preload",
        "empirical_and_physical_overread",
        "authority_smuggling",
    }
    check("matrix_verdict", matrix.get("audit_status") == "repair_required", "matrix verdict is repair_required")
    check("matrix_dimensions", dimensions == expected_dimensions and len(rows) == 10, "matrix contains the exact ten audit dimensions")
    blocking_rows = [row for row in rows if row.get("repair_blocking") is True]
    check("matrix_one_blocking_repair", len(blocking_rows) == 1, "exactly one audit row is repair-blocking")
    check("matrix_no_hidden_import", all(row.get("hidden_import_detected") is False for row in rows), "no audit row detects hidden import")
    summary = matrix.get("summary", {})
    check("matrix_summary_counts", summary.get("audit_dimension_count") == 10 and summary.get("repair_blocking_finding_count") == 1, "matrix summary counts bind the ten-by-one result")
    check("matrix_next_route", matrix.get("next_route", {}).get("packet_type") == "source_extension_candidate" and matrix.get("next_route", {}).get("executed") is False, "matrix selects one unexecuted candidate repair")

    disposition = parsed.get(ART / "v22_p4_t02_b2_common_envelope_audit_disposition_v1.yaml", {})
    check("disposition_verdict", disposition.get("decisive_result") == "repair_required", "disposition is repair_required")
    check("disposition_no_fog", disposition.get("no_fog_check") is True, "disposition is mathematically decisive")
    check("disposition_next_role", disposition.get("next_required_packet", {}).get("role_family") == "candidate-constructor@0.2.0", "Candidate Constructor owns the repair")
    check("disposition_unexecuted", disposition.get("next_required_packet", {}).get("executed") is False, "repair is not executed")
    check("disposition_no_distance", disposition.get("distance_to_gr", {}).get("changed") is False, "Distance-to-GR is unchanged")

    conflict = parsed.get(ART / "parent_conflict_review_p4_t02_b2_common_envelope_smuggling_audit.yaml", {})
    check("conflict_resolved", conflict.get("status") == "resolved" and conflict.get("resolution_rounds") == 1, "one resolution round completed")
    check("conflict_children", len(conflict.get("child_inputs", [])) == 2, "two child inputs are bound")
    check("conflict_no_unresolved", conflict.get("blocking_conflict_count") == 0 and conflict.get("unresolved_conflicts") == [], "no unresolved blocking conflict remains")
    check("conflict_fused_result", conflict.get("fused_result_type") == "repair_required", "parent fused result is repair_required")
    check("conflict_next_role", conflict.get("fused_next_role") == "candidate-constructor@0.2.0" and conflict.get("next_role_execution_authorized") is False, "parent selects but does not authorize repair execution")

    child_math = parsed.get(ART / "child_phys_math_p4_t02_b2_common_envelope_smuggling_audit.yaml", {})
    child_phil = parsed.get(ART / "child_phys_phil_p4_t02_b2_common_envelope_smuggling_audit.yaml", {})
    check("child_math_verdict", child_math.get("decisive_local_verdict", {}).get("selected_verdict") == "repair_required", "mathematics child confirms repair_required")
    check("child_phil_verdict", child_phil.get("smuggling_audit_result", {}).get("result_type") == "repair_required", "philosophy child confirms repair_required")
    check("child_parallel_revision", child_math.get("conflict_resolution_revision", {}).get("round") == 1 and child_phil.get("conflict_resolution_revision", {}).get("revision_round") == 1, "both children record parallel revision round one")

    tex_path = ART / "v22_p4_t02_b2_common_envelope_smuggling_audit_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.is_file() else ""
    for token in [
        "repair\\_required",
        "r_R+r_D=2r_S",
        "\\operatorname{rank}(\\Resp)=2",
        "continuous parameter",
        "FIND-V22-P4T02-B2-RESPONSE-IMAGE-RANK-001",
        "candidate-constructor@0.2.0",
        "Non-conclusion",
    ]:
        check(f"tex_token:{token}", token in tex, f"TeX contains {token}")

    compile_receipt = json.loads((ART / "v22_p4_t02_b2_common_envelope_smuggling_audit_latex_compile_receipt.json").read_text(encoding="utf-8"))
    check("compile_pass", compile_receipt.get("status") == "PASS", "bundled Tectonic compile passed")
    check("compile_source_hash", compile_receipt.get("source_sha256") == EXPECTED_HASHES["v22_p4_t02_b2_common_envelope_smuggling_audit_v1.tex"], "compile binds the final TeX source")
    check("compile_pages", compile_receipt.get("page_count") == 6 and compile_receipt.get("rendered_page_count") == 6, "six pages compiled and rendered")
    check("visual_all_pages", compile_receipt.get("visually_inspected_pages") == [1, 2, 3, 4, 5, 6] and compile_receipt.get("visual_inspection_status") == "PASS", "all six pages were inspected")
    check("visual_findings_clear", not any(compile_receipt.get("visual_findings", {}).values()), "no visual defect flags are set")
    check("pdf_non_authority", compile_receipt.get("tracked_pdf_created") is False and compile_receipt.get("proof_authority") is False, "temporary PDF is non-authoritative")

    task = parsed.get(TASK / "00_TASK.yaml", {})
    job = parsed.get(TASK / "jobs/AJ-RT-20260810-006-001.yaml", {})
    role = parsed.get(TASK / "roles/smuggling-auditor@0.2.0--RT-20260810-006.yaml", {})
    completion = parsed.get(TASK / "jobs/completions/AJC-AJ-RT-20260810-006-001.yaml", {})
    check("task_closed", task.get("status") == "completed" and task.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED", "task is closed precheckpoint")
    check("task_boundary", task.get("claim_boundary", {}).get("boundary_status") == "completed_closed", "task claim boundary is closed")
    check("job_completed", job.get("status") == "completed" and job.get("role_decomposition", {}).get("subagent_count") == 2, "one outer job with two child units completed")
    check("job_children_completed", all(child.get("status") == "completed" for child in job.get("role_decomposition", {}).get("children", [])), "job records both children completed")
    check("role_expired", role.get("status") == "expired_completed", "task overlay expired at completion")
    check("completion_result", completion.get("objective_result") == "repair_required_no_target_import_exact_response_rank_defect", "completion records exact result")
    check("completion_progress", completion.get("physics_progress_status", {}).get("status") == "no_distance_delta", "physics progress uses an allowed decisive status")
    check("completion_distance", completion.get("distance_to_gr_delta", {}).get("changed") is False, "completion keeps Distance-to-GR unchanged")
    check("completion_burdens", len(completion.get("distance_to_gr_status", [])) == 14, "all fourteen expanded burden rows are present")
    check("completion_payload", len(completion.get("new_mathematical_payload", [])) >= 5 and len(completion.get("mathematical_payload_manifest", [])) >= 4, "new mathematical payload and manifest are substantive")
    check("completion_freeze", completion.get("freeze_criteria_status", {}).get("freeze_decision") == "not_frozen" and completion.get("freeze_criteria_status", {}).get("next_allowed_route") == "candidate_constructor", "freeze evaluation selects bounded repair")
    check("completion_cycle", completion.get("route_cycle_control", {}).get("current_cycle_step") == "smuggling_auditor", "route-cycle control records the audit step")
    check("completion_audit", completion.get("smuggling_audit_result", {}).get("verdict") == "repair_required" and completion.get("smuggling_audit_result", {}).get("target_import_detected") is False, "completion audit result is exact")
    check("completion_next", completion.get("selected_next_route", {}).get("selected_next_packet_type") == "source_extension_candidate" and completion.get("selected_next_route", {}).get("executed") is False, "completion selects an unexecuted candidate repair")
    ontology = completion.get("ontology_law_research_packet", {})
    check("ontology_route", ontology.get("route") == "ontology-law-research-packet" and ontology.get("trigger_classification") == "derivation_critical_missing_source_law", "ontology-law route receipt is present")
    check("ontology_payload_mode", ontology.get("packet_payload_mode") == "candidate_law_refutation" and bool(ontology.get("candidate_law_refutation", {}).get("refuted_candidate")), "bounded information-count refutation is substantive")
    check("ontology_open_continuation", ontology.get("adoption_status", {}).get("status_pair") == "blocked_adoption_open_continuation", "adoption remains blocked while continuation stays open")
    check("ontology_human_gate", ontology.get("human_gate_request", {}).get("required_before_adoption") is True, "human authority is required before adoption")
    auth = completion.get("authorization_layers", {})
    check("completion_authority_false", all(value is False or value == "" for key, value in auth.items() if key != "protected_scoped_gate_review_scope"), "all protected and outward authorization flags remain false")
    check("project_signals_empty", completion.get("project_improvement_signals") == [], "no project-improvement signal is emitted")

    handoff_path = ROOT / "research_control/handoffs/handoff-1003.yaml"
    handoff = parsed.get(handoff_path, {})
    check("handoff_hash", sha256(handoff_path) == "b7926adde7570d49c8f90b196d03b151f022c324243bfe0b6fe7813d9ba184e8", "handoff hash is bound")
    check("handoff_completion_hash", handoff.get("completion_sha256") == EXPECTED_CONTROL_HASHES["jobs/completions/AJC-AJ-RT-20260810-006-001.yaml"], "handoff binds completion")
    check("handoff_status", handoff.get("status") == "ready_for_v22_p4_t02_b2_common_envelope_quotient_rank_repair_after_checkpoint", "handoff is checkpoint-gated")
    check("handoff_result", handoff.get("claim_boundary", {}).get("decisive_result") == "repair_required", "handoff records repair_required")
    check("handoff_rank", handoff.get("claim_boundary", {}).get("response_rank") == 2 and handoff.get("claim_boundary", {}).get("positive_projective_image_dimension") == 1, "handoff binds rank and projective dimension")
    check("handoff_next", handoff.get("required_next_packet", {}).get("executed") is False and handoff.get("selected_next_route", {}).get("role_family") == "candidate-constructor@0.2.0", "handoff selects an unexecuted Candidate Constructor repair")

    program = parsed.get(ROOT / "research_control/program_state.yaml", {})
    block = program.get("v22_p4_t02_b2_common_envelope_smuggling_audit", {})
    check("program_active", program.get("active_task_id") == "RT-20260810-006" and program.get("latest_handoff_id") == "handoff-1003", "program state points to RT006 and handoff-1003")
    check("program_block", block.get("decisive_result") == "repair_required" and block.get("response_rank") == 2, "program state contains the exact audit result")
    check("program_next", block.get("selected_next_packet_type") == "source_extension_candidate" and block.get("selected_next_execution_ready_now") is False, "program next route is checkpoint-gated")

    backlog = parsed.get(ROOT / "research_control/design/v22_recommendation_backlog.yaml", {})
    p4_t02 = next((item for item in backlog.get("plan_tasks", backlog if isinstance(backlog, list) else []) if isinstance(item, dict) and item.get("plan_task_id") == "P4-T02"), None)
    if p4_t02 is None and isinstance(backlog, dict):
        for value in backlog.values():
            if isinstance(value, list):
                p4_t02 = next((item for item in value if isinstance(item, dict) and item.get("plan_task_id") == "P4-T02"), None)
                if p4_t02:
                    break
    check("backlog_p4_t02", isinstance(p4_t02, dict), "P4-T02 backlog row exists")
    if isinstance(p4_t02, dict):
        check("backlog_audit", p4_t02.get("runtime_source_extension_smuggling_audit_executed") is True and p4_t02.get("runtime_source_extension_smuggling_audit_result") == "repair_required", "backlog records completed audit")
        check("backlog_rank", p4_t02.get("runtime_response_image_rank") == 2 and p4_t02.get("runtime_positive_projective_image_dimension") == 1, "backlog records exact rank result")
        check("backlog_repair", p4_t02.get("runtime_common_envelope_quotient_rank_repair_selected") is True and p4_t02.get("runtime_common_envelope_quotient_rank_repair_executed") is False, "backlog selects but does not execute repair")

    registry_expectations = [
        ("AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260810-006-001"),
        ("CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id", "CB-V22-P4-T02-B2-COMMON-HYPERBOLICITY-ENVELOPE-SMUGGLING-AUDIT-001"),
        ("DIRECTOR_DECISION_REGISTRY.csv", "decision_id", "DDR-20260810-006"),
        ("RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260810-006"),
        ("ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref", "smuggling-auditor@0.2.0--RT-20260810-006"),
        ("MARKDOWN_SOURCE_REGISTRY.csv", "object_id", "MD-V22-P4-T02-B2-PARENT-FUSION-COMMON-ENVELOPE-SMUGGLING-AUDIT-V1"),
        ("TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V22-P4-T02-B2-COMMON-ENVELOPE-SMUGGLING-AUDIT-V1"),
    ]
    for name, key, value in registry_expectations:
        matches = [row for row in csv_rows(ROOT / "registries" / name) if row.get(key) == value]
        check(f"registry:{name}", len(matches) == 1, f"{value} occurs exactly once")
        if matches and "validation_status" in matches[0]:
            check(f"registry_status:{name}", matches[0].get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED" or matches[0].get("validation_status") == "PASS", "registry row has a passing precheckpoint status")

    generated_wiki = [
        ROOT / "wiki/tex/tex-v22-p4-t02-b2-common-envelope-smuggling-audit-v1.md",
        ROOT / "wiki/markdown/md-v22-p4-t02-b2-parent-fusion-common-envelope-smuggling-audit-v1.md",
    ]
    for path in generated_wiki:
        check(f"generated_wiki:{path.name}", path.is_file(), "registered source derivative exists")

    for path in list(TASK.rglob("*")) + [ROOT / "research_control/handoffs/handoff-1003.yaml", ROOT / "research_control/handoffs/handoff-1003.md"]:
        if path.is_file() and path.suffix in {".yaml", ".md", ".tex", ".py", ".json"}:
            data = path.read_bytes()
            check(f"newline:{path.relative_to(ROOT)}", data.endswith(b"\n") and not data.endswith(b"\n\n"), "file has exactly one terminal newline")

    failures = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "v22_p4_t02_b2_common_envelope_smuggling_audit_validation_v1",
        "task_id": "RT-20260810-006",
        "job_id": "AJ-RT-20260810-006-001",
        "status": "PASS" if not failures else "FAIL",
        "decisive_result": "repair_required",
        "target_import_detected": False,
        "response_image_relation": "r_R+r_D=2*r_S",
        "response_rank": 2,
        "response_kernel_dimension": 2,
        "projective_image_parameter_count": 1,
        "realized_nonzero_sign_orbit_count": 6,
        "check_count": len(checks),
        "failure_count": len(failures),
        "checks": checks,
        "authority": "operational_validation_only_not_proof_or_physics_promotion",
        "authority_limits": {
            "candidate_repair_executed": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
            "proof_authority": False,
            "physics_promotion_authorized": False,
        },
    }

    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_common_envelope_smuggling_audit_compact_receipt_v1",
            "task_id": "RT-20260810-006",
            "job_id": "AJ-RT-20260810-006-001",
            "status": report["status"],
            "decisive_result": "repair_required",
            "target_import_detected": False,
            "response_rank": 2,
            "projective_image_parameter_count": 1,
            "realized_nonzero_sign_orbit_count": 6,
            "check_count": len(checks),
            "failure_count": len(failures),
            "full_report_path": str(REPORT.relative_to(ROOT)),
            "full_report_sha256": sha256(REPORT),
            "candidate_repair_executed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    output = report if args.json else {
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
    }
    print(json.dumps(output, indent=2, sort_keys=True) if args.json else output)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
