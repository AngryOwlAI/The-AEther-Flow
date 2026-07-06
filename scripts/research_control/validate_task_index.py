#!/usr/bin/env python3
"""Validate generated research-control task-index outputs.

This validator is project-control evidence only. A PASS confirms that the
generated task-index outputs are fresh, structurally consistent with tracked
task records, and preserve declared non-authority boundaries. It does not make
the generated task index authoritative and does not promote any physics claim.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
REPORT_SCHEMA_ID = "research_control_task_index_validation_report_v1"
VALIDATOR_NAME = "scripts/research_control/validate_task_index.py"
VALIDATOR_VERSION = "v1"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_task_index  # noqa: E402


HARD_RENDERER_ISSUES = {
    "invalid_status",
    "malformed_yaml",
    "missing_completion",
    "status_conflict",
}
SUPPORT_ONLY_ROLE_PREFIXES = (
    "documentation-curator@",
    "memory-system-maintainer@",
    "process-integrity-auditor@",
    "project-control-maintainer@",
    "project-system-director@",
    "validator-engineer@",
)
SUPPORT_ONLY_TASK_MARKERS = (
    "ci_",
    "current_frontier",
    "dashboard",
    "documentation",
    "folder",
    "github_actions",
    "memory_integration",
    "project_control",
    "publication",
    "reproducibility",
    "research_control_task_index",
    "task_index",
    "validator",
)
FORBIDDEN_OVERREAD_PATTERNS = {
    "proof_authority": (
        r"\bas proof authority\b",
        r"\bproof authority established\b",
    ),
    "benchmark_promotion": (
        r"\bbenchmark promotion (authorized|complete|completed|established|proved)\b",
        r"\bbenchmark gate chair closure (authorized|complete|completed|established)\b",
    ),
    "gate_chair_verdict_authority": (
        r"\bgate chair verdict (authorized|created|established|proved)\b",
    ),
    "einstein_equation_derivation": (
        r"\beinstein[- ]equation(?:s)? (derived|established|proved)\b",
        r"\bderives? einstein[- ]equation(?:s)?\b",
    ),
    "completed_derivation": (
        r"\bcompleted derivation (authorized|complete|completed|established|proved)\b",
        r"\bfirst-principles gr derivation complete\b",
    ),
}
NEGATING_CONTEXT = (
    "blocked",
    "does not",
    "forbidden",
    "no ",
    "not ",
    "without",
)


@dataclass
class ValidationFinding:
    code: str
    message: str
    severity: str
    path: str = ""
    task_id: str = ""
    field: str = ""
    value: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            key: value
            for key, value in {
                "code": self.code,
                "message": self.message,
                "severity": self.severity,
                "path": self.path,
                "task_id": self.task_id,
                "field": self.field,
                "value": self.value,
            }.items()
            if value
        }


@dataclass
class TaskIndexValidationReport:
    repo_root: Path
    errors: list[ValidationFinding] = field(default_factory=list)
    warnings: list[ValidationFinding] = field(default_factory=list)
    checks: dict[str, Any] = field(default_factory=dict)
    row_count: int = 0
    renderer_issue_count: int = 0
    renderer_issue_kind_counts: dict[str, int] = field(default_factory=dict)
    source_fingerprint: str = ""
    output_hashes: dict[str, str] = field(default_factory=dict)

    def error(self, code: str, message: str, **context: str) -> None:
        self.errors.append(ValidationFinding(code=code, message=message, severity="error", **context))

    def warn(self, code: str, message: str, **context: str) -> None:
        self.warnings.append(ValidationFinding(code=code, message=message, severity="warning", **context))

    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_id": REPORT_SCHEMA_ID,
            "validator_name": VALIDATOR_NAME,
            "validator_version": VALIDATOR_VERSION,
            "generated_at": utc_now(),
            "status": "PASS" if self.ok() else "FAIL",
            "repo_root": self.repo_root.as_posix(),
            "operational_receipt_only": True,
            "task_index_authority": False,
            "physics_proof_authority": False,
            "no_physics_delta": True,
            "hard_fail_count": len(self.errors),
            "warning_count": len(self.warnings),
            "row_count": self.row_count,
            "renderer_issue_count": self.renderer_issue_count,
            "renderer_issue_kind_counts": self.renderer_issue_kind_counts,
            "source_fingerprint": self.source_fingerprint,
            "output_hashes": self.output_hashes,
            "checked_failure_modes": [
                "required_header_equality",
                "generated_output_freshness",
                "csv_rows_match_tracked_renderer",
                "source_task_directory_existence",
                "completion_path_existence_for_completed_jobs",
                "task_status_compatibility",
                "support_only_physics_delta_false",
                "forbidden_task_index_overread_language",
                "historical_metadata_issues_reported_not_invented",
            ],
            "checks": self.checks,
            "errors": [finding.as_dict() for finding in self.errors],
            "warnings": [finding.as_dict() for finding in self.warnings],
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = [{key: value or "" for key, value in row.items()} for row in reader]
        return list(reader.fieldnames or []), rows


def row_signature(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{field: row.get(field, "") for field in render_task_index.HEADER} for row in rows]


def support_only_row(row: dict[str, str]) -> bool:
    role_family = row.get("role_family", "").lower()
    task_type = row.get("task_type", "").lower()
    if role_family.startswith(SUPPORT_ONLY_ROLE_PREFIXES):
        return True
    return any(marker in task_type for marker in SUPPORT_ONLY_TASK_MARKERS)


def negated_context(text: str, start: int) -> bool:
    context = text[max(0, start - 180) : start].lower()
    return any(marker in context for marker in NEGATING_CONTEXT)


def row_text(row: dict[str, str]) -> str:
    return " ".join(str(row.get(field, "")) for field in render_task_index.HEADER)


def check_forbidden_overread(report: TaskIndexValidationReport, rows: list[dict[str, str]]) -> None:
    for row in rows:
        text = row_text(row).lower()
        for code, patterns in FORBIDDEN_OVERREAD_PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text):
                    if negated_context(text, match.start()):
                        continue
                    report.error(
                        code,
                        "Generated task-index row contains forbidden positive overread language.",
                        task_id=row.get("task_id", ""),
                        value=match.group(0),
                    )


def validate_task_index(repo_root: Path = REPO_ROOT) -> TaskIndexValidationReport:
    repo_root = repo_root.resolve()
    report = TaskIndexValidationReport(repo_root=repo_root)

    index = render_task_index.build_index(repo_root)
    report.row_count = int(index["row_count"])
    report.renderer_issue_count = int(index["issue_count"])
    report.renderer_issue_kind_counts = dict(Counter(item["issue_kind"] for item in index["issues"]))
    report.source_fingerprint = str(index["source_fingerprint"])

    csv_text, markdown_text, wiki_markdown_text = render_task_index.rendered_texts(index)
    expected_rows = row_signature(index["rows"])
    freshness_checks = {
        "csv": render_task_index.compare_text(repo_root, render_task_index.DEFAULT_CSV_PATH, csv_text),
        "markdown": render_task_index.compare_text(repo_root, render_task_index.DEFAULT_MARKDOWN_PATH, markdown_text),
        "wiki_markdown": render_task_index.compare_text(
            repo_root,
            render_task_index.DEFAULT_WIKI_MARKDOWN_PATH,
            wiki_markdown_text,
        ),
    }
    report.checks["freshness"] = freshness_checks
    report.output_hashes = {
        "csv": render_task_index.sha256_text(csv_text),
        "markdown": render_task_index.sha256_text(markdown_text),
        "wiki_markdown": render_task_index.sha256_text(wiki_markdown_text),
    }
    for name, check in freshness_checks.items():
        if not check["fresh"]:
            report.error(
                "generated_output_stale",
                f"Generated task-index {name} output is not fresh.",
                path=str(check["path"]),
                value=str(check["status"]),
            )

    actual_header, actual_rows = load_csv(repo_root / render_task_index.DEFAULT_CSV_PATH)
    actual_rows = row_signature(actual_rows)
    report.checks["header"] = {
        "actual": actual_header,
        "expected": render_task_index.HEADER,
        "matches": actual_header == render_task_index.HEADER,
    }
    if actual_header != render_task_index.HEADER:
        report.error(
            "required_header_mismatch",
            "Generated task-index CSV header does not match task_index_schema_v1.",
            path=render_task_index.DEFAULT_CSV_PATH,
            value=",".join(actual_header),
        )

    report.checks["csv_rows_match_renderer"] = actual_rows == expected_rows
    if actual_rows != expected_rows:
        report.error(
            "csv_rows_mismatch",
            "Generated task-index CSV rows do not match rows derived from tracked task records.",
            path=render_task_index.DEFAULT_CSV_PATH,
        )

    for issue in index["issues"]:
        issue_kind = str(issue.get("issue_kind", ""))
        if issue_kind in HARD_RENDERER_ISSUES:
            report.error(
                issue_kind,
                str(issue.get("message", "Renderer reported a hard task-index issue.")),
                path=str(issue.get("source_path", "")),
                task_id=str(issue.get("task_id", "")),
            )
        else:
            report.warn(
                issue_kind or "renderer_issue",
                str(issue.get("message", "Renderer reported a historical task-index metadata issue.")),
                path=str(issue.get("source_path", "")),
                task_id=str(issue.get("task_id", "")),
            )

    for row in actual_rows:
        task_id = row.get("task_id", "")
        task_dir = repo_root / render_task_index.TASKS_ROOT / task_id
        if not task_id:
            report.error("missing_task_id", "Generated task-index row has a blank task_id.")
        elif not task_dir.is_dir():
            report.error(
                "source_task_directory_missing",
                "Generated task-index row does not have a matching tracked task directory.",
                task_id=task_id,
                path=f"{render_task_index.TASKS_ROOT}/{task_id}",
            )

        status = row.get("status", "")
        if status not in render_task_index.STATUS_VALUES:
            report.error(
                "invalid_status",
                "Generated task-index row has an unsupported status value.",
                task_id=task_id,
                field="status",
                value=status,
            )

        completion_path = row.get("completion_path", "")
        if completion_path and not (repo_root / completion_path).exists():
            report.error(
                "completion_path_missing",
                "Generated task-index row names a completion path that does not exist.",
                task_id=task_id,
                path=completion_path,
            )

        if support_only_row(row) and row.get("physics_delta", "") != "false":
            report.error(
                "support_only_physics_delta",
                "Support-only project-control task row must preserve physics_delta=false.",
                task_id=task_id,
                field="physics_delta",
                value=row.get("physics_delta", ""),
            )

    check_forbidden_overread(report, actual_rows)
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--write-report", help="Write the JSON report to this path.")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = validate_task_index(Path(args.repo_root))
    except render_task_index.TaskIndexError as exc:
        report = TaskIndexValidationReport(repo_root=Path(args.repo_root).resolve())
        report.error("renderer_error", str(exc))

    payload = report.as_dict()
    if args.write_report:
        report_path = Path(args.write_report)
        if not report_path.is_absolute():
            report_path = Path(args.repo_root).resolve() / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif report.ok():
        print("Task-index validation passed.")
    else:
        print("Task-index validation failed:")
        for error in payload["errors"]:
            path = f" {error['path']}" if error.get("path") else ""
            task = f" {error['task_id']}" if error.get("task_id") else ""
            print(f"- {error['code']}:{path}{task} {error['message']}")
    return 0 if report.ok() else 1


if __name__ == "__main__":
    raise SystemExit(main())
