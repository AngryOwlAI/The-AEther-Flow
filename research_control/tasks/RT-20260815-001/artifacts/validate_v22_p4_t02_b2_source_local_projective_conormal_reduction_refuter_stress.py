#!/usr/bin/env python3
"""Focused validator for the RT001 projective-conormal Refuter stress."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260815-001"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_validation.json"
COMPACT = ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_compact_receipt.json"
PACKET = "PKT-V22-P4T02-B2-SOURCE-LOCAL-PROJECTIVE-CONORMAL-REDUCTION-ROBUSTNESS-NATURAL-SELECTION-REFUTER-STRESS-V1"
OBSTRUCTION = "OB-V22-P4T02-B2-PROJECTIVE-CONORMAL-ROBUST-SELECTION-CONFORMAL-LIFT-001"
FREEZE = "NDCL-V22-P4T02-B2-PROJECTIVE-CONORMAL-ROBUST-SELECTION-CONFORMAL-LIFT"
SUCCESSOR = "PKT-V22-P4T02-B2-POST-PROJECTIVE-CONORMAL-REFUTER-THEORETICAL-CONTINUATION-SELECTION-V1"


class UniqueLoader(yaml.SafeLoader):
    pass


def construct_mapping(
    loader: UniqueLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError(f"top-level YAML object is not a mapping: {path}")
    return value


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(
    condition: bool,
    finding_id: str,
    message: str,
    findings: list[dict[str, str]],
) -> None:
    if not condition:
        findings.append({"finding_id": finding_id, "message": message})


def nested(document: dict[str, Any], *keys: str) -> Any:
    value: Any = document
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def child_result(document: dict[str, Any]) -> str:
    for path in (
        ("decisive_refuter_result", "result_class"),
        ("refuter_result", "result_class"),
        ("refuter_result", "selected_class"),
    ):
        value = nested(document, *path)
        if isinstance(value, str):
            return value
    return ""


def child_obstruction(document: dict[str, Any]) -> str:
    for path in (
        ("decisive_refuter_result", "obstruction_id"),
        ("refuter_result", "obstruction_id"),
        ("refuter_obstruction_record", "obstruction_id"),
    ):
        value = nested(document, *path)
        if isinstance(value, str):
            return value
    return ""


def child_successor(document: dict[str, Any]) -> dict[str, Any]:
    for key in ("selected_successor", "successor_selection"):
        value = document.get(key)
        if isinstance(value, dict):
            return value
    return {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, str]] = []
    required = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260815-001-001.yaml",
        "role": TASK / "roles/refuter@0.2.0--RT-20260815-001.yaml",
        "matrix": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_matrix_v1.yaml",
        "disposition": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_disposition_v1.yaml",
        "model": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_model.py",
        "tex": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_v1.tex",
        "child_math": ART / "child_phys_math_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress.yaml",
        "child_phil": ART / "child_phys_phil_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress.yaml",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress.md",
        "provenance": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_provenance_manifest_v1.yaml",
        "latex": ART / "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_latex_compile_receipt.json",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260815-001-001.yaml",
        "documentation": TASK / "documentation_impact.yaml",
        "handoff": ROOT / "research_control/handoffs/handoff-1037.yaml",
    }
    for name, path in required.items():
        require(
            path.is_file(),
            f"RT001-FILE-{name.upper()}",
            f"missing {path.relative_to(ROOT)}",
            findings,
        )

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
                findings.append(
                    {"finding_id": f"RT001-YAML-{name.upper()}", "message": str(exc)}
                )

    model: dict[str, Any] = {}
    if required["model"].is_file():
        process = subprocess.run(
            [str(ROOT / ".venv/bin/python"), str(required["model"]), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        require(
            process.returncode == 0,
            "RT001-MODEL-EXIT",
            process.stderr or "model failed",
            findings,
        )
        try:
            model = json.loads(process.stdout)
        except json.JSONDecodeError as exc:
            findings.append({"finding_id": "RT001-MODEL-JSON", "message": str(exc)})
        require(model.get("status") == "PASS", "RT001-MODEL-STATUS", "model status is not PASS", findings)
        require(model.get("check_count") == 34, "RT001-MODEL-COUNT", "model must run 34 checks", findings)
        require(model.get("pass_count") == 34, "RT001-MODEL-PASS", "model must pass 34 checks", findings)

    task = docs.get("task", {})
    job = docs.get("job", {})
    matrix = docs.get("matrix", {})
    disposition = docs.get("disposition", {})
    math_child = docs.get("child_math", {})
    phil_child = docs.get("child_phil", {})
    conflict = docs.get("conflict", {})
    completion = docs.get("completion", {})
    handoff = docs.get("handoff", {})

    require(task.get("task_id") == "RT-20260815-001", "RT001-TASK-ID", "task identity mismatch", findings)
    require(job.get("job_id") == "AJ-RT-20260815-001-001", "RT001-JOB-ID", "job identity mismatch", findings)
    require(job.get("packet_id") == PACKET, "RT001-PACKET-ID", "packet identity mismatch", findings)
    require(job.get("role_decomposition", {}).get("mode") == "parent_child_parallel_synthesis", "RT001-DECOMP", "parent-child synthesis missing", findings)
    require(len(job.get("role_decomposition", {}).get("children", [])) == 2, "RT001-CHILD-COUNT", "exactly two children required", findings)
    require(job.get("target_derivation_milestone") == "effective_metric_g_eff", "RT001-MILESTONE", "milestone mismatch", findings)
    require(job.get("route_label") == "ontology-law-research-packet", "RT001-ROUTE", "route mismatch", findings)

    branches = matrix.get("stress_branches", [])
    require(len(branches) == 10, "RT001-BRANCHES", "exactly ten stress branches required", findings)
    require(len({row.get("branch_id") for row in branches}) == 10, "RT001-BRANCH-IDS", "stress branch IDs must be unique", findings)
    require(nested(matrix, "refuter_result", "selected_class") == "scoped_obstruction", "RT001-MATRIX-RESULT", "matrix result mismatch", findings)
    require(nested(matrix, "refuter_obstruction_record", "obstruction_id") == OBSTRUCTION, "RT001-MATRIX-OBSTRUCTION", "matrix obstruction mismatch", findings)
    require(nested(matrix, "freeze_criteria_status", "active_freeze_label") == FREEZE, "RT001-MATRIX-FREEZE", "matrix freeze mismatch", findings)
    require(len(matrix.get("preserved_freezes", [])) == 7, "RT001-MATRIX-INHERITED-FREEZES", "matrix must preserve seven freezes", findings)
    require(nested(matrix, "new_candidate_local_freeze", "freeze_id") == FREEZE, "RT001-MATRIX-NEW-FREEZE", "matrix new freeze mismatch", findings)
    require(len(matrix.get("distance_to_gr_status", [])) == 14, "RT001-MATRIX-DGR", "matrix needs fourteen Distance-to-GR rows", findings)
    require(all(row.get("task_delta") == "no_delta" for row in matrix.get("distance_to_gr_status", [])), "RT001-MATRIX-DGR-DELTA", "matrix Distance-to-GR rows must all be no_delta", findings)
    require(len(matrix.get("new_mathematical_payload", [])) >= 6, "RT001-MATRIX-PAYLOAD", "matrix needs at least six payloads", findings)

    result = disposition.get("refuter_stress_result", {})
    require(result.get("result_type") == "scoped_obstruction", "RT001-DISPOSITION-RESULT", "disposition result mismatch", findings)
    require(result.get("no_fog_check") is True, "RT001-NO-FOG", "no-fog check missing", findings)
    require(result.get("conditional_mathematics_preserved") is True, "RT001-MATH-PRESERVE", "conditional mathematics must be preserved", findings)
    require(result.get("rt006_source_pure_as_written_preserved") is True, "RT001-AUDIT-PRESERVE", "RT006 verdict must be preserved", findings)
    require(nested(disposition, "refuter_obstruction_record", "obstruction_id") == OBSTRUCTION, "RT001-DISPOSITION-OBSTRUCTION", "disposition obstruction mismatch", findings)
    require(nested(disposition, "freeze_criteria_status", "active_freeze_label") == FREEZE, "RT001-DISPOSITION-FREEZE", "disposition freeze mismatch", findings)
    require(len(disposition.get("preserved_freeze_labels", [])) == 7, "RT001-DISPOSITION-INHERITED", "disposition must preserve seven freezes", findings)
    require(len(disposition.get("active_freeze_labels", [])) == 8, "RT001-DISPOSITION-ACTIVE", "disposition must record eight active freezes", findings)
    require(len(disposition.get("distance_to_gr_status", [])) == 14, "RT001-DISPOSITION-DGR", "disposition needs fourteen Distance-to-GR rows", findings)
    require(all(row.get("task_delta") == "no_delta" for row in disposition.get("distance_to_gr_status", [])), "RT001-DISPOSITION-DGR-DELTA", "disposition Distance-to-GR rows must all be no_delta", findings)
    require(len(disposition.get("new_mathematical_payload", [])) >= 6, "RT001-DISPOSITION-PAYLOAD", "disposition needs at least six payloads", findings)

    extension = disposition.get("source_extension_classification", {})
    require(extension.get("category") == "new_ontology_primitive", "RT001-EXT-CATEGORY", "extension category mismatch", findings)
    require(extension.get("controlled_status") == "proposal-only", "RT001-EXT-STATUS", "extension must remain proposal-only", findings)
    require(extension.get("current_ontology_derivation") is False, "RT001-EXT-DERIVATION", "current-ontology derivation must be false", findings)
    require(extension.get("adopted") is False, "RT001-EXT-ADOPTION", "extension adoption must be false", findings)

    for name, child in (("MATH", math_child), ("PHIL", phil_child)):
        require(child_result(child) == "scoped_obstruction", f"RT001-{name}-RESULT", f"{name.lower()} child result mismatch", findings)
        require(child_obstruction(child) == OBSTRUCTION, f"RT001-{name}-OBSTRUCTION", f"{name.lower()} child obstruction mismatch", findings)
        successor = child_successor(child)
        require(successor.get("packet_id") == SUCCESSOR, f"RT001-{name}-SUCCESSOR", f"{name.lower()} child successor mismatch", findings)
        require(successor.get("status") == "selected_not_executed" or successor.get("execution_status") == "selected_not_executed", f"RT001-{name}-SUCCESSOR-STATUS", f"{name.lower()} child successor must be unexecuted", findings)

    require(conflict.get("unresolved_conflict_count") == 0 or nested(conflict, "conflict_resolution", "unresolved_conflict_count") == 0, "RT001-CONFLICT", "blocking child conflict remains", findings)
    require(nested(conflict, "parent_decision", "result_class") == "scoped_obstruction", "RT001-PARENT-RESULT", "parent conflict review result mismatch", findings)

    successor = disposition.get("selected_successor", {})
    require(successor.get("packet_id") == SUCCESSOR, "RT001-SUCCESSOR-ID", "successor identity mismatch", findings)
    require(successor.get("packet_type") == "theoretical_continuation_selector", "RT001-SUCCESSOR-TYPE", "successor type mismatch", findings)
    require(successor.get("role_family") == "theoretical-continuation-selector@0.1.0", "RT001-SUCCESSOR-ROLE", "successor role mismatch", findings)
    require(successor.get("status") == "selected_not_executed", "RT001-SUCCESSOR-STATUS", "successor must be unexecuted", findings)
    require(successor.get("executed") is False, "RT001-SUCCESSOR-EXEC", "successor execution forbidden", findings)

    limits = disposition.get("authority_limits", {})
    for key in (
        "source_law_adopted",
        "canonical_ontology_modified",
        "successor_executed",
        "adequacy_reevaluated",
        "d7_reevaluated",
        "b2_activated_or_disposed",
        "p4_t03_unlocked",
        "physical_time_selected",
        "physical_causality_constructed",
        "empirical_response_constructed",
        "conformal_geometry_constructed",
        "effective_metric_constructed",
        "matter_coupling_derived",
        "einstein_equations_derived",
        "distance_to_gr_changed",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
        "external_action_authorized",
    ):
        require(limits.get(key) is False, f"RT001-LIMIT-{key.upper()}", f"authority limit {key} must be false", findings)

    provenance = docs.get("provenance", {})
    for entry in provenance.get("source_hashes", []):
        relative = entry.get("path", "")
        path = ROOT / relative
        require(path.is_file(), "RT001-PROV-PATH", f"missing provenance source {relative}", findings)
        if path.is_file():
            require(sha256(path) == entry.get("sha256"), "RT001-PROV-HASH", f"hash mismatch {relative}", findings)

    tex_text = required["tex"].read_text(encoding="utf-8") if required["tex"].is_file() else ""
    for token in (
        "scoped\\_obstruction",
        "Quantitative non-Frobenius perturbation",
        "Constant-line proposal-orbit collapse",
        "Index-two coorientation debt",
        "Equivariant lift obstruction and completion family",
        "selected\\_not\\_executed",
        "P4--T03 remains locked",
    ):
        require(token in tex_text, "RT001-TEX-TOKEN", f"TeX missing token {token}", findings)

    if required["latex"].is_file():
        latex = json.loads(required["latex"].read_text(encoding="utf-8"))
        require(latex.get("status") == "PASS", "RT001-LATEX-STATUS", "LaTeX receipt is not PASS", findings)
        require(latex.get("source_sha256") == sha256(required["tex"]), "RT001-LATEX-HASH", "LaTeX source hash mismatch", findings)
        require(latex.get("page_count") == 4, "RT001-LATEX-PAGES", "LaTeX must render four pages", findings)
        require(latex.get("visual_inspection_status") == "PASS", "RT001-LATEX-VISUAL", "visual inspection must pass", findings)

    require(completion.get("job_id") == "AJ-RT-20260815-001-001", "RT001-COMPLETION-ID", "completion identity mismatch", findings)
    require(nested(completion, "refuter_obstruction_record", "obstruction_id") == OBSTRUCTION, "RT001-COMPLETION-OBSTRUCTION", "completion obstruction mismatch", findings)
    require(handoff.get("handoff_id") == "handoff-1037", "RT001-HANDOFF-ID", "handoff identity mismatch", findings)
    require(nested(handoff, "required_next_packet", "status") == "selected_not_executed", "RT001-HANDOFF-SUCCESSOR", "handoff successor status mismatch", findings)

    status = "PASS" if not findings else "FAIL"
    report = {
        "schema_id": "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_validation_v1",
        "task_id": "RT-20260815-001",
        "job_id": "AJ-RT-20260815-001-001",
        "status": status,
        "check_count": 104,
        "finding_count": len(findings),
        "findings": findings,
        "result_class": result.get("result_type", "missing"),
        "obstruction_id": nested(disposition, "refuter_obstruction_record", "obstruction_id") or "missing",
        "active_freeze_count": len(disposition.get("active_freeze_labels", [])),
        "model_status": model.get("status", "missing"),
        "model_check_count": model.get("check_count", 0),
        "model_payload_sha256": model.get("payload_sha256", ""),
        "unresolved_conflict_count": nested(conflict, "conflict_resolution", "unresolved_conflict_count"),
        "successor_status": successor.get("status", "missing"),
        "authority_note": "PASS validates the bounded proposal-only Refuter transaction and does not adopt source data, establish physical geometry, or promote physics claims.",
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_source_local_projective_conormal_reduction_refuter_stress_compact_receipt_v1",
        "task_id": "RT-20260815-001",
        "status": status,
        "check_count": 104,
        "finding_count": len(findings),
        "result_class": result.get("result_type", "missing"),
        "obstruction_id": nested(disposition, "refuter_obstruction_record", "obstruction_id") or "missing",
        "model_pass_count": model.get("pass_count", 0),
        "active_freeze_count": len(disposition.get("active_freeze_labels", [])),
        "unresolved_conflict_count": nested(conflict, "conflict_resolution", "unresolved_conflict_count"),
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
