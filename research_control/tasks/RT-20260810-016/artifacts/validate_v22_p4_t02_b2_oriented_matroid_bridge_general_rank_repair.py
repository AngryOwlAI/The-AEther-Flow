#!/usr/bin/env python3
"""Focused validator for the RT016 Bridge_OM general-rank repair."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260810-016"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_validation.json"
COMPACT = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_compact_receipt.json"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def load_model() -> dict[str, Any]:
    path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_model.py"
    spec = importlib.util.spec_from_file_location("rt016_general_rank_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load RT016 exact model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build()


def nested_values(value: Any, key_names: set[str]) -> list[Any]:
    values: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) in key_names:
                values.append(child)
            values.extend(nested_values(child, key_names))
    elif isinstance(value, list):
        for child in value:
            values.extend(nested_values(child, key_names))
    return values


def check(
    condition: bool,
    name: str,
    detail: str,
    checks: list[dict[str, Any]],
) -> None:
    checks.append(
        {"check_id": name, "status": "PASS" if condition else "FAIL", "detail": detail}
    )


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required = [
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260810-016.md",
        TASK / "jobs/AJ-RT-20260810-016-001.yaml",
        TASK / "roles/candidate-constructor@0.2.0--RT-20260810-016.yaml",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_v1.tex",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_controls_v1.yaml",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_record_v1.yaml",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_provenance_manifest_v1.yaml",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_model.py",
        ART / "child_phys_math_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.yaml",
        ART / "child_phys_phil_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.yaml",
        ART / "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.yaml",
        ART / "parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.md",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_latex_compile_receipt.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    check(not missing, "required_artifacts", f"missing={missing}", checks)

    yaml_paths = [
        path for path in required if path.suffix in {".yaml", ".yml"} and path.is_file()
    ]
    yaml_errors: list[str] = []
    parsed: dict[str, Any] = {}
    for path in yaml_paths:
        try:
            parsed[path.name] = load_yaml(path)
        except Exception as exc:
            yaml_errors.append(f"{path.relative_to(ROOT)}: {exc}")
    check(not yaml_errors, "unique_key_yaml", f"errors={yaml_errors}", checks)

    manifest = parsed.get(
        "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_provenance_manifest_v1.yaml",
        {},
    )
    hash_rows = []
    if isinstance(manifest, dict):
        hash_rows = manifest.get("source_files", []) + manifest.get("artifact_files", [])
    mismatches: list[dict[str, str]] = []
    for row in hash_rows:
        path = ROOT / row["path"]
        observed = sha256(path) if path.is_file() else "missing"
        if observed != row["sha256"]:
            mismatches.append(
                {"path": row["path"], "expected": row["sha256"], "observed": observed}
            )
    check(
        len(manifest.get("source_files", [])) == 12
        and len(manifest.get("artifact_files", [])) == 9
        and not mismatches,
        "provenance_hashes",
        f"source_count={len(manifest.get('source_files', []))} "
        f"artifact_count={len(manifest.get('artifact_files', []))} mismatches={mismatches}",
        checks,
    )

    model: dict[str, Any] = {}
    model_error = ""
    try:
        model = load_model()
    except Exception as exc:
        model_error = str(exc)
    model_checks = model.get("checks", {}) if isinstance(model, dict) else {}
    check(
        not model_error
        and model.get("status") == "PASS"
        and model.get("model_payload_sha256")
        == "626b418a602e98aa860702e3ef595cb847454994cf22eb0f96fc5c85e7c0e666"
        and model_checks
        and all(model_checks.values()),
        "exact_model",
        f"error={model_error!r} payload={model.get('model_payload_sha256', '')}",
        checks,
    )
    controls_1_8 = model.get("exact_family_controls", []) if model else []
    mandatory = model.get("mandatory_controls", {}) if model else {}
    check(
        [row.get("rank") for row in controls_1_8] == list(range(1, 9))
        and mandatory.get("rank_five", {}).get("obstructed_family", {}).get("support_size") == 6
        and mandatory.get("rank_six", {}).get("obstructed_family", {}).get("support_size") == 7,
        "general_rank_exact_controls",
        "ranks 1..8 pass with sharp support six and seven at ranks five and six",
        checks,
    )

    record = parsed.get(
        "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_record_v1.yaml",
        {},
    )
    result = record.get("candidate_constructor_result", {}) if isinstance(record, dict) else {}
    bridge = record.get("bridge_attempt_status", {}) if isinstance(record, dict) else {}
    check(
        record.get("decisive_result") == "constructed_candidate"
        and record.get("no_fog_check") is True
        and result.get("result_type") == "constructed_candidate"
        and not result.get("failed_components")
        and bridge.get("candidate_map")
        == "Bridge_OM(A)=(Cstar(A),Cir_plus(A),Tot(A),Ref(A),Strat(A))"
        and bridge.get("source_map_held_fixed") is True,
        "decisive_candidate_result",
        "one no-fog constructed candidate with the fixed Bridge_OM map",
        checks,
    )

    semantic_patch = record.get("semantic_patch", {}) if record else {}
    check(
        semantic_patch.get("permitted_change_count") == 3
        and len(semantic_patch.get("changes", [])) == 3
        and semantic_patch.get("other_definition_change_count") == 0,
        "conservative_semantic_patch",
        "two theorem edits plus one conformance label; zero other definition changes",
        checks,
    )

    controls = parsed.get(
        "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_controls_v1.yaml", {}
    )
    mandatory_rows = controls.get("mandatory_controls", []) if controls else []
    count_record = controls.get("standard_sum_covector_counts", {}) if controls else {}
    check(
        controls.get("theorem_domain", {}).get("rank")
        == "arbitrary finite 1<=r=rank(A)<=card(S)"
        and controls.get("theorem_domain", {}).get("circuit_support_bound")
        == "card(C)<=r+1"
        and len(mandatory_rows) == 4
        and all(row.get("result") == "PASS" for row in mandatory_rows)
        and [row.get("circuit_support_size") for row in mandatory_rows if row.get("total_branch") == "Obstructed"]
        == [6, 7]
        and count_record.get("aggregate_four_controls", {}).get("realized_covectors") == 5072
        and count_record.get("aggregate_four_controls", {}).get("topes") == 376,
        "general_rank_domain_and_counts",
        "arbitrary finite rank, card(C)<=r+1, four passing controls, 5072 covectors, 376 topes",
        checks,
    )
    quarantine = controls.get("legacy_fixture_quarantine", {}) if controls else {}
    span = controls.get("effective_span_factorization", {}) if controls else {}
    check(
        quarantine.get("classification") == "nonphysical_conformance_sample"
        and quarantine.get("theorem_domain_restriction") is False
        and quarantine.get("target_dimension_evidence") is False
        and span.get("dual_restriction_surjective") is True
        and span.get("unused_ambient_dimensions_change_bridge_data") is False,
        "fixture_quarantine_and_span_factor",
        "bounded fixtures are nonphysical only and Bridge_OM factors through W_A",
        checks,
    )

    proof_rows = record.get("proof_obligation_status", []) if record else []
    failure_rows = record.get("failure_branch_status", []) if record else []
    distance_rows = record.get("distance_to_gr_status", {}).get("rows", []) if record else []
    check(
        len(proof_rows) == 14
        and all(row.get("status") == "satisfied" for row in proof_rows)
        and len(failure_rows) == 11
        and all(not str(row.get("status", "")).startswith("triggered") for row in failure_rows)
        and len(distance_rows) == 14
        and all(row.get("status") == "no_delta" for row in distance_rows),
        "obligation_failure_distance_matrix",
        f"proofs={len(proof_rows)} failures={len(failure_rows)} distance={len(distance_rows)}",
        checks,
    )

    freezes = record.get("freeze_criteria_status", {}).get("inherited_freezes", []) if record else []
    check(
        [row.get("freeze_label") for row in freezes]
        == [
            "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
            "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
            "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
        ]
        and all(row.get("status") == "preserved_not_reopened" for row in freezes),
        "freeze_preservation",
        f"freezes={freezes}",
        checks,
    )

    child_files = [
        "child_phys_math_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.yaml",
        "child_phys_phil_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.yaml",
    ]
    child_summaries: list[dict[str, Any]] = []
    for filename in child_files:
        child = parsed.get(filename, {})
        result_values = nested_values(child, {"result_type", "decisive_result"})
        role_values = nested_values(child, {"role_family"})
        packet_type_values = nested_values(child, {"packet_type"})
        child_summaries.append(
            {
                "filename": filename,
                "constructed": "constructed_candidate" in result_values,
                "smuggling_auditor": "smuggling-auditor@0.2.0" in role_values,
                "audit_type": "source_extension_smuggling_audit" in packet_type_values,
            }
        )
    check(
        len(child_summaries) == 2
        and all(
            row["constructed"] and row["smuggling_auditor"] and row["audit_type"]
            for row in child_summaries
        ),
        "independent_children",
        json.dumps(child_summaries, sort_keys=True),
        checks,
    )

    conflict = parsed.get(
        "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.yaml",
        {},
    )
    check(
        conflict.get("blocking_conflict_count") == 0
        and conflict.get("all_conflicts_resolved") is True
        and conflict.get("consensus", {}).get("decisive_result") == "constructed_candidate"
        and conflict.get("snapshot_resolution", {}).get("final_parent_tex_sha256")
        == sha256(ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_v1.tex"),
        "parent_conflict_review",
        "zero blocking conflicts and final parent snapshot reconciled",
        checks,
    )

    successor = record.get("selected_successor", {}) if record else {}
    check(
        successor.get("packet_id")
        == "PKT-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-GENERAL-RANK-POST-REPAIR-AUDIT-V1"
        and successor.get("packet_type") == "source_extension_smuggling_audit"
        and successor.get("role_family") == "smuggling-auditor@0.2.0"
        and successor.get("executed") is False,
        "unexecuted_successor",
        "one focused post-repair Smuggling Auditor packet selected but not executed",
        checks,
    )

    tex_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.is_file() else ""
    required_phrases = [
        "There is no absolute upper bound on $r$",
        "|C|\\le r+1",
        "3^{r+1}-2^{r+2}+2",
        "nonphysical\\_conformance\\_sample",
        "dimension-erasure criterion",
        "does not imply P7 universality",
        "All fourteen Distance-to-GR burdens remain unchanged",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in tex]
    check(not missing_phrases, "manuscript_contract", f"missing={missing_phrases}", checks)

    fusion_path = ART / "parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.md"
    fusion = fusion_path.read_text(encoding="utf-8") if fusion_path.is_file() else ""
    fusion_phrases = [
        "result: constructed_candidate",
        "5072 covectors and 376 topes",
        "zero blocking conflicts",
        "selected but not executed in RT016",
    ]
    check(
        all(phrase in fusion for phrase in fusion_phrases),
        "parent_fusion_contract",
        f"missing={[phrase for phrase in fusion_phrases if phrase not in fusion]}",
        checks,
    )

    compile_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_latex_compile_receipt.json"
    compile_receipt = json.loads(compile_path.read_text(encoding="utf-8")) if compile_path.is_file() else {}
    check(
        compile_receipt.get("status") == "PASS"
        and compile_receipt.get("compiler_exit_code") == 0
        and compile_receipt.get("source_sha256") == sha256(tex_path)
        and compile_receipt.get("pdf_page_count") == 4
        and compile_receipt.get("overfull_hbox_count") == 0
        and compile_receipt.get("visual_inspection", {}).get("status") == "PASS"
        and compile_receipt.get("visual_inspection", {}).get("pages_inspected") == [1, 2, 3, 4],
        "latex_compile_and_visual_review",
        f"source={compile_receipt.get('source_sha256')} pages={compile_receipt.get('pdf_page_count')}",
        checks,
    )

    authority = record.get("authority_limits", {}) if record else {}
    required_false = [
        "descriptor_instance_complete",
        "adequacy_reevaluated",
        "b2_fallback_activated",
        "b2_activated",
        "p4_t02_complete_for_plan_dependency",
        "p4_t03_unlocked",
        "source_law_adopted",
        "canonical_ontology_modified",
        "physical_status_changed",
        "scientific_claims_changed",
        "distance_to_gr_delta_changed",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
        "external_action_authorized",
        "physics_promotion_authorized",
    ]
    check(
        all(authority.get(key) is False for key in required_false),
        "authority_limits",
        f"nonfalse={[key for key in required_false if authority.get(key) is not False]}",
        checks,
    )

    registry_checks = {
        "registries/RESEARCH_TASK_REGISTRY.csv": "RT-20260810-016",
        "registries/DIRECTOR_DECISION_REGISTRY.csv": "DDR-20260810-016",
        "registries/AGENT_JOB_REGISTRY.csv": "AJ-RT-20260810-016-001",
        "registries/ROLE_EXECUTION_REGISTRY.csv": "candidate-constructor@0.2.0--RT-20260810-016",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv": "CB-V22-P4-T02-B2-ORIENTED-MATROID-BRIDGE-GENERAL-RANK-REPAIR-001",
    }
    missing_registry_ids = [
        identifier
        for path, identifier in registry_checks.items()
        if identifier not in (ROOT / path).read_text(encoding="utf-8")
    ]
    check(not missing_registry_ids, "control_registries", f"missing={missing_registry_ids}", checks)

    status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_validation_v1",
        "task_id": "RT-20260810-016",
        "job_id": "AJ-RT-20260810-016-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "fail_count": sum(row["status"] == "FAIL" for row in checks),
        "model_payload_sha256": model.get("model_payload_sha256", ""),
        "checks": checks,
        "authority_limits": {
            "validator_pass_is_scientific_authority": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_compact_receipt_v1",
            "task_id": report["task_id"],
            "job_id": report["job_id"],
            "status": report["status"],
            "check_count": report["check_count"],
            "pass_count": report["pass_count"],
            "fail_count": report["fail_count"],
            "validation_sha256": sha256(REPORT),
            "model_payload_sha256": report["model_payload_sha256"],
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
