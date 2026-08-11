#!/usr/bin/env python3
"""Focused validation for the RT009 robust-invariance Refuter transaction."""

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
REPORT = ART / (
    "v22_p4_t02_b2_source_law_space_robust_invariance_protection_"
    "refuter_stress_validation.json"
)
COMPACT = ART / (
    "v22_p4_t02_b2_source_law_space_robust_invariance_protection_"
    "refuter_stress_compact_receipt.json"
)
MODEL = ART / (
    "v22_p4_t02_b2_source_law_space_robust_invariance_protection_"
    "refuter_stress_model.py"
)
SUCCESSOR = (
    "PKT-V22-P4T02-B2-POST-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-REFUTER-"
    "THEORETICAL-CONTINUATION-SELECTION-V1"
)
OBSTRUCTION = (
    "OB-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-"
    "ROBUSTNESS-001"
)
LOCAL_FREEZE = (
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-"
    "ROBUSTNESS"
)


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


def parse_yaml(path: Path, *, unique: bool = True) -> Any:
    loader = UniqueKeyLoader if unique else yaml.SafeLoader
    return yaml.load(path.read_text(encoding="utf-8"), Loader=loader)


def load_model() -> dict[str, object]:
    spec = importlib.util.spec_from_file_location("rt009_refuter_model", MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load RT009 exact model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_model()


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
    task_root = ROOT / "research_control/tasks/RT-20260811-009"
    yaml_paths = {
        "task": task_root / "00_TASK.yaml",
        "role": task_root / "roles/refuter@0.2.0--RT-20260811-009.yaml",
        "job": task_root / "jobs/AJ-RT-20260811-009-001.yaml",
        "completion": task_root
        / "jobs/completions/AJC-AJ-RT-20260811-009-001.yaml",
        "handoff": ROOT / "research_control/handoffs/handoff-1023.yaml",
        "matrix": ART
        / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_refuter_stress_matrix_v1.yaml",
        "obstruction": ART
        / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_refuter_obstruction_v1.yaml",
        "manifest": ART
        / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_refuter_stress_provenance_manifest_v1.yaml",
        "child_math": ART
        / "child_phys_math_p4_t02_b2_source_law_space_robust_invariance_protection_refuter_stress.yaml",
        "child_phil": ART
        / "child_phys_phil_p4_t02_b2_source_law_space_robust_invariance_protection_refuter_stress.yaml",
        "conflict": ART
        / "parent_conflict_review_p4_t02_b2_source_law_space_robust_invariance_protection_refuter_stress.yaml",
    }
    parsed: dict[str, Any] = {}
    parse_errors: dict[str, str] = {}
    for name, path in yaml_paths.items():
        try:
            parsed[name] = parse_yaml(path)
        except Exception as exc:  # pragma: no cover - diagnostic path
            parse_errors[name] = str(exc)
    check(
        not parse_errors and len(parsed) == len(yaml_paths),
        "strict_unique_yaml",
        f"parsed={len(parsed)} errors={parse_errors}",
        checks,
    )

    model = load_model()
    check(
        model.get("status") == "PASS"
        and model.get("check_count") == 10
        and model.get("passed_check_count") == 10
        and model.get("failed_check_count") == 0
        and sha256(MODEL)
        == "08c539ccd60ac48d3d7b597b1494bebc567f680d9e2ba95c3a606aa02f079a90",
        "exact_model",
        f"status={model.get('status')} pass={model.get('passed_check_count')}/{model.get('check_count')} hash={sha256(MODEL)}",
        checks,
    )

    manifest = parsed.get("manifest", {})
    sources = manifest.get("sources", []) if isinstance(manifest, dict) else []
    mismatches: list[str] = []
    for source in sources:
        rel = source.get("path", "")
        expected = source.get("sha256", "")
        path = ROOT / rel
        actual = sha256(path) if path.is_file() else "MISSING"
        if actual != expected:
            mismatches.append(f"{rel}:{actual}!={expected}")
    check(
        manifest.get("source_count") == 24
        and len(sources) == 24
        and not mismatches,
        "provenance_manifest",
        f"declared={manifest.get('source_count')} rows={len(sources)} mismatches={mismatches}",
        checks,
    )

    matrix = parsed.get("matrix", {})
    fixed = matrix.get("fixed_results_preserved", [])
    branches = matrix.get("stress_branches", [])
    payloads = matrix.get("new_mathematical_payload", [])
    check(
        matrix.get("decisive_result_class") == "scoped_obstruction"
        and matrix.get("refuter_result", {}).get("selected_count") == 1
        and len(fixed) == 7
        and all(row.get("status") == "preserved" for row in fixed),
        "decisive_result_and_fixed_scope",
        f"result={matrix.get('decisive_result_class')} selected={matrix.get('refuter_result', {}).get('selected_count')} fixed={len(fixed)}",
        checks,
    )
    check(
        len(branches) == 10
        and len({row.get("branch_id") for row in branches}) == 10
        and len(payloads) == 5
        and len({row.get("payload_id") for row in payloads}) == 5,
        "stress_branches_and_new_payload",
        f"branches={len(branches)} payloads={len(payloads)}",
        checks,
    )
    branch_ids = {row.get("branch_id") for row in branches}
    check(
        {
            "STRESS-03-NESTED-VARIATION-ENLARGEMENT",
            "STRESS-04-ORIENTATION-TRANSPORT",
            "STRESS-05-SAME-SLICE-PRODUCT-LIFTS",
            "STRESS-08-NONTRIVIAL-EQSRC-DEMAND",
        }.issubset(branch_ids),
        "exact_countermodel_contract",
        "variation, complete-reflection, transverse-lift, and nontrivial-arrow controls present",
        checks,
    )

    freezes = matrix.get("preserved_freezes", [])
    freeze_ids = [row.get("freeze_id") for row in freezes]
    check(
        len(freeze_ids) == 6
        and len(set(freeze_ids)) == 6
        and LOCAL_FREEZE in freeze_ids
        and matrix.get("freeze_criteria_status", {}).get("freeze_decision")
        == "locally_frozen",
        "freeze_contract",
        f"count={len(freeze_ids)} local={LOCAL_FREEZE in freeze_ids}",
        checks,
    )
    distance = matrix.get("distance_to_gr_status", [])
    check(
        len(distance) == 14
        and len({row.get("burden") for row in distance}) == 14
        and all(row.get("task_delta") == "no_delta" for row in distance),
        "distance_to_gr_matrix",
        f"rows={len(distance)} all_no_delta={all(row.get('task_delta') == 'no_delta' for row in distance)}",
        checks,
    )
    successor = matrix.get("selected_successor", {})
    check(
        successor.get("packet_id") == SUCCESSOR
        and successor.get("packet_type") == "theoretical_continuation_selector"
        and successor.get("role_family")
        == "theoretical-continuation-selector@0.1.0"
        and successor.get("execution_status") == "selected_not_executed"
        and matrix.get("authority_limits", {}).get("successor_executed") is False,
        "successor_selected_not_executed",
        f"packet={successor.get('packet_id')} status={successor.get('execution_status')}",
        checks,
    )

    obstruction = parsed.get("obstruction", {})
    obstruction_record = obstruction.get("refuter_obstruction_record", {})
    obstruction_freeze = obstruction_record.get("freeze_criteria_status", {})
    check(
        obstruction.get("result_class") == "scoped_obstruction"
        and obstruction_record.get("obstruction_id") == OBSTRUCTION
        and obstruction_record.get("minimal_countermodel_available") is True
        and obstruction_record.get("source_extension_repair_possible")
        == "repair_possible"
        and obstruction_freeze.get("active_freeze_label") == LOCAL_FREEZE
        and obstruction_record.get("global_no_go_claim_authorized") is False
        and obstruction_record.get("future_source_extension_impossibility_authorized")
        is False,
        "obstruction_schema_and_scope",
        f"result={obstruction.get('result_class')} id={obstruction_record.get('obstruction_id')} freeze={obstruction_freeze.get('active_freeze_label')}",
        checks,
    )

    child_summaries: list[dict[str, object]] = []
    for name in ("child_math", "child_phil"):
        child = parsed.get(name, {})
        child_text = json.dumps(child, sort_keys=True)
        child_summaries.append(
            {
                "name": name,
                "scoped_obstruction": "scoped_obstruction" in child_text,
                "successor": SUCCESSOR in child_text,
                "local_freeze": LOCAL_FREEZE in child_text,
            }
        )
    check(
        len(child_summaries) == 2
        and all(
            row["scoped_obstruction"]
            and row["successor"]
            and row["local_freeze"]
            for row in child_summaries
        ),
        "independent_child_convergence",
        json.dumps(child_summaries, sort_keys=True),
        checks,
    )

    conflict = parsed.get("conflict", {})
    expected_child_hashes = {
        "child_phys_math": "1439672919aa8587a6f8df969bede0cb3f7f8a3c93ee21cdd88758bf5361a1fb",
        "child_phys_phil": "f8e3471b6c269b992c8fd4d426023ce4ccf5fe715cf8ea91c2ab1826ae89d6b5",
    }
    actual_child_hashes = {
        row.get("execution_unit_id"): row.get("sha256")
        for row in conflict.get("child_outputs", [])
    }
    check(
        conflict.get("status") == "resolved"
        and conflict.get("unresolved_blocking_conflict_count") == 0
        and conflict.get("unresolved_blocking_conflicts") == []
        and actual_child_hashes == expected_child_hashes,
        "parent_conflict_review",
        f"status={conflict.get('status')} unresolved={conflict.get('unresolved_blocking_conflict_count')} hashes={actual_child_hashes}",
        checks,
    )

    tex_path = ART / (
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_"
        "refuter_stress_v1.tex"
    )
    tex = tex_path.read_text(encoding="utf-8") if tex_path.is_file() else ""
    required_tex = [
        "scoped\\_obstruction",
        "F_\\epsilon",
        "(1-\\alpha)\\epsilon",
        "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-",
        "No delta",
        "REFUTER-THEORETICAL-CONTINUATION-SELECTION-V1",
    ]
    missing_tex = [token for token in required_tex if token not in tex]
    check(
        not missing_tex,
        "manuscript_contract",
        f"missing={missing_tex}",
        checks,
    )

    compile_path = ART / (
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_"
        "refuter_stress_latex_compile_receipt.json"
    )
    compile_receipt = json.loads(compile_path.read_text(encoding="utf-8"))
    visual = compile_receipt.get("visual_inspection", {})
    check(
        compile_receipt.get("status") == "PASS"
        and compile_receipt.get("source_sha256") == sha256(tex_path)
        and compile_receipt.get("compile_pass_count") == 2
        and compile_receipt.get("page_count") == 5
        and visual.get("status") == "PASS"
        and visual.get("inspected_page_count") == 5
        and compile_receipt.get("pdf_required_by_registry") is False,
        "latex_compile_and_visual_review",
        f"status={compile_receipt.get('status')} passes={compile_receipt.get('compile_pass_count')} pages={compile_receipt.get('page_count')} visual={visual.get('status')}",
        checks,
    )

    registry_checks = {
        "registries/RESEARCH_TASK_REGISTRY.csv": "RT-20260811-009",
        "registries/DIRECTOR_DECISION_REGISTRY.csv": "DDR-20260811-009",
        "registries/AGENT_JOB_REGISTRY.csv": "AJ-RT-20260811-009-001",
        "registries/ROLE_EXECUTION_REGISTRY.csv": "refuter@0.2.0--RT-20260811-009",
        "registries/CLAIM_BOUNDARY_REGISTRY.csv": "CB-V22-P4-T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-REFUTER-STRESS-001",
        "registries/TEX_SOURCE_REGISTRY.csv": "TEX-V22-P4-T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-REFUTER-STRESS-V1",
        "registries/MARKDOWN_SOURCE_REGISTRY.csv": "MD-V22-P4-T02-B2-PARENT-FUSION-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-REFUTER-STRESS-V1",
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

    completion = parsed.get("completion", {})
    handoff = parsed.get("handoff", {})
    plan_result = completion.get("plan_result", {})
    check(
        completion.get("objective_result") == "scoped_obstruction"
        and plan_result.get("selected_successor_packet_id") == SUCCESSOR
        and plan_result.get("selected_successor_executed") is False
        and completion.get("parent_child_synthesis", {})
        .get("conflict_review", {})
        .get("unresolved_conflicts")
        == []
        and handoff.get("handoff_id") == "handoff-1023"
        and handoff.get("completion_sha256") == sha256(yaml_paths["completion"])
        and handoff.get("required_next_packet", {}).get("executed") is False,
        "completion_and_handoff",
        f"completion={completion.get('objective_result')} handoff={handoff.get('handoff_id')} successor={plan_result.get('selected_successor_executed')}",
        checks,
    )

    program = parse_yaml(ROOT / "research_control/program_state.yaml", unique=False)
    program_result = program.get(
        "v22_p4_t02_b2_source_law_space_robust_invariance_protection_refuter_stress",
        {},
    )
    check(
        program.get("active_task_id") == "RT-20260811-009"
        and program.get("active_agent_job_id") == "AJ-RT-20260811-009-001"
        and program.get("latest_handoff_id") == "handoff-1023"
        and program_result.get("decisive_result") == "scoped_obstruction"
        and program_result.get("obstruction_id") == OBSTRUCTION
        and program_result.get("active_freeze_count") == 6
        and program_result.get("selected_successor_packet_id") == SUCCESSOR
        and program_result.get("selected_successor_executed") is False
        and program_result.get("handoff_sha256") == sha256(yaml_paths["handoff"]),
        "program_state",
        f"task={program.get('active_task_id')} handoff={program.get('latest_handoff_id')} result={program_result.get('decisive_result')}",
        checks,
    )

    backlog_path = ROOT / "research_control/design/v22_recommendation_backlog.yaml"
    backlog = parse_yaml(backlog_path, unique=False)
    p4 = next(
        (
            row
            for row in backlog.get("items", [])
            if row.get("plan_task_id") == "P4-T02"
        ),
        {},
    )
    check(
        p4.get("runtime_active_task_id") == "RT-20260811-009"
        and p4.get("runtime_active_job_id") == "AJ-RT-20260811-009-001"
        and p4.get(
            "runtime_source_law_space_robust_invariance_protection_refuter_stress_executed"
        )
        is True
        and p4.get(
            "runtime_source_law_space_robust_invariance_protection_refuter_stress_result"
        )
        == "scoped_obstruction"
        and p4.get("runtime_selected_next_packet_id") == SUCCESSOR
        and p4.get("runtime_selected_next_role_family")
        == "theoretical-continuation-selector@0.1.0"
        and p4.get(
            "runtime_source_law_space_robust_invariance_protection_post_refuter_theoretical_selector_executed"
        )
        is False,
        "v22_backlog_runtime",
        f"task={p4.get('runtime_active_task_id')} result={p4.get('runtime_source_law_space_robust_invariance_protection_refuter_stress_result')} next={p4.get('runtime_selected_next_packet_id')}",
        checks,
    )

    authority = matrix.get("authority_limits", {})
    check(
        authority.get("source_law_adopted") is False
        and authority.get("canonical_ontology_modified") is False
        and authority.get("adequacy_reevaluated") is False
        and authority.get("b2_activated_or_disposed") is False
        and authority.get("p4_t03_unlocked") is False
        and authority.get("distance_to_gr_changed") is False
        and authority.get("proof_authority") is False
        and authority.get("publication_authorized") is False
        and authority.get("push_authorized") is False
        and authority.get("external_action_authorized") is False,
        "authority_and_downstream_locks",
        json.dumps(authority, sort_keys=True),
        checks,
    )

    status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    return {
        "schema_id": (
            "v22_p4_t02_b2_source_law_space_robust_invariance_protection_"
            "refuter_stress_validation_v1"
        ),
        "task_id": "RT-20260811-009",
        "job_id": "AJ-RT-20260811-009-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "fail_count": sum(row["status"] == "FAIL" for row in checks),
        "checks": checks,
        "authority_limits": {
            "validator_pass_is_scientific_authority": False,
            "fixed_tuple_theorem_preserved": True,
            "written_syntax_source_purity_verdict_preserved": True,
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
            "schema_id": (
                "v22_p4_t02_b2_source_law_space_robust_invariance_protection_"
                "refuter_stress_compact_receipt_v1"
            ),
            "task_id": report["task_id"],
            "job_id": report["job_id"],
            "status": report["status"],
            "check_count": report["check_count"],
            "pass_count": report["pass_count"],
            "fail_count": report["fail_count"],
            "validation_sha256": sha256(REPORT),
            "model_sha256": sha256(MODEL),
        }
        COMPACT.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
