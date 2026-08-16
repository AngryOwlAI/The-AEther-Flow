#!/usr/bin/env python3
"""Focused validation for RT-20260816-001."""

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
ART = ROOT / "research_control/tasks/RT-20260816-001/artifacts"
RECORD = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_record_v1.yaml"
CONTROLS = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_controls_v1.yaml"
MODEL = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_model.py"
TEX = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_extension_v1.tex"
CHILD_MATH = ART / "child_phys_math_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law.yaml"
CHILD_PHIL = ART / "child_phys_phil_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law.yaml"
CONFLICT = ART / "parent_conflict_review_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law.yaml"
FUSION = ART / "parent_fusion_notes_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law.md"
PROVENANCE = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_provenance_manifest_v1.yaml"
LATEX_RECEIPT = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_latex_compile_receipt.json"
VALIDATION = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_validation.json"
COMPACT = ART / "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_compact_receipt.json"

RESULT = "proposal_only_measurable_fiber_occurrence_law_constructed_pending_smuggling_audit"
SUCCESSOR = "PKT-V22-P4T02-B2-PROPOSAL-ONLY-MEASURABLE-FIBER-OCCURRENCE-LAW-SOURCE-EXTENSION-SMUGGLING-AUDIT-V1"


class UniqueLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


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
    required = [RECORD, CONTROLS, MODEL, TEX, CHILD_MATH, CHILD_PHIL, CONFLICT, FUSION, PROVENANCE, LATEX_RECEIPT]
    checks["required_files"] = all(path.is_file() for path in required)
    if not checks["required_files"]:
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        return {"status": "FAIL", "checks": checks, "missing": missing}

    record = load_yaml(RECORD)
    controls = load_yaml(CONTROLS)
    child_math = load_yaml(CHILD_MATH)
    child_phil = load_yaml(CHILD_PHIL)
    conflict = load_yaml(CONFLICT)
    provenance = load_yaml(PROVENANCE)
    latex_receipt = json.loads(LATEX_RECEIPT.read_text(encoding="utf-8"))

    checks["exclusive_result"] = record.get("result_type") == RESULT and record.get("result_count") == 1
    checks["roots_6"] = record["proposal_roots"]["root_count"] == len(record["proposal_roots"]["items"]) == 6
    checks["domains_10"] = record["formal_domains"]["domain_count"] == len(record["formal_domains"]["items"]) == 10
    checks["objects_11"] = record["formal_objects"]["object_count"] == len(record["formal_objects"]["items"]) == 11
    checks["maps_10"] = record["formal_maps"]["map_count"] == len(record["formal_maps"]["items"]) == 10
    checks["theorems_6"] = record["theorem_targets"]["theorem_count"] == len(record["theorem_targets"]["items"]) == 6
    checks["obligations_16"] = record["proof_obligations"]["obligation_count"] == len(record["proof_obligations"]["items"]) == 16
    checks["obligations_discharged"] = all(item.get("status") == "discharged" for item in record["proof_obligations"]["items"])
    checks["branches_15"] = record["failure_branches"]["branch_count"] == len(record["failure_branches"]["items"]) == 15
    checks["branches_not_triggered"] = record["failure_branches"]["triggered_count"] == 0 and all(item.get("status") == "not_triggered" for item in record["failure_branches"]["items"])
    checks["controls_6"] = controls.get("control_count") == len(controls.get("controls", [])) == 6 and all(item.get("passed") is True for item in controls["controls"])
    checks["freezes_8"] = record["freeze_status"]["freeze_count"] == len(set(record["freeze_status"]["labels"])) == 8 and record["freeze_status"]["all_preserved"] is True
    rows = record["distance_to_gr_status"]["rows"]
    checks["distance_14_no_delta"] = record["distance_to_gr_status"]["row_count"] == len(rows) == 14 and record["distance_to_gr_status"]["literal_no_delta_row_count"] == 14 and all(row.get("status") == "no_delta" for row in rows)
    checks["descent_scope_guard"] = record["descent_scope"]["section_sheaf_descent"] is True and record["descent_scope"]["arbitrary_local_probability_coupling_descent"] is False
    checks["successor_exact_unexecuted"] = record["selected_successor"]["packet_id"] == SUCCESSOR and record["selected_successor"]["status"] == "selected_not_executed" and record["selected_successor"]["executed"] is False
    checks["downstream_locks"] = all(value is False for value in record["downstream_locks"].values())
    checks["children_converge"] = RESULT in scalar_values(child_math) and RESULT in scalar_values(child_phil) and SUCCESSOR in scalar_values(child_math) and SUCCESSOR in scalar_values(child_phil)
    checks["conflict_resolved"] = conflict.get("unresolved_conflict_count") == 0 and conflict.get("canonical_successor_packet_id") == SUCCESSOR

    source_checks = []
    for item in record["governing_sources"]["items"]:
        source_checks.append(sha256(ROOT / item["path"]) == item["sha256"])
    checks["record_source_hashes"] = len(source_checks) == record["governing_sources"]["source_count"] == 6 and all(source_checks)

    model_run = subprocess.run([sys.executable, str(MODEL)], cwd=ROOT, text=True, capture_output=True, check=False)
    model_payload = json.loads(model_run.stdout) if model_run.stdout else {}
    checks["model_pass_19"] = model_run.returncode == 0 and model_payload.get("status") == "PASS" and model_payload.get("check_count") == 19 and all(model_payload.get("checks", {}).values())
    checks["model_payload_bound"] = model_payload.get("payload_sha256") == record["exact_controls"]["exact_model_payload_sha256"] == controls["model_receipt"]["payload_sha256"]

    provenance_checks = []
    for item in provenance.get("sources", []):
        path = ROOT / item["path"]
        provenance_checks.append(path.is_file() and sha256(path) == item["sha256"])
    checks["provenance_hashes"] = provenance.get("source_count") == len(provenance.get("sources", [])) and all(provenance_checks)
    checks["latex_compile_visual_pass"] = latex_receipt.get("status") == "PASS" and latex_receipt.get("page_count") in {3, 4} and latex_receipt.get("visual_inspection_status") == "PASS"

    tex_text = TEX.read_text(encoding="utf-8")
    fusion_text = FUSION.read_text(encoding="utf-8")
    checks["tex_claim_guards"] = all(token in tex_text for token in ["proposal-only", "current ontology", "physical probability", "no\\_delta"])
    checks["fusion_claim_guards"] = all(token in fusion_text for token in [RESULT, SUCCESSOR, "no_delta", "not executed"])

    whitespace_paths = required + [VALIDATION, COMPACT]
    whitespace_ok = True
    for path in whitespace_paths:
        if not path.exists() or path.suffix == ".pdf":
            continue
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
        "schema_id": "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_validation_v1",
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
        VALIDATION.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_compact_receipt_v1",
            "status": payload["status"],
            "authority": "operational_validation_only",
            "check_count": payload.get("check_count", 0),
            "failed_checks": [key for key, value in payload.get("checks", {}).items() if not value],
            "validation_sha256": sha256(VALIDATION),
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
