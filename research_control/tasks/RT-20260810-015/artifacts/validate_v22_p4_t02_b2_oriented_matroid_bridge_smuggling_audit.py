#!/usr/bin/env python3
"""Focused validator for the RT015 oriented-matroid bridge smuggling audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260810-015"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_validation.json"
COMPACT = ART / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_compact_receipt.json"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def load_model() -> dict[str, Any]:
    path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_model.py"
    spec = importlib.util.spec_from_file_location("rt015_audit_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load RT015 exact model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build()


def nested_values(value: Any, key_names: set[str]) -> list[Any]:
    values: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) in key_names:
                values.append(child)
            values.extend(nested_values(child, key_names))
    elif isinstance(value, list):
        for child in value:
            values.extend(nested_values(child, key_names))
    return values


def check(
    condition: bool,
    name: str,
    detail: str,
    checks: list[dict[str, Any]],
) -> None:
    checks.append(
        {"check_id": name, "status": "PASS" if condition else "FAIL", "detail": detail}
    )


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required = [
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260810-015.md",
        TASK / "jobs/AJ-RT-20260810-015-001.yaml",
        TASK / "roles/smuggling-auditor@0.2.0--RT-20260810-015.yaml",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_v1.tex",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_matrix_v1.yaml",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_disposition_v1.yaml",
        ART
        / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_provenance_manifest_v1.yaml",
        ART / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_model.py",
        ART / "child_phys_math_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.yaml",
        ART / "child_phys_phil_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.yaml",
        ART
        / "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.yaml",
        ART / "parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.md",
        ART
        / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_latex_compile_receipt.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    check(not missing, "required_artifacts", f"missing={missing}", checks)

    yaml_paths = [
        path
        for path in required
        if path.suffix in {".yaml", ".yml"} and path.is_file()
    ]
    yaml_errors: list[str] = []
    parsed: dict[str, Any] = {}
    for path in yaml_paths:
        try:
            parsed[path.name] = load_yaml(path)
        except Exception as exc:
            yaml_errors.append(f"{path.relative_to(ROOT)}: {exc}")
    check(not yaml_errors, "unique_key_yaml", f"errors={yaml_errors}", checks)

    provenance = parsed.get(
        "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_provenance_manifest_v1.yaml",
        {},
    )
    mismatches: list[dict[str, str]] = []
    source_rows = provenance.get("source_files", []) if isinstance(provenance, dict) else []
    for row in source_rows:
        path = ROOT / row["path"]
        observed = sha256(path) if path.is_file() else "missing"
        if observed != row["sha256"]:
            mismatches.append(
                {
                    "path": row["path"],
                    "expected": row["sha256"],
                    "observed": observed,
                }
            )
    check(
        len(source_rows) == 12 and not mismatches,
        "source_hashes",
        f"count={len(source_rows)} mismatches={mismatches}",
        checks,
    )

    model: dict[str, Any] = {}
    model_error = ""
    try:
        model = load_model()
    except Exception as exc:
        model_error = str(exc)
    model_checks = model.get("checks", {}) if isinstance(model, dict) else {}
    check(
        not model_error
        and model.get("status") == "PASS"
        and model_checks
        and all(model_checks.values()),
        "exact_model",
        f"error={model_error!r} payload={model.get('model_payload_sha256', '')}",
        checks,
    )
    rank_controls = (
        model.get("general_rank_extension", {}).get("controls", []) if model else []
    )
    check(
        [row.get("rank") for row in rank_controls] == [1, 2, 3, 4, 5, 6]
        and rank_controls[4].get("minimal_positive_circuit_support_bound") == 6
        and rank_controls[5].get("minimal_positive_circuit_support_bound") == 7,
        "general_rank_extension",
        "ranks 1..6 with support ceilings 6 and 7 at ranks 5 and 6",
        checks,
    )

    matrix = parsed.get(
        "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_matrix_v1.yaml", {}
    )
    dimensions = matrix.get("dimensions", []) if isinstance(matrix, dict) else []
    dimension_ids = [row.get("dimension_id") for row in dimensions]
    rank_rows = [
        row for row in dimensions if row.get("dimension_id") == "AUD-06-RANK-CAP"
    ]
    check(
        len(dimensions) == 16 and len(set(dimension_ids)) == 16,
        "audit_matrix_dimensions",
        f"dimension_count={len(dimensions)} unique={len(set(dimension_ids))}",
        checks,
    )
    check(
        matrix.get("decisive_verdict") == "repair_required"
        and len(rank_rows) == 1
        and rank_rows[0].get("local_verdict") == "repair_required",
        "rank_cap_verdict",
        "one repair_required verdict tied to AUD-06-RANK-CAP",
        checks,
    )

    disposition = parsed.get(
        "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_disposition_v1.yaml", {}
    )
    successor = (
        disposition.get("selected_successor", {})
        if isinstance(disposition, dict)
        else {}
    )
    check(
        disposition.get("decisive_verdict") == "repair_required"
        and disposition.get("verdict_count") == 1
        and successor.get("packet_id")
        == "PKT-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-GENERAL-RANK-REPAIR-V1"
        and successor.get("role_family") == "candidate-constructor@0.2.0"
        and successor.get("executed") is False,
        "decisive_disposition",
        "repair_required with one unexecuted Candidate Constructor repair",
        checks,
    )
    freezes = disposition.get("preserved_freeze_labels", []) if disposition else []
    check(
        freezes
        == [
            "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
            "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
            "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
        ],
        "freeze_preservation",
        f"freezes={freezes}",
        checks,
    )

    child_summaries: list[dict[str, Any]] = []
    for filename in (
        "child_phys_math_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.yaml",
        "child_phys_phil_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.yaml",
    ):
        child = parsed.get(filename, {})
        values = nested_values(
            child,
            {
                "decisive_verdict",
                "overall_verdict",
                "audit_verdict",
                "verdict",
                "decisive_result",
                "result_type",
            },
        )
        child_summaries.append(
            {"filename": filename, "verdict_values": [str(v) for v in values]}
        )
    check(
        len(child_summaries) == 2
        and all(summary["verdict_values"] for summary in child_summaries),
        "independent_children",
        json.dumps(child_summaries, sort_keys=True),
        checks,
    )

    conflict = parsed.get(
        "parent_conflict_review_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.yaml",
        {},
    )
    check(
        conflict.get("blocking_conflict_count") == 0
        and conflict.get("all_conflicts_resolved") is True,
        "parent_conflict_review",
        f"blocking={conflict.get('blocking_conflict_count')} "
        f"resolved={conflict.get('all_conflicts_resolved')}",
        checks,
    )

    tex_path = ART / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.is_file() else ""
    phrases = [
        "repair\\_required",
        "arbitrary finite rank",
        "|C|\\le r+1",
        "not forbidden target import",
        "Distance-to-GR",
        "selects, but does not execute",
    ]
    missing_phrases = [phrase for phrase in phrases if phrase not in tex]
    check(
        not missing_phrases,
        "manuscript_contract",
        f"missing={missing_phrases}",
        checks,
    )

    compile_path = (
        ART
        / "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_latex_compile_receipt.json"
    )
    compile_receipt = (
        json.loads(compile_path.read_text(encoding="utf-8"))
        if compile_path.is_file()
        else {}
    )
    compile_pass = compile_receipt.get("status") == "PASS" or compile_receipt.get(
        "compile_status"
    ) == "PASS"
    check(
        compile_pass,
        "latex_compile",
        f"receipt_status={compile_receipt.get('status', compile_receipt.get('compile_status'))}",
        checks,
    )

    registry_checks = {
        "registries/RESEARCH_TASK_REGISTRY.csv": "RT-20260810-015",
        "registries/DIRECTOR_DECISION_REGISTRY.csv": "DDR-20260810-015",
        "registries/AGENT_JOB_REGISTRY.csv": "AJ-RT-20260810-015-001",
        "registries/ROLE_EXECUTION_REGISTRY.csv": "smuggling-auditor@0.2.0--RT-20260810-015",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv": "CB-V22-P4-T02-B2-ORIENTED-MATROID-BRIDGE-SMUGGLING-AUDIT-001",
    }
    missing_registry_ids = [
        identifier
        for path, identifier in registry_checks.items()
        if identifier not in (ROOT / path).read_text(encoding="utf-8")
    ]
    check(
        not missing_registry_ids,
        "control_registries",
        f"missing={missing_registry_ids}",
        checks,
    )

    status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_validation_v1",
        "task_id": "RT-20260810-015",
        "job_id": "AJ-RT-20260810-015-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "fail_count": sum(row["status"] == "FAIL" for row in checks),
        "model_payload_sha256": model.get("model_payload_sha256", ""),
        "checks": checks,
        "authority_limits": {
            "validator_pass_is_scientific_authority": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        compact = {
            "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_compact_receipt_v1",
            "task_id": report["task_id"],
            "job_id": report["job_id"],
            "status": report["status"],
            "check_count": report["check_count"],
            "pass_count": report["pass_count"],
            "fail_count": report["fail_count"],
            "validation_sha256": sha256(REPORT),
            "model_payload_sha256": report["model_payload_sha256"],
        }
        COMPACT.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
