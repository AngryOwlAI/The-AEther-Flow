#!/usr/bin/env python3
"""Focused validator for the RT014 proposal-only oriented-matroid bridge.

The validator checks exact task-local construction and control contracts.  It
does not promote theorem truth, ontology, physical meaning, B2 status, Gate
authority, or Distance-to-GR.
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
ARTIFACTS = ROOT / "research_control/tasks/RT-20260810-014/artifacts"
REPORT_PATH = ARTIFACTS / "v22_p4_t02_b2_oriented_matroid_bridge_validation.json"
COMPACT_PATH = ARTIFACTS / "v22_p4_t02_b2_oriented_matroid_bridge_compact_receipt.json"

CANDIDATE_MAP = "Bridge_OM(A)=(Cstar(A),Cir_plus(A),Tot(A),Ref(A),Strat(A))"
RESULT = "constructed_candidate"
NEXT_ROLE = "smuggling-auditor@0.2.0"
NEXT_PACKET = "PKT-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SMUGGLING-AUDIT-V1"
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
PROOF_IDS = {f"PO-{index:02d}" for index in range(1, 15)}
FAILURE_IDS = {f"FB-{index:02d}" for index in range(1, 12)}


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


def suffix_id(value: Any, prefix: str) -> str:
    text = str(value or "")
    head = text.split("-", 2)
    if len(head) < 2:
        return text
    return f"{prefix}-{head[1]}"


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
        "child_phys_math_p4_t02_b2_oriented_matroid_bridge.yaml",
        "child_phys_phil_p4_t02_b2_oriented_matroid_bridge.yaml",
        "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge.yaml",
        "parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge.md",
        "v22_p4_t02_b2_oriented_matroid_covector_circuit_bridge_v1.tex",
        "v22_p4_t02_b2_oriented_matroid_bridge_record_v1.yaml",
        "v22_p4_t02_b2_oriented_matroid_bridge_fixtures_v1.yaml",
        "v22_p4_t02_b2_oriented_matroid_bridge_provenance_manifest_v1.yaml",
        "v22_p4_t02_b2_oriented_matroid_bridge_model.py",
        "v22_p4_t02_b2_oriented_matroid_bridge_latex_compile_receipt.json",
    ]
    missing = [name for name in required if not (ARTIFACTS / name).is_file()]
    check("required_artifacts_present", not missing, {"missing": missing, "count": len(required)})
    if missing:
        return emit(args, checks)

    yaml_names = [
        "child_phys_math_p4_t02_b2_oriented_matroid_bridge.yaml",
        "child_phys_phil_p4_t02_b2_oriented_matroid_bridge.yaml",
        "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge.yaml",
        "v22_p4_t02_b2_oriented_matroid_bridge_record_v1.yaml",
        "v22_p4_t02_b2_oriented_matroid_bridge_fixtures_v1.yaml",
        "v22_p4_t02_b2_oriented_matroid_bridge_provenance_manifest_v1.yaml",
    ]
    loaded: dict[str, dict[str, Any]] = {}
    parse_errors: list[str] = []
    for name in yaml_names:
        try:
            loaded[name] = load_yaml(ARTIFACTS / name)
        except Exception as exc:
            parse_errors.append(f"{name}: {exc}")
    check(
        "strict_unique_key_yaml",
        not parse_errors and len(loaded) == len(yaml_names),
        {"parsed": len(loaded), "expected": len(yaml_names), "errors": parse_errors},
    )
    if parse_errors:
        return emit(args, checks)

    record = loaded["v22_p4_t02_b2_oriented_matroid_bridge_record_v1.yaml"]
    fixtures = loaded["v22_p4_t02_b2_oriented_matroid_bridge_fixtures_v1.yaml"]
    conflict = loaded["parent_conflict_review_p4_t02_b2_oriented_matroid_bridge.yaml"]
    check(
        "decisive_candidate_map",
        record.get("decisive_result") == RESULT
        and record.get("no_fog_check") is True
        and record.get("bridge_attempt_status", {}).get("candidate_map") == CANDIDATE_MAP
        and record.get("bridge_attempt_status", {}).get("status")
        == "candidate_map_constructed_proposal_only_pending_smuggling_audit",
        {
            "result": record.get("decisive_result"),
            "no_fog": record.get("no_fog_check"),
            "map": record.get("bridge_attempt_status", {}).get("candidate_map"),
        },
    )

    repairs = record.get("type_repairs", [])
    check(
        "three_typing_repairs",
        {row.get("repair_id") for row in repairs}
        == {
            "BR-01-CERTIFICATE-ORBIT-DESCENT",
            "BR-02-FINITE-COMPLEXITY-PATH-DOMAIN",
            "BR-03-ADEQUATE-EXACT-DECISION-DOMAIN",
        }
        and all(row.get("result") == "repaired" for row in repairs),
        {"repair_count": len(repairs), "ids": [row.get("repair_id") for row in repairs]},
    )

    obligations = record.get("proof_obligation_status", [])
    obligation_ids = {suffix_id(row.get("obligation_id"), "PO") for row in obligations}
    failures = record.get("failure_branch_status", [])
    failure_ids = {suffix_id(row.get("branch_id"), "FB") for row in failures}
    check(
        "exact_fourteen_proof_obligations",
        len(obligations) == 14
        and obligation_ids == PROOF_IDS
        and all(str(row.get("status", "")).startswith("satisfied") for row in obligations),
        {"count": len(obligations), "missing": sorted(PROOF_IDS - obligation_ids)},
    )
    check(
        "exact_eleven_failure_branches",
        len(failures) == 11
        and failure_ids == FAILURE_IDS
        and all(str(row.get("status", "")).startswith("not_triggered") for row in failures),
        {"count": len(failures), "missing": sorted(FAILURE_IDS - failure_ids)},
    )

    freeze_rows = record.get("freeze_criteria_status", {}).get("inherited_freezes", [])
    freeze_ids = {row.get("freeze_label") for row in freeze_rows}
    check(
        "exact_three_freezes_preserved",
        freeze_ids == FREEZES
        and len(freeze_rows) == 3
        and all(row.get("status") == "preserved_not_reopened" for row in freeze_rows)
        and record.get("freeze_criteria_status", {}).get("new_freeze_added") is False,
        {"freezes": sorted(str(value) for value in freeze_ids)},
    )

    distance = record.get("distance_to_gr_status", {})
    distance_rows = distance.get("rows", [])
    distance_burdens = {row.get("burden") for row in distance_rows}
    check(
        "expanded_distance_to_gr_matrix_no_delta",
        len(distance_rows) == 14
        and distance_burdens == BURDENS
        and all(row.get("status") == "no_delta" for row in distance_rows)
        and distance.get("changed") is False
        and distance.get("ledger_updated") is False,
        {
            "count": len(distance_rows),
            "missing": sorted(BURDENS - distance_burdens),
            "extra": sorted(distance_burdens - BURDENS),
        },
    )

    payloads = record.get("new_mathematical_payload", [])
    check(
        "new_mathematical_payload",
        len(payloads) >= 5 and len({row.get("payload_id") for row in payloads}) == len(payloads),
        {"count": len(payloads), "ids": [row.get("payload_id") for row in payloads]},
    )

    successor = record.get("selected_successor_packet", {})
    check(
        "smuggling_audit_selected_not_executed",
        successor.get("packet_id") == NEXT_PACKET
        and successor.get("packet_type") == "source_extension_smuggling_audit"
        and successor.get("role_family") == NEXT_ROLE
        and successor.get("status") == "selected_not_executed"
        and successor.get("executed_in_rt014") is False,
        {"packet": successor.get("packet_id"), "role": successor.get("role_family")},
    )

    model_path = ARTIFACTS / "v22_p4_t02_b2_oriented_matroid_bridge_model.py"
    model_run = subprocess.run(
        [sys.executable, str(model_path), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    model: dict[str, Any] = {}
    model_error = ""
    try:
        model = json.loads(model_run.stdout)
    except json.JSONDecodeError as exc:
        model_error = str(exc)
    inventories = model.get("inventories", {})
    expected_counts = {
        "A_F4": (51, 14, 0, "Feasible"),
        "A_F5": (71, 20, 0, "Feasible"),
        "A_F6": (99, 28, 0, "Feasible"),
        "A_O4": (51, 14, 1, "Obstructed"),
        "A_O5": (71, 20, 2, "Obstructed"),
        "A_O6": (99, 28, 3, "Obstructed"),
    }
    count_failures: dict[str, Any] = {}
    for name, expected in expected_counts.items():
        row = inventories.get(name, {})
        actual = (
            row.get("realized_covector_count"),
            row.get("tope_count"),
            row.get("minimal_positive_circuit_count"),
            row.get("total_certificate", {}).get("tag"),
        )
        if actual != expected:
            count_failures[name] = {"expected": expected, "actual": actual}
    model_checks = model.get("checks", {})
    variation = model.get("variation_stratification", {})
    check(
        "exact_model_and_inventory",
        model_run.returncode == 0
        and model.get("status") == "PASS"
        and model.get("candidate_map") == CANDIDATE_MAP
        and len(inventories) == 6
        and not count_failures
        and model_checks
        and all(model_checks.values())
        and variation.get("arbitrary_continuous_paths_admitted") is False
        and len(variation.get("determinant_minor_walls", [])) == 1,
        {
            "returncode": model_run.returncode,
            "status": model.get("status"),
            "configuration_count": len(inventories),
            "count_failures": count_failures,
            "model_error": model_error,
        },
    )
    check(
        "fixture_record_matches_model",
        fixtures.get("model_payload_sha256") == model.get("model_payload_sha256")
        and fixtures.get("exact_domain", {}).get("fixture_field") == "Q"
        and fixtures.get("exact_domain", {}).get(
            "arbitrary_exact_representation_with_only_sign_and_rank"
        )
        is False
        and fixtures.get("variation_stratification", {}).get("arbitrary_continuous_paths_admitted")
        is False
        and all(fixtures.get("exact_checks", {}).values()),
        {
            "fixture_payload": fixtures.get("model_payload_sha256"),
            "model_payload": model.get("model_payload_sha256"),
        },
    )

    child_rows = conflict.get("child_outputs", [])
    child_failures: list[str] = []
    for row in child_rows:
        path = ROOT / str(row.get("path", ""))
        if not path.is_file() or sha256(path) != row.get("sha256"):
            child_failures.append(str(row.get("execution_unit")))
    check(
        "parent_child_synthesis_complete",
        len(child_rows) == 2
        and not child_failures
        and conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_count") == 0
        and conflict.get("unresolved_blocking_conflicts") == [],
        {
            "child_count": len(child_rows),
            "child_hash_failures": child_failures,
            "status": conflict.get("status"),
        },
    )

    manifest = loaded["v22_p4_t02_b2_oriented_matroid_bridge_provenance_manifest_v1.yaml"]
    manifest_rows = list(manifest.get("sources", [])) + list(manifest.get("child_sources", []))
    hash_failures: list[dict[str, str]] = []
    for row in manifest_rows:
        path = ROOT / str(row.get("path", ""))
        expected = str(row.get("sha256", ""))
        if not path.is_file():
            hash_failures.append({"path": str(row.get("path")), "reason": "missing"})
        else:
            actual = sha256(path)
            if actual != expected:
                hash_failures.append(
                    {"path": str(row.get("path")), "reason": "hash", "expected": expected, "actual": actual}
                )
    check(
        "source_provenance_hashes",
        len(manifest_rows) >= 15 and not hash_failures,
        {"source_count": len(manifest_rows), "failures": hash_failures},
    )

    tex_path = ARTIFACTS / "v22_p4_t02_b2_oriented_matroid_covector_circuit_bridge_v1.tex"
    tex_text = tex_path.read_text(encoding="utf-8")
    compile_receipt = load_json(
        ARTIFACTS / "v22_p4_t02_b2_oriented_matroid_bridge_latex_compile_receipt.json"
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
            "status": compile_receipt.get("status"),
            "source_hash_match": compile_receipt.get("source_sha256") == sha256(tex_path),
            "page_count": compile_receipt.get("pdf_page_count"),
            "visual_status": compile_receipt.get("visual_inspection", {}).get("status"),
        },
    )
    check(
        "tex_type_repairs_and_claim_blocks",
        "certificate orbit" in tex_text
        and "arbitrary continuous" in tex_text
        and "homogeneous linear feasibility" in tex_text
        and "no Distance-to-GR delta" in tex_text
        and "P4--T03 remains locked" in tex_text,
        "The registered manuscript states all three repairs and downstream blocks.",
    )

    tex_registry_path = ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
    markdown_registry_path = ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"
    with tex_registry_path.open(newline="", encoding="utf-8") as handle:
        tex_rows = list(csv.DictReader(handle))
    with markdown_registry_path.open(newline="", encoding="utf-8") as handle:
        markdown_rows = list(csv.DictReader(handle))
    tex_registry = next(
        (row for row in tex_rows if row.get("object_id") == "TEX-V22-P4-T02-B2-ORIENTED-MATROID-COVECTOR-CIRCUIT-BRIDGE-V1"),
        None,
    )
    markdown_registry = next(
        (row for row in markdown_rows if row.get("object_id") == "MD-V22-P4-T02-B2-PARENT-FUSION-ORIENTED-MATROID-BRIDGE-V1"),
        None,
    )
    check(
        "registered_parent_sources",
        tex_registry is not None
        and tex_registry.get("source_hash") == sha256(tex_path)
        and tex_registry.get("pdf_required") == "false"
        and markdown_registry is not None
        and markdown_registry.get("source_hash")
        == sha256(ARTIFACTS / "parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge.md"),
        {
            "tex_registered": tex_registry is not None,
            "markdown_registered": markdown_registry is not None,
        },
    )

    authority = record.get("authority_limits", {})
    false_flags = [
        "source_bridge_adopted",
        "canonical_ontology_modified",
        "source_primitives_derived_from_current_ontology",
        "descriptor_instance_complete",
        "adequacy_reevaluated",
        "b2_activated_or_disposed",
        "p4_t03_unlocked",
        "physical_causality_constructed",
        "empirical_response_constructed",
        "universal_p7_coverage_constructed",
        "conformal_structure_constructed",
        "effective_metric_constructed",
        "matter_coupling_derived",
        "einstein_equations_derived",
        "gate_b_verdict_issued",
        "benchmark_promoted",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "distance_to_gr_changed",
        "proof_authority",
        "physics_promotion_authorized",
        "publication_authorized",
        "push_authorized",
        "external_action_authorized",
    ]
    mismatches = {key: authority.get(key) for key in false_flags if authority.get(key) is not False}
    check(
        "authority_and_claim_blocks",
        authority.get("proposal_only_bridge_constructed") is True and not mismatches,
        {"mismatches": mismatches},
    )

    return emit(args, checks, model=model)


def emit(
    args: argparse.Namespace,
    checks: list[dict[str, Any]],
    *,
    model: dict[str, Any] | None = None,
) -> int:
    failure_count = sum(row["status"] != "PASS" for row in checks)
    payload: dict[str, Any] = {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_validation_v1",
        "task_id": "RT-20260810-014",
        "job_id": "AJ-RT-20260810-014-001",
        "status": "PASS" if failure_count == 0 else "FAIL",
        "check_count": len(checks),
        "failure_count": failure_count,
        "decisive_result": RESULT,
        "candidate_map": CANDIDATE_MAP,
        "selected_next_role": NEXT_ROLE,
        "selected_next_packet": NEXT_PACKET,
        "selected_next_packet_executed": False,
        "distance_to_gr_changed": False,
        "checks": checks,
        "model_summary": {
            "status": (model or {}).get("status"),
            "model_payload_sha256": (model or {}).get("model_payload_sha256"),
            "configuration_count": len((model or {}).get("inventories", {})),
        },
        "authority_note": (
            "Focused task-local validation evidence only; no ontology, physical, empirical, "
            "Gate, benchmark, proof, adoption, promotion, or Distance-to-GR authority."
        ),
    }
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_compact_receipt_v1",
            "task_id": "RT-20260810-014",
            "job_id": "AJ-RT-20260810-014-001",
            "status": payload["status"],
            "check_count": payload["check_count"],
            "failure_count": payload["failure_count"],
            "decisive_result": RESULT,
            "candidate_map": CANDIDATE_MAP,
            "selected_next_packet_executed": False,
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
