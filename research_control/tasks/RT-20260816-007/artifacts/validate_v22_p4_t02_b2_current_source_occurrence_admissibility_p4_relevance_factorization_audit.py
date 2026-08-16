#!/usr/bin/env python3
"""Focused validator for the RT-20260816-007 factorization audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent

RECORD = ARTIFACTS / "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit_record_v1.yaml"
CONTROLS = ARTIFACTS / "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_controls_v1.yaml"
MODEL = ARTIFACTS / "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_model.py"
MATH_CHILD = ARTIFACTS / "child_phys_math_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit.yaml"
PHIL_CHILD = ARTIFACTS / "child_phys_phil_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit.yaml"
CONFLICT = ARTIFACTS / "parent_conflict_review_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit.yaml"
FUSION = ARTIFACTS / "parent_fusion_notes_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit.md"
TEX = ARTIFACTS / "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit_v1.tex"
COMPILE = ARTIFACTS / "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit_latex_compile_receipt.json"
MANIFEST = ARTIFACTS / "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit_provenance_manifest_v1.yaml"
VALIDATION = ARTIFACTS / "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit_validation.json"
COMPACT = ARTIFACTS / "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit_compact_receipt.json"

RESULT = "current_source_combined_extension_typing_or_provenance_obstruction"
OBSTRUCTION = "OB-V22-P4T02-B2-CURRENT-SOURCE-COMBINED-OCCURRENCE-EXTENSION-TYPING-PROVENANCE-001"
SUCCESSOR = "PKT-V22-P4T02-B2-POST-OCCURRENCE-P4-RELEVANCE-FACTORIZATION-OBSTRUCTION-THEORETICAL-CONTINUATION-SELECTION-V1"
SUCCESSOR_TYPE = "theoretical_continuation_selector"
SUCCESSOR_ROLE = "theoretical-continuation-selector@0.1.0"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing mapping",
                node.start_mark,
                f"duplicate key: {key}",
                key_node.start_mark,
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
    completed = subprocess.run(
        [sys.executable, str(MODEL)],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(completed.stdout)
    if not isinstance(data, dict):
        raise RuntimeError("factorization model did not emit one JSON object")
    return data


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
        RECORD,
        CONTROLS,
        MODEL,
        MATH_CHILD,
        PHIL_CHILD,
        CONFLICT,
        FUSION,
        TEX,
        COMPILE,
        MANIFEST,
    ]
    check("required_artifacts", all(path.is_file() for path in required), f"required={len(required)}")
    if not all(path.is_file() for path in required):
        return {"status": "FAIL", "checks": checks}

    yaml_paths = [RECORD, CONTROLS, MATH_CHILD, PHIL_CHILD, CONFLICT, MANIFEST]
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

    record = parsed[RECORD]
    controls = parsed[CONTROLS]
    math_child = parsed[MATH_CHILD]
    phil_child = parsed[PHIL_CHILD]
    conflict = parsed[CONFLICT]
    manifest = parsed[MANIFEST]

    result_values = {
        record.get("decisive_result", {}).get("result_type"),
        math_child.get("exclusive_result", {}).get("result_type"),
        phil_child.get("selected_result", phil_child.get("decisive_result", {})).get("result_type"),
        conflict.get("final_result", {}).get("result_type"),
    }
    obstruction_values = {
        record.get("decisive_result", {}).get("obstruction_id"),
        conflict.get("final_result", {}).get("obstruction_id"),
    }
    child_text = MATH_CHILD.read_text(encoding="utf-8") + PHIL_CHILD.read_text(encoding="utf-8")
    check("exclusive_result_convergence", result_values == {RESULT}, repr(result_values))
    check("obstruction_identity_convergence", obstruction_values == {OBSTRUCTION} and child_text.count(OBSTRUCTION) >= 4, repr(obstruction_values))
    check(
        "first_failed_primitive",
        record.get("decisive_result", {}).get("first_failed_primitive_id") == "OBJ-02-X-OCC"
        and record.get("dependency_order", [])[0].get("primitive") == "X_OCC",
        str(record.get("decisive_result", {}).get("first_failed_primitive")),
    )

    check(
        "formal_contract_counts",
        len(record.get("formal_domains", [])) == 10
        and len(record.get("formal_objects", [])) == 11
        and len(record.get("formal_maps", [])) == 10
        and len(record.get("theorem_results", [])) == 6
        and len(record.get("proof_obligations", [])) == 16
        and len(record.get("failure_branches", [])) == 15,
        "domains=10 objects=11 maps=10 theorems=6 obligations=16 branches=15",
    )
    control_rows = controls.get("controls", [])
    check(
        "six_exact_controls",
        len(control_rows) == 6 and all(row.get("status") in {"PASS", "PASS_CONDITIONAL"} for row in control_rows),
        f"controls={len(control_rows)}",
    )
    payloads = record.get("new_mathematical_payload", [])
    check(
        "new_mathematical_payload",
        len(payloads) == 8 and all(item.get("proof_control") and item.get("falsifier") for item in payloads),
        f"payloads={len(payloads)}",
    )

    freezes = record.get("preserved_freezes", [])
    distance_rows = record.get("distance_to_gr_status", [])
    check("nine_inherited_freezes", len(freezes) == 9 and len({row.get("freeze_id") for row in freezes}) == 9, f"count={len(freezes)}")
    check("freeze_evaluation", record.get("freeze_evaluation", {}).get("evaluated") is True and record.get("freeze_evaluation", {}).get("new_candidate_local_freeze_created") is False, repr(record.get("freeze_evaluation")))
    check("fourteen_literal_no_delta", len(distance_rows) == 14 and all(row.get("task_delta") == "no_delta" for row in distance_rows), f"rows={len(distance_rows)}")

    binding = record.get("registered_p4_t01_binding", {})
    p4_path = ROOT / binding.get("canonical_path", "")
    check(
        "registered_p4_t01_binding",
        p4_path.is_file()
        and sha256(p4_path) == binding.get("canonical_sha256")
        and binding.get("codomain_id") == "Y_PS"
        and binding.get("codomain_scope") == "source_principal_only",
        str(binding.get("canonical_sha256")),
    )

    successor = record.get("selected_successor", {})
    conflict_successor = conflict.get("selected_successor", {})
    check(
        "successor_selected_not_executed",
        successor.get("packet_id") == SUCCESSOR
        and successor.get("packet_type") == SUCCESSOR_TYPE
        and successor.get("role_family") == SUCCESSOR_ROLE
        and successor.get("status") == "selected_not_executed"
        and successor.get("executed") is False
        and conflict_successor.get("packet_id") == SUCCESSOR
        and conflict_successor.get("executed") is False,
        SUCCESSOR,
    )

    locks = record.get("downstream_locks", {})
    check(
        "downstream_locks",
        locks.get("p4_t02_complete_for_plan_dependency") is False
        and locks.get("occurrence_p4_irrelevance_theorem_established") is False
        and locks.get("response_bridge_constructed") is False
        and locks.get("d7_reevaluated") is False
        and locks.get("b2_activated") is False
        and locks.get("p4_t03_locked") is True
        and locks.get("p4_t03_unlocked_or_executed") is False
        and locks.get("selected_successor_executed") is False,
        repr(locks),
    )

    authority = record.get("authority_limits", {})
    required_false = [
        "current_source_X_OCC_derived",
        "current_source_U_derived",
        "current_source_R_derived",
        "current_source_factorization_theorem_claimed",
        "current_source_nonfactorization_witness_claimed",
        "occurrence_p4_irrelevance_claimed",
        "source_law_adopted",
        "ontology_modified",
        "physical_response_established",
        "effective_metric_constructed",
        "global_no_go_claimed",
        "proof_authority",
        "physics_promotion_authorized",
        "publication_authorized",
        "push_authorized",
        "external_action_authorized",
    ]
    check("authority_blocks", all(authority.get(key) is False for key in required_false), f"checked={len(required_false)}")
    check(
        "parent_conflict_resolved",
        conflict.get("unresolved_blocking_conflict_count") == 0
        and conflict.get("conflict_review", {}).get("conflict_resolution_rounds_used") == 1
        and conflict.get("shared_consensus", {}).get("result_converged") is True,
        repr(conflict.get("unresolved_blocking_conflict_count")),
    )
    check("child_artifacts_distinct", sha256(MATH_CHILD) != sha256(PHIL_CHILD), "independent child hashes differ")

    model = load_model()
    check(
        "exact_model",
        model.get("fail_count") == 0 and model.get("pass_count") == 24 and model.get("check_count") == 24,
        f"payload_sha256={model.get('payload_sha256')}",
    )

    compile_receipt = json.loads(COMPILE.read_text(encoding="utf-8"))
    check(
        "latex_compile_visual_review",
        compile_receipt.get("status") == "PASS"
        and compile_receipt.get("source_sha256") == sha256(TEX)
        and compile_receipt.get("scratch_pdf_page_count") == 3
        and compile_receipt.get("final_pass_warning_count") == 0
        and compile_receipt.get("final_pass_undefined_reference_count") == 0
        and compile_receipt.get("final_pass_overfull_box_count") == 0
        and compile_receipt.get("visual_review", {}).get("status") == "PASS",
        repr(compile_receipt.get("status")),
    )
    tex_text = TEX.read_text(encoding="utf-8")
    tex_identity_text = re.sub(r"\\allowbreak\s*", "", tex_text).replace("\n", "")
    tex_prose_text = re.sub(r"\s+", " ", tex_text)
    check(
        "tex_identity_and_boundaries",
        OBSTRUCTION in tex_identity_text
        and SUCCESSOR in tex_identity_text
        and "selected but not executed" in tex_prose_text
        and "fourteen Distance-to-GR rows" in tex_text
        and "nine inherited local freezes" in tex_text,
        "result, successor, freeze, and no-delta boundaries present",
    )

    manifest_entries = manifest.get("governing_sources", []) + manifest.get("fused_artifacts", [])
    bad_manifest: list[str] = []
    for entry in manifest_entries:
        path = ROOT / entry["path"]
        if not path.is_file() or sha256(path) != entry["sha256"]:
            bad_manifest.append(entry["path"])
    check("provenance_hashes", not bad_manifest, "bad=" + repr(bad_manifest))

    check("whitespace", all(no_whitespace_errors(path) for path in required + [Path(__file__).resolve()]), f"files={len(required) + 1}")

    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "task_id": "RT-20260816-007",
        "job_id": "AJ-RT-20260816-007-001",
        "result_type": RESULT,
        "obstruction_id": OBSTRUCTION,
        "selected_successor_packet_id": SUCCESSOR,
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
            "schema_id": "v22_p4_t02_b2_current_source_occurrence_admissibility_p4_relevance_factorization_audit_compact_receipt_v1",
            "status": result["status"],
            "task_id": result.get("task_id"),
            "job_id": result.get("job_id"),
            "result_type": result.get("result_type"),
            "obstruction_id": result.get("obstruction_id"),
            "selected_successor_packet_id": result.get("selected_successor_packet_id"),
            "check_count": result.get("check_count", 0),
            "pass_count": result.get("pass_count", 0),
            "fail_count": result.get("fail_count", 0),
            "model_payload_sha256": result.get("model_payload_sha256"),
            "successor_executed": False,
            "distance_to_gr_changed": False,
            "authority_note": result.get("authority_note"),
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
