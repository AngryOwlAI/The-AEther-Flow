#!/usr/bin/env python3
"""Focused validator for the RT-20260814-001 theoretical selector."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[4]
TASK = REPO / "research_control/tasks/RT-20260814-001"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector_compact_receipt.json"

SELECTED_ROUTE = "A_CURRENT_SOURCE_EQUIVARIANT_ASYMMETRY_DERIVATION_AUDIT"
SELECTED_PACKET = (
    "PKT-V22-P4T02-B2-CURRENT-SOURCE-EQUIVARIANT-"
    "ASYMMETRY-DERIVATION-AUDIT-V1"
)
SELECTED_ROLE = "ontology-formalizer@0.2.0"
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
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
    pass


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


def validate() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, bool] = {}
    paths = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260814-001-001.yaml",
        "role": TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260814-001.yaml",
        "math_child": ART / "child_phys_math_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector.yaml",
        "phil_child": ART / "child_phys_phil_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector.yaml",
        "comparison": ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_route_comparison_v1.yaml",
        "decision": ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector_decision_v1.yaml",
        "packet": ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selected_future_packet_v1.yaml",
        "manifest": ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_source_provenance_manifest_v1.yaml",
        "tex": ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_route_selection_v1.tex",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector.md",
        "compile": ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector_latex_compile_receipt.json",
        "model": ART / "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector_model.py",
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
        "math_child",
        "phil_child",
        "conflict",
        "comparison",
        "decision",
        "packet",
        "manifest",
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

    if "manifest" in loaded:
        sources = loaded["manifest"].get("sources", [])
        mismatches: list[str] = []
        for item in sources:
            if not isinstance(item, dict):
                mismatches.append("non-map manifest source")
                continue
            source = REPO / str(item.get("path", ""))
            if not source.exists() or sha256(source) != str(item.get("sha256", "")):
                mismatches.append(str(item.get("path", "")))
        checks["source_manifest_hashes"] = not mismatches and len(sources) >= 24
        errors.extend(f"source hash mismatch: {item}" for item in mismatches)

    if "comparison" in loaded:
        comparison = loaded["comparison"]
        routes = comparison.get("routes", [])
        selected = [
            row
            for row in routes
            if isinstance(row, dict) and row.get("disposition") == "selected_not_executed"
        ]
        checks["four_routes_one_selected"] = len(routes) == 4 and len(selected) == 1
        checks["comparison_selects_route_A"] = (
            bool(selected) and selected[0].get("route_id") == SELECTED_ROUTE
        )
        checks["comparison_six_freezes"] = (
            set(comparison.get("preserved_freeze_labels", [])) == FREEZES
        )
        route_a = next(
            (row for row in routes if row.get("route_id") == SELECTED_ROUTE), {}
        )
        checks["route_A_full_groupoid_novelty"] = (
            len(route_a.get("mandatory_novelty_gates", [])) == 6
            and len(route_a.get("permitted_results", [])) == 3
            and route_a.get("selected") is True
        )

    if "decision" in loaded:
        decision = loaded["decision"]
        selected_path = decision.get("selected_path", {})
        theoretical = decision.get("theoretical_decision_output", {})
        checks["decision_identity"] = (
            selected_path.get("route_id") == SELECTED_ROUTE
            and selected_path.get("packet_id") == SELECTED_PACKET
            and selected_path.get("packet_type") == "bounded_theoretical_calculation"
            and selected_path.get("next_role_family") == SELECTED_ROLE
            and selected_path.get("selected_packet_executed") is False
        )
        checks["theoretical_decision_contract"] = (
            theoretical.get("selected_next_packet_type")
            == "bounded_theoretical_calculation"
            and theoretical.get("selected_next_role_family") == SELECTED_ROLE
            and theoretical.get("preserves_claim_blocks") is True
            and theoretical.get("selected_packet_executed") is False
            and bool(theoretical.get("decision_basis"))
            and bool(theoretical.get("theoretical_method"))
            and bool(theoretical.get("decision_consequence"))
            and bool(theoretical.get("new_payload_novelty"))
        )
        matrix = decision.get("distance_to_gr_status", [])
        checks["decision_fourteen_no_delta"] = (
            len(matrix) == 14
            and {row.get("burden") for row in matrix if isinstance(row, dict)} == BURDENS
            and all(row.get("status") == "no_delta" for row in matrix)
        )
        checks["decision_new_payload"] = len(
            decision.get("new_mathematical_payload", [])
        ) >= 5
        parent = decision.get("parent_resolution", {})
        checks["parent_resolution_full_groupoid"] = (
            parent.get("final_consensus_route") == SELECTED_ROUTE
            and parent.get("full_current_source_groupoid_required") is True
            and parent.get("finite_pair_groupoid_replay_forbidden") is True
            and parent.get("route_c_status")
            == "conditional_later_fallback_not_selected_not_executed"
        )

    if "packet" in loaded:
        packet_doc = loaded["packet"]
        packet = packet_doc.get("packet", {})
        checks["future_packet_identity"] = (
            packet.get("packet_id") == SELECTED_PACKET
            and packet.get("packet_type") == "bounded_theoretical_calculation"
            and packet.get("next_role_family") == SELECTED_ROLE
            and packet.get("selected_packet_executed") is False
        )
        checks["future_packet_structure"] = (
            len(packet_doc.get("formal_domains", [])) == 9
            and len(packet_doc.get("formal_objects", [])) == 10
            and len(packet_doc.get("formal_maps", [])) == 9
            and len(packet_doc.get("predeclared_candidate_codomain_grammar", {}).get("candidates", [])) == 6
            and len(packet_doc.get("theorem_targets", [])) == 7
            and len(packet_doc.get("proof_obligations", [])) == 14
            and len(packet_doc.get("failure_branches", [])) == 12
            and len(packet_doc.get("permitted_results", [])) == 3
        )
        material = packet_doc.get("material_distinctness_contract", {})
        checks["future_packet_materially_distinct"] = (
            material.get("full_current_source_groupoid_required") is True
            and material.get("rt002_pair_groupoid_replay_forbidden") is True
            and material.get("no_new_source_primitive") is True
            and material.get("route_c_not_preselected") is True
        )
        checks["future_packet_six_freezes"] = (
            set(packet_doc.get("preserved_freeze_labels", [])) == FREEZES
        )
        packet_matrix = packet_doc.get("distance_to_gr_status", [])
        checks["future_packet_fourteen_no_delta"] = (
            len(packet_matrix) == 14
            and {row.get("burden") for row in packet_matrix} == BURDENS
            and all(row.get("status") == "no_delta" for row in packet_matrix)
        )

    if "conflict" in loaded:
        conflict = loaded["conflict"]
        child_hashes = {
            row.get("execution_unit_id"): row.get("sha256")
            for row in conflict.get("child_inputs", [])
            if isinstance(row, dict)
        }
        checks["child_hashes_bound"] = (
            child_hashes.get("child_phys_math") == sha256(paths["math_child"])
            and child_hashes.get("child_phys_phil") == sha256(paths["phil_child"])
        )
        checks["conflict_resolved"] = (
            conflict.get("status") == "resolved"
            and conflict.get("resolution_round_count") == 2
            and conflict.get("unresolved_conflicts") == []
            and conflict.get("unresolved_blocking_conflict_count") == 0
            and conflict.get("parent_adjudication", {}).get("selected_packet_id")
            == SELECTED_PACKET
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
            and (
                "unresolved_conflicts" in child_text
                or "unresolved_blocking_conflict" in child_text
            )
        )
        checks[f"{name}_six_freezes"] = all(
            freeze in child_text for freeze in FREEZES
        )
        child_rows = recursive_no_delta_rows(loaded[name])
        checks[f"{name}_fourteen_no_delta"] = len(child_rows) == 14

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
            and model.get("check_count") == 14
            and model.get("pass_count") == 14
            and all(model.get("checks", {}).values())
            and model.get("fixed_points") == []
            and model.get("orbit_partition") == [[0, 1]]
            and model.get("invariant_boolean_predicates")
            == [[False, False], [True, True]]
            and model.get("trivial_source_equivariant_maps") == []
            and model.get("torsor_source_equivariant_maps") == [[0, 1], [1, 0]]
        )
        model_summary = model
    except Exception as exc:  # noqa: BLE001
        errors.append(f"model: {exc}")
        checks["exact_model_pass"] = False
        model_summary = {}

    try:
        compile_receipt = json.loads(paths["compile"].read_text(encoding="utf-8"))
        page_count = compile_receipt.get("page_count", 0)
        checks["latex_and_visual_pass"] = (
            compile_receipt.get("status") == "PASS"
            and compile_receipt.get("source_sha256") == sha256(paths["tex"])
            and compile_receipt.get("compile_pass_count") == 2
            and isinstance(page_count, int)
            and page_count == 4
            and compile_receipt.get("final_pass_overfull_box_count") == 0
            and compile_receipt.get("final_pass_underfull_box_count") == 0
            and compile_receipt.get("visual_inspection", {}).get("status") == "PASS"
            and compile_receipt.get("visual_inspection", {}).get("inspected_page_count")
            == page_count
        )
    except Exception as exc:  # noqa: BLE001
        errors.append(f"compile receipt: {exc}")
        checks["latex_and_visual_pass"] = False

    if paths["tex"].exists() and paths["fusion"].exists():
        tex_text = paths["tex"].read_text(encoding="utf-8")
        fusion_text = paths["fusion"].read_text(encoding="utf-8")
        checks["tex_and_fusion_boundary"] = (
            "source-provenance" in tex_text
            and SELECTED_PACKET in fusion_text
            and "unexecuted" in tex_text
            and "unexecuted" in fusion_text
            and "All fourteen Distance-to-GR" in fusion_text
            and "P4-T03" in fusion_text
            and "remains locked" in fusion_text
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
        "schema_id": "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector_validation_v1",
        "task_id": "RT-20260814-001",
        "job_id": "AJ-RT-20260814-001-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "checks": checks,
        "errors": errors,
        "model_summary": model_summary,
        "authority_note": "Focused validation establishes task conformance only; it does not execute the selected packet or change physics authority.",
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {
        "schema_id": "v22_p4_t02_b2_post_finite_bridge_provenance_obstruction_selector_compact_receipt_v1",
        "task_id": "RT-20260814-001",
        "job_id": "AJ-RT-20260814-001-001",
        "status": status,
        "validation_path": str(REPORT.relative_to(REPO)),
        "validation_sha256": sha256(REPORT),
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "selected_route_id": SELECTED_ROUTE,
        "selected_packet_id": SELECTED_PACKET,
        "selected_packet_type": "bounded_theoretical_calculation",
        "selected_role_family": SELECTED_ROLE,
        "selected_packet_executed": False,
        "preserved_freeze_count": len(FREEZES),
        "distance_to_gr_row_count": len(BURDENS),
        "distance_to_gr_all_no_delta": True,
        "authority_note": "Compact task receipt only; no selected-packet execution or scientific promotion authority.",
    }
    COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
