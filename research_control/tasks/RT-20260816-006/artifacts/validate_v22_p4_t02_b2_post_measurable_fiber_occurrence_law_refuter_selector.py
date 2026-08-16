#!/usr/bin/env python3
"""Focused validator for the RT-20260816-006 selector transaction."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent

COMPARISON = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_route_comparison_v1.yaml"
DECISION = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_decision_v1.yaml"
PACKET = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selected_future_packet_v1.yaml"
MODEL = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_model.py"
MATH_CHILD = ARTIFACTS / "child_phys_math_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector.yaml"
PHIL_CHILD = ARTIFACTS / "child_phys_phil_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector.yaml"
CONFLICT = ARTIFACTS / "parent_conflict_review_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector.yaml"
FUSION = ARTIFACTS / "parent_fusion_notes_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector.md"
TEX = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_route_selection_v1.tex"
COMPILE = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_latex_compile_receipt.json"
MANIFEST = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_provenance_manifest_v1.yaml"
VALIDATION = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_validation.json"
COMPACT = ARTIFACTS / "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_compact_receipt.json"

SELECTED_ROUTE = "A_CURRENT_SOURCE_OCCURRENCE_ADMISSIBILITY_RELEVANCE_FACTORIZATION_AUDIT"
SELECTED_PACKET = "PKT-V22-P4T02-B2-CURRENT-SOURCE-OCCURRENCE-ADMISSIBILITY-P4-RELEVANCE-FACTORIZATION-AUDIT-V1"
SELECTED_TYPE = "bounded_theoretical_calculation"
SELECTED_LABEL = "ordinary-research-packet"
SELECTED_ROLE = "ontology-formalizer@0.2.0"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing mapping", node.start_mark,
                f"duplicate key: {key}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain one YAML mapping")
    return data


def load_model() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("rt006_selector_model", MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import selector model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_model()


def find_values(node: Any, key: str) -> list[Any]:
    values: list[Any] = []
    if isinstance(node, dict):
        for current_key, value in node.items():
            if current_key == key:
                values.append(value)
            values.extend(find_values(value, key))
    elif isinstance(node, list):
        for value in node:
            values.extend(find_values(value, key))
    return values


def no_whitespace_errors(path: Path) -> bool:
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        return False
    text = raw.decode("utf-8")
    return "\t" not in text and all(line == line.rstrip(" ") for line in text.splitlines())


def run() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    required = [
        COMPARISON, DECISION, PACKET, MODEL, MATH_CHILD, PHIL_CHILD,
        CONFLICT, FUSION, TEX, COMPILE, MANIFEST,
    ]
    check("required_artifacts", all(path.is_file() for path in required), f"required={len(required)}")
    if not all(path.is_file() for path in required):
        return {"status": "FAIL", "checks": checks}

    yaml_paths = [COMPARISON, DECISION, PACKET, MATH_CHILD, PHIL_CHILD, CONFLICT, MANIFEST]
    parsed: dict[Path, dict[str, Any]] = {}
    parse_ok = True
    for path in yaml_paths:
        try:
            parsed[path] = load_yaml(path)
        except Exception as exc:
            parse_ok = False
            check(f"strict_yaml_{path.name}", False, str(exc))
    check("strict_unique_yaml", parse_ok, f"yaml_artifacts={len(yaml_paths)}")
    if not parse_ok:
        return {"status": "FAIL", "checks": checks}

    comparison = parsed[COMPARISON]
    decision = parsed[DECISION]
    packet = parsed[PACKET]
    conflict = parsed[CONFLICT]
    manifest = parsed[MANIFEST]

    routes = comparison.get("routes", [])
    selected_routes = [route for route in routes if route.get("selected") is True]
    check("four_routes_one_selection", len(routes) == 4 and len(selected_routes) == 1, f"routes={len(routes)} selected={len(selected_routes)}")
    check("selected_route_identity", bool(selected_routes) and selected_routes[0].get("route_id") == SELECTED_ROUTE, SELECTED_ROUTE)

    packet_ids = {
        comparison.get("selection", {}).get("selected_packet_id"),
        decision.get("decisive_result", {}).get("packet_id"),
        decision.get("theoretical_decision_output", {}).get("selected_packet_id"),
        packet.get("packet", {}).get("packet_id"),
        conflict.get("final_selected_packet_id"),
    }
    check("packet_identity_convergence", packet_ids == {SELECTED_PACKET}, repr(packet_ids))
    type_values = {
        comparison.get("selection", {}).get("selected_packet_type"),
        decision.get("decisive_result", {}).get("packet_type"),
        packet.get("packet", {}).get("packet_type"),
        conflict.get("final_selected_packet_type"),
    }
    role_values = {
        comparison.get("selection", {}).get("selected_next_role_family"),
        decision.get("decisive_result", {}).get("next_role_family"),
        packet.get("packet", {}).get("next_role_family"),
        conflict.get("final_selected_role_family"),
    }
    label_values = {
        comparison.get("selection", {}).get("route_label"),
        decision.get("decisive_result", {}).get("route_label"),
        packet.get("packet", {}).get("route_label"),
        conflict.get("final_selected_route_label"),
    }
    check("type_role_label_convergence", type_values == {SELECTED_TYPE} and role_values == {SELECTED_ROLE} and label_values == {SELECTED_LABEL}, f"types={type_values} roles={role_values} labels={label_values}")

    executed = []
    for path in [COMPARISON, DECISION, PACKET, MATH_CHILD, PHIL_CHILD, CONFLICT]:
        executed.extend(find_values(parsed[path], "selected_packet_executed"))
    check("selected_packet_unexecuted", bool(executed) and all(value is False for value in executed), f"values={len(executed)}")

    freezes = decision.get("preserved_freeze_labels", [])
    packet_freezes = packet.get("preserved_freeze_labels", [])
    check("nine_freezes", len(freezes) == 9 and len(set(freezes)) == 9 and packet_freezes == freezes, f"count={len(freezes)}")
    distance_rows = decision.get("distance_to_gr_status", [])
    check("fourteen_literal_no_delta", len(distance_rows) == 14 and all(row.get("status") == "no_delta" for row in distance_rows), f"rows={len(distance_rows)}")
    check(
        "future_packet_contract_counts",
        len(packet.get("formal_domains", [])) == 10
        and len(packet.get("formal_objects", [])) == 11
        and len(packet.get("formal_maps", [])) == 10
        and len(packet.get("theorem_targets", [])) == 6
        and len(packet.get("proof_obligations", [])) == 16
        and len(packet.get("failure_branches", [])) == 15,
        "domains=10 objects=11 maps=10 theorems=6 obligations=16 branches=15",
    )
    payloads = decision.get("new_mathematical_payload", [])
    check("new_mathematical_payload", len(payloads) == 5 and all(item.get("proof_control") and item.get("falsifier") for item in payloads), f"payloads={len(payloads)}")

    locks = decision.get("downstream_locks", {})
    check(
        "downstream_locks",
        locks.get("d7_reevaluated") is False
        and locks.get("b2_activated") is False
        and locks.get("p4_t03_locked") is True
        and locks.get("p4_t03_unlocked_or_executed") is False
        and locks.get("p4_t02_complete_for_plan_dependency") is False
        and locks.get("factorization_audit_executed") is False,
        repr(locks),
    )
    authority_false = [
        "selected_packet_executed", "theorem_truth_inferred",
        "combined_extension_category_constructed", "p4_relevance_map_constructed",
        "full_factorization_theorem_claimed", "p4_irrelevance_claimed",
        "response_bridge_constructed", "source_extension_constructed",
        "current_source_language_modified", "canonical_ontology_modified",
        "scientific_status_changed", "physical_status_changed",
        "distance_to_gr_changed", "global_no_go_claimed",
        "physics_promotion_authorized", "proof_authority",
        "publication_authorized", "push_authorized",
        "external_action_authorized", "completed_derivation_claimed",
    ]
    authority = decision.get("authority_limits", {})
    check("authority_blocks", all(authority.get(key) is False for key in authority_false), f"checked={len(authority_false)}")

    check("parent_conflict_resolved", conflict.get("unresolved_blocking_conflict_count") == 0 and conflict.get("initial_child_consensus") is True, repr(conflict.get("unresolved_blocking_conflict_count")))
    check("child_artifacts_distinct", sha256(MATH_CHILD) != sha256(PHIL_CHILD), "independent artifacts have distinct hashes")
    for child_path in [MATH_CHILD, PHIL_CHILD]:
        child_text = child_path.read_text(encoding="utf-8")
        check(f"child_selection_{child_path.name}", SELECTED_ROUTE in child_text and SELECTED_PACKET in child_text and SELECTED_ROLE in child_text, "canonical selection present")

    model = load_model()
    check("exact_model", model.get("all_pass") is True and model.get("check_count") == 19 and model.get("selected_route") == SELECTED_ROUTE, f"payload_sha256={model.get('payload_sha256')}")

    manifest_entries = manifest.get("governing_sources", []) + manifest.get("fused_artifacts", [])
    bad_manifest: list[str] = []
    for entry in manifest_entries:
        path = ROOT / entry["path"]
        if not path.is_file() or sha256(path) != entry["sha256"]:
            bad_manifest.append(entry["path"])
    check("provenance_hashes", not bad_manifest, "bad=" + repr(bad_manifest))

    compile_receipt = json.loads(COMPILE.read_text(encoding="utf-8"))
    check("latex_compile_visual_review", compile_receipt.get("status") == "PASS" and compile_receipt.get("scratch_pdf_page_count") == 4 and compile_receipt.get("final_pass_warning_count") == 0 and compile_receipt.get("visual_review", {}).get("status") == "PASS", repr(compile_receipt.get("status")))
    tex_text = TEX.read_text(encoding="utf-8")
    check("tex_identity_and_boundaries", SELECTED_PACKET in tex_text and "selected but not executed" in tex_text and "fourteen Distance-to-GR rows" in tex_text and "nine inherited freezes" in tex_text, "selection and boundary text present")

    check("whitespace", all(no_whitespace_errors(path) for path in required + [Path(__file__).resolve()]), f"files={len(required) + 1}")

    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "task_id": "RT-20260816-006",
        "job_id": "AJ-RT-20260816-006-001",
        "selected_route": SELECTED_ROUTE,
        "selected_packet_id": SELECTED_PACKET,
        "model_payload_sha256": model.get("payload_sha256"),
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "checks": checks,
        "authority_note": "Validation is conformance evidence only and creates no theorem, ontology, physical, Distance-to-GR, publication, push, or successor-execution authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipts", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.write_receipts:
        VALIDATION.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_post_measurable_fiber_occurrence_law_refuter_selector_compact_receipt_v1",
            "status": result["status"],
            "task_id": result.get("task_id"),
            "job_id": result.get("job_id"),
            "selected_route": result.get("selected_route"),
            "selected_packet_id": result.get("selected_packet_id"),
            "check_count": result.get("check_count", 0),
            "pass_count": result.get("pass_count", 0),
            "fail_count": result.get("fail_count", 0),
            "model_payload_sha256": result.get("model_payload_sha256"),
            "selected_packet_executed": False,
            "distance_to_gr_changed": False,
            "authority_note": result.get("authority_note"),
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
