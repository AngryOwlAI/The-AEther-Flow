#!/usr/bin/env python3
"""Focused validator for the RT-20260815-003 occurrence-layer packet."""

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
TASK = REPO / "research_control/tasks/RT-20260815-003"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_validation.json"
COMPACT = ART / "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_compact_receipt.json"
RESULT = "current_source_provenance_or_typing_obstruction"
OBSTRUCTION = (
    "OB-V22-P4T02-B2-SOURCE-DERIVED-OCCURRENCE-ADMISSIBILITY-"
    "DESCENT-KERNEL-CURRENT-SOURCE-TYPING-PROVENANCE-001"
)
SUCCESSOR = (
    "PKT-V22-P4T02-B2-POST-OCCURRENCE-ADMISSIBILITY-TYPING-"
    "PROVENANCE-OBSTRUCTION-THEORETICAL-CONTINUATION-SELECTION-V1"
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
ALLOWED_RESULTS = {
    "source_derived_occurrence_admissibility_descent_kernel_theorem",
    "proposal_only_occurrence_law_formalized_pending_smuggling_audit",
    "current_source_provenance_or_typing_obstruction",
    "locality_or_descent_obstruction",
    "invariant_occurrence_kernel_obstruction",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(
                f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}"
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


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


def check(
    condition: bool,
    label: str,
    checks: dict[str, bool],
    failures: list[str],
) -> None:
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
        "decision_record": TASK / "DDR-20260815-003.md",
        "job": TASK / "jobs/AJ-RT-20260815-003-001.yaml",
        "role": TASK / "roles/ontology-formalizer@0.2.0--RT-20260815-003.yaml",
        "controls": ART / "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_controls_v1.yaml",
        "record": ART / "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_record_v1.yaml",
        "model": ART / "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_model.py",
        "child_math": ART / "child_phys_math_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel.yaml",
        "child_phil": ART / "child_phys_phil_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel.yaml",
        "parent_review": ART / "parent_conflict_review_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel.yaml",
        "fusion_notes": ART / "parent_fusion_notes_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel.md",
        "manuscript": ART / "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_v1.tex",
        "latex_receipt": ART / "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_latex_compile_receipt.json",
        "provenance": ART / "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_provenance_manifest_v1.yaml",
        "documentation_impact": TASK / "documentation_impact.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260815-003-001.yaml",
        "handoff_yaml": REPO / "research_control/handoffs/handoff-1039.yaml",
        "handoff_md": REPO / "research_control/handoffs/handoff-1039.md",
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
        "task",
        "job",
        "role",
        "controls",
        "record",
        "child_math",
        "child_phil",
        "parent_review",
        "provenance",
        "documentation_impact",
        "completion",
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
        check(record.get("result_type") == RESULT, "record_result", checks, failures)
        check(record.get("result_count") == 1, "record_one_result", checks, failures)
        check(record.get("obstruction_id") == OBSTRUCTION, "record_obstruction", checks, failures)
        check(len(record.get("formal_domains", [])) == 10, "record_10_domains", checks, failures)
        check(len(record.get("formal_objects", [])) == 12, "record_12_objects", checks, failures)
        check(len(record.get("formal_maps", [])) == 10, "record_10_maps", checks, failures)
        check(len(record.get("theorem_results", [])) == 5, "record_5_theorems", checks, failures)
        check(len(record.get("new_mathematical_payload", [])) == 6, "record_6_payloads", checks, failures)
        check(len(record.get("proof_obligations", [])) == 14, "record_14_obligations", checks, failures)
        check(len(record.get("failure_branches", [])) == 12, "record_12_failure_branches", checks, failures)
        check(
            sum(row.get("status") == "triggered_decisive" for row in record.get("failure_branches", [])) == 1,
            "one_decisive_failure_branch",
            checks,
            failures,
        )
        check(
            {row.get("freeze_id") for row in record.get("preserved_freezes", [])}
            == FREEZES,
            "record_eight_freezes",
            checks,
            failures,
        )
        distances = record.get("distance_to_gr_status", [])
        check(
            len(distances) == 14
            and all(row.get("task_delta") == "no_delta" for row in distances),
            "record_14_literal_no_delta",
            checks,
            failures,
        )
        successor = record.get("selected_successor", {})
        check(
            successor.get("packet_id") == SUCCESSOR
            and successor.get("packet_type") == "theoretical_continuation_selector"
            and successor.get("role_family") == "theoretical-continuation-selector@0.1.0",
            "record_successor_identity",
            checks,
            failures,
        )
        check(
            successor.get("status") == "selected_not_executed"
            and successor.get("executed") is False,
            "record_successor_stop",
            checks,
            failures,
        )

        check(controls.get("result_type") == RESULT, "controls_result", checks, failures)
        check(controls.get("obstruction_id") == OBSTRUCTION, "controls_obstruction", checks, failures)
        check(len(controls.get("conditional_theorem_family", [])) == 5, "controls_5_theorems", checks, failures)
        check(len(controls.get("exact_controls", [])) == 5, "controls_5_exact_controls", checks, failures)
        check(
            controls.get("typing_audit", {}).get("phi_src_semantics_added") is False,
            "controls_phi_uninterpreted",
            checks,
            failures,
        )

        for child_name in ("child_math", "child_phil"):
            values = scalar_values(docs[child_name])
            text = required[child_name].read_text(encoding="utf-8")
            check(RESULT in values or RESULT in text, f"{child_name}_result", checks, failures)
            check(OBSTRUCTION in values or OBSTRUCTION in text, f"{child_name}_obstruction", checks, failures)
            check(SUCCESSOR in values or SUCCESSOR in text, f"{child_name}_successor", checks, failures)
            check(all(freeze in text for freeze in FREEZES), f"{child_name}_eight_freezes", checks, failures)
            check(text.count("no_delta") >= 14, f"{child_name}_fourteen_no_delta", checks, failures)
            child_result_values = {value for value in values if value in ALLOWED_RESULTS}
            check(child_result_values == {RESULT}, f"{child_name}_one_permitted_result", checks, failures)

        review = docs["parent_review"]
        check(
            review.get("unresolved_blocking_conflict_count") == 0,
            "parent_no_unresolved_conflict",
            checks,
            failures,
        )
        final_result = review.get("final_result", {})
        check(
            final_result.get("result_type") == RESULT
            and final_result.get("obstruction_id") == OBSTRUCTION,
            "parent_review_result",
            checks,
            failures,
        )

        try:
            model = json.loads(
                subprocess.check_output(
                    [sys.executable, str(required["model"]), "--json"], text=True
                )
            )
            check(
                model.get("status") == "PASS"
                and model.get("result_type") == RESULT
                and model.get("check_count") == 36
                and model.get("pass_count") == 36,
                "model_36_of_36",
                checks,
                failures,
            )
        except Exception as exc:
            failures.append(f"model:{exc}")

        latex = json.loads(required["latex_receipt"].read_text(encoding="utf-8"))
        check(latex.get("compile_status") == "PASS", "latex_compile_pass", checks, failures)
        check(latex.get("source_sha256") == sha256(required["manuscript"]), "latex_source_hash", checks, failures)
        check(latex.get("page_count") == 5, "latex_page_count", checks, failures)
        visual = latex.get("visual_inspection", {})
        check(
            visual.get("status") == "PASS" and visual.get("pages_inspected") == 5,
            "latex_all_pages_visual_pass",
            checks,
            failures,
        )
        log_scan = latex.get("log_scan", {})
        check(
            log_scan.get("overfull_boxes") == 0
            and log_scan.get("underfull_boxes") == 0
            and log_scan.get("fatal_errors") == 0,
            "latex_log_clean",
            checks,
            failures,
        )

        manifest = docs["provenance"]
        entries = manifest.get("sources", [])
        manifest_ok = bool(entries)
        for entry in entries:
            source_path = REPO / entry["path"]
            manifest_ok = (
                manifest_ok
                and source_path.is_file()
                and sha256(source_path) == entry["sha256"]
            )
        check(manifest_ok, "provenance_hashes_live", checks, failures)

        task = docs["task"]
        job = docs["job"]
        completion = docs["completion"]
        check(task.get("status") == "completed", "task_terminal", checks, failures)
        check(
            job.get("status") == "completed"
            and str(job.get("validation_status", "")).startswith("PASS"),
            "job_terminal_pass",
            checks,
            failures,
        )
        check(
            completion.get("status") == "completed"
            and str(completion.get("validation_status", "")).startswith("PASS"),
            "completion_terminal_pass",
            checks,
            failures,
        )
        completion_text = required["completion"].read_text(encoding="utf-8")
        check(
            RESULT in completion_text
            and OBSTRUCTION in completion_text
            and SUCCESSOR in completion_text
            and completion_text.count("no_delta") >= 14,
            "completion_result_and_distance",
            checks,
            failures,
        )

        handoff = docs["handoff_yaml"]
        check(handoff.get("handoff_id") == "handoff-1039", "handoff_identity", checks, failures)
        handoff_text = required["handoff_yaml"].read_text(encoding="utf-8")
        check(
            RESULT in handoff_text and OBSTRUCTION in handoff_text and SUCCESSOR in handoff_text,
            "handoff_result_and_successor",
            checks,
            failures,
        )
        check(handoff_text.count("no_delta") >= 14, "handoff_14_no_delta", checks, failures)

        tex_text = required["manuscript"].read_text(encoding="utf-8")
        notes_text = required["fusion_notes"].read_text(encoding="utf-8")
        check(
            RESULT in tex_text and OBSTRUCTION in tex_text and SUCCESSOR in tex_text,
            "manuscript_identities",
            checks,
            failures,
        )
        check(
            RESULT in notes_text and OBSTRUCTION in notes_text and SUCCESSOR in notes_text,
            "fusion_identities",
            checks,
            failures,
        )
        tex_registry = (REPO / "registries/TEX_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
        md_registry = (REPO / "registries/MARKDOWN_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
        check(
            "TEX-V22-P4-T02-B2-SOURCE-DERIVED-OCCURRENCE-ADMISSIBILITY-DESCENT-KERNEL-V1" in tex_registry,
            "tex_registry_row",
            checks,
            failures,
        )
        check(
            "MD-V22-P4-T02-B2-PARENT-FUSION-SOURCE-DERIVED-OCCURRENCE-ADMISSIBILITY-DESCENT-KERNEL-V1" in md_registry,
            "markdown_registry_row",
            checks,
            failures,
        )

    status = "PASS" if not failures and all(checks.values()) else "FAIL"
    result = {
        "schema_id": "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_validation_v1",
        "status": status,
        "task_id": "RT-20260815-003",
        "job_id": "AJ-RT-20260815-003-001",
        "result_type": RESULT,
        "obstruction_id": OBSTRUCTION,
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "failures": failures,
        "authority_note": "Focused validation is conformance evidence only. It does not form or adopt the missing source occurrence law, interpret Phi_src, assign physical probability, change Distance-to-GR, execute the successor, or authorize promotion.",
    }
    if args.write_report:
        REPORT.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        compact = {
            "schema_id": "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_compact_receipt_v1",
            "status": status,
            "task_id": "RT-20260815-003",
            "job_id": "AJ-RT-20260815-003-001",
            "result_type": RESULT,
            "obstruction_id": OBSTRUCTION,
            "check_count": len(checks),
            "pass_count": sum(checks.values()),
            "validation_report_sha256": sha256(REPORT),
            "model_status": checks.get("model_36_of_36", False),
            "selected_successor_executed": False,
            "distance_to_gr_changed": False,
            "authority_note": "Compact process receipt only.",
        }
        COMPACT.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
