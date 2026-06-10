#!/usr/bin/env python3
"""Collect and validate tracked project-improvement signals."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from project_signal_types import (  # noqa: E402
    SIGNAL_TYPE_COLUMNS,
    SIGNAL_TYPE_REGISTRY_NAME,
    read_signal_type_rows,
    registry_path as signal_type_registry_path,
    signal_type_names,
)
from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402

SIGNAL_REGISTRY = REPO_ROOT / "registries" / "PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
OPEN_STATUSES = {"open", "pending", "active"}
ALLOWED_STATUSES = OPEN_STATUSES | {"resolved", "completed", "closed", "rejected"}
RESOLUTION_STATUSES = ALLOWED_STATUSES - OPEN_STATUSES
SUCCESS_RESOLUTION_STATUSES = {"resolved", "completed", "closed"}
ALLOWED_SEVERITIES = {"critical", "high", "medium", "low"}
ALLOWED_SIGNAL_TYPE_STATUSES = {"active", "deprecated"}
SIGNAL_REGISTRY_NAME = "PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
SIGNAL_REGISTRY_COLUMNS = (
    "signal_id",
    "created_at",
    "source_task_id",
    "source_job_id",
    "source_role_id",
    "signal_type",
    "severity",
    "status",
    "evidence_path",
    "recommended_skill",
    "recommended_role",
    "notes",
    "resolved_by_job_id",
    "resolution_evidence_path",
    "resolved_at",
)
SIGNAL_FIELDS = (
    "signal_id",
    "signal_type",
    "severity",
    "evidence",
    "evidence_path",
    "recommended_skill",
    "recommended_role",
    "notes",
)


def read_csv_registry(name: str) -> list[dict[str, str]]:
    path = REPO_ROOT / "registries" / name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def read_signals() -> list[dict[str, str]]:
    return read_csv_registry(SIGNAL_REGISTRY_NAME)


def read_signal_types() -> list[dict[str, str]]:
    return read_signal_type_rows(REPO_ROOT)


def read_jobs() -> dict[str, dict[str, str]]:
    return {
        row.get("job_id", ""): row
        for row in read_csv_registry("AGENT_JOB_REGISTRY.csv")
        if row.get("job_id")
    }


def collect_signals(*, status: str | None = None, signal_type: str | None = None) -> dict[str, object]:
    rows = read_signals()
    if status:
        rows = [row for row in rows if row.get("status") == status]
    if signal_type:
        rows = [row for row in rows if row.get("signal_type") == signal_type]
    open_rows = [row for row in rows if row.get("status") in OPEN_STATUSES]
    return {
        "signal_count": len(rows),
        "open_signal_count": len(open_rows),
        "signals": rows,
        "open_signals": open_rows,
    }


def _text(value: Any) -> str:
    return str(value or "").strip()


def _is_blank_signal(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    return not any(_text(value.get(field)) for field in SIGNAL_FIELDS)


def emitted_signal_records() -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    jobs = read_jobs()
    paths = sorted((REPO_ROOT / "research_control" / "tasks").glob("*/jobs/completions/*.yaml"))
    paths.extend(sorted((REPO_ROOT / "research_control" / "handoffs").glob("handoff-*.yaml")))

    for path in paths:
        relative = path.relative_to(REPO_ROOT).as_posix()
        try:
            data = load_yaml(path)
        except StrictYamlError as exc:
            errors.append(f"{relative}: {exc}")
            continue
        signals = data.get("project_improvement_signals", [])
        if signals == "" or signals is None:
            continue
        if not isinstance(signals, list):
            errors.append(f"{relative}: project_improvement_signals must be a list")
            continue
        job_id = _text(data.get("job_id"))
        job = jobs.get(job_id, {})
        source_role_id = _text(data.get("source_role_id")) or job.get("role_id", "")
        for index, signal in enumerate(signals, start=1):
            if _is_blank_signal(signal):
                continue
            if not isinstance(signal, dict):
                errors.append(f"{relative}: project_improvement_signals[{index}] must be a map")
                continue
            records.append(
                {
                    "source_path": relative,
                    "index": index,
                    "source_task_id": _text(data.get("task_id")) or job.get("task_id", ""),
                    "source_job_id": job_id,
                    "source_role_id": source_role_id,
                    "signal": signal,
                }
            )
    return records, errors


def signal_matches(row: dict[str, str], emitted: dict[str, Any]) -> bool:
    signal = emitted["signal"]
    signal_id = _text(signal.get("signal_id"))
    if signal_id and row.get("signal_id") != signal_id:
        return False

    required = {
        "source_task_id": emitted.get("source_task_id", ""),
        "source_job_id": emitted.get("source_job_id", ""),
        "source_role_id": emitted.get("source_role_id", ""),
        "signal_type": _text(signal.get("signal_type")),
        "severity": _text(signal.get("severity")),
    }
    for field_name, expected in required.items():
        if expected and row.get(field_name) != expected:
            return False
    for field_name in ["recommended_skill", "recommended_role"]:
        expected = _text(signal.get(field_name))
        if expected and row.get(field_name) != expected:
            return False

    evidence_path = _text(signal.get("evidence_path"))
    evidence = _text(signal.get("evidence"))
    if evidence_path:
        return row.get("evidence_path") == evidence_path
    if evidence:
        return row.get("notes") == evidence
    return True


def is_completion_evidence_path(relative_path: str) -> bool:
    path = Path(relative_path)
    return (
        not path.is_absolute()
        and path.suffix == ".yaml"
        and len(path.parts) >= 6
        and path.parts[0] == "research_control"
        and path.parts[1] == "tasks"
        and path.parts[3] == "jobs"
        and path.parts[4] == "completions"
    )


def is_director_decision_evidence_path(relative_path: str) -> bool:
    path = Path(relative_path)
    return (
        not path.is_absolute()
        and path.suffix == ".md"
        and len(path.parts) >= 4
        and path.parts[0] == "research_control"
        and path.parts[1] == "tasks"
        and path.name.startswith("DDR-")
    )


def completion_evidence_errors(row: dict[str, str]) -> list[str]:
    signal_id = row.get("signal_id", "")
    evidence_path = row.get("resolution_evidence_path", "")
    errors: list[str] = []
    if not is_completion_evidence_path(evidence_path):
        return [
            f"{signal_id}: {row.get('status')} signal resolution_evidence_path must point to a completion YAML with validation_status PASS"
        ]
    try:
        data = load_yaml(REPO_ROOT / evidence_path)
    except StrictYamlError as exc:
        return [f"{signal_id}: resolution_evidence_path completion YAML is invalid: {exc}"]
    resolved_by_job_id = row.get("resolved_by_job_id", "")
    if _text(data.get("job_id")) != resolved_by_job_id:
        errors.append(f"{signal_id}: resolution_evidence_path job_id must match resolved_by_job_id")
    if _text(data.get("status")) != "completed":
        errors.append(f"{signal_id}: resolution_evidence_path completion status must be completed")
    if _text(data.get("validation_status")) != "PASS":
        errors.append(f"{signal_id}: resolution_evidence_path completion validation_status must be PASS")
    return errors


def rejected_decision_evidence_errors(row: dict[str, str]) -> list[str]:
    signal_id = row.get("signal_id", "")
    evidence_path = row.get("resolution_evidence_path", "")
    if not is_director_decision_evidence_path(evidence_path):
        return [
            f"{signal_id}: rejected signal resolution_evidence_path must point to a PASS completion YAML or Director decision record"
        ]
    text = (REPO_ROOT / evidence_path).read_text(encoding="utf-8")
    lowered = text.lower()
    errors: list[str] = []
    if signal_id and signal_id not in text:
        errors.append(f"{signal_id}: rejection Director decision must name the signal_id")
    if "reject" not in lowered:
        errors.append(f"{signal_id}: rejection Director decision must explain rejection")
    return errors


def completion_signal_ids(completion: dict[str, Any]) -> set[str]:
    signals = completion.get("resolved_project_improvement_signals", [])
    if not isinstance(signals, list):
        return set()
    signal_ids: set[str] = set()
    for signal in signals:
        if isinstance(signal, str):
            signal_id = _text(signal)
        elif isinstance(signal, dict):
            signal_id = _text(signal.get("signal_id"))
        else:
            signal_id = ""
        if signal_id:
            signal_ids.add(signal_id)
    return signal_ids


def shared_resolution_errors(rows: list[dict[str, str]], jobs: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    terminal_by_job: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row.get("status") in RESOLUTION_STATUSES and row.get("resolved_by_job_id"):
            terminal_by_job.setdefault(row["resolved_by_job_id"], []).append(row)

    for job_id, resolved_rows in sorted(terminal_by_job.items()):
        if len(resolved_rows) < 2:
            continue
        signal_ids = sorted(row.get("signal_id", "") for row in resolved_rows if row.get("signal_id"))
        job_row = jobs.get(job_id, {})
        job_path_text = job_row.get("job_path", "")
        if not job_path_text:
            errors.append(
                f"{job_id}: AgentJob resolving multiple project-improvement signals must declare job_path"
            )
            continue
        job_path = REPO_ROOT / job_path_text
        if not job_path.exists():
            errors.append(f"{job_id}: AgentJob resolving multiple signals is missing {job_path_text}")
            continue
        try:
            job = load_yaml(job_path)
        except StrictYamlError as exc:
            errors.append(f"{job_id}: AgentJob YAML is invalid: {exc}")
            continue
        objective = _text(job.get("objective"))
        if not objective:
            errors.append(
                f"{job_id}: AgentJob resolving multiple signals must include an objective naming each signal_id"
            )
        else:
            for signal_id in signal_ids:
                if signal_id not in objective:
                    errors.append(f"{job_id}: AgentJob objective missing resolved signal_id {signal_id}")

        completion_path_text = job_row.get("completion_path", "")
        if not completion_path_text:
            errors.append(
                f"{job_id}: AgentJob resolving multiple signals must declare completion_path"
            )
            continue
        for row in resolved_rows:
            if row.get("resolution_evidence_path") != completion_path_text:
                errors.append(
                    f"{job_id}: shared signal closure row {row.get('signal_id', '')} resolution_evidence_path must match AGENT_JOB_REGISTRY.csv completion_path"
                )
        completion_path = REPO_ROOT / completion_path_text
        if not completion_path.exists():
            errors.append(
                f"{job_id}: AgentJob resolving multiple signals is missing completion {completion_path_text}"
            )
            continue
        try:
            completion = load_yaml(completion_path)
        except StrictYamlError as exc:
            errors.append(f"{job_id}: completion YAML is invalid: {exc}")
            continue
        if _text(completion.get("job_id")) != job_id:
            errors.append(f"{job_id}: completion job_id mismatch")
        if _text(completion.get("status")) != "completed":
            errors.append(f"{job_id}: completion status must be completed")
        if _text(completion.get("validation_status")) != "PASS":
            errors.append(f"{job_id}: completion validation_status must be PASS")

        completion_ids = completion_signal_ids(completion)
        if not completion_ids:
            errors.append(
                f"{job_id}: completion resolving multiple signals must list resolved_project_improvement_signals"
            )
        else:
            for signal_id in signal_ids:
                if signal_id not in completion_ids:
                    errors.append(
                        f"{job_id}: completion resolved_project_improvement_signals missing {signal_id}"
                    )
        if not _text(completion.get("coherent_resolution_summary")):
            errors.append(
                f"{job_id}: completion resolving multiple signals must include coherent_resolution_summary"
            )
    return errors


def resolution_evidence_errors(row: dict[str, str]) -> list[str]:
    status = row.get("status", "")
    if status in SUCCESS_RESOLUTION_STATUSES:
        return completion_evidence_errors(row)
    if status == "rejected":
        completion_errors = completion_evidence_errors(row)
        if not completion_errors:
            return []
        return rejected_decision_evidence_errors(row)
    return []


def validate_signal_registration() -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    signal_type_rows = read_signal_types()
    allowed_signal_types = signal_type_names(REPO_ROOT)
    rows = read_signals()
    jobs = read_jobs()
    seen_signal_types: set[str] = set()
    signal_ids: set[str] = set()

    if not signal_type_registry_path(REPO_ROOT).exists():
        errors.append(f"{SIGNAL_TYPE_REGISTRY_NAME}: missing canonical signal-type registry")
    for row_number, row in enumerate(signal_type_rows, start=2):
        missing_columns = [column for column in SIGNAL_TYPE_COLUMNS if column not in row]
        if missing_columns:
            errors.append(
                f"{SIGNAL_TYPE_REGISTRY_NAME}:{row_number}: missing columns {', '.join(missing_columns)}"
            )
            continue
        signal_type = row.get("signal_type", "").strip()
        if not signal_type:
            errors.append(f"{SIGNAL_TYPE_REGISTRY_NAME}:{row_number}: missing signal_type")
        elif signal_type in seen_signal_types:
            errors.append(f"{SIGNAL_TYPE_REGISTRY_NAME}:{row_number}: duplicate signal_type {signal_type}")
        seen_signal_types.add(signal_type)
        if row.get("status") not in ALLOWED_SIGNAL_TYPE_STATUSES:
            errors.append(f"{SIGNAL_TYPE_REGISTRY_NAME}:{row_number}: status must be active or deprecated")

    for row_number, row in enumerate(rows, start=2):
        missing_columns = [column for column in SIGNAL_REGISTRY_COLUMNS if column not in row]
        if missing_columns:
            errors.append(
                f"{SIGNAL_REGISTRY_NAME}:{row_number}: missing columns {', '.join(missing_columns)}"
            )
        signal_id = row.get("signal_id", "")
        if not signal_id:
            errors.append(f"{SIGNAL_REGISTRY_NAME}:{row_number}: missing signal_id")
        elif signal_id in signal_ids:
            errors.append(f"{SIGNAL_REGISTRY_NAME}:{row_number}: duplicate signal_id {signal_id}")
        signal_ids.add(signal_id)
        if row.get("severity") not in ALLOWED_SEVERITIES:
            errors.append(f"{signal_id}: severity must be critical high medium or low")
        if row.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{signal_id}: status must be open pending active resolved completed closed or rejected")
        if row.get("signal_type") not in allowed_signal_types:
            errors.append(f"{signal_id}: signal_type is not registered in {SIGNAL_TYPE_REGISTRY_NAME}")
        source_job_id = row.get("source_job_id", "")
        if source_job_id and source_job_id not in jobs:
            errors.append(f"{signal_id}: source_job_id is not registered")
        resolved_by_job_id = row.get("resolved_by_job_id", "")
        if row.get("status") in RESOLUTION_STATUSES:
            missing_resolution = [
                field_name
                for field_name in ["resolved_by_job_id", "resolution_evidence_path", "resolved_at"]
                if not row.get(field_name)
            ]
            if missing_resolution:
                errors.append(
                    f"{signal_id}: {row.get('status')} signal missing resolution evidence fields {', '.join(missing_resolution)}"
                )
        if resolved_by_job_id and resolved_by_job_id not in jobs:
            errors.append(f"{signal_id}: resolved_by_job_id is not registered")
        evidence_path = row.get("evidence_path", "")
        if evidence_path:
            evidence = Path(evidence_path)
            if evidence.is_absolute() or any(part == ".." for part in evidence.parts):
                errors.append(f"{signal_id}: evidence_path must be a relative repository path")
            elif not (REPO_ROOT / evidence_path).exists():
                warnings.append(f"{signal_id}: evidence_path does not exist")
        resolution_evidence_path = row.get("resolution_evidence_path", "")
        if resolution_evidence_path:
            resolution_evidence = Path(resolution_evidence_path)
            if resolution_evidence.is_absolute() or any(part == ".." for part in resolution_evidence.parts):
                errors.append(f"{signal_id}: resolution_evidence_path must be a relative repository path")
            elif not (REPO_ROOT / resolution_evidence_path).exists():
                if row.get("status") in RESOLUTION_STATUSES:
                    errors.append(f"{signal_id}: resolution_evidence_path does not exist")
                else:
                    warnings.append(f"{signal_id}: resolution_evidence_path does not exist")
        if (
            row.get("status") in RESOLUTION_STATUSES
            and row.get("resolved_by_job_id")
            and row.get("resolution_evidence_path")
            and (REPO_ROOT / row.get("resolution_evidence_path", "")).exists()
        ):
            errors.extend(resolution_evidence_errors(row))

    emitted, parse_errors = emitted_signal_records()
    errors.extend(shared_resolution_errors(rows, jobs))
    errors.extend(parse_errors)
    for record in emitted:
        signal = record["signal"]
        missing = [
            field_name
            for field_name in ["signal_type", "severity"]
            if not _text(signal.get(field_name))
        ]
        if missing:
            errors.append(
                f"{record['source_path']}: project_improvement_signals[{record['index']}] missing {', '.join(missing)}"
            )
            continue
        if _text(signal.get("signal_type")) not in allowed_signal_types:
            errors.append(
                f"{record['source_path']}: project_improvement_signals[{record['index']}] signal_type is not registered in {SIGNAL_TYPE_REGISTRY_NAME}"
            )
            continue
        if not any(signal_matches(row, record) for row in rows):
            errors.append(
                f"{record['source_path']}: project_improvement_signals[{record['index']}] is not registered in {SIGNAL_REGISTRY_NAME}"
            )

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "registered_signal_type_count": len(signal_type_rows),
        "registered_signal_count": len(rows),
        "emitted_signal_count": len(emitted),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON. This is the default.")
    parser.add_argument("--status", help="Filter by status.")
    parser.add_argument("--type", dest="signal_type", help="Filter by signal type.")
    parser.add_argument(
        "--validate-emitted",
        action="store_true",
        help="Fail if any emitted project_improvement_signals entry is not registered.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.validate_emitted:
        report = validate_signal_registration()
        if args.json:
            print(json.dumps(report, indent=2))
        elif report["status"] == "PASS":
            print("Project-improvement signal validation passed.")
        else:
            print("Project-improvement signal validation failed:")
            for error in report["errors"]:
                print(f"- {error}")
        return 0 if report["status"] == "PASS" else 1

    print(json.dumps(collect_signals(status=args.status, signal_type=args.signal_type), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
