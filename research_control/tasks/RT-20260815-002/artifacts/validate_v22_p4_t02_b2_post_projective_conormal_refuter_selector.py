#!/usr/bin/env python3
"""Focused validator for the RT-20260815-002 post-projective-conormal selector."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[4]
TASK = REPO / "research_control/tasks/RT-20260815-002"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_post_projective_conormal_refuter_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_post_projective_conormal_refuter_selector_compact_receipt.json"
ROUTE = "A_SOURCE_DERIVED_OCCURRENCE_ADMISSIBILITY_THEOREM"
PACKET = "PKT-V22-P4T02-B2-SOURCE-DERIVED-OCCURRENCE-ADMISSIBILITY-DESCENT-KERNEL-THEOREM-V1"
ROLE = "ontology-formalizer@0.2.0"
ROUTE_LABEL = "ontology-law-research-packet"
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
        "decision_record": TASK / "DDR-20260815-002.md",
        "job": TASK / "jobs/AJ-RT-20260815-002-001.yaml",
        "role": TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260815-002.yaml",
        "route_comparison": ART / "v22_p4_t02_b2_post_projective_conormal_refuter_route_comparison_v1.yaml",
        "selector_decision": ART / "v22_p4_t02_b2_post_projective_conormal_refuter_selector_decision_v1.yaml",
        "future_packet": ART / "v22_p4_t02_b2_post_projective_conormal_refuter_selected_future_packet_v1.yaml",
        "model": ART / "v22_p4_t02_b2_post_projective_conormal_refuter_selector_model.py",
        "child_math": ART / "child_phys_math_p4_t02_b2_post_projective_conormal_refuter_selector.yaml",
        "child_phil": ART / "child_phys_phil_p4_t02_b2_post_projective_conormal_refuter_selector.yaml",
        "parent_review": ART / "parent_conflict_review_p4_t02_b2_post_projective_conormal_refuter_selector.yaml",
        "fusion_notes": ART / "parent_fusion_notes_p4_t02_b2_post_projective_conormal_refuter_selector.md",
        "manuscript": ART / "v22_p4_t02_b2_post_projective_conormal_refuter_route_selection_v1.tex",
        "latex_receipt": ART / "v22_p4_t02_b2_post_projective_conormal_refuter_selector_latex_compile_receipt.json",
        "provenance": ART / "v22_p4_t02_b2_post_projective_conormal_refuter_selector_provenance_manifest_v1.yaml",
        "documentation_impact": TASK / "documentation_impact.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260815-002-001.yaml",
        "handoff_yaml": REPO / "research_control/handoffs/handoff-1038.yaml",
        "handoff_md": REPO / "research_control/handoffs/handoff-1038.md",
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
        "task", "job", "role", "route_comparison", "selector_decision",
        "future_packet", "child_math", "child_phil", "parent_review",
        "provenance", "documentation_impact", "completion", "handoff_yaml",
    )
    docs: dict[str, dict[str, Any]] = {}
    try:
        for name in yaml_names:
            docs[name] = load_yaml(required[name])
            checks[f"unique_yaml_{name}"] = True
    except Exception as exc:
        failures.append(f"strict_yaml:{exc}")

    if not failures:
        route = docs["route_comparison"]
        decision = docs["selector_decision"]
        packet = docs["future_packet"]
        routes = route.get("routes", [])
        selected = [item for item in routes if item.get("selected") is True]
        check(len(routes) == 4, "route_count_four", checks, failures)
        check(len(selected) == 1 and selected[0].get("route_id") == ROUTE, "one_route_A_selected", checks, failures)
        selection = route.get("selection", {})
        check(selection.get("selected_packet_id") == PACKET, "route_packet_identity", checks, failures)
        check(selection.get("selected_packet_type") == "bounded_theoretical_calculation", "route_packet_type", checks, failures)
        check(selection.get("route_label") == ROUTE_LABEL, "route_label", checks, failures)
        check(selection.get("selected_next_role_family") == ROLE, "route_role", checks, failures)
        check(selection.get("selected_packet_executed") is False, "route_packet_unexecuted", checks, failures)
        check(set(route.get("preserved_freeze_labels", [])) == FREEZES, "route_eight_freezes", checks, failures)

        decisive = decision.get("decisive_result", {})
        check(decisive.get("route_id") == ROUTE and decisive.get("packet_id") == PACKET, "decision_identity", checks, failures)
        check(decisive.get("next_role_family") == ROLE and decisive.get("selected_packet_executed") is False, "decision_role_and_stop", checks, failures)
        distances = decision.get("distance_to_gr_status", [])
        check(len(distances) == 14 and all(row.get("status") == "no_delta" for row in distances), "distance_rows_14_all_no_delta", checks, failures)
        check(set(decision.get("preserved_freeze_labels", [])) == FREEZES, "decision_eight_freezes", checks, failures)

        packet_meta = packet.get("packet", {})
        check(packet_meta.get("packet_id") == PACKET and packet_meta.get("packet_type") == "bounded_theoretical_calculation", "future_packet_identity", checks, failures)
        check(packet_meta.get("route_label") == ROUTE_LABEL, "future_packet_route_label", checks, failures)
        check(packet_meta.get("next_role_family") == ROLE and packet_meta.get("selected_packet_executed") is False, "future_packet_role_and_stop", checks, failures)
        check(len(packet.get("formal_domains", [])) == 10, "future_packet_10_domains", checks, failures)
        check(len(packet.get("formal_objects", [])) == 12, "future_packet_12_objects", checks, failures)
        check(len(packet.get("formal_maps", [])) == 10, "future_packet_10_maps", checks, failures)
        check(len(packet.get("theorem_targets", [])) == 5, "future_packet_5_theorems", checks, failures)
        check(len(packet.get("proof_obligations", [])) == 14, "future_packet_14_obligations", checks, failures)
        check(len(packet.get("failure_branches", [])) == 12, "future_packet_12_failure_branches", checks, failures)
        check(set(packet.get("preserved_freeze_labels", [])) == FREEZES, "future_packet_eight_freezes", checks, failures)

        for child_name in ("child_math", "child_phil"):
            values = scalar_values(docs[child_name])
            check(ROUTE in values and PACKET in values and ROLE in values, f"{child_name}_canonical_selection", checks, failures)
            child_text = required[child_name].read_text(encoding="utf-8")
            check(child_text.count("no_delta") >= 14, f"{child_name}_fourteen_no_delta_tokens", checks, failures)
            check(all(label in child_text for label in FREEZES), f"{child_name}_eight_freezes", checks, failures)

        review = docs["parent_review"]
        check(review.get("unresolved_blocking_conflict_count") == 0, "parent_no_unresolved_conflict", checks, failures)
        check(review.get("final_selection", {}).get("selected_route_id") == ROUTE, "parent_review_route", checks, failures)
        check(review.get("final_selection", {}).get("selected_packet_id") == PACKET, "parent_review_packet", checks, failures)

        task = docs["task"]
        job = docs["job"]
        completion = docs["completion"]
        check(task.get("status") == "completed", "task_terminal", checks, failures)
        check(job.get("status") == "completed" and str(job.get("validation_status", "")).startswith("PASS"), "job_terminal_pass", checks, failures)
        check(str(completion.get("validation_status", "")).startswith("PASS"), "completion_pass", checks, failures)
        completion_text = required["completion"].read_text(encoding="utf-8")
        check(PACKET in completion_text and completion_text.count("no_delta") >= 14, "completion_packet_and_distance", checks, failures)

        handoff = docs["handoff_yaml"]
        check(handoff.get("handoff_id") == "handoff-1038", "handoff_identity", checks, failures)
        check(PACKET in scalar_values(handoff), "handoff_packet_identity", checks, failures)
        check(False in scalar_values(handoff), "handoff_contains_unexecuted_false", checks, failures)

        manifest = docs["provenance"]
        entries = manifest.get("sources", [])
        manifest_ok = bool(entries)
        for entry in entries:
            source_path = REPO / entry["path"]
            manifest_ok = manifest_ok and source_path.is_file() and sha256(source_path) == entry["sha256"]
        check(manifest_ok, "provenance_hashes_live", checks, failures)

        try:
            model = json.loads(subprocess.check_output([sys.executable, str(required["model"]), "--json"], text=True))
            check(model.get("status") == "PASS" and model.get("check_count") == 28 and model.get("pass_count") == 28, "model_28_of_28", checks, failures)
        except Exception as exc:
            failures.append(f"model:{exc}")

        latex = json.loads(required["latex_receipt"].read_text(encoding="utf-8"))
        check(latex.get("compile_status") == "PASS", "latex_compile_pass", checks, failures)
        check(latex.get("visual_inspection", {}).get("status") == "PASS", "latex_visual_pass", checks, failures)
        check(latex.get("page_count", 0) == 4 and latex.get("visual_inspection", {}).get("pages_inspected") == 4, "latex_all_four_pages_inspected", checks, failures)
        check(latex.get("log_scan", {}).get("overfull_boxes") == 0 and latex.get("log_scan", {}).get("underfull_boxes") == 0, "latex_box_scan_clean", checks, failures)

        tex_text = required["manuscript"].read_text(encoding="utf-8")
        notes_text = required["fusion_notes"].read_text(encoding="utf-8")
        check(PACKET in tex_text and PACKET in notes_text, "registered_sources_packet_identity", checks, failures)
        tex_registry = (REPO / "registries/TEX_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
        md_registry = (REPO / "registries/MARKDOWN_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
        check("TEX-V22-P4-T02-B2-POST-PROJECTIVE-CONORMAL-REFUTER-ROUTE-SELECTION-V1" in tex_registry, "tex_registry_row", checks, failures)
        check("MD-V22-P4-T02-B2-PARENT-FUSION-POST-PROJECTIVE-CONORMAL-REFUTER-SELECTOR-V1" in md_registry, "markdown_registry_row", checks, failures)

    status = "PASS" if not failures and all(checks.values()) else "FAIL"
    result = {
        "schema_id": "v22_p4_t02_b2_post_projective_conormal_refuter_selector_validation_v1",
        "status": status,
        "task_id": "RT-20260815-002",
        "job_id": "AJ-RT-20260815-002-001",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "failures": failures,
        "authority_note": "Validation and rendering are process evidence only and do not prove or adopt an occurrence law or execute the selected packet.",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_post_projective_conormal_refuter_selector_compact_receipt_v1",
            "status": status,
            "task_id": "RT-20260815-002",
            "job_id": "AJ-RT-20260815-002-001",
            "check_count": len(checks),
            "pass_count": sum(checks.values()),
            "validation_report_sha256": sha256(REPORT),
            "model_status": checks.get("model_28_of_28", False),
            "selected_packet_executed": False,
            "distance_to_gr_changed": False,
            "authority_note": "Compact process receipt only.",
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
