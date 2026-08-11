#!/usr/bin/env python3
"""Focused validator for the RT013 post-common-character selector.

This validator checks the task-local scientific/control contract.  It does not
promote theorem truth, ontology, physical meaning, B2 status, or Distance-to-GR.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = ROOT / "research_control/tasks/RT-20260810-013/artifacts"
REPORT_PATH = ARTIFACTS / "v22_p4_t02_b2_post_common_character_selector_validation.json"
COMPACT_PATH = ARTIFACTS / "v22_p4_t02_b2_post_common_character_selector_compact_receipt.json"

PACKET_ID = "PKT-V22-P4T02-B2-ORIENTED-MATROID-COVECTOR-CIRCUIT-BRIDGE-V1"
ROLE_ID = "candidate-constructor@0.2.0"
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
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
    """Safe YAML loader that rejects duplicate mapping keys."""


def construct_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.load(handle, Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected top-level mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected top-level object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, details: Any) -> None:
        checks.append(
            {"check_id": check_id, "status": "PASS" if passed else "FAIL", "details": details}
        )

    required = [
        "child_phys_math_p4_t02_b2_post_common_character_selector.yaml",
        "child_phys_phil_p4_t02_b2_post_common_character_selector.yaml",
        "parent_conflict_review_p4_t02_b2_post_common_character_selector.yaml",
        "parent_fusion_notes_p4_t02_b2_post_common_character_selector.md",
        "v22_p4_t02_b2_post_common_character_route_selection_v1.tex",
        "v22_p4_t02_b2_post_common_character_selector_decision_v1.yaml",
        "v22_p4_t02_b2_post_common_character_route_comparison_v1.yaml",
        "v22_p4_t02_b2_post_common_character_selected_future_packet_v1.yaml",
        "v22_p4_t02_b2_post_common_character_source_provenance_manifest_v1.yaml",
        "v22_p4_t02_b2_post_common_character_selector_model.py",
        "v22_p4_t02_b2_post_common_character_selector_latex_compile_receipt.json",
    ]
    missing = [name for name in required if not (ARTIFACTS / name).is_file()]
    check("required_artifacts_present", not missing, {"missing": missing, "count": len(required)})
    if missing:
        return emit(args, checks)

    yaml_names = [
        "child_phys_math_p4_t02_b2_post_common_character_selector.yaml",
        "child_phys_phil_p4_t02_b2_post_common_character_selector.yaml",
        "parent_conflict_review_p4_t02_b2_post_common_character_selector.yaml",
        "v22_p4_t02_b2_post_common_character_selector_decision_v1.yaml",
        "v22_p4_t02_b2_post_common_character_route_comparison_v1.yaml",
        "v22_p4_t02_b2_post_common_character_selected_future_packet_v1.yaml",
        "v22_p4_t02_b2_post_common_character_source_provenance_manifest_v1.yaml",
    ]
    loaded: dict[str, dict[str, Any]] = {}
    parse_errors: list[str] = []
    for name in yaml_names:
        try:
            loaded[name] = load_yaml(ARTIFACTS / name)
        except Exception as exc:  # exact diagnostic belongs in the report
            parse_errors.append(f"{name}: {exc}")
    check(
        "strict_unique_key_yaml",
        not parse_errors and len(loaded) == len(yaml_names),
        {"parsed": len(loaded), "expected": len(yaml_names), "errors": parse_errors},
    )
    if parse_errors:
        return emit(args, checks)

    comparison = loaded["v22_p4_t02_b2_post_common_character_route_comparison_v1.yaml"]
    routes = comparison.get("routes", [])
    selected_routes = [row for row in routes if row.get("disposition") == "selected_not_executed"]
    check(
        "exact_four_routes_one_selected",
        len(routes) == 4
        and len(selected_routes) == 1
        and selected_routes[0].get("route_id") == "B_NON_CHARACTER_ORIENTED_MATROID_BRIDGE",
        {
            "route_count": len(routes),
            "selected": [row.get("route_id") for row in selected_routes],
        },
    )
    check(
        "exact_three_rejected_routes",
        sum(row.get("disposition") == "not_selected" for row in routes) == 3,
        {"rejected_count": sum(row.get("disposition") == "not_selected" for row in routes)},
    )

    packet = loaded["v22_p4_t02_b2_post_common_character_selected_future_packet_v1.yaml"]
    decision = loaded["v22_p4_t02_b2_post_common_character_selector_decision_v1.yaml"]
    theory = decision.get("theoretical_decision_output", {})
    check(
        "packet_identity_and_role_consistent",
        packet.get("packet_id") == PACKET_ID
        and theory.get("selected_packet_id") == PACKET_ID
        and theory.get("selected_next_role_family") == ROLE_ID
        and packet.get("next_role_family") == ROLE_ID,
        {
            "packet": packet.get("packet_id"),
            "decision_packet": theory.get("selected_packet_id"),
            "role": theory.get("selected_next_role_family"),
        },
    )
    check(
        "selected_packet_unexecuted_everywhere",
        packet.get("selected_packet_executed") is False
        and packet.get("execution_authorized_in_rt013") is False
        and theory.get("selected_packet_executed") is False
        and decision.get("authority_limits", {}).get("selected_packet_executed") is False
        and comparison.get("selection", {}).get("selected_packet_executed") is False,
        "All parent decision surfaces stop before Candidate Constructor execution.",
    )

    objects = packet.get("formal_objects", [])
    maps = packet.get("formal_maps", [])
    obligations = packet.get("proof_obligations", [])
    failures = packet.get("failure_branches", [])
    check(
        "future_packet_executable_contract",
        len(objects) >= 8
        and len(maps) >= 8
        and len(obligations) == 14
        and len(failures) >= 10
        and packet.get("bridge_attempt_status_contract", {}).get("required") is True,
        {
            "objects": len(objects),
            "maps": len(maps),
            "proof_obligations": len(obligations),
            "failure_branches": len(failures),
        },
    )
    allowed_results = set(
        packet.get("bridge_attempt_status_contract", {}).get("allowed_result_types", [])
    )
    check(
        "candidate_constructor_decisiveness_contract",
        allowed_results
        == {
            "constructed_candidate",
            "minimal_countermodel",
            "precise_obstruction",
            "invalid_under_claim_boundary",
        }
        and packet.get("bridge_attempt_status_contract", {}).get(
            "obligations_only_completion_allowed"
        )
        is False,
        {"allowed_results": sorted(allowed_results)},
    )

    fixed_freezes = set(comparison.get("fixed_boundary", {}).get("preserved_freeze_labels", []))
    decision_freezes = set(decision.get("freeze_criteria_status", {}).get("active_freeze_labels", []))
    check(
        "exact_three_freezes_preserved",
        fixed_freezes == FREEZES and decision_freezes == FREEZES,
        {"comparison": sorted(fixed_freezes), "decision": sorted(decision_freezes)},
    )

    distance_rows = decision.get("distance_to_gr_status", [])
    distance_burdens = {row.get("burden") for row in distance_rows if isinstance(row, dict)}
    check(
        "expanded_distance_to_gr_matrix_no_delta",
        len(distance_rows) == 14
        and decision.get("distance_to_gr_status", {}).get("row_count", 14) == 14
        if isinstance(decision.get("distance_to_gr_status"), dict)
        else len(distance_rows) == 14
        and distance_burdens == BURDENS
        and all(row.get("task_delta") == "none" for row in distance_rows),
        {
            "row_count": len(distance_rows),
            "burdens": sorted(str(item) for item in distance_burdens),
            "all_none": all(row.get("task_delta") == "none" for row in distance_rows),
        },
    )
    # The sequence has an attached row_count key in YAML only when represented
    # as a mapping; RT013 uses the established list form.  Enforce the exact
    # burden set separately to avoid expression-precedence ambiguity.
    check(
        "distance_to_gr_burden_set",
        len(distance_rows) == 14
        and distance_burdens == BURDENS
        and all(row.get("task_delta") == "none" for row in distance_rows),
        {"missing": sorted(BURDENS - distance_burdens), "extra": sorted(distance_burdens - BURDENS)},
    )

    payloads = decision.get("selector_level_mathematics", [])
    payload_types = {row.get("payload_type") for row in payloads if isinstance(row, dict)}
    check(
        "new_mathematical_payload",
        len(payloads) >= 5
        and {"theorem", "countermodel", "packet_selection"}.issubset(payload_types),
        {"count": len(payloads), "types": sorted(str(item) for item in payload_types)},
    )

    conflict = loaded["parent_conflict_review_p4_t02_b2_post_common_character_selector.yaml"]
    synthesis = decision.get("parent_child_synthesis", {})
    child_paths = synthesis.get("child_outputs", [])
    child_hash_failures: list[str] = []
    for row in child_paths:
        path = ROOT / str(row.get("output_path", ""))
        expected = row.get("sha256")
        if not path.is_file() or sha256(path) != expected:
            child_hash_failures.append(str(row.get("execution_unit_id")))
    check(
        "parent_child_synthesis_complete",
        len(child_paths) == 2
        and not child_hash_failures
        and conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_count") == 0
        and conflict.get("unresolved_conflicts") == []
        and conflict.get("resolution_round_count") == 1,
        {
            "child_count": len(child_paths),
            "child_hash_failures": child_hash_failures,
            "conflict_status": conflict.get("status"),
        },
    )

    manifest = loaded["v22_p4_t02_b2_post_common_character_source_provenance_manifest_v1.yaml"]
    manifest_rows = list(manifest.get("sources", [])) + list(manifest.get("child_sources", []))
    hash_failures: list[dict[str, str]] = []
    for row in manifest_rows:
        path = ROOT / str(row.get("path", ""))
        expected = str(row.get("sha256", ""))
        if not path.is_file():
            hash_failures.append({"path": str(path), "reason": "missing"})
        else:
            actual = sha256(path)
            if actual != expected:
                hash_failures.append(
                    {"path": str(row.get("path")), "reason": "hash", "expected": expected, "actual": actual}
                )
    check(
        "source_provenance_hashes",
        len(manifest_rows) >= 20 and not hash_failures,
        {"source_count": len(manifest_rows), "failures": hash_failures},
    )

    model_path = ARTIFACTS / "v22_p4_t02_b2_post_common_character_selector_model.py"
    model_run = subprocess.run(
        [sys.executable, str(model_path), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    model_payload: dict[str, Any] = {}
    model_error = ""
    try:
        model_payload = json.loads(model_run.stdout)
    except json.JSONDecodeError as exc:
        model_error = str(exc)
    check(
        "exact_support_model",
        model_run.returncode == 0
        and model_payload.get("status") == "PASS"
        and model_payload.get("check_count") == 12
        and model_payload.get("selected_route") == "B_NON_CHARACTER_ORIENTED_MATROID_BRIDGE",
        {
            "returncode": model_run.returncode,
            "status": model_payload.get("status"),
            "check_count": model_payload.get("check_count"),
            "error": model_error,
        },
    )

    tex_path = ARTIFACTS / "v22_p4_t02_b2_post_common_character_route_selection_v1.tex"
    tex_text = tex_path.read_text(encoding="utf-8")
    compile_receipt = load_json(
        ARTIFACTS / "v22_p4_t02_b2_post_common_character_selector_latex_compile_receipt.json"
    )
    scratch_pdf = ROOT / str(compile_receipt.get("scratch_pdf_path", ""))
    check(
        "latex_compile_and_visual_receipt",
        compile_receipt.get("status") == "PASS"
        and compile_receipt.get("source_sha256") == sha256(tex_path)
        and compile_receipt.get("compiler_exit_code") == 0
        and compile_receipt.get("pdf_page_count") == 5
        and compile_receipt.get("visual_inspection", {}).get("status") == "PASS"
        and scratch_pdf.is_file()
        and sha256(scratch_pdf) == compile_receipt.get("scratch_pdf_sha256"),
        {
            "receipt_status": compile_receipt.get("status"),
            "source_hash_match": compile_receipt.get("source_sha256") == sha256(tex_path),
            "page_count": compile_receipt.get("pdf_page_count"),
            "visual_status": compile_receipt.get("visual_inspection", {}).get("status"),
        },
    )
    check(
        "tex_decision_and_claim_blocks",
        PACKET_ID in tex_text
        and "selected\\_not\\_executed" in tex_text
        and "Distance-to-GR is unchanged" in tex_text
        and "not a global no-go theorem" in tex_text,
        "The registered manuscript states the exact packet and non-conclusions.",
    )

    stale_alias = "PKT-V22-P4T02-B2-NON-CHARACTER-ORIENTED-MATROID-COVECTOR-CIRCUIT-BRIDGE-V1"
    parent_paths = [
        ARTIFACTS / "v22_p4_t02_b2_post_common_character_route_selection_v1.tex",
        ARTIFACTS / "v22_p4_t02_b2_post_common_character_selector_decision_v1.yaml",
        ARTIFACTS / "v22_p4_t02_b2_post_common_character_route_comparison_v1.yaml",
        ARTIFACTS / "v22_p4_t02_b2_post_common_character_selected_future_packet_v1.yaml",
    ]
    alias_hits = [
        path.name for path in parent_paths if stale_alias in path.read_text(encoding="utf-8")
    ]
    check(
        "retained_packet_identity_no_parent_alias",
        not alias_hits,
        {"stale_alias_hits": alias_hits, "retained_packet_id": PACKET_ID},
    )

    authority = decision.get("authority_limits", {})
    blocked_flags = {
        "selected_packet_executed": False,
        "source_bridge_constructed": False,
        "source_bridge_adopted": False,
        "canonical_ontology_modified": False,
        "adequacy_reevaluated": False,
        "b2_activated_or_disposed": False,
        "p4_t03_unlocked": False,
        "effective_metric_constructed": False,
        "distance_to_gr_changed": False,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "publication_authorized": False,
        "push_authorized": False,
        "external_action_authorized": False,
        "global_no_go_claimed": False,
        "completed_derivation_claimed": False,
    }
    authority_mismatches = {
        key: authority.get(key)
        for key, expected in blocked_flags.items()
        if authority.get(key) is not expected
    }
    check(
        "authority_and_claim_blocks",
        not authority_mismatches
        and theory.get("preserves_claim_blocks") is True
        and theory.get("requires_human_gate") is False,
        {"mismatches": authority_mismatches},
    )

    return emit(args, checks, model_payload=model_payload)


def emit(
    args: argparse.Namespace,
    checks: list[dict[str, Any]],
    *,
    model_payload: dict[str, Any] | None = None,
) -> int:
    failure_count = sum(row["status"] != "PASS" for row in checks)
    payload: dict[str, Any] = {
        "schema_id": "v22_p4_t02_b2_post_common_character_selector_validation_v1",
        "task_id": "RT-20260810-013",
        "job_id": "AJ-RT-20260810-013-001",
        "status": "PASS" if failure_count == 0 else "FAIL",
        "check_count": len(checks),
        "failure_count": failure_count,
        "selected_route": "B_NON_CHARACTER_ORIENTED_MATROID_BRIDGE",
        "selected_packet_id": PACKET_ID,
        "selected_next_role": ROLE_ID,
        "selected_packet_executed": False,
        "distance_to_gr_changed": False,
        "checks": checks,
        "model_summary": {
            "status": (model_payload or {}).get("status"),
            "check_count": (model_payload or {}).get("check_count"),
            "failure_count": (model_payload or {}).get("failure_count"),
        },
        "authority_note": (
            "Focused task-local validation evidence only; no theorem, ontology, "
            "physical, empirical, Gate, benchmark, proof, or promotion authority."
        ),
    }
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_post_common_character_selector_compact_receipt_v1",
            "task_id": "RT-20260810-013",
            "job_id": "AJ-RT-20260810-013-001",
            "status": payload["status"],
            "check_count": payload["check_count"],
            "failure_count": payload["failure_count"],
            "selected_route": payload["selected_route"],
            "selected_packet_id": PACKET_ID,
            "selected_packet_executed": False,
            "report_path": str(REPORT_PATH.relative_to(ROOT)),
            "report_sha256": sha256(REPORT_PATH),
        }
        COMPACT_PATH.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        payload["report_path"] = str(REPORT_PATH.relative_to(ROOT))
        payload["compact_receipt_path"] = str(COMPACT_PATH.relative_to(ROOT))
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["status"])
    return 0 if failure_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
