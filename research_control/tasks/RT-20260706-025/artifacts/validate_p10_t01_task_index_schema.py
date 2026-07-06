#!/usr/bin/env python3
"""Validate the v17 P10-T01 task-index schema packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = REPO_ROOT / "research_control/design/task_index_schema_v1.md"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260706-025/artifacts/p10_t01_task_index_schema_report.json"
)

REQUIRED_HEADER = (
    "task_id,parent_task_id,created_at,closed_at,task_type,status,"
    "target_derivation_milestone,milestone_burden,role_family,physics_delta,"
    "ledger_rows_changed,artifact_count,next_recommended_action,"
    "validation_status,completion_path"
)

REQUIRED_PHRASES = [
    "<!-- authority: control -->",
    "# Task Index Schema v1",
    REQUIRED_HEADER,
    "research_control/tasks/TASK_INDEX.csv",
    "research_control/tasks/TASK_INDEX.md",
    "wiki/indexes/research_control_task_index.md",
    "Generated wiki notes, local Obsidian notes, SQLite retrieval indexes, and",
    "P10-T01 defines the schema only. It does not create the generated task index.",
    "Rows may not be used to:",
    "completed derivation",
    "P10-T02 may create the renderer",
]


def validate() -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    if not SCHEMA_PATH.exists():
        errors.append(f"missing schema path: {SCHEMA_PATH.relative_to(REPO_ROOT)}")
        text = ""
    else:
        text = SCHEMA_PATH.read_text(encoding="utf-8")

    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            errors.append(f"schema missing required phrase: {phrase}")

    if text.count(REQUIRED_HEADER) != 1:
        errors.append("required CSV header must appear exactly once")

    if "## Required Row Fields" not in text or "| `task_id` |" not in text:
        errors.append("required row-field table is missing task_id row")

    if "## Generation Rules" not in text or "## Validation Rules" not in text:
        errors.append("generation and validation rule sections are required")

    forbidden_authority_phrases = [
        "proves matter coupling",
        "derives Einstein equations",
        "authorizes benchmark promotion",
    ]
    for phrase in forbidden_authority_phrases:
        if phrase in text:
            errors.append(f"schema contains forbidden promotion phrase: {phrase}")

    return {
        "schema_id": "p10_t01_task_index_schema_validation_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "schema_path": str(SCHEMA_PATH.relative_to(REPO_ROOT)),
        "required_header": REQUIRED_HEADER,
        "physics_proof_authority": False,
        "physics_delta": False,
        "generated_task_index_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"P10-T01 task-index schema validation: {report['status']}")
        for error in report["errors"]:
            print(f"- {error}")

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
