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
import hashlib
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

for import_path in (REPO_ROOT, SCRIPT_DIR):
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))

import render_task_index  # noqa: E402
from scripts.validation.models import (  # noqa: E402
    ValidationFinding as CommonValidationFinding,
    ValidationGateResult,
    ValidationRun,
)
from scripts.validation.reporting import (  # noqa: E402
    DEFAULT_MAX_FINDINGS,
    DEFAULT_RECEIPT_ROOT,
    add_reporting_arguments,
    options_from_namespace,
    render_output,
    write_full_receipt,
)


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
HARD_FINDING_PRIORITY = {
    "generated_output_stale": 0,
    "csv_rows_mismatch": 1,
    "required_header_mismatch": 2,
}
WARNING_GROUP_LIMIT = 5
REPRESENTATIVE_TASK_LIMIT = 3


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


def _finding_identity(finding: ValidationFinding, level: str) -> str:
    code = re.sub(r"[^A-Z0-9]+", "-", finding.code.upper()).strip("-") or "FINDING"
    code = code[:48].rstrip("-")
    priority = HARD_FINDING_PRIORITY.get(finding.code, 99) if level == "ERROR" else 0
    digest = hashlib.sha256(
        json.dumps(finding.as_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()[:12].upper()
    return f"TASK-INDEX-{level}-{priority:02d}-{code}-{digest}"


def _full_finding_message(finding: ValidationFinding) -> str:
    context = [
        f"{key}={value}"
        for key, value in (
            ("path", finding.path),
            ("task_id", finding.task_id),
            ("field", finding.field),
            ("value", finding.value),
        )
        if value
    ]
    if not context:
        return finding.message
    return f"{finding.message} | {' | '.join(context)}"


def _working_tree_hash(report: TaskIndexValidationReport) -> str:
    payload = {
        "source_fingerprint": report.source_fingerprint,
        "output_hashes": report.output_hashes,
        "checks": report.checks,
        "row_count": report.row_count,
        "renderer_issue_count": report.renderer_issue_count,
        "renderer_issue_kind_counts": report.renderer_issue_kind_counts,
        "errors": [finding.as_dict() for finding in report.errors],
        "warnings": [finding.as_dict() for finding in report.warnings],
    }
    digest = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"working-sha256:{digest}"


def adapt_to_common_run(report: TaskIndexValidationReport) -> ValidationRun:
    """Map the legacy task-index result to one complete common run receipt."""

    common_findings: list[CommonValidationFinding] = []
    identity_counts: Counter[str] = Counter()
    for finding, level in (
        *((finding, "ERROR") for finding in report.errors),
        *((finding, "WARN") for finding in report.warnings),
    ):
        base_identity = _finding_identity(finding, level)
        identity_counts[base_identity] += 1
        suffix = f"-{identity_counts[base_identity]}" if identity_counts[base_identity] > 1 else ""
        common_findings.append(
            CommonValidationFinding(
                finding_id=f"{base_identity}{suffix}",
                level=level,
                code=finding.code,
                message=_full_finding_message(finding),
            )
        )

    status = "PASS" if report.ok() else "FAIL"
    exit_code = 0 if report.ok() else 1
    gate = ValidationGateResult(
        gate_id="task_index_validation",
        status=status,
        severity="blocking",
        exit_code=exit_code,
        findings=tuple(common_findings),
    )
    tree_hash = _working_tree_hash(report)
    return ValidationRun(
        run_id=f"TASK-INDEX-{tree_hash.removeprefix('working-sha256:')[:16].upper()}",
        tree_hash=tree_hash,
        status=status,
        exit_code=exit_code,
        gate_results=(gate,),
        profile="shadow_planner",
    )


def _single_line(value: str, limit: int = 240) -> str:
    collapsed = " ".join(value.split())
    encoded = collapsed.encode("utf-8")
    if len(encoded) <= limit:
        return collapsed
    shortened = encoded[: max(0, limit - 3)]
    while shortened:
        try:
            return shortened.decode("utf-8") + "..."
        except UnicodeDecodeError:
            shortened = shortened[:-1]
    return "..."


def render_compact_summary(
    report: TaskIndexValidationReport,
    run: ValidationRun,
    receipt_path: Path,
) -> str:
    """Render hard findings first, followed by bounded historical-warning groups."""

    lines = [
        (
            f"{run.status} gates=1 errors={len(report.errors)} warnings={len(report.warnings)} "
            f"findings={len(report.errors) + len(report.warnings)} receipt={receipt_path}"
        )
    ]
    ordered_errors = sorted(
        report.errors,
        key=lambda finding: (
            HARD_FINDING_PRIORITY.get(finding.code, len(HARD_FINDING_PRIORITY)),
            finding.code,
            finding.path,
            finding.task_id,
            finding.message,
        ),
    )
    for finding in ordered_errors[:DEFAULT_MAX_FINDINGS]:
        context = " ".join(
            value
            for value in (
                f"path={finding.path}" if finding.path else "",
                f"task_id={finding.task_id}" if finding.task_id else "",
            )
            if value
        )
        context = f" {context}" if context else ""
        lines.append(f"ERROR {finding.code}{context}: {_single_line(finding.message)}")
    if len(ordered_errors) > DEFAULT_MAX_FINDINGS:
        lines.append(f"MORE_ERRORS count={len(ordered_errors) - DEFAULT_MAX_FINDINGS}")

    warning_counts = Counter(finding.code for finding in report.warnings)
    warning_task_ids: dict[str, set[str]] = {}
    for finding in report.warnings:
        if finding.task_id:
            warning_task_ids.setdefault(finding.code, set()).add(finding.task_id)
    group_codes = sorted(warning_counts)
    for code in group_codes[:WARNING_GROUP_LIMIT]:
        task_ids = sorted(warning_task_ids.get(code, set()))
        representatives = ",".join(task_ids[:REPRESENTATIVE_TASK_LIMIT]) or "none"
        more_task_ids = max(0, len(task_ids) - REPRESENTATIVE_TASK_LIMIT)
        suffix = f" more_task_ids={more_task_ids}" if more_task_ids else ""
        lines.append(
            f"WARN_GROUP {code} count={warning_counts[code]} task_ids={representatives}{suffix}"
        )
    if len(group_codes) > WARNING_GROUP_LIMIT:
        lines.append(f"MORE_WARNING_GROUPS count={len(group_codes) - WARNING_GROUP_LIMIT}")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_reporting_arguments(parser)
    parser.add_argument("--json", action="store_true", help="Emit legacy full JSON (compatibility alias).")
    parser.add_argument("--write-report", help="Write the JSON report to this path.")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    common_mode_selected = any(
        getattr(args, name)
        for name in ("summary", "json_summary", "full_json", "receipt", "quiet")
    )
    if args.json and common_mode_selected:
        parser.error("--json cannot be combined with a common reporting mode")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(args.repo_root).resolve()
    try:
        report = validate_task_index(repo_root)
    except render_task_index.TaskIndexError as exc:
        report = TaskIndexValidationReport(repo_root=repo_root)
        report.error("renderer_error", str(exc))

    payload = report.as_dict()
    if args.write_report:
        report_path = Path(args.write_report)
        if not report_path.is_absolute():
            report_path = Path(args.repo_root).resolve() / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    run = adapt_to_common_run(report)
    try:
        receipt_path = write_full_receipt(run, repo_root / DEFAULT_RECEIPT_ROOT)
    except (OSError, ValueError) as error:
        print(f"BLOCKED_CONFIGURATION receipt_write_failed: {_single_line(str(error), limit=256)}")
        return 2

    if args.json or args.full_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        options = options_from_namespace(args)
        if options.mode == "summary":
            sys.stdout.write(render_compact_summary(report, run, receipt_path))
        else:
            sys.stdout.write(render_output(run, receipt_path, options))
    return run.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
