#!/usr/bin/env python3
"""Focused validator for the bounded RT011 ontology-law obstruction transaction."""

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
TASK = REPO / "research_control/tasks/RT-20260811-011"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_validation.json"
COMPACT = ART / "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_compact_receipt.json"

OBSTRUCTION = "OB-V22-P4T02-B2-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-COERCIVE-PROTECTION-PRES-SRC-PROVENANCE-001"
SUCCESSOR = "PKT-V22-P4T02-B2-POST-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-COERCIVE-PROTECTION-OBSTRUCTION-THEORETICAL-CONTINUATION-SELECTION-V1"
SUCCESSOR_ROLE = "theoretical-continuation-selector@0.1.0"
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


def load_registry_row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get(key) == value:
                return row
    return {}


def fourteen_no_delta(rows: Any) -> bool:
    return (
        isinstance(rows, list)
        and len(rows) == 14
        and {row.get("burden") for row in rows if isinstance(row, dict)} == BURDENS
        and all(row.get("status") == "no_delta" for row in rows if isinstance(row, dict))
    )


def validate() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, bool] = {}
    paths = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260811-011-001.yaml",
        "role": TASK / "roles/ontology-formalizer@0.2.0--RT-20260811-011.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260811-011-001.yaml",
        "handoff": REPO / "research_control/handoffs/handoff-1025.yaml",
        "math_child": ART / "child_phys_math_p4_t02_b2_source_generated_compact_root_family_coercive_protection_law.yaml",
        "phil_child": ART / "child_phys_phil_p4_t02_b2_source_generated_compact_root_family_coercive_protection_law.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_source_generated_compact_root_family_coercive_protection_law.yaml",
        "record": ART / "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_record_v1.yaml",
        "controls": ART / "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_controls_v1.yaml",
        "manifest": ART / "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_provenance_manifest_v1.yaml",
        "tex": ART / "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_law_v1.tex",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_source_generated_compact_root_family_coercive_protection_law.md",
        "compile": ART / "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_latex_compile_receipt.json",
        "model": ART / "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_model.py",
    }
    checks["all_expected_inputs_exist"] = all(path.exists() for path in paths.values())
    if not checks["all_expected_inputs_exist"]:
        errors.extend(str(path.relative_to(REPO)) for path in paths.values() if not path.exists())

    yaml_names = (
        "task", "job", "role", "completion", "handoff", "math_child",
        "phil_child", "conflict", "record", "controls", "manifest",
    )
    loaded: dict[str, dict[str, Any]] = {}
    for name in yaml_names:
        try:
            loaded[name] = load_yaml(paths[name])
        except Exception as exc:  # noqa: BLE001 - aggregate exact validation failures
            errors.append(f"{name}: {exc}")
    checks["unique_key_yaml_parse"] = len(loaded) == len(yaml_names)

    manifest = loaded.get("manifest", {})
    manifest_sources = manifest.get("sources", [])
    mismatches: list[str] = []
    for item in manifest_sources if isinstance(manifest_sources, list) else []:
        if not isinstance(item, dict):
            mismatches.append("non-map manifest source")
            continue
        source = REPO / str(item.get("path", ""))
        if not source.exists() or sha256(source) != str(item.get("sha256", "")):
            mismatches.append(str(item.get("path", "")))
    checks["source_manifest_hashes"] = (
        not mismatches
        and len(manifest_sources) == 25
        and manifest.get("source_count") == 25
    )
    errors.extend(f"source hash mismatch: {item}" for item in mismatches)

    record = loaded.get("record", {})
    decisive = record.get("decisive_result", {})
    obstruction = record.get("obstruction_record", {})
    checks["record_decisive_obstruction"] = (
        decisive.get("result_type") == "precise_obstruction"
        and decisive.get("obstruction_id") == OBSTRUCTION
        and decisive.get("no_fog_check") is True
        and obstruction.get("scope") == "current_ontology_only"
        and obstruction.get("current_ontology_implication") == "does_not_derive"
        and obstruction.get("source_extension_implication") == "new_primitive_required"
    )
    checks["record_obligation_cardinality"] = len(record.get("proof_obligations", [])) == 14
    checks["record_failure_cardinality"] = len(record.get("failure_branches", [])) == 11
    checks["record_freezes"] = set(record.get("preserved_freeze_labels", [])) == FREEZES
    checks["record_fourteen_no_delta"] = fourteen_no_delta(record.get("distance_to_gr_status"))
    selected = record.get("selected_successor", {})
    checks["record_successor_unexecuted"] = (
        selected.get("packet_id") == SUCCESSOR
        and selected.get("next_role_family") == SUCCESSOR_ROLE
        and selected.get("selected_not_executed") is True
    )

    conflict = loaded.get("conflict", {})
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
        and conflict.get("resolution_rounds") == 1
        and conflict.get("resolved_conflict_count") == 2
        and conflict.get("unresolved_conflicts") == []
        and conflict.get("fusion_result", {}).get("unresolved_blocking_conflict_count") == 0
    )
    for name in ("math_child", "phil_child"):
        text = paths[name].read_text(encoding="utf-8")
        checks[f"{name}_obstruction_identity"] = OBSTRUCTION in text and "precise_obstruction" in text
        checks[f"{name}_six_freezes"] = all(freeze in text for freeze in FREEZES)
        checks[f"{name}_fourteen_no_delta"] = text.count("task_delta: no_delta") == 14

    completion = loaded.get("completion", {})
    checks["completion_terminal_status"] = (
        completion.get("status") == "completed"
        and completion.get("result") == "completed"
        and completion.get("objective_result") == "precise_obstruction"
        and completion.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
    )
    checks["completion_obstruction_contract"] = (
        completion.get("obstruction_record", {}).get("obstruction_id") == OBSTRUCTION
        and completion.get("physics_progress_status", {}).get("status") == "precise_obstruction_found"
        and completion.get("ontology_law_research_packet", {}).get("packet_payload_mode") == "candidate_law_refutation"
        and completion.get("ontology_law_research_packet", {}).get("adoption_status", {}).get("status_pair") == "blocked_adoption_open_continuation"
    )
    checks["completion_payloads"] = (
        len(completion.get("new_mathematical_payload", [])) == 4
        and len(completion.get("mathematical_payload_manifest", [])) == 4
    )
    checks["completion_fourteen_no_delta"] = fourteen_no_delta(completion.get("distance_to_gr_status"))
    checks["completion_six_freezes"] = set(
        completion.get("freeze_criteria_status", {}).get("preserved_freeze_labels", [])
    ) == FREEZES
    checks["completion_successor_unexecuted"] = (
        completion.get("selected_successor", {}).get("packet_id") == SUCCESSOR
        and completion.get("selected_successor", {}).get("role_family") == SUCCESSOR_ROLE
        and completion.get("selected_successor", {}).get("executed") is False
    )

    handoff = loaded.get("handoff", {})
    checks["handoff_binds_completion"] = (
        handoff.get("handoff_id") == "handoff-1025"
        and handoff.get("completion_sha256") == sha256(paths["completion"])
        and handoff.get("claim_boundary", {}).get("completed_completion_sha256") == sha256(paths["completion"])
    )
    checks["handoff_successor_boundary"] = (
        handoff.get("required_next_packet", {}).get("packet_id") == SUCCESSOR
        and handoff.get("required_next_packet", {}).get("executed") is False
        and handoff.get("selected_next_route", {}).get("role_family") == SUCCESSOR_ROLE
        and handoff.get("loop_risk_route") == "theoretical_decision_role_selection"
    )
    checks["handoff_fourteen_no_delta"] = fourteen_no_delta(handoff.get("distance_to_gr_status"))

    checks["control_lifecycle_terminal"] = all(
        loaded.get(name, {}).get("status") == "completed"
        for name in ("task", "job", "role")
    )
    checks["job_children_terminal"] = all(
        row.get("status") == "completed"
        for row in loaded.get("job", {}).get("role_decomposition", {}).get("children", [])
        if isinstance(row, dict)
    )

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
            and model.get("decisive_result") == "precise_obstruction"
            and model.get("obstruction_id") == OBSTRUCTION
            and len(model.get("checks", {})) == 19
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
            and compile_receipt.get("compile_exit_code") == 0
            and compile_receipt.get("page_count") == 5
            and compile_receipt.get("visual_inspection", {}).get("status") == "PASS"
            and compile_receipt.get("visual_inspection", {}).get("inspected_page_count") == 5
        )
    except Exception as exc:  # noqa: BLE001
        errors.append(f"compile receipt: {exc}")
        checks["latex_and_visual_pass"] = False

    task_row = load_registry_row(REPO / "registries/RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260811-011")
    job_row = load_registry_row(REPO / "registries/AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260811-011-001")
    tex_row = load_registry_row(REPO / "registries/TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V22-P4-T02-B2-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-COERCIVE-PROTECTION-LAW-V1")
    md_row = load_registry_row(REPO / "registries/MARKDOWN_SOURCE_REGISTRY.csv", "object_id", "MD-V22-P4-T02-B2-PARENT-FUSION-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-COERCIVE-PROTECTION-LAW-V1")
    checks["control_registry_terminal"] = task_row.get("status") == "completed" and job_row.get("status") == "completed"
    checks["source_registry_hashes"] = tex_row.get("source_hash") == sha256(paths["tex"]) and md_row.get("source_hash") == sha256(paths["fusion"])

    tex_text = paths["tex"].read_text(encoding="utf-8")
    fusion_text = paths["fusion"].read_text(encoding="utf-8")
    tex_flat = " ".join(tex_text.split())
    fusion_flat = " ".join(fusion_text.split())
    tex_identity = tex_flat.replace("\\\\ ", "")
    checks["fused_boundary_language"] = (
        OBSTRUCTION in tex_identity
        and OBSTRUCTION in fusion_text
        and "current canonical source" in tex_text
        and "current canonical source" in fusion_text
        and "selected but not executed" in tex_flat
        and "selected but not executed" in fusion_flat
    )
    checks["no_tab_or_trailing_whitespace"] = all(
        "\t" not in path.read_text(encoding="utf-8")
        and all(line == line.rstrip() for line in path.read_text(encoding="utf-8").splitlines())
        for name, path in paths.items()
        if name not in {"compile"}
    )

    for name, passed in checks.items():
        if not passed:
            errors.append(f"failed check: {name}")
    status = "PASS" if not errors else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_validation_v1",
        "task_id": "RT-20260811-011",
        "job_id": "AJ-RT-20260811-011-001",
        "status": status,
        "validated_at": "2026-08-11T22:06:44Z",
        "decisive_result": "precise_obstruction",
        "obstruction_id": OBSTRUCTION,
        "selected_successor_packet_id": SUCCESSOR,
        "selected_successor_executed": False,
        "check_count": len(checks),
        "passed_check_count": sum(1 for value in checks.values() if value),
        "failed_check_count": sum(1 for value in checks.values() if not value),
        "checks": checks,
        "errors": errors,
        "model_summary": {
            "status": model_summary.get("status"),
            "check_count": len(model_summary.get("checks", {})),
            "first_missing_primitive": model_summary.get("first_missing_primitive"),
        },
        "authority_note": "Focused conformance validation is not source-law truth, ontology adoption, physical evidence, proof promotion, or Distance-to-GR progress.",
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
            "schema_id": "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_compact_receipt_v1",
            "task_id": result["task_id"],
            "job_id": result["job_id"],
            "status": result["status"],
            "check_count": result["check_count"],
            "passed_check_count": result["passed_check_count"],
            "failed_check_count": result["failed_check_count"],
            "finding_count": len(result["errors"]),
            "decisive_result": "precise_obstruction",
            "obstruction_id": OBSTRUCTION,
            "selected_successor_packet_id": SUCCESSOR,
            "selected_successor_executed": False,
            "report_path": REPORT.relative_to(REPO).as_posix(),
            "report_sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
            "authority_note": "Compact validation receipt only; no scientific or promotion authority.",
        }
        COMPACT.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.json:
        print(serialized, end="")
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
