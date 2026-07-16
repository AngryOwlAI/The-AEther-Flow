"""Deterministic bounded output and atomic full receipts for validators."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import tempfile
from typing import TextIO

from scripts.validation.models import ValidationFinding, ValidationRun


DEFAULT_MAX_FINDINGS = 10
DEFAULT_PASS_BUDGET_BYTES = 2 * 1024
DEFAULT_NONPASS_BUDGET_BYTES = 8 * 1024
DEFAULT_RECEIPT_ROOT = Path(".local/validation-receipts")
_SAFE_COMPONENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


@dataclass(frozen=True, slots=True)
class ReportingOptions:
    """One selected console representation."""

    mode: str = "summary"
    max_findings: int = DEFAULT_MAX_FINDINGS

    def __post_init__(self) -> None:
        if self.mode not in {"summary", "json-summary", "full-json", "receipt", "quiet"}:
            raise ValueError(f"unsupported reporting mode: {self.mode}")
        if not isinstance(self.max_findings, int) or not 0 <= self.max_findings <= 10:
            raise ValueError("max_findings must be an integer from 0 through 10")


def add_reporting_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the common mutually exclusive reporter flags to ``parser``."""

    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--summary", action="store_true", help="emit the bounded text summary")
    modes.add_argument("--json-summary", action="store_true", help="emit bounded summary JSON")
    modes.add_argument("--full-json", action="store_true", help="emit the complete receipt JSON")
    modes.add_argument("--receipt", action="store_true", help="emit only the full-receipt path")
    modes.add_argument("--quiet", action="store_true", help="write the receipt without console output")


def options_from_namespace(namespace: argparse.Namespace) -> ReportingOptions:
    for attribute, mode in (
        ("json_summary", "json-summary"),
        ("full_json", "full-json"),
        ("receipt", "receipt"),
        ("quiet", "quiet"),
        ("summary", "summary"),
    ):
        if getattr(namespace, attribute, False):
            return ReportingOptions(mode=mode)
    return ReportingOptions()


def _path_component(value: str, name: str) -> str:
    normalized = value.replace(":", "-")
    if not _SAFE_COMPONENT.fullmatch(normalized):
        raise ValueError(f"{name} is not safe for a receipt path")
    return normalized


def receipt_path(run: ValidationRun, root: Path = DEFAULT_RECEIPT_ROOT) -> Path:
    tree = _path_component(run.tree_hash, "tree_hash")
    run_id = _path_component(run.run_id, "run_id")
    return Path(root) / tree / run_id / "full.json"


def _atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_full_receipt(run: ValidationRun, root: Path = DEFAULT_RECEIPT_ROOT) -> Path:
    """Atomically preserve all findings and return the local receipt path."""

    path = receipt_path(run, root)
    _atomic_write_json(path, run.to_full_receipt())
    return path


def _flatten_findings(run: ValidationRun) -> list[tuple[str, ValidationFinding]]:
    return [
        (gate.gate_id, finding)
        for gate in run.sorted_gate_results
        for finding in gate.sorted_findings
    ]


def _single_line(value: str, limit: int = 240) -> str:
    collapsed = " ".join(value.split())
    encoded = collapsed.encode("utf-8")
    if len(encoded) <= limit:
        return collapsed
    shortened = encoded[: max(0, limit - 3)]
    while True:
        try:
            return shortened.decode("utf-8") + "..."
        except UnicodeDecodeError:
            shortened = shortened[:-1]


def summary_dict(
    run: ValidationRun,
    receipt: Path,
    *,
    max_findings: int = DEFAULT_MAX_FINDINGS,
) -> dict[str, object]:
    if not 0 <= max_findings <= 10:
        raise ValueError("max_findings must be from 0 through 10")
    all_findings = _flatten_findings(run)
    shown = all_findings[:max_findings]
    groups = Counter(finding.code for _, finding in all_findings if finding.level == "WARN")
    shown_group_ids = sorted(groups)[:max_findings]
    return {
        "schema_id": "validation_console_summary_v1",
        "run_id": run.run_id,
        "status": run.status,
        "exit_code": run.exit_code,
        "counts": run.counts,
        "warning_groups": [
            {"stable_id": stable_id, "count": groups[stable_id]}
            for stable_id in shown_group_ids
        ],
        "more_warning_groups": max(0, len(groups) - len(shown_group_ids)),
        "shown_findings": [
            {
                "gate_id": gate_id,
                "finding_id": finding.finding_id,
                "level": finding.level,
                "code": finding.code,
                "message": _single_line(finding.message),
            }
            for gate_id, finding in shown
        ],
        "more_findings": max(0, len(all_findings) - len(shown)),
        "full_receipt": str(receipt),
        "authority": "operational_validation_only",
    }


def render_summary(
    run: ValidationRun,
    receipt: Path,
    *,
    max_findings: int = DEFAULT_MAX_FINDINGS,
) -> str:
    """Render one-line PASS or bounded deterministic non-PASS text."""

    summary = summary_dict(run, receipt, max_findings=max_findings)
    counts = summary["counts"]
    assert isinstance(counts, dict)
    if run.status == "PASS":
        return (
            f"PASS gates={counts['gate_count']} findings={counts['finding_count']} "
            f"receipt={receipt}\n"
        )
    lines = [
        (
            f"{run.status} gates={counts['gate_count']} errors={counts['error_count']} "
            f"warnings={counts['warning_count']} findings={counts['finding_count']} "
            f"more_findings={summary['more_findings']} receipt={receipt}"
        )
    ]
    groups = summary["warning_groups"]
    assert isinstance(groups, list)
    for group in groups:
        lines.append(f"WARN_GROUP {group['stable_id']} count={group['count']}")
    if summary["more_warning_groups"]:
        lines.append(f"MORE_WARNING_GROUPS count={summary['more_warning_groups']}")
    findings = summary["shown_findings"]
    assert isinstance(findings, list)
    for finding in findings:
        lines.append(
            f"{finding['level']} {finding['gate_id']} {finding['finding_id']} "
            f"{finding['code']}: {finding['message']}"
        )
    return "\n".join(lines) + "\n"


def _json_line(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def render_output(run: ValidationRun, receipt: Path, options: ReportingOptions) -> str:
    if options.mode == "quiet":
        return ""
    if options.mode == "receipt":
        return f"{receipt}\n"
    if options.mode == "json-summary":
        return _json_line(summary_dict(run, receipt, max_findings=options.max_findings))
    if options.mode == "full-json":
        return _json_line(run.to_full_receipt())
    return render_summary(run, receipt, max_findings=options.max_findings)


def emit_report(
    run: ValidationRun,
    *,
    options: ReportingOptions | None = None,
    receipt_root: Path = DEFAULT_RECEIPT_ROOT,
    stream: TextIO,
) -> int:
    """Write the full receipt, emit the selected representation, and return an exit code.

    The represented validator exit code is preserved.  A receipt-write failure
    returns 2 because a requested evidence write must not fail silently.
    """

    selected = options or ReportingOptions()
    try:
        path = write_full_receipt(run, receipt_root)
    except (OSError, ValueError) as error:
        message = _single_line(str(error), limit=256)
        stream.write(f"BLOCKED_CONFIGURATION receipt_write_failed: {message}\n")
        return 2
    stream.write(render_output(run, path, selected))
    return run.exit_code


def console_bytes(output: str) -> int:
    return len(output.encode("utf-8"))
