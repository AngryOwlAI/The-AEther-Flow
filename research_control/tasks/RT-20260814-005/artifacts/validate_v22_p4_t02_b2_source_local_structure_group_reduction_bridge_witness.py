#!/usr/bin/env python3
"""Focused validator for the RT005 source-local reduction bridge packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260814-005"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_source_local_structure_group_reduction_bridge_witness_validation.json"
COMPACT = ART / "v22_p4_t02_b2_source_local_structure_group_reduction_bridge_witness_compact_receipt.json"


class UniqueLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, finding_id: str, message: str, findings: list[dict[str, str]]) -> None:
    if not condition:
        findings.append({"finding_id": finding_id, "message": message})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, str]] = []
    required = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260814-005-001.yaml",
        "role": TASK / "roles/candidate-constructor@0.2.0--RT-20260814-005.yaml",
        "atlas": ART / "v22_p4_t02_b2_source_local_projective_conormal_atlas_v1.yaml",
        "record": ART / "v22_p4_t02_b2_source_local_structure_group_reduction_record_v1.yaml",
        "model": ART / "v22_p4_t02_b2_source_local_structure_group_reduction_bridge_witness_model.py",
        "tex": ART / "v22_p4_t02_b2_source_local_structure_group_reduction_bridge_witness_v1.tex",
        "child_math": ART / "child_phys_math_p4_t02_b2_source_local_structure_group_reduction_bridge_witness.yaml",
        "child_phil": ART / "child_phys_phil_p4_t02_b2_source_local_structure_group_reduction_bridge_witness.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_source_local_structure_group_reduction_bridge_witness.yaml",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_source_local_structure_group_reduction_bridge_witness.md",
        "provenance": ART / "v22_p4_t02_b2_source_local_structure_group_reduction_bridge_witness_provenance_manifest_v1.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260814-005-001.yaml",
        "documentation": TASK / "documentation_impact.yaml",
        "handoff": ROOT / "research_control/handoffs/handoff-1035.yaml",
    }
    for name, path in required.items():
        require(path.is_file(), f"RT005-FILE-{name.upper()}", f"missing {path.relative_to(ROOT)}", findings)

    yaml_names = ["task", "job", "role", "atlas", "record", "child_math", "child_phil", "conflict", "provenance", "completion", "documentation", "handoff"]
    docs: dict[str, dict[str, Any]] = {}
    for name in yaml_names:
        path = required[name]
        if path.is_file():
            try:
                docs[name] = load_yaml(path)
            except Exception as exc:
                findings.append({"finding_id": f"RT005-YAML-{name.upper()}", "message": str(exc)})

    if required["model"].is_file():
        proc = subprocess.run(
            [str(ROOT / ".venv/bin/python"), str(required["model"]), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        require(proc.returncode == 0, "RT005-MODEL-EXIT", proc.stderr or "model failed", findings)
        try:
            model = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            model = {}
            findings.append({"finding_id": "RT005-MODEL-JSON", "message": str(exc)})
        require(model.get("status") == "PASS", "RT005-MODEL-STATUS", "model status is not PASS", findings)
        require(model.get("check_count") == 24, "RT005-MODEL-COUNT", "model must run 24 checks", findings)
        require(model.get("pass_count") == 24, "RT005-MODEL-PASS", "model must pass 24 checks", findings)
    else:
        model = {}

    task = docs.get("task", {})
    job = docs.get("job", {})
    atlas = docs.get("atlas", {})
    record = docs.get("record", {})
    math_child = docs.get("child_math", {})
    phil_child = docs.get("child_phil", {})
    conflict = docs.get("conflict", {})
    completion = docs.get("completion", {})
    handoff = docs.get("handoff", {})

    require(task.get("task_id") == "RT-20260814-005", "RT005-TASK-ID", "task identity mismatch", findings)
    require(job.get("job_id") == "AJ-RT-20260814-005-001", "RT005-JOB-ID", "job identity mismatch", findings)
    require(job.get("packet_id") == "PKT-V22-P4T02-B2-SOURCE-LOCAL-STRUCTURE-GROUP-REDUCTION-BRIDGE-WITNESS-CONSTRUCTION-V1", "RT005-PACKET-ID", "packet identity mismatch", findings)
    require(job.get("role_decomposition", {}).get("mode") == "parent_child_parallel_synthesis", "RT005-DECOMP", "parent-child synthesis missing", findings)
    require(len(job.get("role_decomposition", {}).get("children", [])) == 2, "RT005-CHILD-COUNT", "exactly two children required", findings)
    require(job.get("target_derivation_milestone") == "effective_metric_g_eff", "RT005-MILESTONE", "milestone mismatch", findings)
    require(job.get("route_label") == "ontology-law-research-packet", "RT005-ROUTE", "route mismatch", findings)

    extension = atlas.get("source_extension_classification", {})
    require(extension.get("category") == "new_ontology_primitive", "RT005-EXT-CATEGORY", "extension category mismatch", findings)
    require(extension.get("controlled_status") == "proposal-only", "RT005-EXT-STATUS", "extension must be proposal-only", findings)
    require(extension.get("current_ontology_derivation") is False, "RT005-EXT-DERIVATION", "current-ontology derivation must be false", findings)
    require(extension.get("adopted") is False, "RT005-EXT-ADOPTION", "extension adoption must be false", findings)
    require(len(atlas.get("formal_maps", {})) >= 8, "RT005-MAPS", "at least eight formal maps required", findings)
    require(len(atlas.get("proof_obligations", [])) == 14, "RT005-PO", "exactly fourteen proof obligations required", findings)
    require(len(atlas.get("failure_branches", [])) == 11, "RT005-FB", "exactly eleven failure branches required", findings)

    result = record.get("candidate_constructor_result", {})
    require(result.get("result_type") == "constructed_candidate", "RT005-RESULT", "parent result must be constructed_candidate", findings)
    require(result.get("no_fog_check") is True, "RT005-NO-FOG", "no-fog check missing", findings)
    require(record.get("bridge_attempt_status", {}).get("candidate_map") == "Bridge_PCR", "RT005-BRIDGE-MAP", "Bridge_PCR status missing", findings)
    require(record.get("source_extension_classification", {}).get("category") == "new_ontology_primitive", "RT005-RECORD-EXT", "record extension category mismatch", findings)
    require(len(record.get("proof_obligations", [])) == 14, "RT005-RECORD-PO", "record must preserve fourteen obligations", findings)
    require(len(record.get("failure_branches", [])) == 11, "RT005-RECORD-FB", "record must preserve eleven branches", findings)
    require(len(record.get("preserved_freeze_labels", [])) == 7, "RT005-FREEZES", "exactly seven freezes required", findings)
    require(len(record.get("distance_to_gr_status", [])) == 14, "RT005-DGR-COUNT", "fourteen Distance-to-GR rows required", findings)
    require(all(row.get("status") == "no_delta" for row in record.get("distance_to_gr_status", [])), "RT005-DGR-STATUS", "all Distance-to-GR rows must be no_delta", findings)

    require(math_child.get("candidate_constructor_result", {}).get("result_type") == "constructed_candidate", "RT005-MATH-RESULT", "math child result mismatch", findings)
    require(phil_child.get("candidate_constructor_result", {}).get("result_type") == "constructed_candidate", "RT005-PHIL-RESULT", "philosophy child result mismatch", findings)
    require(conflict.get("unresolved_conflict_count") == 0, "RT005-CONFLICT", "blocking child conflict remains", findings)

    successor = record.get("selected_successor", {})
    require(successor.get("packet_id") == "PKT-V22-P4T02-B2-SOURCE-LOCAL-PROJECTIVE-CONORMAL-REDUCTION-SMUGGLING-AUDIT-V1", "RT005-SUCCESSOR-ID", "successor identity mismatch", findings)
    require(successor.get("packet_type") == "source_extension_smuggling_audit", "RT005-SUCCESSOR-TYPE", "successor type mismatch", findings)
    require(successor.get("role_family") == "smuggling-auditor@0.2.0", "RT005-SUCCESSOR-ROLE", "successor role mismatch", findings)
    require(successor.get("status") == "selected_not_executed", "RT005-SUCCESSOR-STATUS", "successor must be unexecuted", findings)
    require(successor.get("executed") is False, "RT005-SUCCESSOR-EXEC", "successor execution forbidden", findings)

    limits = record.get("authority_limits", {})
    for key in (
        "source_law_adopted",
        "eqsrc_adopted",
        "physical_time_selected",
        "causal_cone_constructed",
        "g_eff_constructed",
        "matter_coupling_derived",
        "einstein_equations_derived",
        "d7_reevaluated",
        "b2_activated",
        "p4_t03_unlocked",
        "distance_to_gr_changed",
        "physics_promotion_authorized",
        "publication_authorized",
        "push_authorized",
        "external_action_authorized",
    ):
        require(limits.get(key) is False, f"RT005-LIMIT-{key.upper()}", f"authority limit {key} must be false", findings)

    provenance = docs.get("provenance", {})
    for entry in provenance.get("source_hashes", []):
        rel = entry.get("path", "")
        path = ROOT / rel
        require(path.is_file(), "RT005-PROV-PATH", f"missing provenance source {rel}", findings)
        if path.is_file():
            require(sha256(path) == entry.get("sha256"), "RT005-PROV-HASH", f"hash mismatch {rel}", findings)

    tex_text = required["tex"].read_text(encoding="utf-8") if required["tex"].is_file() else ""
    for token in (
        "constructed\\_candidate",
        "proposal-only",
        "Nonconstancy and frozen-$\\Kstar$ nonfactorization",
        "source\\_extension\\_smuggling\\_audit",
        "P4--T03 remains locked",
    ):
        require(token in tex_text, "RT005-TEX-TOKEN", f"TeX missing token {token}", findings)

    require(completion.get("job_id") == "AJ-RT-20260814-005-001", "RT005-COMPLETION-ID", "completion identity mismatch", findings)
    require(handoff.get("handoff_id") == "handoff-1035", "RT005-HANDOFF-ID", "handoff identity mismatch", findings)
    require(handoff.get("required_next_packet", {}).get("status") == "selected_not_executed", "RT005-HANDOFF-SUCCESSOR", "handoff successor status mismatch", findings)

    status = "PASS" if not findings else "FAIL"
    checks = 72
    report = {
        "schema_id": "v22_p4_t02_b2_source_local_structure_group_reduction_bridge_witness_validation_v1",
        "task_id": "RT-20260814-005",
        "job_id": "AJ-RT-20260814-005-001",
        "status": status,
        "check_count": checks,
        "finding_count": len(findings),
        "findings": findings,
        "model_status": model.get("status", "missing"),
        "model_check_count": model.get("check_count", 0),
        "model_payload_sha256": model.get("payload_sha256", ""),
        "authority_note": "PASS validates the bounded proposal-only construction transaction and does not adopt source data or promote physics claims.",
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_source_local_structure_group_reduction_bridge_witness_compact_receipt_v1",
        "task_id": "RT-20260814-005",
        "status": status,
        "check_count": checks,
        "finding_count": len(findings),
        "result_type": result.get("result_type", "missing"),
        "model_pass_count": model.get("pass_count", 0),
        "unresolved_conflict_count": conflict.get("unresolved_conflict_count", -1),
        "successor_status": successor.get("status", "missing"),
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
