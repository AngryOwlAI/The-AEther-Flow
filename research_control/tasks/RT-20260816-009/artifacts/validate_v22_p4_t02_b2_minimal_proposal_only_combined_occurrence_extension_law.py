#!/usr/bin/env python3
"""Focused validation for RT-20260816-009."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = ROOT / "research_control/tasks/RT-20260816-009/artifacts"
STEM = "v22_p4_t02_b2_minimal_proposal_only_combined_occurrence_extension_law"
RECORD = ART / f"{STEM}_record_v1.yaml"
CONTROLS = ART / f"{STEM}_controls_v1.yaml"
MODEL = ART / f"{STEM}_model.py"
TEX = ART / f"{STEM}_v1.tex"
CHILD_MATH = ART / "child_phys_math_p4_t02_b2_minimal_proposal_only_combined_occurrence_extension_law.yaml"
CHILD_PHIL = ART / "child_phys_phil_p4_t02_b2_minimal_proposal_only_combined_occurrence_extension_law.yaml"
CONFLICT = ART / "parent_conflict_review_p4_t02_b2_minimal_proposal_only_combined_occurrence_extension_law.yaml"
FUSION = ART / "parent_fusion_notes_p4_t02_b2_minimal_proposal_only_combined_occurrence_extension_law.md"
SELECTED = ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_selected_future_packet_v1.yaml"
PROVENANCE = ART / f"{STEM}_provenance_manifest_v1.yaml"
LATEX_RECEIPT = ART / f"{STEM}_latex_compile_receipt.json"
VALIDATION = ART / f"{STEM}_validation.json"
COMPACT = ART / f"{STEM}_compact_receipt.json"

RESULT = "proposal_only_combined_occurrence_extension_law_constructed_pending_smuggling_audit"
CANDIDATE = "CAND-V22-P4T02-B2-IDEMPOTENT-EQUATION-DECORATION-COMBINED-EXTENSION-V1"
LAW = "LAW-V22-P4T02-B2-IDEMPOTENT-EQUATION-DECORATION-NULL-ATTACHMENT-V1"
ATTACHMENT = "deterministic_natural_null_section"
SUCCESSOR = "PKT-V22-P4T02-B2-IDEMPOTENT-EQUATION-DECORATION-COMBINED-EXTENSION-SOURCE-EXTENSION-SMUGGLING-AUDIT-V1"


class UniqueLoader(yaml.SafeLoader):
    pass


def _construct_mapping(
    loader: UniqueLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        result: list[Any] = []
        for item in value.values():
            result.extend(scalar_values(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(scalar_values(item))
        return result
    return [value]


def validate() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    required = [
        RECORD,
        CONTROLS,
        MODEL,
        TEX,
        CHILD_MATH,
        CHILD_PHIL,
        CONFLICT,
        FUSION,
        SELECTED,
        PROVENANCE,
        LATEX_RECEIPT,
    ]
    checks["required_files"] = all(path.is_file() for path in required)
    if not checks["required_files"]:
        missing = [
            str(path.relative_to(ROOT)) for path in required if not path.is_file()
        ]
        return {"status": "FAIL", "checks": checks, "missing": missing}

    record = load_yaml(RECORD)
    controls = load_yaml(CONTROLS)
    child_math = load_yaml(CHILD_MATH)
    child_phil = load_yaml(CHILD_PHIL)
    conflict = load_yaml(CONFLICT)
    selected = load_yaml(SELECTED)
    provenance = load_yaml(PROVENANCE)
    latex_receipt = json.loads(LATEX_RECEIPT.read_text(encoding="utf-8"))

    checks["exclusive_result"] = (
        record.get("result_type") == RESULT and record.get("result_count") == 1
    )
    checks["candidate_and_law"] = (
        record.get("candidate_id") == CANDIDATE
        and record.get("law_id") == LAW
        and record["construction"]["attachment_semantic_mode"] == ATTACHMENT
    )
    checks["roots_4"] = (
        record["proposal_roots"]["root_count"]
        == len(record["proposal_roots"]["items"])
        == 4
    )
    checks["domains_10"] = (
        record["formal_domains"]["domain_count"]
        == len(record["formal_domains"]["items"])
        == 10
    )
    checks["objects_12"] = (
        record["formal_objects"]["object_count"]
        == len(record["formal_objects"]["items"])
        == 12
    )
    checks["maps_10"] = (
        record["formal_maps"]["map_count"]
        == len(record["formal_maps"]["items"])
        == 10
    )
    checks["theorems_6"] = (
        record["theorem_targets"]["theorem_count"]
        == len(record["theorem_targets"]["items"])
        == 6
    )
    obligations = record["proof_obligations"]["items"]
    checks["obligations_16"] = (
        record["proof_obligations"]["obligation_count"] == len(obligations) == 16
        and record["proof_obligations"]["discharged_count"] == 16
        and all(str(item.get("status", "")).startswith("discharged") for item in obligations)
    )
    branches = record["failure_branches"]["items"]
    checks["branches_14"] = (
        record["failure_branches"]["branch_count"] == len(branches) == 14
        and record["failure_branches"]["triggered_count"] == 0
        and all(str(item.get("status", "")).startswith("not_triggered") for item in branches)
    )
    checks["payloads_5"] = (
        record["new_mathematical_payload"]["payload_count"]
        == len(record["new_mathematical_payload"]["items"])
        == 5
    )
    checks["controls_6"] = (
        controls.get("control_count") == len(controls.get("controls", [])) == 6
        and all(item.get("passed") is True for item in controls["controls"])
        and record["exact_controls"]["control_count"] == 6
        and record["exact_controls"]["all_passed"] is True
    )
    checks["freezes_9"] = (
        record["freeze_status"]["freeze_count"]
        == len(set(record["freeze_status"]["labels"]))
        == 9
        and record["freeze_status"]["all_preserved"] is True
    )
    rows = record["distance_to_gr_status"]["rows"]
    checks["distance_14_no_delta"] = (
        record["distance_to_gr_status"]["row_count"] == len(rows) == 14
        and record["distance_to_gr_status"]["literal_no_delta_row_count"] == 14
        and all(row.get("status") == "no_delta" for row in rows)
    )
    checks["material_distinctness"] = (
        record["material_distinctness"]["materially_distinct"] is True
        and record["material_distinctness"]["comparison_count"]
        == len(record["material_distinctness"]["comparisons"])
        == 10
    )
    checks["provenance_dag"] = (
        record["provenance_dag"]["acyclic"] is True
        and record["provenance_dag"]["pre_outcome"] is True
    )
    checks["successor_exact_unexecuted"] = (
        record["selected_successor"]["packet_id"] == SUCCESSOR
        and record["selected_successor"]["packet_type"]
        == "source_extension_smuggling_audit"
        and record["selected_successor"]["next_role"] == "smuggling-auditor@0.2.0"
        and record["selected_successor"]["status"] == "selected_not_executed"
        and record["selected_successor"]["executed"] is False
    )
    checks["selected_packet_exact_unexecuted"] = (
        selected["packet"]["packet_id"] == SUCCESSOR
        and selected["packet"]["packet_type"] == "source_extension_smuggling_audit"
        and selected["packet"]["selected_packet_executed"] is False
        and selected["status"] == "selected_not_executed"
    )
    checks["downstream_locks"] = all(
        value is False for value in record["downstream_locks"].values()
    )

    math_values = scalar_values(child_math)
    phil_values = scalar_values(child_phil)
    checks["children_converge"] = all(
        token in math_values and token in phil_values
        for token in [RESULT, CANDIDATE, LAW, SUCCESSOR]
    )
    checks["child_hashes_bound"] = (
        record["parent_child_synthesis"]["child_math_sha256"] == sha256(CHILD_MATH)
        and record["parent_child_synthesis"]["child_phil_sha256"] == sha256(CHILD_PHIL)
    )
    checks["conflict_resolved"] = (
        conflict.get("unresolved_conflict_count") == 0
        and conflict["canonical_result"]["candidate_id"] == CANDIDATE
        and conflict["canonical_successor_packet_id"] == SUCCESSOR
        and conflict["successor_executed"] is False
    )

    source_checks = []
    for item in record["governing_sources"]["items"]:
        source_checks.append(
            sha256(ROOT / item["path"]) == item["sha256"]
        )
    checks["record_source_hashes"] = (
        len(source_checks) == record["governing_sources"]["source_count"] == 8
        and all(source_checks)
    )

    model_run = subprocess.run(
        [sys.executable, str(MODEL)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    model_payload = json.loads(model_run.stdout) if model_run.stdout else {}
    model_checks = model_payload.get("checks", [])
    checks["model_pass_24"] = (
        model_run.returncode == 0
        and model_payload.get("all_passed") is True
        and model_payload.get("check_count") == 24
        and model_payload.get("passed_count") == 24
        and model_payload.get("failed_count") == 0
        and len(model_checks) == 24
        and all(item.get("passed") is True for item in model_checks)
    )
    checks["model_payload_bound"] = (
        model_payload.get("payload_sha256")
        == record["exact_controls"]["model_payload_sha256"]
        == controls["model_receipt"]["payload_sha256"]
        == "c518499677b3a256ef0a10dd648261fe0b38fefd1f46013169581ea4633fedc3"
    )
    checks["model_source_bound"] = (
        sha256(MODEL)
        == controls["model_receipt"]["model_sha256"]
        == "4fe902787652f61267b4a28b6cc08889afdf388ba14e9a12ef8a25aff4ab9615"
    )

    provenance_checks = []
    for item in provenance.get("sources", []):
        path = ROOT / item["path"]
        provenance_checks.append(path.is_file() and sha256(path) == item["sha256"])
    checks["provenance_hashes"] = (
        provenance.get("source_count") == len(provenance.get("sources", []))
        and all(provenance_checks)
    )
    checks["provenance_acyclic"] = (
        provenance["acyclic_manifest"]["whole_mutable_registry_hashes_included"]
        is False
        and provenance["acyclic_manifest"]["current_frontier_hash_included"]
        is False
        and provenance["acyclic_manifest"]["task_or_job_terminal_hash_included"]
        is False
        and provenance["acyclic_manifest"]["child_to_child_hash_cycle_present"]
        is False
        and provenance["acyclic_manifest"]["parent_output_self_hash_present"]
        is False
    )
    checks["latex_compile_visual_pass"] = (
        latex_receipt.get("status") == "PASS"
        and latex_receipt.get("page_count") == 4
        and latex_receipt.get("visual_inspection_status") == "PASS"
        and latex_receipt.get("source_sha256") == sha256(TEX)
    )

    tex_text = TEX.read_text(encoding="utf-8")
    fusion_text = FUSION.read_text(encoding="utf-8")
    checks["tex_claim_guards"] = all(
        token in tex_text
        for token in [
            "proposal-only",
            "semantically vacuous",
            "no\\_delta",
            "selected but not executed",
        ]
    )
    checks["fusion_claim_guards"] = all(
        token in fusion_text
        for token in [
            RESULT,
            CANDIDATE,
            SUCCESSOR,
            "no_delta",
            "selected but not executed",
        ]
    )

    whitespace_ok = True
    for path in required + [Path(__file__)]:
        data = path.read_bytes()
        if data and not data.endswith(b"\n"):
            whitespace_ok = False
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if "\t" in text or any(line.endswith(" ") for line in text.splitlines()):
            whitespace_ok = False
    checks["whitespace"] = whitespace_ok

    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_minimal_proposal_only_combined_occurrence_extension_law_validation_v1",
        "status": status,
        "authority": "operational_validation_only",
        "check_count": len(checks),
        "checks": checks,
        "model_payload": model_payload,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = validate()
    if args.write:
        VALIDATION.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        compact = {
            "schema_id": "v22_p4_t02_b2_minimal_proposal_only_combined_occurrence_extension_law_compact_receipt_v1",
            "status": payload["status"],
            "authority": "operational_validation_only",
            "check_count": payload.get("check_count", 0),
            "failed_checks": [
                key for key, value in payload.get("checks", {}).items() if not value
            ],
            "validation_sha256": sha256(VALIDATION),
        }
        COMPACT.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
