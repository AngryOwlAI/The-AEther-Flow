#!/usr/bin/env python3
"""Focused validator for the RT004 signed-cubic Smuggling Auditor packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ART = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
REPORT = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_validation.json"
COMPACT = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_compact_receipt.json"
MODEL = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_model.py"


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def load_model() -> dict[str, object]:
    spec = importlib.util.spec_from_file_location("rt004_smuggling_model", MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load exact model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exact_controls()


def nested_values(value: Any, keys: set[str]) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) in keys:
                found.append(child)
            found.extend(nested_values(child, keys))
    elif isinstance(value, list):
        for child in value:
            found.extend(nested_values(child, keys))
    return found


def check(
    condition: bool,
    check_id: str,
    evidence: str,
    rows: list[dict[str, str]],
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "evidence": evidence,
        }
    )


def build_report() -> dict[str, object]:
    checks: list[dict[str, str]] = []
    yaml_names = [
        "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_matrix_v1.yaml",
        "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_disposition_v1.yaml",
        "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_provenance_manifest_v1.yaml",
        "child_phys_math_p4_t02_b2_signed_cubic_viability_selector_smuggling_audit.yaml",
        "child_phys_phil_p4_t02_b2_signed_cubic_viability_selector_smuggling_audit.yaml",
        "parent_conflict_review_p4_t02_b2_signed_cubic_viability_selector_smuggling_audit.yaml",
    ]
    parsed: dict[str, Any] = {}
    parse_errors: dict[str, str] = {}
    for name in yaml_names:
        path = ART / name
        try:
            parsed[name] = parse_yaml(path)
        except Exception as exc:  # exact evidence is preserved in the report
            parse_errors[name] = str(exc)
    check(
        not parse_errors and len(parsed) == len(yaml_names),
        "strict_unique_yaml",
        f"parsed={len(parsed)} errors={parse_errors}",
        checks,
    )

    model = load_model()
    check(
        model.get("status") == "PASS"
        and model.get("check_count") == 8
        and model.get("pass_count") == 8
        and model.get("source_count") == 13,
        "exact_model",
        f"status={model.get('status')} checks={model.get('pass_count')}/{model.get('check_count')} sources={model.get('source_count')}",
        checks,
    )

    provenance = parsed.get(
        "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_provenance_manifest_v1.yaml",
        {},
    )
    sources = provenance.get("sources", []) if isinstance(provenance, dict) else []
    mismatches: list[str] = []
    for source in sources:
        rel = source.get("path", "")
        expected = source.get("sha256", "")
        path = ROOT / rel
        actual = sha256(path) if path.is_file() else "MISSING"
        if actual != expected:
            mismatches.append(f"{rel}:{actual}!={expected}")
    check(
        provenance.get("source_count") == 13
        and len(sources) == 13
        and not mismatches,
        "source_manifest_hashes",
        f"declared={provenance.get('source_count')} rows={len(sources)} mismatches={mismatches}",
        checks,
    )

    matrix = parsed.get(
        "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_matrix_v1.yaml",
        {},
    )
    dimensions = matrix.get("audit_dimensions", []) if isinstance(matrix, dict) else []
    dimension_ids = [row.get("dimension_id") for row in dimensions]
    job_dimension_ids = [row.get("job_dimension_id") for row in dimensions]
    expected_job_dimensions = {
        "source_state_and_semiflow_provenance",
        "positive_gamma_origin_and_sign",
        "bounded_step_horizon_Delta",
        "amplitude_reference_a_star",
        "orientation_token_sigma_and_goal_preload",
        "predeclaration_and_dependency_acyclicity",
        "reflection_equivariance_and_token_nonselection",
        "positive_regraduation_and_dimensionless_reduction",
        "component_not_point_or_probability_occurrence",
        "finite_path_versus_asymptotic_viability",
        "target_empirical_physical_and_workflow_authority_scan",
        "current_ontology_adoption_and_p4_t02_relevance",
    }
    check(
        matrix.get("audit_dimension_count") == 12
        and len(dimensions) == 12
        and len(set(dimension_ids)) == 12
        and set(job_dimension_ids) == expected_job_dimensions,
        "audit_matrix_dimensions",
        f"declared={matrix.get('audit_dimension_count')} rows={len(dimensions)} unique={len(set(dimension_ids))} job_parity={set(job_dimension_ids) == expected_job_dimensions}",
        checks,
    )
    check(
        matrix.get("decisive_verdict") == "source_pure_as_written"
        and matrix.get("source_extension_classification", {}).get("classification")
        == "new_ontology_primitive_candidate"
        and matrix.get("source_extension_classification", {}).get(
            "forbidden_target_import"
        )
        is False,
        "audit_matrix_verdict",
        f"verdict={matrix.get('decisive_verdict')} classification={matrix.get('source_extension_classification', {}).get('classification')}",
        checks,
    )

    disposition = parsed.get(
        "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_disposition_v1.yaml",
        {},
    )
    successor = disposition.get("selected_successor", {}) if disposition else {}
    check(
        disposition.get("verdict_count") == 1
        and disposition.get("decisive_verdict") == "source_pure_as_written"
        and successor.get("packet_id")
        == "PKT-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-SOURCE-EXTENSION-REFUTER-STRESS-V1"
        and successor.get("packet_type") == "source_extension_refuter_stress"
        and successor.get("role_family") == "refuter@0.2.0"
        and successor.get("status") == "selected_not_executed"
        and successor.get("executed") is False,
        "decisive_disposition_and_successor",
        f"verdict={disposition.get('decisive_verdict')} successor={successor.get('packet_id')} executed={successor.get('executed')}",
        checks,
    )

    payloads = disposition.get("new_mathematical_payload", []) if disposition else []
    payload_ids = [row.get("payload_id") for row in payloads]
    check(
        len(payloads) >= 5 and len(payload_ids) == len(set(payload_ids)),
        "new_mathematical_payload",
        f"count={len(payloads)} unique={len(set(payload_ids))}",
        checks,
    )

    expected_freezes = [
        "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
        "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
        "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
        "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    ]
    freezes = disposition.get("preserved_freeze_labels", []) if disposition else []
    check(
        freezes == expected_freezes
        and disposition.get("freeze_status", {}).get("preserved_freeze_count") == 4
        and disposition.get("freeze_status", {}).get("new_freeze_created") is False,
        "freeze_preservation",
        f"freezes={freezes}",
        checks,
    )

    distance = disposition.get("distance_to_gr_status", []) if disposition else []
    check(
        len(distance) == 14
        and len({row.get("burden") for row in distance}) == 14
        and all(row.get("task_delta") == "no_delta" for row in distance)
        and disposition.get("distance_to_gr_delta", {}).get("changed") is False,
        "distance_to_gr_matrix",
        f"rows={len(distance)} unique={len({row.get('burden') for row in distance})} all_no_delta={all(row.get('task_delta') == 'no_delta' for row in distance)}",
        checks,
    )

    child_summaries: list[dict[str, object]] = []
    for name in (
        "child_phys_math_p4_t02_b2_signed_cubic_viability_selector_smuggling_audit.yaml",
        "child_phys_phil_p4_t02_b2_signed_cubic_viability_selector_smuggling_audit.yaml",
    ):
        child = parsed.get(name, {})
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
            {
                "filename": name,
                "verdict_values": [str(value) for value in values],
                "contains_source_pure": "source_pure_as_written"
                in [str(value) for value in values],
            }
        )
    check(
        len(child_summaries) == 2
        and all(row["contains_source_pure"] for row in child_summaries),
        "independent_children",
        json.dumps(child_summaries, sort_keys=True),
        checks,
    )

    conflict = parsed.get(
        "parent_conflict_review_p4_t02_b2_signed_cubic_viability_selector_smuggling_audit.yaml",
        {},
    )
    check(
        conflict.get("blocking_conflict_count") == 0
        and conflict.get("all_conflicts_resolved") is True
        and conflict.get("unresolved_blocking_conflict") is False,
        "parent_conflict_review",
        f"blocking={conflict.get('blocking_conflict_count')} resolved={conflict.get('all_conflicts_resolved')} unresolved={conflict.get('unresolved_blocking_conflict')}",
        checks,
    )

    tex_path = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_source_extension_smuggling_audit_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.is_file() else ""
    required_phrases = [
        "source\\_pure\\_as\\_written",
        "Dimensionless reduction",
        "Reflection proves token nonselection",
        "Finite viability and the asymptotic boundary",
        "not probability occurrence",
        "Distance-to-GR",
        "selects, but does not execute",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in tex]
    check(
        not missing_phrases,
        "manuscript_contract",
        f"missing={missing_phrases}",
        checks,
    )

    compile_path = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_latex_compile_receipt.json"
    compile_receipt = (
        json.loads(compile_path.read_text(encoding="utf-8"))
        if compile_path.is_file()
        else {}
    )
    check(
        compile_receipt.get("status") == "PASS"
        and compile_receipt.get("visual_inspection", {}).get("status") == "PASS"
        and compile_receipt.get("page_count") == 5
        and compile_receipt.get("source_sha256") == sha256(tex_path),
        "latex_compile_and_visual_review",
        f"status={compile_receipt.get('status')} visual={compile_receipt.get('visual_inspection', {}).get('status')} pages={compile_receipt.get('page_count')}",
        checks,
    )

    registry_checks = {
        "registries/RESEARCH_TASK_REGISTRY.csv": "RT-20260811-004",
        "registries/DIRECTOR_DECISION_REGISTRY.csv": "DDR-20260811-004",
        "registries/AGENT_JOB_REGISTRY.csv": "AJ-RT-20260811-004-001",
        "registries/ROLE_EXECUTION_REGISTRY.csv": "smuggling-auditor@0.2.0--RT-20260811-004",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv": "CB-V22-P4-T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-SMUGGLING-AUDIT-001",
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
        "schema_id": "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_validation_v1",
        "task_id": "RT-20260811-004",
        "job_id": "AJ-RT-20260811-004-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "fail_count": sum(row["status"] == "FAIL" for row in checks),
        "model_payload_sha256": model.get("model_payload_sha256", ""),
        "checks": checks,
        "authority_limits": {
            "validator_pass_is_scientific_authority": False,
            "candidate_adopted": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "successor_executed": False,
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
            "schema_id": "v22_p4_t02_b2_signed_cubic_viability_selector_smuggling_compact_receipt_v1",
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
