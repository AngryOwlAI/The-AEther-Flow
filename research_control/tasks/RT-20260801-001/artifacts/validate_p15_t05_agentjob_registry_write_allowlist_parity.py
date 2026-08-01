#!/usr/bin/env python3
"""Validate the bounded P15-T05 AgentJob registry allowlist repair."""

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
    "research_control/tasks/RT-20260801-001/artifacts/"
    "p15_t05_agentjob_registry_write_allowlist_parity_receipt.json"
)
SOURCE_JOB_PATH = (
    "research_control/tasks/RT-20260731-010/jobs/"
    "AJ-RT-20260731-010-001.yaml"
)
SOURCE_ROLE_PATH = (
    "research_control/tasks/RT-20260731-010/roles/"
    "gate-chair@0.1.0--RT-20260731-010.yaml"
)
SOURCE_JOB_ID = "AJ-RT-20260731-010-001"
SOURCE_ROLE_REF = "gate-chair@0.1.0--RT-20260731-010"
EXPECTED_ORDER = [
    "research_control/approvals/approval-20260731-003.yaml",
    "research_control/tasks/RT-20260731-010/**",
    "research_control/handoffs/handoff-0932.yaml",
    "research_control/handoffs/handoff-0932.md",
    "research_control/program_state.yaml",
    "research_control/current_frontier.md",
    "research_control/design/frontier_theorem_inventory.md",
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
    "wiki/pdf/**",
    "wiki/tex/**",
]
PROTECTED_HASHES = {
    SOURCE_JOB_PATH:
        "990e3316fca224499721921ea50e8bb85b153002fbf5f5b4d5407d22db1962a2",
    SOURCE_ROLE_PATH:
        "b3081e8892d428ede1a6c66e157e2b6667e38b2403e656ba87f77c762d615670",
    "research_control/tasks/RT-20260731-010/jobs/completions/"
    "AJC-AJ-RT-20260731-010-001.yaml":
        "57e72816d69f68d8af72939286e07e1217de7c0907170b12b3939d36d62af313",
    "research_control/handoffs/handoff-0932.yaml":
        "6c2a19bd25c6f1be948ed39c8acfc69969e023cabd8a6b585682270e1dc1ca5e",
    "research_control/handoffs/handoff-0932.md":
        "388387928034ba577c7ecda4e5be53bdc683b126487c747467f8a87fbb9cdfd2",
    "research_control/tasks/RT-20260731-010/artifacts/"
    "p15_t05_gate_e_no_manuscript_disposition_v1.tex":
        "daa8533b40e82ee2a1bf5ef2e78b6bd5bd9cc1ffa4c0e27444188bed47e59a5d",
    "research_control/tasks/RT-20260731-010/artifacts/"
    "p15_t05_claim_to_evidence_map_v1.yaml":
        "dfbce44f48f8bd04ad8b9657e63a8ef9767f4cab221d518fc2f5b0ebb9dfbef0",
    "research_control/tasks/RT-20260731-010/artifacts/"
    "p15_t05_reproducibility_manifest_v1.yaml":
        "3c592c93af22b28e1a72be979e9512efeddd16b714e7472d837fa11cf492a22e",
    "research_control/tasks/RT-20260731-010/artifacts/"
    "p15_t05_gate_e_no_manuscript_compact_receipt_v1.json":
        "1314d1a8e63b43e86e2c3825a326bd99b00b0400b23f86c74d07de3bd493c5b6",
    "research_control/tasks/RT-20260731-010/artifacts/"
    "p15_t05_gate_e_no_manuscript_validation_v1.json":
        "c0340ba0c3bc25dc9e5f0eb43558f38f3b5f1139941c7b89eea1384c05e3a24b",
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
            "schema_id": "p15_t05_agentjob_registry_write_allowlist_parity_receipt_v1",
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
    checks["all_four_representations_equal"] = all(
        value == EXPECTED_ORDER for value in representations.values()
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
    if checks["active_task_id"] != "RT-20260801-001":
        errors.append("active_task_id_mismatch")
    if checks["latest_handoff_id"] != "handoff-0933":
        errors.append("latest_handoff_id_mismatch")
    if checks["next_plan_task_id"] != "P13-T02":
        errors.append("next_plan_task_id_mismatch")
    if checks["next_worker_skill"] != "improve-project-system":
        errors.append("next_worker_skill_mismatch")

    return {
        "schema_id": "p15_t05_agentjob_registry_write_allowlist_parity_receipt_v1",
        "task_id": "RT-20260801-001",
        "job_id": "AJ-RT-20260801-001-001",
        "strategy_id": "repair_p15_t05_agentjob_registry_allowlist_parity_v1",
        "source_job_id": SOURCE_JOB_ID,
        "expected_allowed_write_path_count": len(EXPECTED_ORDER),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": checks,
        "authority_limits": {
            "p15_t05_reexecuted": False,
            "p13_t02_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "publication_or_push_authorized": False,
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
