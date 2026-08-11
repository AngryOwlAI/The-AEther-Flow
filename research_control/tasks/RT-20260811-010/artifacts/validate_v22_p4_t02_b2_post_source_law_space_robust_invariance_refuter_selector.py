#!/usr/bin/env python3
"""Focused validator for the bounded RT010 theoretical selector transaction."""

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
TASK = REPO / "research_control/tasks/RT-20260811-010"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector_compact_receipt.json"

SELECTED_ROUTE = "A_SOURCE_GENERATED_COMPACT_ROOT_FAMILY_COERCIVE_PROTECTION_LAW"
SELECTED_CANDIDATE = "CAND-V22-B2-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-COERCIVE-PROTECTION-LAW-V1"
SELECTED_PACKET = "PKT-V22-P4T02-B2-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-COERCIVE-PROTECTION-LAW-FORMALIZATION-V1"
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


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
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


def all_false(mapping: dict[str, Any], fields: tuple[str, ...]) -> bool:
    return all(mapping.get(field) is False for field in fields)


def validate() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, bool] = {}

    paths = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260811-010-001.yaml",
        "role": TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260811-010.yaml",
        "math_child": ART / "child_phys_math_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector.yaml",
        "phil_child": ART / "child_phys_phil_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector.yaml",
        "comparison": ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_route_comparison_v1.yaml",
        "decision": ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector_decision_v1.yaml",
        "packet": ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selected_future_packet_v1.yaml",
        "manifest": ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_source_provenance_manifest_v1.yaml",
        "tex": ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_route_selection_v1.tex",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector.md",
        "compile": ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector_latex_compile_receipt.json",
        "model": ART / "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector_model.py",
    }
    checks["all_expected_artifacts_exist"] = all(path.exists() for path in paths.values())
    if not checks["all_expected_artifacts_exist"]:
        errors.extend(str(path.relative_to(REPO)) for path in paths.values() if not path.exists())

    yaml_names = (
        "task", "job", "role", "math_child", "phil_child", "conflict",
        "comparison", "decision", "packet", "manifest",
    )
    loaded: dict[str, dict[str, Any]] = {}
    for name in yaml_names:
        try:
            loaded[name] = load_yaml(paths[name])
        except Exception as exc:  # noqa: BLE001 - validator must aggregate exact failures
            errors.append(f"{name}: {exc}")
    checks["unique_key_yaml_parse"] = len(loaded) == len(yaml_names)

    if "manifest" in loaded:
        manifest_sources = loaded["manifest"].get("sources", [])
        mismatches: list[str] = []
        for item in manifest_sources:
            if not isinstance(item, dict):
                mismatches.append("non-map manifest source")
                continue
            source = REPO / str(item.get("path", ""))
            expected = str(item.get("sha256", ""))
            if not source.exists() or sha256(source) != expected:
                mismatches.append(str(item.get("path", "")))
        checks["source_manifest_hashes"] = not mismatches and len(manifest_sources) == 18
        errors.extend(f"source hash mismatch: {item}" for item in mismatches)

    if "comparison" in loaded:
        routes = loaded["comparison"].get("routes", [])
        selected = [row for row in routes if isinstance(row, dict) and row.get("disposition") == "selected"]
        checks["four_routes_one_selected"] = len(routes) == 4 and len(selected) == 1
        checks["comparison_selects_canonical_route"] = bool(selected) and selected[0].get("route_id") == SELECTED_ROUTE
        checks["six_freezes_in_comparison"] = set(loaded["comparison"].get("preserved_freeze_labels", [])) == FREEZES

    if "decision" in loaded:
        decision = loaded["decision"]
        selected_path = decision.get("selected_path", {})
        theoretical = decision.get("theoretical_decision_output", {})
        checks["decision_identity"] = (
            selected_path.get("route_id") == SELECTED_ROUTE
            and selected_path.get("candidate_law_id") == SELECTED_CANDIDATE
            and selected_path.get("packet_id") == SELECTED_PACKET
            and selected_path.get("packet_type") == "ontology_law_research_packet"
            and selected_path.get("next_role_family") == SELECTED_ROLE
            and selected_path.get("selected_packet_executed") is False
        )
        checks["theoretical_decision_contract"] = (
            theoretical.get("selected_next_packet_type") == "ontology_law_research_packet"
            and theoretical.get("preserves_claim_blocks") is True
            and theoretical.get("requires_human_gate") is False
            and bool(theoretical.get("decision_basis"))
            and bool(theoretical.get("theoretical_method"))
        )
        matrix = decision.get("distance_to_gr_status", [])
        checks["decision_fourteen_no_delta"] = (
            len(matrix) == 14
            and {row.get("burden") for row in matrix if isinstance(row, dict)} == BURDENS
            and all(row.get("status") == "no_delta" for row in matrix if isinstance(row, dict))
        )
        limits = decision.get("authority_limits", {})
        checks["decision_authority_blocks"] = all_false(
            limits,
            (
                "selected_packet_executed", "scientific_status_changed",
                "physical_status_changed", "source_law_formalized",
                "source_law_proved", "source_law_adopted",
                "canonical_ontology_modified", "adequacy_reevaluated",
                "b2_activated", "p4_t03_unlocked",
                "effective_metric_constructed", "distance_to_gr_changed",
                "global_no_go_claimed", "future_source_extension_impossibility_claimed",
                "physics_promotion_authorized", "proof_authority",
                "publication_authorized", "push_authorized", "external_action_authorized",
            ),
        )

    if "packet" in loaded:
        packet = loaded["packet"].get("packet", {})
        checks["future_packet_identity"] = (
            packet.get("packet_id") == SELECTED_PACKET
            and packet.get("candidate_id") == SELECTED_CANDIDATE
            and packet.get("next_role_family") == SELECTED_ROLE
            and packet.get("selected_packet_executed") is False
        )
        checks["future_packet_obligations"] = len(loaded["packet"].get("proof_obligations", [])) == 14
        checks["future_packet_failure_branches"] = len(loaded["packet"].get("failure_branches", [])) == 11
        checks["future_packet_six_freezes"] = set(loaded["packet"].get("preserved_freeze_labels", [])) == FREEZES

    if "conflict" in loaded:
        conflict = loaded["conflict"]
        children = conflict.get("child_inputs", [])
        child_hashes = {
            row.get("execution_unit_id"): row.get("sha256")
            for row in children if isinstance(row, dict)
        }
        checks["child_hashes_bound"] = (
            child_hashes.get("child_phys_math") == sha256(paths["math_child"])
            and child_hashes.get("child_phys_phil") == sha256(paths["phil_child"])
        )
        checks["conflict_resolved"] = (
            conflict.get("status") == "resolved"
            and conflict.get("resolution_rounds") == 1
            and conflict.get("unresolved_conflicts") == []
            and conflict.get("fusion_result", {}).get("unresolved_blocking_conflict_count") == 0
        )

    for name in ("math_child", "phil_child"):
        if name not in loaded:
            continue
        text = paths[name].read_text(encoding="utf-8")
        checks[f"{name}_selection"] = (
            SELECTED_ROUTE in text and SELECTED_PACKET in text and SELECTED_ROLE in text
        )
        checks[f"{name}_six_freezes"] = all(freeze in text for freeze in FREEZES)
        checks[f"{name}_fourteen_no_delta"] = text.count("task_delta: no_delta") == 14

    try:
        model_run = subprocess.run(
            [sys.executable, str(paths["model"]), "--json"],
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
        )
        model = json.loads(model_run.stdout)
        checks["exact_model_pass"] = (
            model_run.returncode == 0
            and model.get("status") == "PASS"
            and model.get("selected_route_id") == SELECTED_ROUTE
            and model.get("selected_packet_id") == SELECTED_PACKET
            and len(model.get("checks", {})) == 16
            and all(model.get("checks", {}).values())
        )
        model_summary = model
    except Exception as exc:  # noqa: BLE001
        errors.append(f"model: {exc}")
        checks["exact_model_pass"] = False
        model_summary = {}

    try:
        compile_receipt = json.loads(paths["compile"].read_text(encoding="utf-8"))
        checks["latex_and_visual_pass"] = (
            compile_receipt.get("status") == "PASS"
            and compile_receipt.get("source_sha256") == sha256(paths["tex"])
            and compile_receipt.get("compile_pass_count") == 2
            and compile_receipt.get("page_count") == 5
            and compile_receipt.get("visual_inspection", {}).get("status") == "PASS"
            and compile_receipt.get("visual_inspection", {}).get("inspected_page_count") == 5
        )
    except Exception as exc:  # noqa: BLE001
        errors.append(f"compile receipt: {exc}")
        checks["latex_and_visual_pass"] = False

    tex_text = paths["tex"].read_text(encoding="utf-8")
    fusion_text = paths["fusion"].read_text(encoding="utf-8")
    checks["tex_and_fusion_boundary"] = (
        SELECTED_PACKET in fusion_text
        and "selected but not executed" in tex_text
        and "selected but not executed" in fusion_text
        and "all fourteen Distance-to-GR rows" in tex_text
        and "all fourteen Distance-to-GR rows" in fusion_text
        and "Compact-total root-family coercive minimum" in tex_text
        and "compact-total-space minimum theorem" in fusion_text
    )
    checks["no_tab_or_trailing_whitespace"] = all(
        "\t" not in path.read_text(encoding="utf-8")
        and all(line == line.rstrip() for line in path.read_text(encoding="utf-8").splitlines())
        for path in paths.values()
    )

    for name, passed in checks.items():
        if not passed:
            errors.append(f"failed check: {name}")

    status = "PASS" if not errors else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector_validation_v1",
        "task_id": "RT-20260811-010",
        "job_id": "AJ-RT-20260811-010-001",
        "status": status,
        "validated_at": "2026-08-11T20:44:23Z",
        "selected_route_id": SELECTED_ROUTE,
        "selected_candidate_id": SELECTED_CANDIDATE,
        "selected_packet_id": SELECTED_PACKET,
        "selected_packet_executed": False,
        "check_count": len(checks),
        "passed_check_count": sum(1 for value in checks.values() if value),
        "failed_check_count": sum(1 for value in checks.values() if not value),
        "checks": checks,
        "errors": errors,
        "model_summary": {
            "status": model_summary.get("status"),
            "check_count": len(model_summary.get("checks", {})),
            "positive_minimum": model_summary.get("compact_total_root_fixture", {}).get("minimum"),
            "route_b_irrelevance_follows": model_summary.get("factorization_scope_control", {}).get("p4_t02_irrelevance_follows"),
        },
        "authority_note": "Focused conformance validation is not source-law truth, physical evidence, adoption, proof promotion, or Distance-to-GR progress.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT.write_text(serialized, encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_post_source_law_space_robust_invariance_refuter_selector_compact_receipt_v1",
            "task_id": result["task_id"],
            "job_id": result["job_id"],
            "status": result["status"],
            "check_count": result["check_count"],
            "passed_check_count": result["passed_check_count"],
            "failed_check_count": result["failed_check_count"],
            "finding_count": len(result["errors"]),
            "selected_route_id": SELECTED_ROUTE,
            "selected_packet_id": SELECTED_PACKET,
            "selected_packet_executed": False,
            "report_path": REPORT.relative_to(REPO).as_posix(),
            "report_sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
            "authority_note": "Compact validation receipt only; no physics or promotion authority.",
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(serialized, end="")
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
