#!/usr/bin/env python3
"""Validate the v17 P11-T03 validation artifact collector outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "collect_validation_artifacts.py"
JSON_PATH = REPO_ROOT / "output" / "validation_summary.json"
MARKDOWN_PATH = REPO_ROOT / "output" / "validation_summary.md"

REQUIRED_COMMAND_LABELS = {
    "memory_validate_only",
    "current_frontier_check",
    "compact_current_frontier_check",
    "dependency_graph_check",
    "task_index_validation",
    "claim_graph_validation",
    "claim_language_changed_lint",
    "documentation_impact_validation",
    "project_improvement_signal_validation",
    "research_control_validation",
    "research_control_diff_validation",
    "whitespace_diff_check",
}


def validate() -> dict[str, Any]:
    errors: list[str] = []
    checked_paths = [str(SCRIPT_PATH.relative_to(REPO_ROOT)), str(JSON_PATH.relative_to(REPO_ROOT)), str(MARKDOWN_PATH.relative_to(REPO_ROOT))]

    if not SCRIPT_PATH.exists():
        errors.append("collector_script_missing")
        script_text = ""
    else:
        script_text = SCRIPT_PATH.read_text(encoding="utf-8")
    for phrase in [
        "research_control_validation_summary_v1",
        "operational receipt tooling only",
        "does not establish physics proof authority",
        "no_physics_delta",
        "physics_proof_authority",
    ]:
        if phrase not in script_text:
            errors.append(f"collector_missing_phrase:{phrase}")

    if not JSON_PATH.exists():
        errors.append("validation_summary_json_missing")
        summary: dict[str, Any] = {}
    else:
        summary = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if summary.get("schema_id") != "research_control_validation_summary_v1":
        errors.append("validation_summary_schema_mismatch")
    if summary.get("status") != "PASS":
        errors.append("validation_summary_status_not_pass")
    if summary.get("operational_receipt_only") is not True:
        errors.append("validation_summary_not_operational_receipt")
    if summary.get("no_physics_delta") is not True:
        errors.append("validation_summary_missing_no_physics_delta")
    if summary.get("physics_proof_authority") is not False:
        errors.append("validation_summary_allows_physics_proof_authority")
    if summary.get("distance_to_gr_delta") != "none":
        errors.append("validation_summary_distance_delta_not_none")
    if summary.get("required_failure_labels") not in ([], None):
        errors.append("validation_summary_required_failures_present")
    command_labels = {entry.get("label") for entry in summary.get("commands", []) if isinstance(entry, dict)}
    missing_labels = sorted(REQUIRED_COMMAND_LABELS - command_labels)
    if missing_labels:
        errors.append(f"validation_summary_missing_command_labels:{','.join(missing_labels)}")

    if not MARKDOWN_PATH.exists():
        errors.append("validation_summary_markdown_missing")
        markdown = ""
    else:
        markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    for phrase in [
        "# Validation Summary",
        "operational receipt only",
        "not physics proof authority",
        "No physics delta",
        "Command Status",
    ]:
        if phrase not in markdown:
            errors.append(f"validation_summary_markdown_missing_phrase:{phrase}")

    return {
        "schema_id": "p11_t03_validation_artifact_collector_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checked_paths": checked_paths,
        "required_command_labels": sorted(REQUIRED_COMMAND_LABELS),
        "operational_receipt_only": True,
        "no_physics_delta": True,
        "physics_proof_authority": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
