#!/usr/bin/env python3
"""Validate the bounded RT-008 AgentJob registry ordered-allowlist repair."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_PATH = REPO_ROOT / (
    "research_control/tasks/RT-20260730-009/artifacts/"
    "rt008_agentjob_registry_ordered_write_allowlist_parity_receipt.json"
)
SOURCE_JOB_PATH = (
    "research_control/tasks/RT-20260730-008/jobs/"
    "AJ-RT-20260730-008-001.yaml"
)
SOURCE_ROLE_PATH = (
    "research_control/tasks/RT-20260730-008/roles/"
    "candidate-constructor@0.2.0--RT-20260730-008.yaml"
)
SOURCE_JOB_ID = "AJ-RT-20260730-008-001"
SOURCE_ROLE_REF = "candidate-constructor@0.2.0--RT-20260730-008"
EXPECTED_ORDER = [
    "research_control/tasks/RT-20260730-008/**",
    "research_control/handoffs/handoff-0915.yaml",
    "research_control/handoffs/handoff-0915.md",
    "research_control/program_state.yaml",
    "research_control/current_frontier.md",
    "research_control/tasks/TASK_INDEX.csv",
    "research_control/tasks/TASK_INDEX.md",
    "registries/AGENT_JOB_REGISTRY.csv",
    "registries/CLAIM_BOUNDARY_REGISTRY.csv",
    "registries/DIRECTOR_DECISION_REGISTRY.csv",
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "registries/MARKDOWN_SOURCE_REGISTRY.csv",
    "registries/PDF_DERIVATIVE_REGISTRY.csv",
    "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv",
    "registries/RESEARCH_TASK_REGISTRY.csv",
    "registries/ROLE_EXECUTION_REGISTRY.csv",
    "registries/TEX_SOURCE_REGISTRY.csv",
    "registries/CONTENT_SEMANTIC_REGISTRY*",
    "registries/FILE_OBJECT_REGISTRY*",
    "registries/OBJECT_RELATIONSHIP_REGISTRY*",
    "registries/OBSIDIAN_VAULT_REGISTRY*",
    "registries/WIKI_ARTIFACT_REGISTRY*",
    "FOLDER_MAP.md",
    "output/**",
    "wiki/indexes/**",
    "wiki/markdown/**",
    "wiki/tex/**",
]
PROTECTED_HASHES = {
    SOURCE_JOB_PATH:
        "ada7b470952ebbbb520ed7905949ccb10ec2295373c92f0c97413b0462983499",
    SOURCE_ROLE_PATH:
        "c250e1fbf6558856a52e25af6b2b6448cc38472ef7c370a8078f9a3a391b3a3f",
    "research_control/tasks/RT-20260730-008/jobs/completions/"
    "AJC-AJ-RT-20260730-008-001.yaml":
        "1ad072d427eb2782f974a329ba30d40a390c6c0a5793ebfd22aea851225f3acc",
    "research_control/handoffs/handoff-0915.yaml":
        "9769db1d0b36fae321d899d9e5012aa44d2b006fa0f13e10ffc3276b9aeb4023",
    "research_control/handoffs/handoff-0915.md":
        "9df1327eb300def92f57dc8302344ea65718d92104868d4f84dd098230fa3386",
    "research_control/tasks/RT-20260730-008/artifacts/"
    "finite_source_null_background_benchmark_attempt_v1.tex":
        "6b3a4b386567139f4e9a88b0ce61698b681d2193d9b052672638fedbc8bf94b3",
    "research_control/tasks/RT-20260730-008/artifacts/"
    "p9_t02_vacuum_minkowski_case_v1.yaml":
        "2fadb19c5849f1da5843c0e0599dbdc31790eab46587ce6718abbf4d3a0be79c",
    "research_control/tasks/RT-20260730-008/artifacts/"
    "p9_t02_source_output_seal_v1.json":
        "71b7dfb67b40d748867a5c49abf7b50c684f9e4a7f5962d8787a960a3dc541dd",
    "research_control/tasks/RT-20260730-008/artifacts/"
    "p9_t02_provenance_dag_v1.yaml":
        "163d9154e81a7249cdd145841e28c0313fd4ee7b4dccb9621f29bb6b61633e7e",
    "research_control/tasks/RT-20260730-008/artifacts/"
    "p9_t02_target_exposure_ledger_v1.yaml":
        "2bcb4a9c82508af58e680ea488e862e74a379ac82bc66253db4d120c71b3ac3b",
    "research_control/tasks/RT-20260730-008/artifacts/"
    "p9_t02_benchmark_case_receipt_v1.json":
        "49172f707fbaa243462788a2c22a63e19fcdd3ac0656142281fc1f013c8d884b",
    "research_control/tasks/RT-20260730-008/artifacts/"
    "p9_t02_benchmark_case_validation_v1.json":
        "80593070d175a116e7952fac1bba008b60c54541be0db388ee4ecc1074975c5f",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(relative_path: str) -> dict[str, Any]:
    value = yaml.safe_load((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative_path} must contain a YAML mapping")
    return value


def registry_row(name: str, key: str, value: str) -> dict[str, str]:
    with (REPO_ROOT / "registries" / name).open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = [row for row in csv.DictReader(handle) if row.get(key) == value]
    if len(rows) != 1:
        raise ValueError(f"{name} expected one {key}={value} row, found {len(rows)}")
    return rows[0]


def split_paths(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def evaluate() -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, Any] = {}
    try:
        source_job = load_yaml(SOURCE_JOB_PATH)
        source_role = load_yaml(SOURCE_ROLE_PATH)
        job_row = registry_row(
            "AGENT_JOB_REGISTRY.csv", "job_id", SOURCE_JOB_ID
        )
        role_row = registry_row(
            "ROLE_EXECUTION_REGISTRY.csv",
            "execution_role_ref",
            SOURCE_ROLE_REF,
        )
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {
            "schema_id": "rt008_agentjob_registry_ordered_write_allowlist_parity_receipt_v1",
            "status": "FAIL",
            "errors": [str(exc)],
            "checks": {},
        }

    representations = {
        "source_agent_job": source_job.get("allowed_write_paths"),
        "source_execution_role": source_role.get("allowed_write_paths"),
        "agent_job_registry": split_paths(job_row.get("allowed_write_paths", "")),
        "role_execution_registry": split_paths(
            role_row.get("allowed_write_paths", "")
        ),
    }
    for name, observed in representations.items():
        checks[f"{name}_path_count"] = (
            len(observed) if isinstance(observed, list) else None
        )
        checks[f"{name}_matches_expected_order"] = observed == EXPECTED_ORDER
        if observed != EXPECTED_ORDER:
            errors.append(f"ordered_allowlist_mismatch:{name}")
    checks["ordered_representation_count"] = len(representations)
    checks["all_four_representations_equal"] = (
        all(value == EXPECTED_ORDER for value in representations.values())
    )

    protected: dict[str, dict[str, Any]] = {}
    for relative_path, expected in PROTECTED_HASHES.items():
        path = REPO_ROOT / relative_path
        observed = sha256(path) if path.is_file() else None
        protected[relative_path] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": observed == expected,
        }
        if observed != expected:
            errors.append(f"protected_hash_mismatch:{relative_path}")
    checks["protected_hashes"] = protected

    try:
        program_state = load_yaml("research_control/program_state.yaml")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(str(exc))
        program_state = {}
    checks["active_task_id"] = program_state.get("active_task_id")
    checks["latest_handoff_id"] = program_state.get("latest_handoff_id")
    checks["next_plan_task_id"] = program_state.get("next_plan_task_id")
    checks["next_worker_skill"] = program_state.get("next_worker_skill")
    if checks["active_task_id"] != "RT-20260730-009":
        errors.append("active_task_id_mismatch")
    if checks["latest_handoff_id"] != "handoff-0916":
        errors.append("latest_handoff_id_mismatch")
    if checks["next_plan_task_id"] != "P9-T03":
        errors.append("next_plan_task_id_mismatch")
    if checks["next_worker_skill"] != "continue-research":
        errors.append("next_worker_skill_mismatch")

    return {
        "schema_id": "rt008_agentjob_registry_ordered_write_allowlist_parity_receipt_v1",
        "task_id": "RT-20260730-009",
        "job_id": "AJ-RT-20260730-009-001",
        "strategy_id": "repair_rt008_agentjob_registry_ordered_write_allowlist_parity_v1",
        "source_job_id": SOURCE_JOB_ID,
        "expected_allowed_write_path_count": len(EXPECTED_ORDER),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": checks,
        "authority_limits": {
            "p9_t02_reexecuted": False,
            "p9_t03_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
