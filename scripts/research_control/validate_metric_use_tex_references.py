#!/usr/bin/env python3
"""Validate metric-use ledger coverage for configured TeX references.

This validator is support-only project-control tooling. It scans configured
TeX artifacts for high-risk metric-adjacent references and checks that each
detected class is covered by ``registries/METRIC_USE_LEDGER.csv`` or by an
explicit task-local no-use justification comment.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LEDGER = "registries/METRIC_USE_LEDGER.csv"
VALIDATOR_ID = "metric_use_tex_reference_validator"
VALIDATOR_VERSION = "0.1.0"

LEDGER_HEADER = [
    "use_id",
    "task_id",
    "artifact_path",
    "object_used",
    "use_category",
    "declared_scope",
    "allowed_use",
    "forbidden_interpretations",
    "no_target_guard_path",
    "audit_status",
    "stress_status",
    "created_at",
    "notes",
]

LEDGER_EVIDENCE_FIELDS = [
    "object_used",
    "use_category",
    "declared_scope",
    "allowed_use",
    "notes",
]


@dataclass(frozen=True)
class HighRiskClass:
    class_id: str
    title: str
    patterns: tuple[re.Pattern[str], ...]
    ledger_terms: tuple[str, ...]
    justification_terms: tuple[str, ...]


def compiled(patterns: list[str]) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)


HIGH_RISK_CLASSES = [
    HighRiskClass(
        class_id="g_eff",
        title="g_eff reference",
        patterns=compiled(
            [
                r"\bg[_-]?eff\b",
                r"\bg\s*_\s*\{\\mathrm\{eff\}\}",
                r"\bg\s*_\s*\{eff\}",
            ]
        ),
        ledger_terms=("g_eff", "g eff", "g_{\\mathrm{eff}}"),
        justification_terms=("g_eff", "g eff", "all"),
    ),
    HighRiskClass(
        class_id="metricdata_e",
        title="MetricData(E) reference",
        patterns=compiled([r"\bMetricData\s*\(\s*E\s*\)", r"\bMetricFormAssign\b"]),
        ledger_terms=("metricdata", "metricform", "metric form"),
        justification_terms=("metricdata", "metric data", "metricform", "all"),
    ),
    HighRiskClass(
        class_id="proper_time",
        title="proper-time reference",
        patterns=compiled([r"\bproper[-\s]+time\b"]),
        ledger_terms=("proper_time", "proper time", "proper-time"),
        justification_terms=("proper_time", "proper time", "proper-time", "all"),
    ),
    HighRiskClass(
        class_id="detector_calibration",
        title="detector-calibration reference",
        patterns=compiled([r"\bdetector\b", r"\bcalibration\b", r"\bcalibrat(?:e|es|ed|ion)\b"]),
        ledger_terms=("detector", "calibration", "calibrat"),
        justification_terms=("detector", "calibration", "calibrat", "all"),
    ),
    HighRiskClass(
        class_id="stress_energy",
        title="stress-energy reference",
        patterns=compiled([r"\bstress[-\s]+energy\b", r"\bstress[-\s]+tensor\b"]),
        ledger_terms=("stress_energy", "stress energy", "stress-energy", "stress tensor"),
        justification_terms=("stress_energy", "stress energy", "stress-energy", "all"),
    ),
    HighRiskClass(
        class_id="matter_action",
        title="matter-action reference",
        patterns=compiled([r"\bmatter[-\s]+action\b", r"\bmatter[-\s]+Lagrangian\b", r"\bLagrangian\b"]),
        ledger_terms=("matter_action", "matter action", "matter-action", "lagrangian"),
        justification_terms=("matter_action", "matter action", "matter-action", "lagrangian", "all"),
    ),
]


def repo_relative(path: Path, repo_root: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def resolve_repo_path(path_text: str, repo_root: Path) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return repo_root / path


def strip_tex_comments_line(line: str) -> str:
    escaped = False
    for index, char in enumerate(line):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "%" and not escaped:
            return line[:index]
        escaped = False
    return line


def is_tex_declaration_line(line: str) -> bool:
    return bool(
        re.match(
            r"^\s*\\(?:newcommand|renewcommand|providecommand|def|DeclareMathOperator)\b",
            line,
        )
    )


def read_ledger(ledger_path: Path, repo_root: Path) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    if not ledger_path.exists():
        return [], [f"missing metric-use ledger: {repo_relative(ledger_path, repo_root)}"]
    with ledger_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != LEDGER_HEADER:
            errors.append(f"unexpected metric-use ledger header: {reader.fieldnames}")
        rows = list(reader)
    return rows, errors


def configured_tex_paths(
    rows: list[dict[str, str]], repo_root: Path, explicit_paths: list[str] | None
) -> list[Path]:
    if explicit_paths:
        return [resolve_repo_path(path, repo_root) for path in explicit_paths]

    seen: set[str] = set()
    paths: list[Path] = []
    for row in rows:
        artifact_path = row.get("artifact_path", "").strip()
        if not artifact_path.endswith(".tex") or artifact_path in seen:
            continue
        seen.add(artifact_path)
        paths.append(resolve_repo_path(artifact_path, repo_root))
    return paths


def ledger_rows_by_path(rows: list[dict[str, str]], repo_root: Path) -> dict[str, list[dict[str, str]]]:
    by_path: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        artifact_path = row.get("artifact_path", "").strip()
        if not artifact_path:
            continue
        normalized = repo_relative(resolve_repo_path(artifact_path, repo_root), repo_root)
        by_path.setdefault(normalized, []).append(row)
    return by_path


def row_text(row: dict[str, str]) -> str:
    return " ".join(row.get(field, "") for field in LEDGER_EVIDENCE_FIELDS).lower()


def class_covered_by_ledger(rows: list[dict[str, str]], risk_class: HighRiskClass) -> bool:
    for row in rows:
        evidence = row_text(row)
        if any(term.lower() in evidence for term in risk_class.ledger_terms):
            return True
    return False


def no_use_justified(raw_lines: list[str], risk_class: HighRiskClass) -> bool:
    marker = re.compile(r"metric-use-ledger\s*:\s*no-use-justification(?::|\s|-)?(?P<text>.*)", re.IGNORECASE)
    for line in raw_lines:
        match = marker.search(line)
        if not match:
            continue
        text = match.group("text").strip().lower()
        if not text:
            return True
        if any(term.lower() in text for term in risk_class.justification_terms):
            return True
    return False


def scan_text(lines: list[str]) -> dict[str, list[int]]:
    detected: dict[str, list[int]] = {}
    for line_number, raw_line in enumerate(lines, start=1):
        line = strip_tex_comments_line(raw_line)
        if is_tex_declaration_line(line):
            continue
        for risk_class in HIGH_RISK_CLASSES:
            if any(pattern.search(line) for pattern in risk_class.patterns):
                detected.setdefault(risk_class.class_id, []).append(line_number)
    return detected


def scan_configured_path(
    path: Path,
    repo_root: Path,
    ledger_rows: list[dict[str, str]],
) -> dict[str, Any]:
    relative_path = repo_relative(path, repo_root)
    if not path.exists():
        return {
            "path": relative_path,
            "exists": False,
            "status": "FAIL",
            "detected_classes": [],
            "covered_classes": [],
            "no_use_justified_classes": [],
            "findings": [
                {
                    "path": relative_path,
                    "class_id": "missing_configured_tex_artifact",
                    "line_numbers": [],
                    "message": "Configured TeX artifact does not exist.",
                }
            ],
        }

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    detected_by_class = scan_text(raw_lines)
    findings: list[dict[str, Any]] = []
    covered_classes: list[str] = []
    justified_classes: list[str] = []

    class_map = {risk_class.class_id: risk_class for risk_class in HIGH_RISK_CLASSES}
    for class_id, line_numbers in sorted(detected_by_class.items()):
        risk_class = class_map[class_id]
        if class_covered_by_ledger(ledger_rows, risk_class):
            covered_classes.append(class_id)
            continue
        if no_use_justified(raw_lines, risk_class):
            justified_classes.append(class_id)
            continue
        finding_type = "unledgered_reference" if not ledger_rows else "missing_class_ledger_coverage"
        findings.append(
            {
                "path": relative_path,
                "class_id": class_id,
                "title": risk_class.title,
                "finding_type": finding_type,
                "line_numbers": line_numbers,
                "message": (
                    f"{risk_class.title} detected without a matching metric-use ledger row "
                    "or explicit metric-use-ledger no-use justification."
                ),
            }
        )

    status = "PASS" if not findings else "FAIL"
    return {
        "path": relative_path,
        "exists": True,
        "status": status,
        "detected_classes": sorted(detected_by_class),
        "covered_classes": sorted(covered_classes),
        "no_use_justified_classes": sorted(justified_classes),
        "ledger_row_count": len(ledger_rows),
        "findings": findings,
    }


def build_report(
    repo_root: Path,
    ledger_path: Path,
    explicit_paths: list[str] | None = None,
    failure_mode: str = "hard-fail",
) -> dict[str, Any]:
    rows, ledger_errors = read_ledger(ledger_path, repo_root)
    by_path = ledger_rows_by_path(rows, repo_root)
    configured = configured_tex_paths(rows, repo_root, explicit_paths)

    path_reports: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for path in configured:
        relative_path = repo_relative(path, repo_root)
        path_report = scan_configured_path(path, repo_root, by_path.get(relative_path, []))
        path_reports.append(path_report)
        findings.extend(path_report["findings"])

    for error in ledger_errors:
        findings.append(
            {
                "path": repo_relative(ledger_path, repo_root),
                "class_id": "metric_use_ledger_schema_error",
                "finding_type": "ledger_error",
                "line_numbers": [],
                "message": error,
            }
        )

    if findings:
        status = "WARN" if failure_mode == "warn" else "FAIL"
    else:
        status = "PASS"

    return {
        "schema_id": "metric_use_tex_reference_validation_report_v1",
        "validator_id": VALIDATOR_ID,
        "validator_version": VALIDATOR_VERSION,
        "status": status,
        "failure_mode": failure_mode,
        "exit_policy": {
            "PASS": 0,
            "WARN": 0,
            "FAIL": 1,
        },
        "ledger_path": repo_relative(ledger_path, repo_root),
        "configured_scope": "explicit_paths" if explicit_paths else "metric_use_ledger_tex_artifacts",
        "configured_path_count": len(configured),
        "ledger_row_count": len(rows),
        "high_risk_classes": [risk_class.class_id for risk_class in HIGH_RISK_CLASSES],
        "finding_count": len(findings),
        "findings": findings,
        "path_reports": path_reports,
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "source_law_adopted": False,
        "ledger_changed": False,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    parser.add_argument("--ledger", default=DEFAULT_LEDGER)
    parser.add_argument("--paths", nargs="*", help="Explicit TeX paths to scan.")
    parser.add_argument(
        "--failure-mode",
        choices=["hard-fail", "warn"],
        default="hard-fail",
        help="Return nonzero for findings in hard-fail mode; return zero with WARN in warn mode.",
    )
    parser.add_argument("--json", action="store_true", help="Print the report as JSON.")
    parser.add_argument("--json-output", help="Write the report JSON to this path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(args.repo_root).resolve()
    ledger_path = resolve_repo_path(args.ledger, repo_root)
    report = build_report(
        repo_root=repo_root,
        ledger_path=ledger_path,
        explicit_paths=args.paths,
        failure_mode=args.failure_mode,
    )

    if args.json_output:
        output_path = resolve_repo_path(args.json_output, repo_root)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json or not args.json_output:
        print(json.dumps(report, indent=2, sort_keys=True))

    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
