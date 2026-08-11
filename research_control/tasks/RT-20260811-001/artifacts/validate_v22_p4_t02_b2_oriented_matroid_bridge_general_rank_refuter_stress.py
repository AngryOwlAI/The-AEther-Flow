#!/usr/bin/env python3
"""Focused validator for the RT-20260811-001 Bridge_OM Refuter stress."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260811-001"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_validation.json"
COMPACT = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_compact_receipt.json"
MODEL = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_model.py"

EXPECTED_SOURCES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1014.yaml": "6c24758482864dcb1e144af0c5e9fcaebea4d2132df4af9d6ebada63e93444a5",
    "research_control/tasks/RT-20260810-016/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_v1.tex": "c977c9a93e3a543fe18378f51b83773211b483df3377d4187c506ff88768bba4",
    "research_control/tasks/RT-20260810-017/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit_v1.tex": "961d584045e0911151ca79dedf87d90792485ab3504fdbba1366e063ab8e9b25",
    "research_control/tasks/RT-20260810-017/artifacts/parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge_general_rank_post_repair_smuggling_audit.md": "fb6d3f1f4d062fd7f0c0f620a6ad8145142f64048bfc943ca5c4d2c6bf5a2ab8",
}

STRICT_YAML_PATHS = [
    TASK / "00_TASK.yaml",
    TASK / "jobs/AJ-RT-20260811-001-001.yaml",
    TASK / "roles/refuter@0.2.0--RT-20260811-001.yaml",
    ART / "child_phys_math_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress.yaml",
    ART / "child_phys_phil_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress.yaml",
    ART / "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress.yaml",
    ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_matrix_v1.yaml",
    ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_obstruction_v1.yaml",
    ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_provenance_manifest_v1.yaml",
    TASK / "jobs/completions/AJC-AJ-RT-20260811-001-001.yaml",
    ROOT / "research_control/handoffs/handoff-1015.yaml",
]


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys."""


def construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping
)


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_model() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("rt018_refuter_model", MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("model import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_payload()


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append(
        {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail}
    )


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

    for relative, expected in EXPECTED_SOURCES.items():
        path = ROOT / relative
        actual = sha256(path) if path.is_file() else "missing"
        add(
            checks,
            f"source_hash:{relative}",
            actual == expected,
            f"expected={expected} actual={actual}",
        )

    required_files = [
        ART / "parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress.md",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_v1.tex",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_latex_compile_receipt.json",
        TASK / "documentation_impact.yaml",
        ROOT / "research_control/handoffs/handoff-1015.md",
    ]
    for path in required_files:
        add(checks, f"exists:{path.relative_to(ROOT)}", path.is_file(), "required output")

    tex_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_v1.tex"
    if tex_path.is_file():
        tex = tex_path.read_text(encoding="utf-8")
        for token in (
            "scoped obstruction",
            "arbitrarily small fixed-rank wall crossing",
            "All-rank reorientation branch flip",
            "Refinement persistence asymmetry",
            "Named-component projective-modulus noninjectivity",
            "Pointwise totality nonselection",
            "Distance-to-GR matrix",
            "ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
            "THEORETICAL-CONTINUATION-SELECTION-V1",
        ):
            add(checks, f"tex_token:{token}", token in tex, "required fused result token")

    matrix_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_matrix_v1.yaml"
    if matrix_path.is_file():
        matrix = parsed.get(str(matrix_path), load_yaml(matrix_path))
        add(checks, "matrix_result", matrix.get("decisive_result") == "scoped_obstruction", "one allowed Refuter result")
        rows = matrix.get("stress_rows", [])
        add(checks, "stress_rows", len(rows) == 12 and len({row.get("row_id") for row in rows}) == 12, "12 unique stress rows")
        burdens = matrix.get("distance_to_gr_status", [])
        add(checks, "distance_rows", len(burdens) == 14 and all(row.get("status") == "no_delta" for row in burdens), "14 literal no-delta burden rows")
        freezes = matrix.get("preserved_freeze_labels", [])
        add(checks, "inherited_freezes", len(freezes) == 3 and len(set(freezes)) == 3, "three inherited freezes")
        successor = matrix.get("successor_selection", {})
        add(checks, "successor_unexecuted", successor.get("status") == "selected_not_executed" and successor.get("role_family") == "theoretical-continuation-selector@0.1.0", "one unexecuted selector")

    obstruction_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_obstruction_v1.yaml"
    if obstruction_path.is_file():
        obstruction = parsed.get(str(obstruction_path), load_yaml(obstruction_path))
        add(checks, "obstruction_id", obstruction.get("obstruction_id") == "OB-V22-P4T02-B2-OM-BRIDGE-SELECTION-ROBUSTNESS-001", "canonical obstruction identity")
        freeze = obstruction.get("local_freeze", {})
        add(checks, "local_freeze", freeze.get("decision") == "locally_frozen" and freeze.get("diagnostic_use_remains_open", True) is not False and freeze.get("global_p4_t02_freeze") is False, "candidate-local not global freeze")
        add(checks, "inherited_obstruction_freezes", len(obstruction.get("inherited_freezes", [])) == 3, "three inherited freezes preserved")

    canonical_freeze = "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS"
    canonical_obstruction = "OB-V22-P4T02-B2-OM-BRIDGE-SELECTION-ROBUSTNESS-001"
    canonical_packet = "PKT-V22-P4T02-B2-POST-ORIENTED-MATROID-REFUTER-THEORETICAL-CONTINUATION-SELECTION-V1"
    for child_name in (
        "child_phys_math_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress.yaml",
        "child_phys_phil_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress.yaml",
    ):
        child_path = ART / child_name
        if child_path.is_file():
            text = child_path.read_text(encoding="utf-8")
            add(checks, f"child_result:{child_name}", "scoped_obstruction" in text, "child decisive result")
            add(checks, f"child_canonical_ids:{child_name}", all(token in text for token in (canonical_freeze, canonical_obstruction, canonical_packet)), "round-one canonical metadata")
            add(checks, f"child_no_delta:{child_name}", text.count("no_delta") >= 14, "child preserves 14 burden rows")
            add(checks, f"child_revision:{child_name}", "conflict_resolution_revision" in text, "round-one revision record")

    conflict_path = ART / "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress.yaml"
    if conflict_path.is_file():
        conflict = parsed.get(str(conflict_path), load_yaml(conflict_path))
        add(checks, "conflict_review", conflict.get("status") == "resolved" and conflict.get("resolution_rounds") == 1 and conflict.get("unresolved_blocking_conflict_count") == 0, "one resolved metadata round and zero blockers")

    provenance_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_provenance_manifest_v1.yaml"
    if provenance_path.is_file():
        provenance = parsed.get(str(provenance_path), load_yaml(provenance_path))
        entries = provenance.get("artifacts", [])
        valid = bool(entries)
        for entry in entries:
            path = ROOT / entry.get("path", "")
            valid = valid and path.is_file() and sha256(path) == entry.get("sha256")
        add(checks, "provenance_artifact_hashes", valid, f"{len(entries)} artifact hashes")

    try:
        model = load_model()
        add(checks, "exact_model", model.get("status") == "PASS" and len(model.get("checks", {})) == 9 and all(model.get("checks", {}).values()), "nine exact Fraction checks")
    except Exception as exc:  # noqa: BLE001
        model = {"status": "FAIL", "checks": {}, "error": str(exc)}
        add(checks, "exact_model", False, str(exc))

    receipt_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_latex_compile_receipt.json"
    if receipt_path.is_file():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        add(checks, "latex_receipt", receipt.get("status") == "PASS" and receipt.get("visual_inspection_status") == "PASS" and receipt.get("page_count") == receipt.get("visually_inspected_page_count"), "all-page compile and visual inspection")

    whitespace_paths = [
        path for path in ART.glob("*")
        if path.is_file() and path.suffix in {".tex", ".md", ".yaml", ".py"}
    ]
    whitespace_ok = all(
        "\t" not in line and not line.endswith(" ")
        for path in whitespace_paths
        for line in path.read_text(encoding="utf-8").splitlines()
    )
    add(checks, "whitespace", whitespace_ok, f"{len(whitespace_paths)} text artifacts")

    failures = [check for check in checks if check["status"] != "PASS"]
    return {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_validation_v1",
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260811-001",
        "job_id": "AJ-RT-20260811-001-001",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failures),
        "failure_count": len(failures),
        "checks": checks,
        "model_summary": {
            "status": model.get("status"),
            "payload_sha256": model.get("payload_sha256"),
            "checks": model.get("checks", {}),
        },
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
            "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_refuter_stress_compact_receipt_v1",
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
    summary = {key: report[key] for key in ("status", "task_id", "job_id", "check_count", "pass_count", "failure_count")}
    print(json.dumps(summary, indent=2, sort_keys=True) if args.json else report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
