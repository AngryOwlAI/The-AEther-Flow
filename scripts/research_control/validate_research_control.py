#!/usr/bin/env python3
"""Validate the tracked research-control spine."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from strict_yaml import StrictYamlError, load as load_yaml, load_frontmatter
except ImportError:  # pragma: no cover - package import path for tests
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml, load_frontmatter


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = REPO_ROOT / "registries"
CONTROL_DIR = REPO_ROOT / "research_control"

ROLE_COLUMNS = [
    "role_id",
    "version",
    "role_name",
    "role_kind",
    "role_contract_path",
    "authority_level",
    "status",
    "may_execute_autonomously",
    "may_create_outputs",
    "may_modify_sources",
    "may_promote_claims",
    "requires_human_gate",
    "default_output_format",
    "default_validators",
    "created_at",
    "updated_at",
    "notes",
]

DECISION_COLUMNS = [
    "decision_id",
    "task_id",
    "decision_path",
    "director_version",
    "decision_type",
    "selected_role_id",
    "selected_role_version",
    "agent_job_id",
    "status",
    "supersedes_decision_id",
    "requires_human_gate",
    "created_at",
    "activated_at",
    "completed_at",
    "validation_status",
    "notes",
]

JOB_COLUMNS = [
    "job_id",
    "task_id",
    "decision_id",
    "role_id",
    "role_version",
    "job_path",
    "completion_path",
    "status",
    "allowed_write_paths",
    "output_paths",
    "validation_status",
    "created_at",
    "started_at",
    "completed_at",
    "requires_human_gate",
    "notes",
]

TASK_COLUMNS = [
    "task_id",
    "task_path",
    "task_type",
    "status",
    "current_decision_id",
    "current_job_id",
    "parent_task_id",
    "created_at",
    "updated_at",
    "closed_at",
    "closure_status",
    "requires_human_gate",
    "notes",
]

CLAIM_COLUMNS = [
    "claim_boundary_id",
    "scope",
    "applies_to_path",
    "allowed_claims",
    "forbidden_claims",
    "requires_gate_for",
    "authority_source_path",
    "status",
    "created_at",
    "updated_at",
    "notes",
]

REGISTRY_COLUMNS = {
    "AGENT_ROLE_REGISTRY.csv": ROLE_COLUMNS,
    "DIRECTOR_DECISION_REGISTRY.csv": DECISION_COLUMNS,
    "AGENT_JOB_REGISTRY.csv": JOB_COLUMNS,
    "RESEARCH_TASK_REGISTRY.csv": TASK_COLUMNS,
    "CLAIM_BOUNDARY_REGISTRY.csv": CLAIM_COLUMNS,
}

BOOLEAN_FIELDS = {
    "may_execute_autonomously",
    "may_create_outputs",
    "may_modify_sources",
    "may_promote_claims",
    "requires_human_gate",
}

SEMICOLON_FIELDS = {
    "default_validators",
    "allowed_write_paths",
    "output_paths",
    "allowed_claims",
    "forbidden_claims",
    "requires_gate_for",
}

FORBIDDEN_PHRASES = [
    "GR derived from ontology",
    "exact GR recovered from ontology",
    "GR_DERIVED_FROM_ANTHOLOGY",
]

SAFE_BOUNDARY_MARKERS = (
    "forbidden",
    "not established",
    "not authorized",
    "without gate",
    "compatibility-only",
    "claim boundary",
    "blocked claim",
    "open derivation",
)


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def ok(self) -> bool:
        return not self.errors


def repo_path(relative_path: str) -> Path:
    return REPO_ROOT / relative_path


def validate_relative_path(path_text: str) -> str | None:
    if not path_text:
        return None
    path = Path(path_text)
    if path.is_absolute():
        return "absolute paths are not allowed"
    if any(part == ".." for part in path.parts):
        return "path traversal is not allowed"
    return None


def read_csv_rows(name: str) -> list[dict[str, str]]:
    path = REGISTRY_DIR / name
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def existing_by_id(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def validate_registry_columns(report: ValidationReport) -> None:
    for name, expected in REGISTRY_COLUMNS.items():
        path = REGISTRY_DIR / name
        if not path.exists():
            report.error(f"missing registry: registries/{name}")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, [])
        if header != expected:
            report.error(f"{name}: expected columns {expected}, found {header}")


def validate_registry_values(report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]) -> None:
    seen: set[tuple[str, str]] = set()
    id_fields = {
        "AGENT_ROLE_REGISTRY.csv": "role_id",
        "DIRECTOR_DECISION_REGISTRY.csv": "decision_id",
        "AGENT_JOB_REGISTRY.csv": "job_id",
        "RESEARCH_TASK_REGISTRY.csv": "task_id",
        "CLAIM_BOUNDARY_REGISTRY.csv": "claim_boundary_id",
    }
    for registry_name, rows in rows_by_registry.items():
        id_field = id_fields[registry_name]
        local_ids: set[str] = set()
        for row_number, row in enumerate(rows, start=2):
            row_id = row.get(id_field, "")
            if not row_id:
                report.error(f"{registry_name}:{row_number}: missing {id_field}")
            if row_id in local_ids:
                report.error(f"{registry_name}:{row_number}: duplicate {id_field} {row_id}")
            local_ids.add(row_id)
            seen.add((registry_name, row_id))
            for field_name in BOOLEAN_FIELDS & set(row):
                if row[field_name] not in {"true", "false"}:
                    report.error(
                        f"{registry_name}:{row_number}: {field_name} must be lowercase true/false"
                    )
            for field_name in SEMICOLON_FIELDS & set(row):
                if "," in row[field_name]:
                    report.error(
                        f"{registry_name}:{row_number}: {field_name} must use semicolons, not commas"
                    )


def _frontmatter_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    return str(value)


def validate_roles(report: ValidationReport, role_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    roles = existing_by_id(role_rows, "role_id")
    for row in role_rows:
        path_text = row["role_contract_path"]
        reason = validate_relative_path(path_text)
        if reason:
            report.error(f"{row['role_id']}: invalid role_contract_path: {reason}")
            continue
        path = repo_path(path_text)
        if not path.exists():
            report.error(f"{row['role_id']}: missing role contract {path_text}")
            continue
        try:
            frontmatter, _ = load_frontmatter(path)
        except StrictYamlError as exc:
            report.error(f"{path_text}: {exc}")
            continue
        for field_name in [
            "role_id",
            "version",
            "role_kind",
            "authority_level",
            "status",
            "may_execute_autonomously",
            "may_create_outputs",
            "may_modify_sources",
            "may_promote_claims",
            "requires_human_gate",
            "default_output_format",
            "default_validators",
        ]:
            if _frontmatter_value(frontmatter.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{path_text}: frontmatter {field_name} does not match AGENT_ROLE_REGISTRY.csv"
                )
    return roles


def validate_tasks(
    report: ValidationReport,
    task_rows: list[dict[str, str]],
    decision_rows: dict[str, dict[str, str]],
    job_rows: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    tasks = existing_by_id(task_rows, "task_id")
    for row in task_rows:
        reason = validate_relative_path(row["task_path"])
        if reason:
            report.error(f"{row['task_id']}: invalid task_path: {reason}")
            continue
        task_dir = repo_path(row["task_path"])
        task_yaml = task_dir / "00_TASK.yaml"
        if not task_yaml.exists():
            report.error(f"{row['task_id']}: missing 00_TASK.yaml")
            continue
        try:
            task_data = load_yaml(task_yaml)
        except StrictYamlError as exc:
            report.error(f"{task_yaml.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        if str(task_data.get("task_id", "")) != row["task_id"]:
            report.error(f"{row['task_id']}: 00_TASK.yaml task_id mismatch")
        if row["current_decision_id"] and row["current_decision_id"] not in decision_rows:
            report.error(f"{row['task_id']}: current_decision_id is not registered")
        if row["current_job_id"] and row["current_job_id"] not in job_rows:
            report.error(f"{row['task_id']}: current_job_id is not registered")
    return tasks


def validate_director_decisions(
    report: ValidationReport,
    decision_rows: list[dict[str, str]],
    roles: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    decisions = existing_by_id(decision_rows, "decision_id")
    for row in decision_rows:
        reason = validate_relative_path(row["decision_path"])
        if reason:
            report.error(f"{row['decision_id']}: invalid decision_path: {reason}")
            continue
        path = repo_path(row["decision_path"])
        if not path.exists():
            report.error(f"{row['decision_id']}: missing DDR {row['decision_path']}")
            continue
        try:
            frontmatter, body = load_frontmatter(path)
        except StrictYamlError as exc:
            report.error(f"{row['decision_path']}: {exc}")
            continue
        for field_name in [
            "decision_id",
            "task_id",
            "director_version",
            "decision_type",
            "selected_role_id",
            "selected_role_version",
            "agent_job_id",
            "status",
            "requires_human_gate",
        ]:
            if _frontmatter_value(frontmatter.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{row['decision_path']}: frontmatter {field_name} does not match DIRECTOR_DECISION_REGISTRY.csv"
                )
        if row["decision_type"] != "provisional_role" and row["selected_role_id"] not in roles:
            report.error(f"{row['decision_id']}: selected role is not registered")
        if "## Role-Fit Matrix" not in body:
            report.error(f"{row['decision_path']}: missing ## Role-Fit Matrix")
    return decisions


def validate_agent_jobs(
    report: ValidationReport,
    job_rows: list[dict[str, str]],
    roles: dict[str, dict[str, str]],
    decisions: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    jobs = existing_by_id(job_rows, "job_id")
    for row in job_rows:
        reason = validate_relative_path(row["job_path"])
        if reason:
            report.error(f"{row['job_id']}: invalid job_path: {reason}")
            continue
        path = repo_path(row["job_path"])
        if not path.exists():
            report.error(f"{row['job_id']}: missing AgentJob {row['job_path']}")
            continue
        try:
            job = load_yaml(path)
        except StrictYamlError as exc:
            report.error(f"{row['job_path']}: {exc}")
            continue
        for field_name in [
            "job_id",
            "task_id",
            "decision_id",
            "role_id",
            "role_version",
            "status",
            "requires_human_gate",
        ]:
            if _frontmatter_value(job.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{row['job_path']}: {field_name} does not match AGENT_JOB_REGISTRY.csv"
                )
        if row["decision_id"] not in decisions:
            report.error(f"{row['job_id']}: decision_id is not registered")
        if row["role_id"] not in roles:
            provisional = job.get("provisional_role_contract")
            if not isinstance(provisional, dict):
                report.error(f"{row['job_id']}: unregistered role lacks provisional_role_contract")
            elif str(provisional.get("role_id", "")) != row["role_id"]:
                report.error(f"{row['job_id']}: provisional role_id mismatch")
            elif str(provisional.get("expires_after_job_id", "")) != row["job_id"]:
                report.error(f"{row['job_id']}: provisional role must expire after this job")
        for field_name in ["allowed_write_paths", "allowed_generated_paths", "forbidden_paths"]:
            value = job.get(field_name, [])
            if not isinstance(value, list):
                report.error(f"{row['job_path']}: {field_name} must be a list")
                continue
            for item in value:
                if not isinstance(item, str):
                    report.error(f"{row['job_path']}: {field_name} entries must be strings")
                    continue
                reason = validate_relative_path(item.replace("**", "x").replace("*", "x"))
                if reason:
                    report.error(f"{row['job_path']}: invalid {field_name} entry {item}: {reason}")
        if row["completion_path"]:
            completion_path = repo_path(row["completion_path"])
            if not completion_path.exists():
                report.error(f"{row['job_id']}: missing completion {row['completion_path']}")
            else:
                validate_completion(report, row, completion_path)
    return jobs


def validate_completion(report: ValidationReport, job_row: dict[str, str], path: Path) -> None:
    try:
        completion = load_yaml(path)
    except StrictYamlError as exc:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: {exc}")
        return
    expected_id = f"AJC-{job_row['job_id']}"
    if str(completion.get("completion_id", "")) != expected_id:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: completion_id must be {expected_id}")
    if str(completion.get("job_id", "")) != job_row["job_id"]:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: job_id mismatch")
    command_results = completion.get("command_results", [])
    if not isinstance(command_results, list) or not command_results:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: missing command_results")


def validate_program_state(report: ValidationReport, tasks: dict[str, dict[str, str]]) -> None:
    path = CONTROL_DIR / "program_state.yaml"
    if not path.exists():
        report.error("missing research_control/program_state.yaml")
        return
    try:
        state = load_yaml(path)
    except StrictYamlError as exc:
        report.error(f"research_control/program_state.yaml: {exc}")
        return
    active_task_id = str(state.get("active_task_id", ""))
    if active_task_id and active_task_id not in tasks:
        report.error("program_state.yaml: active_task_id is not registered")
    if "gr_derived" in state:
        report.error("program_state.yaml: bootstrap must not define gr_derived")


def handoff_number(path: Path) -> int | None:
    match = re.fullmatch(r"handoff-(\d{4})\.yaml", path.name)
    return int(match.group(1)) if match else None


def validate_handoffs(
    report: ValidationReport,
    tasks: dict[str, dict[str, str]],
    jobs: dict[str, dict[str, str]],
) -> None:
    handoff_dir = CONTROL_DIR / "handoffs"
    if not handoff_dir.exists():
        report.error("missing research_control/handoffs")
        return
    numbers: list[int] = []
    for yaml_path in sorted(handoff_dir.glob("handoff-*.yaml")):
        number = handoff_number(yaml_path)
        if number is None:
            report.error(f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: invalid handoff filename")
            continue
        numbers.append(number)
        md_path = yaml_path.with_suffix(".md")
        if not md_path.exists():
            report.error(f"{yaml_path.name}: missing Markdown mirror")
        try:
            data = load_yaml(yaml_path)
        except StrictYamlError as exc:
            report.error(f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        for field_name in ["handoff_id", "created_at", "task_id", "job_id", "completion_path", "next_action"]:
            if not data.get(field_name):
                report.error(f"{yaml_path.name}: missing {field_name}")
        if str(data.get("task_id", "")) not in tasks:
            report.error(f"{yaml_path.name}: task_id is not registered")
        if str(data.get("job_id", "")) and str(data.get("job_id", "")) not in jobs:
            report.error(f"{yaml_path.name}: job_id is not registered")
        if ".local/" in yaml_path.read_text(encoding="utf-8"):
            report.error(f"{yaml_path.name}: tracked handoff YAML must not use .local/ as authority")
    if numbers and numbers != list(range(min(numbers), max(numbers) + 1)):
        report.error("handoff IDs must be monotonic without gaps")


def validate_approvals(report: ValidationReport, decisions: dict[str, dict[str, str]]) -> None:
    approval_dir = CONTROL_DIR / "approvals"
    if not approval_dir.exists():
        report.error("missing research_control/approvals")
        return
    for path in approval_dir.glob("approval-*.yaml"):
        try:
            data = load_yaml(path)
        except StrictYamlError as exc:
            report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        decision_id = str(data.get("decision_id", ""))
        if decision_id and decision_id not in decisions:
            report.error(f"{path.name}: decision_id is not registered")


def _safe_claim_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in SAFE_BOUNDARY_MARKERS)


def validate_claim_boundaries(report: ValidationReport, claim_rows: list[dict[str, str]]) -> None:
    for row in claim_rows:
        if row["authority_source_path"]:
            reason = validate_relative_path(row["authority_source_path"])
            if reason:
                report.error(f"{row['claim_boundary_id']}: invalid authority_source_path: {reason}")
            elif not repo_path(row["authority_source_path"]).exists():
                report.error(f"{row['claim_boundary_id']}: missing authority_source_path")


def scan_for_forbidden_claims(report: ValidationReport, claim_rows: list[dict[str, str]]) -> None:
    scan_roots = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / ".agents",
        CONTROL_DIR,
        REPO_ROOT / ".codex" / "skills" / "continue-research",
    ]
    registry_path = REGISTRY_DIR / "CLAIM_BOUNDARY_REGISTRY.csv"
    for root in scan_roots:
        paths = [root] if root.is_file() else list(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix not in {".md", ".yaml"}:
                continue
            relative = path.relative_to(REPO_ROOT).as_posix()
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                for phrase in FORBIDDEN_PHRASES:
                    if phrase in line and not _safe_claim_context(line):
                        report.error(f"{relative}:{line_number}: forbidden claim phrase outside boundary context: {phrase}")
    # The registry itself is allowed to contain forbidden phrases in forbidden_claims.
    if registry_path.exists():
        _ = claim_rows


def changed_paths(base_ref: str, staged_only: bool) -> list[str]:
    if staged_only:
        diff_cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", base_ref]
    else:
        diff_cmd = ["git", "diff", "--name-only", "--diff-filter=ACMR", base_ref]
    diff = subprocess.run(diff_cmd, cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if diff.returncode != 0:
        raise RuntimeError(diff.stderr)
    paths = [line.strip() for line in diff.stdout.splitlines() if line.strip()]
    if not staged_only:
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if untracked.returncode != 0:
            raise RuntimeError(untracked.stderr)
        paths.extend(line.strip() for line in untracked.stdout.splitlines() if line.strip())
    return sorted(set(paths))


def _pattern_is_too_broad(pattern: str) -> bool:
    return pattern in {"*", "**", "**/*"} or pattern.startswith("*/") or pattern.startswith("**/")


def _path_matches(path: str, pattern: str) -> bool:
    if _pattern_is_too_broad(pattern):
        return False
    return path == pattern or fnmatch.fnmatch(path, pattern)


def validate_diff(
    report: ValidationReport,
    job_rows: dict[str, dict[str, str]],
    base_ref: str,
    staged_only: bool,
) -> None:
    active_jobs = [row for row in job_rows.values() if row["status"] in {"active", "completed"}]
    if not active_jobs:
        report.error("--check-diff requires an active or completed AgentJob")
        return
    job = sorted(active_jobs, key=lambda row: row["created_at"])[-1]
    allowed = split_semicolon(job["allowed_write_paths"])
    output_paths = split_semicolon(job["output_paths"])
    allowed.extend(output_paths)
    job_path_text = job.get("job_path", "")
    job_path = repo_path(job_path_text) if job_path_text else None
    if job_path and job_path.exists():
        try:
            job_contract = load_yaml(job_path)
        except StrictYamlError as exc:
            report.error(f"{job_path_text}: {exc}")
            job_contract = {}
        generated_paths = job_contract.get("allowed_generated_paths", [])
        if isinstance(generated_paths, list):
            allowed.extend(str(path) for path in generated_paths if str(path))
    try:
        paths = changed_paths(base_ref, staged_only)
    except RuntimeError as exc:
        report.error(str(exc))
        return
    for pattern in allowed:
        if _pattern_is_too_broad(pattern):
            report.error(f"{job['job_id']}: overly broad allowlist pattern {pattern}")
    for changed in paths:
        if changed.startswith(".local/"):
            continue
        if not any(_path_matches(changed, pattern) for pattern in allowed):
            report.error(f"{changed}: changed path is not allowed by {job['job_id']}")


def validate_all(
    *,
    check_diff: bool = False,
    base_ref: str = "HEAD",
    staged_only: bool = False,
) -> ValidationReport:
    report = ValidationReport()
    validate_registry_columns(report)
    rows_by_registry = {
        name: read_csv_rows(name)
        for name in REGISTRY_COLUMNS
        if (REGISTRY_DIR / name).exists()
    }
    if len(rows_by_registry) != len(REGISTRY_COLUMNS):
        return report
    validate_registry_values(report, rows_by_registry)
    roles = validate_roles(report, rows_by_registry["AGENT_ROLE_REGISTRY.csv"])
    decisions = validate_director_decisions(
        report, rows_by_registry["DIRECTOR_DECISION_REGISTRY.csv"], roles
    )
    jobs = validate_agent_jobs(
        report, rows_by_registry["AGENT_JOB_REGISTRY.csv"], roles, decisions
    )
    tasks = validate_tasks(
        report,
        rows_by_registry["RESEARCH_TASK_REGISTRY.csv"],
        decisions,
        jobs,
    )
    validate_program_state(report, tasks)
    validate_handoffs(report, tasks, jobs)
    validate_approvals(report, decisions)
    validate_claim_boundaries(report, rows_by_registry["CLAIM_BOUNDARY_REGISTRY.csv"])
    scan_for_forbidden_claims(report, rows_by_registry["CLAIM_BOUNDARY_REGISTRY.csv"])
    if check_diff:
        validate_diff(report, jobs, base_ref, staged_only)
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable results.")
    parser.add_argument("--check-diff", action="store_true", help="Check current git diff against the latest active/completed AgentJob.")
    parser.add_argument("--staged-only", action="store_true", help="Check staged changes only.")
    parser.add_argument("--base-ref", default="HEAD", help="Git base ref for --check-diff.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = validate_all(
        check_diff=args.check_diff,
        base_ref=args.base_ref,
        staged_only=args.staged_only,
    )
    if args.json:
        print(json.dumps({"errors": report.errors, "warnings": report.warnings}, indent=2))
    else:
        if report.errors:
            print("Research-control validation failed:")
            for error in report.errors:
                print(f"- {error}")
        else:
            print("Research-control validation passed.")
        for warning in report.warnings:
            print(f"Warning: {warning}")
    return 0 if report.ok() else 1


if __name__ == "__main__":
    raise SystemExit(main())
