#!/usr/bin/env python3
"""Collect validation artifacts for local and CI review.

This collector is operational receipt tooling only. A PASS summary means the
configured validation commands completed in the current repository state. It
does not establish physics proof authority, promote a physics claim, authorize
source-law adoption, or change Distance-to-GR status.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
SUMMARY_SCHEMA_ID = "research_control_validation_summary_v1"
FULL_VALIDATION_SCRIPT = Path("scripts/research_control/run_full_research_control_validation.py")
DEFAULT_JSON_PATH = Path("output/validation_summary.json")
DEFAULT_MARKDOWN_PATH = Path("output/validation_summary.md")


def python_bin() -> str:
    return ".venv/bin/python"


def run_full_validation_report(
    repo_root: Path,
    *,
    include_smoke_tests: bool = False,
    tail_chars: int = 1500,
) -> dict[str, Any]:
    command = [
        python_bin(),
        str(FULL_VALIDATION_SCRIPT),
        "--json",
        "--tail-chars",
        str(tail_chars),
    ]
    if include_smoke_tests:
        command.append("--include-smoke-tests")
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if not completed.stdout.strip():
        raise RuntimeError(
            "full validation command produced no JSON output "
            f"(exit={completed.returncode}, stderr={completed.stderr.strip()})"
        )
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"full validation command produced invalid JSON: {exc}") from exc
    if not isinstance(report, dict):
        raise RuntimeError("full validation command did not produce a JSON object")
    report["_collector_source_command"] = command
    report["_collector_source_returncode"] = completed.returncode
    report["_collector_source_stderr_tail"] = completed.stderr[-tail_chars:] if tail_chars > 0 else completed.stderr
    return report


def load_source_report(path: Path) -> dict[str, Any]:
    report = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return report


def command_status_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for command in report.get("commands", []):
        if not isinstance(command, dict):
            continue
        rows.append(
            {
                "label": command.get("label", ""),
                "status": command.get("status", ""),
                "returncode": command.get("returncode"),
                "required": bool(command.get("required", False)),
                "advisory": bool(command.get("advisory", False)),
                "authority_level": command.get("authority_level", ""),
                "purpose": command.get("purpose", ""),
                "command": command.get("command", []),
            }
        )
    return rows


def count_rows(rows: list[dict[str, Any]], *, required: bool | None = None, advisory: bool | None = None) -> int:
    selected = rows
    if required is not None:
        selected = [row for row in selected if row["required"] is required]
    if advisory is not None:
        selected = [row for row in selected if row["advisory"] is advisory]
    return len(selected)


def count_pass(rows: list[dict[str, Any]], *, required: bool | None = None, advisory: bool | None = None) -> int:
    selected = rows
    if required is not None:
        selected = [row for row in selected if row["required"] is required]
    if advisory is not None:
        selected = [row for row in selected if row["advisory"] is advisory]
    return sum(1 for row in selected if row["status"] == "PASS")


def build_summary(report: dict[str, Any], *, repo_root: Path) -> dict[str, Any]:
    rows = command_status_rows(report)
    required_non_advisory_total = count_rows(rows, required=True, advisory=False)
    required_non_advisory_passed = count_pass(rows, required=True, advisory=False)
    advisory_total = count_rows(rows, advisory=True)
    advisory_passed = count_pass(rows, advisory=True)
    status = "PASS" if report.get("status") == "PASS" and required_non_advisory_total == required_non_advisory_passed else "FAIL"
    return {
        "schema_id": SUMMARY_SCHEMA_ID,
        "status": status,
        "source_report_schema_id": report.get("schema_id", ""),
        "source_generated_at": report.get("generated_at", ""),
        "source_command": report.get("_collector_source_command", []),
        "source_returncode": report.get("_collector_source_returncode"),
        "repo_root": str(repo_root),
        "operational_receipt_only": True,
        "no_physics_delta": True,
        "physics_proof_authority": False,
        "distance_to_gr_delta": "none",
        "boundary_note": (
            "Validation artifacts are operational receipts only. They are not "
            "physics proof authority, source-law adoption, benchmark promotion, "
            "Gate Chair verdict, or completed-derivation evidence."
        ),
        "required_failure_labels": report.get("required_failure_labels", []),
        "advisory_failure_labels": report.get("advisory_failure_labels", []),
        "required_check_coverage": report.get("required_check_coverage", {}),
        "command_counts": {
            "total": len(rows),
            "required_non_advisory_total": required_non_advisory_total,
            "required_non_advisory_passed": required_non_advisory_passed,
            "advisory_total": advisory_total,
            "advisory_passed": advisory_passed,
        },
        "commands": rows,
    }


def markdown_bool(value: Any) -> str:
    return "true" if bool(value) else "false"


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Validation Summary",
        "",
        "Authority: operational receipt only. This summary is not physics proof authority, source-law adoption, benchmark promotion, Gate Chair verdict, or completed-derivation evidence.",
        "",
        f"- Status: `{summary.get('status', '')}`",
        f"- Source report schema: `{summary.get('source_report_schema_id', '')}`",
        f"- Source generated at: `{summary.get('source_generated_at', '')}`",
        f"- No physics delta: `{markdown_bool(summary.get('no_physics_delta'))}`",
        f"- Physics proof authority: `{markdown_bool(summary.get('physics_proof_authority'))}`",
        "",
        "## Command Status",
        "",
        "| Label | Status | Required | Advisory | Authority level |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in summary.get("commands", []):
        lines.append(
            "| {label} | {status} | {required} | {advisory} | {authority} |".format(
                label=row.get("label", ""),
                status=row.get("status", ""),
                required=markdown_bool(row.get("required")),
                advisory=markdown_bool(row.get("advisory")),
                authority=row.get("authority_level", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Coverage",
            "",
        ]
    )
    for key, value in sorted(summary.get("required_check_coverage", {}).items()):
        lines.append(f"- `{key}`: `{markdown_bool(value)}`")
    lines.append("")
    return "\n".join(lines)


def write_outputs(summary: dict[str, Any], json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(summary), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--source-report", type=Path, help="Summarize an existing full validation JSON report instead of running it.")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--output-markdown", type=Path, default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--include-smoke-tests", action="store_true")
    parser.add_argument("--tail-chars", type=int, default=1500)
    parser.add_argument("--json", action="store_true", help="Print summary JSON to stdout.")
    parser.add_argument("--markdown", action="store_true", help="Print summary Markdown to stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    if args.source_report:
        report = load_source_report(args.source_report)
    else:
        report = run_full_validation_report(
            repo_root,
            include_smoke_tests=args.include_smoke_tests,
            tail_chars=args.tail_chars,
        )
    summary = build_summary(report, repo_root=repo_root)
    json_path = args.output_json if args.output_json.is_absolute() else repo_root / args.output_json
    markdown_path = args.output_markdown if args.output_markdown.is_absolute() else repo_root / args.output_markdown
    write_outputs(summary, json_path, markdown_path)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    if args.markdown:
        sys.stdout.write(render_markdown(summary))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
