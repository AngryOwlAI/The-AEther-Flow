#!/usr/bin/env python3
"""Focused validator for RT-20260815-007."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[4]
TASK = REPO / "research_control/tasks/RT-20260815-007"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_validation.json"
COMPACT = ART / "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_compact_receipt.json"
RESULT = "canonical_open_event_fibration_typing_descent_theorem"
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-KSTAR-STANDALONE-LOCAL-BRIDGE-IRRELEVANCE",
    "NDCL-V22-P4T02-B2-PROJECTIVE-CONORMAL-ROBUST-SELECTION-CONFORMAL-LIFT",
}
BURDENS = {
    "Source ontology primitives",
    "Source equivalence EqSrc",
    "RetainH",
    "GenH",
    "ObsLoc_lc",
    "Resp_lc",
    "M_src",
    "g_eff",
    "matter coupling",
    "Einstein equations",
    "finite-variation robustness",
    "benchmark promotion",
    "Gate Chair status",
    "current route freeze or hard-fail status",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def csv_row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get(key) == value:
                return row
    return {}


def validate() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, bool] = {}
    paths = {
        "task": TASK / "00_TASK.yaml",
        "decision": TASK / "DDR-20260815-007.md",
        "job": TASK / "jobs/AJ-RT-20260815-007-001.yaml",
        "role": TASK / "roles/ontology-formalizer@0.2.0--RT-20260815-007.yaml",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260815-007-001.yaml",
        "math_child": ART / "child_phys_math_p4_t02_b2_canonical_source_open_event_fibration_typing_descent.yaml",
        "phil_child": ART / "child_phys_phil_p4_t02_b2_canonical_source_open_event_fibration_typing_descent.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_canonical_source_open_event_fibration_typing_descent.yaml",
        "result": ART / "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_theorem_result_v1.yaml",
        "manifest": ART / "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_provenance_manifest_v1.yaml",
        "tex": ART / "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_theorem_v1.tex",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_canonical_source_open_event_fibration_typing_descent.md",
        "compile": ART / "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_latex_compile_receipt.json",
        "model": ART / "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_theorem_model.py",
        "handoff": REPO / "research_control/handoffs/handoff-1041.yaml",
    }
    missing = [str(path.relative_to(REPO)) for path in paths.values() if not path.exists()]
    checks["all_expected_artifacts_exist"] = not missing
    errors.extend(f"missing: {item}" for item in missing)

    yaml_names = ("task", "job", "role", "completion", "math_child", "phil_child", "conflict", "result", "manifest", "handoff")
    loaded: dict[str, dict[str, Any]] = {}
    for name in yaml_names:
        if not paths[name].exists():
            continue
        try:
            loaded[name] = load_yaml(paths[name])
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")
    checks["unique_key_yaml_parse"] = len(loaded) == len(yaml_names)

    if all(name in loaded for name in ("task", "job", "role")):
        checks["terminal_control_state"] = (
            loaded["task"].get("status") == "completed"
            and loaded["task"].get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
            and loaded["task"].get("claim_boundary", {}).get("boundary_status") == "completed_checkpoint_pending"
            and loaded["job"].get("status") == "completed"
            and loaded["job"].get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
            and loaded["role"].get("status") == "expired"
            and loaded["role"].get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
        )

    if "result" in loaded:
        result = loaded["result"]
        checks["exclusive_result"] = (
            result.get("result_type") == RESULT
            and result.get("result_count") == 1
            and result.get("selected_successor", {}).get("status") == "selected_not_executed"
            and result.get("selected_successor", {}).get("executed") is False
        )
        checks["formal_contract_counts"] = (
            len(result.get("formal_domains", [])) == 10
            and len(result.get("formal_objects", [])) == 12
            and len(result.get("formal_maps", [])) == 10
            and len(result.get("theorem_results", [])) == 5
            and len(result.get("proof_obligations", [])) == 14
            and len(result.get("failure_branches", [])) == 12
        )
        checks["eight_freezes"] = set(result.get("preserved_freeze_labels", [])) == FREEZES
        matrix = result.get("distance_to_gr_status", [])
        checks["fourteen_no_delta_rows"] = (
            len(matrix) == 14
            and {row.get("burden") for row in matrix} == BURDENS
            and all(row.get("status") == "no_delta" for row in matrix)
        )
        authority = result.get("authority_limits", {})
        required_false = (
            "general_prop_or_f_prop_constructed",
            "occurrence_law_constructed",
            "source_extension_adopted",
            "canonical_ontology_modified",
            "physical_event_semantics_assigned",
            "physical_probability_assigned",
            "d7_reevaluated",
            "b2_activated",
            "p4_t03_unlocked",
            "g_eff_constructed",
            "distance_to_gr_changed",
            "global_no_go_claimed",
            "physics_promotion_authorized",
            "proof_authority",
            "publication_authorized",
            "push_authorized",
            "external_action_authorized",
        )
        checks["authority_limits"] = all(authority.get(key) is False for key in required_false)

    if "conflict" in loaded:
        conflict = loaded["conflict"]
        checks["child_consensus_and_no_conflict"] = (
            conflict.get("parent_result_type") == RESULT
            and conflict.get("child_consensus") is True
            and conflict.get("unresolved_blocking_conflict_count") == 0
        )

    if "manifest" in loaded:
        manifest = loaded["manifest"]
        entries = manifest.get("governing_sources", []) + manifest.get("fused_artifacts", [])
        mismatches = []
        for item in entries:
            source = REPO / str(item.get("path", ""))
            if not source.exists() or sha256(source) != str(item.get("sha256", "")):
                mismatches.append(str(item.get("path", "")))
        checks["source_manifest_hashes"] = bool(entries) and not mismatches
        errors.extend(f"source hash mismatch: {item}" for item in mismatches)

    if paths["model"].exists():
        run = subprocess.run(
            [sys.executable, str(paths["model"])],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        try:
            model = json.loads(run.stdout)
        except json.JSONDecodeError:
            model = {}
        checks["exact_model_24_of_24"] = (
            run.returncode == 0
            and model.get("all_pass") is True
            and model.get("check_count") == 24
            and model.get("pass_count") == 24
            and model.get("result_type") == RESULT
        )

    if paths["compile"].exists():
        compile_receipt = json.loads(paths["compile"].read_text(encoding="utf-8"))
        checks["latex_compile_receipt"] = (
            compile_receipt.get("status") == "PASS"
            and compile_receipt.get("compiler_exit_code") == 0
            and compile_receipt.get("page_count") == 3
            and compile_receipt.get("source_sha256") == sha256(paths["tex"])
        )

    if "completion" in loaded:
        completion = loaded["completion"]
        checks["completion_identity"] = (
            completion.get("completion_id") == "AJC-AJ-RT-20260815-007-001"
            and completion.get("result", {}).get("result_type") == RESULT
            and completion.get("validation_status") == "PASS_PRECHECKPOINT_STAGING_REQUIRED"
        )
    if "handoff" in loaded:
        handoff = loaded["handoff"]
        checks["handoff_identity"] = (
            handoff.get("handoff_id") == "handoff-1041"
            and handoff.get("task_id") == "RT-20260815-007"
            and handoff.get("result", {}).get("result_type") == RESULT
            and handoff.get("required_next_packet", {}).get("executed") is False
        )

    registry_specs = (
        ("RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260815-007", "status", "completed"),
        ("DIRECTOR_DECISION_REGISTRY.csv", "decision_id", "DDR-20260815-007", "status", "completed"),
        ("AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260815-007-001", "status", "completed"),
        ("ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref", "ontology-formalizer@0.2.0--RT-20260815-007", "validation_status", "PASS_PRECHECKPOINT_STAGING_REQUIRED"),
        ("CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id", "CB-V22-P4-T02-B2-CANONICAL-SOURCE-OPEN-EVENT-FIBRATION-TYPING-DESCENT-001", "status", "completed"),
    )
    registry_ok = True
    for filename, key, value, status_key, expected in registry_specs:
        row = csv_row(REPO / "registries" / filename, key, value)
        registry_ok = registry_ok and row.get(status_key) == expected
    checks["terminal_control_registries"] = registry_ok

    tex_row = csv_row(REPO / "registries/TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V22-P4-T02-B2-CANONICAL-SOURCE-OPEN-EVENT-FIBRATION-TYPING-DESCENT-THEOREM-V1")
    md_row = csv_row(REPO / "registries/MARKDOWN_SOURCE_REGISTRY.csv", "object_id", "MD-V22-P4-T02-B2-PARENT-FUSION-CANONICAL-SOURCE-OPEN-EVENT-FIBRATION-TYPING-DESCENT-THEOREM-V1")
    checks["canonical_source_registry_rows"] = (
        tex_row.get("source_hash") == sha256(paths["tex"])
        and md_row.get("source_hash") == sha256(paths["fusion"])
    ) if paths["tex"].exists() and paths["fusion"].exists() else False

    checks["git_whitespace"] = subprocess.run(
        ["git", "diff", "--check"], cwd=REPO, capture_output=True, text=True, check=False
    ).returncode == 0

    for name, passed in checks.items():
        if not passed:
            errors.append(f"failed check: {name}")
    status = "PASS" if not errors else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_validation_v1",
        "task_id": "RT-20260815-007",
        "job_id": "AJ-RT-20260815-007-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(bool(value) for value in checks.values()),
        "checks": checks,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_compact_receipt_v1",
            "task_id": report["task_id"],
            "job_id": report["job_id"],
            "status": report["status"],
            "check_count": report["check_count"],
            "pass_count": report["pass_count"],
            "validation_sha256": sha256(REPORT),
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
