#!/usr/bin/env python3
"""Focused deterministic validator for RT-20260814-002."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260814-002"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_validation.json"
COMPACT = ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_compact_receipt.json"


class UniqueLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise TypeError(f"{path} did not parse as a mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_model() -> dict[str, Any]:
    path = ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_model.py"
    spec = importlib.util.spec_from_file_location("rt002_audit_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("model import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run()


def check_text_whitespace(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return text.endswith("\n") and "\t" not in text and all(
        line == line.rstrip() for line in text.splitlines()
    )


def run() -> dict[str, Any]:
    required = [
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260814-002.md",
        TASK / "roles/ontology-formalizer@0.2.0--RT-20260814-002.yaml",
        TASK / "jobs/AJ-RT-20260814-002-001.yaml",
        ART / "child_phys_math_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit.yaml",
        ART / "child_phys_phil_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit.yaml",
        ART / "parent_conflict_review_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit.yaml",
        ART / "parent_fusion_notes_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit.md",
        ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_v1.tex",
        ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_record_v1.yaml",
        ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_controls_v1.yaml",
        ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_provenance_manifest_v1.yaml",
        ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_model.py",
        ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_latex_compile_receipt.json",
        TASK / "documentation_impact.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260814-002-001.yaml",
        ROOT / "research_control/handoffs/handoff-1032.yaml",
        ROOT / "research_control/handoffs/handoff-1032.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]

    record = load_yaml(ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_record_v1.yaml")
    controls = load_yaml(ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_controls_v1.yaml")
    manifest = load_yaml(ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_provenance_manifest_v1.yaml")
    model = load_model()
    tex = (ART / "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_v1.tex").read_text(encoding="utf-8")

    source_mismatches: list[dict[str, str]] = []
    for row in manifest.get("sources", []):
        path = ROOT / row["path"]
        actual = sha256(path) if path.exists() else "missing"
        if actual != row["sha256"]:
            source_mismatches.append({"path": row["path"], "expected": row["sha256"], "actual": actual})
    artifact_mismatches: list[dict[str, str]] = []
    for row in manifest.get("task_artifacts", []):
        path = ROOT / row["path"]
        actual = sha256(path) if path.exists() else "missing"
        if actual != row["sha256"]:
            artifact_mismatches.append({"path": row["path"], "expected": row["sha256"], "actual": actual})

    children: list[dict[str, Any]] = []
    for name in ("math", "phil"):
        path = ART / f"child_phys_{name}_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit.yaml"
        children.append(load_yaml(path))
    conflict = load_yaml(ART / "parent_conflict_review_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit.yaml")
    completion = load_yaml(TASK / "jobs/completions/AJC-AJ-RT-20260814-002-001.yaml")
    handoff = load_yaml(ROOT / "research_control/handoffs/handoff-1032.yaml")

    checks = {
        "required_paths": not missing,
        "model_pass": model.get("passed") is True and model.get("passed_count") == 20,
        "model_result": model.get("result_type") == "current_source_equivariant_asymmetry_derivation_theorem",
        "record_result": record.get("result_type") == "current_source_equivariant_asymmetry_derivation_theorem" and record.get("result_count") == 1,
        "theorem_identity": record.get("theorem_id") == "THM-V22-P4T02-B2-CURRENT-SOURCE-KSTAR-ARROW-SUBCLASS-001",
        "candidate_count": len(record.get("candidate_audit", [])) == 6,
        "exactly_one_positive_candidate": sum(row.get("status") == "positive_theorem" for row in record.get("candidate_audit", [])) == 1,
        "proof_obligation_count": len(record.get("proof_obligations", [])) == 14,
        "failure_branch_count": len(record.get("failure_branches", [])) == 12,
        "freeze_count": len(record.get("preserved_freeze_labels", [])) == 6 and len(set(record.get("preserved_freeze_labels", []))) == 6,
        "distance_count": len(record.get("distance_to_gr_status", [])) == 14,
        "distance_no_delta": all(row.get("status") == "no_delta" for row in record.get("distance_to_gr_status", [])),
        "new_payload_count": len(record.get("new_mathematical_payload", [])) >= 1,
        "successor_unexecuted": record.get("selected_successor", {}).get("status") == "selected_not_executed",
        "route_c_not_preselected": record.get("selected_successor", {}).get("route_c_preselected") is False,
        "controls_result": controls.get("result_type") == record.get("result_type"),
        "controls_candidate_count": controls.get("candidate_grammar", {}).get("exact_count") == 6,
        "controls_positive_count": controls.get("candidate_grammar", {}).get("positive_candidate_count") == 1,
        "children_converged": all(
            (child.get("result_type") or child.get("decisive_result", {}).get("result_type"))
            == record.get("result_type")
            for child in children
        ),
        "conflict_resolved": conflict.get("unresolved_blocking_conflict_count") == 0,
        "completion_result": completion.get("decisive_result", {}).get("result_type") == record.get("result_type"),
        "handoff_result": handoff.get("claim_boundary", {}).get("decisive_result") == record.get("result_type"),
        "source_hashes": not source_mismatches,
        "artifact_hashes": not artifact_mismatches,
        "manifest_count": manifest.get("source_count") == len(manifest.get("sources", [])),
        "tex_theorem": "Objectwise-proper compact-support arrow subgroupoid" in tex and "current\\_source\\_equivariant\\_asymmetry\\_derivation\\_theorem" in tex,
        "tex_boundaries": all(phrase in tex for phrase in ("not adopted", "P4--T03 remains locked", "not preselected")),
        "whitespace": all(check_text_whitespace(path) for path in required if path.exists() and path.suffix in {".yaml", ".md", ".tex", ".py"}),
    }
    return {
        "schema_id": "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_validation_v1",
        "task_id": "RT-20260814-002",
        "job_id": "AJ-RT-20260814-002-001",
        "result_type": record.get("result_type"),
        "checks": checks,
        "check_count": len(checks),
        "passed_count": sum(checks.values()),
        "passed": all(checks.values()),
        "missing_paths": missing,
        "source_mismatches": source_mismatches,
        "artifact_mismatches": artifact_mismatches,
        "model_receipt": {"passed_count": model.get("passed_count"), "check_count": model.get("check_count")},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = run()
    if args.write_report:
        REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_compact_receipt_v1",
            "task_id": payload["task_id"],
            "job_id": payload["job_id"],
            "result_type": payload["result_type"],
            "passed": payload["passed"],
            "passed_count": payload["passed_count"],
            "check_count": payload["check_count"],
            "model_receipt": payload["model_receipt"],
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"{payload['passed_count']}/{payload['check_count']} checks pass")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
