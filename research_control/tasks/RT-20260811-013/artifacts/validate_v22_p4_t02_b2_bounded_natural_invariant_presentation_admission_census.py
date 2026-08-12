#!/usr/bin/env python3
"""Focused deterministic validator for the RT013 bounded census."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260811-013"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_validation.json"
COMPACT = ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_compact_receipt.json"
RESULT = "precise_census_typing_obstruction"
OBSTRUCTION = "OB-V22-P4T02-B2-BOUNDED-NATURAL-INVARIANT-PRESENTATION-ADMISSION-CENSUS-TYPING-001"
SUCCESSOR = "PKT-V22-P4T02-B2-POST-BOUNDED-NATURAL-INVARIANT-PRESENTATION-ADMISSION-CENSUS-THEORETICAL-CONTINUATION-SELECTION-V1"


class UniqueLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueLoader, node: yaml.Node, deep: bool = False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def registry_contains(registry: str, key: str) -> bool:
    with (ROOT / "registries" / registry).open(newline="", encoding="utf-8") as handle:
        return any(key in row.values() for row in csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checks = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"check_id": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    required = [
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260811-013.md",
        TASK / "jobs/AJ-RT-20260811-013-001.yaml",
        TASK / "roles/ontology-formalizer@0.2.0--RT-20260811-013.yaml",
        ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_v1.tex",
        ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_record_v1.yaml",
        ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_grammar_receipt_v1.yaml",
        ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_source_provenance_manifest_v1.yaml",
        ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_model.py",
        ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_model_output.json",
        ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_selected_future_packet_v1.yaml",
        ART / "child_phys_math_p4_t02_b2_bounded_natural_invariant_presentation_admission_census.yaml",
        ART / "child_phys_phil_p4_t02_b2_bounded_natural_invariant_presentation_admission_census.yaml",
        ART / "parent_conflict_review_p4_t02_b2_bounded_natural_invariant_presentation_admission_census.yaml",
        ART / "parent_fusion_notes_p4_t02_b2_bounded_natural_invariant_presentation_admission_census.md",
        ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_latex_compile_receipt.json",
    ]
    check("required_files", all(path.is_file() for path in required), ",".join(str(path.relative_to(ROOT)) for path in required if not path.is_file()))

    yaml_paths = [path for path in required if path.suffix == ".yaml"]
    parsed = {}
    yaml_ok = True
    for path in yaml_paths:
        if not path.is_file():
            yaml_ok = False
            continue
        try:
            parsed[path.name] = load_yaml(path)
        except Exception as exc:
            yaml_ok = False
            check(f"yaml_{path.name}", False, str(exc))
    check("unique_key_yaml", yaml_ok)

    record = parsed.get("v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_record_v1.yaml", {})
    grammar = parsed.get("v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_grammar_receipt_v1.yaml", {})
    future = parsed.get("v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_selected_future_packet_v1.yaml", {})
    manifest = parsed.get("v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_source_provenance_manifest_v1.yaml", {})
    conflict = parsed.get("parent_conflict_review_p4_t02_b2_bounded_natural_invariant_presentation_admission_census.yaml", {})
    children = [
        parsed.get("child_phys_math_p4_t02_b2_bounded_natural_invariant_presentation_admission_census.yaml", {}),
        parsed.get("child_phys_phil_p4_t02_b2_bounded_natural_invariant_presentation_admission_census.yaml", {}),
    ]

    decisive = record.get("decisive_result", {}) if isinstance(record, dict) else {}
    check("one_decisive_result", decisive.get("result_type") == RESULT and decisive.get("obstruction_id") == OBSTRUCTION)
    check("no_fog", decisive.get("no_fog_check") == "PASS")

    counts = record.get("enumeration_result", {}) if isinstance(record, dict) else {}
    check("exact_term_counts", [counts.get("src_arena_term_count"), counts.get("nat_term_count"), counts.get("bool_term_count"), counts.get("total_term_count")] == [1, 2, 357, 360])
    check("zero_admission_terms", counts.get("pres_candidate_term_count") == 0 and counts.get("admission_predicate_term_count") == 0)

    obligations = record.get("proof_obligations", []) if isinstance(record, dict) else []
    branches = record.get("failure_branches", []) if isinstance(record, dict) else []
    payloads = record.get("new_mathematical_payload", []) if isinstance(record, dict) else []
    freezes = record.get("preserved_freeze_labels", []) if isinstance(record, dict) else []
    distance = record.get("distance_to_gr_status", []) if isinstance(record, dict) else []
    check("proof_obligations_14", len(obligations) == 14 and len({row.get("obligation_id") for row in obligations}) == 14)
    check("failure_branches_12", len(branches) == 12 and len({row.get("failure_id") for row in branches}) == 12)
    check("new_payloads", len(payloads) >= 1 and all(row.get("summary") for row in payloads))
    check("six_freezes", len(freezes) == 6 and len(set(freezes)) == 6)
    check("distance_14_no_delta", len(distance) == 14 and all(row.get("task_delta") == "no_delta" for row in distance))

    check("grammar_hash", grammar.get("grammar_sha256") == "26dca0ec1771a53d7d11625dde2effb409a84fd44ef3052e1d6380c6b032c42a")
    gcounts = grammar.get("exhaustive_counts", {}).get("height_at_most_two", {}) if isinstance(grammar, dict) else {}
    check("grammar_counts", [gcounts.get("src_arena"), gcounts.get("nat"), gcounts.get("bool"), gcounts.get("all")] == [1, 2, 357, 360])

    model_path = ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_model.py"
    stored_model_path = ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_model_output.json"
    if model_path.is_file() and stored_model_path.is_file():
        live = json.loads(subprocess.check_output([sys.executable, str(model_path)], text=True))
        stored = json.loads(stored_model_path.read_text(encoding="utf-8"))
        check("exact_model_parity", live == stored and live.get("status") == "PASS" and live.get("pass_count") == 12)
    else:
        check("exact_model_parity", False, "model or stored output absent")

    source_hash_ok = True
    sources = manifest.get("sources", []) if isinstance(manifest, dict) else []
    for row in sources:
        path = ROOT / str(row.get("path", ""))
        source_hash_ok = source_hash_ok and path.is_file() and sha256(path) == row.get("sha256")
    check("source_hashes", source_hash_ok and len(sources) == manifest.get("source_count"))

    child_ok = True
    for child in children:
        result = child.get("decisive_result", {}) if isinstance(child, dict) else {}
        child_ok = child_ok and result.get("result_type") == RESULT and result.get("obstruction_id") == OBSTRUCTION
    check("child_consensus", child_ok)
    check("conflict_resolution", conflict.get("unresolved_blocking_conflict_count") == 0 and conflict.get("status") == "PASS")

    packet = future.get("packet", {}) if isinstance(future, dict) else {}
    check("successor_selected_not_executed", packet.get("packet_id") == SUCCESSOR and packet.get("selected_packet_executed") is False and packet.get("next_role_family") == "theoretical-continuation-selector@0.1.0")

    compile_path = ART / "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_latex_compile_receipt.json"
    compile_receipt = json.loads(compile_path.read_text(encoding="utf-8")) if compile_path.is_file() else {}
    check("latex_compile_visual", compile_receipt.get("status") == "PASS" and compile_receipt.get("final_pass_overfull_box_count") == 0 and compile_receipt.get("visual_inspection", {}).get("status") == "PASS")

    check("tex_registered", registry_contains("TEX_SOURCE_REGISTRY.csv", "TEX-V22-P4-T02-B2-BOUNDED-NATURAL-INVARIANT-PRESENTATION-ADMISSION-CENSUS-V1"))
    check("fusion_registered", registry_contains("MARKDOWN_SOURCE_REGISTRY.csv", "MD-V22-P4-T02-B2-PARENT-FUSION-BOUNDED-NATURAL-INVARIANT-PRESENTATION-ADMISSION-CENSUS-V1"))

    limits = record.get("authority_limits", {}) if isinstance(record, dict) else {}
    check("authority_blocks", all(limits.get(key) is False for key in ("source_law_adopted", "canonical_ontology_modified", "meta_grammar_promoted_to_ontology", "phi_src_typed", "distance_to_gr_changed", "global_no_go_claimed", "successor_executed", "physics_promotion_authorized", "proof_authority", "publication_authorized", "push_authorized", "external_action_authorized")))

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    report = {
        "schema_id": "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_validation_v1",
        "task_id": "RT-20260811-013",
        "job_id": "AJ-RT-20260811-013-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(item["status"] == "PASS" for item in checks),
        "checks": checks,
        "authority_note": "Validation is conformance evidence only and creates no scientific promotion or successor authority.",
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_compact_receipt_v1",
        "task_id": "RT-20260811-013",
        "job_id": "AJ-RT-20260811-013-001",
        "status": status,
        "check_count": report["check_count"],
        "pass_count": report["pass_count"],
        "result_type": RESULT,
        "obstruction_id": OBSTRUCTION,
        "term_count": 360,
        "pres_candidate_term_count": 0,
        "distance_to_gr_row_count": 14,
        "distance_to_gr_all_no_delta": True,
        "successor_executed": False,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{status} checks={report['pass_count']}/{report['check_count']}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
