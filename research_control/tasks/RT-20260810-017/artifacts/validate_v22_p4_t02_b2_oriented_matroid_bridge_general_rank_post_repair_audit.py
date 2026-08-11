#!/usr/bin/env python3
"""Focused validator for the RT017 general-rank post-repair audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260810-017"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_audit_validation.json"
COMPACT = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_audit_compact_receipt.json"
MODEL = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_audit_model.py"

EXPECTED_SOURCES = {
    "research_control/handoffs/handoff-1013.yaml": "27aeaea9eb26c141ba57c6f2d292aedb7742db43eccce55017226489e74a7a4d",
    "research_control/tasks/RT-20260810-016/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_v1.tex": "c977c9a93e3a543fe18378f51b83773211b483df3377d4187c506ff88768bba4",
    "research_control/tasks/RT-20260810-016/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_record_v1.yaml": "117a330c085dcbb384e5e4e236642ea0a65b3afbb151dbb2e978ffe2f931a035",
    "research_control/tasks/RT-20260810-016/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_general_rank_controls_v1.yaml": "1ddcedd031a1eb6688e897cde0be52bc9ae61c134f4d4a5decb2aefdd49fb5f5",
    "research_control/tasks/RT-20260810-016/artifacts/parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge_general_rank_repair.md": "c2ebffd9434cc104ac303a22c1e98a1c12b02441c826b488bd40cad7789a8061",
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
}

STRICT_YAML_PATHS = [
    TASK / "00_TASK.yaml",
    TASK / "jobs/AJ-RT-20260810-017-001.yaml",
    TASK / "roles/smuggling-auditor@0.2.0--RT-20260810-017.yaml",
    ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_matrix_v1.yaml",
    ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_disposition_v1.yaml",
    ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_audit_provenance_manifest_v1.yaml",
    ART / "child_phys_math_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit.yaml",
    ART / "child_phys_phil_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit.yaml",
    ART / "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit.yaml",
    TASK / "jobs/completions/AJC-AJ-RT-20260810-017-001.yaml",
    ROOT / "research_control/handoffs/handoff-1014.yaml",
]


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping)


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_model() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("rt017_audit_model", MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("model import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit()


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    parsed: dict[str, Any] = {}
    for path in STRICT_YAML_PATHS:
        exists = path.is_file()
        add(checks, f"exists:{path.relative_to(ROOT)}", exists, "required strict-YAML artifact")
        if exists:
            try:
                parsed[str(path)] = load_yaml(path)
                add(checks, f"yaml:{path.relative_to(ROOT)}", True, "unique-key YAML parse")
            except Exception as exc:  # noqa: BLE001
                add(checks, f"yaml:{path.relative_to(ROOT)}", False, str(exc))

    for rel, expected in EXPECTED_SOURCES.items():
        path = ROOT / rel
        actual = sha256(path) if path.is_file() else "missing"
        add(checks, f"source_hash:{rel}", actual == expected, f"expected={expected} actual={actual}")

    tex_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit_v1.tex"
    fusion_path = ART / "parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit.md"
    latex_receipt = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_audit_latex_compile_receipt.json"
    for path in (tex_path, fusion_path, latex_receipt):
        add(checks, f"exists:{path.relative_to(ROOT)}", path.is_file(), "required role output or render receipt")

    if tex_path.is_file():
        tex = tex_path.read_text(encoding="utf-8")
        required_tokens = [
            "source\\_pure\\_as\\_written",
            "Effective-span target-dimension nonselection",
            "Finite-fixture cap nonidentifiability",
            "nonphysical conformance",
            "5072 covectors",
            "376 topes",
            "Distance-to-GR matrix",
            "GENERAL-RANK-REFUTER-STRESS-V1",
        ]
        for token in required_tokens:
            add(checks, f"tex_token:{token}", token in tex, "focused audit token")

    matrix_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_matrix_v1.yaml"
    if matrix_path.is_file():
        matrix = parsed.get(str(matrix_path), load_yaml(matrix_path))
        add(checks, "matrix_verdict", matrix.get("decisive_verdict") == "source_pure_as_written", "one allowed verdict")
        dims = matrix.get("focused_audit_dimensions", [])
        add(checks, "matrix_dimensions", len(dims) == 12 and len({row.get("dimension_id") for row in dims}) == 12, "12 unique focused dimensions")
        burdens = matrix.get("distance_to_gr_status", [])
        add(checks, "distance_rows", len(burdens) == 14 and len({row.get("burden") for row in burdens}) == 14, "14 unique burden rows")
        freezes = matrix.get("preserved_freezes", [])
        add(checks, "freeze_count", len(freezes) == 3 and len(set(freezes)) == 3, "three inherited freezes")
        successor = matrix.get("selected_successor", {})
        add(checks, "successor_unexecuted", successor.get("executed") is False and successor.get("next_role") == "refuter@0.2.0", "one unexecuted Refuter successor")

    disposition_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_disposition_v1.yaml"
    if disposition_path.is_file():
        disposition = parsed.get(str(disposition_path), load_yaml(disposition_path))
        add(checks, "disposition_verdict", disposition.get("decisive_verdict") == "source_pure_as_written", "focused decisive disposition")
        limits = disposition.get("authority_limits", {})
        add(checks, "disposition_authority", all(limits.get(key) is False for key in (
            "scientific_claims_changed", "physical_status_changed", "distance_to_gr_changed",
            "source_law_adopted", "canonical_ontology_modified", "physics_promotion_authorized",
            "proof_authority", "publication_authorized", "push_authorized", "external_action_authorized",
            "global_no_go_claimed", "future_source_extension_impossibility_claimed",
        )), "all promotion and overread flags false")

    for child_name in (
        "child_phys_math_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit.yaml",
        "child_phys_phil_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit.yaml",
    ):
        child = ART / child_name
        if child.is_file():
            text = child.read_text(encoding="utf-8")
            add(checks, f"child_verdict:{child_name}", "source_pure_as_written" in text, "child concurs on focused verdict")
            add(checks, f"child_no_delta:{child_name}", text.count("no_delta") >= 14 or text.count("No delta") >= 14, "child preserves 14 burden rows")

    conflict_path = ART / "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit.yaml"
    if conflict_path.is_file():
        conflict = parsed.get(str(conflict_path), load_yaml(conflict_path))
        add(checks, "conflict_review", conflict.get("verdict") == "no_conflict" and not conflict.get("unresolved_conflicts"), "zero unresolved blocking conflicts")

    provenance_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_audit_provenance_manifest_v1.yaml"
    if provenance_path.is_file():
        provenance = parsed.get(str(provenance_path), load_yaml(provenance_path))
        entries = provenance.get("artifacts", [])
        valid = bool(entries)
        for entry in entries:
            path = ROOT / entry.get("path", "")
            valid = valid and path.is_file() and sha256(path) == entry.get("sha256")
        add(checks, "provenance_hashes", valid, f"{len(entries)} artifact hashes")

    try:
        model = load_model()
        add(checks, "exact_model", model.get("status") == "PASS" and all(model.get("checks", {}).values()), "exact Fraction checks")
    except Exception as exc:  # noqa: BLE001
        model = {"status": "FAIL", "error": str(exc)}
        add(checks, "exact_model", False, str(exc))

    whitespace_paths = [path for path in ART.glob("*") if path.is_file() and path.suffix in {".tex", ".md", ".yaml", ".py"}]
    whitespace_ok = True
    for path in whitespace_paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if "\t" in line or line.endswith(" "):
                whitespace_ok = False
    add(checks, "whitespace", whitespace_ok, f"{len(whitespace_paths)} text artifacts")

    failures = [check for check in checks if check["status"] != "PASS"]
    return {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_audit_validation_v1",
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260810-017",
        "job_id": "AJ-RT-20260810-017-001",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failures),
        "failure_count": len(failures),
        "checks": checks,
        "model_summary": {"status": model.get("status"), "checks": model.get("checks", {})},
        "authority_note": "Operational validation is not theorem truth, source authority, physical evidence, adoption, or promotion authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_audit_compact_receipt_v1",
            "status": report["status"],
            "task_id": report["task_id"],
            "job_id": report["job_id"],
            "check_count": report["check_count"],
            "pass_count": report["pass_count"],
            "failure_count": report["failure_count"],
            "full_report_path": str(REPORT.relative_to(ROOT)),
            "full_report_sha256": sha256(REPORT),
            "authority_note": report["authority_note"],
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps({k: report[k] for k in ("status", "task_id", "job_id", "check_count", "pass_count", "failure_count")}, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
