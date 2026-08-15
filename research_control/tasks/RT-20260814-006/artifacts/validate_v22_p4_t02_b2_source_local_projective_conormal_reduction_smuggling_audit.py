#!/usr/bin/env python3
"""Focused validator for the RT006 projective-conormal smuggling audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260814-006"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_validation.json"
COMPACT = ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_compact_receipt.json"


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


def child_verdict(document: dict[str, Any]) -> str:
    for key in (
        "smuggling_audit_result",
        "decisive_result",
        "decisive_audit_result",
        "audit_result",
        "audit_verdict",
    ):
        value = document.get(key, {})
        if isinstance(value, dict):
            result = (
                value.get("result_type")
                or value.get("verdict")
                or value.get("permitted_verdict")
                or value.get("decisive_verdict")
            )
            if isinstance(result, str):
                return result
        elif isinstance(value, str):
            return value
    return str(document.get("verdict", ""))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, str]] = []
    required = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260814-006-001.yaml",
        "role": TASK / "roles/smuggling-auditor@0.2.0--RT-20260814-006.yaml",
        "matrix": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_matrix_v1.yaml",
        "disposition": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_disposition_v1.yaml",
        "model": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_model.py",
        "tex": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_audit_v1.tex",
        "child_math": ART / "child_phys_math_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_audit.yaml",
        "child_phil": ART / "child_phys_phil_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_audit.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_audit.yaml",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_audit.md",
        "provenance": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_provenance_manifest_v1.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260814-006-001.yaml",
        "documentation": TASK / "documentation_impact.yaml",
        "handoff": ROOT / "research_control/handoffs/handoff-1036.yaml",
    }
    for name, path in required.items():
        require(path.is_file(), f"RT006-FILE-{name.upper()}", f"missing {path.relative_to(ROOT)}", findings)

    yaml_names = [
        "task",
        "job",
        "role",
        "matrix",
        "disposition",
        "child_math",
        "child_phil",
        "conflict",
        "provenance",
        "completion",
        "documentation",
        "handoff",
    ]
    docs: dict[str, dict[str, Any]] = {}
    for name in yaml_names:
        path = required[name]
        if path.is_file():
            try:
                docs[name] = load_yaml(path)
            except Exception as exc:
                findings.append({"finding_id": f"RT006-YAML-{name.upper()}", "message": str(exc)})

    if required["model"].is_file():
        proc = subprocess.run(
            [str(ROOT / ".venv/bin/python"), str(required["model"]), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        require(proc.returncode == 0, "RT006-MODEL-EXIT", proc.stderr or "model failed", findings)
        try:
            model = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            model = {}
            findings.append({"finding_id": "RT006-MODEL-JSON", "message": str(exc)})
        require(model.get("status") == "PASS", "RT006-MODEL-STATUS", "model status is not PASS", findings)
        require(model.get("check_count") == 24, "RT006-MODEL-COUNT", "model must run 24 checks", findings)
        require(model.get("pass_count") == 24, "RT006-MODEL-PASS", "model must pass 24 checks", findings)
    else:
        model = {}

    task = docs.get("task", {})
    job = docs.get("job", {})
    matrix = docs.get("matrix", {})
    disposition = docs.get("disposition", {})
    math_child = docs.get("child_math", {})
    phil_child = docs.get("child_phil", {})
    conflict = docs.get("conflict", {})
    completion = docs.get("completion", {})
    handoff = docs.get("handoff", {})

    require(task.get("task_id") == "RT-20260814-006", "RT006-TASK-ID", "task identity mismatch", findings)
    require(job.get("job_id") == "AJ-RT-20260814-006-001", "RT006-JOB-ID", "job identity mismatch", findings)
    require(job.get("packet_id") == "PKT-V22-P4T02-B2-SOURCE-LOCAL-PROJECTIVE-CONORMAL-REDUCTION-SMUGGLING-AUDIT-V1", "RT006-PACKET-ID", "packet identity mismatch", findings)
    require(job.get("role_decomposition", {}).get("mode") == "parent_child_parallel_synthesis", "RT006-DECOMP", "parent-child synthesis missing", findings)
    require(len(job.get("role_decomposition", {}).get("children", [])) == 2, "RT006-CHILD-COUNT", "exactly two children required", findings)
    require(job.get("target_derivation_milestone") == "effective_metric_g_eff", "RT006-MILESTONE", "milestone mismatch", findings)
    require(job.get("route_label") == "ontology-law-research-packet", "RT006-ROUTE", "route mismatch", findings)

    dimensions = matrix.get("audit_dimensions", [])
    require(len(dimensions) == 12, "RT006-DIMENSIONS", "exactly twelve audit dimensions required", findings)
    require(len({row.get("dimension_id") for row in dimensions}) == 12, "RT006-DIMENSION-IDS", "audit dimension IDs must be unique", findings)
    aggregate = matrix.get("aggregate_disposition", {})
    require(aggregate.get("verdict") == "source_pure_as_written", "RT006-MATRIX-VERDICT", "matrix verdict mismatch", findings)
    require(aggregate.get("target_import_detected_in_written_premises") is False, "RT006-MATRIX-TARGET", "target import flag must be false", findings)
    require(aggregate.get("independent_source_provenance_established") is False, "RT006-MATRIX-PROVENANCE", "independent provenance must remain false", findings)

    result = disposition.get("smuggling_audit_result", {})
    require(result.get("result_type") == "source_pure_as_written", "RT006-RESULT", "parent result must be source_pure_as_written", findings)
    require(result.get("no_fog_check") is True, "RT006-NO-FOG", "no-fog check missing", findings)
    require(result.get("conditional_mathematics_preserved") is True, "RT006-MATH-PRESERVE", "conditional mathematics must be preserved", findings)
    require(result.get("independent_source_provenance_passed") is False, "RT006-PROVENANCE", "provenance overread detected", findings)
    require(result.get("p4_t02_acceptance_passed") is False, "RT006-P4-CREDIT", "P4 credit must remain false", findings)
    extension = disposition.get("source_extension_classification", {})
    require(extension.get("category") == "new_ontology_primitive", "RT006-EXT-CATEGORY", "extension category mismatch", findings)
    require(extension.get("controlled_status") == "proposal-only", "RT006-EXT-STATUS", "extension must remain proposal-only", findings)
    require(extension.get("current_ontology_derivation") is False, "RT006-EXT-DERIVATION", "current-ontology derivation must be false", findings)
    require(extension.get("adopted") is False, "RT006-EXT-ADOPTION", "extension adoption must be false", findings)
    require(len(disposition.get("new_mathematical_payload", [])) >= 7, "RT006-PAYLOADS", "at least seven fused payloads required", findings)
    require(len(disposition.get("preserved_freeze_labels", [])) == 7, "RT006-FREEZES", "exactly seven freezes required", findings)
    require(len(disposition.get("distance_to_gr_status", [])) == 14, "RT006-DGR-COUNT", "fourteen Distance-to-GR rows required", findings)
    require(all(row.get("status") == "no_delta" for row in disposition.get("distance_to_gr_status", [])), "RT006-DGR-STATUS", "all Distance-to-GR rows must be no_delta", findings)

    require(child_verdict(math_child) == "source_pure_as_written", "RT006-MATH-RESULT", "math child verdict mismatch", findings)
    require(child_verdict(phil_child) == "source_pure_as_written", "RT006-PHIL-RESULT", "philosophy child verdict mismatch", findings)
    canonical_successor = "PKT-V22-P4T02-B2-SOURCE-LOCAL-PROJECTIVE-CONORMAL-REDUCTION-ROBUSTNESS-NATURAL-SELECTION-REFUTER-STRESS-V1"
    require(math_child.get("selected_successor", {}).get("packet_id") == canonical_successor, "RT006-MATH-SUCCESSOR", "math child successor identity mismatch", findings)
    require(phil_child.get("selected_successor", {}).get("packet_id") == canonical_successor, "RT006-PHIL-SUCCESSOR", "philosophy child successor identity mismatch", findings)
    require(math_child.get("conflict_resolution_revision", {}).get("unresolved_conflict_count") == 0, "RT006-MATH-REVISION", "math child identity conflict remains", findings)
    require(phil_child.get("conflict_resolution_revision", {}).get("unresolved_conflict_count") == 0, "RT006-PHIL-REVISION", "philosophy child identity conflict remains", findings)
    require(conflict.get("unresolved_conflict_count") == 0, "RT006-CONFLICT", "blocking child conflict remains", findings)

    successor = disposition.get("selected_successor", {})
    require(successor.get("packet_id") == canonical_successor, "RT006-SUCCESSOR-ID", "successor identity mismatch", findings)
    require(successor.get("packet_type") == "source_extension_refuter_stress", "RT006-SUCCESSOR-TYPE", "successor type mismatch", findings)
    require(successor.get("role_family") == "refuter@0.2.0", "RT006-SUCCESSOR-ROLE", "successor role mismatch", findings)
    require(successor.get("status") == "selected_not_executed", "RT006-SUCCESSOR-STATUS", "successor must be unexecuted", findings)
    require(successor.get("executed") is False, "RT006-SUCCESSOR-EXEC", "successor execution forbidden", findings)

    limits = disposition.get("authority_limits", {})
    for key in (
        "source_law_adopted",
        "eqsrc_adopted",
        "physical_time_selected",
        "causal_cone_constructed",
        "conformal_geometry_constructed",
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
        require(limits.get(key) is False, f"RT006-LIMIT-{key.upper()}", f"authority limit {key} must be false", findings)

    provenance = docs.get("provenance", {})
    for entry in provenance.get("source_hashes", []):
        rel = entry.get("path", "")
        path = ROOT / rel
        require(path.is_file(), "RT006-PROV-PATH", f"missing provenance source {rel}", findings)
        if path.is_file():
            require(sha256(path) == entry.get("sha256"), "RT006-PROV-HASH", f"hash mismatch {rel}", findings)

    tex_text = required["tex"].read_text(encoding="utf-8") if required["tex"].is_file() else ""
    for token in (
        "source\\_pure\\_as\\_written",
        "Bare-source natural-section obstruction",
        "No equivariant conformal lift",
        "Output-relative naturality",
        "proposal-only",
        "selected\\_not\\_executed",
        "P4--T03 remains locked",
    ):
        require(token in tex_text, "RT006-TEX-TOKEN", f"TeX missing token {token}", findings)

    require(completion.get("job_id") == "AJ-RT-20260814-006-001", "RT006-COMPLETION-ID", "completion identity mismatch", findings)
    require(handoff.get("handoff_id") == "handoff-1036", "RT006-HANDOFF-ID", "handoff identity mismatch", findings)
    require(handoff.get("required_next_packet", {}).get("status") == "selected_not_executed", "RT006-HANDOFF-SUCCESSOR", "handoff successor status mismatch", findings)

    status = "PASS" if not findings else "FAIL"
    checks = 82
    report = {
        "schema_id": "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_validation_v1",
        "task_id": "RT-20260814-006",
        "job_id": "AJ-RT-20260814-006-001",
        "status": status,
        "check_count": checks,
        "finding_count": len(findings),
        "findings": findings,
        "model_status": model.get("status", "missing"),
        "model_check_count": model.get("check_count", 0),
        "model_payload_sha256": model.get("payload_sha256", ""),
        "authority_note": "PASS validates the bounded proposal-only audit transaction and does not adopt source data or promote physics claims.",
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_source_local_projective_conormal_reduction_smuggling_compact_receipt_v1",
        "task_id": "RT-20260814-006",
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
