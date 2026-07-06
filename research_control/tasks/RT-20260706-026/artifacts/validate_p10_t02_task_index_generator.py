#!/usr/bin/env python3
"""Task-local smoke validator for the v17 P10-T02 task-index generator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_task_index  # noqa: E402


REPORT_PATH = (
    "research_control/tasks/RT-20260706-026/artifacts/"
    "p10_t02_task_index_generator_report.json"
)
REQUIRED_OUTPUTS = [
    "scripts/research_control/render_task_index.py",
    render_task_index.DEFAULT_CSV_PATH,
    render_task_index.DEFAULT_MARKDOWN_PATH,
    render_task_index.DEFAULT_WIKI_MARKDOWN_PATH,
]


def read_csv_header(path: Path) -> list[str]:
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    return first_line.split(",")


def validate() -> dict[str, Any]:
    index = render_task_index.build_index(REPO_ROOT)
    csv_text, markdown_text, wiki_text = render_task_index.rendered_texts(index)
    errors: list[str] = []
    output_checks: dict[str, dict[str, Any]] = {}

    expected_text = {
        render_task_index.DEFAULT_CSV_PATH: csv_text,
        render_task_index.DEFAULT_MARKDOWN_PATH: markdown_text,
        render_task_index.DEFAULT_WIKI_MARKDOWN_PATH: wiki_text,
    }
    for rel_path in REQUIRED_OUTPUTS:
        path = REPO_ROOT / rel_path
        exists = path.exists()
        output_checks[rel_path] = {
            "exists": exists,
            "sha256": render_task_index.file_hash(path) if exists else "",
        }
        if not exists:
            errors.append(f"missing required output: {rel_path}")
            continue
        if rel_path in expected_text and path.read_text(encoding="utf-8") != expected_text[rel_path]:
            errors.append(f"stale generated output: {rel_path}")

    csv_path = REPO_ROOT / render_task_index.DEFAULT_CSV_PATH
    if csv_path.exists() and read_csv_header(csv_path) != render_task_index.HEADER:
        errors.append("TASK_INDEX.csv header does not match task_index_schema_v1")
    if index["row_count"] <= 0:
        errors.append("renderer produced no task rows")
    if "Generated navigation support only" not in markdown_text:
        errors.append("generated Markdown is missing the non-authority notice")

    return {
        "schema_id": "p10_t02_task_index_generator_smoke_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "required_header": render_task_index.HEADER,
        "row_count": index["row_count"],
        "issue_count": index["issue_count"],
        "source_fingerprint": index["source_fingerprint"],
        "outputs": output_checks,
        "authority_notice": render_task_index.AUTHORITY_NOTICE,
        "p10_t03_still_required": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true", help="write the JSON report")
    parser.add_argument("--json", action="store_true", help="print the JSON report")
    args = parser.parse_args(argv)

    report = validate()
    if args.write_report:
        path = REPO_ROOT / REPORT_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
