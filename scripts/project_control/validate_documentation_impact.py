#!/usr/bin/env python3
"""Validate documentation-impact handling for project-system changes."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
RESEARCH_CONTROL_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(RESEARCH_CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_DIR))

from classify_project_changes import changed_paths_from_git, classify_paths  # noqa: E402
from scripts.validation.models import (  # noqa: E402
    ValidationFinding,
    ValidationGateResult,
    ValidationRun,
)
from scripts.validation.reporting import (  # noqa: E402
    DEFAULT_RECEIPT_ROOT,
    add_reporting_arguments,
    emit_report,
    options_from_namespace,
)
from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


PROJECT_SYSTEM_TASK_PREFIX = "project_system_"
DOC_UPDATE_PATTERNS = {
    "README.md",
    "AGENTS.md",
    "research_control/README.md",
    "research_control/AGENTS.md",
    "github-facing/*.md",
    "github-facing/**/*.md",
    "markdown/**/*.md",
    "registries/HTML_EXPLAINER_REGISTRY.csv",
    "registries/MARKDOWN_SOURCE_REGISTRY.csv",
}
VALIDATOR_COMMAND_TERMS = {
    "classify_project_changes": ("scripts/project_control/classify_project_changes.py",),
    "collect_project_improvement_signals": (
        "scripts/project_control/collect_project_improvement_signals.py",
        "--validate-emitted",
    ),
    "validate_documentation_impact": (
        "scripts/project_control/validate_documentation_impact.py",
    ),
    "bootstrap_memory_system": (
        ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
    ),
    "bootstrap_memory_system_validate_only": (
        ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
        "--validate-only",
    ),
    "validate_research_control": (
        "scripts/research_control/validate_research_control.py",
    ),
    "validate_research_control_check_diff": (
        "scripts/research_control/validate_research_control.py",
        "--check-diff",
    ),
    "unittest": ("unittest",),
}
NO_OP_RECEIPT_GUIDANCE = (
    "If no source documentation update is needed, add a task-local documentation_impact.yaml "
    "with docs_update_required: false, a no_update_rationale, exact classifier reason_codes, "
    "covered changed_paths, generated_derivatives, and validators_run."
)


@dataclass
class DocumentationImpactReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    classification: dict[str, object] = field(default_factory=dict)
    documentation_update_paths: list[str] = field(default_factory=list)
    impact_record_paths: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, object]:
        return {
            "status": "PASS" if self.ok() else "FAIL",
            "errors": self.errors,
            "warnings": self.warnings,
            "classification": self.classification,
            "documentation_update_paths": self.documentation_update_paths,
            "impact_record_paths": self.impact_record_paths,
        }


def matches(path: str, pattern: str) -> bool:
    return path == pattern or fnmatch.fnmatch(path, pattern)


def documentation_update_paths(paths: Iterable[str]) -> list[str]:
    return sorted(
        path
        for path in set(paths)
        if any(matches(path, pattern) for pattern in DOC_UPDATE_PATTERNS)
    )


def impact_record_paths(paths: Iterable[str]) -> list[str]:
    return sorted(
        path
        for path in set(paths)
        if fnmatch.fnmatch(path, "research_control/tasks/*/documentation_impact.yaml")
    )


def task_id_from_path(path: str) -> str:
    parts = Path(path).parts
    if len(parts) >= 3 and parts[0] == "research_control" and parts[1] == "tasks":
        return parts[2]
    return ""


def is_project_system_task(task_id: str) -> bool:
    task_path = REPO_ROOT / "research_control" / "tasks" / task_id / "00_TASK.yaml"
    if not task_path.exists():
        return False
    try:
        task = load_yaml(task_path)
    except StrictYamlError:
        return False
    return str(task.get("task_type", "")).startswith(PROJECT_SYSTEM_TASK_PREFIX)


def project_system_task_ids(paths: Iterable[str]) -> list[str]:
    return sorted(
        task_id
        for task_id in {task_id_from_path(path) for path in paths}
        if task_id and is_project_system_task(task_id)
    )


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str):
        return [value] if value else []
    return []


def bool_value(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return None


def command_list_has(validators_run: list[str], terms: tuple[str, ...]) -> bool:
    return any(all(term in command for term in terms) for command in validators_run)


def live_source_paths(paths: Iterable[str], classification: dict[str, object]) -> list[str]:
    ignored = set(list_value(classification.get("ignored_paths")))
    generated = set(list_value(classification.get("generated_only_paths")))
    return sorted(set(paths) - ignored - generated)


def live_generated_paths(classification: dict[str, object]) -> list[str]:
    return list_value(classification.get("generated_only_paths"))


def covered_by_patterns(path: str, patterns: Iterable[str]) -> bool:
    return any(matches(path, pattern) for pattern in patterns)


def required_validator_names(
    paths: Iterable[str],
    classification: dict[str, object],
    *,
    project_system_task: bool,
) -> list[str]:
    names = {"classify_project_changes", "validate_documentation_impact"}
    names.update(list_value(classification.get("required_validators")))
    if project_system_task:
        names.update(
            {
                "collect_project_improvement_signals",
                "bootstrap_memory_system",
                "bootstrap_memory_system_validate_only",
                "validate_research_control",
                "validate_research_control_check_diff",
            }
        )
    if any(path.startswith("tests/") for path in paths):
        names.add("unittest")
    return sorted(names)


def validate_impact_record(
    report: DocumentationImpactReport,
    path_text: str,
    path_list: list[str],
    *,
    project_system_task: bool,
) -> None:
    path = REPO_ROOT / path_text
    if not path.exists():
        report.error(f"{path_text}: documentation impact record does not exist")
        return
    try:
        record = load_yaml(path)
    except StrictYamlError as exc:
        report.error(f"{path_text}: {exc}")
        return

    required = [
        "documentation_impact_id",
        "task_id",
        "job_id",
        "changed_paths",
        "docs_update_required",
        "reason_codes",
        "source_surfaces_inspected",
        "updated_source_docs",
        "updated_registries",
        "generated_derivatives",
        "no_update_rationale",
        "validators_run",
        "status",
    ]
    for field_name in required:
        if field_name not in record:
            report.error(f"{path_text}: missing {field_name}")

    docs_required = bool_value(record.get("docs_update_required"))
    if docs_required is None:
        report.error(f"{path_text}: docs_update_required must be true or false")
        return
    if not docs_required and not str(record.get("no_update_rationale", "")).strip():
        report.error(f"{path_text}: no_update_rationale is required when docs_update_required=false")
    if docs_required and not (
        list_value(record.get("updated_source_docs")) or list_value(record.get("updated_registries"))
    ):
        report.error(
            f"{path_text}: updated_source_docs or updated_registries is required when docs_update_required=true"
        )
    if str(record.get("status", "")) not in {"completed", "no_update_required", "blocked"}:
        report.error(f"{path_text}: status must be completed no_update_required or blocked")

    record_changed_paths = set(list_value(record.get("changed_paths")))
    for live_path in live_source_paths(path_list, report.classification):
        if live_path not in record_changed_paths:
            report.error(f"{path_text}: changed_paths missing live source change {live_path}")

    generated_patterns = list_value(record.get("generated_derivatives"))
    for live_path in live_generated_paths(report.classification):
        if not covered_by_patterns(live_path, generated_patterns):
            report.error(f"{path_text}: generated_derivatives missing live generated change {live_path}")

    record_reason_codes = set(list_value(record.get("reason_codes")))
    for reason_code in list_value(report.classification.get("reason_codes")):
        if reason_code not in record_reason_codes:
            report.error(f"{path_text}: reason_codes missing classifier reason {reason_code}")

    validators_run = list_value(record.get("validators_run"))
    for validator_name in required_validator_names(
        path_list,
        report.classification,
        project_system_task=project_system_task,
    ):
        terms = VALIDATOR_COMMAND_TERMS.get(validator_name)
        if terms and not command_list_has(validators_run, terms):
            report.error(f"{path_text}: validators_run missing {validator_name}")


def validate_paths(paths: Iterable[str]) -> DocumentationImpactReport:
    path_list = sorted(set(paths))
    report = DocumentationImpactReport(classification=classify_paths(path_list))
    report.documentation_update_paths = documentation_update_paths(path_list)
    report.impact_record_paths = impact_record_paths(path_list)

    project_task = bool(project_system_task_ids(path_list))
    for path in report.impact_record_paths:
        validate_impact_record(
            report,
            path,
            path_list,
            project_system_task=project_task,
        )

    if not report.classification.get("docs_impact_required"):
        return report

    if project_system_task_ids(path_list) and not report.impact_record_paths:
        report.error(
            f"state-changing project-system AgentJob requires documentation_impact.yaml. {NO_OP_RECEIPT_GUIDANCE}"
        )
        return report

    if report.documentation_update_paths or report.impact_record_paths:
        return report

    report.error(
        f"documentation impact is required but no source documentation update or documentation_impact.yaml rationale was found. {NO_OP_RECEIPT_GUIDANCE}"
    )
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_reporting_arguments(parser)
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument(
        "--legacy-human",
        action="store_true",
        help="Emit the previous human-readable PASS or failure list.",
    )
    parser.add_argument("--staged", action="store_true", help="Validate staged changes only.")
    parser.add_argument("--base-ref", default="HEAD", help="Git base reference.")
    parser.add_argument("--no-untracked", action="store_true", help="Ignore untracked files.")
    parser.add_argument("--paths", nargs="*", help="Validate explicit paths instead of Git state.")
    args = parser.parse_args(argv)
    common_mode_selected = any(
        getattr(args, name)
        for name in ("summary", "json_summary", "full_json", "receipt", "quiet")
    )
    if args.json and (args.legacy_human or common_mode_selected):
        parser.error("--json cannot be combined with another reporting mode")
    if args.legacy_human and common_mode_selected:
        parser.error("--legacy-human cannot be combined with a common reporting mode")
    return args


def _finding_id(level: str, message: str, occurrence: int) -> str:
    prefix = re.sub(r"[^A-Z0-9]+", "-", f"DOCUMENTATION-IMPACT-{level}").strip("-")
    digest = hashlib.sha256(
        json.dumps(
            {"message": message, "occurrence": occurrence},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()[:12].upper()
    return f"{prefix}-{digest}"


def _working_tree_digest(payload: dict[str, object]) -> str:
    digest = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    )
    results: dict[str, bytes] = {}
    for label, command in (
        ("head", ["git", "rev-parse", "HEAD"]),
        ("diff", ["git", "diff", "--no-ext-diff", "--binary", "HEAD", "--"]),
        ("untracked", ["git", "ls-files", "--others", "--exclude-standard", "-z"]),
    ):
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0:
            return digest.hexdigest()
        results[label] = completed.stdout
        digest.update(label.encode("ascii") + b"\0" + completed.stdout)
    for raw_path in sorted(path for path in results["untracked"].split(b"\0") if path):
        path = REPO_ROOT / raw_path.decode("utf-8", errors="surrogateescape")
        if path.is_file():
            digest.update(b"untracked-content\0" + raw_path + b"\0" + path.read_bytes())
    return digest.hexdigest()


def adapt_to_common_run(
    report: DocumentationImpactReport,
    selected_paths: Iterable[str],
) -> ValidationRun:
    occurrence_counts: dict[tuple[str, str], int] = {}
    findings: list[ValidationFinding] = []
    for level, code, messages in (
        ("ERROR", "documentation_impact_error", report.errors),
        ("WARN", "documentation_impact_warning", report.warnings),
    ):
        for message in messages:
            key = (level, message)
            occurrence_counts[key] = occurrence_counts.get(key, 0) + 1
            findings.append(
                ValidationFinding(
                    finding_id=_finding_id(level, message, occurrence_counts[key]),
                    level=level,
                    code=code,
                    message=message,
                )
            )
    payload = {
        "legacy": report.as_dict(),
        "selected_paths": sorted(set(selected_paths)),
    }
    digest = _working_tree_digest(payload)
    status = "PASS" if report.ok() else "FAIL"
    exit_code = 0 if report.ok() else 1
    gate = ValidationGateResult(
        gate_id="documentation_impact",
        status=status,
        severity="blocking",
        exit_code=exit_code,
        findings=tuple(findings),
    )
    return ValidationRun(
        run_id=f"DOCUMENTATION-IMPACT-{digest[:16].upper()}",
        tree_hash=f"working-sha256:{digest}",
        status=status,
        exit_code=exit_code,
        gate_results=(gate,),
        profile="shadow_planner",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths: list[str] = []
    try:
        paths = args.paths if args.paths is not None else changed_paths_from_git(
            staged=args.staged,
            base_ref=args.base_ref,
            include_untracked=not args.no_untracked,
        )
        report = validate_paths(paths)
    except RuntimeError as exc:
        report = DocumentationImpactReport()
        report.error(str(exc))

    if args.json:
        print(json.dumps(report.as_dict(), indent=2))
        return 0 if report.ok() else 1
    if args.legacy_human:
        if report.ok():
            print("Documentation-impact validation passed.")
        else:
            print("Documentation-impact validation failed:")
            for error in report.errors:
                print(f"- {error}")
        return 0 if report.ok() else 1
    return emit_report(
        adapt_to_common_run(report, paths),
        options=options_from_namespace(args),
        receipt_root=REPO_ROOT / DEFAULT_RECEIPT_ROOT,
        stream=sys.stdout,
    )


if __name__ == "__main__":
    raise SystemExit(main())
