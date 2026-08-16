#!/usr/bin/env python3
"""Focused validator for the RT-20260815-006 theoretical selector."""

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


REPO = Path(__file__).resolve().parents[4]
TASK = REPO / "research_control/tasks/RT-20260815-006"
ART = TASK / "artifacts"
REPORT = ART / (
    "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
    "selector_validation.json"
)
COMPACT = ART / (
    "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
    "selector_compact_receipt.json"
)

SELECTED_ROUTE = "A_CANONICAL_SOURCE_OPEN_EVENT_FIBRATION_TYPING_DESCENT_PRECURSOR"
SELECTED_PACKET = (
    "PKT-V22-P4T02-B2-CANONICAL-SOURCE-OPEN-EVENT-FIBRATION-"
    "TYPING-DESCENT-THEOREM-V1"
)
SELECTED_TYPE = "bounded_theoretical_calculation"
SELECTED_ROLE = "ontology-formalizer@0.2.0"
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
BURDENS = {
    "Source ontology primitives",
    "Source equivalence EqSrc",
    "RetainH",
    "GenH",
    "ObsLoc_lc",
    "Resp_lc",
    "M_src",
    "g_eff",
    "matter coupling",
    "Einstein equations",
    "finite-variation robustness",
    "benchmark promotion",
    "Gate Chair status",
    "current route freeze or hard-fail status",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe loader that rejects duplicate mapping keys."""


def _construct_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def recursive_no_delta_rows(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if "burden" in value and (
            value.get("status") == "no_delta"
            or value.get("task_delta") == "no_delta"
        ):
            rows.append(value)
        for child in value.values():
            rows.extend(recursive_no_delta_rows(child))
    elif isinstance(value, list):
        for child in value:
            rows.extend(recursive_no_delta_rows(child))
    return rows


def csv_row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get(key) == value:
                return row
    return {}


def validate() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, bool] = {}
    paths = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260815-006-001.yaml",
        "role": TASK / (
            "roles/theoretical-continuation-selector@0.1.0--RT-20260815-006.yaml"
        ),
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260815-006-001.yaml",
        "math_child": ART / (
            "child_phys_math_p4_t02_b2_post_occurrence_typing_provenance_"
            "obstruction_selector.yaml"
        ),
        "phil_child": ART / (
            "child_phys_phil_p4_t02_b2_post_occurrence_typing_provenance_"
            "obstruction_selector.yaml"
        ),
        "conflict": ART / (
            "parent_conflict_review_p4_t02_b2_post_occurrence_typing_"
            "provenance_obstruction_selector.yaml"
        ),
        "comparison": ART / (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "route_comparison_v1.yaml"
        ),
        "decision": ART / (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "selector_decision_v1.yaml"
        ),
        "packet": ART / (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "selected_future_packet_v1.yaml"
        ),
        "manifest": ART / (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "selector_provenance_manifest_v1.yaml"
        ),
        "tex": ART / (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "route_selection_v1.tex"
        ),
        "fusion": ART / (
            "parent_fusion_notes_p4_t02_b2_post_occurrence_typing_"
            "provenance_obstruction_selector.md"
        ),
        "compile": ART / (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "selector_latex_compile_receipt.json"
        ),
        "model": ART / (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "selector_model.py"
        ),
        "handoff": REPO / "research_control/handoffs/handoff-1040.yaml",
    }
    checks["all_expected_artifacts_exist"] = all(path.exists() for path in paths.values())
    if not checks["all_expected_artifacts_exist"]:
        errors.extend(
            str(path.relative_to(REPO)) for path in paths.values() if not path.exists()
        )

    yaml_names = (
        "task",
        "job",
        "role",
        "completion",
        "math_child",
        "phil_child",
        "conflict",
        "comparison",
        "decision",
        "packet",
        "manifest",
        "handoff",
    )
    loaded: dict[str, dict[str, Any]] = {}
    for name in yaml_names:
        if not paths[name].exists():
            continue
        try:
            loaded[name] = load_yaml(paths[name])
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")
    checks["unique_key_yaml_parse"] = len(loaded) == len(yaml_names)

    if all(name in loaded for name in ("task", "job", "role")):
        checks["terminal_control_state"] = (
            loaded["task"].get("status") == "completed"
            and loaded["task"].get("validation_status")
            == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
            and loaded["task"].get("claim_boundary", {}).get("boundary_status")
            == "completed_checkpoint_pending"
            and loaded["job"].get("status") == "completed"
            and loaded["job"].get("validation_status")
            == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
            and loaded["role"].get("status") == "expired"
            and loaded["role"].get("validation_status")
            == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
        )

    if "manifest" in loaded:
        manifest = loaded["manifest"]
        sources = manifest.get("governing_sources", []) + manifest.get(
            "fused_artifacts", []
        )
        mismatches: list[str] = []
        for item in sources:
            source = REPO / str(item.get("path", ""))
            if not source.exists() or sha256(source) != str(item.get("sha256", "")):
                mismatches.append(str(item.get("path", "")))
        checks["source_manifest_hashes"] = not mismatches and len(sources) == 26
        errors.extend(f"source hash mismatch: {item}" for item in mismatches)

    if "comparison" in loaded:
        comparison = loaded["comparison"]
        routes = comparison.get("routes", [])
        selected = [
            row
            for row in routes
            if isinstance(row, dict) and row.get("disposition") == "selected_not_executed"
        ]
        selection = comparison.get("selection", {})
        checks["four_routes_one_selected"] = (
            len(routes) == 4
            and len(selected) == 1
            and selected[0].get("route_id") == SELECTED_ROUTE
            and selection.get("selected_packet_id") == SELECTED_PACKET
            and selection.get("selected_packet_type") == SELECTED_TYPE
            and selection.get("selected_next_role_family") == SELECTED_ROLE
            and selection.get("selected_packet_executed") is False
        )
        checks["comparison_eight_freezes"] = (
            set(comparison.get("preserved_freeze_labels", [])) == FREEZES
        )

    if "decision" in loaded:
        decision = loaded["decision"]
        decisive = decision.get("decisive_result", {})
        theoretical = decision.get("theoretical_decision_output", {})
        checks["decision_identity"] = (
            decisive.get("result_type") == "route_A_selected"
            and decisive.get("route_id") == SELECTED_ROUTE
            and decisive.get("packet_id") == SELECTED_PACKET
            and decisive.get("packet_type") == SELECTED_TYPE
            and decisive.get("next_role_family") == SELECTED_ROLE
            and decisive.get("selected_packet_executed") is False
            and decisive.get("unresolved_blocking_conflict_count") == 0
        )
        checks["theoretical_decision_contract"] = (
            theoretical.get("selected_packet_id") == SELECTED_PACKET
            and theoretical.get("selected_next_packet_type") == SELECTED_TYPE
            and theoretical.get("selected_next_role_family") == SELECTED_ROLE
            and theoretical.get("selected_packet_executed") is False
            and theoretical.get("preserves_claim_blocks") is True
            and bool(theoretical.get("decision_basis"))
            and bool(theoretical.get("theoretical_method"))
            and bool(theoretical.get("decision_consequence"))
        )
        matrix = decision.get("distance_to_gr_status", [])
        checks["decision_fourteen_no_delta"] = (
            len(matrix) == 14
            and {row.get("burden") for row in matrix} == BURDENS
            and all(row.get("status") == "no_delta" for row in matrix)
        )
        checks["five_new_mathematical_payloads"] = (
            len(decision.get("new_mathematical_payload", [])) == 5
        )
        checks["decision_eight_freezes"] = (
            set(decision.get("preserved_freeze_labels", [])) == FREEZES
        )

    if "packet" in loaded:
        packet_doc = loaded["packet"]
        packet = packet_doc.get("packet", {})
        checks["future_packet_identity"] = (
            packet.get("packet_id") == SELECTED_PACKET
            and packet.get("packet_type") == SELECTED_TYPE
            and packet.get("route_id") == SELECTED_ROUTE
            and packet.get("next_role_family") == SELECTED_ROLE
            and packet.get("selected_packet_executed") is False
        )
        checks["future_packet_structure"] = (
            len(packet_doc.get("formal_domains", [])) == 10
            and len(packet_doc.get("formal_objects", [])) == 12
            and len(packet_doc.get("formal_maps", [])) == 10
            and len(packet_doc.get("theorem_targets", [])) == 5
            and len(packet_doc.get("proof_obligations", [])) == 14
            and len(packet_doc.get("failure_branches", [])) == 12
            and len(packet_doc.get("permitted_results", [])) == 4
        )
        checks["future_packet_eight_freezes"] = (
            set(packet_doc.get("preserved_freeze_labels", [])) == FREEZES
        )
        distance_contract = packet_doc.get("distance_to_gr_contract", {})
        checks["future_packet_no_delta_contract"] = (
            distance_contract.get("row_count") == 14
            and distance_contract.get("every_row_status") == "no_delta"
            and distance_contract.get("p4_t02_complete_for_plan_dependency") is False
            and distance_contract.get("p4_t03_locked") is True
        )

    if "conflict" in loaded:
        conflict = loaded["conflict"]
        children = conflict.get("children", {})
        checks["child_hashes_bound"] = (
            children.get("child_phys_math", {}).get("sha256")
            == sha256(paths["math_child"])
            and children.get("child_phys_phil", {}).get("sha256")
            == sha256(paths["phil_child"])
        )
        final_selection = conflict.get("final_selection", {})
        checks["conflict_resolved"] = (
            conflict.get("status") == "complete_no_blocking_conflict"
            and conflict.get("unresolved_blocking_conflict_count") == 0
            and conflict.get("conflict_review", {}).get("blocking_conflict_detected")
            is False
            and final_selection.get("selected_packet_id") == SELECTED_PACKET
            and final_selection.get("selected_packet_executed") is False
        )

    for name in ("math_child", "phil_child"):
        if name not in loaded:
            continue
        child_text = paths[name].read_text(encoding="utf-8")
        checks[f"{name}_final_selection"] = (
            SELECTED_ROUTE in child_text
            and SELECTED_PACKET in child_text
            and SELECTED_ROLE in child_text
            and "selected_not_executed" in child_text
        )
        checks[f"{name}_eight_freezes"] = all(
            freeze in child_text for freeze in FREEZES
        )
        checks[f"{name}_fourteen_no_delta"] = (
            len(recursive_no_delta_rows(loaded[name])) == 14
        )

    try:
        run = subprocess.run(
            [sys.executable, str(paths["model"]), "--json"],
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
        )
        model = json.loads(run.stdout)
        checks["exact_model_pass"] = (
            run.returncode == 0
            and model.get("status") == "PASS"
            and model.get("check_count") == 20
            and model.get("pass_count") == 20
            and all(model.get("checks", {}).values())
            and model.get("selected_route") == SELECTED_ROUTE
            and model.get("selected_future_packet") == SELECTED_PACKET
            and model.get("selected_future_packet_executed") is False
            and set(model.get("preserved_freezes", [])) == FREEZES
            and set(model.get("distance_to_gr_burdens", [])) == BURDENS
        )
        model_summary = model
    except Exception as exc:  # noqa: BLE001
        errors.append(f"model: {exc}")
        checks["exact_model_pass"] = False
        model_summary = {}

    try:
        compile_receipt = json.loads(paths["compile"].read_text(encoding="utf-8"))
        visual = compile_receipt.get("visual_review", {})
        checks["latex_and_visual_pass"] = (
            compile_receipt.get("status") == "PASS"
            and compile_receipt.get("source_sha256") == sha256(paths["tex"])
            and compile_receipt.get("compile_passes") == 2
            and compile_receipt.get("compile_exit_code") == 0
            and compile_receipt.get("pdf_page_count") == 4
            and visual.get("status") == "PASS"
            and visual.get("pages_reviewed") == 4
            and len(visual.get("page_sha256", {})) == 4
        )
    except Exception as exc:  # noqa: BLE001
        errors.append(f"compile receipt: {exc}")
        checks["latex_and_visual_pass"] = False

    if "completion" in loaded and "handoff" in loaded:
        completion = loaded["completion"]
        handoff = loaded["handoff"]
        checks["completion_and_handoff_identity"] = (
            completion.get("status") == "completed"
            and completion.get("objective_result") == "route_A_selected"
            and completion.get("selected_successor", {}).get("packet_id")
            == SELECTED_PACKET
            and completion.get("selected_successor", {}).get("executed") is False
            and handoff.get("handoff_id") == "handoff-1040"
            and handoff.get("completion_sha256") == sha256(paths["completion"])
            and handoff.get("selector_result", {}).get("selected_packet_id")
            == SELECTED_PACKET
            and handoff.get("selector_result", {}).get("successor_executed") is False
        )

    task_registry = csv_row(
        REPO / "registries/RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260815-006"
    )
    decision_registry = csv_row(
        REPO / "registries/DIRECTOR_DECISION_REGISTRY.csv",
        "decision_id",
        "DDR-20260815-006",
    )
    job_registry = csv_row(
        REPO / "registries/AGENT_JOB_REGISTRY.csv",
        "job_id",
        "AJ-RT-20260815-006-001",
    )
    role_registry = csv_row(
        REPO / "registries/ROLE_EXECUTION_REGISTRY.csv",
        "execution_role_ref",
        "theoretical-continuation-selector@0.1.0--RT-20260815-006",
    )
    claim_registry = csv_row(
        REPO / "registries/CLAIM_BOUNDARY_REGISTRY.csv",
        "claim_boundary_id",
        "CB-V22-P4-T02-B2-POST-OCCURRENCE-TYPING-PROVENANCE-OBSTRUCTION-"
        "THEORETICAL-SELECTION-001",
    )
    checks["terminal_registry_state"] = (
        task_registry.get("status") == "completed"
        and decision_registry.get("status") == "completed"
        and decision_registry.get("validation_status")
        == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
        and job_registry.get("status") == "completed"
        and job_registry.get("validation_status")
        == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
        and role_registry.get("validation_status")
        == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
        and claim_registry.get("status") == "completed"
    )

    tex_registry = (REPO / "registries/TEX_SOURCE_REGISTRY.csv").read_text(
        encoding="utf-8"
    )
    md_registry = (REPO / "registries/MARKDOWN_SOURCE_REGISTRY.csv").read_text(
        encoding="utf-8"
    )
    checks["registered_source_rows"] = (
        "TEX-V22-P4-T02-B2-POST-OCCURRENCE-TYPING-PROVENANCE-OBSTRUCTION-ROUTE-SELECTION-V1"
        in tex_registry
        and sha256(paths["tex"]) in tex_registry
        and "MD-V22-P4-T02-B2-PARENT-FUSION-POST-OCCURRENCE-TYPING-PROVENANCE-OBSTRUCTION-SELECTOR-V1"
        in md_registry
        and sha256(paths["fusion"]) in md_registry
    )

    program_state = (REPO / "research_control/program_state.yaml").read_text(
        encoding="utf-8"
    )
    backlog = (
        REPO / "research_control/design/v22_recommendation_backlog.yaml"
    ).read_text(encoding="utf-8")
    checks["program_state_and_backlog_synced"] = (
        "RT-20260815-006" in program_state
        and "handoff-1040" in program_state
        and SELECTED_PACKET in program_state
        and "RT-20260815-006" in backlog
        and SELECTED_PACKET in backlog
        and "selected_packet_executed: false" in backlog
    )

    tex_text = paths["tex"].read_text(encoding="utf-8")
    fusion_text = paths["fusion"].read_text(encoding="utf-8")
    checks["tex_and_fusion_boundary"] = (
        SELECTED_PACKET in tex_text
        and SELECTED_PACKET in fusion_text
        and "not executed" in tex_text
        and "not executed" in fusion_text
        and "fourteen" in fusion_text.lower()
        and "P4-T03" in fusion_text
    )

    text_paths = [path for path in paths.values() if path.exists()]
    checks["no_tab_or_trailing_whitespace"] = all(
        "\t" not in path.read_text(encoding="utf-8")
        and all(
            line == line.rstrip()
            for line in path.read_text(encoding="utf-8").splitlines()
        )
        for path in text_paths
    )

    status = "PASS" if all(checks.values()) and not errors else "FAIL"
    report = {
        "schema_id": (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "selector_validation_v1"
        ),
        "task_id": "RT-20260815-006",
        "job_id": "AJ-RT-20260815-006-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "errors": errors,
        "model_summary": model_summary,
        "authority_note": (
            "Focused validation establishes task conformance only; it does not "
            "execute the selected packet or change scientific authority."
        ),
    }
    REPORT.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    compact = {
        "schema_id": (
            "v22_p4_t02_b2_post_occurrence_typing_provenance_obstruction_"
            "selector_compact_receipt_v1"
        ),
        "task_id": "RT-20260815-006",
        "job_id": "AJ-RT-20260815-006-001",
        "status": status,
        "validation_path": str(REPORT.relative_to(REPO)),
        "validation_sha256": sha256(REPORT),
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "selected_route_id": SELECTED_ROUTE,
        "selected_packet_id": SELECTED_PACKET,
        "selected_packet_type": SELECTED_TYPE,
        "selected_role_family": SELECTED_ROLE,
        "selected_packet_executed": False,
        "preserved_freeze_count": len(FREEZES),
        "distance_to_gr_row_count": len(BURDENS),
        "distance_to_gr_all_no_delta": True,
        "authority_note": (
            "Compact task receipt only; no selected-packet execution or "
            "scientific promotion authority."
        ),
    }
    COMPACT.write_text(
        json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
