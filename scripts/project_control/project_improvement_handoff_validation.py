#!/usr/bin/env python3
"""Validate project-improvement handoff sidecar schema and parity."""

from __future__ import annotations

import csv
import fnmatch
import re
import sys
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from project_signal_types import signal_type_names  # noqa: E402
from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


PROJECT_IMPROVEMENT_HANDOFF_DIR = Path("research_control/project_improvement_handoffs")
PROJECT_IMPROVEMENT_HANDOFF_REQUIRED_AFTER = "2026-06-22T04:00:00Z"
SIGNAL_REGISTRY_NAME = "PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
SIGNAL_REGISTRY = Path("registries") / SIGNAL_REGISTRY_NAME
HANDOFF_ID_RE = re.compile(r"improve-project-handoff_\d{8}_\d{3}")
NORMAL_HANDOFF_RE = re.compile(r"handoff-\d{4}\.yaml")
TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")

OPEN_SIGNAL_STATUSES = {"open", "pending", "active"}
SUCCESS_TERMINAL_SIGNAL_STATUSES = {"resolved", "completed", "closed"}
SIDE_CAR_STATUSES = {"open", "active", "resolved", "closed", "rejected", "superseded"}
SIDE_CAR_SOURCE_KINDS = {
    "research_completion_and_handoff",
    "completion_only",
    "handoff_only",
    "backfilled_from_immutable_source",
}
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
PROTECTED_WRITE_HINT_PREFIXES = (
    "ontology/",
    "legacy_ontology/",
    "manuscripts/",
    "tex/",
    "html/",
    "wiki/",
    "github-facing/",
    "markdown/html-explainer-specs/",
    "markdown/publication-briefs/",
)
PROJECT_BOUNDARY_TRUE_FIELDS = (
    "project_system_only",
)
PROJECT_BOUNDARY_FALSE_FIELDS = (
    "physics_claim_promotion_authorized",
    "canonical_science_source_edits_authorized",
    "generated_derivative_hand_edits_authorized",
    "requires_human_gate",
)
ISSUE_REQUIRED_FIELDS = (
    "signal_id",
    "signal_type",
    "severity",
    "title",
    "description",
    "impact",
    "recommended_skill",
    "recommended_role",
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


def _text(value: Any) -> str:
    return str(value or "").strip()


def _clean_timestamp(value: Any) -> str:
    text = _text(value)
    return text if TIMESTAMP_RE.fullmatch(text) else ""


def timestamp_at_or_after(value: Any, threshold: str = PROJECT_IMPROVEMENT_HANDOFF_REQUIRED_AFTER) -> bool:
    text = _clean_timestamp(value)
    return bool(text and text >= threshold)


def _invalid_relative_path(path_text: str) -> str:
    path = Path(path_text)
    if path.is_absolute():
        return "absolute paths are not allowed"
    if any(part == ".." for part in path.parts):
        return "path traversal is not allowed"
    return ""


def _repo_path(repo_root: Path, path_text: str) -> Path:
    return repo_root / path_text


def _relative(repo_root: Path, path: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _path_matches(path: str, pattern: str) -> bool:
    return path == pattern or fnmatch.fnmatch(path, pattern)


def _allowed_by_patterns(path: str, patterns: list[str]) -> bool:
    return any(_path_matches(path, pattern) for pattern in patterns)


def _is_sidecar_yaml_path(path_text: str) -> bool:
    path = Path(path_text)
    return (
        path.parent == PROJECT_IMPROVEMENT_HANDOFF_DIR
        and path.suffix == ".yaml"
        and HANDOFF_ID_RE.fullmatch(path.stem) is not None
    )


def _is_sidecar_markdown_path(path_text: str) -> bool:
    path = Path(path_text)
    return (
        path.parent == PROJECT_IMPROVEMENT_HANDOFF_DIR
        and path.suffix == ".md"
        and HANDOFF_ID_RE.fullmatch(path.stem) is not None
    )


def _is_signal_source_path(path_text: str) -> bool:
    path = Path(path_text)
    return (
        path.suffix == ".yaml"
        and (
            fnmatch.fnmatch(path_text, "research_control/tasks/*/jobs/completions/*.yaml")
            or fnmatch.fnmatch(path_text, "research_control/handoffs/handoff-*.yaml")
        )
    )


def _read_csv_rows(repo_root: Path, relative_path: Path) -> list[dict[str, str]]:
    path = repo_root / relative_path
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def read_signal_registry(repo_root: Path = REPO_ROOT) -> dict[str, dict[str, str]]:
    return {
        row.get("signal_id", ""): row
        for row in _read_csv_rows(repo_root, SIGNAL_REGISTRY)
        if row.get("signal_id")
    }


def _is_blank_signal(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    return not any(_text(value.get(field)) for field in SIGNAL_FIELDS)


def nonblank_project_improvement_signals(data: dict[str, Any]) -> list[dict[str, Any]]:
    signals = data.get("project_improvement_signals", [])
    if signals in ("", None) or not isinstance(signals, list):
        return []
    return [signal for signal in signals if isinstance(signal, dict) and not _is_blank_signal(signal)]


def _source_timestamp(data: dict[str, Any]) -> str:
    for field_name in ("completed_at", "created_at", "updated_at"):
        timestamp = _clean_timestamp(data.get(field_name))
        if timestamp:
            return timestamp
    return ""


def emitted_signal_source_records(repo_root: Path = REPO_ROOT) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    paths = sorted((repo_root / "research_control" / "tasks").glob("*/jobs/completions/*.yaml"))
    paths.extend(sorted((repo_root / "research_control" / "handoffs").glob("handoff-*.yaml")))
    for path in paths:
        relative = _relative(repo_root, path)
        try:
            data = load_yaml(path)
        except StrictYamlError as exc:
            errors.append(f"{relative}: {exc}")
            continue
        signals = data.get("project_improvement_signals", [])
        if signals in ("", None):
            continue
        if not isinstance(signals, list):
            errors.append(f"{relative}: project_improvement_signals must be a list")
            continue
        nonblank: list[dict[str, Any]] = []
        for index, signal in enumerate(signals, start=1):
            if _is_blank_signal(signal):
                continue
            if not isinstance(signal, dict):
                errors.append(f"{relative}: project_improvement_signals[{index}] must be a map")
                continue
            nonblank.append(signal)
        if nonblank:
            records.append(
                {
                    "source_path": relative,
                    "source_timestamp": _source_timestamp(data),
                    "data": data,
                    "signal_ids": [_text(signal.get("signal_id")) for signal in nonblank if _text(signal.get("signal_id"))],
                }
            )
    return records, errors


def _sidecar_yaml_paths(repo_root: Path) -> list[Path]:
    sidecar_dir = repo_root / PROJECT_IMPROVEMENT_HANDOFF_DIR
    if not sidecar_dir.exists():
        return []
    return sorted(sidecar_dir.glob("improve-project-handoff_*.yaml"))


def read_project_improvement_handoffs(repo_root: Path = REPO_ROOT) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in _sidecar_yaml_paths(repo_root):
        relative = _relative(repo_root, path)
        try:
            data = load_yaml(path)
        except StrictYamlError as exc:
            errors.append(f"{relative}: {exc}")
            continue
        records.append(
            {
                "path": path,
                "relative_path": relative,
                "markdown_path": path.with_suffix(".md"),
                "data": data,
            }
        )
    return records, errors


def _require_map(errors: list[str], owner: str, data: dict[str, Any], field_name: str) -> dict[str, Any]:
    value = data.get(field_name)
    if not isinstance(value, dict):
        errors.append(f"{owner}: {field_name} must be a map")
        return {}
    return value


def _require_list(errors: list[str], owner: str, data: dict[str, Any], field_name: str) -> list[Any]:
    value = data.get(field_name)
    if not isinstance(value, list):
        errors.append(f"{owner}: {field_name} must be a list")
        return []
    return value


def _require_existing_file(
    errors: list[str],
    repo_root: Path,
    owner: str,
    field_label: str,
    path_text: str,
) -> None:
    if not path_text:
        errors.append(f"{owner}: {field_label} is required")
        return
    reason = _invalid_relative_path(path_text)
    if reason:
        errors.append(f"{owner}: {field_label} invalid path {path_text}: {reason}")
        return
    if not _repo_path(repo_root, path_text).is_file():
        errors.append(f"{owner}: {field_label} does not exist: {path_text}")


def _is_project_boundary_true(value: Any) -> bool:
    return value is True


def _is_project_boundary_false(value: Any) -> bool:
    return value is False


def _int_value(value: Any) -> int | None:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _safe_write_hint_errors(owner: str, hints: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(hints, list):
        errors.append(f"{owner}: solution_plan.allowed_write_paths_hint must be a list")
        return errors
    for hint in hints:
        hint_text = _text(hint)
        if not hint_text:
            continue
        reason = _invalid_relative_path(hint_text.replace("**", "x").replace("*", "x"))
        if reason:
            errors.append(f"{owner}: protected write-path hint invalid path {hint_text}: {reason}")
        if hint_text.startswith(PROTECTED_WRITE_HINT_PREFIXES):
            errors.append(f"{owner}: protected write-path hint is not allowed: {hint_text}")
    return errors


def _expected_signal_order(signal_ids: list[str], signal_rows: dict[str, dict[str, str]]) -> list[str]:
    return sorted(
        signal_ids,
        key=lambda signal_id: (
            SEVERITY_ORDER.get(signal_rows.get(signal_id, {}).get("severity", ""), 99),
            signal_rows.get(signal_id, {}).get("created_at", ""),
            signal_id,
        ),
    )


def _signal_ids_from_source_path(repo_root: Path, path_text: str, errors: list[str], owner: str) -> set[str]:
    if not path_text:
        return set()
    path = _repo_path(repo_root, path_text)
    if not path.is_file():
        return set()
    try:
        data = load_yaml(path)
    except StrictYamlError as exc:
        errors.append(f"{owner}: source signal path {path_text} is invalid: {exc}")
        return set()
    return {_text(signal.get("signal_id")) for signal in nonblank_project_improvement_signals(data) if _text(signal.get("signal_id"))}


def _validate_sidecar_record(
    repo_root: Path,
    record: dict[str, Any],
    active_signal_types: set[str],
    signal_rows: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    data = record["data"]
    relative_path = record["relative_path"]
    path = record["path"]
    markdown_path = record["markdown_path"]

    handoff_id = _text(data.get("improvement_handoff_id"))
    if not handoff_id:
        errors.append(f"{relative_path}: missing improvement_handoff_id")
    elif handoff_id != path.stem:
        errors.append(f"{relative_path}: improvement_handoff_id must match filename stem")
    if handoff_id and not HANDOFF_ID_RE.fullmatch(handoff_id):
        errors.append(f"{relative_path}: improvement_handoff_id must match improve-project-handoff_YYYYMMDD_NNN")

    status = _text(data.get("status"))
    if status not in SIDE_CAR_STATUSES:
        errors.append(f"{relative_path}: status must be open active resolved closed rejected or superseded")

    source = _require_map(errors, relative_path, data, "source")
    source_kind = _text(source.get("source_kind"))
    if source_kind not in SIDE_CAR_SOURCE_KINDS:
        errors.append(f"{relative_path}: source.source_kind is unsupported")

    completion_path = _text(source.get("completion_path"))
    handoff_yaml_path = _text(source.get("regular_handoff_yaml_path"))
    handoff_markdown_path = _text(source.get("regular_handoff_markdown_path"))
    if source_kind != "handoff_only":
        _require_existing_file(errors, repo_root, relative_path, "source.completion_path", completion_path)
    if source_kind in {"research_completion_and_handoff", "handoff_only"}:
        _require_existing_file(errors, repo_root, relative_path, "source.regular_handoff_yaml_path", handoff_yaml_path)
        if handoff_yaml_path and not NORMAL_HANDOFF_RE.fullmatch(Path(handoff_yaml_path).name):
            errors.append(f"{relative_path}: source.regular_handoff_yaml_path must point to handoff-####.yaml")
        _require_existing_file(
            errors,
            repo_root,
            relative_path,
            "source.regular_handoff_markdown_path",
            handoff_markdown_path,
        )
    elif handoff_markdown_path:
        _require_existing_file(
            errors,
            repo_root,
            relative_path,
            "source.regular_handoff_markdown_path",
            handoff_markdown_path,
        )

    continuation = _require_map(errors, relative_path, data, "normal_research_continuation")
    if continuation.get("sidecar_does_not_replace_regular_handoff") is not True:
        errors.append(
            f"{relative_path}: normal_research_continuation.sidecar_does_not_replace_regular_handoff must be true"
        )

    boundary = _require_map(errors, relative_path, data, "project_boundary")
    if _text(boundary.get("recommended_skill")) != "improve-project-system":
        errors.append(f"{relative_path}: project_boundary.recommended_skill must be improve-project-system")
    for field_name in PROJECT_BOUNDARY_TRUE_FIELDS:
        if not _is_project_boundary_true(boundary.get(field_name)):
            errors.append(f"{relative_path}: project_boundary.{field_name} must be true")
    for field_name in PROJECT_BOUNDARY_FALSE_FIELDS:
        if not _is_project_boundary_false(boundary.get(field_name)):
            errors.append(f"{relative_path}: project_boundary.{field_name} must be false")

    summary = _require_map(errors, relative_path, data, "signal_summary")
    summary_signal_ids = [_text(signal_id) for signal_id in _require_list(errors, relative_path, summary, "signal_ids") if _text(signal_id)]
    signal_count = _int_value(summary.get("signal_count"))
    if signal_count != len(summary_signal_ids):
        errors.append(f"{relative_path}: signal_summary.signal_count must equal signal_ids length")
    if _text(summary.get("routing_basis")) != "highest_severity_then_created_at_then_signal_id":
        errors.append(
            f"{relative_path}: signal_summary.routing_basis must be highest_severity_then_created_at_then_signal_id"
        )

    issues = _require_list(errors, relative_path, data, "issues")
    issue_signal_ids: list[str] = []
    issue_rows_by_signal_id: dict[str, dict[str, Any]] = {}
    for index, issue in enumerate(issues, start=1):
        if not isinstance(issue, dict):
            errors.append(f"{relative_path}: issues[{index}] must be a map")
            continue
        missing = [field_name for field_name in ISSUE_REQUIRED_FIELDS if not _text(issue.get(field_name))]
        if missing:
            errors.append(f"{relative_path}: issues[{index}] missing {', '.join(missing)}")
        signal_id = _text(issue.get("signal_id"))
        if signal_id:
            issue_signal_ids.append(signal_id)
            issue_rows_by_signal_id[signal_id] = issue
        signal_type = _text(issue.get("signal_type"))
        if signal_type and signal_type not in active_signal_types:
            errors.append(f"{relative_path}: issues[{index}] signal_type is not active")
        severity = _text(issue.get("severity"))
        if severity and severity not in SEVERITY_ORDER:
            errors.append(f"{relative_path}: issues[{index}] severity is unsupported")
        evidence = issue.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{relative_path}: issues[{index}].evidence must be a nonempty list")
        else:
            for evidence_index, evidence_item in enumerate(evidence, start=1):
                if not isinstance(evidence_item, dict):
                    errors.append(f"{relative_path}: issues[{index}].evidence[{evidence_index}] must be a map")
                    continue
                if not _text(evidence_item.get("evidence_path")):
                    errors.append(f"{relative_path}: issues[{index}].evidence[{evidence_index}] missing evidence_path")
                if not _text(evidence_item.get("evidence_summary")):
                    errors.append(f"{relative_path}: issues[{index}].evidence[{evidence_index}] missing evidence_summary")

    if set(summary_signal_ids) != set(issue_signal_ids):
        errors.append(f"{relative_path}: signal_summary.signal_ids must match issue signal_ids")
    if len(issue_signal_ids) != len(set(issue_signal_ids)):
        errors.append(f"{relative_path}: issues must not duplicate signal_id values")
    if source_kind != "backfilled_from_immutable_source" and summary_signal_ids:
        source_signal_ids: set[str] = set()
        for path_text in (completion_path, handoff_yaml_path):
            source_signal_ids.update(_signal_ids_from_source_path(repo_root, path_text, errors, relative_path))
        missing_source_signals = sorted(set(summary_signal_ids) - source_signal_ids)
        if missing_source_signals:
            errors.append(
                f"{relative_path}: sidecar signal_ids must be emitted by the cited completion or regular handoff: {missing_source_signals}"
            )

    for signal_id in sorted(set(summary_signal_ids) | set(issue_signal_ids)):
        row = signal_rows.get(signal_id)
        issue = issue_rows_by_signal_id.get(signal_id, {})
        if not row:
            errors.append(f"{relative_path}: {signal_id} missing {SIGNAL_REGISTRY_NAME} row")
            continue
        for field_name in ("signal_type", "severity", "recommended_skill", "recommended_role"):
            issue_value = _text(issue.get(field_name))
            row_value = _text(row.get(field_name))
            if issue_value and row_value and issue_value != row_value:
                errors.append(f"{relative_path}: {signal_id} {field_name} must match {SIGNAL_REGISTRY_NAME}")

    ordered_signal_ids = _expected_signal_order(summary_signal_ids, signal_rows)
    if ordered_signal_ids:
        selected_signal_id = _text(summary.get("selected_signal_id"))
        if selected_signal_id != ordered_signal_ids[0]:
            errors.append(f"{relative_path}: signal_summary.selected_signal_id does not match routing basis")
        expected_highest = _text(signal_rows.get(ordered_signal_ids[0], {}).get("severity"))
        if _text(summary.get("highest_severity")) != expected_highest:
            errors.append(f"{relative_path}: signal_summary.highest_severity does not match selected signal")

    solution_plan = _require_map(errors, relative_path, data, "solution_plan")
    plan_present = solution_plan.get("present") is True
    plan_status = _text(solution_plan.get("status"))
    if plan_present or plan_status == "ready_to_implement":
        for field_name in ("implementation_role", "objective"):
            if not _text(solution_plan.get(field_name)):
                errors.append(f"{relative_path}: solution_plan.{field_name} is required")
        for field_name in ("required_validators", "plan_steps"):
            value = solution_plan.get(field_name)
            if not isinstance(value, list) or not value:
                errors.append(f"{relative_path}: solution_plan.{field_name} must be a nonempty list")
    if plan_status == "ready_to_implement":
        errors.extend(_safe_write_hint_errors(relative_path, solution_plan.get("allowed_write_paths_hint", [])))

    resolution = _require_map(errors, relative_path, data, "resolution")
    sidecar_terminal = status in {"resolved", "closed", "rejected", "superseded"}
    if sidecar_terminal:
        if status in {"resolved", "closed"}:
            compatible_statuses = SUCCESS_TERMINAL_SIGNAL_STATUSES
        elif status == "rejected":
            compatible_statuses = {"rejected"}
        else:
            compatible_statuses = SUCCESS_TERMINAL_SIGNAL_STATUSES | {"rejected"}
        for signal_id in summary_signal_ids:
            row_status = signal_rows.get(signal_id, {}).get("status", "")
            if row_status in OPEN_SIGNAL_STATUSES:
                errors.append(f"{relative_path}: terminal sidecar cannot include open signal {signal_id}")
            elif row_status and row_status not in compatible_statuses:
                errors.append(f"{relative_path}: {signal_id} status {row_status} is incompatible with sidecar status {status}")
        if status in {"resolved", "closed", "rejected"}:
            for field_name in ("resolved_by_job_id", "resolution_evidence_path", "resolved_at"):
                if not _text(resolution.get(field_name)):
                    errors.append(f"{relative_path}: terminal sidecar resolution.{field_name} is required")

    if not markdown_path.is_file():
        errors.append(f"{relative_path}: missing Markdown mirror")
    else:
        markdown_text = markdown_path.read_text(encoding="utf-8")
        markdown_relative = _relative(repo_root, markdown_path)
        if handoff_id and handoff_id not in markdown_text:
            errors.append(f"{markdown_relative}: Markdown mirror missing improvement_handoff_id")
        for signal_id in summary_signal_ids:
            if signal_id and signal_id not in markdown_text:
                errors.append(f"{markdown_relative}: Markdown mirror missing signal_id {signal_id}")
        for signal_id, issue in issue_rows_by_signal_id.items():
            title = _text(issue.get("title"))
            if title and title not in markdown_text:
                errors.append(f"{markdown_relative}: Markdown mirror missing issue title for {signal_id}")

    return errors


def _source_paths_for_sidecar(data: dict[str, Any]) -> list[str]:
    source = data.get("source", {})
    if not isinstance(source, dict):
        return []
    return [
        path_text
        for path_text in (
            _text(source.get("completion_path")),
            _text(source.get("regular_handoff_yaml_path")),
        )
        if path_text
    ]


def _sidecar_signal_ids(data: dict[str, Any]) -> set[str]:
    summary = data.get("signal_summary", {})
    if not isinstance(summary, dict):
        return set()
    signal_ids = summary.get("signal_ids", [])
    if not isinstance(signal_ids, list):
        return set()
    return {_text(signal_id) for signal_id in signal_ids if _text(signal_id)}


def _sidecar_boundary_is_safe(data: dict[str, Any]) -> bool:
    continuation = data.get("normal_research_continuation", {})
    boundary = data.get("project_boundary", {})
    if not isinstance(continuation, dict) or not isinstance(boundary, dict):
        return False
    return (
        continuation.get("sidecar_does_not_replace_regular_handoff") is True
        and boundary.get("project_system_only") is True
        and boundary.get("physics_claim_promotion_authorized") is False
        and boundary.get("canonical_science_source_edits_authorized") is False
        and boundary.get("generated_derivative_hand_edits_authorized") is False
    )


def _load_yaml_or_none(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        data = load_yaml(path)
    except StrictYamlError:
        return None
    return data if isinstance(data, dict) else None


def conditional_checkpoint_sidecar_paths(
    repo_root: Path,
    candidate_paths: Iterable[str],
    base_allowed_patterns: Iterable[str],
) -> list[str]:
    """Return sidecar paths allowed only by a valid source bridge reference.

    This is intentionally narrower than a directory allowlist. A sidecar YAML
    and Markdown mirror are checkpoint-eligible only when a changed source YAML
    already allowed by the active AgentJob points at that exact sidecar through
    ``project_improvement_bridge`` and the sidecar points back to the source.
    Full sidecar schema validation still runs through the normal validators.
    """

    candidates = {path for path in candidate_paths if path}
    base_allowed = [pattern for pattern in base_allowed_patterns if pattern]
    allowed_sidecars: set[str] = set()

    for source_path in sorted(candidates):
        if not _is_signal_source_path(source_path):
            continue
        if not _allowed_by_patterns(source_path, base_allowed):
            continue
        source = _load_yaml_or_none(repo_root / source_path)
        if not source:
            continue
        signal_ids = {
            _text(signal.get("signal_id"))
            for signal in nonblank_project_improvement_signals(source)
            if _text(signal.get("signal_id"))
        }
        if not signal_ids:
            continue
        bridge = source.get("project_improvement_bridge")
        if not isinstance(bridge, dict):
            continue
        if bridge.get("required") is not True or _text(bridge.get("bridge_status")) != "generated":
            continue
        sidecar_path = _text(bridge.get("improvement_handoff_path"))
        if not sidecar_path or _invalid_relative_path(sidecar_path):
            continue
        if not _is_sidecar_yaml_path(sidecar_path):
            continue
        sidecar = _load_yaml_or_none(repo_root / sidecar_path)
        if not sidecar:
            continue
        if source_path not in _source_paths_for_sidecar(sidecar):
            continue
        if not signal_ids.issubset(_sidecar_signal_ids(sidecar)):
            continue
        if not _sidecar_boundary_is_safe(sidecar):
            continue

        markdown_path = str(Path(sidecar_path).with_suffix(".md"))
        for candidate_sidecar in (sidecar_path, markdown_path):
            if candidate_sidecar in candidates:
                allowed_sidecars.add(candidate_sidecar)

    return sorted(allowed_sidecars)


def _bridge_reference_errors(
    repo_root: Path,
    source_record: dict[str, Any],
    sidecars_by_path: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    source_path = source_record["source_path"]
    signal_ids = set(source_record["signal_ids"])
    if not signal_ids:
        return errors
    if not timestamp_at_or_after(source_record.get("source_timestamp")):
        return errors

    source = source_record["data"]
    bridge = source.get("project_improvement_bridge")
    if not isinstance(bridge, dict):
        errors.append(
            f"{source_path}: nonblank project_improvement_signals after {PROJECT_IMPROVEMENT_HANDOFF_REQUIRED_AFTER} require project_improvement_bridge"
        )
        return errors
    if bridge.get("required") is not True:
        errors.append(f"{source_path}: project_improvement_bridge.required must be true")
    bridge_status = _text(bridge.get("bridge_status"))
    if bridge_status != "generated":
        errors.append(f"{source_path}: project_improvement_bridge.bridge_status must be generated")
    bridge_signal_ids = {_text(signal_id) for signal_id in bridge.get("signal_ids", []) if _text(signal_id)} if isinstance(bridge.get("signal_ids"), list) else set()
    if bridge_signal_ids != signal_ids:
        errors.append(f"{source_path}: project_improvement_bridge.signal_ids must match nonblank project_improvement_signals")
    sidecar_path = _text(bridge.get("improvement_handoff_path"))
    if not sidecar_path:
        errors.append(f"{source_path}: project_improvement_bridge.improvement_handoff_path is required")
        return errors
    reason = _invalid_relative_path(sidecar_path)
    if reason:
        errors.append(f"{source_path}: project_improvement_bridge.improvement_handoff_path invalid path {sidecar_path}: {reason}")
        return errors
    if not sidecar_path.startswith(f"{PROJECT_IMPROVEMENT_HANDOFF_DIR.as_posix()}/"):
        errors.append(f"{source_path}: project_improvement_bridge.improvement_handoff_path must point to project_improvement_handoffs")
    sidecar_record = sidecars_by_path.get(sidecar_path)
    if not sidecar_record:
        errors.append(f"{source_path}: project_improvement_bridge sidecar does not exist: {sidecar_path}")
        return errors
    if source_path not in _source_paths_for_sidecar(sidecar_record["data"]):
        errors.append(f"{source_path}: project_improvement_bridge sidecar does not point back to source")
    sidecar_signal_ids = _sidecar_signal_ids(sidecar_record["data"])
    if not signal_ids.issubset(sidecar_signal_ids):
        errors.append(f"{source_path}: project_improvement_bridge sidecar missing emitted signal_ids")
    sidecar_file = _repo_path(repo_root, sidecar_path)
    if not sidecar_file.is_file():
        errors.append(f"{source_path}: project_improvement_bridge sidecar path is not a file: {sidecar_path}")
    return errors


def validate_project_improvement_handoffs(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    signal_rows = read_signal_registry(repo_root)
    active_signal_types = signal_type_names(repo_root)
    sidecars, sidecar_parse_errors = read_project_improvement_handoffs(repo_root)
    source_records, source_errors = emitted_signal_source_records(repo_root)
    errors.extend(sidecar_parse_errors)
    errors.extend(source_errors)

    for record in sidecars:
        errors.extend(_validate_sidecar_record(repo_root, record, active_signal_types, signal_rows))

    sidecars_by_path = {record["relative_path"]: record for record in sidecars}
    for source_record in source_records:
        errors.extend(_bridge_reference_errors(repo_root, source_record, sidecars_by_path))

    open_sidecars = [
        record
        for record in sidecars
        if _text(record["data"].get("status")) in {"open", "active"}
    ]
    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "improvement_handoff_count": len(sidecars),
        "open_improvement_handoff_count": len(open_sidecars),
        "activation_timestamp": PROJECT_IMPROVEMENT_HANDOFF_REQUIRED_AFTER,
    }
