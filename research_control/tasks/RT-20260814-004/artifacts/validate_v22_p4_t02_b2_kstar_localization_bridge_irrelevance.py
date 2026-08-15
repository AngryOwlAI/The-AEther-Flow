#!/usr/bin/env python3
"""Focused validator for the RT-20260814-004 K-star locality theorem."""

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


REPO = Path(__file__).resolve().parents[4]
TASK = REPO / "research_control/tasks/RT-20260814-004"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_validation.json"
COMPACT = ART / "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_compact_receipt.json"
RESULT = "scoped_k_star_bridge_irrelevance_theorem"
REFUTER_CLASS = "source_side_irrelevance_theorem_path"
THEOREM = "THM-V22-P4T02-B2-KSTAR-STANDALONE-LOCAL-BRIDGE-IRRELEVANCE-001"
LOCAL_FREEZE = "NDCL-V22-P4T02-B2-KSTAR-STANDALONE-LOCAL-BRIDGE-IRRELEVANCE"
PACKET = "PKT-V22-P4T02-B2-SOURCE-LOCAL-STRUCTURE-GROUP-REDUCTION-BRIDGE-WITNESS-CONSTRUCTION-V1"
ROLE = "candidate-constructor@0.2.0"
INHERITED_FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        result: list[Any] = []
        for key, item in value.items():
            result.extend(scalar_values(key))
            result.extend(scalar_values(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(scalar_values(item))
        return result
    return [value]


def csv_row(path: Path, key: str, value: str) -> dict[str, str] | None:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get(key) == value:
                return row
    return None


def check(condition: bool, label: str, checks: dict[str, bool], failures: list[str]) -> None:
    checks[label] = bool(condition)
    if not condition:
        failures.append(label)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    required = {
        "task": TASK / "00_TASK.yaml",
        "decision_record": TASK / "DDR-20260814-004.md",
        "job": TASK / "jobs/AJ-RT-20260814-004-001.yaml",
        "role": TASK / "roles/refuter@0.2.0--RT-20260814-004.yaml",
        "record": ART / "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_record_v1.yaml",
        "controls": ART / "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_controls_v1.yaml",
        "model": ART / "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_model.py",
        "child_math": ART / "child_phys_math_p4_t02_b2_kstar_localization_bridge_irrelevance.yaml",
        "child_phil": ART / "child_phys_phil_p4_t02_b2_kstar_localization_bridge_irrelevance.yaml",
        "parent_review": ART / "parent_conflict_review_p4_t02_b2_kstar_localization_bridge_irrelevance.yaml",
        "fusion_notes": ART / "parent_fusion_notes_p4_t02_b2_kstar_localization_bridge_irrelevance.md",
        "manuscript": ART / "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_theorem_v1.tex",
        "latex_receipt": ART / "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_latex_compile_receipt.json",
        "provenance": ART / "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_provenance_manifest_v1.yaml",
        "documentation_impact": TASK / "documentation_impact.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260814-004-001.yaml",
        "handoff_yaml": REPO / "research_control/handoffs/handoff-1034.yaml",
        "handoff_md": REPO / "research_control/handoffs/handoff-1034.md",
        "program_state": REPO / "research_control/program_state.yaml",
        "backlog": REPO / "research_control/design/v22_recommendation_backlog.yaml",
    }
    checks: dict[str, bool] = {}
    failures: list[str] = []
    for name, path in required.items():
        check(path.is_file(), f"required_path_{name}", checks, failures)

    if failures:
        result = {"status": "FAIL", "checks": checks, "failures": failures}
        print(json.dumps(result, indent=2, sort_keys=True) if args.json else "FAIL")
        return 1

    yaml_names = (
        "task", "job", "role", "record", "controls", "child_math", "child_phil",
        "parent_review", "provenance", "documentation_impact", "completion",
        "handoff_yaml",
    )
    docs: dict[str, dict[str, Any]] = {}
    try:
        for name in yaml_names:
            docs[name] = load_yaml(required[name])
            checks[f"unique_yaml_{name}"] = True
    except Exception as exc:
        failures.append(f"strict_yaml:{exc}")

    if not failures:
        record = docs["record"]
        controls = docs["controls"]
        check(record.get("result_type") == RESULT, "record_exclusive_result", checks, failures)
        check(record.get("result_count") == 1, "record_result_count_one", checks, failures)
        check(record.get("refuter_result_class") == REFUTER_CLASS, "record_refuter_class", checks, failures)
        check(record.get("theorem_id") == THEOREM, "record_theorem_identity", checks, failures)
        check(len(record.get("proof_obligations", [])) == 14, "record_14_obligations", checks, failures)
        check(len(record.get("failure_branches", [])) == 12, "record_12_failure_branches", checks, failures)
        check(len(record.get("new_mathematical_payload", [])) == 5, "record_five_payloads", checks, failures)
        check(len(record.get("predeclared_bridge_grammar", {}).get("candidates", [])) == 6, "record_six_candidates", checks, failures)
        check(set(record.get("preserved_freeze_labels", [])) == INHERITED_FREEZES, "record_six_inherited_freezes", checks, failures)
        check(set(record.get("active_freeze_labels", [])) == INHERITED_FREEZES | {LOCAL_FREEZE}, "record_seven_active_freezes", checks, failures)
        distances = record.get("distance_to_gr_status", [])
        check(len(distances) == 14 and all(row.get("status") == "no_delta" for row in distances), "record_14_no_delta", checks, failures)
        successor = record.get("selected_successor", {})
        check(successor.get("packet_id") == PACKET and successor.get("next_role") == ROLE, "record_successor_identity", checks, failures)
        check(successor.get("packet_type") == "source_extension_candidate" and successor.get("status") == "selected_not_executed", "record_successor_type_and_stop", checks, failures)
        check(record.get("authority_limits", {}).get("successor_executed") is False, "record_successor_unexecuted", checks, failures)
        check(record.get("downstream_locks", {}).get("p4_t03_locked") is True, "record_p4_t03_locked", checks, failures)

        check(controls.get("result_type") == RESULT and controls.get("refuter_result_class") == REFUTER_CLASS, "controls_result_and_class", checks, failures)
        check(len(controls.get("predeclared_bridge_grammar", {}).get("candidates", [])) == 6, "controls_six_candidates", checks, failures)
        check(len(controls.get("exact_control_families", [])) == 11, "controls_11_families", checks, failures)
        check(len(controls.get("theorem_results", [])) == 5, "controls_five_theorems", checks, failures)
        check(len(controls.get("proof_obligations", [])) == 14, "controls_14_obligations", checks, failures)
        check(len(controls.get("failure_branches", [])) == 12, "controls_12_failure_branches", checks, failures)
        check(controls.get("freeze_criteria_status", {}).get("active_freeze_count") == 7, "controls_seven_freezes", checks, failures)

        for child_name, expected_hash in (
            ("child_math", "fa68b3019c16116e0b6d9dc5d25911afbcb31ac7c4c61e8f51b6ef1281b9d1ce"),
            ("child_phil", "dd5c46e6daaa1ea0bb5589bf9fb589d9b753fe2e77551abd83d91b5135985dbc"),
        ):
            values = scalar_values(docs[child_name])
            check(sha256(required[child_name]) == expected_hash, f"{child_name}_hash", checks, failures)
            check(RESULT in values and REFUTER_CLASS in values and PACKET in values and ROLE in values, f"{child_name}_canonical_result", checks, failures)
            check(docs[child_name].get("conflict_resolution_revision", {}).get("unresolved_conflict_count") == 0, f"{child_name}_conflict_resolved", checks, failures)
            child_text = required[child_name].read_text(encoding="utf-8")
            check(child_text.count("no_delta") >= 14, f"{child_name}_14_no_delta_tokens", checks, failures)
            check(all(label in child_text for label in INHERITED_FREEZES), f"{child_name}_six_inherited_freezes", checks, failures)

        review = docs["parent_review"]
        check(review.get("unresolved_blocking_conflict_count") == 0, "parent_no_unresolved_conflict", checks, failures)
        check(review.get("conflict_review", {}).get("conflict_resolution_rounds_used") == 1, "parent_one_resolution_round", checks, failures)
        check(review.get("final_result", {}).get("scientific_result") == RESULT, "parent_result", checks, failures)
        check(review.get("final_result", {}).get("selected_packet_id") == PACKET, "parent_packet", checks, failures)

        task = docs["task"]
        job = docs["job"]
        completion = docs["completion"]
        check(task.get("status") == "completed" and str(task.get("validation_status", "")).startswith("PASS"), "task_terminal", checks, failures)
        check(job.get("status") == "completed" and str(job.get("validation_status", "")).startswith("PASS"), "job_terminal", checks, failures)
        check(str(completion.get("validation_status", "")).startswith("PASS") and completion.get("objective_result") == RESULT, "completion_pass_and_result", checks, failures)
        completion_distances = completion.get("distance_to_gr_status", [])
        check(len(completion_distances) == 14 and all(row.get("status") == "no_delta" for row in completion_distances), "completion_14_no_delta", checks, failures)
        check(completion.get("selected_successor", {}).get("packet_id") == PACKET and completion.get("selected_successor", {}).get("executed") is False, "completion_successor_unexecuted", checks, failures)

        handoff = docs["handoff_yaml"]
        check(handoff.get("handoff_id") == "handoff-1034", "handoff_identity", checks, failures)
        check(handoff.get("required_next_packet", {}).get("packet_id") == PACKET, "handoff_packet_identity", checks, failures)
        check(handoff.get("required_next_packet", {}).get("status") == "selected_not_executed", "handoff_packet_unexecuted", checks, failures)
        check(handoff.get("completion_sha256") == sha256(required["completion"]), "handoff_completion_hash", checks, failures)
        handoff_distances = handoff.get("distance_to_gr_status", [])
        check(len(handoff_distances) == 14 and all(row.get("status") == "no_delta" for row in handoff_distances), "handoff_14_no_delta", checks, failures)

        state_text = required["program_state"].read_text(encoding="utf-8")
        check('active_task_id: "RT-20260814-004"' in state_text and 'latest_handoff_id: "handoff-1034"' in state_text, "program_state_frontier_identity", checks, failures)
        check(f'decisive_result: "{RESULT}"' in state_text and "active_freeze_count: 7" in state_text, "program_state_result_and_freeze", checks, failures)
        check(f'selected_successor_packet_id: "{PACKET}"' in state_text and "selected_successor_executed: false" in state_text, "program_state_successor", checks, failures)
        backlog_text = required["backlog"].read_text(encoding="utf-8")
        check("runtime_kstar_localization_bridge_irrelevance_theorem_result: scoped_k_star_bridge_irrelevance_theorem" in backlog_text, "backlog_result", checks, failures)
        check(PACKET in backlog_text and "runtime_selected_next_role_family: candidate-constructor@0.2.0" in backlog_text, "backlog_successor", checks, failures)

        manifest = docs["provenance"]
        entries = manifest.get("sources", [])
        manifest_ok = len(entries) == manifest.get("source_count") == 21
        for entry in entries:
            path = REPO / entry["path"]
            manifest_ok = manifest_ok and path.is_file() and sha256(path) == entry["sha256"]
        check(manifest_ok, "provenance_21_hashes_live", checks, failures)

        try:
            model = json.loads(subprocess.check_output([sys.executable, str(required["model"]), "--json"], text=True))
            check(model.get("status") == "PASS" and model.get("check_count") == 18 and model.get("pass_count") == 18, "model_18_of_18", checks, failures)
        except Exception as exc:
            failures.append(f"model:{exc}")

        latex = json.loads(required["latex_receipt"].read_text(encoding="utf-8"))
        check(latex.get("compile_status") == "PASS" and latex.get("warning_count") == 0, "latex_compile_clean", checks, failures)
        visual = latex.get("visual_inspection", {})
        check(visual.get("status") == "PASS" and visual.get("pages_inspected") == latex.get("page_count") == 4, "latex_four_pages_visual", checks, failures)
        check(latex.get("source_sha256") == sha256(required["manuscript"]), "latex_source_hash", checks, failures)

        tex_row = csv_row(REPO / "registries/TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V22-P4-T02-B2-KSTAR-LOCALIZATION-BRIDGE-IRRELEVANCE-THEOREM-V1")
        md_row = csv_row(REPO / "registries/MARKDOWN_SOURCE_REGISTRY.csv", "object_id", "MD-V22-P4-T02-B2-PARENT-FUSION-KSTAR-LOCALIZATION-BRIDGE-IRRELEVANCE-V1")
        task_row = csv_row(REPO / "registries/RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260814-004")
        job_row = csv_row(REPO / "registries/AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260814-004-001")
        claim_row = csv_row(REPO / "registries/CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id", "CB-V22-P4-T02-B2-KSTAR-LOCALIZATION-BRIDGE-IRRELEVANCE-001")
        check(tex_row is not None and tex_row.get("source_hash") == sha256(required["manuscript"]), "tex_registry_hash", checks, failures)
        check(md_row is not None and md_row.get("source_hash") == sha256(required["fusion_notes"]), "markdown_registry_hash", checks, failures)
        check(task_row is not None and task_row.get("status") == "completed", "task_registry_terminal", checks, failures)
        check(job_row is not None and job_row.get("status") == "completed" and bool(job_row.get("completion_path")), "job_registry_terminal", checks, failures)
        check(claim_row is not None and claim_row.get("status") == "completed", "claim_boundary_registry_terminal", checks, failures)

        doc = docs["documentation_impact"]
        check(doc.get("status") == "completed" and doc.get("docs_update_required") is True, "documentation_impact_complete", checks, failures)
        check(doc.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED", "documentation_impact_status", checks, failures)

        all_text = "\n".join(path.read_text(encoding="utf-8") for path in required.values() if path.suffix in {".yaml", ".md", ".tex"})
        check("P4-T03 remains locked" in all_text or "p4_t03_locked" in all_text, "p4_t03_lock_language", checks, failures)
        check("global no-go" in all_text, "global_no_go_guard_language", checks, failures)

    status = "PASS" if not failures and all(checks.values()) else "FAIL"
    result = {
        "schema_id": "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_validation_v1",
        "status": status,
        "task_id": "RT-20260814-004",
        "job_id": "AJ-RT-20260814-004-001",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "failures": failures,
        "authority_note": "Validation and rendering are process evidence only and do not adopt K_star or the future source law, assign physical meaning, promote physics, or execute the selected packet.",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_kstar_localization_bridge_irrelevance_compact_receipt_v1",
            "status": status,
            "task_id": "RT-20260814-004",
            "job_id": "AJ-RT-20260814-004-001",
            "check_count": len(checks),
            "pass_count": sum(checks.values()),
            "validation_report_sha256": sha256(REPORT),
            "model_status": checks.get("model_18_of_18", False),
            "scientific_result": RESULT,
            "refuter_result_class": REFUTER_CLASS,
            "candidate_local_freeze_id": LOCAL_FREEZE,
            "active_freeze_count": 7,
            "selected_packet_executed": False,
            "distance_to_gr_changed": False,
            "authority_note": "Compact process receipt only.",
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
