#!/usr/bin/env python3
"""Focused validator for the RT008 robust-invariance Smuggling Auditor packet."""

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
REPORT = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_validation.json"
COMPACT = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_compact_receipt.json"
MODEL = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_model.py"


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
    spec = importlib.util.spec_from_file_location("rt008_smuggling_model", MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load exact model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_payload()


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
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_matrix_v1.yaml",
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_disposition_v1.yaml",
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_provenance_manifest_v1.yaml",
        "child_phys_math_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_audit.yaml",
        "child_phys_phil_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_audit.yaml",
        "parent_conflict_review_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_audit.yaml",
    ]
    parsed: dict[str, Any] = {}
    parse_errors: dict[str, str] = {}
    for name in yaml_names:
        path = ART / name
        try:
            parsed[name] = parse_yaml(path)
        except Exception as exc:
            parse_errors[name] = str(exc)
    check(
        not parse_errors and len(parsed) == len(yaml_names),
        "strict_unique_yaml",
        f"parsed={len(parsed)} errors={parse_errors}",
        checks,
    )

    model = load_model()
    check(
        model.get("all_pass") is True
        and model.get("check_count") == 12
        and model.get("pass_count") == 12
        and model.get("payload_sha256")
        == "189b55235384c36ef6886fcf8c91107c02a3928a0de275d8592eb34755cbd888",
        "exact_model",
        f"all_pass={model.get('all_pass')} checks={model.get('pass_count')}/{model.get('check_count')} payload={model.get('payload_sha256')}",
        checks,
    )

    provenance_name = (
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_provenance_manifest_v1.yaml"
    )
    provenance = parsed.get(provenance_name, {})
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
        provenance.get("source_count") == 12
        and len(sources) == 12
        and not mismatches,
        "source_manifest_hashes",
        f"declared={provenance.get('source_count')} rows={len(sources)} mismatches={mismatches}",
        checks,
    )

    matrix_name = (
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_matrix_v1.yaml"
    )
    matrix = parsed.get(matrix_name, {})
    dimensions = matrix.get("audit_dimensions", []) if isinstance(matrix, dict) else []
    dimension_ids = [row.get("dimension_id") for row in dimensions]
    job_dimension_ids = [row.get("job_dimension_id") for row in dimensions]
    expected_job_dimensions = {
        "source_law_arena_provenance",
        "admissible_set_K_and_inward_orientation",
        "generator_family_A_admissibility",
        "variation_multifunction_Delta_and_countermodel_exclusion",
        "tangent_conormal_and_strict_margin_role",
        "EqSrc_groupoid_provenance_and_coherence",
        "predeclaration_nonadaptivity_versus_epistemic_independence",
        "certificate_orbit_and_positive_regraduation",
        "exact_fixture_quarantine",
        "goal_property_preload_and_root_nonselection",
        "target_empirical_physical_and_workflow_authority_scan",
        "current_ontology_adoption_and_p4_t02_relevance",
    }
    check(
        matrix.get("audit_dimension_count") == 12
        and len(dimensions) == 12
        and len(set(dimension_ids)) == 12
        and set(job_dimension_ids) == expected_job_dimensions,
        "audit_matrix_dimensions",
        f"declared={matrix.get('audit_dimension_count')} rows={len(dimensions)} unique={len(set(dimension_ids))} parity={set(job_dimension_ids) == expected_job_dimensions}",
        checks,
    )
    check(
        matrix.get("decisive_verdict") == "source_pure_as_written"
        and all(row.get("written_syntax_source_pure") is True for row in dimensions)
        and all(
            row.get("independent_source_provenance_established") is False
            for row in dimensions
        ),
        "audit_matrix_verdict_scope",
        f"verdict={matrix.get('decisive_verdict')} syntax_pure={all(row.get('written_syntax_source_pure') is True for row in dimensions)} provenance_false={all(row.get('independent_source_provenance_established') is False for row in dimensions)}",
        checks,
    )

    disposition_name = (
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_disposition_v1.yaml"
    )
    disposition = parsed.get(disposition_name, {})
    successor = disposition.get("selected_successor", {}) if disposition else {}
    classification = disposition.get("source_extension_classification", {})
    check(
        disposition.get("verdict_count") == 1
        and disposition.get("decisive_verdict") == "source_pure_as_written"
        and classification.get("classification") == "new_ontology_primitive_candidate"
        and classification.get("relation_to_current_ontology") == "not_derived"
        and classification.get("forbidden_target_import") is False
        and classification.get("adopted") is False,
        "decisive_disposition_and_classification",
        f"verdict={disposition.get('decisive_verdict')} classification={classification.get('classification')} derived={classification.get('relation_to_current_ontology')} adopted={classification.get('adopted')}",
        checks,
    )
    check(
        successor.get("packet_id")
        == "PKT-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-REFUTER-STRESS-V1"
        and successor.get("packet_type") == "source_extension_refuter_stress"
        and successor.get("role_family") == "refuter@0.2.0"
        and successor.get("status") == "selected_not_executed"
        and successor.get("executed") is False,
        "successor_selected_not_executed",
        f"packet={successor.get('packet_id')} role={successor.get('role_family')} status={successor.get('status')} executed={successor.get('executed')}",
        checks,
    )

    payloads = disposition.get("new_mathematical_payload", []) if disposition else []
    payload_ids = [row.get("payload_id") for row in payloads]
    check(
        len(payloads) == 5 and len(set(payload_ids)) == 5,
        "new_mathematical_payload",
        f"count={len(payloads)} unique={len(set(payload_ids))}",
        checks,
    )

    expected_freezes = [
        "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
        "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
        "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
        "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
        "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    ]
    freezes = disposition.get("preserved_freeze_labels", []) if disposition else []
    check(
        freezes == expected_freezes
        and disposition.get("freeze_status", {}).get("preserved_freeze_count") == 5
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

    child_names = [
        "child_phys_math_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_audit.yaml",
        "child_phys_phil_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_audit.yaml",
    ]
    child_summaries: list[dict[str, object]] = []
    for name in child_names:
        child = parsed.get(name, {})
        values = nested_values(
            child,
            {"decisive_verdict", "overall_verdict", "audit_verdict", "verdict"},
        )
        child_summaries.append(
            {
                "filename": name,
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

    conflict_name = (
        "parent_conflict_review_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_audit.yaml"
    )
    conflict = parsed.get(conflict_name, {})
    expected_child_hashes = {
        "child_phys_math": "8ac0b6fc0d62e05b96627b23743dee96da1dfe579c1b99d2e800517648026df5",
        "child_phys_phil": "edcfca5e45ef7607f34f898a7d67534f1353000a18d9e67ea1b46ad8a7ba765c",
    }
    actual_child_hashes = {
        row.get("execution_unit_id"): row.get("sha256")
        for row in conflict.get("reviewed_children", [])
    }
    check(
        conflict.get("blocking_conflict_count") == 0
        and conflict.get("all_conflicts_resolved") is True
        and conflict.get("unresolved_blocking_conflict") is False
        and actual_child_hashes == expected_child_hashes,
        "parent_conflict_review",
        f"blocking={conflict.get('blocking_conflict_count')} resolved={conflict.get('all_conflicts_resolved')} child_hashes={actual_child_hashes}",
        checks,
    )

    tex_path = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_audit_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.is_file() else ""
    required_phrases = [
        "source\\_pure\\_as\\_written",
        "Classifier noninversion",
        "One-root pass/fail pairs",
        "Transport preserves supplied data but selects none",
        "Twelve-dimension audit",
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

    compile_path = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_latex_compile_receipt.json"
    compile_receipt = (
        json.loads(compile_path.read_text(encoding="utf-8"))
        if compile_path.is_file()
        else {}
    )
    check(
        compile_receipt.get("status") == "PASS"
        and compile_receipt.get("visual_inspection", {}).get("status") == "PASS"
        and compile_receipt.get("local_pdf", {}).get("page_count") == 5
        and compile_receipt.get("source", {}).get("sha256") == sha256(tex_path)
        and compile_receipt.get("local_pdf", {}).get("pdf_required_by_registry") is False,
        "latex_compile_and_visual_review",
        f"status={compile_receipt.get('status')} visual={compile_receipt.get('visual_inspection', {}).get('status')} pages={compile_receipt.get('local_pdf', {}).get('page_count')}",
        checks,
    )

    registry_checks = {
        "registries/RESEARCH_TASK_REGISTRY.csv": "RT-20260811-008",
        "registries/DIRECTOR_DECISION_REGISTRY.csv": "DDR-20260811-008",
        "registries/AGENT_JOB_REGISTRY.csv": "AJ-RT-20260811-008-001",
        "registries/ROLE_EXECUTION_REGISTRY.csv": "smuggling-auditor@0.2.0--RT-20260811-008",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv": "CB-V22-P4-T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-SMUGGLING-AUDIT-001",
        "registries/TEX_SOURCE_REGISTRY.csv": "TEX-V22-P4-T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-SMUGGLING-AUDIT-V1",
        "registries/MARKDOWN_SOURCE_REGISTRY.csv": "MD-V22-P4-T02-B2-PARENT-FUSION-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-SMUGGLING-AUDIT-V1",
    }
    missing_registry_ids = [
        identifier
        for path, identifier in registry_checks.items()
        if identifier not in (ROOT / path).read_text(encoding="utf-8")
    ]
    check(
        not missing_registry_ids,
        "control_and_source_registries",
        f"missing={missing_registry_ids}",
        checks,
    )

    completion_path = (
        ROOT
        / "research_control/tasks/RT-20260811-008/jobs/completions/AJC-AJ-RT-20260811-008-001.yaml"
    )
    handoff_path = ROOT / "research_control/handoffs/handoff-1022.yaml"
    completion = parse_yaml(completion_path) if completion_path.is_file() else {}
    handoff = parse_yaml(handoff_path) if handoff_path.is_file() else {}
    check(
        completion.get("objective_result") == "source_pure_as_written"
        and completion.get("parent_child_synthesis", {})
        .get("conflict_review", {})
        .get("unresolved_conflicts")
        == []
        and handoff.get("handoff_id") == "handoff-1022"
        and handoff.get("required_next_packet", {}).get("executed") is False,
        "completion_and_handoff",
        f"completion={completion.get('objective_result')} handoff={handoff.get('handoff_id')} successor_executed={handoff.get('required_next_packet', {}).get('executed')}",
        checks,
    )

    status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_validation_v1",
        "task_id": "RT-20260811-008",
        "job_id": "AJ-RT-20260811-008-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "fail_count": sum(row["status"] == "FAIL" for row in checks),
        "model_payload_sha256": model.get("payload_sha256", ""),
        "checks": checks,
        "authority_limits": {
            "validator_pass_is_scientific_authority": False,
            "independent_source_provenance_established": False,
            "current_ontology_derivation_established": False,
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
            "schema_id": "v22_p4_t02_b2_source_law_space_robust_invariance_protection_smuggling_compact_receipt_v1",
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
